#!/usr/bin/env python3
"""Read-only pdfminer representation audit; no pixel or curve measurement."""
from __future__ import annotations
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

import pdfminer
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTChar
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFContentParser, PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSEOF, PSKeyword, keyword_name, literal_name
from pdfminer.utils import apply_matrix_pt
from PIL import Image

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf')
SHA = 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4'
IDS = {'Im0':1770, 'Im1':1771, 'Im2':1774, 'Im3':1775, 'Im4':1776,
       'Im5':1777, 'Im6':1778, 'Im7':1779, 'Im8':1780, 'Im9':1781,
       'Im10':1772, 'Im11':1773}
PRIOR_COUNTS = {'BT':10,'Do':12,'ET':10,'Q':14,'TJ':10,'Tc':15,'Td':7,
                'Tf':14,'Tj':8,'Tm':11,'Tw':13,'W':2,'cm':12,'f':3,
                'g':2,'gs':1,'n':2,'q':14,'re':5,'rg':2}


def sha(data): return hashlib.sha256(data).hexdigest()


def pin(p):
    p = Path(p)
    return {'path':str(p), 'bytes':p.stat().st_size, 'sha256':sha(p.read_bytes())}


def require(value, why):
    if not value: raise ValueError(why)


def image_bbox(ctm):
    corners = [apply_matrix_pt(ctm, p) for p in ((0,0),(1,0),(1,1),(0,1))]
    return [min(p[0] for p in corners), min(p[1] for p in corners),
            max(p[0] for p in corners), max(p[1] for p in corners)]


def membership(images):
    require(len(images) == 12, 'image invocation count not twelve')
    require(len({x['name'] for x in images}) == 12, 'duplicate image name')
    require({x['name']:x['object_id'] for x in images} == IDS, 'prior pypdf identities differ')
    for x in images:
        i = int(x['name'][2:])
        require(x['native_dimensions'] == ([741,88] if i < 6 else [745,92]), 'native dimensions differ')


def path_record(path, ctm):
    return {'native_path': [list(p) for p in path], 'ctm':list(ctm),
            'transformed_path': [[p[0], *[list(apply_matrix_pt(ctm, (p[i],p[i+1])))
                for i in range(1,len(p),2)]] for p in path]}


class Recorder(PDFPageAggregator):
    def __init__(self, manager):
        super().__init__(manager)
        self.images = []
        self.paths = []

    def render_image(self, name, stream):
        raw = stream.get_rawdata()
        encoded = stream.get_data()
        with Image.open(io.BytesIO(encoded)) as im:
            require(im.format == 'JPEG', 'terminal codestream is not JPEG')
            header = {'format':im.format, 'mode':im.mode, 'size':list(im.size)}
        dimensions = [int(stream.attrs['Width']),int(stream.attrs['Height'])]
        require(header['size'] == dimensions, 'JPEG header dimensions differ')
        self.images.append({'name':name, 'object_id':stream.objid,
            'native_dimensions':dimensions, 'bits_per_component':int(stream.attrs['BitsPerComponent']),
            'filters':[literal_name(f) for f,p in stream.get_filters()],
            'color_space':str(stream.attrs.get('ColorSpace')),
            'ctm':list(self.ctm), 'unclipped_bbox_points':image_bbox(self.ctm),
            'encoded_jpeg_bytes':len(encoded), 'encoded_jpeg_sha256':sha(encoded),
            'predecipher_raw_bytes':len(raw), 'predecipher_raw_sha256':sha(raw),
            'predecipher_raw_differs_from_jpeg':raw != encoded, 'jpeg_header':header})
        super().render_image(name,stream)

    def paint_path(self, state, stroke, fill, evenodd, path):
        rec = path_record(path,self.ctm)
        rec.update({'stroke':stroke,'fill':fill,'evenodd':evenodd,
                    'line_width':state.linewidth,'dash':state.dash,
                    'stroke_color':state.scolor,'fill_color':state.ncolor})
        self.paths.append(rec)
        super().paint_path(state,stroke,fill,evenodd,path)


class Interpreter(PDFPageInterpreter):
    def __init__(self, manager, device):
        super().__init__(manager,device)
        self.clip_requests = []
        self.unpainted_ends = []
        self.invocations = []

    def do_Do(self,arg):
        name = literal_name(arg)
        reference = self.xobjmap[name]
        obj = resolve1(reference)
        self.invocations.append({'name':name,'object_id':reference.objid,
                                 'subtype':literal_name(obj.attrs['Subtype']),
                                 'ctm':list(self.ctm)})
        require(literal_name(obj.attrs['Subtype']) == 'Image', 'unexpected form or other XObject')
        super().do_Do(arg)

    def do_W(self):
        rec = path_record(self.curpath,self.ctm); rec['rule']='nonzero'
        self.clip_requests.append(rec)
        super().do_W()

    def do_W_a(self):
        rec = path_record(self.curpath,self.ctm); rec['rule']='evenodd'
        self.clip_requests.append(rec)
        super().do_W_a()

    def do_n(self):
        self.unpainted_ends.append(path_record(self.curpath,self.ctm))
        super().do_n()


