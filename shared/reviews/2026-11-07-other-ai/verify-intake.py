"""Record the returned review and verify its stored evidence without running it."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import csv
import gzip
import hashlib
import io
import json
import shutil
import statistics
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    incoming = ROOT / 'incoming'
    incoming.mkdir(exist_ok=True)
    receipts = []
    for name in ['PatchQuestions_Research_Review.md', 'PatchQuestions_Review_Progress.zip']:
        source = WORKSPACE / name
        data = source.read_bytes()
        target = incoming / name
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f'Refusing to replace an existing receipt: {target}')
        if not target.exists():
            shutil.copyfile(source, target)
        receipts.append({'file': name, 'bytes': len(data), 'sha256': digest(data)})

    checks = {}
    with zipfile.ZipFile(incoming / receipts[1]['file']) as z:
        entries = z.infolist()
        names = [item.filename for item in entries]
        assert len(names) == len(set(names)), 'Duplicate ZIP paths'
        assert sum(item.file_size for item in entries) < 50_000_000
        for item in entries:
            path = PurePosixPath(item.filename)
            assert not path.is_absolute() and '..' not in path.parts
            assert '\\' not in item.filename and ':' not in item.filename
            assert (item.external_attr >> 16) & 0o170000 != 0o120000
        assert z.testzip() is None, 'ZIP CRC failure'
        checks['zip_members'] = len(entries)
        checks['zip_crc_passed'] = True
        manifest = json.loads(z.read('reference/FILE_MANIFEST.json'))
        for item in manifest['files']:
            data = z.read('reference/' + item['path'])
            assert len(data) == item['bytes']
            assert digest(data) == item['sha256'], item['path']
        checks['reference_manifest_files_verified'] = len(manifest['files'])
        original = WORKSPACE / 'exports/PatchQuestions_AI_Review_2026-11-07.zip'
        checks['original_review_package_sha256'] = digest(original.read_bytes())
        with zipfile.ZipFile(original) as old:
            for item in manifest['files']:
                assert old.read(item['path']) == z.read('reference/' + item['path'])
        checks['all_reference_payloads_match_original_export'] = True
        for name in ['scores.csv', 'summary.json', 'audit.json', 'intervention.json']:
            assert z.read('reference/paper/' + name) == z.read('run_cpython_3_12_14/' + name)
        checks['stored_reproduction_byte_matches'] = ['scores.csv', 'summary.json', 'audit.json', 'intervention.json']
        frozen = [json.loads(line) for line in gzip.decompress(z.read('reference/paper/frozen_cases.jsonl.gz')).splitlines()]
        fresh = [json.loads(line) for line in gzip.decompress(z.read('run_cpython_3_12_14/fresh_cases.jsonl.gz')).splitlines()]
        assert frozen == fresh
        checks['fresh_matrix_records_equal_reference'] = len(frozen)

        rows = list(csv.DictReader(io.StringIO(z.read('reference/paper/scores.csv').decode())))
        checks['reference_score_rows'] = len(rows)
        effects = json.loads(z.read('reviewer_checks/effects_redundancy_sensitivity.json'))
        macro = {}
        for policy in sorted({r['policy'] for r in rows}):
            groups = defaultdict(list)
            for row in rows:
                if row['policy'] == policy and int(row['budget']) == 3:
                    groups[row['family']].append(row)
            macro[policy] = {}
            for metric in ['heldout_exact', 'queries_used']:
                value = statistics.fmean(statistics.fmean(float(r[metric]) for r in rs) for rs in groups.values())
                assert abs(value - effects['budget3'][policy][metric]) < 1e-12
                macro[policy][metric] = value
        checks['independently_recomputed_budget3_macro'] = macro
        checks['question_saving_vs_tree_percent'] = 100 * (macro['lookahead']['queries_used'] - macro['frugal']['queries_used']) / macro['lookahead']['queries_used']
        checks['question_saving_vs_entropy_percent'] = 100 * (macro['entropy']['queries_used'] - macro['frugal']['queries_used']) / macro['entropy']['queries_used']

        crossed = list(csv.DictReader(io.StringIO(z.read('reviewer_checks/crossed_probe_rows.csv').decode())))
        grouped = defaultdict(list)
        for row in crossed:
            grouped[row['scoring_suite'], row['pool'], row['policy'], int(row['budget'])].append(row)
        summary = json.loads(z.read('reviewer_checks/crossed_probe_results.json'))
        for item in summary['results']:
            rs = grouped[item['scoring_suite'], item['pool'], item['policy'], item['budget']]
            for field, column in [('heldout_exact', 'heldout_exact'), ('queries', 'queries_used')]:
                assert abs(statistics.fmean(float(r[column]) for r in rs) - item[field]) < 1e-12
        checks['crossed_score_rows'] = len(crossed)
        checks['crossed_summary_cells_verified'] = len(summary['results'])
        checks['crossed_budget3_entropy_frugal'] = [r for r in summary['results'] if r['budget'] == 3 and r['policy'] in ['entropy', 'frugal']]

        classes = []
        canonical = lambda row: json.dumps(row, sort_keys=True, ensure_ascii=True)
        for case in frozen:
            q = list(map(canonical, case['query_outputs']))
            h = list(map(canonical, case['heldout_outputs']))
            classes.append({'family': case['family'], 'split': case['split'], 'configurations': len(q), 'joint_classes': len(set(zip(q, h)))})
        checks['independently_counted_behavior_classes'] = classes
        assert all(c['joint_classes'] == (30 if c['family'] == 'hex_format' else c['configurations']) for c in classes)
        fixture = json.loads(z.read('reviewer_checks/protocol_validation.json'))['inconsistent_pick_fixture']
        case = next(c for c in frozen if c['family'] == fixture['family'] and c['split'] == fixture['split'])
        t, p, j = fixture['target'], fixture['picked_original_candidate'], fixture['query']
        assert case['query_outputs'][t][j] != case['query_outputs'][p][j]
        assert case['heldout_outputs'][t] == case['heldout_outputs'][p]
        checks['inconsistent_pick_fixture_confirmed_against_frozen_data'] = {'family': case['family'], 'split': case['split'], 'target': t, 'picked_original_candidate': p, 'query': j}

        checks['reviewer_claimed_random_validation'] = json.loads(z.read('reviewer_checks/random_path_validation.json'))
        checks['reviewer_claimed_tree_validation'] = json.loads(z.read('reviewer_checks/tree_enumeration_validation.json'))
        checks['final_review_missing_from_returned_zip'] = 'PatchQuestions_Research_Review.md' not in names
        checks['reference_manuscript_is_unchanged_original'] = True
        checks['archive_member_hashes'] = [{'path': item.filename, 'bytes': item.file_size, 'sha256': digest(z.read(item.filename))} for item in entries]

    report = {
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'runtime': sys.version,
        'scope': 'Receipt integrity, stored reproduction equality, independent aggregation and frozen-data checks. No attached Python code executed; no new CPython 3.12 reproduction, notebook kernel execution, model session or repository repair performed.',
        'incoming_files': receipts,
        'checks': checks,
    }
    target = ROOT / 'INTAKE-VERIFICATION.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in checks.items() if k not in ['archive_member_hashes', 'independently_counted_behavior_classes', 'crossed_budget3_entropy_frugal']}, indent=2))


if __name__ == '__main__':
    main()
