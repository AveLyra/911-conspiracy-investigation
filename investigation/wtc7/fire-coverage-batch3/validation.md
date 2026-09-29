# Batch 3 execution and validation

2026-09-24. Research-only record. Root read the applicable main/worktree
instructions and the repository-orchestration, evidence-audit,
source-of-truth, development-verification, PDF and context-distiller skills.
The prospective protocol and both representation/key addenda remain intact.

## Acceptance, not just passing commands

Implemented: fixed extraction, 25 native-image paired observations, preserved
pair/full freezes, source review, independent comparison and integrated
51-figure coverage timeline. Verified within scope: source correspondence,
schema, exact comparison repeatability, independent arithmetic and source
attribution checks. **Not accepted as a complete 26-target native study:**
Figure 5-121 failed the declared representation gate. Its failure remains
visible in every coverage total and is not repaired by full-page viewing.

Neither software success nor separated AI readings validates camera
authenticity, optical detection accuracy, interior heat, physical model
sufficiency, causation, an operational bridge, human acceptance or the charter.

## Source/extraction and actual visual coverage

Held source: `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf`,
52,766,002 bytes, 797 physical pages, SHA-256
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.

`extract.py` imports the unchanged, pinned main `prepare_assets.py` and changes
only the declared output root/page selection/order for physical 251–286.
`assets/run01/wrapper-receipt.json` records the actual overrides and pins.
Wrapper SHA `01bcffbb573f3ad4bd1487371306622615a7e182f6b6c5e67681dfb83c9d44f8`;
imported extractor SHA
`d9dbd73bc7483e5e1d136085c257bc5db3c808db53e4d95b40feade9c71e5af1`.
The original extractor's differently scoped verification mode was not used.

The producer recorded 36 pages, 56 image objects/invocations and 317 products,
with no recorded producer diagnostics. The independent pdfminer.six parser
verified every terminal JPEG byte stream, native dimension and placement;
maximum placement residual was 0.0 PDF points. All 317 product sizes/hashes
and 328 recorded input pins passed. The encrypted PDF's stored ciphertext
differs from all 56 decrypted terminal JPEG streams: matching the latter is
report-image correspondence, not original-camera authentication.

Root and the source reviewer each actually viewed all 36 complete page
renders at original render detail, including source context not in the new
annotation set. Root and the observer each viewed all 25 complete native
JPEGs before reading the other's labels. The source reviewer also viewed
the 25 selected JPEGs for association. After both full freezes the observer
reviewed 14 specified complete pages; see their critical review rather than
crediting them with root/source review's 36-page coverage.

Root repeated four of the 23 remaining-image presentations following a
context continuation: 27 presentations cover 23 distinct remaining images,
plus the original two pair images. Repeated presentation adds neither a new
sample nor an independent observer. Root's prior pair first look and general
source knowledge remain disclosed. Controls test six textual scenarios, not
visual sensitivity/specificity. No manual observation record changed after
cross-observer/source exchange.

## Commands and results actually obtained

Working directory for the commands below is this directory. `python3` denotes
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Python is 3.12.14; the independent parser is pdfminer.six 20251230. The machine
receipts retain the source/code pins and runtime fields actually recorded by
each implementation; the initial tile receipt's dependency-pin omission is
disclosed below. Generated outputs used fresh paths; no old output
was overwritten to manufacture a repeat.

```text
python3 -B -m unittest -v test_compare test_reconstruct_tiles
  Root: 31 tests passed, exit 0 (0.598 seconds).
  28 comparison/schema controls plus 3 geometry controls.

python3 -B compare.py --labels root.json observer.json --out comparison-full01.json
python3 -B compare.py --labels root.json observer.json --out comparison-full02.json
python3 -B compare.py --scope pair --labels root-pair.json observer-pair.json --out comparison-pair01.json
python3 -B compare.py --scope pair --labels root-pair.json observer-pair.json --out comparison-pair02.json
  All four historical comparisons: exit 0.
cmp comparison-full01.json comparison-full02.json
cmp comparison-pair01.json comparison-pair02.json
  Both exit 0: byte-identical repeated outputs.

python3 -B -m unittest -v test_independent_observation_check
  Root: 7 tests passed, exit 0 (0.001 seconds).

python3 -B independent_observation_check.py \
  --full-runs comparison-full01.json comparison-full02.json \
  --pair-runs comparison-pair01.json comparison-pair02.json \
  --out independent-observation-root02
  Exit 0: all four comparisons independently match;
  both reviewers' pair rows unchanged within full records.
cmp independent-observation-root02/comparisons.json independent-observation-check01/comparisons.json
cmp independent-observation-root02/receipt.json independent-observation-check01/receipt.json
  Both exit 0: root replay exactly matches separate check.

python3 -B verify_extraction.py
  Technical reviewer: exit 0; 36 pages / 56 objects / 317 products / 25 selected.
```

