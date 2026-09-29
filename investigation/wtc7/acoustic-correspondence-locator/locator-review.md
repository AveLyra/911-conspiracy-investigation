# Independent held-record locator review

September 20, 2026. Reviewer: `next_discriminator`. Working research only.
Main controls, the complete charter, source/evidence skills and this unit's
protocol were read. Scope was the existing three source trees and fixed
queries, with the separately declared MIME-decoding check below. This review
made no network request, OCR, page display, archive extraction, media or
solver operation, source mutation, or legal/canonical promotion. Only this
note was written. The separate spine-review route was not repeated here.

## Result

**Scoped reproduction pass; no located original, not evidence of absence.**
The file inventory, saved search results, source hashes, archive-name coverage,
PDF page counts, sparse-page list and extraction warnings reproduce. No new
candidate was found by the additional check for MIME-encoded inline email
text. This supports closing this particular held-file locator pass with its
limits recorded. It does not establish that either cited email is absent
from all holdings, never existed, is currently withheld, or was destroyed.

| Reproduced mode | Coverage |
|---|---:|
| Raw UTF-8 text search | 101 files: 94 EML, 6 TXT, 1 MD |
| PDF text-layer locator | 81 PDFs, 860 pages |
| ZIP member names only | 9 ZIPs, 25,682 member entries |
| Filename only | 21 files |
| Total inventory | 212 paths |
| Content-read source hashes independently checked before/after | 191 |

All three query-hit files have **acoustic-only** hits: the processed Fletcher
PDF at physical page 76 and its two related text versions. There are no saved
organization/date matches, filename matches or ZIP-member-name matches.
These three representations must not be counted as three independently
corroborating correspondence records. Root separately reports that its complete
view of PDF page 76 identifies a contents-page heading, not an email; this
review did not repeat that visual content classification.

## Pins and prospective protocol additions

