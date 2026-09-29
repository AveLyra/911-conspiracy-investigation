# Actual verification and preserved failures

2026-09-24. Root integration record; no historical measurement or human
acceptance. Main was read-only. Research branch
`research/sherlock-wtc7-investigation`, HEAD
`e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`; intentional uncommitted WIP.

## Frozen scope and readings

|Artifact|SHA256|
|---|---|
|PROTOCOL.md|0c5a522ae46c220c1aa6f793a477008a39ee93dcb79aa4c53ec754f91530b260|
|LOCAL-REPRESENTATION-FOLLOWUP.md|e920a5e5bfe850263c62d4609b79429e68797d6a064c527873a80967f689258c|
|root-source-reading.md|4f0955fbca60825fb80f1fbe429b3e1fca85ab8056868ab4ac6a413f67faa3ee|
|independent-source-review.md|4fc02a331596390245cb856b8bafc4c2c573643181f5d2c651e3449ab67ae242|
|verification.md|384f28096aa5d75256e2cc9600ce1b26c1d27903df27d6637fb46ba13de1a349|

Root and the source reviewer each viewed all five newly rendered pages plus
the held whole physical256 page, the three new native representations and
the held Figure5-127 JPEG. These are six complete pages and four image
representations per reader, not ten independent observations. Both notes were
saved before interpretation exchange. Prior source familiarity and shared
selection preclude a blind or independent-historical-source claim.

Source criticism narrowed two report claims before closeout: fewer pixels
alone do not prove lower usable detail; a composite cannot recover the whole
window worksheet, but eligible no-fire cells can display a window code. The
delimiters and one letter in the embedded title remain unresolved rather than
being silently normalized to an exact filename.

## Render and extraction commands

Working directory for new outputs:
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/schmidt-source-lineage`.
After guards for absent `physical-164.png` and `figure530-000.jpg`, ran:

```sh
env FONTCONFIG_FILE=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/render02/fonts.conf /Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 164 -l 168 -r 110 -png /Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf physical
```

Poppler26.05.0 returned0 (the next `&&` command executed). Five PNGs were
created and completely viewed. No render diagnostic appeared. Existing
worktree-only font config SHA256
`efad83414e2fe278aecbc3da620fa7c6ce1ebfac3d691594dc9a99120b6701c3`.
The chained `pdfimages -f 167 -l 167 -j ... figure530` call failed because
the assumed bundled executable did not exist; whole shell command exit127.
`command -v pdfimages` also returned no executable. Do not describe the
original compound command as a successful extraction.

Fallback used the small fixed [extractor](extract_selected.py) with bundled
Python3.12.14/pypdf6.10.0. First run, code hash
`b9b31ea132f75eb7ff42e30c873ce17e17da0c060b6bd5b8d2f130e9fd1d7c65`,
failed on `ref.idnum`: ordinary dictionary indexing had dereferenced the
object. No output directory was created (confirmed with `test ! -e
representations`). The only repair was replacing XObject indexing with
`raw_get(name)`, retaining the actual indirect object identifier. Corrected
code hash `4b7cbd535b587ae95ed1ea1224be162dc8234cfa2c6be47426fafafa733935ce`.

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 extract_selected.py
```

Corrected run exit0; three fixed exports and `representations/receipt.json`
created without overwrites. Source hash matched before/after. JPEGs use the
decrypted terminal DCT streams; the screenshot is a lossless PNG of decoded
Flate RGB samples. Earlier exploratory use of pypdf's convenience `.images`
JPEG data yielded re-encoded bytes; direct XObject streams match the prior
held Figure5-127 exactly. That convenience conversion was not accepted as
native JPEG lineage and does not imply corruption of earlier derivatives.
An exploratory fitz check failed with ModuleNotFoundError; no installation.

## Independent and root reproduction

[verification.md](verification.md) contains the exact independently authored
pdfminer code and existing-directory collision wrapper. Root read both full
blocks, then executed both with bundled `python3 -B`, extracting the two
`python` fences and running their compiled code while capturing their JSON.
Root replay returned:

- Three independently parsed image objects match; both JPEG byte streams
  equal the exports, and all2,359,296 PNG RGB sample bytes equal source data.
- Five full-page PNGs have expected935x1210 dimensions and recorded hashes;
  no independent full-page rerender is claimed.
- Selected inputs/outputs unchanged; no warnings.
- The collision wrapper passes: producer exit1 with expected FileExistsError,
  zero stdout, unchanged files and member names. This is refusal before writes,
  not a second successful extraction. Stderr751bytes, SHA256
  `17146a7863f527bda9d163088fdab510e07f3089bb8e2dc69d34f74bdfd05085`.

This verifies only fixed-source representation and collision behavior, not
all formats, hostile-input security, output-partial recovery, or the scientific
interpretation. The source hash remains
`30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f`.

## Locator verification

The independent locator ran at15:17:14UTC:11,444 main file paths and23,096
worktree paths, zero matches. Both enumerations exit0/empty stderr and zero
Git components. Its physical-CWD/Git-root checks identify main at
`499cefc8a67f4870b62d181493560f0995e0e1ee` and the research HEAD above.
Five main intake/facts CSV/JSON files were covered; index search exit1 with
empty stdout/stderr. Exact predicate is preserved in [search log](search-log.md).

Root separately replayed using subprocess argument arrays, per-root cwd and
NUL-separated `rg --files --hidden --no-ignore -0 -g '!**/.git/**' -g
'!**/.git' ROOT`, checking return0, empty stderr and `.git` absent from every
path component. Case-insensitive basename matching used the same three regex
alternatives. Counts were11,444 and23,099, with zero matches. The worktree
count increased by three while new notes were being written; the exact set
difference was not separately retained or verified.
Sorted absolute-path lists joined byNUL with a finalNUL had hashes:

- Main: `5fb16f956e71c20639ea21efe5908a82b8846e2515c178c45d867b6b4e0b0530`.
- Worktree: `28bc6690121ea813101d774e6b384f0a15ef3a380045f8447bd7dd1fa36d1756`.

Root confirmed exactly these five index files and replayed the text search:

- `facts/fact-index.csv`
- `facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv`
- `facts/production-reconciliation/production-2025-06-05-manifest-summary.json`
- `intake/audits/2026-09-11-supplement-integrity.json`
- `intake/source-inventory.csv`

Result again exit1, no matches or diagnostics. These are finite name/index
queries, not full content/archives/correspondence searches or global absence.

## Boundaries and remaining work

New gallery source failure was investigated through ordinary native browser
navigation; explicit security block ended the route. No circumvention,
contact, source upload, original media acquisition, image synthesis, thermal
measurement, model execution or accepted Sherlock/Faraday mutation. Old denied
and approval-pending routes remain untouched. Generic panel-codebook/masked-
field feedback is deduplicated locally under SFB004/005, not sent while the
designated task's routing is unresolved.

The goal remains active. This unit completes its bounded retrieval/source
test but leaves native-photo/clock/workbook/model-input dependencies unresolved.
No main/raw/legal promotion, commit or push. Follow the current STATUS for
independent remaining work; do not turn these passes into scientific closure.

Final root checks: five frozen note/protocol hashes match; all eight local
Markdown link targets in report/validation exist; source PDF hash still matches.
`git diff --check` passes for tracked WIP (not a test of untracked files).
Main HEAD and its same seven pre-existing tracked dirty paths match intake;
this is a status check, not an assertion that every unrelated file's contents
were hashed. Root reread the final report. Generic feedback and research
navigation were updated locally; original source readings remain frozen.
