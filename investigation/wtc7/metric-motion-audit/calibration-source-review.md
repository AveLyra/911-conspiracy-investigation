# Saved Camera 3 tape: public calibration-source review

September 12, 2026. Separately authored computational AI source review; not human or expert certification. The [protocol](PROTOCOL.md), [charter](../CHARTER.md) and repository preservation/privacy rules control. This is a new, bounded supplement to [clock-source-review.md](clock-source-review.md); that earlier review's zero-new-PDF-page coverage remains an accurate historical record and is not rewritten.

## Result

The six inspected pages establish a stated **floor-to-floor calibration method** and a table of floor elevations. They do **not identify the architectural endpoints of the saved 58.293 m TapeMeasure**. No page specifies that saved value, selects its two numbered floors, or shows its endpoints in a labeled image or drawing.

There is affirmative numerical support for a floor-spacing origin: using the lab's stated conversion, **58.293 m = 191.25 ft exactly = 15 x 12.75 ft**. At the printed table precision, seven distinct floor pairs have that separation: 24-39, 25-40, 26-41, 27-42, 28-43, 29-44 and 30-45. The number alone therefore cannot select an endpoint pair. This does not show that the tape is wrong; it shows that its floor identities are not recoverable from these pages and that scalar agreement is not an endpoint identification.

## Actual source coverage

All source files below were read only under `/Users/admin/docs/911`. The new note is the only authored artifact and is in the investigation checkout, whose branch was verified as `research/sherlock-wtc7-investigation`.

- Visually inspected **all six complete existing page PNGs**, at their original supplied 935 x 1210 presentation: floor-spacing page 1 and Lab-Instructions pages 1, 2, 3, 4 and 5. No crops, overlays, generated images, new rendering or video images were used.
- Read the floor PDF's complete one-page extracted text to check the visually read table; parsed all 48 floor/Roof rows and tested all 1,128 unordered row pairs. Opened both PDFs with `pypdf` to confirm their page counts: one and five.
- Read the complete `reading-products.json` manifest, rehashed both PDFs and all six PNGs, and confirmed all **eight source/derivative hash comparisons pass**. The manifest describes these PNGs as prior 110-dpi Poppler reading derivatives; this pass verifies identity against that manifest, not a newly reproduced rendering.
- Read the complete sanitized `saved-tracker-settings.json`, the current source review, full protocol and charter. Did not open the original TRK, its personal path fields, application, video, historical point data, any model/case materials, agency-production contents, held packet, or external link.
- No new historical measurement, decoding, matching, acceleration fit, source retrieval, bridge use, canonical promotion, commit or external transmission. This is not a clean holdout: the saved calibration and earlier case imagery were already familiar; no prior image observation is relabeled as new viewing.

## What the pages actually supply

The floor PDF is headed *Elevations of Floors of WTC 7*. Its columns give incremental from/to-floor spacing in feet/inches and decimal feet, plus each floor's overall height and elevation in feet. It lists floors 1 through 47 and a Roof row. Its title is a floor-elevation attribution, not a labeled architectural drawing. This exact page has no cited drawing number, source reference, datum explanation, or diagram connecting its rows to video features.

The Roof row gives overall height 612.083 ft and elevation 921.333 ft. The table does not call that row a parapet top, window top, or particular visible roof outline. Across all 48 printed rows, elevation minus overall height is 309.250 ft; that internal consistency does not establish a physical datum independently. The table also explicitly contains nonuniform intervals, including 14 ft 3 in from 45 to 46, 14 ft 10 in from 47 to Roof, and 14 ft 9 in for each interval from 21 through 24. A uniform-floor assumption for the entire building would contradict the sheet.

| Lab physical page | Complete-page observation relevant to this check |
|---|---|
| 1 | Introduction and interpretive claims about the collapses. No tape value, selected floor pair, dimensional drawing or endpoint illustration. Those interpretive claims are not adopted as findings here. |
| 2 | Describes kit example files and footage, suggests a stationary neighboring-building point for camera-motion checks, associates visible window rows with floors, and warns that floor spacing varies. It does not identify which row boundary or which floors the saved Camera 3 tape uses. |
| 3 | Specifies Camera 3 as 15 fps and a three-frame step as a nominal 0.2 s example. Directs rotating axes to a vertical building edge; choosing two reasonably separated floors; obtaining their separation from the supplied documents; converting feet to metres by 0.3048; placing a calibration stick/tape at those floors aligned with the vertical coordinate axis; and assigning the real-world distance. It names no fixed pair or saved 58.293 m value. |
| 4 | Explains velocity-graph regression, gravity comparison and interpretation questions; links the kit and Tracker. No additional floor/end-point assignment. No claim in these interpretive instructions supplies an independent calibration. |
| 5 | Further interpretation/follow-up questions and references to other material. No saved-tape endpoint identification. Those linked materials were not followed in this task. |

