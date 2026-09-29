# Same decoded image, different PNG bytes

2026-09-24. Root check performed only after INTEGRITY-ADDENDUM.md was saved and
hashed (`032019da2eb2c14781eabe2da18c5f17be287e39f9bf7ec8b5290dc47349d243`).
This is a mechanical two-file integrity result, not an image observation,
independent historical source or new video decode.

## Result

Both stored source-6925 PNGs match their own saved identities. Their encoded
bytes differ at seven positions, but **every decompressed filter/scanline byte
and every decoded pixel agrees**. No pixel discrepancy was found in this pair.
The files remain unchanged; neither was overwritten or silently rehashed.

| Layer | Tilted unit `candidates01/f006925.png` | Penthouse unit `run01/camera2/f006925.png` |
|---|---|---|
| Encoded bytes | 121238 | 121238 |
| SHA-256 | `cdd265e54fceb34833cc73de718780e2b371f34f7a52204a5fa3f3221e4bf9ce` | `f9bcee99394139893f6ee6932ae5434b949da1c57f965a4cae02d57b0dccdc59` |
| Complete decompressed filter/scanline SHA-256 | `695ae9d4a25421f7432e4a70ea1f2045f1b2f8627fe5eec4150be6df0bf2c7ec` | same |
| Actual decoded 307200-pixel-byte SHA-256 | `399e3918077427fcda44a00b897ad051df147b65c6078a584d470532ad5cde7c` | same |

Both are single-frame, 8-bit grayscale, noninterlaced 640×480 PNGs. Each has
IHDR (13 bytes), IDAT (65536), IDAT (55633), IEND (0), with every CRC verified
and no trailing bytes. Joined IDAT streams decode to the same 307680-byte
filtered raster; the extra 480 bytes are row-filter tags. Pillow independently
returns the same mode, dimensions and complete pixel array from each file.
Each actual pixel hash equals its own selection record's stored luma hash.

The source clock fields also agree in the stored rows: index string `6925`,
PTS `692502`, time base `1/2997`, encoded seconds `230834/999`. Those are
stored-clock identities, not authenticated exposure timing. The stored full
video-frame hash was not rederived: this check decoded PNGs, not the MOV.

## Actual execution and failure history

The alternate-inventory lane's initial cross-copy byte-equality assumption
failed and remains recorded there. Root's first metadata locator likewise
returned empty lists because it compared the stored string index with integer
6925. It was corrected to exact string `6925`, requiring exactly one row in
each selection; no source was changed or treated as absent.

The successful stdout-only bundled Python command imported `pathlib`, `json`,
`hashlib`, `struct`, `zlib`, `sys`, `io` and Pillow. It:

1. Located exactly one `frame_index_zero_based == '6925'` row per selection.
2. Rehashed actual PNG bytes against each row's own `png_identity`; checked
   the older selection identity against its receipt and the newer PNG identity
   directly against its receipt's `camera2/f006925.png` product.
3. Parsed each entire file, verified PNG signature, bounded chunks, every CRC,
   exact IHDR, final empty IEND and complete consumption without trailing data.
4. Joined IDAT, used `zlib.decompressobj`, required end-of-stream with no unused
   data, and checked the complete filtered-raster length.
5. Decoded each in memory with Pillow, required L mode, 640×480 and one frame,
   hashed all pixel bytes and checked the saved luma pins.
6. Compared actual encoded bytes, complete filtered rasters and pixel arrays;
   counted seven encoded-byte differences and asserted complete pixel equality.

Exit 0: `PASS_TWO_FILE_INTEGRITY_NO_DISPLAY`. Runtime: bundled Python3.12.14,
Pillow12.3.0, zlib compiled/runtime 1.2.12. The full command and stdout are in
this task's execution history. An independently authored chunk/CRC/zlib replay
is separately recorded in integrity-review.md; that is not another historical
exposure. No screen display, new source image, normalization, enhancement,
brightness measurement, video decode or physical event calculation occurred.

## What this resolves and does not

It resolves the observed **encoded-file mismatch** as two encodings with the
same decoded grayscale image under the checked readers, not as a different
point appearance. It does not identify the software or setting responsible
for the encoding difference, authenticate the source recording, restore color,
or explain the bright point. A hash mismatch was a valid trigger for inquiry,
not affirmative evidence of tampering; equal pixels are not independent
corroboration of the historical scene. The original first-pass records stand.
