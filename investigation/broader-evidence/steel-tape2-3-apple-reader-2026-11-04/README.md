> **Consolidation note:** This is a historical public-branch review, not a newly run decode. Five `RAW-LOCAL` logs and the source movie are not included in this package. The logs were already present on the public source branch at commit `cb8bc2395431a924e8a1eeb740c544eea8ad2aed`. Source counts here describe an AVFoundation storage-format read; the requested independent decode failed. Historical summaries and hashes are preserved, and their log references do not imply the logs are bundled. See [consolidation provenance](CONSOLIDATION.json).

# Apple storage-format reader: 11,606 samples; independent source decode still unavailable

November 4, 2026. A separate Apple AVFoundation implementation completed a storage-format read of the unchanged WTC Tape 2-3 movie. It returned **11,610 buffers containing11,606 media samples**, including **four zero-sample buffers**. The requested ARGB decode failed with **AVFoundationErrorDomain -11833**, whose reported reason was: “The decoder required for this media cannot be found.” There is **no completed independent decoded-frame count** from this attempt.

The original native tables still declare **11,607** positive-sized samples; earlier FFprobe reported11,607 while reading11,606packets and11,606frames. These values and the failed12planned/11emitted extraction are preserved unchanged. Agreement between two storage-reader counts does not select a preferred quantity or establish the file's authoring history, camera completeness, the exact selection mechanism or intent.

## Input, implementation and actual test boundaries

