import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = runpy.run_path(str(ROOT / "scripts/make-pilot-notebook.py"))
ARTIFACT = ROOT / "artifacts/main-track-pilot.ipynb"


class PilotNotebookTests(unittest.TestCase):
    def setUp(self):
        self.notebook = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.cells = {cell["id"]: "".join(cell["source"]) for cell in self.notebook["cells"]}
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data = self.root / "competition"
        self.model = self.root / "model"
        self.wheels = self.root / "wheels"
        for directory in (self.data / "snapshots", self.data / "sample_submission", self.model, self.wheels):
            directory.mkdir(parents=True)
        self.sample = self.data / "sample_submission/agent.yaml"
        self.sample.write_text("name: sample\ninstruction: Base instructions\n", encoding="utf-8")
        (self.model / "config.json").write_text("{}", encoding="utf-8")
        (self.model / "model.safetensors").touch()
        (self.wheels / "swegemma-test.whl").touch()
        self.tasks = [
            dict(instance_id=f"{repo}-{index}", repo=repo, patch="evaluator-only")
            for repo in ["org/Requests", "org/FastAPI", "org/Rich", "org/HTTPX"]
            for index in range(2)
        ]
        (self.data / "tasks.jsonl").write_text("\n".join(map(json.dumps, self.tasks)), encoding="utf-8")

    def scope(self, arm):
        scope = {}
        exec(self.cells["arm-settings"], scope)
        exec(self.cells["embedded-sources"], scope)
        scope.update(ARM=arm, WORKING=self.root / arm, DATA=self.data, WHEELS=self.wheels, MODEL=self.model)
        scope["tempfile"] = SimpleNamespace(mkdtemp=lambda prefix: tempfile.mkdtemp(prefix=prefix, dir=self.root))
        return scope

    def test_artifact_regenerates_and_embeds_current_sources_without_private_inputs(self):
        scope = self.scope("sample-control")
        sources = scope["SOURCES"]
        self.assertEqual(set(sources), {*GENERATOR["FILES"], "organizer/pinned-v3.ipynb", "organizer/LICENSE.txt"})
        for filename in GENERATOR["FILES"]:
            self.assertEqual(sources[filename], (ROOT / filename).read_text(encoding="utf-8"))
        mini = self.root / "pinned.ipynb"
        license_file = self.root / "LICENSE"
        mini.write_text(sources["organizer/pinned-v3.ipynb"], encoding="utf-8")
        license_file.write_text(sources["organizer/LICENSE.txt"], encoding="utf-8")
        self.assertEqual(GENERATOR["build_notebook"](mini, license_file), self.notebook)
        for cell in self.notebook["cells"]:
            if cell["cell_type"] == "code":
                self.assertEqual(cell["outputs"], [])
                compile("".join(cell["source"]), cell["id"], "exec")

    def test_all_three_arms_run_the_actual_cpu_preflight_and_keep_the_same_schedule(self):
        schedules = []
        original = self.sample.read_bytes()
        for arm in ["sample-control", "sample-policy", "standalone"]:
            with self.subTest(arm=arm), redirect_stdout(io.StringIO()):
                scope = self.scope(arm)
                exec(self.cells["prepare-pilot"], scope)
                schedules.append(scope["SCHEDULE"].read_bytes())
                protocol = json.loads(scope["PROTOCOL"].read_bytes())
                self.assertEqual(protocol["held_out_repository"], "org/HTTPX")
                selected = json.loads(schedules[-1])
                self.assertEqual({task["repo"] for task in selected}, {"org/Requests", "org/FastAPI", "org/Rich"})
                self.assertTrue(all(set(task) == {"instance_id", "repo"} for task in selected))
                self.assertEqual(scope["RUN_DIR"].name, arm)
                self.assertIn("1800", scope["launcher"])
                agent = scope["AGENT"]
                if arm == "sample-control":
                    self.assertEqual((agent / "agent.yaml").read_bytes(), original)
                if arm == "sample-policy":
                    self.assertIn("Base instructions", (agent / "prompts/root-repair-policy.md").read_text())
                if arm == "standalone":
                    self.assertEqual((agent / "agent.yaml").read_text(), (ROOT / "candidate/agent.yaml").read_text())
                with self.assertRaises(FileExistsError):
                    exec(self.cells["prepare-pilot"], scope)
                with patch("subprocess.run") as launch:
                    exec(self.cells["launch-pilot"], scope)
                    launch.assert_called_once_with(scope["launcher"], check=True)
        self.assertEqual(schedules, [schedules[0]] * 3)
        self.assertEqual(self.sample.read_bytes(), original)

    def test_result_export_uses_arm_names_and_preserves_prior_outputs(self):
        scope = self.scope("sample-control")
        with redirect_stdout(io.StringIO()):
            exec(self.cells["prepare-pilot"], scope)
            run_dir = scope["RUN_DIR"]
            run_dir.mkdir(parents=True)
            for name, text in [("manifest.json", "{}"), ("results.jsonl", ""), ("status.json", "{}")]:
                (run_dir / name).write_text(text, encoding="utf-8")
            (run_dir / "private-trace.txt").write_text("evaluator-only", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                exec(self.cells["launch-pilot"], scope)
            exec(self.cells["export-evidence"], scope)
            with zipfile.ZipFile(scope["bundle"]) as bundle:
                self.assertEqual(set(bundle.namelist()), {
                    "sample-control/" + name for name in
                    ["manifest.json", "results.jsonl", "status.json", "development-schedule.json", "protocol.json"]})
            with self.assertRaises(FileExistsError):
                exec(self.cells["export-evidence"], scope)


if __name__ == "__main__":
    unittest.main()
