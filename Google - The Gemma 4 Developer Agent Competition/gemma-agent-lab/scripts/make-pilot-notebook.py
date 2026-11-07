"""Build the self-contained private Kaggle pilot notebook from reviewed local sources."""

import argparse
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "private-data/organizer/gemma-getting-started-organizer-v3.ipynb"
OUTPUT = ROOT / "artifacts/main-track-pilot.ipynb"
SOURCE_URL = "https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent"
FILES = (
    "scripts/run-kaggle.py", "scripts/freeze-schedule.py", "scripts/build-submission.py",
    "candidate/agent.yaml", "candidate/eval_config.yaml", "candidate/instruction.md",
)

CONFIG = '''from pathlib import Path
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import zipfile

ARM = "sample-control"  # Choose sample-control, sample-policy, or standalone.
DATA = Path("/kaggle/input/competitions/gemma-4-developer-agent")
WHEELS = Path("/kaggle/input/datasets/metric/gemma-4-developer-agent-wheelhouse")
MODEL = Path("/kaggle/input/models/google/gemma-4/other/gemma-4-31b-it-qat-w4a16-ct/2")
WORKING = Path("/kaggle/working")
'''

PREPARE = '''if ARM not in {"sample-control", "sample-policy", "standalone"}:
    raise ValueError("Unknown ARM. Choose one of the three names in the settings cell.")
if not (DATA / "tasks.jsonl").is_file() or not (DATA / "snapshots").is_dir():
    raise FileNotFoundError(f"Attach the competition data at {DATA}.")
if ARM != "standalone" and not (DATA / "sample_submission/agent.yaml").is_file():
    raise FileNotFoundError("The selected arm needs the organizer's sample_submission directory.")
if not any(WHEELS.glob("swegemma-*.whl")):
    raise FileNotFoundError(f"Attach the organizer wheelhouse at {WHEELS}.")
if not (MODEL / "config.json").is_file() or not any(MODEL.glob("*.safetensors")):
    raise FileNotFoundError(f"Attach the official 31B QAT model version 2 at {MODEL}.")

OUTPUT_ROOT = WORKING / "main-track-pilot"
if OUTPUT_ROOT.exists():
    raise FileExistsError(f"{OUTPUT_ROOT} already exists. Save its outputs and start a fresh Kaggle session.")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=False)
STAGE = Path(tempfile.mkdtemp(prefix="gemma-main-pilot-"))
for relative, source in SOURCES.items():
    target = STAGE / relative
    target.parent.mkdir(exist_ok=True, parents=True)
    with target.open("x", encoding="utf-8", newline="\\n") as handle:
        handle.write(source)

schedule_tools = runpy.run_path(str(STAGE / "scripts/freeze-schedule.py"))
task_file = DATA / "tasks.jsonl"
repos = {task["repo"] for task in schedule_tools["read_tasks"](task_file)}
httpx = sorted(repo for repo in repos if repo.rsplit("/", 1)[-1].casefold() == "httpx")
if len(httpx) != 1:
    raise ValueError(f"Expected one HTTPX repository in the attached task identities, found {httpx}.")
HOLDOUT = httpx[0]
SCHEDULE = OUTPUT_ROOT / "development-schedule.json"
schedule = schedule_tools["freeze_schedule"](schedule_tools["read_tasks"](task_file),
    mode="development", holdout_repo=HOLDOUT, count=3, seed="gemma-main-v1")
if len({task["repo"] for task in schedule}) != 3:
    raise ValueError("The pilot expects three distinct development repositories in the public task revision.")
schedule_tools["write_schedule"](SCHEDULE, schedule)
PROTOCOL = OUTPUT_ROOT / "protocol.json"
with PROTOCOL.open("x", encoding="utf-8") as handle:
    json.dump({"arm": ARM, "mode": "development", "held_out_repository": HOLDOUT,
               "seed": "gemma-main-v1", "scheduled": 3, "wall_budget_seconds": 1800}, handle, indent=2)

AGENT = STAGE / "agent"
builder = runpy.run_path(str(STAGE / "scripts/build-submission.py"))
original = STAGE / "candidate" if ARM == "standalone" else DATA / "sample_submission"
members = builder["members"](original)
AGENT.mkdir()
for relative in members:
    destination = AGENT / relative
    destination.parent.mkdir(exist_ok=True, parents=True)
    shutil.copyfile(original / relative, destination)
if ARM == "sample-policy":
    builder["add_policy"](AGENT, STAGE / "candidate/instruction.md")
builder["members"](AGENT)
RUN_DIR = OUTPUT_ROOT / "runs" / ARM
launcher = [sys.executable, "-B", str(STAGE / "scripts/run-kaggle.py"),
    "--starter", str(STAGE / "organizer/pinned-v3.ipynb"), "--data", str(DATA),
    "--agent", str(AGENT), "--schedule", str(SCHEDULE), "--output", str(RUN_DIR),
    "--wall-seconds", "1800", "--environment", "kaggle-offline-l4x4-main-pilot-v1"]
subprocess.run([*launcher, "--preflight"], check=True)
print(f"Arm {ARM} | held out {HOLDOUT} | cold wall-clock limit 1800 seconds")
print(json.dumps(schedule, indent=2))
'''

