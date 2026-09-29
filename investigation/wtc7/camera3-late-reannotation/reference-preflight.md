# Reference baseline preflight

Root viewed the complete native frame288 before selecting provisional
centers, then the complete analytical reference-box overlay and all six
21/31-pixel reference patches. This note is frozen before numerical scoring.
These are computational visual observations, not human landmark approval.

- R1 (272,400): both patches cover the bright foreground streetlamp cluster,
  including its dark internal/adjacent structure. Accepted as a recognizable
  texture neighborhood, not as an identified fixed material center.
- R2 (168,348): both patches cover the foreground diagonal facade/window-band
  neighborhood; the larger patch includes more of the bright window boundary.
  The center itself lies on relatively plain facade. Accepted as the intended
  texture patch, with a warning that smaller-patch uniqueness may fail.
- R3 (673,292): both patches cover the upper right-neighbor masonry/window
  neighborhood. Contrast is visibly low, and the larger patch includes more
  left-edge/sky context. Accepted for the declared numerical texture test;
  this visual association does not certify sufficient contrast or uniqueness.

No center was moved. All three candidates proceed under both declared sizes;
retain any texture, correlation, margin, tie or boundary failure. Do not
silently drop a failing reference to manufacture an all-three map. None is
asserted to share the target facade's depth or yield physical calibration.
