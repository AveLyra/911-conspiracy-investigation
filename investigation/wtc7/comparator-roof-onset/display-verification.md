# Independent display verification

September 20, 2026 UTC. Working research only; bounded derivative/layout check
under the existing investigation charter, [PROTOCOL.md](PROTOCOL.md) and
[FEATURES.md](FEATURES.md). This is separate from the frozen
[independent extraction verification](independent-verification.md).

**PASS for the current display01/display02 bytes and the declared navigation
layout.** All nine sheet pairs are byte-identical. All 18 complete decoded RGB
sheet rasters exactly match the independent in-memory composition described
below. All 242 source-frame pairs, complete selected maps, display receipts and
source/extraction pins reconcile. No correction to the current display outputs
is required by this check.

No historical image was displayed, no observer selection or observation
findings were read, and no historical source decoder was invoked. The PNGs
were decoded numerically in memory only. No producer module/function was
imported or called by the verification program. Only this new note was written;
the frozen independent-verification.md was not edited.

## Scope and implementation reading

The current main controls/full charter and relevant evidence-audit,
source-preservation and development-verification instructions were read for
this bounded unit. The complete FEATURES.md and make_display.py were read,
along with the exact inherited helper's sheets function and installed Pillow
thumbnail implementation. Their role here is to preserve the declared display
contract and distinguish a successful derivative check from scientific or
historical acceptance.

The current make_display.py routes display01 to run02 and display02 to run03.
It refuses an existing output directory, requires the exact ordered source
indices 239–480 and checks each selected PNG's byte count/hash before creating
the display directory. Absolute source PNG paths passed to the helper resolve
to those admitted inputs. The helper resizes the entire source raster and
places it above its own source-index/time label; it does not crop the source.

The existing-directory refusal was inspected, **not re-executed** in this
display check. The helper has no per-cell independent visual detector, and the
display receipt is not a general future-run admission mechanism. Current
method/code/input identities and complete output membership were checked
externally here.

## Actual numerical checks

A single independent inline Python program (exact recipe below) returned
exit0 with these results:

- Both complete extraction selected maps have exactly 242 rows, whole-source
  indices 239–480 in order, mapped one-to-one onto output ordinals
  comparator/frame-0001.png through frame-0242.png. These namespaces remain
  distinct.
- All 242 encoded PNG pairs are exactly equal; all 484 mapped PNG byte
  count/hash records agree with the final extraction receipts. The complete
  selected JSON maps are byte-identical.
- Both final extraction receipts retain their previously frozen hashes,
  status complete and 364 products each. All 728 product identities were
  rehashed, and actual file membership reconciles to each receipt plus
  start.json/receipt.json. Source media, extraction script, protocol,
  dependencies, FFmpeg/ffprobe and Python executable identities agree with
  their recorded before/after pins.
- The two display receipts are themselves byte-identical. Each declares
  exactly the nine expected sheets, the current frozen feature plan and
  producer/helper pins, the admitted source-map pin, all 242 ordered indices,
  and Pillow12.0.0. All 18 listed sheet identities and exact directory
  membership agree.
- Each unique admitted source image is single-frame RGB1280×720. An expected
  full-frame 320×180 thumbnail was reconstructed using explicit
  Pillow BICUBIC, box=None and reducing_gap=2.0. This is the installed
  thumbnail method's actual default path for these dimensions/PNG inputs;
  it includes downsampling, not a native-pixel or nearest-neighbor display.
- The oracle assembled white RGB sheets without calling the producer or
  inherited sheets function: five columns, 320×208 cells, thumbnail at the
  cell origin and the black default-font label at x+3,y+182.
- All 242 labels per display were independently formed from the exact
  rational clock using Decimal six-place rounding. They agree with the
  producer's float formatting. Each row's source_pts × source_time_base
  equals source_seconds_exact, and the float field equals its float
  conversion. PTS are source_index × 1001, with time base1/30000 in this
  particular retained set. Six displayed decimals are a navigation format,
  not six-decimal physical-time precision.
