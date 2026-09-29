# Fixed Camera2 source and presentation verification

2026-09-24. Independent numerical/source check under this unit's `PROTOCOL.md`,
not an appearance or historical-continuity review. No root/observer annotation
file or historical image was visually inspected by this verifier. The existing
PNGs were decoded as arrays for exact representation checks only; there was no
new video decode, frame extraction, image generation, crop export, point
selection, or motion calculation.

**Result:** all 17 fixed native PNGs, their native luma hashes, exact PTS joins,
and all image-region samples of the 17 existing panels pass the checks below.
The saved synthetic coordinate-control image and its panel also match the
declared formula and mapping at every checked sample. No current input or
product mismatch was found. These checks do not validate the observers'
feature identities or establish uninterrupted historical continuity.

## Exact source coverage

The verified native files are main
`research/sherlock-wtc7-investigation/multiview-onset-review/refine01/camera2/fNNNNNN.png`.
All seventeen panels were available in the investigation worktree under
`camera2-target-trackability/present01/fNNNNNN-target-panel.png`; no fallback
to a main panel was needed. Exact absolute paths and separate byte/pixel hashes
for every item are in `verification.json`.

Each native image is **640×480, PNG mode L**. Each panel is **665×983, RGB**.
The selected indices exactly match the 17-member protocol list, in order, and
are a subset of the previously declared 71-member event selection. The parent
selection and parent extraction receipt both name and pin these native PNGs;
the presentation detail repeats the same 17 complete selection rows.

| Frame, zero based | Saved PTS | Exact saved seconds | Physical CSV line including header |
|---:|---:|---|---:|
| 6593 | 659301 | 219767/999 | 6595 |
| 6654 | 665404 | 665404/2997 | 6656 |
| 6751 | 675100 | 675100/2997 | 6753 |
| 6841 | 684101 | 684101/2997 | 6843 |
| 6886 | 688601 | 688601/2997 | 6888 |
| 6916 | 691603 | 691603/2997 | 6918 |
| 6931 | 693102 | 231034/999 | 6933 |
| 6946 | 694600 | 694600/2997 | 6948 |
| 6961 | 696104 | 696104/2997 | 6963 |
| 6976 | 697602 | 232534/999 | 6978 |
| 6991 | 699101 | 699101/2997 | 6993 |
| 7006 | 700604 | 700604/2997 | 7008 |
| 7021 | 702103 | 702103/2997 | 7023 |
| 7036 | 703601 | 703601/2997 | 7038 |
| 7051 | 705100 | 705100/2997 | 7053 |
| 7081 | 708102 | 8742/37 | 7083 |
| 7104 | 710404 | 710404/2997 | 7106 |

The time base is **1/2997 for every selected row**. Exact rational equality
`seconds = PTS × time_base` passes, and the selected times increase strictly.
The check retained the actual PTS; it did not replace it with `100 × index`,
an assumed constant frame rate, rounded decimal times, or a historical clock.

The 8,042 saved CSV rows and 8,042 saved `frames.json` entries agree with the
parent's checked-frame count. A supplemental read-only command checked all
8,042 CSV index fields are contiguous zero-based indices; thus the table's
physical-line locator is actually verified, not merely assumed. For each of
the 17 selected rows, PTS and best-effort timestamp also match `frames.json`.

## Pixel and coordinate-display checks

The reading-aid mapping is the exclusive source crop `[270,95,475,400)`, scale
3, with its top-left pixel at panel `(40,28)`. The tested panel image region
is `[40,28,655,943)`, or 615×915 pixels. For every panel sample, the independent
check recovered its source index by integer division:

```text
source_x = 270 + floor((panel_x - 40) / 3)
source_y = 95  + floor((panel_y - 28) / 3)
```

Every RGB component equals the corresponding native grayscale value:
**28,698,975 channel samples across all 17 panels, zero differences**.
This checks every 3×3 replicated block, not a corner-only spot check. Each
panel's 21 x-tick and 30 y-tick anchor samples were also checked black at
their declared exterior positions. Labels or feature marks have not altered
any image-region sample. Glyph wording, font appearance, and optical
legibility were not independently rendered or OCR-validated here; the entire
panel files match the saved product hashes.

