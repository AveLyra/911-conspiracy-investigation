# Independent nonvisual method audit

2026-09-19. Research-only review of the declared sparse-frame method and
preserved outputs. No source retrieval, video probing/decoding, visual
interpretation, source edits, producer edits or changes to prior freezes.
Pillow opened already-produced PNGs solely for numerical pixel/geometry checks;
no image was displayed. The reviewer owns only this note.

## Result and admission boundary

The control and historical repeat products reconcile: **2,848 preserved
inventory rows** passed integer-PTS/order and native-geometry checks.
All **56 selected PNG instances** additionally passed selection, rational-time,
per-frame metadata, PNG-byte and RGB-pixel hash checks.
Each comparison pair has identical `frames.json` bytes
and corresponding PNG bytes/pixels. The historical subtotal is **48 PNG
instances / 24 per pass** and **2,598 inventory rows / 1,299 per pass**; the
remaining eight PNGs and 250 rows are the two control-option runs. These are
not counts of independent historical images or cameras.

**Dub6 44 is not admitted.** Both runs retain 829 explicit decode error lines,
including error concealment. Exit zero, complete output, expected dimensions,
stable timestamps and identical repeated pixels do not establish faithful
reconstruction of damaged input. The method review does not reverse root's
exclusion or evaluate any Dub6 image. Dub5 has no warnings/errors in the
inspected probe/decode logs and nine repeat-matching sparse samples; this
supports the limited descriptive workflow, not historical authenticity,
scientific measurement, visual correspondence or the charter's human gate.

## Controls and numerical checks

FRAME-PLAN.md and sample_frames.py were read completely before this audit.
Existing main controls and the unit PROTOCOL remain controlling; the
evidence-falsification/source-of-truth and development-verification skills
were used for provenance, independent checks and bounded negative testing.

The synthetic source is 881,930 bytes, SHA-256
`03faf8b842dbec9ea7358b91f3cb0097a40a1b0719696b698025a4b79599b8c6`.
Both saved probes contain 125 frames. Independently selected indices are
0, 60, 120 and 124; corresponding exact PTS times are 0, 2, 4 and 62/15
seconds, with time base 1/30. All output pixels equal the expected full-frame
red, green, blue and blue RGB triples respectively. Both sets are 96×64 RGB,
SAR 4:3, with interlaced_frame/top_field_first = 0/0. `frames.json`, all four
PNG byte hashes and all four pixel hashes agree between guessing enabled and
disabled. Their receipts are not byte-identical: the option flag and retained
warning differ. Guessing enabled records one “Guessed Channel Layout: stereo”
warning; guessing disabled records none. The creation command/log describe
FFV1/bgr0 AVI plus PCM stereo and 125 encoded frames. This is a finite control
of selection/color and that input option on this source, not a DV-decoder or
historical audio validation.

The saved three negative controls report rejection of wrong hash, wrong count
and existing destination. This reviewer independently reran all three against
the current unchanged helper and control artifacts, then tested missing PTS,
boolean PTS, duplicate PTS, changing width and zero time base in memory.
All eight rejected. The existing-destination test reaches `mkdir` and raises
before any subprocess; no video decoder was invoked. A before/after digest
check around the first negative-test pass found all 15 inspected protected
files unchanged (helper, plan, control-results and 12 files in guess-off).
The exact focused repeat command and outputs are retained below.

Historical rows independently reconcile as follows, in each run:

| Source | Inventory | Selected zero-based indices | Time base | Geometry / SAR / interlace flags |
| --- | ---: | --- | --- | --- |
| Dub5 15 | 475 | 0,60,120,180,240,300,360,420,474 | 6673/200000 | 720×480 / 8:9 / 1,0 |
| Dub6 44, excluded | 824 | 0,60,120,180,240,300,360,420,480,540,600,660,720,780,823 | 333667/10000000 | 720×480 / 8:9 / 1,0 |

