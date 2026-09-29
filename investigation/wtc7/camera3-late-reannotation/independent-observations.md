# Independent Camera 3 late-window image observations

Frozen computational-observer table, 2026-09-12. Working/exploratory research;
not a human or expert annotation, physical acceleration measurement, cause
finding, or source-authenticity determination.

I read the current main-checkout AGENTS.md, this worktree's WORKFLOW.md,
START-HERE.md and investigation CHARTER.md, and the complete new PROTOCOL.md.
The evidence-falsification-auditor and source-of-truth-guardian skills informed
the distinction between image observations, derived coordinates, material
identity and subsequent inference. No authority boundary was crossed.

Before freezing these files I did not read saved coordinate arrays, trajectory
fits, the root observer's annotations, or prior reports. Shared task instructions
and the new protocol supplied feature definitions, sampling, and source context.
This is independent annotation of shared images, not independent source evidence
or an independently blinded historical holdout. Numerical comparison must occur
after this freeze and must preserve this table.

## Coverage and integrity

I individually viewed all 22 native frame PNGs and all 22 target crop PNGs in
`views01`: frame 258, then 288 through 348 inclusive in steps of 3. I also viewed
`reference-baseline.png` and both 21/31 patches for R1, R2 and R3 (seven reference
displays), so all 51 receipt-listed image products were visually inspected.
Target crops 258, 288, 339 and 342 were reviewed again before freezing, to check
the edge reading and the late smoke boundary. Intervening unsaved video frames
were not inspected, and no video was decoded in this subtask.

A read-only Python 3.14.0 check loaded `views01/receipt.json` and compared each
of its 51 `products` against both its byte count and SHA-256. All 51 matched;
there were no failures. An initial check tried the wrong receipt key (`files`)
and stopped with KeyError; the corrected check used `products` and completed.
This verifies agreement with this receipt, not historical authenticity or an
independent reconstruction of the source-to-image transform.

- Protocol SHA-256: `7b13e006ab382121452f6e7c59f37d7f586b57f297a7e1c7154b86b2aae06c2f`.
- Receipt SHA-256: `8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161`.
- Branch verified: `research/sherlock-wtc7-investigation`.
- Images: native 720 by 480; target crop [295,125,535,375), nearest-neighbor factor 3.
- Rulers are outside the image and identify native integer pixel centers.

Reproducible integrity command, run from the investigation worktree:

```sh
python3 -c 'import json,hashlib,pathlib; p=pathlib.Path("research/sherlock-wtc7-investigation/camera3-late-reannotation/views01"); r=json.loads((p/"receipt.json").read_text()); entries=r["products"]; failures=[x["name"] for x in entries if hashlib.sha256((p/x["name"]).read_bytes()).hexdigest()!=x["sha256"] or (p/x["name"]).stat().st_size!=x["bytes"]]; print("Checked entries:",len(entries)); print("Failures:",failures); print("Receipt SHA256:",hashlib.sha256((p/"receipt.json").read_bytes()).hexdigest())'
```

## Frozen annotation table

Every number is an integer native-image coordinate. Bounds are inclusive
subjective localization judgments, not calibrated probabilities or confidence
intervals. Visual confidence terms describe edge legibility only. A is the
geometric top/right facade intersection; its recognizable shape is not proof
of an invariant physical material point. B samples the main upper silhouette
at fixed x=322; no distinctive persistent material marker was identified at
B in any inspected frame. The JSON contains the full frame-specific notes.

