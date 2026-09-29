# Camera2 inventory refusal: independent diagnosis

2026-09-19. Bounded review of the preserved `run01-VID-WTC7-001` failure and
frozen parser. No new decode, image/reference display, source acquisition or
edit, helper/test/protocol change, or historical extraction occurred here.

## Finding and scope

All **8,042** nonblank inventory lines contain the three required integer
fields followed by exactly one terminal `|`. For example, the complete
allowlisted first record is `pts=0|width=640|height=480|`. Splitting on `|`
creates an empty fourth token; the frozen parser's requirement that every
token contain `=` therefore raises `frame_inventory_malformed` immediately.

The entire selected inventory matches that syntax. It has no leading,
interior or doubled empty token, nonempty unknown field, or other payload.
Both preserved ffprobe commands exited zero; inventory stderr is empty.
This is a parser/serialization mismatch, not an observed missing timestamp,
changed raster or decoder error. Why FFprobe emits the final separator has
not been traced to its source code; a particular omitted-section explanation
would remain a hypothesis.

The inventory pass already decoded and enumerated **8,042 frames**. The failure
preceded the second FFmpeg extraction pass, not all decoding. No planned-frames
file, accepted frames file, source success receipt, decode stdout/stderr,
native image or overview exists in this failed source directory. The created
native/overview directories are empty. No other source run was reviewed here.