- Every RGB byte of each saved sheet matches its expected full layout,
  including labels, padding, and the three unused cells on the last sheet.
  All outputs are single-frame RGB PNGs of the expected dimensions.
- All 761 captured paths were rehashed again after the comparisons and
  remained unchanged, including source media, receipts, code/method pins,
  source PNGs, maps, output sheets and the frozen prior verification note.

This is 242 unique thumbnail reconstructions and 18 complete output-raster
comparisons, not 484 independently reconstructed source images. Equality of
the paired native PNG bytes extends the run02 reconstruction to run03.

## Coverage and complete-sheet pins

Paths below are within both display01/comparator-overview and
display02/comparator-overview. Each pair has the same byte count and SHA-256.

| Sheet | Whole-source indices | Frames | Raster | Bytes | SHA-256 |
|---|---|---:|---|---:|---|
| sheet-0000.png | 239–268 | 30 | 1600×1248 | 820160 | afb0a92138969e6ba137fd626f5f35adf1f5cefebdd9b86a74b80ad6b705588f |
| sheet-0030.png | 269–298 | 30 | 1600×1248 | 721429 | ebc4481b642119276f087f420671abc7af3e286b137319524b55c96c16c43a93 |
| sheet-0060.png | 299–328 | 30 | 1600×1248 | 693429 | 59734ebe0a98c4321e845b3ea4795c2c1db8aa029150399ba9e3f9bba95989f1 |
| sheet-0090.png | 329–358 | 30 | 1600×1248 | 765310 | 22421663be4c6d748bcb7bbf9d19f7e046dca69c04535a16bdeb294ab1c0d958 |
| sheet-0120.png | 359–388 | 30 | 1600×1248 | 727623 | 8324fc98f34d38035685c78c122b7823d7beb8ae472a8c406bf9f5dfbaa70a48 |
| sheet-0150.png | 389–418 | 30 | 1600×1248 | 1076892 | 9d2c423a2df52066dfa2984f5853a75952a3214ef2554645760978a7f43711db |
| sheet-0180.png | 419–448 | 30 | 1600×1248 | 1453221 | 76f7c94e384c53a0c72cc12bdd512ed57d3f986aaf0e78fc10f0f8ebe4f1fc07 |
| sheet-0210.png | 449–478 | 30 | 1600×1248 | 1564140 | c325ebfb13757320920a3d8c652516ff1b9309e9365546a561d2e9c9b9966f81 |
| sheet-0240.png | 479–480 | 2 | 1600×208 | 132724 | 9dbec5d9e7afab3771b5b65bcdef3f8da53ec10b23c22afff3d33b49dea55a21 |

There are eight 30-frame sheets and one two-frame sheet: 242, not 270,
source-frame occurrences per display. Pairing the two sets does not create
additional independent historical evidence.

The first label is `#239  t=7.974633s`; the final two are
`#479  t=15.982633s` and `#480  t=16.016000s`.
The [8,16) selection and its immediate boundary frames retain the meaning
established in the extraction record; sheet offsets 0000,0030,…,0240 are
output-group offsets, not source indices or physical event times.

## Receipt and unchanged authority pins

