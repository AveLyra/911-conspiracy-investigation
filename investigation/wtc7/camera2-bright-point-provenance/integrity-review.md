# Independent two-PNG integrity review

2026-09-24. Reviewer `/root/curve_source`, reused prior-informed AI and prior
source/presentation checker. This is a separate read-only implementation check,
not independent historical evidence or human review. The root's expected
results were known. No root/producer code or Pillow was imported.

**Result: PASS.** The two source6925 PNG files have different encoded bytes
but identical complete decompressed filter/scanline streams and identical
independently reconstructed grayscale pixels. Each file matches its own
preserved selected-map/receipt chain. No repair, repinning or overwrite occurred.
This does not determine why the encodings differ, authenticate an emitter,
or make them independent exposures.

## Authority and exact scope

Read the complete `INTEGRITY-ADDENDUM.md` before mechanical processing and
verified its SHA-256:
`032019da2eb2c14781eabe2da18c5f17be287e39f9bf7ec8b5290dc47349d243`.
It prospectively permits only the declared two-PNG mechanical integrity check.
PNG pixels were decoded/reconstructed in memory; **no image was displayed,
no video was decoded**, and no new image, brightness score, coordinate,
exposure join or physical measurement was produced. The original broad
no-decode rule remains in force outside this exact exception.