The saved `controls02` synthetic source has the pixel formula
`(x % 256, y % 256, x // 256 + 4*(y // 256))`. All **921,600** source channel
samples agree with that formula. All **1,688,175** channel samples in its
panel image region agree with the inverse-index mapping; the same 21/30 tick
anchors pass. This is a check of an already-saved control, not generation of
a new synthetic image, historical tracker execution, or accuracy calibration.

## Duplicate information and source-level limits

- The 17 native luma hashes are all distinct: no selected-to-selected exact
  luma duplicate was found.
- For every selected index, the saved decoded-YUV hash differs from the
  immediately preceding index's saved hash. The corresponding saved
  `identical_to_previous_decoded_frame` field is false and consistent in the
  selection and frame map. This is a **map-level check**, not new YUV decoding.
- These statements do not inspect every intervening image or exclude repeats,
  blended exposures, dropped frames, edits, or near-duplicates between samples.
  The sparse list cannot demonstrate uninterrupted tracking or first loss.
- The source MOV's current 208,810,910 bytes match SHA-256
  `84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730`.
  The source-identity record calls it a secondary-hosted, explicitly converted
  analysis copy, not an authenticated native/complete broadcast master.
- The preserved earlier decode record reports exit 0 and 8,042 checked
  frames, with one classified stereo audio-layout-guess line and zero
  unclassified diagnostic lines. This verifier did not rerun that decoder or
  read its local-only log, and does not erase the recorded warning.

## Pins, verification scope, and execution

`verification.json` SHA-256:
`88cdf8b9a22c987e4caf624e3335981e0a087f8647901dc1aeeaafaab0237688`.
It preserves **59** before/after-checked input identities, including the MOV,
maps, selected native PNGs, panel/control products, source code snapshots,
protocols, and receipts. All **22** `present01` product pins and all **6**
`controls02` product pins match. The main and worktree `present01/receipt.json`
copies are byte-identical. The record distinguishes a copy from independent
corroboration; no source and derivative counts are added as evidence samples.

Key receipt/source pins:

| Artifact | SHA-256 |
|---|---|
| Camera2 source selection | `dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e` |
| Parent refinement declaration | `700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a` |
| Parent refine01 receipt | `c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503` |
| present01 receipt | `7ca7abe5bc9d67511213a627a5ae65b1e506952b88896f780779d5fbf7c63f29` |
| controls02 receipt | `f68a4213b08271407b617c40101d549c00e132410a1af41bbc6875d1f248e0a4` |

The verifier used bundled Python **3.12.14**, NumPy **2.3.5**, and Pillow
**12.3.0**. It did not import the presentation producer. Its channel-wise
coordinate formula and inverse index mapping differ from the producer's
crop/resize and repeated-array comparison, while sharing Pillow for PNG
decoding. This is implementation independence within stated common-library
limits, not independent capture provenance.

The initial assertion-based command, run with the bundled executable and
`-B -`, exited 0 and created only the sanitized `verification.json` with
exclusive-create mode. A second read-only command verified CSV line locators.
No assertion failed in either. Initial broad metadata printing was truncated
by the tool; the actual programmatic checks read the complete selected JSON/
CSV files and all product pins. Truncated output was not treated as a complete
manual review of the other cameras or all historical frames.

## Read-only replay

The following complete replay checks the saved output pins, source joins, all
panel pixels, and synthetic samples without writing any image, code, or data
file. Run using the absolute bundled executable:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -
```

Supply this Python block on standard input:

```python
from pathlib import Path
from fractions import Fraction
import csv, hashlib, json
import numpy as np
from PIL import Image
M=Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
W=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation')
U=W/'camera2-lower-feature-continuity'
vpath=U/'verification.json'
assert hashlib.sha256(vpath.read_bytes()).hexdigest()=='88cdf8b9a22c987e4caf624e3335981e0a087f8647901dc1aeeaafaab0237688'
v=json.loads(vpath.read_text())
def pin(p):
 with p.open('rb') as f:return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(f,'sha256').hexdigest()}
