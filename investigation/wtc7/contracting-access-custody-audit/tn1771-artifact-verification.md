# TN1771: independent derivative integrity verification

September 28, 2026. Research only. This is a local artifact-integrity check,
not historical authentication, scientific validation, a model replay or an
assessment of the report's conclusions.

## Scope and separation

Main AGENTS/WORKFLOW/START-HERE and the main investigation CHARTER control.
The verifier read only the scope/acquisition portion of
[the TN1771 follow-through](tn1771-provenance-followup-2026-09-28.md), before
checking the PDF and its derivatives. The task separately authorized all
physical pages 1-46 for geometry and image-integrity checks. Root reported
terminal rendering exit 0 and supplied the receipt pin before the check.

The evidence-falsification-auditor, source-of-truth-guardian and PDF skills
were used to keep byte/representation checks separate from scientific source
reading. This verifier did not import the renderer, run a model, display a
PDF page or PNG, extract PDF text, or interpret page content. Existing text
derivatives were hashed as opaque bytes, not read as text. Source-body review
belongs to root and the separate scientific reader. Only this new note was
written; original files, previous notes and frozen review records were untouched.

## Source, receipt and exact coverage

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `nist-tn1771-source01.pdf` | 2,084,385 | `c94d92defa00689c906f54a7075e4887a1bdd86731688b34d98200ec29fc94e3` |
| [render receipt](tn1771-render01/receipt.json) | 236,526 | `6b7d81ac18ad024c3b53c0b45ae785d62bc4b6aa1570fce40f54fcb47bef210e` |

Both actual hashes and sizes matched the expected pins. Pypdf reports an
unencrypted **46-page** source. The receipt has exactly the declared sequence
`tn1771` physical pages **1 through 46**, with no duplicate or missing page.
The source pin in the receipt also matched the actual source file.

All **192 receipt-listed products** matched their byte counts, SHA-256 values
and resolved paths. The listed files remained within `tn1771-render01`; its
actual file inventory equaled those products plus the receipt. Products include
images, extracted-text files, per-page/parser/version logs, font configuration
and listed font-cache files. No missing or extra files were found.

Each of the **46 PNGs** passed signature/IHDR checks, Pillow `verify()`, a fresh
open with full `load()`, RGB mode, single-frame status, expected native size,
and an exact decoded-pixel SHA-256 match to the receipt's `pixel_sha256`.
All PNG headers are 8-bit truecolor.

Geometry was read only for the 46 declared PDF pages. Every page has
MediaBox = CropBox = `(0.0, 0.0, 612, 792)` points, rotation 0, UserUnit 1.
At the recorded **200 dpi**, every image is **1700 x 2200 pixels**. Expected
dimensions were calculated independently using exact fractions and ceiling
rounding, `ceil(page_points * 200 / 72)`, with rotation handling in the checker.
This is geometry/decoding verification, not a visual judgment of page fidelity.

## Actual command, versions and diagnostics

The read-only, stdout-only checker was supplied inline to:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

It used standard-library modules, Pillow and pypdf, not investigation renderer
code. Hash/header handles used context managers; image handles and the PDF
reader were closed. Python warnings and pypdf logger output were captured and
required to be empty. Runtime: **Python 3.12.14** (Clang 22.1.3), **pypdf 6.10.0**,
**Pillow 12.3.0**. The complete inline command is preserved in the task's tool
history, not as a separately pinned repository program.

