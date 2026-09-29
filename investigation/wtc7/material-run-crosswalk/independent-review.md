# Independent material-ID and property-card review

2026-09-12. Exploratory WP3/Q06/Q10. **PASS for the stated numeric/namespace
scope.** The source extraction, producer comparison and report arithmetic are
separate operations. This is not an executable-deck certification, material
substitution, historical-run reconstruction or validation of collapse physics.

## Authority, scope and independence

Fresh main AGENTS and WORKFLOW, the complete new protocol, the investigation
charter, and the prior keyword-method reviews were read. The previously read
source-of-truth-guardian, evidence-falsification-auditor and
development-verification skills keep source records, derived ID joins, semantic
interpretation and physical inference separate. All writes are exploratory
independent artifacts in this new isolated-worktree unit. Main, the original
compressed inputs, legal records, held sources and previous units are unchanged.
No source instruction, solver, include, deletion or shell command embedded in a
source was executed; nothing was transmitted, committed, pushed or promoted.

The new independent parser uses Python standard-library streaming, Decimal
numeric values, fixed-field/CSV rules and separate metadata/element states.
It imports neither the new producer nor the prior producer. Prior independently
written parser experience and previously reviewed source-pin/card-layout
constants were used. The protocol and prior accepted results already identified
the expected 23-part/19-MID question; this is independent software reconstruction
of selected evidence, **not blind discovery or independent historical evidence**.

The complete first source pass and `independent01.json` froze before any new
producer code/result access. Only after that freeze were `run01.json`, `run02.json`
and their schemas read. The root parser itself was not imported or read to design
this extraction. The comparison and report-arithmetic functions were appended
after `# INDEPENDENT_EXTRACTION_END`; the extraction prefix remains byte-identical.

Protocol SHA-256:
`4406af3500c495adc95edd1c86e07901f73e6cafa43a39bfc57a8920c34c552a`.
The four authorized originals are SRC-116, SRC-119, SRC-120 and SRC-121.
Compressed and uncompressed size/hash pins are explicit constants; source
filenames never choose a new path. SRC-118 may be identified as an include
dependency, but its body was not read in this unit. Unknown keyword names are
hashed; comments and headings are not emitted. Title hashes do not authenticate
the physical meaning of a part.

## Actual extraction and integrity

`independent01.json` completed exit 0/PASS on the first historical-source
attempt, in **45.870129 seconds**, with **222,314,496 bytes observed peak RSS**.
All four gzip streams reached EOF and matched both compressed and uncompressed
pins before/after processing. There was no historical extraction failure.

| Source | Uncompressed bytes | Physical lines | Counted element records |
| --- | ---: | ---: | --- |
| SRC-116 | 17,314 | 1,921 | Damage sets, not active mesh elements |
| SRC-119 | 508,372 | 7,905 | 2,461 solids |
| SRC-120 | 232,959,541 | 4,088,491 | 2,042,843 shells |
| SRC-121 | 333,947,423 | 7,196,443 | 964,067 shells; 3,190 beams; 33,364 discrete |
| Total | 567,432,650 | 11,294,760 | 3,006,910 shells; 3,190 beams; 33,364 discrete; 2,461 solids |

The 512 MiB cap applies separately to each decompressed file, not to the
four-file aggregate. Each line is bounded at 16 KiB. The 768 MiB memory gate
checks observed peak RSS; it is not an operating-system allocation limit.
No node-coordinate arrays or decompressed body exports were created. Element
IDs are checked for duplicates within each explicit family; distinct families
are not silently merged into one namespace.

The parser independently reconstructs **459 PARTs, 459 SECTIONs, 379 MATs and
392 element-referenced parts**. Every used part definition is present. Of those
used parts, 23 reference 19 effective MIDs not defined in the inspected typed
geometry/material sources. The remaining 67 defined parts are not counted as
used merely because their definitions exist. Full numeric PART/SECTION/MAT
cards preserve blank fields as null, not zero properties, and retain exact
Decimal-valued strings rather than first converting them to binary floats.

