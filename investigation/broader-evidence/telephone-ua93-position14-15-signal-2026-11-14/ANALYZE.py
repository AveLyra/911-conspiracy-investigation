#!/usr/bin/env python3
"""Bounded waveform search; see PLAN.json. Does not transcribe or calibrate time."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
if len(sys.argv)!=4: raise SystemExit('Usage: ANALYZE.py EXCERPT.mp3 POSITION14.mp3 POSITION15.mp3')
expected=['c2ca0fa51b17036457449285871d1f337e6e0d31588af1792133b18a2a7f76f5','20bc0d4c08fbb78f784a8e18b24a402926d3ea56bfa1bdaa88392035903f4ace','27eb01802a6ff6c0c75f2046ec10ec5d4052bf783dfb9df617cba5e2a4bfb71e']
paths=[Path(x) for x in sys.argv[1:]]
for p,e in zip(paths,expected):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 assert h.hexdigest()==e, 'Source hash mismatch'

def decode(path,source):
 cmd=['ffmpeg','-hide_banner','-loglevel','error']
 if source:cmd+=['-ss','6200']
 cmd+=['-i',str(path)]
 if source:cmd+=['-t','700']
 af='pan=mono|c0=c0,highpass=f=80,lowpass=f=400' if source else 'highpass=f=80,lowpass=f=400'
 cmd+=['-af',af,'-ac','1','-ar','1000','-f','s16le','-']
 return np.frombuffer(subprocess.check_output(cmd),dtype='<i2').astype(np.float32)/32768
clip=decode(paths[0],False)
results={'search_window':[6200,6900],'recordings':[]}
for path,sha in zip(paths[1:],expected[1:]):
 x=decode(path,True)
 sx=np.concatenate(([0.0],np.cumsum(x,dtype=np.float64)));sq=np.concatenate(([0.0],np.cumsum(x*x,dtype=np.float64)))
 windows=[]
 for start in [10,30,50,70,-10]:
  orig=clip[abs(start)*1000:(abs(start)+5)*1000]
  if start<0:orig=orig[::-1]
  candidates=[]
  for scale in ([1.0] if start<0 else [0.99,0.995,1.0,1.005,1.01]):
   count=round(len(orig)*scale);y=np.interp(np.arange(count)/scale,np.arange(len(orig)),orig).astype(np.float32);y-=y.mean();n=len(y);yn=float(np.linalg.norm(y))
   sums=sx[n:]-sx[:-n];denom=np.sqrt(np.maximum(sq[n:]-sq[:-n]-sums*sums/n,0))*yn
   raw=fftconvolve(x,y[::-1],mode='valid');co=np.divide(raw,denom,out=np.zeros_like(raw),where=denom>1e-7)
   ind=int(np.argmax(np.abs(co)));candidates.append({'scale':scale,'source_offset':round(6200+ind/1000,3),'coefficient':float(co[ind]),'source_minus_scaled_clip':round(6200+ind/1000-abs(start)*scale,3)})
  best=max(candidates,key=lambda t:abs(t['coefficient']))
  windows.append({'clip_start_seconds':abs(start),'reverse_control':start<0,'best':best,'all_scale_candidates':candidates})
 main=[r for r in windows if not r['reverse_control'] and abs(r['best']['coefficient'])>=0.25]
 clusters=[[r for r in main if abs(r['best']['source_minus_scaled_clip']-a['best']['source_minus_scaled_clip'])<=0.4] for a in main]
 count=max(map(len,clusters),default=0)
 entry={'source_sha256':sha,'decoded_window_seconds':len(x)/1000,'windows':windows,'qualifying_consistent_windows':count,'predeclared_match':count>=3};results['recordings'].append(entry)
 print(json.dumps({'sha256':sha,'windows':[{'clip':r['clip_start_seconds'],'reverse':r['reverse_control'],**r['best']} for r in windows],'qualifying_count':count,'match':count>=3}),flush=True)
with Path('RESULTS.json').open('x') as f:json.dump(results,f,indent=2);f.write('\n')
