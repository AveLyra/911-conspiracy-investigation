#!/usr/bin/env python3
"""Dense extraction/direct-score verification. Never imports producer/core."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
from PIL import Image, __version__ as PILLOW

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
PARENT_CHECK_SHA='56784c9f63ea2f8fc775e0d6d77635a80ea1dc3b4aff5dd9326d954272afa2ef'
PARENT_CONFIG_SHA='56efd21495ef21b37df9137438f0b53183a120b59b1b43eb0f498b4ac47d65b2'
FFMPEG=Path('/opt/homebrew/bin/ffmpeg')
FFPROBE=Path('/opt/homebrew/bin/ffprobe')


def identity(path):
    path=Path(path)
    with path.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    return {'sha256':sha,'bytes':path.stat().st_size}


def read(path):return json.loads(Path(path).read_text())


def pinned(path,expected):
    actual=identity(path)
    assert all(actual[k]==v for k,v in expected.items() if k in actual),str(path)


def load_arithmetic():
    path=PARENT/'independent_check.py'
    assert identity(path)['sha256']==PARENT_CHECK_SHA
    spec=importlib.util.spec_from_file_location('reviewed_independent_arithmetic',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def checked_receipt(directory):
    receipt=read(directory/'receipt.json')
    assert receipt['status']=='complete',str(directory)
    for name,pin in receipt['products'].items():pinned(directory/name,pin)
    if 'before' in receipt:
        assert receipt['before']==receipt['after']
        state=receipt['before']
        if 'pins' in state:
            groups=[state['pins']]
            if 'inherited' in state:
                assert isinstance(state['inherited'],dict) and 'pins' in state['inherited']
                groups.append(state['inherited']['pins'])
            for group in groups:
                assert isinstance(group,dict) and group
                for path,value in group.items():
                    assert Path(path).is_absolute() and set(value)=={'sha256','bytes'}
                    pinned(path,value)
        else:
            assert isinstance(state,dict) and state
            for path,value in state.items():
                assert Path(path).is_absolute() and isinstance(value,dict) and set(value)=={'sha256','bytes'},'Unknown receipt state schema'
                pinned(path,value)
    for a,b in [('inputs_before','inputs_after'),('binary_pins','binary_pins_after')]:
        if a in receipt:
            assert receipt[a]==receipt[b]
            for path,pin in receipt[a].items():pinned(path,pin)
    if 'commands' in receipt:
        assert all(c.get('exit',c.get('returncode'))==0 for c in receipt['commands'])
    return receipt


def extraction(first,second,record):
    pinned(PARENT/'config.json',{'sha256':PARENT_CONFIG_SHA})
    config=read(PARENT/'config.json')
    source=Path(config['early_video']['path']);pinned(source,config['early_video'])
    before=identity(source)
    runs=[]
    for directory in (first,second):
        receipt=checked_receipt(directory)
        assert receipt['source_before']==receipt['source_after']==before
        maps=[]
        for file in directory.glob('*-selected.json'):
            value=read(file)
            if isinstance(value,list) and len(value)==240:maps.append((file,value))
        assert len(maps)==1,'Need unique 240-row selected map'
        path,rows=maps[0]
        assert [r['source_index'] for r in rows]==list(range(300,540))
        for r in rows:
            assert Fraction(r['source_time_base'])==Fraction(1,30000)
            assert r['source_pts']==r['source_index']*1001
            assert Fraction(r['source_seconds_exact'])==Fraction(r['source_pts'],30000)
            assert 10<=Fraction(r['source_seconds_exact'])<18
            pinned(directory/r['png'],r)
        checks=read(directory/'synthetic-checks.json')
        assert len(checks)==6 and all(v is True for v in checks.values())
        runs.append((receipt,path,rows))
    assert runs[0][2]==runs[1][2]
    # Synthetic containers can carry different metadata; historical maps/PNGs/
    # sheets must agree. Identify historical prefix from the selected map.
    prefix=runs[0][1].name.removesuffix('-selected.json')
    historical=[name for name in runs[0][0]['products'] if name.startswith(prefix)]
    for name in historical:assert (first/name).read_bytes()==(second/name).read_bytes(),name
    assert len(list((first/(prefix+'-overview')).glob('*.png')))==8
    coarse_path=Path(config['early_map']['path']);pinned(coarse_path,config['early_map'])
    coarse={r['quarter_bin']:r for r in read(coarse_path)}
    dense={r['source_index']:r for r in runs[0][2]}
    for sec in range(10,18):
        c=coarse[sec];d=dense[c['source_index']]
        pinned(coarse_path.parent/c['png'],c)
        assert (coarse_path.parent/c['png']).read_bytes()==(first/d['png']).read_bytes()
    def run(args):
        p=subprocess.run(args,capture_output=True,timeout=60)
        record.setdefault('commands',[]).append({'argv':args,'exit':p.returncode,
            'stderr_utf8':p.stderr.decode(errors='replace'),'stdout_bytes':len(p.stdout),
            'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()})
        assert p.returncode==0 and not p.stderr
        return p.stdout
    frames=json.loads(run([str(FFPROBE),'-v','error','-select_streams','v:0','-show_frames',
        '-show_entries','frame=pts,width,height','-of','json',str(source)]))['frames']
    assert len(frames)==1130
    assert all(f['pts']==i*1001 and f['width']==320 and f['height']==224 for i,f in enumerate(frames))
    chosen=[i for i,f in enumerate(frames) if 10<=Fraction(f['pts'],30000)<18]
    assert chosen==list(range(300,540))
    raw=run([str(FFMPEG),'-nostdin','-v','error','-noautorotate','-i',str(source),'-map','0:v:0',
             '-an','-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','pipe:1'])
    size=320*224*3;assert len(raw)==1130*size
    for row in runs[0][2]:
        i=row['source_index'];expected=raw[i*size:(i+1)*size]
        for directory in (first,second):
            with Image.open(directory/row['png']) as image:
                assert image.size==(320,224) and image.mode=='RGB' and image.tobytes()==expected
    assert identity(source)==before
    return {'full_decoded_frames':1130,'selected_indices':[300,539],'selected_frames_per_run':240,
        'selected_png_pixel_comparisons':480,'coarse_exact_overlaps':8,'historical_equal_products':len(historical),
        'source_before':before,'source_after':identity(source),'maps':[identity(r[1]) for r in runs],
        'synthetic_checks_per_run':6,'limitations':'Same installed decoder; full sequential decode rather than selection helper. No original-camera exposure/custody inference.'}


def scores(first,second,math):
    dense_config=read(HERE/'config.json')
    for entry in dense_config.values():pinned(entry['path'],entry)
    config=read(PARENT/'config.json')
    receipts=[checked_receipt(d) for d in (first,second)]
    assert receipts[0]['products']==receipts[1]['products']
    for name in receipts[0]['products']:assert (first/name).read_bytes()==(second/name).read_bytes()
    imap=read(first/'input-map.json')
    em=Path(imap['early_map']);cm=Path(imap['c_map'])
    early=imap['early'];refs=imap['references']
    assert em==Path(dense_config['dense_map']['path']) and cm==Path(config['c_map']['path'])
    for name,value in imap['source_pins'].items():
        entry=dense_config[name] if name=='dense_map' else config[name]
        pinned(entry['path'],value)
    assert [r['source_index'] for r in early]==list(range(300,540))
    assert [r['source_index'] for r in refs]==[12900,12960,13020]
    assert early==read(em)
    actual_c={r['source_index']:r for r in read(cm)}
    assert all(actual_c[r['source_index']]==r for r in refs)
    for field in ('early_video','c_video','c_map','core'):pinned(config[field]['path'],config[field])
    images={};targets={};arm=config['first']
    static,dynamic=math.mask(arm['static'],arm['crop']),math.mask(arm['dynamic'],arm['crop'])
    assert static.sum()==4786 and dynamic.sum()==3528 and not (static&dynamic).any()
    for directory,rows,size,destination,isref in [(em.parent,early,(320,224),images,False),(cm.parent,refs,(1280,720),targets,True)]:
        for r in rows:
            p=directory/r['png'];pinned(p,r)
            with Image.open(p) as image:assert image.size==size
            assert Fraction(r['source_pts'])*Fraction(r['source_time_base'])==Fraction(r['source_seconds_exact'])
            destination[r['source_index']]=math.working(p,arm['crop'] if isref else None)
    rows=read(first/'results.json')
    expected={(r['source_index'],e['source_index']) for r in refs for e in early}
    assert len(rows)==720 and {(r['reference_index'],r['source_index']) for r in rows}==expected
    comparisons=[];maxscore=maxcoverage=0.;nulls=0
    e_byid={r['source_index']:r for r in early};r_byid={r['source_index']:r for r in refs}
    for row in rows:
        for key in ('pts','time_base'):
            assert row['source_'+key]==e_byid[row['source_index']]['source_'+key]
            assert row['reference_'+key]==r_byid[row['reference_index']]['source_'+key]
        with np.load(first/row['surface_file'],allow_pickle=False) as f:
            s=f['static_scores'];coverage=f['static_coverage']
        assert s.shape==coverage.shape==(21,51,51)
        assert np.isfinite(coverage).all() and coverage.min()>=-1e-12 and coverage.max()<=1+1e-12
        finite=np.argwhere(np.isfinite(s))
        chosen=sorted(finite.tolist(),key=lambda a:(-s[tuple(a)],config['scales'][a[0]],a[1],a[2]))[:2]
        assert len(chosen)==len(row['transforms'])
        assert row['missing_reason']==(None if chosen else 'all_static_transforms_invalid')
        for ordinal,((si,y,x),t) in enumerate(zip(chosen,row['transforms'])):
            scale=config['scales'][si]
            assert (t['requested_scale'],t['top'],t['left'])==(scale,y,x)
            assert t['static_score']==float(s[si,y,x]) and t['static_coverage']==float(coverage[si,y,x])
            a,v,geometry=math.canvas(images[row['source_index']],scale)
            for k,value in geometry.items():assert t[k]==value
            assert t['dx']==x-25 and t['dy']==y-25
            ox,oy=geometry['canvas_x'],geometry['canvas_y'];w,h=geometry['raster_width'],geometry['raster_height']
            intersection=[max(0,ox),max(0,oy),min(230,ox+w),min(170,oy+h)]
            assert t['canvas_intersection']==intersection and t['scaled_raster_intersection']==[intersection[0]-ox,intersection[1]-oy,intersection[2]-ox,intersection[3]-oy]
            assert t['scale_x']==w/180 and t['scale_y']==h/120
            assert t['translation_boundary']==(x in (0,50) or y in (0,50)) and t['scale_boundary']==(si in (0,20))
            region,valid=a[y:y+120,x:x+180],v[y:y+120,x:x+180]
            score,cov,reason,n=math.direct(region,targets[row['reference_index']],static,valid)
            ds,dc,dr,dn=math.direct(region,targets[row['reference_index']],dynamic,valid)
            assert score is not None and reason is None
            error=abs(score-t['static_score']);ce=abs(cov-t['static_coverage'])
            d=t['dynamic'];assert d['missing_reason']==dr and d['pixels']==dn
            ce=max(ce,abs(dc-d['coverage']))
            if ds is None:assert d['score'] is None;nulls+=1
            else:assert d['score'] is not None;error=max(error,abs(ds-d['score']))
            assert error<=1e-9 and ce<=1e-12
            maxscore=max(maxscore,error);maxcoverage=max(maxcoverage,ce)
            comparisons.append({'reference_index':row['reference_index'],'source_index':row['source_index'],
                'ordinal':ordinal,'static_score':score,'dynamic_score':ds,'dynamic_missing_reason':dr,
                'max_score_error':error,'max_coverage_error':ce})
    ranks=read(first/'rankings.json')
    assert set(ranks)=={'12900','12960','13020'}
    for rid in (12900,12960,13020):
        union=set()
        for kind in ('static','dynamic'):
            values=[]
            for row in rows:
                if row['reference_index']!=rid or not row['transforms']:continue
                t=row['transforms'][0];value=t['static_score'] if kind=='static' else t['dynamic']['score']
                if value is not None:values.append((row['source_index'],value))
            values.sort(key=lambda pair:(-pair[1],pair[0]));r=ranks[str(rid)][kind]
            assert r['ranking']==[{'source_index':i,'score':v} for i,v in values]
            ids=[i for i,v in values];assert r['top_two']==ids[:2];union.update(ids[:2])
            assert r['exact_best_ties']==([i for i,v in values if v==values[0][1]] if values else [])
            assert r['endpoint_leader']==(bool(values) and values[0][0] in (300,539))
            for delta in [.005,.01,.02]:
                near=[i for i,v in values if values[0][1]-v<=delta] if values else []
                assert r['near_best'][str(delta)]==near
                bands=[]
                for index in sorted(near):
                    if bands and index==bands[-1][1]+1:bands[-1][1]=index
                    else:bands.append([index,index])
                assert r['near_best_bands'][str(delta)]==bands
        assert ranks[str(rid)]['shortlist_union']==sorted(union)
    for entry in dense_config.values():pinned(entry['path'],entry)
    return {'pairs':720,'input_images':243,'selected_transform_checks':len(comparisons),'dynamic_nulls':nulls,
        'max_absolute_score_error':maxscore,'max_absolute_coverage_error':maxcoverage,
        'two_run_products':len(receipts[0]['products']),'ranking_groups':3,'comparisons':comparisons}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['synthetic','extraction','scores'])
    parser.add_argument('--first',type=Path);parser.add_argument('--second',type=Path)
    args=parser.parse_args();arithmetic=load_arithmetic();checks=arithmetic.synthetic()
    if args.mode=='synthetic':print(json.dumps({'pass':True,'checks':checks}));return
    if args.first is None or args.second is None:raise ValueError('Two run directories required')
    output=HERE/('extraction-check.json' if args.mode=='extraction' else 'independent-check.json')
    if output.exists():raise FileExistsError('Refusing existing independent result')
    result={'status':'started','mode':args.mode,'synthetic_checks':checks,'script':identity(Path(__file__)),
        'protocol':identity(HERE/'PROTOCOL.md'),'parent_arithmetic':identity(PARENT/'independent_check.py'),
        'python':platform.python_version(),'numpy':np.__version__,'pillow':PILLOW,
        'binary_pins':{str(p):identity(p) for p in (FFMPEG,FFPROBE)},
        'score_tolerance':1e-9,'coverage_tolerance':1e-12,
        'independence':'No producer/core import. Reuses hash-pinned separate checker arithmetic; shared Pillow, decoder and source files. No image viewing or source authentication.'}
    start=time.monotonic()
    try:
        result['verification']=extraction(args.first,args.second,result) if args.mode=='extraction' else scores(args.first,args.second,arithmetic)
        result['status']='complete'
    except Exception as exc:
        result.update(status='failed',error_type=type(exc).__name__,error=str(exc));raise
    finally:
        result['elapsed_s']=time.monotonic()-start
        with output.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':result['status'],'mode':args.mode}))


if __name__=='__main__':main()
