#!/usr/bin/env python3
"""Read only five declared public ZIP entries; preserve one unchanged PNG."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import platform
import unittest
import zipfile
from PIL import Image

HERE=Path(__file__).resolve().parent
PARENT=Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
PARENT_HASH='c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
IMAGE_HASH='8b782fd8895cb246d6e8248dfc97cca6387f667b9329bda24e9083beac54fb31'
PDF_HASH='8dacd6cbb61b554c21da2cfa6447ebbb3248a06d04a44596b5c31088e5beb411'
MEMBERS=[(38,'The Kit/WTC7-Camera 3/WTC7 Floor Spacing.pdf',32383,PDF_HASH),
         (46,'The Kit/WTC7-Dan Rather/WTC7 CountedWindows.png',2568512,IMAGE_HASH),
         (47,'The Kit/WTC7-Dan Rather/WTC7 Floor Spacing.pdf',32383,PDF_HASH),
         (49,'The Kit/WTC7-Tilted Camera/CountedWindows.png',2568512,IMAGE_HASH),
         (53,'The Kit/WTC7-Tilted Camera/WTC7 Floor Spacing.pdf',32383,PDF_HASH)]


def digest(data):return hashlib.sha256(data).hexdigest()


def read_member(archive,index,name,size,sha):
    entries=archive.infolist()
    if not 0<=index<len(entries):raise ValueError('ordinal')
    entry=entries[index]
    if entry.filename!=name or sum(e.filename==name for e in entries)!=1:raise ValueError('name_identity')
    if entry.is_dir() or entry.flag_bits&1 or entry.file_size!=size or size>3000000:raise ValueError('size_or_type')
    if (entry.external_attr>>16)&0o170000==0o120000:raise ValueError('symlink')
    data=archive.read(entry)
    if len(data)!=size or digest(data)!=sha:raise ValueError('body_identity')
    return data


class Controls(unittest.TestCase):
    def source(self):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z:z.writestr('safe.txt',b'abc')
        return zipfile.ZipFile(io.BytesIO(stream.getvalue()))
    def test_exact(self):
        with self.source() as z:self.assertEqual(read_member(z,0,'safe.txt',3,digest(b'abc')),b'abc')
    def test_index(self):
        with self.source() as z:
            with self.assertRaises(ValueError):read_member(z,1,'safe.txt',3,digest(b'abc'))
    def test_name(self):
        with self.source() as z:
            with self.assertRaises(ValueError):read_member(z,0,'other.txt',3,digest(b'abc'))
    def test_size(self):
        with self.source() as z:
            with self.assertRaises(ValueError):read_member(z,0,'safe.txt',4,digest(b'abc'))
    def test_hash(self):
        with self.source() as z:
            with self.assertRaises(ValueError):read_member(z,0,'safe.txt',3,digest(b'abd'))


def main(out):
    if out not in ['source-docs01','source-docs02']:raise ValueError('output_scope')
    dest=HERE/out
    if dest.exists():raise ValueError('output_exists')
    parent=PARENT.read_bytes()
    if len(parent)!=172774879 or digest(parent)!=PARENT_HASH:raise ValueError('parent_identity')
    bodies={}
    with zipfile.ZipFile(io.BytesIO(parent)) as z:
        for index,name,size,h in MEMBERS:bodies[index]=read_member(z,index,name,size,h)
    if not bodies[38]==bodies[47]==bodies[53] or bodies[46]!=bodies[49]:raise ValueError('duplicate_identity')
    with Image.open(io.BytesIO(bodies[49])) as im:
        im.load();geometry=list(im.size);mode=im.mode;pixel_sha=digest(im.tobytes())
    document_pins={n:digest((HERE/n).read_bytes()) for n in ['PROTOCOL.md','SOURCE-ADDENDUM.md','root-observations.md']}
    dest.mkdir()
    with (dest/'counted-windows.png').open('xb') as stream:stream.write(bodies[49])
    output=(dest/'counted-windows.png').read_bytes()
    if output!=bodies[49]:raise ValueError('output_changed')
    result={'parent_bytes':len(parent),'parent_sha256':PARENT_HASH,'producer_sha256':digest(Path(__file__).read_bytes()),
            'python':platform.python_version(),'declared_document_pins':document_pins,
            'members':[{'index_zero_based':i,'name':n,'bytes':s,'sha256':h} for i,n,s,h in MEMBERS],
            'counted_image':{'png':'counted-windows.png','sha256':digest(output),'geometry':geometry,'mode':mode,'decoded_pixel_sha256':pixel_sha},
            'confirmed_duplicate_groups':[[38,47,53],[46,49]],
            'scope':'body hash/duplicate checks and unchanged source copy; not label or architectural verification'}
    if digest(PARENT.read_bytes())!=PARENT_HASH:raise ValueError('source_changed')
    with (dest/'receipt.json').open('x') as stream:json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')
    print(json.dumps({'status':'pass','members_checked':5,'counted_image':result['counted_image'],'receipt_sha256':digest((dest/'receipt.json').read_bytes())}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--test',action='store_true');p.add_argument('--out');a=p.parse_args()
    if a.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls));raise SystemExit(not result.wasSuccessful())
    main(a.out)