LAUNCH = '''if RUN_DIR.exists():
    raise FileExistsError(f"Results already exist at {RUN_DIR}. Start a fresh Kaggle session for a new run.")
subprocess.run(launcher, check=True)
'''

EXPORT = '''if not (RUN_DIR / "manifest.json").is_file():
    raise FileNotFoundError(f"No finalized manifest. Inspect {RUN_DIR / 'status.json'} and the worker output.")
bundle = WORKING / f"{ARM}-pilot-results.zip"
with zipfile.ZipFile(bundle, "x", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in ("manifest.json", "results.jsonl", "status.json"):
        archive.write(RUN_DIR / name, f"{ARM}/{name}")
    archive.write(SCHEDULE, f"{ARM}/development-schedule.json")
    archive.write(PROTOCOL, f"{ARM}/protocol.json")
print((RUN_DIR / "status.json").read_text(encoding="utf-8"))
print(f"Download {bundle.name} from the notebook outputs.")
'''


def cell(kind, name, source, hidden=False):
    result = dict(cell_type=kind, id=name, metadata={}, source=source.strip().splitlines(keepends=True))
    if kind == "code":
        result.update(execution_count=None, outputs=[])
        if hidden:
            result["metadata"] = {"jupyter": {"source_hidden": True}}
    return result


def build_notebook(starter, license_file):
    runner = runpy.run_path(str(ROOT / "scripts/run-kaggle.py"))
    pinned = runner["official_cells"](starter)
    official = [cell("code", name, pinned[runner[key]]) for name, key in (("install", "INSTALL"), ("serve", "SERVE"))]
    metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
    mini = dict(nbformat=4, nbformat_minor=5, metadata=metadata, cells=official)
    sources = {filename: (ROOT / filename).read_text(encoding="utf-8") for filename in FILES}
    sources["organizer/pinned-v3.ipynb"] = json.dumps(mini, ensure_ascii=True)
    license_text = license_file.read_text(encoding="utf-8")
    if "Apache License" not in license_text or "END OF TERMS AND CONDITIONS" not in license_text:
        raise ValueError("Supply the complete Apache License 2.0 text.")
    sources["organizer/LICENSE.txt"] = license_text
    # All serialized values are strings, so this JSON literal is also valid Python.
    payload = "SOURCES = " + json.dumps(sources, ensure_ascii=True, indent=2)
    intro = f"""# Main-track pilot · Gemma 4 Developer Agent

Run one arm per **fresh private Kaggle session**. Attach the competition data, the organizer's gemma-4-developer-agent-wheelhouse, and Google Gemma 4 **31B IT QAT W4A16 CT, version 2**. Select the competition L4×4 accelerator and disable Internet. These inputs match the [organizer’s starter notebook]({SOURCE_URL}).

The primary comparison is **sample-control** (the organizer’s 31B sample, including its adapters) against **sample-policy** (the same sample with extra root repair instructions). **standalone** runs the independent single-agent candidate as a separate configuration. Select an arm below and run the cells in order. Use the same notebook, input versions and machine settings for both primary arms.

The pilot freezes three public tasks using seed `gemma-main-v1`, one per development repository, and reserves the entire HTTPX repository. Each arm has 1,800 seconds of cold elapsed time including verification. This pilot measures development performance. The competition scores hidden tasks separately.
"""
    credit = f"""### Embedded source

The collapsed cell carries the local scripts, candidate configuration, and the installation and model-serving cells from Ryan Holbrook’s *Getting Started – Gemma 4 Developer Agent*, version 3, under Apache License 2.0. The complete license is bundled in `organizer/LICENSE.txt`. The pilot runs those two hash-checked cells inside its worker. [Organizer notebook]({SOURCE_URL}) · [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
"""
    finish = """### Retrieve the result

Download the arm’s result ZIP before ending the session. Extract each ZIP into the same local directory. To compare the primary arms, run the following from the project folder with the extracted paths. A failed worker can leave its status and partial evidence in the private notebook output.

```sh
node scripts/compare-runs.mjs sample-control/manifest.json sample-policy/manifest.json
```"""
    cells = [
        cell("markdown", "pilot-overview", intro), cell("code", "arm-settings", CONFIG),
        cell("markdown", "source-credit", credit), cell("code", "embedded-sources", payload, hidden=True),
        cell("markdown", "prepare-heading", "### Prepare the agent and verify the frozen schedule"),
        cell("code", "prepare-pilot", PREPARE),
        cell("markdown", "launch-heading", "### Start the timed GPU run"),
        cell("code", "launch-pilot", LAUNCH), cell("markdown", "export-heading", finish),
        cell("code", "export-evidence", EXPORT),
    ]
    return dict(nbformat=4, nbformat_minor=5, metadata=metadata, cells=cells)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--starter", type=Path, default=STARTER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--apache-license", type=Path, help="Path to complete Apache 2.0 license text")
    args = parser.parse_args()
    license_file = args.apache_license or next(
        (ROOT / "private-data/validator-env").glob("google_cloud_core-*.dist-info/licenses/LICENSE"), None)
    if license_file is None:
        parser.error("Pass --apache-license with a local copy of the complete Apache License 2.0.")
    notebook = build_notebook(args.starter, license_file)
    args.output.parent.mkdir(exist_ok=True, parents=True)
    args.output.write_text(json.dumps(notebook, ensure_ascii=True, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"Built {args.output}")


if __name__ == "__main__":
    main()
