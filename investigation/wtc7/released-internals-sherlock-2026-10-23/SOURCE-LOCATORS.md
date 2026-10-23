# Source links and exact locators

October 23, 2026. Companion to the [full review](README.md). Original values,
comment markers and filenames are preserved, not reconciled. Source hash means
identity of examined bytes, not authentication of a historical solver run.

## Reading the references

- Original input line numbers below are **1-based physical lines in the
  decompressed text**, not GitHub-rendered JSON line numbers.
- For ZIP contents, use the exact member path plus member SHA256. For gzip
  inputs, the [originals manifest](source-excerpts.json) gives stored compressed
  and decompressed hashes. Never confuse the two.
- [source-excerpts.json](source-excerpts.json) provides verbatim selected rows
  and original physical-line numbers. Its `label` values below are exact search
  keys. [source_excerpts.py](source_excerpts.py) reproduces the extraction from
  held originals without executing any source command.
- Full original production files are **not newly uploaded**. No official public
  full-input download URL was established in this unit. Excerpt links are links
  to this preservation derivative, not invented links to an agency download.
- Whole-file census claims have an archive/member scope rather than one source
  line. Their executable method, exact denominator and structured-output location
  are given explicitly. A line number cannot substitute for that scope.

## Original input identities

| Original | Stored SHA256 |
| --- | --- |
| `ANSYS Thermal Data.zip` | `2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181` |
| `1 Floor_8-16_15AUG07.apdl` | `e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64` |
| `2 Floor_GR_TO_7-22AUG07.apdl` | `e96f23597454737ca3177d22e8cd857561b937658189b5d9e1b49ae5bdbdf8f9` |
| `3_LOADS AND SOLU_15AUG07_0.25LL-names_redacted.apdl` | `bb07af3ff1537348f87a6ea95123d3620d588766d278649829c9f35247c33e5a` |
| `wtc7_global_8a_no-conn-matl.k.gz` | `f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d` |
| `WTC7_CaseB_400pm.int.gz` | `51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447` |
| `Damage_Global_ANSYS_CaseB_4.0hr.k.gz` | `982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da` |
| `G6A_CaseA_El_Delete_List.k.gz` | `aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273` |
| `elem_thick_to-renum.k.gz` | `c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59` |
| `discrete_mass.k.gz` | `2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7` |

Paths identify engineering sources, not a release-completeness conclusion. The
six-file omission/delivery history remains dated history; those six are present.

## 1. Fresh archive, floor and case census

| Finding | Exact scope / locator | Preserved output and limit |
| --- | --- | --- |
| 25,634 regular files; A/B/C 8,364/8,906/8,364 | All regular members of the hash-pinned ZIP | [observations.json](observations.json), `/archive` and `/cases`; file counts, not run counts |
| 19,162 distinct byte hashes; 6,472 duplicate copies | SHA256 of every complete ZIP body | `/archive/unique_body_hashes`, `/archive/duplicate_copies_beyond_one_per_hash`; no semantic equivalence inferred |
| 25,188 `.int`, 173 `.nod`, 272 PNG, one extensionless file | Every ZIP member basename and suffix | `/cases/*/types`; directories excluded |
| Floors 7-14; odd/even packaging contrast | Exact `WTC7-Fl##-` filename prefixes | `/floor_prefixes`; labels are not physical-member authentication |
| 2,435,737 BF/TEMP and 5,240,592 BFE/TEMP rows | Literal commands in all non-NUL floor-prefixed text bodies | `/floor_prefixes/*/BF_rows` and `BFE_rows`; layered/time/case repetitions remain |
| 162 constant-25 body groups, each with 36 copies | Complete bodies for every hash occurring 36 times | [verification.json](verification.json), `groups36_all_literal_BF_TEMP_25` and floor counts; alternate CSV reader, not independent physical evidence |
| B's extras: 96 SLNo, 173 `.nod`, 272 PNG, `mover` | Basename inventory and literal include graph | `/cases`, `/same_basename_comparison`, [full review](README.md); PNG pixels not interpreted |
| All PNG headers 1,077 x810 | IHDR bytes16-23 of every PNG body; ZIP CRC checked | `/png_dimensions`; not a visual-content result |

The [census code](audit.py) reads complete member bodies without extracting or
executing them. The [separate check](check_patterns.py) confirms hash groups,
all 36 root drivers and September thermal counts. Original local verification
and byte-identical repeat receipts are retained.

### Floor 7 activation and actual include order