For these files each selected PTS integer equals its source index, but exact
seconds use the respective rational time base, not an assumed 30 fps.
Every inventory row had integer, strictly increasing PTS and stream-matching
dimensions. All six selected-row sets match their retained `showinfo` sequence
and time base. The raster is not aspect-corrected or deinterlaced; SAR 8:9 and
interlacing remain interpretation limits. Current historical source byte
counts and hashes match FRAME-PLAN and the previously reviewed acquisition
pins. The helper calls source identity checks before and after sampling; this
audit independently verifies current bytes, not a separately witnessed past
before/after acquisition history.

## Diagnostic accounting and concrete method concerns

All nonempty probe diagnostic lines and all explicit decode severity tags were
traversed, with address-normalized message counts independently reconciled to
the receipt lists. Counts below are per run and concern log messages, not the
number of corrupt frames or affected pixels.

| Output | Probe stderr physical lines | Decode warning lines | Decode error lines | Decode fatal/panic lines |
| --- | ---: | ---: | ---: | ---: |
| Control, guess off | 0 | 0 | 0 | 0 |
| Control, guess on | 0 | 1 | 0 | 0 |
| Dub5 run01 | 0 | 0 | 0 | 0 |
| Dub5 run02 | 0 | 0 | 0 | 0 |
| Dub6 run01 | 580 | 0 | 829 | 0 |
| Dub6 run02 | 580 | 0 | 829 | 0 |

Each Dub6 decode log has 542 explicit “Concealing bitstream errors” lines plus
287 “AC EOB marker is absent” lines. Its probe has 288 explicit concealment
lines, 287 marker lines and five repeat-summary lines (50, 78, 78, 24, 24).
Thus 580 **physical** probe lines expand to 829 reported diagnostic messages
when those 254 repetitions are counted; do not call the 580 lines 580 distinct
errors or infer 829 damaged frames. Decode message totals by kind agree across
runs, but ordering/addresses and whole-log hashes differ. Decode stdout is
empty for all six sample executions. The three retained version pairs identify
FFmpeg/ffprobe 7.1.1, with empty version stderr. The synthetic creation log has
no explicit warning/error/fatal/panic messages.

Concrete limitations:

1. **“automatic_checks: passed” is not diagnostic clearance.** At helper
   lines 113–119, the same pass string is written even when the adjacent list
   contains 829 errors. Its “not visual/human acceptance” qualifier helps, but
   does not explicitly say decode integrity failed or admission is pending.
   Report this as “identity/index/time/dimension/hash checks passed; Dub6
   decoder errors unresolved; excluded.” Keep the original receipt intact.
2. **The receipt's diagnostic summary omits probe stderr.** At lines 71–73
   probe stderr is retained on disk but discarded from the returned local
   variable; lines 113–118 summarize decode stderr only. This caused no hidden
   clearance here because both logs were independently examined and Dub6 is
   excluded. In another input, a probe-only diagnostic could coexist with an
   empty receipt warning list. Empty list must not mean all stages were clean.
3. **Repeatability is not decoder validation.** The two runs use the same
   FFmpeg build and same source bytes. ffprobe and ffmpeg are not independent
   decoder implementations. Deterministic error concealment can reproduce
   identical PNGs twice. The lossless FFV1 control does not test malformed DV.
4. **The diagnostic summary is a literal three-tag filter.** The helper
   captures warning/error/fatal tags, not every possible diagnostic format or
   panic tag. No panic-tag message was found in these logs. Full log review,
   not only that list, is required by the plan.
5. **Sparse sampling and stored metadata have bounded meaning.** Nine or
   fifteen selected indices cannot test absence or duration of an intervening
   event, prove uninterrupted wide/zoom continuity, or authenticate a camera
   clock. RGB output involves display color conversion; interlaced pixels and
   non-square SAR remain uncorrected. No photometric/geometric measurement is
   accepted by this review.

