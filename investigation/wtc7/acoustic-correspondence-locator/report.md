# Acoustic correspondence: bounded search result

2026-09-20 UTC. **Neither of the two cited emails was located by this search.**
This closes the declared held-record and small public-metadata routes; it does
not establish that the records do not exist, were withheld, were destroyed, or
would contradict NIST. The [prior acoustic assessment](../nist-acoustic-detectability/report.md)
is unchanged: conditional negative evidence, with the actual-receiver detection
bridge still unverified.

Targets: the Applied Research Associates to NIST correspondence dated July31,2008,
and Loizeaux Group International to NIST correspondence dated August5,2008,
cited in NCSTAR1-9 printed357, footnotes4/5. Those citations identify concrete
records to seek, not independently available copies or verified contents.

## What was searched—and what was not

| Route | Actual coverage | Result and evidential limit |
|---|---|---|
| Intake/exhibit spines | Six specified files, including130 source-inventory,50 assignment and25 exhibit-map data rows, plus the supplementary-production audit and two locator notes. | No organization/acoustic/full-date match. Three broader date fragments were unrelated court-opinion metadata, two referring to the same item. Index rows are not unique sources. [Spine review](spine-review.md). |
| Held filename inventory | All212 paths returned with ignored files included under main `exhibits/raw`, `exhibits/processed`, `authority/nist`. | No fixed-query filename candidate. Exact inventory independently reproduced by two enumeration methods. Not a whole-repository/mailbox inventory. |
| Readable file text |101 files searched with the fixed queries;191 file paths across text/PDF/ZIP routes hashed before/after. | Two acoustic hits in text derivatives of the Fletcher declaration packet. Raw text search alone did not decode MIME or read binary data. |
| PDF text layers |81 exhibits PDFs,860 pages. Five authority publication PDFs excluded as candidate original emails; their filename inventory is retained. | Sole hit: physical76 of processed EXH-014. Five sparse-text pages are limitations, not assumed blank. No OCR/full visual reading of860 pages. |
| ZIP member names |Nine archives,25,682 member records. | No fixed-query member-name candidate. Names were read, not extracted contents. Nested/compressed data and attachments are not ruled out by this result. |
| MIME follow-up |Same94 `.eml` files;104 decoded inline text parts, including86 base64 HTML parts;48 attachment parts excluded. | Independent reviewer found no additional fixed-query hit and no decode error. No bodies, signatures or address lists printed. This closes one encoding blind spot, not attachment coverage. |
| Public metadata |Four declared searches, each restricted to NIST/National Archives domains, using only published names/dates/subject. | Combined return showed six report/public-comment locators, not a candidate original email. No exhaustive site/catalog crawl or independent document authentication. [Search ledger](public-search.md). |

The fixed query families were organization names, both complete target dates
in several common forms, and acoustic/NLAWS/audibility terms. See
[the locator](locate.py) and [preserved results](locator01.json); spelling/OCR,
raw encodings, changed dates, anonymous files and unsearched paths remain
possible failure modes. The spine route used additional broad fragments and
disposed of its actual hits rather than counting them as candidates.

## The actual positive hit

Root rendered and viewed the complete physical76 of
[processed EXH-014](/Users/admin/docs/911/exhibits/processed/exh-014-2010-04-16-dcd-quick-fletcher-declaration.pdf).
It is a **table-of-contents page**, printedvii, inside the filed declaration
packet; the page carries the court's76-of152 stamp. It lists the PhaseIII
acoustic section at report page706. It is not either email, not a reproduction
of the acoustic study, and not a new independent evidentiary source.

Both text hits are similarly acoustic contents entries. Thus the three hit
files do not represent three corroborating documents. Source PDF SHA-256:
`0b436dfe3347c5d975851a9c44cfc3336ed59521cfebeaa88438609fd4dd7992`.
The one150dpi PyMuPDF page-check image and receipt are preserved. Root made one
complete-page display, with no observed missing text or clipping and no render
warning; no full packet reading or legal interpretation is claimed.

## Coverage defects and disconfirming checks

The strongest objection to a non-location result is that the search could miss
an existing record. We tested a concrete instance:94 emails had initially been
searched in their raw stored representation. The independent decoded-inline-text
pass found86 base64 HTML parts but no added hits. That makes this route stronger
than the initial raw search; it does not make it exhaustive.

