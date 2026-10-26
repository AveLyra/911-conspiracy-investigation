# Scope, provenance, verification and disclosure

26 October 2026. Source downloads are exclusive writes. URL, UTC access time,
HTTP status/content type, final URL, length and SHA-256 are preserved. Failures
remain failures. A source hash identifies the downloaded bytes; it does not make
their statements true or establish that they reproduce every originally held record.

## What was actually inspected

Eleven source responses were acquired; two retrievals failed. The source ledger
includes non-evidentiary portal snapshots as well as seven PDFs. Acquisition of an
entire packet is not a claim to have substantively read its every page.

Native PDF text was extracted for the two FBI EO packets, plaintiffs' averment,
two KSA briefs and the congressional release. The congressional scan had no native
text. OCR processed79 pages (Joint Inquiry34; September 2003 FBI release26; July 2007
EC19), then65 selected supplemental-release carrier pages164–228. OCR is a fallible
local derivative; rendered source pages control a transcription claim. Scans that
yielded only a Bates string to native extraction contained substantive visible
material, including actual carrier bills. A PDF text search cannot establish that
those records are absent.

The review is targeted: bank/check and repayment passages, original interview
continuations and attachment references, the2005 call tables, the2007 enclosure
description, the cited averment paragraphs and KSA's attribution objections, and
the selected original-carrier return/bills. Specific image-inspection pages and
derivative scope are listed in [READING-SCOPE.json](READING-SCOPE.json). Rendering,
OCR, reading and factual verification are separate operations.

The downloaded averment has566 physical PDF pages. On its first page it carries
the **9541-1 page1-of566** stamp and **10199-1 page2-of567** stamp. Therefore its
physical p.416 is printed p.415, 9541-1p.416 and10199-1p.417. These pagination layers
are retained, not described as missing substantive text or tampering. Browser
`#page=` links here refer to physical pages of the acquired PDF; future server
versions could differ. The SHA-256 anchors the version used.

The September 2003 collection includes an August 18 transcription cover for the
August 4–6 interview, followed by selected continuations including printedpp.5–7.
It is not treated as a complete unbroken FD-302. The July 2007 memo names an
enclosure; acquiring its cover does not establish receipt of the whole enclosure.

## Reproducible, limited calculations

[recount_calls.py](recount_calls.py) takes the pinned Part5 PDF and extracts dated
rows on physicalpp.35–37. It emits67 rows total,27 in the inclusive December 6, 1999
through February 4, 2000 window:21 containing BAYOUMI#2 and6 containing BAYOUMI#4.
Its output [CALL-ROWS.json](CALL-ROWS.json) preserves row text, source page and
extracted-text line. This checks a printed-table count, not unique calls or speakers.
It does not silently change the averment's22 count or reconstruct its selection rule.

The manually reviewed AT&T sample contains eightJune23, 2000 detail rows: sixSaudi
Arabia, twoUK. Printed billed durations are1,1,1,3,11,17,4,4minutes, summing42;
the usage summary also says eight/42:00. This is one carrier-record chain. We do
not label bill durations as measured conversation lengths or identify redacted
recipients. A positive sample match does not validate all FBI or litigant analyses.

[verify_public.py](verify_public.py) checks manifest bytes, required record sections,
local link targets, counts, the eight-row arithmetic and the allowed public file
types. These are preservation/package checks, not a determination of historical
cause, legal admissibility, completeness of releases or anyone's intent.

## Preservation, versions and publication

Old sources remain byte-identical; the five preceding acquired sources were
rehash-checked. Earlier public documents are referenced at preserved commit
`7c13591e60d5c07ee176184cd834374b31f3e145`. The public publication base was advanced
normally to already-published main commit`41f8bb08b7e38d3d49d07c6dbb5212d7b65b8f92`,
preserving the other additive investigation. This tranche uses a new directory;
no prior file, finding, baseline identifier or published commit is replaced.

Each new text has a saved Git diff against `/dev/null`; unchanged-document status
is explicit. Draft revisions, if any, are preserved locally with their text diff
and explained in EDITORIAL-CORRECTIONS.json. Factual corrections to our own draft
are distinct from resolving a source conflict. PDF/image checks are separate from
these text diffs.

The public payload is reviewed research prose, small non-identifying field
transcriptions, URLs/hashes and reproducibility code. Raw PDFs, full OCR,
carrier/account identifiers, third-party personal/contact details, private case
records, correspondence, signatures, credentials and litigation strategy are not
included. The acquired source bytes remain in the research worktree, distinct
from this public mirror; this publication does not claim a remote backup of those
entire source binaries.

Only this run's additions are staged. Commit author/committer, authenticated
AveLyra account, exact PUBLIC destination and current remote branch are checked
before a normal push using the documented ghave/gitave helpers. Remote commit and
file bytes are verified afterward, with a separate local publication receipt.
Preparation, local commit and remote publication are never equated. No outreach,
FOIA filing, private push, overwrite, history rewrite or deletion is part of this
tranche.
