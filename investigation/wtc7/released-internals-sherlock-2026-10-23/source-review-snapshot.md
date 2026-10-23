# Sherlock review of released NIST model-file internals

October 23, 2026. Local research review, not a historical-cause finding, expert
engineering opinion or legal filing. Raw agency productions and prior conflicting
records remain unchanged. This review is **not published, committed or pushed**.

## Answer

Yes: the project has examined actual command bodies, mesh topology, material
references, thermal assignments and damage lists, not only filenames or metadata.
Earlier work included complete lexical scans and selected independently coded
mesh/thermal joins. This fresh unit rechecks every June thermal-archive member,
the three released APDL bodies and all six September compressed inputs. Reading
bytes and parsing selected commands is not understanding every possible command,
proving what ran, independently reconstructing the fires or reproducing collapse.

The strongest pattern is a **well-populated geometry/temperature package with
incomplete joins to the executed cases and validation outputs**. A large number
of files can coexist with a small number of critically missing links. That is a
concrete reproducibility issue; it does not identify concealment or demolition.

The fresh follow-up also finds repeated, unequal **ANSYS BF/TEMP commands within
the same supplied floor/step input tree**, separately from the already documented
repeated LS-DYNA coefficients. The literal values and their order are inspectable;
their effective historical use and physical consequences are not established.

## Fresh coverage and quantities

Inputs are the retained June and September production directories under
`/Users/admin/docs/911/exhibits/raw/`; exact path and source hashes appear in
[observations.json](observations.json). The June archive SHA256 remains
`2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181`.

| Quantity | Fresh result | What it does not measure |
| --- | ---: | --- |
| ZIP regular files | 25,634, plus 5 directory entries | Independent simulations or physical observations |
| Case A / B / C files | 8,364 / 8,906 / 8,364 | Equal semantic scope or equal exposure |
| Distinct exact body hashes | 19,162 | Independent evidence sources |
| Duplicate copies beyond one per hash | 6,472 (25.25% of files) | 6,472 irregularities |
| ANSYS-compatible `.int` files | 25,188 | A complete executed ANSYS run |
| BF/TEMP statements | 2,435,737 | Unique heated nodes or independent temperatures |
| BFE/TEMP statements | 5,240,592 | Unique elements; layer/step/case repetitions remain |
| Supplied scalar fields in those statements | 23,398,105 | Independent physical measurements |
| Case B extras versus the common 8,364 basenames | 96 SLNo `.int`, 173 `.nod`, 272 PNG, one `mover` | Demonstrated extra historical processing |
| PNG files | 272, all 1,077 x 810 pixels | This unit does not interpret their pixels |
| September input gzip streams | 6, all read to EOF; 602,566,715 decompressed bytes | Results, restart history or actual invocation |

The archive contains 512,164,809 uncompressed bytes including PNGs. Each archive
body was read and CRC-checked; source archive and gzip hashes match before/after.
The June APDL hashes match the existing June manifest. No source program executed.

### Much of the byte repetition is ordinary constant-temperature material

There are 162 body hashes with 36 copies each: 5,832 files, split equally between
literal Fl10 and Fl14 prefixes. A separate reader verifies that every command in
these bodies is a BF/TEMP assignment of exactly 25. These groups account for
5,670 of the 6,472 copies beyond one per hash, or 87.61% of the redundancy. This
is strong evidence against treating extensive repetition itself as suspicious.
It does not determine the temperature of every component on those floors.

Of 8,364 shared basenames, exact-byte matches number 2,298 for A/B, 2,391 for A/C
and 2,295 for B/C. Cases are neither all identical nor wholly independent files.
Identical drivers can call different bodies, and different bytes can reflect only
formatting or a header. Byte similarity is not a physics-equivalence metric.

## Which floors were released?

Four different meanings of "floor coverage" must not be merged:

1. NIST's reported fire reconstruction: the principal uncontrolled fires were
   on 7, 8, 9, 11, 12 and 13. It simulated base fire histories for 7, 8 and 12,
   with time-shifted derivatives for the other three.
2. The released thermal archive has literal filename prefixes Fl07 through Fl14.
3. Released ANSYS geometry filenames describe ground through 16; this is not
   equivalent to all 16 stories receiving fire exposure.
4. The September geometry represents the global building, while its released
   thermal snapshot is Case B at 4 p.m., not a complete thermal time history
   for all 47 floors or all three cases.

