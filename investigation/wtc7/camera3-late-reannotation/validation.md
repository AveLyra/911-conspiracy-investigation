# Dense late-annotation validation and handoff

Research-only, 2026-09-12. The broad investigation remains active and
incomplete. This unit changes the evidentiary assessment of the saved-track
difference; it does not complete WP2, calibrate physical motion or identify
a collapse mechanism. The charter still controls scope.

## Workspace and authority

All new files and navigation edits are in the isolated sparse worktree
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, base
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. Changes remain intentionally
uncommitted alongside earlier investigation work. Original sources remain
read-only dependencies in `/Users/admin/docs/911`; the sparse checkout is
not self-contained. No merge, commit, push, source alteration, legal drafting,
canonical fact promotion, transmission or accepted Sherlock finding occurred.

The initial new protocol was frozen before dense-image generation and
annotation. The separate joint addendum was declared after the first
results/review, before the joint computation; prior-result familiarity and
preliminary hand-inspection were disclosed. Earlier protocols, observations,
fit results and reviews were not rewritten into retrospective agreement.

## Actual image and source work

The complete source decode used the prior pinned no-seek grayscale command.
The 1,350,045-byte WMV SHA-256 remains
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
All 442 frame hashes and the complete 152,755,200-byte raw stream match the
prior diagnostic map (raw SHA-256
`1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`).
The decode exited 0 and retains three corruption-warning mentions; raw stderr
was not exported. Diagnostic identity is not clean/source-clock certification.

Each image observer actually viewed all 22 native frames, all 22 target
crops and seven reference displays. Indices are258 and288..348 step3.
The reference implementer separately viewed the seven reference displays.
No new PDF pages, architectural drawing or hidden interior were inspected.
Only 22 of 442 decoded frames received new full-frame visual review here.

All 51 product file hashes/sizes agree. The reference implementer's separate
NumPy slice/repeat check reproduced every image-interior value of all 28
enlarged crops: 36,447,552 RGB values. This does not add visual coverage or
physical resolution. Root read the full preparation code and method review.
The factor 3 target rulers address exact integer pixel centers. Factor 8
reference rulers use a floor-center tick, half a display pixel from the
geometric center; their pixels remain inside the correct source block.

## Frozen annotations and fit results

The two new JSON/Markdown tables were frozen before comparison. Root knew
prior results; the separate observer did not consult old arrays/results or
root labels before its freeze. Both use the same public-copy images and
specified feature definitions. This is not human, licensed-expert or
independent-source validation.

All 207 declared fit dispositions are retained: 187 computed and 20 uncomputed
for missing B localization. Every computed window contains linear and
quadratic coefficients/residuals and exact specified perturbation semantics.
No unlocalizable point was filled. Saved point envelopes remain unknown/null.
Both independent visual narratives, including B342/345 and R3/21 disagreement,
remain unchanged. No consensus track replaces them.

The exact-rational verifier was independently implemented without reading
or importing the producer first. Root then read its entire 437-line source
and reran it successfully. The two receipts are identical except command.
Coverage: 935 coefficients, 4,070 residuals, 2,035 weights, 236 interval endpoints,
44 comparison rows and284 source decimal fields. Maximum acceleration error
is 3.257 × 10⁻12 px/s². Tolerances were declared before verification, not enlarged
after results. Source gates, own synthetic checks and retained positive
control data are detailed in [independent-fit-review.md](independent-fit-review.md).

## Reference and joint-feasibility reproduction

The reference producer computes 132 rows and all 22,308 real NCC candidates;
14 full synthetic fixtures supply 2,366 additional scores. Root read its
entire 291-line source and independently recomputed the scores using raw
moments/math.fsum instead of centered-product arrays. Every selected offset,
gate and 44 translation groups agree. Maximum correlation error 4.441 × 10⁻16;
maximum standard-deviation error 2.843 × 10⁻14. Zero integer vertical optima
do not imply exact camera stationarity or a sub-half-pixel uncertainty bound.

The joint producer uses exact Fractions. Root read its complete source and
independently checked original-box inequalities on a quarter-pixel integer
lattice, importing no producer. All 6 scenarios, 115 witness rows and 304
original observer-box memberships pass exactly. All 5 full synthetic groups
(7 control solutions, including rejection/touching cases) pass. This verifier
is intentionally scoped to the current rational lattice; it is not a
general-purpose interval package certification. Witnesses are mathematical
countermodels, not annotations, interpolated footage or physical simulations.

## Commands and runtime

