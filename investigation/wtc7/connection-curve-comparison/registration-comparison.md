# Candidate registration comparison and full anchor envelopes

2026-09-27. Source-mapping preparation only; actual human review pending.
Both prior-informed AI notes froze before exchange:

- Root: `registration-root.md`, SHA-256
  `ec66ae85a45a0169b7e8cc61698cc522e75cda2f2905f4c283f45f88de1f55a7`.
- Separate reader: `registration-independent.md`, SHA-256
  `25dd8b7f89a282c78b9e9b4415c05f3a507309fec13b5d64ee0313a354259805`.

They agree on axis quantities/ranges, the lower ordinate's10^3 multiplier,
solid=spring and dashed=shell, and all seven bolt colors. They share one
published source; this agreement is not historical corroboration, human
review or physical validation. Both source notes remain unchanged.

## Small positional differences and distinct uncertainty conventions

The root selects integer **pixel cells**, interpreted with their full
footprint and an extra +/-3-cell radius. The separate reader estimates
continuous line-center coordinates from the upper-left page edge, with
an assessed +/-6-render-unit interval. These are different declared
conventions, not conflicting physical pixel measurements.

After putting both centers into continuous page-edge coordinates, all six
anchor center differences are only0.5render units per axis. Root's energy
left boundary is cell473 (center473.5), versus reader474. The remaining
integer anchor values coincide, but root's cell centers are0.5greater.
All six root assessed-plus-cell rectangles fit within the reader's broader
assessed rectangles. Do not average them, select the narrower as validated,
or divide uncertainty by reader count. Both are subjective allowances, not
independent error distributions. Human corrections become a separately
attributed record, not edits to either frozen reading.

Root's interior tick positions are expressly linear predictions. The other
reader lists visually assessed major-tick candidates, with approximately
regular spacing; that is not a second exact calibration. All candidates
must remain checkable. The lower panel's left edge and span differ from the
upper panel, so a shared x registration is disallowed.

## Full root anchor footprint conversion

This completes the method critic's specific request for intervals rather
than only center examples. For root cell(i,j), radius3 means page-edge
rectangle [i-3,i+4]x[j-3,j+4]. PDF X=0.36x; PDF Y=792-0.36y.
Every rectangle was intersected with **all twelve** actual strip boxes.
These six anchors each intersect exactly one strip; none touches a seam.
Other ticks can cross seams: the independent200,000N-m ordinate candidate
intersects both Im9 andIm10, which must both be retained.

PDF values below are exact at the stated decimal precision. Native intervals
are rounded **outwards** to0.01source-cell edge units for display; that
precision describes the transformation, not measurement accuracy. Use the
unrounded Fraction calculation for later propagation, never a rounded center.

| Anchor | PDF X points | PDF Y points | Strip | Native u interval | Native v interval |
|---|---|---|---|---|---|
| F0 |[160.56,163.08]|[492.12,494.64]|Im5|[67.15,72.41]|[29.71,35.00]|
| FR |[464.76,467.28]|[492.12,494.64]|Im5|[701.17,706.43]|[29.71,35.00]|
| FT |[160.56,163.08]|[709.92,712.44]|Im0|[67.15,72.41]|[15.74,21.00]|
| E0 |[169.20,171.72]|[189.72,192.24]|Im11|[87.57,92.83]|[21.87,27.13]|
| ER |[465.84,468.36]|[189.72,192.24]|Im11|[705.24,710.49]|[21.87,27.13]|
| ET |[169.20,171.72]|[413.28,415.80]|Im6|[87.57,92.83]|[16.12,21.38]|

The native values reference each named strip's own upper-left edge, not a
stitched panel. Im5 has a different vertical scale fromIm0–4. Source pixels
are not reconstructed solver samples. Geometry does not establish visibility
through the PDF's white paint, glyphs, keys or clipping. The two notes agree
on the explicit white-mask rectangles and refuse a page-wide clipping claim.

The separate reader's broad bolt-key exclusion boxes extend5render units
farther downward in force and7in energy. Preserve the union as the initial
exclusion: force x[1040,1160],y[310,470]; energy x[575,695],y[1138,1302].
This deliberately includes whitespace. No curve support is asserted in the
small differing regions or recovered beneath those keys. Changing these
exclusions later requires a documented source check, not a favorable metric.

A subsequent read-only pypdf content-stream order check on the pinned page
narrows the clipping uncertainty without recovering underlying curves. All
twelve image invocations occur at zero-based operations26–85. White fills
occur afterward at105 and137. The two clip scopes are enclosed by q/Q at
114/125 and146/157; they contain text operations, no image invocation. The
graphics-state stack balances. Thus these two local clips do not clip the
already painted graph strips. White overpainting and native glyphs remain
part of the visible composition. This is a single-parser order check, not
a second rendering validation or proof of any hidden curve's identity.

## Actual verification

Root read the entire new synthetic-control implementation and receipt.
Bundled Python3.12.14 replay passed all20 named controls. Its complete JSON
matches the producer's Python3.14.0 receipt except `python` and `executable`.
The saved producer code/receipt remain unchanged. This is a replay, not a
new independent implementation of every test.

Before importing that code, root separately derived the six envelopes from
the JSON CTMs using Fraction arithmetic. Afterward, all six matched the
control functions exactly, including strip membership and four native bounds.
Root additionally executed the separate reader's complete embedded geometry
script: all33 tick entries and the control-pin line reproduced its saved
stdout exactly, with no stderr. This reproduces the conversion, not the
reader's visual placement. The note's two-decimal values are descriptive
rounding, not outward-rounded coverage bounds to feed into later analysis.

Synthetic controls are detailed in [registration-method-review.md](registration-method-review.md).
They exercise known raster marks, y inversion, cell footprints, differing
strip scales, multiple seam candidates and explicit refusal of ambiguous
support. They do not validate JPEG-artifact tolerance, automatic line
classification, actual historical linewidth or hidden support. The explicit
support guard depends on correct input declarations; it does not detect an
unreported crossing. No ordinary dash gap is bridged at this stage.

## Permitted next action

Use the [human source-mapping packet](human-review-packet.md) once the
read-only viewer passes its recorded checks. The six root candidates are navigational suggestions, not
accepted coordinates; preserve the other reader's broader alternatives.
Record actual coverage, corrections and unreadable items. Later selected
curve samples and their graphical uncertainty require separate checks before
any consequential metric. Neither reader agreement nor a green software
test clears HUMAN-REVIEW-GATE.md. No graph mismatch, calibration adequacy,
historical cause, intent or legal conclusion is established here.
