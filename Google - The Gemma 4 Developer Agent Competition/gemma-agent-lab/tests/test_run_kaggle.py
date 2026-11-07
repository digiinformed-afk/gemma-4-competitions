import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'run-kaggle.py'
spec = importlib.util.spec_from_file_location('run_kaggle', SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class KaggleRunnerTests(unittest.TestCase):
    def test_sample_assets_hash_allows_only_the_builder_overlay(self):
        base = {'agent.yaml': 'a', 'prompts/base.md': 'b', 'skills/probe/scripts/probe.py': 'c'}
        variant = {**base, 'agent.yaml': 'd', 'prompts/root-repair-policy.md': 'e'}
        self.assertEqual(runner.sample_assets_hash(base), runner.sample_assets_hash(variant))
        variant['skills/probe/scripts/probe.py'] = 'different'
        self.assertNotEqual(runner.sample_assets_hash(base), runner.sample_assets_hash(variant))

    def setUp(self):
        self.tasks = [SimpleNamespace(instance_id=f'i{x}', repo=f'org/r{x}', patch='test-only sentinel')
                      for x in range(3)]
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name)
        (self.output / 'rows').mkdir()

    def test_frozen_schedule_resolves_dataset_order_and_rejects_extra_fields(self):
        self.assertEqual(runner.resolve_schedule([{'instance_id': 'i2', 'repo': 'org/r2'}, 'i0'],
                                                 self.tasks), [self.tasks[2], self.tasks[0]])
        bad = [['i0', 'i0'], ['missing'], [], [{'instance_id': 'i0', 'repo': 'wrong'}],
               [{'instance_id': 'i0', 'repo': 'org/r0', 'patch': 'gold'}]]
        for schedule in bad:
            with self.subTest(schedule=schedule), self.assertRaises(ValueError):
                runner.resolve_schedule(schedule, self.tasks)

    def test_cells_accept_only_reviewed_setup_and_skip_other_code(self):
        path = self.output / 'starter.ipynb'
        cells = [dict(cell_type='code', source=s) for s in [['setup\r\n'], 'serve', 'other']]
        runner.write_json(path, {'cells': cells})
        with patch.object(runner, 'INSTALL', runner.digest('setup')), patch.object(runner, 'SERVE', runner.digest('serve')):
            selected = runner.official_cells(path)
            self.assertEqual(set(selected.values()), {'setup', 'serve'})
            cells[0]['source'] = 'setup\nextra()'
            runner.write_json(path, {'cells': cells})
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                runner.official_cells(path)

    def test_official_result_classification(self):
        task = self.tasks[0]
        result = SimpleNamespace(instance_id='i0', repo='org/r0', tool_calls=4)
        cases = [(True, 'x', 0, None, 'resolved'),
                 (False, 'x', 1, None, 'test_failure'), (False, '', 0, None, 'empty_patch'),
                 (False, 'x', 1, 'Failed to apply agent patch: line 4', 'invalid_patch'),
                 (False, '', -1, 'Agent exceeded session timeout (1.0 min)', 'timeout'),
                 (False, 'x', 1, 'unclassified verifier error', 'unresolved')]
        for resolved, agent_patch, exit_code, error, expected in cases:
            with self.subTest(expected=expected):
                result.resolved, result.agent_patch = resolved, agent_patch
                result.test_exit_code, result.error = exit_code, error
                row = runner.result_row(task, result, 10.0)
                self.assertEqual(row['outcome'], expected)
                self.assertIsNone(row['tool_errors'])
                self.assertNotIn('patch', row)
        result.instance_id = 'i1'
        with self.assertRaisesRegex(ValueError, 'different task'):
            runner.result_row(task, result, 1.0)

    def test_deadline_preserves_finished_task_and_marks_only_active_task_timed_out(self):
        row = dict(instance_id='i0', outcome='resolved', seconds=2.0, tool_errors=None)
        runner.write_json(self.output / 'rows' / '000001.json', row)
        runner.write_json(self.output / 'active.json', dict(instance_id='i1', started_monotonic=10))
        runner.write_json(self.output / 'prepared.json', {'schedule': [t.instance_id for t in self.tasks]})
        with patch.object(runner.time, 'monotonic', return_value=13):
            runner.finalize(self.output, 'budget_exhausted', started=0)
        rows = [json.loads(line) for line in (self.output / 'results.jsonl').read_text().splitlines()]
        self.assertEqual([r['instance_id'] for r in rows], ['i0', 'i1'])
        self.assertEqual((rows[1]['outcome'], rows[1]['seconds']), ('timeout', 3))
        manifest = runner.read_json(self.output / 'manifest.json')
        self.assertEqual(manifest['elapsed_wall_seconds'], 13)
        self.assertEqual(manifest['schedule'], ['i0', 'i1', 'i2'])

    def test_deadline_after_row_commit_does_not_double_count_and_failure_is_diagnostic(self):
        row = dict(instance_id='i0', outcome='resolved', seconds=2.0, tool_errors=None)
        runner.write_json(self.output / 'rows' / '000001.json', row)
        runner.write_json(self.output / 'active.json', dict(instance_id='i0', started_monotonic=0))
        with patch.object(runner.time, 'monotonic', return_value=2):
            runner.finalize(self.output, 'worker_failed', started=0)
        self.assertEqual((self.output / 'results.jsonl').read_text().count('\n'), 1)
        self.assertFalse((self.output / 'manifest.json').exists())
        self.assertEqual(runner.read_json(self.output / 'status.json')['status'], 'worker_failed')

    def test_interrupted_run_keeps_committed_rows_and_freezes_pending_ids(self):
        schedule = [dict(instance_id=t.instance_id, repo=t.repo) for t in self.tasks]
        runner.write_json(self.output / 'prepared.json', {'schedule': schedule})
        runner.write_json(self.output / 'rows' / '000001.json', dict(instance_id='i0', outcome='resolved'))
        runner.write_json(self.output / 'active.json', dict(instance_id='i1'))
        remaining = self.output / 'remaining.json'
        report = runner.recover(self.output, remaining)
        self.assertEqual((report['committed'], report['committed_resolved']), (1, 1))
        self.assertEqual(runner.read_json(remaining), schedule[1:])
        self.assertFalse(report['has_final_manifest'])
        with self.assertRaises(FileExistsError):
            runner.recover(self.output, remaining)


if __name__ == '__main__':
    unittest.main()
