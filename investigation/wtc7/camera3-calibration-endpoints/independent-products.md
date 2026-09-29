# Independent product and coordinate review

Disposition: **pass for the six run01 PNGs' selected-pixel provenance and exact
crop mapping, with a presentation-label qualification**. This is a byte,
array and coordinate check, not image interpretation, a new source decode,
historical-exposure authentication or physical calibration.

The complete [protocol](PROTOCOL.md), SHA-256
`8c23c82af39edf6cc1ff6627e3c70e38728b599c830b41865ec457d3f7950981`,
and [prepare.py](prepare.py), SHA-256
`fb1a69aca54d0b945adbc4e8e620ddcc2b6adc3d3101465bd71748461db977e3`,
were read before checking the products. The evidence-audit,
development-verification and source-of-truth skills guide this review.
Only this review document was written; sources, code, receipts, images and
other analysts' observations were not edited or interpreted.

## Inputs and execution lineage actually checked

The [run01 receipt](run01/receipt.json) is 8,271 bytes, SHA-256
`8ae034a788f93a8c8c80704c4fe4b675105065be2a28567e9c4c21cf47a83219`.
The separate [initial pin list](run01/initial.json) is 1,958 bytes, SHA-256
`01ece30f675a270d2e4145f51b290af1900cf2c9554d39a3f15a518b1407ae33`.
The initial file, receipt initial list and receipt final list are exactly
equal. All **eight** current input files were independently rehashed before
and after the pixel checks and match those lists:

