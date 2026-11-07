# PatchQuestions revised paper package

Prepared 7 November 2026. Read paper/PatchQuestions_Writeup.md for the revised paper, paper/README.md for reproduction, and SUBMISSION-CHECKLIST.md for the exact platform steps still needed. No account or submission action was performed.

The paper reports reproduced CPU resource results and an exploratory single-family intervention. There are no Gemma, human-study or repository-repair measurements.

Run the self-contained paper/PatchQuestions.ipynb in a fresh CPU kernel, or use:

    python -B tools/reproduce_paper.py --paper paper --output fresh-run
    python -B -m unittest discover -s tests -v

The complete independent reviewer checks can also be rerun:

    python -B reviewer/reviewer_audit.py
    python -B reviewer/protocol_audit.py

The reference sources are preserved under reviewer/reference. The legacy run_cpython_3_12_14 directory name is retained because the audit imports from it; the current recorded local run used Windows CPython 3.12.14. Coarse timing source reads/writes were made explicitly UTF-8. The unchanged reviewer source is reviewer/reviewer_audit.original.py.

CLAIM-EVIDENCE.md maps retained statements to artifacts. QUESTIONS-RESOLVED.md answers the revision challenges. STATUS.md and CHANGELOG.md record decisions, completed checks and remaining access boundaries. FILE_MANIFEST.json lists every payload except itself. The archive SHA256 is supplied alongside the ZIP.

This ZIP contains synthetic matrices and project code, with local user/workspace paths replaced in evidence copies. It excludes credentials, private competition tasks, model weights, installed libraries and private supervisor plans. This local package does not make a public license or author-rights declaration on the author's behalf.