Exact root members are `CaseA_Temps/WTC7-N.int`,
`CaseB_Temps/INTFILES+10%14SEP07/WTC7-N.int` and
`CaseC_Temps/WTC7-N.int`, for **every N from1 through12**.

In each A/B member, line1 is `!/input,WTC7-Fl07-N,int`. C line1 is
`/input,WTC7-Fl07-N,int`, without the `!`. Lines2-8 call prefixes
09,11,13,08,10,12,14 in that order. Full text and member hashes for all36
are in [source-excerpts.json](source-excerpts.json), labels `A-step-driver-1`
through `C-step-driver-12`. [observations.json](observations.json),
`/step_driver_records`, retains every parsed reference and line number.

Under the static same-parent interpretation, reachable counts are A8,292,
B8,376 and C8,364, with no unmatched active thermal basename. This is not proof
of historical working directory, invocation or non-use elsewhere. B's Fl07
SLNo bodies exist and are referenced within floor drivers even though its
top-level Fl07 branch is commented.

## 2. Unequal ANSYS temperature assignments

All paths below are **members of the pinned thermal ZIP**. No original number is
changed or selected as the effective solver temperature.

### Node32223, prefix Fl14, suffix10: all three cases

| Exact case parent | `WTC7-Fl14-CoreB-10.int`, line3037 | `WTC7-Fl14-1C137-10.int`, line4 | `WTC7-Fl14-2C137-10.int`, line12 |
| --- | ---: | ---: | ---: |
| `CaseA_Temps/` | `BF,32223,TEMP,716.37126158898` | `BF,32223,TEMP,147.92918794817` | `BF,32223,TEMP,25` |
| `CaseB_Temps/INTFILES+10%14SEP07/` | `BF,32223,TEMP,735.35309903946` | `BF,32223,TEMP,154.12150800272` | `BF,32223,TEMP,25` |
| `CaseC_Temps/` | `BF,32223,TEMP,670.91492016075` | `BF,32223,TEMP,136.79702245968` | `BF,32223,TEMP,25` |

The corresponding `WTC7-Fl14-10.int` drivers identify the include order.
Selected original driver-line numbers and hashes are in [source-excerpts.json](source-excerpts.json),
labels `A-Fl14-step-10-selected-driver-calls` and equivalent B/C labels.
All nine original body hashes and exact source rows are independently located
by the post-result [overlap-verification.json](overlap-verification.json).

These are **post-scan descriptive extremes** among root-active branches, not
prospectively selected observations. They are not three historical measurements,
three simultaneous temperatures or a reconstructed heating/cooling sequence.

### Node170516, B/Fl08, suffix1

Parent is `CaseB_Temps/INTFILES+10%14SEP07/`:

| Member | Physical line | Original text |
| --- | ---: | --- |
| `WTC7-Fl08-1C101-1.int` | 2 | `BF,170516,TEMP,29.64507976372` |
| `WTC7-Fl08-2C101-1.int` | 9 | `BF,170516,TEMP,29.61663097324` |
| `WTC7-Fl08-SLNo-1.int` | 2 | `BF,170516,TEMP,51.01935961897` |

Verbatim excerpts, member hashes and selected original driver calls appear in
[source-excerpts.json](source-excerpts.json), `B-Fl08-step-1-*` labels.

### Coverage and denominator

[bf-overlap-with-ranges.json](bf-overlap-with-ranges.json), `/floor_steps`, records
all288cells:3cases x8floor prefixes x12step suffixes. It retains repeated/equal
and unequal counts separately, root-activation flags, missing/NUL inputs and
source-order locators. Totals are **sums of per-floor/per-step IDs**, not globally
unique nodes or independent defects. Unequal BF assignments occur in70/96A cells,
96/96B cells and70/96C cells. B has19,044 SLNo-involving unequal ID/cell occurrences;
15,084 are in the root-commented Fl07 branch and3,960 in other root-active branches.

The effective consumer/solver rule and historical invocation remain unknown
here. No first/last/max/sum/average resolution is assumed. [trace_bf_overlap.py](trace_bf_overlap.py)
does not execute the source; [verify_overlaps.py](verify_overlaps.py) checks
the complete roster, source-row totals and selected raw locators.

## 3. LS-DYNA initialization, damage hooks and missing joins

All master references are to decompressed `wtc7_global_8a_no-conn-matl.k.gz`.

