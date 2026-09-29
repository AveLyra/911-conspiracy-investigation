# Thermal-response paper: independent artifact verification

September 28, 2026. Research only. This check establishes bounded local
source/derivative integrity, not historical authenticity, scientific adequacy,
experimental validation, a model replay, or a WTC 7 conclusion.

## Scope and authority

Main repository AGENTS/WORKFLOW/START-HERE and the main investigation CHARTER
control. The [prospective scope](thermal-response-followup-2026-09-28.md)
authorized this one target paper and all 27 physical pages under its short-paper
rule. Root reported rendering terminal exit 0 and supplied its receipt pin
before the independent artifact check began. Root and the separate source
reader own scientific interpretation; this verifier did not read their findings.

The evidence-falsification-auditor, source-of-truth-guardian and PDF skills
maintained the separation between artifact integrity and scientific review.
Only this new note was written. No source, receipt, product, model, drawing,
legal record or other research note was edited. No new network request,
renderer execution, PDF text extraction or source-content interpretation
occurred in the artifact check. Existing extracted-text products were hashed
as opaque bytes; no PNG or PDF page was displayed. Decoding images for pixel
hashes is not a visual/content review.

## Source and receipt pins

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `thermal-response-927871-source01.pdf` | 1,241,013 | `953b493d550eda3f8a00f67e4c05817e6112f4baedeb48e542f84a313de5b432` |
| [render receipt](thermal-response-render01/receipt.json) | 149,583 | `22720bbc011a580fea398bb420e3f39dbd0cb9b27f289212a82da44e47434e2a` |

Both pins and byte counts were independently recomputed. Pypdf reports the
source unencrypted and containing **27 pages**. All physical pages **1-27**,
in that exact order and with the receipt source label `thermal`, were covered
by the geometry/image checks. These pins identify held bytes, not a verified
publisher-to-local custody chain or historical authenticity.

The acquisition history in the root scope note says a first urllib request
returned HTTP 403 before creating a file, followed by a successful curl GET
of the same official public URL, without credentials or an alternate source:
`https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=927871`.
That is **root-reported acquisition history**, not a transport check repeated
or independently certified by this artifact verifier. The failed request is
retained rather than relabeled as a successful initial acquisition.

## Actual integrity and geometry results

All **116 receipt-listed products** matched their actual byte counts,
SHA-256 values and resolved paths. This includes images, extracted-text files,
rendering/parser/version logs, font configuration and listed font-cache files.
Product paths remained inside the declared render directory. Its actual file
inventory exactly equaled the listed products plus the receipt: no missing or
extra files. The receipt's page membership and order matched the independently
specified list of physical pages 1 through 27.

All **27 PNGs** passed:

- PNG signature and IHDR checks, including 8-bit truecolor headers;
- Pillow `verify()`, followed by a fresh open and complete `load()`;
- RGB mode, a single frame and the receipt's native dimensions;
- exact SHA-256 of decoded pixel bytes against each `pixel_sha256` value;
- independently computed dimensions from each source page's geometry.

All 27 PDF pages have MediaBox = CropBox = `(0, 0, 612, 792)` points,
rotation 0, UserUnit 1. At the recorded **200 dpi**, all images are
**1700 x 2200 pixels**. Dimensions were calculated using exact fractions,
rounding upward as `ceil(page_points * 200 / 72)`; the checker also handled
rotation explicitly. Page geometry access did not extract or display contents.

## Commands, versions and diagnostics

The independent checker ran as an inline, read-only, stdout-only program:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

It used standard-library modules, Pillow and pypdf; it did not import the
renderer or other investigation code. Hash/header file handles used explicit
context managers; Pillow instances and the PDF reader were closed. Captured
Python warnings and pypdf logger output were required to be empty, not ignored.
Runtime: **Python 3.12.14** (Clang 22.1.3), **pypdf 6.10.0**, **Pillow 12.3.0**.
The inline source is in the task's tool-call history, not a separately saved
and pinned repository program.

