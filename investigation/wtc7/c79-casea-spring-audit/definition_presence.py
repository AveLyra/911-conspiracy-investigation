#!/usr/bin/env python3
"""Bounded definition-family presence check, never evaluates source programs."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

BASE=Path(__file__).resolve().parent
SOURCE=Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PINS={
 119:('discrete_mass.k.gz',70199,'2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7',508372,7905,'8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
 120:('elem_thick_to-renum.k.gz',23162693,'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59',232959541,4088491,'7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
 121:('wtc7_global_8a_no-conn-matl.k.gz',47520888,'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d',333947423,7196443,'8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf')}

def require(ok,code):
    if not ok:raise ValueError(code)

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def classify(raw):
    s=raw.split(b'$',1)[0].strip().upper()
    if not s.startswith(b'*'):return None
    for family in ('DEFINE_CURVE','DEFINE_TABLE','DEFINE_FUNCTION'):
        prefix=('*'+family).encode()
        if s.startswith(prefix):
            return {'family':family,'exact_base':s==prefix,'keyword_sha256':hashlib.sha256(s).hexdigest()}
    return None

def controls():
    checks=[]
    for label,condition in [
        ('comment_excluded',classify(b'$ *DEFINE_TABLE') is None),
        ('data_excluded',classify(b'1,2,3') is None),
        ('case_insensitive',classify(b' *define_curve ')['exact_base']),
        ('variant_explicit',not classify(b'*DEFINE_CURVE_TITLE')['exact_base']),
        ('table_family',classify(b'*DEFINE_TABLE_2D')['family']=='DEFINE_TABLE'),
        ('function_family',classify(b'*DEFINE_FUNCTION')['family']=='DEFINE_FUNCTION'),
        ('substring_not_key',classify(b'*COMMENT_DEFINE_TABLE') is None),
    ]:require(condition,'control_'+label);checks.append(label)
    return checks

def calculate():
    receipts={};hits=[]
    for src,(name,size,chash,usize,lines,uhash) in PINS.items():
        path=SOURCE/name;require(path.stat().st_size==size and sha(path)==chash,'source_pin_before')
        count=total=0;h=hashlib.sha256()
        with gzip.open(path,'rb') as f:
            while True:
                raw=f.readline(16385)
                if not raw:break
                count+=1;total+=len(raw);require(len(raw)<=16384 and total<=512*1024*1024,'source_cap')
                require(raw.isascii() and b'\0' not in raw,'nonascii_or_NUL');h.update(raw)
                hit=classify(raw)
                if hit:hits.append({'source':src,'line':count,**hit})
        require((total,count,h.hexdigest())==(usize,lines,uhash),'raw_pin')
        require(path.stat().st_size==size and sha(path)==chash,'source_pin_after')
        receipts[str(src)]={'compressed_bytes':size,'compressed_sha256':chash,'uncompressed_bytes':total,
            'lines':count,'uncompressed_sha256':h.hexdigest(),'eof':True,'after_pin':True}
    counts=Counter(r['family'] for r in hits)
    return {'sources':receipts,'hits':hits,'family_counts':{k:counts[k] for k in ('DEFINE_CURVE','DEFINE_TABLE','DEFINE_FUNCTION')},
        'variant_count':sum(not r['exact_base'] for r in hits),
        'limits':'Keyword-family presence only within three pinned streams; no curve-body arithmetic, solver semantics or broader-corpus absence claim.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--controls',action='store_true');p.add_argument('--output');a=p.parse_args()
    tests=controls()
    if a.controls:print(json.dumps({'controls':tests}));return
    require(a.output and re.fullmatch(r'definition-presence[0-9]+\.json',a.output),'output_scope')
    out=BASE/a.output;require(not out.exists(),'output_exists');result=calculate()
    receipt={'status':'PASS','code_sha256':sha(Path(__file__)),'command':sys.argv,'controls':tests,'result':result}
    with out.open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'status':'PASS','output':out.name,'sha256':sha(out),'counts':result['family_counts'],'variants':result['variant_count']}))

if __name__=='__main__':main()