| Frame | A x | A y | A x bounds | A y bounds | B y | B y bounds |
|---:|---:|---:|---|---|---:|---|
| 258 | 513 | 139 | 512–514 | 137–141 | 167 | 165–169 |
| 288 | 513 | 139 | 512–514 | 137–141 | 168 | 166–170 |
| 291 | 513 | 139 | 512–514 | 137–141 | 168 | 166–170 |
| 294 | 513 | 139 | 512–514 | 137–141 | 169 | 167–171 |
| 297 | 513 | 140 | 512–514 | 138–142 | 171 | 169–173 |
| 300 | 512 | 140 | 511–514 | 138–142 | 173 | 171–175 |
| 303 | 512 | 142 | 511–514 | 140–144 | 175 | 173–177 |
| 306 | 511 | 146 | 510–513 | 144–148 | 179 | 177–181 |
| 309 | 511 | 151 | 510–513 | 149–153 | 184 | 182–186 |
| 312 | 510 | 156 | 509–512 | 154–158 | 190 | 188–192 |
| 315 | 510 | 165 | 509–512 | 163–167 | 198 | 196–200 |
| 318 | 510 | 174 | 508–512 | 172–176 | 208 | 206–210 |
| 321 | 510 | 185 | 508–512 | 183–187 | 218 | 215–221 |
| 324 | 510 | 197 | 508–512 | 195–199 | 231 | 228–234 |
| 327 | 510 | 210 | 508–512 | 208–212 | 243 | 240–246 |
| 330 | 510 | 224 | 508–512 | 222–226 | 257 | 254–260 |
| 333 | 510 | 240 | 508–512 | 238–242 | 272 | 269–275 |
| 336 | 511 | 257 | 509–513 | 255–259 | 287 | 283–291 |
| 339 | 512 | 275 | 510–514 | 273–277 | 304 | 299–309 |
| 342 | 514 | 294 | 512–516 | 292–296 | null | unlocalizable |
| 345 | 516 | 314 | 514–518 | 312–317 | null | unlocalizable |
| 348 | 518 | 334 | 516–520 | 332–337 | null | unlocalizable |

A is localized in 22/22 frames; B in 19/22. Within the 21 late marks alone,
A is localized in 21/21 and B in 18/21. The final three B positions are
unlocalizable, not zero and not missing-at-random. They must not be filled by
interpolation or inferred from the clearer right contour. No fit is supplied.

The upper outline changes from a stepped roof arrangement toward a much
smoother/sloped right portion and a flatter left portion. Pixel-scale steps
become more conspicuous later. Those observations do not resolve how much of
the apparent shape change is physical, projection-related, or source encoding.
Smoke increasingly obscures the left rim; B339 is marginal and intentionally
has a broad envelope. At B342 and later I could not distinguish the direct
main-rim border without extending a neighboring contour, so I supplied null.
Foreground structures hide an increasing amount of the facade. A348 remains
a small visible lip with reduced placement confidence. No conclusion about
physical cause, gravity compatibility, support loss, intent or mechanism follows.

## Separate stationary-reference visual preflight

These are independent baseline-only judgments made without scoring or seeing
correlation results. An accepted association permits a diagnostic attempt;
it does not certify stationarity, unique later matching, calibration or an
uncertainty bound. The exact protocol reference centers were supplied to this
observer and are not independent coordinate estimates.

| Reference | 21 patch | 31 patch | Baseline visual basis and limits |
|---|---|---|---|
| R1 (272,400) | Accept for diagnostic scoring | Accept for diagnostic scoring | Both patches contain the streetlamp cluster and its asymmetric dark/light structure. Some bright areas are saturated/soft; the larger patch adds the boundary against the facade. A lamp center is not independently localized here. |
| R2 (168,348) | Accept for diagnostic scoring | Accept for diagnostic scoring | Window/sill junction and dark/light boundaries are visible. The larger patch adds adjacent window geometry. Repeated windows create possible aliases that scoring must retain. |
| R3 (673,292) | Reject on visual preflight | Accept provisionally for diagnostic scoring | The small patch is diffuse pale masonry with insufficiently distinctive visual identity. The larger patch adds a left silhouette/edge segment and broader masonry structure, allowing a tentative texture association. It remains soft and potentially repetitive; a matching or contrast screen may still fail. |

This observer would not score R3's 21 patch. Preserve any difference from
another observer's preflight as a disagreement rather than silently replacing
these decisions. No reference scores or camera translation estimates were
computed in this subtask.

Only this Markdown and its JSON counterpart were written. Source images,
receipts, protocols, prior analyses, canonical records, and main were untouched.
