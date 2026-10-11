# OEM original drawing search results

October 4, 2026. Research only. The twelve selected local metadata files do
**not identify a held original M1.01, M1.07 or M4.01**, W98-7134 submission,
or an E5/SK-58 revision disposition resolving the same-segment question.
This is limited inventory coverage, not a claim that those records do not
exist locally or elsewhere. No binary contents or archive members were searched.

The search does identify a concrete next candidate: municipal
**NYC-WTC_000171753**, catalogued as a one-page `O.E.M. / 7 World Trade Center /
98-145 / fuel line route` item. Its exact official URL is already in the
selected catalog. It is a catalog lead, not a newly held mechanical drawing.
The inspected context does not establish its date, author, contents or
relationship to E5. No collapse-cause ranking changes.

## Located records and exclusions

| Metadata location | Disposition and evidence limit |
| --- | --- |
| Catalog lines 36, 76, 97; NYC-WTC_000173900 / FSK-58 | Repeated catalog references to one source already acquired and reviewed in the structural followup, not three corroborating sources or a newly found disposition. |
| Catalog lines 80, 101; NYC-WTC_000172233 | Catalog reference to the already held E5 framing source. Its design relationship to SK-58 remains unresolved. |
| Catalog line 82; 5576A | Reference to already reviewed NYC-WTC_000172166 inspection-request material. It is not an approval or installed-state certificate. |
| Catalog lines 18 and 67; OEM | Collection/topic description and a citation to NIST's report, not underlying originals. |
| Equipment SELECTION line 18; OEM | A prospective page-reading supplement for NCSTAR1-1J, not a drawing inventory or new original. |
| Catalog lines 87 and 108; O.E.M., 98-145, NYC-WTC_000171753 | Fuel-line-route lead with an exact official URL. No original read in this metadata unit. |

The report-source PDF and the two already reviewed municipal PDFs were located
and hash-checked again; this was a byte-identity check, not a rereading or new
historical authentication. Their source hashes remain:

- NCSTAR1-1J, 578804 bytes: `7b1fe2a7a94a67c54fdaabe27e3309b439551512cff97e5026e0b62bb51bf623`.
- NYC-WTC_000172233, 145877 bytes: `0c1a0d8ea7c269d297e1d5374c4fa2118b848293a8f6cf49c263c82a6830b3f1`.
- NYC-WTC_000173900, 107823 bytes: `6dac8359d2f3c9ea98721c1b69f55038838d6755ea806d114cd55ff0b81d86df`.

The equipment inventory manifest explicitly inventories **39 generated
artifacts**, not 39 original equipment drawings. The other source manifest has
94 entries spanning existing sources, render dependencies and local derivatives.
Neither is an archive-wide inventory of original construction documents.
The two CSVs have 143 and 25 logical data rows respectively, with no unequal
row widths under Python's CSV reader. Schema/row checks do not authenticate
the entries or establish comprehensive holdings.

No confidentiality-marked court packet, unrelated correspondence, raw archive,
unindexed file or model payload was opened. The Salomon E-5 versus OEM E5
distinction remains a required identity check; neither search produced an E5
token hit in the selected metadata. This is not proof E5 drawings are absent:
the already held municipal E5 source is catalogued by title instead.

## Complete search coverage

File numbers are the exact paths in the frozen [protocol](PROTOCOL.md).
All twelve were present. Counts are matched token occurrences, not documents,
logical rows or independent evidence. Both passes matched only files 3 and 7.
The supplemental pass overlaps the first and must not be added as new evidence.

