# Eight-frame source/representation check

2026-09-24. Checker `/root/curve_source`. **PASS: all eight prospectively
selected files exist and match their recorded identities, dimensions and
source-index/PTS joins.** No image was displayed or decoded. This is a
metadata/integrity check, not a flash observation, historical authentication,
photometric calibration, motion remeasurement or absence verdict.

Read the complete current PROTOCOL.md before this selected check:
6,040 bytes, SHA-256
`5cb7933fbdc109801245363b0bd15e49622907dd85fb4fdb8eec08f4cf346ff0`.
Main controls/charter continue to govern. Earlier source/timing/provenance
notes supplied locators and recording limits, not authority to acquire media.
No source, old observation, or legal record was changed. This is the only
file written by this checker for the task.

## Actual command and acceptance

Executed read-only `python3 -B - <<'PY'` inline checks from the main workspace
using `pathlib`, `hashlib`, `fractions`, `csv`, `io`, `json`, `struct` and `sys`.
Python **3.13.7**; exit 0; result
`PASS_EIGHT_SELECTED_FRAMES_METADATA_AND_BYTES_ONLY`.

The selected check read and then reread **26 distinct files**, all unchanged:
the protocol, source videos, relevant maps/source identities, receipts and
selected PNGs. It checked literal file sizes/SHA-256, PNG signature/IHDR,
unique selected-map membership, exact `Fraction(PTS) * Fraction(time_base)`
joins, and corresponding receipt product membership. No Pillow, FFmpeg,
media player, image-viewing tool, network, or new extraction was used.
The PNG checks are header checks, not pixel decompression or a new proof
of source-to-pixel correctness.

Camera2: all four chosen run01 PNGs are byte-identical to their run02
counterparts. Both complete selection maps have 421 selected records from
the 8,042-frame source; each requested index occurs exactly once. Both
recorded before/after input-pin dictionaries agree and match actual current
source/map/identity bytes. Every selected timing field matches the original
timing CSV row at that zero-based source index.

Camera3: all four PNGs have exactly one `native_unmarked` product entry in
the views01 receipt and one corresponding clock row. Those clock rows equal
the indexed records in the prior WMV diagnostic map; their recorded pixel
hashes also equal the prior map's entries. The map contains 442 clock and
pixel-hash records. These stored pixel-hash equalities were checked without
decompressing PNGs; no freshly computed pixel hash is claimed.

## Literal selected paths

```text
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/run01/camera2/f006593.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/run01/camera2/f006717.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/run01/camera2/f006958.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera2-penthouse-event/run01/camera2/f007013.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-late-reannotation/views01/frame-0258.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-late-reannotation/views01/frame-0300.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-late-reannotation/views01/frame-0330.png
/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-late-reannotation/views01/frame-0348.png
```

Camera2 PNG IHDRs specify **640×480, 8-bit grayscale**; Camera3 specify
**720×480, 8-bit grayscale**. Both have PNG compression/filter method zero
and are noninterlaced in the IHDR. Native here means the retained full
stored-resolution derivative, not a camera-original image or a color image.

| Camera | Zero-based source index | PTS | Time base | Exact encoded seconds | PNG bytes | PNG SHA-256 |
|---|---:|---:|---|---|---:|---|
| 2 | 6593 | 659301 | 1/2997 | 219767/999 | 124462 | `39bcb70c16ccc468133edf92b3a9dc9ea43edbc5692d82d8adcfc08cc22903a8` |
| 2 | 6717 | 671703 | 1/2997 | 223901/999 | 123245 | `286e194659c7bc7fc2a1bdc5180be5e99210af0631b8afd7945494cbe47000b9` |
| 2 | 6958 | 695804 | 1/2997 | 695804/2997 | 121390 | `8026c0851012674c8dba4c70551c0e4e062ddaa7f58879dd5a6c9791454513c3` |
| 2 | 7013 | 701303 | 1/2997 | 701303/2997 | 122931 | `0187a544c81ed0eff4f452d0744eb40eec6aec37ae35a0f2059f4e931ab3c5c7` |
| 3 WMV | 258 | 17200 | 1/1000 | 86/5 | 93612 | `4fc10778ab5ca7d94719cf9880c26b6ce5e3f622ce4aca2d1fc3e749c246e571` |
| 3 WMV | 300 | 20000 | 1/1000 | 20 | 94380 | `69b101de4136fbfc6ce43a41b26e76292325e36298f01dcd7b97bdea71c8a717` |
| 3 WMV | 330 | 22000 | 1/1000 | 22 | 79726 | `ba874f8721db2d01c4eb8c40d8fa54794339d1571c3aad4ec4d85bb0580fe448` |
| 3 WMV | 348 | 23200 | 1/1000 | 116/5 | 72005 | `91e7cc04d40b343c4dadc85d0690fd583eb918a07aa4d661f0dbc2a8c24e4598` |