| Literal thermal prefix | Files per A or C | Files in B | Root-driver activation in supplied text |
| --- | ---: | ---: | --- |
| Fl07 | 72 | 84 | Commented in all 12 A and B step drivers; active in all 12 C drivers |
| Fl08 | 2,016 | 2,028 | Active A/B/C |
| Fl09 | 72 | 84 | Active A/B/C |
| Fl10 | 2,016 | 2,028 | Active A/B/C |
| Fl11 | 72 | 84 | Active A/B/C |
| Fl12 | 2,016 | 2,028 | Active A/B/C |
| Fl13 | 72 | 84 | Active A/B/C |
| Fl14 | 2,016 | 2,028 | Active A/B/C |

Each A/C odd-prefix group contains 12 floor drivers and 60 core/slab files.
Each even-prefix group also contains 1,944 member-level files. B adds 12 SLNo
files per floor prefix. Thus a 28:1 file-count contrast does **not** mean 28 times
as much heat or 28 times the physical model coverage. For example, A/Fl09 has
73,140 BF rows in only 72 files, while A/Fl08 has 99,468 BF rows in 2,016 files.
Much of the difference is how commands are split into files.

All 36 top-level `WTC7-N.int` drivers were inspected. Under the declared static
same-case-directory assumption, A reaches 8,292 files, B reaches 8,376 and C
reaches 8,364. No active thermal `.int` target is absent by its exact basename.
A has 72 uncalled Fl07 files; B has 84, plus 173 `.nod` files and `mover` outside
this include graph. Image bodies are not part of that graph. These are static
reachability results, not proof those files were never used by another process.

NIST describes **12 half-hour instants**, beginning at 12:30 p.m., not twelve
independent one-hour simulations. A filename suffix alone does not authenticate
that clock mapping. Earlier notes' term "hour driver" should not be read as
one-hour spacing. Source: NCSTAR1-9 printed391, physical457.

### The "below Floor 13" premise needs qualification

Five of the six principal fire-floor labels are below13; that is a count of
labels, not a measurement of the majority of heat, burning area or structural
damage. Floor13 itself is included. No heat-budget majority has been established
by our image work. A fire below a slab can heat the beams supporting that slab.

NIST explicitly says no fire was simulated on14, yet fire on13 heats structure
at14. Its graphics also use different floor-label conventions for slabs and
supporting beams. Therefore Fl14 files or an apparently hot upper floor are not
by themselves evidence of invented upstairs fires. Conversely, those conventions
are not a blanket explanation of every file prefix: a node/element/elevation and
physical-member crosswalk is still required. Source: printed390,394,396;
physical456,460,462. The full relevant pages were inspected.

The genuine question is whether the lower-floor histories, heat transfer,
connections, support loss and propagation reproduce the observed upper-building
motion with realistic remaining resistance. Lower fires are neither a proof of
that chain nor a mechanical contradiction by themselves.

## A more specific new lead: unequal ANSYS assignments within a floor/step

The follow-up traces literal active calls within all 288 supplied case/floor/step
drivers (3 cases x8 prefixes x12 suffixes). BF nodal commands are kept separate
from BFE element/layer commands. It does not select a first/last/max/average
solver rule. The execution record, any applicable cumulative-load settings,
actual command interpretation, run echo and resulting nodal state are missing
from this analysis.

Motivating locator, B/Fl08 suffix1, node170516, in floor-driver include order:

| Source member | Physical line | Literal BF/TEMP value |
| --- | ---: | ---: |
| `WTC7-Fl08-1C101-1.int` | 2 | 29.64507976372 |
| `WTC7-Fl08-2C101-1.int` | 9 | 29.61663097324 |
| `WTC7-Fl08-SLNo-1.int` | 2 | 51.01935961897 |

This is not just an image caption, filename or repeated identical assignment.
It is also not yet a demonstrated erroneous effective temperature. Separate
component exports, temporary assignments, intended replacement, and other
preprocessing remain alternatives. No tested rule is substituted for run evidence.

| Case | Floor/step cells with unequal BF values | Unequal IDs summed within cells | Of those, involving SLNo |
| --- | ---: | ---: | ---: |
| A | 70 of96 | 117,386 | 0 |
| B | 96 of96 | 132,796 | 19,044 |
| C | 70 of96 | 117,386 | 0 |

**Denominator warning:** these are sums over floor/step cells, not unique building
nodes or independent defects. Available-but-root-commented Fl07 cells remain in
this census. Of B's19,044 SLNo-involving unequal ID/cell occurrences,15,084 are in
that commented Fl07 branch and3,960 are in active other-floor branches. Those
counts cannot be treated as historical applied loads.

For completeness, the largest within-driver ranges among active root branches
occur at node32223, Fl14 suffix10, in all three cases. This extreme was selected
**after** scanning the full roster; it is a descriptive extreme, not a prospective
test or a newly timed historical event.

