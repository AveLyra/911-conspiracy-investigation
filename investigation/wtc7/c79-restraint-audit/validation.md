# Column 79 restraint audit verification

Research only, September 13, 2026. This is verification of source interpretation,
input extraction and declared joins, not a licensed engineering review, physical
experiment, historical solver reproduction or collapse-cause finding. The
[report](report.md), [direct-incidence protocol](PROTOCOL.md) and
[contact extension](CONTACT-TRACE-PROTOCOL.md) define the scientific scope.

## Authority, runtime and source preservation

Worktree: `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`, branch
`research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. New unit artifacts and existing research
WIP remain uncommitted. Main is a read-only source dependency. No raw, canonical,
pleading or correspondence file was edited, no source program or solver was
executed, and neither Sherlock finding acceptance nor an operational Faraday
bridge was invoked. Held sources remain excluded. No commit, push or transmission.

Actual root runtime: bundled Python 3.12.14, NumPy 2.3.5, pypdf 6.10.0,
Poppler 26.05.0; dependency bundle 26.905.11957. Python executable:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Commands use `-B` to avoid bytecode writes. Selected-page PDF rendering used
the bundled `pdftoppm` and the previously verified local font configuration.
The bundled and PATH `pdftotext` probes failed; bounded pypdf extraction was
used instead. A missing local executable is not a source failure.

The geometry sources are preserved under the user-supplied supplementary
production folder on main. Each root extraction checks compressed bytes before
and after, reads all three admitted geometry streams to EOF, and records
decompressed byte/line/hash receipts. Comments, arbitrary titles and unsupported
keyword strings are suppressed or hashed, not executed or printed as instructions.

| Source | Compressed bytes | SHA-256 | Decompressed bytes / physical lines |
|---|---:|---|---:|
| SRC-119, discrete_mass.k.gz | 70,199 | 2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7 | 508,372 / 7,905 |
| SRC-120, elem_thick_to-renum.k.gz | 23,162,693 | c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59 | 232,959,541 / 4,088,491 |
| SRC-121, wtc7_global_8a_no-conn-matl.k.gz | 47,520,888 | f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d | 333,947,423 / 7,196,443 |

The thermal include is identified, not followed by these extractions. The two
candidate damage lists are not applied. A separate candidate-list join is
tracked below; it does not alter these frozen source-scan outputs. Hash equality
is preservation evidence relative to admitted bytes, not historical authenticity.

## Published-source inspection

The independent [source review](source-review.md) inspected 12 complete technical
pages: NCSTAR 1-9 physical 638–641 and NCSTAR 1-9A physical 80, 110, 130, 132, 139,
147, 158 and 172. Root separately viewed ten of those pages: all four 1-9 pages
and 1-9A 80, 110, 130, 132, 139 and 147. Root does not claim to have visually
reviewed 158/172. Full captions, legends and timing context were included;
text-extraction search hits are not counted as visual inspection.

Both originals were freshly hash-checked. NCSTAR 1-9 SHA-256 is
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`;
NCSTAR 1-9A is
`cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
Their PDF encryption flags are true, but ordinary local tools read them without
a supplied password. No decrypted/re-exported PDF was made. Inspection was
limited to admitted technical pages, not blanket clearance of unreviewed content.

Root visually inspected eight complete pages of the admitted May 2007 Version
971 manual: physical 364, 366, 370, 402, 403, 1161, 1171 and 1174. Complete text
was additionally read for 363, 365, 367, 369, 371, 376, 407, 1162, 1172 and 1173;
those text-only pages are not represented as full-page visual review. The
source PDF has SHA-256
`f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d`.
The 2025 URL directory is not its edition date. Root render commands completed
at exit 0 in `/private/tmp/c79-manual-root.xlKa1O/`. Applicable historical build,
initialization and control behavior remain unverified by the manual alone.

The separate [manual-method review](contact-method-review.md), SHA-256
`b720e2330f46efc75e527db2aa3154147e36fa0210eee4eecb6597d3a128bb55`,
records 47 complete page views: 1; 362–376; 394–395; 400–407; 472–476; 856–863;
1161–1164; 1171–1174. Root read that complete review but does not claim those
47 visual views as its own. This arm interprets the primary manual, not the
numeric source arrays. It adds concrete control/initialization dependencies
and cautions that no direct rotational constraint does not prove zero assembled
rotational effect. The report incorporates that distinction. The agent's initial
write failed at a disconnected approval service; absence of a partial target
was checked before the same bounded write was retried successfully.

## Direct node-incidence reconstruction

The producer [map_restraint.py](map_restraint.py) imports the admitted existing
[member-map helper](../model-member-map/map_members.py), pinned to
`f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b`.
Its 27 controls comprise 17 existing helper controls plus ten new graph controls,
not 27 separate structural experiments. [root01.json](root01.json) and
[root02.json](root02.json) are complete create-only extractions; each performs
two complete phases across all three geometry files. The complete result
objects are equal except elapsed_seconds; the saved files are not byte-identical.

The separate [verify_restraint.py](verify_restraint.py) implementation ran 15
controls and three full phases over the three geometry sources, producing
[independent01.json](independent01.json). Root had received the reviewer's
summary counts and PID1179 conclusion before saving its own code, but not the
independent arrays or implementation. Root did not adapt its selector to those
counts. This is independent algorithmic extraction, not blind discovery of
the counts; both arms also knew the earlier diagnostic/PID179 association.

The frozen [comparer](compare_restraint.py) checks both root outputs against
the independent result. [comparison01.json](comparison01.json) and root's
actual consumer replay [comparison-root01.json](comparison-root01.json) are
PASS and differ only in command and elapsed_seconds. The reviewer inspected
the consumer receipt rather than inferring success from a live process.

Compared common fields include all 952 seed and 20 neighbor records, ordered
physical vertices, part namespaces, source and element line locators, seed
intersections, 873 seed IDs, 891 coordinate triples, the diagnostic/part set,
two incident part references, three include edges, four transform cards,
five global element-count groups and the 3,593,049 unique-node total. Across
the two comparisons: 61,574 numeric scalars, 3,940 strings, 37 booleans and
1,962 nulls, with zero differences. The 28,686 compared coordinate components
include repeated per-element values; they are not extra independent locations.
Coordinates agree exactly as parsed binary64 values, not as source-decimal
strings or unrounded physical positions.

Fifteen comparer controls, all 15 independent controls and all 27 root controls
were replayed and passed. Controls cover family/ID/source/line changes, effective
part namespaces, vertex ordering and repeated slots, orientation-node treatment,
boolean IDs, blank padding and a one-ULP coordinate change. See the exact
[independent review](independent-review.md) for mappings and remaining coverage.

Important exclusions remain: root lacks independent coordinate source/line
locators, some continuation/full-definition cards and individual row locators.
The diagnostic-heading hashes use different recipes and are not coerced to
equality. Root's initial contact/NSET inventory and node constraint-field
statistics were not independently verified by this graph comparison. All
actual selected neighbors are shells, so this real-data agreement does not
establish exhaustive beam/discrete generality. The existing-output refusal
guard has synthetic coverage, not a claimed fresh full CLI refusal test here.

The reported 18 shared seed nodes at two exact Z levels were additionally
derived by root and checked by the independent reviewer from the frozen arrays:
nine at −71.1708 and nine at −43.6118, matching the saved seed Z bounds without
rounding. This is presentation verification, not a new source scan or floor map.

## Typed contact and set reconstruction

The root [trace_contacts.py](trace_contacts.py) and separately written
[verify_contacts.py](verify_contacts.py) parse the three observed contact
variants, typed node/segment/part sets and the frozen seed association. The
contact protocol was written after the first graph inventory but before the
new join. Root's first contact code and full pass were complete before receiving
the independent contact-count summary; no result selection was adapted to it.

[contacts-root01.json](contacts-root01.json) and
[contacts-root02.json](contacts-root02.json) each completed three geometry EOF
reads and nine synthetic controls. Their complete objects agree except
elapsed_seconds. The independent final extraction in
[independent-contacts01.json](independent-contacts01.json) completed all three
EOF reads, 22 controls, 18.977921 seconds and 143,949,824 peak bytes in its
receipt. Runtime/memory are implementation observations, not physics evidence.

The [contact comparer](compare_contacts.py) includes every one of the 93 typed
sets, 88 zero-intersection sets, 742 selected segments, three selected
nonsegment membership rows, six contacts, 36 numeric cards, 288 numeric slots
and 12 selector records. It also checks the three source EOF receipts for each
root comparison. Per root: 12,491 numeric, 730 null, 123 string and six boolean
scalars, zero mismatches. All 27 actual adapter mutation controls passed; all
22 independent and nine root controls were rerun and passed.

[contact-comparison01.json](contact-comparison01.json) and root's completed
[contact-comparison-root01.json](contact-comparison-root01.json) both pass.
The reviewer checked the complete consumer object: differences are only
command[1], command[3] and elapsed_seconds. Test-stderr hashes actually agree,
so no test-timing hash exclusion was required. Consumer replay is not another
independently implemented source extraction.

The comparer normalizes only explicit aliases/field meanings. Segment unique
membership means ordered four-node tuples; node/part unique membership means
unique IDs. Extra ordered segment rows are not full-attribute duplication or
duplicate contact pairs. Heading hashes here both cover the CID-plus-heading
card without CR/LF; the independent stripped-heading-only hash is excluded.
Some independent row ordinals/slot positions and full-attribute/unordered
duplicate statistics have no separate root counterpart. The detailed
[contact review](independent-contact-review.md) states these exclusions and
preserves zero results rather than discarding them.

### Preserved failed independent attempt

The first independent implementation passed 18 controls but its source pass
failed the declared 768 MiB memory gate at exit 1 before producing a numerical
result. [The original code](verify_contacts-before-memory-fix.py) and
[failure record](independent-contact-failed01.json) are preserved. That receipt
is a reconstruction of the observed failed invocation, not a fabricated
original machine receipt. Exact peak memory and inner source/line locator were
not captured: the final memory check masked the inner failure. No missing
value is supplied retrospectively.

The revised implementation uses compact numeric arrays instead of storing
large Python tuple/frozenset counters, retaining exact ordered/null semantics
and adding four controls. It then completed successfully under the same gate.
This is a failure and repair of our extraction software, not a NIST defect or
evidence about collapse dynamics. All earlier and final artifacts remain intact.

The root first metadata reader also did not recognize the ID-before-OFFSET
variants as headed contact cards; it safely hashed them rather than reading
the headings as numbers. The separately declared contact reader handles the
observed variants. Original graph results and their limited metadata are not
rewritten to suggest the first pass did more than it did.

## Typed candidate-list intersections

The [candidate protocol](CANDIDATE-JOIN-PROTOCOL.md) and later prospective
[Case A extension](CASEA-ID-EXTENSION.md) preserve the decision to move from
retained-data joins to the available small raw list. [join_candidates.py](join_candidates.py)
uses the source-pinned prior run06 result/receipts for set 2 candidate geometry
and the frozen independent direct graph. It does not re-extract the old whole
mesh. Set 2 node arrays are distinct physical vertices in first-occurrence
order, sufficient for membership but not complete repeated connectivity slots.
Beam orientation nodes and discrete cross-family matches remain separate.

The only fresh source read is SRC-117, compressed 103,872 bytes, SHA-256
`aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273`.
Each actual pass reaches EOF at 325,983 uncompressed bytes / 45,156 physical
lines, SHA-256
`a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25`.
Its 45,152 shell IDs are unique. No complete Case A geometry was reconstructed;
typed-ID overlap with the complete seed/direct-neighbor graph conditionally
determines exact shared-seed-node incidence. This is not contact/proximity
coverage or evidence of the list's historical purpose or activation.

All 1,543 set 2 shell records, six explicit beams and 355 discrete numeric
counterparts retain explicit zero seed/neighbor typed-EID matches and zero
shared-seed-node matches; orientation-only seed matches are also zero. The
beam list itself has 361 unique IDs, not two 361-element samples. Case A has
zero typed-ID overlap. No positive coordinate match occurs in these actual
joins; the matching-coordinate code path is tested synthetically only.

[candidate-join01.json](candidate-join01.json) and root's completed
[candidate-join-root01.json](candidate-join-root01.json) both pass all 17
controls and have equal scientific results and before/after pins. The reviewer
checked the actual complete consumer receipt: differences are command[1],
command[3], elapsed_seconds and peak_rss_bytes only. Root read the entire new
script and both protocols before executing its replay. This is same-code
consumer reproduction using previously independently verified geometry, not
a second independent candidate-join algorithm. The
[candidate review](independent-candidate-review.md) records exact coverage,
source/list locators, failure history and exclusions. An initial approval
timeout created no process; the checked retry is not a restarted live job or
a numerical failure.

| Additional frozen artifact | SHA-256 |
|---|---|
| CANDIDATE-JOIN-PROTOCOL.md | aa8360f3ec379479f79f161c5bacc8cf443321e62710e6701bd98077368213c7 |
| CASEA-ID-EXTENSION.md | d19acd0497e46b023ebe088dfbc40d35ad0f35751d1c09b46cb8f776cb7a5860 |
| join_candidates.py | 348fb74f1b6f93b57ee8b9f9f40810ad74e14bafc7470282f3f200735455fc81 |
| candidate-join01.json | a29de50566ccfba66001db77a50851f63f765769b40130ae22186f2211cda3d2 |
| candidate-join-root01.json | b346227545a2d8f7a7235c1b968834a7056a626a52fb84f04a59da873c6b1a1c |

## Frozen artifact pins

| Artifact | SHA-256 |
|---|---|
| PROTOCOL.md | b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d |
| CONTACT-TRACE-PROTOCOL.md | f367dab9cf29f4958afed5a354a37bfcf1d5cb0f92e8fc39aab3009c2e529c80 |
| map_restraint.py | 4d49ed698f9802a859a364d4f71721d54e1d3511b50bd96f7b02f5ac3bc7b520 |
| root01.json | f400538d74607464ea7e03a1692965f58c710c841df3a54833e202685e0bdfef |
| root02.json | 179682c5caf5cdfac31c508d88e545a843fb07839bb7150832333790ed9e90e3 |
| verify_restraint.py | 5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a |
| independent01.json | d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7 |
| compare_restraint.py | 787db0403077f275300b01b4ec2057f78f09a985a79ac0506989e0db2de789e7 |
| comparison01.json | e8170327902408d76cdc136342fc8d3c4017a92704d9027ba7fbfe5ea7e7455e |
| comparison-root01.json | 10bb00990aa15f9afbbfafa446c510e5c73e97ca1e5e37823152b60a6c23fba3 |
| trace_contacts.py | ba35168bab6391ddd1126433d00047ec18d3f24dde9b4fb4f9250b29241688d8 |
| contacts-root01.json | 04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859 |
| contacts-root02.json | 27d22a353b601d1bf2797ea80f846bebe4d42e8467f663778413897437770ed5 |
| verify_contacts-before-memory-fix.py | 5edd81e375e0e4c437a36a05d55f15714703120d40bf50ce61f71570608c188c |
| independent-contact-failed01.json | 32cd17305341a70d4d30c206b8f8bcf0024bf1b31ff108605581e59f8b8b5901 |
| verify_contacts.py | bcc87b26b50de22325a36a3da96343e1306230dd91e3efef240d6cece059b91b |
| independent-contacts01.json | b30b8ee5435e7cf8ce2ea979245b07fa4b0577606bf97638dbfd76b21043c7c3 |
| compare_contacts.py | e3298754cdcda2098ed376b4149384598d941f68e2c6245a84424b2a9c2c21f1 |
| contact-comparison01.json | 15e6c98727074d577ac1839b93a6525b4d0ae403996403da4ea73dd131b1e2e9 |
| contact-comparison-root01.json | eb8d0391fb08c59a2125afc46c7d81a1b5a2e9f8a15f4fefee99ef81172a20a0 |

## Reproduction commands

From this unit's directory, using the executable specified above in place of
`PY`, the actual root producer invocations were:

```sh
PY -B map_restraint.py --output root01.json
PY -B map_restraint.py --output root02.json
PY -B trace_contacts.py --output contacts-root01.json
PY -B trace_contacts.py --output contacts-root02.json
PY -B compare_restraint.py --output comparison-root01.json
PY -B compare_contacts.py --output contact-comparison-root01.json
PY -B join_candidates.py --output candidate-join-root01.json
```

Do not rerun these commands over existing results: use fresh output names.
The independent notes and JSON receipts preserve their exact commands,
producer/input pins, controls and comparison exclusions. Reading input files
and testing our parsers is not execution of the released model.

## Review and integration disposition

The final report SHA-256 is
`6b57c44b9e6b194b019a8a362cb5242ab1f3b69ec679907389382e5593d59fda`.
The source reviewer read the complete report and confirmed the requested
replacement of wording implying actual selected pairs with candidate pairings
under these definitions. The disposition is appended to the existing
[source review](source-review.md), with initial/final report hashes and exact
exclusions; no added numeric or manual interpretation is certified by that arm.

The separate numeric reviewer read the final report and the full substantive
validation at SHA-256
`e5e59c051b1b98ce9216a1db381e1cd09949f137447cb6dacc1ddbecab278f49`.
All stated numerical counts, denominators, source-line totals, candidate limits
and 25 displayed artifact pins passed. Its final disposition in the existing
[contact review](independent-contact-review.md) distinguishes that hash-pinned
review from subsequent root-only nonnumeric closeout/navigation additions.
No material numerical correction was required. Computational agent review is
not outside licensed structural or forensic expert certification.

The first [artifact receipt](closeout01.json) passed nine Python syntax checks,
13 JSON parses, 11 Markdown checks, 56 local links, 25 table pins and all five
frozen root/consumer pair comparisons. It is retained as an earlier snapshot;
the source-review addendum and final validation/navigation text were completed
after it. The [second receipt](closeout02.json) failed one navigation check:
the then-current validation linked to that same not-yet-created output file.
All numeric pair/hash checks passed. The failed receipt is preserved; this
was a self-reference timing defect in the closeout workflow, not missing
scientific data. The final `closeout03.json` records the current unit snapshot
under the same [checker](check_artifacts.py); its name is deliberately plain
text here so a future output is not treated as an existing linked source.
Existing closeout files
are deliberately excluded from its manifest to avoid self-reference; prior
checks are not retroactively rewritten. The worktree's `git diff --check`
and main `tools/validate_record.py --strict` passed; the latter checks record
headers, issue/fact links and citation tags, not this scientific conclusion.
No browser check applies to these local numeric CLIs and Markdown artifacts.

Root also encountered a wrong-checkout path probe, truncated diagnostic
displays and one patch-context mismatch during integration. These produced no
numerical result or source modification; corrected scoped reads/patches were
used. Such tool/inspection failures are not source evidence or successful
independent checks. The original failed independent contact pass remains
separately documented above rather than subsumed into these navigation events.

The research navigation and existing STATUS handoff now point to this unit
and its next slave-to-master geometry test. Generic typed-relation, card-order
and resource-failure lessons are deduplicated under SFB-004/SFB-005 locally.
The designated Sherlock task is archived and routing remains unresolved;
no send, acknowledgment, fix or bridge execution is claimed.

Nothing about a successful comparer establishes an
initialized contact pair, its surviving restraint, a physical column buckling
condition, historical run identity or intent. The broad investigation remains
active; this unit supplies a source/input bridge and a concrete next mechanical
test, not the charter's complete causal-chain assessment.
