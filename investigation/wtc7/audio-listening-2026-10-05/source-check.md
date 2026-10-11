# Independent source check — four held stereo excerpts

Checked October 5, 2026 by the separate `audio_source_check` agent. Research-only verification under the main investigation charter and this unit's protocol. No listening, event annotation, historical signal interpretation, acceptance on behalf of a human, new decode, disclosure, commit, or push was performed.

**Disposition:** All four held WAVs pass the declared byte, structure, and recorded source-map checks. Both encoded source tracks also match the acquisition manifest and the original receipt; fresh allowlisted stream probes match the stored metadata. This establishes present integrity relative to the held records and consistency of the recorded derivation. It does not freshly reproduce the audio decode, authenticate an original microphone recording, or validate an event time or causal interpretation.

## Scope and authority

Read the main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, investigation `CHARTER.md`, the worktree `AGENTS.md`, the source-of-truth-guardian and evidence-falsification-auditor skills, this unit's `PROTOCOL.md`, the earlier acoustic protocol, and the complete `audit_audio.py` implementation. The worktree `AGENTS.md` differs from main; main's current controls supplied in the assignment remain controlling. No legal or main research files were edited.

The unit protocol SHA-256 was checked before substantive verification and again at the final postcheck: `c0d6f9aafd8295cfef9e2f865a174c2afbd1335e398fca333a638d7c7782b4af` (6,002 bytes).

Acceptance for this check was: exact four held files; fresh SHA-256 and size match to `receipt.json`; valid RIFF/WAVE structure with 44,100 Hz, two channels, 32-bit IEEE float; declared data lengths, frame counts, and durations; exact interval/source joins to `measurements.json` and the pinned slicing implementation; acquisition-manifest/source-byte joins; and a final hash postcheck. Neither successful file parsing nor these checks establishes perceptual access.

All WAV and original audit paths below are under the main directory `/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/`. This report alone is a new worktree research derivative.

## Fresh measured WAV properties

The files are `run01/<name>-stereo.wav`. Every property in this table was freshly measured; every hash/size pair exactly matches `receipt.json.products`.

| Name | SHA-256 | File bytes | Data bytes | Sample frames | Duration |
|---|---|---:|---:|---:|---:|
| spoken | `5b12b06ab0f2699539e5621b8483d9c96163364cabdace3768c8b296240de127` | 6,350,458 | 6,350,400 | 793,800 | 18 s |
| msnbc | `b9758e82432a354fc584b22529b03c84aefc7b192d8579d5b8f95de3b715b292` | 13,406,458 | 13,406,400 | 1,675,800 | 38 s |
| edited | `b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd` | 8,820,058 | 8,820,000 | 1,102,500 | 25 s |
| comparator | `2a846dcd29fe82f32f5c0694afd05c99a6c5a6923dae78c5c1ccbf1dc7eb59d0` | 5,997,658 | 5,997,600 | 749,700 | 17 s |

For every file, the little-endian RIFF size equals file size minus eight. The chunks are exactly `fmt ` (18 bytes, header offset 12), `fact` (4 bytes, header offset 38), and `data` (header offset 50; payload offset 58). The format tag is 3 (IEEE float); channels 2; sample rate 44,100; byte rate 352,800; block alignment 8; bits per channel sample 32; format extension size 0. The `fact` frame count equals `data_bytes / 8`, which also equals the relevant `measurements.json.windows.<name>.quality.sample_frames`. All chunks fit inside RIFF bounds and parsing terminates at the declared end without an extra trailing chunk.

The scalar channel-sample count is twice the sample-frame count. No sample amplitudes, sound categories, waveforms, or spectra were inspected or interpreted for this check.

## Source-map joins

These source IDs and intervals agree exactly across this unit's protocol, the earlier protocol, `measurements.json`, and `audit_audio.py.WINDOWS`. Index bounds refer to decoded stereo sample frames; the end is exclusive.

| Name | Source ID | Track interval | Full-decode frame interval | Local-to-track coordinate |
|---|---|---|---|---|
| spoken | VID-WTC7-007 | [58, 76) s | [2,557,800, 3,351,600) | `58 + local_seconds` |
| msnbc | VID-WTC7-007 | [578, 616) s | [25,489,800, 27,165,600) | `578 + local_seconds` |
| edited | VID-WTC7-007 | [430, 455) s | [18,963,000, 20,065,500) | `430 + local_seconds` |
| comparator | VID-DEM-002 | [8, 25) s | [352,800, 1,102,500) | `8 + local_seconds` |

