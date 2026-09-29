# Primary-source acquisition log

2026-09-20 UTC. Public, nonsensitive source retrieval under the protocol's
declared expansion; not a new disclosure of case files or strategy.

Two queries, each restricted to fema.gov/nist.gov/govinfo.gov:

1. `FEMA 403 World Trade Center building performance study chapter 7 Fiterman Hall debris WTC 7`
2. `FEMA 403 chapter 5 WTC 7 collapse debris 30 West Broadway`

The first located the agency's Chapter7, Peripheral Buildings; the second
located Chapter5, WTC7. Search snippets identify potential source-supported
outside-building damage and an approximate debris map; these are locator
leads, not inspected pages or adopted measurements. Search-engine recency
labels are not the report's publication date. Do not import the search
results' causal conclusions as premises for this debris-only test.

Selected exact public PDFs before acquisition:

- `https://www.fema.gov/pdf/library/fema403_ch5.pdf`
- `https://www.fema.gov/pdf/library/fema403_ch7.pdf`

Each retrieval is bounded to30seconds and30MiB, preserves response headers
and bytes, follows ordinary redirects and performs no authentication, access
bypass or route retry after denial. File-format, page count, hashes and
actual outcome must be recorded before source admission. No other result,
chapter or substitute domain is selected by this record.

## Actual retrieval and format checks

Both selected FEMA links returned HTTP 200 from the exact FEMA URLs. The
retrieved bytes are preserved under `source/` with response headers:

| file | bytes | SHA-256 | pages | PDF checks |
|---|---:|---|---:|---|
| `fema403-ch5.pdf` | 3,507,765 | `8f1f4dd1dd419c7fa2877e20dc8f3c152da0887e85c604e5cf8730a9fd554f22` | 32 | PDF; not repaired; not encrypted |
| `fema403-ch7.pdf` | 3,507,094 | `fa18b362784df0a2bf1816ecd81e3e5d0c6525ec54c7bc9a6000ad8a3c306887` | 20 | PDF; not repaired; not encrypted |

Retrieval was bounded to 30 seconds and 30 MiB per file. No retry after denial,
authentication, access-control bypass, private source, or additional source
was used. The selected-page renderer verified both FEMA hashes and the held
NIST NCSTAR 1A hash, rendered 12 complete pages at 150 dpi, reported zero
MuPDF warnings, and verified that all pinned inputs were unchanged.
