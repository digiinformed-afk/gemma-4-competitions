"""Audit existing PatchQuestions artifacts and rerun in a separate output folder.

Run from any directory: python -B shared/verify_workspace.py
This never writes to the original project or replaces its reference results.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/public/project"
OUTPUT = Path(__file__).resolve().parent / "verification" / "2026-11-07-python315"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT,
                        help="New output directory; existing directories are never overwritten")
    OUTPUT = parser.parse_args().output.resolve()
    OUTPUT.mkdir(parents=True, exist_ok=False)
    report = {"review_date_pkt": "2026-11-07", "python": platform.python_version(),
              "source": str(SOURCE), "output": str(OUTPUT), "commands": []}
    report["source_sha256"] = {p.name: sha(p.read_bytes()) for p in sorted(SOURCE.iterdir()) if p.is_file()}
    rows = list(csv.DictReader((SOURCE / "scores.csv").open(encoding="utf-8")))
    families = sorted({r["family"] for r in rows})
    summary = json.loads((SOURCE / "summary.json").read_text(encoding="utf-8"))
    rebuilt = {m: {b: statistics.mean(statistics.mean(float(r["heldout_exact"]) for r in rows
                 if r["family"] == f and r["policy"] == m and r["budget"] == b)
                 for f in families) for b in summary[m]} for m in summary}
    assert all(math.isclose(v, summary[m][b], abs_tol=1e-12) for m, budgets in rebuilt.items() for b, v in budgets.items())
    keys = {(r["family"], r["split"], r["target"], r["policy"], r["budget"]) for r in rows}
    episodes = {(r["family"], r["split"], r["target"]) for r in rows}
    assert len(rows) == len(keys) == len(episodes) * 6 * 4 == 18000
    report["stored_results"] = {"rows": len(rows), "episodes": len(episodes), "families": len(families),
                                "summary_matches_scores": True, "summary_rebuilt": rebuilt}
    report["questions_at_budget3"] = {m: statistics.mean(statistics.mean(float(r["queries_used"]) for r in rows
        if r["family"] == f and r["policy"] == m and r["budget"] == "3") for f in families)
        for m in ("entropy", "lookahead", "frugal")}
    manuscript = (SOURCE / "PatchQuestions_Writeup.md").read_text(encoding="utf-8")
    report["manuscript_whitespace_words"] = len(manuscript.split())
    notebook = json.loads((SOURCE / "PatchQuestions.ipynb").read_text(encoding="utf-8"))
    embedded = {}
    for cell in notebook["cells"]:
        text = "".join(cell["source"])
        if text.startswith("%%writefile "):
            first, code = text.split("\n", 1)
            filename = first.split(maxsplit=1)[1]
            embedded[filename] = code.rstrip() == (SOURCE / filename).read_text(encoding="utf-8").rstrip()
    report["notebook_modules_match"] = embedded
    assert all(embedded.values())
    with zipfile.ZipFile(SOURCE / "PatchQuestions_Research_Package.zip") as archive:
        report["zip_entries"] = archive.namelist()
        report["zip_files_differing_from_working_copy"] = [name for name in archive.namelist()
            if (SOURCE / name).is_file() and sha(archive.read(name)) != sha((SOURCE / name).read_bytes())]
        report["research_extensions_absent_from_zip"] = [name for name in
            ("cognitive_probe.py", "cognitive-core-study.md", "research-evidence-notes.md", "research-library.json")
            if name not in archive.namelist()]
    modules = ("benchmark.py", "replay.py", "analyze.py", "intervention.py", "verify.py", "cognitive_probe.py")
    for name in (*modules, "frozen_cases.jsonl.gz"):
        shutil.copy2(SOURCE / name, OUTPUT / name)
    for module, arguments, output_name in (
        ("benchmark.py", [], "summary.json"), ("analyze.py", [], "audit.json"),
        ("intervention.py", [], "intervention.json"), ("verify.py", [], "verify.txt"),
        ("cognitive_probe.py", ["--check"], "cognitive-check.txt")):
        started = time.perf_counter()
        result = subprocess.run([sys.executable, "-B", module, *arguments], cwd=OUTPUT,
                                capture_output=True, text=True, timeout=180)
        (OUTPUT / output_name).write_text(result.stdout, encoding="utf-8")
        (OUTPUT / (module + ".stderr.txt")).write_text(result.stderr, encoding="utf-8")
        report["commands"].append({"command": [sys.executable, "-B", module, *arguments],
            "exit_code": result.returncode, "elapsed_seconds": round(time.perf_counter()-started, 3)})
        if result.returncode:
            (OUTPUT / "workspace-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            raise RuntimeError(f"{module} failed; see {OUTPUT}")
    rerun = json.loads((OUTPUT / "summary.json").read_text(encoding="utf-8"))
    report["runtime_summary_delta_percentage_points"] = {
        m: {b: 100 * (rerun[m][b] - summary[m][b]) for b in summary[m]} for m in summary}
    report["original_sources_unchanged"] = all(sha((SOURCE/name).read_bytes()) == digest
                                              for name, digest in report["source_sha256"].items())
    assert report["original_sources_unchanged"]
    (OUTPUT / "workspace-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("source_sha256", "stored_results", "zip_entries")}, indent=2))


if __name__ == "__main__":
    main()
