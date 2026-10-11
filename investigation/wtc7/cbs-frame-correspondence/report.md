# CBS source frame comparison pilot

2026-10-04 UTC, October 3 locally. **The pilot strengthens two scene-specific
leads but does not identify an exact published exposure.** Clip 7 index 564
leads both geometry and changing-detail scores for Figure 5-142. For Figure
5-143, several Clip 3 frames fit the geometry nearly equally well; changing
detail remains only partly testable. No finding about fire severity or collapse
cause follows.

This follows the completed [eight-clip screen](../cbs-vince-source-screen/stage4/report.md)
using the separately declared [protocol](PROTOCOL.md) and [regions](regions.json).
The protocol was reviewed and corrected before scoring, not fitted to these
results. All original sources, earlier observations and the unrelated human
comparator ±1-pixel placement record remain unchanged.

## What the scores establish

The method fits scale and translation using specified stationary-geometry
regions, then compares changing regions without refitting. The latter include
background and smoke as well as bright flame-like detail: they are not pure
fire measurements. The table gives the full-raster arm; separate even/odd-row
arms preserve the same leading indices.

| Reference and candidate clip | Best static score and index | Best dynamic score at each frame's best static transform | Decisive limitation |
| --- | --- | --- | --- |
| Figure 5-142 / Clip 7 | 0.91844 at 564 | 0.84636 at 564 | Useful bounded candidate, not unique exposure authentication. Reference processing, soft detail and hidden lower context remain. |
| Figure 5-143 / Clip 3 | 0.98929 at 188 | 0.86676 at 141 | Frames 118, 141, 165 and 188 lie within 0.005 of the best static score. Dynamic coverage at 188 fails the fixed gate, so its dynamic counterpart is untested, not rejected. |

As preregistered, dynamic ranking uses each frame's best **static** transform;
it does not maximize dynamic scores over both retained geometry alternatives.
The runner-up geometry and its dynamic score remain in the complete results.

For Figure 5-143, only five of nine full-arm candidate frames have an admitted
dynamic score. At the static fit for index 188, dynamic coverage is about
77.9 percent, below the declared 85-percent minimum. Four near-best geometry
fits and incomplete changing-detail coverage cannot locate one exact moment.
The static winner 188 also uses only about 87.3 percent of its static mask;
the other three 0.005-near-best static fits use effectively the full mask.
Their scores therefore compare different surviving content, another reason
not to interpret the small score advantage as exact identity.
The available dynamic leader 141 does not prove that 188 is a different exposure.
All three comparison arms have the same geometry/dynamic leaders; those arms
are correlated treatments of one recording, not three independent sources.

For Figure 5-142, index 564 is the sole member of each full-arm near-best set
at differences 0.005, 0.01 and 0.02 for both metrics. That is separation **within
these nine samples and this method**, not a confidence level or proof that
unexamined frames cannot match better. Its even/odd static leaders range from
about 0.91981 to 0.91999; dynamic leaders from about 0.84741 to 0.85474.

The cross-view comparisons were retained. Across arms, Figure 5-142 against
Clip 3 has static maxima about 0.536–0.569; Figure 5-143 against Clip 7 has
static maxima about 0.698–0.712. These lower maxima favor the intended pairings
within the declared test, but cross-view scenes are not authenticated unrelated
negative controls and do not calibrate a false-match probability. Full results,
coverage, missing scores, transforms and all 72 near-best sets remain in
[pilot01](pilot01/summary.json), not just the winners.

## Native image check

Root viewed the eight unique shortlisted native images once each, in declared
order, without crops, generated detail or new enhancements. The
[complete observations](root-observations.md) retain the scores-known, nonblind
review status. The known sign/building/corner/overhang arrangement is recovered
at Clip 7 index 564. Clip 3 candidates recover the local facade/grid arrangement
while their bright and veiled outlines change. No unique fine transient pattern
was established against either report still.

The shortlist also contains failures of visual usefulness. Clip 7 index 0 is
strongly impaired street/vehicle-like content, not a recovered reference 142
scene; index 282 is a tight, veiled, context-poor crop. A top-two rule produces
runners-up even when they are poor candidates. They were inspected and retained,
not silently presented as positive matches or removed to improve the result.
No new independent human or second-reader acceptance of these candidates is
claimed; the separate reviewer audited the method and reference masks.

## Coverage and verification

Each run tested all 108 declared combinations: 18 previously extracted frames,
two references and three representations, including 54 paired and 54 cross-view
comparisons. Those are only 18 distinct candidate frames from 1317 inventoried
in Clips 3 and 7; 1299 were not scored. This is the implementation pilot, not
the planned full-frame search. No new media was acquired or decoded.

Fresh controls passed: 11 inherited registration checks, 16 independent direct
arithmetic controls, 73 producer/oracle comparison checks, and 25 new adapter
tests. Root read the adapter/tests and reran all 25. The new tests include all
39 parity/scale cases showing excluded native bottom-quarter changes do not
alter any admitted working or scaled pixel. The 108-combination synthetic
wiring test uses mocked scores; it is not historical matching validation.

Both historical runs completed: about 41.55 and 41.86 seconds, within their
240-second cap, each approximately 21.5 MB before its terminal receipt and
below 256 MiB. The independent artifact audit checks complete coverage,
rankings, groups, input hashes and repeat products; its report is linked from
the execution record. Root separately reconstructed each of the 216 retained
transforms without importing the matcher and directly recalculated 347 finite
scores plus 85 unavailable-score decisions. Maximum observed score difference
was 6.49e-13, below the declared verification tolerance 1e-9. This selected-score
check shares Pillow/NumPy and does not recompute all FFT surfaces or authenticate
historical recording custody. Actual commands and limits are in
[the execution record](execution.md).

## Interpretation and next test

The strongest alternative to exact identity is straightforward: stationary
architecture can match over many frames while changing imagery is obscured,
cropped, differently processed or too similar to identify one exposure. The
pilot demonstrates that limitation rather than resolving it. Both report
captions acknowledge intensity adjustments; the full processing history and
original-camera lineage are not supplied by a high correlation. No inference
of fabrication, harmlessness or intent is warranted from that gap.

The next discriminating task is the declared all-frame comparison over the
same two sources, with the same frozen regions and scoring rule and a separately
reviewed finite extraction/storage schedule. Preserve missing dynamic coverage,
cross-view controls, ties and boundary winners. Do not tune the masks to make
one frame win. Even an eventual exact-image correspondence would establish only
a source relationship; field timing, absolute chronology, glass state and
interior temperature would require their own evidence and human checks.

Claim strength: the calculated scores/ranks are directly reproducible within
this procedure; scene associations remain bounded descriptive inferences.
Exact exposure remains underdetermined. Neither favorable matching nor failure
under this limited transform family is evidence for a collapse mechanism.
The full investigation remains active and incomplete; no accepted Sherlock/
Faraday finding, matrix save, legal promotion, disclosure, staging, commit or
push occurred.

The [separate synthesis critique](synthesis-review.md) found no outstanding
material correction after the dynamic-ranking label was clarified. Its
additional static-coverage caveat is included above. The critique does not
substitute for human acceptance or a second independent historical source.