Root replayed `verify_extraction.py` through `python3 -B -c` with only its
single output filename changed in memory from
`independent-extraction-verification.json` to
`root-extraction-verification.json`. The unchanged script was compiled with
its real `__file__` and the original script bytes remained the recorded
input. Result: exit 0, the same counts and 0.0 maximum placement residual.
`cmp root-extraction-verification.json independent-extraction-verification.json`
then returned 0. This is a same-code replay of the independent parser, not a
third parser implementation.

The independent observation checker imports no producer comparison code.
It independently validates all four frozen records, exact membership,
schema/enums, finite nonboolean coordinates, native bounds, reason presence,
smoke/target consistency, pair carry-forward and JPEG header dimensions,
then reconstructs every saved comparison. Its 42 input/code pins are checked
again at the end. Root read the complete checker and its seven controls;
replaying it verifies calculation, not the adequacy of image descriptions.

The comparison adapter preserves the old per-image schema. Its only in-memory
change to the pinned batch-2 source is replacing the fixed count 13 with the
new key's actual membership; pair/full keys are separately pinned. Symlink,
traversal, changed-input and existing-output guards remain enabled. Full
details and the initial fixture failure are in [technical-review.md](technical-review.md).

## Tiled image: failed method preserved and independently checked

The declared 17-strip gate returned exit 2, `accepted: false`, no decoded
pixels and no assembled PNG. Final-strip height residual:
0.03845249743589463 points; allowed 0.0001. Largest join residual:
0.000015299999972739897 points. Close joins do not imply common pixel scale.

The initial failed receipt pins tiles/key/addendum/producer but omitted
imported comparison dependencies then under development. It remains unchanged;
do not claim it had a fully frozen dependency closure. Root independently
recomputed the geometry from the preserved decimal CTMs using Ruby rational
arithmetic, importing no producer code and decoding no pixels. The exact
command is in `root-tile-check.json`. Final residual is
`7498237/195000000` points (about 0.03845249743589744), agreeing with rejection.
The independent result supports the failure conclusion; it does not
retroactively supply the original run's missing dependency pins.

## Source-qualified join and substantive review

`coverage-timeline.json` declares ten exact inputs. Root independently
rehashed all ten with Ruby/Digest and checked 51 rows: exit 0. Source reviewer
checked the exact prior-25/new-26 union, 50 distinct JPEG IDs/hashes, one
unscored 17-strip figure, ten matching context recurrences, source-family
links, 51 display-order members and seven empty completed-match lists.
Clock/floor statements remain attributed; nothing converts visible/labeled
floors into a burning-floor count. The
[separate technical join review](coverage-join-review.md) records its
independently executed checks, not a fresh all-page optical review:
1,745 assertions, 176 distinct actual files rehashed before/after and 364
inherited new-row source-field equalities, all passing. Its read-only
`check_coverage_join.py` is pinned at
`9297094bccd7ca3110c18a3249908b95f705e4310037d031f8f84608e9f65dd2`.
Root read all 144 script lines and ran
`python3 -B check_coverage_join.py`: exit 0, the same 1,745 assertions,
176 files, 364 equalities and zero failures. This is replay of the separate
join implementation, not another source/clock authentication.

Root freshly rehashed all four observation records, both anonymous keys,
protocol/addenda, source attributions/review, four producer comparisons and
the source PDF: all match their frozen pins below. Root read the complete
source and observation critical reviews before synthesis. The final critic
checks report claims and scope; it cannot substitute for original-camera
authentication, new Chapter 9 inspection or professional engineering review.

The [final critical review](final-critical-review.md) requested three precise
corrections: identify the full records as the exhaustive comparison, retain
facade-associated versus uncertain rather than asserting foreground identity,
and distinguish no independent model validation from a performed failed
test. Its optional timing-dependence clarification was also incorporated.
The critic re-read the entire assembled report and verified all four changes;
no frozen observation changed. Final report SHA:
`0290f01755f6e3116b231c68caebff689c0a7048f02414455ba9e578a7b04407`.
Rechecked final-review SHA:
`823ba515343128926af4310ac48f61da22ef29288afe88daaa4131b601f8f7a2`.
The technical reviewer separately checked this validation's claims and caught
overbroad wording about recorded runtime fields; the narrowed sentence above
now describes only fields actually recorded, with the tile omission retained.

Root's Ruby local-link check found all 17 then-present links across the report,
validation, source/timeline and final/coverage reviews, exit 0. The later-added
final-review link names the already-read existing file. `git diff --check`
passed for tracked research changes; this does not validate untracked content.
The preexisting seven-file main dirty list and research HEAD were rechecked
unchanged. No unrelated main changes were reverted or attributed to this unit.

