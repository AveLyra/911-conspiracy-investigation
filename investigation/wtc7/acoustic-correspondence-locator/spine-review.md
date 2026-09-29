# Bounded intake/exhibit-spine locator review

2026-09-20. Research-only, local read-only source search. **Neither target email,
nor a candidate source/exhibit join to it, was located in the six declared
spine/locator files searched below.** This is not a whole-repository finding,
an archive-content search, or evidence that either email does not exist.

Targets are the Applied Research Associates → NIST correspondence dated
July 31, 2008, and Loizeaux Group International → NIST correspondence dated
August 5, 2008, cited by NCSTAR 1-9 printed p. 357. A report footnote, later
paraphrase or matching name alone would not be the underlying email. No such
candidate or citation hit appeared in this limited route.

## Authority and boundaries

Read the entire local PROTOCOL.md, main AGENTS.md, WORKFLOW.md, START-HERE.md,
and complete research CHARTER.md, plus source-of-truth-guardian and
evidence-falsification-auditor skills. Their practical effect here was to leave
canonical spines untouched, distinguish indexed metadata from actual source
documents, and qualify non-location by demonstrated search coverage.

Protocol SHA-256:
`0a4d8ce28b0cecf0d7ea9f40691795decaef0affbaaaa47515573f50654a6165`.
Fresh main-control hashes:

- AGENTS.md: `0bfca4efc4e9eabdaa895f7268407bb7a47c0ecc2a4599d957454cd0623c2aa8`
- WORKFLOW.md: `17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a`
- START-HERE.md: `30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72`
- CHARTER.md: `54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`

Only this new working note was written. No main/raw/legal/canonical file,
accepted state, existing research result or source was changed. No network,
acquisition, outreach, broad repository search, PDF opening, archive inspection,
media, model execution or operational derivation was performed by this reader.
Root separately owns the declared raw/processed/authority and archive/PDF routes;
their coverage and results are not asserted by this note.

## Exact searched scope and integrity

All paths in this table are relative to `/Users/admin/docs/911`.
Both `rg --files exhibits/index -g '*.csv'` and the repeat with
`--hidden --no-ignore` returned exactly the two index CSVs shown below.
All six full file contents were searched with the patterns below; this is not
a claim to have substantively read every unrelated inventory description.

| File | Bytes | Newline count (`wc -l`) | Parsed coverage | SHA-256 before and after search |
|---|---:|---:|---|---|
| `intake/source-inventory.csv` | 75,287 | 131 | 130 CSV data rows | `3c5edb80cae7da063c6ca1f1c25b33696df32df5aac2e594a90ca907a0a2964d` |
| `exhibits/index/exhibit-assignment-log.csv` | 22,596 | 51 | 50 CSV data rows | `e5016b6fffdd037410cdaa6dca1171424333458bf326963b62307e8b054e41e0` |
| `exhibits/index/exhibit-map.csv` | 8,186 | 26 | 25 CSV data rows | `2d1e61b551d5adf83ff07be57703fa9db3e316248305b5ca1b7838580b3176a9` |
| `intake/audits/2026-09-11-supplement-integrity.json` | 56,512 | 2,066 | 7 recorded archive members; metadata/text searched | `bef3e413bf02060782568e58bfab77bdb0e64b5ed59ba04dc0d6882c6d4f79f2` |
| `intake/to-process.md` | 864 | 23 | Full text searched | `bb2f3406bb47059fdb9abae99d02774879df369a99f41c351c1f5fbefd49b430` |
| `intake/missing-documents.md` | 6,036 | 61 | Full text searched | `197efe8eabf7a6d235ff7beb5004df0bf0170a1fb1acac8de06efcc821932eeb` |

Totals: 6 files, 169,481 bytes, 2,358 newline characters; 205 parsed CSV data
rows across the three CSVs. The newline counts are not independent document
counts. No before/after hash changed.

The integrity JSON reports 7 members, 6 gzip files, no duplicate member names,
all extracted/member-integrity checks passing, and no gzip cap reached in its
earlier audit. Its inspection policy describes bounded streaming checks, not
model/script execution. These are **the saved audit's reported results**;
this task did not repeat decompression, verify the archive itself, or inspect
model data. Searching that JSON does not search every byte in the archive it
describes and does not turn the earlier audit into an email index.

## Searches actually run

Working directory for all following search commands: `/Users/admin/docs/911`.
Commands emitted only matched terms, line numbers and paths, avoiding a dump
of unrelated correspondence or inventory notes.

### Organization/acoustic sweep

```sh
rg -n -i -o -- 'loiz(eaux|aux)|applied[[:space:]_-]+research([[:space:]_-]+associates)?|\bARA\b|\bLGI\b|nla(ws)?|acoust[a-z]*|audib[a-z]*|sound[a-z]*|blast[a-z]*|propagat[a-z]*|microphon[a-z]*' intake/source-inventory.csv exhibits/index/exhibit-assignment-log.csv exhibits/index/exhibit-map.csv intake/audits/2026-09-11-supplement-integrity.json intake/to-process.md intake/missing-documents.md
```

