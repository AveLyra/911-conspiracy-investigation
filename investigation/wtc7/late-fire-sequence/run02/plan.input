# Declared source-boundary and denser sample selection

2026-09-19, after acquisition/container probing, before historical image
derivatives. PROTOCOL.md SHA-256:
`878822418fae5d60096bbc509e101025cdd23463f062ce6fb7e0eb25c9098ef9`.
The exact machine manifest is selection.json; its hash is pinned at execution.
This is prior-informed source follow-up, not an unused/blind test set.

## Sources and fixed indices

- Dub5 14: acquired73206324bytes, SHA-256
  `055319a4017ce2f097dd8e9eb3ab5cbacd33bde06463d13eb4f6e32a30f655aa`;
  container578frames,720×480DV,yuv411p,SAR8:9,time base333651/10000000.
  Select indices0,30,60,…,570 and572,573,574,575,576,577: **26** samples.
- Dub5 15: existing60183924bytes, SHA-256
  `8a4e3e02105d65140c2a3dc0bc95af0d907866de85353d5c9f498636aea79781`;
  container475frames,720×480DV,yuv411p,SAR8:9,time base6673/200000.
  Select0,15,30,…,465 and474, plus1,2,3,4,5: **38** samples.

Together64selected native images per pass. Exact source counts/dimensions/PTS
must be reconciled against full decoded inventories; the container probe is
not already a decoder-fidelity check. No six-second interval is selected or
assumed. The approximately1s/0.5s coverage is deliberately distinct from the
six consecutive frames at each proposed boundary. Each source retains its
own PTS zero and time base. Do not create one merged event clock or concatenate
the files merely because their numbers are adjacent.

## Processing, controls and observation

Use versioned sample_sequence.py, evolving the preceding unit's pinned helper,
with strict explicit source/index manifest and plan hashes. Keep original
helper/output history unchanged. The accompanying helper review documents
synthetic tests and narrow changes before any historical run. Require both
probe and decode diagnostic gates and retained exit status; any unreviewed
diagnostic blocks image admission even if output hashes repeat.

Native decoding is video-only with copyts, noautorotate, noautoscale, no rate
conversion, no interpolation, no deinterlacing, no enhancement or SAR resampling.
RGB PNGs are display derivatives. Retain source PTS/time base, native dimensions,
SAR/interlace metadata and hashes. No audio interpretation or calibrated
photometry. Human review and scientific measurement acceptance remain pending.

Run two exclusive output directories. Require repeated index/PTS/pixel/file
identity and unchanged source hashes. Synthetic ground truth must cover exact
selection/PTS/geometry/color and gate negatives, including probe-only errors,
decoder severity, malformed indices and refusal of existing destinations.

Root and the prior separate AI observer each inspect all admitted native PNGs,
not thumbnails or a generated movie. No montage/overview is part of this first
pass. Label actual viewing coverage and freeze new conclusions before exchange.
Both have prior reference/sample familiarity, and filenames are known. This
does not count as independent camera evidence or a human spot-check.

For each source record view/framing, persistent geometric anchors, clear
orange/flame-like forms, obscuration and obvious discontinuities at the sampled
cadence. At the source boundary compare the final six14frames with the first
six15frames for matching composition, feature trajectory, haze and visible
forms. These can support or contradict adjacency, but ordinary similarity is
not exact frame identity or proof of an unedited recording. Unsampled intervals
remain explicitly untested. Figure157and158are compared separately.

No automated optical registration, image-similarity threshold, pulse-duration
estimate, no-event claim, floor assignment, fire area/temperature or causal
ranking is accepted in this stage. A positive boundary mismatch is meaningful;
failure to find an edit is weaker than a demonstrated continuous camera tape.
If the boundary is incompatible or diagnostics fail, preserve it and follow the
specific missing source/version rather than optimize away the discrepancy.
