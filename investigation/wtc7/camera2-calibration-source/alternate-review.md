# Alternate saved-project inventory — independent source lane

2026-09-19. Research-only. This review inventories one specified archived Dan
Rather project; it does not validate historical measurement, media identity,
physical calibration, a publication table, or a collapse explanation.

## Result and version discriminator

The specified project contains **two PointMass tracks, 150 saved x/y rows in
total**, not an alternative complete eight-track export. Each track has 75
finite rows and 75 saved key-frame indices, exactly `0,6,...,444`; there are no
duplicate row or key indices, unmatched keys, nonkey saved rows, out-of-domain
rows, or extra PointMass arrays reported by the parser. One label is the
allowlisted `NW Corner`; the second remains a hash/length identity (15
characters, SHA-256
`2b5305c568efc9144c87cb9b9d4c9c47ef690dc717bcc4599eb011fcb0d30786`).
No arbitrary source label or author path was printed or written.

The complete literal clip domain is 962 video frames and 161 selected steps
`0,6,...,960`. Each track lacks saved rows at 86 selected steps
`450,456,...,960`, and at 887 of the 962 video indices. These are **absence
relative to saved domains**, not findings that measurements were deleted,
never existed, or should have existed. Key membership is saved state, not
proof of human marking or independent measurement.

This is a concrete source-version discriminator: this particular TRK cannot
be substituted as a complete saved multipoint project merely because it is
in the same kit. Its two histories might still be relevant to a subset or a
different analysis. Testing that possibility requires a separately declared
all-candidate comparison using this project's own clock and coordinate
settings, or a byte-identified publication-input project/export with a clear
source-to-table mapping. No coordinate transformation, table comparison,
clock/origin adjustment, or numerical series-pair selection was performed
here. A different track count is not evidence of falsification or intent.

## Literal settings (not calibration acceptance)

The saved semantic version is `6.1.2`, length label `m`, mass label `kg`.
There are four items in the single track collection: CoordAxes, TapeMeasure,
and the two PointMass objects. There is one coordinate-system row and one
tape row, both indexed zero. The exact field locators and lexical values are
in both safe exports.

| Saved object | Saved values |
|---|---|
| Panel | width 704.0; height 480.0; magnification 1.0; center 359,256 |
| Clip | start frame 0; step size 6; step count 161; start time 0.0; play all steps true |
| Stepper control | delta_t 33.3667000333667; rate 1.0; current frame 0 |
| Coordinate system | fixed origin/angle/scale true; locked false |
| Coordinate row | origin 479.7266754270696,399.2641261498029; angle −0.7742201649280619; xscale=yscale=1.9452779103716007 |
| Tape row | endpoints 425.0,319.0 and 427.0,190.49999999999966; saved world length 66.0654 |
| Tape settings | fixed tape/length and stick mode true; readonly false |

The panel dimensions are saved project settings, not a newly probed media
raster. No angle-unit or physical scale inference is needed for this
inventory. No literal filter, reference-frame, time-source, autofill, or
dependent candidate was found by the frozen exporter's declared predicates.
Absence of such nodes does not establish absence of earlier processing or
editing. No archived video was decoded, viewed, exported, or executed.

## Provenance and verification

All SHA-256 values below identify held bytes, not historical authenticity.

| Item | Bytes | SHA-256 |
|---|---:|---|
| Preserved parent ZIP | 172774879 | `c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189` |
| Exact `The Kit/WTC7-Dan Rather/DistantViewWTC7.trz`, outer zero-based entry 41 | 9477547 | `8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e` |
| TRK, nested zero-based entry 4 | 68489 | `5aa2bea2b6532713bc9abae647e0486c937892a96d33a3892fc0f6109a11a693` |
| Frozen pure parser | 20921 | `872d37a02cbbad8c8e80e2f40068e0f8e0606411c4494173bf7f3c9f24b36181` |
| Frozen parser tests | 10343 | `62f72f9566a3b606d22b7e52ef2d44ee9020dcc5058933bd0edcecf9e655c4e1` |
| Adapter | 13878 | `81101ca484ea6b506bfed88954cd8ca1adecd5d3cd5ec84e8f7fdb6749b15b16` |
| Adapter tests | 5396 | `2982d336df92355c68d954a98be14694cd96b58ba0868aa2cf98d058740e2e92` |
| Protocol used during both runs | 6436 | `6be332d9537498582e7196c3adfa42ce29a7be6954824e4cea5d365665d74947` |
| Each exclusive export, 01 and 02 | 510859 | `e068c83b22a2bbeacf2b632bf68088a1ce32600455b9a5e258c946e5f6a80586` |

Commands actually run, using Python 3.12.14 at
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`:

```text
python3 -B alternate-tests.py
python3 -B alternate-export.py --out alternate-export01.json
python3 -B alternate-export.py --out alternate-export02.json
cmp alternate-export01.json alternate-export02.json
```

The commands were invoked with absolute script paths in this directory, using
the runtime above. The synthetic command passed **25 tests** before any
historical body parse: 17 frozen-parser controls and eight adapter/oracle
controls. Negative fixtures successfully rejected source/hash/size/ordinal,
path, numeric, locator, key-state, missing-state, and omission mutations.
Both fresh historical exports exited zero; `cmp` exited zero with no output.
No failing test or historical export was suppressed; no implementation repair
was needed after the first synthetic run.

Each historical export also passed a distinct `minidom` direct-source
traversal, without calling parser traversal helpers: 1,133 resolved locator
occurrences, 348 scalar lexical checks, two serialized key arrays, all 150
PointMass rows, all 300 coordinates, and all 150 key-membership flags. Counts
include repeated locators where the export intentionally presents a field in
more than one context. The verifier separately reconstructs source-track and
row counts, original frame indices, key lists, and clip/video missing domains.
The source and producer bytes were rechecked after processing. Independent
traversal is a software cross-check on the same evidence; the two exports are
repeatability, not independent historical corroboration or expert review.

## Read and mutation coverage

Read in full: current main AGENTS.md, WORKFLOW.md, START-HERE.md and investigation
CHARTER.md; this unit's PROTOCOL.md; evidence-falsification-auditor,
source-of-truth-guardian, development-verification skills and the first two
skills' linked claim-ledger/audit references; frozen 359-line parser and
225-line tests. The complete exact TRK bytes were parsed twice and checked
against a separate DOM traversal twice. Output inspection covered sanitized
track/index/key/missing summaries, all allowlisted settings and coordinate/
tape state; no human-by-human examination of every coordinate is claimed.
One oversized sanitized inspection was truncated by the tool; its settings
and summaries were reissued in compact form. This was an inspection-display
limit, not an export or parser failure.

Writes were confined to `alternate-export.py`, `alternate-tests.py`, the two
new exclusive `alternate-export*.json` files, and this review. Raw sources,
the frozen exporter, prior results, main, legal records and other worktree
changes were preserved. No authority promotion, transmission, publication,
Sherlock/Faraday acceptance, causal-ranking update, commit or push occurred.
