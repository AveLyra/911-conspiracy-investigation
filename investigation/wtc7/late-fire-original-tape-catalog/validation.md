# Retrieval and verification record

2026-09-20 UTC. Research-only; no video acquisition or scientific measurement.
No tests here establish a collapse mechanism, current record withholding,
camera-master provenance or human specialist acceptance.

## Current-source reads

All nine Drive calls have exact request and normalized response JSON under
sources/: six list_folder calls, two get_file_metadata calls and one bounded
text fetch. Each envelope says isError:false. The full General listing is
200,598 saved JSON bytes; its large console display was truncated, so later
count/name/identity checks used the complete saved JSON, not the displayed
fragment. Metadata bodies do not retain independent provider request IDs or
execution timestamps; scope timing is the actual tool/patch history, not an
extra server attestation.

The [independent audit](independent-provenance.md) retains the complete read-only
Python command for all18 JSON files and22 source/scope pins. Root read that
command fully, extracted its sole shell-embedded Python block and reran it from
the worktree root with bundled Python, without optimization: exit0, PASS.
Counts282 rows/282 IDs/281 titles and all path/metadata joins match. This is a
rerun of the separately written audit, not a third independent method.

The [web-search ledger](crosswalk-search.md) retains four exact queries and
eight distinct primary URL attempts (five readable, three browser-size
failures). No source media was obtained by that agent. The later PDF read was
declared separately in READ-SCOPE-04, not silently added to its search cap.

## Exact PDF acquisition and inspection

Runtime: bundled Python3.12.14, pypdf6.10.0, Pillow12.3.0; dependency bundle
26.905.11957. Executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
The bundled pdfinfo/pdftoppm wrappers are not asserted to be native Poppler:
their SHA-256 values are respectively
`fee70ade670fb025343aca2b5c3a2aacacb8ed9edce1b716b233b5de924b6bf5`
and `de772e88ab9977ccde25def9b403bf42675d75f5dd82b19fbd7d8123ad183159`.

From this unit's absolute directory, the actual acquisition was:

```sh
curl --fail --location --max-redirs 3 --proto '=https' --proto-redir '=https' --max-time 55 --max-filesize 25000000 --no-clobber --silent --show-error --output sources/nistspecialpublication1000-5v4.pdf --write-out 'http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1000-5v4.pdf
```

Handle88097 completed exit0, HTTP200,18,342,113bytes, final URL unchanged.
No retry or overwrite. `shasum -a 256` and bundled `pdfinfo` returned0; hash
`19281ca238382466a4a0029784d4789fb78cf4d8e4785ac49370c01f9aa94433`.
The container has224 pages, PDF1.5, no encryption, title Progress report on the
Federal building and fire safety investigation of the World Trade Center
disaster. Embedded metadata identifies2015 digitization/re-encoding; cover
identifies June2004 report publication. Neither is a camera-event timestamp.

Using bundled Python/PyPDF, root called extract_text on every page and searched
the exact regexes preserved in pdf-text-scan.json. That JSON retains the first
12 page texts (up to9,000 characters each) and match contexts, not every page's
full text or every visible character. The initial boundary-sensitive CBS
expression missed concatenated text. A separate literal search over all224
pages retained that limitation and found CBS on9,12,42,145,154; Dub5 and
Dub-space-5 had no match. WTCI/TapeID/Derivedfrom hits and misses are not a
validated archive crosswalk; visible screenshot fields can be absent from OCR.
Both extraction commands exited0. The complete relevant page images control
the schema readings, not these noisy negative keyword results.

Actual render commands (bundled pdftoppm wrapper):

