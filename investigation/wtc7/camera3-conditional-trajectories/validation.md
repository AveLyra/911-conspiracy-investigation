# Conditional-trajectory validation and execution

Research-only unit in `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`,
branch `research/sherlock-wtc7-investigation`, base
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. Previous source/media/metric
units remain frozen. The preceding goal turn made progress by closing the
endpoint/repetition review; this unit now reconstructs actual saved-point
trajectories rather than repeating a generic calibration gate.

## Prospective choices and actual reading

[PROTOCOL.md](PROTOCOL.md), SHA-256
`d7fd79c3269155a06225346273aab4a6352c14c233beda4fa88989d244d3ec01`,
fixed ordinal tracks, all71 indices, eight view selections, both clocks,
six geometry scenarios, all241 windows per track/clock, three polynomial
degrees, perturbation sensitivities, control cases and tolerances before
the numeric coordinate export and historical fitting. Source settings and
prior endpoint observations were already known; this was not blind.
The separate [method review](methods-review.md) was completed before that
reviewer inspected point arrays or fits. No criterion was tuned toward g.

Root read the current charter, control/navigation/handoff, complete sanitized
settings, clock/source review and tagged clock-semantics report. New primary
software reading: PointMass2840–2865,2900–2932,3350–3400 for numeric source
fields, ImageCoordSystem1128–1148 for the inverse transform; later
PointMass1174–1315 and2933–2960 for the declared keyframe follow-up. These
are finite source ranges, not a whole-program or original-binary audit.
No new PDF pages, model-production contents or held packet were inspected.

## Extraction and diagnostic images

Observed successful command, exit0:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-conditional-trajectories/extract_points.py --out extraction01
```

The known-hash public project was parsed as inert, size-bounded XML with
DTD/entity rejection. Export was limited to the two ordinal PointMass
arrays' numeric indices/x/y literals, approved numeric configuration, and
current diagnostic clock rows. No arbitrary source strings, original track
names, private paths, comments or raw XML were displayed or written.
One positive allowlist fixture and six negative extraction fixtures passed.
The [extraction receipt](extraction01/receipt.json) preserves five before/
after pins and both71-point counts. Exact numeric export SHA-256:
`f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3`.

Observed successful command, original live exec40431 completed with exit0:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-conditional-trajectories/prepare_views.py --out views01
```

The source WMV SHA-256 is
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
Pinned FFmpeg's exact old default command decoded from the beginning. All
442 frame hashes and the152,755,200-byte grayscale stream matched the old
diagnostic; raw SHA-256
`1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`.
Raw data were held in memory, not retained again. Diagnostics remained
unexported except size/hash and three corruption-warning mentions. No new
warning localization or clean-media certification is claimed.

Eight unmarked720×480 grayscale PNGs and eight separate RGB saved-query
overlays were preserved, plus the [view receipt](views01/receipt.json).
Root and the separate observer each viewed all16 displays from **eight
distinct source frames**, then froze notes before comparing descriptions
or reading fitted acceleration values. Root note SHA-256:
`be801a615f9e2b43dda8ce28a6b92909d7366a386e53a44edea5fa55e9dfcedd`;
separate observation SHA-256:
`622ddc4475bdea35891bbf3781ec0718f81fd80d064fa2fc9dd5abbf3f6944c0`.
This is8/71 saved marks per track, not full pointwise validation or human
spot-check. No retrospective clean holdout is claimed.

## Fits and independent reproduction

Observed successful command, original exec13825 completed with exit0:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-conditional-trajectories/fit_trajectories.py --out fit01
```

Python3.13.7/NumPy2.3.4 produced six files: controls, exact clock arrays,
all fits, transformed trajectories, summary and receipt. All12 producer
controls passed before historical fit values were loaded. All964 windows
succeeded. Every coefficient/residual, all six geometry variants and every
quadratic perturbation weight remain in the output; no best-g filter was
applied. The conventional gravity reference is not an input to the fits.
All71 distinct current-PTS/nominal saved-row times coincide exactly; that
agreement creates redundant scenarios, not independent clock evidence.

The independent [verifier](verify_trajectories.py), SHA-256
`710d196aba2600d102c7cb92d532d6a6e85aed6af633be8bcc199539e7b6efd0`,
does not import producer code. It independently parses numeric fields,
reconstructs overlay pixels, solves exact rational polynomial normal
equations, evaluates every residual and acceleration-response functional,
checks conditions by a separate Jacobi eigensolver, and uses high-precision
Taylor trigonometry for geometry conversion. Read the complete
[independent verification](independent-verification.md) for exact scope.

Independent coverage includes142 point pairs/284 literal coordinates,
11 configuration fields,304 clock rows, eight native frame identities and
all2,764,800 overlay pixels. It checks964 windows,5,784 scalar polynomial
fits,17,352 coefficients,67,464 residual scalars,11,244 response weights,
5,784 quadratic geometry cases and12 full geometry trajectories. Maximum
coefficient error is about1.121e−12, image-acceleration error3.492e−12 and
SSE error1.216e−11, inside the prospective1e−9/1e−8 tolerances. Nine exact
preparation groups and twelve analytic counterparts to producer controls
pass; producer flags do not retain all control intermediate arrays.

Root read all722 lines of the frozen verifier before rerunning it:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3 research/sherlock-wtc7-investigation/camera3-conditional-trajectories/verify_trajectories.py --fit-run fit01 --out independent-root01.json
```

