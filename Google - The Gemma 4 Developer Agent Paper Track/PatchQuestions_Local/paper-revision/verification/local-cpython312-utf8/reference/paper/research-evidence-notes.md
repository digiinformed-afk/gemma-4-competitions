# PatchQuestions research library verification

Verified on 6 November 2026. The companion JSON is a curated reading set, not an exhaustive literature search. It contains 30 entries. All summaries are short original paraphrases. Full text, figures and videos have not been copied into the app data.

## Evidence treatment

- The `verification` field states whether a primary abstract, author publication page, official technical article or official cross-link supplied the evidence.
- The `action` field is our suggested application to this project, not a finding claimed by the cited source.
- The `caveat` field records limitations, overlap and retrieval failures.
- Videos were verified using indexed metadata and links in the official SWE-agent documentation. They were not watched in full. The second video's display title is descriptive because exact YouTube metadata could not be retrieved. The MIT talk is an event page, with no verified recording link.
- Publication dates distinguish arXiv submission dates from later conference or journal publication where known. Month-only and year-only values must not be displayed as exact days.
- Numeric rankings and capability claims in model announcements are deliberately omitted from summaries. Those claims age quickly.

## Immediate research implications

1. Asking a developer distinguishing questions is established prior art. Compare directly with InPaFer, LEARN2FIX and the active-learning literature. The paper's potential contribution is the resource, controlled decomposition of probe generation and selection, exact expectations and any new evidence. It should not claim to have invented interactive filtering.
2. Dynamic behavioral grouping is established in xTestCluster. Explain whether our partitions are only an evaluation representation or a new intervention.
3. The existing synthetic configuration study does not establish performance with Gemma-generated edits or on real repository repairs. A small, fixed Gemma pilot is a high-priority way to strengthen competition relevance.
4. Separate question count from human effort. A compound regex query can encode several distinctions and request a long structured answer. Record input length, answer length and, if possible, timed annotation or a simpler answer format.
5. Keep query-generation inputs separate from hidden target/reference outputs. Record model, exact artifact revision, prompt, temperature, seed or seed limitations, runtime, API/model cost and invalid actions.
6. The original 750 target–split episodes reuse only eight API families. They do not become 750 independently sampled real bugs. Show per-family results and avoid overstating statistical independence.
7. The current setting always includes a correct candidate and a perfect oracle. Include a small robustness study with no correct candidate or abstention, or retain that limitation plainly.
8. The oracle-free generative research adviser is a planning tool. Any recommended experiment remains planned until execution logs and artifacts are attached. Provider-generated citations should match verified library records or be marked unverified.

## One-week task ordering

- First, freeze current results and protocol. Read the three closest prior-art papers and write a comparison table.
- Next, run a narrowly scoped Gemma candidate or probe-generation pilot using a frozen task subset and budget. Compare random informative and entropy under the same conditions.
- Then, add a blind transfer or robustness test and question-complexity accounting. Investigate failures rather than only increasing the number of episodes.
- Finish with a reproducibility run, artifact checks and a clear results table. Leave time to submit the actual Kaggle Writeup before the deadline.

## Competition requirements checked

The indexed official Kaggle overview confirms a 3,000-word maximum, original unpublished research, five equally weighted judging dimensions, and a final deadline of 12 November 2026 at 23:59 UTC (13 November, 04:59 in Pakistan). It also states that saved drafts are not considered. Model restrictions in the main prediction competition are a separate scope from APIs used to assist research planning. Graph and embedding data use is encouraged in the overview rather than mandatory for paper submissions.

Primary source: https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview

## Source reference map for parent citation verification

Closest prior art: `turn8view0`, `turn7view0`, `turn7view1`, `turn7view5`, `turn4search2`.

Modern agent baselines: `turn3academia0`, `turn3academia1`, `turn3academia2`, `turn3academia3`.

Benchmark quality: `turn5search2`, `turn5academia5`, `turn5academia6`.

Foundations: `turn4search0`, `turn6search17`, `turn8view1`, `turn8view2`.

Test generation: `turn7view2`, `turn7view3`, `turn7view4`.

Gemma and competition: `turn5academia4`, `turn8search0`, `turn8search1`, `turn9search1`.

Engineering guidance: `turn12view2`, `turn12view3`, `turn11search0`, `turn11search1`.

Videos/talks: `turn11youtube5`, `turn9search2`, `turn9search4`.

Root must reopen a page or perform its own confirming search before citing a subagent source in the final user answer. App entries use ordinary verified source URLs.
