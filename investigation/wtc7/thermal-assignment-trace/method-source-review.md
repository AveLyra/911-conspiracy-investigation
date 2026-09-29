# Repeated thermal-node assignments: bounded primary-source review

2026-09-12. WP3 / Q06 / Q10. Working methods note, not a solver reproduction or a historical temperature finding. This reviewer worked independently of the new numerical row-order trace and did not inspect raw model payloads, member-map results, held material, or solver outputs. The sole permanent write is this file in the investigation worktree.

Controls read were current main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, and the investigation `CHARTER.md`, plus the two preceding model-member-map methods notes. The source-of-truth and evidence-falsification skills keep this note exploratory and distinguish a report's assertions from authenticated historical execution. The PDF skill supplied the page-level visual checks.

## Result and applicability

No applicable repeated-assignment rule was found in this bounded pass. Neither first, last, maximum, minimum, sum, nor average is established as the historical solver's treatment of repeated `*LOAD_THERMAL_VARIABLE_NODE` cards. A recorded row order remains an input property; it does not select the solver's effective temperature.

There is a concrete improvement over the earlier methods note's open-ended build uncertainty: NIST NCSTAR 1-9A, physical PDF **117**, printed **66**, section **3.6.3**, identifies **mpp971dR4 beta, revision 41161**, and says double precision was used for the global analyses. This is a **NIST-reported build**, not an independently authenticated executable or a demonstrated match between a historical run and the released input bytes. It provides a specific target for version documentation and run-record checks.

The report also identifies the transfer stage: PDF **107** / printed **56**, under *Temperature Application*, describes mapping the Case B, four-hour temperature profile to LS-DYNA nodal properties. PDF **103** / printed **52**, Figure **3-48**, places the temperature ramp at calculation time **6.5-8.5 s**, followed by applied ANSYS damage at **8.5 s**. The four-hour fire state and the calculation clock are different quantities. These pages do not specify spatial interpolation, ownership of a shared node, output-row generation, or resolution of repeated thermal cards.

