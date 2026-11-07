"""Create an explicit-file-list review bundle without changing paper originals."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parents[1]
source = root / 'Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/public/project'
out = root / 'exports'
out.mkdir(exist_ok=True)
destination = out / 'PatchQuestions_AI_Review_2026-11-07.zip'
if destination.exists():
    raise SystemExit('Refusing to overwrite existing review package.')
entries = {}
for p in sorted(source.iterdir()):
    if p.is_file() and p.suffix.lower() in {'.py', '.md', '.json', '.csv', '.ipynb', '.gz', '.png'}:
        entries['paper/' + p.name] = p.read_bytes()
for name in ['PROGRAM-PLAN.md', 'RESEARCH-REVIEW.md', 'EXPERIMENT-PROTOCOL.md', 'REQUIREMENTS-COVERAGE.md']:
    entries['context/' + name] = (root / 'shared' / name).read_bytes()
entries['REVIEW_PROMPT.md'] = (root / 'shared/OTHER-AI-PAPER-REVIEW-PROMPT.md').read_bytes()
for p in sorted((root / 'shared/verification/2026-11-07-python315').iterdir()):
    if p.is_file() and p.suffix in {'.json', '.csv', '.txt'}:
        value = p.read_text(encoding='utf-8')
        for prefix in [str(root), str(root).replace('\\', '\\\\')]:
            value = value.replace(prefix, '<WORKSPACE>')
        for prefix in [r'C:\Users\Inspection Br', r'C:\\Users\\Inspection Br']:
            value = value.replace(prefix, '<USER_PROFILE>')
        entries['verification/python-3.15.2/' + p.name] = value.encode('utf-8')
entries['START_HERE.md'] = b'''# PatchQuestions: external AI review bundle

Prepared 7 November 2026. This is a review package, not a Kaggle submission.

## Use

Upload the ZIP to the reviewing AI and paste REVIEW_PROMPT.md. It asks 28 difficult research questions and requires answers, evidence, counterexamples and practical improvements.

## Reading order

1. REVIEW_PROMPT.md: complete review assignment.
2. paper/PatchQuestions_Writeup.md: current manuscript.
3. paper/README.md, Python modules and PatchQuestions.ipynb: implementation and reproduction.
4. paper/scores.csv, summary.json, audit.json, intervention.json: original reference results.
5. context/RESEARCH-REVIEW.md: closest prior art and novelty risks.
6. context/EXPERIMENT-PROTOCOL.md: proposed Gemma pilot.
7. context/REQUIREMENTS-COVERAGE.md: official source review and access gaps.
8. verification/python-3.15.2/: separate cross-runtime rerun and audit.

The newer cognitive_probe.py, cognitive-core-study.md and research notes are included, unlike the older research ZIP. Embedded paths in historical notes may reflect the original workspace; use this reading map instead. This package grants no new license and does not publish the work.

## Evidence boundaries

The draft attributes reference measurements to CPython 3.12.14. paper/cross_version_summary.json records historical 3.13.5 results. The separate 3.15.2 rerun reproduced entropy/tree aggregates but has small random-policy differences. Keep runtimes separate; do not claim a fresh 3.12.14 reproduction.

The 18,000 reference rows represent 750 target/split conditions on eight families, six policies and four budgets. These are not 750 independent bugs. The benchmark assumes a correct candidate and perfect labels; candidate execution costs and human time are separate from question count.

No Gemma pilot, human-time study, real-repository repair evaluation or leaderboard submission has been completed. The proposed 32-session pilot is a feasibility study. The entropy masking check is a control, not a model result.

## Competition context

Recorded paper deadline: 12 November 2026 23:59 UTC / 13 November 04:59 PKT. Report maximum: 3,000 words. Original unpublished research and an explicitly submitted Kaggle Writeup are required. Five equally weighted dimensions: Novelty, Quality, Relevance, Verifiability and Clarity. Recheck current sources rather than assuming the schedule remains unchanged.

- https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview
- https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules
- https://www.kaggle.com/competitions/gemma-4-developer-agent/overview
- https://www.kaggle.com/competitions/gemma-4-developer-agent/rules

Full HARNESS_README, actual official sample files and exact model terms are not included or claimed reviewed. Source summaries are included, not downloaded copies of all papers or rules. Report source-access limitations honestly.

## Reproduction and integrity

Copy the Python modules into a fresh writable run directory and execute the documented commands there. Do not replace reference results. Put frozen_cases.jsonl.gz beside cognitive_probe.py for its --check control. The frozen archive contains grading outputs: never expose it to an evaluated model with filesystem access.

FILE_MANIFEST.json lists SHA-256 hashes and byte counts of every payload except itself. Original paper files are unchanged copies. Local user/workspace paths in verification copies were replaced with placeholders. No dashboard databases, API keys, account credentials, private uploads or restricted Kaggle datasets are bundled.
'''
manifest = {'prepared_date': '2026-11-07', 'purpose': 'External AI review, not competition submission',
    'files': [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
               'sanitized': name.startswith('verification/')} for name, data in sorted(entries.items())]}
entries['FILE_MANIFEST.json'] = json.dumps(manifest, indent=2).encode('utf-8')
with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in sorted(entries.items()):
        archive.writestr(name, data)
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(entries)
    for item in manifest['files']:
        assert hashlib.sha256(archive.read(item['path'])).hexdigest() == item['sha256']
    assert not any(name.endswith('.zip') or '..' in Path(name).parts for name in archive.namelist())
    assert not any(b'Inspection Br' in archive.read(name) for name in archive.namelist())
(out / 'OTHER-AI-PAPER-REVIEW-PROMPT.md').write_bytes(entries['REVIEW_PROMPT.md'])
(out / 'PatchQuestions_AI_Review_START_HERE.md').write_bytes(entries['START_HERE.md'])
checksum = hashlib.sha256(destination.read_bytes()).hexdigest()
(out / 'PatchQuestions_AI_Review_2026-11-07.sha256').write_text(checksum + '  ' + destination.name + '\n', encoding='utf-8')
print(json.dumps({'archive': str(destination), 'bytes': destination.stat().st_size,
                  'entries': len(entries), 'sha256': checksum, 'integrity': 'passed'}, indent=2))
