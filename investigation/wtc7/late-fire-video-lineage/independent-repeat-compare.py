#!/usr/bin/env python3
"""Compare admitted repeat products, not path-bearing full receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def identity(data):
    return {'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result', action='append', required=True)
    parser.add_argument('--id', action='append', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    require(identity(b'a') != identity(b'b') and identity(b'a') == identity(b'a'), 'synthetic_identity_control')
    runs, inputs = {}, {}
    for name in args.result:
        require(bool(re.fullmatch(r'independent-reconciliation-[0-9]{2}\.json',name)), 'result_name')
        data = (HERE/name).read_bytes()
        record = json.loads(data)
        require(record['status'] == 'passed', 'result_not_passed')
        inputs[name] = identity(data)
        for run in record['runs']:
            require(run['status'] == 'passed' and run['run'] not in runs, 'run_state_or_duplicate')
            runs[run['run']] = run
    output = []
    for source_id in args.id:
        require(bool(re.fullmatch(r'VID-WTC7-00[1-6]|PESKIN-COMPLETE|CAMERA3-KIT-MP4',source_id)), 'source_id')
        a, b = (runs[f'run0{n}-{source_id}'] for n in [1,2])
        require(a['source'] == b['source'] and a['material_products'] == b['material_products'], 'recorded_material_disagreement')
        material = {}
        for name, expected in a['material_products'].items():
            require(bool(re.fullmatch(r'(?:native/frame-[0-9]+|overview/sheet-[0-9]+)\.png',name)), 'material_name')
            left = (HERE/a['run']/source_id/name).read_bytes()
            right = (HERE/b['run']/source_id/name).read_bytes()
            require(left == right and identity(left) == expected, 'current_material_disagreement')
            material[name] = expected
        tables = {}
        for name in ['planned-frames.json','frames.json','frame-inventory.stdout']:
            left = (HERE/a['run']/source_id/name).read_bytes()
            right = (HERE/b['run']/source_id/name).read_bytes()
            require(left == right, 'plan_frame_inventory_disagreement')
            tables[name] = identity(left)
        output.append({'source_id':source_id,'native':a['samples'],'overviews':a['sheets'],
                       'material_products':material,'identical_data_products':tables,'status':'byte_identical'})
    require(bool(re.fullmatch(r'independent-repeat-comparison-[0-9]{2}\.json',args.out)), 'output_name')
    result = {'status':'passed','producer':identity(Path(__file__).read_bytes()),'input_results':inputs,
              'comparisons':output,'whole_receipt_identity_claimed':False,'images_displayed':0}
    with (HERE/args.out).open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True)
        stream.write('\n')
    print(json.dumps({'output':args.out,'identity':identity((HERE/args.out).read_bytes()),
                      'comparisons':[{k:c[k] for k in ['source_id','native','overviews','status']} for c in output]}))


if __name__ == '__main__':
    main()