| File/input | Bytes where relevant | SHA-256 |
|---|---:|---|
| FEATURES.md | 6836 | bfee24a125a8358d076ef0cd78f23958764385762e8802ae8be1ec77c88289d7 |
| make_display.py | 1835 | eca487f93797ae675bc7376789e90f9a2ee2386f8d985446bd50ee3a02300694 |
| Both display receipt.json files | 4235 each | f74edbde4b8a440f99dcce2cf0f9e1d2ca9ecd5a81508d495475741c7d2c76ea |
| Both comparator-selected.json maps | 98723 each | 14c72246559d79812c1eef4b42d977c64d1f28bc97d0f034a945cddb8db5561a |
| run02/receipt.json | 70641 | e17b37b98c136ba81c79c70ccd03f4b709b127507fd5c6111c5b217b2a14856c |
| run03/receipt.json | 70641 | e7f2303079ad3810ccab88d403eb548a71b05db9bdb5f4e595e043bfdfcd4f28 |
| extract_window.py | 10415 | e316e1fd6e76cdd770e7ec7637491ea7b552d3a9c475a5c38d5d37552538c726 |
| PROTOCOL.md | 6240 | 1d1d1993a6d9a27f66037d5abef449ffe685e7238c20a81a9b85f97ae240883c |
| Main A/V extract_frames.py helper | 11356 | 2fc45bb67ba656c3670fea188f2b71261a9ca315718aaf92e16010ef4bcceb6a |
| Main Peskin sample_every_second.py dependency | 9351 | a913be680052ceb61ddf1ed89ef675c9d21972f8869a62e9e038be2f8048d40b |
| Historical MP4, exact path in recipe/receipt | 4901052 | 8560cd686a18c8fcc16fe802691e0f17f117c713b4cd1862017af24d391ce5a2 |
| Frozen independent-verification.md | 29861 | 2c6f7515fbc46091cb5f68bb3e83167fabb8436dd04fb1a10efe6b7939c6c338 |

## Rendering and evidential limits

All 242 native PNGs decoded here carry aspect, chromaticity and gamma metadata
keys; the 18 sheets have an empty Pillow info dictionary. The sheets therefore
do **not** preserve native PNG rendering metadata. This matches the helper's
construction of a new RGB sheet and is disclosed, not silently treated as a
metadata-free source or an equal color-managed viewing appearance.

Stored RGB values and the prescribed spatial mapping are verified.
Color-managed viewer interpretation, final on-screen size, readability and
visual feature recognition were not independently checked here. No color,
brightness or photometric inference is supported. Thumbnails remain
navigation-only: 4:1 linear reduction loses local detail, and a small feature's
apparent absence cannot become a reliable negative. The declared native-frame
and uncertainty rules remain necessary.

The independent assembly avoids reusing the producer's composition loop,
but deliberately uses the **same installed Pillow12.0.0 rasterizer/font
family** to test that declared layout exactly. It is not an independent
resampling implementation or comprehensive environment/build attestation.

The prior source-decoder/synthetic/diagnostic controls were **not rerun**.
Their previous results and retained colorspace-fallback notices remain in
independent-verification.md; rehashing their products does not constitute
re-executing those checks or making the logs warning-free. This note does not
assess observers' display counts, native refinement choices, feature identity,
placement envelopes, event findings or agreement. It establishes no source
authenticity, real-world timing, physical motion, causal conclusion, legal
fact or new canonical record.

## Actual command and reproducible check

Read-only context/schema inspection used sed/rg on the named method/helper
files, jq on the two display/final extraction receipts, and inspect.getsource
on PIL.Image.Image.thumbnail. The check below ran from the research worktree,
with bytecode writes disabled. It writes no files, imports no producer code,
does not invoke FFmpeg, and prints only validation counts/pins/clock labels.
All PNG decoding uses the already captured bytes that were hashed.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B - <<'PY'
import hashlib, io, json, sys
from pathlib import Path
from fractions import Fraction
from decimal import Decimal
from collections import Counter
from PIL import Image, ImageDraw
N = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/comparator-roof-onset')
MAIN = Path('/Users/admin/docs/911')
HELPER = MAIN/'research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/extract_frames.py'
assert sys.flags.optimize == 0 and Image.__version__ == '12.0.0'
seen = {}
def identity(data):
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()}
def capture(path, expected=None):
    path = Path(path)
    data = path.read_bytes()
    got = identity(data)
    if expected is not None:
        assert got == expected, (str(path), got, expected)
    if path in seen:
        assert got == seen[path], ('changed during check',str(path))
    seen[path] = got
    return data
def pinned(path, sha):
    data = capture(path)
    assert identity(data)['sha256'] == sha, str(path)
    return data
def obj(path, expected=None):
    return json.loads(capture(path, expected))