def chars(layout):
    if isinstance(layout,LTChar): yield layout.get_text()
    for child in getattr(layout,'_objs',[]): yield from chars(child)


def run(out_name):
    require(Path(out_name).name == out_name and out_name not in ('','.','..'), 'out must be one child name')
    out = HERE / out_name
    require(not out.exists() and not out.is_symlink(),'output already exists')
    inputs = [SOURCE,Path(__file__).resolve(),HERE/'PROTOCOL.md',Path(sys.executable),Path(pdfminer.__file__)]
    before = [pin(p) for p in inputs]
    require(before[0]['sha256'] == SHA,'source pin mismatch')
    stderr = io.StringIO(); logger=logging.getLogger('pdfminer'); handler=logging.StreamHandler(stderr)
    logger.addHandler(handler)
    with warnings.catch_warnings(record=True) as captured, contextlib.redirect_stderr(stderr):
        warnings.simplefilter('always')
        with SOURCE.open('rb') as stream:
            document=PDFDocument(PDFParser(stream),password='')
            selected = None
            for number,page in enumerate(PDFPage.create_pages(document),1):
                if number == 76: selected = page; break
            require(selected is not None,'physical page76 missing')
            parser=PDFContentParser(selected.contents); counts=Counter()
            while True:
                try: position,obj=parser.nextobject()
                except PSEOF: break
                if isinstance(obj,PSKeyword): counts[keyword_name(obj)] += 1
            require(dict(counts) == PRIOR_COUNTS,'operator counts differ from prior pypdf')
            manager=PDFResourceManager(caching=True); device=Recorder(manager); interpreter=Interpreter(manager,device)
            interpreter.process_page(selected)
            membership(device.images)
            require(len(interpreter.invocations) == len(device.images),'invocation/device count differs')
            for a,b in zip(interpreter.invocations,device.images):
                require(a['name']==b['name'] and a['object_id']==b['object_id'] and a['ctm']==b['ctm'],'invocation mismatch')
            output = {'status':'pdfminer_representation_verified_against_prior_pypdf_metadata',
                'source_sha256':SHA,'source_encrypted':bool(document.encryption),
                'physical_page':76,'printed_page':25,'mediabox':list(selected.mediabox),
                'cropbox':list(selected.cropbox),'rotate':selected.rotate,
                'operator_counts':dict(sorted(counts.items())), 'image_invocations':device.images,
                'painted_paths':device.paths,'clip_requests':interpreter.clip_requests,
                'unpainted_path_ends':interpreter.unpainted_ends,
                'native_text_characters_in_device_order':''.join(chars(device.get_result())),
                'prior_pypdf_comparison':{'named_object_ids_match':True,'native_dimensions_match':True,
                    'operator_counts_match':True,'prior_metadata_is_in_render_agent_technical_note':True,
                    'jpeg_hash_and_transform_comparison':'not available in earlier pypdf inventory'},
                'runtime':{'python':platform.python_version(),'pdfminer.six':pdfminer.__version__},
                'input_pins_before':before,
                'limitations':['No raster pixels decoded; JPEG header only.',
                    'No graph ordinate, force, displacement, energy, model identity, or curve metric extracted.',
                    'Recorded bounding boxes are unclipped. pdfminer does not apply clipping in its layout interpreter; clipping requests are separately preserved, not silently treated as applied.',
                    'Native text collection preserves PDF glyph device order, not a reading-order assertion.',
                    'Entry-point module/executable pins are not complete runtime dependency closure.',
                    'Independent parser verification is not independent historical evidence.']}
    logger.removeHandler(handler)
    output['stderr']=stderr.getvalue()
    output['warnings']=[{'category':w.category.__name__,'message':str(w.message)} for w in captured]
    output['input_pins_after']=[pin(p) for p in inputs]
    require(output['input_pins_after']==before,'inputs changed during check')
    with out.open('x') as stream: json.dump(output,stream,indent=2,sort_keys=True);stream.write('\n')
    print(json.dumps({'status':output['status'],'images':len(device.images),'painted_paths':len(device.paths),
        'clip_requests':len(interpreter.clip_requests),'unpainted_ends':len(interpreter.unpainted_ends),
        'output':pin(out),'stderr_bytes':len(output['stderr']),'warning_count':len(output['warnings'])}))


class Controls(unittest.TestCase):
    def test_affine_bbox(self):
        self.assertEqual(image_bbox((2,0,0,3,5,7)),[5,7,7,10])
        self.assertEqual(image_bbox((0,2,-3,0,5,7)),[2,7,5,9])

    def test_membership(self):
        x=[{'name':k,'object_id':v,'native_dimensions':[741,88] if int(k[2:])<6 else [745,92]} for k,v in IDS.items()]
        membership(x)
        with self.assertRaises(ValueError): membership(x[:-1])
        with self.assertRaises(ValueError): membership(x[:-1]+[x[0]])
        x[0]['object_id']=-1
        with self.assertRaises(ValueError): membership(x)

    def test_known_sha(self):
        self.assertEqual(sha(b'abc'),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='representation-check01.json');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    if a.self_test:unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:run(a.out)
