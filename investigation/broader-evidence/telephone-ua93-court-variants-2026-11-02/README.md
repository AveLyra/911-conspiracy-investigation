# Two UA93 court assets: equal decoded text, different source bytes

November 2, 2026, America/New_York; execution receipts extend into November 3 UTC. TEL02/TEL04, AUD016-A1, TC05-B105 and TC06-B110. This is a source-version and recording-locator test using an already-held public court archive. It does not recover or authenticate a native telephone recording.

## Why this pair was inspected

The [preceding FBI review](https://github.com/AveLyra/911-conspiracy-investigation/blob/5c2a489db46eb230900d41b05f1710497e636965/investigation/broader-evidence/telephone-recording-custody-relays-2026-11-02/README.md) identifies a reported Gronlund-associated cassette receipt and September 11 handover at the Boston FBI office. Its actual tape/item/receipt/examination/retention chain remains missing. The already-held court prosecution index supplied no literal Gronlund row match; that does not establish what is in the separately distributed presentation archive.

The [court ZIP](https://coop.vaed.uscourts.gov/moussaoui/flights.zip), linked from the [P200054 exhibit page](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200054.html), contains fourteen members. None is Gronlund-named. It contains the following **two different UA93 members**. They occur in the same held archive; no earlier/later chronology is inferred from their names or order.

| Archive member | Original bytes | SHA-256 | Decoded text definitions |
|---|---:|---|---:|
| UA93.swf | 3,464,811 | f104ab54492e05550c9e776894e0dbb0d9238039a8f2e9c40be41b1a122d7675 | 420 |
| UA 93 Calls.swf | 3,464,520 | 9b6703c286cc4e5be8de36728c10bc0fc60dc54e4b732898ba4d4fbfda2fec5e | 420 |

## Actual test result

The two sources differ in bytes and by **291 bytes of file length**. The existing passive reader recovered **420 text definitions / 379 distinct decoded strings** from each. The **exact multiset of decoded codepoint strings matches**, including every repeated occurrence, NUL and other codepoint. No whitespace, case or source-value normalization was used to obtain that result. The shared multiset digest is `9a4da7dc704250b0cb7d2649a8b47586653bdbe16bfce3ce3a50eb9c1419dede`.

This establishes equality only in that decoded representation. It does **not** establish equal font shapes, geometry, color, layering, buttons, actions, visited screens, execution order, actual trial display or historical accuracy. The definition IDs and offsets differ. A field location valid in one member cannot be applied blindly to the other. The exact source bytes remain separate and unchanged; no preferred version or cause of the difference is selected.

Both have SWF-version-5 headers, a declared 12 frames per second, 176 declared root frames and the same stage rectangle. Those are authoring metadata, not call duration, a carrier clock or proof of runtime behavior. Their complete numeric tag-count dictionaries differ: tag code **28** occurs **1,216** times in UA93.swf and **1,190** times in UA 93 Calls.swf. This test does not interpret those instructions or simulate their effect. Equal counts for other tag types would not establish equal tag bodies.

### Gronlund is a stored term, not an authenticated tape

The decoded definitions contain Gronlund, Glick and Beamer terms in both members. For example, a Gronlund-matching definition appears at **UA93.swf: character ID 679, uncompressed tag offset 282713**, and its raw decoded-string hash matches **UA 93 Calls.swf: ID 1754, offset 3415889**. Other Gronlund-associated definitions occupy different IDs/offsets too. [RESULTS.json](RESULTS.json) preserves selected safe term coordinates and source hashes; it excludes the full text table, recipient/contact/phone fields and compound text contents.

An exact term hit is not independent voice/caller identification, proof that a particular text was displayed, or a unique join between the court data and the Boston cassette. These objects may contain a court summary of information derived from several sources; the source-to-exhibit construction/attribution records remain unacquired. Multiple definitions, duplicate labels or two source variants are not multiple calls or independent corroboration.

### No standard SWF sound tags in these two members

The complete recursive tag traversal found **zero** occurrences of the selected sound-definition/playback/stream tag codes **14, 15, 17, 18, 19, 45 and 89** in either member. Neither inspected object therefore supplies an identified Gronlund recording through those standard sound structures. No sound payload was extracted, decoded or listened to.

This is not a claim that the full archive, other court holdings or the FBI lack the recording. Other members were inventoried but not decoded in this unit. External media, unused/opaque data, script references and runtime behavior were not evaluated. The objects contain actions, which were counted but neither interpreted nor executed. The cassette's historical existence or fate cannot be inferred from this bounded result.

## What actually ran

The unchanged court ZIP was verified at **28,304,524 bytes**, SHA-256 `3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801`. Only **UA93.swf** and **UA 93 Calls.swf** were read and preserved as separately named local derivatives; no executable launcher or Flash/ActionScript ran. Both full passive extractions and tag inventories remain local on the verified Intel store. No new download, external query, OCR, ASR, audio/voice/caller/clock inference or native carrier decoding occurred.

The initial source lookup used a guessed flights.zip filename and failed; the preserved acquisition script identifies the actual court-flights.zip path, which passed the media guard and byte checks. That was our path error, not missing historical evidence. A prior protocol had expressly left the Calls variant uninspected; the bounded reading-history check found no completed comparison of this pair. Completed Lyles/Ong/AA77 tests were not repeated as new findings.

The equality calculation treats raw decoded strings as a multiset, not a set. Fixed comparator controls require a reordered identical input to match and reject changed multiplicity, case changes and removal of a NUL. These controls test the comparison rule; they are not an independent SWF implementation or historical authentication. The same existing font/tag parser underlies both extraction and reproduction, so parser dependence remains a limitation. The court's original authoring project and a verified actual runtime/display are not available in this test.

## Next records, preservation and scope

The most useful inputs remain the actual Boston cassette/evidence receipt and source-to-court-recording construction/copy records. For presentation versions, obtain the authoring projects, exact build/delivery/version manifest, source-to-field mapping and any external media references with their source/custody. The present equality result cannot decide why the bytes, IDs or tag counts differ or whether those differences affect a particular visited screen.

All earlier FBI handling times, source-specific 9:03/9:11 status reports, 9:36/10:45 endpoint accounts, provider/recording assertions and earlier telephone conflicts remain unchanged. No historical discrepancy is resolved, no clock/leg/caller is selected and no inference of fabrication, concealment, motive or attack mechanism follows. A different build/export or assembly is a possible untested explanation, not an adopted one.

All five original work-plan tracks and eighteen full requirements remain open or partial. Existing Keyton/usage/court sources and completed technical-owner work remain recognized. [OPEN-TODOS.md](OPEN-TODOS.md), [source pins](SOURCES.json), [method](METHOD.md), [checklist](CHECKLIST.md), [verification](VERIFICATION.json) and the [actual additive diff](REVISION.diff) distinguish the performed source test from missing originals and unperformed empirical tests. Raw media, full text, contacts, recipient/personnel/signature information, masked identities, private case/correspondence and internal coordination are excluded from the public derivative. No outreach/request/fee/mailbox, deletion, overwrite, private push, merge or history rewrite occurred.
