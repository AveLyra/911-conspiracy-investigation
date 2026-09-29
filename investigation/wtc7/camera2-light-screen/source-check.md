# Complete held-source preflight

2026-09-24. Separate checker `/root/curve_source`. **PASS for all 421 held
native PNGs, their saved grayscale pixels, source/map pins and exact clock
joins.** This is preparation for a chronological qualitative screen, not
an image-viewing record, flash detector, calibrated negative test or physical
finding. Presentation-page verification remains separate and pending below.

The complete new PROTOCOL.md was read before this check. Its checked identity
was 8,725 bytes, SHA-256
`8f715d88286e404fd2e20209e216a98e559860086f55161d722fe56916c6ef25`.
Main controls/charter remain controlling. The checker has prior source and
scene familiarity; preparation-role separation is not historical independence
or blinding. No historical image was displayed, video decoded, source acquired,
private packet opened, or prior annotation changed. This is the only file
written by this checker for the current task.

## Exact inputs

Selected native directory:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/run01/camera2/`

All **421** files `f006593.png` through `f007013.png`, inclusive, were checked.
The complete literal filename/byte/hash/luma-hash/PTS records are the pinned
`selection.json` in that same directory. There are no omitted or repeated
source indices in this selection, and the directory's `f*.png` filename set
exactly matches it. Overview pages are different products, not native frames.

Source video actually rehashed:
`/Users/admin/docs/911/research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov`

Original timing files actually rehashed:

```text
/Users/admin/docs/911/research/sherlock-wtc7-investigation/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv
/Users/admin/docs/911/research/sherlock-wtc7-investigation/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frames.json
/Users/admin/docs/911/research/sherlock-wtc7-investigation/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/source-identity.json
```

The selected extraction receipt is
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/run01/receipt.json`.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Converted MOV | 208810910 | `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730` |
| frame-map.csv | 867161 | `ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812` |
| frames.json | 3389769 | `424a2c27064548797ca9f4f0855781af490e4c912c7ccd5bc5340ee9a20524f0` |
| source-identity.json | 449 | `632c27b1ad4d04bddd991568a7c30206841ae3af5606fac801e61ffff561ca38` |
| run01/camera2/selection.json | 330219 | `e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d` |
| run01/receipt.json | 68222 | `a5c72edd8f7714c0916c7b66f39f745c2cd7d73c99510f6c8a4be87ed751a114` |

## Actual independent check

Executed read-only `python3 -B - <<'PY'` inline code using `pathlib`,
`hashlib`, `fractions`, `csv`, `io`, `json`, `sys` and Pillow. Runtime:
**Python 3.13.7, Pillow 12.0.0**. Exit 0; actual result:
`PASS_ALL_421_NATIVE_SOURCE_AND_PIXEL_JOINS`.

The checker did not import a producer or verifier module and did not run
FFmpeg. Its assertions were:

1. Verify the selected-map fixed pin, source ID VID-WTC7-001, complete
   extraction status, 8,042 checked source frames, 421 selected rows, declared
   640×480 geometry and exit 0. Verify the original `input_pins`,
   `input_pins_before` and `input_pins_after` dictionaries are identical;
   independently hash every file named by these four input entries.
2. Parse all **8,042** original CSV map rows and preserved probe-frame records.
   Require zero-based index order, equal source PTS and best-effort timestamps
   in both representations, strictly increasing PTS, time base 1/2997 and
   exact rational seconds equality. Verify preserved source-frame geometry
   640×480 and YUV420P metadata. Source-identity metadata must name the same
   source ID and actual rehashed MOV identity.
3. Require selected indices exactly `6593,6594,…,7013`, in order, and exact
   corresponding names. Compare **every original CSV field** for each selected
   row, not only index and timestamp. Compare saved duration ticks with the
   next original source PTS difference and the saved rational duration with
   those ticks divided by 2997. These are stored-clock joins, not motion or
   exposure measurements.
