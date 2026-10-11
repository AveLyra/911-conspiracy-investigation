#!/usr/bin/env python3
"""Separate direct arithmetic checker; no producer/core imports or image viewing."""
import hashlib
import json
from pathlib import Path
import platform
import argparse
import time
from fractions import Fraction

import numpy as np
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).resolve().parent
SCORE_TOL = 1e-9
COVERAGE_TOL = 1e-12


def pin(path):
    with Path(path).open('rb') as f:
        sha = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'sha256':sha,'bytes':Path(path).stat().st_size}


def check_pin(path, expected):
    actual = pin(path)
    for field in ('sha256','bytes'):
        if field in expected and actual[field] != expected[field]:
            raise AssertionError((str(path),field))


def mask(rectangles,crop):
    x0,y0,x1,y1 = crop
    # Explicit working-pixel centers, independent of producer mask helper.
    result = np.zeros((120,180),bool)
    for y in range(120):
        py = y0+(y+.5)*(y1-y0)/120
        for x in range(180):
            px = x0+(x+.5)*(x1-x0)/180
            result[y,x] = any(a<=px<c and b<=py<d for a,b,c,d in rectangles)
    return result


def working(path,crop=None):
    with Image.open(path) as image:
        if crop is not None:
            image=image.crop(tuple(crop))
        return np.asarray(image.convert('L').resize((180,120),Image.Resampling.BILINEAR),dtype=float)


def canvas(image,scale):
    width,height=round(180*scale),round(120*scale)
    enlarged=np.asarray(Image.fromarray(image.astype('uint8')).resize((width,height),Image.Resampling.BILINEAR))
    left,top=25+(180-width)//2,25+(120-height)//2
    output=np.zeros((170,230),float)
    valid=np.zeros(output.shape,bool)
    # Independent intersection coordinates: no slicing with negative origins.
    x0,y0=max(0,left),max(0,top)
    x1,y1=min(230,left+width),min(170,top+height)
    if x1>x0 and y1>y0:
        output[y0:y1,x0:x1]=enlarged[y0-top:y1-top,x0-left:x1-left]
        valid[y0:y1,x0:x1]=True
    return output,valid,{'raster_width':width,'raster_height':height,'canvas_x':left,'canvas_y':top}


def direct(region,target,selection,valid):
    selected=selection & valid
    n=int(selected.sum())
    coverage=n/int(selection.sum())
    if coverage<.85:return None,coverage,'coverage',n
    if n<32:return None,coverage,'pixel_count',n
    a=region[selected].astype(np.longdouble)
    b=target[selected].astype(np.longdouble)
    a-=a.mean();b-=b.mean()
    aa=np.sum(a*a);bb=np.sum(b*b)
    if aa/n<=1e-8 or bb/n<=1e-8:return None,coverage,'variance',n
    return float(np.sum(a*b)/np.sqrt(aa*bb)),coverage,None,n


def synthetic():
    checks={}
    a=np.arange(120*180,dtype=float).reshape(120,180)%251
    full=np.ones(a.shape,bool)
    checks['pearson_gain_offset']=abs(direct(a,a*2+3,full,full)[0]-1)<SCORE_TOL
    checks['pearson_inversion']=abs(direct(a,-a,full,full)[0]+1)<SCORE_TOL
    checks['flat_null']=direct(np.ones(a.shape),a,full,full)[2]=='variance'
    sparse=np.zeros(a.shape,bool);sparse[:2,:10]=True
    checks['small_mask_null']=direct(a,a,sparse,full)[2]=='pixel_count'
    checks['coverage_null']=direct(a,a,full,sparse)[2]=='coverage'
    checks['full_native_mask']=mask([[10,20,110,220]],[10,20,110,220]).all()
    left=mask([[10,20,60,220]],[10,20,110,220])
    checks['half_native_mask']=int(left.sum())==10800 and left[:,:90].all() and not left[:,90:].any()
    for scale in [.75,1,1.75]:
        out,v,t=canvas(a,scale)
        width,height=round(180*scale),round(120*scale)
        x,y=25+(180-width)//2,25+(120-height)//2
        expected=max(0,min(230,x+width)-max(0,x))*max(0,min(170,y+height)-max(0,y))
        checks['canvas_'+str(scale)]=int(v.sum())==expected and out.shape==(170,230) and t['canvas_x']==x and t['canvas_y']==y
    if not all(checks.values()):raise AssertionError(checks)
    return {key:bool(value) for key,value in checks.items()}