Shell connectivity and required thickness continuation are paired as one
element, with fixed 8-character and 16-character fields respectively. Beam
orientation fields are not treated as additional physical endpoints. Discrete
records retain their family and zero-ground endpoint convention without a
physical span calculation. Both documented old single-card and two-card SOLID
forms have explicit shape handling; unsupported required variants fail safely.

Metadata is parsed at its specified fixed/CSV positions. The declared include
transform is checked numerically before assigning the SRC-120 offset. Raw
numeric card fields remain raw; PID/MID/SECID references receive only the
appropriate declared +1000, while zero/blank sentinels do not become IDs 1000.
The transform's four source rows and their original cardinalities are retained.
No temperature conversion, constitutive curve semantics, equation-of-state or
hourglass-definition join is inferred from those integers.

## Executed controls and preserved adapter failure

All **15 synthetic controls** passed before source processing and were rerun
for the later comparisons: fixed blanks, CSV blanks, adjacent full-width
fields, Decimal precision, rejection of nonnumeric labels/extra fields,
duplicate metadata, zero sentinels, blank PART title and unused-part handling,
definition/reference offsets, shell pairing/missing continuation, duplicate
element IDs, separate beam/discrete candidate joins and unsupported element
families. The standalone receipt is `independent-controls01.json`.

The first post-freeze comparison failed with a `KeyError` in the adapter:
plain `*INCLUDE` producer records omit `cards`, whereas the independent schema
stores an empty list. The correction was only below the frozen extraction
boundary, mapping that omitted non-transform card array to an empty list.
The failure is preserved in `independent-comparison01.json`, SHA-256
`49a4c8702051eb1188a8d0449034ee34110c111f64ac2cfd94420854a36c3379`.
It was not a source-value disagreement, and no source pass was rerun to repair
the schema adapter. Earlier source evidence is unchanged.

## Comparable producer results

`independent-comparison02.json` completed exit 0/PASS_COMPARABLE_SCOPE with no
failures. The tolerance was declared as absolute 1e-8 before comparison;
the **maximum observed numeric error is exactly zero** when the independent
Decimal values are compared to the producer's serialized numeric values.

The independently reconstructed coverage checked against the producer is:

- All **459 PART PID/SECID/MID references**, original/effective IDs and source
  locators, and all **392 used-part element-family count/presence rows**.
- All 19 missing effective MIDs, 23 affected used parts, the 379 effective MAT
  IDs, definition cardinalities and per-source element counts.
- **47 full selected PART cards**, including the 23 cross-region counterparts;
  **24 full SECTION blocks** and **20 full MAT blocks** provided by the root's
  selection. Full metadata card line numbers and null slots agree.
- All **1,904 damage-ID matches**: 1,543 explicit shells, six explicit beams and
  355 separate discrete-family numeric candidates. Connectivity values,
  source/line/PID and same-family/candidate distinctions agree.
- Both complete set-ID joins, the three include locations/targets and transform
  cards, and all four compressed/decompressed EOF/hash/line receipts.

This involves **25,227 independent numeric scalar checks**, 6,472 null checks,
812 boolean checks and additional list/map/value comparisons. These are
comparison operations, not that many independent observations. A separate
equality check confirms the two root result trees differ only in elapsed time;
its comparisons are recorded separately and are not credited as independent
source verification. No title-hash recipe differences occurred in the 47
selected PART comparisons.

The independent extraction additionally retains 23 outside SECTION blocks and
four outside MAT blocks absent from the root's narrower full-card selection.
They are not discarded or coerced to make selection sizes match. The four
additional effective MIDs are **1722, 1752, 1753 and 1782**. Conversely, the
root's curve point arrays are not independently reconstructed here. The report's
count of 59 DEFINE_CURVE blocks is independently checked through the retained
exact keyword-name hash counts; this does not verify their ordinates, referents
or historical solver use. Nonselected PART properties beyond PID/SECID/MID
were parsed but not retained as full cards in the independent checkpoint.