Camera2 decimal display equivalents are approximately 219.986986987,
224.125125125, 232.166833500 and 234.001668335 seconds. Camera3 equivalents
are 17.2, 20, 22 and 23.2 seconds. These are unsynchronized file clocks,
not equivalent physical instants or authenticated exposure times. Prior
rooftop/descent labels explain selection only; this check did not verify them.

## Camera2 source and map chain

Source actually rehashed:
`/Users/admin/docs/911/research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov`

208,810,910 bytes; SHA-256
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`.
The held acquisition manifest identifies VID-WTC7-001 as a secondary-hosted,
expressly converted analysis copy, not an authenticated native or complete
broadcast master.

Primary held timing map:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv`

867,161 bytes; SHA-256
`ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812`.
The associated `frames.json` and `source-identity.json` were also rehashed
against the extraction's input pins. Use actual PTS, not a rounded uniform
rate: the timing record reports irregular 99/100/104-tick intervals.

Under the worktree investigation base:

| Metadata file | Bytes | SHA-256 |
|---|---:|---|
| camera2-penthouse-event/run01/camera2/selection.json | 330219 | `e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d` |
| camera2-penthouse-event/run02/camera2/selection.json | 330219 | `e297292a04a093d757b7693b9914abe4b88db4e6b836461f49c8dee411e78b2d` |
| camera2-penthouse-event/run01/receipt.json | 68222 | `a5c72edd8f7714c0916c7b66f39f745c2cd7d73c99510f6c8a4be87ed751a114` |
| camera2-penthouse-event/run02/receipt.json | 68222 | `a85520fbeb1e6b8992d9fd012329d41cf2f56975fddb237678218407069b4b57` |

The two receipts are not byte-identical; no such assertion is needed for
the matched selections and four paired PNGs. Both record complete status,
exit 0, **one known audio-layout stereo-guess diagnostic**, and zero
unclassified diagnostic lines. That is not a warning-free decode. This pass
read the structured diagnostic summary, not the raw decoder log or a rerun.

## Camera3 source and map chain — WMV, not the old MP4

Source actually rehashed:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv`

1,350,045 bytes; SHA-256
`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`.
It matches the extraction receipt's before/after source pins and the held
public lab-kit inventory's selected outer-member product identity. The kit
receipt was rehashed: 2,557 bytes,
`4e3f10f0fd0601b955bfcef64453c6e8dfb93eb5b21b8d994e222839e30fc2dd`.
No ZIP member was re-extracted or archive CRC newly checked here. The held
provenance describes the public WTC-911-Motion-Lab kit; this packaging link
does not authenticate a camera master or independent exposure history.

The old VID-WTC7-002 `NIST Camera 3.mp4` is a different 331,368-byte,
232-frame file with time base 1/15000 and SHA-256
`0c147549fa51c57686bd506c1d979af23835e72ac777fa30e2f2eb8b15aeb8be`.
Those are held-manifest/timing facts, not a fresh hash of that unused MP4.
Indices 258/300/330/348 in this audit belong to the **442-frame WMV**; they
must not be joined to that shorter MP4 or treated as a NIST-original clock.

Exact held clock/pixel-map path:
`/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-recording-comparison/wmv-diagnostic/run02/default-frames.json`

136,937 bytes; SHA-256
`8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2`.
Its adjacent `receipt.json` is 13,520 bytes; SHA-256
`11bb4f4d44031621322b068648647f4e0c437f61510d3b4e6d380e8fc62cc227`.
Both match views01's pinned inputs.

The selected derivative receipt is
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/camera3-late-reannotation/views01/receipt.json`:
21,509 bytes; SHA-256
`8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161`.
It retains **pass_diagnostic_only** status and **three corrupt mentions**.
The older receipt retains **diagnostic_complete_no_sequence_admitted**;
default and single-thread warning indices are **37,55,63**, with identical
raw outputs in that recorded comparison. All four selected clock records
have null `warning_log_line`; none is one of those indices. This does **not**
establish clean historical pixels, absence of propagated artifacts, or a
usable original exposure clock. This check does not upgrade those statuses.

## Limits for the proposed spatial audit

All eight are full-frame grayscale derivatives; they preserve neither color
nor an independently calibrated radiometric response. A current hash proves
agreement with held bytes, not correctness of conversion, exposure/shutter
settings, sensitivity to an internal or outward luminous event, or original
scene continuity. A visible exterior region need not reveal a concealed
source; a hidden source could still illuminate an exposed region. Both
possibilities remain for the observers to consider.

These eight sparse stills cannot establish a transient event's presence or
absence between them or throughout either video. No intensity, clipping,
contrast, duration, charge, flash-count or detection-probability measurement
was made. The next qualitative review remains bounded by the protocol; any
temporal/detector test requires its own declaration and applicable human and
synthetic-control gates. No acquisition, source promotion, cause ranking,
or accepted-engine change follows from this pass.