def verify(first,second):
    config=json.loads((HERE/'config.json').read_text())
    receipts=[]
    for directory in (first,second):
        receipt=json.loads((directory/'receipt.json').read_text())
        assert receipt['status']=='complete' and receipt['mode']=='screen'
        assert receipt['before']==receipt['after']
        for p,value in receipt['before']['pins'].items():check_pin(p,value)
        for p,value in receipt['products'].items():check_pin(directory/p,value)
        receipts.append(receipt)
    assert receipts[0]['products']==receipts[1]['products'],'Two-run products differ'
    for name in receipts[0]['products']:
        assert (first/name).read_bytes()==(second/name).read_bytes(),name
    maps={}
    for name in ('early_video','c_video','early_map','c_map','core'):
        check_pin(config[name]['path'],config[name])
    for name,desired,size in [('early_map',[(30000*i+1000)//1001 for i in range(38)],[320,224]),
                               ('c_map',[(430+s)*30 for s in config['c_local_seconds']],[1280,720])]:
        p=Path(config[name]['path']);raw=json.loads(p.read_text())
        assert len({r['source_index'] for r in raw})==len(raw)
        byid={r['source_index']:r for r in raw}
        chosen=[byid[i] for i in desired]
        for row in chosen:
            assert Fraction(row['source_pts'])*Fraction(row['source_time_base'])==Fraction(row['source_seconds_exact'])
            file=p.parent/row['png'];check_pin(file,row)
            with Image.open(file) as image:assert list(image.size)==size
        maps[name]=(p,chosen)
    early,refs=maps['early_map'][1],maps['c_map'][1]
    for second_idx,row in enumerate(early):
        assert Fraction(row['source_seconds_exact'])==Fraction(row['source_index']*1001,30000)
        assert Fraction(second_idx)<=Fraction(row['source_seconds_exact'])<Fraction(second_idx)+Fraction(1001,30000)
    for local,row in zip(config['c_local_seconds'],refs):
        assert Fraction(row['source_seconds_exact'])==430+local
    imap=json.loads((first/'input-map.json').read_text())
    assert imap['early']==early and imap['references']==refs
    assert imap['early_map']==str(maps['early_map'][0]) and imap['c_map']==str(maps['c_map'][0])
    for key,value in imap['source_pins'].items():check_pin(config[key]['path'],value)
    assert imap['dimensions']=={'early':[320,224],'C':[1280,720]}
    rows=json.loads((first/'results.json').read_text())
    expected={(r['source_index'],e['source_index']) for r in refs for e in early}
    assert len(rows)==228 and {(r['reference_index'],r['source_index']) for r in rows}==expected
    images={r['source_index']:working(maps['early_map'][0].parent/r['png']) for r in early}
    targets={}
    ref_byid={r['source_index']:r for r in refs};early_byid={r['source_index']:r for r in early}
    for local,row in zip(config['c_local_seconds'],refs):
        arm=config['first' if local<5 else 'third']
        static,dynamic=mask(arm['static'],arm['crop']),mask(arm['dynamic'],arm['crop'])
        assert static.sum()>=32 and dynamic.sum()>=32 and not (static&dynamic).any()
        targets[row['source_index']]=(working(maps['c_map'][0].parent/row['png'],arm['crop']),static,dynamic)
    comparisons=[];maxscore=maxcoverage=0.;nulls=0
    for row in rows:
        e=early_byid[row['source_index']];ref=ref_byid[row['reference_index']]
        for key in ('pts','time_base'):
            assert row['source_'+key]==e['source_'+key] and row['reference_'+key]==ref['source_'+key]
        with np.load(first/row['surface_file'],allow_pickle=False) as saved:
            assert set(saved.files)=={'static_scores','static_coverage'}
            scores=saved['static_scores'];coverage=saved['static_coverage']
        assert scores.shape==coverage.shape==(21,51,51)
        assert np.isfinite(coverage).all() and coverage.min()>=-COVERAGE_TOL and coverage.max()<=1+COVERAGE_TOL
        finite=np.argwhere(np.isfinite(scores))
        order=sorted(finite.tolist(),key=lambda ijk:(-scores[tuple(ijk)],config['scales'][ijk[0]],ijk[1],ijk[2]))[:2]
        assert len(row['transforms'])==len(order)
        assert row['missing_reason']==(None if order else 'all_static_transforms_invalid')
        target,static,dynamic=targets[row['reference_index']]
        for ordinal,((si,top,left),t) in enumerate(zip(order,row['transforms'])):
            scale=config['scales'][si]
            assert (t['requested_scale'],t['top'],t['left'])==(scale,top,left)
            assert t['dx']==left-25 and t['dy']==top-25
            assert t['translation_boundary']==(left in (0,50) or top in (0,50))
            assert t['scale_boundary']==(si in (0,20))
            assert t['static_score']==float(scores[si,top,left]) and t['static_coverage']==float(coverage[si,top,left])
            a,v,transform=canvas(images[row['source_index']],scale)
            for key,value in transform.items():assert t[key]==value
            x,y=transform['canvas_x'],transform['canvas_y'];w,h=transform['raster_width'],transform['raster_height']
            rectangle=[max(0,x),max(0,y),min(230,x+w),min(170,y+h)]
            assert t['canvas_intersection']==rectangle
            assert t['scaled_raster_intersection']==[rectangle[0]-x,rectangle[1]-y,rectangle[2]-x,rectangle[3]-y]
            assert t['scale_x']==w/180 and t['scale_y']==h/120
            region,valid=a[top:top+120,left:left+180],v[top:top+120,left:left+180]
            s,sc,reason,n=direct(region,target,static,valid)
            assert s is not None and reason is None
            ds,dc,dr,dn=direct(region,target,dynamic,valid)
            score_error=abs(s-t['static_score']);cov_error=abs(sc-t['static_coverage'])
            assert score_error<=SCORE_TOL and cov_error<=COVERAGE_TOL
            d=t['dynamic'];assert d['missing_reason']==dr and d['pixels']==dn
            cov_error=max(cov_error,abs(dc-d['coverage']))
            assert cov_error<=COVERAGE_TOL
            if ds is None:
                assert d['score'] is None;nulls+=1
            else:
                assert d['score'] is not None
                score_error=max(score_error,abs(ds-d['score']));assert score_error<=SCORE_TOL
            maxscore=max(maxscore,score_error);maxcoverage=max(maxcoverage,cov_error)
            comparisons.append({'reference_index':row['reference_index'],'source_index':row['source_index'],'ordinal':ordinal,
                                'static_score':s,'dynamic_score':ds,'dynamic_missing_reason':dr,
                                'max_score_error':score_error,'max_coverage_error':cov_error})
    rankings=json.loads((first/'rankings.json').read_text())
    assert set(rankings)=={str(r['source_index']) for r in refs}
    for ref in refs:
        subset=[r for r in rows if r['reference_index']==ref['source_index']]
        stored=rankings[str(ref['source_index'])];union=set()
        for kind in ('static','dynamic'):
            values=[]
            for r in subset:
                if not r['transforms']:continue
                t=r['transforms'][0];value=t['static_score'] if kind=='static' else t['dynamic']['score']
                if value is not None:values.append((r['source_index'],value))
            values.sort(key=lambda pair:(-pair[1],pair[0]))
            expected_ranking=[{'source_index':i,'score':v} for i,v in values]
            assert stored[kind]['ranking']==expected_ranking
            ids=[i for i,v in values];assert stored[kind]['top_two']==ids[:2];union.update(ids[:2])
            for delta in config['near_best_differences']:
                expected_near=[i for i,v in values if values[0][1]-v<=delta] if values else []
                assert stored[kind]['near_best'][str(delta)]==expected_near
        assert stored['shortlist_union']==sorted(union)
    return {'pairs':len(rows),'selected_transform_checks':len(comparisons),'dynamic_nulls':nulls,
            'max_absolute_score_error':maxscore,'max_absolute_coverage_error':maxcoverage,
            'two_run_products':len(receipts[0]['products']),'comparisons':comparisons,
            'source_map_frames':44,'ranking_groups':6}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--synthetic-only',action='store_true')
    parser.add_argument('--first',type=Path)
    parser.add_argument('--second',type=Path)
    args=parser.parse_args()
    checks=synthetic()
    if args.synthetic_only:
        print(json.dumps({'synthetic_checks':checks,'pass':True}));return
    if args.first is None or args.second is None:raise ValueError('Both completed run directories required')
    destination=HERE/'independent-check.json'
    if destination.exists():raise FileExistsError('Refusing existing independent result')
    result={'status':'started','synthetic_checks':checks,'script':pin(Path(__file__)),
            'preserved_pre_historical_failure':{'receipt':'58f375','exit':1,'phase':'synthetic result JSON serialization','error':'NumPy boolean not JSON serializable','repair':'Convert synthetic check booleans to Python bool; no numerical method or acceptance change'},
            'protocol':pin(HERE/'PROTOCOL.md'),'config':pin(HERE/'config.json'),
            'python':platform.python_version(),'numpy':np.__version__,'pillow':PILLOW_VERSION,
            'score_tolerance':SCORE_TOL,'coverage_tolerance':COVERAGE_TOL,
            'independence':'Separate checker, no producer/core import; shared Pillow resizing, sources, protocol and source-informed code/schema review. No image viewing or historical authentication.'}
    started=time.monotonic()
    try:
        result['verification']=verify(args.first,args.second)
        result['status']='complete'
    except Exception as exc:
        result.update(status='failed',error_type=type(exc).__name__,error=str(exc))
        raise
    finally:
        result['elapsed_s']=time.monotonic()-started
        with destination.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':result['status'],'pairs':result['verification']['pairs']}))


if __name__=='__main__':main()