Base directory for paths below:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/`.

| Exact relative PNG path | Bytes | SHA-256 |
|---|---:|---|
| tilted-camera-source-join/candidates01/f006925.png | 121238 | `cdd265e54fceb34833cc73de718780e2b371f34f7a52204a5fa3f3221e4bf9ce` |
| camera2-penthouse-event/run01/camera2/f006925.png | 121238 | `f9bcee99394139893f6ee6932ae5434b949da1c57f965a4cae02d57b0dccdc59` |

The comparison lane's previously failed cross-copy encoded-byte-equality
assertion is preserved as described in the addendum. Equal stored luma-hash
fields were not taken as a substitute for reconstructing the actual pixels.

## Actual command, checks and controls

Ran read-only inline `python3 -B - <<'PY'` with pathlib, collections,
struct, zlib, hashlib, json and sys. Runtime **Python3.13.7**;
zlib compile/runtime versions both **1.2.12**. The command exited0.
No files were written by that command. `rg --files`, narrow `rg -n -C5`
and read-only JSON-key inspection first located the exact metadata joins.

The independent program:

1. Rehashed the addendum and both actual PNGs. Read each own selection/receipt,
   required exactly one `f006925.png` row, source index6925 and stored PTS692502,
   and compared actual byte identities with the selected row. Checked each
   selection's actual bytes against its receipt pin. The penthouse receipt
   also names the PNG directly; the candidate receipt binds it through the
   pinned selection. No other representation's PNG hash was substituted.
2. Parsed from the PNG signature to the final IEND, requiring bounded lengths,
   complete consumption, correct chunk CRCs, a single leading13-byte IHDR,
   contiguous IDAT payloads and an empty terminal IEND without trailing bytes.
   Actual IHDR is640×480,8-bit grayscale, compression/filter methods0,
   noninterlaced. Actual chunk sequence/lengths in both files is
   IHDR13, IDAT65536, IDAT55633, IEND0; no ancillary chunk is present.
3. Joined both IDAT payloads in order and used bounded `zlib.decompressobj`
   output. Required end-of-stream, no unused or unconsumed compressed data,
   and exactly307680 decompressed bytes:480 rows of one filter byte plus640
   residual bytes. Compared the complete decompressed byte arrays, not only
   their hashes.
4. Implemented PNG row reconstruction directly for filters0–4, one byte per
   pixel. Each pixel uses the reconstructed left, prior-row above and upper-left
   values; modulo256 addition and PNG's Paeth tie rule were explicit. Both
   actual files use one Sub-filter row and479 Paeth-filter rows. Compared all
   307200 reconstructed pixel bytes with each other and each saved luma hash.
5. Counted all encoded byte differences and assigned them to parsed chunk
   payload/CRC regions. Reread both PNGs, both selected maps and both receipts
   at the end; all six file identities remained unchanged.

Before reconstructing the historical PNGs, fixed synthetic residual vectors
for previous row `[10,20,30,40]` reconstructed `[15,18,45,36]` under every
filter0–4: `[15,18,45,36]`, `[15,3,27,247]`, `[5,254,15,252]`,
`[10,1,21,250]`, `[5,254,15,247]`. Additional Paeth checks exercised selection
of left, above, upper-left and a tie; a zero-previous-row edge case reconstructed
`[7,9,6]` from filter4 residuals `[7,2,253]`. All passed. An in-memory
checksum-covered IHDR-byte mutation was rejected; neither source file was
changed. These bounded controls test the reconstruction/checker's relevant
operations, not a general-purpose PNG implementation or visual sensitivity.

## Own-chain metadata pins

| Relative metadata path | Bytes | SHA-256 |
|---|---:|---|
| tilted-camera-source-join/candidates01/selection.json | 492545 | `360d4646eb9318da7dd741f3c6be4d57c6c7c6879313514c98826257c7f89552` |
| tilted-camera-source-join/candidates01/receipt.json | 1403 | `7032350a5ce8de9297def16dc163c53dae055f16d6f5a18f703b9a3f5f54b778` |
| camera2-penthouse-event/run01/camera2/selection.json | 330219 | `e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d` |
| camera2-penthouse-event/run01/receipt.json | 68222 | `a5c72edd8f7714c0916c7b66f39f745c2cd7d73c99510f6c8a4be87ed751a114` |

These are current preserved-file integrity joins, not independent historical
authentication of those receipts, the original video or a camera exposure.

## Results and inference ceiling

| Comparison | Actual result |
|---|---|
| Encoded PNG bytes | Unequal:7 differing byte positions;3 lie in IDAT payload and4 in IDAT CRC bytes. |
| Complete decompressed filter/scanline stream | Equal,307680 bytes; SHA-256 `695ae9d4a25421f7432e4a70ea1f2045f1b2f8627fe5eec4150be6df0bf2c7ec`. |
| Complete reconstructed grayscale pixels | Equal,307200 bytes; SHA-256 `399e3918077427fcda44a00b897ad051df147b65c6078a584d470532ad5cde7c`. |
| Both own selected-map/receipt joins | Pass; no contradictory pin or decoded-pixel mismatch found. |
| Fixed filter controls and CRC-tamper refusal | Pass. |

The command's terminal result was
`PASS_BOTH_OWN_RECEIPTS_PNG_CHUNKS_CRCS_IDENTICAL_SCANLINES_AND_INDEPENDENTLY_RECONSTRUCTED_PIXELS`.

This corroborates root's reported Pillow-pixel equality through a separate
PNG-filter implementation without Pillow. It still shares the source bytes,
PNG specification and zlib-family decompression dependency; it is not an
independent historical observation or independent compression-library test.
Matching scanlines already imply matching deterministic reconstructed pixels;
those two layers should not be counted as separate historical corroboration.

The maximum conclusion is different encodings of the same decoded grayscale
image at the two checked paths. Encoder version, settings, nondeterminism or
other causes of the compressed-byte difference have **not** been established.
The result does not explain the earlier MOV conversion, test the point in an
independent representation, or alter any frozen visible-appearance judgment.
No other source-frame integrity exception was investigated here.

The initial status message accidentally compressed this distinction into
"no images/video shown/decoded"; an immediate correction explicitly stated
that PNG scanlines/pixels were mechanically decoded, no image was displayed,
and no video was decoded. This record preserves the precise performed scope.
Only this new review file is authored; method-review and original records remain
unchanged. Final source-family conclusions still await the assembled ledger.