These are primary records of what the public lab supplies and instructs. The floor sheet is not, by itself, an authenticated original architectural drawing or an independent second measurement of the building. That provenance limit does not make its concrete dimensional entries unusable as explicitly attributed, conditional inputs.

## Exact conversion and non-unique pairs

Using the printed conversion factor as an exact decimal:

`(58293/1000) / (3048/10000) = 765/4 ft = 191.25 ft = 191 ft 3 in`.

Also, `15 x 12.750 ft = 191.250 ft`, and `191.250 x 0.3048 = 58.293 m` exactly. No rounding tolerance was used to select matches.

| Lower floor | Upper floor | Lower overall height, ft | Upper overall height, ft | Difference, ft |
|---|---|---:|---:|---:|
| 24 | 39 | 302.500 | 493.750 | 191.250 |
| 25 | 40 | 315.250 | 506.500 | 191.250 |
| 26 | 41 | 328.000 | 519.250 | 191.250 |
| 27 | 42 | 340.750 | 532.000 | 191.250 |
| 28 | 43 | 353.500 | 544.750 | 191.250 |
| 29 | 44 | 366.250 | 557.500 | 191.250 |
| 30 | 45 | 379.000 | 570.250 | 191.250 |

All seven are fifteen **intervals**, not a claim that fifteen visible rows or a particular number of failed stories has been identified. Enumeration included the Roof row; no Roof-to-listed-floor pair equals this length at the printed precision. This is table arithmetic, not a disproof of a tape placed on two other architectural features with that length. The feet/inches column's 14 ft 10 in is printed as 14.833 ft; the exact-match enumeration uses the printed overall-height/elevation values, and does not treat three-decimal rounding as survey accuracy.

The saved sanitized record provides endpoints (414.3770672546858, 196.24035281146615) and (416.95700110253586, 390.7276736493937), an assigned length 58.293 and unit `m`. Those image coordinates contain no architectural labels. The previous source review separately established their internal consistency with the saved pixel scale; this pass did not repeat that distance calculation or inspect the corresponding video features.

In particular, a visible window-row top is not automatically a floor slab elevation, and the table's Roof is not automatically a parapet/roof-outline point. Equal vertical offsets at two corresponding window features might cancel, but neither that equality nor the selected features are established by these six pages. Projection, depth and source-raster relationships also remain separate dependencies. Square/non-square-pixel differences alone would not demonstrate a major vertical-scale error, especially for a nearly vertical same-image tape; no historical rescale is invented here.

## Claim ledger and finite disposition

| Claim | Layer / strength | Support, alternative and discriminator |
|---|---|---|
| The lab prescribes a floor-based metric calibration. | Observed document content; A for what is written. | Lab page 3 explicitly supplies the procedure and conversion. This establishes the instruction, not faithful execution in a particular saved project. |
| The assigned tape length is compatible with fifteen regular 12.75-ft floor intervals. | Exact derived arithmetic; A for the equality, C for the physical interpretation. | Seven exact table pairs support compatibility. A different feature pair or method could give the same scalar; the saved choice is not established by equality. |
| These six pages uniquely identify the saved tape's architectural endpoints. | Not established; D for historical attribution. | No selected floor pair or labeled endpoint image appears; seven table matches defeat uniqueness from length alone. A project-linked annotation naming the two architectural features and their dimensional source could resolve this. |
| The calibration is demonstrated wrong, or all conditional metric inference is unusable. | Unsupported by this check. | The pages provide a coherent method and compatible dimensions. Endpoint and geometry assumptions can be stated and tested without turning their present uncertainty into a measured error. |
| This Camera 3 calibration validates Camera 2 target scale or a collapse mechanism. | Unsupported transfer / out of scope. | Neither cross-view correspondence nor mechanism-discriminating observations are supplied by these pages. No physical or causal ranking changes. |

