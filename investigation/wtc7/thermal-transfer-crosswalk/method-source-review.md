# Thermal transfer: bounded primary-source methods crosswalk

2026-09-12. WP3 / Q06 / Q10. Exploratory documentary review, independent of the released-script scan. This reviewer did not inspect raw model payloads, June-production scripts, held material, or new scanner output. The only permanent write is this note in the investigation worktree. No solver run, outreach, private transfer, canonical/legal edit, commit, or push occurred.

Current main `AGENTS.md`, investigation `CHARTER.md`, and the worktree `STATUS.md` thermal-assignment handoff were read for this task; `WORKFLOW.md` and `START-HERE.md` were read earlier in the same source-review assignment. The source-of-truth and evidence-falsification skills require separation of documentary descriptions from authenticated implementation and execution. The PDF skill required complete-page checks for the important method passages. The earlier duplicate-rule/build review remains frozen in `../thermal-assignment-trace/method-source-review.md`; those searches were not repeated.

## Result

The actual WTC 7 LS-DYNA nodal-temperature export program, implementation version, and provided-code reference were **not identified** in this bounded pass. Two positive findings nevertheless sharpen the next comparison:

1. NIST's WTC 7 account distinguishes an ANSYS thermal-load set from a **second thermal-load set for LS-DYNA**. It does not establish that LS-DYNA temperatures were exported from a completed ANSYS structural-response solution.
2. The expressly referenced tower predecessor documents a **closest-thermal-node** transfer algorithm. Its demonstrated destination is **ANSYS structural body loads for WTC 1/2**, not the WTC 7 LS-DYNA nodal-temperature keyword stream.

These are useful documentary leads, not an identified exporter or a rule for repeated thermal assignments.

## Which interface, and which direction?

The following crosswalk separates roles; it is not a reconstructed executable call graph.

| Stage | Documentary pin | What the passage establishes and does not establish |
|---|---|---|
| FDS gas field → thermal analysis | NCSTAR 1-9, physical PDF 455 / printed 389, §10.1 | Names the Fire Structure Interface (FSI); describes 100 s temporal and 1 m spatial averaging of the gas field. These are not LS-DYNA nodal-selection rules. |
| Thermal results → ANSYS structural loading | NCSTAR 1-9, PDF 457 / printed 391, §10.3.1; PDF 524 / printed 458, §11.1 | Describes 12 output instants at 30-minute intervals beginning at 12:30 p.m., ANSYS-compatible temperature/gradient body loads, and linear interpolation **between thermal load steps**. That interpolation is temporal. |
| Thermal-load data → LS-DYNA | NCSTAR 1-9, PDF 457 / printed 391, §10.3.1 | Separately identifies a second input data set. The generator, exact upstream files, spatial algorithm, and keyword-writing convention are not specified here. |
| ANSYS structural response → LS-DYNA initial conditions | NCSTAR 1-9, PDF 523 / printed 457, §11.1 | Explicitly describes fire-induced structural damage transfer. This is a distinct branch, not proof of thermal-export provenance. |

