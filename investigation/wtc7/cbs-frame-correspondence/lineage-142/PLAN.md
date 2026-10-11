# Figure 5-142 held source lineage check

2026-10-04. Research only. Prior turn was progress: the complete paired
comparison and verification finished. This follow-up asks whether the held
files or their directly linked catalogue records identify the original source,
frame or field, or the processing that produced Figure 5-142. It does not
repeat the matcher or infer historical authenticity from a hash.

## Fixed scope and acceptance

Inspect the original Clip 7 AVI, the Figure 5-142 report JPEG, NCSTAR 1-9's
document metadata and image object 2850/0 on physical page 272, the saved
acquisition/catalogue records, and directly referenced report context. Record
the exact files and metadata surfaces actually inspected. Source hashes must
match the existing records before and after inspection. Work locally; no new
acquisition, external upload, media decoding, image views, enhancement or
fitting. Existing historical products and annotations remain unchanged.

The collector will expose container/stream/chapter metadata via the installed
ffprobe, header-level RIFF structure and INFO fields without scanning movie
payloads, JPEG application/comment metadata without decoding pixels, and the
PDF document/image dictionaries and XMP where present. Preserve unknown fields
and report parser limits. Embedded DV packet metadata is outside this check;
absence from ordinary container tags cannot rule out timecode in the essence.
PDF creation dates describe the document, not the image exposure. Provider
normalization/omission is not provider-side absence.

Use a small read-only collector with explicit bounds and synthetic malformed-
header checks. Save its exact JSON stdout as a new research derivative. No raw
file is rewritten. Do not create a general provenance framework. The separate
documentary reviewer examines source context/catalogue pointers without media
views; a separate review checks the collector/result and proposed conclusions.

Deliver a concise lineage report, reproducible collector/output, and review.
Acceptance is an actual source-to-still pointer or a precisely bounded
non-recovery with the next discriminating record/test identified. Neither
non-recovery nor ordinary editing metadata proves concealment or validates the
underlying structural account. A qualitative fire observation requires its own
place/time/visibility resolution, not necessarily exact exposure identity.

## Inputs and boundaries

- Clip 7: `../../cbs-vince-source-screen/stage4/raw/clip7-attempt1.avi`,
  140334936 bytes, SHA256
  `a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b`.
- JPEG: `../../fire-coverage-batch3/assets/run01/images/A-7c7cc22dc34c.jpg`,
  151488 bytes, SHA256
  `68c9d384ac3b1099361f255f80a74d387073d67500089099765f4f0cf030215a`.
- PDF: `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`,
  52766002 bytes, SHA256
  `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.

Bound each external metadata command to 30 seconds. Read at most 4 MiB of
RIFF metadata payloads, at most 10000 header records, and depth 12; movie/index
payloads are skipped. JPEG file is below 1 MiB. No new image derivatives or
large products are needed. Fail visibly on unexpected structure or changed
input; retain failed checks rather than quietly accepting partial results.

All outputs stay in this investigation worktree. Main/legal records, raw
evidence, human acceptance, Sherlock/Faraday activation, feedback destination,
commit/push and disclosure status are unchanged. Full charter remains active.
