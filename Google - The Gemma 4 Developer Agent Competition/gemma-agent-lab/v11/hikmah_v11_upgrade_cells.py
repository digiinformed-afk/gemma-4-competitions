"""Reconstruct documented V11 on the saved runtime-v2.2 pilot; no GPU result implied.

The earlier Canvas export was unavailable. This implementation is a reconstruction,
not a recovered byte-for-byte copy. Use the repaired notebook as --baseline.
"""

import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path


REVISION = "v11-reconstructed-2026-11-09"
EVALUATION = dict(max_time_minutes=10, max_tool_calls=65, max_turns=95,
                  timeout_seconds=90, verification_timeout_seconds=300)
SAMPLING = dict(temperature=0.15, top_p=0.90, max_output_tokens=2560)
POLICY = """
## V11: complete call chains within the repair budget

Batch related symbol searches into a single focused git grep command where useful.
For a changed API, trace its public entry point, wrapper/factory, stored parameter,
internal consumer and callers. Read those related definitions together. Wire the
required behavior through the whole call chain, including defaults and annotations;
an internal-only change cannot implement a public keyword argument. Preserve old
call behavior. Apply this method to the current issue; do not assume a task-specific
answer or inspect grading inputs.

After editing, run a cheap import and inspect.signature check of the affected public
API, then one minimal call with the issue's new input. Only proceed to targeted
pytest once the import and public API are coherent. Treat setup failures separately
from assertion failures. Use a focused regression instead of a full suite.

Use get_status initially, after initial diagnosis, after the main edit, and before
submission if budget permits. These four checks and the final 60 seconds are a
planning reserve, not additional harness allowances. If fewer than 60 seconds or
few calls remain, stop expanding the search, inspect the diff, remove your scratch
changes and call submit_patch. Leave room for the final text response. Do not spend
the submission reserve on another speculative edit or a long test command.
""".strip()

EXPORT = '''# Evidence and uploadable configuration are separate archives.
bundle = WORKING / f"{ARM}-pilot-v11-results.zip"
if bundle.exists():
    raise FileExistsError(bundle)
with zipfile.ZipFile(bundle, "x", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(OUTPUT_ROOT.rglob("*")):
        if path.is_file():
            archive.write(path, path.relative_to(OUTPUT_ROOT.parent))
    for name in ("scripts/run-kaggle.py", "scripts/sandbox-runtime.py", "supplemental-wheels.json"):
        archive.write(STAGE / name, "runtime-source/" + name)
print("Private evidence archive:", bundle)
if (RUN_DIR / "status.json").exists():
    print((RUN_DIR / "status.json").read_text())
if (RUN_DIR / "results.jsonl").exists():
    print((RUN_DIR / "results.jsonl").read_text())
if RUN_RETURN_CODE != 0:
    print("INVALID RUN: inspect logs and preflight. No performance conclusion.")

# Local evaluator budgets belong to this pilot, not the uploaded agent archive.
# The worker validates AGENT with the organizer's validator before evaluation.
submission = WORKING / "submission.zip"
if submission.exists():
    raise FileExistsError(submission)
with tempfile.TemporaryDirectory(prefix="hikmah-v11-package-") as package_temp:
    package_root = Path(package_temp) / "agent"
    shutil.copytree(AGENT, package_root)
    for name in ("eval_config.yaml", "eval_config.yml"):
        (package_root / name).unlink(missing_ok=True)
    package_report = builder["build"](package_root, submission, None)
with zipfile.ZipFile(submission) as archive:
    assert "agent.yaml" in archive.namelist(), "Root agent.yaml missing"
RUN_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(submission, RUN_DIR / "submission.zip")
(RUN_DIR / "submission-build.json").write_text(json.dumps(package_report, indent=2))
print("Candidate agent archive (not submitted):", submission)
print(json.dumps(package_report, indent=2))
'''


def replace_once(text, before, after):
    if text.count(before) != 1:
        raise ValueError(f"Expected one baseline marker: {before[:100]!r}")
    return text.replace(before, after, 1)


def set_source(cell, text):
    cell["source"] = text.splitlines(keepends=True)


