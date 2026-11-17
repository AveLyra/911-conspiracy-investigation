# Court P200055 exhibit bundle: source pin and contents

November 16, 2026 · TEL02–TEL04 / AUD016-A1. The federal court's publicly linked exhibit bundle was acquired and checked as a source for later comparison of the Flight 93 telephone summaries. This is acquisition and archive-integrity progress; the call presentation has not yet been displayed or decoded in this unit.

## Official source and integrity

The [court's P200055 entry](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200055.html) identifies a prosecution summary concerning Flight 93 and links a [Flash presentation ZIP](https://coop.vaed.uscourts.gov/moussaoui/flights.zip), noting that it also contains information on other flights. A direct download on November 16, 2026 produced **28,304,524 bytes**, SHA-256 `3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801`. `unzip -t` reported no compressed-data errors for **14 members**. This verifies archive readability, not authorship, evidence completeness or historical accuracy. The original ZIP is preserved locally on the verified media store and is not republished here.

The archive includes two differently named Flight 93 files. Their uncompressed bytes were read from the ZIP without running the files:

| Member name | Uncompressed bytes | SHA-256 |
| --- | ---: | --- |
| `UA93.swf` | 3,464,811 | `f104ab54492e05550c9e776894e0dbb0d9238039a8f2e9c40be41b1a122d7675` |
| `UA 93 Calls.swf` | 3,464,520 | `9b6703c286cc4e5be8de36728c10bc0fc60dc54e4b732898ba4d4fbfda2fec5e` |

Both begin with an `FWS` signature. Different member names, byte sizes and hashes are preserved. Their visual contents, relationship and any relevance to a specific entry have not been tested. The bundle also includes executable launcher files; none was executed. Do not treat the archive as the original carrier spreadsheet, recordings, source worksheet or complete prosecution production.

## Next discriminating test

The [prior source comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/2b5dc2a71fda41aee52b9e1f1a5bc7eb5bcd1fba/investigation/broader-evidence/telephone-grandcolas-short-attempts-2026-11-16/README.md) preserves the NPS **2, 3, 2 seconds** and May 2004 briefing **2, 3, 3 seconds** sequences, with their row association unresolved. **TODO:** inspect the relevant exhibit entries through a safe, documented, reproducible method; record the actual displayed values and determine whether the source records can be joined. The court exhibit is a summary, and an exhibit reading cannot alone authenticate caller, actual duration or original carrier field. Preserve all prior observations and source dependencies. Native carrier data, the underlying message, field dictionary and custody remain open.

The court entry and ZIP share provenance and are not independent measurements. No content difference, correction, motive, concealment or historical cause is inferred from the two SWF hashes. This report is a newly named additive source pin; existing files and conflicting records remain unchanged.
