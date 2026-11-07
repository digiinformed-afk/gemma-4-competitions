# Combined Gemma program: paper first, agent second

**Execution update, 7 November 2026.** The external review follow-up has been completed in this chat. The revised resource paper, fresh CPython 3.12.14 reproduction, transcript-cost analysis, tested strict supervisor and successfully executed notebook are recorded in the [paper revision status](<../Google - The Gemma 4 Developer Agent Paper Track/PatchQuestions_Local/paper-revision/STATUS.md>). The completed paper uses CPU evidence; a new-family experiment is deferred and the model pilot remains optional pending demonstrated access. The new executable supervisor supersedes the older proposed pilot sample and scoring details. The [main-track status](<../Google - The Gemma 4 Developer Agent Competition/gemma-agent-lab/MAIN-TRACK-STATUS.md>) records separately completed agent packaging/validation. The earlier inventory and dates below remain planning history where superseded by those execution records. No account or submission action has occurred in this revision.

Reviewed **7 November 2026**, Asia/Karachi. User decision: coordinate both competitions through one program while keeping the existing folders. This is the current scheduling authority when older track blueprints differ. All proposed experiments below remain unexecuted unless a verification result is explicitly identified.

## Decision and research direction

Use **PatchQuestions as the paper submission**, positioned as an auditable resource for studying behavioral ambiguity and question selection. Add one small Gemma evaluation if access and time permit. After submission, adapt the useful evidence-selection ideas to the autonomous repair agent and measure them in the official harness.

The shared question is: **How should a small coding agent spend a limited budget on evidence before committing to a patch?** The two evaluations answer different parts:

| Paper evaluation | Main-track evaluation |
|---|---|
| Controlled API configurations, visible candidate behavior, a supervisor-owned trusted oracle, up to three labels | Real repository issues, one permitted Gemma base per submission, available tools and executable evidence |
| Full agreement on a finite held-out suite; questions, errors and cost | Resolved tasks / all scheduled tasks; total wall time and failed/empty submissions |
| Isolates selection quality and limitations of the probe pool | Tests whether a bounded evidence policy improves final repairs within the global budget |

The shared component is the evidence-selection policy and its logging. A disagreement between patches does not identify the correct behavior. The main agent must obtain its evidence from issue requirements, existing tests/contracts or justified relations. It cannot ask the hidden reference solution or assume a human oracle exists. If evidence remains inconclusive, preserve the best supported candidate and finalize within budget.

Allocate **90% of work time to paper completion and 10% to shared access/setup until the paper is submitted**. Assume roughly 4–6 focused hours a day; this is a planning assumption, not a known availability commitment. If time is tighter, drop optional experiments in the order stated below. Freeze new research scope on **10 November, 18:00 PKT**.

## Verified deadlines and deliverables

| Milestone | Official UTC | Pakistan time | Internal target |
|---|---|---|---|
| Paper final submission | 12 Nov 2026, 23:59 | **13 Nov, 04:59** | First complete submission **11 Nov, 20:00 PKT**; final audit **12 Nov, 18:00 PKT** |
| Main entry / team merger | 25 Nov 2026, 23:59 | **26 Nov, 04:59** | Verify entry/access now; finalize team before **24 Nov evening** |
| Main final submission | 2 Dec 2026, 23:59 | **3 Dec, 04:59** | Stable candidate by **29 Nov**; final selections by **1 Dec evening** |

The paper requires a submitted Kaggle Writeup, original unpublished work, and at most 3,000 words. Include title/subtitle, abstract, introduction, methods/experiments and related work. A public notebook or accessible PDF link is optional. Saved drafts do not qualify. Its five equally weighted criteria are Novelty, Quality, Relevance, Verifiability and Clarity. Joining the main track is not required. The resource award is the closest fit; this is a positioning recommendation, not a prediction of acceptance or an award. [Official paper overview](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview)