| Claim | Exact original location | Source link / preserved conflict |
| --- | --- | --- |
| Active termination4.50s; alternatives commented | Master9-12 | [source-excerpts.json](source-excerpts.json), `master-termination`; `$20.0`, `$8.501`, active`4.50` retained |
| Gravity curve scaling | Curve1 header646, points648-669 | `master-curve-1`; interpretation is not actual run evidence |
| Thermal ramp offset6.5, reaches full ordinate after2.0 | Curve2 header675, points677-698 | `master-curve-2`; 6.5+2.0=8.5, later than active termination |
| Outside-region transformed include | Master5,520,133-5,520,142 | `master-include-and-damage-hooks`; original transformation rows retained |
| Mass and thermal active include names | Master7,196,425-7,196,432 | Same excerpt; commented `WTC7-1.int` and active `WTC7_CaseB_400pm.int` remain distinct |
|4.1h reference versus4.0h delivered name | Master7,196,436-7,196,437; companion basename `Damage_Global_ANSYS_CaseB_4.0hr.k.gz` | Both names retained; not a finding that their content is equivalent |
| Damage-delete hooks commented | Master7,196,439-7,196,442 | Both shell and beam delete hooks carry `$`; no activation inferred |
| Damage categories and six penthouse beams | Decompressed4.0hfile: labels5,251,1554,1914; explicit six IDs1915-1920 | `damage-labels-and-penthouse-beams`; categories do not identify historical cause |