## Consequential distinction: absent where required, supplied elsewhere

All 19 missing effective master-region MIDs have same-original-ID definitions
in SRC-120 under different effective IDs. The counterpart set is 1025, 1033,
1711, 1712, 1713, 1723, 1731, 1733, 1741, 1742, 1743, 1751, 1761, 1762,
1763, 1772, 1773, 1802 and 1803. This is affirmative supplied-property evidence
and contradicts an unqualified assertion that those original-number material
cards are absent everywhere. It does not satisfy the master-region references
without an authenticated assembly/mapping change.

Each of the 23 affected master parts has an outside same-original-PID counterpart.
Nineteen complete raw PART numeric cards match. Four differ in their MID field:

| Original PID | Master raw MID | Outside raw MID | Outside effective MID |
| ---: | ---: | ---: | ---: |
| 722 | 712 | 722 | 1722 |
| 752 | 742 | 752 | 1752 |
| 753 | 743 | 753 | 1753 |
| 782 | 772 | 782 | 1782 |

Twenty-one cross-region title hashes match; those for parts 25 and 33 differ.
These comparisons describe source records, not equal mechanical behavior.
The four reference changes are a concrete reason not to treat same-number
parts as interchangeable. The tested ceiling is a namespace/property-reference
gap, not proof of why a definition is absent, what a historical executable read,
or what capacity the actual building possessed.

Part 98 is a different case: it has **1,106 beam records** and references
supplied section 98 and MID 50. Its six damage-list beam candidates, numeric
material/section cards and source locators all reproduce. They are not part of
the missing-MID group. An engineering reading of MAT024/SECTION_BEAM must still
use the separate primary-method review and historical-version caveats; these
numeric checks alone cannot establish yielding, fracture, deletion, calibrated
capacity or actual failure.

## Report-to-evidence assessment

The complete root `report.md` was read at SHA-256
`3aa26d1afa723da8c69876ff3711964259562cf6824a142176ff93909cd7dee9`.
`independent-report01.json` completes a separate PASS_REPORT_ARITHMETIC test
of all 14 derived summary fields plus the displayed 23-row table and 13
additional count/card assertions. It derives those values from the frozen
independent extraction without importing `summarize_materials.py` or rereading
source bodies.

In particular, the **16,324 shell records** in the affected parts, **206 of
1,543 shell-list matches** across seven affected parts, zero affected-part
discrete candidates, 19 identical/4 different raw PART cards, 21 matching
title hashes, source byte/line totals, beam IDs/lines and stated numeric MAT50
and SECTION98 fields all agree. Other shell matches are in parts 11 and 27.
The two tested DELETE_ELEMENT keyword families have zero active keyword-hash
occurrences in these streams; this is not a claim about every possible deletion,
restart or historical control mechanism.

The report correctly distinguishes a supplied outside-namespace counterpart
from a definition applicable to the master region; an unqualified absence claim
would be wrong. It also preserves the separation between selected damage IDs,
explicit-family records, cross-family candidates and actual failure/deletion.
No numerical correction is required in the reviewed report version.

This review checks report arithmetic and numeric card positions, **not the
primary manual/NIST prose interpretation**. Those portions are the separate
method-source review's responsibility. A numeric PASS does not independently
validate the claimed failure-strain semantics, cross-section interpretation,
calibration method, mass allocation, historical solver build or physical
connection model. The report's existing conditional wording and no-ranking-change
ceiling are essential, not optional qualifications.

## Artifact pins and repeat commands

