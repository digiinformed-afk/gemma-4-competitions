"""CPU checks for the exported notebook; these do not grade model repairs."""
import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("upgrade", ROOT / "hikmah_v11_upgrade_cells.py")
upgrade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upgrade)


class V11Tests(unittest.TestCase):
    def setUp(self):
        self.notebook = json.loads((ROOT / "hikmah-main-track-pilot-v11.ipynb").read_text())
        self.cells = self.notebook["cells"]
        self.sources = ast.literal_eval(ast.parse("".join(self.cells[3]["source"])).body[0].value)

    def test_clean_export_and_no_embedded_wheels(self):
        for i, cell in enumerate(self.cells):
            if cell["cell_type"] == "code":
                self.assertEqual(cell["outputs"], [])
                self.assertIsNone(cell["execution_count"])
                compile("".join(cell["source"]), f"cell-{i}", "exec")
        wheels = json.loads(self.sources["supplemental-wheels.json"])
        self.assertEqual(len(wheels), 6)
        for name, record in wheels.items():
            self.assertEqual(set(record), {"input_filename", "sha256"})
            self.assertEqual(record["input_filename"], name)
        with self.assertRaisesRegex(ValueError, "baseline marker|already applied"):
            upgrade.upgrade(self.notebook)

    def test_all_arms_prepare_with_equal_budgets_and_separate_policy(self):
        for arm in ("sample-control", "sample-policy", "sample-hikmah"):
            with self.subTest(arm=arm), tempfile.TemporaryDirectory() as temporary:
                work = Path(temporary)
                data, wheels, model = [work / name for name in ("data", "wheels", "model")]
                for path in (data / "snapshots", wheels, model, data / "sample_submission/configs"):
                    path.mkdir(parents=True)
                tasks = [dict(instance_id=task, repo=repo) for task, repo in (
                    ("requests_7309", "requests"), ("rich_3130", "rich"),
                    ("fastapi_14262", "fastapi"), ("httpx_1", "httpx"))]
                (data / "tasks.jsonl").write_text("".join(json.dumps(t) + "\n" for t in tasks))
                (wheels / "swegemma-fixture.whl").touch()
                (model / "config.json").write_text("{}")
                (model / "fixture.safetensors").touch()
                (data / "sample_submission/agent.yaml").write_text("name: fixture\ninstruction: !include prompt.md\n")
                (data / "sample_submission/prompt.md").write_text("Fixture base instruction")
                (data / "sample_submission/configs/sampling.yaml").write_text(
                    "temperature: 0.2\nmax_output_tokens: 8192\nthinking_config:\n  thinking_budget: 4096\n")
                actual_run_path = runpy.run_path
                def fixture_run_path(path):
                    result = actual_run_path(path)
                    if path.endswith("freeze-schedule.py"):
                        # Only task selection is mocked. This checks preparation,
                        # not competition data access or real task identities.
                        result["freeze_schedule"] = lambda *a, **kw: tasks[:3]
                    return result
                scope = dict(Path=Path, json=json, runpy=runpy, shutil=shutil, subprocess=subprocess,
                             sys=sys, tempfile=tempfile, zipfile=zipfile, ARM=arm, DATA=data,
                             WHEELS=wheels, MODEL=model, WORKING=work, SOURCES=self.sources,
                             EVAL_CONFIG=upgrade.EVALUATION)
                with patch.object(runpy, "run_path", side_effect=fixture_run_path), \
                     patch.object(subprocess, "run") as command, contextlib.redirect_stdout(io.StringIO()):
                    exec(compile("".join(self.cells[5]["source"]), "prepare", "exec"), scope)
                self.assertTrue(command.call_args.kwargs["check"])
                import yaml
                sampling = yaml.safe_load((scope["AGENT"] / "configs/sampling.yaml").read_text())
                self.assertEqual({k: sampling[k] for k in upgrade.SAMPLING}, upgrade.SAMPLING)
                self.assertEqual(sampling["thinking_config"]["thinking_budget"], 1024)
                self.assertEqual(json.loads((scope["AGENT"] / "eval_config.yaml").read_text())["evaluation"], upgrade.EVALUATION)
                prompt = "\n".join(p.read_text() for p in scope["AGENT"].rglob("*.md"))
                self.assertEqual("V11: complete call chains" in prompt, arm == "sample-hikmah")
                protocol = json.loads(scope["PROTOCOL"].read_text())
                self.assertEqual(protocol["wall_budget_seconds"], 4200)
                self.assertEqual(protocol["scheduled"], 3)

    def test_export_keeps_evidence_out_of_submission(self):
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            stage = work / "stage"
            for relative, content in self.sources.items():
                path = stage / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            agent = stage / "agent"
            agent.mkdir()
            (agent / "agent.yaml").write_text("name: fixture\ninstruction: Fixture\n")
            (agent / "eval_config.yaml").write_text("evaluation: {}\n")
            output = work / "pilot"
            run = output / "runs/sample-hikmah"
            run.mkdir(parents=True)
            (run / "status.json").write_text('{"status":"fixture"}')
            (run / "private-worker.log").write_text("fixture evidence")
            scope = dict(Path=Path, json=json, shutil=shutil, tempfile=tempfile, zipfile=zipfile,
                         WORKING=work, ARM="sample-hikmah", OUTPUT_ROOT=output, STAGE=stage,
                         RUN_DIR=run, AGENT=agent, RUN_RETURN_CODE=0,
                         builder=runpy.run_path(str(stage / "scripts/build-submission.py")))
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile("".join(self.cells[9]["source"]), "export", "exec"), scope)
            with zipfile.ZipFile(work / "submission.zip") as archive:
                self.assertEqual(archive.namelist(), ["agent.yaml"])
            self.assertTrue((agent / "eval_config.yaml").exists())
            self.assertEqual((run / "submission.zip").read_bytes(), (work / "submission.zip").read_bytes())
            with zipfile.ZipFile(work / "sample-hikmah-pilot-v11-results.zip") as archive:
                self.assertTrue(any(name.endswith("private-worker.log") for name in archive.namelist()))


if __name__ == "__main__":
    unittest.main()
