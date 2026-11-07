import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, rm, rmdir, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {compareRuns} from '../scripts/compare-runs.mjs';
import {summarize} from '../scripts/summarize.mjs';

const schedule = [
  {instance_id: 'a1', repo: 'a'}, {instance_id: 'a2', repo: 'a'},
  {instance_id: 'b1', repo: 'b'}, {instance_id: 'b2', repo: 'b'},
  {instance_id: 'b3', repo: 'b'},
];

function manifest(run_id, overrides = {}) {
  return {
    run_id, schedule, model_revision: 'test-model', harness_revision: 'test-grader',
    data_revision: 'test-data', environment_revision: 'test-env',
    prompt_sha256: (run_id === 'baseline' ? 'a' : 'b').repeat(64),
    wall_budget_seconds: 12, elapsed_wall_seconds: 11,
    ...overrides,
  };
}

function row(instance_id, outcome, tool_errors = 0) {
  return {instance_id, outcome, seconds: 4, tool_errors};
}

test('pairs by ID and keeps missing, explicit unstarted and unknown counters distinct', () => {
  const baseline = [row('a1', 'resolved'), row('a2', 'resolved', 1), row('b1', 'timeout', null)];
  const candidate = [row('b2', 'resolved'), row('b1', 'resolved'), row('a1', 'resolved'), row('b3', 'unstarted')];
  const report = compareRuns(manifest('baseline'), baseline, manifest('candidate'), candidate);
  assert.deepEqual(report.paired, {scheduled: 5, both_resolved: 1, candidate_only: 2, baseline_only: 1, both_unresolved: 1});
  assert.deepEqual(report.by_repository, [
    {repo: 'a', scheduled: 2, both_resolved: 1, candidate_only: 0, baseline_only: 1, both_unresolved: 0},
    {repo: 'b', scheduled: 3, both_resolved: 0, candidate_only: 2, baseline_only: 0, both_unresolved: 1},
  ]);
  assert.deepEqual(report.discordant_tasks.map(pair => [pair.instance_id, pair.baseline_outcome, pair.candidate_outcome]),
    [['a2', 'resolved', 'unstarted'], ['b1', 'timeout', 'resolved'], ['b2', 'unstarted', 'resolved']]);
  assert.equal(report.resolve_rate_delta, 0.2);
  assert.deepEqual(report.baseline.missing_result_ids, ['b2', 'b3']);
  assert.deepEqual(report.candidate.missing_result_ids, ['a2']);
  assert.equal(report.candidate.outcomes.unstarted, 2);
  assert.equal(report.baseline.tool_errors, null);
  assert.equal(report.baseline.known_tool_error_subtotal, 1);
  assert.equal(report.baseline.unknown_tool_error_rows, 1);
  assert.equal(report.candidate.tool_errors, 0);
  assert.equal(report.candidate.sum_task_seconds, 16);
  assert.equal(report.candidate.elapsed_wall_seconds, 11);
  assert.match(report.ordered_schedule_sha256, /^[a-f0-9]{64}$/);
});

test('incompatible runs and over-budget results cannot form an equal-budget comparison', () => {
  const base = manifest('baseline');
  for (const [field, value] of Object.entries({
    run_id: 'baseline', wall_budget_seconds: 14, elapsed_wall_seconds: 13,
    model_revision: 'changed', harness_revision: 'changed', data_revision: 'changed',
    environment_revision: 'changed', prompt_sha256: 'invalid', schedule: [...schedule].reverse(),
  })) {
    assert.throws(() => compareRuns(base, [], manifest('candidate', {[field]: value}), []), Error, field);
  }
  assert.throws(() => compareRuns(base, [], manifest('candidate', {
    schedule: [{...schedule[0], repo: 'b'}, ...schedule.slice(1)],
  }), []), /repositories/);
  const duplicate = [schedule[0], schedule[0]];
  assert.throws(() => compareRuns(manifest('a', {schedule: duplicate}), [], manifest('b', {schedule: duplicate}), []), /unique/);
});

test('malformed inputs fail and a binary unresolved grade keeps its original meaning', () => {
  for (const invalidSchedule of ['ab', [], [1], [''], ['  '], [' a']]) {
    assert.throws(() => summarize([], invalidSchedule), /Scheduled IDs/);
  }
  const valid = row('id', 'unresolved', null);
  assert.equal(summarize([valid], ['id']).outcomes.unresolved, 1);
  assert.throws(() => summarize([{...valid, tool_errors: undefined}], ['id']), /tool_errors/);
  assert.throws(() => summarize([{...valid, outcome: 'unknown'}], ['id']), /outcome/);
  assert.throws(() => summarize([{...valid, seconds: -1}], ['id']), /seconds/);
});

test('CLI resolves per-manifest files and reads Windows BOM, blank lines and CRLF', async t => {
  const dir = await mkdtemp(join(tmpdir(), 'gemma-paired-'));
  t.after(async () => {
    for (const filename of ['baseline.json', 'baseline.jsonl', 'candidate.json', 'candidate.jsonl']) {
      await rm(join(dir, filename), {force: true});
    }
    await rmdir(dir);
  });
  for (const id of ['baseline', 'candidate']) {
    const results = id + '.jsonl';
    await writeFile(join(dir, id + '.json'), '\uFEFF' + JSON.stringify(manifest(id, {results_file: results})));
    await writeFile(join(dir, results), '\uFEFF\r\n' + JSON.stringify(row('b1', id === 'candidate' ? 'resolved' : 'unresolved')) + '\r\n');
  }
  const cli = fileURLToPath(new URL('../scripts/compare-runs.mjs', import.meta.url));
  const call = () => execFileSync(process.execPath, [cli, join(dir, 'baseline.json'), join(dir, 'candidate.json')],
    {encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe']});
  const report = JSON.parse(call());
  assert.equal(report.paired.candidate_only, 1);
  assert.equal(report.paired.both_unresolved, 4);
  await writeFile(join(dir, 'candidate.jsonl'), '\n{truncated');
  assert.throws(call, /line 2/);
});