4. Read each selected PNG's actual bytes. Require its size/SHA-256 to match
   both the selected row and its receipt product. Decode those bytes with
   Pillow in memory; require format PNG, mode **L**, dimensions **640×480**,
   one PNG frame, and 307,200 bytes of decoded grayscale pixels. Require
   `sha256(image.tobytes())` to equal that row's saved `luma_sha256`.
   No conversion, resize, filtering, enhancement or coordinate measurement
   was performed. Verify the selected-map identity against its receipt too.
5. Check the recorded diagnostic summary and full-stream digest below.
   Reread all **428 distinct checked files** at the end; every byte size/hash
   was unchanged. This includes the protocol and metadata as well as the
   421 native PNGs; it is not a count of independent exposures.

The first selected frame retains PTS 659301, exact encoded seconds
219767/999; the last retains PTS 701303, exact seconds 701303/2997. The source
index is not a nominal frame-rate substitute. All intermediate joins passed.

## Recorded diagnostics and scope ceiling

The saved run has **one assessed PCM stereo-layout-guess line** and **zero
unclassified diagnostic lines**. This is not warning-free decoding. Its
recorded full raw-stream SHA-256 is
`1490b125faceae77a19edbda835682da3876f503c766af04be6cf6e93751b4dc`.
This pass checked the recorded value and summaries; it did not regenerate
the raw stream or reclassify the raw local-only decoder log. The older
full-video-to-Y-plane linkage remains the existing extraction's result,
not a fresh independent video decode here.

The saved multiview diagnostic's mixed/banded interruption is frames
1046–1064 (approximately 34.9–35.5 encoded seconds), outside this 6593–7013
interval. That does not certify absence of other image defects within it.
The original timing record's missing-PTS/duplicate checks do not establish
historical continuity, original interlacing or exposure timing.

The actual source is a secondary-hosted, explicitly converted access copy,
not an authenticated native or complete broadcast master. Its full-resolution
Y-plane images discard color and lack a calibrated photometric/exposure
response. Matching saved pixels can preserve inherited source/conversion
artifacts. Pillow decoding is a shared library dependency, not a new source
of historical corroboration. No visually inspected image, light-change
candidate, nondetection, flash attribution or mechanism ranking follows
from this preflight.

## Presentation verification status

Pending generation and receipts. No presentation page has yet been checked
or viewed by this checker. The later separate check must verify every native
image interior, index/order/label and coverage contract without importing
the producer, and preserve any discrepancy. A source-pixel pass alone does
not admit an unverified presentation or satisfy the visual-screen coverage
requirement.

## Completed independent presentation check

Appended after root reported that both historical presentations completed.
This supersedes the preceding pending status without changing that earlier
preflight record. The pre-append note had SHA-256
`f287477412517a8bb42b127a228bd85d0cf66b2dec3310bd0ce379a6fbd45674`.

Read the complete 291-line `present.py`. Its current SHA-256 matched root's
declared final producer:
`71074fe186b99f99c1cf8ccd4f7c980e0ed4abb8f76f389f8cc6f2f1798c38b1`.
The test-file pin also matched
`51d59a2157b2a0898096fccebe5f0597dbd8967cd277596c2ae5495f43582010`.
The protocol still matched the preflight pin. This checker did not import
the producer or test module, or rerun the producer's controls; root's reported
12-control result remains attributed to root.

