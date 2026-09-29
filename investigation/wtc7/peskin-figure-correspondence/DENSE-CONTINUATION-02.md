# Coverage failure and decoder continuation

The first historical execution completed `dense00` with 240 selected frames and
eight exact source-anchor pixel matches. `dense01` failed its exact probe/filter
PTS-list comparison: showinfo contains 215 frames, PTS 2510022 through 2517162;
the independent ffprobe invocation contains 240 in-scope frames, through 2517996.
The missing 25 are a final suffix, with no extra filter PTS. Preserve this failed
directory and the successful first chunk. This is an extraction failure, not a
historical footage anomaly or evidence about NIST.

The decoder used `-noaccurate_seek`, a requested start two seconds before the
selected interval, and input `-t 12`. The observed cutoff is consistent with
the read duration including an earlier keyframe lead-in. Installed FFmpeg's
manual distinguishes input duration and seeking to an earlier seek point.
Do not identify the unlogged exact seek point merely by subtracting 12 seconds.
The next version increases only that read allowance to 24 seconds. The filter
still selects the identical half-open eight-second PTS interval; no new analytic
candidate, transform, metric or frame interpolation is added. Exact ffprobe
list equality, eight anchor-pixel comparisons and all warning gates remain
required. An insufficient allowance must still fail rather than hide a gap.

Continue the remaining three chunks in fresh `dense11`, `dense12`, `dense13`
slots, with corresponding `repro11`, `repro12`, `repro13`. Do not rerun or replace
the already complete first chunk. Its exact source is preserved byte-for-byte
as `dense_match01.py` (SHA256 8c5c92932c43183d0861e16282f95e7be360a36bd9ee016c639e638ebed82bb1)
and its same-code `repro00` must complete before the new production directories
are populated, so the old runner's baseline budget remains satisfied.

Updated storage slots: original `dense00` 450 MiB; failed `dense01` 100 MiB;
each of the three new primary chunks 400 MiB; each of four reproduction chunks
10 MiB; all other unit artifacts at most 150 MiB. Sum: 1940 MiB, below the
original 2 GiB unit cap. The first run's saved PNGs plus the three remaining
chunks retain the original maximum of 64 new native PNGs. The failed chunk
reached no native-image-writing stage. No reproduction creates native PNGs.

All completed chunks must share the exact pinned mathematical core, source,
targets, original declarations and runtime/tool versions. Keep their different
decoder-runner versions and this amendment explicit rather than treating the
new execution code as byte-identical to the old code. Reproduce each chunk with
the exact runner that produced it. Aggregate only complete source-PTS coverage;
retain the failed earlier partial scores but do not include them a second time.
