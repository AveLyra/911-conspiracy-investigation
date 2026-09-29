# Independent nonvisual receipt and timestamp reconciliation

2026-09-19. Research-only computational check. **Original-helper admitted
set complete:** all five completed run01 subsets and their five run02 repeats
are reconciled and materially reproduced. A separately declared kit-only v2
pair also passed and reproduced below: six admitted source pairs in total.
Camera2/001 and 27Angles/006 remain excluded. This is not full eight-source coverage
or visual screening. No source image, reference figure, visual/root/observer
note was displayed or interpreted in this lane.

## Independent method and actual result

The new `independent-reconcile.py` does not import the screening helper or call
its `frame_plan`. It reads every preserved `frame-inventory.stdout` row,
requires integer PTS and unchanged positive native geometry, and computes
bins by integer multiplication and floor division:
`bin = (PTS × time_base_numerator) // (time_base_denominator × bin_seconds)`.
It independently selects the first decoded source index in each occupied bin,
reconstructs all per-bin counts, first/last PTS, occupied range and internal
empty bins, and compares every planned and emitted-frame row.

Before historical inventory reads, four positive synthetic groups checked
negative PTS, exact boundaries, first-frame selection, gaps and rational times;
six negative fixtures checked duplicate/decreasing PTS, changing dimensions,
invalid integers, extra fields and empty input. All passed on the first run.
These are the checker’s controls, not a newly executed screening-helper suite.

| Completed subset checked | All inventory frames | Selected native PNGs | Overview sheets | Receipt product-hash references | Native geometry / time base |
|---|---:|---:|---:|---:|---|
| run01-VID-WTC7-002 | 232 | 8 | 1 | 46 | 720×480 / 1/15000 |
| run01-VID-WTC7-003 | 1437 | 24 | 2 | 80 | 480×360 / 1/90000 |
| run01-VID-WTC7-004 | 74983 | 167 | 14 | 390 | 320×240 / 1/90000 |
| run01-VID-WTC7-005 | 74982 | 167 | 14 | 390 | 320×240 / 1/2997 |
| run01-PESKIN-COMPLETE | 88924 | 198 | 17 | 458 | 1620×1080 / 1/1000 |

The initial three-source batch (002–004) passed: 76,652 inventory rows, 199
selected PNGs, 17 complete overview products, and 516 outer/source product-hash
references. The table now also includes the two subsequent original-helper
admissions, detailed below. Repeated
hash references intentionally include shared products listed in both receipt
layers; they are not 516 independent images or sources. No internal empty
bins occurred in these three inventories.

Every native PNG was loaded without display and checked for RGB mode, exact
stored dimensions, encoded-byte hash and size. Every overview was checked for
RGB mode, 960×1120 geometry, encoded hash, complete consecutive 12-sample
groups (last group may be partial) and no missing/extra PNG files. This checks
coverage and integrity, not the legibility or correctness of visible labels.
All selected showinfo integer PTS, sequence, geometry and filter time bases
matched the independent plan; rounded decimal log time was only a secondary
consistency check, never the binning authority.

The current source bytes matched the selection and all before/after source
pins. Current protocol, selection, helper, test and executable hashes matched;
snapshots and all outer/source product references were checked. All recorded
subprocess exits were zero. Probe/inventory stderr was empty. Each decode
contained exactly 13 reviewed software-colorspace fallback notices and no
other warning/error/fatal/panic line. Raw diagnostics remained local and were
not printed into this note or messages.

## Exact execution and reproducibility record

