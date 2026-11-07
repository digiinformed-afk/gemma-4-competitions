"""Run one frozen public-task schedule in a fresh Kaggle Linux process.

Attach the organizer's exported Getting Started v3 notebook, its competition/model/
wheelhouse inputs, an unpacked submission and a schedule from freeze-schedule.py.
Run this script from a notebook shell. Each invocation owns its own model server.
The wall budget includes offline installation, loading, generation, verification
and teardown. This local public-task timing includes verification.
"""

import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time


DATA = Path('/kaggle/input/competitions/gemma-4-developer-agent')
# Only these two reviewed cells from the organizer's public v3 notebook are used.
# The sample task loop, file rewrites and archive creation are skipped.
INSTALL = 'c3032e216b0a393aec76180338e56f3ae5d7d995b5de9913f78b79a1fa1105af'
SERVE = '05c129500663d3b377f0ffec84ff7145a942e5414717f1a7733108c619c71b9a'


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def file_hash(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def sample_assets_hash(files):
    # The builder changes only agent.yaml and its reserved root instruction include.
    # Keep skills, original prompts, adapters and all other assets equal across arms.
    assets = {name: sha for name, sha in files.items()
              if name not in {'agent.yaml', 'prompts/root-repair-policy.md'}}
    return digest(json.dumps(assets, sort_keys=True))


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_json(path, obj):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def official_cells(path):
    found = {}
    for cell in read_json(path)['cells']:
        if cell['cell_type'] != 'code':
            continue
        source = ''.join(cell['source']).replace('\r\n', '\n').rstrip()
        key = digest(source)
        if key in (INSTALL, SERVE):
            found[key] = source
    if found.keys() != {INSTALL, SERVE}:
        raise ValueError('Export the original v3 Getting Started notebook. Setup cell digest mismatch.')
    return found


def resolve_schedule(items, tasks):
    if not isinstance(items, list) or not items:
        raise ValueError('Provide a nonempty JSON array of task IDs or {instance_id,repo} rows.')
    by_id = {}
    for task in tasks:
        if task.instance_id in by_id:
            raise ValueError(f'Duplicate dataset task: {task.instance_id}')
        by_id[task.instance_id] = task
    selected = []
    seen = set()
    for item in items:
        task_id = item if isinstance(item, str) else item.get('instance_id') if isinstance(item, dict) else None
        if not isinstance(task_id, str) or task_id not in by_id or task_id in seen:
            raise ValueError(f'Unknown or repeated scheduled task ID: {task_id!r}')
        task = by_id[task_id]
        if isinstance(item, dict) and (set(item) != {'instance_id', 'repo'} or item['repo'] != task.repo):
            raise ValueError(f'Schedule row must contain only the matching instance_id and repo: {task_id}')
        seen.add(task_id)
        selected.append(task)
    return selected


def result_row(task, result, seconds):
    if (result.instance_id, result.repo) != (task.instance_id, task.repo):
        raise ValueError('Returned result belongs to a different task')
    error = result.error or ''
    if result.resolved is True:
        outcome = 'resolved'
    elif result.resolved is not False:
        raise ValueError('Evaluator did not return a boolean resolution grade')
    elif error.startswith('Agent exceeded session timeout'):
        outcome = 'timeout'
    elif error.startswith('Failed to apply agent patch:'):
        outcome = 'invalid_patch'
    elif error:
        outcome = 'unresolved'
    elif not (result.agent_patch or '').strip():
        outcome = 'empty_patch'
    elif result.test_exit_code > 0:
        outcome = 'test_failure'
    else:
        outcome = 'unresolved'
    return dict(instance_id=task.instance_id, outcome=outcome, seconds=seconds,
                test_exit_code=result.test_exit_code, tool_calls=result.tool_calls, tool_errors=None)


def settings(root):
    import yaml
    files = [root / name for name in ('eval_config.yaml', 'eval_config.yml') if (root / name).exists()]
    if len(files) > 1:
        raise ValueError('Conflicting evaluation settings files')
    raw = (yaml.safe_load(files[0].read_text(encoding='utf-8')) or {}) if files else {}
    cfg = raw.get('evaluation', raw)
    turns = cfg.get('max_turns', cfg.get('max_llm_calls'))
    return dict(timeout_seconds=int(cfg.get('timeout_seconds', 300)),
                verification_timeout_seconds=int(cfg.get('verification_timeout_seconds', 300)),
                max_time_minutes=float(cfg.get('max_time_minutes', 60.0)),
                max_tool_calls=int(cfg.get('max_tool_calls', 100)),
                max_turns=int(turns) if turns is not None else None)


def run_worker(args):
    cells = official_cells(args.starter)
    scope = {'__name__': '__main__', 'AGENT_DIR': args.agent, 're': re}
    exec(compile(cells[INSTALL], '<official-v3-wheel-install>', 'exec'), scope)
    from importlib.metadata import version
    from adk_submission import validate_directory
    from adk_submission.discovery import discover_declared_models
    from adk_submission.yaml_loader import load_yaml
    from google.adk.agents.context_cache_config import ContextCacheConfig
    from google.adk.apps._configs import EventsCompactionConfig
    from swegemma.config import EvalConfig, build_submission_limits
    from swegemma.evaluate import Evaluator
    from swegemma.models import load_tasks
    from swegemma.results import append_task_result
    import torch

    task_file = args.data / 'tasks.jsonl'
    scheduled = resolve_schedule(read_json(args.schedule), load_tasks(task_file))
    limits, constraints = build_submission_limits()
    validate_directory(args.agent, limits=limits)
    models = discover_declared_models(args.agent)
    if len(models) != 1:
        raise ValueError('Expected one declared model across all agents')
    model = next(iter(models))
    if not torch.cuda.is_available():
        raise RuntimeError('A Kaggle GPU runtime is required')
    root_config = load_yaml(args.agent / 'agent.yaml', args.agent, limits=limits)
    instruction = root_config.get('instruction')
    if not isinstance(instruction, str) or not instruction.strip():
        raise ValueError('Expected a root instruction string in agent.yaml')
    config_settings = settings(args.agent)
    versions = {p: version(p) for p in ('swegemma', 'adk-submission', 'adk-eval-core', 'google-adk', 'vllm')}
    bundle = {path.relative_to(args.agent).as_posix(): file_hash(path)
              for path in sorted(args.agent.rglob('*')) if path.is_file()}
    adapters = {name: value for name, value in bundle.items() if name.startswith('adapters/')}
    # A paired instruction-only run must use the same resolved agent topology,
    # model settings and subagents even when its root instruction is in a new file.
    other_config = {key: value for key, value in root_config.items() if key != 'instruction'}
    yaml_paths = [name for name in bundle if name.startswith('sub_agents/') and name.endswith(('.yml', '.yaml'))]
    agents = {name: load_yaml(args.agent / name, args.agent, limits=limits) for name in yaml_paths}
    environment = dict(label=args.environment, gpu=[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
                       torch=str(torch.__version__), runner=file_hash(Path(__file__)), evaluation=config_settings,
                       sample_assets=sample_assets_hash(bundle),
                       agent_config=digest(json.dumps([other_config, agents], sort_keys=True)))
    manifest = dict(run_id=args.output.name, schedule=[dict(instance_id=t.instance_id, repo=t.repo) for t in scheduled],
                    model_revision=f'google/gemma-4/other/{model}/2;adapters={digest(json.dumps(adapters, sort_keys=True))}',
                    harness_revision=json.dumps(versions, sort_keys=True),
                    data_revision=file_hash(task_file), environment_revision=json.dumps(environment, sort_keys=True),
                    prompt_sha256=digest(instruction), submission_files_sha256=bundle,
                    wall_budget_seconds=args.wall_seconds, results_file='results.jsonl',
                    timing_scope='cold worker startup through teardown, including public-task verification')
    write_json(args.output / 'prepared.json', manifest)
    harness_output = args.output / 'harness'
    try:
        exec(compile(cells[SERVE], '<official-v3-model-server>', 'exec'), scope)
        config = EvalConfig(tasks_path=task_file, snapshots_dir=args.data / 'snapshots', results_dir=harness_output,
                            submission_dir=args.agent, models=scope['models'], sandbox='subprocess',
                            adapter_manifest=scope['adapters'], limits=limits, generation_constraints=constraints,
                            context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=1800, cache_intervals=10),
                            events_compaction_config=EventsCompactionConfig(compaction_interval=15, overlap_size=2,
                                                                          token_threshold=14336, event_retention_size=5),
                            graph_dir=str(args.data / 'graphs'), embeddings_dir=str(args.data / 'embeddings'),
                            wheels_dir=args.data / 'wheels', verbose=False, **config_settings)
        evaluator = Evaluator(config)
        for index, task in enumerate(scheduled, start=1):
            started = time.monotonic()
            write_json(args.output / 'active.json', dict(instance_id=task.instance_id, started_monotonic=started))
            print(f'[{index}/{len(scheduled)}] {task.instance_id}', flush=True)
            result = asyncio.run(evaluator.evaluate_task(task=task, task_index=index, total_tasks=len(scheduled)))
            row = result_row(task, result, time.monotonic() - started)
            write_json(args.output / 'rows' / f'{index:06}.json', row)
            # Preserve evaluator evidence separately from the uploadable agent.
            append_task_result(result, harness_output)
            (args.output / 'active.json').unlink()
    finally:
        if scope.get('server_instance') is not None:
            scope['server_instance'].stop()


def finalize(output, status, started):
    rows = [read_json(path) for path in sorted((output / 'rows').glob('*.json'))]
    active = output / 'active.json'
    if status == 'budget_exhausted' and active.exists():
        task = read_json(active)
        if not any(row['instance_id'] == task['instance_id'] for row in rows):
            rows.append(dict(instance_id=task['instance_id'], outcome='timeout', tool_errors=None,
                             seconds=time.monotonic() - task['started_monotonic']))
    (output / 'results.jsonl').write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
    elapsed = time.monotonic() - started
    write_json(output / 'status.json', dict(status=status, elapsed_wall_seconds=elapsed, recorded_tasks=len(rows)))
    if status in {'complete', 'budget_exhausted'} and (output / 'prepared.json').exists():
        manifest = read_json(output / 'prepared.json')
        manifest.update(status=status, elapsed_wall_seconds=elapsed)
        write_json(output / 'manifest.json', manifest)


def recover(output, remaining_path=None):
    """Read rows committed before interruption without manufacturing timing or grades."""
    prepared = output / 'prepared.json'
    if not prepared.is_file():
        raise ValueError('No prepared task manifest. This run stopped before task evaluation began.')
    schedule = read_json(prepared)['schedule']
    ids = {task['instance_id'] for task in schedule}
    rows = [read_json(path) for path in sorted((output / 'rows').glob('*.json'))]
    recorded = {row['instance_id'] for row in rows}
    if len(ids) != len(schedule) or len(recorded) != len(rows) or not recorded <= ids:
        raise ValueError('Checkpoint has repeated or unscheduled task IDs')
    remaining = [task for task in schedule if task['instance_id'] not in recorded]
    if remaining_path:
        if not remaining:
            raise ValueError('All scheduled rows are already committed')
        with remaining_path.open('x', encoding='utf-8') as target:
            json.dump(remaining, target, indent=2)
            target.write('\n')
    return {'committed': len(recorded), 'scheduled': len(schedule),
            'committed_resolved': sum(row['outcome'] == 'resolved' for row in rows),
            'remaining': remaining, 'has_final_manifest': (output / 'manifest.json').is_file()}


def terminate_group(process):
    # The organizer server and its workers inherit this fresh process group.
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=0.5)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def supervise(args):
    if sys.platform != 'linux':
        raise SystemExit('Use a fresh Kaggle Linux GPU notebook with the official inputs.')
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'rows').mkdir()
    started = time.monotonic()
    status = 'worker_failed'
    process = None
    try:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), *sys.argv[1:], '--worker'],
                                   start_new_session=True)
        # Give the supervisor a small allowance for teardown and writing final records.
        remaining = max(0, args.wall_seconds - 2 - (time.monotonic() - started))
        try:
            if process.wait(timeout=remaining) == 0:
                status = 'complete'
        except subprocess.TimeoutExpired:
            status = 'budget_exhausted'
    finally:
        if process is not None and (process.poll() is None or status != 'complete'):
            terminate_group(process)
        finalize(args.output, status, started)
    print(f'{status}: {args.output}', flush=True)
    return 0 if (args.output / 'manifest.json').exists() else 1


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('starter', 'agent', 'schedule', 'output'):
        parser.add_argument('--' + name, type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument('--data', type=Path, default=DATA, help='official competition directory')
    parser.add_argument('--wall-seconds', required=True, type=int, help='cold elapsed time cap including verification')
    parser.add_argument('--environment', required=True, help='immutable runtime image/revision or a frozen environment ID')
    parser.add_argument('--preflight', action='store_true', help='check inputs and pinned starter cells without using a GPU')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.wall_seconds < 5 or not args.environment.strip():
        parser.error('Set --wall-seconds to at least five and give an environment ID.')
    if not (args.agent / 'agent.yaml').is_file() or not args.schedule.is_file() or not args.starter.is_file():
        parser.error('Input notebook, schedule and root agent.yaml must exist.')
    if args.output.is_relative_to(args.agent) or args.output.is_relative_to(args.data.resolve()):
        parser.error('Choose a new output directory separate from the submission and the competition data.')
    return args


if __name__ == '__main__':
    if '--recover' in sys.argv[1:]:
        parser = argparse.ArgumentParser(description='Inspect saved task work after a run stops.')
        parser.add_argument('--recover', required=True, type=Path, metavar='RUN_DIRECTORY')
        parser.add_argument('--remaining', type=Path, help='write pending IDs to a new diagnostic schedule file')
        recovery = parser.parse_args()
        try:
            print(json.dumps(recover(recovery.recover, recovery.remaining), indent=2))
        except (OSError, ValueError) as error:
            parser.exit(1, f'Recovery failed: {error}\n')
        sys.exit(0)
    args = parse_args()
    if args.preflight:
        from types import SimpleNamespace
        official_cells(args.starter)
        with (args.data / 'tasks.jsonl').open(encoding='utf-8-sig') as records:
            identities = [SimpleNamespace(instance_id=row['instance_id'], repo=row['repo'])
                          for line in records if line.strip() for row in [json.loads(line)]]
        selected = resolve_schedule(read_json(args.schedule), identities)
        print(f'Pinned v3 setup verified. Matched {len(selected)} scheduled task identities.')
    elif args.worker:
        run_worker(args)
    else:
        raise SystemExit(supervise(args))
