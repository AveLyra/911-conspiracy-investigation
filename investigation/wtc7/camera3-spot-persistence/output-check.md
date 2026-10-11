# Independent selected-output audit

2026-10-04. Checker `/root/sibling_byte_audit`. **PASS for the declared seven
diagnostic derivatives.** All seven PNGs were freshly decompressed without
display, and every720×480 grayscale pixel buffer matches the original map's
expected hash. Frame258 also equals the older PNG both pixel-for-pixel and
byte-for-byte. No new selected-output blocker was found. This is not a visual
finding, human approval, historical-source authentication or clean-pixel claim.

The frozen [source preflight](source-check.md) remains unchanged. Its initial
adapter diagnosis is history, not a claim that the repaired adapter still has
that defect. Current full protocol/code and the run receipt/method review were
read in `10a391` and `b60b7b`, both exit0, before checking the outputs.

## Fresh checks performed

From the dedicated investigation worktree, a read-only inline command used
`/Users/admin/.pyenv/shims/python3 -B - <<'PY'`, standard-library
`pathlib/hashlib/json/fractions/re` and Pillow12.0.0. It imported no producer,
executed no old pipeline, displayed no image and launched no video decoder.
The successful full check is `48aae4`, exit0, Python3.13.7.

- Exactly ten regular nonsymlink files are in `run01`: seven declared PNGs,
  `start.json`, `receipt.json`, and `decode.stderr.local.txt`. No extra image,
  raw stream, failure receipt or unintended product is present there.
- The seven receipt rows are exactly255–261, once each, with expected filenames.
  Each container's actual byte count/hash agrees with its receipt entry.
- Each newly decompressed PNG is formatPNG, modeL,720×480,345600 bytes. Its
  calculated pixel SHA equals both the original held map and the new receipt.
- Each clock dictionary equals the original indexed map record; exact rational
  seconds equal PTS×timebase. The earlier258 PNG was independently opened and
  its pixel buffer compared directly, not only by hash.
- All eleven current input files match both recorded before/after pin sets.
  These include source WMV, map, old receipt/code/258 PNG, final adapter/tests/
  protocol, charter, FFmpeg executable and actual Python executable.
- Every field retained in `start.json`, except its expected `started` status,
  agrees with the final receipt. The command is identical to the old default
  command. Final status is `pass_diagnostic_only`, return code0.
- Twenty-three distinct files were hashed before and after this audit and
  remained unchanged: eleven inputs, ten run products, source preflight and
  method review. No source, old freeze or generated product was edited.

## Seven image identities and timing joins

Paths below are under this unit's `run01/`. Native shape/mode and original-map
pixel-hash equality passed for every row. Complete pixel target hashes are in
the frozen source check and original map; this is a fresh check of those targets,
not another inference from the producer's `all_frame_hashes_match` flag.

| Index / file | PNG bytes | PNG container SHA-256 | PTS / exact seconds | New log frame line |
| --- | ---: | --- | --- | ---: |
|255 / `frame-0255.png`|94052|`d9ea1a35f3d12e2e12ab5b60616b776b66416eccde2750bb4a317d4dbff1e712`|17000 /17|2281|
|256 / `frame-0256.png`|94015|`30985d23ff57dd097e6dcf6d4fdc59caf33332defd24df2aec887e983ecb3aae`|17066 /8533/500|2290|
|257 / `frame-0257.png`|93597|`19671c944e4ddd3fe2386dc72331353f077861a367e3947f01344d9fa88bf1ea`|17133 /17133/1000|2296|
|258 / `frame-0258.png`|93612|`4fc10778ab5ca7d94719cf9880c26b6ce5e3f622ce4aca2d1fc3e749c246e571`|17200 /86/5|2302|
|259 / `frame-0259.png`|94174|`68ee1991a33544a8df21cf1fd8a3abc2abf1f8edb95a0d19d22fc925128040cd`|17266 /8633/500|2311|
|260 / `frame-0260.png`|93893|`80ebf6b8978ec40fb4d5b368222837a96a8b762bdd272bbfcc64be744526a751`|17333 /17333/1000|2320|
|261 / `frame-0261.png`|93460|`ac21f287571806c0c6eac666433f307071a97617c3ebcc8cdf3a71b69c296654`|17400 /87/5|2329|

All times use the encoded1/1000-second time base. They are not exposure times
or event-day clocks. The receipt's copied `clock.decoder_log_line` fields refer
to **the old run02 map's log**, not this new stderr. The final column above
comes from a separate parse of the actual new log; differing line positions
do not constitute different clocks or picture indices.

