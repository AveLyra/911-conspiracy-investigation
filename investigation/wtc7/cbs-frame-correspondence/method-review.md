# CBS frame correspondence: pre-score method review

2026-10-04 UTC. Separate methodological reader `/root/stage2_visual`.
This is a research-method critique, not independent historical evidence.

## Disposition

**Conditional acceptance for the bounded source-candidate pilot only.** The
current protocol resolves the two material pre-score defects identified during
review: interpolation can contaminate nominally valid pixels, and the initial
ranking language left comparison groups underspecified. No additional protocol
or region change is required by this review. Execution remains conditional on
the protocol's fresh adapter controls, source/frame joins, reproducibility and
bounded-run checks. This review does not certify that implementation or those
checks have passed.

The pilot can proceed on that basis without pretending to satisfy the charter's
actual-human review gate for consequential automated measurements. Candidate
retrieval is the approved purpose; exact exposure, event timing, glass state,
fire magnitude, physical mechanism, model validation and hypothesis rankings
are not outputs authorized by a correspondence score. A later consequential
use still needs its applicable human review. No extra general review framework
or premature human gate is proposed here.

## Reviewed versions and actual scope

The final protocol was read through its end; pins below were checked at
2026-10-04 02:46:53 UTC. Earlier protocol wording was also read and critiqued
before correction. No historical candidate score or candidate image was read
for this review.

| Record | SHA-256 |
| --- | --- |
| Current `PROTOCOL.md` | `4cf06e45c4216fa8662c90b84d4a9f78278b6704b1fcae342746cc9f4c556faa` |
| Unchanged `regions.json` | `5bec4e5a1275f3cfaafd82fc534065ff190b3278c33bc1a5beb8f482de111694` |
| Main-repository investigation `CHARTER.md` | `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd` |
| Completed CBS source-screen `stage4/report.md` | `5408e26089855db635ffee0f4fea453d7bb2a4ba5b59203c962900431db2f733` |
| Reused Peskin `match_screen.py` | `06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8` |
| Peskin arithmetic `method-review.md` | `6d34ed85e8405dc67f1a9c40ea2f8c310eb84822c68505d54fdf28f1bb6d1abb` |

The main charter was reread, the numerical kernel and its arithmetic review
were read completely, and the preparation record was read. Prior source-screen
familiarity is substantial: this reader performed stages 2–4 using a frozen
textual reference record inherited from a replacement-reader setup. This is
neither blinding nor a fresh independent historical source. The two new
reference views below serve only the new mask audit; they do not revise old
frozen observations or retroactively remove their textual-reference limitation.

## Actual reference views and mask checks

Both authorized reference JPEGs were displayed once, complete and native, with
`view_image(detail="original")`, in the order 143 then 142. Both displays
succeeded. Before/after tool clocks both read **2026-10-04 02:39:41 UTC**.
There were no candidate displays, transforms, crops, audio, network retrievals
or additional reference displays.

| Reference | Native dimensions | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `../fire-coverage-batch3/assets/run01/images/A-60c26b7f3416.jpg` (143) | 705 × 480 | 115624 | `744b8faff26ea05c8303dfe278d1644f7e949a0f0b3ec02ab13abf9a4af3fb75` |
| `../fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg` (142) | 706 × 457 | 151488 | `68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a` |

For 143, the static rectangles correspond to the pale right-hand facade and
middle rectangular grid below the upper irregular dark features. The dynamic
rectangle covers the broad left orange/yellow and veiled region. The visible
bottom copyright strip is outside the declared masks. These are plausible
registration regions, but the static content is sparse/repetitive and the
dynamic rectangle is not a pure flame mask. This view does not create a new
shared finding about the fine descending trace noted differently in the prior
source screen.

For 142, the static rectangles correspond to the separate left foreground
building, the green sign and the right facade grid. Their declared native
bounds avoid the obvious red report labels and top copyright strip at this
descriptive inspection. The two dynamic rectangles cover the veiled gap and
orange/yellow region adjacent to the facade corner. They also include stable
background. This is not a quantified certification that every resampled pixel
is label-free, smoke-free or physically stationary. The different object
depths make parallax a real limitation of the allowed transform family.

A fresh read-only bundled-Python check opened the two image headers, checked
declared dimensions, rectangle bounds and the half-open working-center mask
mapping. It asserted disjoint static/dynamic masks and exited zero:

| Reference | Static working pixels | Dynamic working pixels | Intersection |
| --- | ---: | ---: | ---: |
| 143 | 2783 | 5236 | 0 |
| 142 | 2951 | 1827 | 0 |

This validates those dimensions, bounds and center-mask counts, not the new
adapter, interpolation support, historical matching or statistical independence.
No mask retuning is requested.

## Material findings and their disposition

1. **Excluded-pixel leakage — corrected prospectively, controls still required.**
   Initial protocol SHA
   `38df9ee7cd401a343b9940f1fa93ef812f0427ab46298333c841809b843f8b22`
   combined bilinear image resampling with nearest-sampled binary validity.
   That alone does not stop excluded bottom-quarter pixels contributing to
   otherwise valid boundary pixels, either during normalization or later scale
   changes. The current finite rule excludes working rows 88–119 and a further
   two rows above the scaled validity boundary. Its adequacy is conditional on
   the required excluded-pixel invariance tests for all three representations
   and thirteen scales at the fixed sizes. Two inputs identical in permitted
   native pixels but different in excluded pixels must produce identical
   declared-valid working and scaled values. A failed invariant stops scoring;
   an arbitrary zero fill must not become valid black evidence. This is a
   bounded engineering guard, not a proof for arbitrary filters or dimensions.

2. **Ranking groups — corrected before scoring.** The initial wording did not
   explicitly settle joint versus separate paired/cross-view ranking, or which
   metric's “best score” defined near-best sets. The current protocol specifies
   paired-only visual shortlists, separate target/source-clip/representation/
   metric sensitivity sets, and explicit empty/reasoned all-invalid groups.
   That is sufficiently determinate for the pilot. Cross-view results must
   remain visible, not be silently dropped when inconvenient.

3. **Reuse boundary — appropriate but not an adapter certificate.** The pinned
   core computes masked correlation on actual valid overlap and enforces the
   strict variance floor. The old hard-coded target dimensions, full-valid
   canvases and historical runner cannot establish the new adapter's behavior.
   The prior arithmetic review expressly does not verify new Pillow resizing,
   parity handling, validity guards, masks, search ranking or historical
   discrimination. Fresh core results reported in `METHOD-NOTES.md` are root's
   reported runs, not executions by this reviewer. Required new controls must
   be demonstrated separately, including the strict variance-boundary behavior.

## Strongest false-match and false-negative alternatives

- Repeated facade modules and smooth pale areas can yield similar static
  scores at different locations or times. The same geometry may persist while
  smoke/flame appearance changes; another recording can share the view. A
  stable-scene/changed-dynamic synthetic control is therefore substantive, not
  ceremonial.
- Dynamic regions contain stationary background and broad brightness/veiling
  gradients. A high dynamic score need not identify one exposure. Spatially
  disjoint masks do not make their scores independent evidence; full/even/odd
  representations are also correlated treatments of the same recording.
- Cross-view controls are difficult alternatives, not authenticated unrelated
  negatives. They cannot by themselves estimate a false-match probability.
  Testing many translations, scales and frames also favors chance high scores;
  neither peak correlation nor the three near-best tolerances is a confidence
  level or a calibrated error rate.
- Allowed scale/translation may fail under parallax, unknown report crops,
  nonlinear intensity adjustment, annotation effects or reference-field
  processing. Failure is therefore limited to this search. Different overlap
  masks can also change which content contributes despite the 85-percent
  coverage gate; keep coverage/surfaces rather than presenting all scores as
  comparisons over identical content.
- The 18-frame pilot is sparse coverage, not the 1317-frame planned population.
  It cannot recover an absent-between-samples moment. Its 108 comparisons are
  computational tests, not 108 independent observations. A successful pilot
  does not authorize dense decoding or erase the separate finite execution
  schedule requirement.

These limitations are compatible with useful candidate retrieval if preserved
in the synthesis. They prevent a best-scoring frame from becoming exact source
identity, a physical observation, or a new hypothesis ranking by implication.

## Acceptance boundary and verification record

This review used local text reads, `shasum -a 256`, file/header checks, the
read-only mask arithmetic above, and exactly two authorized image displays.
No historical computation, new adapter execution, core-control rerun, dense
decode, runtime/output-cap test or source-index/PTS join verification was
performed by this reviewer. Implementation acceptance belongs to the pending
separate audit and observable protocol controls, not this conditional verdict.
The approved deliverable here is only this methodological review. Old records,
regions, protocol, legal materials and historical judgments were not edited.