Primary report: [NIST NCSTAR 1-9A, official PDF](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=861612). Its [official publication page](https://www.nist.gov/publications/global-structural-analysis-response-world-trade-center-building-7-fires-and-debris-0) identifies the report and links to that PDF.

## Documentary checks beyond the previously inspected card page

The earlier review established the May 2007 Version 971 expression `T(t)=TB+TS*f(t)` at PDF 1011 / printed 22.67. That finding is inherited from `../model-member-map/method-source-review.md` and `../model-member-map/method-followup.md`; this pass did not treat another reading of that page as new evidence.

The same [officially hosted May 2007 Version 971 manual](https://lsdyna.ansys.com/wp-content/uploads/2025/02/ls-dyna_971_manual_k.pdf), designated **M971**, adds these relevant limits:

- **PDF 46 / GS.2:** multiple keyword blocks are permitted; the manual describes input as order independent except for termination and explains that input is counted and reordered before fuller checks. This general description is not a rule for conflicting values assigned repeatedly to one node. It gives no support for assuming that textual last occurrence controls. The uniqueness instruction on this page concerns `*NODE` definitions; it must not be silently converted into a prohibition on repeated thermal-load records.
- **PDF 1004 / 22.60:** the VARIABLE and VARIABLE_NODE options share thermal load type 4. The allowed combination of options in one type does not specify how an overlapping node's values combine. These loads are described for structural-only analysis.
- **PDF 1009-1010 / 22.65-22.66:** the set-based VARIABLE option has selection/exclusion fields and the same base-plus-scaled-curve expression. Its inspected remarks supply no repeated-node precedence or composition rule.

The official [V971 R3.1 / R3.43919 release notes](https://lsdyna.ansys.com/ls-dyna-v971-r3/), *Loads*, describe a correction involving more than 99,999 load curves with `*LOAD_THERMAL_VARIABLE`. The official [V971 R5.1 / R5.64536 release notes](https://www.dynasupport.com/news/ls-dyna-v971-r5.1-r5.1.64536-released), *Loads*, describe an MPP optimization for disabling processor-unreferenced curves, including curves used by VARIABLE_NODE. Neither item is a repeated-assignment rule. Neither identifies behavior in the NIST-reported R4 beta build. Their existence is a reason to keep implementation identity explicit, not evidence that either feature or defect affected the released deck.

## Search coverage and finite stop

Eight initial public searches used the following query strings, with the domains restricted to `ansys.com`, `dynasupport.com`, and `lstc.com`, except the two WTC 7 queries, which were restricted to `nist.gov`:

1. `"LOAD_THERMAL_VARIABLE_NODE" "multiple"`
2. `"LOAD_THERMAL_VARIABLE_NODE" "duplicate"`
3. `"LOAD_THERMAL_VARIABLE" "last"`
4. `WTC 7 LS-DYNA temperature ANSYS transfer 971`
5. `"LOAD_THERMAL_VARIABLE" "same node"`
6. `"LOAD_THERMAL_VARIABLE" "overwritten"`
7. `"LOAD_THERMAL_VARIABLE" "sum"`
8. `"WTC 7" "LS-DYNA" "971"`

After the local report disclosed the exact version string, one justified follow-up query searched `"mpp971dR4" "41161"` across the four official domains above. It returned the NIST report, not an implementation description. This ninth search closes the bounded pass; it is not an exhaustive search of vendor archives or the internet.

Results included later-version manuals/release notes and NIST methodology. Later-version search snippets about other keywords, same-node constraints, sensor controls, or overwritten material parameters were not treated as rules for this keyword. No substantive result here relies on a third-party explanation or on modern-version behavior.

M971's complete 2,206-page extracted text was searched for `duplicate`, first/last definition/specification/occurrence phrases, and the exact VARIABLE_NODE keyword. A second full-text pass checked `overwrit`, `supersed`, `precedence`, `same node`, `more than once`, and `last occurrence`. These are discovery searches, not a complete reading of all pages. Complete selected pages read beyond the inherited card pin were **46-47, 61, 65-66, 739, 1004-1010, and 1012**. Pages 61 and 739 concern full-deck restart input and exchange-factor material definitions, respectively; their matching words do not govern this duplicate thermal-card question. The general-input and neighboring thermal sections above, rather than isolated search snippets, support the conclusions.

NCSTAR 1-9A's complete 173-page extracted text was searched for `971`, `interpolat`, `transfer`, `temperature distribution`, and `thermal loading`. Complete selected pages read were **1-4, 53, 103, 106-110, and 117**; blank front-matter pages were retained as such. The complete pages **103, 107, and 117** were rendered and visually checked, confirming the initialization diagram, mapping statement, and version/revision number.

The linked NCSTAR 1-9 was also checked locally for section 10.3.3 and nodal/interpolation references. Selected extracted pages returned by that discovery were **407, 481, 560, 569, and 631**. Page 481 / printed 415 identifies the Case B section, and page 631 / printed 565 repeats the global nodal-ramp account. These selected results did not supply a transfer algorithm or duplicate rule. This report is related NIST documentation, not independent corroboration of the same modeling process.

Selected web reading covered the NIST publication entry, the R3.1 release-note version header and *Loads* section, and the R5.1 *Include Options*, *Loads*, *Thermal*, and *General* sections. The vendor release-note directory linked by Ansys returned HTTP 403 through the web reader. The large NIST PDF exceeded that reader's size limit. Exact-term web `find` returned no match for some keywords visibly present in subsequently opened text; those failures were not treated as negative technical evidence. No paid account, private service, solver, or outreach was used.

## Source integrity and reproduction

The existing official-report copy in `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf` was read without modification. A fresh public download on 2026-09-12 produced identical bytes:

| Source | Edition / source pin | SHA-256 |
|---|---|---|
| NCSTAR 1-9A | November 2008 report with January 2009 change sheet; 173 PDF pages; 26,952,697 bytes | `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4` |
| M971 | May 2007 / Version 971; 2,206 PDF pages | `f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d` |
| Existing NCSTAR 1-9 local PDF | Read-only source-discovery dependency; no new byte match to its official endpoint performed here | `30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f` |

Fresh report copy: `/private/tmp/thermal-rule-source-pass.fnOtFZ/ncstar-1-9a-official.pdf`. The unmodified M971 copy remains `/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf`. A matching hash establishes byte identity between the acquired/local copies, not execution or physical validity. The HTML release-note pages were read online; no local HTML preservation/hash is claimed.

Acquisition used `curl --fail --location --silent --show-error --max-time 60 --output` with the exact official NCSTAR 1-9A URL above. The sandboxed attempt failed DNS resolution; a scoped network-approved retry succeeded. The failed retrieval has no engineering significance. The assumed bundled `pdftotext` path did not exist, so extraction used the bundled Python/pypdf runtime. No source was rewritten to repair extraction.

PDF extraction: `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3` with `pypdf.PdfReader`, page-by-page `extract_text()`; verified Python 3.12.14 and pypdf 6.10.0. Renders used `/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm` (verified Poppler 26.05.0), `-f N -l N -singlefile -r 100 -png`, and `FONTCONFIG_FILE=/Users/admin/docs/911/research/sherlock-wtc7-investigation/nist-camera-method-audit/fonts.conf`. Output prefixes are `/private/tmp/thermal-rule-source-pass.fnOtFZ/nist-pN`. All three render commands succeeded without stderr. Temporary public-source copies and QA images remain local.

## What would resolve the material uncertainty

The strongest new claim is **A, directly established as a documentary statement**: NIST reports the particular R4 beta revision above. A weaker and presently unestablished claim would be that those exact executable bytes processed these exact released files in that configuration. An authenticated run header, executable/build record, and input/include hashes could establish that bridge; contradictory run evidence would displace the proposed match.

For the duplicate-card question, the highest-value records are now specific:

1. Documentation or implementation notes for **mpp971dR4 beta revision 41161** specifying repeated VARIABLE_NODE behavior, including whether input sorting or MPP decomposition affects it.
2. The model-author temperature-mapping/export routine and its versioned node-assignment convention, matched to the released inputs. It must explain shared nodes, interpolation, repeated rows, and whether any preprocessing consolidation occurred.
3. The corresponding input echo/warnings and nodal thermal output, matched to the historical run, to distinguish a documented rule from what was actually processed.

None was acquired in this pass. A future separately authorized synthetic test could establish behavior of its tested executable and configuration; it would not, by itself, authenticate historical use or validate the physical thermal field.

Until those dependencies are resolved, report source order, repeated coefficients, and any explicitly labeled counterfactual reductions descriptively. Do not promote an assignment envelope or an assumed first/last reduction to a bound on the resulting temperature. No solver run, canonical promotion, case-record edit, transmission, commit, or push occurred.
