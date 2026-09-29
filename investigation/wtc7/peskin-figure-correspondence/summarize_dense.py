"""Summarize all declared dense candidates, not confidence or original clocks."""
import argparse
import json
from pathlib import Path

import dense_match as dense
import match_screen as core

BASE=Path(__file__).resolve().parent


def islands(rows):
    groups=[]
    for row in sorted(rows,key=lambda r:r['global_index']):
        if not groups or row['global_index']!=groups[-1][-1]['global_index']+1:groups.append([])
        groups[-1].append(row)
    return [{'first_pts':g[0]['source_pts'],'last_pts':g[-1]['source_pts'],'count':len(g)} for g in groups]


def controls():
    assert islands([])==[]
    rows=[{'global_index':i,'source_pts':1000+i*33} for i in [0,1,3,4,8]]
    assert islands(rows)==[{'first_pts':1000,'last_pts':1033,'count':2},
                          {'first_pts':1099,'last_pts':1132,'count':2},
                          {'first_pts':1264,'last_pts':1264,'count':1}]
    assert islands(rows[::-1])==islands(rows)
    return 3


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--require-reproduction',action='store_true');a=p.parse_args()
    checks=controls();all_rows=[];frames=[];pins={};reference=None;reproductions=[]
    for chunk,interval in enumerate(dense.CHUNKS):
        name=dense.PRODUCTION_RUNS[chunk];folder=BASE/name
        receipt=json.loads((folder/'receipt.json').read_text())
        if receipt['status']!='completed' or receipt['interval']!=list(interval):raise ValueError('chunk status/interval')
        if receipt['source_before']!=receipt['source_after'] or receipt['source_before']['sha256']!=dense.VIDEO_HASH:raise ValueError('source identity')
        expected_runner='8c5c92932c43183d0861e16282f95e7be360a36bd9ee016c639e638ebed82bb1' if chunk==0 else core.sha(dense.__file__)
        if receipt['script_sha256']!=expected_runner:raise ValueError('undeclared runner version')
        shared_pins={k:v for k,v in dense.PINS.items() if k!='DENSE-CONTINUATION-02.md'}
        if any(receipt['dependency_pins'].get(k)!=v for k,v in shared_pins.items()):raise ValueError('shared method pins')
        identity={k:receipt[k] for k in ['core_sha256','tools','numpy','pillow','python']}
        if reference is None:reference=identity
        if identity!=reference:raise ValueError('mixed dense versions')
        for f in ['frames.json','results.json']:
            pin=receipt['outputs'][f];path=folder/f
            if path.stat().st_size!=pin['bytes'] or core.sha(path)!=pin['sha256']:raise ValueError('input changed')
        ff=json.loads((folder/'frames.json').read_text());rr=json.loads((folder/'results.json').read_text())
        if len(ff)!=receipt['frame_count'] or not 1<=len(ff)<=275 or len(rr)!=2*len(ff):raise ValueError('frame/result counts')
        if [r['frame_index'] for r in ff]!=list(range(len(ff))):raise ValueError('frame order')
        if {(r['frame_index'],r['target']) for r in rr}!={(i,key) for i in range(len(ff)) for key in core.TARGETS}:raise ValueError('target coverage')
        for row in rr:
            f=ff[row['frame_index']]
            if row['source_pts']!=f['source_pts'] or row['source_time_base']!='1/1000':raise ValueError('PTS join')
            row.update(global_index=len(frames)+row['frame_index'],run=name)
            native=folder/f"native-{row['frame_index']:04d}.png"
            if native.exists():row['native_png']=str(native)
            all_rows.append(row)
        frames.extend(ff);pins[name]=core.sha(folder/'receipt.json')
        repro=BASE/name.replace('dense','repro')/'receipt.json'
        if a.require_reproduction:
            r=json.loads(repro.read_text())
            if r['status']!='completed' or r['compare_to']!=name:raise ValueError('reproduction status')
            if r['script_sha256']!=expected_runner or r['dependency_pins']!=receipt['dependency_pins']:raise ValueError('reproduction runner/method')
            if r['reproduction_surface_comparisons']!=len(rr) or r['reproduction_native_pixel_matches']!=len(receipt['native_images']):raise ValueError('reproduction counts')
            for key,value in identity.items():
                if r[key]!=value:raise ValueError('reproduction version')
            reproductions.append({'run':repro.parent.name,'receipt_sha256':core.sha(repro)})
    pts=[r['source_pts'] for r in frames]
    if len(pts)>1100 or pts!=sorted(set(pts)):raise ValueError('combined frame coverage')
    result={}
    for key in core.TARGETS:
        rows=[r for r in all_rows if r['target']==key and r['geometry_candidates']]
        result[key]={}
        for metric in ['static_score','dynamic_score']:
            eligible=[r for r in rows if r['geometry_candidates'][0][metric] is not None]
            ranked=sorted(eligible,key=lambda r:(-r['geometry_candidates'][0][metric],r['source_pts']))
            if not ranked:
                result[key][metric]={'eligible_count':0,'top_four':[],'best_score':None,
                    'descriptive_score_bands':{str(delta):[] for delta in [.005,.01,.02]}}
                continue
            best=ranked[0]['geometry_candidates'][0][metric]
            result[key][metric]={'eligible_count':len(eligible),'top_four':ranked[:4],'best_score':best,
                'descriptive_score_bands':{str(delta):islands([r for r in eligible if r['geometry_candidates'][0][metric]>=best-delta]) for delta in [.005,.01,.02]}}
    data={'status':'completed','script_sha256':core.sha(__file__),'controls_passed':checks,
          'frame_count':len(frames),'comparison_count':len(all_rows),'source_time_base':'1/1000',
          'first_pts':pts[0],'last_pts':pts[-1],'chunk_receipt_pins':pins,'reproductions':reproductions,
          'results':result,'limits':'Fixed-transform candidate rankings and descriptive bands only; not exposure identity, clock authentication, confidence intervals, fire temperatures or causal ranking.'}
    core.save(a.output,data)
    print(json.dumps({'status':'completed','frames':len(frames),'comparisons':len(all_rows),
        'best_pts':{key:{m:result[key][m]['top_four'][0]['source_pts'] if result[key][m]['top_four'] else None for m in result[key]} for key in result}}))


if __name__=='__main__':main()
