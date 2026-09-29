#!/usr/bin/env python3
"""Declared image-content diagnostic, not motion/calibration or exposure authentication."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import unittest
import numpy as np
from PIL import Image, __version__ as pillow_version

HERE=Path(__file__).resolve().parent
REGIONS={'full':[32,16,632,464], 'left_foreground':[40,270,300,460],
         'right_background':[500,160,630,320], 'target_smoke':[280,70,480,320]}
BRANCHES={'nearest':Image.Resampling.NEAREST, 'bilinear':Image.Resampling.BILINEAR, 'box':Image.Resampling.BOX}
QUERIES=[0,67,135,203,271,339,407,475]


def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def require(ok,message):
    if not ok: raise ValueError(message)


def mask(rect):
    x0,y0,x1,y1=rect; y,x=np.mgrid[0:480:4,0:640:4]
    return (x>=x0)&(x<x1)&(y>=y0)&(y<y1)


def metrics(candidates,query):
    c=np.asarray(candidates,dtype=np.float64); q=np.asarray(query,dtype=np.float64)
    require(c.ndim==2 and q.ndim==1 and c.shape[1]==len(q) and len(q)>0,'array shape')
    require(np.isfinite(c).all() and np.isfinite(q).all(),'nonfinite input')
    mae=np.abs(c-q).mean(axis=1)
    cm=c-c.mean(axis=1,keepdims=True); qm=q-q.mean()
    denom=np.sqrt(np.sum(cm*cm,axis=1)*np.dot(qm,qm))
    corr=np.divide(cm@qm,denom,out=np.full(len(c),np.nan),where=denom>0)
    return mae,corr


def choose(mae,ids):
    require(len(mae)==len(ids) and len(ids)>=2 and len(set(ids))==len(ids),'candidate identities')
    require(np.isfinite(mae).all(),'nonfinite MAE')
    order=sorted(range(len(ids)),key=lambda i:(float(mae[i]),ids[i]))
    a,b=order[:2]
    return {'candidate_index':ids[a], 'mae':float(mae[a]), 'runner_up_index':ids[b],
            'runner_up_mae':float(mae[b]), 'gap':float(mae[b]-mae[a]),
            'exact_minimum_ties':[ids[i] for i in order if mae[i]==mae[a]],
            'at_candidate_boundary':ids[a] in (min(ids),max(ids))}


def nullable(values): return [float(v) if np.isfinite(v) else None for v in values]


def run(out_name):
    require(bool(re.fullmatch(r'[a-z][a-z0-9_-]*',out_name)),'unsafe output name')
    out=HERE/out_name; require(not out.exists(),'output exists')
    cdir=HERE/'candidates01'; qdir=HERE/'views01'
    cdoc=json.loads((cdir/'selection.json').read_text()); qdoc=json.loads((qdir/'receipt.json').read_text())
    require(cdoc['checked_frames']==8042 and cdoc['geometry']==[640,480],'candidate source contract')
    cr=cdoc['images']; qr=qdoc['selected']
    ids=[int(r['frame_index_zero_based']) for r in cr]
    require(ids==list(range(6500,7201)),'candidate membership')
    require([r['index'] for r in qr]==QUERIES and qdoc['geometry']==[720,480],'query membership')
    paths=[HERE/'PROTOCOL.md',HERE/'SCENE-ADDENDUM.md',Path(__file__),cdir/'selection.json',
           cdir/'receipt.json',qdir/'receipt.json']
    pins={str(p.relative_to(HERE)):sha(p) for p in paths}
    candidates=[]
    for r in cr:
        path=cdir/r['png']; h=sha(path)
        require(h==r['png_identity']['sha256'],'candidate PNG hash')
        with Image.open(path) as im:
            require(im.mode=='L' and im.size==(640,480),'candidate raster')
            require(hashlib.sha256(im.tobytes()).hexdigest()==r['luma_sha256'],'candidate Y hash')
            candidates.append(np.array(im)[::4,::4])
        pins[str(path.relative_to(HERE))]=h
    candidates=np.stack(candidates)
    regions={name:mask(rect) for name,rect in REGIONS.items()}
    results=[]
    for branch,mode in BRANCHES.items():
        for r in qr:
            path=qdir/r['png']; h=sha(path); require(h==r['sha256'],'query PNG hash')
            with Image.open(path) as im:
                require(im.mode=='L' and im.size==(720,480),'query raster')
                require(hashlib.sha256(im.tobytes()).hexdigest()==r['luma_sha256'],'query Y hash')
                resized=im.resize((640,480),mode)
                q=np.array(resized)[::4,::4]
            pins[str(path.relative_to(HERE))]=h
            item={'branch':branch,'query_index':r['index'],'query_pts':r['pts'],
                  'query_time_seconds_exact':r['time_seconds_exact'],'regions':{}}
            for name,m in regions.items():
                mae,corr=metrics(candidates[:,m],q[m])
                item['regions'][name]={'pixels':int(m.sum()),'mae':mae.tolist(),'correlation':nullable(corr)}
                if name=='full': item['selected']=choose(mae,ids)
            selected_row=cr[item['selected']['candidate_index']-6500]
            item['selected'].update(candidate_pts=selected_row['source_pts'],
                                    candidate_time_seconds_exact=selected_row['source_time_seconds_exact'])
            results.append(item)
    output={'candidate_indices':ids,'regions_half_open':REGIONS,'grid':'native (0,0) every fourth pixel',
            'results':results,'limits':'Source-content correspondence diagnostic; no authenticated exposure, clock, physical calibration or cause.'}
    require(all(sha(HERE/p)==h for p,h in pins.items()),'input changed')
    out.mkdir()
    with (out/'scores.json').open('x') as f: json.dump(output,f,sort_keys=True,allow_nan=False); f.write('\n')
    summary={'queries':len(QUERIES),'candidates':len(ids),'branches':len(BRANCHES),'regions':len(REGIONS),
             'comparisons':len(results)*len(REGIONS)*len(ids),
             'selections':[{'branch':r['branch'],'query_index':r['query_index'],**r['selected']} for r in results],
             'visual_candidate_union':sorted({r['selected']['candidate_index'] for r in results})}
    with (out/'summary.json').open('x') as f: json.dump(summary,f,indent=2,sort_keys=True); f.write('\n')
    receipt={'inputs':pins,'python':platform.python_version(),'numpy':np.__version__,'pillow':pillow_version,
             'scores_sha256':sha(out/'scores.json'),'summary_sha256':sha(out/'summary.json')}
    with (out/'receipt.json').open('x') as f: json.dump(receipt,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(summary))


class Controls(unittest.TestCase):
    def test_copy_and_brightness(self):
        q=np.array([10,20,30,40]); a,r=metrics(np.array([q,q+5]),q)
        np.testing.assert_allclose(a,[0,5]); np.testing.assert_allclose(r,[1,1])
    def test_local_change(self):
        a,r=metrics([[10,20,30,80]],[10,20,30,40]); self.assertEqual(a[0],10); self.assertLess(r[0],1)
    def test_undefined_constant(self):
        a,r=metrics([[1,1,1],[1,2,3]],[5,5,5]); self.assertTrue(np.isnan(r).all()); self.assertEqual(nullable(r),[None,None])
    def test_tie_and_boundary(self):
        r=choose(np.array([0,0,2]),[20,10,30]); self.assertEqual(r['candidate_index'],10)
        self.assertEqual(r['exact_minimum_ties'],[10,20]); self.assertEqual(r['gap'],0); self.assertTrue(r['at_candidate_boundary'])
    def test_regions(self):
        self.assertEqual({n:int(mask(b).sum()) for n,b in REGIONS.items()},
                         {'full':16800,'left_foreground':3055,'right_background':1320,'target_smoke':3100})
    def test_resampling_grid(self):
        source=np.tile(np.arange(480,dtype=np.uint16)[:,None]%256,(1,720)).astype(np.uint8)
        for mode in BRANCHES.values():
            q=np.array(Image.fromarray(source).resize((640,480),mode))[::4,::4]
            self.assertEqual(q.shape,(120,160)); np.testing.assert_array_equal(q[:,0],np.arange(0,480,4)%256)
        x=np.tile(np.arange(720,dtype=np.uint16)%256,(480,1)).astype(np.uint8)
        q=np.array(Image.fromarray(x).resize((640,480),Image.Resampling.NEAREST))
        expected=np.floor((np.arange(640)+0.5)*720/640).astype(int)%256
        np.testing.assert_array_equal(q[0],expected)
    def test_bad_values(self):
        with self.assertRaises(ValueError): metrics([[np.nan,0]],[0,1])
        with self.assertRaises(ValueError): choose(np.array([0,1]),[1,1])


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--test',action='store_true'); p.add_argument('--out'); args=p.parse_args()
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    run(args.out)
