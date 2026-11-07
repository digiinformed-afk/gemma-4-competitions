"""Reproduce the revised paper in a new directory, preserving reference files."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--paper', type=Path, default=Path(__file__).resolve().parent.parent / 'public/project')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    source, output = a.paper.resolve(), a.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    for f in source.glob('*.py'):
        shutil.copyfile(f, output / f.name)
    shutil.copyfile(source / 'frozen_cases.jsonl.gz', output / 'frozen_cases_reference.jsonl.gz')
    record = {'runtime': sys.version, 'source_files': {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in source.glob('*.py')}, 'runs': []}
    commands = [(['benchmark.py'], 'summary.json'), (['analyze.py'], 'audit.json'), (['intervention.py'], 'intervention.json'), (['verify.py'], 'verify.txt'), (['export_cases.py'], 'export.txt'), (['paper_analysis.py'], 'revision-analysis.txt')]
    for args, stdout in commands:
        start = time.perf_counter()
        r = subprocess.run([sys.executable, '-B', *args], cwd=output, capture_output=True)
        (output / stdout).write_bytes(r.stdout)
        (output / (args[0] + '.stderr.txt')).write_bytes(r.stderr)
        record['runs'].append({'argv': ['python', '-B', *args], 'returncode': r.returncode, 'wall_seconds': time.perf_counter() - start})
        (output / 'REPRODUCTION.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
        if r.returncode:
            raise RuntimeError(r.stderr.decode(errors='replace'))
    equal_matrices = gzip.decompress((output / 'frozen_cases.jsonl.gz').read_bytes()) == gzip.decompress((source / 'frozen_cases.jsonl.gz').read_bytes())
    record['reference_comparison'] = {'scores_byte_equal': (output / 'scores.csv').read_bytes() == (source / 'scores.csv').read_bytes(), 'frozen_records_equal': equal_matrices, **{name: json.loads((source / name).read_bytes()) == json.loads((output / name).read_bytes()) for name in ['summary.json', 'audit.json', 'intervention.json']}}
    # The presentation control always uses the pinned frozen resource.
    shutil.copyfile(output / 'frozen_cases.jsonl.gz', output / 'runtime_frozen_cases.jsonl.gz')
    shutil.copyfile(source / 'frozen_cases.jsonl.gz', output / 'frozen_cases.jsonl.gz')
    r = subprocess.run([sys.executable, '-B', 'cognitive_probe.py', '--check'], cwd=output, capture_output=True)
    (output / 'cognitive-check.txt').write_bytes(r.stdout)
    (output / 'cognitive-check.stderr.txt').write_bytes(r.stderr)
    record['presentation_control_returncode'] = r.returncode
    (output / 'REPRODUCTION.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    if r.returncode:
        raise RuntimeError(r.stderr.decode(errors='replace'))
    print(json.dumps(record['reference_comparison'], indent=2))


if __name__ == '__main__':
    main()