The main deliverable is `submission.zip` with root `agent.yaml`; scoring uses validated repairs under one 12-hour run including setup. Current allowed bases are 31B, 12B, E4B and E2B QAT W4A16 CT variants; every agent in an archive must use the same base. L4×4 sessions are offline. The E2B/E4B bonus requires an eligible final selection. These live details supersede older indexed 31B-only descriptions. [Official main overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview)

Main rules allow one daily submission and two final selections; paper rules allow five daily submissions and two final selections. Each track has its own entry and submission. Check account eligibility, authorship and rights before publishing; publish competition code through the associated Kaggle forum/notebook routes. [Main rules](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules), [Paper rules](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules)

## What the workspace actually contains

The paper folder contains the draft, executable standard-library benchmark, 18,000 score rows, summaries, a notebook, frozen behavior matrices and an interactive replay interface. The main folder contains a research application, draft prompts, evaluation-accounting tools and a proposed compute plan. It does not yet contain evidence of an official evaluated agent, trained adapter or scored submission.

The 7 November audit independently checked:

- The 18,000 rows cover 750 target/split episodes × six policies × four budgets, without duplicate result keys. Stored family-macro summaries agree with the CSV.
- All six Python modules embedded in the notebook match their current standalone files. Existing ZIP members match the working copies.
- An isolated **Python 3.15.2** rerun completed the benchmark, analysis, regex intervention, eight depth-two solver checks, blind protocol check and 750 named/masked entropy consistency checks.
- The deterministic entropy/tree aggregates match the stored reference. At budget three, the random baseline differs by approximately −0.197 percentage points and random-informative by +0.00182 points. This is a cross-runtime check, **not** a reproduction under the claimed CPython 3.12.14 runtime.
- `cognitive_probe.py`, its study note and the expanded research notes/library are absent from the existing research ZIP. The notebook does not yet include the cognitive pilot. Package them if the revised paper relies on them.
- The current manuscript has about **1,806 whitespace-delimited words**, leaving room for a focused update; check Kaggle's final rendering/count separately.

Evidence: [audit JSON](verification/2026-11-07-python315/workspace-audit.json). Original artifacts were hashed before and after the isolated rerun and remained unchanged. Python 3.12.14 was not installed on this host at review time. Original 3.12 measurements and the pre-existing 3.13 record remain historical artifacts until independently reproduced in the corresponding runtime.

## The paper’s strongest defensible story

The stored budget-three results are **76.32% random-informative, 85.27% entropy and 85.48% frugal tree**. The tree gain over entropy is only **0.21 percentage points**. Mean questions fall from 2.266 for ordinary lookahead to 1.864 for frugal lookahead, but entropy already uses 1.882. The 17.7% saving is relative to ordinary lookahead, not entropy.

The more useful diagnostic is the regex pool: all existing queries still give a 30% reference score, while the exploratory compound-probe intervention reaches 86.25% at three questions on both the original scoring suite and its separate transfer suite. This is one post-hoc family intervention, not a general improvement estimate or a human-time result.

Lead with three contributions that can be audited: a finite behavioral-ambiguity resource; exact policy comparisons and a limited-search reference; and evidence that a poor probe vocabulary can dominate policy choice. Add a narrowly described Gemma pilot to establish model-facing usability. Do not claim a new general clarification algorithm, a cognitive-core architecture, 750 independent real bugs, or a leaderboard gain. [Prior-art review and reading priorities](RESEARCH-REVIEW.md)

## Paper sprint: 7–12 November

| PKT date | Priority work | Concrete exit condition |
|---|---|---|
| **7 Nov** | Freeze current artifacts and scope; incorporate the closest prior-art comparison; check paper entry and model access | Checksums, unchanged reference results, one-page contribution statement, and a selected pilot protocol. Artifact audit completed in this review; account/model access still unverified. |
| **8 Nov** | Reproduce in 3.12.14 if available; run Gemma plumbing on development episodes; freeze prompts/settings | Valid evaluator/agent separation, actions parse correctly, logs contain model revision and runtime. If access is still unavailable by **18:00**, take the CPU-only fallback. |
| **9 Nov** | Run the fixed Gemma pilot and matched classical baselines | Complete scheduled denominator, raw transcripts, failures retained, per-family outcomes. No tuning on pilot results. |
| **10 Nov** | Analyze; add only a predeclared presentation-sensitivity repeat if the pilot is complete | Paired outcomes and failure taxonomy; scope frozen at **18:00**. No new model, training or repository campaign after cutoff. |
| **11 Nov** | Revise manuscript, tables and related work; run the notebook; rebuild release package | One consistent paper/notebook/results version; all main claims trace to artifacts. First complete Kaggle submission targeted by **20:00**. |
| **12 Nov** | Check rendered Writeup, notebook access, authors, citations and submission state | Final audit by **18:00**; leave the remaining buffer for corrections. Confirm Submitted status, not merely Saved/Draft. |