for p,expected in v['input_pins'].items():assert pin(Path(p))==expected
F=[6593,6654,6751,6841,6886,6916,6931,6946,6961,6976,6991,7006,7021,7036,7051,7081,7104]
assert v['fixed_frames']==F and [x['frame'] for x in v['checks']]==F
selection=json.loads((M/'multiview-onset-review/refine01/camera2/selection.json').read_text())
rows=[x for x in selection['images'] if int(x['frame_index_zero_based']) in F]
assert [int(x['frame_index_zero_based']) for x in rows]==F
T=M/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001'
with (T/'frame-map.csv').open(newline='') as f:maps=list(csv.DictReader(f))
meta=json.loads((T/'frames.json').read_text())['frames']
assert len(maps)==len(meta)==8042
assert all(int(x['frame_index_zero_based'])==i for i,x in enumerate(maps))
sy=95+np.arange(915)//3; sx=270+np.arange(615)//3
luma=[]; compared=0
for r,x in zip(rows,v['checks']):
 i=x['frame']; assert r['png']==f'f{i:06d}.png'
 for key in ('source_pts','source_time_base','source_time_seconds_exact','best_effort_timestamp','decoded_sha256','identical_to_previous_decoded_frame'):
  assert r[key]==maps[i][key]
 assert int(r['source_pts'])==meta[i]['pts']
 assert int(r['best_effort_timestamp'])==meta[i]['best_effort_timestamp']
 assert Fraction(r['source_time_seconds_exact'])==int(r['source_pts'])*Fraction(r['source_time_base'])
 assert x['map_row_1_based_including_header']==i+2
 assert (maps[i]['decoded_sha256']==maps[i-1]['decoded_sha256'])==x['equal_to_previous_decoded_frame_per_map']
 with Image.open(x['native_path']) as im:
  im.load(); assert im.mode=='L' and im.size==(640,480)
  a=np.asarray(im); digest=hashlib.sha256(im.tobytes()).hexdigest()
  assert digest==r['luma_sha256']==x['native_luma_sha256']; luma.append(digest)
 with Image.open(x['panel_path']) as im:
  im.load(); assert im.mode=='RGB' and im.size==(665,983)
  b=np.asarray(im); assert hashlib.sha256(im.tobytes()).hexdigest()==x['panel_rgb_sha256']
 actual=b[28:943,40:655,:]; expected=a[sy[:,None],sx[None,:]]
 assert np.all(actual==expected[:,:,None]); compared+=actual.size
 assert all(np.all(b[26,40+(q-270)*3,:]==0) for q in range(270,475,10))
 assert all(np.all(b[28+(q-95)*3,38,:]==0) for q in range(100,400,10))
assert len(set(luma))==17 and compared==28698975
C=Path(v['synthetic_control']['path'])
with Image.open(C/'synthetic-source.png') as im:
 im.load(); assert im.mode=='RGB' and im.size==(640,480); s=np.asarray(im)
 yy,xx=np.indices((480,640))
 assert np.array_equal(s[:,:,0],xx%256)
 assert np.array_equal(s[:,:,1],yy%256)
 assert np.array_equal(s[:,:,2],xx//256+4*(yy//256))
with Image.open(C/'synthetic-panel.png') as im:
 im.load(); assert im.mode=='RGB' and im.size==(665,983); b=np.asarray(im)
 assert np.array_equal(b[28:943,40:655,:],s[sy[:,None],sx[None,:],:])
 assert all(np.all(b[26,40+(q-270)*3,:]==0) for q in range(270,475,10))
 assert all(np.all(b[28+(q-95)*3,38,:]==0) for q in range(100,400,10))
for p,expected in v['input_pins'].items():assert pin(Path(p))==expected
print('PASS: 17 selected frames, exact PTS joins, 28698975 historical panel channel samples, saved synthetic source/panel, 59 unchanged pins')
```

The saved Python block above was then read directly from this Markdown and
executed using the bundled interpreter with `-B`, exit 0. It printed exactly
the stated PASS line. No code was imported from the producer, and this replay
wrote no files. It reproduces the representation check rather than creating
a second historical observation.

Passing representation checks cannot be relabeled an accuracy percentage,
human-review acceptance, historical motion estimate, physical calibration,
cause ranking, or an authentication of the original recording clock.
