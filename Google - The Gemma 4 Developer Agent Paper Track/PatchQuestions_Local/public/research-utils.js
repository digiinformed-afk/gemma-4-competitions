export function csvRows(text) {
  const rows = [];
  let row = [],
    field = "",
    quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '"') {
      if (quoted && text[i + 1] === '"') {
        field += '"';
        i++;
      } else quoted = !quoted;
    } else if (ch === "," && !quoted) {
      row.push(field);
      field = "";
    } else if ((ch === "\n" || ch === "\r") && !quoted) {
      if (ch === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      if (row.some((x) => x.trim())) rows.push(row);
      row = [];
      field = "";
    } else field += ch;
  }
  if (quoted) throw new Error("CSV contains an unclosed quoted field.");
  row.push(field);
  if (row.some((x) => x.trim())) rows.push(row);
  return rows;
}
export function analyzeCsv(text, name) {
  const rows = csvRows(text.replace(/^\uFEFF/, ""));
  const header = rows.shift()?.map((x) => x.trim()) || [];
  const fields = ["family", "policy", "budget", "heldout_exact"];
  const index = Object.fromEntries(fields.map((f) => [f, header.indexOf(f)]));
  if (fields.some((f) => index[f] < 0))
    throw new Error(
      "Expected columns: family, policy, budget, heldout_exact. Use the benchmark scores.csv format.",
    );
  if (!rows.length || rows.length > 100000)
    throw new Error("Import 1–100,000 data rows.");
  const grouped = new Map(),
    families = new Set();
  rows.forEach((row, i) => {
    const family = row[index.family]?.trim(),
      policy = row[index.policy]?.trim(),
      budget = Number(row[index.budget]),
      value = Number(row[index.heldout_exact]);
    if (
      !family ||
      !policy ||
      !row[index.budget]?.trim() ||
      !row[index.heldout_exact]?.trim() ||
      !Number.isInteger(budget) ||
      budget < 0 ||
      budget > 100 ||
      !Number.isFinite(value) ||
      value < 0 ||
      value > 1
    )
      throw new Error("Invalid measurement on CSV row " + (i + 2) + ".");
    families.add(family);
    const key = JSON.stringify([family, policy, budget]);
    const g = grouped.get(key) || { sum: 0, n: 0 };
    g.sum += value;
    g.n++;
    grouped.set(key, g);
  });
  const macro = new Map();
  for (const [key, g] of grouped) {
    const [, p, b] = JSON.parse(key),
      k = JSON.stringify([p, b]);
    macro.set(k, [...(macro.get(k) || []), g.sum / g.n]);
  }
  const results = {};
  for (const [key, values] of macro) {
    const [p, b] = JSON.parse(key);
    results[p] ||= {};
    results[p][b] = values.reduce((a, v) => a + v, 0) / values.length;
  }
  return {
    id: crypto.randomUUID(),
    name,
    created: new Date().toISOString(),
    rows: rows.length,
    results,
    families: [...families],
  };
}
export function citation(source) {
  return `@misc{${source.id},\n  title = {${source.title.replace(/[{}]/g, "")}},\n  author = {${source.authors.replace(/[{}]/g, "")}},\n  year = {${source.year}},\n  url = {${source.url}},\n  note = {Metadata checked 2026-11-06}\n}`;
}
