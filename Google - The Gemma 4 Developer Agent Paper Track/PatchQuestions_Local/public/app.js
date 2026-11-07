import { analyzeCsv, citation } from "./research-utils.js";
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const uid = () => crypto.randomUUID();
const pct = (value, digits = 1) => (Number(value) * 100).toFixed(digits) + "%";
const date = (value) =>
  new Date(
    value.length === 10 ? value + "T12:00:00+05:00" : value,
  ).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    timeZone: "Asia/Karachi",
  });
const DEADLINE = new Date("2026-11-12T23:59:00Z");
const WRITEUP =
  "https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/which-question-should-a-coding-agent-ask-before-ch";
const NOTEBOOK = "https://www.kaggle.com/code/muhammadnaveed624/patchquestions";
const methods = {
  random: "Random",
  random_split: "Informative random",
  diversity: "Most outcomes",
  entropy: "Entropy",
  lookahead: "Lookahead",
  frugal: "Frugal tree",
};
const families = {
  url_quote: "URL quoting",
  query_pairs: "Query parsing",
  csv_fields: "CSV reading",
  wrap: "Text wrapping",
  json_wire: "JSON serialization",
  regex_search: "Regex matching",
  base64_read: "Base64 decoding",
  hex_format: "Hex formatting",
};
const colors = {
  random: "#b5baa9",
  random_split: "#a79e65",
  diversity: "#bd886e",
  entropy: "#6c94a3",
  lookahead: "#a291b0",
  frugal: "#4d7144",
};
const providers = {
  gemini: "Google Gemini",
  openai: "OpenAI",
  anthropic: "Anthropic",
  groq: "Groq",
  openrouter: "OpenRouter",
};
const gates = {
  baseline: "Measured baseline",
  archive: "Reproducible archive",
  draft: "Kaggle draft prepared",
  novelty: "Prior-art comparison complete",
  blind: "Blind extension evaluated",
  gemma: "Gemma pilot documented",
  cost: "Question cost measured",
  reproduce: "Final notebook verified",
  submitted: "Kaggle submission confirmed",
};
const nav = [
  ["overview", "Overview", "grid"],
  ["experiments", "Experiments", "flask"],
  ["library", "Research library", "book"],
  ["adviser", "AI adviser", "spark"],
  ["sprint", "Sprint plan", "check"],
  ["paper", "Paper & submission", "file"],
  ["files", "Project files", "folder"],
];
const paths = {
  grid: "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
  flask: "M9 3h6M10 3v6L4 19a1 1 0 0 0 1 2h14a1 1 0 0 0 1-2L14 9V3M7 15h10",
  book: "M12 5C8 2 4 3 2 4v16c4-2 7-1 10 1 3-2 6-3 10-1V4c-4-2-7-2-10 1zm0 0v16",
  spark: "m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5z",
  check: "M9 5h12M9 12h12M9 19h12M3 5l1 1 2-2M3 12l1 1 2-2M3 19l1 1 2-2",
  file: "M5 2h9l5 5v15H5zM14 2v6h5M8 12h8M8 16h8",
  folder: "M3 5h7l2 3h9v12H3z",
  arrow: "M7 17 17 7M7 7h10v10",
  right: "M4 12h16m-6-6 6 6-6 6",
  clock: "M12 8v5l3 2M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0",
  plus: "M12 4v16M4 12h16",
  search: "M21 21l-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0",
  close: "M6 6l12 12M6 18 18 6",
  download: "M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5",
  upload: "M12 16V4m-5 5 5-5 5 5M4 16v5h16v-5",
  settings: "M4 6h16M4 12h16M4 18h16M8 3v6m8 0v6m-7 0v6",
  menu: "M3 6h18M3 12h18M3 18h18",
  circle: "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0",
  tick: "M4 12l5 5L20 6",
  bookmark: "M6 3h12v18l-6-4-6 4z",
  alert: "m12 3 10 18H2zm0 5v5m0 3v1",
  network: "M9 3h6v6H9zM3 15h6v6H3zM15 15h6v6h-6zM12 9v3M6 15v-3h12v3",
  send: "m22 2-7 20-4-9-9-4zm-11 11L22 2",
};
const icon = (name, size = 18) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${paths[name] || paths.file}"/></svg>`;
const badge = (text, tone = "") =>
  `<span class="badge ${tone}">${esc(text)}</span>`;
const button = (label, action, extra = "", kind = "", iconName = "") =>
  `<button class="btn ${kind}" data-action="${action}" ${extra}>${iconName ? icon(iconName, 15) : ""}${esc(label)}</button>`;
const link = (url, label, className = "text-link") =>
  `<a class="${className}" href="${esc(url)}" target="_blank" rel="noreferrer">${esc(label)} ${icon("arrow", 14)}</a>`;
const section = (title, detail = "", action = "") =>
  `<div class="section-head"><div><h2>${esc(title)}</h2>${detail ? `<p>${esc(detail)}</p>` : ""}</div>${action}</div>`;
const empty = (title, text) =>
  `<div class="empty">${icon("book", 28)}<h3>${esc(title)}</h3><p>${esc(text)}</p></div>`;
