# Frozen saved-point observation comparison

2026-09-24. Research-only categorical comparison, completed after both reader
records were frozen. This checker read the protocol and both complete notes,
including reasons and viewing logs. No historical image was decoded or viewed,
no new coordinates or physical fit were made, and neither note was changed.
The comparison script imports neither the presentation producer nor its tests.

## Result and coverage

Both records contain exactly **83 unique ordered frame/track rows** matching
the pinned saved project and run01 manifest: PM05 has 43 rows (35 nonkeys and
eight keys); PM08 has 40 rows (all keys). The union is exactly 50 frames,
150 through 444 at spacing six. Missing counterparts are not scored:
PM08 at 150–204 and PM05 at 408–444.

Both notes contain exactly 50 ordered panel-view entries. Every listed hash
matches the corresponding actual PNG bytes, manifest product, and run01
receipt product. PNG headers also report 1128 × 648 for all 50 panels. Both
notes report complete original-detail viewing, including all 83 present
plain/marked crop pairs, with no skipped or failed views. This check establishes
the consistency and file identity of those recorded coverage claims; it does
not independently witness the readers' perception or certify their accuracy.

Strict category equality is counted separately for each axis. Root's explicit
one-to-one abbreviation legend is expanded to the observer's full category
names; that lossless notation expansion is not a semantic recoding. No
uncertain, unresolved, different-feature or negative class is combined with
another class.

| Subset | Rows | Host agreement | Feature agreement | Lower-foot relation agreement | All three agree |
|---|---:|---:|---:|---:|---:|
| All | 83 | 78 | 64 | 69 | 63 |
| PM05 | 43 | 40 | 27 | 31 | 27 |
| PM08, all keys | 40 | 38 | 37 | 38 | 36 |
| PM05 nonkeys | 35 | 35 | 23 | 23 | 23 |
| PM05 keys | 8 | 5 | 4 | 8 | 4 |
| All keys | 48 | 43 | 41 | 46 | 40 |

There are **20 distinct disagreement rows**: 16 PM05 and four PM08. There
are five host, 19 feature and 14 relation disagreements; these overlap and
must not be summed as distinct rows. These are agreement counts, not accuracy
estimates. Key membership describes saved metadata, not verified manual marks.

## Every differing row

Each entry below preserves both original category assignments. For compact
display only, use the root note's fixed legend: B=`building`,
M=`mixed_or_unresolved`; J=`corner_or_junction`, E=`roof_edge_only`,
U=`uncertain`, N=`none_resolved`; C=`candidate`, D=`different_feature`,
R=`unresolved`. Triples are **host / feature / lower-foot relation**.
The exact reasons for each listed frame/track remain in both unchanged notes
and are printed verbatim by the read-only comparison script.

| Frame | Track | Saved key | Root | Observer | Differing axes |
|---:|---|---|---|---|---|
| 252 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 258 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 264 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 270 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 276 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 282 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 288 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 294 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 300 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 306 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 312 | PM05 | false | B/J/C | B/E/D | feature, relation |
| 318 | PM05 | false | B/J/R | B/E/D | feature, relation |
| 330 | PM08 | true | B/J/R | B/E/D | feature, relation |
| 336 | PM08 | true | B/E/R | B/E/D | relation |
| 372 | PM05 | true | B/E/R | M/U/R | host, feature |
| 378 | PM05 | true | B/E/R | M/U/R | host, feature |
| 384 | PM05 | true | B/E/R | M/U/R | host, feature |
| 390 | PM05 | true | M/U/R | M/N/R | feature |
| 438 | PM08 | true | B/E/R | M/U/R | host, feature |
| 444 | PM08 | true | B/E/R | M/U/R | host, feature |

For a complete marginal accounting, the ordered pairs below are root/observer.
Unlisted pairs occur zero times.

| Axis | Ordered pair | Count |
|---|---|---:|
| Host | B/B | 75 |
| Host | B/M | 5 |
| Host | M/M | 3 |
| Feature | J/J | 37 |
| Feature | J/E | 13 |
| Feature | E/E | 25 |
| Feature | E/U | 5 |
| Feature | U/N | 1 |
| Feature | U/U | 2 |
| Relation | C/C | 37 |
| Relation | C/D | 11 |
| Relation | R/D | 3 |
| Relation | R/R | 32 |

## Semantic audit of the frozen reasons

**Neighborhood size is not standardized by this protocol.** It calls for a
location-neighborhood classification but supplies no radius or calibrated
distance threshold. Root expressly classifies a nearby feature association,
not the exact subpixel center. The observer also declares a neighborhood
reading, but uses `different_feature` when the displayed gap looks on an
adjoining roof segment beside a separately distinguishable step turn. It
would be inaccurate to call the observer's procedure an exact-center or
subpixel test: neither reader conducted one.

