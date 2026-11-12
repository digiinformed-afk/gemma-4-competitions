# Implementation checkpoint — 12 November 2026

## Current verified state (supersedes historical notes below)

Kaggle version 3 / 368723141 completed all 64 scheduled sessions on four L4 GPUs. Its complete downloaded output, original sources and independent local replay are retained in [verification/gpu-attempt-368723141](verification/gpu-attempt-368723141/README.md). Strict successes: named 3/16, masked 4/16, entropy-assisted 8/16; the 16 zero-question responses all failed strict parsing because of Markdown fences. Every scored request's token accounting matches server usage (116 requests, calibrated offset +1). The canonical manuscript now includes this exploratory pilot and its limitations.

The future-run zero-question prompt now explicitly specifies bare JSON and prohibits Markdown fences; the original scored source and failures remain intact. Twenty supervisor tests and the retained-evidence replay passed locally. No corrected-prompt GPU rerun is claimed. Kaggle paper draft was updated; final submission will be recorded only after platform confirmation.

## Historical checkpoints

Draft PR #3 contains the implementation. Eighteen CPU tests pass, including all 64 sessions through a scripted transport with replayed grades. GPU model scores are pending.

The complete manuscript draft is at https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/patchquestions-a-benchmark-for-budgeted-api-contr . Kaggle counts 2,445 words (report body starts at Abstract; title and subtitle use their dedicated fields). All six checklist items are filled. Final submission remains pending.

Run 368669099 failed before model loading because the new notebook defaulted to Python 3.13 while organizer wheels require CPython 3.12. The failed version is retained.

The corrected notebook was copied from the existing working Hikmah Python 3.12 notebook, retaining the pinned original environment and inputs. It contains only the new GPU experiment code. The active version is https://www.kaggle.com/code/digiinformed/patchquestions-gpu-pilot-python-3-12?scriptVersionId=368670223 . Logs confirm Python 3.12.13 and GPU L4 x4. Inspect its logs and outputs, repair recoverable failures, retain the archive and replay grades before updating manuscript claims.

The full CPU notebook was executed successfully in a fresh CPython 3.12.14 process in 14.6 seconds; its executed copy and runtime record are in paper-gpu/verification. All four GPU payload files have byte-verified source hashes in PACKAGE_MANIFEST.json. Subsequent package revisions add streamed logs, multi-turn/long synthetic calibration and GPU snapshots; active Kaggle version 368670223 retains its earlier immutable source. Those later package changes have not been executed on GPU yet.


Attempt 368670223 terminated after 1,333.3 seconds. Retained worker.log shows CUDA OOM during warmup with 256 dummy requests. No scored plan or model session was produced. The installer subprocess environment had not propagated the graph-memory setting to the worker. Failure logs, environment and provenance are retained under verification/gpu-attempt-368670223. Corrected version 2 is running at https://www.kaggle.com/code/digiinformed/patchquestions-gpu-pilot-python-3-12?scriptVersionId=368678382 . It carries the official graph-memory environment into the worker, uses 80% memory utilization, and extends the organizer server command with --max-num-seqs 1 and --max-num-batched-tokens 8192. It also streams worker output and calibrates opening, multi-turn and long synthetic prompts before freezing the 64-session schedule. Results remain pending.
