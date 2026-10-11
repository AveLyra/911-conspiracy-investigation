# Timing-basis verification and coverage

2026-10-04. Research-only execution record for [report.md](report.md), under
[PLAN.md](PLAN.md). No historical video decoding, audio/image-frame reinspection,
new acquisition, provider query, transmission or accepted-engine change occurred.
Document-page viewing below is not a new reading of the native video pixels.
Separate reviewers are agents, not human experts or human-acceptance substitutes.

## Source and extraction identity

[source-pins.json](source-pins.json) records 18 fresh root comparisons with prior
SHA-256 pins and the amended plan's identity (19 files). Command `4d3a12`, exit0,
used Python `hashlib.sha256(Path(...).read_bytes())` and asserted every expected
hash before saving the manifest. The inputs include both primary PDFs, ten
documentary join/review records, three previous sibling-lineage outputs and
the three initial extraction JSON files. These are byte-identity checks, not
authentication of historical source assertions.

The NCSTAR source is 52,766,002 bytes, 797 pages, SHA-256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
The held SP1000-5v4 source is 18,342,113 bytes, 224 pages, SHA-256
`19281ca238382466a4a0029784d4789fb78cf4d8e4785ac49370c01f9aa94433`.
The Python runtime used for this unit was
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
version3.12.14, with pypdf6.10.0. It was located through the provided dependency
inventory, not inferred from the shell's default Python.

### Text locator and preserved correction

The all-797-page text locator used `pypdf.PdfReader` and `re.finditer` with
case-insensitive source-name, figure, timing, timecode, clock and CBS patterns.
It was a locator, **not a complete visual examination**. Its saved result is
[ncstar-locator.json](ncstar-locator.json), including all hit-page counts and
only the first context per pattern per page.

- First execution: `67e1a4`, session13259, completed in `465c88`, exit0.
  The complete tool response was not retained for artifact creation.
- Identical capture rerun: `b82744`, session6665, completed in `bac19e`, exit0;
  that complete JSON response was saved with `apply_patch`. The first run did
  not fail or time out; its artifact capture was omitted.
- Final inspection found the saved `patterns` map used doubled regex
  backslashes. Those strings cannot be executed directly as the intended
  regular expressions. Original bytes remain unchanged; this representation
  defect is not silently repaired or called a valid executable specification.
- Corrected-map audit: `ed43f0`, session15160, completed in `e43535`, exit0.
  [locator-verification.json](locator-verification.json) contains the actually
  executed patterns and flags. A fresh scan of all797 text layers reproduced
  **every saved per-page count**, all48 hit pages and all51 saved contexts as
  substrings of their corresponding extracted page text. Source hashes were
  equal before/after. No new search terms or wider source population were added.

Counts by pattern: source-name0; figures18; timing40; timecode9; clock5; CBS2.
Zero text-layer source-name hits do not mean the names/credits are absent from
bitmap figures or other records. The visibly present CBS figure credits, for
example, are not additional text-layer hits.

### Selected complete page text

Command `4f90dd`, exit0, extracted and saved the complete text of PDF pages
131–134,163–164,260–275,298–299: **24 pages** in
[selected-pages.json](selected-pages.json). Root read all24 complete text layers.
After PDF263 returned the explicit5-128/130/131 comparison references, the plan
was amended before reading the five additional complete text layers255–259.
Command `ed9250`, exit0, saved [anchor-pages.json](anchor-pages.json); root read
all five. Total selected textual coverage is **29 unique pages**. Selection
does not certify text-extraction completeness for raster-only content.

Separate reviewer `sibling_byte_audit` re-extracted the first24 pages from the
source PDF (`f3b385`, exit0), then the five anchor pages (`710413`, exit0).
Every saved text string matched exactly; source hashes and797-page count agreed.
The anchor JSON hash is
`67d22c7dd0c5ee21401f827949a5a92710abbfcb8a3fdf8cd05faaaf5147e6a0`.
These are independent code executions against the same primary source, not
independent historical observations.

## Actual document-page inspection

