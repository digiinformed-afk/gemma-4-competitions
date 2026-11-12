# Implementation checkpoint — 12 November 2026

Draft PR #3 contains the implementation. Eighteen CPU tests pass, including all 64 sessions through a scripted transport with replayed grades. GPU model scores are pending.

The complete manuscript draft is at https://www.kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/patchquestions-a-benchmark-for-budgeted-api-contr . Kaggle counts 2,445 words (report body starts at Abstract; title and subtitle use their dedicated fields). All six checklist items are filled. Final submission remains pending.

Run 368669099 failed before model loading because the new notebook defaulted to Python 3.13 while organizer wheels require CPython 3.12. The failed version is retained.

The corrected notebook was copied from the existing working Hikmah Python 3.12 notebook, retaining the pinned original environment and inputs. It contains only the new GPU experiment code. The active version is https://www.kaggle.com/code/digiinformed/patchquestions-gpu-pilot-python-3-12?scriptVersionId=368670223 . Logs confirm Python 3.12.13 and GPU L4 x4. Inspect its logs and outputs, repair recoverable failures, retain the archive and replay grades before updating manuscript claims.

The full CPU notebook was executed successfully in a fresh CPython 3.12.14 process in 14.6 seconds; its executed copy and runtime record are in paper-gpu/verification. All four GPU payload files have byte-verified source hashes in PACKAGE_MANIFEST.json. Subsequent package revisions add streamed logs, multi-turn/long synthetic calibration and GPU snapshots; active Kaggle version 368670223 retains its earlier immutable source. Those later package changes have not been executed on GPU yet.