def upgrade(baseline):
    notebook = copy.deepcopy(baseline)
    cells = notebook["cells"]
    if len(cells) != 10 or [i for i, c in enumerate(cells) if c["cell_type"] == "code"] != [1, 3, 5, 7, 9]:
        raise ValueError("Expected the saved ten-cell repaired pilot")
    settings = "".join(cells[1]["source"])
    settings = replace_once(settings, 'ARM = "sample-control"', 'ARM = "sample-hikmah"')
    settings = settings.replace(", or standalone.", ".")
    start = settings.index("EVAL_CONFIG = ")
    settings = settings[:start] + "EVAL_CONFIG = " + repr(EVALUATION) + "\n"
    set_source(cells[1], settings)

    tree = ast.parse("".join(cells[3]["source"]))
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Assign):
        raise ValueError("Expected one literal SOURCES assignment")
    if [getattr(t, "id", None) for t in tree.body[0].targets] != ["SOURCES"]:
        raise ValueError("Expected SOURCES assignment")
    sources = ast.literal_eval(tree.body[0].value)
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in sources.items()):
        raise ValueError("Expected text sources")
    if "V11: complete call chains" in sources["candidate/hikmah-policy.md"]:
        raise ValueError("V11 already applied")
    sources["candidate/hikmah-policy.md"] += "\n\n" + POLICY + "\n"
    # Keep only wheel filenames and digests in the public notebook. Attach the
    # existing private runtime wheelhouse when running the notebook on Kaggle.
    wheels = json.loads(sources["supplemental-wheels.json"])
    sources["supplemental-wheels.json"] = json.dumps({
        name: {"input_filename": name, "sha256": record["sha256"]}
        for name, record in wheels.items()
    }, indent=2)
    set_source(cells[3], "SOURCES = " + json.dumps(sources, ensure_ascii=True, indent=2) + "\n")

    prepare = "".join(cells[5]["source"])
    prepare = replace_once(prepare, '{"sample-control", "sample-policy", "sample-hikmah", "standalone"}',
                           '{"sample-control", "sample-policy", "sample-hikmah"}')
    prepare = prepare.replace('main-track-pilot-v2', 'main-track-pilot-v11')
    prepare = prepare.replace('"revision": "runtime-v2.2"', '"revision": ' + repr(REVISION))
    prepare = replace_once(prepare, 'schedule_tools["write_schedule"](SCHEDULE, schedule)',
        'expected_ids = ["requests_7309", "rich_3130", "fastapi_14262"]\n'
        'if [task["instance_id"] for task in schedule] != expected_ids:\n'
        '    raise ValueError("Public-task revision changed: review and freeze the schedule explicitly.")\n'
        'schedule_tools["write_schedule"](SCHEDULE, schedule)')
    prepare = replace_once(prepare, 'if sampling_path.is_file():',
                           'if not sampling_path.is_file():\n    raise FileNotFoundError(sampling_path)\nif sampling_path.is_file():')
    prepare = replace_once(prepare, 'sampling["max_output_tokens"] = 8192',
        'sampling.update(' + repr(SAMPLING) + ')\n'
        '    # Keep the thinking allowance below the total output-token cap.\n'
        '    if isinstance(sampling.get("thinking_config"), dict):\n'
        '        sampling["thinking_config"]["thinking_budget"] = 1024')
    prepare = prepare.replace('kaggle-offline-l4x4-main-pilot-v2.2', 'kaggle-offline-l4x4-main-pilot-v11')
    # Three 10-minute tasks plus verification and cold model startup need more
    # headroom than the old 2,700-second run. This is a local measurement cap.
    prepare = prepare.replace('2700', '4200')
    set_source(cells[5], prepare)
    set_source(cells[9], EXPORT)
    set_source(cells[0], """# Hikmah Main Track — Version 11 (reconstructed)

Prepared 9 November 2026. **GPU evaluation pending.** This reconstructs the documented
V11 plan on the saved repaired runtime-v2.2 notebook; it is not the original Canvas export.

Use a fresh **private** Kaggle Python 3.12 session, L4 ×4, Internet off. Attach the
competition data, official 31B QAT model v2, organizer wheelhouse, and the existing
private Hikmah Runtime Wheelhouse. The earlier attachment supplies Pygments only;
attach the other five wheels from the repair ZIP source/extra-wheels/ directory
or extend the private wheelhouse to contain all six hash-pinned wheels.
No model weights, competition snapshots, task statements or wheel bytes are bundled.

Default arm: `sample-hikmah`. For a matched comparison rerun `sample-control` and
`sample-policy` in fresh sessions with the identical V11 budgets and sampling.
Only Hikmah receives the V11 call-chain policy. The local cold wall cap is 4,200s.
The ten-minute task budget is a local experiment setting, not a claim about final
competition limits. A 3/3 pilot is a debugging milestone, not evidence of generalization.
""")
    set_source(cells[8], """### Export private evidence and the candidate

Run the export cell even after a failed worker. Download the private evidence ZIP
and `/kaggle/working/submission.zip`. The latter contains the agent configuration
with `agent.yaml` at ZIP root; it is not a Kaggle submission confirmation. Evaluator
settings are excluded from that archive. Run official final validation in the
competition environment before uploading. Do not publish private traces or inputs.
""")
    notebook.setdefault("metadata", {})["hikmah"] = {
        "revision": REVISION, "provenance": "reconstructed; original Canvas export unavailable",
        "gpu_tested": False, "baseline_sha256": hashlib.sha256(
            json.dumps(baseline, sort_keys=True).encode()).hexdigest(),
        "evaluation": EVALUATION, "sampling": SAMPLING,
        "implementation_choices": {"thinking_budget": 1024, "cold_wall_seconds": 4200},
    }
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "code":
            cell.update(execution_count=None, outputs=[])
            compile("".join(cell["source"]), f"v11-cell-{i}", "exec")
    for name, source in sources.items():
        if name.endswith(".py"):
            compile(source, name, "exec")
    return notebook


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    notebook = upgrade(json.loads(args.baseline.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as target:
        json.dump(notebook, target, indent=1)
        target.write("\n")
    print(args.output)


if __name__ == "__main__":
    main()
