# Excerpt C lineage methods and verification

October 7, 2026. Follow the [prospective scope](PROTOCOL.md). All new artifacts
are research derivatives in the investigation worktree, not on main.

## Inputs and saved retrieval

| Input | SHA-256 |
|---|---|
| Main preserved 2020 secondary HTML | `1d01d8ffce7358095c7aaf605d9f6dd91c69ab1eaa5440afb19ab2402dd33a2a` |
| Existing late-fire CD-video parent response | `13684f381a30e3571566fd88f0e64c15635e78faf981f972fb20d10f21174931` |
| New CD138 request | `136e7a2e6cfd883c0d8816e706ac406a3be0d62be16cec865ebe6d5ff1277897` |
| New CD138 response | `aeedd9f7ddcbbbbf12bdcc840776cac19d830dacaaa784d02367b40bda159138` |
| Main NCSTAR 1-9 PDF | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| Reused Peskin page-277 render | `d53ea02bdd49539b25ef1e3d6cf20a11fa8b5823d540025a6148f6a75cd95528` |

The first two pins were independently checked by the read-only inventory
reviewer and checked again by root. The new request and response preserve
the complete connector objects, including null parent fields and access
qualifiers. One of four allowed folder listings was used; no metadata read
or media acquisition followed. This unused allowance is not evidence of
exhaustion. The historical parent listing and fresh child listing were
retrieved on different dates; their agreement is an ID/route match, not proof
that all parent or child content stayed unchanged between dates.

## Page inspection

Bundled `pdfinfo` identified a 797-page, 52,766,002-byte PDF. Bundled Python
3.12 pypdf extracted physical pages 277, 282, 284 and 286 to terminal output;
their printed numbers are respectively 233, 238, 240 and 242. Root then
visually inspected all four complete page images. The earlier 110-dpi
page-277 render was reused. Three new full-page PNGs were rendered with
Poppler 26.05.0 using the following command pattern and page numbers
282, 284, 286, without cropping or intensity adjustment:

```text
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f PAGE -l PAGE -r 150 -singlefile -png /Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf research/sherlock-wtc7-investigation/audio-listening-2026-10-05/c-source-lineage/pages/ncstar-1-9-physical-PAGE
```

The output directory was created explicitly before rendering. The scoped
worktree render command was approved and returned aggregate exit 0, followed
by successful hashing of all three generated PNGs. Individual renderer exit
codes were not captured separately. It emitted this diagnostic three times:

```text
Fontconfig error: Cannot load default config file: File not found
```

Root found the complete pages, credits, captions and page numbers readable.
This is visual adequacy for the credit check, not proof of pixel identity
with another renderer or the camera sources. A second rendering run was not
performed; no repeat-run equality is claimed for these three pages.

| Physical page | PNG SHA-256 |
|---:|---|
| 282 | `6aa98b3999269ca4bee0094f5b03292dd0a41ccbefa2b2a1aa3b57eeebd674b3` |
| 284 | `6449ec0500acd28fa4318e7ee08516be781bb4436a57b82599cf16e4498753c2` |
| 286 | `c030ffe79c90c854f441349ae86f1fb6fd6e9e2450508ab4bbcc1ab3db727bc4` |

An earlier attempt to call `/opt/homebrew/bin/pdfinfo` and `pdftotext` failed
because those paths do not exist. The bundled tools above provided the
successful path; that setup error did not alter or invalidate the source.

## Local verification

A read-only Ruby JSON check passed all nine assertions: exact requested URL,
top_k 1000, response isError false, five returned rows, four files and one
folder, five unique IDs, no exact target filename, exact five titles, and
the four catalog byte sizes plus null folder size. The command returned
exit 0. These are metadata-consistency checks, not content authentication.
All input and output pins in the tables were computed from actual files.

Root read the scientific abstract at the university-hosted source on October
7. Only its bounded finding of formulation-dependent laboratory pressure
behavior is used. The full paper and a WTC 7-scale acoustic prediction were
not evaluated in this unit.

The separate local inventory was performed by
`/root/quiet_mechanism_inference_review`, sharing the same sources and task
context. It was not blind, independent historical corroboration or a human
expert review. Its negative filename coverage does not exclude renamed files
or unenumerated archive members.

Root's final local checks parsed both new JSON files, resolved all eight
local links in the report/methods, passed `git diff --check`, checked the new
text files for trailing whitespace, and rehashed the unchanged source PDF.
These commands all completed successfully; they do not certify historical
authenticity or scientific acceptance.

The embedded-credit and catalog-name limitations are already covered by
SFB-004/SFB-005's September 16 lineage-key and September 20 catalog-semantics
fixtures in `SHERLOCK-FEEDBACK.md`. No duplicate issue or new external
message was created. Existing feedback-routing limits remain unchanged.

The [final separate review](independent-review.json) found no material issue
in report SHA-256 `c61c89bf1827cdb07cb96c46a324260ad1de4db8f84237e39958787640d30a71`.
It visually checked all four complete pages and independently passed nine
input/output hash checks, nine metadata assertions and the full-page PNG
dimensions using read-only Python. It did not rerender pages, inspect new
media or recheck the scientific abstract. The missing source-to-soundtrack
identity link remains its strongest objection to a causal inference.
