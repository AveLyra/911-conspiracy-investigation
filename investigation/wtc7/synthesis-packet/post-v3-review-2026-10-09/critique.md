# Root-report critique

October 9, 2026. Bounded inference review by `/root/envelope_arithmetic`,
separate from the already-frozen [integrity review](integrity-review.md).
One precision correction was required and is verified below. No other material
correction was identified within the reviewed selection. This is not historical
corroboration, engineering endorsement, human acceptance or a cause finding.

## Reviewed versions and correction

The complete initial [report](report.md) was read at receipt `9b454e`, with
SHA256 `5711b9499abc9cb79eb86283911d4450a865a6005256a1bfacadff39598605a1`.
Its A03 consequence said, “This replaces the earlier zero-coverage status.”
That was too broad: the four earlier primary/primary, primary/peer,
peer/primary and peer/peer solid/dash combinations had respectively **0, 1,
0 and 1** selected segments, not four zeros. The structured check in
`1f8208`, recorded in the integrity review, supports that distinction.

The repaired A03 sentence is: “The two previously zero primary-dash
combinations become positive; each peer-dash combination retains its one prior
segment.” It accurately distinguishes the two newly positive combinations from
the two already positive combinations. The after counts remain 27, 25, 26 and
24; these are conditional graphical segments, not physical forces or energy.

The repaired report SHA256 is
`4010fa0f0ec71655e4da9b9746c03bd116a370bd78ce0e92faca5115912f7ba7`.
Receipt `fdbb31` verified the exact changed row and this hash using:

```sh
rg -n '^\| A03 |^Final integrity' report.md
shasum -a 256 report.md integrity-review.md
```

The integrity review remained
`1cb413c0c630c9356ba986b9422aff3d058ffe14746370ee3c0193eab118293e`.
A final full report read at `3cc8cf` confirmed the repaired wording. That
command's exit 1 came from checking the not-yet-created `critique.md` with
`ls`, not from a failed report read. No frozen reading or source was edited.

## Substantive coverage

The review covered [SCOPE](SCOPE.md), [inputs](inputs.json), all eleven selected
addition reports and all four baseline reports, plus the frozen opposed
reviews and their recorded hashes. The material index was hash-checked, not
re-adjudicated claim by claim. Opposed reviews were read only after the
integrity note was frozen; their two file hashes and sizes matched
`review-freezes.json` at `db0d50`. This confirms the saved artifacts, not an
independent observation of every reader's access history.

The synthesis retains the important contrary facts: reported preservation
concerns and incomplete questionnaire returns; unresolved control-letter
review; the published collapse/arrest contrast and surviving-capacity burden;
affirmative fire evidence; and user-reported bangs whose source and detection
comparability remain unresolved. Quiet-process compatibility is not promoted
to demonstrated capability or historical use. The conclusions do not confuse
a weakness in the exact NIST sequence with rejection of every fire pathway,
or an imposed support-removal state with its executed mechanism.

The report also correctly preserves the measurement and access ceilings:
positive F7 coverage is conditional on annotations; physical discrepancies
remain null; all 84 packet entries remain uninspected; no NBC media was
acquired; DNS failure supplied no HTTP content; and synthetic pointer results
do not establish historical trajectories or general human localization
accuracy. No new robust ranking, equal-odds conclusion, source-authentication
claim or authorized next execution is implied by the proposed discriminators.

## Limits and closeout boundary

No primary PDF, image, media, gated DEP substance or new source was reviewed in
this critique. There was no new retrieval, historical computation or expert
validation. Prior participation in F7 annotation/checker work and municipal
and Cather reviews makes this a disclosed shared-source computational review,
not a blind or historically independent assessment. The evidence-falsification
and source-of-truth skills informed these limits and the correction.

The report's final verification paragraph was still pending when reviewed;
root owns its closeout update and final link/pin checks. The integrity note's
nine-heading STATUS check records the pre-navigation state. A newly added
supplement header must be excluded by explicit bounds in any final replay;
the old command is not claimed to reproduce that count against changed STATUS.
