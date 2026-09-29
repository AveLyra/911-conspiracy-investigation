# Prospective handling of one tiled report image

2026-09-24, after extraction metadata and before any reconstruction or new
annotation. No image appearance selected this route. Physical252 contains17
same-width JPEG strips (sixteen975×39 and one975×37), besides a separate image.
The source reviewer must first confirm these strips compose one target figure.
If so, annotate one reconstructed raster, not17 decontextualized exposures.

This addendum supplements the frozen PROTOCOL without replacing its hash.
The anonymous key must pin this addendum and the reconstruction receipt; both
observers read it before the derived image. This is faithful source decoding,
not generated historical evidence or an enhanced illustration.

1. Preserve every original encoded strip, placement matrix, object identifier,
   dimensions and source hash. Source reviewer supplies the figure association
   separately; the anonymous observer key must not expose that caption.
2. Independently verify the tiles have one common horizontal placement/scale,
   no rotation/reflection, matching width/channels and vertically contiguous,
   non-overlapping placement at the same scale. Use the PDF's actual numeric
   precision, with a prospective maximum residual of1e-4 PDF points at each
   join; report actual residuals. A larger residual, gap, transform, mask or
   width/color mismatch stops simple row assembly; do not fix it visually.
3. Sort by the verified top-to-bottom page placement. Concatenate complete
   decoded rows exactly into a975×661 PNG. No crop, interpolation, resampling,
   enhancement, inpainting, color adjustment or blending. JPEG strip-edge
   artifacts are preserved. The PNG is a reconstructed report-native raster,
   not a single original embedded JPEG or a camera original.
4. Reopen the PNG and verify each corresponding row range equals the decoded
   parent strip pixel-for-pixel. A second implementation independently checks
   order/geometry, parent encoded bytes and every output pixel; integrity alone
   cannot validate figure association or historical authenticity.
5. Anonymous key labels the asset's representation as reconstructed_tiled_raster
   and records dimensions/path/PNG hash plus addendum/receipt pins. Its
   native_pdf_dimensions field, retained for the existing observation schema,
   denotes the exact combined source pixel grid here, not a single PDF object.
   Non-tiled assets retain their unchanged JPEG contract. Validator permits
   PNG only for this specifically verified tiled reconstruction, not arbitrary
   derived imagery. Selection/order still includes all declared target figures.

If these checks cannot be met, preserve the figure as an explicit unresolved
representation with full-page source review, not an invented seamless image
or a no-fire observation. No whole-floor/heat/causal conclusion or extra event
count follows. All prior observation, privacy and source-preservation gates
remain. Root/observer pair records still freeze before the remaining batch.