Root rendered PDF270,272,273,299 using the bundled `pdftoppm` wrapper. Actual
command form (run separately for each listed page):

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 270 -l 270 -r 110 -singlefile -png /Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf /private/tmp/wtc7-timing-pages.rhWfS5/page-270
```

| PDF page | Initial command / session | Completion | PNG SHA-256 |
| --- | --- | --- | --- |
| 270 | `0c29e2` /33522 | `4698a0`, exit0 | `703906e2bc19085b306d087ab850485a2ddaf48cc43907e4ce72547875b90158` |
| 272 | `4c8eb2` /10518 | `d0f72a`, exit0 | `6fe5e5f743fe05c2088bf09dddd1b56c83f3a0000e8100fec1fb86fc66a652fc` |
| 273 | `4c3514` /2898 | `9c38eb`, exit0 | `b7893bc3e5eabf69b510bfdd1a7fd137b0bfebd499e47d0966ff877a7acb2f3b` |
| 299 | `30623a` /63421 | `9ea820`, exit0 | `c8981c296bf7e3d2aa7a59f8bda014fe0de5b6845925d9826e0ef94dd8cca0d7` |

All four PNGs were actually opened. Captions/prose were legible with no apparent
clipping; map/source relationships and credit placement were inspected. The
renderer emitted Fontconfig configuration/cache warnings and repetitive stderr
was truncated in tool capture. Full warning logs were not retained. This is
**not a warning-free render, independent-renderer comparison or font-fidelity
certification**. No fire/glazing pixel reclassification is claimed. Generated
PNGs remain temporary local derivatives, not source replacements.

Root also opened the already held SP page images146,147,150,156 and read the
full visible pages (printedH-4,H-5,H-8,H-14). Command `f33e7a`, exit0, checked
the PDFs and derivative hashes, including:

| Existing SP page image | SHA-256 |
| --- | --- |
| `sp1000-5v4-schema-146.png` | `158d05d07bfcb8dce6ddca28ee8c7601eaca8f95b895aa292dd5872018563723` |
| `sp1000-5v4-schema-147.png` | `c44853021fa77269bee7d9f06aedfeee1e7d0e98db19de724de5f2e738e89ac7` |
| `sp1000-5v4-attributes-150.png` | `0d0ca642bf2df6563c5f949c70053ebd46ca0ef08b60d5845f06c40bae861fe5` |
| `sp1000-5v4-timing-156.png` | `ba79f9bb3ded176f7af9ff705b2f7d61bc6f5f1d9c83a2e42c350cfb94d5d088` |

The example VideoList row is not a populated record for these CBS clips. The
general copy/digitization/timing workflow is positive documentary context,
not proof that a particular edit or clock calibration occurred here.

## Separate documentary join review

Reviewer `sibling_method_review` inspected the three selected attribution
entries/schema, complete selected acquisition/refresh records for Clips3/7,
the complete eight-file folder listing, direct listing ancestry and the existing
request receipt/lineage review. The reviewer checked ten documentary pins across
separate hash commands and verified the Clip3/7 saved-record joins in `104b1c`,
exit0 (that command itself checked three control-file hashes, not all ten).
Root reproduced all ten documentary pins within `4d3a12`. No broader production-archive
search, current provider lookup or independent historical-media reading is
claimed.

Positive publication joins in `fire-coverage-batch3/source-attributions.json`:

| Figure | PDF / printed page | PDF object | Extracted asset |
| --- | --- | --- | --- |
| 5-141 | 271 /227 | 2847/0 | `A-a80015cf23e0` |
| 5-142 | 272 /228 | 2850/0 | `A-7c7cc22dc34c` |
| 5-143 | 273 /229 | 2853/0 | `A-60c26b7f3416` |

The attribution file's unauthenticated-clock classification is a research
classification, not a native NIST database flag. Asset hashes quoted there were
not a new direct-media check in this unit. The earlier direct PDF/JPEG identity
check remains separately scoped and pinned in the previous lineage report.

Positive access-copy joins from saved selected-success receipts:

| Clip | Provider ID | Bytes | Received-file SHA-256 |
| --- | --- | --- | --- |
| 3 | `1ksEl9qtGFxPGBqWDWcJfEnniSyiT7uyf` | 23,621,148 | `ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d` |
| 7 | `1CnLqGzglKNyLeNwTrXBR1kxHdogB96wh` | 140,334,936 | `a2aefd37d58a7f2e7cea73c8d06114ec941e2178d1a4ddc9419649dd9936487b` |

The saved listing chain is root `17lDS4YslnUaOHv-x2CEhWLVzmceNllk1` →
VideoClips `1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn` → Vince Dementri folder
`1EjgG0oRrJ6VGrVG304qKDAUmKd80n5Rg` → the selected files. Root/folder ancestry
uses listing context where native parent fields were omitted; the Vince folder
includes the explicit parent. The request receipt is reconstructed context,
not a provider-native request log. Preserve Dementri/Demetri spelling variants.
Missing captured fields and2019 repository dates do not establish absent
provider metadata or2001 recording time.

This review found useful asset/access-copy identity joins but no populated
camera/master/edit-to-paired-still timing join **within that selected population**.
It says nothing conclusive about unsearched records or present agency custody.

## Arithmetic and inference review

Root command `f33e7a`, exit0, calculated the literal marginal difference of
caption ranges142[15:55,16:04] and143[15:56,16:05] as[-480,600] seconds.
This is orientation arithmetic, not a statistical interval; the ranges share
upstream dependencies and their joint uncertainty is unspecified.

The separate text/inference reviewer confirmed exact final+2/+1-minute caption
shifts, unexplained endpoint choices in earlier travel estimates, and the
minimum-versus-upper-bound distinction. The general major-event clock method
does not independently calibrate this untimestamped news sequence. The reviewer
also required preserving these counterpoints, incorporated in the report:

- Continuous original footage or independently timed comparison observations
  could establish reliable relative order without an accurate camera clock.
- Irreversible window changes can constrain order if the observations really
  are comparable; no such physical transition is newly established here.
- 5-130 is an enlargement, and5-128/131 are not demonstrated independent clocks.
  Their7m43s nominal-time difference versus approximate7m45s prose is not a
  material contradiction.
- Shared visual timing creates an independence/double-counting risk, not proof
  of a circular structural simulation, exaggerated temperature or false result.

The separately reviewed report snapshot had SHA-256
`7a6ec7d98d7e6fe6e5e5e5981b92c55b2567ece4d51f225d27916975043ce188`.
The reviewer found no material inference correction remaining within its scope;
it did not independently inspect SP imagery or the catalogue in that review.
Root subsequently added its explicit same-video qualification for5-128/131;
the resulting report hash is
`9c0159856d8fd7ef909e528f444193997513b1eabc98a48cce278561ba1a5526`.
The documentary reviewer also read the completed report and verification prose.
Its one requested correction concerned the command-to-hash-check attribution
above; that correction is incorporated, not a change to the source findings.

Final root check `ef34f9`, exit0: all19 manifest source/plan identities matched;
all five JSON artifacts parsed; the29 unique selected pages and corrected
locator counts/contexts reconciled; all13 then-present local prose links in
three Markdown files existed; both navigation entries were present. This was
not a new all-PDF extraction or historical-media run. `git diff --check`
(`4b460f`, exit0) passed for tracked changes; the same root routine separately
checked trailing whitespace in this unit's three untracked Markdown files.
The locator-verification artifact hash is
`fd44a57c0c4ead679191e332c4b7b5a0ca4f4a875838fe7c785d0bae9e02696f`.

## Boundaries and unrun checks

No numerical collapse simulation, model-input sensitivity run, new window-state
annotation, camera-clock authentication, historical cause test or physical
probability update was performed. The existing actual-human/window/model joins
and comparator placement ranges are unchanged. No statutory withholding or
intent finding follows. No staging, commit, push or legal/canonical promotion.

A filename filter for `1-5a|1_5a|1000-5v4` under the main authority directory
returned no match (`cbafba`, exit1); it was not an archive-wide absence test and
did not trigger acquisition. Truncated broad navigation/search outputs were
not treated as complete record inventories. The entire charter remains active;
this completed document unit is not scientific completion of the investigation.
