# Two NARA scans of a New York retention email

## Sources and scope

On 2026-11-16 we examined page 1 of the [ZNY-417 scan](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-ZNY-417-Email.pdf), catalog [7604062](https://catalog.archives.gov/id/7604062), and compared it with page 1 of the previously acquired [ZNY-408 scan](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/e-Other/5-ZNY-408-Email.pdf), catalog [7604059](https://catalog.archives.gov/id/7604059). The [finding aid](https://www.archives.gov/research/foia/faa-finding-aid-72-83) lists them separately. ZNY-417 is 27,261 bytes, SHA-256 `d20860f90908c5927d30ec5c32c8f7426cd72301fae44ad09ef89174cc4adb71`. ZNY-408 is 27,799 bytes, SHA-256 `dae440053aaa85f356f5a2a4ed4a95349141eb10eb22b5fecaa120db19496cc2`.

## Observations

Both visible pages reproduce a September 16 forward of a September 14 record-retention message. Both specify the UTC interval `110000 UTC to 120400 UTC` and show local examples for September 10 and 11. Both direct retention until further notice and retention in case of doubt. Visual side-by-side review shows the same message and layout; these are not independent corroborating accounts of the instruction. This is a comparison of the displayed content, not proof that the two PDFs originated from the same physical sheet or digital scan.

The PDF bytes differ, and MuPDF renders at a 1× matrix produced different RGB sample hashes: ZNY-408 `ae9775339a83fe570c1dc955c0cd6d063a390155301a237414e5217f36932d6b`; ZNY-417 `9076a46aefed3b20f4a6fcf9e626826ef69e0933b298a8347351123e41de8705`. Extracted text hashes also differ. PDF metadata reports creation dates `D:20050610040845-04'00'` and `D:20050610040536-04'00'`, respectively. Those are recorded metadata values, not independently authenticated dates. The differences are preserved; their cause is untested. No evidence here establishes manipulation or a change in the substantive instruction.

## Limits and outstanding work

The previous [finding-aid note](https://github.com/AveLyra/911-conspiracy-investigation/blob/fad8d0684ab79b519a5a0e612e87d26a88eb8768/investigation/broader-evidence/faa-zny-retention-finding-aid-2026-11-16/README.md) examined descriptions rather than the underlying emails. ZNY-408 had already been acquired in an [earlier review](https://github.com/AveLyra/911-conspiracy-investigation/blob/91ffe18d1c4b8f651258d30d5335fa7b8d7e50f1/investigation/broader-evidence/faa-zny-accident-file-routing-2026-11-05/README.md); a [separate correction](https://github.com/AveLyra/911-conspiracy-investigation/pull/13) preserves that history. ZNY-417 is now acquired and examined for this comparison. The original September 14 message and its full distribution, read/delivery evidence, implementation, hold release and disposition remain TODOs. ZNY-423 and ZNY-426 require checking against existing work before any claim that they are missing.

## Verification and revision

Single-page PDF metadata, document SHA-256, MuPDF extracted text, and 1× RGB raster hashes checked locally; visual comparison covered the full pages. The source text is not a chain-of-custody authentication. This is an additive file, and its Git addition is the diff against an absent predecessor. No earlier source or report was overwritten.
