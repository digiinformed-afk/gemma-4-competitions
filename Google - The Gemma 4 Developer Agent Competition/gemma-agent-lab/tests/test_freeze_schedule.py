import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "freeze-schedule.py"
spec = importlib.util.spec_from_file_location("freeze_tasks", SCRIPT)
freeze_tasks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freeze_tasks)


def source_tasks():
    return [
        {"instance_id": f"{repo}-{i}", "repo": repo, "patch": "hidden", "test_patch": "hidden"}
        for repo, size in [("a", 3), ("b", 1), ("c", 3), ("held", 4)]
        for i in range(size)
    ]


class FreezeTests(unittest.TestCase):
    def test_round_robin_determinism_exclusion_and_identity_only(self):
        source = source_tasks()
        schedule = freeze_tasks.freeze_schedule(source, "development", "held", 7)
        self.assertEqual(len({row["instance_id"] for row in schedule}), 7)
        self.assertEqual({row["repo"] for row in schedule[:3]}, {"a", "b", "c"})
        self.assertEqual({row["repo"] for row in schedule[3:5]}, {"a", "c"})
        self.assertEqual({row["repo"] for row in schedule[5:]}, {"a", "c"})
        self.assertTrue(all(set(row) == {"instance_id", "repo"} for row in schedule))
        revised = [dict(row, patch="new", test_patch="different") for row in reversed(source)]
        self.assertEqual(freeze_tasks.freeze_schedule(revised, "development", "held", 7), schedule)
        self.assertEqual(freeze_tasks.freeze_schedule(source, "development", "held", 2), schedule[:2])

    def test_holdout_is_disjoint_and_bounded(self):
        source = source_tasks()
        holdout = freeze_tasks.freeze_schedule(source, "holdout", "held", 3, seed="fixed")
        self.assertEqual(len(holdout), 3)
        self.assertTrue(all(row["repo"] == "held" for row in holdout))
        self.assertEqual(holdout, freeze_tasks.freeze_schedule(reversed(source), "holdout", "held", 3, seed="fixed"))
        with self.assertRaisesRegex(ValueError, "only 4"):
            freeze_tasks.freeze_schedule(source, "holdout", "held", 5)
        with self.assertRaisesRegex(ValueError, "only 7"):
            freeze_tasks.freeze_schedule(source, "development", "held", 8)

    def test_rejects_bad_metadata_everywhere_even_outside_the_selected_split(self):
        source = source_tasks()
        for invalid in [None, {}, {"repo": "", "instance_id": "x"}, {"repo": "held", "instance_id": 5},
                        {"repo": "held", "instance_id": " x"}, source[-1]]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                freeze_tasks.freeze_schedule([*source, invalid], "development", "held", 1)
        for mode, held_out, count in [("bad", "held", 1), ("development", "absent", 1),
                                     ("development", "held", 0), ("development", "held", True)]:
            with self.subTest(mode=mode, held_out=held_out, count=count), self.assertRaises(ValueError):
                freeze_tasks.freeze_schedule(source, mode, held_out, count)

    def test_cli_never_overwrites_or_publishes_a_partial_schedule(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.jsonl"
            output = Path(directory) / "frozen.json"
            source.write_text("\n".join(map(json.dumps, source_tasks())), encoding="utf-8-sig")
            command = [sys.executable, "-B", str(SCRIPT), str(source), str(output),
                       "--mode", "development", "--holdout-repo", "held", "--count", "2"]
            subprocess.run(command, capture_output=True, check=True)
            original = output.read_bytes()
            self.assertEqual(len(json.loads(original)), 2)
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(original, output.read_bytes())
            output.unlink()
            with source.open("a", encoding="utf-8") as handle:
                handle.write("\n{")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Invalid JSON at line", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
