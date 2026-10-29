# Court archive contains separate encoded sound resources; two telephone candidates decoded locally

The held court archive contains sound resources outside the four flight-diagram files previously used for telephone-summary text. A passive inspection found MP3-format event resources in **Lyles.swf, Ong.swf, Atta.swf and Jarrah.swf**. Two exact event resources from the first two files can be extracted and decoded locally. This advances the recording-artifact route under **AUD016-A1 / TC05-B105 / TC06-B110 and TEL02**. It does not authenticate speakers, calls, device/service, native recording provenance or carrier/operator fields.

## Source and actual scope

The [court's P200054 page](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200054.html) links the [original distributed ZIP](https://coop.vaed.uscourts.gov/moussaoui/flights.zip). It describes a Flight77 summary that also includes the other three flights. The unchanged held ZIP is **28,304,524 bytes**, SHA-256 **3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801**, acquired October27,2026 at13:40:38.310051UTC. It contains12SWFs and two launchers. Those are not14 independent source records.

Eight specified SWFs were recursively traversed, including nested sprites. Four other SWFs and the launchers were inventoried only. Nothing executable was run. Earlier work decoded selected static text; this unit adds resource classification and two local audio-format decodes. The [earlier briefing review](https://github.com/AveLyra/911-conspiracy-investigation/blob/681797a20a39d8c30e367c2220be15a191e3a409/investigation/broader-evidence/telephone-may13-briefings-2026-10-29/README.md) and all earlier originals/conflicting values remain unchanged.

| SWF member | DefineSound event resources | Streaming blocks | Result scope |
|---|---:|---:|---|
| AA11.swf |0|0|No inspected standard sound/import/video/binary tags|
| AA77.swf |0|0|Same bounded result|
| UA175.swf |0|0|Same bounded result|
| UA93.swf |0|0|Same bounded result|
| Lyles.swf |2|541|Root event1 selected for local decode|
| Ong.swf |2|2894|Root event1 selected for local decode|
| Atta.swf |3|579|Resource/header census only; no decoding/listening|
| Jarrah.swf |5|431|Resource/header census only; no decoding/listening|

This is **12 event definitions, not12 calls**. A small3,137-byte sound-data payload has the same SHA-256 in all four ancillary files: **ad509a1a6288c0aab21e9d2d220ebc8203a4de99e3232e25cd19d313136c1984**. Their resource IDs and containing bodies differ. Without listening or playback-state analysis its role is unassigned; count neither four independent recordings nor four corroborating events from this repeated resource. Streaming blocks also need not be distinct recordings or nonempty audio frames. The zero counts in the diagrams do not exclude external/script-loaded audio or sound elsewhere in the archive.

## Exact two-resource extraction and test

Both selected DefineSound tags begin at **uncompressed SWF byte26**, root container, soundID1. Their MP3 frame sequences start at byte41 after the tag header, sound fields and separate signed16bit SeekSamples value. Ranges below are zero-based, half-open, in the decompressed SWF, not byte positions in the ZIP or compressed SWF.

| Field | Lyles.swf event1 | Ong.swf event1 |
|---|---:|---:|
| MP3 frame byte range |[41,540776)|[41,492897)|
| MP3 bytes |540735|492856|
| Decoder sample rate/channels |44100Hz / mono|11025Hz / mono|
| SWF declared sample count |1987200|2726784|
| Signed SeekSamples field |0|1669|
| Standalone decoded sample count |1987200|2729664|
| Decoded minus declared count |0|2880|
| Declared count divided by probed rate |45.061224490s|247.327346939s|
| Decoded count divided by probed rate |45.061224490s|247.588571429s|

The **Ong resource's declared count, standalone decoded count and playback offset are different quantities, all preserved here**. The difference2880samples is about0.261224490seconds at11025Hz. The1669 offset is separately about0.151383220seconds; it is not silently subtracted or treated as explaining the difference. The standalone decoder did not receive SWF playback instructions. Encoder latency/padding, publication/authoring sample accounting, or other format behavior are untested possibilities; no preferred explanation or discrepancy resolution is adopted. These results do not establish an edit, deletion, fabricated call, precise conversational length or a historical clock offset.

Exact extracted MP3 SHA-256 values:

- Lyles: **53d4d3256cf941cb2ad659e4bfdaed341e440d4dfa1484a3c84b2e07210e197e**.
- Ong: **b1340270d0e8f4b159bb4b057ea57ec227cd021fb12dc5fd37a46b7e3e9b78b5**.

FFmpeg/ffprobe7.1.1 locally decoded original-rate/channel signed16bit PCM. PCM byte-derived sample counts agreed with summed probed-frame samples. FFmpeg and ffprobe share a library family: this is **not independent decoder validation**. Bitrate-duration warnings occurred; these figures use exact emitted PCM counts, not bitrate duration estimates. No trimming, resampling, normalization or source overwrite occurred. Raw MP3 derivatives remain on guarded local media; PCM was hashed in memory only. No audio was listened to, transcribed, uploaded or published, and no claim is made about its audible contents.

## Method controls and limits

Member hashes, declared/decompressed length limits, tag/container bounds, terminalEnd positions and nested-sprite traversal were checked. Exact tag tuples also agreed with the earlier local parser. A known event-tag fixture and three malformed-container cases checked identification/rejection. A portable reproduction used a separate arithmetic RECT-header offset calculation and reproduced all eight member hashes/counts plus the two PCM hashes/counts. This reuses traversal logic and the same codec implementation; agreement is not a second independent source or universal parser certification.

Tag/field interpretation follows the [Adobe2012SWF19 specification, mirrored copy](https://open-flash.github.io/mirrors/swf-spec-19.pdf): printed177–180/188 for coding/event/latency fields;181–184 for streams;235–237 for numeric tag index. The originalAdobe endpoint returned404. Mirror identity, bytes and hash are recorded; no claim that it is the exact historical authoring version. Only relevant passages were read, not all243pages. The code treats sound-definition counts and playback controls separately.

The critical adverse limit is provenance: **a court presentation may contain prepared excerpts or other derivatives**. Recovering valid encoded bytes does not establish an unedited recipient/carrier master, voice identity, service type or linkage to a particular switch row. File names and trial-page labeling alone cannot make those joins. Radio-named files remain out of this chat's substantive recorder interpretation.

## TODOs and continuation

TEL01–TEL04 and the inherited conflicting carrier/briefing/usage values remain open in [OPEN-TODOS.json](OPEN-TODOS.json). Native engineering dictionaries, switch/operator/transfer records, actual Keyton/usage originals and source-to-call worksheets were not recovered. Four targeted engineer searches and a museum-route inspection did not produce those originals; their non-acquisition is not evidence of destruction, withholding or wrongdoing. No failed route was retold as a new suspicious finding.

The next feasible test is **passive mapping of the selected sound IDs to SoundInfo/button/timeline controls**, frozen before execution, to distinguish defined resources from actual played intervals. Independent native source-recording and exhibit-preparation/custody records are needed for any stronger authenticity or excerpt claim. Museum recipient-supplied audio remains a separate accession/transfer lead, not an acquired original. All five work-plan tracks and18original-input requirements remain; this bounded resource/test advance does not complete them.

Source hashes/locators: [SOURCES.json](SOURCES.json), [RESOURCE-COUNTS.json](RESOURCE-COUNTS.json), [DECODE-RESULTS.json](DECODE-RESULTS.json). Method: [reproduce_resources.py](reproduce_resources.py), [REPRODUCE.md](REPRODUCE.md). Actual scope/checklist: [REVIEW-AND-CHECKS.json](REVIEW-AND-CHECKS.json). The exact additive note/code diff is [TEXT-CHANGES.diff](TEXT-CHANGES.diff); predecessor reports remain frozen. Raw archive/audio/PDF/images, private correspondence, personal/contact/account fields, case strategy and credentials are excluded from the public payload. No outreach, fee, request/filing, private push, deletion, merge, history rewrite or historical conspiracy finding is made.
