#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
import numpy as np
rate=1000

def decode(p):
 b=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-af','highpass=f=80,lowpass=f=400','-ac','1','-ar',str(rate),'-f','s16le','-'])
 return np.frombuffer(b,dtype='<i2').astype(np.float32)/32768
clip=decode(sys.argv[1]); source=decode(sys.argv[2]);shift=6541048;n=5000
results=[]
def corr(a,b):
 a=a-a.mean();b=b-b.mean();d=np.linalg.norm(a)*np.linalg.norm(b)
 return float(np.dot(a,b)/d) if d>1e-9 else None
for start in [0,20,40,60,80]:
 y=clip[start*rate:start*rate+n];i=shift+start*rate
 score=corr(source[i:i+n],y);reverse=corr(source[i:i+n],y[::-1])
 values=[]
 for t in range(0,7141,60):
  if abs(t-6541.048)<10:continue
  j=t*rate+start*rate
  if j+n<=len(source):
   c=corr(source[j:j+n],y)
   if c is not None:values.append(abs(c))
 rank=1+sum(z>=abs(score) for z in values)
 results.append({'clip_start_seconds':start,'target_source_start_seconds':i/rate,'correlation':score,'reversed_correlation':reverse,'absolute_rank':rank,'control_count':len(values),'max_control_absolute':max(values)})
out={'results':results,'target_shift_seconds':6541.048,'disclaimer':'Post-result exploratory held-out windows and local control grid; no inference of clock time or audio contents.'}
with Path('HOLDOUT-RESULTS.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