Executed a separate read-only inline command:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 -B - <<'PY'
```

The command body used independent `pathlib`/`hashlib`/`fractions`/CSV/JSON/
`collections.Counter` traversal plus Pillow. Actual runtime was **Python
3.12.14, Pillow 12.3.0**. This intentionally used the recorded presentation
runtime for exact default-font rendering; it differs from the earlier
3.13.7/Pillow12.0.0 source-only check. No producer module was imported, no
video was decoded, and no image was presented to this observer.

Exit 0; actual result:
**PASS_ALL_PAGES_PIXELS_LABELS_SOURCE_ORDER_COVERAGE_AND_REPEATS**.

### Complete checks, not sampled panels

For **each** of run01 and run02:

- Verified complete-presentation-only status, 84 pages, 421 unique indices,
  504 slots, no presentation warnings, and unchanged source-generation
  diagnostic classification. The existing one-line source audio-layout
  warning is not erased by an empty presentation-warning list.
- Reconciled every receipt input/runtime pin and the saved before/after JSON
  products with actual files. Checked the exact expected key sets: **430
  input files** and **10 runtime/code files**. Both before/after maps agree;
  actual pins were checked again at the end. Rechecked source rows against
  the primary timing CSV and all 421 native PNG/grayscale hashes.
- Checked every one of the **93 listed product files** against its receipt
  byte size/SHA-256. The directory contained exactly those products plus its
  receipt; no omitted/unlisted file or failure marker was accepted. Producer,
  test, protocol and selected-map snapshots equal their pinned originals.
- Derived page membership directly from the declared rule, rather than
  accepting the producer's list: page p contains `6593+5p` through
  `6598+5p`. Verified all 84 page numbers, exact basenames, six ordered cells,
  full native names/pins/PTS/time-base/rational-time fields, and half-open
  image/label rectangles. The labels were independently constructed as
  `source INDEX | PTS PTS_VALUE | t=EXACT_RATIONAL s` from the source rows.
- Opened all 84 PNGs in memory: each is a single-frame **L-mode 1280×1512**
  image, with no image-info metadata, matching its encoded-byte and decoded
  page-luma hashes. This is mechanical PNG decoding, not visual inspection.
- For **every one of 504 image appearances**, directly sliced the decoded
  page byte plane row-by-row at the declared 640×480 native region and
  compared all bytes with the independently loaded source PNG's pixels.
  This did not use the producer's paste/crop/composition function.
- For **all 504 external label strips**, reconstructed the specified 640×24
  grayscale strip with background 24, default font size14, text position
  (6,3) and text value240. Checked text bounding-box fit and compared every
  decoded strip byte, including its background, with the page. The six
  image rectangles plus six strips cover the whole canvas; there is no
  unchecked margin or interior overlay.
- Counted **421 unique source indices / 504 appearances**, with exactly
  **83 boundary frames repeated twice**, all other frames once. Counted all
  **420 consecutive in-scope adjacent pairs exactly once** within pages.
  Boundary repetition is presentation context, not another exposure.

### Pins and repeated-run comparison

All filenames below are under this `camera2-light-screen` unit:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| run01/receipt.json | 249217 | `bafcb0d149a7e6867ec02b8d106aa573c973391bcb94bfa3370a809f360bd473` |
| run02/receipt.json | 249217 | `8a5d32bb0cd481939222e6f13da48764d840e5597a70e4b80527d68b27c5148d` |
| run01/manifest.json | 452911 | `58e9ae14cfc47c4fddd1caf883675c9387aafc28daac65f10c0bd42f68d5869d` |
| run02/manifest.json | 452911 | `58e9ae14cfc47c4fddd1caf883675c9387aafc28daac65f10c0bd42f68d5869d` |

Every corresponding one of the **93 non-receipt product files** was checked
for actual byte equality across runs. This includes all **84 PNG page pairs**
and nine metadata/snapshot files. Receipts were parsed and compared: the
**only difference** was the command's `--out run01` versus `--out run02`
argument. They are correctly not described as byte-identical.

### Admission ceiling

The fixed presentation passed this independent implementation check and can
proceed to the separately authorized qualitative viewing stage. Its appearance
to the viewing tool, full native-detail readability, and all required actual
observer coverage remain untested by this mechanical check. No visual label,
light-change candidate, nondetection, physical interpretation or human review
was supplied here.

The checker shares the exact Pillow/default-font/runtime family and the same
source bytes with the producer. Its separate byte-slicing/order/coverage code
is not a separate decoder technology, independent historical exposure,
OCR-based text reading, detector-sensitivity test or external expert review.
The successful source/presentation checks cannot establish flash absence,
calibrate recording sensitivity, or bypass later measurement/human gates.