| Case | CoreB line3037 | 1C137 line4 | 2C137 line12 | Range of supplied values |
| --- | ---: | ---: | ---: | ---: |
| A | 716.37126158898 | 147.92918794817 | 25 | 691.37126158898 |
| B | 735.35309903946 | 154.12150800272 | 25 | 710.35309903946 |
| C | 670.91492016075 | 136.79702245968 | 25 | 645.91492016075 |

Members are `WTC7-Fl14-CoreB-10.int`, `WTC7-Fl14-1C137-10.int` and
`WTC7-Fl14-2C137-10.int` in each case's directory. Their whole-body hashes,
verbatim source rows and driver pins are in `overlap-verification.json`.
The contrast is large enough to prioritize the implementation/state question.
It does **not** show a node was simultaneously at these temperatures, identify
that node's physical member, establish temperature inflation, or prove these
values were used to produce a published collapse figure. The ordered example
also cautions against assuming every later assignment makes a model hotter.

Full cell counts and all selected source-order examples are in
[bf-overlap-with-ranges.json](bf-overlap-with-ranges.json). The simpler prior
pass is retained in [bf-overlap.json](bf-overlap.json).

## Ranked technical leads: what is important and what is absent

These are research priorities, not numerical probabilities of misconduct.

| Priority / lead | Observation or prior result | Why it matters / strongest alternative | Discriminating record or test |
| --- | --- | --- | --- |
| High: temperature assignment semantics | Fresh ANSYS overlaps above; fresh LS-DYNA count870,201 rows,628,127IDs,235,010 repeated IDs,170,491 unequal TS IDs | Unequal values affect reproducibility unless actual preprocessing/consumer behavior is known. Component-boundary export or intentional replacement is plausible. Repeats do not establish uniform inflation. | Generator/source mapping, command settings, historical solver/version/input echo and matched nodal output |
| High: case/configuration confounding | A/B Fl07 branches off; C on. B additionally has96 live-referenced SLNo bodies, though its Fl07 branch is off | The supplied case trees differ in more than scalar temperature values. This need not be the configuration actually run. | Complete executed case manifests; isolate changes with justified matched cases |
| High: incomplete executed global package | Master termination4.50s, thermal ramp scheduled6.5-8.5s, damage include/delete hooks commented; names4.1h while supplied list4.0h | Current bytes do not demonstrate the published collapse run. A gravity-stage/restart package is an ordinary explanation and restart-output hooks exist. | Original restart decks/dumps, invocation, message/d3hsp, effective include tree, source-to-figure run map |
| High: sensitive damage-transfer boundary | Prior trace:1,543 candidate shell IDs and361 beam-list IDs; labels243connection shells,1,300buckled-beam shells,355connection beams,6penthouse-decoupling beams | Small numerical handoffs can determine stability. Element deletion is a disclosed modeling procedure, not evidence of real-world charges. Need residual force/energy/contact and connection mapping. | Damage provenance and times, residual state, actual deleted-element/output histories, controlled handoff sensitivity |
| High: properties and run namespace | Prior verified map:23used parts reference19 undefined master-region MIDs;16,324shell records. Numerical counterparts exist at+1000 IDs in included namespace | Missing joins can prevent faithful execution, but do not mean all property information is absent. Stripping specialized connection properties is a known release boundary. | Redaction/substitution map and exact executed constitutive definitions; no guessed repairs |
| High: matched non-collapse control | Published control uses4h temperatures and3.5hdamage; its inputs/results are not joined here | Missing counterpart prevents an independent threshold test. Prior timing comparison shows shorter control followup, but NIST says it stabilized. Shorter duration alone does not invalidate it. | Stability/energy/displacement criteria and equal-horizon justified comparison |
| High/medium: material cutoff calibration | Oct22local audit: MID11/curve27 reacheszero stress at plasticstrain0.160; MID29/curve13 at0.290, each over a0.001decline interval | This is a strain-failure representation, **not** a time trigger. Finite ductility is an ordinary explanation. Calibration, mesh sensitivity and actual threshold attainment remain material questions. | Material tests/calibration, D3HSP curve-use table, actual strain/stress/deletion histories and installed-member mapping |
| Medium: source-fire histories and independence | Published7/8/12base histories;9/11/13shifted. NIST acknowledges possible Floor12and derivative duration/window-adjacent burning overestimation | The claimed initiating region depends on inferred histories; reuse can propagate a common error across floors. Histories may be justified by available evidence; no measured temperature inflation follows from façade images alone. | Independent visibility-qualified observations; source/result mappings; plausible duration/ventilation alternatives |
| Medium: specific broken/unmatched content | Freshly verified one328-byte all-NUL body;8unmatched named APDL dependencies; date/version and4.0/4.1labels | Concrete integrity/version questions, not a claim of general corruption or removal. An intact copy or renamed equivalent may exist. | Agency originals/checksums and filename/content crosswalk |
| Medium: publication/validation joins | Preserved west-penthouse timing difference, caption/panel offsets, late exterior-shape mismatch | Quantitative targets for validation; caption errors, alignment definitions and modeling limitations remain alternatives | Native identified output runs, event definitions, independent timing and uncertainties |
| Lower causal weight: metadata/format | AVI dimension/codec-description tension, animation wrapper changes, CDX/replay differences | Important provenance questions, not identified physics errors or affirmative tampering evidence | Native originals/version hashes, archived original response headers/WARC payloads |