The user completes account sign-in and rule acceptance where required; this planning review did not access a signed-in Kaggle account. Actual publishing/submission is a later release action, not a task already completed here.

**Core experiment:** run the existing named-versus-masked frozen-matrix Gemma pilot, with random-informative and entropy on the identical episodes. It is smaller and safer than building a full patch-generation pipeline this week. It measures evidence selection, not code repair. See the [locked experiment protocol](EXPERIMENT-PROTOCOL.md).

**CPU-only fallback:** submit the resource study with the improved related-work comparison, explicit version sensitivity, full per-family results and careful probe-design limitations. Gemma evaluation is valuable for relevance but is not listed as a universal submission requirement on the paper overview. State clearly that model and real-repository validation remain future work.

**Drop first:** a second model, a large family expansion, real-repository candidate generation, LoRA, reinforcement learning, extra agent roles, or dashboard redesign. Drop presentation repeats next if needed. Retain reproduction, correct baselines, limitations and a submitted Writeup.

## Manuscript and release gates

Aim for 2,500–2,850 words in the final rendered report to preserve margin. A suggested allocation is abstract 150; introduction/contributions 300; resource/protocol 500; methods 300; results and pilot 650; related work 350; limitations/reproduction 300. Tables and references may affect Kaggle's count, so use the platform's final interpretation.

| Judging dimension | Required improvement |
|---|---|
| Novelty | Explain the narrow addition relative to InPaFer, LEARN2FIX and xTestCluster. Avoid claiming interactive filtering or behavioral grouping is new. |
| Quality | Separate fixed-suite evidence from transfer. Label regex redesign exploratory and the small Gemma sample a feasibility study. |
| Relevance | Explain the maintainer-assisted use case and the exact difference from the offline competition. Include model logs if the pilot runs. |
| Verifiability | One command/notebook sequence, versioned matrices, checksums, all scheduled outcomes, prompts and raw transcripts. |
| Clarity | Distinguish selection policy, probe vocabulary and oracle. Use one main result table and one diagnostic table. |

Before release, make the manuscript, notebook, ZIP and README agree on runtime, policy names, modules and results. Include the new pilot runner/data only if used. Declare an appropriate license after rights/attribution review. The synthetic benchmark's hidden grading matrices can be public for reproducibility, but keep them outside evaluated agent access. Do not bundle competition datasets, reference fixes, credentials or local workspace backups into a public artifact. Check notebook and report links from a signed-out view.

## Main-track roadmap after paper submission

| PKT dates | Work | Promotion gate |
|---|---|---|
| **13–15 Nov** | Obtain current official harness/sample, record versions and hash tasks; run sample unchanged on 3–5 representative development issues | Correct model load, patch capture and grading. Validate buggy baseline fails and gold fix passes in evaluator-only sandboxes. |
| **16–18 Nov** | Establish a simple lexical repair agent; freeze repository-disjoint development/confirmation folds | Reproducible complete logs, all scheduled tasks counted, setup and tool errors separated from repair failures. |
| **19–21 Nov** | One bounded evidence-selection ablation: use a distinguishing check only when multiple supported candidates remain | Better paired resolved outcomes or useful efficiency at equal total budget; no correctness loss hidden by reporting only started tasks. |
| **22–24 Nov** | Compare the strongest scaffold using 31B and a separate E4B run if quota permits; test bounded graph retrieval only for observed localization failures | Stable quality/runtime tradeoff across repositories; no mixing base models in one archive. Confirm entry/team status before cutoff. |
| **25–27 Nov** | Optional small adapter pilot only after baseline and exact loader work | Exported adapter reloads in official offline harness and improves untouched confirmation tasks. Otherwise retain no-adapter agent. |
| **28–29 Nov** | Full-budget rehearsal and artifact validation | One valid archive finishes within measured global budget, with finalization reserve and complete accounting. |
| **30 Nov–1 Dec** | Use limited daily submission opportunities; inspect failures and choose final artifacts | Preserve the strongest validated submission. Select E4B/E2B only if supported by results and intended bonus strategy. |
| **2 Dec** | Recovery buffer and submission-state checks | Correct final selections and hashes well before **3 Dec, 04:59 PKT**. |