Unit:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/acoustic-correspondence-locator`.

- `locator01.json`: SHA-256
  `905c194634c54959fc370aac541535cb38d24438676ce48631745f39511fd123`.
- `locate.py`: SHA-256
  `4d3ffd125798e557973965de08d3903536f3252783bc3b0fb4ed6157dc2dd3db`,
  matching the saved script pin.
- Recorded protocol SHA-256:
  `0a4d8ce28b0cecf0d7ea9f40691795decaef0affbaaaa47515573f50654a6165`.
  This exactly matches the current protocol's unchanged **first 4,708 bytes**.
  Root appended prospective page-review and follow-up scope sections; the
  original locator record was not overwritten to conceal that distinction.
- Current protocol at this review's check: 6,580 bytes, SHA-256
  `2c80b4b37d358ecfcb1dc49d3c5426a3a2c274188874a819fc1b40fd2007f1a1`.

The public-metadata follow-up authorized in the later protocol is root's
separate route, not part of this review's executed work. The initial relative
path failure described in the protocol remains inherited execution history;
this reviewer did not reproduce it or interpret it as source absence.

## Actual independent checks

The read-only audit ran as an inline command, without importing `locate.py`
or creating a new test framework:

`PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B -`

It exited 0. The following is its reproducible procedure, not a claim that an
additional verifier script was saved:

1. Load the frozen locator; require 212 unique paths. Verify its scope and
   inventory command against the declared trees. Execute
   `rg --files --hidden --no-ignore exhibits/raw exhibits/processed authority/nist`
   with cwd `/Users/admin/docs/911`; compare the complete path set with the
   saved rows. Independently enumerate the same three trees with
   `Path.rglob('*')`/`is_file()` and compare again. Both sets agree exactly;
   ripgrep returns 0 with empty stderr. No listed file is a symlink.
2. Derive each file's mode independently from its suffix and tree. Check each
   recorded size and filename-query result. For every content-read file, hash
   the actual bytes and require agreement with both saved before/after hashes.
   Rehash all 191 again after the audit; every hash is unchanged.
3. Read all 101 raw-text files and reproduce their fixed-query results and
   replacement-character counts. Whitespace normalization and case-insensitive
   regex matching follow the declared rule, with result order normalized for
   comparison. No source body is printed. Additional encoding indicators find
   zero UTF-16 BOM files, zero files containing NUL, and zero UTF-8 replacement
   characters in this set; these facts do not solve MIME encoding.
4. Reopen the nine ZIP central directories using `zipfile.ZipFile.infolist()`.
   Reproduce every member count, every member-name query result and each
   extension histogram. No member content is decompressed or extracted.
   The non-directory entries include 26 PDF, 3 EML, 274 PNG, 25,188 INT,
   173 NOD, 3 APDL, 6 GZ, one PPT, one PPTX, one ZIP and one extensionless
   entry. Names alone cannot establish what any neutrally named payload says.
5. Reopen all 81 eligible exhibit PDFs using installed PyMuPDF 1.27.2.2 and
   reproduce all 860 text-layer page checks, page hit lists, `<20` stripped
   character flags, and exact recorded warnings. The five authority/NIST
   publication PDFs remain filename-only as expressly declared; no earlier
   operational Appendix D pages are added to the search.
6. Confirm the runtime strings against the record: Python 3.13.7 and PyMuPDF
   1.27.2.2. Rehash the producer and verify the recorded protocol's exact
   preserved byte prefix. This checks recorded versions and present code,
   not every native dependency or historical runtime state.

The only five flagged sparse pages reproduce at main
`exhibits/raw/advanced_litigation_considerations_may_2021.pdf`, physical 35,
and `exhibits/raw/pro-se-info.pdf`, physical 1–4. Four PDFs reproduce the
warning `repaired broken tree structure in outline`; no new extraction error
or incomplete row was found. These are successful text-layer checks using
the same parser family as root, not an independent PDF renderer or proof that
all page content has a usable text layer.

## Meaningful blind spot tested: encoded email text

Code inspection found that the original pass treats EML as raw UTF-8 text.
This can miss a relevant phrase in base64/quoted-printable bodies even when
UTF-8 decoding reports no errors. The reviewer announced this specific
extension before execution; it was also added prospectively to the protocol.

Within the same 94 EML files, `email.parser.BytesParser` with the default
email policy parsed leaf parts. Parts marked as attachments or carrying a
filename were excluded; only inline `text/plain` and `text/html` parts were
decoded via their declared content/transfer encoding. HTML text was extracted
with `HTMLParser(convert_charrefs=True)` and entity-decoded. The same fixed
queries were applied, retaining only counts and any added locator labels.
No decoded body, address list or signature was printed or saved.

Results: **152 leaf parts; 104 inline text parts checked; 48 attachment parts
excluded.** The checked inline parts comprise **86 base64 HTML**, 8
quoted-printable and 10 with unspecified transfer encoding. There were **zero
decode errors and zero added query hits**. This closes a concrete raw-body
encoding gap for those inline parts and queries only; it is not a review of
the excluded attachments or a finding about their contents.

Ten synthetic expected-positive organization/date fixtures and one unrelated
negative fixture passed. Nine deliberately unsupported variants were also
confirmed as misses, including acronyms, hyphenated organization text, compact
or two-digit-year dates and ordinal dates. Those are tests of query boundaries,
not evidence that a historical document uses one of those forms. No repeated
synonym-expansion search was performed.

## Remaining limits and strongest objection

- The 21 filename-only entries include presentations, compressed/model data,
  images, extensionless/nonstandard-suffix files and the five excluded NIST
  publications. Their bytes were not content-searched or given saved content
  hashes by this locator. A filename match is not an original-document join;
  a filename nonmatch does not exclude one.
- Archive members and 48 EML attachments were not content-searched here.
  Some may also exist as separately searched extracted files, but this review
  did not establish an exhaustive payload-to-loose-file correspondence.
- The five sparse pages remain unreviewed visually by this reviewer. More
  importantly, a page with a searchable header exceeding 20 characters may
  still contain an image-only email or enclosure. The sparse-page flag is
  not a comprehensive image-only-content detector. OCR was not performed.
- The query set handles the declared ordinary variants, not every spelling,
  acronym, punctuation, extraction-order, embedded-image or encoding variant.
  A matching date alone would also be a candidate locator, not authentication.
- The complete filenames are limited to three declared trees, not the entire
  repository, user's computer, agency holdings or public record. The separate
  source-inventory/spine review is not independently certified by this note.

**Strongest objection to an absence claim:** a genuine record could remain
inside an unsearched payload, as image content, or under terminology the fixed
queries do not recognize. The appropriate conclusion is therefore: *the
specified held-file search, including the bounded inline-MIME check, located
no candidate original correspondence*. It does not change the conditional
acoustic assessment, identify misconduct, or establish model falsity. A
specific source/attachment/index join can reopen a bounded follow-up; generic
possibility alone is not a reason to cycle the same locator indefinitely.
