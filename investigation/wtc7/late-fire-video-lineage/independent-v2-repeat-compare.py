#!/usr/bin/env python3
"""Read and compare only the two independently admitted v2 kit runs."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def pin(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def main():
    require(pin(b'a') == pin(b'a') and pin(b'a') != pin(b'b'), 'identity_control')
    input_pins, records = {}, []
    for n, expected in [(1,'54564700528a0381761b5d838b6da49db9f30885c73b0797fc41426568273d1b'),
                        (2,'4286f4f9b7d767191c308c8c33aa269a651d4a4fe4d15a9c97fff6e18a365c0a')]:
        name=f'independent-v2-reconciliation-0{n}.json'
        data=(HERE/name).read_bytes()
        require(pin(data)['sha256'] == expected, 'independent_result_pin')
        decoded=json.loads(data)
        require(decoded['status'] == 'passed' and len(decoded['runs']) == 1, 'independent_result_status')
        record=decoded['runs'][0]
        require(record['status'] == 'passed' and record['run'] == f'v2-run0{n}-CAMERA3-KIT-MP4', 'run_identity')
        source_dir=HERE/record['run']/'CAMERA3-KIT-MP4'
        require(pin((source_dir/'receipt.json').read_bytes()) == record['source_receipt'], 'current_source_receipt_pin')
        input_pins[name]=pin(data)
        records.append(record)
    a,b=records
    require(a['source'] == b['source'] and a['material_products'] == b['material_products'], 'material_pin_maps')
    products={}
    for name, expected in a['material_products'].items():
        require(bool(re.fullmatch(r'(?:native/frame-[0-9]+|overview/sheet-[0-9]+)\.png',name)), 'material_path')
        x=(HERE/a['run']/'CAMERA3-KIT-MP4'/name).read_bytes()
        y=(HERE/b['run']/'CAMERA3-KIT-MP4'/name).read_bytes()
        require(x == y and pin(x) == expected, 'material_bytes')
        products[name]=expected
    data_products={}
    for name in ['planned-frames.json','frames.json','frame-inventory.stdout']:
        x=(HERE/a['run']/'CAMERA3-KIT-MP4'/name).read_bytes()
        y=(HERE/b['run']/'CAMERA3-KIT-MP4'/name).read_bytes()
        require(x == y, 'data_product_bytes')
        data_products[name]=pin(x)
    result={'status':'passed','producer':pin(Path(__file__).read_bytes()),'input_results':input_pins,
            'source_id':'CAMERA3-KIT-MP4','native_pngs':a['samples'],'overview_pngs':a['sheets'],
            'material_products':products,'identical_data_products':data_products,
            'whole_receipt_identity_claimed':False,'images_displayed':0}
    target=HERE/'independent-v2-repeat-comparison.json'
    with target.open('x') as output:
        json.dump(result,output,indent=2,sort_keys=True)
        output.write('\n')
    print(json.dumps({'output':target.name,'identity':pin(target.read_bytes()),'native':a['samples'],'overviews':a['sheets'],'data_files':len(data_products),'status':'byte_identical'}))


if __name__ == '__main__':
    main()
