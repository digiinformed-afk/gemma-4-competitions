"""Run inspected reviewer checks in a new directory, retaining all logs."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import time
import zipfile
import argparse

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-name', default='local-cpython312')
    parser.add_argument('--utf8-reviewer', action='store_true')
    args = parser.parse_args()
    assert '/' not in args.run_name and '\\' not in args.run_name and args.run_name not in {'.', '..'}
    run = ROOT / 'verification' / args.run_name
    run.mkdir(parents=True, exist_ok=False)
    incoming = WORKSPACE / 'PatchQuestions_Review_Progress.zip'
    with zipfile.ZipFile(incoming) as z:
        for item in z.infolist():
            if item.filename.startswith('reference/paper/') and not item.is_dir():
                relative = Path(item.filename)
                assert '..' not in relative.parts
                target = run / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(item.filename))
        for name in ['reviewer_audit.py', 'protocol_audit.py']:
            (run / name).write_bytes(z.read(name))
    if args.utf8_reviewer:
        path = run / 'reviewer_audit.py'
        shutil.copyfile(path, run / 'reviewer_audit.original.py')
        original = path.read_text(encoding='utf-8')
        needle = "source=(REF/'benchmark.py').read_text()"
        assert original.count(needle) == 1
        modified = original.replace(needle, "source=(REF/'benchmark.py').read_text(encoding='utf-8')")
        modified = modified.replace(".write_text(modified)", ".write_text(modified, encoding='utf-8')")
        path.write_text(modified, encoding='utf-8')
    source = run / 'reference/paper'
    fresh = run / 'run_cpython_3_12_14'
    fresh.mkdir()
    for p in source.glob('*.py'):
        shutil.copyfile(p, fresh / p.name)
    shutil.copyfile(source / 'frozen_cases.jsonl.gz', fresh / 'frozen_cases_reference.jsonl.gz')
    record = {'runtime': sys.version, 'platform': sys.platform, 'runs': [], 'comparisons': {}, 'reviewer_portability_edit': "Explicit UTF-8 for reading/writing benchmark source in dynamic timing variants; untouched original preserved" if args.utf8_reviewer else None}
    commands = [(['benchmark.py'], fresh, 'summary.json'), (['analyze.py'], fresh, 'audit.json'), (['intervention.py'], fresh, 'intervention.json'), (['verify.py'], fresh, 'verify.txt'), (['export_cases.py'], fresh, 'export.txt'), (['cognitive_probe.py', '--check'], fresh, 'cognitive-check.txt'), (['reviewer_audit.py'], run, 'reviewer_audit.stdout.txt'), (['protocol_audit.py'], run, 'protocol_audit.stdout.txt')]
    for args, cwd, output in commands:
        started = time.perf_counter()
        result = subprocess.run([sys.executable, '-B', *args], cwd=cwd, capture_output=True)
        (cwd / output).write_bytes(result.stdout)
        (cwd / (args[0] + '.stderr.txt')).write_bytes(result.stderr)
        record['runs'].append({'argv': ['python', '-B', *args], 'cwd': str(cwd.relative_to(run)), 'returncode': result.returncode, 'wall_seconds': time.perf_counter() - started})
        (run / 'EXECUTION-RECORD.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
        print(args[0], result.returncode, flush=True)
        if result.returncode:
            raise RuntimeError(result.stderr.decode(errors='replace'))
    for name in ['summary.json', 'audit.json', 'intervention.json', 'scores.csv']:
        original, actual = (source / name).read_bytes(), (fresh / name).read_bytes()
        equal = json.loads(original) == json.loads(actual) if name.endswith('.json') else original == actual
        assert equal, name
        record['comparisons'][name] = {'semantic_equal': equal, 'byte_equal': original == actual, 'actual_sha256': hashlib.sha256(actual).hexdigest()}
    record['scope'] = 'Fresh same-version Windows execution. JSON parsed equality accommodates Windows stdout newlines; source/reference data preserved unchanged. No model session.'
    (run / 'EXECUTION-RECORD.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record['comparisons'], indent=2))


if __name__ == '__main__':
    main()