## Important exact pins

| File / result | SHA-256 |
| --- | --- |
| PROTOCOL.md | `ecdd7be9123231e05217c456ebc5ffbaa71c7828802d1212e0ed26a784e559c6` |
| PAIR-KEY-NOTE.md | `dad716c5bee95ade5269556f2260cfe6659c810f1bbfa11703ad9fbba6717979` |
| TILED-IMAGE-ADDENDUM.md | `bede56a07730055dd16e20d6be22e3e1f32667504ee9028346cbb3e4bbebd724` |
| root.json | `e8e7b7d23e993c68ecc0ee0df16a39a9204d4b0665f9734e08096e21925044c5` |
| observer.json | `6c4021bd658cc7f7b64af061c320809cdec1cbe923803a690a12e13d0015e1ac` |
| root-pair.json | `d802f84a342b81a3386f1c7472ef3e2342a46133da61b7e7ca3bfee7e0b6fd44` |
| observer-pair.json | `795eb0b549f5883bce3d749cc85f16189ab577b1a8b792546181b70479ef5982` |
| full / pair anonymous key | `50144e50b2907bdd0dd4a62f398bedf3c8f40dc3008888580486496ddebd094f` / `5b01f713bd100c8eda211800b29e93704b023dd6f12aaaa7c7f1210fe79da8e1` |
| each producer full comparison | `9c78daeb0f7c81c71b7031095c3cbe2065bea142d369c2f75f76b83bf4664952` |
| each producer pair comparison | `f2fae74a01b5abc2f956cbc71b95d2610895dd679f0b88b7c8d42a0d9abf68fa` |
| each independent comparisons output | `2b4a91da7eb6467462610c75b375d3e408f0dbd6b9457786c6ffb7966abeabdc` |
| each independent comparison receipt | `d3202ef648e9368e9b3ad0f0a70858b1e7bf97648c3e94ba3139ab79e8ba12d6` |
| each independent extraction receipt | `ef80e0d3535c9e12a4a6be71623c52ed2622232dac52faa3266777ca49d35b89` |
| original failed tile receipt | `4c355391295581c4a02b9de7e296e6ccd52a65a8336c814b76c033ee5a62712b` |
| root rational tile check | `64a6409ebd969f176cdb818dc335cf5576ca222f6f6eb41ff37cafcae739e66c` |
| source-attributions.json | `c79c043fd6c0e87505481df94080f6d3a325c74f90e27f870a49f0b69a0cd20d` |
| source-review.md | `46808a13baf18f160b5290bd2b9b2fe04418e28eadc17985efe986cad1f708a0` |
| root-source-review.md | `8dd0bdc1c30ad1190302689615ee6fa5f708f13ecebe98d9ed97228837ab630c` |
| coverage-timeline.json | `08141aa6d221f80bec33501761b5f19030706bb1e0badfd035375bcb93c73aab` |
| coverage-timeline.md | `9f387e007e2cf2fc659c7c3074214c44b35b9bb91c45eb409d29bc98720ebce7` |

Additional source, page, asset, code and runtime pins reside in the receipts
and source/timeline manifests. Hash identity establishes which bytes were
used; it does not certify their historical truth.

## Failed attempts and scope boundaries retained

- The first combined synthetic run had four errors from a symlinked `/var`
  temporary-root fixture. Resolving the fixture root fixed the tests; no
  production path guard was relaxed.
- The first tile execution was sandbox-denied before output creation. The
  scoped authorized retry produced the rejection receipt, not an accepted image.
- Root's first rational-check command used unsupported Ruby `filter_map`;
  `map.compact` fixed only runtime compatibility. Criteria/data did not change.
- Read-only metadata probes for nonexistent summary/environment keys returned
  null; the actual schema was inspected instead. An earlier page-list probe
  used the wrong plural field, failed, and was corrected before page viewing.
  These are inspection mistakes, not evidence absence or successful reviews.
- A combined correction patch failed its context match and changed neither
  target. Root inspected the actual lines and reapplied the same substantive
  corrections with matching context. The final critic's two preliminary
  timeline checks assumed nonexistent enum names; its preserved review records
  the corrected actual-schema checks without changing data or criteria.
- Truncated combined text displays were not counted as complete reading of
  omitted content; required selected reviews were read separately. No full
  reading of the large research navigation/feedback files is claimed.

Main remained on its preexisting seven-file dirty list at the recorded
checks. Research WIP remains intentionally uncommitted on
`research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`. This unit edited only its own
directory plus narrow status/navigation and deduplicated software feedback.
No main/raw/legal/accepted-engine mutation, source upload, solver, outreach,
send, commit or push. Pending drawing/archive access and archived Sherlock
feedback-routing permissions remain unchanged. No universal all-Luna
clearance, physical cause ordering or goal completion follows.
