# Earlier-copy transition and stereo correspondence screen

October 7, 2026. Research only; full investigation charter remains active.
Bounded computations reproduced and separately reviewed. No historical cause,
intent, original-sound, human-acceptance or legal-record finding.

## Result

The earlier upload has a conspicuous picture discontinuity between adjacent
presented frames 175 and 176, at approximately **5.8392 / 5.8725 seconds**.
Dense inspection corrects the coarse screen: a broad background facade is
still partly visible afterward. Its apparent movement cannot be timed as
uninterrupted physical motion merely from this derivative's frame spacing.

The held earlier soundtrack and excerpt C produced **no dominant-peak
scale-one waveform candidate** under the prospective criterion. Indeed, no
individual one-second block/channel comparison reached |r| = 0.95. The highest
forward-search magnitude was **0.1585056081**; the time-reversed-reference
maximum was **0.1378209406**. This supplies no audio-based alignment between
the copies. It does not establish unrelated soundtracks, fabrication, silence,
sound identity, or exclusion of shared audio after time scaling or processing.

## Sources and selection

- Earlier video: `../media/SIbqaybkbWI.f133.mp4`, 758,909 bytes, SHA-256
  `3f6db089b0e89cdfc030f6aaaf81227931681d26e0bd3c801b98cdcf486ba0d7`.
- Earlier audio: repair-disabled `../media/SIbqaybkbWI.f140.unmodified.m4a`,
  611,813 bytes, SHA-256
  `0776b39a597f236c85b98b0f1dd3931cb654ab08c967d508d5bfa6fc64f145ef`.
- C: [preserved stereo WAV](/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/edited-stereo.wav),
  SHA-256 `b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd`.
  This is the 25-second derivative of compilation file coordinates [430,455),
  not a newly authenticated camera recording.

The [earlier-copy report](../early-copy-report.md) supplies acquisition,
platform metadata, repair history and known source-chain limits. The
[prospective protocol](PROTOCOL.md) was saved before dense extraction and
historical waveform comparison, after the coarser screen was known.
No new historical media was acquired in this stage. Previous sources,
transformed copies, tests and results are preserved.

## Dense picture review

Both runs extracted every presented frame in PTS [4,7): 90 native 320×224 RGB
images, source indices 120–209 inclusive, at nominal 30000/1001 fps and source
time base 1/30000. The controlled extractor applies no crop, scale,
stabilization, interpolation or optical motion fitting. Overview thumbnails
are for screening; native files preserve the stored raster.

Root inspected all 90 thumbnails and native indices 174–177 before a separate
reader's findings. [Frozen notes](root-dense-notes.json) retain that coverage.
The main change is at 175/176: both framing and cloud configuration change
abruptly. A narrow inconsistent-looking strip at the bottom of 175 is visible
but has not received field/interlace/compression analysis. An edit or source
interruption is indicated, not a specific editor, duration, intention or
concealment finding. The strongest alternative is source-chain processing or
unpreserved capture intervals; nominal output cadence is not camera cadence.

The separate reader additionally selected 179/180. Root then inspected those
two native frames and agrees there is a stepped background-outline change
relative to foreground roofs; this is not a measured physical displacement.
No second comparable whole-scene replacement was identified in this limited
screen. No source-wide continuity finding follows.

An explicitly declared post-screen check found **90 distinct decoded RGB
hashes and zero byte-identical adjacent frames**. All maximal exact-equality
runs are singletons, indices 120–209. Because lossy decoding can make repeated
source exposures unequal, this is not proof of 90 unique camera exposures.
See [execution notes](execution-notes.md) for the order of this follow-up.

## Waveform method and controls

The installed decoder processed each whole input to native 44,100-Hz,
two-channel float32 PCM, with no gain change, channel mixing, seeking,
filtering or rate change at decoding. Decoder defaults and AAC packet
skip/discard metadata are retained; decoded coordinates are not authenticated
physical time. Float64 samples were then resampled as whole files to 6,300 Hz
using `scipy.signal.resample_poly(1,7,window=('kaiser',5.0),padtype='constant')`.