Result: no matches, exit 1, empty output. This is ripgrep's ordinary no-match
status, not a failed source read. The `nla(ws)?` term is intentionally broader
than the named NLAWS solver and still produced no hit.

### Complete target-date variants

```sh
rg -n -i -o -- '(2008[-_/ .]?0?7[-_/ .]?31|2008[-_/ .]?0?8[-_/ .]?0?5|0?7[-_/ .]31[-_/ .](2008|08)|0?8[-_/ .]0?5[-_/ .](2008|08)|31[-_ ,.]*(jul|july)[-_ ,.]*2008|(jul|july)[-_ ,.]*31[-_ ,.]*2008|0?5[-_ ,.]*(aug|august)[-_ ,.]*2008|(aug|august)[-_ ,.]*0?5[-_ ,.]*2008)' intake/source-inventory.csv exhibits/index/exhibit-assignment-log.csv exhibits/index/exhibit-map.csv intake/audits/2026-09-11-supplement-integrity.json intake/to-process.md intake/missing-documents.md
```

Result: no matches, exit 1, empty output. Formats include named-month orders,
year-first and month-first numeric forms, two-digit years in the latter,
and compact year-first forms.

### Broader fragments and reversed numeric dates

```sh
rg -n -i -o -- 'loiz[a-z]*|research[ _-]*associates|2008|july[[:space:]_,./-]*31|31[[:space:]_,./-]*july|august[[:space:]_,./-]*0?5|0?5[[:space:]_,./-]*august|20080731|20080805|2008[[:space:]_,./-]*(jul|aug)|31[[:space:]_,./-]*0?7[[:space:]_,./-]*2008|0?5[[:space:]_,./-]*0?8[[:space:]_,./-]*2008' intake/source-inventory.csv exhibits/index/exhibit-assignment-log.csv exhibits/index/exhibit-map.csv intake/audits/2026-09-11-supplement-integrity.json intake/to-process.md intake/missing-documents.md
```

Result: exit 0, three matched fragments on three lines, disposed of below.
No further synonym loop was attempted after checking them.

| Locator hit | Minimal follow-up | Disposition |
|---|---|---|
| `intake/source-inventory.csv:91`, `2008` | CSV parser identified SRC-090, document type `court_opinion_pdf`, date 2009-05-08. A bounded excerpt around the year in its notes identifies a September 2008 argument date. | Court-opinion metadata, not the July/August target correspondence or an acoustic citation. No underlying opinion opened. |
| `intake/source-inventory.csv:100`, `July 31` | CSV parser identified SRC-100, document type `court_opinion_pdf`, date 2019-07-31. | Wrong year and document role, not the July 31, 2008 email. |
| `exhibits/index/exhibit-assignment-log.csv:48`, `July 31` | CSV parser identified the same SRC-100 and 2019-07-31 date. | Duplicate metadata route to the same non-target opinion; not another candidate or corroboration. |

Follow-up used Python's standard `csv.DictReader`, not line-splitting, to count
data rows and print only source ID, date, document type and names of fields
matching `2008|July\s*31`. A second narrow call emitted only up to 45 characters
either side of `2008` in SRC-090's notes. No unrelated correspondence body,
sender/recipient list or bulk record content was emitted.

Other actual checks: `wc -lc` and `shasum -a 256` on the six explicit paths;
`head -n 1` on the three CSVs to identify schemas; `command -v jq` (available
at `/opt/homebrew/bin/jq`); `jq 'type, keys'` on the integrity JSON, followed by
selection of member/gzip/integrity counts, the first member's key names and
`.inspection_policy`. All these checks and both CSV-parser calls exited 0.
The second six-file hash pass matched the first. No command execution error
or missing input was encountered on this assigned route.

## Meaning and remaining coverage limits

Directly established (scope-limited grade A): these exact preserved metadata
files produced no target-organization, acoustic-term or complete target-date
match under the recorded searches; the three wider date-fragment hits were
non-target court-opinion metadata. Consequently no primary email was available
to read through this route and no new acoustic support or contradiction was
obtained from it.

Unresolved (grade D): whether the originals are held in unindexed files,
anonymous attachments, compressed members, scanned/image-only material, other
inventories, encoded content, or differently named/dated records. Text patterns
are not exhaustive semantic recognition; administrative indexes may be
incomplete. This reader did not search the correspondence log, other legal
spines, all repository files, underlying PDFs or private mailboxes. Root's
separate authorized routes may locate a document despite this negative result.

The result does **not** establish nonexistence, present withholding, destruction,
bad faith, or failure of the acoustic analysis. It does not strengthen or
weaken the physics merely because a locator failed. The prior conditional
acoustic assessment remains unchanged.

The immediate next check is comparison with root's already-declared
raw/processed/authority filename, archive-member and bounded PDF locator
results—not another speculative spelling sweep here. A verified artifact with
matching sender/recipient/date, original message context or defensible access-copy
lineage would overturn this non-location result and support a separately
declared complete-document review. If none is found, close this intake/exhibit
route with these limits; any wider search needs its own exact scope.
