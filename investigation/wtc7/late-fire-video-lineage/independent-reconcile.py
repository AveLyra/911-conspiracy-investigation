#!/usr/bin/env python3
"""Independent receipt/integer-bin checker. No helper import or image display."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
from PIL import Image

HERE = Path(__file__).resolve().parent
PINS = {'PROTOCOL.md':'f81d1e7e1d8ae914cd62e182cd6f2db642bd60e19737d204f18d3b97d1e70486',
        'selection.json':'e5abd641738cbbb7656f2c4d0f70336725247787d8955637082a44401047fdc0',
        'screen_local.py':'b5048a0a19347861fe8567ffcffd54a69dfb9df284ebb6bc66c503b54723375c',
        'test_screen_local.py':'5988d73bfb93e24546f015983c0070f7e767c831f8330973b03f962731337b74'}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def pin(path):
    h, size = hashlib.sha256(), 0
    with Path(path).open('rb') as stream:
        while block := stream.read(1048576):
            h.update(block)
            size += len(block)
    return {'bytes':size, 'sha256':h.hexdigest()}


def read(path):
    return json.loads(Path(path).read_text())


def bins(text, tick, seconds):
    parsed = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split('|')
        require(len(parts) == 3, 'inventory_field_count')
        fields = dict(p.split('=', 1) for p in parts)
        require(set(fields) == {'pts','width','height'}, 'inventory_names')
        require(all(re.fullmatch('-?[0-9]+', v) for v in fields.values()), 'inventory_integer')
        parsed.append(tuple(int(fields[k]) for k in ('pts','width','height')))
    require(bool(parsed), 'inventory_empty')
    require(all(a[0] < b[0] for a,b in zip(parsed, parsed[1:])), 'pts_order')
    require(len({r[1:] for r in parsed}) == 1 and min(parsed[0][1:]) > 0, 'geometry')
    counts, first = Counter(), {}
    for index, (pts, width, height) in enumerate(parsed):
        key = (pts*tick.numerator)//(tick.denominator*seconds)
        counts[key] += 1
        first.setdefault(key, (index,pts))
    keys = sorted(first)
    plan = [{'sample_index':i, 'bin':k, 'source_frame_index':first[k][0], 'source_pts':first[k][1],
             'source_time_base':str(tick), 'source_seconds_exact':str(Fraction(first[k][1])*tick),
             'bin_start_seconds':k*seconds, 'bin_end_seconds_exclusive':(k+1)*seconds} for i,k in enumerate(keys)]
    coverage = {'decoded_frame_count':len(parsed), 'first_source_pts':parsed[0][0], 'last_source_pts':parsed[-1][0],
                'observed_bin_range':[keys[0],keys[-1]], 'occupied_bin_count':len(keys),
                'empty_bins_within_observed_range':[i for i in range(keys[0],keys[-1]+1) if i not in first],
                'frame_count_per_occupied_bin':[{'bin':k,'frames':counts[k]} for k in keys]}
    return plan, coverage, parsed[0][1:]


def controls():
    text = '\n'.join(f'pts={p}|width=4|height=3' for p in [-1,0,1,4])
    plan,cov,_ = bins(text,Fraction(1),2)
    require([r['bin'] for r in plan] == [-1,0,2], 'control_negative_boundary')
    require([r['source_frame_index'] for r in plan] == [0,1,3], 'control_first')
    require(cov['empty_bins_within_observed_range'] == [1] and sum(r['frames'] for r in cov['frame_count_per_occupied_bin']) == 4, 'control_gap')
    plan,_,_ = bins('pts=5|width=4|height=3\npts=6|width=4|height=3',Fraction(1,3),2)
    require([r['bin'] for r in plan] == [0,1] and plan[0]['source_seconds_exact'] == '5/3', 'control_rational')
    bad = ['pts=0|width=4|height=3\npts=0|width=4|height=3', 'pts=2|width=4|height=3\npts=1|width=4|height=3',
           'pts=0|width=4|height=3\npts=1|width=5|height=3', 'pts=N/A|width=4|height=3',
           'pts=0|width=4|height=3|extra=1', '']
    for value in bad:
        try:
            bins(value,Fraction(1),2)
        except ValueError:
            continue
        raise ValueError('control_expected_refusal')
    return {'positive_groups':4,'negative_fixtures':6,'status':'passed_before_historical_inventory'}


def png(path, dimensions):
    with Image.open(path) as image:
        image.load()
        require(image.mode == 'RGB' and image.size == dimensions, 'png_actual_geometry_mode')


def check_run(name, sources):
    require(bool(re.fullmatch(r'run0[12]-(?:VID-WTC7-00[1-6]|PESKIN-COMPLETE|CAMERA3-KIT-MP4)',name)), 'run_name')
    run, source_id = HERE/name, name.split('-',1)[1]
    folder = run/source_id
    outer, receipt = read(run/'receipt.json'), read(folder/'receipt.json')
    source = sources[source_id]
    expected = {k:source[k] for k in ('bytes','sha256')}
    require(outer['status'] == receipt['status'] == 'completed', 'not_completed')
    require(outer['requested_source_ids'] == [source_id] and outer['selection_source_count'] == 8, 'subset')
    require(len(outer['sources']) == 1 and outer['sources'][0]['source_id'] == source_id and outer['sources'][0]['status'] == 'completed', 'outer_source')
    require(receipt['source'] == source and pin(source['path']) == expected, 'source_configuration_pin')
    for p in [outer['source_pins_before'][source_id],outer['source_pins_after'][source_id],receipt['source_before'],receipt['source_after']]:
        require(p == expected, 'recorded_source_pin')
    require(outer['sources'][0]['receipt'] == pin(folder/'receipt.json'), 'source_receipt_pin')
    for key, current, snapshot in [('protocol_identity','PROTOCOL.md','protocol.snapshot.md'),('selection_identity','selection.json','selection.snapshot.json'),('script_identity','screen_local.py','screen_local.snapshot.py')]:
        require(outer[key] == pin(HERE/current) == pin(run/snapshot), 'control_snapshot_pin')
    for tool in outer['tools'].values():
        require(pin(tool['path']) == {k:tool[k] for k in ('bytes','sha256')}, 'tool_pin')
    references = 0
    for base, record in [(run,outer),(folder,receipt)]:
        for relative, identity in record['products'].items():
            path = (base/relative).resolve()
            require(path.is_relative_to(base.resolve()) and pin(path) == identity, 'product_pin')
            references += 1
        require(all(c['returncode'] == 0 for c in record['commands']), 'command_exit')
    stream = [s for s in receipt['allowlisted_probe']['streams'] if s['codec_type'] == 'video'][0]
    tick = Fraction(stream['time_base'])
    plan, coverage, dimensions = bins((folder/'frame-inventory.stdout').read_text(),tick,source['step_seconds'])
    require(plan == read(folder/'planned-frames.json'), 'independent_plan')
    require(all(receipt['coverage'][k] == v for k,v in coverage.items()), 'independent_coverage')
    require(dimensions == (stream['width'],stream['height']), 'probe_geometry')
    frames = read(folder/'frames.json')
    require(len(frames) == len(plan) == receipt['sample_count'] == outer['sources'][0]['samples'], 'sample_count')
    for row, proposed in zip(frames,plan):
        require(all(row[k] == v for k,v in proposed.items()), 'frame_plan_row')
        require((row['width'],row['height']) == dimensions, 'frame_geometry')
        require(pin(folder/row['png']) == {k:row[k] for k in ('bytes','sha256')}, 'native_pin')
        png(folder/row['png'],dimensions)
    require({p.name for p in (folder/'native').glob('*.png')} == {Path(r['png']).name for r in frames}, 'native_coverage')
    sheets = receipt['overview_sheets']
    require(len(sheets) == (len(frames)+11)//12 == outer['sources'][0]['overview_sheets'], 'overview_count')
    for i,sheet in enumerate(sheets):
        require(sheet['sample_indices'] == list(range(i*12,min((i+1)*12,len(frames)))), 'overview_sample_coverage')
        require(pin(folder/sheet['path']) == {k:sheet[k] for k in ('bytes','sha256')}, 'overview_pin')
        png(folder/sheet['path'],(960,1120))
    require({p.name for p in (folder/'overview').glob('*.png')} == {Path(s['path']).name for s in sheets}, 'overview_coverage')
    for name in ('probe.stderr','frame-inventory.stderr'):
        require(not (folder/name).read_bytes().strip(), 'probe_inventory_diagnostic')
    log = (folder/'decode.stderr').read_text()
    warnings = [line for line in log.splitlines() if re.search(r'\[(?:warning|error|fatal|panic)\]',line)]
    exact = r'(?:\[swscaler @ 0x[0-9a-f]+\]\s*)+\[warning\] No accelerated colorspace conversion found from yuv420p to rgb24\.'
    require(all(re.fullmatch(exact,line.strip()) for line in warnings), 'unreviewed_diagnostic')
    require(receipt['diagnostic_summary'] == {'reviewed_software_colorspace_fallback_notices':len(warnings),'unreviewed_warning_or_error_count':0}, 'diagnostic_disposition')
    shows = []
    for line in log.splitlines():
        if 'Parsed_showinfo_' in line and re.search(r'\bn:\s*\d+',line):
            m = re.search(r'\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:(\S+).*?\bs:(\d+)x(\d+)',line)
            require(m is not None, 'showinfo_format')
            shows.append((int(m[1]),int(m[2]),Fraction(m[3]),int(m[4]),int(m[5])))
    require(len(shows) == len(plan), 'showinfo_count')
    for i,(actual,row) in enumerate(zip(shows,plan)):
        require(actual[:2] == (i,row['source_pts']) and actual[3:] == dimensions, 'showinfo_pts_geometry')
        require(abs(actual[2]-Fraction(row['source_seconds_exact'])) <= Fraction(1,100), 'showinfo_decimal_consistency')
    bases = re.findall(r'config in time_base:\s*(\d+/\d+)',log)
    require(bool(bases) and all(Fraction(b) == tick for b in bases), 'showinfo_timebase')
    require(pin(source['path']) == expected, 'source_changed')
    material = {r['png']:{k:r[k] for k in ('bytes','sha256')} for r in frames}
    material.update({s['path']:{k:s[k] for k in ('bytes','sha256')} for s in sheets})
    return {'run':run.name,'source_id':source_id,'status':'passed','source':expected,'outer_receipt':pin(run/'receipt.json'),
            'source_receipt':pin(folder/'receipt.json'),'inventory':pin(folder/'frame-inventory.stdout'),
            'decoded_frames':coverage['decoded_frame_count'],'samples':len(frames),'sheets':len(sheets),
            'geometry':list(dimensions),'time_base':str(tick),'empty_bins':coverage['empty_bins_within_observed_range'],
            'product_hash_references':references,'fallback_notices':len(warnings),'material_products':material}


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--run',action='append',required=True)
    cli.add_argument('--out',required=True)
    args = cli.parse_args()
    require(bool(re.fullmatch(r'independent-reconciliation-[0-9]{2}\.json',args.out)), 'output_name')
    target = HERE/args.out
    require(not target.exists() and not target.is_symlink(), 'output_exists')
    tested = controls()
    current = {name:pin(HERE/name) for name in PINS}
    require(all(current[name]['sha256'] == value for name,value in PINS.items()), 'control_pin')
    sources = {s['id']:s for s in read(HERE/'selection.json')['sources']}
    results = [check_run(name,sources) for name in args.run]
    require(all(pin(HERE/name) == current[name] for name in PINS), 'control_changed')
    result = {'status':'passed','synthetic_controls':tested,'producer':pin(__file__),'control_pins':current,'runs':results,
              'visual_images_displayed':0,'helper_imported':False,'no_causal_or_historical_clock_inference':True}
    with target.open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True)
        stream.write('\n')
    print(json.dumps({'output':args.out,'receipt':pin(target),'runs':[{k:r[k] for k in ('run','decoded_frames','samples','sheets','product_hash_references','fallback_notices')} for r in results]}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        code = str(error) if isinstance(error,ValueError) and re.fullmatch('[a-z_]+',str(error)) else 'verification_operation_failed'
        print(json.dumps({'status':'failed','code':code}),file=sys.stderr)
        sys.exit(1)