The LS-DYNA repeat figures are now freshly reproduced: 37.41% of unique IDs repeat,
27.14% have unequal supplied TS. These are different proportions and are not
percentages of wrongly modeled building nodes. The earlier member map's Column79
region has 63 unequal nodes in 7 groups of 9; 45 later values lower, 18 higher. This unit
does not rerun that mesh join. Regular elevation spacing suggests testing export
segment boundaries, not automatically assigning floor names or intent.

### Specific absent pieces, not an unbounded list of "missing evidence"

- The exact run and restart chain connecting the supplied inputs to published
  collapse and control figures; matched output histories, not just animations.
- The LS-DYNA temperature-generation/mapping implementation and the semantics of
  unequal repeated rows. ANSYS thermal loading and structural-damage transfer are
  different branches; do not conflate them.
- Exact dependencies named by released APDL: two July geometry names and
  `FL2-LOAD1` through `FL7-LOAD1`. August geometry may be renamed or different;
  equivalence is unproven. The three supplied APDL files do not name any
  `WTC7-N.int` thermal driver; the loads file's four TIME commands are1,2,3,4.
  That is evidence of an incomplete invocation chain, not proof the thermal data
  were never used elsewhere.
- The4.1hdamage filename, the3.5hdamage counterpart, and exact identities of
  results and connection laws associated with each case. Existing-withheld,
  not-found-by-this-review and not-in-this-package are different statuses.
- A mapping from node/element labels to physical members, drawings, heated faces
  and elevations wherever the argument depends on floor or column identity.
- Calibration provenance and actual attainment of consequential failure cutoffs,
  not merely their presence in a material table.

Six inputs originally omitted were later delivered: preserve that delivery
history but do not call those six still missing. Case B 8,906 versus historical 8,910
remains an accounting discrepancy, not four identified missing technical files.
The old 25,644 comparison is conditional accounting, not an identified lost file.

### A subtle reference-state lead, lower priority

Released upper-floor APDL has `TREF,20` atline23; gravity loads set `TUNIF,20`
at line 4417. NCSTAR 1-9 printed 391 says initially 23 C. Many supplied BF values and
LS-DYNA TS entries are 25. Retain 20/23/25 as distinct documented values. Reference
temperature for expansion, initial temperature and an ambient-looking supplied
field are different roles; this is **not yet a demonstrated contradiction**.
An executed unit/reference-state crosswalk would establish whether any nonzero
initial strain or material effect followed. Do not treat a few degrees as
evidence of an unmeasured large collapse effect.

## What looks intriguing but presently carries little weight

- `mover` has9literal `mv` commands, not a deletion command. An unknown external
  alias or environment is conceivable but not evidenced by this file. No source
  script was executed. Missing environment records do not prove trace erasure.
- "Delete column elements" can describe geometry construction or model
  reduction. A commented card is not an applied physical failure. Part79 is not
  automatically architectural Column79.
- A peak over300is not inconsistent with a statement about initiating column
  temperatures unless the node, material, case and time match. Slab and beam
  temperatures cannot be substituted for a column's temperature.
- B's +10% label is not by itself evidence of cherry-picking. The report describes
  **gas-temperature** A/B/C cases with B +10% and C -10%, and all three thermal
  families are supplied. Steel temperatures need not scale by exactly 1.1.
  What remains is configuration and selected-executed-case comparability.
- Regular ID increments, repeated ambient loads, export timestamps, consistent
  image sizes and thousands of geometry lines are expected engineering patterns.
  They become consequential only when linked to a material mismatch or provenance
  break. Do not count multiple descriptions of the same source as independent clues.
- Our own previous shell census counted thickness rows as additional shells.
  The corrected 3,006,910 shell count matches NIST's published typed count. That
  error belongs to our audit, not NIST. Fresh parser failures are likewise retained
  here rather than relabeled source discrepancies.