| Artifact | SHA-256 |
| --- | --- |
| Frozen source extraction | `1cd998cff02b9cf4e947339fa1efbdaf1ae8bb6703fa644a61bab8ca26416a3c` |
| Extraction-time full script | `4c75b9a5e2d017928be05db9de8473c226718e1fcd282407c522dbd02714db79` |
| Retained extraction prefix | `4caa98ce70e5eb78125052da7ee97c42e3aac415fe25a28dcf66a1a77072fca2` |
| Verifier before final report-pin update, preserved snapshot | `d0138111f29ce25796d923b7fc0a8d21ffac87cc57f48fcb420696711f10e0e1` |
| Final verifier with adapters | `f29bd685260fcc86d9b5cc64aebfb81ee7d05ced716e6f6064ba537a0486ac07` |
| Passing comparison02 | `3997f9409c02bffc6c3d0d757da7b2b19d5336a1dcf5d27df52a2ee7f825ffcc` |
| Passing report arithmetic01 | `2b521f5b6dbbe037e56ecd9a07ffac46d106300f906434c1971435aa5c801846` |
| Standalone controls01 | `d9f2fcd5812ff50481f978baec195b4c3ac1b6d93147a3895e3678edbd2559f9` |
| Root run01 | `b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594` |
| Root run02 | `7663fa0b97ea7f3177aca68de215115db77b499da97530250d382d0214b129b3` |

The extraction-time whole script has a receipt hash, but only its unchanged
extraction prefix is retained verbatim within the later script; the CLI/adapters
have transparently evolved. No separate snapshot of that extraction-time full
script is claimed. The later pre-report-pin script is preserved in full as
`verify_materials-before-report-pin.py`, with the exact d013… hash above.

From the isolated worktree, the parent executed these exact consumer-verification
commands. Their create-only outputs now exist; any further repeat needs a new
unused output name. The first command reconstructs original sources; the other
two consume frozen derivatives only:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/material-run-crosswalk/verify_materials.py --output independent03.json
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/material-run-crosswalk/verify_materials.py --compare --output independent-comparison03.json
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/sherlock-wtc7-investigation/material-run-crosswalk/verify_materials.py --report --output independent-report02.json
```

All three parent-run consumer checks are now complete and their saved receipts
were read and hash-checked by this verifier. Each reports PASS and all 15 controls.
The fresh source run used the preserved d013… script and produced a result
object **exactly equal** to the frozen first independent result; this equality
was also directly checked here. The two adapter reruns used final f29… code.

| Parent consumer artifact | SHA-256 | Elapsed seconds | Observed peak bytes |
| --- | --- | ---: | ---: |
| `independent03.json` | `037f94228f5f8a6dce2514eb84abf95df5c3201492c3e25e88d2b3edba495a27` | 45.305560 | 220,135,424 |
| `independent-comparison03.json` | `da3bf4338cc6ab1134207609b66d22db31687bfbe410fc578230009e8ee6dd02` | 0.103096 | 41,844,736 |
| `independent-report02.json` | `23b8c47373c38b958e8a7eebc8c0f74c2247f4b9a35001e6a0ed00a8a643a3ff` | 0.008933 | 34,242,560 |

These are attributed consumer reruns of the independent implementation, not a
third independently designed algorithm or another historical source. AST syntax
and scoped diff-whitespace checks also passed. No new source work followed them.

## Final report revision reviewed

After the original report arithmetic PASS, the parent preserved that exact report
as `report-before-review-edits.md`, with matching SHA-256
`3aa26d1afa723da8c69876ff3711964259562cf6824a142176ff93909cd7dee9`.
The final report was read completely and compared against that preserved version.
Its SHA-256 is
`a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf`.
There are exactly three edits: curve arrays are explicitly labeled as lacking
independent source reconstruction; the damage list is described as not activated
in the inspected assembly rather than historically unused; and six abbreviated
beam source-line numbers are written in full. No arithmetic or source values
changed. The edits preserve and clarify the permissible claim boundaries.

The report-arithmetic adapter's report pin changed only after the parent's fresh
source pass finished, with the immediately preceding whole script saved and its
hash checked. The extraction prefix and all existing results remain unchanged.
Final disposition remains PASS for the numeric/namespace scope, with primary
semantic interpretations and historical run identity outside this review's
independent verification ceiling.

This bounded independent unit is terminal. There is no pending extraction,
comparison or report-arithmetic step, and no source/code change is proposed.