The early audio decoded to 1,665,024 stereo sample frames; C to 1,102,500.
Their resampled counts are 237,861 and 157,500. Each of C's 25 nonoverlapping
one-second blocks was compared against every fully contained one-second
reference window at the resampled grid, separately for all four channel
pairs. Window-specific demeaned Pearson correlation used an FFT numerator
and independently calculated sliding moments. Numerically unreliable centered
energy is undefined, not zero. Every signed profile is retained.

A candidate required at least three consecutive blocks, one channel pair and
polarity, each |r| ≥ 0.95 at its eligible global maximum, with source-minus-C
offset range ≤ 5 ms. First/last C blocks and source windows within 20 ms of
file edges were excluded only from candidate qualification, not the saved
scores. Up to five separated display peaks are not the entire search. The
threshold and tolerance are exploratory, not calibrated error rates or timing
confidence bounds. Reference reversal tests temporal-order sensitivity; it
does not constitute an independent null population.

Before historical calculations, 17 synthetic checks passed: exact/direct
normalization, sign/indexing, gains/DC offsets, inversion/channel swap,
non-grid shift through 44.1-to-6.3-kHz resampling, recoverable edited segments
without false bridging, constant/near-constant rejection, malformed inputs,
independent noise, repeated-tone ambiguity, reversal, edge eligibility and
overlapping candidates whose union is invalid. Maximum direct-versus-FFT
error was 5.55×10⁻¹⁶. Perfect competing tonal matches were retained rather
than treated as unique recording identification.

The first controlled implementation and `controls01` remain preserved. Root
requested a software guard tying historical runs to successful same-code,
same-protocol/runtime controls, and explicit decoder-version/packet records.
No score rule changed. Updated `controls02` passed the same 17 checks;
historical execution used that version. These tests do **not** calibrate
sensitivity to arbitrary codec generations, sample-clock drift, time
stretching, channel mixing, nonlinear filtering or acoustic environments.

## Numerical results

Maximum absolute correlation across all query blocks and source lags:

| C / earlier channel | Forward reference | Reversed reference |
|---|---:|---:|
| Left / left | 0.158506 | 0.137821 |
| Left / right | 0.152287 | 0.135589 |
| Right / left | 0.132841 | 0.129696 |
| Right / right | 0.129581 | 0.132345 |

Neither direction yielded an individual block at the 0.95 threshold or a
qualifying sequence. These are maxima from dependent searches, not p-values
or calibrated probabilities. They are not measures of event loudness or of
whether the reported bang exists. No agent listening is claimed.

Full outputs: [forward search](audio01/forward.json),
[reversed-reference check](audio01/reversed.json),
[first audio receipt](audio01/receipt.json),
[repeat receipt](audio02/receipt.json). Decoded and resampled arrays and all
200 signed profiles per run are retained alongside the reports.

## Verification and limitations

Dense runs `dense01` and `dense02` each passed six synthetic extractor checks.
Root independently rehashed all 145 manifest products in each run and its
controlled inputs; all pins match. The 96 historical frame/sheet/map/probe
products match between runs. An attempted existing-output run correctly
refused with exit 1, and all 158 files in the first output tree stayed unchanged.

Root reviewed the audio implementation and separately verified all 208
`controls02` product pins and its matching code pin before historical runs.
Both historical runs completed, each retaining 218 manifest products.
Root rehashed all 436 audio products, checked the unchanged controlled inputs
and empty-error successful decoder calls, and confirmed all 218 paired
products byte-identical. Each run retains 399,588,016 manifest-product bytes.

