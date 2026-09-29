"""Stream pinned media as data; dense candidate search, not historical timing."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import signal
import subprocess
import sys
import threading
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image

import match_screen as core

BASE = Path(__file__).resolve().parent
SOURCE = core.MAIN/'fire-originals/peskin/sources/peskin-commons-resumed.webm'
VIDEO_HASH = '0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d'
CORE_HASH = '06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8'
FRAME_INDEX_HASH = '8dc374556367b22a20f91567ac1461fa04fe8f0b66ab757586c33ca7d00108df'
FFMPEG, FFPROBE = '/opt/homebrew/bin/ffmpeg', '/opt/homebrew/bin/ffprobe'
CHUNKS = [(2502,2510),(2510,2518),(2518,2526),(2526,2534)]
WIDTH, HEIGHT = 1620,1080
PINS = {
    'PROTOCOL.md':'e445a976b664e6d2bd8c619d415cf0c1eb0ccc4866743082231b34f0a0f00537',
    'METHOD-01.md':'412c7aae4da6010d4323d900182c8419dc314fd64953ed9c2c3878b3bd335e6c',
    'DENSE-01.md':'8a7ac08aa7901c0de5956b617950f9fda35a786b7a9b58a26c7ba54c785413f8',
    'DENSE-GATES-01.md':'8d0c5bae4654c99813d0d896989963c2b557e80e87a160cbedc5edcebce3ebda',
    'controls01/summary.json':'175019b3d873ea8632ea14dd4cec1fd4dc35b6c3f9557dab7503491d4e7ffcc7',
    'direct_oracle.py':'f1ecbbb6fc4c48c58786d43287ac65cdeb1a3428b93ca0ae5bec6bccf43a4e71',
    'fixtures/producer-comparison01.json':'db673cc6d6a4fc11fc6026ffa1688ce35fd5934b83fcc7067f556b72b647f136',
}
SLOTS = {f'{kind}{i:02d}':limit*1024**2 for kind,limit in [('dense',450),('repro',10)] for i in range(4)}


def storage_check():
    totals={name:0 for name in SLOTS};baseline=0
    for f in BASE.rglob('*'):
        if f.is_symlink():raise ValueError('unit symlink not permitted')
        if f.is_file():
            top=f.relative_to(BASE).parts[0];size=f.stat().st_size
            if top in totals:totals[top]+=size
            else:baseline+=size
    if baseline>150*1024**2 or any(totals[k]>SLOTS[k] for k in totals):raise ValueError('slot/baseline storage cap')
    if baseline+sum(totals.values())>2*1024**3:raise ValueError('aggregate storage cap')
    return {'baseline_bytes':baseline,'slot_bytes':totals}


def alarm_handler(signum, frame):
    raise TimeoutError('overall process budget')


def digest(b):return hashlib.sha256(b).hexdigest()


def get_shortlist(rows):
    selected=set()
    for target in core.TARGETS:
        rr=[r for r in rows if r['target']==target and r['geometry_candidates']]
        for metric in ('static_score','dynamic_score'):
            valid=[r for r in rr if r['geometry_candidates'][0][metric] is not None]
            selected.update(r['frame_index'] for r in sorted(valid,key=lambda r:(-r['geometry_candidates'][0][metric],r['frame_index']))[:4])
    return selected


def parse_showinfo(text, count, start, end):
    pattern=r'\[Parsed_showinfo_[^\]]+\]\s+n:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([^ ]+).*?\bs:(\d+)x(\d+)\b'
    matches=re.findall(pattern,text)
    bases=re.findall(r'config in time_base: (\d+/\d+)',text)
    if not bases or set(bases)!={'1/1000'} or len(matches)!=count:raise ValueError('PTS count/timebase')
    rows=[]
    for i,(n,pts,shown,w,h) in enumerate(matches):
        pts=int(pts);seconds=Fraction(pts,1000)
        if int(n)!=i or (int(w),int(h))!=(WIDTH,HEIGHT) or not start<=seconds<end:raise ValueError('PTS order/geometry/interval')
        displayed=float(shown)
        if not math.isfinite(displayed) or abs(float(seconds)-displayed)>.01:raise ValueError('PTS display mismatch')
        if rows and pts<=rows[-1]['source_pts']:raise ValueError('nonincreasing PTS')
        rows.append({'frame_index':i,'source_pts':pts,'source_time_base':'1/1000'})
    return rows


def main():
    p=argparse.ArgumentParser();p.add_argument('--chunk',type=int,choices=range(4),required=True)
    p.add_argument('--run',required=True);p.add_argument('--compare-to');a=p.parse_args()
    for s in (a.run,a.compare_to):
        if s is not None and not re.fullmatch(r'[a-z][a-z0-9]{1,24}',s):raise ValueError('unsafe run name')
    if a.run!=f'{"repro" if a.compare_to else "dense"}{a.chunk:02d}':raise ValueError('undeclared run slot')
    if a.compare_to and a.compare_to!=f'dense{a.chunk:02d}':raise ValueError('wrong comparison slot')
    out=BASE/a.run;out.mkdir(exist_ok=False);start,end=CHUNKS[a.chunk]
    receipt={'status':'started','interval':[start,end],'script_sha256':core.sha(__file__),
             'core_sha256':core.sha(core.__file__),'dense_protocol_sha256':core.sha(BASE/'DENSE-01.md'),
             'protocol_sha256':core.sha(BASE/'PROTOCOL.md'),'commands':[],'compare_to':a.compare_to,
             'numpy':np.__version__,'pillow':Image.__version__,'python':sys.version,'argv':sys.argv}
    core.save(out/'start.json',receipt);begin=time.monotonic();proc=None;timer=None
    prior=None;prior_native={};native_verified=[];written_budget=0
    old_handler=signal.signal(signal.SIGALRM,alarm_handler)
    signal.setitimer(signal.ITIMER_REAL,300)
    try:
        if receipt['core_sha256']!=CORE_HASH:raise ValueError('core version changed')
        for name,pin in PINS.items():
            if core.sha(BASE/name)!=pin:raise ValueError('frozen dependency pin changed')
        receipt['dependency_pins']=PINS;receipt['storage_before']=storage_check()
        control=json.loads((BASE/'controls01/summary.json').read_text())
        if not control['pass'] or control['script_sha256']!=CORE_HASH:raise ValueError('control gate')
        if SOURCE.stat().st_size!=696711067 or core.sha(SOURCE)!=VIDEO_HASH:raise ValueError('video pin')
        receipt['source_before']={'bytes':SOURCE.stat().st_size,'sha256':VIDEO_HASH}
        receipt['tools']={}
        for tool in (FFMPEG,FFPROBE):
            v=subprocess.run([tool,'-version'],capture_output=True,check=True,timeout=10)
            receipt['tools'][Path(tool).name]={'sha256':core.sha(tool),'version':v.stdout.decode().splitlines()[0]}
        if a.compare_to:
            prior=json.loads((BASE/a.compare_to/'receipt.json').read_text())
            if prior['status']!='completed' or prior['compare_to'] is not None:raise ValueError('prior not completed production')
            for field in ('interval','script_sha256','core_sha256','dense_protocol_sha256','protocol_sha256','dependency_pins','source_before','tools','numpy','pillow','python'):
                if prior[field]!=receipt[field]:raise ValueError('prior identity mismatch')
            if not 1<=prior['frame_count']<=275:raise ValueError('prior count outside cap')
            manifests=prior['outputs']
            expected={f'scores-{key}-{i:04d}.npz' for key in core.TARGETS for i in range(prior['frame_count'])}
            expected|={'start.json','decode.stderr.txt','frame-probe.json','frame-probe.stderr.txt','frames.json','results.json'}
            expected|={r['path'] for r in prior['native_images']}
            if set(manifests)!=expected:raise ValueError('prior manifest membership')
            for name,entry in manifests.items():
                if Path(name).name!=name:raise ValueError('prior manifest path')
                f=BASE/a.compare_to/name
                if f.is_symlink() or f.stat().st_size!=entry['bytes'] or core.sha(f)!=entry['sha256']:raise ValueError('prior output integrity')
            prior_native={r['frame_index']:r for r in prior['native_images']}
            if sorted(prior_native)!=prior['shortlist_indices'] or len(prior_native)>16 or len(prior_native)!=len(prior['native_images']):raise ValueError('prior native membership')
            for i,r in prior_native.items():
                if r['path']!=f'native-{i:04d}.png' or not 0<=i<prior['frame_count']:raise ValueError('prior native path/index')
                if {k:r[k] for k in ('bytes','sha256')}!=manifests[r['path']]:raise ValueError('prior native pin mismatch')
        fp=core.MAIN/'fire-originals/peskin/derivatives/run01/frames.json'
        if core.sha(fp)!=FRAME_INDEX_HASH:raise ValueError('frame index pin')
        anchors={r['source_pts']:r for r in json.loads(fp.read_text()) if start<=Fraction(r['source_pts'],1000)<end}
        if len(anchors)!=8:raise ValueError('anchor coverage')
        anchor_pixels={}
        for pts,r in anchors.items():
            f=fp.parent/r['png']
            if core.sha(f)!=r['sha256']:raise ValueError('anchor PNG pin')
            with Image.open(f) as im:anchor_pixels[pts]=digest(im.convert('RGB').tobytes())
        targets={}
        for key,(asset,h,sboxes,dboxes) in core.TARGETS.items():
            f=core.MAIN/'fire-annotation/assets/run-01/images'/f'{asset}.jpg'
            if core.sha(f)!=h:raise ValueError('target pin')
            with Image.open(f) as im:targets[key]=(core.working(im),core.mask_for(sboxes),core.mask_for(dboxes))
        argv=[FFMPEG,'-nostdin','-hide_banner','-loglevel','info','-copyts','-seek_timestamp','1','-noaccurate_seek',
              '-ss',str(start-2),'-t','12','-noautorotate','-i',str(SOURCE),'-map','0:v:0','-an',
              '-vf',f"select='gte(t,{start})*lt(t,{end})',showinfo",'-noautoscale','-pix_fmt','rgb24',
              '-fps_mode','passthrough','-enc_time_base:v','demux','-f','rawvideo','pipe:1']
        receipt['commands'].append(argv)
        rows=[];pixel_rows=[];retained={};comparisons=0;size=WIDTH*HEIGHT*3
        with (out/'decode.stderr.txt').open('xb') as err:
            proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=err)
            timer=threading.Timer(max(1,270-(time.monotonic()-begin)),proc.kill);timer.start()
            for i in range(276):
                if time.monotonic()-begin>275:raise ValueError('wall budget')
                raw=proc.stdout.read(size)
                if not raw:break
                if len(raw)!=size or i==275:raise ValueError('partial frame/frame cap')
                im=Image.frombytes('RGB',(WIDTH,HEIGHT),raw);work=core.working(im)
                pixel_rows.append({'frame_index':i,'decoded_rgb_sha256':digest(raw)})
                if i in prior_native:
                    with Image.open(BASE/a.compare_to/prior_native[i]['path']) as old_image:
                        if old_image.size!=(WIDTH,HEIGHT) or digest(old_image.convert('RGB').tobytes())!=digest(raw):raise ValueError('native decoded pixel reproduction mismatch')
                    native_verified.append(i)
                for key,args in targets.items():
                    best,scores,overlap=core.register(work,*args)
                    filename=f'scores-{key}-{i:04d}.npz'
                    if a.compare_to:
                        with np.load(BASE/a.compare_to/filename,allow_pickle=False) as old:
                            if not np.array_equal(scores,old['scores'],equal_nan=True) or not np.array_equal(overlap,old['overlap'],equal_nan=True):raise ValueError('reproduction surface mismatch')
                        comparisons+=1
                    else:
                        if written_budget+scores.nbytes+overlap.nbytes+100000+16*(size+1000000)+10*1024**2>SLOTS[a.run]:raise ValueError('conservative output budget')
                        with (out/filename).open('xb') as stream:np.savez_compressed(stream,scores=scores,overlap=overlap)
                        written_budget+=(out/filename).stat().st_size
                    rows.append({'frame_index':i,'target':key,'geometry_candidates':best})
                selected=get_shortlist(rows)
                if not a.compare_to:
                    if i in selected:retained[i]=raw
                    retained={j:b for j,b in retained.items() if j in selected}
                if i%80==79:
                    print(json.dumps({'status':'running','chunk':a.chunk,'frames':i+1}),flush=True)
                    if sum(f.stat().st_size for f in out.rglob('*') if f.is_file())>SLOTS[a.run]:raise ValueError('chunk storage cap')
            proc.stdout.close();code=proc.wait(timeout=10);timer.cancel()
        if code:raise ValueError('decode exit')
        log=(out/'decode.stderr.txt').read_text(errors='replace')
        if re.search(r'corrupt|invalid data|error|warning|conceal',log,re.I):raise ValueError('decode warning gate')
        times=parse_showinfo(log,len(pixel_rows),start,end)
        if not times:raise ValueError('empty interval')
        probe=[FFPROBE,'-v','error','-read_intervals',f'{start-2}%{end+1}','-select_streams','v:0',
               '-show_frames','-show_entries','frame=pts,best_effort_timestamp,width,height','-of','json',str(SOURCE)]
        receipt['commands'].append(probe);pr=subprocess.run(probe,capture_output=True,timeout=20)
        (out/'frame-probe.json').write_bytes(pr.stdout);(out/'frame-probe.stderr.txt').write_bytes(pr.stderr)
        if pr.returncode or pr.stderr.strip():raise ValueError('frame probe diagnostic')
        probed=[]
        for r in json.loads(pr.stdout)['frames']:
            if 'pts' not in r or 'best_effort_timestamp' not in r:raise ValueError('missing probe timestamp')
            if start<=Fraction(r['pts'],1000)<end:
                if r['pts']!=r['best_effort_timestamp'] or (r['width'],r['height'])!=(WIDTH,HEIGHT):raise ValueError('probe field mismatch')
                probed.append(r['pts'])
        if probed!=[r['source_pts'] for r in times]:raise ValueError('probe/filter PTS list mismatch')
        for r,t in zip(pixel_rows,times):r.update(t)
        actual={r['source_pts']:r['decoded_rgb_sha256'] for r in pixel_rows if r['source_pts'] in anchors}
        if actual!=anchor_pixels:raise ValueError('anchor decoded pixel mismatch')
        for r in rows:r.update(times[r['frame_index']])
        if len(retained)>16:raise ValueError('shortlist image cap')
        native=[]
        for i,raw in sorted(retained.items()):
            f=out/f'native-{i:04d}.png';Image.frombytes('RGB',(WIDTH,HEIGHT),raw).save(f)
            native.append({'frame_index':i,'path':f.name,'sha256':core.sha(f),'bytes':f.stat().st_size})
        if a.compare_to:
            if sorted(get_shortlist(rows))!=prior['shortlist_indices']:raise ValueError('prior shortlist disagrees with reproduced ranking')
            if len(times)!=prior['frame_count'] or sorted(native_verified)!=prior['shortlist_indices']:raise ValueError('reproduction coverage mismatch')
            if pixel_rows!=json.loads((BASE/a.compare_to/'frames.json').read_text()) or rows!=json.loads((BASE/a.compare_to/'results.json').read_text()):raise ValueError('reproduction row/pixel mismatch')
        core.save(out/'frames.json',pixel_rows);core.save(out/'results.json',rows)
        if core.sha(SOURCE)!=VIDEO_HASH:raise ValueError('source changed')
        output_bytes=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
        if output_bytes+1024**2>SLOTS[a.run]:raise ValueError('final storage cap with receipt reserve')
        receipt.update(status='completed',source_after={'bytes':SOURCE.stat().st_size,'sha256':VIDEO_HASH},
                       frame_count=len(times),first_pts=times[0]['source_pts'],last_pts=times[-1]['source_pts'],
                       anchor_pixel_matches=len(actual),frame_probe_matches=len(probed),native_images=native,
                       reproduction_surface_comparisons=comparisons,output_bytes=output_bytes,
                       reproduction_native_pixel_matches=len(native_verified),
                       elapsed_seconds=time.monotonic()-begin,shortlist_indices=sorted(get_shortlist(rows)))
        receipt['outputs']={f.name:{'bytes':f.stat().st_size,'sha256':core.sha(f)} for f in out.iterdir() if f.is_file()}
        receipt['storage_after']=storage_check()
        receipt['elapsed_seconds']=time.monotonic()-begin
        if receipt['elapsed_seconds']>300:raise ValueError('final wall budget')
        core.save(out/'receipt.json',receipt)
        print(json.dumps({'status':'completed','chunk':a.chunk,'frames':len(times),'anchors':len(actual),'elapsed_seconds':receipt['elapsed_seconds']}))
    except Exception as e:
        receipt.update(status='failed',exception_type=type(e).__name__,elapsed_seconds=time.monotonic()-begin,
                       message=str(e) if isinstance(e,ValueError) else 'Inspect local diagnostics without exporting metadata')
        core.save(out/'failure.json',receipt);print(json.dumps({'status':'failed','chunk':a.chunk,'type':type(e).__name__}));raise SystemExit(1)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old_handler)
        if timer:timer.cancel()
        if proc and proc.poll() is None:proc.kill();proc.wait(timeout=10)


if __name__=='__main__':main()
