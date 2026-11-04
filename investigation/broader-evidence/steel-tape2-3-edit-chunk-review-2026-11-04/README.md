# WTC Tape 2-3: native chunk addresses and edit intervals

November4,2026. A second native pass maps **all11,607 declared first-track video samples** into the existing file's media-data region. The metadata-based ranges are positive, ordered, within the file, and do not overlap. The recorded edit has a different extent from the complete nominal media timeline: **11,605 nominal sample intervals fit fully, one intersects partly, and the final interval is outside**. The earlier11,607reported/11,606read-packets/11,606read-frames observations remain preserved. Actual decoder selection and the cause of those different readouts are not adjudicated.

This advances the native-address/edit portion of **T23-01**. It does not authenticate the camera original, establish a historical edit or missing footage, complete an independent decoder test, identify a steel piece's origin, or complete any of the original eighteen work-plan criteria.

## Source, primary definitions and actual scope

The unchanged [public movie](https://drive.google.com/file/d/1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw/view) is815,698,448bytes, SHA-256 `4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb`. A new full-file hash matches the November3 acquisition. Size and modification time were unchanged. Media was read from the verified Intel store, without a new download, source write, local media copy, image/audio generation, listening, decoding or FFprobe rerun.

The [preceding native sample-table report](https://github.com/AveLyra/911-conspiracy-investigation/blob/7ea858bf359684cea350aa3d55d1ed6f609761b8/investigation/broader-evidence/steel-tape2-3-native-tables-2026-11-04/README.md) and its failed12planned/11emitted extraction remain unchanged. This report adds header timescales/durations, both tracks' edit entries, and first-track sample-to-chunk, chunk-offset, description and data-reference fields. Only the first track's sample addresses are mapped. Audio packet layout, audio alignment and compressed payload validity are outside this pass.

Ten public Apple definitions were acquired and read: five initial parent pages, the two explicitly linked edit/chunk tables, and sample-description/data-reference parents plus the linked reference-entry table. [SOURCE-PINS.json](SOURCE-PINS.json) contains each URL, access date, raw-source hash, exact reading lines and field use. The separate index is navigation only. Raw copyrighted definition bodies stay local. One initially guessed `data_reference_atom` route returned404; the correct indexed `media_data_reference_atom` route was acquired separately. The404 is a route result, not a movie discrepancy or evidence of removal.

Apple's [chunk definition](https://developer.apple.com/documentation/quicktime-file-format/chunk_offset_atom) specifies file-relative offsets. The [run table](https://developer.apple.com/documentation/quicktime-file-format/Sample-to-chunk_atom/Sample-to-chunk_table) specifies which consecutive chunks use each samples-per-chunk/description entry. The [edit table](https://developer.apple.com/documentation/quicktime-file-format/Edit_list_atom/Edit_list_table) distinguishes segment duration in movie units from start time in media units. These definitions support the arithmetic below; they do not establish the export history or what a particular decoder presents.

## Native fields and byte locators

Offsets are zero-based bytes. Native chunk, description and reference IDs are one-based; sample indexes in our map are zero-based. [NATIVE-MAPPING.json](NATIVE-MAPPING.json) preserves complete selected table entries and atom extents.

| Native observation | Value | Field byte locator |
| --- | --- | --- |
| Movie `mvhd` timescale/duration | **600 / 464704** | **815620060 / 815620064** |
| First-track `mdhd` timescale/duration | **2997 / 2321400** | **815620380 / 815620384** |
| First-track `elst` entry | **one** entry: duration464704, media start0, rate raw65536 (1.0) | Entry begins **815620340**; start **815620344**; rate **815620348** |
| Second-track `mdhd` timescale/duration | **44100 / 34155797** | **815691861 / 815691865** |
| Second-track `elst` entry | **one** entry: duration464704, media start0, rate raw65536 | Entry begins **815691821** |
| First-track `stsc` run count | **1526** | **815620717**; entries **815620721** |
| First-track `stco` chunk count | **1550** | **815685493**; entries **815685497** |
| Used sample description | ID1, format`cvid`, data-reference index1 | Description **815620595**; reference-index field **815620609** |
| Used data reference | ID1, type`alis`, flags1, self-reference bit set, **zero opaque reference-data bytes** | Entry **815620559**; flags **815620568** |

Version/flags for the selected outer headers/tables are retained, not inferred from filename or an earlier tool. The data-reference bit declares the same file as the movie atom, under Apple's reference definition; its documentation allows different forks on multi-fork systems. Our bounds check applies to the ordinary byte stream actually held. No other fork or external alias target was opened, and no path/name payload is published.

## Address mapping result

The1,526native run entries over1,550chunks account for **11,607 samples**, the same number of stored sizes. There are **zero unmapped size entries and zero excess declared samples**. Every calculated first-track sample range lies within the `mdat` payload, bytes **48 through815620031** inclusive, and within the815,698,448-byte file. No overlapping first-track ranges were observed. This checks metadata addresses and file bounds, not media content validity, frame independence or source completeness.

The complete11,607-row address map is [SAMPLE-MAP-LF.csv](SAMPLE-MAP-LF.csv). Its header is line1; sample index0 is line2, index11605 is line11607 and index11606 is line11608. Each row records sample index, native chunk, absolute offset, declared size, end-exclusive, description ID and bounds flags.

The measured CSV used CRLF delimiters, which the default Git whitespace check rejected. Its **exact original bytes** are preserved reversibly in [SAMPLE-MAP-ORIGINAL-CRLF.base64.txt](SAMPLE-MAP-ORIGINAL-CRLF.base64.txt). The separately named LF table is a readable derivative with identical fields, rows, order and values. [SERIALIZATION.json](SERIALIZATION.json) pins both hashes and the actually passed byte-for-byte reconstruction and field-equality checks. No original source or measured CSV was rewritten, and Git whitespace settings/checks were not relaxed.


| Sample index | Chunk | File start | Size | End-exclusive |
| --- | --- | --- | --- | --- |
| 0 | 1 | **48** | **54508** | **54556** |
| 11605 | 1550 | **815502668** | **57988** | **815560656** |
| 11606 | 1550 | **815560656** | **57988** | **815618644** |

The final two samples have separate metadata address ranges with the same length. Their compressed bytes were not compared for equality and were not decoded. The result is contrary to a specific out-of-file/truncated-address explanation for these declared ranges. It does not establish valid imagery, a camera-original timeline, or an explanation of the earlier counter difference.

## Duration and edit observations kept side by side

| Layer | Preserved value |
| --- | --- |
| Native movie duration | `464704/600 = 58088/75`, about **774.506666667s** |
| Native first-track media duration | `2321400/2997 = 773800/999`, about **774.574574575s** |
| Native first-track timing table | **11607 × 200 = 2321400** media units |
| Native first-track edit | Starts at media0, rate1, lasts **464704 movie units** |
| Prior FFprobe stream duration | **774.506507s** |
| Prior FFprobe counts | **11607 reported / 11606 packets read / 11606 frames read** |
| Prior extraction acceptance | **12 planned / 11 emitted; parent expected-count check FAILED** |

The new media header independently supplies the2997timescale that was only a prior-tool assumption in the preceding conditional calculation. The old report and its conditional comparison are not rewritten. The different native movie/media durations and prior tool duration remain distinct observations. The difference between the two native durations is exactly `1696/24975`, about **0.067907908s**; this is not a measured loss of historical footage.

Using the observed edit fields, rate1 and both native timescales, the edit endpoint is `464704 × 2997 / 600 = 58029912/25 = 2321196.48` media units. The nominal200-unit sample intervals are treated as half-open ranges. Under that arithmetic:

- **11605 intervals**, indexes0–11604, lie fully within the recorded edit range.
- Index**11605**, range2321000–2321200, intersects the endpoint partly.
- Index**11606**, range2321200–2321400, lies outside it.

Thus **11606 nominal intervals intersect** that recorded range while11607are declared and mapped in the file. This is exact interval geometry. We have not traced FFprobe's edit-list implementation, packet filtering, duration conversion, frame emission, codec validity or boundary behavior. The numerical relation does not prove which mechanism produced its readouts, choose a preferred count, explain why the file was authored this way, or authenticate a historical event. The presence of an `elst` atom alone is not evidence of deceptive editing.

The earlier Apple timing page's `stts`/`ctts` wording difference remains preserved. The movie-header parent page's layout omits a reserved row while its later topic lists ten reserved bytes. Only its initial timescale/duration fields were interpreted here, before that unused tail. These reference-document limitations are not movie-alteration evidence.

## Actual verification and remaining work

The executed [edit_chunk_mapping.py](edit_chunk_mapping.py) uses the unchanged [native_tables.py](native_tables.py) from the preceding pass. **31controls passed:14previous controls plus17additional controls.** They include malformed lengths and versions, absolute offsets, signed empty edits, fractional rates, variable chunk sizes, mismatched sample counts, out-of-media ranges, overlaps, reference bounds and interval boundaries. Negative conditions are retained in output instead of replacing counts or silently clamping a discrepancy.

A separate [independent_mapping_check.py](independent_mapping_check.py) used `int.from_bytes`, its own chunk lookup and closed-form arithmetic. It checked every CSV row against fresh metadata reads and reproduced all11,607addresses, bounds, lack of overlaps, native time fields, reference flag and11,605full/onepartial/oneoutside result. [VERIFICATION.json](VERIFICATION.json) records actual outcomes. This is independent reading/arithmetic code, **not an independent decoder**.

For reproduction, first resolve the matching movie through the repository media-store guard and verify its SHA-256. In a directory containing the three published scripts, use new output paths with `python3 -B edit_chunk_mapping.py <guarded-source> <new-results.json> <new-map.csv>`; then `python3 -B independent_mapping_check.py <guarded-source> <new-results.json> <new-map.csv> <new-check.json>`. To check the exact published measurement bytes, first run `python3 -B restore_original_map.py SAMPLE-MAP-ORIGINAL-CRLF.base64.txt <new-original-map.csv>`; use that restored original with the unchanged native result and checker. The readable LF derivative has a distinct serialization hash and is not substituted for the measured CRLF input. Source opens `rb`; outputs are exclusive new files. Neither standalone program replaces the repository guard.

**T23-01 remains PARTIAL:** native size/timing/address/reference/edit reading and these arithmetic checks are complete for this source. Actual export/configuration lineage, decoder-policy tracing and a genuinely independent decode/presentation test remain unperformed. **T23-02–04** camera/tape/filming logs, identifier/intake/geometry/coupon/transfer/disposition and source-supported piece joins remain TODO. Museum **CONS-POL-02–07** implementation/version records and all eighteen original five-track criteria remain open or partial. Missing FAA correction/receipt/signed disposition, telephone originals and recorder/materials inputs are not supplied by this file audit.

Earlier source/report/failure bytes are preserved. This additive original-research bundle contains only notes, code, table metadata and source pins: no movie, extracted image/audio, raw copyrighted definition body, personal/reference-path content, case correspondence or credentials. No outreach, fee, request, filing, private push, merge, deletion, overwrite or history rewrite occurred. No conclusion about conspiracy, attack participation, demolition, misconduct or intent follows from these address and interval observations.
