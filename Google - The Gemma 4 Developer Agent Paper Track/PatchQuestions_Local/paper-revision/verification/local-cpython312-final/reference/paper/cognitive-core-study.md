# Can Gemma still choose a useful question when the API clues disappear?

Karpathy proposes retaining general strategies for problem-solving while letting a model look up more of its factual knowledge. In the Dwarkesh interview he discusses this around 13 minutes and again at 56:20. We borrow one question from that proposal. Can a coding model use the pattern of disagreement between candidates even when it cannot recognize the API from the examples? [Interview and transcript](https://www.dwarkesh.com/p/andrej-karpathy)

Imagine four patches. An ordinary example gives identical results for all four. Another example divides them into two pairs. The latter still gives a developer a useful choice if the two outcomes are renamed A and B. Within each column we replace distinct outputs with distinct tokens, replace input names with indices, and preserve candidate order across conditions. Labels only have meaning within a column.

## Control result

Using the original frozen data, greedy entropy chose the same questions and retained the same candidate rows in both views across all 750 target–split episodes from eight families, with a budget of three. Renaming outcomes preserves the size of every group used by entropy. This check establishes that both views contain the same information for that strategy. It measures the experiment setup. Gemma performance remains an open question.

From the public/project folder run `python cognitive_probe.py --check`. For an interactive episode run `python cognitive_probe.py --family csv_fields --split 19 --target 0 --view masked`. Switch to `--view named` for its matched pair. The supervisor owns the process. Give the model only its JSON messages. Keep command arguments, files, process access and final score outside the model context.

## One-week pilot

Freeze one Gemma checkpoint, inference settings, prompts and scoring rules before starting. Begin with split 19 and target indices 0 and 1 for every family (16 paired episodes, 32 sessions). This convenience sample is for feasibility. Use fresh model context for every session, alternate condition order, and use the identical three-question ceiling. Provide only the same action instructions and the appropriate matrix. Log exact model ID, replies, actions, oracle answers, token counts and elapsed time. Count invalid actions as failures and retain the transcript. Stop after 32 sessions or a predeclared cost cap and report any missing pairs.

Score each pick by agreement on every held-out input. Report paired wins, losses and ties, separately by family, alongside questions used, uninformative queries and picks inconsistent with observed answers. Compare entropy and random informative selection on those same targets. If entropy stops with tied candidates, average over uniform final picks. Do not substitute the published full-benchmark average for a matched baseline.

A named-view advantage could reflect familiarity, tokenization, input length or readability. Equal scores could also reflect failure in both views. Report absolute scores. A useful follow-up permutes the anonymous labels and row order to check sensitivity to presentation. Neither outcome identifies what Gemma learned internally. Reserve claims about new-task transfer for a blind extension on fresh families.

## How the clarification literature changes the paper

Ambig-SWE separates detecting missing information, asking, and using the answer. PatchQuestions starts after ambiguity has already been exposed through candidate disagreement. Its narrower contribution is controlled measurement of which question the agent spends next. [Ambig-SWE](https://arxiv.org/abs/2502.13069)

Edwards and Schuster study when a repository agent should ask or proceed. Allowing an early pick and reporting questions used exposes that choice in our setting. [Ask or Assume?](https://aclanthology.org/2026.findings-emnlp.15/)

SWE-Clar evaluates clarification and subsequent implementation separately. Keeping the interaction transcript lets a reviewer distinguish a well-chosen question followed by a bad patch choice from a question that supplied no information. [SWE-Clar](https://arxiv.org/abs/2610.31854)