The strongest alternative to treating the repeated Dub6 images as reliable
is reproducible decoder concealment of the same damaged bitstream. The logs
affirmatively support that concern, not merely a speculative possibility.
The current logs do not attribute corruption to original recording, later
dubbing/encoding, storage, transfer or deliberate action; no such attribution
is made. A separately authorized source-integrity investigation or alternative
provenance-backed source would be needed. No repair, diagnostic suppression,
new decode or retroactive admission is proposed as already accomplished.

## Verification commands and scope

Executed locally from
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/late-fire-catalog-join`:

- `cat FRAME-PLAN.md sample_frames.py`: full read; exit 0.
- `cat`/`jq` reads of control results, six receipts, both control frame lists,
  and exact creation/probe/decode command arrays; exit 0.
- `shasum -a 256 FRAME-PLAN.md sample_frames.py control01/control-results.json`:
  pins below; exit 0.
- Independent read-only Python/Pillow traversal of all six probes, frame JSONs,
  PNGs, receipts and probe/decode stderr logs: exit 0. Selection was computed
  with a separate increment-by-60 loop plus final index; producer `indices`
  or `sample` was not imported for this verification. Checked every inventory
  row's PTS/order and dimensions, then every selected-output row's rational
  time, PTS, dimensions, SAR/interlace fields, file name, PNG SHA-256 and RGB
  SHA-256, plus expected control pixels, retained showinfo PTS and time base,
  code/plan pins, and current source identity. Result: 56 PNG instances, 2,848
  inventory rows, all three material-product comparison pairs equal.
- Separate read-only negative-test pass imported the existing helper with
  Python `-B`, tested the eight cases above, checked 15 protected file hashes
  before/after, and printed version/log/command hashes: exit 0. Only calls
  guaranteed to fail before creating outputs or invoking a subprocess were
  made to `sample`; other tests use in-memory JSON or read-only identity.
- A final read-only Python comparison of exact saved command arrays exited 0:
  both historical repeat probe commands are identical; each historical decode
  pair differs only in its output destination. Both historical command sets
  have video-only mapping, no autorotation/autoscaling, RGB24 and passthrough
  flags. Control decode commands differ only in the guessing option and output
  destination; control probe commands are identical.

The following exact focused repeat of the eight negative checks also exited 0
(the earlier pass additionally checked the 15 unchanged hashes):

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B - <<'PY'
from pathlib import Path
import copy,importlib.util,json
b=Path.cwd();s=importlib.util.spec_from_file_location('audit_target',b/'sample_frames.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
p=b/'control01/guess-off';r=json.loads((p/'receipt.json').read_text());d=json.loads((p/'probe.stdout').read_text());source=Path(r['source'])
def changed(key,value):
    z=copy.deepcopy(d)
    if key=='missing':del z['frames'][0]['pts']
    elif key=='time_base':z['streams'][0]['time_base']=value
    else:z['frames'][1][key]=value
    return z
cases=[('wrong-hash',lambda:m.identity(source,'0'*64,r['source_bytes'])),('wrong-count',lambda:m.inventory(d,124)),('existing-destination',lambda:m.sample(source,r['source_sha256'],r['source_bytes'],125,p))]
for label,key,value in [('missing-PTS','missing',None),('boolean-PTS','pts',True),('duplicate-PTS','pts',0),('changing-geometry','width',97),('zero-time-base','time_base','0/30')]:
    cases.append((label,lambda key=key,value=value:m.inventory(changed(key,value),125)))
for label,action in cases:
    try:action()
    except (AssertionError,FileExistsError) as e:print(label,type(e).__name__)
    else:raise RuntimeError('not rejected: '+label)
PY
```

Actual output:

```text
wrong-hash AssertionError
wrong-count AssertionError
existing-destination FileExistsError
missing-PTS AssertionError
boolean-PTS AssertionError
duplicate-PTS AssertionError
changing-geometry AssertionError
zero-time-base AssertionError
```

