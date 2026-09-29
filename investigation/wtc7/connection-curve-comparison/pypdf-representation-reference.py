#!/usr/bin/env python3
"""Separate pypdf metadata baseline, produced after pdfminer result freeze."""
import argparse
from collections import Counter
import contextlib
import hashlib
import io
import json
import logging
from pathlib import Path
import platform
import sys
import unittest
import warnings

import pypdf
from pypdf import PdfReader
from pypdf.generic import ContentStream

HERE=Path(__file__).resolve().parent
SOURCE=Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
SOURCE_SHA='cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
INDEPENDENT=HERE/'representation-check01.json'
INDEPENDENT_SHA='517d657d206e6ac5b955be53bde63d5fecd9bc7b6fa05c971d6e88d7f111834b'
TOLERANCE=1e-9


def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,why):
    if not ok:raise ValueError(why)
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}


def compose(current,added):
    a,b,c,d,e,f=current;g,h,i,j,k,l=added
    return (a*g+c*h,b*g+d*h,a*i+c*j,b*i+d*j,a*k+c*l+e,b*k+d*l+f)


def bbox(m):
    a,b,c,d,e,f=m
    xs=[e,a+e,a+c+e,c+e];ys=[f,b+f,b+d+f,d+f]
    return [min(xs),min(ys),max(xs),max(ys)]


def fresh(name):
    require(name not in ('','.','..') and Path(name).name==name,'single child output name required')
    p=HERE/name
    require(not p.exists() and not p.is_symlink(),'output exists')
    return p