The source-level before/after and outer post-failure identities agree:
208,810,910 bytes, SHA-256
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`;
`source_after_matches_pin=true`. These recorded checks establish unchanged
bytes during that attempt. This reviewer did not freshly rehash the MOV.

## Preserved versions

Paths are relative to `run01-VID-WTC7-001/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `failure.json` | 2536 | `5fdf241545d8de32918af90f8ea5a5ac755d71c4703913a37a70f77a46f593a0` |
| `VID-WTC7-001/failure.json` | 3300 | `b332c59bbe0b642bc7a6093c9687c96eb45100a6b6cf8aa5acc9a57f0ba1571b` |
| `VID-WTC7-001/frame-inventory.stdout` | 264274 | `1402a823c8139f18c81b5d866fc0d8e54a5c037e35bb7c58b02d0200714f67d0` |
| `VID-WTC7-001/frame-inventory.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `screen_local.snapshot.py` | 20080 | `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c` |
| `selection.snapshot.json` | 2574 | `e5abd641738cbbb7656f2c4d0f70336725247787d8955637082a44401047fdc0` |
| `protocol.snapshot.md` | 7503 | `f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486` |

Raw inventory and failure products remain unchanged. Only structural counts,
allowlisted integer examples, fixed categories and hashes were printed.

## Narrow follow-up candidate

Recognize exactly one terminal empty token only when there are three nonempty
preceding tokens; then run the unchanged exact-key-set, duplicate-key, integer,
fixed-dimension and increasing-PTS checks. Keep old untrailed syntax. Record
the recognized-terminal-separator count and hash/preserve the unmodified raw
inventory. Reject leading/interior/repeated empty tokens and every unknown
nonempty field. Do not broadly use `rstrip('|')` or remove all empty tokens.
This is a grammar correction, not a decoder-warning whitelist.

An in-memory adapter followed by the frozen parser preserves all numeric
records and produces **135 candidate samples**, two-second bins 0–134, without
internal empty bins. Original PTS run from 0 through 804101 at 1/2997; dimensions
remain 640×480. Selected source indices run from 0 through 8032; the last selected
PTS is 803201. This is a metadata plan, not extracted/accepted image coverage.
Its hypothetical frozen-format `planned-frames.json` serialization is 33523
bytes, SHA-256
`d89223e0196065177cef188b0daabbfea7a569668926733f975b1397803e17ce`.
No plan file was written.

Seventeen in-memory controls passed: three positive syntax/time cases, eleven
syntax refusals, two duplicate/decreasing-PTS refusals and one raster-change
refusal. The original parser's historical-text refusal was also reproduced.
These do not alter the frozen helper's earlier 16-test receipt.

## Reproducible diagnostic command

The initial structural/hashing check and in-memory parser/control commands used
bundled Python 3.12.14 with `-B`. The consolidated equivalent below runs from
the investigation worktree, uses only saved text and synthetic records, and
writes nothing. It preserves the tested narrow adapter explicitly.

<!-- BEGIN DIAGNOSTIC CODE -->
```python
from pathlib import Path
import hashlib, importlib.util, json, re
from fractions import Fraction
run = Path('research/sherlock-wtc7-investigation/late-fire-video-lineage/run01-VID-WTC7-001')
spec = importlib.util.spec_from_file_location('frozen', run/'screen_local.snapshot.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
data = (run/'VID-WTC7-001/frame-inventory.stdout').read_bytes()
assert hashlib.sha256(data).hexdigest() == '1402a823c8139f18c81b5d866fc0d8e54a5c037e35bb7c58b02d0200714f67d0'
raw = data.decode().splitlines(keepends=True)
assert len(raw) == 8042 and all(re.fullmatch(r'pts=-?\d+\|width=\d+\|height=\d+\|\n', x) for x in raw)
def normalize(lines):
    for line in lines:
        text = line.strip()
        if text.endswith('|'):
            parts = text.split('|')
            if len(parts) != 4 or parts[-1] != '' or any(not p for p in parts[:-1]):
                raise m.CheckError('terminal_delimiter_shape')
            text = '|'.join(parts[:-1])
        yield text
def plan(lines):
    return m.frame_plan(lines, Fraction(1,2997), 2, (640,480))
try:
    plan(raw)
except m.CheckError as error:
    assert str(error) == 'frame_inventory_malformed'
else:
    raise AssertionError('Original refusal not reproduced')
rows, coverage = plan(normalize(raw))
assert len(rows) == 135 and coverage['empty_bins_within_observed_range'] == []
serialized = (json.dumps(rows, indent=2, sort_keys=True)+'\n').encode()
assert len(serialized) == 33523
assert hashlib.sha256(serialized).hexdigest() == 'd89223e0196065177cef188b0daabbfea7a569668926733f975b1397803e17ce'
positive = [['pts=0|width=640|height=480'], ['pts=0|width=640|height=480|'],
            [f'pts={p}|width=640|height=480|' for p in (-1,0,5994)]]
for case in positive:
    plan(normalize(case))
bad = ['|pts=0|width=640|height=480|', 'pts=0||width=640|height=480|',
       'pts=0|width=640|height=480||', 'pts=0|width=640|height=480|unknown=7|',
       'pts=0|width=640|unknown=480|', 'pts=0|width=640|width=480|',
       'pts=0|width=640|', 'pts=N/A|width=640|height=480|',
       'pts=0.5|width=640|height=480|', 'pts=0|width=640|height=48.0|',
       'pts=0|width=640|height=480|nonempty']
negative = [[x] for x in bad]
negative += [[f'pts={p}|width=640|height=480|' for p in ps] for ps in ((0,0),(1,0))]
negative += [['pts=0|width=640|height=480|','pts=1|width=639|height=480|']]
for case in negative:
    try:
        plan(normalize(case))
    except m.CheckError:
        pass
    else:
        raise AssertionError('Invalid record accepted')
print({'status':'pass', 'inventory_rows':8042, 'candidate_samples':135,
       'positive_controls':len(positive), 'negative_controls':len(negative)})
```
<!-- END DIAGNOSTIC CODE -->

## Required follow-up and limits

Any implemented correction should be a separately preserved/reviewed helper
revision with targeted positive/negative tests and the full synthetic suite
rerun. Keep the old helper, source selection/protocol and failed run intact;
use a new destination for any fresh historical attempt. Require exact agreement
with this pinned inventory's integer values and candidate plan, followed by
fresh source integrity, actual diagnostics, showinfo/PNG reconciliation and
material derivative repeat checks. Parsing this inventory does not clear a
later decode warning or extraction failure.

No figure correspondence, pulse duration, historical time/absence, physical
cause or other-source status follows. A first attempt to save this memo timed
out in automatic permission review; the file was confirmed absent and the
permitted single retry was used. That timeout was not a finding that the action
was unsafe, a source change or a numerical failure.

## Separate diagnostic: VID-WTC7-006 unsupported Late SEI

2026-09-19 follow-up, restricted to the saved `run01-VID-WTC7-006` receipts,
technical diagnostics, existing plan, file-name counts and frozen reconciliation
code. Prior Camera2 findings above are unchanged. No decode, image display,
helper/warning change, upload, contact or source acquisition occurred.

**Disposition: retain the source as failed/unresolved.** Its offending message
is an H.264 decoder unsupported-feature warning, not the already reviewed
swscaler conversion fallback. The preserved record does not establish whether
unsupported late-SEI handling affects only auxiliary metadata, presentation
semantics or decoded pixels. It therefore cannot presently be reclassified as
harmless stream information or a verified recoverable pixel-processing issue.
The process's zero exit and production of files show that it continued; they
do not establish image or timing fidelity.

### Exact warning classification

The saved decode stderr contains 321 warning-labeled lines and no lines with
error, fatal or panic labels:

| Component and message family | Count | Current disposition |
|---|---:|---|
| `h264`: “Late SEI is not implemented.” followed by the decoder's generic version/update guidance | 154 | Unsupported coded-stream feature; not cleared |
| `h264`: accompanying generic request to upload a sample/contact developers | 154 | Secondary advisory accompanying the same unsupported-feature reports; no external action authorized or taken |
| `swscaler`: the exact previously reviewed yuv420p-to-rgb24 accelerated-conversion-unavailable notice | 13 | Existing software-fallback allowance; not the reason this source failed |

After removing log component/severity prefixes, the complete two repeated
H.264 messages have respectively 182 and 158 characters and SHA-256:

- `ed2a4b15981d1d0df3862ec4b28442350668a4d5d9b61ed6210e9cd829dacbea`
- `8ce11ab2e222a9a8eb19ff11e388e84726476c72d9f50b48867927fd02226f70`

This pins their exact text without republishing the companion's destination
and contact boilerplate. Diagnostic suggestions are untrusted tool output,
not permission to upgrade software or transmit a sample. Counts are warning
occurrences, not 154 independently identified affected frames or exposures.

### Preserved coverage, partial products and integrity

The two source ffprobe commands and second-pass ffmpeg command all exited zero.
Source failure is phase `decode`, category `decode_diagnostic_review`, at the
classifier before the helper's usual showinfo/PNG reconciliation. The inventory
stderr is empty. The preserved inventory records 23,439 decoded frames at
1280×720, H.264/yuv420p, time base 1/15360, PTS 0 through 12000256. Its selected
15-second plan has 53 samples across bins 0–52 with no internal empty bins.

This reviewer independently ran only the frozen `reconcile_showinfo` function
against the already saved stderr and plan. All 53 logged selected-output indices,
integer PTS, display-time consistency, dimensions and filter time base reconcile
with the plan. There are 53 sequentially named partial native PNG files; no PNG
was opened or visually checked here, and no product-integrity/fidelity conclusion
was inferred from their names. There are zero overviews, no `frames.json` and
no source success receipt. This limited timing-log agreement does not clear the
unsupported-feature warnings or convert partial files into accepted screening.

Source before/after and outer post-failure identities agree at 124,393,041 bytes,
SHA-256 `1ea6063dac3847ee01969987bcee66991056d85ad61839ec301fb888a4456d87`;
`source_after_matches_pin=true`. As in the Camera2 diagnosis, these are verified
preserved receipt values; this lane did not freshly reopen/rehash the video.

Paths below are relative to `run01-VID-WTC7-006/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `failure.json` | 2535 | `f52efb16901220f0c95d09af750f21aae3952178ea255060b75566dcc96703f0` |
| `VID-WTC7-006/failure.json` | 8051 | `74e4efea410879b5d4e07fd8666ccb0eeb44811ce5ead54f0452039f1197d163` |
| `VID-WTC7-006/frame-inventory.stdout` | 798659 | `7603bc9031ddc7db8f03bac4bd29a6b0ddbc152bbc6e511099c278da521977e9` |
| `VID-WTC7-006/frame-inventory.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `VID-WTC7-006/planned-frames.json` | 12917 | `97b8d95d68477d7f945dec8e0caa805665b2caca020fadfd504d24058bea52d4` |
| `VID-WTC7-006/decode.stderr` | 86299 | `db2f866d47cc1de2a8636df79f7792731476c3e86d448c89555eebd7ae25ce72` |
| `VID-WTC7-006/decode.stdout` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `screen_local.snapshot.py` | 20080 | `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c` |

### One bounded compatibility follow-up, not a shared whitelist

The Camera2 terminal-separator correction has concrete syntax evidence and
targeted controls; it cannot resolve this different failure. Do not include
Late SEI in the same warning allowance or repeat source 006 merely because the
grammar revision succeeds elsewhere.

For this source, a useful next test needs a new, source-backed hypothesis about
the unsupported payload and a version-pinned compatible decoding route. A
bounded comparison would retain the exact source and selected PTS/raster plan,
identify what handling changed, and compare complete selected raster products
and timing while retaining all diagnostics. A second run with unchanged code,
warning suppression, stripping unspecified metadata or transcoding until the
warning disappears would not answer that question. Any alternate route would
need its own controls and scope declaration; none was run or selected here.
If those prerequisites cannot be met within the chosen follow-up budget, keep
the 006 refusal as an explicit coverage gap and continue other admitted sources
without calling the eight-file screen complete.

The strongest alternative to a damaged-pixel reading is that these unsupported
messages concern data that do not affect the displayed samples. The strongest
objection to calling them harmless is that neither the saved log nor zero exit
establishes what was skipped or its effect. The present evidence selects neither
claim. No inference about fire content, a six-second episode, historical absence
or collapse mechanism follows.

### Checks actually run

Read-only Python 3 here-doc commands counted severity/component families,
hashed and structurally classified the two non-allowlisted messages, read
sanitized integrity/coverage fields and counted existing file names. The
bundled Python 3.12.14 `-B` command imported the frozen snapshot, loaded the
saved plan and called:

```python
frozen.reconcile_showinfo(saved_decode_stderr, saved_plan,
                         Fraction(1, 15360), (1280, 720))
```

It returned without exception for all 53 entries. All diagnostic inspection
commands exited zero. No whole raw log or incidental media metadata was
printed, and no subprocess launched a decoder. The helper's original failure
remains a failure; these checks are narrower additional observations.

## Kit MP4 inventory: same terminal token, mixed with valid v1 records

Read-only check of `run01-CAMERA3-KIT-MP4`, 2026-09-19. Its 443 nonblank
inventory records comprise one first record with exactly one terminal `|`
after the three integer fields, followed by 442 ordinary untrailed records
already valid under v1. No other grammar, unknown field/payload or leading,
interior or repeated empty token exists. No broader correction is needed.

An initial all-lines-trailed checker intentionally stopped at the 442 other
shapes; a second structural check identified all as existing v1 grammar.
Both recorded ffprobe commands exited zero; inventory stderr is empty. All
443 rows retain 720×480 and strictly increasing PTS 0–452608, time base
1/15360. Source-level failure remains `frame_inventory_malformed`. No plan,
decode stderr, native PNG or overview exists; the image directories are empty.
The inventory pass ran, but second-pass PNG extraction did not. No decoding,
viewing or candidate extraction was performed in this diagnostic lane.

Recorded before/after/post-failure source identities agree: 3,996,436 bytes,
SHA-256 `4ecc57a5dd23b56c7ec0368a309889f38fcd762fd4769a580e0e3c6ea379fe98`,
with `source_after_matches_pin=true`; the media was not freshly rehashed here.
Relative to `run01-CAMERA3-KIT-MP4/`, preserved pins are:

- `failure.json`, 2541 bytes: `a9ffca15dd1057b3d450828ac5b6378291c183998b702fc60aaad5014905c3d7`.
- `CAMERA3-KIT-MP4/failure.json`, 3333 bytes: `dfa693fc3ef1fe5c7004a6e3c77d85b69316632c829d20cd2bf602cba332a2ea`.
- `CAMERA3-KIT-MP4/frame-inventory.stdout`, 14066 bytes: `61a54dc649d4a3cb7e7cd9d562a5ad173729534896de5d20fb0892ef8497ceb6`.
- `CAMERA3-KIT-MP4/frame-inventory.stderr`, zero bytes: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `screen_local.snapshot.py`, 20080 bytes: `b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c`.

Include a mixed trailed/untrailed fixture in the revision's tests, keeping all
unknown-field refusals. This clears only the identified grammar question;
downstream decoding remains untested and 006's Late-SEI refusal remains
unresolved. The first attempt to append this section timed out in automatic
permission review without modifying the memo; the permitted retry was used.

## Camera2 v2: grammar passed; audio-layout warning remains refused

2026-09-19. Bounded independent diagnostic of the root agent's preserved
`v2-run01-VID-WTC7-001` attempt. This section does not modify or replace the
earlier v1 finding. No decoder, image viewer, new historical extraction,
source acquisition, warning-policy change or further helper revision was
run in this diagnostic lane. Camera2 remains unadmitted in this unit.

### Exact diagnostic counts and disposition

The entire saved decode stderr has 721 lines. Fourteen are warning-labeled:

| Exact message category | Count | Frozen disposition |
|---|---:|---|
| Audio input (`pcm_s16le`): `Guessed Channel Layout: stereo` | 1 | Not allowlisted; sole offending warning category |
| Exact reviewed swscaler yuv420p-to-rgb24 accelerated-conversion-unavailable notice | 13 | Existing software-fallback allowance |

There are zero error-, fatal- or panic-labeled lines. The single unknown
message, with component/address/severity prefixes removed, is 30 characters,
SHA-256 `ef84a8a0e8494a5ccb3413224fa0688425c2b8e6476a07b4f9117c62dd3dfa2a`.
Each of the other 13 complete warning lines matches the existing exact
allowance, including its component-prefix grammar. The frozen v2 classifier's
`decode_diagnostic_review` refusal was reproduced from the saved log. A
separate in-memory check of only the 13 already-allowed lines returned the
expected count; no filtered historical log or accepted receipt was written.

Thus the foreseen audio-layout guess is the only non-allowlisted warning in
this saved attempt. Its wording and audio-input component identify an audio
layout inference, not a reported video-pixel decoding error. The recorded
command explicitly maps video and excludes audio. These facts are the
strongest alternative to interpreting the refusal as evidence of damaged
video. They do not establish that all video output is faithful, nor authorize
silently changing a diagnostic gate. The observation is narrower than
"the decode is valid" or "the warning is harmless."

### Phase, partial products and recorded integrity

Both source ffprobe commands and the second-pass FFmpeg extraction command
exited zero. Probe and inventory stderr are empty. The source failure is
phase `decode`, category `decode_diagnostic_review`; the outer failure is
phase `sources` with the same category. The guard fired before the helper's
usual showinfo and native-PNG checks.

V2 recognized 8,042 terminal delimiters across 8,042 inventory frames. Raw
inventory bytes equal the preserved v1 inventory. The actual 135-row plan
equals the independently pinned hypothetical plan byte for byte: 33,523
bytes, SHA-256 `d89223e0196065177cef188b0daabbfea7a569668926733f975b1397803e17ce`.
It covers occupied two-second bins 0–134 with no internal empty bins, native
dimensions 640×480 and source time base 1/2997. Inventory PTS range is
0–804101; the last selected source index is 8032, PTS 803201.

Only saved-text reconciliation was additionally run here: the unchanged
snapshot's `reconcile_showinfo` agrees with all 135 planned output indices,
integer PTS, display-time rounding, dimensions and filter time base. There
are 135 sequential partial native PNG filenames, zero overviews, no
`frames.json`, no source success receipt and no outer success receipt.
No PNG was opened, validated, hashed or visually inspected in this lane.
The timing-log check and filename count do not turn these files into admitted
screening products or establish pixel fidelity or repeatability.

Source-level before/after and outer before/post-failure identities all agree:
208,810,910 bytes, SHA-256
`84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`,
with `source_after_matches_pin=true`. These are verified preserved receipt
values; this reviewer did not freshly reopen or rehash the MOV.

Paths below are relative to `v2-run01-VID-WTC7-001/`:

| File | Bytes | SHA-256 |
|---|---:|---|
| `failure.json` | 2724 | `6e36fca8de38de284753145dfc328eca0e5d9c56707c974fab37dbaaaf4fdba2` |
| `VID-WTC7-001/failure.json` | 13944 | `d19a94533d29150a0be32788d1aeeadc9bc9f6bb3091efab4e877a369731fb3a` |
| `VID-WTC7-001/frame-inventory.stdout` | 264274 | `1402a823c8139f18c81b5d866fc0d8e54a5c037e35bb7c58b02d0200714f67d0` |
| `VID-WTC7-001/decode.stderr` | 90022 | `bfbc6d062ab410d64b1c0996a9d9f2ecc9f851b5a566803351ad4d7ffbcff0a5` |
| `VID-WTC7-001/decode.stdout` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `screen_local.snapshot.py` | 20997 | `890963c2104f53813593b4e09da9b3c5892d2461a2a6a415f06f84842b31d8f9` |
| `grammar-followup.snapshot.md` | 2663 | `8c1f26316c6ace3f68fb06881b9eed465827672bb7d7168aa250275ae8efa723` |

Protocol/selection snapshots still match the original pins recorded above.
The original and v2 helper/test files, protocol, selection and declaration
were rehashed without changes. The earlier memo's 17,810-byte prefix, SHA-256
`49ee290e5efa918aa648fb175b096ca6bcabca5ececf8503c66efc294c1e2dab`,
is preserved by this append.

### Checks and limits

Two read-only here-doc commands used bundled Python 3.12.14 with `-B` from
the investigation worktree. They read only the saved JSON/text, counted
existing image filenames, hashed the listed text/control files, classified
all severity-labeled lines, compared recorded source identities, imported
the pinned v2 snapshot and called its diagnostic classifier and:

```python
saved_v2.reconcile_showinfo(saved_decode_stderr, saved_plan,
                           Fraction(1, 2997), (640, 480))
```

Both inspection commands exited zero. No raw log, source path or incidental
media metadata was printed. No browser or external service was used. The
evidence-audit distinction between observed diagnostics, derived timing
agreement and unestablished fidelity is the basis for retaining the refusal.
No additional whitelist, unchanged retry or new helper revision is proposed
within this unit. Any future admission needs a separately justified,
source-backed diagnostic review and its own authorized controls; the current
partial screen must retain Camera2 and source 006 as explicit gaps. This
section does not independently verify the other six sources or establish
historical absence, event duration, physical calibration or causal ranking.
