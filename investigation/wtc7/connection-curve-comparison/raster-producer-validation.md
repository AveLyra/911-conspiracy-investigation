# Synthetic raster producer: commands, results and limits

September 27, 2026. Reused/prior-informed AI implementation by `curve_render`.
This is a finite synthetic presentation/uncertainty experiment, not historical
curve tracing, an identity classifier, human acceptance or physical validation.
Development-verification, evidence-falsification-auditor and
source-of-truth-guardian were applied to preserve failed outcomes and keep
software verification separate from scientific acceptance.

## Frozen inputs and implementation

Read current main AGENTS and complete CHARTER, then the complete raster stage,
NUMERICAL-PROTOCOL, HUMAN-REVIEW-GATE and REGISTRATION-STAGE. Root clarified
point-sampling, rounding, half-open bands and codec settings before the sweep.
No full sweep preceded root's complete producer inspection and clearance.
Root supplied several sampler boundary expectations before tests; these are
shared controls, not an unseen independent oracle.

| Input / code | SHA-256 |
| --- | --- |
| RASTER-UNCERTAINTY-STAGE.md | 4adaa3b617a624de9353feda130c1778e0c60d00e133d88754f66baa3298b248 |
| raster_uncertainty.py | 878872fcde4316e2655e156221de970a41f5186351a9525159c7eb7520e8760f |
| test_raster_uncertainty.py | eef9c8e5bd97bcb40f6f47f7e32419cff6b0ea5a43539acbb4bf486b7e036188 |

Only the two scripts, `synthetic-run01`, `synthetic-run02` and this note were
created by this implementation job. Source images/PDF, prior viewer,
registration, historical arithmetic, main/legal/raw files and navigation were
not changed. No historical pixel file was read. No browser or image viewing
was used by this producer; exact synthetic sampling and pixel computations
were tested numerically. Independent review and any synthetic visual QA are
separate from this producer's checks.

Runtime: bundled Python 3.12.14; Pillow 12.3.0; reported JPEG codec 6.2;
libjpeg-turbo 3.1.4.1. The executable SHA is
`ac60cfe0268614638d0ffa35f3b0284fc7b3a11482723793455e17eeb278509e`;
Pillow entry SHA `7361b6ad3878589affe5956e4a4da24d71398b0891fd3a8c15e9362217b4ca01`;
imaging-binary SHA `ee754300d3bda6413b80ddabe3a7ed7b419e1b0468bf2830e2b19fe68f14be42`.
These are entry/binary pins, not a complete dependency closure.

