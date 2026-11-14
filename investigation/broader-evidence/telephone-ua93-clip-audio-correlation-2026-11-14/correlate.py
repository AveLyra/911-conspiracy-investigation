#!/usr/bin/env python3
"""Experimental waveform location only; see PLAN.json. Paths are local, not uploaded."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
rate=1000
clip_path=Path(sys.argv[1]); sources=[Path(x) for x in sys.argv[2:]]

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def decode(p):
 b=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-af','highpass=f=80,lowpass=f=400','-ac','1','-ar',str(rate),'-f','s16le','-'])
 return np.frombuffer(b,dtype='<i2').astype(np.float32)/32768.0
cliphash=sha(clip_path)
assert cliphash=='c2ca0fa51b17036457449285871d1f337e6e0d31588af1792133b18a2a7f76f5'
clip=decode(clip_path)
expected=['9de37587fd7ea43934225f60db118cb3c67e97b103aefeb243b1bbc4827d1c82','e887c08dd70a295f91089dddb1f0b2756edfeae1a269ea48631f0bf37972d2d5']
assert len(sources)==2
out={'sample_rate':rate,'inputs':{'clip_sha256':cliphash},'windows_seconds':[10,30,50,70],'window_seconds':5,'sources':[]}
for path,exp in zip(sources,expected):
 actual=sha(path);assert actual==exp
 x=decode(path);n=5*rate
 sx=np.concatenate(([0.0],np.cumsum(x,dtype=np.float64)))
 sq=np.concatenate(([0.0],np.cumsum(x*x,dtype=np.float64)))
 moving_sum=sx[n:]-sx[:-n];energy=np.maximum(sq[n:]-sq[:-n]-moving_sum*moving_sum/n,0.0)
 denom=np.sqrt(energy)
 results=[]
 for start in [10,30,50,70,-10]:
  y=clip[abs(start)*rate:abs(start)*rate+n].copy()
  if start<0:y=y[::-1].copy()
  y-=y.mean();ynorm=float(np.linalg.norm(y))
  if ynorm<1e-7: raise RuntimeError('clip window is silent')
  raw=fftconvolve(x,y[::-1],mode='valid')
  cor=np.divide(raw,denom*ynorm,out=np.zeros_like(raw),where=denom>1e-6)
  index=int(np.argmax(np.abs(cor)));score=float(cor[index])
  results.append({'clip_offset_seconds':abs(start),'reverse_control':start<0,'clip_rms':round(ynorm/(n**0.5),8),'source_offset_seconds':index/rate,'correlation':score,'source_minus_clip_seconds':round(index/rate-abs(start),3)})
  del raw,cor
 main=[r for r in results if not r['reverse_control'] and abs(r['correlation'])>=0.25]
 cluster=max(([r for r in main if abs(r['source_minus_clip_seconds']-a['source_minus_clip_seconds'])<=0.2] for a in main),key=len,default=[])
 out['sources'].append({'sha256':actual,'decoded_seconds':len(x)/rate,'windows':results,'qualifying_consistent_window_count':len(cluster),'predeclared_match':len(cluster)>=3})
 print(json.dumps(out['sources'][-1]),flush=True)
 del x,sx,sq,moving_sum,energy,denom
with Path('RESULTS.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
