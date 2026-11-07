"""Build a self-contained offline notebook from the nine canonical modules."""
from pathlib import Path
import base64
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent / 'paper' if (ROOT.parent / 'paper').is_dir() else ROOT.parent / 'public/project'
MODULES = ['benchmark.py', 'replay.py', 'analyze.py', 'intervention.py', 'verify.py', 'export_cases.py', 'cognitive_probe.py', 'paper_analysis.py', 'pilot.py']


def cell(kind, source, **metadata):
    result = {'cell_type': kind, 'id': hashlib.sha256(source.encode()).hexdigest()[:12], 'metadata': metadata, 'source': source.splitlines(keepends=True)}
    if kind == 'code':
        result.update(execution_count=None, outputs=[])
    return result


def main():
    frozen = base64.b64encode((PAPER / 'frozen_cases.jsonl.gz').read_bytes()).decode()
    cells = [cell('markdown', '# PatchQuestions\n\nAn executable resource for budgeted API-contract disambiguation. Run all cells in a fresh CPU kernel. No network, model, GPU or pip install is needed for these experiments. Reference runtime is CPython 3.12.14. This notebook materializes nine source modules in a new writable subdirectory and preserves the embedded reference matrices separately. No learned-model session is performed.\n'),
             cell('code', 'import base64, contextlib, gzip, io, json, os, runpy, sys, tempfile\nfrom pathlib import Path\nwork = Path(tempfile.mkdtemp(prefix="patchquestions-", dir=Path.cwd())).resolve()\nos.chdir(work)\nsys.path.insert(0, str(work))\nprint("Runtime:", sys.version)\nprint("Output directory:", work.name)\n')]
    for name in MODULES:
        source = (PAPER / name).read_text(encoding='utf-8')
        cells.append(cell('code', f'Path({name!r}).write_text({source!r}, encoding="utf-8")\n', embedded_module=name, embedded_source_sha256=hashlib.sha256(source.encode()).hexdigest()))
    cells += [cell('code', f'reference = base64.b64decode({frozen!r})\nPath("reference_frozen_cases.jsonl.gz").write_bytes(reference)\nPath("frozen_cases.jsonl.gz").write_bytes(reference)\n'),
              cell('markdown', '## Rebuild the reference experiment\n\nThe 18,000 rows reuse 750 target–split conditions across eight families. Scores are exact expectations for this finite resource.\n'),
              cell('code', 'stream = io.StringIO()\nwith contextlib.redirect_stdout(stream):\n    runpy.run_path("benchmark.py", run_name="__main__")\nPath("summary.json").write_text(stream.getvalue(), encoding="utf-8")\nprint(stream.getvalue())\n'),
              cell('code', 'from analyze import audit\nreport = audit()\nPath("audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")\nprint(json.dumps(report, indent=2))\n'),
              cell('markdown', '## Cross policy and probe pool\n\nThe intervention is exploratory and uses richer answer channels. The analysis computes entropy and frugal at budgets 1–3 on both scoring suites, with selected input/answer code-point costs. These are not human-time or tokenizer measurements.\n'),
              cell('code', 'stream = io.StringIO()\nwith contextlib.redirect_stdout(stream):\n    runpy.run_path("intervention.py", run_name="__main__")\nPath("intervention.json").write_text(stream.getvalue(), encoding="utf-8")\nprint(stream.getvalue())\nfrom paper_analysis import build\nrevision = build(Path("revision-results"))\n'),
              cell('markdown', '## Verify, export and test the scoring boundary\n\nHistorical replay runners retain the original held-out-only endpoint. The new supervisor also checks consistency. The fixture below demonstrates why this matters; it is a deterministic software test.\n'),
              cell('code', 'runpy.run_path("verify.py", run_name="__main__")\nrunpy.run_path("export_cases.py", run_name="__main__")\nold = [json.loads(x) for x in gzip.decompress(reference).splitlines()]\nnew = [json.loads(x) for x in gzip.decompress(Path("frozen_cases.jsonl.gz").read_bytes()).splitlines()]\nprint("Frozen matrix equality under this runtime:", old == new)\n# Keep the pinned matrix for the presentation control and future pilot.\nPath("runtime_frozen_cases.jsonl.gz").write_bytes(Path("frozen_cases.jsonl.gz").read_bytes())\nPath("frozen_cases.jsonl.gz").write_bytes(reference)\nimport subprocess\ncheck = subprocess.run([sys.executable, "-B", "cognitive_probe.py", "--check"], capture_output=True, text=True, check=True)\nprint(check.stdout)\n'),
              cell('code', 'from pilot import Session, load_cases\nimport random\ncases = load_cases(Path("frozen_cases.jsonl.gz"))\nc = cases["wrap", 43]\norder = list(range(len(c["configs"])))\nrandom.Random(2026).shuffle(order)\nsession = Session(c, 10, order, "named")\nsession.step({"ask": 9})\nanswer_to_model, grade = session.step({"pick": order.index(14)})\nassert answer_to_model is None\nassert grade["heldout_exact"] and not grade["query_consistent"] and not grade["success"]\nprint("Contradictory-pick fixture:", grade)\nprint("No model session was executed.")\n')]
    notebook = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3.12.14'}}, 'nbformat': 4, 'nbformat_minor': 5}
    path = PAPER / 'PatchQuestions.ipynb'
    path.write_text(json.dumps(notebook, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'notebook': str(path), 'modules': len(MODULES), 'cells': len(cells)}))


if __name__ == '__main__':
    main()