## Actual commands and retained failures

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/test_raster_uncertainty.py
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/raster_uncertainty.py --run synthetic-run01
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/raster_uncertainty.py --run synthetic-run02
```

Focused controls: **14/14 passed** before the sweep, and **14/14 passed** on
the post-sweep rerun. No test assertions failed. They cover exact declared
subpixel counts, half-up mixing, band/domain/dash edges, contrast and off-color
threshold equality, all seven colors' 0–16 sampled-coverage mixtures,
blank/white/bool/nonfinite/malformed rejection, disconnected components,
complete cell envelopes and all allowances, explicit gap leakage reporting,
codec roundtrips, all three separately rendered ambiguity pairs, fixed output
names, exclusive writes, wrong protocol pin and retained injected execution
failure. The injected failure occurs only in a temporary synthetic test
directory; it is not a failed scientific fixture.

Both first full-run attempts stopped at `output.mkdir(exist_ok=False)` with
`PermissionError: [Errno 1] Operation not permitted` in the sandbox. Neither
created its output directory, so no per-run failure file could be written.
The exact commands were rerun through normal scoped worktree-write approval.
Approved runs both exited 0 and retained every declared result. No threshold,
allowance, fixture or codec setting was changed after outcomes.

## Saved schema and actual coverage

Fixture IDs are `color-wW-mM-pP-style`, where M and P are **twice** the slope
and phase. Each `cases/<id>/<codec>.json` accompanies its PNG/JPEG. The JSON
records exact parameters/settings, base/encoded/decoded hashes, warnings,
all 128 column records and complete per-fixture summary lists. Each column
retains `truth_support`, twice-valued analytic `truth_centerline_y2`, **all**
disconnected `runs_y` cell-edge intervals and widths, missing/ambiguous/single
status, a single-run envelope only if justified, and all four expanded
envelopes/widths/coverage outcomes. Missing or ambiguous coverage is null,
not false agreement. Gap candidates remain separate from true support.

An additional read-only standard-library check independently enumerated the
saved IDs and codecs against the full Cartesian set, checked each column
index sequence and verified every listed product's byte length/hash:

- **112 actual base IDs × 5 codecs = 560 distinct cases**;
- **71,680 actual column records**: 53,760 true-support and 17,920 gap columns;
- **30 actual ambiguity images**, from three pairs × two sides × five codecs;
- **1,158 products + manifest = 1,159 files per run**, 30,865,680 bytes each;
- zero codec warnings; no gap-column candidate was found on this finite grid.

Every relative filename and every file byte—including manifest—was compared
between run01/run02: **all 1,159 matched exactly**. Six source/code/control
input pins matched before/after and again after both runs.

Both manifest SHA-256:
`97ee9afda99a508c1fcbbe6d8b3f27df6674a0f970f43dcb651ba1182c2b60a8`.
Both summary SHA-256:
`df55c100e43b5740d0eb16bf0b03a49afe3163b76030bfe825b3792aa3641362`.
See [run01 manifest](synthetic-run01/manifest.json),
[run02 manifest](synthetic-run02/manifest.json) and
[complete run01 summaries](synthetic-run01/summary.json). The manifests pin
all per-column JSON/image products and runtime record. Deterministic manifests
use an exact fixed command template rather than run-specific timestamps or
output-directory names; actual commands above distinguish the two executions.

## Results, including failures

Each codec has 10,752 true-support columns. The four rightmost values below
count **single-run enclosure failures only**, at allowances 0, 1, 2, 4.
Missing and ambiguous columns remain unresolved at every allowance and are
not counted as successful enclosures.

| Codec | Missing | Ambiguous | Single run | Failures at 0 / 1 / 2 / 4 px |
| --- | ---: | ---: | ---: | --- |
| PNG | 0 | 0 | 10,752 | 0 / 0 / 0 / 0 |
| JPEG 95, subsampling 0 | 0 | 0 | 10,752 | 0 / 0 / 0 / 0 |
| JPEG 75, subsampling 0 | 16 | 40 | 10,696 | 64 / 0 / 0 / 0 |
| JPEG 75, subsampling 2 | 2,213 | 1,409 | 7,130 | 2,259 / 540 / 0 / 0 |
| JPEG 50, subsampling 2 | 2,610 | 2,386 | 5,756 | 2,081 / 433 / 0 / 0 |

The finite grid therefore falsifies a claim that this fixed known-color probe
always recovers a unique supported envelope under all declared encodings.
Increasing an allowance cannot restore missing support or resolve multiple
components. Widths expand by exactly twice the allowance; lower failure
counts do not imply higher precision. The favorable PNG/95 results are not
historical uncertainty calibration or a population-level detection rate.

All three different-latent-scene pairs have equal visible base RGB, encoded
bytes and decoded RGB under every codec. The latent descriptors and draw/mask
order are saved in separate `ambiguity/<id>/latent.json` files. The crossing
pair changes identity assignments after the crossing; the dash pair replaces
dashing with opaque white gap masks over a solid line; the absence pair hides
a present line under a whole-image white mask. Both sides are independently
rendered. Codec preservation does not make these fifteen independent findings:
there are three constructive counterexamples to universal pixel-only identity.
Independent analytic review must still verify these constructions.

## Inference ceiling and next prerequisites

The sampled-color predicate is an exact implementation of a supplied target
test, not a method of authenticating which historical curve supplied a pixel.
The 4×4 sampler estimates area coverage; it is not analytic area integration.
Selected artificial colors, widths and codecs do not estimate the historical
JPEG history, ink, overlays or compression artifacts. Mixed-color crossings,
gridlines/text rejection and a human labeling task are not tested by the 560
isolated-line cases. A zero gap-candidate count here is not general absence
evidence. Independent replay, not this producer's self-comparison, addresses
implementation independence.

Before consequential historical curve extraction: actual human axis/legend
and selected-coordinate checks; source-native color/linewidth/overlay and
clip characterization; explicit visible-support and unresolved-identity
declarations; and independent source-to-coordinate verification remain
necessary. No historical metric, native solver recovery, constitutive-law
replacement, cause ranking, legal conclusion or human acceptance follows.