pins = {
    N/'FEATURES.md':'bfee24a125a8358d076ef0cd78f23958764385762e8802ae8be1ec77c88289d7',
    N/'make_display.py':'eca487f93797ae675bc7376789e90f9a2ee2386f8d985446bd50ee3a02300694',
    N/'independent-verification.md':'2c6f7515fbc46091cb5f68bb3e83167fabb8436dd04fb1a10efe6b7939c6c338',
    N/'extract_window.py':'e316e1fd6e76cdd770e7ec7637491ea7b552d3a9c475a5c38d5d37552538c726',
    N/'PROTOCOL.md':'1d1d1993a6d9a27f66037d5abef449ffe685e7238c20a81a9b85f97ae240883c',
    HELPER:'2fc45bb67ba656c3670fea188f2b71261a9ca315718aaf92e16010ef4bcceb6a',
    MAIN/'research/sherlock-wtc7-investigation/fire-originals/peskin/sample_every_second.py':'a913be680052ceb61ddf1ed89ef675c9d21972f8869a62e9e038be2f8048d40b',
    N/'run02/receipt.json':'e17b37b98c136ba81c79c70ccd03f4b709b127507fd5c6111c5b217b2a14856c',
    N/'run03/receipt.json':'e7f2303079ad3810ccab88d403eb548a71b05db9bdb5f4e595e043bfdfcd4f28',
}
for path, pin in pins.items():
    pinned(path, pin)
indices = list(range(239,481))
relative_sheets = [f'comparator-overview/sheet-{i:04d}.png' for i in range(0,242,30)]
run_receipts, maps, display_receipts = {}, {}, {}
product_checks = 0
for run_name, display_name in [('run02','display01'),('run03','display02')]:
    run = N/run_name
    display = N/display_name
    r = obj(run/'receipt.json')
    assert r['status'] == 'complete' and r['historical_frames'] == 242
    assert r['source_before'] == r['source_after']
    capture(r['source_path'],r['source_before'])
    assert r['script'] == r['script_after'] == seen[N/'extract_window.py']
    assert r['dependencies'] == r['dependencies_after']
    assert r['binaries'] == r['binaries_after']
    for group in ['dependencies','binaries']:
        for path, item in r[group].items():
            capture(path,item)
    assert r['python_executable'] == r['python_executable_after']
    capture(sys.executable,r['python_executable'])
    assert r['pillow'] == Image.__version__
    assert len(r['products']) == 364
    actual = {str(p.relative_to(run)) for p in run.rglob('*') if p.is_file()}
    assert actual == set(r['products']) | {'start.json','receipt.json'}
    for rel,item in r['products'].items():
        capture(run/rel,item)
        product_checks += 1
    rows = obj(run/'comparator-selected.json',r['products']['comparator-selected.json'])
    assert [row['source_index'] for row in rows] == indices
    assert [row['png'] for row in rows] == [f'comparator/frame-{i:04d}.png' for i in range(1,243)]
    for row in rows:
        assert {k:row[k] for k in ['bytes','sha256']} == r['products'][row['png']]
        exact = Fraction(row['source_pts']) * Fraction(row['source_time_base'])
        assert row['source_time_base'] == '1/30000'
        assert row['source_pts'] == row['source_index']*1001
        assert Fraction(row['source_seconds_exact']) == exact
        assert row['source_seconds'] == float(exact)
        exact_label = format(Decimal(exact.numerator)/Decimal(exact.denominator),'.6f')
        assert format(row['source_seconds'],'.6f') == exact_label
    d = obj(display/'receipt.json')
    assert d['feature_plan'] == seen[N/'FEATURES.md']
    assert d['script'] == seen[N/'make_display.py']
    assert d['helper'] == seen[HELPER]
    assert d['pillow'] == Image.__version__
    assert d['source_map'] == seen[run/'comparator-selected.json']
    assert d['source_indices'] == indices
    assert set(d['products']) == set(relative_sheets)
    actual = {str(p.relative_to(display)) for p in display.rglob('*') if p.is_file()}
    assert actual == set(relative_sheets) | {'receipt.json'}
    for rel,item in d['products'].items():
        capture(display/rel,item)
    run_receipts[run_name],maps[run_name],display_receipts[display_name] = r,rows,d
