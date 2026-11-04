# WTC Tape 2-3: native sample tables alongside the earlier counts

November 4, 2026. The restored Intel share allowed a read-only native-table inspection of the unchanged public movie. The first track's sample-size table contains **11,607 entries, all positive**. Its timing table also counts **11,607 samples**. The previously published FFprobe run reported **11,607** but read **11,606 packets and 11,606 frames**. All these observations are retained; their cause is unresolved.

This completes the sample-size/timing-table portion of **T23-01**. Edit-list, chunk mapping, export-lineage and independent-decoder work remains open. No original work-plan criterion is completed by this table inspection.

## Source and actual work

The [publicly linked movie](https://drive.google.com/file/d/1UzY8uR-jH_pmgTzRPok5zgrvB7xfZ4iw/view) is the same 815,698,448-byte file acquired November 3, 2026: SHA-256 `4beeea4b0e66c5fcaf68f5336ea4b76518f89c6d1cfbba6833915e359f8a4bcb`. A new full-file hash matched; size and modification time were unchanged. No new movie download, source write, local media copy, image generation, listening, decoding or FFprobe rerun occurred. The prior [source acquisition and count report](https://github.com/AveLyra/911-conspiracy-investigation/blob/da9fd9dfb7d1af87c88143b0148914439420c4cd/investigation/broader-evidence/steel-tape2-3-source-2026-11-03/README.md) remains unchanged.

A new Python parser read structural atom headers and complete `stsz` and `stts` payloads in both tracks. Other payloads were skipped. It inventories **42 atoms under its explicitly traversed container types**, not every possible embedded atom. First-track raw four-byte markers are `vide` at byte 815620408 and `cvid` at byte 815620599. The earlier FFprobe identified Cinepak video with tag `cvid`; that association is separate from native table reading. Additional handler/codec fields were not interpreted.

Apple describes `stsz` as recording sample counts and sizes, with the default-size case omitting the size array. Apple describes `stts` as sample-count/time-delta runs; their sum precedes overall-timescale and edit-list mapping. The definitions support reading these tables, not a causal explanation of this export. [Sample-size definition](https://developer.apple.com/documentation/quicktime-file-format/sample_size_atom), [timing definition](https://developer.apple.com/documentation/quicktime-file-format/time-to-sample_atom).

## Exact native observations

Offsets and table indexes are zero-based. Full atom paths, extents, flags, versions, runs and first/last size entries are in [NATIVE-TABLES.json](NATIVE-TABLES.json).

| Observation | Preserved value | Exact locator |
| --- | --- | --- |
| First-track `stsz` count | **11,607** | `/moov[1]/trak[1]/mdia[1]/minf[1]/stbl[1]/stsz[1]`; count byte **815639049** |
| Stored sizes | **11,607 positive; zero zero-sized entries** | Same table, array starts **815639053**; `fields.positive_size_count` and `fields.zero_size_count` |
| First and last sample sizes | Index0 **54,508**; index11606 **57,988** bytes | Entry bytes **815639053** and **815685477** |
| Size minimum, maximum, sum | **43,980 / 64,468 / 678,996,796** bytes | Derived from all size-array values |
| First-track `stts` | One run: **11,607 samples × 200 = 2,321,400 media units** | `/moov[1]/trak[1]/mdia[1]/minf[1]/stbl[1]/stts[1]`; entry-count byte **815620693**, run **815620697**, delta **815620701** |
| Deferred edit list | First-track `elst`, 28 bytes; uninterpreted | Atom **815620324**, payload **815620332**, end-exclusive **815620352** |
| Deferred chunk tables | First-track `stsc` / `stco`; uninterpreted | Atoms **815620705** / **815685481** |

The second track has raw markers `soun` and `twos`; its `stsz` default-size field is1 and count34,155,797, while its single `stts` run has count34,155,797 and delta1. These fields are preserved. No audio playback, PCM packet-layout or per-channel byte interpretation, or audiovisual synchronization test occurred. The generic `stsz` product in the result is not verified audio packet bytes.

## Conflicting layers preserved

| Layer | Value | Actual scope |
| --- | --- | --- |
| Prior FFprobe7.1.1 `nb_frames` | **11,607** | Saved tool report |
| Prior `nb_read_packets` | **11,606** | Completed earlier packet count |
| Prior `nb_read_frames` | **11,606** | Completed earlier decoded-frame count, same FFmpeg library family |
| New native `stsz` | **11,607**, all sizes positive | Size table; no decode |
| New native `stts` | **11,607**, delta200 | Timing table; no edit/presentation mapping |
| Prior extraction acceptance | **12 planned / 11 emitted** | Child exited0; parent expected-count check **failed**, still failed |

A zero-sized entry is not observed in this first-track size array. That is a narrow negative result for one proposed check. It does not establish that each declared sample exists at the correct payload address, is valid, is presented, or decodes. The chunk/extent/edit/decoder checks remain unperformed. The final two sizes both equal57,988 bytes; equal lengths alone do not demonstrate equal payloads or duplicated images. Payload equality was not tested.

A timing calculation is conditional: applying the **previously reported**, not newly header-verified, FFprobe time base `1/2997` to the native sum gives `2321400/2997 = 773800/999`, approximately **774.574574575 seconds**. The prior stream duration was **774.506507 seconds**: a numerical difference of about **0.068067575 seconds** under that assumption. The media/movie header timescales and edit-list fields are not interpreted here. This is not an established duration error, missing-footage measurement or filming-clock calibration.

Apple's saved timing definition itself says `stts` in its title/overview but `ctts` in the layout's Type row. Both descriptions are retained with line locators and the source hash in [SOURCE-PINS.json](SOURCE-PINS.json). The parser recognizes the literal `stts` bytes in this movie. Apple's differing descriptions remain unresolved; they are not evidence of movie alteration.

## Verification and limits

**Fourteen controls passed**, covering truncated headers, overclaimed table lengths, unsupported version, nested absolute offsets, extended atom size, size-to-parent-end, and preservation of zero-size/delta values in valid synthetic inputs. A separate `int.from_bytes` reader, without importing the parser, checked all11,607 sizes and the timing run at the saved offsets. It reproduced the counts, positive-size total, size sum and final entry. This verifies reading/arithmetic, not a decoder or historical footage.

[VERIFICATION.json](VERIFICATION.json) records actual checks. [native_tables.py](native_tables.py) is the executed parser. Reproduce against a lawfully held matching source by first resolving it through the repository's `tools/media_path.py` and verifying the SHA-256, then running `python3 -B native_tables.py <resolved-source> <new-output.json>`. Source mode is `rb`; the output must be new. The standalone parser does not replace the media-store guard. No movie, extracted images, audio, copyrighted definition bodies, personal data, correspondence or credentials are included.

**TODO T23-01:** obtain/check the corresponding primary layouts, then interpret `elst`, `mdhd`, `mvhd`, `stsc`, `stco`; trace sample-to-chunk addresses, media-data bounds and edit/presentation intervals. Obtain export/configuration lineage and a genuinely independent implementation test. Keep all counters. Changing the expected extraction count is not acceptance of the failed check.

**TODO T23-02–04:** original camera/tape and filming/export logs; N10-C3B/uncertain-marking originals; intake/alias/geometry/coupon/transfer/disposition records; source-supported physical-piece/cross-file joins. The museum policy [CONS-POL-02–07 records](https://github.com/AveLyra/911-conspiracy-investigation/blob/b1ebd3c0856174ec3362469d81686fc0a6ec65ea/investigation/broader-evidence/steel-collections-policy-2026-11-04/RECORD-TARGETS.json) remain unacquired. All eighteen original FAA/telephone/recorder/materials/steel criteria remain open or partial.

Export conventions, edit/presentation treatment, source integrity and implementation behavior remain distinct untested causal possibilities. These table observations do not establish substitution, deliberate editing, lost camera footage, misconduct, explosives, conspiracy or motive. Earlier records and failures are unchanged; this is an additive source-integrity result.
