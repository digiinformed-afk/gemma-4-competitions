"""Scoring, secrecy, failure-denominator and recovery regression checks."""
from pathlib import Path
import copy
import io
import json
import random
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'paper' if (ROOT / 'paper').is_dir() else ROOT.parent / 'public/project'
sys.path.insert(0, str(PAPER))
import pilot


class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = pilot.load_cases(PAPER / 'frozen_cases.jsonl.gz')
        cls.info = {'served_model': 'scripted-fixture', 'model_revision': 'fixture-only', 'tokenizer_revision': 'fixture-only', 'quantization': 'none', 'serving_stack': 'test-double', 'hardware': 'CPU fixture', 'context_tokens': 100000, 'max_tokens': 64, 'temperature': 0, 'top_p': 1, 'seed': 7, 'timeout_seconds': 10}

    def session(self, family='wrap', split=43, target=10, view='named'):
        c = self.cases[family, split]
        order = list(range(len(c['configs'])))
        random.Random(2026).shuffle(order)
        return pilot.Session(c, target, order, view, 9123)

    def test_inconsistent_heldout_success_is_primary_failure(self):
        s = self.session()
        s.step({'ask': 9})
        _, grade = s.step({'pick': s.order.index(14)})
        self.assertTrue(grade['heldout_exact'])
        self.assertFalse(grade['query_consistent'])
        self.assertFalse(grade['success'])

    def test_target_pick_succeeds(self):
        s = self.session()
        s.step({'ask': 9})
        _, grade = s.step({'pick': s.key})
        self.assertTrue(grade['success'])
        self.assertTrue(grade['identity_exact'])

    def test_invalid_json_and_types(self):
        for value in ['[]', 'null', '{"ask":true}', '{"pick":1.0}', '{"ask":0,"pick":1}', '{"ask":0,"ask":1}', 'text {"pick":0}', '{"ask":NaN}']:
            with self.subTest(value=value), self.assertRaises(pilot.ProtocolError):
                pilot.parse_action(value)

    def test_repeated_query_and_out_of_range(self):
        s = self.session()
        s.step({'ask': 0})
        for action in [{'ask': 0}, {'ask': -1}, {'ask': 999}, {'pick': -1}, {'pick': 999}]:
            with self.assertRaises(pilot.ProtocolError):
                s.step(action)

    def test_three_asks_then_pick(self):
        s = self.session()
        for j in range(3):
            s.step({'ask': j})
        with self.assertRaises(pilot.ProtocolError):
            s.step({'ask': 3})
        self.assertTrue(s.step({'pick': s.key})[1]['success'])
        with self.assertRaises(pilot.ProtocolError):
            s.step({'pick': s.key})

    def test_model_input_whitelist_and_no_private_grade(self):
        s = self.session()
        self.assertEqual(set(s.initial), {'inputs', 'outputs', 'budget', 'instructions'})
        messages = [{'role': 'user', 'content': pilot.encode(s.initial)}]
        req = pilot.model_request(messages, self.info)
        self.assertEqual(set(req), {'model', 'messages', 'temperature', 'top_p', 'seed', 'max_tokens', 'stream'})
        for forbidden in ['target', 'heldout_outputs', 'configs', 'family', 'session_id', 'tools', 'frozen_cases']:
            self.assertNotIn(forbidden, pilot.encode(req))
        req['messages'].clear()
        self.assertEqual(len(messages), 1)
        self.assertIsNone(s.step({'pick': s.key})[0])

    def test_masking_preserves_every_partition(self):
        a, b = self.session(), self.session(view='masked')
        for j in range(len(a.grid[0])):
            for i in range(len(a.grid)):
                for k in range(len(a.grid)):
                    self.assertEqual(a.grid[i][j] == a.grid[k][j], b.grid[i][j] == b.grid[k][j])
        self.assertEqual(pilot.baseline(a, 'entropy'), pilot.baseline(b, 'entropy'))

    def test_matched_old_sample_baselines(self):
        values = {p: [] for p in ['entropy', 'random_split']}
        for (family, split), c in self.cases.items():
            if split != 19:
                continue
            for target in [0, 1]:
                session = pilot.Session(c, target, list(range(len(c['configs']))), 'named')
                for p in values:
                    values[p].append(pilot.baseline(session, p)['success'])
        self.assertAlmostEqual(sum(values['entropy']) / 16, .875)
        self.assertAlmostEqual(sum(values['random_split']) / 16, .7991009931139931, places=7)

    def test_plan_pairing_and_private_sampling(self):
        plan = pilot.make_plan(self.cases, 'hash-fixture', self.info, seed=1)
        self.assertEqual(len(plan['schedule']), 32)
        for i in range(0, 32, 2):
            a, b = plan['schedule'][i:i+2]
            self.assertEqual((a['pair_id'], a['target'], a['order']), (b['pair_id'], b['target'], b['order']))
            self.assertNotEqual(a['view'], b['view'])
        for name in {x['family'] for x in plan['schedule']}:
            entries = [x for x in plan['schedule'] if x['family'] == name and x['view'] == 'named']
            n = len(self.cases[name, 19]['configs'])
            self.assertEqual(sum(x['target'] < n // 2 for x in entries), 1)

    def test_unstarted_sessions_remain_in_denominator(self):
        plan = pilot.make_plan(self.cases, 'hash-fixture', self.info, seed=2)
        first = plan['schedule'][0]
        row = {'session_id': first['session_id'], 'status': 'completed', 'success': True, 'heldout_exact': True}
        summary = pilot.summarize(plan, [row])
        self.assertEqual(summary['scheduled'], 32)
        self.assertEqual(summary['unstarted_or_interrupted'], 31)
        self.assertEqual(summary['conditions'][first['view']]['denominator'], 16)
        with self.assertRaises(ValueError):
            pilot.summarize(plan, [row, row])

    def test_remote_endpoint_rejected_before_import_or_network(self):
        with self.assertRaises(ValueError):
            pilot.run(Path('missing'), Path('missing'), 'https://example.com', Path('missing'), Path('missing'))

    def test_transport_logs_truncation_and_missing_sessions(self):
        data = PAPER / 'frozen_cases.jsonl.gz'
        plan = pilot.make_plan(self.cases, pilot.sha(data.read_bytes()), self.info, seed=3)
        plan['schedule'] = plan['schedule'][:2]
        responses = [json.dumps({'choices': [{'finish_reason': 'length', 'message': {'content': '{"pick":0}'}}]}).encode()] * 2
        class Tokenizer:
            def apply_chat_template(self, *args, **kwargs):
                return [1, 2]
        class Opener:
            def open(self, request, timeout):
                body = json.loads(request.data)
                self_outer.assertNotIn('tools', body)
                return io.BytesIO(responses.pop())
        self_outer = self
        fake = types.SimpleNamespace(AutoTokenizer=types.SimpleNamespace(from_pretrained=lambda *a, **k: Tokenizer()))
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            folder = Path(tmp)
            pilot.save_json(folder / 'plan.json', plan)
            with patch.dict(sys.modules, {'transformers': fake}), patch.object(pilot, 'build_opener', return_value=Opener()):
                pilot.run(folder / 'plan.json', data, 'http://127.0.0.1:8000', folder, folder / 'run')
            summary = json.loads((folder / 'run/SUMMARY.json').read_text())
            self.assertEqual(sum(x['successes'] for x in summary['conditions'].values()), 0)
            for path in (folder / 'run').glob('*.result.json'):
                row = json.loads(path.read_text())
                self.assertEqual(row['error'], 'output_truncated')
            self.assertEqual(len(list((folder / 'run').glob('*.events.jsonl'))), 2)


class GPUPlanTests(unittest.TestCase):
    setUpClass = classmethod(PilotTests.setUpClass.__func__)
    session = PilotTests.session
    def test_tokenizer_mapping_is_counted_by_ids(self):
        class Tokenizer:
            def apply_chat_template(self, *args, **kwargs):
                assert kwargs['return_dict'] is False
                return {'input_ids': [[1, 2, 3, 4, 5]], 'attention_mask': [[1]*5]}
        self.assertEqual(pilot.count_tokens(Tokenizer(), [], self.info), 5)

    def test_controls_match_targets_and_zero_budget(self):
        plan = pilot.make_plan(self.cases, 'hash', self.info, seed=9, controls=True)
        self.assertEqual(len(plan['schedule']), 64)
        entries = [e for e in plan['schedule'] if e.get('arm') == 'zero']
        self.assertEqual(len(entries), 16)
        session = pilot.new_session(self.cases, entries[0])
        with self.assertRaises(pilot.ProtocolError):
            session.step({'ask': 0})
        self.assertTrue(session.step({'pick': session.key})[1]['success'])

    def test_incomplete_pair_is_excluded_from_complete_analysis(self):
        plan = pilot.make_plan(self.cases, 'hash', self.info, seed=9)
        first = plan['schedule'][0]
        summary = pilot.summarize(plan, [{'session_id': first['session_id'], 'success': True}])
        self.assertEqual(summary['paired_complete']['pairs'], 0)
        self.assertEqual(summary['paired_complete']['ties'], 0)
        self.assertEqual(summary['paired_failure_inclusive']['incomplete_pairs'], 16)

    def test_entropy_question_uses_visible_survivors(self):
        s = self.session()
        while len(s.asked) < 3:
            j = pilot.entropy_question(s)
            if j is None:
                break
            before = len(s.survivors)
            s.step({'ask': j})
            self.assertLess(len(s.survivors), before)
        self.assertIn(s.key, s.survivors)

    def test_transcript_replays_and_detects_tampered_grade(self):
        data = PAPER / 'frozen_cases.jsonl.gz'
        plan = pilot.make_plan(self.cases, pilot.sha(data.read_bytes()), self.info, seed=11)
        plan['schedule'] = plan['schedule'][:1]
        spec = plan['schedule'][0]
        session = pilot.new_session(self.cases, spec)
        action = {'pick': session.key}
        _, grade = session.step(action)
        with tempfile.TemporaryDirectory() as folder:
            d = Path(folder)
            pilot.save_json(d/'plan.json', plan)
            (d/'events.jsonl').write_text(pilot.encode({'action': action})+'\n')
            row = dict(grade, session_id=spec['session_id'], transcript='events.jsonl')
            pilot.save_json(d/(spec['session_id']+'.result.json'), row)
            self.assertEqual(pilot.replay(d, data)['recorded'], 1)
            row['success'] = False
            (d/(spec['session_id']+'.result.json')).write_text(pilot.encode(row))
            with self.assertRaises(ValueError):
                pilot.replay(d, data)


if __name__ == '__main__':
    unittest.main()