The organizer's starter input documentation lists 129 public tasks in four repositories; the hidden tasks come from different repositories. Public task validity has also been discussed by Kaggle staff. Therefore check the latest harness and gold-patch controls before interpreting local agent scores. A community replacement grader is not automatically the official evaluator. [Official starter inputs](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent/input), [discussion containing staff response](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747248)

For every main-track comparison: hide `patch` and `test_patch` during generation; reset task memory; freeze tasks/model/prompt/harness hashes; grade in fresh sandboxes; count timeouts, invalid patches, setup failures and unstarted tasks. Compare paired wins/losses by repository. With only four public repositories, small effects and uncertainty estimates are fragile. Do not tune exclusively to public leaderboard feedback.

Use the total runtime equation `(720 minutes − measured setup − reserve) / scheduled tasks` as a planning aid. For 120 tasks, 45 minutes setup and 72 minutes reserve, the illustrative allowance is about 5.0 minutes per task. Measure actual overhead, inference, tools and finalization in the current harness; do not invent configuration keys or assume uncharged work.

## Compute and dependencies

The existing plan records **200 user-reported Colab units plus Kaggle GPUs**. Current balance, available hardware and account quota were not verified. Units are not GPU-hours and consumption varies by runtime. Do not buy extra compute to preserve this schedule without a separate decision.

Keep the existing allocation ceilings: 20 units profiling/paper feasibility; 80 conditional SFT; 40 comparisons; 20 export/reload; **40 held in reserve**. Charge any paper pilot to the first 20 units rather than adding a new allowance. Freeze/release the remaining allocations only after measured compatibility and benefit; they are ceilings, not spending targets. Use CPU for benchmark analysis. L4×4 is 96 GB across four devices, not one 96 GB GPU. Verify permitted use before placing paper-only workloads on competition-restricted accelerators.

The immediate dependency is access to one reproducible Gemma inference environment. Use a suitable Colab runtime for the paper pilot if model terms and memory allow. Preserve the exact checkpoint and serving settings. Main-track evaluation must subsequently use the official permitted artifact and offline harness. Prefer a completed CPU resource paper over losing the deadline to model setup.

## Risks and decisions

| Risk | Response / stop rule |
|---|---|
| Novelty overlaps established interactive repair work | Narrow the claim and add direct comparison; do not try to invent a new theme during the final days. |
| Gemma unavailable or matrix too large for context | Diagnose on development episodes; if unresolved by 8 Nov 18:00, use fallback. Report truncation as a feasibility limitation. |
| Wrong trusted labels or leaked target | Supervisor-only files/process; fail the run on leakage and restart before analyzing results. |
| Fewer labels presented as less human effort | Log prompt/answer size and wall time; make human-time claims only with real timed evidence. |
| Historical/runtime-dependent results diverge | Keep each runtime's results separate; use frozen reference matrices for model-policy comparisons. |
| Main harness changes or environment failures | Version/hash the harness and rerun gold controls; do not call packaging failures model regressions. |
| Scope consumes submission buffer | Stop new experiments on 10 Nov; submit the strongest complete evidence. |

The next work item is **freeze the paper contribution and pilot specification, then establish Gemma access on development episodes**. Main-agent training and broad scaffold changes remain behind the paper release.
