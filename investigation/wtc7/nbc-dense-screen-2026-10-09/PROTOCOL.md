# NBC candidate dense picture screen

October 9, 2026. Prospective selection for a research-only extension of the
separately acquired two-file NBC packet. This does not authenticate sound or
measure collapse motion. Existing twelve-frame findings and the three C
reference pictures are already known; this is not a blind or held-out test.

## Fixed inputs and decision

Use unchanged local source bytes under
`/Users/admin/docs/911-worktrees/nbc-media-acquisition-2026-10-09/research/sherlock-wtc7-investigation/nbc-media-acquisition-2026-10-09/`.
Verify the acquisition manifest's sizes and SHA-256 hashes before and after.
The two files are `sources/collapse wtc.mpg` and `sources/wtc5.mpeg.mpg`.
The separately authorized acquisition removed a local-byte dependency; it did
not establish camera custody, building identity or original soundtrack.

Ask whether these candidates contain recognizable pictures corresponding to
Excerpt C's third shot, using the existing full-raster frames 0421, 0571 and
0721 from `../audio-listening-2026-10-05/c-full-visual-review/run01/compilation/`.
The distinctive relation is the tall dark facade at image right, the lower
cupola-bearing building and the intervening street/dust view. A city skyline
or dust plume alone is insufficient. A possible match triggers a separately
declared continuous sequence comparison, not immediate source acceptance.

## Selection and inspection

1. Inventory all decoded video frames and their best-effort presentation
   timestamps. Retain original PTS as available; reject non-increasing or
   missing best-effort timestamps instead of inventing a cadence.
2. Small candidate: inspect every decoded frame (previous count 295).
3. Large candidate: first decoded frame in every occupied one-second bin of
   its absolute encoded timestamp, plus the final frame if not already chosen.
   Do not fill empty bins. Record actual spacing and count (not assumed 30 fps).
4. Retain full 320x240 decoded rasters in PNGs and labeled row-major sheets,
   20 frames per sheet. Labels lie outside the raster. No crops, enhancement,
   interpolation or stabilization. Decode/color conversion remains a viewing
   derivative; square-pixel sheets are not geometric calibration.
5. Root reads every sheet against the three references. A separate AI reader
   checks a fixed sample: sheets with zero-based ordinal divisible by three,
   separately within each candidate. Record disagreements before resolving
   them; any ambiguous match must receive native-frame inspection. These are
   AI visual screens, not actual human acceptance or expert review.

Known large-file decode warnings remain visible. Preserve every stderr and
command, and identify corruption as a limit on negative matching. Do not repair
the source, silently drop suspect frames, or equate exit zero with clean media.

## Verification and conclusion limits

Test frame selection on explicit variable-rate, boundary, duplicate and missing
timestamp fixtures before historical extraction. Reconcile selected indices,
PNG counts and decoded showinfo PTS. Reproduce extraction in a second output
directory and compare all selected PNG hashes and sample maps. An independent
checker must recompute selection from the saved frame inventory without using
the selection function. Preserve all failures and stop if selection or frame
identity cannot be reconciled.

A negative small-file result covers every successfully decoded frame, not a
missing original or arbitrary reframing. A negative large-file result covers
only the selected images; a brief inserted shot, alternate crop, corruption or
unrecognizable view can escape it. Report the largest observed sample gap.
No audio listening, loudness inference, historical time alignment, source-wide
silence claim, original-soundtrack authentication or cause ranking follows.
No main/legal records, frozen material index or human-review gates change.
No publication or push is authorized. Keep a dated result and status link;
preserve the older acquisition failures as history.