const state = {
  w: null,
  saved: null,
  baseline: null,
  sources: [],
  revision: 0,
  view: location.hash.slice(1) || "overview",
  saving: false,
  conflict: false,
  saveError: "",
  apiKey: "",
  models: [],
  providerBusy: false,
  connected: false,
  libraryQuery: "",
  libraryType: "all",
  libraryFilter: "all",
  expTab: "results",
  run: "baseline",
  budget: "3",
  family: "csv_fields",
  target: 0,
  asked: [],
  cases: null,
  prompt: "",
  aiBusy: false,
  aiError: "",
  includePaper: false,
  sourceSelection: [],
  showContext: false,
  discovery: [],
  importing: false,
  mobile: false,
  taskFilter: "all",
  manuscriptMode: "read",
  files: [],
};
const app = document.querySelector("#app");
let saveTimer, toastTimer, modalClose, aiController;
async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    signal: options.signal || AbortSignal.timeout(30000),
  });
  const data = await response.json();
  if (!response.ok) {
    const error = new Error(data.error || "Request failed.");
    error.status = response.status;
    throw error;
  }
  return data;
}
function toast(text) {
  const box = document.querySelector("#toast");
  box.innerHTML = icon("tick", 16) + `<span>${esc(text)}</span>`;
  box.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => box.classList.remove("show"), 5000);
}
function download(name, text, type = "application/json") {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function allSources() {
  return [...state.sources, ...state.w.customSources];
}
function mutate(fn, rerender = true) {
  const next = structuredClone(state.w);
  fn(next);
  state.w = next;
  clearTimeout(saveTimer);
  saveTimer = setTimeout(flush, 600);
  if (rerender) render();
  else saveIndicator();
}
function saveIndicator() {
  const el = document.querySelector("#save-status");
  if (el)
    el.innerHTML = `<i class="${state.saveError ? "bad" : ""}"></i>${esc(state.saveError ? "Unsaved changes" : state.saving ? "Saving changes" : state.w !== state.saved ? "Unsaved changes" : "All changes saved")}`;
}
async function flush() {
  if (state.saving || state.conflict || state.w === state.saved) return;
  const snapshot = state.w;
  state.saving = true;
  saveIndicator();
  try {
    const d = await api("/api/workspace", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workspace: snapshot, revision: state.revision }),
    });
    state.revision = d.revision;
    state.saved = snapshot;
    state.saveError = "";
  } catch (error) {
    state.saveError = error.message;
    state.conflict = error.status === 409;
    renderError();
  } finally {
    state.saving = false;
    saveIndicator();
  }
  if (state.saved === snapshot && state.w !== state.saved) void flush();
}
function renderError() {
  const box = document.querySelector("#save-error");
  if (box)
    box.innerHTML = state.saveError
      ? `${icon("alert", 18)}<span>${esc(state.saveError)}</span>${button("Export backup", "backup")}${button(state.conflict ? "Reload saved version" : "Retry save", state.conflict ? "reload" : "retry-save")}`
      : "";
}
function navigate(view) {
  if (![...nav.map((x) => x[0]), "settings"].includes(view)) view = "overview";
  state.view = view;
  state.mobile = false;
  history.replaceState(null, "", "#" + view);
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}
function ask(prompt) {
  state.prompt = prompt;
  navigate("adviser");
}
function nextTasks() {
  return [...state.w.tasks]
    .filter((t) => t.status !== "done")
    .sort((a, b) => {
      const ready = (t) =>
        t.status !== "blocked" &&
        t.depends.every(
          (id) => state.w.tasks.find((x) => x.id === id)?.status === "done",
        );
      return (
        Number(ready(b)) - Number(ready(a)) ||
        { high: 0, medium: 1, low: 2 }[a.priority] -
          { high: 0, medium: 1, low: 2 }[b.priority] ||
        a.due.localeCompare(b.due)
      );
    });
}
function stat(label, value, detail, ic) {
  return `<div class="stat"><div><span>${esc(label)}</span>${icon(ic, 16)}</div><strong>${esc(value)}</strong><p>${esc(detail)}</p></div>`;
}
function inline(text) {
  return esc(text)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(
      /\[([^\]]+)\]\((https:\/\/[^)]+)\)/g,
      (_, label, url) =>
        `<a href="${url}" target="_blank" rel="noreferrer">${label}</a>`,
    );
}
function markdown(text) {
  return `<div class="markdown">${text
    .split("\n")
    .map((line) => {
      if (line.startsWith("### ")) return `<h4>${inline(line.slice(4))}</h4>`;
      if (line.startsWith("## ")) return `<h3>${inline(line.slice(3))}</h3>`;
      if (line.startsWith("# ")) return `<h2>${inline(line.slice(2))}</h2>`;
      if (/^[-*] |^\d+[.)] /.test(line))
        return `<div class="md-list">• <span>${inline(line.replace(/^([-*]|\d+[.)]) /, ""))}</span></div>`;
      if (line.startsWith("|"))
        return `<div class="md-table">${esc(line)}</div>`;
      return line.trim()
        ? `<p>${inline(line)}</p>`
        : '<div class="md-space"></div>';
    })
    .join("")}</div>`;
}
function render() {
  if (!state.w) return;
  const days = Math.max(0, Math.floor((DEADLINE - Date.now()) / 86400000));
  app.innerHTML = `<aside class="sidebar ${state.mobile ? "open" : ""}"><button class="brand" data-view="overview"><span>${icon("network", 25)}</span><div>PatchQuestions<small>RESEARCH LAB</small></div></button><div class="project-switch"><i></i><div><strong>Gemma 4 · Paper Track</strong><span>Final-week workspace</span></div><span>⌄</span></div><div class="nav-label">WORKSPACE</div><nav>${nav.map(([id, label, ic]) => `<button class="${state.view === id ? "active" : ""}" data-view="${id}">${icon(ic)}<span>${label}</span>${id === "library" ? `<small>${allSources().length}</small>` : id === "adviser" ? '<i class="tiny-dot"></i>' : ""}</button>`).join("")}</nav><div class="sidebar-deadline">${icon("clock", 19)}<span>Submission deadline<strong>13 Nov · 04:59 PKT</strong></span><div class="deadline-track"><i style="width:${Math.min(100, Math.max(0, (1 - (DEADLINE - Date.now()) / (7 * 86400000)) * 100))}%"></i></div><p>${days} days to turn ideas into evidence</p></div><div class="sidebar-bottom"><button data-view="settings">${icon("settings")}Model & workspace settings</button><div class="profile"><i>MN</i><span><strong>Muhammad Naveed</strong><small>Private research workspace</small></span></div></div></aside>${state.mobile ? '<button class="shade" aria-label="Close navigation" data-action="close-nav"></button>' : ""}<main><header><div class="breadcrumbs"><button class="icon-btn mobile-menu" data-action="menu" aria-label="Open navigation">${icon("menu")}</button><span>Research workspace</span><b>›</b><strong>${esc(nav.find((x) => x[0] === state.view)?.[1] || "Settings")}</strong></div><div class="top-actions"><span id="save-status"></span>${link("https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview", "Competition")}</div></header><div id="save-error" class="error-banner"></div><div class="content">${({ overview, experiments, library, adviser, sprint, paper, files, settings }[state.view] || overview)()}</div><footer>PatchQuestions Research Lab<span>Evidence first. One focused experiment at a time.</span>${link("/project/research-evidence-notes.md", "Source verification notes")}</footer></main>`;
  saveIndicator();
  renderError();
  if (state.view === "files") void refreshFiles();
}
function heading(kicker, title, description, actions = "") {
  return `<div class="page-heading"><div><span class="eyebrow">${kicker}</span><h1>${title}</h1><p>${description}</p></div><div class="row gap">${actions}</div></div>`;
}
function overview() {
  const w = state.w,
    delta = Math.max(0, DEADLINE - Date.now()),
    d = Math.floor(delta / 86400000),
    h = Math.floor((delta % 86400000) / 3600000),
    ready = Object.values(w.gates).filter(Boolean).length;
  return `<div class="page-kicker"><i></i>GEMMA 4 DEVELOPER AGENT PAPER TRACK<span>${new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", timeZone: "Asia/Karachi" })}</span></div><div class="hero"><div><h1>Good research.<br><em>Clear next steps.</em></h1><p>Turn the PatchQuestions baseline into a stronger,<br>verifiable research submission.</p><div class="row gap">${button("Plan my next move", "plan", "", "primary", "spark")}${button("View sprint plan", "nav-sprint", "", "", "right")}</div></div><div class="countdown"><div>${icon("clock", 16)}The final week<i></i></div><strong>${delta > 0 ? `${d}<small>d</small> ${h}<small>h</small>` : "Closed"}</strong><p>Until the paper submission closes</p><div class="countdown-foot"><span>13 November 2026</span><b>04:59 PKT</b></div>${link("https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview/description", "Official timeline")}</div></div><div class="stats">${stat("EXPERIMENTS COMPLETED", w.experiments.filter((e) => e.status === "complete").length, w.experiments.filter((e) => e.status !== "complete").length + " awaiting evidence", "flask")}${stat("CURATED RESEARCH SOURCES", allSources().length, allSources().filter((s) => w.sourceState[s.id]?.read).length + " read · checked 6 Nov", "book")}${stat("SPRINT PROGRESS", w.tasks.filter((t) => t.status === "done").length + "/" + w.tasks.length, w.tasks.filter((t) => t.status === "doing").length + " in progress", "check")}${stat("RESEARCH READINESS", ready + "/" + Object.keys(gates).length, "Researcher-reviewed evidence gates", "circle")}</div><div class="two-col"><section>${section("Where to focus next", "Priorities based on the current research gaps", button("All tasks", "nav-sprint", "", "text-only", "right"))}<div class="focus-list">${nextTasks()
    .slice(0, 3)
    .map(
      (t, i) =>
        `<div class="focus-card"><i>${i + 1}</i><div><h3>${esc(t.title)}</h3><p>${esc(t.detail)}</p><div class="meta"><span>${icon("clock", 12)}${t.hours}h estimate</span><span>Due ${date(t.due)}</span>${badge(t.priority + " priority", "warm")}</div></div><button class="icon-btn" data-action="ask-task" data-id="${t.id}" aria-label="Discuss ${esc(t.title)}">${icon("arrow", 17)}</button></div>`,
    )
    .join(
      "",
    )}</div><div class="warning">${icon("alert", 18)}<div><strong>The most important evidence gap</strong><p>The baseline uses curated API configurations. A recorded Gemma pilot and a blind extension will help establish relevance beyond these controlled examples.</p></div></div></section><section>${section("What the evidence says", "Frozen baseline · 3 oracle questions")}<div class="panel evidence"><div class="evidence-number"><div><small>Frugal tree</small><strong>85.48<span>%</span></strong></div><div class="delta">+0.21 pp<small>vs entropy</small></div></div><div class="mini-bars">${["random_split", "entropy", "frugal"].map((m) => `<div><label>${methods[m]}</label><span><i style="width:${state.baseline.summary[m][3] * 100}%;background:${colors[m]}"></i></span><b>${pct(state.baseline.summary[m][3], 2)}</b></div>`).join("")}</div><p class="caption">Equal family weights across 8 API families. This measures agreement on every held-out input in the finite suite.</p>${button("Explore results and limitations", "nav-experiments", "", "text-only", "right")}</div><div class="insight"><span class="eyebrow">A RESULT WORTH FOLLOWING</span><h3>Better questions changed<br>the regex result.</h3><div><span>30.0%</span>${icon("right", 23)}<strong>86.25%</strong></div><p>Four redesigned probes. One exploratory family. Match question complexity before making a stronger claim.</p>${button("Inspect the experiment", "regex-experiment", "", "text-only", "right")}</div></section></div>${section("Start with the closest research", "Read these before making a novelty claim", button("Research library", "nav-library", "", "text-only", "right"))}<div class="source-previews">${allSources()
    .filter((s) => ["inpafer", "learn2fix", "xtestcluster"].includes(s.id))
    .map(
      (s) =>
        `<button class="source-preview" data-action="source" data-id="${s.id}"><div>${badge("Closest prior art", "green")}${icon("book", 17)}</div><h3>${esc(s.title)}</h3><p>${esc(s.summary)}</p><div class="source-foot"><span>${s.year} · Research paper</span>${icon("arrow", 17)}</div></button>`,
    )
    .join("")}</div>`;
}
function library() {
  const list = allSources().filter(
    (s) =>
      (state.libraryType === "all" || s.type === state.libraryType) &&
      (state.libraryFilter !== "saved" || state.w.sourceState[s.id]?.saved) &&
      (state.libraryFilter !== "unread" || !state.w.sourceState[s.id]?.read) &&
      (state.libraryFilter !== "high" || s.priority === "high") &&
      [s.title, s.authors, s.summary, ...s.tags]
        .join(" ")
        .toLowerCase()
        .includes(state.libraryQuery.toLowerCase()),
  );
  return (
    heading(
      "THE WORK BEHIND THE WORK",
      `Research library <small class="count-label">${allSources().length}</small>`,
      "Papers, engineering insights, expert talks and tools. With a reason to read each one.",
      button("Add a source", "add-source", "", "", "plus") +
        button("Discover research", "discover", "", "primary", "search"),
    ) +
    `<div class="library-note">${icon("book", 22)}<div><strong>Can Gemma choose a question when the API clues disappear?</strong><p>Read the <a href="/project/cognitive-core-study.md">paired experiment protocol and control result</a>, then explore Karpathy’s interview and the clarification studies below.</p></div></div><div class="toolbar"><label class="search">${icon("search", 17)}<input id="library-query" aria-label="Search research library" placeholder="Search a paper, author, idea or topic…" value="${esc(state.libraryQuery)}"></label><select id="library-filter" aria-label="Filter reading list">${options({ all: "All sources", high: "High priority", saved: "Saved reading list", unread: "Unread sources" }, state.libraryFilter)}</select>${button("Citations", "citations", "", "", "download")}</div><div class="tabs">${[
      ["all", "All resources"],
      ["paper", "Papers"],
      ["article", "Articles"],
      ["video", "Videos"],
      ["talk", "Expert talks"],
      ["news", "News"],
      ["documentation", "Documentation"],
    ]
      .map(
        ([id, n]) =>
          `<button data-action="library-type" data-id="${id}" class="${state.libraryType === id ? "active" : ""}">${n}<small>${id === "all" ? allSources().length : allSources().filter((s) => s.type === id).length}</small></button>`,
      )
      .join(
        "",
      )}</div><p class="results-label">${list.length} sources <span>Curated and checked 6 November 2026 · expandable reading list</span></p><div class="library-grid">${list
      .map(
        (s) =>
          `<article class="source-card"><div class="row between"><span class="source-type">${icon(s.type === "video" || s.type === "talk" ? "send" : "file", 15)}${esc(s.type)} · ${s.year}</span><button class="icon-btn ${state.w.sourceState[s.id]?.saved ? "saved" : ""}" data-action="bookmark" data-id="${s.id}" aria-label="Save ${esc(s.title)}">${icon("bookmark", 17)}</button></div><button class="card-title" data-action="source" data-id="${s.id}"><h3>${esc(s.title)}</h3></button><p class="byline">${esc(s.authors)}</p><p>${esc(s.summary)}</p><div class="tags">${s.tags
            .slice(0, 3)
            .map((t) => `<span>${esc(t)}</span>`)
            .join(
              "",
            )}</div><div class="source-foot"><span>${s.priority === "high" ? "● Priority reading" : "Supporting context"}${state.w.sourceState[s.id]?.read ? " · Read" : ""}</span><button class="text-link" data-action="source" data-id="${s.id}">Briefing ${icon("arrow", 14)}</button></div></article>`,
      )
      .join(
        "",
      )}</div>${list.length ? "" : empty("No matching sources", "Try another term or clear the filter.")}`
  );
}
function options(map, current) {
  return Object.entries(map)
    .map(
      ([id, label]) =>
        `<option value="${esc(id)}" ${current === id ? "selected" : ""}>${esc(label)}</option>`,
    )
    .join("");
}
function chart(results) {
  const width = 820,
    height = 245,
    left = 48,
    top = 15,
    plotW = 745,
    plotH = 180;
  const budgets = [
    ...new Set(
      Object.values(results)
        .flatMap((v) => Object.keys(v))
        .map(Number),
    ),
  ].sort((a, b) => a - b);
  const max = Math.max(3, ...budgets);
  const x = (b) => left + (b / max) * plotW,
    y = (v) => top + (1 - v) * plotH;
  return `<svg class="chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="Behavioral agreement by question budget"><title>Exact finite-suite agreement, by policy and oracle question budget</title>${[0, 0.25, 0.5, 0.75, 1].map((v) => `<line x1="${left}" x2="${left + plotW}" y1="${y(v)}" y2="${y(v)}" stroke="#e3e8da" stroke-dasharray="3 4"/><text x="${left - 10}" y="${y(v) + 4}" text-anchor="end">${v * 100}%</text>`).join("")}${budgets.map((b) => `<text x="${x(b)}" y="${y(0) + 23}" text-anchor="middle">${b}</text>`).join("")}${Object.entries(
    results,
  )
    .map(([m, values]) => {
      const points = budgets
        .filter((b) => values[b] !== undefined)
        .map((b) => [x(b), y(values[b])]);
      return `<polyline fill="none" stroke="${colors[m] || "#888"}" stroke-width="${m === "frugal" ? 3 : 1.7}" points="${points.map((p) => p.join(",")).join(" ")}"/>${points.map((p) => `<circle cx="${p[0]}" cy="${p[1]}" r="3" fill="${colors[m] || "#888"}"/>`).join("")}`;
    })
    .join(
      "",
    )}<text x="${width / 2}" y="${height - 5}" text-anchor="middle">Trusted oracle questions</text></svg><div class="chart-legend">${Object.keys(
    results,
  )
    .map(
      (m) =>
        `<span><i style="background:${colors[m] || "#888"}"></i>${esc(methods[m] || m)}</span>`,
    )
    .join("")}</div>`;
}
function experiments() {
  const results =
    state.run === "baseline"
      ? state.baseline.summary
      : state.w.runs.find((r) => r.id === state.run)?.results ||
        state.baseline.summary;
  return (
    heading(
      "MEASURE. QUESTION. REPEAT.",
      "Experiments",
      "Inspect the evidence, test the next hypothesis and keep an honest record.",
      button(
        state.importing ? "Importing…" : "Import scores CSV",
        "import-run",
        state.importing ? "disabled" : "",
        "",
        "upload",
      ) + button("New experiment", "new-experiment", "", "primary", "plus"),
    ) +
    `<input id="score-upload" type="file" accept=".csv" hidden><div class="tabs">${[
      ["results", "Results explorer"],
      ["register", "Experiment register"],
      ["sandbox", "Probe sandbox"],
    ]
      .map(
        ([id, label]) =>
          `<button data-action="experiment-tab" data-id="${id}" class="${state.expTab === id ? "active" : ""}">${label}</button>`,
      )
      .join("")}</div>${
      state.expTab === "sandbox"
        ? sandbox()
        : state.expTab === "register"
          ? `<div class="experiment-grid">${state.w.experiments.map((e) => `<button class="experiment-card" data-action="experiment" data-id="${e.id}"><div class="row between">${icon("flask", 20)}${badge(e.status, e.status === "complete" ? "green" : "")}</div><h3>${esc(e.title)}</h3><p>${esc(e.hypothesis)}</p><div class="experiment-result">${esc(e.result || "Evidence has not been collected yet.")}</div><div class="source-foot">${esc(e.metric)} ${icon("arrow", 16)}</div></button>`).join("")}</div>`
          : `<div class="toolbar"><select id="run-choice" aria-label="Choose results run">${options({ baseline: "Frozen baseline · CPython 3.12.14", ...Object.fromEntries(state.w.runs.map((r) => [r.id, r.name])) }, state.run)}</select><select id="budget" aria-label="Question budget">${options(Object.fromEntries([0, 1, 2, 3].map((b) => [String(b), b + " oracle questions"])), state.budget)}</select>${button("Ask AI to critique", "critique-results", "", "soft", "spark")}</div><div class="panel chart-panel">${section("Question budget vs. behavioral agreement", state.run === "baseline" ? "Exact expectations · eight API families · 750 target/split episodes" : "Imported CSV · family-macro averaging")}${chart(results)}</div><div class="panel table-panel"><div class="panel-head"><h3>Policy comparison</h3>${badge("Budget " + state.budget)}</div><div class="table-scroll"><table><thead><tr><th>Policy</th><th>Held-out agreement</th><th>Evidence</th></tr></thead><tbody>${Object.entries(
              results,
            )
              .map(
                ([m, r]) =>
                  `<tr><td><i class="color-dot" style="background:${colors[m]}"></i>${esc(methods[m] || m)}</td><td>${r[state.budget] === undefined ? "—" : pct(r[state.budget], 2)}</td><td>${state.run === "baseline" ? "Measured finite-suite expectation" : "Imported · awaiting review"}</td></tr>`,
              )
              .join(
                "",
              )}</tbody></table></div><p class="caption">Equal family weights. A candidate succeeds only when it matches every held-out input, including exception classes. Repeated configurations do not form independent bug samples.</p></div>${
              state.run === "baseline"
                ? `<div class="panel table-panel"><div class="panel-head"><h3>Where performance changes</h3><span>Three questions · all-probes reference</span></div><div class="table-scroll"><table><thead><tr><th>API family</th><th>Informative random</th><th>Entropy</th><th>Frugal tree</th><th>All probes</th></tr></thead><tbody>${Object.entries(
                    state.baseline.audit,
                  )
                    .map(
                      ([f, r]) =>
                        `<tr><td>${families[f]}</td><td>${pct(r.random_split[0])}</td><td>${pct(r.entropy[0])}</td><td>${pct(r.frugal[0])}</td><td>${pct(r.ceiling)}</td></tr>`,
                    )
                    .join("")}</tbody></table></div></div>`
                : ""
            }<div class="warning">${icon("alert", 19)}<div><strong>Interpret results at their tested scope</strong><p>Curated candidates, perfect oracle labels and a correct candidate in every pool. Model-generated patches, realistic question cost and a blind extension remain open experiments.</p></div></div>`
    }`
  );
}
function sandbox() {
  if (!state.cases) {
    void loadCases();
    return empty(
      "Loading frozen cases",
      "Preparing the candidate behavior matrix.",
    );
  }
  const c = state.cases.find(
    (x) => x.family === state.family && x.split === 19,
  );
  const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const alive = c.configs
    .map((_, i) => i)
    .filter((i) =>
      state.asked.every((j) =>
        eq(c.query_outputs[i][j], c.query_outputs[state.target][j]),
      ),
    );
  const probes = c.query_inputs
    .map((input, j) => {
      const counts = {};
      alive.forEach((i) => {
        const out = JSON.stringify(c.query_outputs[i][j]);
        counts[out] = (counts[out] || 0) + 1;
      });
      return {
        input,
        j,
        groups: Object.keys(counts).length,
        entropy: -Object.values(counts).reduce(
          (s, n) => s + (n / alive.length) * Math.log2(n / alive.length),
          0,
        ),
      };
    })
    .sort((a, b) => b.entropy - a.entropy);
  return `<div class="library-note"><div><span class="eyebrow">INTERACTIVE WALKTHROUGH</span><h2>See why a question helps.</h2><p>Choose a simulated intended configuration and reveal up to three expected outputs. This explains the method. A blind model evaluation must keep its target and grading data outside the agent’s context.</p></div>${icon("network", 45)}</div><div class="toolbar"><select id="sandbox-family" aria-label="Sandbox API family">${options(families, state.family)}</select><label>Simulated target <select id="sandbox-target" aria-label="Simulated intended configuration">${options(Object.fromEntries(c.configs.map((_, i) => [String(i), "Candidate " + (i + 1)])), String(state.target))}</select></label>${button("Reset", "sandbox-reset")}</div><div class="stats three">${stat("CANDIDATES REMAINING", alive.length + "/" + c.configs.length, "Consistent with revealed outputs", "network")}${stat("QUESTIONS USED", state.asked.length + "/3", "Trusted labels", "book")}${stat("HELD-OUT AGREEMENT", pct(alive.filter((i) => eq(c.heldout_outputs[i], c.heldout_outputs[state.target])).length / alive.length), "Uniform draw among survivors", "circle")}</div><div class="two-col"><div class="panel"><div class="panel-head"><h3>Choose a distinguishing input</h3>${badge("Sorted by entropy")}</div><div class="probe-list">${probes.map((p) => `<button data-action="probe" data-id="${p.j}" ${state.asked.includes(p.j) || state.asked.length >= 3 ? "disabled" : ""}><code>${esc(JSON.stringify(p.input))}</code><span>${p.groups} outcomes · ${p.entropy.toFixed(2)} bits</span>${icon(state.asked.includes(p.j) ? "tick" : "right", 15)}</button>`).join("")}</div></div><div class="panel"><div class="panel-head"><h3>What the oracle answered</h3></div>${state.asked.length ? state.asked.map((j, i) => `<div class="oracle-answer"><small>QUESTION ${i + 1}</small><code>${esc(JSON.stringify(c.query_inputs[j]))}</code><pre>${esc(JSON.stringify(c.query_outputs[state.target][j], null, 2))}</pre></div>`).join("") : empty("Ask your first question", "An input where candidates disagree can eliminate uncertainty.")}<div class="candidate-chips">${c.configs.map((_, i) => `<span class="${alive.includes(i) ? "survives" : "eliminated"}">Candidate ${i + 1}</span>`).join("")}</div></div></div>`;
}
async function loadCases() {
  try {
    state.cases = await api("/cases.json");
    if (state.view === "experiments") render();
  } catch (e) {
    toast(e.message);
  }
}
function evidence() {
  return {
    project: "PatchQuestions",
    deadline: DEADLINE.toISOString(),
    baseline: state.baseline,
    experiments: state.w.experiments,
    tasks: state.w.tasks,
    notes: state.w.notes,
    readiness: state.w.gates,
    importedRuns: state.w.runs,
    sources: allSources()
      .filter((s) => state.sourceSelection.includes(s.id))
      .map((s) => ({
        id: s.id,
        title: s.title,
        url: s.url,
        summary: s.summary,
        action: s.action,
        caveat: s.caveat,
        notes: state.w.sourceState[s.id]?.notes || "",
      })),
    ...(state.includePaper ? { manuscript: state.w.manuscript } : {}),
  };
}
function adviser() {
  return (
    heading(
      "A THINKING PARTNER, GROUNDED IN YOUR WORK",
      "AI research adviser",
      "Analyze the evidence, challenge claims and choose the next useful experiment.",
      button(
        state.apiKey && state.w.settings.model
          ? providers[state.w.settings.provider] +
              " · " +
              state.w.settings.model
          : "Connect an API model",
        "nav-settings",
        "",
        "",
        "settings",
      ),
    ) +
    `<div class="adviser-layout"><section class="panel chat-panel">${
      state.w.messages.length
        ? ""
        : `<div class="chat-welcome"><span>${icon("spark", 29)}</span><h2>What should we learn next?</h2><p>Your baseline, experiment register, sprint plan and selected research travel with each question.</p><div class="prompt-grid">${[
            ["next", "Plan the next experiment"],
            ["novelty", "Challenge our novelty"],
            ["regex", "Analyze the regex finding"],
            ["gemma", "Prepare a Gemma pilot"],
          ]
            .map(
              ([id, label]) =>
                `<button data-action="prompt" data-id="${id}">${label}${icon("arrow", 15)}</button>`,
            )
            .join("")}</div></div>`
    }<div class="chat-messages">${state.w.messages.map((m) => `<article class="message ${m.role}"><div class="message-head"><span>${m.role === "assistant" ? icon("spark", 15) : "MN"}</span><strong>${m.role === "assistant" ? "Research adviser" : "You"}</strong><small>${m.role === "assistant" ? esc(providers[m.provider] || m.provider) + " · " + esc(m.model) : date(m.created)}</small></div>${markdown(m.text)}${m.role === "assistant" ? `<div class="message-foot"><button data-action="advice-task" data-id="${m.id}" class="text-link">${icon("plus", 13)}Turn advice into a task</button><button data-action="save-advice" data-id="${m.id}" class="text-link">${icon("bookmark", 13)}Save as note</button><details><summary>Usage</summary><code>${esc(m.usage)}</code></details></div>` : ""}</article>`).join("")}</div>${state.aiBusy ? `<div class="thinking">Reviewing your evidence…${button("Cancel", "cancel-ai")}</div>` : ""}${state.aiError ? `<div class="inline-error">${esc(state.aiError)}</div>` : ""}<div class="chat-composer"><textarea id="ai-prompt" aria-label="Ask your research adviser" rows="3" maxlength="12000" placeholder="Ask about your next experiment, a result, a paper or the submission…">${esc(state.prompt)}</textarea><div><span><i></i>${state.sourceSelection.length} sources + project evidence</span>${button("Send", "send-ai", state.aiBusy ? "disabled" : "", "primary", "send")}</div><p class="caption">Each send calls your selected provider and may incur API charges. The model receives the evidence at right. It has no live browsing or experiment execution.</p></div></section><aside class="context-panel"><div class="panel"><div class="panel-head"><h3>Included evidence</h3>${icon("check", 17)}</div><div class="context-item">${icon("tick", 14)}Frozen baseline and provenance</div><div class="context-item">${icon("tick", 14)}Experiments, sprint and notes</div><label class="context-item"><input id="include-paper" type="checkbox" ${state.includePaper ? "checked" : ""}>Include current manuscript</label><div class="row between"><strong>Research selection</strong><button class="text-link" data-action="priority-sources">Priority set</button></div><div class="context-sources">${allSources()
      .map(
        (s) =>
          `<label><input data-select-source="${s.id}" type="checkbox" ${state.sourceSelection.includes(s.id) ? "checked" : ""}><span>${esc(s.title)}<small>[${esc(s.id)}]</small></span></label>`,
      )
      .join(
        "",
      )}</div>${button(state.showContext ? "Hide request evidence" : "Inspect request evidence", "toggle-context", "", "text-only")}${state.showContext ? `<pre class="context-preview">${esc(JSON.stringify(evidence(), null, 2))}</pre>` : ""}</div><p class="caption">Advice is a proposal. Confirm claims against original sources and record measured results before updating the paper.</p></aside></div>`
  );
}
async function sendAI() {
  state.prompt = document.querySelector("#ai-prompt")?.value || state.prompt;
  if (!state.prompt.trim() || state.aiBusy) return;
  if (!state.apiKey || !state.w.settings.model) {
    toast("Connect a provider and choose a text model first.");
    navigate("settings");
    return;
  }
  const context = JSON.stringify(evidence());
  if (context.length > 65000) {
    state.aiError =
      "This evidence selection is too large. Deselect sources or omit the manuscript.";
    render();
    return;
  }
  const question = state.prompt;
  state.aiBusy = true;
  state.aiError = "";
  aiController = new AbortController();
  render();
  try {
    const d = await api("/api/ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "generate",
        provider: state.w.settings.provider,
        apiKey: state.apiKey,
        model: state.w.settings.model,
        maxTokens: state.w.settings.maxTokens,
        prompt: question,
        context,
        history: state.w.messages
          .slice(-10)
          .map((m) => ({ role: m.role, content: m.text.slice(0, 10000) })),
      }),
      signal: aiController.signal,
    });
    mutate((w) => {
      const created = new Date().toISOString();
      w.messages = [
        ...w.messages,
        { id: uid(), role: "user", text: question, created },
        {
          id: uid(),
          role: "assistant",
          text: d.answer,
          created,
          model: w.settings.model,
          provider: w.settings.provider,
          usage: JSON.stringify(d.usage).slice(0, 500),
        },
      ].slice(-200);
    }, false);
    state.prompt = "";
    if (d.incomplete)
      state.aiError =
        "The response reached its output limit. Increase the budget in settings if needed.";
  } catch (e) {
    state.aiError =
      e.name === "AbortError"
        ? "Request cancelled. The provider may already have processed part of it."
        : e.message;
  } finally {
    state.aiBusy = false;
    aiController = null;
    if (state.view === "adviser") render();
  }
}
const prompts = {
  next: "Given the actual time remaining and current evidence, propose the three highest-value next research actions. Include time estimates, a precise protocol, acceptance criteria and stopping rules.",
  novelty:
    "Compare PatchQuestions to InPaFer, LEARN2FIX, DiffTGen and xTestCluster. Identify overlap, defensible differences and the evidence needed for a credible contribution.",
  regex:
    "Critique the compound-regex probe finding. Design a cost-matched confirmatory test on a frozen unseen suite, including noisy oracle labels.",
  gemma:
    "Design a minimal reproducible Gemma 4 candidate/probe generation pilot for 10–20 fixed tasks. Keep grading data blind and report absent-correct-candidate cases, prompts, model version, token use and seeds.",
};
function sprint() {
  return (
    heading(
      "A SHORT RUNWAY. A FOCUSED PLAN.",
      "The final-week sprint",
      "Prioritize evidence that can change the paper. Leave room to reproduce and submit.",
      button("Review the plan", "review-sprint", "", "", "spark") +
        button("Add task", "new-task", "", "primary", "plus"),
    ) +
    `<div class="week-strip">${Array.from({ length: 7 }, (_, i) => {
      const day = "2026-11-" + String(6 + i).padStart(2, "0"),
        ts = state.w.tasks.filter((t) => t.due === day);
      return `<div><small>${["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"][i]}</small><strong>${6 + i}</strong><span>${ts.filter((t) => t.status === "done").length}/${ts.length} complete</span><div><i style="width:${ts.length ? (ts.filter((t) => t.status === "done").length / ts.length) * 100 : 0}%"></i></div></div>`;
    }).join(
      "",
    )}</div><div class="sprint-summary"><span><strong>${state.w.tasks.filter((t) => t.status === "done").length}</strong> completed</span><span><strong>${state.w.tasks.filter((t) => t.status === "doing").length}</strong> in progress</span><span><strong>${state.w.tasks.filter((t) => t.status === "blocked").length}</strong> blocked</span><span><strong>${state.w.tasks.filter((t) => t.status !== "done").reduce((n, t) => n + t.hours, 0)}h</strong> remaining estimate</span><select id="task-filter" aria-label="Filter sprint tasks">${options({ all: "All tasks", todo: "To do", doing: "In progress", done: "Complete", blocked: "Blocked" }, state.taskFilter)}</select></div><div class="task-list">${state.w.tasks
      .filter(
        (t) => state.taskFilter === "all" || t.status === state.taskFilter,
      )
      .map((t) => {
        const dependencies = t.depends.filter(
          (id) => state.w.tasks.find((x) => x.id === id)?.status !== "done",
        );
        return `<article class="task-card ${t.status === "done" ? "completed" : ""}"><button class="task-check" data-action="toggle-task" data-id="${t.id}" aria-label="${t.status === "done" ? "Reopen" : "Complete"} ${esc(t.title)}">${icon(t.status === "done" ? "tick" : "circle", 22)}</button><div><h3><button data-action="edit-task" data-id="${t.id}">${esc(t.title)}</button>${badge(t.priority, "warm")}</h3><p>${esc(t.detail)}</p><div class="meta"><span>${icon("clock", 12)}${t.hours}h</span><span>Due ${date(t.due)}</span>${dependencies.length ? `<span class="dependency">Depends on ${dependencies.length} unfinished task(s)</span>` : ""}</div></div><select data-task-status="${t.id}" aria-label="Status for ${esc(t.title)}">${options({ todo: "To do", doing: "In progress", done: "Complete", blocked: "Blocked" }, t.status)}</select><button data-action="ask-task" data-id="${t.id}" class="icon-btn" aria-label="Discuss ${esc(t.title)}">${icon("spark", 17)}</button></article>`;
      })
      .join(
        "",
      )}</div><div class="buffer-note">${icon("clock", 20)}<p><strong>Protect the submission buffer.</strong> Target 12 November at 18:00 PKT. The official close is 13 November at 04:59 PKT.</p></div>`
  );
}
function paper() {
  const words = state.w.manuscript.trim().split(/\s+/).length;
  return (
    heading(
      "TURN THE EVIDENCE INTO A CLEAR CONTRIBUTION",
      "Paper & submission",
      "Keep claims, citations, research decisions and final checks in one place.",
      button("Request paper review", "paper-review", "", "", "spark") +
        button("Export manuscript", "export-paper", "", "primary", "download"),
    ) +
    `<div class="submission-banner"><div>${badge("Kaggle draft prepared", "green")}<p>Last verified 6 November. Check the live submission status on Kaggle.</p></div>${link(WRITEUP, "Open Kaggle writeup", "btn")}${link(NOTEBOOK, "Companion notebook", "btn")}</div><div class="paper-layout"><section class="panel"><div class="panel-head"><div class="segment"><button class="${state.manuscriptMode === "read" ? "active" : ""}" data-action="paper-mode" data-id="read">Read</button><button class="${state.manuscriptMode === "edit" ? "active" : ""}" data-action="paper-mode" data-id="edit">Edit manuscript</button></div><span id="word-count">${badge(words.toLocaleString() + " / 3,000 words", words > 3000 ? "warm" : "green")}</span></div>${state.manuscriptMode === "edit" ? `<textarea id="manuscript" class="manuscript-editor" aria-label="Manuscript editor" maxlength="100000">${esc(state.w.manuscript)}</textarea>` : `<div class="manuscript-text">${markdown(state.w.manuscript)}</div>`}</section><aside><div class="panel readiness"><div class="panel-head"><h3>Evidence readiness</h3>${badge(Object.values(state.w.gates).filter(Boolean).length + "/" + Object.keys(gates).length)}</div><p class="caption">Researcher-reviewed checks. These do not synchronize or submit the Kaggle entry.</p>${Object.entries(
      gates,
    )
      .map(
        ([id, label]) =>
          `<label><input type="checkbox" data-gate="${id}" ${state.w.gates[id] ? "checked" : ""}>${label}</label>`,
      )
      .join(
        "",
      )}</div><div class="panel rubric"><h3>What the judges assess</h3>${[
      ["Novelty", "Distinguish the contribution from closest prior work."],
      ["Quality", "Show what generalizes beyond the original families."],
      ["Relevance", "Connect the resource to agentic software engineering."],
      ["Verifiability", "Record methods, prompts, data and results."],
      ["Clarity", "Keep the claim focused and reproducible."],
    ]
      .map(([t, p]) => `<div><strong>${t}</strong><p>${p}</p></div>`)
      .join(
        "",
      )}<p class="caption">Five equally weighted criteria. This checklist does not estimate a judge’s score.</p>${link("https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview/description", "Official rubric")}</div></aside></div>${section("Research notes & decisions", "Record why the method changed and which claims are supported.")}<div class="notes-layout"><form id="note-form" class="panel form-card"><label>Decision or note title<input name="title" required maxlength="500" placeholder="What changed, and why?"></label><label>Evidence and reasoning<textarea name="text" required maxlength="30000" rows="6" placeholder="Link the experiment or source. Record the decision and its limits."></textarea></label><button class="btn primary" type="submit">${icon("plus", 15)}Save research note</button></form><div>${state.w.notes
      .slice()
      .reverse()
      .map(
        (n) =>
          `<article class="panel note"><span class="eyebrow">${date(n.created)}</span><h3>${esc(n.title)}</h3>${markdown(n.text)}</article>`,
      )
      .join("")}</div></div>`
  );
}
const fileList = [
  [
    "PatchQuestions_Research_Package.zip",
    "Complete research package",
    "Source, frozen data, scores, paper and reproduction notes",
    "ZIP",
  ],
  [
    "PatchQuestions.ipynb",
    "Reproducible notebook",
    "Self-contained CPU notebook for Kaggle or Jupyter",
    "IPYNB",
  ],
  [
    "scores.csv",
    "Per-target measurements",
    "18,000 rows across six policies and four budgets",
    "CSV",
  ],
  [
    "frozen_cases.jsonl.gz",
    "Frozen behavior matrices",
    "40 case records with query and grading outputs",
    "GZ",
  ],
  [
    "research-library.json",
    "Verified research library",
    "Source metadata, summaries, actions and caveats",
    "JSON",
  ],
  [
    "PatchQuestions_Writeup.md",
    "Original paper draft",
    "Frozen report behind the initial Kaggle writeup",
    "MD",
  ],
  [
    "benchmark.py",
    "Benchmark implementation",
    "Finite candidates, probes and reference policies",
    "PY",
  ],
  [
    "replay.py",
    "Blinded evaluation protocol",
    "JSON stdin/stdout runner; isolate target from agent",
    "PY",
  ],
  [
    "verify.py",
    "Independent checks",
    "Depth-two enumeration and protocol smoke checks",
    "PY",
  ],
  [
    "intervention.py",
    "Regex follow-up experiment",
    "Original, single-flag and compound probe comparison",
    "PY",
  ],
];
function files() {
  return (
    heading(
      "A TRACEABLE RESEARCH RECORD",
      "Project files",
      "The original resource, supporting measurements and new run artifacts.",
      button("Workspace backup", "backup", "", "", "download") +
        button("Upload evidence", "upload-evidence", "", "primary", "upload"),
    ) +
    `<input hidden type="file" id="evidence-upload"><div class="provenance">${icon("check", 21)}<div><strong>Frozen baseline · CPython 3.12.14</strong><p>Captured 6 November 2026. Archive SHA-256 <code>${state.baseline.sha256}</code></p></div></div><div class="file-grid">${fileList.map(([name, title, detail, ext]) => `<a class="file-card" href="/project/${name}" download><span>${ext}</span><div><h3>${title}</h3><p>${detail}</p><small>${name}</small></div>${icon("download", 17)}</a>`).join("")}</div>${section("Uploaded evidence", "Run logs, frozen protocols, prompts and new measurements. Maximum 5 MB per file.")}<div id="uploaded-files">${uploadTable()}</div><div class="file-note"><strong>Run experiments in Kaggle or your Python environment.</strong><p>The app analyzes score CSVs and keeps records. Uploading source archives it; execution takes place in your experiment environment. Keep grading matrices outside an evaluated agent’s context.</p></div>`
  );
}
function uploadTable() {
  return state.files.length
    ? `<div class="panel table-scroll"><table><thead><tr><th>File</th><th>Size</th><th>Uploaded</th><th>Download</th></tr></thead><tbody>${state.files.map((f) => `<tr><td>${esc(f.name)}</td><td>${(f.size / 1024).toFixed(1)} KB</td><td>${date(f.created_at)}</td><td><a class="text-link" href="/api/files?id=${encodeURIComponent(f.id)}">${icon("download", 15)}Download</a></td></tr>`).join("")}</tbody></table></div>`
    : empty(
        "Build the evidence trail",
        "Upload the frozen protocol, Gemma prompts, run logs and new scores as research progresses.",
      );
}
async function refreshFiles() {
  try {
    const d = await api("/api/files");
    state.files = d.files || [];
    const box = document.querySelector("#uploaded-files");
    if (box) box.innerHTML = uploadTable();
  } catch (e) {
    toast(e.message);
  }
}
function settings() {
  return (
    heading(
      "YOUR MODEL, YOUR RESEARCH",
      "Model & workspace settings",
      "Connect a provider API to make the research adviser available.",
    ) +
    `<div class="settings-layout"><div class="panel settings-card">${section("AI provider", "Requests go through the app server to the provider you choose.")}<label>Provider<select id="provider">${options(providers, state.w.settings.provider)}</select></label><label>API key<input id="api-key" type="password" autocomplete="off" spellcheck="false" maxlength="1000" value="${esc(state.apiKey)}" placeholder="Paste your provider API key"></label><p class="caption">Your key stays in this page’s memory and is sent only to the app server and selected provider for your requests. It is excluded from saved records and exports. Re-enter it after a reload.</p><div class="row gap">${button(state.providerBusy ? "Connecting…" : "Fetch available models", "connect-provider", state.providerBusy ? "disabled" : "", "primary", "network")}${state.apiKey ? button("Clear key", "clear-key") : ""}</div>${state.connected ? `<p class="connection-success">✓ Provider returned ${state.models.length} available model IDs.</p>` : ""}<label>Model ID<input id="model" list="model-options" maxlength="200" value="${esc(state.w.settings.model)}" placeholder="Choose a returned ID or enter an exact ID"><datalist id="model-options">${state.models.map((m) => `<option value="${esc(m.id)}">${esc(m.name)}</option>`).join("")}</datalist></label><p class="caption">Discovery lists account access. Choose a text model supported by the provider’s generation endpoint.</p><label>Maximum output tokens <strong id="token-value">${state.w.settings.maxTokens.toLocaleString()}</strong><input id="max-tokens" type="range" min="512" max="8000" step="128" value="${state.w.settings.maxTokens}"></label><p class="caption">This limits output, including model reasoning where applicable. Input-token charges and pricing depend on your provider. Generation runs only when you press Send.</p></div><div><div class="panel settings-card"><h3>Private research workspace</h3><p>Tasks, notes, reading progress, experiments, manuscript edits and adviser conversations save across sessions.</p><div class="row gap wrap">${button("Export backup", "backup", "", "", "download")}${button("Restore backup", "restore", "", "", "upload")}</div><input id="backup-upload" type="file" accept=".json" hidden><hr><h3>Official deadline</h3><strong>13 November 2026 · 04:59 PKT</strong><p>12 November · 23:59 UTC. The plan aims to finish several hours earlier. Check Kaggle for organizer changes.</p>${link("https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview/description", "Official requirements")}</div><p class="caption">The adviser helps analyze research. Gemma experiments require their own recorded model, prompts, evaluation protocol and run artifacts.</p></div></div>`
  );
}
function showModal(title, html, onSubmit) {
  const overlay = document.querySelector("#overlay"),
    previous = document.activeElement;
  overlay.innerHTML = `<div class="modal-backdrop"><section class="modal" role="dialog" aria-modal="true" aria-label="${esc(title)}"><div class="modal-head"><h2>${esc(title)}</h2><button data-action="close-modal" class="icon-btn" aria-label="Close dialog">${icon("close", 20)}</button></div>${html}</section></div>`;
  document.body.style.overflow = "hidden";
  const close = () => {
    overlay.innerHTML = "";
    document.body.style.overflow = "";
    document.removeEventListener("keydown", trap);
    modalClose = null;
    render();
    previous?.focus();
  };
  const trap = (e) => {
    if (e.key === "Escape") close();
    if (e.key === "Tab") {
      const list = [
        ...overlay.querySelectorAll(
          "button:not([disabled]),a[href],input,textarea,select",
        ),
      ];
      if (e.shiftKey && document.activeElement === list[0]) {
        e.preventDefault();
        list.at(-1)?.focus();
      } else if (!e.shiftKey && document.activeElement === list.at(-1)) {
        e.preventDefault();
        list[0]?.focus();
      }
    }
  };
  document.addEventListener("keydown", trap);
  overlay.querySelector("button")?.focus();
  overlay.querySelector(".modal-backdrop").onclick = (e) => {
    if (e.target === e.currentTarget) close();
  };
  if (onSubmit)
    overlay.querySelector("form").onsubmit = (e) => {
      e.preventDefault();
      onSubmit(new FormData(e.target), e.target);
    };
  modalClose = close;
}
function openSource(id) {
  const s = allSources().find((x) => x.id === id),
    p = state.w.sourceState[id] || { read: false, saved: false, notes: "" };
  showModal(
    "Research briefing",
    `<div class="row gap">${badge(s.type, "green")}${badge(s.category)}<span class="muted">${s.year}</span></div><h2 class="source-detail-title">${esc(s.title)}</h2><p class="authors">${esc(s.authors)}</p><p class="lede">${esc(s.summary)}</p><div class="brief"><h4>How to use it this week</h4><p>${esc(s.action)}</p></div><div class="brief caution"><h4>What to keep in mind</h4><p>${esc(s.caveat)}</p></div><div class="row gap wrap source-links">${link(s.url, s.type === "video" || s.type === "talk" ? "Open video / talk" : "Open original source", "btn primary")}${s.pdfUrl ? link(s.pdfUrl, "Open paper PDF", "btn") : ""}${button("Export citation", "source-citation", `data-id="${s.id}"`, "", "download")}</div><div class="source-toggles"><label><input data-source-read="${s.id}" type="checkbox" ${p.read ? "checked" : ""}>Mark as read</label><label><input data-source-save="${s.id}" type="checkbox" ${p.saved ? "checked" : ""}>Save to reading list</label></div><label>Your research notes<textarea data-source-note="${s.id}" rows="4" maxlength="15000">${esc(p.notes)}</textarea></label><p class="caption">Metadata and linked source checked ${esc(s.verifiedAt)}. Summaries are research notes. Video entries disclose playback limits in their caveats. Consult the original for the full work.</p>${button("Discuss this source with AI", "discuss-source", `data-id="${s.id}"`, "soft", "spark")}`,
  );
}
function taskEditor(id, detail = "") {
  const t = state.w.tasks.find((t) => t.id === id);
  showModal(
    t ? "Edit sprint task" : "Add a sprint task",
    `<form class="form-grid"><label>Task title<input name="title" required maxlength="500" value="${esc(t?.title || "")}"></label><label>Protocol and acceptance criteria<textarea name="detail" rows="4" required maxlength="15000">${esc(t?.detail || detail)}</textarea></label><div class="form-two"><label>Due date<input type="date" name="due" required value="${t?.due || "2026-11-07"}"></label><label>Estimated hours<input name="hours" type="number" min="0" max="200" step="0.25" required value="${t?.hours || 2}"></label></div><div class="form-two"><label>Priority<select name="priority">${options({ high: "High", medium: "Medium", low: "Low" }, t?.priority || "high")}</select></label><label>Status<select name="status">${options({ todo: "To do", doing: "In progress", done: "Complete", blocked: "Blocked" }, t?.status || "todo")}</select></label></div><label>Dependencies<select name="depends" multiple size="4">${state.w.tasks
      .filter((x) => x.id !== id)
      .map(
        (x) =>
          `<option value="${x.id}" ${t?.depends.includes(x.id) ? "selected" : ""}>${esc(x.title)}</option>`,
      )
      .join(
        "",
      )}</select><small>Ctrl / Command selects multiple tasks.</small></label><button class="btn primary" type="submit">Save task ${icon("tick", 15)}</button></form>`,
    (data) => {
      const next = {
        id: t?.id || uid(),
        title: String(data.get("title")),
        detail: String(data.get("detail")),
        due: String(data.get("due")),
        hours: Number(data.get("hours")),
        priority: String(data.get("priority")),
        status: String(data.get("status")),
        depends: data.getAll("depends"),
        sourceIds: t?.sourceIds || [],
      };
      mutate((w) => {
        if (t) w.tasks = w.tasks.map((x) => (x.id === id ? next : x));
        else w.tasks.push(next);
      });
      modalClose();
      toast("Sprint task saved.");
    },
  );
}
function experimentEditor(id) {
  const e = state.w.experiments.find((x) => x.id === id);
  const fields = [
    ["hypothesis", "Hypothesis"],
    ["method", "Protocol / method"],
    ["metric", "Primary metric"],
    ["result", "Measured result"],
    ["limitation", "Limitations and failure cases"],
    ["command", "Command or notebook entry point"],
    ["evidence", "Evidence artifact or provenance"],
  ];
  showModal(
    e ? "Experiment record" : "Design an experiment",
    `<form class="form-grid"><label>Experiment title<input name="title" value="${esc(e?.title || "")}" maxlength="500" required></label><label>Status<select name="status">${options({ planned: "Planned", running: "Running", complete: "Complete", blocked: "Blocked" }, e?.status || "planned")}</select></label>${fields.map(([id, label]) => `<label>${label}<textarea name="${id}" rows="${id === "method" ? 4 : 2}" maxlength="${id === "metric" ? 500 : 15000}" ${id === "hypothesis" || id === "method" ? "required" : ""}>${esc(e?.[id] || "")}</textarea></label>`).join("")}<button class="btn primary" type="submit">Save experiment ${icon("tick", 15)}</button></form>`,
    (data) => {
      const next = {
        id: e?.id || uid(),
        title: String(data.get("title")),
        status: String(data.get("status")),
        created: e?.created || new Date().toISOString(),
        ...Object.fromEntries(fields.map(([id]) => [id, String(data.get(id))])),
      };
      mutate((w) => {
        if (e)
          w.experiments = w.experiments.map((x) => (x.id === id ? next : x));
        else w.experiments.push(next);
      });
      modalClose();
      toast("Experiment record saved.");
    },
  );
}
function addSource() {
  showModal(
    "Add a research source",
    `<form class="form-grid"><label>Title<input name="title" maxlength="500" required></label><label>Original source URL<input name="url" type="url" pattern="https://.*" required maxlength="2000" placeholder="https://…"></label><div class="form-two"><label>Type<select name="type">${options(Object.fromEntries(["paper", "article", "video", "talk", "news", "documentation"].map((x) => [x, x])), "paper")}</select></label><label>Year<input name="year" type="number" min="1900" max="2200" value="2026" required></label></div><label>Authors or publisher<input name="authors" maxlength="1500"></label><label>What does it say?<textarea name="summary" maxlength="15000" rows="3" required></textarea></label><label>How can we use it this week?<textarea name="action" maxlength="15000" rows="3" required></textarea></label><button class="btn primary" type="submit">Add source</button></form>`,
    (data) => {
      const entry = {
        id: uid(),
        title: String(data.get("title")),
        url: String(data.get("url")),
        type: String(data.get("type")),
        year: Number(data.get("year")),
        authors: String(data.get("authors") || "Not recorded"),
        summary: String(data.get("summary")),
        action: String(data.get("action")),
        category: "Added by researcher",
        priority: "medium",
        caveat:
          "User-added source. Verify the original before citing its claims.",
        tags: ["To review"],
        verifiedAt: new Date().toISOString().slice(0, 10),
      };
      mutate((w) => w.customSources.push(entry));
      modalClose();
      toast("Source added for review.");
    },
  );
}
function discover() {
  state.discovery = [];
  showModal(
    "Discover useful research",
    `<p>Search live scholarly metadata through Crossref. Inspect new sources before relying on their claims. For videos, arXiv and news, use the focused searches below.</p><form id="discovery-form" class="toolbar"><input name="query" aria-label="Research search query" maxlength="200" minlength="2" required value="interactive patch filtering automated program repair"><button class="btn primary" type="submit">Search ${icon("search", 15)}</button></form><div class="external-searches">${link("https://arxiv.org/search/?query=automated+program+repair&searchtype=all", "Search arXiv")}${link("https://www.youtube.com/results?search_query=software+engineering+agents+research+talk", "Find research talks")}${link("https://news.google.com/search?q=Gemma%204%20software%20engineering", "Find news")}</div><div id="discovery-results"></div>`,
    async (data, form) => {
      const box = document.querySelector("#discovery-results"),
        btn = form.querySelector("button");
      btn.disabled = true;
      box.innerHTML = "<p>Searching scholarly records…</p>";
      try {
        const d = await api(
          "/api/discover?q=" + encodeURIComponent(String(data.get("query"))),
        );
        state.discovery = d.results;
        box.innerHTML = d.results.length
          ? d.results
              .map(
                (r, i) =>
                  `<div class="discovery-row"><h3>${link(r.url, r.title)}</h3><p class="authors">${esc(r.authors)} · ${r.year || "Date unavailable"}</p><p>${esc(r.summary)}</p>${button("Add for review", "add-discovery", `data-id="${i}" ${!r.year ? "disabled" : ""}`, "", "plus")}</div>`,
              )
              .join("")
          : empty(
              "No results returned",
              "Try a narrower phrase or one of the external searches.",
            );
      } catch (e) {
        box.innerHTML = `<div class="inline-error">${esc(e.message)}</div>`;
      } finally {
        btn.disabled = false;
      }
    },
  );
}
async function upload(file) {
  if (!file || !file.size || file.size > 5000000)
    throw new Error("Choose a nonempty file under 5 MB.");
  const form = new FormData();
  form.append("file", file);
  return api("/api/files", { method: "POST", body: form });
}
async function importRun(file) {
  if (!file) return;
  state.importing = true;
  render();
  try {
    if (file.size > 5000000) throw new Error("Choose a CSV under 5 MB.");
    const run = analyzeCsv(await file.text(), file.name);
    const d = await upload(file);
    run.fileId = d.id;
    mutate((w) => w.runs.push(run), false);
    state.run = run.id;
    state.expTab = "results";
    toast("Run analyzed and raw CSV archived.");
  } catch (e) {
    toast(e.message);
  } finally {
    state.importing = false;
    render();
  }
}
async function connectProvider() {
  if (!state.apiKey) {
    toast("Enter an API key for the selected provider.");
    return;
  }
  state.providerBusy = true;
  render();
  try {
    const d = await api("/api/ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action: "models",
        provider: state.w.settings.provider,
        apiKey: state.apiKey,
      }),
    });
    state.models = d.models;
    state.connected = true;
    toast("Provider connected. Choose a text-generation model.");
  } catch (e) {
    state.connected = false;
    toast(e.message);
  } finally {
    state.providerBusy = false;
    render();
  }
}
document.addEventListener("click", async (event) => {
  const target = event.target.closest("[data-view],[data-action]");
  if (!target) return;
  if (target.dataset.view) {
    navigate(target.dataset.view);
    return;
  }
  const { action, id } = target.dataset;
  if (action === "close-modal") {
    modalClose?.();
    return;
  }
  if (action.startsWith("nav-")) {
    navigate(action.slice(4));
    return;
  }
  const actions = {
    menu: () => {
      state.mobile = true;
      render();
    },
    "close-nav": () => {
      state.mobile = false;
      render();
    },
    backup: () =>
      download(
        "PatchQuestions-workspace-backup.json",
        JSON.stringify(state.w, null, 2),
      ),
    reload: () => location.reload(),
    "retry-save": () => {
      state.saveError = "";
      void flush();
    },
    plan: () => ask(prompts.next),
    "critique-results": () =>
      ask(
        "Critique our baseline and imported results. Identify the strongest and weakest evidence, and propose the most useful four-hour follow-up.",
      ),
    "ask-task": () => {
      const t = state.w.tasks.find((x) => x.id === id);
      ask(
        "Help execute this task: " +
          t.title +
          "\n" +
          t.detail +
          "\nProvide a protocol, acceptance criteria and a stopping rule within " +
          t.hours +
          " hours.",
      );
    },
    "regex-experiment": () => experimentEditor("regex"),
    source: () => openSource(id),
    bookmark: () =>
      mutate((w) => {
        const p = w.sourceState[id] || { read: false, saved: false, notes: "" };
        w.sourceState[id] = { ...p, saved: !p.saved };
      }),
    "library-type": () => {
      state.libraryType = id;
      render();
    },
    "source-citation": () => {
      const s = allSources().find((x) => x.id === id);
      download(s.id + ".bib", citation(s), "application/x-bibtex");
    },
    citations: () =>
      download(
        "PatchQuestions-citations.bib",
        allSources()
          .filter(
            (s) => state.libraryType === "all" || s.type === state.libraryType,
          )
          .map(citation)
          .join("\n\n"),
        "application/x-bibtex",
      ),
    "discuss-source": () => {
      const s = allSources().find((x) => x.id === id);
      if (!state.sourceSelection.includes(id)) state.sourceSelection.push(id);
      modalClose?.();
      ask(
        "Compare our contribution to [" +
          s.id +
          "] " +
          s.title +
          ". Identify overlap, defensible differences and one feasible next experiment.",
      );
    },
    "add-source": addSource,
    discover,
    "add-discovery": () => {
      const r = state.discovery[Number(id)];
      if (allSources().some((s) => s.url === r.url)) {
        toast("This source is already in your library.");
        return;
      }
      mutate((w) =>
        w.customSources.push({
          id: "crossref-" + uid(),
          title: r.title.slice(0, 500),
          authors: r.authors.slice(0, 1500) || "Authors not recorded",
          year: r.year,
          type: "paper",
          category: "New discovery",
          priority: "medium",
          url: r.url,
          summary: r.summary,
          action:
            "Read the original and record its practical relevance to our protocol.",
          caveat:
            "Imported Crossref metadata. Claims, full text and relevance still need review.",
          tags: ["To review"],
          verifiedAt: new Date().toISOString().slice(0, 10),
        }),
      );
      target.disabled = true;
      toast("Source added with a review-needed caveat.");
    },
    "experiment-tab": () => {
      state.expTab = id;
      render();
    },
    "new-experiment": () => experimentEditor(),
    experiment: () => experimentEditor(id),
    "import-run": () => document.querySelector("#score-upload").click(),
    probe: () => {
      if (state.asked.length < 3 && !state.asked.includes(Number(id))) {
        state.asked.push(Number(id));
        render();
      }
    },
    "sandbox-reset": () => {
      state.asked = [];
      render();
    },
    prompt: () => {
      state.prompt = prompts[id];
      render();
      document.querySelector("#ai-prompt")?.focus();
    },
    "send-ai": sendAI,
    "cancel-ai": () => aiController?.abort(),
    "priority-sources": () => {
      state.sourceSelection = allSources()
        .filter((s) => s.priority === "high")
        .slice(0, 12)
        .map((s) => s.id);
      render();
    },
    "toggle-context": () => {
      state.showContext = !state.showContext;
      state.prompt =
        document.querySelector("#ai-prompt")?.value || state.prompt;
      render();
    },
    "advice-task": () => {
      const m = state.w.messages.find((x) => x.id === id);
      taskEditor(null, m.text.slice(0, 15000));
    },
    "save-advice": () => {
      const m = state.w.messages.find((x) => x.id === id);
      mutate((w) =>
        w.notes.push({
          id: uid(),
          title: "AI research note · " + date(m.created),
          text: m.text,
          created: new Date().toISOString(),
        }),
      );
      toast("Advice saved to research notes.");
    },
    "connect-provider": connectProvider,
    "clear-key": () => {
      state.apiKey = "";
      state.connected = false;
      state.models = [];
      render();
      toast("API key cleared from this page.");
    },
    "new-task": () => taskEditor(),
    "edit-task": () => taskEditor(id),
    "toggle-task": () =>
      mutate((w) => {
        const t = w.tasks.find((x) => x.id === id);
        t.status = t.status === "done" ? "todo" : "done";
      }),
    "review-sprint": () =>
      ask(
        "Review the sprint against the actual time remaining. Identify the critical path, which tasks to cut, the minimum defensible evidence package and a submission buffer.",
      ),
    "paper-mode": () => {
      state.manuscriptMode = id;
      render();
    },
    "paper-review": () => {
      state.includePaper = true;
      ask(
        "Review the manuscript against novelty, quality, relevance, verifiability and clarity. Identify unsupported claims and specific evidence needed.",
      );
    },
    "export-paper": () =>
      download(
        "PatchQuestions-manuscript.md",
        state.w.manuscript,
        "text/markdown",
      ),
    "upload-evidence": () => document.querySelector("#evidence-upload").click(),
    restore: () => document.querySelector("#backup-upload").click(),
  };
  try {
    await actions[action]?.();
  } catch (error) {
    toast(error.message || "This action could not be completed.");
  }
});
document.addEventListener("input", (event) => {
  const t = event.target;
  if (t.id === "library-query") {
    const value = t.value,
      start = t.selectionStart;
    state.libraryQuery = value;
    render();
    const input = document.querySelector("#library-query");
    input.focus();
    input.setSelectionRange(start, start);
  }
  if (t.id === "ai-prompt") state.prompt = t.value;
  if (t.id === "api-key") {
    state.apiKey = t.value;
    state.connected = false;
  }
  if (t.id === "model") mutate((w) => (w.settings.model = t.value), false);
  if (t.id === "max-tokens") {
    mutate((w) => (w.settings.maxTokens = Number(t.value)), false);
    document.querySelector("#token-value").textContent = Number(
      t.value,
    ).toLocaleString();
  }
  if (t.id === "manuscript") {
    mutate((w) => (w.manuscript = t.value), false);
    const words = t.value.trim().split(/\s+/).filter(Boolean).length;
    document.querySelector("#word-count").innerHTML = badge(
      words.toLocaleString() + " / 3,000 words",
      words > 3000 ? "warm" : "green",
    );
  }
  if (t.dataset.sourceNote) {
    const id = t.dataset.sourceNote;
    mutate((w) => {
      w.sourceState[id] ||= { read: false, saved: false, notes: "" };
      w.sourceState[id].notes = t.value;
    }, false);
  }
});
document.addEventListener("change", async (event) => {
  const t = event.target;
  try {
    if (t.id === "library-filter") {
      state.libraryFilter = t.value;
      render();
    }
    if (t.id === "run-choice") {
      state.run = t.value;
      render();
    }
    if (t.id === "budget") {
      state.budget = t.value;
      render();
    }
    if (t.id === "sandbox-family") {
      state.family = t.value;
      state.target = 0;
      state.asked = [];
      render();
    }
    if (t.id === "sandbox-target") {
      state.target = Number(t.value);
      state.asked = [];
      render();
    }
    if (t.id === "include-paper") {
      state.includePaper = t.checked;
      render();
    }
    if (t.dataset.selectSource) {
      const id = t.dataset.selectSource;
      state.sourceSelection = t.checked
        ? [...state.sourceSelection, id]
        : state.sourceSelection.filter((x) => x !== id);
      render();
    }
    if (t.dataset.sourceRead || t.dataset.sourceSave) {
      const id = t.dataset.sourceRead || t.dataset.sourceSave;
      mutate((w) => {
        w.sourceState[id] ||= { read: false, saved: false, notes: "" };
        w.sourceState[id][t.dataset.sourceRead ? "read" : "saved"] = t.checked;
      }, false);
    }
    if (t.id === "provider") {
      state.apiKey = "";
      state.models = [];
      state.connected = false;
      mutate((w) => {
        w.settings.provider = t.value;
        w.settings.model = "";
      });
    }
    if (t.dataset.taskStatus) {
      mutate(
        (w) =>
          (w.tasks.find((x) => x.id === t.dataset.taskStatus).status = t.value),
      );
    }
    if (t.id === "task-filter") {
      state.taskFilter = t.value;
      render();
    }
    if (t.dataset.gate) {
      mutate((w) => (w.gates[t.dataset.gate] = t.checked));
    }
    if (t.id === "score-upload") await importRun(t.files?.[0]);
    if (t.id === "evidence-upload" && t.files?.[0]) {
      toast("Uploading evidence…");
      await upload(t.files[0]);
      await refreshFiles();
      toast("Project file uploaded.");
      t.value = "";
    }
    if (t.id === "backup-upload" && t.files?.[0]) {
      const file = t.files[0];
      if (file.size > 1000000) throw new Error("Backup must be under 1 MB.");
      const candidate = JSON.parse(await file.text());
      if (
        !candidate ||
        !Array.isArray(candidate.tasks) ||
        !Array.isArray(candidate.experiments) ||
        !candidate.settings ||
        !Array.isArray(candidate.customSources)
      )
        throw new Error("This is not a PatchQuestions workspace backup.");
      await api("/api/workspace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(candidate),
      });
      showModal(
        "Review workspace restoration",
        `<p>This backup contains ${candidate.tasks.length} tasks, ${candidate.experiments.length} experiments and ${candidate.messages?.length || 0} messages. Restoring replaces the current workspace content. Export your current backup first if needed.</p><form><button class="btn primary" type="submit">Restore this backup</button></form>`,
        () => {
          mutate((w) => {
            Object.keys(w).forEach((k) => delete w[k]);
            Object.assign(w, candidate);
          });
          modalClose();
          toast("Backup restored. Saving to the local workspace.");
        },
      );
    }
  } catch (error) {
    toast(error.message);
  }
});
document.addEventListener("submit", (event) => {
  if (event.target.id === "note-form") {
    event.preventDefault();
    const data = new FormData(event.target);
    mutate((w) =>
      w.notes.push({
        id: uid(),
        title: String(data.get("title")),
        text: String(data.get("text")),
        created: new Date().toISOString(),
      }),
    );
    toast("Research note saved.");
  }
});
document.addEventListener("keydown", (event) => {
  if (
    event.target.id === "ai-prompt" &&
    (event.ctrlKey || event.metaKey) &&
    event.key === "Enter"
  ) {
    event.preventDefault();
    void sendAI();
  }
});
window.addEventListener("beforeunload", (event) => {
  if (state.w && state.w !== state.saved) {
    event.preventDefault();
    event.returnValue = "";
  }
});
window.addEventListener("hashchange", () => navigate(location.hash.slice(1)));
async function start() {
  try {
    const [workspace, baseline, sources] = await Promise.all([
      api("/api/workspace"),
      api("/baseline.json"),
      api("/project/research-library.json"),
    ]);
    state.w = workspace.workspace;
    state.saved = state.w;
    state.revision = workspace.revision;
    state.baseline = baseline;
    state.sources = sources;
    state.sourceSelection = sources
      .filter((s) => s.priority === "high")
      .slice(0, 12)
      .map((s) => s.id);
    render();
  } catch (error) {
    app.innerHTML = `<div class="load-error">${icon("alert", 28)}<h1>Let’s reconnect your workspace.</h1><p>${esc(error.message)}</p><button class="btn primary" onclick="location.reload()">Retry connection</button><p class="caption">Your local data remains in the data folder beside the app.</p></div>`;
  }
}
void start();
