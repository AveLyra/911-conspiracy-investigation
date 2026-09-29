# Dense continuation declaration

Saved after the fixed32sample screen and before any new dense video frames.
Initial results are exploratory candidate scores: T148's best static sample
is2522, its best dynamic sample2521; T149's best sample on both metrics is2524.
This does not establish either exact frame. Root has viewed complete native
samples2521,2522,2524; an independent reviewer is checking the full initial
shortlist. Preserve all32sample/64comparison results and all score surfaces.

Retain the original METHOD-01 registration unchanged for a full-frame candidate
search in the entire declared [2502,2534) interval, not just the favorable few
seconds. Use four disjoint eight-second source-PTS chunks: [2502,2510),
[2510,2518), [2518,2526), [2526,2534). At most550decoded frames per chunk and
1100combined accepted frames; at most16new full-resolution shortlisted PNGs
per chunk,64for this unit. Per-chunk output cap450MiB and wall budget300seconds,
within the unit's2GiB cap. No new storage of all full-frame RGB images.

Stream full1620x1080rgb24 frames from the unchanged pinned video, using the
tested absolute timestamp seek/no-accurate-seek/no-autorotate selection pattern.
Capture showinfo PTS with unchanged source timebase, match count/order to raw
frames, and compare the selected list with independently invoked ffprobe
per-frame PTS/best-effort timestamps. These share the FFmpeg code family and
do not authenticate original camera cadence. Require exact decoded-pixel
agreement for each common one-second sample with its already pinned PNG;
JPEG/PNG/container hashes are not decoded-pixel hashes. Keep warnings local
and fail acceptance on unreviewed decode warnings, missing timestamps or
partial/extra frames. Use a timer and create-only paths; preserve failures.

For all frames retain every static scale/translation score surface and overlap,
the two highest static geometry candidates, dynamic-region scores evaluated
after fitting, and sourcePTS/decoded-RGB hash. Store only the union of each
chunk's top4static and top4dynamic frames per target as full native PNGs.
Reproduction must be in separate output paths and compare actual arrays,
candidate rankings and native selected pixels. A saved start/lock is not a
live-process handle.

The independent source review identifies a substantial limitation: these
foreground-based masks do not establish background WTC7 alignment. This run
therefore remains a candidate-finding stage. Before exact correspondence or
time separation, check background structural alignment and separated dynamic
regions on shortlisted frames, retaining alternative scales/frames and
generation/blur/interlace possibilities. Do not choose a3second interval as
an acceptance requirement or reinterpret0.005/0.01/0.02score bands as confidence.

Method wording corrections retained additively, without rewriting the frozen
METHOD-01 or earlier receipts: the implementation is binary64 evaluation of
linear (not circular) correlation, not exact arithmetic. Its population-
variance acceptance is strictly greater than1e-8 (at/below is rejected).
The independent oracle uses an inclusive boundary and does not certify
equivalence at that exact threshold. These nuances do not invalidate the
tested nonconstant integer-valued image-overlap domain, and no historical
score is changed by this clarification. The independent core comparison does
not certify the full registration or an original exposure.
