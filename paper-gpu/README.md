# PatchQuestions GPU pilot

The notebook executes 64 preregistered sessions with base Gemma 4 31B QAT. The core has 16 paired named/masked cases (32 sessions). The controls have 16 zero-question named cases and 16 entropy-assisted final picks. Targets and row orders match across arms. Greedy generation uses a 128-token output cap and thinking disabled, subject to successful server/tokenizer calibration.

Attach the organizer wheelhouse, Google Gemma 4 31B QAT w4a16 version 2, and the main competition only when this experiment is within that competition's permitted accelerator scope. Internet stays disabled for L4. The self-contained notebook embeds the evaluator and frozen data. It performs offline installation and launches the worker in a fresh process.

Outputs include environment and model metadata, a disjoint calibration exchange, frozen private plan, matched baselines, preflight token counts, per-turn transcripts, failure-inclusive summaries, complete-pair comparisons, and independently replayed grades. All data stays outside the text-only model's tools/context except the displayed matrix and acquired answers. A timestamped zip and SHA-256 file are written under /kaggle/working even if calibration or scoring fails. Save the notebook version with outputs and retain the archive.

CPU verification uses the canonical project's paper-revision/tests/test_pilot.py. The implementation adds token-mapping, control-arm, incomplete-pair, entropy-selection, and tampered-transcript checks to the original twelve tests. No GPU result is bundled.

For external local serving, use the canonical pilot.py freeze, baselines, run, summarize and replay commands. Pass --controls to freeze to include all 64 sessions. An existing run directory is never overwritten. Failed runs are preserved and corrected configurations receive a new run ID.