At local frame `j`, the recorded decoded-track coordinate is `start + j / 44100`. This exact sample-index arithmetic does not provide exact acoustic event timing, original camera time, original recording speed, or synchronization with any video. The 98 seconds of excerpts are not 98 seconds of independent event coverage: three share the same compilation and the comparator concerns another building.

The inspected implementation calls `runner.decode(sources[key], raw, key + "-full-decode")` without start, duration, mono, resampling, normalization, or filtering options. Its command is `/opt/homebrew/bin/ffmpeg -nostdin -loglevel error -n -i SOURCE -map 0:a:0 -vn -c:a pcm_f32le -f f32le TEMP_OUTPUT`. It maps the complete decoded bytes as `<f4`, reshapes them into two channels, then writes `np.array(decoded[start * SR:end * SR], dtype=np.float32)` using `wavfile.write(..., SR, x)`. Both recorded full-decode commands have exit 0 and zero stderr bytes. The separately executed legacy seek/mono paths do not supply these held stereo WAVs.

The receipt records Python 3.13.7, NumPy 2.3.4, SciPy 1.16.2, and FFmpeg/ffprobe 7.1.1. Recorded FFmpeg binary SHA-256 is `7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`; recorded ffprobe binary SHA-256 is `fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad`. These are historical receipt values, not newly verified binary identities.

## Encoded sources and recorded full decodes

Source files are relative to `/Users/admin/docs/911/research/wtc7-video-comparison/media/`.

| Source ID | Local path | Fresh bytes | Fresh SHA-256 |
|---|---|---:|---|
| VID-WTC7-007 | `compilations/WTC Building 7 Collapse - 27 Angles [cmp7rV2aZhM].f140.m4a` | 12,637,745 | `d8b75d1f861a327a38e73f00b645c511b27734325305cbecd4e18dc20d71558c` |
| VID-DEM-002 | `comparators/explosive/Capital One Tower Implosion [rW_xXcS4y3A].f140.m4a` | 730,245 | `c6992f04793f46a7326eae28e3f373db21de84cc2ae9c26f89ec430dc1143e7f` |

Each fresh hash/size matches the acquisition manifest's allowlisted `record_id`, `local_path`, `sha256`, and `bytes` fields, the original `source_before`, original `source_after`, and code's source pins. No acquisition URLs, platform info JSONs, credentials, or delivery tokens were printed or inspected. The acquisition manifest's current whole-file SHA-256 is `5f39f34f6ba978ff8e030c632ab49c54950faaaf2fb3654ccd5cdc14bdfee6dc` (5,733 bytes); that hash pins the file version but does not authorize or describe its other fields.

Fresh `ffprobe` output for each encoded file contains one audio stream (index 0), AAC, planar float decode format, stereo, 44,100 Hz, time base `1/44100`, start PTS 0 and start time 0. It exactly matches the selected fields of the pinned stored stream metadata. VID-WTC7-007 has duration_ts 34,458,624, duration 781.374694 s, and 33,651 encoded frames. VID-DEM-002 has duration_ts 1,988,608, duration 45.093152 s, and 1,942 encoded frames. Those encoded-frame counts are not PCM sample-frame counts.

`measurements.json.full_decode` records the following; these decoded buffers were **not regenerated or freshly hashed** in this check:

| Source | Recorded decoded sample frames | Recorded duration | Recorded raw full-decode SHA-256 |
|---|---:|---:|---|
| VID-WTC7-007 | 34,458,624 | 781.3746938775511 s | `7a122128ed8a4197fd75fafad0f206b909ec0317382176ddd9ee4fe133d3ed80` |
| VID-DEM-002 | 1,988,608 | 45.09315192743764 s | `25cd810c22544dc2f988094c584b28e96feae7782e30d95c1590fae41a3b17dc` |

All excerpt bounds fall within those recorded full-decode lengths.

## Dependency pins and actual checks

| Dependency relative to main acoustic-audit | Fresh SHA-256 | Result |
|---|---|---|
| `audit_audio.py` | `fe57ac658782f374d97eb791cb78a64c2ba790f2d7223a956aaf7490f1a95697` | Matches receipt `procedure_sha256`; implementation read completely |
| `PROTOCOL.md` | `098ec5c221016b9b3101cdb593f34945639b1f57a0763a3e316fc6141054c0d0` | Matches receipt `protocol_sha256` |
| `run01/receipt.json` | `f03593d8aa2f76a27e5ce9bca43dad273c07e71c3b35ad20b0a49645cacb93f8` | Fresh version pin; stored status `complete` |
| `run01/measurements.json` | `2dde71b13b60a32bfe675258410575a430567c126b77e0320fcce5d0895425cc` | 11,408 bytes; matches receipt product |
| `run01/stream-metadata.json` | `18d1d126d2f2549d161bd4e0174268e70f2a5df83a46495147b922e7757c3b23` | 2,386 bytes; matches receipt product |