def write(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')


def run(out_name,comparison_name):
    out=fresh(out_name);comparison=fresh(comparison_name)
    require(out!=comparison,'two distinct outputs required')
    inputs=[SOURCE,INDEPENDENT,HERE/'representation-check.py',Path(__file__).resolve(),
            HERE/'PROTOCOL.md',Path(sys.executable),Path(pypdf.__file__)]
    before=[pin(p) for p in inputs]
    require(before[0]['sha256']==SOURCE_SHA,'source hash mismatch')
    require(before[1]['sha256']==INDEPENDENT_SHA,'independent result not frozen version')
    capture=io.StringIO();logger=logging.getLogger('pypdf');handler=logging.StreamHandler(capture);logger.addHandler(handler)
    with warnings.catch_warnings(record=True) as caught,contextlib.redirect_stderr(capture):
        warnings.simplefilter('always')
        reader=PdfReader(SOURCE)
        if reader.is_encrypted:reader.decrypt('')
        page=reader.pages[75]
        require(list(map(float,page.mediabox))==[0,0,612,792] and int(page.get('/Rotate',0))==0,'unsupported page transform')
        operations=ContentStream(page.get_contents(),reader).operations
        ctm=(1,0,0,1,0,0);stack=[];images=[]
        counts=Counter(op.decode('latin1') for operands,op in operations)
        resources=page['/Resources']['/XObject']
        for operands,op in operations:
            if op==b'q':stack.append(ctm)
            elif op==b'Q':
                require(bool(stack),'unbalanced Q');ctm=stack.pop()
            elif op==b'cm':ctm=compose(ctm,tuple(map(float,operands)))
            elif op==b'Do':
                name=operands[0];ref=resources.raw_get(name);obj=ref.get_object()
                require(str(obj['/Subtype'])=='/Image','unexpected non-image XObject')
                encoded=obj.get_data()
                images.append({'name':str(name).lstrip('/'),'object_id':ref.idnum,'generation':ref.generation,
                    'native_dimensions':[int(obj['/Width']),int(obj['/Height'])],
                    'bits_per_component':int(obj['/BitsPerComponent']), 'filter':str(obj['/Filter']),
                    'ctm':list(ctm),'unclipped_bbox_points':bbox(ctm),
                    'encoded_jpeg_bytes':len(encoded),'encoded_jpeg_sha256':sha(encoded)})
        require(not stack,'unbalanced q')
    logger.removeHandler(handler)
    after=[pin(p) for p in inputs];require(before==after,'input changed')
    baseline={'status':'pypdf_reference_only','physical_page':76,'source_sha256':SOURCE_SHA,
        'source_encrypted':reader.is_encrypted,'image_invocations':images,'operator_counts':dict(sorted(counts.items())),
        'runtime':{'python':platform.python_version(),'pypdf':pypdf.__version__},
        'stderr':capture.getvalue(),'warnings':[{'category':w.category.__name__,'message':str(w.message)} for w in caught],
        'input_pins_before':before,'input_pins_after':after,
        'limits':['No pixel decode, image assembly, resampling, ordinate extraction, or series identification.',
            'Image boxes are unclipped, matching the independent receipt convention.',
            'This baseline was generated only after the pdfminer receipt had been saved and hash frozen.',
            'Source image codestream bytes are decrypted JPEG representation, not solver arrays.']}
    write(out,baseline)
    # Comparison begins after the independent result and this baseline both exist.
    independent=json.loads(INDEPENDENT.read_text())
    by_name={x['name']:x for x in independent['image_invocations']}
    require(len(images)==len(by_name)==12,'membership count mismatch')
    require(set(by_name)=={x['name'] for x in images},'image name mismatch')
    rows=[]
    for x in images:
        other=by_name[x['name']]
        for field in ('object_id','native_dimensions','bits_per_component','encoded_jpeg_bytes','encoded_jpeg_sha256'):
            require(x[field]==other[field],field+' differs: '+x['name'])
        ctm_residual=max(abs(a-b) for a,b in zip(x['ctm'],other['ctm']))
        box_residual=max(abs(a-b) for a,b in zip(x['unclipped_bbox_points'],other['unclipped_bbox_points']))
        require(ctm_residual<=TOLERANCE and box_residual<=TOLERANCE,'placement mismatch')
        rows.append({'name':x['name'],'object_id':x['object_id'],'jpeg_bytes_hash_and_dimensions_match':True,
                     'max_ctm_residual_points':ctm_residual,'max_bbox_residual_points':box_residual})
    require(baseline['operator_counts']==independent['operator_counts'],'operator count mismatch')
    require([pin(p) for p in inputs]==before,'input changed before comparison completion')
    result={'status':'cross_parser_representation_match','independent_receipt':pin(INDEPENDENT),
        'pypdf_reference_receipt':pin(out),'comparison_code':pin(Path(__file__).resolve()),
        'physical_page':76,'source_sha256':SOURCE_SHA,'tolerance_points':TOLERANCE,
        'operator_counts_match':True,'checks':rows,
        'limits':['Independent PDF parser confirmation does not establish physical model accuracy or independent historical evidence.',
            'No clipped-support equality claimed; clip requests are preserved in pdfminer receipt.']}
    write(comparison,result)
    print(json.dumps({'reference':pin(out),'comparison':pin(comparison),'images':len(images),
        'max_ctm_residual_points':max(x['max_ctm_residual_points'] for x in rows),
        'max_bbox_residual_points':max(x['max_bbox_residual_points'] for x in rows),
        'stderr_bytes':len(baseline['stderr']),'warning_count':len(baseline['warnings'])}))


class Controls(unittest.TestCase):
    def test_matrix_composition_order(self):
        self.assertEqual(compose((2,0,0,3,5,7),(1,0,0,1,2,4)),(2,0,0,3,9,19))
        self.assertEqual(compose((1,0,0,1,2,4),(2,0,0,3,5,7)),(2,0,0,3,7,11))
    def test_rotated_bbox(self):self.assertEqual(bbox((0,2,-3,0,5,7)),[2,7,5,9])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='pypdf-representation01.json');p.add_argument('--comparison-out',default='representation-comparison01.json');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:run(a.out,a.comparison_out)