The [publicly linked movie](https://drive.google.com/file/d/1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw/view) is815,698,448bytes, SHA-256 `4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb`. Full hashes before and after both source attempts matched; source size/modification time also remained unchanged. The movie stayed in the verified Intel media store. No new historical-media download, source write, local movie copy, audio request/listening, pixel inspection or frame/audio/video export occurred.

The executed [AppleReader.swift](AppleReader.swift) was compiled with installed Apple Swift6.4, language mode5, and AVFoundation/CoreMedia/CoreVideo. The binary's direct linkage lists Apple/system frameworks, without libavformat/libavcodec. The source reader did not invoke FFmpeg. This is a separate framework/software path, not a source audit of Apple's closed implementation and not an independent historical evidence source. Every historical read in this comparison uses the **same movie bytes**.

The installed toolchain, framework linkage, code hashes, settings, three actual controls and34log-consistency/comparison checks are in [VERIFICATION.json](VERIFICATION.json). Four compiler deprecation warnings were retained locally; compilation exited0 and the controls actually ran. No software was installed. Metadata arrays retain exact timestamp values, timescales, flags and epochs; invalid or non-finite time representations are not rewritten as zero elapsed seconds.

Apple's [initializer definition](https://developer.apple.com/documentation/AVFoundation/AVAssetReaderTrackOutput/init(track:outputSettings:)) specifies storage-format samples when settings are nil. Its general class description separately says output is uncompressed; both passages are pinned without rewriting either. The installed output-header comments explicitly describe nil settings skipping decoding and returning decode-order buffers. The raw observed formats and image-buffer presence below are recorded independently of those descriptions. [Track-output class](https://developer.apple.com/documentation/avfoundation/avassetreadertrackoutput), [asset-reader class](https://developer.apple.com/documentation/avfoundation/avassetreader).

## Controls and source results kept separate

| Input and requested setting | Terminal observation | Samples / buffers / image buffers |
| --- | --- | --- |
| Generated three-frame H.264, nil settings | Completed | **3 / 7 / 0**; four zero-sample buffers |
| Same three-frame H.264, requested32ARGB | Completed | **3 / 3 / 3** |
| Deliberately invalid22-byte fixture, nil | Rejected during track loading, error-11829 | No completed count |
| Historical Cinepak source, nil | Completed; formats`cvid` for positive samples and`none` for zero-sample buffers | **11606 / 11610 / 0**; four zero-sample buffers |
| Historical Cinepak source, requested32ARGB | Failed, startReading returnedfalse; error-11833 | **No completed decoded count**; raw partial counters are0 |

The positive fixture contains exactly three procedural frames, has a retained source hash and a separate FFprobe3/3/3verification. FFmpeg was used only to construct/check that control, not to count/decode the historical source in this unit. [FIXTURE-PROTOCOL.md](FIXTURE-PROTOCOL.md) gives the generator/settings and exact fixture hashes. The H.264 control does **not** establish Cinepak decoder availability. Its purpose is to test the counter and requested-image path with a known input.

A process exit0 means the program saved a result. Source ARGB mode still has `counts_complete:false`, `reader_status:failed` and `start_reading_return:false`; its raw0partial counters are not reported as a successful finding of zero historical frames. Apple's [decoderNotFound definition](https://developer.apple.com/documentation/avfoundation/averror-swift.struct/code/decodernotfound) and installed AVError.h line67identify-11833. This records the limitation of the tested installed path, not corruption, substitution or an absence of frames in the movie. Other pixel formats, backends and a compatible independent Cinepak decoder were not tested or installed.

## Complete metadata logs and precise locators

The five program-output JSON files are historical logs, not decoded media, and are not included in this package. Their full hashes and reader versions are in [SOURCE-PINS.json](SOURCE-PINS.json); the filenames below identify those omitted records.

- `source-nil-RAW-LOCAL.json` (raw log not included in this package): `buffer_count`, `sample_count_sum`, `zero_sample_buffer_count`, `observed_buffer_formats`, `sample_rows`, `reader_status`.
- `source-argb-RAW-LOCAL.json` (raw log not included in this package): `start_reading_return`, `counts_complete`, `reader_error.domain/code/failure_reason`, empty `sample_rows`.
- `positive-nil-RAW-LOCAL.json` (raw log not included in this package), `positive-argb-RAW-LOCAL.json` (raw log not included in this package), `negative-nil-RAW-LOCAL.json` (raw log not included in this package): actual control outputs.

Each `sample_rows` entry has the saved schema: buffer index, sample count, PTS, DTS, duration, total sample size, format, image-buffer presence, DoNotDisplay attachment ornull. Each raw time is `[value,timescale,flags,epoch]`. In source nil mode, buffer0 and11607–11609have zero samples and zero sample bytes; their format is`none`. The final such buffer carries PTS`[464704,600,1,0]`. Two intermediate zero-sample buffers have invalid raw-time representations; those are retained, not converted to timestamp0.

The installed SDK describes marker-only buffers in nil-setting configurations and directs callers to check reader status at end/error. The known three-frame control also emitted four zero-sample buffers. Therefore the extra buffers are not unique to the historical file; a buffer total is not automatically a media-sample or decoded-frame total. CMSampleBufferGetNumSamples can also return0on error, so zero alone is not a universal interpretation rule. Here the storage reads completed, the zero-sample buffers had zero data bytes/no format, and the control supplied the same zero-buffer count. These observations and the general API caveat are retained together.

## Ordered numerical correspondence, not payload-byte authentication

The executed [analyze_reader_results.py](analyze_reader_results.py) checked every returned row and compared positive-sample metadata with the previous complete native address map. Its34checks passed; these are log/arithmetic checks, not34independent experiments. [COUNTS-AND-TIMES.json](COUNTS-AND-TIMES.json) retains every check, summary and first/last/zero-sample row.

All11,606positive buffers have one sample, a `cvid` format, PTS`200*j/2997` for ordered indexj=0…11605, duration`200/2997`, and sizes matching that ordered prefix of the11,607-entry native map. This is a numeric row correspondence under the stated index/timing relationship. Compressed payloads were not hashed or compared for byte identity. Equal sizes and matching timing are not a cryptographic sample-to-file join.

The last positive buffer is **buffer index11606**, with PTS/DTS`[2321000,2997,1,0]`, duration`[200,2997,1,0]`, sample size**57988**, and no image buffer. The previously mapped native sample index11606has nominal time2321200–2321400; no positive buffer with that PTS occurs in this completed Apple read. That is a retained output observation, not a finding that the corresponding in-file byte range is missing or invalid.

The last returned packet-duration field reaches nominal media time**2321200**, while the native edit endpoint from the preceding arithmetic is **2321196.48**. The difference is exactly**88/25media units**, or**88/74925seconds**. The final zero-sample marker instead carries the movie/edit endpoint**464704/600seconds**. The packet duration, end marker, native movie/media durations and prior FFprobe duration774.506507remain separate. Actual pixel presentation/clipping and its cause have not been tested.

## Preserved comparisons and remaining requirements

| Measurement layer | Preserved value |
| --- | --- |
| Native size/timing declarations | **11607**; all size entries positive |
| Native address map | **11607** ranges within mdat; no overlaps/out-of-file ranges observed |
| Native edit-interval arithmetic | **11605full +1partial +1outside** nominal intervals |
| Prior FFprobe7.1.1 | **11607reported /11606packets /11606decoded frames** |
| New Apple nil-setting read | **11606samples /11610buffers /4zero-sample buffers**, completed |
| New Apple ARGB source decode | **Failed-11833; no completed independent decoded count** |
| Prior image-selection acceptance | **12planned /11emitted; FAILED**, unchanged |

The numerical agreement of the two storage-reading paths makes the11,606readout independently reproducible at that specific layer. It does not establish an independent11,606decoded-image count: only the old FFmpeg-family decoded count is complete. Neither the reader result nor native edit arithmetic decides which quantity should be used for a different measurement purpose, why the file was authored this way, or whether it is a complete camera original. No conclusion of deceptive alteration, suppression, conspiracy or intent is supported by this unit.

**T23-01 remains PARTIAL.** Independent Apple storage-format reading was completed. Independent source decoding was attempted and failed with the decoder-not-found result; a successful compatible independent Cinepak decode/presentation test remains missing. Actual export/configuration/authoring records, implementation-policy tracing, and any needed payload-hash correspondence remain TODOs. T23-02–04camera/filming/identifier/intake/coupon/transfer/disposition/source-piece joins and CONS-POL-02–07museum implementation/version records remain unacquired. All eighteen original FAA/telephone/recorder/materials/steel criteria remain open or partial.

The [preceding address/edit report](https://github.com/AveLyra/911-conspiracy-investigation/blob/d50585c09361adb918b7b330d4ae29cf99c19362/investigation/broader-evidence/steel-tape2-3-edit-chunk-review-2026-11-04/README.md) and every earlier source/counter/failure are unchanged. [REVISION.diff](REVISION.diff) records the historical source-branch addition against the preceding preserved combined review; it does not include this derivative’s consolidation note or link changes. Source research and public copies remain separate. No raw historical/control movie, pixels/audio, SDK/document bodies, binary/module cache, personal/private/case/correspondence/reference paths or credentials are published. No outreach, fee, newrequest, filing, installation, deletion, source overwrite, private push or history rewrite was performed.
