# Camera3 spot persistence: input preflight

2026-10-04. Read-only source/representation review before any new image view or
decode. Owner `/root/sibling_byte_audit`. Fixed target: zero-based decoded WMV
ordinals255–261, qualitative persistence only. This note does not authorize an
extraction, classify a cause, supply human acceptance or alter earlier freezes.

## Result and material limitation

**PASS for current held-byte identity and the seven saved timing joins.** Fifteen
source/receipt/map/binary/log/PNG identities match their retained expected pins
before and after the check. All seven selected map records match the retained
probe and actual saved decoder-log lines. The existing258 PNG is correctly
joined at the metadata level; its pixels were not decompressed in this preflight.

**Seven already-held grayscale planes were not located in the inspected route.**
The complete `camera3-late-reannotation/prepare.py` reads a fresh full decode
into memory, checks all442 frame hashes and the full raw hash, then saves22
selected frames:258 and288–348 step3. It does not save the full raw stream.
The earlier run02 receipt likewise records a raw stdout hash, not a saved full
raw-plane artifact. The six neighbors are not among views01's declared products.
The bounded main recording-comparison/provenance filename check, including
ignored files, located no `.gray`, `.yuv`, `.raw`, `.bin`, `.dat` or relevant
plane artifact; its sole `.npy` hit was an unrelated matching score array.
This is not an archive-wide absence finding. Given the located route, a new
decode is needed to materialize the seven images; hashes alone cannot reconstruct
pixels. The existing seven per-frame hashes provide exact prospective targets.

The reusable contract is the prior no-seek, full-stream, no-autorotate/no-autoscale,
passthrough grayscale decode, followed by complete raw/hash agreement and direct
720×480 frame slicing. No old pipeline was executed here. Root must freeze the
new protocol and extraction/failure contract before any new decode. A fresh
run must not inherit “passed” status from this preflight or silently overwrite
old outputs. Diagnostic-only source status remains even if all hashes match.

## Exact source and index identity

Path abbreviations below are literal bases:

- `M=/Users/admin/docs/911/research/sherlock-wtc7-investigation`
- `B=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation`
- `D=M/camera3-recording-comparison/wmv-diagnostic/run02`
- `V=B/camera3-late-reannotation/views01`

Source: `M/camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv`.
This is the442-frame public-kit WMV, **not** the different232-frame old MP4.
Retained stream metadata: stream index1, codec `wmv3`,720×480,`yuv420p`,SAR1:1,
time base1/1000. The derived grayscale output is720×480 bytes/frame. Calling it
a “Y plane” does not establish byte identity to an original camera's luma plane,
color fidelity, radiometric calibration or an unprocessed exposure.

The seven rows below are stored output ordinals and presentation times, not
original camera exposure numbers, event-day times or independent wall clocks.
All have `warning_log_line:null`; all selected probe rows report P pictures,
`interlaced_frame:0`, `repeat_pict:0`, dimensions720×480 and matching best-effort
timestamps. Their spacing is66/67 ticks; use actual PTS, not rounded15fps times.

| Ordinal | PTS, 1/1000 s | Exact encoded seconds | Expected grayscale pixel SHA-256 |
| ---: | ---: | --- | --- |
|255|17000|17|`c1e64c8cd1bb896379f1cae1771d799946b1580540462a57428c155f7f1ba386`|
|256|17066|8533/500|`9832633f5627ab9895c8635a53d4c09b3f651e8e672704ed28198d955a29a46d`|
|257|17133|17133/1000|`305d7a647832d7613fa754d2c3e6bbeecfad05e57b4b77cacc0657e8f8414533`|
|258|17200|86/5|`486e653f5100477a6ab2b6994aff023a4e4aae2ed22c24ef72c67956fe6976ea`|
|259|17266|8633/500|`43d3bd1224d77eff8aeed53a2efa0d55a3301aa3e174ed77f9e4cb5bcaba5dae`|
|260|17333|17333/1000|`779591c24426e5eca4c927276a766cb30a045fdb4adf5890535b2bd0d16d5a39`|
|261|17400|87/5|`a692bb454d665d1bd0712666e9dbb2e5b02b238ecb818f9cd8493b238a60e17c`|

