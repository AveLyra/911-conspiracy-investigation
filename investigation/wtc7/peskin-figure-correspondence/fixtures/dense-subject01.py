"""Stream pinned media as data; dense candidate search, not historical timing."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
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
        if abs(float(seconds)-float(shown))>.01:raise ValueError('PTS display mismatch')
        if rows and pts<=rows[-1]['source_pts']:raise ValueError('nonincreasing PTS')
        rows.append({'frame_index':i,'source_pts':pts,'source_time_base':'1/1000'})
    return rows


def main():
    p=argparse.ArgumentParser();p.add_argument('--chunk',type=int,choices=range(4),required=True)
    p.add_argument('--run',required=True);p.add_argument('--compare-to');a=p.parse_args()
    for s in (a.run,a.compare_to):
        if s is not None and not re.fullmatch(r'[a-z][a-z0-9]{1,24}',s):raise ValueError('unsafe run name')
    out=BASE/a.run;out.mkdir(exist_ok=False);start,end=CHUNKS[a.chunk]
    receipt={'status':'started','interval':[start,end],'script_sha256':core.sha(__file__),
             'core_sha256':core.sha(core.__file__),'dense_protocol_sha256':core.sha(BASE/'DENSE-01.md'),
             'protocol_sha256':core.sha(BASE/'PROTOCOL.md'),'commands':[],'compare_to':a.compare_to,
             'numpy':np.__version__,'pillow':Image.__version__}
    core.save(out/'start.json',receipt);begin=time.monotonic();proc=None;timer=None
    try:
        if receipt['core_sha256']!=CORE_HASH:raise ValueError('core version changed')
        control=json.loads((BASE/'controls01/summary.json').read_text())
        if not control['pass'] or control['script_sha256']!=CORE_HASH:raise ValueError('control gate')
        if SOURCE.stat().st_size!=696711067 or core.sha(SOURCE)!=VIDEO_HASH:raise ValueError('video pin')
        receipt['source_before']={'bytes':SOURCE.stat().st_size,'sha256':VIDEO_HASH}
        receipt['tools']={}
        for tool in (FFMPEG,FFPROBE):
            v=subprocess.run([tool,'-version'],capture_output=True,check=True,timeout=10)
            receipt['tools'][Path(tool).name]={'sha256':core.sha(tool),'version':v.stdout.decode().splitlines()[0]}
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
            for i in range(551):
                if time.monotonic()-begin>275:raise ValueError('wall budget')
                raw=proc.stdout.read(size)
                if not raw:break
                if len(raw)!=size or i==550:raise ValueError('partial frame/frame cap')
                im=Image.frombytes('RGB',(WIDTH,HEIGHT),raw);work=core.working(im)
                pixel_rows.append({'frame_index':i,'decoded_rgb_sha256':digest(raw)})
                for key,args in targets.items():
                    best,scores,overlap=core.register(work,*args)
                    filename=f'scores-{key}-{i:04d}.npz'
                    if a.compare_to:
                        with np.load(BASE/a.compare_to/filename,allow_pickle=False) as old:
                            if not np.array_equal(scores,old['scores'],equal_nan=True) or not np.array_equal(overlap,old['overlap'],equal_nan=True):raise ValueError('reproduction surface mismatch')
                        comparisons+=1
                    else:
                        with (out/filename).open('xb') as stream:np.savez_compressed(stream,scores=scores,overlap=overlap)
                    rows.append({'frame_index':i,'target':key,'geometry_candidates':best})
                selected=get_shortlist(rows)
                if not a.compare_to:
                    if i in selected:retained[i]=raw
                    retained={j:b for j,b in retained.items() if j in selected}
                if i%80==79:
                    print(json.dumps({'status':'running','chunk':a.chunk,'frames':i+1}),flush=True)
                    if sum(f.stat().st_size for f in out.rglob('*') if f.is_file())>450*1024**2:raise ValueError('chunk storage cap')
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
            if pixel_rows!=json.loads((BASE/a.compare_to/'frames.json').read_text()) or rows!=json.loads((BASE/a.compare_to/'results.json').read_text()):raise ValueError('reproduction row/pixel mismatch')
        core.save(out/'frames.json',pixel_rows);core.save(out/'results.json',rows)
        if core.sha(SOURCE)!=VIDEO_HASH:raise ValueError('source changed')
        output_bytes=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
        if output_bytes>450*1024**2:raise ValueError('final storage cap')
        receipt.update(status='completed',source_after={'bytes':SOURCE.stat().st_size,'sha256':VIDEO_HASH},
                       frame_count=len(times),first_pts=times[0]['source_pts'],last_pts=times[-1]['source_pts'],
                       anchor_pixel_matches=len(actual),frame_probe_matches=len(probed),native_images=native,
                       reproduction_surface_comparisons=comparisons,output_bytes=output_bytes,
                       elapsed_seconds=time.monotonic()-begin,shortlist_indices=sorted(get_shortlist(rows)))
        if receipt['elapsed_seconds']>300:raise ValueError('final wall budget')
        core.save(out/'receipt.json',receipt)
        print(json.dumps({'status':'completed','chunk':a.chunk,'frames':len(times),'anchors':len(actual),'elapsed_seconds':receipt['elapsed_seconds']}))
    except Exception as e:
        receipt.update(status='failed',exception_type=type(e).__name__,elapsed_seconds=time.monotonic()-begin,
                       message=str(e) if isinstance(e,ValueError) else 'Inspect local diagnostics without exporting metadata')
        core.save(out/'failure.json',receipt);print(json.dumps({'status':'failed','chunk':a.chunk,'type':type(e).__name__}));raise SystemExit(1)
    finally:
        if timer:timer.cancel()
        if proc and proc.poll() is None:proc.kill();proc.wait(timeout=10)


if __name__=='__main__':main()
