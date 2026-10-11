# Independent metadata locator review

October 4, 2026. Research only. All twelve selected metadata files were present
and searched completely. The initial query returned 13 token occurrences on
9 distinct physical lines; the separately declared supplement returned 8
occurrences on 5 lines. Each pass matched only the catalog-lead memo and the
equipment-source reading selection. Ten files had zero matches in both passes.

No selected metadata identified a held original of OEM M1.01, M1.07, M4.01
dated March 29, 1999, or W98-7134. The supplemental NYC-WTC_000171753 /
98-145 result is a catalog fuel-route lead, not a verified mechanical sheet,
revision disposition or installed-state record. This conclusion is limited
to the declared metadata and queries.

## Scope and independence

Read the full current main CHARTER, AGENTS and WORKFLOW, and this unit's
PROTOCOL before searching. Source metadata remained read-only. Root notified
this checker of the punctuated-OEM variant after the initial search; the full
SUPPLEMENT was then read before the separate supplemental pass. This is an
independent rerun and classification check, not a blinded search or an
independent historical witness. The later root-draft review is recorded below.

Control pins:

- PROTOCOL: `b9be45ee200520371986504fe60fb5842ba2e47953c150f4c3a1cef9e3627cf6`.
- SUPPLEMENT: `f85c634c1cc4d83b586359ab8efbea4a305660fb7f85e279aa8bd2888930c9a1`.
- Main CHARTER: `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
- Main AGENTS: `934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857`.
- Main WORKFLOW: `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`.

## Exact coverage

Paths below are relative to `/Users/admin/docs/911`. Counts are token
occurrences from the initial/supplemental queries, not independent records or
CSV logical rows. All hashes were checked before/after and were unchanged.
Total coverage: 175997 bytes, 1269 newline counts, twelve distinct metadata
artifacts. There were no missing files or unreported coverage gaps within this
list. The files are not twelve independent primary sources.

| ID | Selected path | Bytes | Initial / supplement matches | SHA-256 |
| --- | --- | ---: | ---: | --- |
| F01 | `intake/source-inventory.csv` | 85213 | 0 / 0 | `ae60fc8c4fbe9cfa6771f013b4ab974871e53893ca9fcfa1c729bd9b38081332` |
| F02 | `exhibits/index/exhibit-map.csv` | 8186 | 0 / 0 | `2d1e61b551d5adf83ff07be57703fa9db3e316248305b5ca1b7838580b3176a9` |
| F03 | `research/WTC7_archive_leads_2026-09-16.md` | 17737 | 12 / 7 | `01f7419ec36c6686ac154c6f6e05e3309d90704069957119cfc9efb8160bc3ea` |
| F04 | `research/sherlock-wtc7-investigation/fuel-system-audit/source-log.md` | 6207 | 0 / 0 | `cde7bc4bc8b783dcf61a05ef2327b145d877732cfdad9dbdd89bce979a5d5185` |
| F05 | `research/sherlock-wtc7-investigation/fuel-system-audit/nist-source-review/source-log.md` | 7637 | 0 / 0 | `0ff5707df1bcee9fb9547043ae4266b2ca3c0e87b550215bfdadf8debd942c8f` |
| F06 | `research/sherlock-wtc7-investigation/fuel-system-audit/nist-source-review/source-manifest.json` | 28182 | 0 / 0 | `ce748a582152d8c69a16d5bd73b0314ff5bf9f2bf9a6cb5d593df5fe0119dc2b` |
| F07 | `research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/SELECTION.md` | 2757 | 1 / 1 | `85a8ee9695d59891786835d0892433a59f6e24e1618318f173641ba42f254e9c` |
| F08 | `research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/inventory-review/SELECTION.md` | 3713 | 0 / 0 | `56ad50fd4a7bffb2cb454eedb8bf258fd74f0c4212eb3e034d10f40ed32564f5` |
| F09 | `research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/inventory-review/artifact-manifest.json` | 6499 | 0 / 0 | `f2a596e49ae34dbbb598adfb96ea7efb4a70545e67961ce2a0bb816b52dd99a2` |
| F10 | `research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/acquisition-log.md` | 2947 | 0 / 0 | `736b8d665a424a3d4c4d1da9a9d4c274391570fbb4eeb41f8f995a37a998c893` |
| F11 | `research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/installed-records/source-log.md` | 4847 | 0 / 0 | `fe093ddad2280b5969742e48dc5c55d905d42f94b711ecd152c4c5c5fcdc3a85` |
| F12 | `research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/errata-review/SELECTION.md` | 2072 | 0 / 0 | `46e51b8ebd8ebb8e1866d55a953a95ebba0a2d085cee7f893f956e9033268bb7` |

## Literal query rules and receipts

Actual search command form was `rg -n -o -i -U --pcre2 PATTERN`, with every
one of F01-F12 passed explicitly as a file argument. Separate count checks
used `rg -c --include-zero -i -U --pcre2 PATTERN` with the same exact list.
No directory argument or recursive content search was used. Initial pattern:

```regex
(?<![[:alnum:]])(?:M[[:space:]_.-]*1[[:space:]_.-]*(?:01|07)|M[[:space:]_.-]*4[[:space:]_.-]*01|W[[:space:]_.-]*98[[:space:]_.-]*7134|E[[:space:]_.-]*5|(?:F[[:space:]_.-]*)?SK[[:space:]_.-]*58|5576[[:space:]_.-]*A|(?:NYC[[:space:]_.-]*WTC[[:space:]_.-]*)?0*(?:172233|173900)|OEM)(?![[:alnum:]])
```

Supplemental pattern, after reading the new declaration:

```regex
(?<![[:alnum:]])(?:O[[:space:]_.-]*E[[:space:]_.-]*M|98[[:space:]_.-]*145|(?:NYC[[:space:]_.-]*WTC[[:space:]_.-]*)?0*171753)(?![[:alnum:]])
```

Both use case-insensitive alphanumeric boundaries, optional whitespace,
underscore, period or hyphen between components, and multiline matching.
Municipal numeric IDs allow the known prefix and zero padding. Dates were
not searched broadly. The initial OEM term is literal; the supplement covers
the punctuated form. The literal supplemental token returned is `O.E.M`
(the source displays a following terminal period).

Actual terminal receipts, all exit 0:

- Initial tokens `e32f34`; counts `e841fd`: F03 12 occurrences on 8 lines,
  F07 1 occurrence on 1 line.
- Supplemental tokens `613172`; counts `87322a`: F03 7 occurrences on
  4 lines, F07 1 on 1 line. Three literal OEM occurrences repeat initial
  hits; supplemental counts must not be added as new independent evidence.
- `shasum -a 256`, `wc -c`, and `wc -l` on the same twelve explicit paths:
  `60e4de`. Final twelve-file hashes: `ab51b4`, UTC 18:11:59.
- Bounded numbered Markdown context: `5675fc` and `fe5fc3`. No matching
  CSV rows existed; no row values were disclosed. The initial search needed
  no CSV parsing; aggregate schema checks for the later draft review are below.

## Matched locations and dispositions

| File and physical line(s) | Literal match(es) / useful public identifier | Classification and limit |
| --- | --- | --- |
| F03:18 | `OEM` | General catalog collection context; not a held drawing. |
| F03:36,76 | `NYC-WTC_000173900`; `FSK-58` / `fsk-58` | Catalog lead for a two-page revised-sketch item. The selected September 16 memo does not itself prove acquisition, included attachments, approval or execution. |
| F03:97 | `NYC-WTC_000173900` twice | Link text plus URL for the same catalog item; not two records. |
| F03:80,101 | `NYC-WTC_000172233` once, then twice | Catalog enclosure-framing-plan entry and repeated link/URL. They do not identify the requested March 1999 original mechanical sheets. |
| F03:82 | `5576A`, associated with `NYC-WTC_000172166` | Catalog inspector-request lead, two pages. A project identifier does not establish an inspection result, accepted correction or same piping segment. |
| F03:67 | `OEM` | NCSTAR 1-1J report citation, printed 27 / physical 61. A report assertion/citation is not its underlying engineering record. |
| F07:18, with source declaration at F07:5 | `OEM` | Reading/derivative selection for the held NCSTAR 1-1J access copy; not an original mechanical-sheet inventory. |
| F03:87, supplemental | `NYC-WTC_000171753`, `O.E.M`, `98-145` | One-document/one-page catalog fuel-line-route lead. Candidate for a separately scoped official-source retrieval; no acquisition or primary-content reading in this check. |
| F03:108, supplemental | `NYC-WTC_000171753` twice | Catalog link and URL for the same item; no additional source or corroboration. |

F07's public PDF path was checked only with
`stat -f '%N bytes=%z type=%HT' research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/sources/ncstar-1-1j-attempt02.pdf`
from main: regular file, 578804 bytes (`a82406`, exit 0). Its identity/hash
here is the selection's metadata assertion; no binary was opened or hashed
in this task. No candidate original mechanical sheet was located for a new
existence/identity check. The selected manifests' zero matches do not establish
that their derivatives are original source drawings.

Initial tokens M1.01, M1.07, M4.01, W98-7134 and E5 had no matches. No unrelated
Salomon E5 hit was observed within this selection; an E5 reference elsewhere
must still be assigned to its actual system before an OEM join. Standalone
SK-58 did not occur; the two sketch-token matches were FSK-58/fsk-58.

## Limits and next discriminator

The strongest reason this could miss a held original is that an inventory may
omit sheet numbers, use another naming form, point to a scanned collection,
or omit an unindexed holding. The actual punctuated O.E.M. miss demonstrates
one naming limitation; its correction does not make the search exhaustive.
No finding of global absence, destruction, concealment or no further records
is supported. No inference about physical installation or a common segment
follows from these identifiers.

The concrete next candidate within the observed metadata is the one-page
NYC-WTC_000171753 / 98-145 route item, with complete-source identity and content
review separately declared before retrieval. It may be only a cover or may
fail to join the sheets. The original M1.01/M1.07/M4.01 revision set,
W98-7134 disposition, Change Order 23/beam sketch, sprinkler and installation/
inspection dependencies remain unresolved by this search.

No confidential Aegis packet, unrelated correspondence, archive or binary
contents were read; no network, OCR, acquisition, canonical write, old-output
overwrite, engine action, external transfer, staging, commit or push occurred.
Only this new review note was written. No technical or human acceptance is
claimed.

## Root-draft verification

Read the complete 119-line `report.md` at SHA-256
`b0b186d895f048360d3df8e72e54b8a5f56fa322e07d9fdc9bdf5b583321b116`
(`d93af3`, exit 0). Its twelve metadata sizes/hashes, per-file counts, match
locations, catalog/report/derivative distinctions and bounded negative result
agree with the independent checks above. No material factual correction is
required within this checked scope. The independent regex was slightly
broader for separated F-SK and unprefixed zero-padded IDs; that produced no
additional match and does not change the declared coverage.

For the draft's additional aggregate claims, a stdout-only Python `csv.reader`
pass over just F01 and F02 used `open(newline='', encoding='utf-8')`, counted
data rows and compared each width to its header. No row values were printed.
Results (`e7bf80`, exit 0): 143 data rows / 11 fields / 0 unequal widths for
F01; 25 rows / 8 fields / 0 unequal widths for F02. These are schema/count
checks, not authentication or an assertion of complete holdings.

`jq` inspection of the two selected manifest objects returned 94 entries in
F06 and 39 in F09 (`253cc3`, exit 0). The latter's scope explicitly says
generated artifacts; the former describes local bytes/dependencies without
acquisition authentication (`1f292c`, exit 0). Those counts do not represent
94 or 39 original construction drawings.

`stat -f '%N bytes=%z type=%HT'` on the draft's three exact public PDF paths
confirmed regular files of 578804, 145877 and 107823 bytes respectively
(`482a65`, exit 0). The draft's three hash strings agree with this checker's
earlier independent provenance/derivation receipts. No fresh PDF hash or
content read was performed in this metadata task; root's additional fresh
binary-hash execution claim is not independently replayed here.

Root separately reported beginning the 171753 acquisition follow-up. This
review does not inspect that new source or recast its contents as a metadata
finding. The inventory report records the catalog-lead state of this unit;
any later acquisition or reading belongs in that separate prospective unit.
Root may finalize the independent-verification status without treating this
AI review as human acceptance or authorization for another action.
