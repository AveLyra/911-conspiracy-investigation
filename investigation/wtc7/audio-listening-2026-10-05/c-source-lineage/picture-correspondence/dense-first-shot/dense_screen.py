"""Dense fixed first-shot driver; unchanged parent scoring, no clock inference."""
import argparse
import contextlib
from fractions import Fraction
import hashlib
import importlib.util
import io
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

HERE=Path(__file__).resolve().parent
REFERENCE_IDS=[12900,12960,13020]
DENSE_IDS=list(range(300,540))


def pin(path):
    with Path(path).open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    return {'sha256':digest,'bytes':Path(path).stat().st_size}


def checked(spec):
    if not isinstance(spec,dict) or not isinstance(spec.get('path'),str) or not re.fullmatch('[0-9a-f]{64}',spec.get('sha256','')):
        raise ValueError('required path/hash pin')
    p=Path(spec['path']);v=pin(p)
    if any(v[k]!=spec[k] for k in ('sha256','bytes') if k in spec): raise ValueError('pin mismatch')
    return p


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def dependencies():
    cfg=json.loads((HERE/'config.json').read_text())
    required={'parent_config','parent_adapter','parent_tests','parent_protocol','dense_map'}
    if set(cfg)!=required: raise ValueError('dense config membership')
    paths={k:checked(v) for k,v in cfg.items()}
    review=json.loads((HERE/'preparation-review.json').read_text())
    if review.get('decision')!='proceed_with_boundaries' or review.get('protocol_sha256')!=pin(HERE/'PROTOCOL.md')['sha256']:
        raise ValueError('method review missing/stale')
    parent=module(paths['parent_adapter'],'dense_parent_adapter')
    if (paths['parent_config'].resolve()!=parent.HERE/'config.json'
            or paths['parent_tests'].resolve()!=parent.HERE/'test_picture_screen.py'
            or paths['parent_protocol'].resolve()!=parent.HERE/'PROTOCOL.md'):
        raise ValueError('parent dependency path mismatch')
    c=parent.config_load();core=module(checked(c['core']),'dense_inherited_core')
    for k in ('early_video','c_video','early_map','c_map'): checked(c[k])
    if (platform.python_version(),np.__version__,Image.__version__)!=('3.13.7','2.3.4','12.0.0'):
        raise ValueError('declared runtime mismatch')
    return cfg,paths,parent,c,core


def state(cfg,paths,parent,c):
    inherited=parent.state(c)
    files=[HERE/'dense_screen.py',HERE/'test_dense_screen.py',HERE/'PROTOCOL.md',HERE/'config.json',HERE/'preparation-review.json',*paths.values()]
    files += [checked(c[k]) for k in ('early_video','c_video','early_map','c_map')]
    return {'inherited':inherited,'pins':{str(p):pin(p) for p in files}}


def dense_rows(parent,rows):
    if not isinstance(rows,list) or len(rows)!=240: raise ValueError('dense map must have exactly240 rows')
    selected=parent.select_rows(rows,DENSE_IDS)
    if [r['source_index'] for r in rows]!=DENSE_IDS: raise ValueError('dense map order/membership')
    for r in selected:
        i=r['source_index']
        if (type(r['source_pts']) is not int or r['source_pts']!=i*1001
                or r['source_time_base']!='1/30000'
                or Fraction(r['source_seconds_exact'])!=Fraction(i*1001,30000)
                or not Fraction(10)<=Fraction(r['source_seconds_exact'])<18):
            raise ValueError('dense PTS/index contract')
    return selected


def reference_rows(parent,rows):
    selected=parent.select_rows(rows,REFERENCE_IDS)
    for r,s in zip(selected,(430,432,434)):
        if Fraction(r['source_seconds_exact'])!=s: raise ValueError('reference PTS contract')
    return selected


def verify_pairs(rows):
    expected={(r,i) for r in REFERENCE_IDS for i in DENSE_IDS}
    actual=[(r['reference_index'],r['source_index']) for r in rows]
    if len(actual)!=720 or len(set(actual))!=720 or set(actual)!=expected:
        raise ValueError('Cartesian coverage failure')


def bands(indices):
    ordered=sorted(set(indices));out=[]
    for i in ordered:
        if not out or i!=out[-1][1]+1: out.append([i,i])
        else: out[-1][1]=i
    return out


def rankings(parent,rows):
    out={}
    for ri in REFERENCE_IDS:
        result=parent.rank([r for r in rows if r['reference_index']==ri])
        for kind in ('static','dynamic'):
            arm=result[kind]
            arm['near_best_bands']={d:bands(ids) for d,ids in arm['near_best'].items()}
            arm['exact_best_ties']=[r['source_index'] for r in arm['ranking'] if r['score']==arm['ranking'][0]['score']] if arm['ranking'] else []
            arm['endpoint_leader']=bool(arm['ranking'] and arm['ranking'][0]['source_index'] in (300,539))
        out[str(ri)]=result
    return out


def gate(parent,path,frozen):
    r=json.loads((path/'receipt.json').read_text())
    if r.get('mode')!='controls' or r.get('status')!='complete' or r.get('before')!=frozen or r.get('after')!=frozen:
        raise ValueError('stale/failed control receipt')
    for name,p in r['products'].items():
        relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts or pin(path/relative)!=p: raise ValueError('control product mismatch')
    q=json.loads((path/'controls.json').read_text())
    if not (q.get('pass') is True and q.get('dense_tests')>=8 and q.get('parent_tests')==9
            and q.get('inherited')=={'controls':11,'pass':True}): raise ValueError('control coverage failure')
    return pin(path/'receipt.json')


