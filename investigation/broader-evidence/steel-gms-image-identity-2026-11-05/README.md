> Public derivative of the November 5, 2026 native GMS photo-byte comparison.

# Byte comparison of overlapping GMS steel photographs

November 5, 2026. STL02–STL03 / B188 / H005. The [earlier catalog study](https://github.com/AveLyra/911-conspiracy-investigation/blob/45764423bccc2fade555b4a5d3cecf5d88a15db6/investigation/broader-evidence/steel-gms-disc-transmittal-2026-11-05/README.md) identified 21 candidates by shared case-folded basename and listed size. This unit tests the actual public mirror file bodies after verifying the operational media store. The [compressed-copy catalog](https://archive.org/metadata/nist-foia-09-42-r32) and the expanded [Internet Archive mirror](https://archive.org/details/NIST_9-11_Release_32) are separate representations.

| Check | Result |
| --- | ---: |
| Target paths in G33D9 / G33D11 | 20 / 21 |
| HTTP 200 responses that decoded as JPEG | 41 / 41 |
| Bodies matching their catalog-declared lengths | 41 / 41 |
| Candidate pairs equal by SHA-256 and full byte comparison | 21 / 21 |
| Distinct SHA-256 digests among the 41 bodies | 20 |
| Combined response size | 48,399,705 bytes |

Nineteen digests each occur in two placements. One occurs in three. The three-place example is the file with basename `C89-Sharp-4-4-02-Dsc02881.jpg`. It appears once in G33D9 under the Claremont grouping and twice in G33D11, once under `Column Buckling` and once under `Sharp-4-04-02`. The individual source URLs, SHA-256, sizes and pair IDs are in the source pins. Those three placements represent a single tested JPEG byte sequence.

## Scope and reproducibility

The unit re-parsed the pinned Release 32 manifest and selected every cross-disc pair with a shared case-folded basename. The 41 exact file bodies were fetched from the expanded mirror and retained in the verified operational store. Pillow decoded each JPEG. A separate pass recomputed all SHA-256 values, checked each against its acquisition record and compared full byte sequences for each of the 21 pairs. For independent verification, fetch each `source_url` in the source pins to a distinct path, check its `response_sha256`, then run `cmp` on the files whose IDs appear together in `compared_pairs`. Retrieval times in the source pins are request start times in UTC.

This establishes duplication within the selected public mirror paths. The result leaves original disc lineage, agency production scope, direction of copying, and any item-level preservation or building attribution open. One photograph in multiple folders supplies one image body. The folder labels `WTCI-102-I` and `WTCI-134-I` and the court opinion's additional `WTCI-143-I` wording remain separate records. [Court opinion, pp. 28–30](https://www.govinfo.gov/content/pkg/USCOURTS-dcd-1_15-cv-01991/pdf/USCOURTS-dcd-1_15-cv-01991-2.pdf#page=28)

## Open records

- Verify the 17 W14A, W14B and C12 target photographs separately. This comparison covers the cross-disc shared basenames. The prior catalog pass found all 17 in G33D9 and no exact basename hits in G33D11. A different filename or an edited derivative remains possible.
- Obtain the GMS transmittal and supplemental itemized production index to match disc identifiers to original transfer records and any replacement list. Archive paths and duplicates alone leave that mapping unverified.
- Obtain the dated specimen records and NIST attribution worksheet. The tested JPEG copies supply no independent specimen ID or building-of-origin determination.
- Carry the NSF sponsor report `UCB/CE-Steel-05/2002` forward under both cited dates. That search is separate from this image comparison.

The published derivative contains original notes and metadata. Source JPEGs and the full local acquisition record are retained separately.

[Source pins, hashes and pairs](SOURCE-PINS.json)