Runtime: Python 3.12.14 with Pillow 12.3.0, already installed. Command:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-video-lineage/independent-reconcile.py --run run01-VID-WTC7-002 --run run01-VID-WTC7-003 --run run01-VID-WTC7-004 --out independent-reconciliation-01.json
```

Exit zero. Result: 38,837 bytes, SHA-256
`e908efd1c5a96fd7a1a287e28723f2b561fbf08df7c10125e08ebca7481f617f`.
The checker is 11,862 bytes, SHA-256
`547cc1c701ac01cf08c466b6bcb3e2b6534176f0025298ada96a71dfdc658f90`.
The JSON retains full material-product pins, source and receipt hashes and
all checked control identities for later admitted-repeat comparison. Complete
path-bearing receipts are not expected to be byte-identical across repeats.

| Source ID | Current verified source SHA-256 |
|---|---|
| VID-WTC7-002 | `0c147549fa51c57686bd506c1d979af23835e72ac777fa30e2f2eb8b15aeb8be` |
| VID-WTC7-003 | `af5c19dd597ecbe3cafbd163550fcd9c3ee9225d7f7b4f8e7000eb8ffb8232a3` |
| VID-WTC7-004 | `c0614a1432591c920b5d8bb26990ec2f50b6f27952ce9293b38d199686a0fac3` |

## Coverage, failures and limits

Read completely: PROTOCOL.md, EXECUTION-2026-09-19.md, selection.json,
helper-review.md and helper-critical-review-2026-09-19.md. Main controls,
charter and applicable evidence/source-of-truth/verification skills were read
fully in this continuing agent lane; current control hashes were rechecked.
The helper was not imported or read wholesale: a targeted `rg` inspection
located the documented exact diagnostic message and showinfo fields only.
No `frame_plan` implementation was read for the independent calculation.

The first checker-file save hit an automatic permission-review timeout; a
read-only existence check confirmed that no file had been created. The single
permitted retry succeeded. No historical check failed and no acceptance rule
was changed after seeing these results. Saved helper/source files were not
edited. The checker, separate repeat comparator and exclusive result JSONs
are the only new computation artifacts from this lane, alongside this note.

VID-WTC7-001 was reported by root as refused at `frame_inventory_malformed`;
this lane has not independently diagnosed that failure or treated partial
outputs as admitted evidence. VID-WTC7-006 was later reported by root as
refused at `decode_diagnostic_review`; no partial output is admitted here.
CAMERA3-KIT-MP4 was reported by root as refused at
`frame_inventory_malformed`; that failed v1 attempt is not admitted. The
separately declared v2 kit pair is checked below. All five admitted
original-helper repeats are now reconciled; failed sources were not retried
unchanged by this lane or represented as visually absent.
Each refusal/unattempted status must remain distinct in the eventual
full-selection record. A revised-parser run requires its own specific
contract, controls and admission; the original checker remains pinned to v1.

The checker tests integer timing, product integrity and processing consistency
on preserved decoder output. It is not an independent historical decoder,
camera-original authentication, visual shot match, continuous pulse-duration
measurement or physical explanation. Fifteen-second coarse sampling can miss
shorter events even if every declared selected sample is reproduced.

## Incremental check: VID-WTC7-005

After root supplied its completed original-helper receipt, the unchanged
checker was invoked with `--run run01-VID-WTC7-005 --out
independent-reconciliation-02.json`, using the same absolute runtime/script
paths as the first command. Exit zero: all 74,982 inventory rows, 167 selected
native PNGs, 14 overview sheets and 390 outer/source product references passed
the same complete nonvisual checks. No internal empty bins; exactly 13
accepted software-conversion notices and no unknown warning/error. No image
was displayed or interpreted. Synthetic checker controls ran again and passed.

Result: 31,172 bytes, SHA-256
`d6db26ebb46cdbfd52bc1e7ee36668e714f865bb55f59c68127d7cc4070bb12f`.
Source: 181,624,272 bytes, SHA-256
`2e4c66dd912b79aa0dbddde683aef7d90b2679055f918a964c4f9757aab8c844`.
The cumulative four-source scope is 151,634 inventory rows, 366 selected
native PNGs, 31 overview sheets and 906 receipt product-hash references.
This addition does not change the unreviewed/refused status of other sources
or supply any admitted repeat comparison.
The first note-table edit mistakenly copied 004's time base into the 005 row;
inspection of the actual JSON corrected it to **1/2997**. The checker used
the correct source time base throughout; no calculation or result was changed.

## Peskin admission and original-helper repeats 002–005

The unchanged checker ran with `--run run01-PESKIN-COMPLETE --out
independent-reconciliation-03.json`: exit zero, 88,924 integer inventory rows,
198 native PNGs, 17 overviews and 458 product-hash references checked. Source
geometry is 1620×1080, time base 1/1000, no internal empty bins; 13 exact
accepted software-fallback notices and no other warning/error. Current source
pin: 696,711,067 bytes, SHA-256
`0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d`.
Result03: 36,960 bytes, SHA-256
`e1f4ed415df539b30df40a8e579f9e258d018949c1cbb23e7f4d25ac95518b02`.
The first command request timed out in approval before process creation;
output absence was verified and the single permitted retry succeeded.

The same checker then ran with four repeated `--run` arguments:
`run02-VID-WTC7-002`, `run02-VID-WTC7-003`, `run02-VID-WTC7-004`,
`run02-VID-WTC7-005`, and `--out independent-reconciliation-04.json`.
Exit zero. All 151,634 repeat inventory rows, 366 native PNGs, 31 overview
sheets and 906 outer/source product references passed the full original
checks. Counts, time bases, geometry and diagnostic dispositions equal their
respective first runs. Result04: 69,029 bytes, SHA-256
`11d223a2073908205709b490c3206dc9f26c48fe3310b8c70336dbdfbb6b57f3`.

The separate `independent-repeat-compare.py` was then invoked, using the same
absolute Python runtime and unit path, with:

```text
--result independent-reconciliation-01.json --result independent-reconciliation-02.json --result independent-reconciliation-04.json --id VID-WTC7-002 --id VID-WTC7-003 --id VID-WTC7-004 --id VID-WTC7-005 --out independent-repeat-comparison-01.json
```

Exit zero. A simple same/different-byte identity control ran first. Every
actual native and overview file was re-read, checked against the independently
verified pins and compared directly byte-for-byte across repeats. All **397
material images** match, as do each source's complete `planned-frames.json`,
`frames.json` and `frame-inventory.stdout` (12 data files across four pairs).
No whole path-bearing receipt identity is claimed. Output: 67,634 bytes,
SHA-256 `3f6112de27195cb572d19a9293eaba4ab03510d5c3481bb05f8fe9234b71c61b`;
its producer pin and all input-result pins are retained inside it. No image
was displayed or interpreted. No failed scientific comparison was discarded.

The five admitted original sources now cover 240,558 inventory rows, 564
native samples, 48 overviews and 1,364 receipt product-hash references. This
is still five of the eight declared sources, not a complete eight-source
screen. A note-edit patch with a stray unmatched context line was refused
without changing the note; the corrected patch succeeded. That edit error
did not affect scripts, data or verification results.

## Final original-helper admitted repeat: Peskin

Root supplied `run02-PESKIN-COMPLETE` after its completion. The unchanged
checker ran with `--run run02-PESKIN-COMPLETE --out
independent-reconciliation-05.json`: exit zero. All 88,924 inventory rows,
198 native samples, 17 overviews and 458 receipt-product references passed.
The same source/raster/time-base and diagnostic dispositions hold. The verified
source receipt SHA-256 is
`7bf293861be6b5202b324a2008444d1da7f40d990d084a15f2f5cd5140b86c56`.
Result05: 36,960 bytes, SHA-256
`61d85077b7e42e3df7dfa1fddd07f3544262ca799e4647971c21c9e89180b150`.

The separate repeat comparator ran with `--result
independent-reconciliation-03.json --result independent-reconciliation-05.json
--id PESKIN-COMPLETE --out independent-repeat-comparison-02.json`:
exit zero. All **215** actual native/overview files match byte-for-byte, as do
the complete plan, frame-table and inventory files. Result: 36,261 bytes,
SHA-256 `83f943389a2395ffe4b772b33d1ad79d517f286d4ac4054d0fd365bcf92ff67d`.

Across all five admitted original-helper sources, **564 native PNGs and 48
overviews (612 material images)** reproduce exactly. All 15 complete data
products (plan, frame table and inventory for each source) also reproduce.
Both runs' receipts have been independently reconciled, totaling 2,728 product
hash references; those duplicate references are not independent sources.
No whole path-bearing receipt identity is asserted. Original 001, 006 and kit
refusals remain outside admission; v2 requires the separate contract below.

All checking/comparison invocations exited zero on actual execution. A second
note-update patch had an unmatched line-break context and was rejected before
editing; it was corrected after inspecting the current note. This affected
only note maintenance, not source bytes, computation, acceptance or results.

## Separate kit-only v2 first-pass reconciliation

After root supplied the specific v2 contract and admitted completed kit path,
this lane read GRAMMAR-FOLLOWUP.md entirely, the full v1-to-v2 helper diff and
the complete revised test file. It did not import either screening helper or
execute `frame_plan`; root/other-reviewer execution of the 26 helper tests is
not represented as this lane's execution. The `diff` command returned its
normal status 1 for differences; hashes were then checked separately.

The new `independent-reconcile-v2.py` is a 6,083-byte, separately named adapter,
SHA-256 `45139bb3b4ebc3ea26a4fb1c1d2058fd6c3548e8b7a54653260d02c3d3c936d0`.
It verifies and compiles this lane's unchanged original verifier bytes into
memory, with exactly three count-guarded identifier substitutions: v2 run
prefix, source-ID parsing after removing that prefix, and the revised helper
filename for identity comparison. It does not execute code from media,
documents or either screening helper. All original product, diagnostic,
integer-timestamp and geometry checks remain. Its CLI admits **only the kit
ID** in v2-run01 or v2-run02.

A narrow independent bin-wrapper recognizes exactly one terminal delimiter
after three nonempty tokens, counts it, and passes the remaining exact fields
to the unchanged integer-bin checker. Before historical inventory checking,
the original four positive groups/six negative fixtures passed; three new
plain/all-trailed/mixed variants preserved plans and counts, and 13 negative
fixtures rejected leading/interior/repeated empty tokens, extra/unknown/
duplicate/missing fields, noninteger PTS, duplicate/decreasing PTS and geometry
change. No source inventory was rewritten or saved in normalized form.

Extra current-byte and snapshot checks covered:

| Control | SHA-256 |
|---|---|
| GRAMMAR-FOLLOWUP.md | `8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723` |
| screen_local_v2.py | `890963c2104f53813593b4e09da9b3c5892d2461a2a6a415f06f84842b31d8f9` |
| test_screen_local_v2.py | `61fee5f4bd23a6ce3b6abd372c3f40d6d9e0d3ea9ab3d71ebe745c239c731c83` |

Command, same absolute runtime and unit script location as above:
`python3 -B independent-reconcile-v2.py --run v2-run01-CAMERA3-KIT-MP4
--out independent-v2-reconciliation-01.json`. Exit zero. All **443** source
inventory records, **15** native RGB PNGs, **2** overviews and **63** outer/source
product-hash references passed. Source raster 720×480, time base 1/15360, no
internal empty bins; exactly one terminal delimiter was recognized and the
raw inventory hash preserved. Thirteen accepted software-conversion notices,
no unknown warning/error. No image was viewed or interpreted.

Result: 5,814 bytes, SHA-256
`54564700528a0381761b5d838b6da49db9f30885c73b0797fc41426568273d1b`.
Verified source: 3,996,436 bytes, SHA-256
`4ecc57a5dd23b56c7ec0368a309889f38fcd762fd4769a580e0e3c6ea379fe98`.
Verified source receipt SHA-256:
`d8a52061d7017392e26a2b2f8042954d86cf0f7697aeb58157ec373d1829876a`.

The original kit grammar refusal remains preserved as a failed v1 attempt;
this v2 success is a separately declared serialization compatibility result,
not an erased failure or revised source evidence. Root reports v2 Camera2
refused downstream at `decode_diagnostic_review`; it is not admitted or
diagnosed by this lane. Original 006 remains refused. The kit v2 repeat was
pending at this first-pass stage and is completed below. No conclusion about historical
authenticity, pulse duration, visual identity or mechanism follows.

## Completed kit v2 repeat and six-source aggregate

The same kit-only adapter ran with `--run v2-run02-CAMERA3-KIT-MP4 --out
independent-v2-reconciliation-02.json`, using the established absolute runtime
and unit path. Exit zero. The original checker controls and targeted grammar
controls passed again before historical reconciliation. All 443 inventory
rows, 15 native samples, two overviews, 63 product-hash references, exact
integer plans, coverage, showinfo fields, source/tool/control identities and
v2 declaration/revision snapshots passed. Exactly one terminal delimiter and
13 accepted software-conversion notices; no unreviewed diagnostic. Verified
source receipt SHA-256:
`916bb712553543f69649bb9eb9246258fcbfcf0dcd37bcbbc8bf33987c8b68c6`.
Result02: 5,814 bytes, SHA-256
`4286f4f9b7d767191c308c8c33aa269a651d4a4fe4d15a9c97fff6e18a365c0a`.

Then `python3 -B independent-v2-repeat-compare.py` ran under the same absolute
runtime and unit path: exit zero. It first checked a synthetic same/different
byte-identity control, pinned both independent result files by the exact known
hashes, checked their current source receipts, and directly compared all
actual files. All **17** native/overview images and the complete plan,
frame-table and inventory files match byte-for-byte. Output:
`independent-v2-repeat-comparison.json`, 3,589 bytes, SHA-256
`a2e7bc7a60648c433da5090f1ba08253a32c76ac9122cab95c63db33d71006a0`.
Its producer and input-result identities are preserved in the output. No
path-bearing whole-receipt equality or visual interpretation is claimed.

Final finite scope for this nonvisual lane:

| Admitted source pairs | Complete inventory rows per pass | Native samples per pass | Overviews per pass | Exact repeated material images | Exact repeated data products | Receipt product-hash references across both passes |
|---|---:|---:|---:|---:|---:|---:|
| Original-helper 002–005 and PESKIN-COMPLETE; declared v2 CAMERA3-KIT-MP4 | 241001 | 579 | 50 | 629 | 18 | 2854 |

**Excluded IDs remain VID-WTC7-001 and VID-WTC7-006.** Their reported failed
attempts are not visual negatives or accepted processing. The original kit
v1 refusal remains preserved alongside its distinct, declared v2 success.
This is all six admitted source pairs, not all eight originally selected
sources, and not all frames viewed by a human. No human review, historical
originality, clock time, pulse duration or causal inference is established.