## How a Sherlock-style investigation should proceed

The detective's useful move is to locate **where competing explanations predict
different records**, not to find the most suggestive word in the largest folder.

1. **Reconstruct the sequence.** Original receipt -> file identity -> actual
   input graph -> solver invocation/restarts -> numerical outputs -> rendered
   figure -> published claim. Mark missing joins instead of assuming them.
2. **Separate four hypotheses.** Routine iterative/export history; incomplete
   production; materially defective or selectively validated modeling; deliberate
   misrepresentation. They can coexist, but each requires different evidence.
   A deceptive scientific record would still not establish demolition of WTC7.
3. **Look for consequential clustering.** Do unexplained case changes, unknown
   assignment rules and withheld laws all affect the same initiating connection
   or timing comparison? That would raise research priority. Shared workflow or
   an announced withholding boundary is a strong ordinary alternative.
4. **Use negative controls.** Trace cold floors, untouched members, stable runs,
   known-common exports and unaffected figures with the same method. The ambient
   duplicates above are one useful control; contrary outcomes must stay visible.
5. **Audit both favorable and unfavorable choices.** Include lower and higher
   repeated values, collapse and arrest cases, earlier and later files, and the
   unsuccessful attempts. Apply the same native-file standard to UAF: PDF labels
   cannot establish Model9/10G3005section assignments without native exports.
6. **Escalate claims only with discriminators.** A demonstrated material error
   needs a reproducible consequence. Intent needs evidence of knowledge and a
   decision to misrepresent or suppress; actors and a historical operation need
   their own independent evidence. Missing files and an imperfect model do not
   supply those links.

**Best immediate technical target:** determine the effective temperature state
for specific repeated BF and LS-DYNA nodes using authenticated consumer/run
records, then map those nodes to the structural model. In parallel, seek the
executed collapse/control chain and failure-curve calibration. These are more
discriminating than another generic anomaly count.

## Source links and prior work

- [Official NIST FAQ](https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation), Q8-9for floors and proposed chain. RetrievedOctober23,2026.
- [NCSTAR1-9official PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf): printed387,389-392,394,396; physical453,455-458,460,462. Held source SHA256 `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.
- [Thermal-transfer crosswalk](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055/investigation/wtc7/thermal-transfer-crosswalk/report.md), full-body lexical coverage and separate thermal/damage branches.
- [Member map](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055/investigation/wtc7/model-member-map/report.md), corrected shell counts and selected column mapping.
- [Thermal assignment trace](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055/investigation/wtc7/thermal-assignment-trace/report.md),63node regional trace and its limitations.
- [Material/run crosswalk](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055/investigation/wtc7/material-run-crosswalk/report.md),19material references and transformed counterparts.
- [Discrepancy index](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055/investigation/wtc7/released-file-discrepancy-index/index.md), stable historical DISC identifiers; older coverage wording remains historical.
- [Public67lead prioritization](https://github.com/AveLyra/911-conspiracy-investigation/blob/5243c055/investigation/wtc7/lead-prioritization-2026-10-22/README.md), broader motion, connection, custody and record leads.
- LocalOct22material-curve review: `../material-curve-response-2026-10-22/REPORT.md` and `EXECUTION.md`; findings attributed to that separately verified saved-input analysis, not a new constitutive simulation here.

The linked research reports are not independent historical sources or evidence
that the public remote was reverified during this unit. Physical samples, access
contracts and actor allegations are distinct investigations, not conclusions
obtainable from these model-file internals.

## Verification and preservation

[PROTOCOL.md](PROTOCOL.md), [audit.py](audit.py), [test_audit.py](test_audit.py),
[observations.json](observations.json), [check_patterns.py](check_patterns.py),
[verification.json](verification.json), [trace_bf_overlap.py](trace_bf_overlap.py),
[verify_overlaps.py](verify_overlaps.py), `overlap-verification.json`.

Six parser tests passed after the final parser changes. The full census reached
EOF and preserves source hashes. A separately implemented CSV reader reproduces
the September row/repetition counts; the36-copy groups and all36root drivers
were separately source-checked. The overlap checker verifies the complete288cell
roster, unchanged prior summary fields, matching BF totals and exact raw locators
and include order for the three case maxima. This is post-result checking, not
a blinded independent investigation, general APDL/LS-DYNA certification or
physical validation.

Two new-analysis mistakes are retained: the first reader rejected comma-separated
thermal cards; the next temporarily swapped TS/TB field meanings. Both are our
parser errors, not agency discrepancies. The failed receipt and rejected output
remain alongside the corrected run. Unrelated worktree files are untouched.