From the isolated worktree, using
`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/shims/python3` (Python 3.13.7;
NumPy 2.3.4 / Pillow 12.0.0 where used):

```text
research/sherlock-wtc7-investigation/camera3-late-reannotation/prepare.py --out views01
research/sherlock-wtc7-investigation/camera3-late-reannotation/reference_diagnostic.py --out reference01
research/sherlock-wtc7-investigation/camera3-late-reannotation/analyze.py --out analysis01
research/sherlock-wtc7-investigation/camera3-late-reannotation/verify_reference.py --out root-reference-verification01.json
research/sherlock-wtc7-investigation/camera3-late-reannotation/verify_fits.py --output independent-fit-root01.json
research/sherlock-wtc7-investigation/camera3-late-reannotation/verify_joint.py --out joint-root-verification01.json
```

All listed executions ended with exit 0. The independent fit checker also
executed with its default output name under Python 3.13.7. The independent
observer's integrity check and joint producer used Python 3.14.0; that
producer's exact command/receipt are in [joint-review.md](joint-review.md).
Source/input/code/product pins and before/after equality are retained in
the corresponding receipts. Existing outputs must not be overwritten for
another run; no archival execution handle is currently live.

## Failures, omissions and review disposition

- The independent image-hash check initially assumed a `files` receipt key;
  it failed before checking products. The corrected `products` check passed.
- The joint producer's first sandboxed attempt failed at directory creation,
  before outputs or scientific calculations. Scoped escalation then succeeded.
  Existing-output refusal subsequently returned 2 with unchanged output hashes.
- The reference producer also refused an existing output with exit 2 and
  unchanged hashes. No failing reference was removed after scoring.
- Some exceptional preparation failures would not produce a durable receipt;
  no such failure is claimed for the completed preparation. The ruler defect
  above is retained; no generated images were silently repaired.
- Two fit rejection fixtures preserve reason labels, not attempted arrays.
  The independently inspected source defines the attempts; analogous tests
  are not represented as a full replay of those producer attempts.
- Four unlocalizable B comparison entries omit their still-known x/dx fields.
  The independent review supplies those source-pinned x differences separately
  without filling y or rewriting the frozen comparison output.
- Several root report/navigation patch attempts failed before mutation
  (context mismatch or wrong path); corrected edits succeeded. They were
  not scientific runs.
- Interpretation review required explicit absence of a full 21-point B/A−B
  fit and the distinction between unknown physical inequality and unsupported
  proof. The report incorporates both. The joint-feasibility concern received
  a new declared calculation and independent check, not a prose assertion.

The repository's `tools/validate_record.py --strict` was run read-only from
main and exited 0: headers, issue↔fact links and citation tags. It does not
validate these scientific results or mean new case facts were promoted.
Scoped link/syntax/whitespace results and final report-review identity are
recorded at closeout below.

## Durable next action

Use the existing STATUS.md handoff, not another charter. The dark upper-facade
band's right corner is a specific second-feature candidate visible in the
already reviewed images. Its material correspondence and geometry need a
new baseline preflight/source join; do not force B through smoke or claim a
new physical scale. Structural/member-map work on the available supplementary
inputs and the other charter workstreams remain open. None of this clears
the held packet or authorizes a solver run, Faraday execution, private
transfer or legal promotion.

Generic measurement/interval/failure lessons were deduplicated under
SFB-002/SFB-004. They remain local and pending while the designated Sherlock
task is archived and the user's routing decision is unresolved; no new
delivery, acknowledgment or fix is claimed.

## Final closeout

The complete [final report review](final-report-review.md) found no material
correction outstanding at report SHA-256
`af93973ab00ed333efafbbc4ecb3389522252b317f72880f7423b213a0c6bf61`.
The review SHA-256 is
`08bfa9651649de5cad640308cac90623e32699203f210ad76831010bac7c5dfc`.
Root read the entire final review and rechecked both pins; the report was
not changed after that review. This is scoped report-to-evidence review,
not another source, physical validation or independent joint reproduction.

Final local checks passed for 12 Markdown files and 38 local links, the
conflict/trailing-space scan, all seven Python syntax trees and five final
report/review/protocol/annotation pins. The tracked navigation edits pass
`git diff --check`. These checks do not audit unrelated working-tree changes.
Main acquired concurrent case-document and instruction edits during this
unit. Root reread the current AGENTS.md; the unrelated case drafts were not
reviewed or changed, and nothing was staged or transmitted.

No calculation process remains live. The investigation's next substantive
test and all uncommitted state are recorded in the existing STATUS.md.
