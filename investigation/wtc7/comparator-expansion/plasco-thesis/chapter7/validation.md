> **Preservation note:** This is a public derivative of a dated working research document. Source-access and verification statements below are historical reports; they were not independently rerun for this package. No source media, full-text papers, images or rendered pages are included. Missing linked items are identified in the text; local filesystem paths, if any, are withheld. The companion [provenance record](../../PROVENANCE.json) records the changes and original hashes.

# Chapter 7 documentary verification

2026-09-09. Static documentary work, not FE/CFD execution or historical authentication. The [protocol](PROTOCOL.md) was saved before the chapter was read. The additive extractor (supporting item not included in this public package) reuses the earlier chapter's parsing/rendering approach without changing its frozen code or outputs.

## Acquisition and generated coverage

No new source was retrieved. The preserved institutional thesis matches 12,229,604 bytes, 291 physical pages, SHA-256 `0d76577bbf898dfa2d1587d02f1cc51378d531e3b59983fc0d4db8665fd575b4`. The script refuses a different source baseline or existing run directory. Source, protocol, code, command, runtime, rendering diagnostics and each output are recorded in run01/receipt.json (supporting item not included in this public package); receipt SHA-256 `b0af034428537d4978f9f475a93da27d7c404909a5a6f9cf4c500150be636d6d`.

Command: use the bundled Python 3.12.14 with `-B derive.py --run run01`, exporting the existing thesis `derivatives/fonts.conf` as `FONTCONFIG_FILE` and its parent as `FONTCONFIG_PATH` before Python. The receipt retains absolute command paths and actual pypdf/Poppler versions. All 51 text/PNG page pairs were generated; all render return codes were zero with empty stdout/stderr. The source before/after fingerprint matched.

## Actual root inspection and checks

All 51 text pages, physical 227–277 / printed 212–262, were read in order in bounded complete-page batches. Root visually inspected these **33 complete pages**:

228, 231, 232, 238, 239, 240, 241, 242, 244, 246, 247, 248, 250, 251, 254, 255, 256, 257, 258, 259, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 275, 276, 277.

The first independent integrity check incorrectly assumed every page should be portrait 935×1210. It stopped on physical page 231, the landscape coupling diagram. That was a failed verification assumption, not a failed render or corrupted source. Inspection confirmed that page's 1210×935 full-page output. The source and generated files were not rewritten to satisfy the check.

A corrected check derived expected dimensions from each PDF page's media box and rotation at 110 dpi. It passed all 51 orientation-aware dimensions, all 102 text/PNG hashes and byte counts, source/code/protocol pins, exact page/crosswalk coverage and all 51 clean render receipts. Fresh pypdf extraction matched all 51 saved texts exactly. This root check did not rerender all PNGs.

Separately evaluated elementary arithmetic: `3*3600+20*60=12000`; `200*63=12600`; `12600/3600=3.5`; `126000/3600=35`; `2*3600+50*60=10200`; `0.37*180/pi=21.199438419840458`; `0.33*180/pi=18.90760723931717`; `4.2+1.5+5=10.7`. These check printed statements, not hidden historical clock arrays or an executed model. No figure was digitized, enhanced, corrected or substituted for its source.

### Subsequent complete root rerun

Root subsequently executed the unchanged extractor into the fresh root02 directory (supporting item not included in this public package), using the same pinned runtime and font environment. All **51 text pairs and 51 PNG pairs reproduced byte-for-byte** against run01. Source-before/after, code and protocol pins matched; exact physical-page coverage matched; all 102 render receipts across the two runs had zero return codes and empty stdout/stderr. The root02 receipt SHA-256 is `2bbeb4a6514b8465489a88621b16eb00b3a3991c30e678df2ac45a13b52c6f5e`. This later rerender supersedes only the earlier root check's no-rerender limit; it does not change the source, establish independent historical evidence or reproduce a structural solver.

## Remaining verification boundary

The completed [independent review](independent-review.md) read all 51 text pages, visually checked 34 complete pages before the primary draft and three additional pages at closeout (**37 distinct complete pages**), independently recomputed elementary arithmetic, verified all 102 derivative hashes and matched all 51 fresh texts. It did not rerender pixels. Its two precision recommendations were incorporated after root viewed physical pages 241, 242 and 248; the revised report also expressly rejects treating the original/revised cases as a one-variable ablation. These changes do not claim blanket independent approval of later unreviewed edits.

Native model/media acquisition, licensed expertise, physical validation, connection testing, dynamic impact, held-out comparison and journal/thesis equivalence remain outside this completed documentary pass. No case data entered Sherlock or Faraday and no protected acceptance or publication state changed.