The [separate dense review](independent-dense-review.json) records 752 passing
assertions: a fresh sequential decode of all 1,130 source frames, exact PTS
selection, actual pixel equality for all 180 historical PNGs across the two
runs, and independent rechecking of synthetic pixels/clock/rejection behavior.
Two synthetic MKV containers differ in bytes between runs; their decoded
pixels and timestamps match. The 96 historical products are byte-identical.
Both readers agree on the main transition and source-chain limits. This is
separate nonblind, same-source AI computational review using the same FFmpeg
implementation, not independent historical corroboration, human acceptance
or qualified expert opinion.

The [separate audio review](independent-audio-review.json) verified 848 product
pins across both control and historical runs, freshly decoded both inputs and
reproduced both resampled arrays exactly. All 200 signed profiles match across
historical runs. An independently written direct oracle checked 800 positions
(zero, middle, last and reported best per profile), with maximum absolute
error 7.12×10⁻¹⁴ against a declared 1e-9 tolerance. It independently regenerated
eligible maxima and candidate intervals from the profiles and agrees there
are no candidates. The [read-only checker](review_audio.py) imports no producer
functions. This is not independent recomputation of every correlation lag;
decoder and resampler libraries are shared. Displayed five-peak lists were
checked for repeat equality, not independently ranked. No audio listening or
expert validation follows from these numerical tests. The separate inferential
read found no material overstatement after the review-role labels were made
explicit.

Exact calls use the saved scripts:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 T/dense_frames.py dense01
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 T/dense_frames.py dense02
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B T/audio_screen.py controls T/controls02
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B T/audio_screen.py historical T/audio01 --controls T/controls02/receipt.json
/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B T/audio_screen.py historical T/audio02 --controls T/controls02/receipt.json
```

`T` is this report's absolute containing directory. Receipts retain concrete
decoder/probe calls, source/product hashes and environment versions. Dense
work used Python 3.12.14, NumPy 2.3.5 and Pillow 12.3.0; audio used Python
3.13.7, NumPy 2.3.4, SciPy 1.16.2 and ffmpeg/ffprobe 7.1.1. The first dense
attempt failed at sandbox directory creation before extracting anything; its
scoped retry succeeded. A later read-only Ruby summary command had a syntax
error and was corrected; it did not alter scientific outputs. Intentional
refusal tests are not failed historical experiments.

## Consequence for the thermal-mechanism question

Assuming the user's term means nanothermite, a proposed thermal mechanism
must not automatically inherit the sound predictions of conventional
high-explosive demolition. Conversely, nanothermite is not a synonym for
silent reaction. Primary laboratory work measured pressure generation and
found that it was not determined by temperature alone ([Jacob, Kline and
Zachariah, 2018](https://doi.org/10.1063/1.5021890);
[author-hosted paper](https://mrzgroup.ucr.edu/sites/g/files/rcwecm2316/files/2019-02/2018_jap_2d_temperature.pdf)).
This study does not establish received sound levels for a building scenario,
historical capability, presence at WTC 7 or recording-specific detectability.
Its abstract and metadata were checked through the web reader; no new local
preservation copy is claimed.

Here, an absence of relevant sounds has not been established: the user's C
observation includes a bang, and neither its source nor recording lineage is
authenticated. Compatibility with a quieter hypothetical mechanism is not
positive identification. No cause ranking changes from this stage alone.

## Next discriminating work

The next source test is to recover the identified longer release copy or
establish image correspondence and rate relationships across the held copies.
Only then should a new, prospectively bounded audio test allow specific
speed/processing alternatives, with transformed positive controls and retained
competing alignments. Do not select a convenient audio shift to align the bang
with a desired structural event. Human listening, sound-source attribution,
recording detectability, material provenance and structural feasibility remain
separate requirements. A missing waveform match does not settle any of them.

## Working state

Saved in `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. This stage is intentional
uncommitted research alongside pre-existing work. No commit, push, main-repo
evidence modification, case promotion or external transmission. The generic
waveform-specificity lesson extends the existing Sherlock feedback note;
delivery remains pending the previously identified archived-task routing
decision. This does not block the next independent local source test.
