# Compute plan: Colab Pro + Kaggle

Updated 6 November 2026. User-confirmed resources: Colab Pro with 200 compute units, plus Kaggle competition GPUs. No units have been consumed by this project and no GPU session has been started by this assistant. The 200 units are the reported starting balance, not a live account reading.

## Platform responsibilities

**Kaggle:** establish the official 31B baseline, exercise the exact competition model and adapter-loading path, run offline harness validation, and perform full-budget rehearsals. Verify current account quota and actual accelerator availability in Kaggle before scheduling. Do not assume unlimited GPU hours.

Target **L4 ×4: 96 GB aggregate GPU memory across four devices**, with internet disabled. The competition page states these sessions consume quota at twice the older T4 ×2/P100 rate, subject to change. This is not a single 96 GB GPU. See [official accelerator details](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview/upgraded-accelerators).

The cognitive-core-inspired ledger and compaction ablations come before the main SFT pilot. They add no new Colab allocation: use CPU for design/trace checks and budgeted Kaggle runs for scaffold comparisons. See the [research brief](cognitive-core-research.md).

**Colab Pro:** inspect and prepare development-only training data on CPU; profile the assigned GPU; run a small E4B adapter pilot if supported; compare a few controlled training configurations; export and reload adapters. Colab results are development evidence, not a replacement for the competition harness. Do not assume its managed runtime can reproduce the harness's Docker isolation.

## Proposed allocation, not committed spend

| Stage | Maximum planned units | Release condition |
|---|---:|---|
| Compatibility and throughput profiling | 20 | Check GPU, VRAM, model loading, training-step memory and unit consumption |
| E4B verified-trace SFT pilot | 80 | Exact model/template support established; sample adapter loads in Kaggle |
| Controlled comparisons | 40 | Pilot is stable; compare only a few configurations on frozen validation folds |
| Export and reload verification | 20 | Promising candidate; check adapter integrity and repeatability |
| Recovery reserve | 40 | Keep unallocated until an actual recovery need or measured gain justifies it |
| Total | 200 | Stop or rescope before exceeding the reported balance |

Unused stage units remain unspent. Stop a weak pilot early. This allocation intentionally prioritizes a reproducible no-adapter submission and a modest adaptation experiment over a large RL campaign.

## Measure before estimating duration

Colab hardware and runtime availability vary; 200 compute units do not imply a fixed number of GPU hours. Read the assigned GPU and the consumption rate shown by Colab. For a measured rate r units/hour, a stage with C units has an approximate ceiling C/r hours. If a rate is not displayed, estimate it from a sufficiently long timed balance change. Include model-loading and idle connected time in the observed cost. Do not treat a short training-step timing as total session billing.

Record session date, GPU type, VRAM, available balance, observed units/hour, model revision, peak training memory and examples/hour. Check unit expiration in the account; it has not been inspected here. Recalculate each new session and stop GPU runtimes when GPU work is done. Prepare data and analyze logs on CPU wherever practical.

## Model and training gates

1. Run the official Kaggle sample unchanged on a small task set.
2. In Colab, confirm available hardware and compatibility before downloading a large model or starting training. Prefer E4B for the first pilot; even this requires an actual memory smoke test at the intended sequence length.
3. Check the train/serve base revision, chat template, target modules and quantization path. Training with a generic quantization backend does not prove that the competition's QAT artifact can load the resulting adapter.
4. Produce a tiny adapter, save it and verify loading in the exact Kaggle harness before releasing the 80-unit training allowance.
5. Compare no-adapter and adapter outcomes on identical held-out tasks. Promote only on end-to-end repair and runtime evidence.
6. Consider 12B only if measured memory and throughput leave adequate headroom. Do not plan 31B Colab training until the assigned GPU and a training-step memory test demonstrate feasibility. Keep the 31B Kaggle baseline available regardless.

## Persistence and transfer

Save resumable checkpoints, optimizer/scheduler state when applicable, training configuration, split hashes and final adapter checksums to user-controlled persistent storage. Keep checkpoint cadence short enough that interruptions do not lose a large fraction of a stage. Copy working data to runtime-local storage for training and persist checkpoints deliberately; avoid heavy training I/O directly against mounted Drive.

Transfer only intended submission artifacts into the competition notebook. Keep credentials, raw gold evaluation patches and held-out verification tests out of agent-visible inputs. Check artifact checksums after transfer and verify the complete offline run in Kaggle.

Source for variable availability, runtime behavior and storage guidance: [official Colab FAQ](https://research.google.com/colaboratory/faq.html). Allocations and platform assignments above are project recommendations, not service guarantees.