The earlier [content audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/lsdyna-supplement-content-audit/report.md)
records1,543shell and361beam-list candidates and the inactive CaseA companion.
The corrected [member map](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/model-member-map/report.md#the-mesh-count-is-now-a-record-count)
distinguishes element records from thickness rows. The old double counting was
our audit error; it is not an agency discrepancy.

### Repeated LS-DYNA coefficients

In decompressed `WTC7_CaseB_400pm.int.gz`, the keyword is line2; numeric rows
are lines3-870,203; the final line is870,204. Exact first cards and field order
are preserved under `lsdyna-first-node-cards-field-order` in [source-excerpts.json](source-excerpts.json).
Fresh complete-stream counts are in [observations.json](observations.json),
`/gzip_sources` entry with that basename, `/thermal`:870,201rows,628,127IDs,
235,010repeated IDs,170,491unequal TS IDs; TB0and LCID2 throughout.

The previously verified regional trace is distinct:
[thermal-assignment report](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/thermal-assignment-trace/report.md#column-79-region-repetitions).
Its concrete example has node921518 at thermal lines512,465and512,527,
TS50.57and46.97; master NODE record925,814; incident shells PID179. All63regional
unequal nodes remain in that earlier trace;45later values lower,18higher.
This publication does not rerun or silently extend the physical-member mapping.

### Material namespace and zero-stress curves

The earlier [material/run crosswalk](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/material-run-crosswalk/report.md#exact-missing-reference-map)
lists all23parts, their19material references,16,324shell records and exact
PART card lines. Master part25 at2315is one example. Transformed numeric
counterparts are not automatically definitions in the master namespace.

The selected curve cutoffs were reread directly for this publication:

| Material / referenced curve | Exact original master lines | Preserved values |
| --- | --- | --- |
| MID11 / curve27 | Material2166-2169; curve1047-1058 | Header1048; strain/stress1057=`0.1590,5.665E+08`,1058=`0.1600,0.000E+08` |
| MID29 / curve13 | Material2365-2368; curve857-871 | Header858;869=`0.289,6.302E+08`,870=`0.290,0.000E+08`,871=`1.000,0.000E+08` |

Full selected curves and material-row whitespace are in [source-excerpts.json](source-excerpts.json),
`master-material-and-zero-stress-curve-locators`, `master-curve-13` and
`master-curve-27`. These are strain coordinates, not seconds. A finite-ductility
law is a strong ordinary alternative; actual calibration and threshold attainment
are not established. Prior manual-role interpretation is documented in the
[published material-method review](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/material-run-crosswalk/method-source-review.md).
The [Version971primary manual](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf)
is not proof of the exact historical executable or its unlabeled field behavior.

## 4. APDL dependencies, reference states and byte integrity

| Finding | Exact source location | Limit |
| --- | --- | --- |
| July geometry references versus August delivered basenames | Loads APDL15and16 | Filename/version join remains unproven, not necessarily missing content |
| `FL7-LOAD1` through `FL2-LOAD1` calls | Loads APDL4275-4280 | No exact named counterpart in inspected selected package |
| Four literal TIME commands | Loads APDL585,4435,4451,4570 | Values1,2,3,4; not proof no separate thermal run existed |
|20reference/initial values | Upper-floor APDL21`TOFFST,273`,23`TREF,20`; loads APDL4416comment and4417`TUNIF,20` | Different roles from published initial23and supplied25; no effect inferred |
| Internal15August versus22AUG filename | Lower-floor APDL line3 | Both values retained; no preferred date chosen |
| Null-filled file | ZIP member `CaseB_Temps/INTFILES+10%14SEP07/WTC7-Fl08-1C137-2.int`, bytes0-327 | All328bytes00; no meaningful text line numbers |
| `mover` contents | ZIP member `CaseB_Temps/INTFILES+10%14SEP07/mover`, lines1-9 | Nine literal`mv`commands; no source execution or external-alias inference |

The APDL and mover excerpts are in [source-excerpts.json](source-excerpts.json).
The null body SHA256 is`7b4499c3cc6e82a9da3100028f52af7f8c1e9ee60e33010a108e401989782962`.
The [discrepancy index](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/released-file-discrepancy-index/index.md)
preserves the stable IDs and earlier delivery/accounting limits. In particular,
8,906versus8,910does not identify four missing filenames; six later-delivered
inputs are not still missing.

## 5. Primary NIST report pages and external source links

Source edition: November2008 NCSTAR1-9, held PDF SHA256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
PDF links use physical pages; printed-page locators are separately stated.

| Report claim | Printed / physical page | Primary link |
| --- | --- | --- |
| Base histories7/8/12and shifted9/11/13; possible duration/window-adjacent overestimate |387/453| [Section9.5](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=453) |
|8->9onehour later;12->11onehour later;12->13half-hour later |389/455| [Section10.2](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=455) |
| No14th-floor fire simulated; expected adjacent-story heating |390/456| [Heating assumptions](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=456) |
| Initially23C;12half-hour instants; separate ANSYS/LS-DYNA thermal sets; B+10%gas temperatures |391/457| [Section10.3.1](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=457) |
| C-10%gas temperatures; structural model differences |392/458| [Continuation](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=458) |
| Floor/beam labeling and adjacent-floor exposure |394/460| [Floor7discussion and footnote1](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=460) |
| Floor13/14thermal response |396/462| [Floor-specific results](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=462) |
| Earlier damage control uses4h temperatures,3.5hdamage |568/634| [Control description](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf#page=634) |

[NIST FAQ Q8-9](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation)
identifies the principal uncontrolled-fire floors7-9and11-13and describes the
proposed sequence. It is a reported account, not independent validation of it.

For the control-horizon comparison, NCSTAR1-9A physical156/printed105reports
termination12.76s and a stable control; physical127/printed76reports firstC79
buckling14.7s in the higher-damage case. The prior [October21crosscheck](https://github.com/AveLyra/911-conspiracy-investigation/blob/a1979eb700276e13e46e67cceff6a0954a55a649/investigation/wtc7/c79-and-timing-crosschecks-2026-10-21/README.md)
preserves the8.5sdamage-application reference,4.26versus6.2sfollowup and1.94sdifference.
Those values do not establish an invalid stopping criterion or delayed collapse.

## 6. Previously documented timing and metadata leads

These are retained review topics, **not newly measured results in this unit**:

- [Animation/timing audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/3236dd82/investigation/wtc7/animation-timing-audit-2026-10-16/README.md): west-penthouse observation9.3s versus model6.9/7.3s; Fig12-68caption/panel offsets; wrapper canvas355x300versus464x368; unresolved external-video lineage.
- [October21caption crosscheck](https://github.com/AveLyra/911-conspiracy-investigation/blob/a1979eb700276e13e46e67cceff6a0954a55a649/investigation/wtc7/c79-and-timing-crosschecks-2026-10-21/README.md): NCSTAR1-9A Fig4-60, printed109/physical160;14.5versus19.5first-panel/caption calculation value, with full conflicting caption/panel values retained.
- [AVI header audit](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/research/faraday-wtc7-model-compare/review/avi-container-stream-header-audit-2026-10-04.md):998x725main header versus996x724stream;`file`description versus`CRAM`/`msvideo1`; native-source authentication remains open.
- [CDX/replay-layer discrepancy](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055a8fb30a2e8c773e96e7930490e2c20d1/investigation/wtc7/wayback-replay-capture-2026-10-09/cdx-replay-layer-discrepancy-2026-10-10.md):2011index records4,112-4,113bytes versus13,113-byte replay error pages. They describe different archive layers; original WARC response payloads/headers remain unverified.

Each linked audit controls its detailed byte/page/timestamp pins and limitations.
No deletion, video substitution, deliberate manipulation or historical cause
follows merely from this list. Negative findings and ordinary alternatives remain
part of the review rather than being removed to strengthen a preferred theory.
