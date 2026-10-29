# Four AWA-570 copies: different PDF entities, matching tested page representations

**All four acquired NARA copies have 65 pages. Their complete file bytes differ, but every page's extracted text and rendered pixels matched the comparison reference under the stated method.** Different modification timestamps and instance identifiers remain preserved. This does not demonstrate a change to the displayed historical account between these copies, and it does not explain every binary difference or authenticate their earlier history.

This advances B129 / FAA PD01–PD04 and **BVC-T03**, the counterpart-copy question in the [preceding review](https://github.com/AveLyra/911-conspiracy-investigation/blob/2fe66dcb3817ed3d37b2594805f950d6cd4854ee/investigation/broader-evidence/faa-bulletin-version-control-2026-10-29/README.md). That review and its exact conflicting observations are unchanged. The three copies described there as unacquired are now held and tested here; the exact interview-exhibit/native version chain remains a different missing input.

## Entities and timestamps preserved side by side

These are four catalog placements of AWA-570, *Summary of Air Traffic Hijack Events*, not four independent investigations or four established historical editions. The actual public download links were read in each catalog UI before acquisition. All originals were retained separately without deduplication or modification.

| NARA identifier / catalog placement | Acquired bytes | PDF `/ModDate`, exactly as stored |
|---|---:|---|
| [7596136 — AAL77](https://catalog.archives.gov/id/7596136) | 4,439,909 | `D:20131105191925-05'00'` |
| [7597139 — UAL93](https://catalog.archives.gov/id/7597139) | 4,439,875 | `D:20131105113219-05'00'` |
| [7597905 — AAL11](https://catalog.archives.gov/id/7597905) | 4,439,887 | `D:20131106105214-05'00'` |
| [7598444 — UAL175](https://catalog.archives.gov/id/7598444) | 4,439,891 | `D:20131106142716-05'00'` |

The new acquisitions occurred October 29, 2026; [SOURCES.json](SOURCES.json) gives each exact access time, exposed URL, page count, byte count and full SHA-256. Every file has a different SHA-256. The catalog's coarse “3 MB” label remains alongside the measured counts; its display convention/entity mapping has not been authenticated. Do not treat a matching count or label as a substitute for byte comparison.

The inspected Info dictionaries share `/CreationDate` **`D:20051116095539-05'00'`**, `/Creator` **`Canon DR-9080C TWAIN`**, and `/Producer` **`Adobe Acrobat 10.1.8 Paper Capture Plug-in`**. Selected XMP fields give the same create-date/tool/producer values in their own syntax, the four respective modification/metadata timestamps, a shared DocumentID and distinct InstanceIDs. [METADATA.json](METADATA.json) retains the literal fields, identifiers and each decoded XMP-stream hash. The shared ID is a metadata association, not independent proof of common authorship, complete lineage or authentic historical statements.

These are reported PDF metadata values. They are **not independently authenticated creation, modification, event, dispatch or receipt times**. The 2001 cover/event labels, 2005 creation fields and 2013 modification fields are different labelled observations; no preferred reconstructed chronology, responsible operator, processing cause or wrongdoing is inferred. No claim that metadata alone explains all different bytes is made.

## What the content comparison actually tested

The preserved 7596136 body was the computational reference, not a preferred historical account. Each whole PDF was rendered once with **pdftoppm 26.05.0 at 120 dpi**, with identical settings. All **260 generated page images** were decoded with Pillow 12.3.0. Image mode, dimensions and SHA-256 over decoded pixel bytes matched for every corresponding page in each candidate/reference pairing. Comparing decoded pixels avoids substituting PNG compression/metadata for the displayed image.

All 65 pages of each PDF were also extracted with **pypdf 6.10.0**. Exact per-page UTF-8 text hashes matched without whitespace or spelling normalization. The result is **no differing page in either tested representation** across the three comparisons. These are dependent comparisons of the same page positions, not 195 independent historical confirmations. [PAGE-COMPARISON.json](PAGE-COMPARISON.json) supplies each file's pagewise text and decoded-pixel hashes and all comparison outcomes.

There was **no new all-page human reading**. The preceding review's selected six book images and 14 interview images remain separately described; they are not recounted as new readings. No changed-page region was selected for fresh transcription because the comparison detected none. Text equality alone would have been insufficient: the preceding review demonstrated that the graphic cover's extracted text misses its visible title, which is why rendered pixels were compared too.

This is not a complete PDF-object, invisible-text, annotation, form, embedded-content or native-version forensic examination. Equality at 120 dpi cannot certify equality of every feature or higher-resolution representation. The conclusion is confined to these acquired entities, this extractor/renderer/version/resolution and the exact page-order comparisons. A different historical copy or native file could change the assessment. All four differing original byte streams and metadata remain preserved without reconciliation.

## What this changes and what it leaves open

The available four placements have now been acquired and tested, so they should no longer be described as three unexamined downloadable counterparts in a current status account. They have **not supplied a demonstrated visible/textual revision of the account**, or independent corroboration of its truth. This is relevant contrary evidence to treating different hashes or catalog placements alone as proof of changed substantive wording.

The specific gaps in the preceding interview review remain: actual earlier alert bulletins; time-stamping/recall instructions; native book/file histories; distribution and recipient/backup copies; actual collection/disposal and applicable authority; the exact book exhibited in each interview; both September 30 and November 10, 2004 recordings, their defect/coverage/custody records and notes; and early briefing CD-ROM/receipt records. The reported intention to collect/destroy outdated information remains an attributed statement with uncertain implementation. These matching contemporary archive representations do not establish that all earlier versions survived or that any particular original was destroyed.

The **actual corrected May 2003 QFR and delivery acknowledgment, signed action/no-action and reasons, recommendation implementation/disposition, and case-specific policy/routing remain TODOs**. This comparison does not acquire them or convert investigation closure into proof of their completion. Telephone, steel, recorder and materials original-input requirements remain open, with technical work owned by the existing technical chat. All five tracks and 18 deferred requirements are preserved.

## Reproduction, preservation and limits

[REPRODUCE.md](REPRODUCE.md) gives the executed method and commands; [METHOD-AND-CHECKS.json](METHOD-AND-CHECKS.json) records runtime, actual acquisition/comparison scope, warnings, checklist and protected predecessors. [OPEN-TODOS.json](OPEN-TODOS.json) records BVC-T03's partial advance and remaining discriminating inputs. [TEXT-CHANGES.diff](TEXT-CHANGES.diff) contains exact additions of these research notes, not an alleged historical version diff. Source acquisition, computation, historical inference and publication are separate milestones.

Public notes exclude original PDFs/rasters/full text extractions, signatures, personal/contact/account data, private case correspondence and strategy. No source was overwritten, deduplicated or deleted. No outreach, fee, new request/filing, mailbox access, private push, merge or public-history rewrite is performed by this study. A separate two-query telephone original-report locator check obtained no new source and is not counted as a published finding or evidence of absence. The substantive goal remains active.