| File | Bytes | Initial tokens | Supplemental tokens | SHA-256 |
| ---: | ---: | ---: | ---: | --- |
| 1 | 85213 | 0 | 0 | `ae60fc8c4fbe9cfa6771f013b4ab974871e53893ca9fcfa1c729bd9b38081332` |
| 2 | 8186 | 0 | 0 | `2d1e61b551d5adf83ff07be57703fa9db3e316248305b5ca1b7838580b3176a9` |
| 3 | 17737 | 12 | 7 | `01f7419ec36c6686ac154c6f6e05e3309d90704069957119cfc9efb8160bc3ea` |
| 4 | 6207 | 0 | 0 | `cde7bc4bc8b783dcf61a05ef2327b145d877732cfdad9dbdd89bce979a5d5185` |
| 5 | 7637 | 0 | 0 | `0ff5707df1bcee9fb9547043ae4266b2ca3c0e87b550215bfdadf8debd942c8f` |
| 6 | 28182 | 0 | 0 | `ce748a582152d8c69a16d5bd73b0314ff5bf9f2bf9a6cb5d593df5fe0119dc2b` |
| 7 | 2757 | 1 | 1 | `85a8ee9695d59891786835d0892433a59f6e24e1618318f173641ba42f254e9c` |
| 8 | 3713 | 0 | 0 | `56ad50fd4a7bffb2cb454eedb8bf258fd74f0c4212eb3e034d10f40ed32564f5` |
| 9 | 6499 | 0 | 0 | `f2a596e49ae34dbbb598adfb96ea7efb4a70545e67961ce2a0bb816b52dd99a2` |
| 10 | 2947 | 0 | 0 | `736b8d665a424a3d4c4d1da9a9d4c274391570fbb4eeb41f8f995a37a998c893` |
| 11 | 4847 | 0 | 0 | `fe093ddad2280b5969742e48dc5c55d905d42f94b711ecd152c4c5c5fcdc3a85` |
| 12 | 2072 | 0 | 0 | `46e51b8ebd8ebb8e1866d55a953a95ebba0a2d085cee7f893f956e9033268bb7` |

The original pass missed the punctuated `O.E.M.` form. Root encountered it
in the catalog context and saved the [supplement](SUPPLEMENT.md) before the
second pass. This is a disclosed adaptation, not a claim of blind search.
Both searches use `rg --multiline -n -o -i -P PATTERN FILE`:

```text
Initial:
(?<![A-Za-z0-9])(?:M[\s._-]*1[\s._-]*0[17]|M[\s._-]*4[\s._-]*01|W[\s._-]*98[\s._-]*7134|E[\s._-]*5|F?SK[\s._-]*58|5576[\s._-]*A|OEM|(?:NYC[\s._-]*WTC[\s._-]*0*)?(?:172233|173900))(?![A-Za-z0-9])
Supplement:
(?<![A-Za-z0-9])(?:O[\s._-]*E[\s._-]*M|98[\s._-]*145|(?:NYC[\s._-]*WTC[\s._-]*0*)?171753)(?![A-Za-z0-9])
```

## Actual verification and limits

Root used bundled Python 3.12.14 for a stdout-only wrapper and `ripgrep 15.2.0`.
The wrapper extracted all twelve numbered paths from the protocol, hashed
each before search and checked every `rg` return code. Exit 1 meant no match;
no command error was recoded as absence. All search stderr streams were empty.
Initial wrapper session58339 completed exit0 (receipt e2ad24); supplemental
search and CSV structure check completed exit0 (d045bc). Source and manifest
identity check completed exit0 (c71928). No inventory was edited or exported.

Protocol SHA-256: `b9be45ee200520371986504fe60fb5842ba2e47953c150f4c3a1cef9e3627cf6`.
Supplement SHA-256: `f85c634c1cc4d83b586359ab8efbea4a305660fb7f85e279aa8bd2888930c9a1`.

The [independent rerun and draft review](review.md) reproduced all twelve
metadata pins, search counts and classifications, then independently checked
the CSV and manifest aggregates. No material correction was needed. Its
slightly broader separator/zero-padding forms yielded no additional match.
It checked the three held PDFs by file size and prior provenance receipts,
not a fresh binary hash; root's fresh three-PDF hash check remains separately
attributed. Review SHA-256:
`2cf68b4b0d81bd290d9f51acb7775cf61faa03f0f9882053b02c11d5f25aa238`.
This is computational checking, not independent historical or human acceptance.

The strongest objection to a broad negative finding is concrete: our known E5
source exists even though these metadata do not contain an E5 token. Different
labels, unindexed drawings, scanned contents, archive members and holdings
outside this selection can defeat this search. Therefore the grade-A finding
is only the bounded metadata result; original-record availability remains
underdetermined. Missing metadata is not evidence of concealment.

## Next source test

The separately declared [fuel-route followup](../fuel-route-followup/report.md)
has now acquired and read the exact one-page NYC-WTC_000171753 candidate from
the official address in the catalog. Its findings belong in that source
review, not retroactively in this metadata search. Do not infer M1.01 contents
from the catalog label or guess adjacent attachments. The original mechanical sheets, E5/SK-58 disposition,
beam/Change Order 23, sprinkler and installed-state questions remain distinct.

This naming/source-role issue is covered by existing SFB-005 catalog fixtures;
no separate product defect or fix is established. Feedback stays local under
the archived-destination boundary. No main/legal edit, transfer, fee, stage,
commit or push. Full goal remains active and incomplete.
