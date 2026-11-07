import {createHash} from 'node:crypto';
import {dirname, resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {readJson, readResults, summarize} from './summarize.mjs';

const usage = `Usage: node scripts/compare-runs.mjs <baseline-manifest.json> <candidate-manifest.json>

Each run manifest records:
  run_id                 unique ID for the run
  model_revision         exact model and adapter identity
  harness_revision       grading harness identity
  data_revision          frozen evaluation data identity
  environment_revision   shared hardware, serving and decoding configuration
  prompt_sha256          SHA-256 of this run's prompt
  wall_budget_seconds    predeclared global time limit
  elapsed_wall_seconds   measured elapsed time, including setup and finalization
  schedule               ordered array of {"instance_id":"...","repo":"..."}
  results_file           path to graded JSONL, resolved from this manifest's directory

Use the same frozen schedule and budget for both runs. Record grading outcomes using
the schema in dist/experiment-template.jsonl. Missing scheduled rows count as
unstarted and unresolved. The JSON report retains discordant task IDs and outcomes.`;

const fixedFields = ['model_revision', 'harness_revision', 'data_revision', 'environment_revision'];

function checkManifest(manifest) {
  for (const field of ['run_id', ...fixedFields]) {
    if (typeof manifest?.[field] !== 'string' || !manifest[field].trim()) {
      throw Error(`Manifest requires a nonblank ${field}.`);
    }
  }
  if (typeof manifest.prompt_sha256 !== 'string' || !/^[a-f0-9]{64}$/i.test(manifest.prompt_sha256)) {
    throw Error(`${manifest.run_id} requires a 64-digit hexadecimal prompt_sha256.`);
  }
  for (const field of ['wall_budget_seconds', 'elapsed_wall_seconds']) {
    if (!Number.isFinite(manifest[field]) || manifest[field] <= 0) {
      throw Error(`${manifest.run_id} requires a positive ${field}.`);
    }
  }
  if (manifest.elapsed_wall_seconds > manifest.wall_budget_seconds) {
    throw Error(`${manifest.run_id} exceeded its global wall budget (${manifest.elapsed_wall_seconds}s > ${manifest.wall_budget_seconds}s).`);
  }
  if (!Array.isArray(manifest.schedule) || manifest.schedule.length === 0) {
    throw Error(`${manifest.run_id} requires a nonempty ordered schedule.`);
  }
  for (const task of manifest.schedule) {
    if (typeof task?.repo !== 'string' || !task.repo.trim() || task.repo !== task.repo.trim()) {
      throw Error(`${manifest.run_id} has a missing or invalid schedule repository.`);
    }
  }
}

function newCounts() {
  return {scheduled: 0, both_resolved: 0, candidate_only: 0, baseline_only: 0, both_unresolved: 0};
}

function describeRun(manifest, summary, missing) {
  return {
    run_id: manifest.run_id,
    prompt_sha256: manifest.prompt_sha256,
    elapsed_wall_seconds: manifest.elapsed_wall_seconds,
    missing_result_ids: missing,
    ...summary,
  };
}

export function compareRuns(baseline, baselineRows, candidate, candidateRows) {
  checkManifest(baseline);
  checkManifest(candidate);
  if (baseline.run_id === candidate.run_id) throw Error('A comparison requires distinct run IDs.');
  for (const field of [...fixedFields, 'wall_budget_seconds']) {
    if (baseline[field] !== candidate[field]) throw Error(`Runs differ in ${field}.`);
  }
  const schedule = baseline.schedule;
  if (schedule.length !== candidate.schedule.length ||
      schedule.some((task, index) => task.instance_id !== candidate.schedule[index].instance_id ||
        task.repo !== candidate.schedule[index].repo)) {
    throw Error('Runs differ in scheduled task IDs, repositories or order.');
  }

  const ids = schedule.map(task => task.instance_id);
  const baselineSummary = summarize(baselineRows, ids);
  const candidateSummary = summarize(candidateRows, ids);
  const baselineResults = new Map(baselineRows.map(row => [row.instance_id, row.outcome]));
  const candidateResults = new Map(candidateRows.map(row => [row.instance_id, row.outcome]));
  const overall = newCounts();
  const byRepo = new Map();
  const discordant = [];
  for (const {instance_id, repo} of schedule) {
    const before = baselineResults.get(instance_id) ?? 'unstarted';
    const after = candidateResults.get(instance_id) ?? 'unstarted';
    let category;
    if (before === 'resolved') {
      category = after === 'resolved' ? 'both_resolved' : 'baseline_only';
    } else {
      category = after === 'resolved' ? 'candidate_only' : 'both_unresolved';
    }
    if (!byRepo.has(repo)) byRepo.set(repo, newCounts());
    const repository = byRepo.get(repo);
    overall.scheduled++;
    overall[category]++;
    repository.scheduled++;
    repository[category]++;
    if (category === 'candidate_only' || category === 'baseline_only') {
      discordant.push({instance_id, repo, baseline_outcome: before, candidate_outcome: after});
    }
  }
  // Serialize only the two public identity fields. JSON tuples preserve order and boundaries.
  const scheduleDigest = createHash('sha256')
    .update(JSON.stringify(schedule.map(task => [task.instance_id, task.repo])))
    .digest('hex');
  return {
    ...Object.fromEntries(fixedFields.map(field => [field, baseline[field]])),
    wall_budget_seconds: baseline.wall_budget_seconds,
    ordered_schedule_sha256: scheduleDigest,
    baseline: describeRun(baseline, baselineSummary, ids.filter(id => !baselineResults.has(id))),
    candidate: describeRun(candidate, candidateSummary, ids.filter(id => !candidateResults.has(id))),
    paired: overall,
    resolve_rate_delta: (overall.candidate_only - overall.baseline_only) / overall.scheduled,
    by_repository: [...byRepo].map(([repo, counts]) => ({repo, ...counts})),
    discordant_tasks: discordant,
  };
}

async function loadRun(path) {
  const manifest = await readJson(path);
  if (typeof manifest?.results_file !== 'string' || !manifest.results_file.trim()) {
    throw Error(`${path} requires a results_file path.`);
  }
  const resultPath = resolve(dirname(path), manifest.results_file);
  return {manifest, resultPath, rows: await readResults(resultPath)};
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === '--help') {
    console.log(usage);
  } else {
    try {
      if (args.length !== 2) throw Error(usage);
      const [baseline, candidate] = await Promise.all(args.map(loadRun));
      if (baseline.resultPath === candidate.resultPath) throw Error('Both manifests point to the same results file.');
      const report = compareRuns(baseline.manifest, baseline.rows, candidate.manifest, candidate.rows);
      console.log(JSON.stringify(report, null, 2));
    } catch (error) {
      console.error(error.message);
      process.exitCode = 1;
    }
  }
}
