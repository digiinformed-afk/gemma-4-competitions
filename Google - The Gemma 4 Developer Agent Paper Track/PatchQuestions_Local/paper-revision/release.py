"""Validate and assemble the revised resource with complete payload hashes."""
from pathlib import Path
import ast
import hashlib
import json
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]
PAPER = ROOT.parent / 'public/project'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    text = (PAPER / 'PatchQuestions_Writeup.md').read_text(encoding='utf-8')
    visible = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    counts = {'scope': 'Entire Markdown including title, subtitle, table contents and references. The official page provides no detailed word-tokenization algorithm; final platform rendering must be checked.', 'raw_whitespace_tokens': len(text.split()), 'visible_whitespace_tokens': len(visible.split()), 'alphanumeric_words': len(re.findall(r"\b[\w]+(?:[’'–-][\w]+)*\b", visible))}
    assert max(counts[k] for k in counts if k != 'scope') < 3000
    for heading in ['## Abstract', '## Introduction', '## Methods and endpoints', '## Results', '## Related work', '## References']:
        assert heading in text
    (ROOT / 'WORD-COUNT.json').write_text(json.dumps(counts, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(WORKSPACE / 'exports/PatchQuestions_AI_Review_2026-11-07.zip') as old:
        original_modules = ['benchmark.py', 'analyze.py', 'intervention.py', 'verify.py', 'replay.py', 'export_cases.py', 'cognitive_probe.py']
        for name in original_modules:
            assert old.read('paper/' + name) == (PAPER / name).read_bytes(), name
    notebook = json.loads((PAPER / 'PatchQuestions.ipynb').read_text(encoding='utf-8'))
    modules = []
    for cell in notebook['cells']:
        if 'embedded_module' in cell['metadata']:
            name = cell['metadata']['embedded_module']
            source = (PAPER / name).read_text(encoding='utf-8')
            assert sha(source.encode()) == cell['metadata']['embedded_source_sha256'], name
            tree = ast.parse(''.join(cell['source']))
            embedded = tree.body[0].value.args[0].value
            assert embedded == source
            modules.append(name)
        if cell['cell_type'] == 'code':
            assert cell['execution_count'] is not None
            assert not any(o['output_type'] == 'error' for o in cell['outputs'])
    assert len(modules) == 9
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-v'], capture_output=True)
    (ROOT / 'verification/pilot-tests.txt').write_bytes(result.stdout + result.stderr)
    assert result.returncode == 0
    completed = ROOT / 'verification/local-cpython312-final'
    execution = json.loads((completed / 'EXECUTION-RECORD.json').read_text(encoding='utf-8'))
    assert len(execution['runs']) == 8 and all(x['returncode'] == 0 for x in execution['runs'])
    assert all(x['semantic_equal'] for x in execution['comparisons'].values())
    notebook_record = json.loads((ROOT / 'verification/notebook/EXECUTION.json').read_text(encoding='utf-8'))
    assert notebook_record['completed'] and notebook_record['error_outputs'] == 0
    assert notebook_record['executed_code_cells'] == 16
    analysis = json.loads((ROOT / 'verification/revision-analysis/revision-results.json').read_text(encoding='utf-8'))
    crossed = json.loads((completed / 'reviewer_checks/crossed_probe_results.json').read_text(encoding='utf-8'))
    for row in analysis['crossed']:
        match = next(x for x in crossed['results'] if (x['scoring_suite'], x['pool'], x['policy'], x['budget']) == (row['suite'], row['pool'], row['policy'], row['budget']))
        assert abs(row['heldout_exact'] - match['heldout_exact']) < 1e-12
        assert abs(row['questions'] - match['queries']) < 1e-12

    entries = {}
    def add(name, path):
        entries[name] = path.read_bytes()
    paper_files = modules + ['PatchQuestions_Writeup.md', 'PatchQuestions.ipynb', 'README.md', 'scores.csv', 'summary.json', 'audit.json', 'intervention.json', 'frozen_cases.jsonl.gz', 'cross_version_summary.json']
    for name in paper_files:
        add('paper/' + name, PAPER / name)
    for name in ['STATUS.md', 'CHANGELOG.md', 'CLAIM-EVIDENCE.md', 'QUESTIONS-RESOLVED.md', 'SUBMISSION-CHECKLIST.md', 'WORD-COUNT.json']:
        add(name, ROOT / name)
    for name in ['reproduce_paper.py', 'build_notebook.py', 'execute_notebook.py']:
        add('tools/' + name, ROOT / name)
    add('tests/test_pilot.py', ROOT / 'tests/test_pilot.py')
    for folder in ['revision-analysis', 'notebook']:
        for path in sorted((ROOT / 'verification' / folder).rglob('*')):
            if path.is_file() and path.suffix != '.ipynb':
                add('evidence/' + folder + '/' + path.relative_to(ROOT / 'verification' / folder).as_posix(), path)
    add('evidence/pilot-tests.txt', ROOT / 'verification/pilot-tests.txt')
    add('evidence/local-cpython312-final/EXECUTION-RECORD.json', completed / 'EXECUTION-RECORD.json')
    for folder in ['reviewer_checks', 'run_cpython_3_12_14']:
        for path in sorted((completed / folder).iterdir()):
            if path.is_file() and path.suffix in {'.json', '.csv', '.txt', '.gz'}:
                add('evidence/local-cpython312-final/' + folder + '/' + path.name, path)
    for name in ['reviewer_audit.py', 'reviewer_audit.original.py', 'protocol_audit.py']:
        add('reviewer/' + name, completed / name)
    for name in original_modules + ['scores.csv', 'summary.json', 'audit.json', 'intervention.json', 'frozen_cases.jsonl.gz']:
        add('reviewer/reference/paper/' + name, completed / 'reference/paper' / name)
    for name in original_modules:
        add('reviewer/run_cpython_3_12_14/' + name, completed / 'run_cpython_3_12_14' / name)
    add('reviewer/FINAL-EXTERNAL-REVIEW.md', WORKSPACE / 'PatchQuestions_Research_Review.md')
    entries['START_HERE.md'] = b'''# PatchQuestions revised paper package

Prepared 7 November 2026. Read paper/PatchQuestions_Writeup.md for the revised paper, paper/README.md for reproduction, and SUBMISSION-CHECKLIST.md for the exact platform steps still needed. No account or submission action was performed.

The paper reports reproduced CPU resource results and an exploratory single-family intervention. There are no Gemma, human-study or repository-repair measurements.

Run the self-contained paper/PatchQuestions.ipynb in a fresh CPU kernel, or use:

    python -B tools/reproduce_paper.py --paper paper --output fresh-run
    python -B -m unittest discover -s tests -v

The complete independent reviewer checks can also be rerun:

    python -B reviewer/reviewer_audit.py
    python -B reviewer/protocol_audit.py

The reference sources are preserved under reviewer/reference. The legacy run_cpython_3_12_14 directory name is retained because the audit imports from it; the current recorded local run used Windows CPython 3.12.14. Coarse timing source reads/writes were made explicitly UTF-8. The unchanged reviewer source is reviewer/reviewer_audit.original.py.

CLAIM-EVIDENCE.md maps retained statements to artifacts. QUESTIONS-RESOLVED.md answers the revision challenges. STATUS.md and CHANGELOG.md record decisions, completed checks and remaining access boundaries. FILE_MANIFEST.json lists every payload except itself. The archive SHA256 is supplied alongside the ZIP.

This ZIP contains synthetic matrices and project code, with local user/workspace paths replaced in evidence copies. It excludes credentials, private competition tasks, model weights, installed libraries and private supervisor plans. This local package does not make a public license or author-rights declaration on the author's behalf.
'''
    sanitized = []
    replacements = [(str(WORKSPACE), '<WORKSPACE>'), (str(WORKSPACE).replace('\\', '\\\\'), '<WORKSPACE>'), (str(Path(sys.executable)), '<PYTHON>'), (str(Path(sys.executable)).replace('\\', '\\\\'), '<PYTHON>')]
    for name, data in list(entries.items()):
        if name.endswith(('.json', '.txt', '.md')):
            content = data.decode('utf-8')
            old = content
            for before, after in replacements:
                content = content.replace(before, after)
            if content != old:
                sanitized.append(name)
                entries[name] = content.encode('utf-8')
    manifest = {'prepared_date': '2026-11-07', 'purpose': 'Revised research resource and reproducibility package; no Kaggle submission performed', 'files': [{'path': name, 'bytes': len(data), 'sha256': sha(data), 'sanitized_local_paths': name in sanitized} for name, data in sorted(entries.items())]}
    entries['FILE_MANIFEST.json'] = json.dumps(manifest, indent=2).encode()
    export = WORKSPACE / 'exports/PatchQuestions_Paper_Revision_2026-11-07.zip'
    with zipfile.ZipFile(export, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    with zipfile.ZipFile(export) as z:
        assert z.testzip() is None
        for item in manifest['files']:
            assert sha(z.read(item['path'])) == item['sha256']
        assert not any(b'Inspection Br' in z.read(name) for name in z.namelist())
    export.with_suffix('.sha256').write_text(sha(export.read_bytes()) + '  ' + export.name + '\n', encoding='utf-8')
    report = {'archive': str(export), 'bytes': export.stat().st_size, 'sha256': sha(export.read_bytes()), 'payloads': len(manifest['files']), 'word_counts': counts, 'source_modules_original': len(original_modules), 'notebook_modules': len(modules), 'notebook_code_cells_executed': 16, 'pilot_regression_tests': 12, 'integrity': 'passed'}
    (ROOT / 'verification/RELEASE.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