## Diagnostic taxonomy and source context

Independent text parsing counted442 video decoder-frame records in the new
log. The selected seven ordinal/PTS/timebase records agree with the old map;
no corruption warning is associated with one of those seven. This checks all
record counts but does not claim a fresh pixel check of all442 pictures.
Three corruption messages associate through matching decoder context with:

| Ordinal | PTS | New warning line | Following frame line |
| ---: | ---: | ---: | ---: |
|37|2466|383|384|
|55|3666|482|483|
|63|4200|551|552|

There are **four warning-level lines**, not three total warnings: these three
video corruption warnings plus line2, audio stream0:0, `Guessed Channel Layout:
mono`. No `[error]` or `[fatal]` line occurs in this completed log. The audio
layout diagnostic also appears at line2 in the retained old default and
single-thread logs, checked directly (`a75bd8`, exit0). The old strict-stop log
also retains that audio warning and its known later fatal/error termination.
No new audio analysis or hearing inference was made. Producer `corrupt_mentions:3`
is accurate; stdout `warnings_retained:3` must be understood as that narrow
corruption count, not an exhaustive total-warning count.

New log context identifies the same held `Camera3.wmv` ASF input and stream0:1
WMV3 video,720×480,yuv420p,SAR1:1. The three local warning indices match the
earlier source diagnosis. That older visual diagnosis placed their neighborhoods
in countdown imagery; it was not repeated here. Neither local nonwarning status,
reproducible decoding nor byte identity proves no propagated artifact or an
authentic original camera exposure. Diagnostic-only status is retained.

## Failure and repair chronology

My first output-check command `9f3353` passed seven PNG/pixel/clock checks and
the warning ordinal joins, then exited1 because I mistakenly asserted exactly
three **total** severity warnings. Direct inspection `c1b0fb`, exit0, identified
the fourth audio-layout warning. Prior-log inspection `a75bd8` established that
it was already present. The final check distinguishes these categories; it
does not weaken the protocol's three-corruption-message/pixel-identity rule.
No source, producer, receipt or image was changed to obtain the pass.

Root reports the first execution attempt stopped at output-directory creation
on a filesystem permission denial, before FFmpeg, with no run01 directory;
the exact approved retry completed once (`abe1b8`, exit0). This checker did not
execute or witness either command; the saved success receipt and diagnostics
were verified. The method reviewer independently reports twelve synthetic
tests passed after the bounded pre-execution failure-receipt repair. Those
tests were not rerun by this output checker. Static rereading confirms basic
decode metadata now precedes length validation and timeout partial metadata
is retained; the original preflight snapshot remains preserved.

## Pins and limit of reproduction

| Artifact | SHA-256 |
| --- | --- |
|`PROTOCOL.md`|`bb2e8f38e7c0d7aadb3421252a2fe054dfa36d00101403e5250f161df1cba2b0`|
|Final `prepare.py`|`f498addbabe11fec2e4e3e0ced8834a9702f2c1fecd28d5a4e964433e6ebc480`|
|Final `test_prepare.py`|`f1dbd648e5e1fefcda9994a9e818206f33e5cfb6428c5cd96752df3ec55422bb`|
|`source-check.md`, unchanged|`4b702bfd5c4a1210dfc634ade4ad50eae6e08fc3e604bb962754f9db73491766`|
|`method-review.md`|`48353b824eda36f7a5ed145d041a768d1685d0363831c4da12b4e28959d51b64`|
|`run01/start.json`,3605 bytes|`8ae560ba4621fd4219e0fb6a19f71b61410aca08e70b62029ba4ed70ec33dc45`|
|`run01/receipt.json`,9065 bytes|`6e11c42c6c84be3749dc78f9f8840a2b9c7731e77e9fbd1d35207629a641b478`|
|`run01/decode.stderr.local.txt`,632935 bytes|`ced7c23271cb34c5907023ab301a0fcd2b0951500ff2697a771734e9a4011c13`|

The producer reports complete442-frame raw identity,152755200 bytes, SHA
`1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b`.
This audit checks that reported value against the old pinned map and verifies
the seven selected PNG pixel buffers directly. It **does not independently
redecode or rehash the unretained complete raw stream**, certify the decoder,
or infer whether the spot persists. No additional full decode is warranted by
the checks, which found no selected-pixel discrepancy. Root controls admission
to the separate two-reader visual phase under the unchanged protocol.
Only this working output check was added; no matrix, source, human gate, main/
legal file, engine, acquisition, transfer, commit or push changed.