The five sparse PDF pages are raw `pro-se-info.pdf` pages1–4 and
`advanced_litigation_considerations_may_2021.pdf` page35. They were not OCRed or
visually interpreted. Four PDF paths reported repaired outline-tree structure;
warnings are retained in the results, not hidden by successful extraction.
The paths are two copies of the skepticism memo and two copies of the Abdelfattah
opinion. These diagnostics are a parser limitation, not an indication of
historical alteration or proof that any page text was missing.

The sparse-text flag is not a complete image-content detector: a searchable
header can coexist with an image-only enclosure. Successful text extraction
therefore does not establish complete content-search coverage even on the other
855 pages. The reviewer also demonstrated nine ordinary query variants that
the fixed patterns do not recognize; those are declared limitations, not new
historical hits or grounds for silently expanding the result.

The archive inventory includes26 PDF members and3 email members, but archive
contents were not searched. It also includes a nested archive and many model-data
members. No claim of complete archive-content coverage follows from member names.
Likewise, searching legal inventory rows is not searching all the documents they
describe. Official hosting of a public comment does not endorse its assertions;
no science or misconduct allegation from those search snippets was adopted.

## Verification actually performed

- The small locator ran once with explicit Python3.13.7/PyMuPDF1.27.2.2:
  `PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B research/sherlock-wtc7-investigation/acoustic-correspondence-locator/locate.py`.
  Session27076 completed exit0, no restart. Its11 known-text query assertions
  passed before source processing. No new dependencies or global settings.
- It preserved results for212 paths,191 before/after content hashes and all
  selected PDF warnings/sparse-page locators. No source change or incomplete
  parsing status was reported. Source hashing covers the read paths, not all
  filename-only content or every runtime dependency.
- The [independent locator review](locator-review.md) reproduced inventory,
  source hashes, text hits, PDF page locators/warnings and archive-name results,
  then performed the MIME follow-up. Its methods and remaining limitations are
  reported separately; it did not independently hear historical audio.
- The [spine review](spine-review.md) independently checked its six inputs and
  before/after identities; root read its complete note. No canonical spine was
  changed. The two search routes are not two historical witnesses.
- Root's later read-only check returned exit0 for the exact current212-path
  inventory, all191 current source hashes, frozen locator/script identities,
  locator AST parse and the source/PNG pins for the single full-page check.
  Root read both independent notes completely. Review hashes:
  `880b7a80a255e87b96e1ca13c9d5ccc2df2c179793df24161313cc80b5f78949`
  (spines) and
  `e0c0e47b6283c79b2ec16291fce3bbb4119a0b41e631113a48368b95e0d521b9`
  (locator). Root did not independently repeat the MIME-decoding extension.
- Locator result SHA-256:
  `905c194634c54959fc370aac541535cb38d24438676ce48631745f39511fd123`.
  Run-time protocol SHA-256:
  `0a4d8ce28b0cecf0d7ea9f40691795decaef0affbaaaa47515573f50654a6165`.
  Later visual/MIME/public-search appendices were prospective additions; the
  unchanged original prefix reconstructs that run-time protocol hash. They do
  not silently relabel the earlier search as covering the added routes.

Initial relative-path inventory commands ran in the research worktree and found
no source directories; rerunning in the declared main source repository resolved
that locator mistake. Ordinary ripgrep no-match exit1 is distinguished from a
command/read failure. One attempted note read preceded the reviewer's save;
the completed note was later read. These workflow errors are not evidence
about the historical records. No source upload, new FOIA request, outreach,
solver, media acquisition, legal promotion, commit or push occurred.
One later no-op documentation patch failed to match a wrapped line; it changed
no file and the intended substantive addition was then applied correctly.
An initial naive Markdown-link check misread a regular expression inside a
fenced command as a link. Excluding code samples corrected the checker without
editing frozen notes; the corrected read-only pass verified both review hashes,
five Markdown files and all eight local links, exit0. This is a scoped link
check, not a general Markdown parser or scientific validation.

## Disposition

Both target records remain **unresolved, not located within declared coverage**.
There is no new support for or against their reported acoustic substance.
An authenticated copy or defensible access copy, with matching correspondence
context and non-operational urban-path reasoning/data, would materially change
the available test. A broad name match or repetition of the report footnote
would not.

Do not repeat this same fixed-query route as if repetition adds evidence.
Retain the exact records as unavailable-to-this-review inputs. New catalog,
archive-content or record-access evidence could reopen the route; the current
result neither authorizes a new disclosure request nor narrows existing record
or discovery interests. Continue a different feasible charter discriminator
while this source-support limit remains explicit.