Original exec11462 completed with **exit0, pass**. Root receipt SHA-256:
`30e78ffd3df7e6a624fd490fd6834fcfd3ed684ac45c6b8cd642a1ffd59ba9f4`.
Whole-JSON comparison with the reviewer's
`4d1ec768f50a46da08cd5768c90b4fa4b25cfba1d0e33cdf749fe0cbc82f86e7`
receipt confirmed every field identical except the command. This is a
rerun of the independent method, not a third method or a new source.

## Figure and keyframe follow-up

`plot_results.py` ran with original exec86678 completing exit0. The figure
retains10 series/622 samples:142 positions and480 nominal-clock sliding
window coefficients. Full-span fits remain in the data but are not plotted.
No chosen y limits hide extrema. Root viewed the full1500×1350 figure:
labels, legend, reference line and all three panels are readable, and the
plot distinguishes assigned positions from window accelerations. Its
generation receipt's “not yet visually reviewed” status is frozen generation
history; this paragraph records the later visual check. No browser/UI work.

The separate [keyframe addendum](KEYFRAME-ADDENDUM.md) was declared **after**
initial fits were inspected. The first indexed-int parser exited1 before
exporting values. Shape-only inspection identified braced integer-list
serialization; the declared bounded normalization then completed exit0
through the original yielded tool handle. All71 saved marks in each track
are explicit keys; no non-key marks or extra keys. The
[independent source review](keyframe-source-review.md), fully read by root,
reproduces the numeric membership and reconstructs the exact failed-checker
bytes. It does not prove manual annotation or absence of earlier processing.
The original protocol, point export and fitted results remain unchanged.

## Final report and figure review

The complete [numerical report review](report-numeric-review.md) checks all
displayed window, dimensional, residual and unit-response values against
independent calculations. It reconstructs all ten plotted series and all
622 samples field-for-field, verifying that every nominal sliding window
is included. Its [numeric receipt](report-numeric-receipt01.json) preserves
twelve unchanged input pins; SHA-256
`145fbca36cf3c2fcfff357a5f3e0bb89f31fcbd51c6ca648741e0352ab12ae89`.
Root read this complete review and its ledger-update confirmation. The
rounded sensitivity table is explicitly not an outward-rounded strict
bound; the final report now directs strict inequalities to the retained
full-precision weights.

The separate [interpretation review](final-interpretation-review.md), also
fully read by root, passes the full report and subsequently its five updated
claim-strength cells at report hash
`fcad554e3dedf1dc2cf1eb55a47223980ef0d8357630bf0b0587208cd5624df7`.
Review SHA-256:
`ede36e37b7292b0f5f3245d105264b9141868490f75d1e3ad9162b7ffc09997b`.
It credits conditional near-gravity support without converting it to a
whole-building or mechanism finding. It does not certify numerical products
or figure completeness from visual/source agreement.

The final report hash is
`c2e66e0bf2b9f43d71fced142445d2f65097ce06ea49059a53fe5114be49fb2d`.
Only the explicit rounding/strict-bound clarification differs from the
source-reviewed version; no number, selection or scientific result changed.
The numerical reviewer confirmed that exact final paragraph change and its
reversibility to the preceding report hash; root read the appended check.
Final numerical-review SHA-256:
`685010fefbbd08441d9ad0d9a25ae3b14a2aa3171aa8c48dfdd47d512db36b4b`.
Both bounded reviewers and all current execution handles are terminal.

Scoped integration checked **14 Markdown documents, 177 local-link
occurrences, six Python ASTs and nine explicitly frozen unit pins**, with
no issues. Of those link occurrences,104 resolve through the original
read-only repository because the investigation checkout is sparse; this
is not a self-contained-checkout claim. Direct whitespace/conflict-marker
checks included untracked new documents. The tracked navigation diff check
also passed. No canonical-record validator, browser validation or extra
historical reproduction is implied by these structural checks. Current
research remains uncommitted; the existing status/navigation and generic
local-only feedback were updated without source or authority promotion.

## Failures and preserved boundaries

An initial observer product checker expected a `path` field where the
receipt uses `name`; it failed before verification, then passed after a
schema-specific correction. The keyframe parser's first format rejection
is separately retained, not relabeled success. A read attempted before the
numeric review was saved found no file; the completed review was subsequently
read in full. Aborted patch-context matches made no changes. No numerical
historical-fit failure or new decode-identity failure occurred. Every live
producer/verifier handle above was resumed to an observed terminal result;
none was restarted merely because the first observation yielded.

This work grants no physical calibration, original exposure identity, human
approval, force/mass inference or cause ranking. No source modification,
new production/held-packet payload access, external retrieval/transfer,
Sherlock case import/accepted finding, Faraday execution, legal-record
promotion, filing, commit, merge or push. The full charter remains active
and incomplete. Source/evidence skills preserved positive near-gravity
support alongside calibration, tracking and fit-window limitations.