def controls(out,parent,core,paths):
    inherited_dir=out/'inherited';inherited_dir.mkdir(); inherited=core.controls(inherited_dir)
    pt=parent.module(paths['parent_tests'],'dense_parent_tests');pt.ADAPTER=parent;pt.CORE=core
    dt=module(HERE/'test_dense_screen.py','dense_tests');dt.DRIVER=sys.modules[__name__];dt.PARENT=parent
    log=io.StringIO()
    with contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
        a=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(pt))
        b=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(dt))
    with (out/'tests.txt').open('x') as f:f.write(log.getvalue())
    result={'pass':a.wasSuccessful() and b.wasSuccessful(),'parent_tests':a.testsRun,'dense_tests':b.testsRun,'inherited':inherited}
    parent.save(out/'controls.json',result)
    if not result['pass']: raise ValueError('synthetic control failure')
    return result


def screen(out,paths,parent,c,core,start):
    em=paths['dense_map'];cm=Path(c['c_map']['path'])
    early=dense_rows(parent,json.loads(em.read_text()));refs=reference_rows(parent,json.loads(cm.read_text()))
    images=[core.working(parent.frame(em,r,c['early_dimensions'])) for r in early]
    targets=[core.working(parent.frame(cm,r,c['c_dimensions']).crop(c['first']['crop'])) for r in refs]
    static,dynamic=parent.masks(c['first'])
    if (int(static.sum()),int(dynamic.sum()),int((static&dynamic).sum()))!=(4786,3528,0):raise ValueError('mask count mismatch')
    sources={k:pin(checked(c[k])) for k in ('early_video','c_video','c_map')}
    sources['dense_map']=pin(em)
    parent.save(out/'input-map.json',{'source_pins':sources,'early':early,'references':refs,'early_map':str(em),'c_map':str(cm),'dimensions':{'early':c['early_dimensions'],'C':c['c_dimensions']}})
    results=[]
    for ref,target in zip(refs,targets):
        for row,image in zip(early,images):
            parent.budget(out,start,c)
            best,scores,coverage=parent.register(core,image,target,static,dynamic,c['scales'])
            if scores.shape!=(21,51,51) or coverage.shape!=scores.shape: raise ValueError('surface geometry')
            name=f"surfaces-C{ref['source_index']}-E{row['source_index']}.npz"
            with (out/name).open('xb') as f:np.savez_compressed(f,static_scores=scores,static_coverage=coverage)
            parent.budget(out,start,c)
            results.append({'reference_index':ref['source_index'],'source_index':row['source_index'],
                'source_pts':row['source_pts'],'source_time_base':row['source_time_base'],
                'reference_pts':ref['source_pts'],'reference_time_base':ref['source_time_base'],
                'surface_file':name,'transforms':best,'missing_reason':None if best else 'all_static_transforms_invalid'})
    verify_pairs(results);parent.save(out/'results.json',results);parent.save(out/'rankings.json',rankings(parent,results))
    for path,rows in ((em,early),(cm,refs)):
        for r in rows:checked({'path':str(path.parent/r['png']),'sha256':r['sha256'],'bytes':r['bytes']})
    return {'pairs':720,'surface_shape':[21,51,51],'frames_verified':243}


def run_name(mode,name):
    if mode not in ('controls','screen') or not isinstance(name,str):raise ValueError('mode/name')
    if (mode=='screen' and name not in ('screen01','screen02')) or (mode=='controls' and not re.fullmatch('controls[0-9]{2}',name)):
        raise ValueError('run name not admitted')


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['controls','screen']);p.add_argument('--run',required=True);p.add_argument('--controls');a=p.parse_args()
    run_name(a.mode,a.run)
    if a.controls:run_name('controls',a.controls)
    cfg,paths,parent,c,core=dependencies();frozen=state(cfg,paths,parent,c)
    g=gate(parent,HERE/a.controls,frozen) if a.mode=='screen' and a.controls else None
    if a.mode=='screen' and g is None:raise ValueError('passing controls required')
    out=HERE/a.run;out.mkdir(exist_ok=False);start=time.monotonic()
    receipt={'mode':a.mode,'status':'started','before':frozen,'controls_receipt':g};parent.save(out/'start.json',receipt)
    def timeout(*_):raise RuntimeError('wall time cap')
    old=signal.signal(signal.SIGALRM,timeout);signal.alarm(600)
    try:
        receipt['result']=controls(out,parent,core,paths) if a.mode=='controls' else screen(out,paths,parent,c,core,start)
        receipt['after']=state(cfg,paths,parent,c)
        if receipt['after']!=frozen:raise ValueError('input/dependency changed')
        parent.budget(out,start,c);receipt['status']='complete'
    except Exception as e:
        receipt.update(status='failed',error_type=type(e).__name__,error=str(e));raise
    finally:
        signal.alarm(0);signal.signal(signal.SIGALRM,old);receipt['elapsed_s']=time.monotonic()-start
        receipt['products']={str(p.relative_to(out)):pin(p) for p in out.rglob('*') if p.is_file() and p.name not in ('receipt.json','start.json')}
        parent.save(out/'receipt.json',receipt)
    print(json.dumps({'status':receipt['status'],'result':receipt['result']}))


if __name__=='__main__':main()
