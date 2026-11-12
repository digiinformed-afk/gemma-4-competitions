"""Strict frozen-matrix supervisor. No learned-model results are bundled.

Core commands and tests use the standard library. Live inference additionally
needs a local Hugging Face tokenizer and a local chat-completions HTTP server.
The evaluated completion model receives text only and has no execution tools.
"""
import argparse
import copy
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import random
import secrets
import statistics
import time
from urllib.request import Request, urlopen, build_opener, ProxyHandler
from urllib.parse import urlparse

INSTRUCTION = 'Select a candidate from the displayed behavior matrix. Send exactly one JSON object: {"ask": column} or {"pick": row}. Indices start at zero. Each ask returns the intended output. Use at most three distinct asks, then pick a row consistent with every answer. You may pick early. No prose or other keys.'


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_cases(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return {(c['family'], c['split']): c for c in map(json.loads, f)}


class ProtocolError(ValueError):
    pass


def parse_action(raw):
    def unique(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ProtocolError('duplicate_key')
            obj[key] = value
        return obj
    try:
        action = json.loads(raw, object_pairs_hook=unique)
    except (ValueError, TypeError) as exc:
        raise ProtocolError('malformed_json') from exc
    if type(action) is not dict or len(action) != 1 or next(iter(action)) not in {'ask', 'pick'}:
        raise ProtocolError('invalid_keys')
    if type(next(iter(action.values()))) is not int:
        raise ProtocolError('noninteger_index')
    return action


class Session:
    def __init__(self, case, target, order, view, label_seed=0, budget=3):
        if sorted(order) != list(range(len(case['configs']))) or not 0 <= target < len(order):
            raise ValueError('invalid private episode')
        self.case, self.target, self.order = case, target, order
        self.key = order.index(target)
        named = [[encode(v) for v in case['query_outputs'][i]] for i in order]
        self.grid = copy.deepcopy(named)
        if view == 'masked':
            rng = random.Random(label_seed)
            for j in range(len(named[0])):
                values = list(dict.fromkeys(row[j] for row in named))
                labels = [f'v{k}' for k in range(len(values))]
                rng.shuffle(labels)
                mapping = dict(zip(values, labels))
                for i in range(len(order)):
                    self.grid[i][j] = mapping[named[i][j]]
        elif view != 'named':
            raise ValueError('unknown view')
        self.budget = budget
        self.asked = []
        self.survivors = list(range(len(order)))
        self.finished = False
        self.initial = {'inputs': case['query_inputs'] if view == 'named' else list(range(len(named[0]))), 'outputs': self.grid, 'budget': budget, 'instructions': INSTRUCTION if budget else 'Choose now. Send exactly one JSON object with a pick integer. No questions are available.'}

    def step(self, action):
        if self.finished:
            raise ProtocolError('already_finished')
        action = parse_action(encode(action))
        if 'ask' in action:
            j = action['ask']
            if not 0 <= j < len(self.grid[0]):
                raise ProtocolError('query_out_of_range')
            if j in self.asked:
                raise ProtocolError('repeated_query')
            if len(self.asked) >= self.budget:
                raise ProtocolError('budget_exceeded')
            self.asked.append(j)
            self.survivors = [i for i in self.survivors if self.grid[i][j] == self.grid[self.key][j]]
            return {'answer': self.grid[self.key][j]}, None
        row = action['pick']
        if not 0 <= row < len(self.order):
            raise ProtocolError('pick_out_of_range')
        self.finished = True
        held = self.case['heldout_outputs'][self.order[row]] == self.case['heldout_outputs'][self.target]
        consistent = row in self.survivors
        grade = {'status': 'completed', 'valid_completion': True, 'query_consistent': consistent, 'heldout_exact': held, 'success': consistent and held, 'identity_exact': self.order[row] == self.target, 'questions': len(self.asked), 'survivors': len(self.survivors)}
        return None, grade  # The private grade is never returned to the model.


def baseline(session, policy):
    grid, target = session.grid, session.key
    @lru_cache(None)
    def visit(ids, remaining, depth):
        choices = [j for j in remaining if len({grid[i][j] for i in ids}) > 1] if depth else []
        if not choices:
            held = session.case['heldout_outputs']
            score = sum(held[session.order[i]] == held[session.target] for i in ids) / len(ids)
            return score, 0.0
        if policy == 'entropy':
            def utility(j):
                from collections import Counter
                return -sum(n * math.log2(n) for n in Counter(grid[i][j] for i in ids).values())
            choices = [max(choices, key=utility)]
        values = [visit(tuple(i for i in ids if grid[i][j] == grid[target][j]), tuple(k for k in remaining if k != j), depth - 1) for j in choices]
        return statistics.fmean(v[0] for v in values), 1 + statistics.fmean(v[1] for v in values)
    if policy not in {'entropy', 'random_split'}:
        raise ValueError('unknown policy')
    score, questions = visit(tuple(range(len(grid))), tuple(range(len(grid[0]))), session.budget)
    return {'heldout_exact': score, 'success': score, 'questions': questions, 'final_selection': 'uniform among consistent survivors'}


def make_plan(cases, data_hash, info, seed=None, controls=False):
    required = {'served_model', 'model_revision', 'tokenizer_revision', 'quantization', 'serving_stack', 'hardware', 'context_tokens', 'max_tokens', 'temperature', 'top_p', 'seed', 'timeout_seconds'}
    if set(info) - {'chat_template_kwargs'} != required or any(value is None for value in info.values()):
        raise ValueError('model-info must contain exactly the documented fields with confirmed values')
    if any(type(info[k]) is not int or info[k] <= 0 for k in ['context_tokens', 'max_tokens', 'timeout_seconds']):
        raise ValueError('invalid limits')
    rng = random.Random(secrets.randbits(256) if seed is None else seed)
    episodes = []
    for f in sorted({f for f, split in cases if split == 19}):
        c = cases[f, 19]
        n = len(c['configs'])
        # One secret draw from each half of configuration order, per family.
        for target in [rng.randrange(n // 2), rng.randrange(n // 2, n)]:
            order = list(range(n))
            rng.shuffle(order)
            episodes.append({'pair_id': f'pair-{len(episodes):02}', 'family': f, 'split': 19, 'target': target, 'order': order, 'label_seed': rng.getrandbits(64)})
    rng.shuffle(episodes)
    schedule = []
    for i, episode in enumerate(episodes):
        for view in (['named', 'masked'] if i % 2 == 0 else ['masked', 'named']):
            schedule.append({**episode, 'view': view, 'session_id': episode['pair_id'] + '-' + view})
    if controls:
        extra = []
        for entry in schedule:
            if entry['view'] == 'named':
                for arm in ('zero', 'entropy_pick'):
                    extra.append({**entry, 'arm': arm, 'session_id': entry['pair_id'] + '-' + arm})
        rng.shuffle(extra)
        schedule.extend(extra)
    return {'schema': 2, 'created_utc': datetime.now(timezone.utc).isoformat(), 'data_sha256': data_hash, 'source_sha256': sha(Path(__file__).read_bytes()), 'instruction_sha256': sha(INSTRUCTION.encode()), 'model_info': info, 'retry_rule': 'No retries. Preserve all failures; corrected infrastructure requires a new run ID.', 'sampling': 'Two targets per family, stratified by configuration-index half; convenience feasibility sample, no population inference.', 'schedule': schedule}


def model_request(messages, info):
    # Explicit whitelist. No plan, target, grading data, tools or filenames.
    request = {'model': info['served_model'], 'messages': copy.deepcopy(messages), 'temperature': info['temperature'], 'top_p': info['top_p'], 'seed': info['seed'], 'max_tokens': info['max_tokens'], 'stream': False}
    if info.get('chat_template_kwargs'):
        request['chat_template_kwargs'] = copy.deepcopy(info['chat_template_kwargs'])
    return request


def summarize(plan, records):
    allowed = {s['session_id'] for s in plan['schedule']}
    if len({r['session_id'] for r in records}) != len(records) or any(r['session_id'] not in allowed for r in records):
        raise ValueError('duplicate or unscheduled result')
    keyed = {r['session_id']: r for r in records}
    output = {'scheduled': len(allowed), 'recorded': len(records), 'unstarted_or_interrupted': len(allowed) - len(records), 'conditions': {}}
    for view in ['named', 'masked']:
        ids = [s['session_id'] for s in plan['schedule'] if s['view'] == view and s.get('arm', 'free') == 'free']
        output['conditions'][view] = {'denominator': len(ids), 'successes': sum(bool(keyed.get(i, {}).get('success', False)) for i in ids), 'heldout_only_successes': sum(bool(keyed.get(i, {}).get('heldout_exact', False)) for i in ids), 'completed': sum(keyed.get(i, {}).get('status') == 'completed' for i in ids)}
    pairs = {}
    for entry in plan['schedule']:
        if entry.get('arm', 'free') == 'free':
            pairs.setdefault(entry['pair_id'], {})[entry['view']] = keyed.get(entry['session_id'])
    paired = {'named_wins': 0, 'masked_wins': 0, 'ties': 0, 'incomplete_pairs': 0}
    for pair in pairs.values():
        if any(pair.get(v) is None for v in ['named', 'masked']):
            paired['incomplete_pairs'] += 1
        a, b = [bool((pair.get(v) or {}).get('success', False)) for v in ['named', 'masked']]
        paired['ties' if a == b else 'named_wins' if a else 'masked_wins'] += 1
    output['paired_failure_inclusive'] = paired
    complete = {'named_wins': 0, 'masked_wins': 0, 'ties': 0, 'pairs': 0}
    for pair in pairs.values():
        if all(pair.get(v) is not None for v in ('named', 'masked')):
            a, b = [bool(pair[v].get('success')) for v in ('named', 'masked')]
            complete['pairs'] += 1
            complete['ties' if a == b else 'named_wins' if a else 'masked_wins'] += 1
    output['paired_complete'] = complete
    output['arms'] = {}
    for arm in ('free', 'zero', 'entropy_pick'):
        ids = [e['session_id'] for e in plan['schedule'] if e.get('arm', 'free') == arm]
        output['arms'][arm] = {'scheduled': len(ids), 'successes': sum(bool(keyed.get(i, {}).get('success')) for i in ids), 'statuses': dict(Counter(keyed.get(i, {}).get('status', 'unstarted') for i in ids))}
    return output


def save_json(path, value):
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(value, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())


def count_tokens(tokenizer, messages, info):
    encoded = tokenizer.apply_chat_template(messages, tokenize=True,
        add_generation_prompt=True, return_dict=False, truncation=False,
        **info.get('chat_template_kwargs', {}))
    ids = encoded['input_ids'] if hasattr(encoded, 'keys') else encoded
    if hasattr(ids, 'tolist'):
        ids = ids.tolist()
    if ids and isinstance(ids[0], list):
        if len(ids) != 1:
            raise ValueError('expected one tokenized conversation')
        ids = ids[0]
    return len(ids)


def new_session(cases, spec):
    return Session(cases[spec['family'], spec['split']], spec['target'],
                   spec['order'], spec['view'], spec['label_seed'],
                   budget=0 if spec.get('arm') == 'zero' else 3)


def entropy_question(session):
    choices = [j for j in range(len(session.grid[0])) if j not in session.asked]
    def utility(j):
        sizes = Counter(session.grid[i][j] for i in session.survivors).values()
        return -sum(n * math.log2(n) for n in sizes)
    informative = [j for j in choices if len({session.grid[i][j] for i in session.survivors}) > 1]
    return max(informative, key=utility) if informative else None


def initial_messages(session):
    return [{'role': 'system', 'content': session.initial['instructions']},
            {'role': 'user', 'content': encode(session.initial)}]


def preflight(plan, cases, tokenizer):
    info = plan['model_info']
    report = []
    for spec in plan['schedule']:
        session = new_session(cases, spec)
        messages = initial_messages(session)
        first = count_tokens(tokenizer, messages, info)
        # Conservative history: all permitted turns use the largest rendered
        # query/action/answer exchange for this matrix. No truncation is used.
        exchanges = [(encode({'ask': j}), encode({'answer': row[j]}))
                     for row in session.grid for j in range(len(row))]
        action, answer = max(exchanges, key=lambda e: count_tokens(tokenizer,
            messages + [{'role': 'assistant', 'content': e[0]},
                        {'role': 'user', 'content': e[1]}], info))
        for _ in range(session.budget):
            messages.extend([{'role': 'assistant', 'content': action}, {'role': 'user', 'content': answer}])
        worst = count_tokens(tokenizer, messages, info)
        report.append({'session_id': spec['session_id'], 'opening_tokens': first,
                       'conservative_tokens': worst, 'fits': worst + info['max_tokens'] <= info['context_tokens']})
    return report


def replay(directory, data_path):
    plan = json.loads((directory / 'plan.json').read_text())
    if sha(data_path.read_bytes()) != plan['data_sha256']:
        raise ValueError('data hash mismatch')
    cases = load_cases(data_path)
    records = []
    for spec in plan['schedule']:
        path = directory / (spec['session_id'] + '.result.json')
        if not path.exists():
            continue
        record = json.loads(path.read_text())
        session = new_session(cases, spec)
        grade = None
        questions = []
        usage = Counter()
        for event in map(json.loads, (directory / record['transcript']).read_text().splitlines()):
            if event.get('usage'):
                usage.update({k: v for k, v in event['usage'].items() if isinstance(v, (int, float))})
            if 'action' in event:
                before = len(session.survivors)
                def query_entropy(j):
                    sizes = Counter(session.grid[i][j] for i in session.survivors).values()
                    return -sum((n / before) * math.log2(n / before) for n in sizes)
                question = event['action'].get('ask')
                entropy = query_entropy(question) if question is not None else None
                best = max((query_entropy(j) for j in range(len(session.grid[0])) if j not in session.asked), default=0)
                _, grade = session.step(event['action'])
                if 'ask' in event['action']:
                    questions.append({'column': event['action']['ask'], 'survivors_before': before, 'survivors_after': len(session.survivors), 'uninformative': before == len(session.survivors), 'fraction_eliminated': 1 - len(session.survivors) / before, 'entropy_bits': entropy, 'best_available_entropy_bits': best, 'relative_entropy': entropy / best if best else None})
        hidden = session.case['heldout_outputs']
        record['uniform_survivor_score'] = sum(hidden[session.order[i]] == hidden[session.target] for i in session.survivors) / len(session.survivors)
        record['survivors_after_questions'] = len(session.survivors)
        record['question_diagnostics'] = questions
        record['token_usage'] = dict(usage)
        if record['status'] == 'completed':
            if grade is None or any(record.get(k) != v for k, v in grade.items()):
                raise ValueError('transcript grade mismatch: ' + spec['session_id'])
        records.append(record)
    result = summarize(plan, records)
    result['transcript_diagnostics'] = [{k: r[k] for k in ('session_id', 'uniform_survivor_score', 'survivors_after_questions', 'question_diagnostics', 'token_usage')} for r in records]
    return result


def run(plan_path, data_path, endpoint, tokenizer_path, output):
    # Local endpoints only. No authenticated service or paid API is used.
    parsed = urlparse(endpoint)
    if parsed.scheme != 'http' or parsed.hostname not in {'127.0.0.1', 'localhost', '::1'} or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Use a local unauthenticated server origin')
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    if sha(data_path.read_bytes()) != plan['data_sha256'] or sha(Path(__file__).read_bytes()) != plan['source_sha256']:
        raise ValueError('frozen data or supervisor changed')
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path), local_files_only=True, trust_remote_code=False)
    output.mkdir(parents=True, exist_ok=False)
    save_json(output / 'plan.json', plan)
    save_json(output / 'RUN.json', {'plan_sha256': sha(plan_bytes), 'endpoint': endpoint, 'tokenizer_path': str(tokenizer_path), 'scope': 'Text-only frozen-matrix evaluation; preserve all failures and raw responses.'})
    cases = load_cases(data_path)
    records = []
    info = plan['model_info']
    checks = preflight(plan, cases, tokenizer)
    save_json(output / 'PREFLIGHT.json', checks)
    if not all(r['fits'] for r in checks):
        raise ValueError('context preflight failed; inspect PREFLIGHT.json')
    opener = build_opener(ProxyHandler({}))
    for spec in plan['schedule']:
        session = new_session(cases, spec)
        messages = initial_messages(session)
        started = time.monotonic()
        row = {'session_id': spec['session_id'], 'view': spec['view'], 'status': 'interrupted', 'success': False, 'heldout_exact': None}
        event_path = output / (spec['session_id'] + '.events.jsonl')
        try:
            with event_path.open('x', encoding='utf-8') as events:
                def log(event):
                    events.write(encode(event) + '\n')
                    events.flush()
                    os.fsync(events.fileno())
                if spec.get('arm') == 'entropy_pick':
                    for _ in range(3):
                        j = entropy_question(session)
                        if j is None:
                            break
                        action = {'ask': j}
                        answer, _ = session.step(action)
                        log({'action': action, 'source': 'entropy', 'answer': answer})
                        messages.extend([{'role': 'assistant', 'content': encode(action)}, {'role': 'user', 'content': encode(answer)}])
                    messages.append({'role': 'user', 'content': 'Select a consistent row now. Send only a JSON pick object.'})
                for turn in range(1 if spec.get('arm') in ('zero', 'entropy_pick') else 4):
                    request = model_request(messages, info)
                    count = count_tokens(tokenizer, messages, info)
                    log({'turn': turn, 'request': request, 'prompt_tokens_preflight': count})
                    if count + info['max_tokens'] > info['context_tokens']:
                        raise ProtocolError('context_overflow')
                    remaining = info['timeout_seconds'] - (time.monotonic() - started)
                    if remaining <= 0:
                        raise TimeoutError('session_timeout')
                    with opener.open(Request(endpoint.rstrip('/') + '/v1/chat/completions', data=encode(request).encode(), headers={'Content-Type': 'application/json'}), timeout=remaining) as response:
                        raw = response.read().decode('utf-8')
                    log({'turn': turn, 'raw_response': raw})
                    response = json.loads(raw)
                    choice = response['choices'][0]
                    if choice['finish_reason'] == 'length':
                        raise ProtocolError('output_truncated')
                    if choice['message'].get('tool_calls'):
                        raise ProtocolError('unexpected_tool_call')
                    text = choice['message']['content']
                    log({'usage': response.get('usage'), 'finish_reason': choice['finish_reason']})
                    action = parse_action(text)
                    if spec.get('arm') in ('zero', 'entropy_pick') and 'ask' in action:
                        raise ProtocolError('pick_required')
                    answer, grade = session.step(action)
                    log({'action': action, 'source': 'model', 'answer': answer})
                    if grade is not None:
                        row.update(grade)
                        break
                    messages.extend([{'role': 'assistant', 'content': text}, {'role': 'user', 'content': encode(answer)}])
                else:
                    raise ProtocolError('missing_pick')
        except (Exception,) as exc:
            row.update(status='protocol_failure' if isinstance(exc, ProtocolError) else 'infrastructure_failure', error_type=type(exc).__name__, error=str(exc), success=False)
        row.update(elapsed_seconds=time.monotonic() - started, questions=len(session.asked), transcript=event_path.name)
        save_json(output / (spec['session_id'] + '.result.json'), row)
        records.append(row)
        temporary = output / 'SUMMARY.tmp'
        temporary.write_text(json.dumps(summarize(plan, records), indent=2), encoding='utf-8')
        temporary.replace(output / 'SUMMARY.json')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    freeze = sub.add_parser('freeze')
    freeze.add_argument('--controls', action='store_true', help='Include zero-question and entropy-assisted named arms')
    freeze.add_argument('--data', type=Path, default=Path(__file__).with_name('frozen_cases.jsonl.gz'))
    freeze.add_argument('--model-info', type=Path, required=True)
    freeze.add_argument('--output', type=Path, required=True)
    live = sub.add_parser('run')
    live.add_argument('--plan', type=Path, required=True)
    live.add_argument('--data', type=Path, default=Path(__file__).with_name('frozen_cases.jsonl.gz'))
    live.add_argument('--endpoint', required=True)
    live.add_argument('--tokenizer', type=Path, required=True)
    live.add_argument('--output', type=Path, required=True)
    verify = sub.add_parser('replay')
    verify.add_argument('directory', type=Path)
    verify.add_argument('--data', type=Path, default=Path(__file__).with_name('frozen_cases.jsonl.gz'))
    report = sub.add_parser('summarize')
    report.add_argument('directory', type=Path)
    refs = sub.add_parser('baselines')
    refs.add_argument('--plan', type=Path, required=True)
    refs.add_argument('--data', type=Path, default=Path(__file__).with_name('frozen_cases.jsonl.gz'))
    a = p.parse_args()
    if a.command == 'freeze':
        save_json(a.output, make_plan(load_cases(a.data), sha(a.data.read_bytes()), json.loads(a.model_info.read_text(encoding='utf-8')), controls=a.controls))
    elif a.command == 'run':
        run(a.plan, a.data, a.endpoint, a.tokenizer, a.output)
    elif a.command == 'replay':
        print(json.dumps(replay(a.directory, a.data), indent=2))
    elif a.command == 'summarize':
        plan = json.loads((a.directory / 'plan.json').read_text(encoding='utf-8'))
        rows = [json.loads(f.read_text(encoding='utf-8')) for f in sorted(a.directory.glob('*.result.json'))]
        print(json.dumps(summarize(plan, rows), indent=2))
    else:
        plan = json.loads(a.plan.read_text(encoding='utf-8'))
        if sha(a.data.read_bytes()) != plan['data_sha256']:
            raise ValueError('data hash mismatch')
        cases = load_cases(a.data)
        rows = []
        for s in plan['schedule']:
            session = Session(cases[s['family'], s['split']], s['target'], s['order'], s['view'], s['label_seed'])
            rows.append({'session_id': s['session_id'], **{p: baseline(session, p) for p in ['entropy', 'random_split']}})
        print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
