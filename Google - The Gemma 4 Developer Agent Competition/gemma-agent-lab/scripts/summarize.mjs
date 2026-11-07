import {readFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {wilson} from '../dist/logic.js';

export const outcomes = [
  'resolved', 'unresolved', 'test_failure', 'timeout', 'setup_failure', 'invalid_patch',
  'empty_patch', 'unstarted',
];

export function summarize(rows, scheduled) {
  if (!Array.isArray(scheduled) || scheduled.length === 0 ||
      scheduled.some(id => typeof id !== 'string' || !id.trim() || id.trim() !== id)) {
    throw Error('Scheduled IDs must be a nonempty array of nonblank string IDs without surrounding whitespace.');
  }
  const allowed = new Set(scheduled);
  if (allowed.size !== scheduled.length) throw Error('Scheduled IDs must be unique.');
  if (!Array.isArray(rows)) throw Error('Result rows must be an array.');

  const seen = new Set();
  const counts = Object.fromEntries(outcomes.map(outcome => [outcome, 0]));
  let seconds = 0;
  let toolErrors = 0;
  let unknownToolErrorRows = 0;
  for (const row of rows) {
    if (!row || !allowed.has(row.instance_id)) throw Error('Result row has an unscheduled or missing instance_id.');
    if (seen.has(row.instance_id)) throw Error(`Duplicate result for ${row.instance_id}.`);
    if (!outcomes.includes(row.outcome) || !Number.isFinite(row.seconds) || row.seconds < 0 ||
        (row.tool_errors !== null && (!Number.isSafeInteger(row.tool_errors) || row.tool_errors < 0))) {
      throw Error(`Invalid outcome, seconds or tool_errors for ${row.instance_id}.`);
    }
    seen.add(row.instance_id);
    counts[row.outcome]++;
    seconds += row.seconds;
    if (row.tool_errors === null) unknownToolErrorRows++;
    else toolErrors += row.tool_errors;
  }
  if (!Number.isFinite(seconds) || !Number.isSafeInteger(toolErrors)) {
    throw Error('Result totals exceed the supported numeric range.');
  }
  counts.unstarted += scheduled.length - seen.size;
  return {
    scheduled: scheduled.length,
    resolved: counts.resolved,
    resolve_rate: counts.resolved / scheduled.length,
    descriptive_wilson_95: wilson(counts.resolved, scheduled.length),
    outcomes: counts,
    sum_task_seconds: seconds,
    tool_errors: unknownToolErrorRows ? null : toolErrors,
    known_tool_error_subtotal: toolErrors,
    unknown_tool_error_rows: unknownToolErrorRows,
    note: 'Task seconds are not necessarily global wall time. Measure total elapsed runtime separately. Missing scheduled tasks count as unstarted and unresolved.',
  };
}

export async function readResults(filename) {
  const lines = (await readFile(filename, 'utf8')).replace(/^\uFEFF/, '').split(/\r?\n/);
  const rows = [];
  for (const [index, line] of lines.entries()) {
    if (!line.trim()) continue;
    try {
      rows.push(JSON.parse(line));
    } catch {
      throw Error(`Invalid JSON in ${filename} at line ${index + 1}.`);
    }
  }
  return rows;
}

export async function readJson(filename) {
  return JSON.parse((await readFile(filename, 'utf8')).replace(/^\uFEFF/, ''));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [results, schedule] = process.argv.slice(2);
  if (!results || !schedule) throw Error('Usage: node scripts/summarize.mjs <results.jsonl> <scheduled-ids.json>');
  console.log(JSON.stringify(summarize(await readResults(results), await readJson(schedule)), null, 2));
}