The complete saved argument array for every rendering was checked against
the exact source, physical page and output prefix, using this recorded form:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png SOURCE OUTPUT_PREFIX
```

The uppercase names above are explanatory placeholders. Actual receipt arrays
were compared exactly; the commands were **not rerun**. There is no crop flag.
All **28 recorded commands** have exit 0: 27 page renderings and one
`pdftoppm -v` command.

- All **54 per-page stdout/stderr logs** and `parser.stderr` are actually empty.
- The receipt's warning array is empty. The fresh PDF/PNG check emitted no
  captured Python warnings or pypdf logger diagnostics.
- The version command's stdout is empty; its stderr contains a **144-byte
  informational banner** for Poppler/pdftoppm **26.05.0** and copyright notices.
  The banner was read. It is not a rendering warning; not all stderr files are
  empty.
- Recorded input-before and input-after lists are equal. The source entry was
  independently checked against the actual source. **Seven non-source
  dependency pins were not freshly rehashed.** Equality of recorded pins is not
  a complete dependency audit or evidence of a hermetic execution environment.

Actual run: tool chunk `09bfc8`, **exit 0**, reported wall time approximately
**0.73 seconds**. All source, product, receipt, page-membership, geometry, PNG
and diagnostic assertions passed. There was no failed independent-check
attempt in this unit; the earlier empty metadata query and root's reported
HTTP 403 acquisition attempt are separate events.

## Exact checked interval and limits

One before/after interval covered **118 distinct files**: the source PDF,
the receipt and all 116 products. Actual sizes and hashes were unchanged
across that interval. The compact sorted-key JSON inventory, mapping absolute
paths to byte counts and SHA-256 values, has snapshot digest:

`6c528d58efaa194916b284412faca88c95b06a8ab998e7c73cdb3ef545fc5ecf`

The full snapshot existed within the checker; only its digest is recorded here.
This is not a separately preserved full snapshot artifact or an attestation
about bytes before acquisition or after the checking interval. No earlier
floor-model verification interval is merged into this one.

Matching saved hashes, pixel hashes and page dimensions does not independently
establish rendering fidelity to a newly rendered PDF, the correctness of text
extraction, source authenticity, validity of heat-transfer assumptions,
calibration independence, adequacy of reported agreement, structural sag
prediction, or applicability to the historical WTC 7 collapse. No model was
run, and no graph was digitized.

## Earlier official metadata locator: exact coverage

This verifier had previously completed the bounded metadata locator. The
following queries were each submitted once with `domains: ["nist.gov"]`:

1. `"927871" "Thermal response"` - **empty results**.
2. `"Thermal response of a composite floor system to the standard fire exposure"`
   - returned the official catalog, matching PDF locator and an author index.

Only [the official NIST publication catalog](https://www.nist.gov/publications/thermal-response-composite-floor-system-standard-fire-exposure)
was opened: all 169 returned lines, with material metadata at lines 115-156.
It identifies *Thermal response of a composite floor system to the standard
fire exposure*, **Dilip K. Banerjee**, *Fire Safety Journal*, publication date
**December 1, 2019**, DOI **10.1016/j.firesaf.2019.102930**. Catalog creation is
December 1, 2019, and update December 10, 2019. These are catalog fields, not
an independently established publication or execution chronology.

The second query returned the exact PDF locator
`https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=927871`; this locator
agent did not open/download the PDF or follow the DOI. Search automatically exposed
an extended PDF abstract snippet; it was not treated as reviewed body content.
The author-index result was not opened. The metadata pass used exactly **two
queries and one HTML-page open**, with no failed opens or retries. Its first
empty query is bounded negative search coverage, not an absence finding.

The catalog abstract describes comparison of predicted and measured heating
profiles and identifies structural analysis as a subsequent use. Those are
the publication's stated aims/claims, not this verifier's assessment of the
full paper or its scientific validation status. Root's subsequent acquisition
and the separate readers' page-content review must remain separately attributed.
