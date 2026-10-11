"""Frozen held-image retrieval adapter; synthetic controls precede scoring."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import signal
import sys
import time
import unittest
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent


def pin(path):
    with Path(path).open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': Path(path).stat().st_size}


def checked(spec):
    p = Path(spec['path']); actual = pin(p)
    if any(actual[k] != spec[k] for k in ('sha256', 'bytes') if k in spec):
        raise ValueError('input pin mismatch')
    return p


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def save(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False); f.write('\n')


def geometry(box, size):
    if (len(box) != 4 or any(type(x) is not int for x in box)
            or not 0 <= box[0] < box[2] <= size[0]
            or not 0 <= box[1] < box[3] <= size[1]):
        raise ValueError('invalid rectangle')


def masks(arm, size=(1280, 720)):
    crop = arm['crop']; geometry(crop, size)
    xs = crop[0] + (np.arange(180)+.5)*(crop[2]-crop[0])/180
    ys = crop[1] + (np.arange(120)+.5)*(crop[3]-crop[1])/120
    output = []
    for name in ('static', 'dynamic'):
        mask = np.zeros((120,180), bool)
        for box in arm[name]:
            geometry(box,size)
            if box[0]<crop[0] or box[1]<crop[1] or box[2]>crop[2] or box[3]>crop[3]:
                raise ValueError('mask outside crop')
            a,b,c,d = box; mask |= (xs[None,:]>=a)&(xs[None,:]<c)&(ys[:,None]>=b)&(ys[:,None]<d)
        if mask.sum()<32: raise ValueError('insufficient mask')
        output.append(mask)
    if (output[0]&output[1]).any(): raise ValueError('overlapping masks')
    return output


def canvas(image, scale):
    a = np.asarray(image)
    if a.shape!=(120,180) or not np.isfinite(a).all() or a.min()<0 or a.max()>255:
        raise ValueError('working geometry/range')
    if not np.isfinite(scale) or scale<.75 or scale>1.75: raise ValueError('scale')
    sw,sh = round(180*scale),round(120*scale)
    x,y = 25+(180-sw)//2,25+(120-sh)//2
    left,top,right,bottom = max(0,x),max(0,y),min(230,x+sw),min(170,y+sh)
    raster = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((sw,sh),Image.Resampling.BILINEAR))
    out = np.zeros((170,230),float); valid = np.zeros_like(out,bool)
    out[top:bottom,left:right]=raster[top-y:bottom-y,left-x:right-x]; valid[top:bottom,left:right]=True
    return out,valid,{'requested_scale':scale,'raster_width':sw,'raster_height':sh,
        'scale_x':sw/180,'scale_y':sh/120,'canvas_x':x,'canvas_y':y,
        'canvas_intersection':[left,top,right,bottom],'scaled_raster_intersection':[left-x,top-y,right-x,bottom-y]}


def dynamic_score(core, image, target, mask, valid):
    good = mask & valid; n=int(good.sum()); coverage=n/int(mask.sum())
    reason = 'coverage' if coverage<.85 else ('pixel_count' if n<32 else None)
    score = None if reason else core.scalar_pearson(image,target,good)
    if score is None and reason is None: reason='variance'
    return {'score':score,'coverage':coverage,'pixels':n,'missing_reason':reason}


def register(core, image, target, static, dynamic, scales):
    scores=[]; coverages=[]; proposals=[]
    for scale in scales:
        a,v,t=canvas(image,scale)
        s,c=core.pearson_surface(a,target,static,v)
        if s.shape!=(51,51) or c.shape!=(51,51): raise ValueError('translation grid changed')
        scores.append(s);coverages.append(c)
        ids=np.flatnonzero(np.isfinite(s)); order=np.lexsort((ids,-s.flat[ids]))[:2]
        for index in ids[order]:
            y,x=map(int,np.unravel_index(index,s.shape))
            d=dynamic_score(core,a[y:y+120,x:x+180],target,dynamic,v[y:y+120,x:x+180])
            proposals.append({'static_score':float(s[y,x]),'static_coverage':float(c[y,x]),
                'dynamic':d,'top':y,'left':x,'dx':x-25,'dy':y-25,
                'translation_boundary':x in (0,50) or y in (0,50),
                'scale_boundary':scale in (.75,1.75),**t})
    proposals.sort(key=lambda z:(-z['static_score'],z['requested_scale'],z['top'],z['left']))
    return proposals[:2],np.array(scores),np.array(coverages)


def rank(rows):
    out={};union=set()
    for name in ('static','dynamic'):
        def score(r):
            return r['transforms'][0]['static_score'] if name=='static' else r['transforms'][0]['dynamic']['score']
        valid=[r for r in rows if r['transforms'] and score(r) is not None]
        valid.sort(key=lambda r:(-score(r),r['source_index']))
        ids=[r['source_index'] for r in valid];union.update(ids[:2])
        out[name]={'ranking':[{'source_index':r['source_index'],'score':score(r)} for r in valid],
            'top_two':ids[:2],'near_best':{str(d):[r['source_index'] for r in valid if score(valid[0])-score(r)<=d] for d in (.005,.01,.02)}}
    out['shortlist_union']=sorted(union); return out


def select_rows(rows, indices):
    if not isinstance(rows,list): raise ValueError('map must be list')
    ids=[r['source_index'] for r in rows]
    if any(type(i) is not int for i in ids) or len(ids)!=len(set(ids)): raise ValueError('duplicate/bad source index')
    paths=[r['png'] for r in rows]
    if len(paths)!=len(set(paths)): raise ValueError('duplicate frame path')
    mapping={r['source_index']:r for r in rows}
    if any(i not in mapping for i in indices): raise ValueError('missing selected frame')
    chosen=[mapping[i] for i in indices]
    for r in chosen:
        p=Path(r['png'])
        if p.is_absolute() or '..' in p.parts: raise ValueError('frame path escape')
        if Fraction(r['source_pts'])*Fraction(r['source_time_base'])!=Fraction(r['source_seconds_exact']):
            raise ValueError('inconsistent PTS')
    return chosen


def frame(map_path, row, size):
    p=map_path.parent/row['png']; checked({'path':str(p),'sha256':row['sha256'],'bytes':row['bytes']})
    with Image.open(p) as im:
        if im.size!=tuple(size) or getattr(im,'n_frames',1)!=1: raise ValueError('frame geometry')
        im.load(); return im.copy()


def config_load():
    c=json.loads((HERE/'config.json').read_text())
    expected={'working_dimensions':[180,120],'canvas_dimensions':[230,170],'offset_grid':[-25,25],
        'min_coverage':.85,'min_pixels':32,'variance_strict_gt':1e-8,'max_seconds':600,'max_bytes':402653184,
        'early_dimensions':[320,224],'c_dimensions':[1280,720],'c_local_seconds':[0,2,4,14,19,24],
        'near_best_differences':[.005,.01,.02],'scales':[round(.75+.05*i,2) for i in range(21)]}
    if any(c.get(k)!=v for k,v in expected.items()): raise ValueError('unsupported frozen configuration')
    for arm in ('first','third'): masks(c[arm])
    return c


def state(c):
    files=[Path(__file__).resolve(),HERE/'test_picture_screen.py',HERE/'PROTOCOL.md',HERE/'config.json',checked(c['core']),Path(sys.executable),Path(np.__file__),Path(Image.__file__)]
    return {'pins':{str(p):pin(p) for p in files},'python':platform.python_version(),
            'numpy':np.__version__,'pillow':Image.__version__,'platform':platform.platform()}


def gate(path, frozen):
    r=json.loads((path/'receipt.json').read_text())
    if r.get('mode')!='controls' or r.get('status')!='complete' or r.get('before')!=frozen or r.get('after')!=frozen:
        raise ValueError('stale/failed controls')
    for name,p in r['products'].items():
        if pin(path/name)!=p: raise ValueError('controls product mismatch')
    q=json.loads((path/'controls.json').read_text())
    if q.get('pass') is not True or q.get('tests_run',0)<8 or not q.get('inherited',{}).get('pass'):
        raise ValueError('incomplete controls')
    return pin(path/'receipt.json')


def budget(out,start,c):
    if time.monotonic()-start>c['max_seconds']: raise RuntimeError('wall time cap')
    if sum(p.stat().st_size for p in out.rglob('*') if p.is_file())>c['max_bytes']: raise RuntimeError('output byte cap')


def screen(out,c,core,start):
    sources={k:pin(checked(c[k])) for k in ('early_video','c_video','early_map','c_map')}
    em,cm=Path(c['early_map']['path']),Path(c['c_map']['path'])
    early=select_rows(json.loads(em.read_text()),[(30000*i+1000)//1001 for i in range(38)])
    refs=select_rows(json.loads(cm.read_text()),[(430+s)*30 for s in c['c_local_seconds']])
    for i,r in enumerate(early):
        if (r['quarter_bin']!=i or Fraction(r['source_seconds_exact'])!=Fraction(r['source_index']*1001,30000)
                or not Fraction(i)<=Fraction(r['source_seconds_exact'])<Fraction(i)+Fraction(1001,30000)):
            raise ValueError('early selection PTS')
    for s,r in zip(c['c_local_seconds'],refs):
        if Fraction(r['source_seconds_exact'])!=430+s: raise ValueError('C selection PTS')
    # Verify all selected files and geometry before scoring; retain only small working arrays.
    images=[core.working(frame(em,r,c['early_dimensions'])) for r in early]
    targets=[]
    for s,r in zip(c['c_local_seconds'],refs):
        arm=c['first' if s<5 else 'third']; im=frame(cm,r,c['c_dimensions'])
        targets.append((core.working(im.crop(arm['crop'])),*masks(arm)))
    save(out/'input-map.json',{'source_pins':sources,'early':early,'references':refs,'early_map':str(em),'c_map':str(cm),'dimensions':{'early':c['early_dimensions'],'C':c['c_dimensions']}})
    results=[]
    for ri,(ref,args) in enumerate(zip(refs,targets)):
        for row,image in zip(early,images):
            budget(out,start,c)
            best,scores,coverage=register(core,image,*args,c['scales'])
            name=f"surfaces-C{ref['source_index']}-E{row['source_index']}.npz"
            with (out/name).open('xb') as f: np.savez_compressed(f,static_scores=scores,static_coverage=coverage)
            results.append({'reference_index':ref['source_index'],'source_index':row['source_index'],
                'source_pts':row['source_pts'],'source_time_base':row['source_time_base'],
                'reference_pts':ref['source_pts'],'reference_time_base':ref['source_time_base'],
                'surface_file':name,'transforms':best,'missing_reason':None if best else 'all_static_transforms_invalid'})
    save(out/'results.json',results)
    save(out/'rankings.json',{str(r['source_index']):rank([x for x in results if x['reference_index']==r['source_index']]) for r in refs})
    for k,p in sources.items():
        if pin(Path(c[k]['path']))!=p: raise ValueError('source changed')
    for path,rows,size in ((em,early,c['early_dimensions']),(cm,refs,c['c_dimensions'])):
        for r in rows: checked({'path':str(path.parent/r['png']),'sha256':r['sha256'],'bytes':r['bytes']})
    return {'pairs':len(results),'surface_shape':[21,51,51],'frames_verified':44}


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['controls','screen']);p.add_argument('--run',required=True);p.add_argument('--controls')
    a=p.parse_args()
    if any(not re.fullmatch('[a-z][a-z0-9]{1,30}',s) for s in [a.run]+([a.controls] if a.controls else [])): raise ValueError('run name')
    c=config_load();frozen=state(c);core=module(checked(c['core']),'pinned_picture_core')
    control_pin=gate(HERE/a.controls,frozen) if a.mode=='screen' and a.controls else None
    if a.mode=='screen' and control_pin is None: raise ValueError('controls required')
    out=HERE/a.run;out.mkdir(exist_ok=False);start=time.monotonic()
    receipt={'mode':a.mode,'before':frozen,'status':'started','controls_receipt':control_pin}
    save(out/'start.json',receipt)
    def timeout(*_): raise RuntimeError('wall time cap')
    old=signal.signal(signal.SIGALRM,timeout);signal.alarm(c['max_seconds'])
    try:
        if a.mode=='controls':
            inherited_dir=out/'inherited';inherited_dir.mkdir();inherited=core.controls(inherited_dir)
            tests=module(HERE/'test_picture_screen.py','picture_adapter_tests');tests.ADAPTER=sys.modules[__name__];tests.CORE=core
            result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
            summary={'pass':result.wasSuccessful(),'tests_run':result.testsRun,'inherited':inherited}
            save(out/'controls.json',summary)
            if not summary['pass']: raise ValueError('synthetic controls failed')
            receipt['result']=summary
        else: receipt['result']=screen(out,c,core,start)
        receipt['after']=state(c)
        if receipt['after']!=frozen: raise ValueError('method inputs changed')
        budget(out,start,c);receipt['status']='complete'
    except Exception as exc:
        receipt.update(status='failed',error_type=type(exc).__name__,error=str(exc));raise
    finally:
        signal.alarm(0);signal.signal(signal.SIGALRM,old)
        receipt['elapsed_s']=time.monotonic()-start
        receipt['products']={str(x.relative_to(out)):pin(x) for x in out.rglob('*') if x.is_file() and x.name not in ('receipt.json','start.json')}
        save(out/'receipt.json',receipt)
    print(json.dumps({'status':receipt['status'],'result':receipt['result']}))


if __name__=='__main__': main()
