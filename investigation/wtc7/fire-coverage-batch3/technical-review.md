# Batch 3 technical review

2026-09-24. Research-only technical verification, independent of the two
visual annotators. This reviewer did not view image pixels, source captions,
source interpretations or historical observation labels while performing
these checks. Reading image headers, encoded streams and placement metadata
is not visual inspection. No source or prior batch file was edited.

## Result and scope

The second PDF parser reproduced the encoded JPEG bytes, native dimensions
and placement bounding boxes for all 56 image objects/invocations on the 36
physical source pages 251-286. Maximum bounding-box residual was 0.0 PDF
points against the extraction key. All 25 JPEGs in the frozen selected-image
key are included in those checks. All 317 products listed in the original
extraction receipt matched their recorded byte counts and SHA-256 hashes.
The independent receipt records 328 inputs and checks them again after the
calculation. This establishes technical correspondence to the held report,
not historical authenticity, figure association, visual accuracy or fire
severity.

The report is encrypted. For every one of the 56 images, pdfminer's stream
bytes before decipher differ from its decrypted terminal DCT/JPEG codestream.
The extracted JPEGs match the latter exactly. Calling predecipher ciphertext
the JPEG source would therefore produce a false integrity failure. Neither
representation is demonstrated to be original camera data.

The proposed 17-strip reconstruction failed the prospectively declared
common-scale requirement. The last 37-pixel strip has a height residual of
0.03845249743589463 PDF points relative to the first strip's vertical scale,
above the 0.0001-point tolerance. Its immediate join residual is only
0.00000010000007932831068 points; the largest join residual among all strips
is 0.000015299999972739897 points. Thus contiguous joins do not establish
equal pixel scale. No pixels were decoded and no PNG was written. The
failed gate and all tile byte pins, dimensions, object IDs, transforms and
row ranges remain in `assets/assembled01/receipt.json`. The source reviewer
was notified to retain an explicit unresolved representation rather than
invent a scored native image or a no-fire finding. There are 25 scored JPEG
representations, not 26 accepted native-image observations or 26 independent
exposures.

## Reuse and validation

`compare.py` loads the hash-pinned batch 2 `summarize.py` without modifying
that file. Its sole in-memory source replacement is:

```diff
- len(data["assets"]) == 13
+ len(data["assets"]) == len(SAMPLE)
```

The adapter supplies the declared pair/full membership and new protocol/key
pins. Every original per-asset field, enum, numeric/boolean, bounds, nonempty
reason, target/null and smoke-consistency check remains unchanged. The
original five-axis comparison and raw descriptions/rectangles are reused
without consensus edits, region matching, area totals or severity scoring.
Pair records pin the two-image key; full records pin the 25-image key under
`PAIR-KEY-NOTE.md`. Each key's exact bytes are frozen, so runtime membership
cannot be changed silently. Duplicate keys and asset IDs fail validation.

The adapter adds canonical containment checks and rejects symlinks in every
input/output path component. Outputs use exclusive creation. Protocol,
anonymous key, source JPEGs, adapter, imported batch 2 module and observation
records are checked before/after comparison and immediately before writing.
Both protocol addenda are pinned as inputs. The failed reconstruction means
the adapter accepts JPEG only; there is no permissive PNG branch.

All 31 synthetic controls passed before any historical observation summary:
7 reused rule controls, 11 reused per-asset/schema checks, 1 reuse-membership
load check, 9 adapter controls and 3 prospective geometry controls. The old
provenance fixture is replaced by batch 3-specific membership/path tests.
Pair/full samples are checked at
2/25 entries. Tests cover mismatched membership/hash/dimensions, duplicate
keys and reviewers, nonfinite/boolean coordinates, bounds, enums, reasons,
null and smoke consistency, source header failures, changed inputs, symlink
and traversal rejection, occupied outputs, exact repeat equality and an
independent synthetic comparison oracle. Synthetic source checks prohibit
pixel decoding. These controls test implementation behavior and schema
comprehension; they do not calibrate image detection.

The first combined test run had four fixture errors because the macOS
temporary-directory path used `/var`, a symlink. The fixture now resolves its
own temporary root; the production no-symlink guard was not weakened. The
rerun passed all 31 tests. The first historical tile command was denied write
access by the sandbox before creating the output directory; the authorized
scoped retry wrote the failure receipt and exited 2 for the declared geometry
rejection. No failure was converted into a pass.

## Commands actually run

Working directory for these commands was this batch directory. Runtime:
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

```text
python3 -B -m unittest -v test_reconstruct_tiles
  3 tests passed before the historical tile gate.
python3 -B reconstruct_tiles.py
  Scoped retry: exit 2; accepted false; 17 tiles; PNG written false.
python3 -B -m unittest -v test_compare test_reconstruct_tiles
  First run: 31 tests, 4 temporary-root fixture errors.
  After fixture correction: 31 tests passed, 0.595 seconds.
python3 -B verify_extraction.py
  Exit 0; accepted true; 36 pages; 56 objects; 317 products;
  25 selected JPEGs; maximum placement residual 0.0 points.
```

The independent parser is pdfminer.six; its exact version and the Python
version are recorded in the machine receipt. The producer uses pypdf. No
producer `--verify` route was called. No new source acquisition, network
request, original write, legal-spine update or engine import was performed.

## Pins and limits

| Artifact | SHA-256 |
| --- | --- |
| Independent extraction receipt | `ef80e0d3535c9e12a4a6be71623c52ed2622232dac52faa3266777ca49d35b89` |
| Failed tiled-image receipt | `4c355391295581c4a02b9de7e296e6ccd52a65a8336c814b76c033ee5a62712b` |
| Batch 2 reused source | `f24bb98a1b988a8eef20ae2095d5ec7fa6819e3520f0516cbca126c733641464` |
| Batch 2 reused tests | `e2b971fe187d60ca81c1475dd63afa13d3b137cbbdcfa2680cd557bc6d5995a5` |
| Comparison adapter | `593c51aad319739898aa8f0c3c8fc7e802f22904815b81adad36304327f6a6f7` |
| Adapter tests | `9484e6e54420615130cbf9d1917ee60cfb350e23a04391b39fe1c95901aa476b` |
| Independent parser script | `da7b95636b33740ece16d644a8f871324fe8892eeb4275654b597544758afb84` |
| Frozen full anonymous key | `50144e50b2907bdd0dd4a62f398bedf3c8f40dc3008888580486496ddebd094f` |
| Frozen pair anonymous key | `5b01f713bd100c8eda211800b29e93704b023dd6f12aaaa7c7f1210fe79da8e1` |

The tiled-image receipt pins its producer script, extraction key, addendum
and tile files but omitted its imported `compare.py`/batch 2 dependency pins.
Those dependencies were still being developed at that time. The saved
receipt is left intact, and no claim of a fully frozen dependency closure is
made for that first gate. An independent direct recomputation from the
preserved key is required to close that provenance limitation. The later
extraction receipt does pin the imported adapter and batch 2 source.

Full observation-record comparison and two exact repeated historical runs
are intentionally deferred until both complete records are frozen and root
requests the comparison. Independent full-to-pair row equality, independent
recomputation of the historical comparison, substantive reason adequacy,
figure/source associations, all visual reviews and the coverage join remain
separate acceptance checks. This technical pass alone does not accept the
whole batch or complete WP1.