```sh
pdftoppm -f 145 -l 148 -r 110 -png sources/nistspecialpublication1000-5v4.pdf sources/sp1000-5v4-schema
pdftoppm -f 156 -l 156 -r 110 -png sources/nistspecialpublication1000-5v4.pdf sources/sp1000-5v4-timing
pdftoppm -f 1 -l 1 -r 110 -png sources/nistspecialpublication1000-5v4.pdf sources/sp1000-5v4-cover
pdftoppm -f 150 -l 155 -r 110 -png sources/nistspecialpublication1000-5v4.pdf sources/sp1000-5v4-attributes
```

The first three commands ran in one shell invocation whose final status was0;
their individual exit statuses were not retained. The fourth ran separately
and returned0. All12 expected output images exist and were inspected. This
does not substitute a combined shell status for three independently checked
command statuses.

Root and another AI reviewer each individually displayed all12 complete PNGs
at original detail: PDF1,145–148,150–156. The observer's initial six-page section
was retained unchanged before appending the additional six-page inspection.
Root's initial and follow-up notes were saved before the observer's substantive
results arrived; both knew the source and the earlier search lead. No claim of
blind discovery, independent historical source or all224-page visual coverage.
The observer independently rehashed source/PNG bytes and recorded them in
pdf-schema-review.md. No rendering repeat or independent PDF renderer is claimed.

## Failures and authority boundaries

Root first guessed an HTML filename that did not exist; it listed actual files
and used nist-repository.html. A nested-AGENTS filename search returned no matches,
not a failed inspection of an existing instruction. pdftotext was not found;
the available PyPDF extraction and bundled rendering route was used instead.
The independent audit records an unsupported head option and an overly narrow
preliminary title pattern, corrected before its completed checks. None was
treated as source absence or a waived failed scientific test.

All acquired media/document sources, original reports and frozen observations
from preceding units remain unchanged. Current notes are research derivatives.
No SRC/FACT promotion, legal amendment, engine acceptance, outside transmission,
commit or push. Whole-goal acceptance is still incomplete.

Actual record-spine check: `python3 /Users/admin/docs/911/tools/validate_record.py
--strict`, invoked from the investigation worktree, returned0 with
`OK (headers + issue↔fact links + citation tags)`. It does not validate the
physical conclusions or approve legal promotion.

## Final mechanical checks and review-version boundary

The final inline Python check parsed19 JSON files (18 request/response files
and the PDF text scan), checked whitespace in13 Markdown files, and resolved12
local links. It also verified the PDF's size, SHA-256 and224-page count; all12
PNG hashes against the observer's record, formats and dimensions; and the
unchanged11,645-byte prefix of the observer's initial review. It exited0 with
PASS. These are artifact-integrity checks, not validation of the collapse
mechanism or historical camera timing.

`git diff --check -- research/README.md
research/sherlock-wtc7-investigation/STATUS.md
research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md` returned0. The
research branch and HEAD were rechecked as
`research/sherlock-wtc7-investigation` / `e8d83d7`.

The critical review pins an earlier report snapshot. An attempted byte-level
reconstruction by removing only the later two validation-navigation lines
failed, including simple adjacent blank-line variants. The reviewer then
identified a second two-line addition describing the separate PDF review and
observation chronology. Removing both additions (four lines /317 bytes) in
memory reconstructs the exact earlier SHA-256
`7afa6a47ef00f2d76f33a62e196f1c91676d1d5038d5ce64de4bbfd70d1dffba`.
Root independently repeated that reconstruction successfully. The current
report remains unchanged at SHA-256
`05dd451f058578137c32ae02f6782afdb127e7df2f7cfda3dd7adc7e18e3e203`.
The chronology addition is not merely navigation; the fresh full current-text
review and its limits are preserved in the append-only critical-review record.

A repeated artifact check initially rejected a valid local link because its
`:499` line suffix was treated as part of the filename. After explicitly
stripping only a terminal colon-and-digits line locator, the same check exited0:
19 JSON,13 Markdown files,12 local links, the pinned PDF and12 PNGs, and the
initial observer prefix all passed. No source, link or acceptance requirement
was changed to obtain that result.
