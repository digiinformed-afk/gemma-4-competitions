"""Execute the final notebook in a fresh Jupyter kernel, preserving failures."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent / 'paper' if (ROOT.parent / 'paper').is_dir() else ROOT.parent / 'public/project'


def main():
    runtime = ROOT / 'kernel-runtime'
    scratch = runtime / 'tmp'
    scratch.mkdir(parents=True, exist_ok=True)
    os.environ['TEMP'] = str(scratch)
    os.environ['TMP'] = str(scratch)
    import nbformat
    from nbclient import NotebookClient
    spec = runtime / 'kernels/patchquestions'
    spec.mkdir(parents=True, exist_ok=True)
    (spec / 'kernel.json').write_text(json.dumps({'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'], 'display_name': 'PatchQuestions isolated Python', 'language': 'python'}), encoding='utf-8')
    os.environ['JUPYTER_PATH'] = str(runtime)
    os.environ['JUPYTER_RUNTIME_DIR'] = str(runtime / 'runtime')
    os.environ['IPYTHONDIR'] = str(runtime / 'ipython')
    for name in ['runtime', 'ipython']:
        (runtime / name).mkdir(exist_ok=True)
    verification = ROOT / 'verification/notebook'
    verification.mkdir(parents=True, exist_ok=True)
    work = ROOT / 'notebook-work'
    work.mkdir(exist_ok=True)
    notebook = nbformat.read(PAPER / 'PatchQuestions.ipynb', as_version=4)
    original_sha = hashlib.sha256((PAPER / 'PatchQuestions.ipynb').read_bytes()).hexdigest()
    started = time.perf_counter()
    client = NotebookClient(notebook, timeout=180, startup_timeout=45, iopub_timeout=30, kernel_name='patchquestions', resources={'metadata': {'path': str(work)}})
    report = {'runtime': sys.version, 'input_notebook_sha256': original_sha, 'packages': {n: importlib.metadata.version(n) for n in ['nbclient', 'nbformat', 'ipykernel', 'jupyter-client']}, 'completed': False}
    try:
        client.execute()
        report['completed'] = True
        report['executed_code_cells'] = sum(c.cell_type == 'code' and c.execution_count is not None for c in notebook.cells)
        report['error_outputs'] = sum(o.output_type == 'error' for c in notebook.cells if c.cell_type == 'code' for o in c.outputs)
    finally:
        report['wall_seconds'] = time.perf_counter() - started
        nbformat.write(notebook, verification / 'PatchQuestions.executed.ipynb')
        (verification / 'EXECUTION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if report['completed']:
        nbformat.write(notebook, PAPER / 'PatchQuestions.ipynb')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