Existing `V/frame-0258.png` has exactly one `native_unmarked` product entry and
one258 clock row. That row equals `D/default-frames.json` record258, including
the pixel hash. Actual PNG signature/IHDR is720×480,8-bit grayscale, standard
compression/filter methods0, noninterlaced. PNG file SHA is distinct from the
decoded-pixel SHA. Header and receipt checks are not a new pixel-value proof.

## Current pins: expected equals actual

All fifteen rows below were checked twice in the successful final command.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
|Source WMV above|1350045|`48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722`|
|`D/default-frames.json`|136937|`8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2`|
|`D/receipt.json`|13520|`11bb4f4d44031621322b068648647f4e0c437f61510d3b4e6d380e8fc62cc227`|
|`D/wmv-probe.json`|139303|`38e8690fedc3330fcb5cf904462d4945aed7bfac4bfd8da9d9766d536237df8b`|
|`D/synthetic-checks.json`|3315|`e7d029e1140e65f9373ad9dd4ed9ae39d13ea88dae2597d81b31e7fe24b7ab1b`|
|`B/camera3-late-reannotation/prepare.py`|5653|`0b7baeb81236a7ab8fdb5435ed7d86e10c754e22fd35f94051d96538ae29d139`|
|`B/camera3-late-reannotation/PROTOCOL.md`|7092|`7b13e006ab382121452f6e7c59f37d7f586b57f297a7e1c7154b86b2aae06c2f`|
|`/opt/homebrew/bin/ffmpeg`|421968|`7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569`|
|`/opt/homebrew/bin/ffprobe`|351920|`fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad`|
|`D/default.stderr.local.txt`|626570|`b556ad3d3ee0dd5b8cd4550eb849596043997227933f1276f72674214284072d`|
|`D/single.stderr.local.txt`|617108|`5cdb7d359fe56901d5b0748d2ef89d72e210c34d8d4add96234afddbab577027`|
|`D/stop-on-error.stderr.local.txt`|58004|`55991f6643fa47d365071ad599ccebfd94b4de32465bcbd1e2f5ac491de802fd`|
|`V/receipt.json`|21509|`8bf54e80ccb0eb823cd9a09fc45e285fa4a649c166aaf2b26d551c13782c3161`|
|`V/frame-0258.png`|93612|`4fc10778ab5ca7d94719cf9880c26b6ce5e3f622ce4aca2d1fc3e749c246e571`|
|`M/camera3-provenance/kit-inventory/run-v1/receipt.json`|2557|`4e3f10f0fd0601b955bfcef64453c6e8dfb93eb5b21b8d994e222839e30fc2dd`|

The recorded full grayscale stream is152,755,200 bytes,442×720×480, SHA
`1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`.
That is agreement between retained map/receipt fields, **not a fresh raw-stream
hash**. Whole-file hashes establish held-byte identity, not historical authenticity.

## Warning provenance and prior controls

The retained default log contains three `corrupt decoded frame` warnings at
lines391/555/629, immediately followed by the same decoder-context frame records
at392/556/630. Their saved ordinals are37/55/63,PTS2466/3666/4200. This check
confirmed those literal log/context joins. Selected255–261 decoder records are
at2280/2292/2303/2309/2323/2332/2337 and match their respective PTS.

The prior diagnostic report attributes the inspected warning neighborhoods to
countdown graphics, not visible building imagery. That is a preserved earlier
visual finding; this checker viewed none. It narrows a corruption objection but
does not prove no propagated decoding effect or clean later historical pixels.
The prior default/single passes recorded identical raw hashes; the strict
stop-on-error run recorded exit183 after37 raw frames. Neither was rerun here.
views01 recorded three warning mentions, exit0 and `pass_diagnostic_only`; its
stderr hash differs from run02 and its stderr was not retained as a local file.
No byte identity between those two stderr streams is claimed or required.

The prior synthetic receipt records twelve successful checks: fixture pixels,
timestamps and no warnings; same/nested/intervening contexts; terminal warning;
rejection of compressed repeats, double warnings, malformed PTS, unparsed serious
diagnostics and unresolved warnings. These are **read retained test results**,
not tests executed now. The full prior preparation source preserves direct
pixel slicing, input-before/after pins and raw/frame hash gates. Its exceptional
failure coverage is limited; the old validation notes that some failures lack
a durable receipt. Do not treat it as a general extraction-framework approval.