Source: [NIST NCSTAR 1-9, official publication entry](https://www.nist.gov/publications/structural-fire-response-and-probable-collapse-sequence-world-trade-center-building-7), linking its [official PDF endpoint](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861611). Page pins above refer to the hash-identified local 797-page copy below.

The prior [NCSTAR 1-9A temperature-application passage](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612), PDF 107 / printed 56, provides the downstream Case B four-hour nodal-profile description. It does not fill the implementation gap between the second data set and the released cards. This prior finding is inherited, not newly rediscovered here.

Consequently, “ANSYS-to-LS-DYNA exporter” is a search label, not a proven requirement that the exporter read structural-response results. A thermal-analysis result database could be the upstream source; the inspected documentation neither proves nor excludes that particular implementation. The exact generator could also consist of several routines. A single program name is not required for an eventual adequate crosswalk.

## Concrete predecessor algorithm, with limits

[NCSTAR 1-5G, official PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-5g.pdf), PDF **120-121 / printed 76-77**, §4.7.2, selects structural components, exports beam-centroid or shell-node coordinates/identifiers, loads the thermal solution at the required time, takes temperatures or gradients at the closest thermal nodes, and writes ANSYS-compatible body-load text. It repeats over the necessary locations and times. PDF **137 / printed 93**, §5.6.2, supplies the analogous truss/core-beam procedure; PDF **168 / printed 124**, §7.6, addresses core columns. PDF **215 / printed 171**, §8.3, describes transfer of the generated thermal-load files to the structural-analysis group, not distribution of generator source code. PDF **313 / printed 269** references ANSYS Release 8.0 documentation (2003).

This is a positive spatial-method lead for the **tower thermal-to-ANSYS branch**. NCSTAR 1-9 describes its approach as similar; similarity is insufficient to establish identical WTC 7 LS-DYNA selection, tie-breaking, shared-node handling, or output serialization. The Release 8.0 bibliography entry is not a WTC 7 executable identifier. No named WTC 7 exporter, implementation listing, or downloadable code package was identified in the inspected material.

## Named software in the supporting paper is upstream

The report's bibliography leads to Prasad and Baum, [*Coupled Fire Dynamics and Thermal Response of Complex Building Structures* — NIST publication entry](https://www.nist.gov/publications/coupled-fire-dynamics-and-thermal-response-complex-building-structures), [official paper PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=101257). It appeared in *Proceedings of the Combustion Institute* 30 (2005), 2255-2262; the NIST entry gives the 2004 conference date.

PDF **6-7 / printed 2260-2261** identifies **ANSYS 7.1 parametric design language** for thermal-model construction, **SLATEC** for numerical special-function calculations, and macros selecting external faces and imposing radiative heat flux. These concern thermal geometry/boundary loading, not an identified WTC 7 nodal exporter. No macro filename or WTC 7 export-version match is supplied in these passages. ANSYS 7.1 in this tower example and the separate Release 8.0 documentation citation above must not be combined into a claimed WTC 7 version history.

## Crosswalk test for the separately reviewed code

A relevant implementation bridge should establish the actual source thermal field, the destination geometry/identifiers, the spatial association and selection domain, and the writing of the resulting LS-DYNA thermal input. Matching filenames or generic words such as “interface,” “macro,” or “mapping” is insufficient. A routine that selects ANSYS nodes and applies existing body-load files may be an ANSYS structural driver, not the generator of LS-DYNA nodal cards. Conversely, an exporter need not use any particular APDL command vocabulary; absence of a selected token is not proof that the function is absent.

Still unresolved are the WTC 7 generator's source/version and invocation, source-result time/state and units, geometric association and ties, component/region selection, repeated-row generation or consolidation, and linkage from generated files to the released deck and historical run. These are dependencies to test, not claims that the underlying operations were incorrect. The tower method would be disconfirmed as a WTC 7 exporter explanation by implementation or run records demonstrating another mapping procedure. The bounded search failure is not evidence that the code never existed or is unavailable elsewhere.

## Search coverage and finite stop

Six targeted searches were performed, using `nist.gov`, with `ansys.com` also permitted for queries 3, 5, and 6:

1. `"WTC 7" "LS-DYNA" "temperature" "mapping"`
2. `"WTC 7" "ANSYS" "interface" "temperature"`
3. `"WTC 7" "LS-DYNA" "interpolation"`
4. `"NCSTAR 1-5G" "interface" "mapping"`
5. `"WTC 7" "thermal" "interpolated" "LS-DYNA"`
6. `"WTC 7" "FSI" "source code"`

Selected official results, the bibliography-linked supporting paper, and the NCSTAR 1-9 publication entry were then opened. No seventh targeted query was added. Material-property interpolation snippets were not mistaken for temperature mapping. The NCSTAR 1-5B appendices publication entry concerns FDS/FSI/ANSYS thermal validation, not an identified LS-DYNA exporter; its PDF was not added to this pass. No third-party explanation supplies a substantive conclusion.

NCSTAR 1-9 selected-range discovery searched PDF 455-457 and 589-646 for interface/mapping/export/program/script/subroutine/interpolation terms, and 523-540 for APDL/input/load-step/macro/mapping/script/version terms. Complete selected text read was PDF **1-3, 455-457, and 522-524**. This is not a full 797-page reading.

NCSTAR 1-5G's 340-page extracted text received program/script/subroutine/macro/source-code/APDL/mapping/LS-DYNA/version discovery searches, including a layout-extraction pass because ordinary extraction joined words. Complete selected text read was PDF **3-5, 9-10, 41-45, 100, 118-121, 136-138, 153-154, 168-169, 215-216, 233, and 313-314**. Blank/image-only extracted pages were not treated as proof of absent content. This is not complete substantive reading of all 340 pages.

The eight-page supporting paper received full-text discovery for LS-DYNA, map, export, source code, routine, macro, ANSYS, and SLATEC. Its opening abstract/introduction was read online and complete PDF **6-8** locally. No claim of reading every intervening equation is made. Complete rendered pages visually checked were **NCSTAR 1-9: 455, 457; NCSTAR 1-5G: 120, 121, 168; paper: 6, 7**. The full-page check confirms that the poorly extracted footer on 1-5G PDF 121 is printed page 77.

## Source integrity and reproducibility

| Source copy | Edition / extent | SHA-256 |
|---|---|---|
| Existing `authority/nist/wtc7/ncstar-1-9.pdf` | Cover: November 2008; 797 physical PDF pages; no fresh official byte-match performed in this pass | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |
| Fresh public `ncstar1-5g.pdf` | September 2005; 340 pages; 29,847,167 bytes | `f6aa637c05c4ff1ae2a6a5e9192471aa69e6e0aa97a4bbe5aa33afd68a3526ea` |
| Fresh public `prasad-baum-coupled-fire.pdf` | Journal volume 30 (2005); 8 pages; 761,491 bytes | `2bcbf4cb442d180c485e971ea504c4a3a17c21f618fd4c0e8b22aa60872d1019` |

The existing report was read at `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf` without modification. Fresh public PDFs and all renders are in `/private/tmp/thermal-transfer-method.abc7tO/`. Downloads used the exact official URLs linked above and `curl --fail --location --silent --show-error --max-time 60 --output`. The large 1-5G PDF exceeded the web reader's size limit; scoped network-approved acquisition succeeded after sandbox DNS failure. Those access failures have no methodological significance. Public HTML pages were read online; no preserved HTML hash is claimed.

Extraction used `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` (Python 3.12.14, pypdf 6.10.0), including `extract_text(extraction_mode='layout')`. Rendering used the bundled `dependencies/bin/override/pdftoppm` (Poppler 26.05.0), `-f N -l N -singlefile -png`, 105 dpi for 1-9/paper and 110 dpi for 1-5G. `FONTCONFIG_FILE` was `/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf`. All selected renders exited successfully without stderr.

Complete-page QA files, all in that temporary directory:

- `ncstar1-9-p455.png`, `ncstar1-9-p457.png`
- `ncstar1-5g-p120.png`, `ncstar1-5g-p121.png`, `ncstar1-5g-p168.png`
- `prasad-baum-6.png`, `prasad-baum-7.png`

Hashes identify inspected bytes, not historical execution or physical validity. This pass ends with the documented two-output distinction and a scoped predecessor-method lead; the actual WTC 7 LS-DYNA thermal exporter remains unresolved.