The recorded argument array for each rendering was compared exactly against
its page, source and output prefix, using the following form:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -singlefile -r 200 -png SOURCE OUTPUT_PREFIX
```

Uppercase terms here are explanatory placeholders; actual receipt arrays were
checked, not re-executed. No crop flag was present. All **47 recorded commands**
have exit 0: 46 page renderings and one `pdftoppm -v` command.

- All **92 per-page stdout/stderr files** are empty, as is `parser.stderr`.
- The receipt's warning array is empty. Fresh PDF/PNG checking produced no
  captured Python warnings or pypdf logger diagnostics.
- Version-command stdout is empty. Its **144-byte stderr** was read and contains
  the normal Poppler/pdftoppm **26.05.0** banner and copyright notices, not a
  rendering warning. It would be incorrect to say all stderr files are empty.
- The receipt's input-before and input-after lists agree. The source entry was
  freshly checked. **Seven non-source dependency pins were not freshly rehashed**:
  the two renderer modules, pdftoppm executable, input font configuration,
  Python executable and the Pillow/pypdf package entry files. Receipt-pin
  agreement is not independent verification of those dependencies, their full
  transitive contents, or a hermetic execution environment.

Actual result: tool chunk `bce83a`, **exit 0**, reported wall time approximately
**1.12 seconds**. All source, receipt, inventory, page-order, geometry, PNG,
command-record and diagnostic assertions passed. No failed independent-check
attempt occurred in this unit, and no rendering was rerun.

## Before/after interval and evidentiary limits

One verification interval covered **194 distinct files**: the source PDF,
receipt and 192 products. Their actual byte counts and hashes were unchanged
between the before/after snapshots. The compact sorted-key JSON mapping of
absolute paths to byte counts and SHA-256 values has snapshot digest:

`cc6975b231d66d810e8f0112a6850c8b0baa12cf9616157bf1f805497949a8f3`

The full snapshot existed within the checker; only its digest is recorded here.
This is not a separately saved full-inventory artifact or a statement about
the files before acquisition or after the checking interval. Earlier floor-model
and thermal-paper checks remain separate intervals.

Root's scope/acquisition note reports one successful create-only curl fetch
from `https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1771.pdf`, after
its official web/frontmatter inspection. This verifier did not repeat or audit
that transport operation. Root-reported source acquisition and source-content
findings must not be attributed to these hash checks.

Integrity, successful decoding and dimensional agreement do not independently
prove accurate rendering against a fresh PDF render, correct text extraction,
authentic historical provenance, scientific adequacy, native model availability,
predictive rather than fitted agreement, or relevance to a historical WTC 7
failure. No curve digitization, sensor-history reconstruction or simulation ran.

## Prior official metadata locator: exact record

Before this artifact task, the same verifier completed a separate bounded
metadata pass. Exactly two queries were submitted once each, restricted by
`domains: ["nist.gov"]`:

1. `"NIST TN 1771" "Thermal Behavior"`
2. `"1771" "A Study of Thermal Behavior of a Composite Floor System"`

Both returned results. Only the
[official NIST publication catalog](https://www.nist.gov/publications/study-thermal-behavior-composite-floor-system-standard-fire-resistance-tests)
was opened: all **175 returned lines**, with material metadata at 115-162.
It identifies *A Study of Thermal Behavior of a Composite Floor System in
Standard Fire Resistance Tests*, **Dilip K. Banerjee and John L. Gross**,
publication date **October 26, 2012**, report **NIST Technical Note 1771**,
DOI **10.6028/NIST.TN.1771**. Catalog creation is October 26, 2012 and update
November 10, 2018. No draft/revision designation appeared in that catalog;
this does not establish a unique PDF edition or verified execution chronology.

The second query returned these exact PDF locators:

- `https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1771.pdf`
- `https://nvlpubs.nist.gov/nistpubs/technicalnotes/nist.tn.1771.pdf`

The metadata locator opened neither PDF and did not navigate the DOI. Their
byte identity/edition equivalence was not tested. Search automatically exposed
PDF snippets, including a TN1771 cover snippet listing only Dilip Banerjee;
this was retained as incomplete locator metadata, not body-review evidence or
a resolved authorship error. Root's later title-page reading is separate.

Metadata coverage was **two successful queries and one successful HTML open**,
with no empty query, failed web open, retry, new file, offsite search or download
by the locator. The title/catalog is a source lead, not proof of channel identity,
validation quality or a structural-sag comparison.

Local orientation did encounter output truncation: an initial combined full
STATUS/audit read was too broad. The locator recovered the current STATUS
opening, lines 1-54, and reread the complete preceding thermal-response audit
separately. Older STATUS history was not completely read, and the truncated
attempt is not represented as complete coverage. No query was repeated to
recover that local-read failure. The artifact task itself read only the new
TN1771 scope/acquisition portions and performed no new network retrieval.