The inspection used `sed` to read the instruction/method files and `shasum -a 256` to pin dependencies. A read-only `python3 - <<'PY'` command at `2026-10-05T06:43:03.486759+00:00`, under Python 3.13.7, used only standard-library `csv`, `hashlib`, `json`, `struct`, `pathlib`, `sys`, and `datetime`. It did not import or execute the historical audit program. The essential actually executed operations were:

```python
with p.open('rb') as f:
    sha = hashlib.file_digest(f, 'sha256').hexdigest()
# Every WAV hash/size asserted equal to receipt products, before and after parsing.
magic, size, wave = struct.unpack('<4sI4s', f.read(12))
cid, n = struct.unpack('<4sI', f.read(8))
tag, ch, sr, byterate, align, bits = struct.unpack('<HHIIHH', fmt[:16])
assert (tag, ch, sr, byterate, align, bits) == (3, 2, 44100, 352800, 8, 32)
frames = databytes // align
assert frames == fact == (end - start) * sr
assert (w['audio_id'], w['start_s'], w['end_s_exclusive']) == (key, start, end)
assert w['quality']['sample_frames'] == frames
```

This is an excerpt of the verification operations, not a standalone script. The command also asserted RIFF/chunk bounds, exact chunk order, no trailing data, method/protocol/product hashes, source-manifest paths/hashes/sizes against both receipt source states, required stored stream format/start fields, full-decode command outcomes, and containment of every interval within its recorded decoded length. Its actual exit was 0, with the final output:

```text
PASS four WAV byte/header/map joins; two encoded-source byte/manifest/receipt joins; stored full-decode lineage inspected; no decode or listening performed
```

A second read-only Python command invoked this exact allowlisted probe, separately for the two source paths in the source table:

```text
/opt/homebrew/bin/ffprobe -v error -show_entries stream=index,codec_name,codec_type,sample_fmt,sample_rate,channels,channel_layout,time_base,start_pts,start_time,duration_ts,duration,nb_frames -of json SOURCE_PATH
```

Both returned exit 0, empty stderr, and exact equality to the corresponding allowlisted stored fields. This was a metadata probe, not a new PCM decode or playback.

That second command performed a **final** fresh full-file hash/size pass on all four WAVs after the source/method review and stream probes, at `2026-10-05T06:43:41.541942+00:00`; every file again matched its table hash/size and the receipt. It also rehashed the six method/receipt/protocol dependencies listed above, including the unit protocol. Actual exit 0; final output:

```text
PASS fresh allowlisted source stream probes and final four WAV hash/size postchecks
```

No substantive integrity, structure, or source-map check failed. During navigation an initial broad file listing was truncated, a no-match `rg` search exited 1, and `cmp` of main/worktree `AGENTS.md` exited 1 because their contents differ; the applicable instruction files were subsequently read directly. Those navigation outcomes were not treated as evidence checks or concealed as successful comparisons.

## Evidentiary limit and disconfirming conditions

**Directly observed:** current bytes, sizes, WAV headers, dependency hashes, source hashes, and fresh stream metadata. **Derived:** PCM-frame counts, durations, and arithmetic sample-coordinate mappings. **Recorded derivation, not freshly reproduced:** that these WAV payloads were generated from the specified complete decodes by the reviewed method. The hash join and matching method/receipt strongly support that recorded lineage, but a coordinated incorrect or altered upstream record would not be excluded by internal consistency alone.

No hashes establish historical authenticity, original microphone custody, an unedited soundtrack, a genuine event-source attribution, listener capability, event onset precision, A/V synchronization, or the opportunity to detect an absent sound. Unknown editing, codec history, microphone geometry, propagation delay, and record provenance remain outside this check. A changed byte hash, malformed header, discordant source ID/interval, different source stream start/rate, or independent decode mismatch would defeat the relevant passing claim. An original-recording provenance or event-timing conclusion would require separate evidence, not more precision in sample arithmetic.

No root listening response, sealed capability fixture, or synthetic transcript was accessed. No historical annotation was made or accepted. This source check supplies the preparation needed for the unit's separately gated listening or human-review path; it does not itself satisfy that path.