assert capture(N/'run02/comparator-selected.json') == capture(N/'run03/comparator-selected.json')
assert capture(N/'display01/receipt.json') == capture(N/'display02/receipt.json')
for a,b in zip(maps['run02'],maps['run03']):
    assert a == b
    assert capture(N/'run02'/a['png']) == capture(N/'run03'/b['png'])
sheet_results = []
source_info_keys = Counter()
for start in range(0,242,30):
    group = maps['run02'][start:start+30]
    size = (1600,208*((len(group)+4)//5))
    expected = Image.new('RGB',size,'white')
    draw = ImageDraw.Draw(expected)
    labels = []
    for j,row in enumerate(group):
        source_bytes = capture(N/'run02'/row['png'])
        with Image.open(io.BytesIO(source_bytes)) as im:
            assert im.format == 'PNG' and im.mode == 'RGB' and im.size == (1280,720)
            assert im.n_frames == 1
            source_info_keys.update(im.info.keys())
            im.load()
            # Full extent: no crop/box; explicit pinned Pillow thumbnail defaults.
            small = im.resize((320,180),Image.Resampling.BICUBIC,box=None,reducing_gap=2.0)
        x,y = (j%5)*320,(j//5)*208
        expected.paste(small,(x,y))
        t = Fraction(row['source_seconds_exact'])
        seconds = format(Decimal(t.numerator)/Decimal(t.denominator),'.6f')
        label = f"#{row['source_index']}  t={seconds}s"
        labels.append(label)
        draw.text((x+3,y+182),label,fill='black')
    rel = f'comparator-overview/sheet-{start:04d}.png'
    pair = []
    for display_name in ['display01','display02']:
        data = capture(N/display_name/rel)
        pair.append(data)
        with Image.open(io.BytesIO(data)) as actual:
            assert actual.format == 'PNG' and actual.mode == 'RGB' and actual.n_frames == 1
            assert actual.size == size and actual.info == {}
            actual.load()
            assert actual.tobytes() == expected.tobytes(), ('full raster mismatch',display_name,rel)
    assert pair[0] == pair[1],('encoded pair mismatch',rel)
    sheet_results.append({'sheet':rel,'source_indices':[group[0]['source_index'],group[-1]['source_index']],
                          'count':len(group),'size':list(size),'first_label':labels[0],
                          'last_label':labels[-1],**identity(pair[0])})
# Rehash every captured path, including receipts, source media, all run products,
# producer/method pins and output sheets, after comparisons.
for path,before in seen.items():
    assert identity(path.read_bytes()) == before, ('changed before final pass',str(path))
result = {
    'status':'PASS', 'historical_source_decode_invoked':False,'images_displayed':0,
    'producer_imported':False,'pillow':Image.__version__,
    'run_products_rehashed':product_checks,'source_png_pairs_exact':242,
    'full_source_thumbnails_reconstructed':242,'sheet_pairs_encoded_exact':9,
    'whole_sheet_rgb_exact':18,'display_product_pins_checked':18,
    'source_map_pair_exact':True,'display_receipt_pair_exact':True,
    'source_indices_per_display':[239,480],'labels_per_display':242,
    'source_png_info_key_counts':dict(source_info_keys),'captured_paths_rehashed_after':len(seen),
    'display_receipt':seen[N/'display01/receipt.json'],
    'source_map':seen[N/'run02/comparator-selected.json'],
    'feature_plan':seen[N/'FEATURES.md'],'display_script':seen[N/'make_display.py'],
    'frozen_verification_unchanged':seen[N/'independent-verification.md'],
    'sheets':sheet_results,
}
print(json.dumps(result,sort_keys=True,indent=2))
PY
```