The finite answer is therefore **method and candidate separation supported; exact endpoint assignment unresolved within complete six-page coverage**. The concrete unresolved dependency is a source-linked identification of both tape endpoints in the referenced image, including whether the chosen observable is a floor elevation, corresponding window feature, parapet or other outline, and the dimensional/projection justification for that pair. This is a next-test description, not authorization for a further pipeline or restricted-material access.

## Exact pins and execution

All paths in the next table are relative to this read-only root:

`/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/`

| Path | Bytes | SHA-256 |
|---|---:|---|
| `reading-products.json` | 3793 | `35b0364fdbac5c8806c06e33fd67cd99b4a63064f440f8b57e1a0db8fb63cbba` |
| `kit-inventory/run-v1/outer/Lab-Instructions.pdf` | 55206 | `c3a9c7aa44f914dbcc7dd2e5604020db0466de8c27f9d71f70d485b80aeb5557` |
| `lab-pages/instructions-1.png` | 311518 | `5d9ddb41adf68b7c9ae2f4f08bd4816b439c649f3fcf516b3c8ae60f5b6d8b7b` |
| `lab-pages/instructions-2.png` | 270299 | `db158bee98576c0c0093a6804fc2ae72397c932dbd8fe89d6f8b15a5594e11e7` |
| `lab-pages/instructions-3.png` | 311040 | `02e3725cc4cc45cc33823835783accf8d665b2cc090775a0fbfc5f6700bf2626` |
| `lab-pages/instructions-4.png` | 277093 | `cca9412ec74f92f9c61a7b3dfabf4ed96d025d052bd6a52e548126752d1a916f` |
| `lab-pages/instructions-5.png` | 199234 | `507e2e4698ee8561845d21a99c32cdbcb535aac784330f399557de8f1221c221` |
| `kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/WTC7 Floor Spacing.pdf` | 32383 | `8dacd6cbb61b554c21da2cfa6447ebbb3248a06d04a44596b5c31088e5beb411` |
| `lab-pages/floor-spacing-1.png` | 182810 | `abb9750ad4d9d7370e02701d9c5764570c816480a1d38d091927fc52e69af6ff` |
| `kit-inventory/run-v1/saved-tracker-settings.json` | 13039 | `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb` |

Worktree control/source-review pins, relative to `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/`:

- `CHARTER.md`: `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
- `metric-motion-audit/PROTOCOL.md`: `2ef59293a4e7994929964878ace70cef3569b4b689008e7ef85c66dc1e00e800`.
- `metric-motion-audit/clock-source-review.md`: `4cdbcb768dfe9d70c3638f1903139c387ff2f325e8eaf4c6ed40e3274821f08c`.

Actual read-only calculation runtime: Python **3.12.14**, `pypdf` **6.10.0**, executable `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. The hash/page-count check and enumeration both exited 0. No temporary script or output file was created. The narrow arithmetic is reproducible with:

```python
from fractions import Fraction as F
from itertools import combinations
from pypdf import PdfReader

path = ('/Users/admin/docs/911/research/sherlock-wtc7-investigation/'
        'camera3-provenance/kit-inventory/run-v1/outer/The Kit/'
        'WTC7-Camera 3/WTC7 Floor Spacing.pdf')
labels = {'Roof', *(str(i) for i in range(1, 48))}
rows = []
for line in PdfReader(path).pages[0].extract_text().splitlines():
    fields = line.split()
    if len(fields) >= 4 and fields[-3] in labels:
        rows.append((fields[-3], F(fields[-2]), F(fields[-1])))
assert len(rows) == len({r[0] for r in rows}) == 48
assert {e-h for _, h, e in rows} == {F('309.250')}
feet = F('58.293') / F('0.3048')
pairs = [(a[0], b[0]) for a, b in combinations(rows, 2)
         if abs(a[1]-b[1]) == feet]
assert feet == F('191.25') == 15*F('12.750')
assert len(pairs) == 7
print(feet, pairs)
```

The embedded code above was extracted from the authored Markdown and executed read-only with the same runtime; it exited 0 and returned 765/4 ft and the same seven pairs (upper/lower order in its output). All eight PDF/page hashes were also rechecked after authorship and still match. The initial combined instruction/source read exceeded the tool's aggregate display budget; the full protocol, charter and current source review were subsequently read individually. No truncated output was counted as complete. The evidence skill prompted the distinction between scalar compatibility and endpoint identification; the PDF skill required complete-page visual coverage; the source-of-truth skill kept this exploratory supplement separate from preserved sources and frozen prior results. No authority boundary changed.