- Source and nested alias: each 1,350,045 bytes, SHA-256
  `48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
  These match the old diagnostic's `source_before` and `source_after`.
- FFmpeg executable: 421,968 bytes, SHA-256
  `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`;
  also agrees with the binary identity in the old diagnostic receipt.
- Old diagnostic receipt: 13,520 bytes, SHA-256
  `11bb4f4d44031621322b068648647f4e0c437f61510d3b4e6d380e8fc62cc227`.
- Old `default-frames.json`: 136,937 bytes, SHA-256
  `8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2`;
  also matches its product pin in that old receipt.
- Sanitized saved settings: 13,039 bytes, SHA-256
  `ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb`.
  Only its identity was checked; this pass did not parse original project XML
  or independently reconstruct the old application's configuration.
- The protocol and preparation code identified above.

The new recorded decode argv exactly equals the old `default` diagnostic
argv. The old map contains exactly 442 records and 442 pixel hashes. Its raw
count and the new receipt both describe 152,755,200 grayscale bytes, with raw
SHA-256 `1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`.
The new producer records subprocess return code zero and equality of all 442
fresh frame hashes to the old map. **This independent pass did not re-decode
the source or independently hash the unretained full fresh raw stream**; its
direct fresh-pixel validation covers the three retained selected frames below.
Do not describe that as a second full 442-frame decode.

The old receipt remains `diagnostic_complete_no_sequence_admitted`. Its
warning indices remain 37, 55 and 63; the three selected old records have no
warning-log association. The new receipt reports three warning mentions but
expressly makes no new warning-localization claim. No diagnostic text was
opened or exported. Neither old warning locality nor equal decoded bytes is
an independent certification of historical image quality or timing.

## All six PNGs checked

Every PNG was opened computationally, not visually interpreted. All three
native files are mode **L**, **720×480**, uint8. All three crop files are mode
**L**, **630×1035**, uint8. Every native and crop file's bytes match its receipt
pin. The output directory contains exactly the six PNGs, initial list and
receipt—eight files, with no failure artifact.

| Selected index | Diagnostic PTS × time base | Exact seconds | Native grayscale pixel SHA-256, matching old frame hash |
|---|---|---|---|
| 138 | 9200 × 1/1000 | 46/5 | `5c91a1376ac74ff0b015d13984ee6618f61ba37ebdb696136192d339b257e972` |
| 141 | 9400 × 1/1000 | 47/5 | `0fd466995d6160fff8281db29aac3f887ea425d25f7e01bf026d31bbcf105d09` |
| 168 | 11200 × 1/1000 | 56/5 | `fc3d6c167692d66dbaea5799e71504ce40f1ea1bab8fac039a2e3d4eb0870e53` |

The ordered selection is exactly 138, 141, 168. Each table entry was checked
against the old record's index/PTS/time-base/exact-seconds fields, and the
rational PTS multiplication was checked independently. These are inherited
diagnostic timestamps, not authenticated original exposure times or the old
Tracker engine's analysis-time table.

## Independent crop reconstruction

Without importing `prepare.py` or calling its PIL crop/resize functions,
NumPy reconstructed each display from the retained native array:

```text
expected = repeat(repeat(native[80:425, 300:510], 3, axis=0), 3, axis=1)
```

Every display pixel agrees: **652,050 pixels per crop**, **1,956,150 across
the three crops**. Each native crop contributes 210×345 = **72,450** source
cells; the 3×3 blocks add no historical resolution. The receipt's crop box
`[300,80,510,425)` and scale 3 are correct.

For integer display pixel indices `(u,v)`, the represented native pixel index
is `(300+floor(u/3), 80+floor(v/3))`. A native pixel `(x,y)` occupies the entire
3×3 block starting at `(3(x−300),3(y−80))`. Under an integer-pixel-centre
convention, the centre of that block is one display pixel right/down, at
`(3(x−300)+1,3(y−80)+1)`. Four exact centre round trips—including opposite crop
corners and points near the tape coordinates—were checked. This convention
must not be confused with source-cell origins or a claim that an arbitrary
subpixel Tracker mark has independently established physical meaning.

## Presentation qualification and remaining scope

The protocol describes a **“coordinate-labelled display aid.”** The run01
crop PNGs have no coordinate ticks, labels, analytical footer or padding:
their entire raster consists of repeated source pixels, as the independent
comparison verifies. Their coordinate map is recoverable exactly from the
receipt, so this is **not a pixel corruption or wrong crop-coordinate
transform**. It is an unmet presentation-label detail. Describe them as
unlabelled crops; a later, separately identified labelled derivative can meet
that presentation requirement without rewriting these originals. This issue
was reported to root before this review was saved.

This review used Python 3.13.7, NumPy 2.3.4 and Pillow 12.0.0. Both read-only
checks returned observed exit zero. No FFmpeg command was run by the reviewer,
no browser/image was displayed, and no architectural or causal inference was
made. The six-PNG outcome does not extend to any later refinement products,
which were not part of this job. The root and separate annotator's visual
label/correspondence assessments remain independent work with their own
limits.

## Additive refinement01 product check

After completing the original run01 review above, root requested a separate
check of the 12× endpoint patches and query overlays. The original result and
its missing on-image coordinate-label qualification remain unchanged.

The complete [refine.py](refine.py) was read at SHA-256
`8bf67d74d89dc3ef89f3a23f622a1aba2104e9d1f7883a0d49cb6b7079734cd8`.
The [refinement01 receipt](refinement01/receipt.json), SHA-256
`104c342609d05b3067c65463841429f368771ce416950ef0c0bac58c760d037d`,
records the exact same run01 receipt and native-file identities already
checked above. Its declaration hash
`4a87459c047d179854fae44e52d125056422f0058c50384fb309b24678a1835f`
matches current `root-observations.md`; **only that document's bytes/hash,
not its visual conclusions, were inspected in this pass**.

The directory has exactly **13 files**: six unmarked patches, six separate
query-overlay PNGs and the receipt. All 12 image-file hashes match their
receipt entries, with the exact ordered six `(frame, upper/lower)` records.
Source/code/declaration/receipt/product identities—**19 distinct files**—were
rechecked before and after the array tests. No new decode or image display
was performed.

| Region, at each of frames 138/141/168 | Native crop box | Unmarked mode and size | Overlay mode and size |
|---|---|---|---|
| Upper | `[398,184,432,210)` | L, 408×312 | RGB, 408×312 |
| Lower | `[400,377,434,405)` | L, 408×336 | RGB, 408×336 |

Independent NumPy slicing and 12-fold row/column repetition reconstruct every
unmarked pixel exactly: 127,296 per upper patch, 137,088 per lower patch,
**793,152 across all six**. These represent 884 or 952 original source cells
per patch, not added detail.

The declaration treats integer native indices as pixel centres. For crop
origin `(x0,y0)` and scale 12, its continuous display convention is
`u=12(x−x0)+5.5`, `v=12(y−y0)+5.5`. Exact Fraction calculations from the stored
binary64 query values reproduce the recorded display coordinates with zero
difference, and inverse mapping returns the same stored native coordinates:

| Query | Display centre in each corresponding patch |
|---|---|
| Upper | `(202.02480705622975, 152.38423373759383)` |
| Lower | `(208.98401323043026, 170.23208379272432)` |

This verifies the **declared analytical convention**, not an authenticated
original Tracker coordinate convention, a fresh point localization, source
subpixel resolution or physical endpoint identity.

Without calling the producer's drawing code, four explicit NumPy rectangular
masks reconstructed each overlay's positive-coordinate rasterization: two
horizontal and two vertical red arms, integer-truncated endpoints, width two,
with the central gap unpainted. Every RGB pixel agrees with the independently
expanded grayscale patch plus those masks: **793,152 overlay pixels checked**,
with exactly **104 red-arm pixels per overlay, 624 total**. The source pixels
outside the arms are unchanged and the pixel containing the query centre is
not painted. The marked overlays are separate derivatives; they do not
retroactively turn the initial run01 crops into coordinate-labelled images.

Disposition for this additive scope: **pass for identities, all 12× patch
pixels, declared query-coordinate mapping and complete overlay raster
reconstruction**. The read-only verification returned observed exit zero.
No visual/architectural inference, historical timing/decoder validation,
physical scale determination or automatic admission of the old rejected
measurement sequence follows. Per the bounded request, the product review
stops here.
