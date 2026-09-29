# Two-file integrity exception, before mechanical decoding

2026-09-24. The alternate-inventory lane reported that the two held PNGs for
Camera2 source index 6925 have unequal encoded-byte hashes but equal stored
luma hashes. Its cross-copy byte-equality assertion failed; that failure and
the original files remain preserved. No inference of pixel equality, corruption
or alteration follows yet.

This prospectively extends PROTOCOL.md solely to inspect those two files:

- `../tilted-camera-source-join/candidates01/f006925.png`
- `../camera2-penthouse-event/run01/camera2/f006925.png`

First verify actual file identities against each file's own selected-map and
receipt, not against the other representation's PNG hash. Parse PNG chunks,
validate signatures/lengths/CRCs and IHDR, join IDAT and decompress it. Compare
the complete decompressed filter/scanline streams, retaining any difference.
Then independently decode both with the existing bundled Pillow and compare
mode, size and all pixel bytes to each other and each stored luma hash. These
are integrity checks, not visual interpretation. Record runtime/library
versions and distinguish shared-code checks from historical independence.

Do not infer why a byte difference arose without encoder/runtime provenance.
If actual decoded pixels differ or either receipt fails, stop historical
reuse and report the exact failure; do not overwrite or silently repair either
file, recompute its historical pin, or choose the preferred copy. If pixels
match, the maximum conclusion is different encodings of the same decoded
image under the checked paths, not independent exposures or a physical light.

No image is displayed; no video is decoded; no new historical PNG, brightness
score, coordinate, source match or physical measurement is created. Other
protocol and actual-human boundaries are unchanged. Root performs the check;
the independent final reviewer must inspect its coverage and result.