For PM05 252–312, this distinction is visible in the reasons themselves.
Root repeatedly acknowledges the marked gap on, below, or image-left of the
adjoining ledge while retaining the nearby foot as a candidate. The observer
describes substantially that same ledge/nearby-turn configuration but labels
the immediate marked neighborhood as roof edge/different feature. For example,
at 258 root says the candidate association is broader than exact placement;
the observer retains a broad junction-region reading as the alternative.
This is evidence of an operational-definition limitation, not grounds to
erase the 11 C/D disagreements or select one reader's label as truth.

PM05 318 and PM08 330–336 retain a further distinction: root uses unresolved
relation where the observer uses different feature. At PM08 336 both call the
local appearance roof edge; their relation labels still differ. Unresolved
is not a finding of sameness, and different feature is not an authenticated
historical replacement. No recoding is justified by their shared doubts.

PM05 372–384 and PM08 438–444 concern whether a weak local roof/face boundary
remains sufficiently readable amid smoke. Root treats it as building/roof
edge; the observer retains mixed host/uncertain feature. Those may include
genuine perceptual threshold differences as well as neighborhood emphasis;
this text-only comparison cannot adjudicate them. PM05 390 is a narrower
uncertain-versus-none-resolved distinction. Both give mixed host and unresolved
foot relation and allow a concealed building feature; neither reports physical
absence or destruction from that label.

The joint candidate rows are PM05 150–246 (17 samples) and PM08 210–324
(20 samples). Both record unresolved relation for every PM05 saved-key row,
360–402; this is not evidence that key rows were invalid, fabricated or manually
entered. Across the later samples, appearance agreement on a roof edge cannot
be silently promoted to agreement that a persistent material corner was tracked.

**Strongest limit:** a high agreement count here could reflect shared images,
saved-point cues, prior knowledge and broad categories, while a disagreement
can partly reflect an unfixed observation unit. These records do not furnish
independent validation of a historical track or a numerical localization error.
Neither can settle H0, publication-version identity, physical scale,
acceleration, support failure or a collapse mechanism. Human/qualified review
and the charter's separate measurement gates remain unmet by this comparison.

If a later follow-up needs a sharper distinction, it should separately declare
and test “feature somewhere in a defined neighborhood” versus “appearance at
the displayed cell,” with uncertainty and source-grounded spatial conventions.
That would be a new versioned protocol, not a correction of these frozen rows
or permission to retrofit a cutoff. No such follow-up was executed here.

## Pins and reproduction

| Input | Bytes | SHA-256 |
|---|---:|---|
| PROTOCOL.md | 7098 | `50785dd33e8543a0de76932be36e011693998cffa11a734040b3fb4f1ec3680d` |
| root-observations.md | 18738 | `e31b2f9cbc880872aec69201c155f27c0aa3d3bed9bb5cea8d7748976c853a76` |
| observer.md | 29001 | `9fe612f5df31b4a37557b57cde83d9f979499a5bf48744c06726ef4873b3b117` |
| run01/manifest.json | 326297 | `e32a70c421e4df661d9a2eeb8d057109668276a29597d8dab03fcfdca06f6fb6` |
| run01/receipt.json | 67109 | `18dd861e333aaea0675c06c56477b2c5442ae8e805ed6c7ba5895cb85ccca8a1` |
| ../tilted-camera-source-join/project01.json | 1078537 | `4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8` |

The complete 50 panel hash list is already preserved separately in each frozen
note and run01's manifest; it is not replaced by a new copied authority here.
The comparator hashes every actual panel twice and checks the two logs against
the manifest and receipt. It independently reads saved source key membership,
not a producer-derived assumption about which rows were manually marked.

Actual commands were run from this unit directory:

```sh
wc -l PROTOCOL.md root-observations.md observer.md
shasum -a 256 PROTOCOL.md root-observations.md observer.md run01/manifest.json run01/receipt.json
sed -n '1,150p' PROTOCOL.md
sed -n '1,200p' root-observations.md
sed -n '1,255p' observer.md
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B comparison.py
```

An additional read-only Python command printed the manifest/receipt keys,
counts and their source/manifest pins before implementation; no derived image
or observation was produced. The saved comparator run exited 0 with `PASS`
under Python 3.12.14. All six pinned inputs and all 50 panel byte hashes were
unchanged after checking. It reports the counts above and all 20 differing
rows, including both full reasons, to stdout without writing data files.

Comparator: `comparison.py`, 9109 bytes, SHA-256
`d907e6d235e91f0e29d7c78362b8264e36bb4b591c92766fb7fe773960d6f4b1`.
Only this note and the comparator are added by this follow-up. The producer,
tests, sources, generated runs and both observations are untouched. The
evidence-audit discipline shaped the explicit semantic ceiling and preservation
of disagreements; no historical or legal conclusion is promoted.
