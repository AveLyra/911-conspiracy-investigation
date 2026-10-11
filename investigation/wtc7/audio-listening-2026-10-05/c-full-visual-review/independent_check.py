"""Preserved reviewer command body; no extraction-helper imports or file writes."""
from pathlib import Path
from fractions import Fraction
import json, hashlib, struct
base=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/audio-listening-2026-10-05/c-full-visual-review/run01')
old=Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/run01')
rows=json.loads((base/'compilation-selected.json').read_text())
fixed=json.loads((base/'fixed-native-selection.json').read_text())
assert len(rows)==750 and [r['source_index'] for r in rows]==list(range(12900,13650))
assert all(Fraction(r['source_seconds_exact'])==Fraction(r['source_index'],30)==r['source_pts']*Fraction(r['source_time_base']) for r in rows)
assert fixed==rows[::30] and [Fraction(r['source_seconds_exact']) for r in fixed]==list(range(430,455))
for r in rows:
 data=(base/r['png']).read_bytes()
 assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
 assert struct.unpack('>II',data[16:24])==(1280,720)
sheets=sorted((base/'compilation-overview').glob('sheet-*.png'))
assert [p.name for p in sheets]==['sheet-%04d.png'%i for i in range(0,750,30)]
assert all(struct.unpack('>II',p.read_bytes()[16:24])==(1600,1248) for p in sheets)
oldrows=json.loads((old/'compilation-selected.json').read_text())
oldmap={r['source_index']:r for r in oldrows if 13020<=r['source_index']<13290}
assert len(oldmap)==270
for r in rows[120:390]:
 prior=oldmap[r['source_index']]
 assert prior['sha256']==r['sha256'] and prior['bytes']==r['bytes']
 assert hashlib.sha256((old/prior['png']).read_bytes()).hexdigest()==r['sha256']
source=Path('/Users/admin/docs/911/research/wtc7-video-comparison/media/compilations/WTC Building 7 Collapse - 27 Angles [cmp7rV2aZhM].f136.mp4')
assert source.stat().st_size==124393041 and hashlib.sha256(source.read_bytes()).hexdigest()=='1ea6063dac3847ee01969987bcee66991056d85ad61839ec301fb888a4456d87'
print(json.dumps({'selection_contiguous_and_exact_times':750,'fixed_integer_second_frames':25,'actual_native_png_hashes_and_geometry':750,'overview_sheets_and_geometry':25,'actual_old_overlap_hashes':270,'current_source_pin':'pass'}))
