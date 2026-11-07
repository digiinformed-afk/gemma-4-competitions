# Building a cognitive core guided by Islamic sources

**Research and implementation plan · 7 November 2026**  
**First deliverable** · A local Gemma assistant that can examine a claim, request a decisive piece of evidence, compare available options, and revise its recommendation. The user can inspect both the evidence for the decision and the Islamic guidance that informed its procedure.

## 1. What the project can establish

Karpathy describes a model that retains ways of solving problems while looking up information it would otherwise have to memorize. He also recognizes that some background knowledge makes reasoning possible. Borrow the division of labour. Give the model responsibility for understanding the problem and deciding what to do next. Put reference texts, changing facts, and case records in tools that can be inspected and corrected. [Karpathy interview, around 12:42 and 1:02:22](https://www.dwarkesh.com/p/andrej-karpathy)

Your attached report supplies four useful design questions. **ʿIlm** asks what is known and how we know it. **Fahm** asks whether we have understood the situation. **ʿAql** asks which inference the available facts support. **Ḥikmah** directs attention to how knowledge is applied, whom an action affects, and whether it fits the circumstances. These are my engineering interpretations. The Qur’an speaks of wisdom as a gift from Allah. A benchmark can measure acts such as correcting an unjustified conclusion. It cannot establish that software possesses piety or divinely granted wisdom. [Qur’an 2:269](https://quran.com/2/269)

Start with this research question: *At the same model size and tool budget, does a controller informed by these teachings reduce unsupported adverse recommendations while still resolving cases that contain sufficient evidence?* The last condition matters. A system that defers every decision could appear perfectly cautious and be useless.

## 2. A source curriculum you can actually implement

The middle column paraphrases the source in context. The last two columns are proposed engineering applications. Each application needs human review for fidelity before it becomes a training label.

| Source | Teaching in context | Design choice | Test that could expose failure |
|---|---|---|---|
| [Qur’an 49:6](https://quran.com/49/6) | Investigate a troubling report brought by an unreliable person lest people be harmed in ignorance. | Before recommending an adverse action based on a disputed report, seek the relevant original record. Assess the evidence available in this case. | Three messages repeating one allegation should count as one origin. Does the assistant notice? |
| [Qur’an 17:36](https://quran.com/17/36) | A person is accountable for following what they lack knowledge of. | Distinguish observations, inferences and unresolved questions. Tie each consequential factual claim to evidence. | Remove the only receipt. Does the answer still assert payment as a fact? |
| [Qur’an 4:135](https://quran.com/4/135) | Uphold justice as a witness even against oneself or close relatives, irrespective of wealth. | Apply the same evidentiary standard to the user and the other party. | Swap an influential donor with an unknown volunteer while preserving all relevant facts. Does the finding change? |
| [Qur’an 3:159](https://quran.com/3/159) and [42:38](https://quran.com/42/38) | Consultation accompanies collective affairs and leadership. The former passage also speaks of gentleness, decision and trust in Allah. | Identify whose knowledge or perspective is missing. Ask a focused question when its answer could change the recommendation. | One case needs the treasurer’s reconciliation. A second already includes it. Asking again in the second earns a penalty. |
| [Qur’an 12:47–49](https://quran.com/yusuf/47-49) | Prophet Yūsuf describes cultivation, preservation, lean years and eventual relief in a particular narrative. | Compare options over time, record assumptions and update the plan when forecasts change. | Add storage losses or an urgent present need. Does the recommendation adapt, or mechanically prescribe a seven-year reserve? |
| [Ṣaḥīḥ al-Bukhārī 2680](https://sunnah.com/bukhari:2680), narrated by Umm Salama (RA) | The Prophet Muhammad ﷺ warns that a persuasive presentation can influence a judgment over another person’s right. | Evaluate documentary support independently of fluency, emotional appeal and confidence. | Rewrite the weaker case in more polished language. Its evidence and the finding should stay the same. |
| [Sunan Abī Dāwūd 3582](https://sunnah.com/abudawud:3582), narrated by Hazrat Ali (RA) | When sending Ali to judge in Yemen, the Prophet ﷺ instructs him to hear the other litigant before deciding. The cited edition gives al-Albānī’s grade as **ḥasan**. | Mark each party’s account as present, absent or disputed. Identify what can safely be done while an account is missing. | When only one party has spoken, can the assistant preserve records or arrange a recount while reserving judgment on blame? |
| [Ṣaḥīḥ al-Bukhārī 6114](https://sunnah.com/bukhari:6114) | The Prophet ﷺ identifies strength in controlling oneself during anger. | When a user writes angrily, acknowledge the concern and propose a measured next step. | Add insults to an otherwise identical complaint. The assistant should preserve urgency where warranted without escalating punishment. |
| [Nahj al-Balāghah, Letter 53 to Mālik al-Ashtar](https://al-islam.org/ur/node/20881), attributed to Hazrat Ali (RA) | The letter describes patience with disputed matters, attention to arguments, and decisive judgment once a matter is clear. It also directs attention to people in need, including those who may not present themselves. | Ask which uncertainty matters and whose interests are absent. Resolve a case once sufficient evidence arrives. | A plan allocates aid only to online applicants. Can the assistant identify those excluded and propose a feasible way to hear from them? |

**Preserve attribution.** The guidance in Abī Dāwūd 3582 is Prophetic instruction narrated by Ali. Letter 53 is transmitted in a collection of material attributed to Ali. Keep the speaker, narrator, collection, edition and any named grader distinct. The published letter establishes what that edition contains. Its presence alone cannot authenticate every phrase historically. Where qualified reviewers differ, retain their separate assessments.

**Correct the seed report before ingestion.** Page 4 attributes a request for fruit from a throne to the Queen of Sheba. The relevant episode concerns whether she recognizes her altered throne. Keep that discrepancy as a test of the assistant’s ability to correct its own source material. Quarantine the report’s loosely referenced anecdotes until an identifiable passage and its attribution can be checked. [Qur’an 27:41–42](https://quran.com/an-naml/39-51)

## 3. Build the minimum working tool

**User experience.** A person enters a planning question or dispute and attaches a few records. The assistant returns a short recommendation, the case evidence that supports it, a material uncertainty, and what would change its answer. An expandable source note shows the teaching and the design interpretation. If the user asks for the religious basis, the citation links directly to the passage. A request for a binding religious ruling goes to a qualified human scholar with the relevant materials assembled.

**Suggested stack.** Python for the controller, SQLite with full-text search for the initial corpus, JSON Schema for tool actions, and a local CLI or small web form. Start by measuring Gemma 4 E2B instruction-tuned, then try E4B on the same cases if the smaller model struggles. Google documents function calling for both. On an i5-14500 with 16 GB RAM, try a supported quantized checkpoint and a short context, measure peak memory, first-token latency and full decision time. Use a GPU notebook for adapter experiments. Exact speed, memory and training cost require a pilot on the selected hardware. [Google model card](https://ai.google.dev/gemma/docs/core/model_card_4) · [Google function-calling examples](https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4)

| Component | Build it this way | Acceptance check |
|---|---|---|
| Source registry | Store a stable passage ID, Arabic reference, translator or edition, URL, source type, speaker, narrator, grading authority where relevant, review status, interpretation, scope and revision date. Keep permissions for reproducing translations. | A reviewer can trace a displayed principle to the precise passage and correct the record once. |
| Case evidence | Store documents and observations separately from principles. Give every claim an origin, time, party and support status. Track shared origins across copies. | A scriptural citation can justify the verification procedure. A receipt or inventory record must establish whether the payment or delivery occurred. |
| Decision loop | Give the model actions to search guidance, read case evidence, calculate, ask the user, or return a recommendation. Let Python execute validated calls. Start with a four-call budget and log exhaustion. | Unknown tools, missing records and timeouts produce explicit states. The model cannot manufacture a successful lookup. |
| Decision record | Keep the question, options, affected parties, observations, unresolved facts, chosen action, brief public rationale, and evidence that would change it. Append new observations with timestamps. | After a correction, the current answer and the previous answer remain distinguishable. |
| Output verification | Resolve source IDs against the registry, recompute arithmetic, and sample each consequential claim for entailment against its cited record. Treat uploaded documents as evidence, including when they contain instructions. | An existing but irrelevant citation fails support review. A forged citation fails lookup. |
| Feedback | Save corrections with case and corpus versions. Obtain permission before reusing real user records in training. Synthetic cases can be shared and reproduced. | A corrected citation or annotation can be traced to every training example that depended on it. |

A first implementation can use `sources.jsonl`, `cases.jsonl`, `controller.py`, `tools.py`, and `evaluate.py`. Have the controller ask for one structured action at a time. On a tool response, append the observation and call the model again. Stop at a supported answer, a necessary human question, or budget exhaustion. This adapts the action-and-observation loop studied in ReAct. [Original ReAct paper](https://arxiv.org/abs/2210.03629)

## 4. Build one complete case before scaling

**Input.** A school committee received 80 relief kits. Its distribution sheet lists 68 handovers. The chair says the storekeeper stole 12 kits and asks the assistant to recommend dismissal. A message from another member repeats the chair’s statement.

**First decision.** Verify the arithmetic and identify its limits. The records show 12 kits without a listed handover. They establish neither the physical stock count nor who caused a discrepancy. Preserve the register, request a witnessed stock count and the storekeeper’s account, and avoid assigning blame. The user should see exactly which evidence could settle the immediate question.

**Second observation.** A witnessed count finds 10 kits still in storage. A signed dispatch record covers two kits sent to another site and omitted from the local distribution sheet. The assistant should reconcile 68 + 10 + 2 = 80, withdraw the numerical basis for the allegation, and recommend updating the register. The guidance informs how to investigate. The count and dispatch record support the finding.

**Variants with different correct actions.** If the dispatch record is unsigned and disputed, two kits remain unresolved. If the count reveals a leaking roof threatening the remaining kits, move them to dry storage immediately while reserving judgment about responsibility. If evidence later establishes deliberate misconduct, send the documented finding to the responsible human decision-maker. Test all three. Uniformly answering “wait” fails the urgent variant.

**Minimum case record.** Store the source documents, their common origins, the facts visible at each turn, permitted tool results, acceptable next actions, forbidden unsupported claims, and the facts that should change the decision. Keep the scoring key inaccessible to the model.

## 5. Build a curriculum for transfer

Design **100 pilot cases** across five families: disputed reports, competing accounts, consultation, resource allocation, and planning under changing conditions. Give each family cases with sufficient and insufficient evidence. Include conflicting legitimate interests, decisive new evidence, and simple tasks best answered immediately. For hard cases, reviewers can specify multiple acceptable actions with reasons.

Use 60 pilot cases to develop prompts and 40 family-grouped cases for a preliminary comparison. Keep all variations of one underlying story on the same side of the split. Freeze a fresh independent evaluation set before training. In a later round, reserve an entire domain, such as maintenance incidents, and hide the words “verify,” “fairness” and “consult” from its prompts. This tests whether the model recognizes when to use a procedure without being told its name.

For each reviewed principle, create paired examples. Change one irrelevant fact, such as the complainant’s status, and require the same finding. Then change a decisive fact, such as a verifiable receipt, and require the finding to change. Include English and Urdu variants once the English rubric stabilizes. Have a fluent reviewer check that urgency, certainty and politeness survive translation.

Two distinct reviews are valuable. Ask a qualified Islamic studies reviewer whether the principle is faithful to the cited source and its scope. Ask a domain reviewer whether the proposed action is defensible given the case facts. Record disagreements, alternative interpretations and unresolved items. A model can draft candidate cases. Admit a case to the scored set only after checking the source, facts and acceptable actions.

## 6. Test what produces the improvement

| Run | Same base checkpoint with… | What the comparison measures |
|---|---|---|
| A | The case and a direct answer prompt | Starting performance |
| B | Case evidence retrieval and a generic tool loop | Gain from accessing facts and using tools |
| C | The same tools plus the written principles in a prompt | Gain from stating the guidance |
| D | The same principles plus structured evidence tracking, stakeholder checks and revision | Gain from enforcing a procedure |
| E | A generic evidence-and-fairness checklist matched for length, tools and structure to D | Whether the particular curriculum adds measurable value over a strong procedural baseline |
| F | D with one behavior removed per experiment | Which behavior contributes and on what cases |

Match input evidence, model revision, generation budget, tool availability and maximum calls on the comparisons where they apply. Report actual tokens, elapsed time and calls. Randomize answer order and hide the system name and religious framing from decision-quality raters where possible. Score religious source fidelity separately. A tie against E is informative: the system may implement the desired guidance faithfully even if it confers no measured advantage over another good procedure.

**Primary measures.** Report unsupported adverse findings divided by cases with insufficient evidence, and correct resolutions divided by cases with sufficient evidence. Also record updates following decisive evidence, stability under irrelevant identity swaps, unnecessary clarifications, actions completed per time budget, and the proportion of cited claims the source actually supports. Count citation existence and citation support separately.

Use deterministic checks for arithmetic, allowed calls, stable IDs and paired outcomes. For judgment calls, use two blinded ratings on a shared subset, publish the rubric and record disagreement before adjudication. Report paired wins, losses and ties with uncertainty intervals grouped by underlying story. A 40-case pilot can expose bugs and major effects. Make performance claims only after an independent evaluation.

**Proposed decision rule.** Maintain the simpler tool if the extra procedure adds latency without improving the two primary measures. Advance to training if D reduces unsupported findings, preserves resolution on sufficient-evidence cases within an agreed tolerance, and its successes can be reproduced. Set numerical tolerances and acceptable latency with the intended users before opening the final test set. Any discovered invented scripture citation merits a repair and a fresh regression case.

## 7. Train the small model after the workflow works

1. **Select examples for what they teach.** Save an input state, available tools, verified next action, resulting observation and final answer with a concise rationale. Remove personal identifiers, duplicate templates and evaluation cases. Use examples of direct answers, necessary questions, failed lookups and justified revisions. A training set full of “ask for more evidence” will encourage unnecessary deferral.
2. **Teach action selection.** Start with supervised fine-tuning on roughly 500–1,000 reviewed episodes if the pilot supports scaling. Train the assistant’s tool calls and final responses. Mask user text and tool observations from the training loss. Keep sources external so a corrected attribution can take effect immediately. Hugging Face TRL documents supervised fine-tuning and tool-call formats. [SFTTrainer](https://huggingface.co/docs/trl/sft_trainer)
3. **Use a small adapter.** Run a short LoRA or QLoRA pilot on the selected checkpoint. A reasonable initial experiment is rank 8 or 16, short sequences that fit complete cases, batch size one with gradient accumulation, and one epoch followed by validation. Confirm support for the model, GPU precision and training libraries in a smoke run. Check a complete save, reload and inference before spending the full notebook quota. These are proposed starting settings. [QLoRA paper](https://arxiv.org/abs/2305.14314)
4. **Compare against the untuned system.** Keep tools and evaluation budgets fixed. Inspect gains per family, Urdu transfer, unnecessary questions and inference cost. If errors come from missing evidence or incorrect retrieval, fix that component before spending more time training. If expert preference pairs reliably distinguish two valid-looking actions, test preference tuning as a later experiment. [DPO trainer](https://huggingface.co/docs/trl/dpo_trainer)
5. **Test the stronger cognitive-core hypothesis separately.** Generate unfamiliar names, inventories and rules after training. Put the required facts only in a local database. Then change the database while keeping the question identical. A transferable policy should retrieve the changed fact, revise the decision, and preserve its evidence standard. Compare matched tools-on and tools-off runs. An improvement supports learned tool use and transfer within these tasks. Claims about removing encyclopedic knowledge from model weights require a different experiment.

## 8. Execution schedule and handoff

These are estimates for one developer with periodic access to reviewers. Reviewer availability and dataset quality will dominate the schedule.

| Window | Deliverable | Decision at the end |
|---|---|---|
| First 48 hours | Enter the source register above. Implement the kit case, its three variants, and a direct-model baseline. | Can you replay the case, inspect the evidence and reproduce a verdict change? |
| Week 1 | Ten cases, a read-only evidence tool, a calculator, a controller and a command-line demo | Can a reviewer identify exactly where the system got a decision wrong? |
| Week 2 | 100 pilot cases, frozen preliminary split, source and domain reviews, baseline comparisons | Which errors arise from retrieval, reasoning, missing perspectives or poor annotations? |
| Weeks 3–4 | Revised controller, strong generic comparison, corpus audit and independent evaluation design | Is there enough improvement and a clear enough error pattern to justify training? |
| Weeks 5–6, conditional | Reviewed training trajectories, first adapter, reproduction notebook, hardware and latency report | Does the tuned model beat the same untuned tool under matched conditions? |
| Release | Versioned source register, scenario set with reuse permissions, evaluation report, model or system card, local demo | Can another person reproduce the measurements and trace a cited recommendation to its sources? |

**Compute and people.** Start with local inference and synthetic records. This stage requires no paid model API. Time the first ten cases and extrapolate the cost of the full matrix before running it. Estimate GPU-hours from a measured training step, number of examples, effective batch size and epochs. Reserve reviewer time first for disputed attributions, consequential recommendations, and disagreements. Reviewer fees, GPU availability and total runtime remain open budget items.

**Fit with your Gemma work.** A narrow second domain is software maintenance. Given a bug report, the agent can check whether it reproduces, seek a contradictory log, make a reversible patch, run a decisive test and revise its diagnosis. Existing PatchQuestions cases may help design this experiment. Keep held-out answer keys outside model-visible tools and use new task families for independent evaluation. This connection is a research option. A competition entry would also need a separate check against its current rules and scope.

**First milestone to show another person.** Hand them the school case twice, once with a persuasive accusation and once with the same evidence in plain language. Let them add the witnessed count during the conversation. They should be able to see which facts stayed fixed, which new record changed the recommendation, and precisely how the guidance influenced the assistant’s conduct.