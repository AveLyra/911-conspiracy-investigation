# A second collected-steel movie: readable marking and unequal frame counters

November 3, 2026. The previously unexamined public **WTC Tape 2-3.mov** supplies two useful leads: a visible **N10-C3B** marking and a reproducible difference between a reported frame count and the counts emitted by the selected demux/decode pass. The earlier Tape 3 records and uncertainties remain unchanged. These observations identify records and reproduction questions; they do not establish a building origin, later custody, missing camera footage or deliberate editing.

## Source acquired and preserved

[NIST’s archive entry](https://www.nist.gov/world-trade-center-investigation/photos-videos-and-simulations) led to its [Collected Steel repository](https://googledrive.nist.gov/folders/1mO5PPh1ZyZafGUtWrzqhiaDwzTqyEPG-) and [Video folder](https://drive.google.com/drive/folders/1vSfhviqoDXiIeObJqyPlbuqrfWdwTAUY). The preserved seven-item listing identifies [WTC Tape 2-3.mov](https://drive.google.com/file/d/1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw/view), ID **1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw**. Current metadata retained the same name and size. We selected it as the next-smallest unexamined file, not because its name proved a chronological sequence or independent source.

The complete anonymous download is **815,698,448 bytes**, SHA-256 **`4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb`**, MD5 **`be6770700b7f33e3dd5f07400a809f87`**. Saved bytes were read back and matched the download hash. Retrieval began **2026-11-03T21:34:12.967803+00:00** and finished **2026-11-03T21:36:14.477082+00:00**. This identifies the current public archive entity; it does not authenticate an original camera tape, original filming date or specimen custody. [Source pins](SOURCE-PINS.json).

The Drive tool rejected the file at its 256 MiB transfer limit. An ordinary anonymous download through the actual public large-file warning form succeeded. A local check first overlooked the submit button’s label stored in an input value; that failed attempt was retained and the saved form used without a second initial-page request. There was no sign-in or access-denial bypass. These are acquisition/tool events, not historical evidence of withholding.

## T23-C01 — Reported count versus read packets and frames

| Measurement of this same video stream | Observed value | Scope |
| --- | --- | --- |
| FFprobe metadata field `nb_frames` | **11,607** | Reported field; no independent native sample-table interpretation performed. |
| `nb_read_packets` with `-count_packets` | **11,606** | Packets emitted by this selected FFprobe demux path. |
| `nb_read_frames` with `-count_frames` | **11,606** | Frames emitted by this selected decoder pass. |
| Planned uniformly spaced native images | **12** | Selection used the reported count to propose zero-based endpoint 11606. |
| Images actually emitted by that selection | **11** | Last requested index 11606 did not produce an image in that run. |

The separate count command completed with **exit 0 and empty warning output**, using FFprobe **7.1.1**. Its installed command help was checked for the counting options. The image-producing FFmpeg child completed with exit 0, but the Python checker then failed its expected-12 versus actual-11 assertion. **That original sample-acceptance check remains failed.** The actual eleven images were retained; no substitute endpoint, changed expected value or invented twelfth image was used. [Exact values and commands](COUNTS.json) · [frame manifest](FRAME-MANIFEST.json).

The counting pass, source hash and failed endpoint test make the difference reproducible for this entity and software configuration. They do not identify its cause. Container/table accounting, edit-list treatment, empty or omitted samples, and demux/decoder behavior are untested possibilities. No native tables or alternate edit/decoder policies were tested here, and no preferred counter or explanation is selected. A difference between these layers is not, by itself, proof of corruption, a lost original frame, a cut, fabrication or an elapsed gap in the filmed events. The original camera/tape, export history, native sample/edit tables and an independent reproduction are needed to distinguish those possibilities.

The [earlier Tape 3 study](https://github.com/AveLyra/911-conspiracy-investigation/blob/75347e9c38e09b5c2037ee9490e6c2c5acf0f799/investigation/broader-evidence/steel-candidate-originals-2026-10-27/README.md) reported **6,399 stored/reported and decoded entries** for that different file. That earlier result remains unchanged and was not recounted. It neither authenticates Tape 2-3 nor makes the two files independent corroboration.

## T23-O01–O03 — Field markings and collection context

All indices are zero-based decoder-input indices; times are reported presentation locators, not a filming date or historical clock.

| Observation | Actual full-frame locator | Reading and limitation |
| --- | --- | --- |
| T23-O01 | **8440 / 563.229897 seconds**, frame-09 | Upper line **N10-C3B** is readable on visible structural material. The lower line remains **B-1/8-1 uncertain**. A diagonal line and cross-shaped mark are visible. No inventory, construction-origin or custody join accepted. |
| T23-O02 | **2110 / 140.807474 seconds**, frame-03 | An **M4-like prefix** and an incompletely accepted suffix; lower **S-1/5-1-like** line. Full identifier remains unaccepted. The original partial transcription is retained in OBSERVATIONS.json. |
| T23-O03 | Frames 01,04,07,08,10,11; exact indices/PTS in manifest | Structural members/plates on pavement and racks outdoors, with visible open surfaces, deformation and white markings. No active cutting, measuring, transport, preservation instruction or later disposition established from these sampled stills. |

The readings were recorded before the limited held-text check. A subsequent exact search for N10/C3B in the two held NCSTAR 1-3B page-text derivatives, physical pages 87 and 94, returned no match. That two-page searchable-layer result is not a complete inventory search or proof the identifier is absent. The earlier failed PDF route was not retried. No source label or desired match was used to complete an unreadable character. [Observations](OBSERVATIONS.json).

The new readable string is a specific target for marking photographs, intake/alias records, retained-piece/coupon crosswalks and source filming logs. It is not an authenticated final catalog number or WTC 7 attribution. Nearby surfaces and labels are not assumed to belong to one specimen. Sparse sampled views do not establish or exclude overlap with Tape 3; file counts and repeated views are not independent witness or specimen counts. The strongest objection to a lost-evidence inference is the absent specimen/instruction/transfer/disposition join. A visible stored member also cannot establish adequate preservation or representative scientific sampling.

## Actual reading, method and limits

Metadata describes a **640×480 Cinepak (`cvid`), RGB24** video, reported rate **2997/200** fps, video duration **774.506507 seconds**, and format duration **774.506667 seconds**. These are separate reported quantities, retained without correction. The format creation tag reads **2010-06-11T17:49:08Z**, the video tag **2010-06-11T17:49:09Z**, and Drive metadata creation/modification **2019-11-26T06:38:59.078Z**. These object fields do not authenticate filming or measure audio/video synchronization. Audio metadata is retained separately; audio content was not listened to or transcribed. [Metadata](METADATA.json).

Before content reading, twelve indices were frozen by `floor(k*(11607-1)/11)` for k=0…11: **0,1055,2110,3165,4220,5275,6330,7385,8440,9495,10550,11606**. Only the first eleven produced PNGs. All eleven actual raster hashes and native dimensions were verified. **Eight** were individually viewed: frames **01,03,04,07,08,09,10,11**. One labeled, reduced navigation overview was viewed; its final unused slot says no output and is not a source blank image. Its thumbnails are not full-detail readings of frames02/05/06. No additional interval or full-frame view was used. [Reading scope](READING-SCOPE.json).

The one full count pass was prospectively added after the concrete endpoint mismatch; it was not an unchanged count rerun. FFmpeg and FFprobe share a library family, so their agreement is not independent decoder validation. No continuous scene census, voice/person identification, AI enhancement, interpolated frame, calibrated physical dimension, camera-clock authentication, material test, building attribution, historical-cause or intent inference was performed. Source size and modification time remained unchanged through extraction and counting; hashes prove entity identity, not historical conclusions. [Verification and failed checks](VERIFICATION.json).

## TODOs and preservation

**T23-01:** native sample/duration/edit tables, applicable export/software configuration and independent count reproduction. **T23-02:** original camera/tape and export/source lineage. **T23-03:** actual N10-C3B and uncertain-marking photographs/intake/alias/geometry/coupon/transfer/disposition records. **T23-04:** a source-supported scene/cross-file overlap map if needed. Each remains unperformed; no missing original is silently supplied by the current download. [Acceptance and carried-forward records](OPEN-TODOS.json).

All earlier FAA, telephone, recorder, materials and steel original-input requirements remain open or partial. The [preceding SAVE review](https://github.com/AveLyra/911-conspiracy-investigation/blob/71b47a3713297a336e56109e9cea805a8547fa3e/investigation/broader-evidence/steel-save-marking-followup-2026-11-03/README.md), its M/N/M2 readings and all underlying source bytes remain unchanged. The new [REVISION.diff](REVISION.diff) appends this report to the immediately preceding preserved combined version, with no removed historical text. [Request checklist](CHECKLIST.md).

Only minimized original notes, links, hashes, metadata, locators and limitations are published. The movie, audio, frame images, contact sheet, raw warning/documents, personal/contact fields, private case material, correspondence, litigation strategy, credentials and coordination records are excluded. There was no outreach, new request, fee, filing, physical test, private push, deletion, source overwrite or history rewrite. Acquisition, measurement, historical authentication and publication remain separate states.
