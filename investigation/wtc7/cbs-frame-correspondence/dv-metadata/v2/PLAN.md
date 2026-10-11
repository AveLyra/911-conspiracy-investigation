# Chunked storage correction for the DV metadata inventory

2026-10-04, before revised historical execution. Version1 Clips1 and2 both
reached the1MiB compressed-metadata limit and returned exit1; their complete
error captures remain in the parent directory. They produced no accepted
results. Post-failure source hashes and all11 frozen dependencies matched.
No other version1 historical clip was run. Do not relabel these refusals passes.

The failure was an incorrect compression-size allowance, not a demonstrated
malformed frame or timing finding. Revise storage, not extraction: keep the
unchanged parent extractor, RIFF traversal, all eight inputs/5567 frames,
raw pack retention and no-semantic-clock interpretation. No historical image
or audio decoding, new acquisition, changed source association or frame sampling.

## Revised resource contract

Split retained metadata into at most25 files per clip, each covering100 whole
frames except a final1–100-frame chunk. Every raw chunk is at most957000 bytes;
every compressed artifact must remain at most1MiB. Total raw storage is bounded
by23925000 bytes and total compressed storage by25MiB per clip. This is an
explicit increase over version1's **total per-clip**1MiB limit, not compliance
with that failed criterion. The separate8MiB JSON summary cap remains unchanged.

Write computed binary derivatives locally under the fixed version2 results
directory using exclusive creation. Do not reuse a partial directory, follow
symlink output paths, overwrite files or delete refusals. Use only fixed chunk
basenames, not embedded source paths. A chunk directory without its verified
sibling `clipN-result.json` manifest remains incomplete; manifests stay outside
the chunk-only directories. A failed command is never an accepted result merely
because it left files on disk.

Require exact gap-free, nonoverlapping coverage of[0,expected_frames), chunk
count=ceil(frames/100), exact byte/frame counts, per-chunk raw and compressed
hashes, strict decompression with EOF and no trailing data, and concatenated
equality to the original retained bytes. Reopen all artifacts before reporting
success. Source and frozen dependency checks must pass after collection before
the final result is created. Keep every failure/partial artifact visible.

## Verification and interpretation

Freeze this plan, wrapper, storage module and synthetic tests plus the exact
parent freeze and every parent frozen dependency. Test storage boundaries,
invalid counts, corruption, truncation, extra compressed bytes, missing or
reordered/overlapping chunks, collisions and unsafe output paths. Test wrapper
post-check refusal; no final accepted result on a changed source/dependency.
Obtain separate method review before restarting the fixed eight-file collection.

Original version1 code remains unchanged. The wrapper's explicit storage-function
substitution is versioned and pinned; it is not a silent modification of the
historical method. All raw timing candidates remain uninterpreted unless a
separate checked semantic conversion is actually performed. Successful storage
does not authenticate a clock or establish event order. Full charter and existing
human/pixel/legal/privacy/archived-feedback boundaries remain unchanged.
