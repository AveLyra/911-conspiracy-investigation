"""Read-only, same-decoder signal comparison, never playback or historical clocks.

python compare_decoded_signals.py /path/to/court-flights.zip --helper PATH
Requires local ffmpeg/ffprobe and NumPy; makes no network call or media file.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import struct
import subprocess
import sys
import zipfile
import numpy as np

ARCHIVE_SHA='3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801'
HELPER_SHA='2af3d0339c5ca876255948a014205f8caa6ff019c1303e79a0ba774a22f36ade'
EXPECTED={
 'Lyles.swf':{'member':'28f2a83db87177a2538ebd36ddfc03b63e7b696b7d16603a793921ff27ce4ec7','event':'53d4d3256cf941cb2ad659e4bfdaed341e440d4dfa1484a3c84b2e07210e197e','stream':'b01692e3acebe4731d1c863da1162a70b2bc21cad3d99f913a3810bb10b9be92'},
 'Ong.swf':{'member':'8c844a2370852e55597a4aa73ef8b8ff0e6c03e3fec982a9cd98aeb937e5a3ec','event':'b1340270d0e8f4b159bb4b057ea57ec227cd021fb12dc5fd37a46b7e3e9b78b5','stream':'076067d2fe207c9efb95d62ed0a1cc33f24df2f60568cdf143631885b15fcfcd'}}
RATE=8000
MAX_NFFT=2**22
DIRECT_TOL=1e-9

def sha(b):return hashlib.sha256(b).hexdigest()

def pearson(x,y):
    x=x-x.mean();y=y-y.mean();den=float(np.linalg.norm(x)*np.linalg.norm(y))
    return None if den==0 else float(np.dot(x,y)/den)

def search(x,y,maxlag,min_overlap,exclude=2000):
    nx,ny=len(x),len(y);need=nx+ny-1;nfft=1<<(need-1).bit_length()
    if nfft>MAX_NFFT:raise ValueError('FFT scope exceeds2^22')
    lo=max(-maxlag,-ny+1);hi=min(maxlag,nx-1);lags=np.arange(lo,hi+1,dtype=np.int64)
    a=np.maximum(0,lags);b=np.minimum(nx,lags+ny);c=a-lags;d=b-lags;n=b-a
    def prefix(z):return np.concatenate(([0.0],np.cumsum(z,dtype=np.float64)))
    px,py=prefix(x),prefix(y);qx,qy=prefix(x*x),prefix(y*y)
    sx,sy=px[b]-px[a],py[d]-py[c];xx,yy=qx[b]-qx[a],qy[d]-qy[c]
    dot=np.fft.irfft(np.fft.rfft(x,nfft)*np.fft.rfft(y[::-1],nfft),nfft)[lags+ny-1]
    vx=xx-sx*sx/n;vy=yy-sy*sy/n;valid=(n>=min_overlap)&(vx>1e-20)&(vy>1e-20)
    corr=np.full(len(lags),np.nan);corr[valid]=(dot[valid]-sx[valid]*sy[valid]/n[valid])/np.sqrt(vx[valid]*vy[valid])
    if not np.any(valid):return {'status':'no_valid_overlap_or_variance','candidate_lags':len(lags),'eligible_lags':0}
    masked=np.where(valid,np.abs(corr),-np.inf);i=int(np.argmax(masked));j=int(np.argmax(np.where(valid,corr,-np.inf)))
    direct=pearson(x[a[i]:b[i]],y[c[i]:d[i]])
    if direct is None or abs(direct-float(corr[i]))>DIRECT_TOL:raise ValueError('Direct/FFT Pearson disagreement')
    others=valid&(np.abs(lags-lags[i])>exclude)
    alt=int(np.argmax(np.where(others,np.abs(corr),-np.inf))) if np.any(others) else None
    def point(k):return {'lag_samples':int(lags[k]),'signed_pearson':float(corr[k]),'overlap_samples':int(n[k])}
    return {'status':'ok','candidate_lags':len(lags),'eligible_lags':int(valid.sum()),'nfft':nfft,'best_absolute':point(i),'greatest_signed':point(j),'alternative_outside_exclusion':point(alt) if alt is not None else None,'alternative_exclusion_samples':exclude,'direct_selected_pearson':direct,'direct_fft_abs_difference':abs(direct-float(corr[i])),'x_overlap_range':[int(a[i]),int(b[i])],'y_overlap_range':[int(c[i]),int(d[i])],'x_unmatched_prefix_suffix':[int(a[i]),int(nx-b[i])],'y_unmatched_prefix_suffix':[int(c[i]),int(ny-d[i])]}

def controls():
    rng=np.random.default_rng(9110);x=rng.normal(size=40000);pos=0.6*x[137:-503]+2;neg=-0.6*x[137:-503]-2;noise=rng.normal(size=len(pos));results={}
    for label,y in [('cropped_gain_dc',pos),('cropped_negative_gain_dc',neg),('unrelated_noise',noise)]:
        results[label]=search(x,y,500,math.ceil(.8*min(len(x),len(y))))
    for label,sign in [('cropped_gain_dc',1),('cropped_negative_gain_dc',-1)]:
        t=results[label]['best_absolute'];assert t['lag_samples']==137 and abs(t['signed_pearson']-sign)<DIRECT_TOL
    assert abs(results['unrelated_noise']['best_absolute']['signed_pearson'])<.1
    return {'seed':9110,'expected_lag_samples':137,'positive_and_negative_gain_and_dc':'pass','unrelated_noise_absolute_max_under_0_1':'pass','results':results,'scope':'Algorithm controls only, not historical/voice/source authentication'}

def command(exe,args,payload=None):
    r=subprocess.run([exe,*args],input=payload,capture_output=True,timeout=90)
    if r.returncode:raise RuntimeError('Local media command failed: '+r.stderr.decode(errors='replace')[:4000])
    return r

def decoded(payload,ffmpeg,ffprobe):
    probe_args=['-v','error','-select_streams','a:0','-show_entries','stream=codec_name,sample_rate,channels','-of','json','pipe:0']
    p=command(ffprobe,probe_args,payload);streams=json.loads(p.stdout)['streams'];assert len(streams)==1
    meta=streams[0];rate=int(meta['sample_rate']);channels=int(meta['channels']);assert meta['codec_name']=='mp3' and channels==1
    native_args=['-v','warning','-i','pipe:0','-map','0:a:0','-c:a','pcm_s16le','-f','s16le','pipe:1']
    n=command(ffmpeg,native_args,payload);assert len(n.stdout)%(2*channels)==0
    count=len(n.stdout)//(2*channels);assert count/rate<=300
    view_args=['-v','warning','-i','pipe:0','-map','0:a:0','-ac','1','-ar',str(RATE),'-c:a','pcm_f32le','-f','f32le','pipe:1']
    v=command(ffmpeg,view_args,payload);assert len(v.stdout)%4==0
    a=np.frombuffer(v.stdout,dtype='<f4').astype(np.float64);assert len(a)<=RATE*300 and np.isfinite(a).all()
    r={'mp3_bytes':len(payload),'mp3_sha256':sha(payload),'probe':meta,'native_pcm_format':'s16le original rate/channel; no seeking metadata applied','native_pcm_bytes':len(n.stdout),'native_pcm_samples_per_channel':count,'native_pcm_sha256':sha(n.stdout),'analysis_view':'Derived mono8000Hz f32le; FFmpeg default resampler, no silence removal/gain/crop; not replacement original','analysis_samples':len(a),'analysis_rate':RATE,'analysis_f32_sha256':sha(v.stdout),'analysis_rms':float(np.sqrt(np.mean(a*a))),'analysis_min':float(a.min()),'analysis_max':float(a.max()),'commands':{'probe':probe_args,'native':native_args,'view':view_args},'stderr':{'probe':p.stderr.decode(errors='replace'),'native':n.stderr.decode(errors='replace'),'view':v.stderr.decode(errors='replace')},'returncodes':[p.returncode,n.returncode,v.returncode]}
    return r,a

def extract(raw,helper):
    data=helper.unpack(raw);start=8+(5+4*(data[8]>>3)+7)//8+4;tags=list(helper.walk(data,start,len(data)));events=[];blocks=[];head=[]
    for code,offset,body,path in tags:
        if code==14 and path=='root' and struct.unpack_from('<H',body)[0]==1:
            assert len(body)>=9 and body[2]>>4==2;events.append((offset,body[9:],{'declared_sample_count':struct.unpack_from('<I',body,3)[0],'seek_samples':struct.unpack_from('<h',body,7)[0],'rate_code':(body[2]>>2)&3}))
        if path=='root' and code in (18,45):
            assert len(body)==6 and body[1]>>4==2;head.append({'offset':offset,'latency_seek':struct.unpack_from('<h',body,4)[0],'rate_code':(body[1]>>2)&3})
        if code==19 and path=='root':
            assert len(body)>=4;blocks.append((offset,body[4:],struct.unpack_from('<Hh',body)))
    assert len(events)==1 and len(head)==1 and blocks
    return events[0],b''.join(b[1] for b in blocks),{'header':head[0],'block_count':len(blocks),'first_last_offsets':[blocks[0][0],blocks[-1][0]],'sample_prefix_sum':sum(b[2][0] for b in blocks),'first_seek_samples':blocks[0][2][1]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive');p.add_argument('--helper',type=Path,default=Path(__file__).resolve().parent.parent/'telephone-court-audio-resources-2026-10-29/reproduce_resources.py');p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe',default='ffprobe');args=p.parse_args()
    b=args.helper.read_bytes();assert sha(b)==HELPER_SHA;spec=importlib.util.spec_from_file_location('pinned_existing_walker',args.helper);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    tests=controls();archive=Path(args.archive);assert sha(archive.read_bytes())==ARCHIVE_SHA
    versions={}
    for name,exe in [('ffmpeg',args.ffmpeg),('ffprobe',args.ffprobe)]:
        v=command(exe,['-version']).stdout;versions[name]={'version_line':v.decode().splitlines()[0],'version_output_sha256':sha(v)}
    result={'archive_url':'https://coop.vaed.uscourts.gov/moussaoui/flights.zip','archive_sha256':ARCHIVE_SHA,'script_sha256':sha(Path(__file__).read_bytes()),'helper_sha256':HELPER_SHA,'software':{'Python':platform.python_version(),'NumPy':np.__version__,**versions},'parameters':{'analysis_rate':RATE,'global_max_lag_samples':30*RATE,'global_min_overlap':'max(30s,80% shorter array)','window_samples':10*RATE,'local_max_lag_samples':RATE,'local_min_overlap':'90% window','peak':'greatest absolute Pearson with sign; greatest signed also retained','lag_definition':'event[k+lag] aligns with stream[k]; nominal analysis units only','secondary_exclusion_samples':2000,'direct_fft_tolerance':DIRECT_TOL,'FFT_max_points':MAX_NFFT,'source_seek_and_player_metadata_applied':False},'controls':tests,'results':[],'scope':'Same-decoder file-signal comparison only; no listening/runtime/speaker/carrier/custody/historical clock authentication'}
    with zipfile.ZipFile(archive) as z:
        for member,pins in EXPECTED.items():
            assert z.getinfo(member).file_size<=64*1024*1024;raw=z.read(member);assert sha(raw)==pins['member'];event,stream,meta=extract(raw,h);offset,payload,fields=event;assert sha(payload)==pins['event'] and sha(stream)==pins['stream']
            e,x=decoded(payload,args.ffmpeg,args.ffprobe);s,y=decoded(stream,args.ffmpeg,args.ffprobe);global_fit=search(x,y,30*RATE,max(30*RATE,math.ceil(.8*min(len(x),len(y)))))
            row={'member':member,'member_sha256':pins['member'],'event_tag_offset':offset,'event_fields':fields,'stream_fields':meta,'event_decode':e,'stream_decode':s,'global_fit':global_fit,'windows':[]}
            if global_fit['status']=='ok':
                x0,x1=global_fit['x_overlap_range'];y0,y1=global_fit['y_overlap_range'];assert x1-x0==y1-y0;win=10*RATE
                for pos in range(0,((x1-x0)//win)*win,win):
                    a=x[x0+pos:x0+pos+win];b=y[y0+pos:y0+pos+win];local=search(a,b,RATE,math.ceil(.9*win));row['windows'].append({'overlap_start_analysis_sample':pos,'event_start_analysis_sample':x0+pos,'stream_start_analysis_sample':y0+pos,'samples':win,'pearson_at_global_alignment':pearson(a,b),'local_fit':local})
                row['window_tail_not_analyzed_samples']=(x1-x0)%win
            result['results'].append(row)
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=='__main__':main()
