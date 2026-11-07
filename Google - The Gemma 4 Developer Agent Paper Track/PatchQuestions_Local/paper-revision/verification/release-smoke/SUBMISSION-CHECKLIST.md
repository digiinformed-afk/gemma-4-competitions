# Submission preparation and source coverage

Checked 7 November 2026. This is a preparation record, not a personal eligibility determination or a submitted entry.

## Official source coverage

The live [paper overview](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/overview) was read through description, timeline, evaluation, submission requirements, awards and citation. The live [paper rules](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/rules) were read through competition terms, all nine competition-specific rules and all 18 foundational sections. The browser showed a signed-out session; no account or acceptance state was changed. Earlier external-review claims about a signed-in draft are attributed to that reviewer.

The overview specifies a title/subtitle, abstract, introduction, research description with methods/experiments, and related work/citations. The report limit is 3,000 words. It permits related unpublished resources and optional code/PDF links; main-track entry is optional. The five judging criteria are equally weighted. The deadline remains 12 November 2026, 23:59 UTC, or 13 November, 04:59 PKT. A saved draft requires a final submission action.

The rules specify a five-person team limit, five daily submissions and up to two final selections. They cover entry, eligibility, sharing, resource access, rights and winner documentation. They name Apache 2.0 as the winner license type. Those declarations require the author's own account and rights information; this local package makes no such declaration on their behalf.

## Prepared files

| Item | File / state |
|---|---|
| Writeup title | Manuscript first H1 |
| Subtitle | Manuscript bold line following title |
| Report | Manuscript from Abstract onward, including references |
| Required sections | Present in `paper/PatchQuestions_Writeup.md` |
| Local length check | `WORD-COUNT.json` includes title, subtitle, tables and references under multiple counting methods; all below 3,000 |
| Optional code notebook | `paper/PatchQuestions.ipynb`, freshly executed, 16 code cells, zero error outputs |
| Reproduction package | Source, reference data, evidence, scripts, tests and payload SHA256 manifest included |
| Research claims | CPU resource and exploratory intervention only; no model or repair results implied |
| Public links | Not created; a public notebook URL can be added to Project Links after upload |
| Author/account/rights declarations | To be completed by the author before publication |
| Platform draft/final status | Not changed or independently verified in this session |

## Final platform actions

1. Open the competition's New Writeup form under the author's account.
2. Copy the title, subtitle and report from the revised manuscript. Recheck the platform's rendered count; our counting methods are local checks because the overview gives no detailed tokenization rule.
3. If supplying code, upload/import the executed notebook and link its publicly accessible Kaggle page through Project Links. The ZIP is a supporting/recovery package, not a substitute for the Writeup.
4. Confirm attribution, unpublished status, eligibility and rights using the author's actual information. Confirm notebook and any linked assets are accessible as required.
5. Review the complete rendered entry and use Submit before the deadline. This revision work has not performed that action.

## Primary literature reading record

| Reference | Primary source and depth used |
|---|---|
| InPaFer | https://arxiv.org/html/2004.08746v2 — title/authors/version, Section 2 overview and interactive-stage passages |
| LEARN2FIX | https://arxiv.org/html/1912.07758v1 — title/authors/version, active-oracle-learning method and algorithm |
| xTestCluster | https://arxiv.org/html/2207.11082v2 — title/authors/version, approach and cross-execution/clustering definitions |
| Generalized binary search | https://nowak.ece.wisc.edu/GBS_arxiv_v4.pdf — title/author, abstract, problem setup and introductory algorithm |
| CodeMonkeys | https://arxiv.org/html/2501.14723v2 — title/authors/version, candidate-generation and selection-state-machine passages |
| Ambig-SWE | https://arxiv.org/abs/2502.13069v3 — title/authors/revision and abstract |
| Ask or Assume? | https://aclanthology.org/2026.findings-emnlp.15/ — official title/authors/venue/year and abstract |

This is targeted comparison, not an exhaustive novelty search or reproduction of those systems. Their published performance is not our evidence.

The paper revision does not depend on restricted main-track tasks, HARNESS_README, an official agent sample or model terms. Those remain separate main-track/access checks. The source package contains synthetic standard-library matrices, not competition task data or reference patches.
