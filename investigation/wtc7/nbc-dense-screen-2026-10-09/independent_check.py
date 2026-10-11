#!/usr/bin/env python3
"""Read-only independent audit of the two declared NBC picture-screen runs.

Preserved from the successful inline checker. Does not import producer code.
Checks derivative identity and bookkeeping, not historical source authenticity.
"""
import hashlib, json, re, zlib
from fractions import Fraction
from pathlib import Path
from PIL import Image
base = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/nbc-dense-screen-2026-10-09')
def pin(path):
    with path.open('rb') as f:
        h = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': h}
def load(path):
    return json.loads(path.read_text())
out = {'runs': {}, 'run_comparison': {}}
for name in ('run01', 'run02'):
    directory = base / name
    receipt = load(directory / 'receipt.json')
    assert receipt['status'] == 'complete', (name, receipt['status'])
    assert receipt['inputs_before'] == receipt['inputs_after']
    for path, expected in receipt['inputs_before'].items():
        assert pin(Path(path)) == expected, (name, 'input pin')
    for path, expected in receipt['binaries'].items():
        assert pin(Path(path)) == expected, (name, 'binary pin')
    for relative, expected in receipt['products'].items():
        assert pin(directory / relative) == expected, (name, 'product pin', relative)
    actual_files = {str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file() and p.name not in ('start.json', 'receipt.json')}
    assert actual_files == set(receipt['products']), (name, 'unlisted product')
    assert all(c['exit_code'] == 0 for c in receipt['commands'])
    results = {'all_product_pins_verified':len(receipt['products']), 'inputs_verified':len(receipt['inputs_before']), 'candidates': {}}
    for label in ('small','large'):
        src = receipt['sources'][label]
        assert src['before'] == src['after'] == pin(Path(src['path']))
        inv = load(directory / (label+'-inventory.stdout'))
        assert len(inv['streams']) == 1
        stream = inv['streams'][0]
        tick = Fraction(stream['time_base'])
        assert tick > 0
        frames = inv['frames']
        assert len(frames) > 0
        assert all(type(f['best_effort_timestamp']) is int and (f['width'],f['height']) == (320,240) for f in frames)
        exact_times = tuple(Fraction(f['best_effort_timestamp'])*tick for f in frames)
        assert all(exact_times[i] < exact_times[i+1] for i in range(len(exact_times)-1))
        if label == 'small':
            expected_indices = list(range(len(frames)))
            bins = None
        else:
            first_per_bin = {}
            for i, t in enumerate(exact_times):
                first_per_bin.setdefault(t.numerator // t.denominator, i)
            expected_indices = list(first_per_bin.values())
            if expected_indices[-1] != len(frames)-1:
                expected_indices += [len(frames)-1]
            bins = len(first_per_bin)
        rows = load(directory / (label+'-selected.json'))
        assert [r['source_index'] for r in rows] == expected_indices, (name,label,'exact selection')
        assert len(rows) == (295 if label == 'small' else 357)
        extraction = next(c for c in receipt['commands'] if c['label']==label+'-extract')
        filter_text=extraction['argv'][extraction['argv'].index('-vf')+1]
        assert [int(x) for x in re.findall(r'eq\(n,(\d+)\)',filter_text)] == expected_indices
        log = (directory / (label+'-extract.stderr.txt')).read_text()
        bases = re.findall(r'config in time_base:\s*(\d+/\d+)',log)
        assert bases and all(Fraction(b)==tick for b in bases)
        show = []
        for line in log.splitlines():
            if 'Parsed_showinfo_' not in line or not re.search(r'\bn:\s*\d+\s+pts:', line):
                continue
            item = {}
            for field in ('n','pts'):
                item[field] = int(re.search(r'\b'+field+r':\s*(-?\d+)',line).group(1))
            item['size'] = tuple(map(int,re.search(r'\bs:(\d+)x(\d+)',line).groups()))
            item['format'] = re.search(r'\bfmt:(\S+)',line).group(1)
            item['checksum'] = int(re.search(r'\bchecksum:([A-Fa-f0-9]+)',line).group(1),16)
            show.append(item)
        assert len(show) == len(expected_indices)
        pngs = sorted((directory / label).glob('*.png'))
        assert len(pngs)==len(rows)
        for slot,(idx,row,item,png) in enumerate(zip(expected_indices,rows,show,pngs,strict=True)):
            assert item['n']==slot and item['pts']==frames[idx]['best_effort_timestamp']
            assert item['size']==(320,240) and item['format']=='rgb24'
            assert row['best_effort_timestamp']==frames[idx]['best_effort_timestamp'] and row['pts']==frames[idx].get('pts')
            assert Fraction(row['time_base'])==tick and Fraction(row['seconds_exact'])==exact_times[idx]
            assert row['png']==str(png.relative_to(directory))
            assert {'bytes':row['bytes'],'sha256':row['sha256']}==pin(png)
            with Image.open(png) as im:
                im.load()
                assert im.mode=='RGB' and im.size==(320,240)
                assert zlib.adler32(im.tobytes(),0)==item['checksum'], (name,label,slot,'showinfo pixel checksum')
                sheet_index, tile = divmod(slot,20)
                x,y=(tile%4)*320,(tile//4)*268
                with Image.open(directory / (label+'-sheets') / ('sheet-%02d.png'%sheet_index)) as sheet:
                    assert sheet.mode=='RGB'
                    assert sheet.crop((x,y,x+320,y+240)).tobytes()==im.tobytes(),(name,label,slot,'sheet raster')
        gap = max((exact_times[b]-exact_times[a] for a,b in zip(expected_indices,expected_indices[1:])),default=Fraction(0))
        assert str(gap)==src['max_selected_gap_seconds']
        assert src['decoded_count']==len(frames) and src['selected_count']==len(rows)
        inventory_diagnostics=(directory / (label+'-inventory.stderr.txt')).read_text().splitlines()
        extracted_diagnostics=[line for line in log.splitlines() if re.search('corrupt|damaged|warning|error|conceal|not available',line,re.I)]
        assert extracted_diagnostics==src['diagnostic_lines']
        results['candidates'][label]={'decoded':len(frames),'selected':len(rows),'occupied_bins':bins,'first_index':expected_indices[0],'last_index':expected_indices[-1],'first_seconds_exact':str(exact_times[expected_indices[0]]),'last_seconds_exact':str(exact_times[expected_indices[-1]]),'max_gap_exact':str(gap),'png_hash_raster_showinfo_pts_sheet_checks':len(rows),'inventory_diagnostic_line_count':len(inventory_diagnostics),'extract_diagnostic_line_count':len(extracted_diagnostics)}
    out['runs'][name]=results
for label in ('small','large'):
    left=load(base/'run01'/(label+'-selected.json'))
    right=load(base/'run02'/(label+'-selected.json'))
    assert left==right
    for row in left:
        assert (base/'run01'/row['png']).read_bytes()==(base/'run02'/row['png']).read_bytes()
    assert load(base/'run01'/(label+'-inventory.stdout'))==load(base/'run02'/(label+'-inventory.stdout'))
    sheets1=sorted((base/'run01'/(label+'-sheets')).glob('*.png'))
    sheets2=sorted((base/'run02'/(label+'-sheets')).glob('*.png'))
    assert len(sheets1)==len(sheets2)
    for a,b in zip(sheets1,sheets2,strict=True):
        assert a.name==b.name and a.read_bytes()==b.read_bytes()
    out['run_comparison'][label]={'complete_inventory_equal':True,'complete_selected_rows_equal':True,'all_png_bytes_equal':len(left),'all_sheet_bytes_equal':len(sheets1)}
print(json.dumps(out,indent=2))