The assertion-based helper must not be invoked with optimization that disables
Python assertions. This review used ordinary `python3 -B`, not `-O`, and does
not test an optimized invocation. `run_command` checks return codes before
continuing, but its command JSON files do not independently record numeric
exit status; this reviewer did not rerun the historical decodes or witness
their original execution. The preserved successful receipts, logs, inspected
code and root's execution record are the scope of that historical-run check.

This is another AI agent's independent numerical traversal of shared artifacts,
not a human or independent-source review. No root/observer visual notes, report
figure images, image sheets or new scene interpretations were used. No final
visual admission, model ranking or scientific causal inference follows.

## Version and output pins

Current SHA-256 values independently computed in this review:

| Record | SHA-256 |
| --- | --- |
| FRAME-PLAN.md | `c5bc934477182bd6d9f85f893f9a57517090c5a3aa1d0492724f625cab9964af` |
| sample_frames.py | `bd4267da1f80cb565322caa67a0ab8b8e5de181e31eaf0b68e4505e8a4258a68` |
| control01/control-results.json | `c9bc3b648b341bea141ecfd2582adbb1e2c5d98a44d94d8b5e5d51348b9b8238` |
| Both control frames.json | `51efd3f8802d6b093e6b8c912129e8b79c77c6cce4d5b0455a1fb8b9927e8086` |
| Both Dub5 frames.json | `441eb21ecf567a8d4f7791a21445b6001ca3b3add09f63829c56f4202964b988` |
| Both Dub6 frames.json | `a00c56c4005fb8ce847fdd82cbbc99b54abb674e0d113ca787c8e4ab174e2df3` |
| control guess-off receipt.json | `666c80186d164b64d60bfdc04ca5ea4da46260a511aab0fb27e40a8428b52337` |
| control guess-on receipt.json | `f297db3a12ef24e694965f8aa8f57393a09a71f3767ebb902101f625ca2568a3` |
| Both Dub5 receipt.json | `0b47df31206e9daeff601d9c56de9bcb86c71e7f67749738a57e21327d68f359` |
| run01 Dub6 receipt.json | `69db5f09f480579ad9a8dc88239106497cc1ebfad9db70e27097599780aa1f2c` |
| run02 Dub6 receipt.json | `c83f180242e33444c3744a315fe0ce163d2c9c80b163a11d99a5c1d848e10ea8` |
| Both control probe.stdout | `2a12143980b41697efe7798044e7ec7a5eb47f694d0d8a0a3710805ea393e3e0` |
| Both Dub5 probe.stdout | `9278d5d193d2a5910f15d34ff7e1b1db92109be8e7dca957424ca786f32f453e` |
| Both Dub6 probe.stdout | `361df46e42dcaf36a7b0f7eb2bb1226516c6c1e5f7993a7d6951ddd0f88a1f28` |
| run01 Dub6 decode.stderr | `014ec988ba72a2392ee2427d11b7c27ae5a5b13b32acf1f12054f2c4b3a371b9` |
| run02 Dub6 decode.stderr | `4da430488d00928c89c194aca8d2a94afc1affb9676e3fa4994df661a54b1877` |
| run01 Dub6 probe.stderr | `f19e2e015029b43221152dc2e9ae7e060a2f9d8c9d732e8e9ce298a9afa05b69` |
| run02 Dub6 probe.stderr | `324219e08f9478b868cd6b96fbe5a05851c4bddbaff2ba358c260d84151d49a7` |

Per-PNG and RGB hashes are retained in the pinned frame JSONs and were all
recomputed, not merely compared between receipts. The source AVI hashes are
the exact ones in FRAME-PLAN and `independent-source-review.md`; both current
files matched those pins. Whole command/log/receipt identity is not claimed
across runs: output paths, memory addresses and message ordering can differ.
Matching source and product hashes do not make the two runs independent
historical evidence.