## Runtime and actual verification

Bare `python3` currently resolves to Homebrew3.14.0 and lacks installed Pillow
and NumPy metadata. Explicit `/Users/admin/.pyenv/shims/python3` resolves to
3.13.7 with Pillow12.0.0/NumPy2.3.4 metadata, matching the prior versions.
Its resolved executable `/Users/admin/.pyenv/versions/3.13.7/bin/python3.13`
is33816 bytes, SHA`7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e`.
These are interpreter/package identity checks, not fresh image-library tests or
a dynamic-library build attestation. FFmpeg/ffprobe executables match old pins;
they were not launched. The old receipts report7.1.1, not a freshly queried version.

Actual final check: read-only inline `python3 -B - <<'PY'` using
`pathlib/hashlib/json/fractions/struct/re` (`ff0149`, exit0):15 before/after pins;
seven selected ordinal/PTS/probe/log joins;258 receipt join and PNG header;
three warning/context joins. No media or PNG-pixel decode. Runtime metadata
commands `6eaf82` and explicit-pyenv `191bc9` both exited0.

Preserved failed checks: `f483e8` exited1 after pins/selected joins/header passed
because my log assertion mistakenly expected `frame_pts` rather than `pts`.
Literal-line inspection `859af8` corrected that checker assumption. `8e9e8b`
then passed all integrity assertions but exited1 querying unavailable Pillow
metadata in bare Python3.14; the separate runtime checks resolved the route.
Mixed main/worktree locator `3a0590` exited2 for three worktree-only files; the
correct worktree read `8f8e0e` supplied them. Combined control output was
truncated; WORKFLOW/START-HERE and the full charter were reread separately.
No failed command altered sources or executed a historical pipeline.

Coverage: current main AGENTS/WORKFLOW/START-HERE and full charter; STATUS top110
lines; complete October assessment, original flash observer note, old preparation
source, flash source check, late-annotation validation and WMV diagnostic report;
complete run02 receipt/synthetic-check JSON; selected views01 receipt fields,
seven map/probe rows, and listed warning/log lines. `rg --files --hidden
--no-ignore` was limited to the declared main camera3 recording/provenance route
for raw-plane availability; no broad body/source search or image inspection.
The full charter hash remains`54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd`.
Only this new working source check was written. All prior freezes, source media,
legal/main files, human gates, matrix and engine state remain untouched.

## Prospective adapter handoff, before historical execution

Root subsequently supplied the complete new protocol, adapter and seven-method
synthetic test source. All three were read (`5389e4`, exit0); no tests or adapter
were run by this checker. Root reports seven passing synthetic methods; that
is attributed execution, not my reproduction. The development-verification
skill was applied to keep static review distinct from executed tests.

Snapshot pins checked with `shasum -a 256` (`267dcd`, exit0):

- New protocol: `bb2e8f38e7c0d7aadb3421252a2fe054dfa36d00101403e5250f161df1cba2b0`.
- New `prepare.py`: `c3efc984e4a076d97de420f3fd576e2d7fcfdeafb7e523b8b7dc5f56b08e8a1a`.
- New `test_prepare.py`: `78f5a041ccdc2cf1244d00505d9affe0ac3ab5182c7a418d1fd474752afb71da`.

The protocol explicitly permits one exact-recipe decode after source/method
checks, verifies all442 grayscale hashes, saves only seven native PNGs, and
requires selected PNG re-decompression plus old258 pixel equality. This is
consistent with the available hash/map route and scoped missing-plane finding.
The adapter imports only the pinned old module's definitions, not its `main`.
It adds a60-second timeout and retains new stderr rather than relying on the
unretained views01 stderr. No historical extraction had been performed by this
checker or reported complete when this snapshot was read.

One narrow failure-receipt issue was sent to root/method review: in this adapter
snapshot, `selected_planes` can reject raw length before `receipt['decode']`
receives the completed subprocess's return code, byte count and hash. Stderr
and the exception are saved, but that branch's return-status detail is lost.
The suggested repair is to capture decode metadata before length validation,
with a focused synthetic failure check. A later code/test version needs its own
review/pin; this source preflight does not silently certify that repair. Root
owns the implementation, frozen protocol and eventual go/no-go decision.
