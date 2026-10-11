#!/usr/bin/env python3
"""Frozen exploratory waveform-correspondence screen; controls run separately."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import time

import numpy as np
import scipy
from scipy import signal

HERE = Path(__file__).resolve().parent
RATE = 6300
FFMPEG = Path('/opt/homebrew/bin/ffmpeg')
FFPROBE = Path('/opt/homebrew/bin/ffprobe')
INPUTS = {
    'reference': (HERE.parent / 'media/SIbqaybkbWI.f140.unmodified.m4a',
                  '0776b39a597f236c85b98b0f1dd3931cb654ab08c967d508d5bfa6fc64f145ef'),
    'query': (Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/edited-stereo.wav'),
              'b8557ab9a0f2ac6dc9d3d59d0334de96431340ad34f2e5642c47a5a51a3a09dd'),
}


def identity(path):
    with path.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def save(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def array_hash(x):
    return hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()


def vector(x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError('Expected nonempty finite vector')
    return x


def pearson_profile(query, reference):
    """Index k compares query with reference[k:k+n], no wrapping or padding."""
    q, r = vector(query), vector(reference)
    n = len(q)
    if n < 2 or len(r) < n:
        raise ValueError('Insufficient window or reference length')
    # Extended-precision rolling moments reduce accumulated cancellation. The
    # rejection threshold remains the protocol's float64 epsilon and raw power.
    ld = np.longdouble
    sums = np.r_[ld(0), np.cumsum(r.astype(ld), dtype=ld)]
    squares = np.r_[ld(0), np.cumsum(r.astype(ld)**2, dtype=ld)]
    s, ss = sums[n:] - sums[:-n], squares[n:] - squares[:-n]
    energy = ss - s*s/n
    qld = q.astype(ld)
    qss = np.sum(qld*qld)
    qe = np.sum((qld - np.mean(qld))**2)
    floor = np.maximum(ld(1e-18)*n, 64*np.finfo(np.float64).eps*ss)
    qfloor = max(ld(1e-18)*n, 64*np.finfo(np.float64).eps*qss)
    out = np.full(len(r)-n+1, np.nan, dtype=np.float64)
    good = energy > floor
    if qe <= qfloor:
        return out
    # Center both operands before FFT to avoid large DC products. Correct the
    # residual sum of the rounded centered query for each reference window.
    qc = q - float(np.mean(qld))
    offset = float(np.mean(r.astype(ld)))
    numerator = signal.correlate(r-offset, qc, mode='valid', method='fft')
    numerator -= np.asarray((s - ld(offset)*n)/n, dtype=float)*float(np.sum(qc, dtype=ld))
    out[good] = numerator[good] / np.sqrt(np.asarray(energy[good]*qe, dtype=float))
    if np.any(np.abs(out[np.isfinite(out)]) > 1 + 1e-9):
        raise ArithmeticError('Correlation exceeds numerical allowance')
    # Only remove floating-point overshoot of the exact [-1,1] range.
    return np.clip(out, -1, 1)


def peak(profile, index, rate, block):
    value = float(profile[index])
    return {'reference_sample': int(index), 'reference_s': index/rate,
            'source_minus_C_s': index/rate-block, 'r': value,
            'abs_r': abs(value), 'polarity': 1 if value >= 0 else -1}


def summarize(profile, rate, block, reference_length):
    finite = np.flatnonzero(np.isfinite(profile))
    best = int(finite[np.argmax(np.abs(profile[finite]))]) if len(finite) else None
    magnitude = np.where(np.isfinite(profile), np.abs(profile), -np.inf)
    candidates = list(signal.find_peaks(magnitude)[0])
    if len(profile) and np.isfinite(profile[0]):
        candidates.append(0)
    if len(profile)>1 and np.isfinite(profile[-1]):
        candidates.append(len(profile)-1)
    if best is not None:
        candidates.append(best)
    ordered = sorted(set(candidates), key=lambda k: (-magnitude[k], k))
    shown = []
    for k in ordered:
        if all(abs(k-old)/rate >= .05 for old in shown):
            shown.append(k)
            if len(shown) == 5:
                break
    edge = int(np.ceil(.020*rate))
    eligible = finite[(finite >= edge) & (finite+rate <= reference_length-edge)]
    ebest = int(eligible[np.argmax(np.abs(profile[eligible]))]) if len(eligible) else None
    return {'block': block, 'finite_scores': len(finite), 'undefined_scores': len(profile)-len(finite),
            'best': None if best is None else peak(profile,best,rate,block),
            'displayed_peaks': [peak(profile,k,rate,block) for k in shown],
            'eligible_best': None if ebest is None else peak(profile,ebest,rate,block)}


def sequences(rows, block_count, rate):
    """All inclusion-maximal qualifying intervals; no greedy lost overlap."""
    valid = []
    for start in range(1, block_count-1):
        offsets, polarity = [], None
        for end in range(start, block_count-1):
            p = rows[end]['eligible_best']
            if p is None or p['abs_r'] < .95:
                break
            if polarity is not None and p['polarity'] != polarity:
                break
            polarity = p['polarity']
            offsets.append(p['reference_sample']-end*rate)
            if (max(offsets)-min(offsets))*200 > rate:
                break
            if end-start+1 >= 3:
                valid.append((start,end,min(offsets),max(offsets),polarity))
    maximal = [v for v in valid if not any(w[0]<=v[0] and w[1]>=v[1] and (w[0],w[1])!=(v[0],v[1]) for w in valid)]
    return [{'first_block':a,'last_block':b,'blocks':b-a+1,
             'lag_samples_min':lo,'lag_samples_max':hi,'lag_s_min':lo/rate,
             'lag_s_max':hi/rate,'polarity':p} for a,b,lo,hi,p in maximal]


def screen(query, reference, rate, out=None, prefix='screen'):
    q,r = np.asarray(query,dtype=float),np.asarray(reference,dtype=float)
    if q.ndim!=2 or r.ndim!=2 or q.shape[1]!=2 or r.shape[1]!=2:
        raise ValueError('Stereo arrays required; no implicit downmix')
    if not np.isfinite(q).all() or not np.isfinite(r).all() or len(q)%rate or len(q)<3*rate:
        raise ValueError('Finite complete query blocks required')
    results = {}
    for a in range(2):
        for b in range(2):
            key=f'C{a}-R{b}'
            rows=[]
            for block in range(len(q)//rate):
                scores=pearson_profile(q[block*rate:(block+1)*rate,a],r[:,b])
                if out is not None:
                    with (out/f'{prefix}-{key}-block{block:02d}.npy').open('xb') as f:
                        np.save(f,scores,allow_pickle=False)
                rows.append(summarize(scores,rate,block,len(r)))
            results[key]={'blocks':rows,'candidates':sequences(rows,len(rows),rate)}
    return {'rate':rate,'query_frames':len(q),'reference_frames':len(r),
            'query_float64_sha256':array_hash(q),'reference_float64_sha256':array_hash(r),
            'pairs':results,'profile_axis':'index = reference window start sample; signed source-minus-C lag = index/rate-block',
            'candidate_scope':'Dominant eligible peak, scale one, heuristic only; absence is not shared-audio exclusion'}


def resample(x):
    return signal.resample_poly(np.asarray(x,dtype=np.float64),1,7,axis=0,
                                window=('kaiser',5.0),padtype='constant')


def controls(out):
    rng=np.random.default_rng(7102026)
    checks={}; details={'seed':7102026}
    def check(name,condition):
        checks[name]=bool(condition)
        save(out/(name+'.json'),{'pass':bool(condition)})
        if not condition:
            raise AssertionError(name)
    q=rng.normal(size=17);r=rng.normal(size=83)
    actual=pearson_profile(q,r)
    direct=np.array([np.dot(q-q.mean(),w-w.mean())/np.sqrt(np.sum((q-q.mean())**2)*np.sum((w-w.mean())**2)) for w in np.lib.stride_tricks.sliding_window_view(r,len(q))])
    details['direct_max_error']=float(np.max(np.abs(actual-direct)))
    check('direct_normalization',np.max(np.abs(actual-direct))<1e-12)
    for name,query,ref in [('constant',np.ones(20),np.ones(60)),('nearconstant',1+1e-12*rng.normal(size=20),1+1e-12*rng.normal(size=60))]:
        check(name+'_undefined',np.isnan(pearson_profile(query,ref)).all())
    failures=0
    for query,ref in [(np.array([np.nan,1]),np.ones(4)),(np.ones(3),np.ones(2)),(np.array([1]),np.ones(2))]:
        try:pearson_profile(query,ref)
        except ValueError:failures+=1
    check('malformed_refused',failures==3)
    rate=100;ref=rng.normal(size=(1200,2));query=ref[137:937,::-1]*np.array([-2.,.7])+np.array([1.2,-.3])
    result=screen(query,ref,rate,out,'shift-swap')
    save(out/'shift-swap.json',result)
    for key,sign in [('C0-R1',-1),('C1-R0',1)]:
        rows=result['pairs'][key]['blocks']
        check(key+'_signed_shift',all(abs(p['best']['r']-sign)<1e-12 and p['best']['reference_sample']==137+i*rate for i,p in enumerate(rows)))
        check(key+'_candidate',result['pairs'][key]['candidates']==[{'first_block':1,'last_block':6,'blocks':6,'lag_samples_min':137,'lag_samples_max':137,'lag_s_min':1.37,'lag_s_max':1.37,'polarity':sign}])
    # Query has an actual one-second omitted segment at its fourth-second edge.
    edited=np.concatenate([ref[100:500],ref[600:1000]])
    edit=screen(edited,ref,rate,out,'edited');save(out/'edited.json',edit)
    check('edit_segments_not_bridged',all([(x['first_block'],x['last_block'],x['lag_samples_min']) for x in edit['pairs'][k]['candidates']]==[(1,3,100),(4,6,200)] for k in ['C0-R0','C1-R1']))
    noise=screen(rng.normal(size=(800,2)),ref,rate,out,'noise');save(out/'noise.json',noise)
    check('independent_noise_no_candidate',not any(p['candidates'] for p in noise['pairs'].values()))
    tone=np.sin(2*np.pi*10*np.arange(1200)/rate);toneref=np.column_stack([tone,tone]);tonequery=toneref[100:900]
    tonal=screen(tonequery,toneref,rate,out,'tone');save(out/'tone.json',tonal)
    check('tonal_competing_peaks',all(len(row['displayed_peaks'])==5 and all(p['abs_r']>.999999 for p in row['displayed_peaks']) for row in tonal['pairs']['C0-R0']['blocks']))
    reverse=screen(query,ref[::-1].copy(),rate,out,'reverse');save(out/'reverse.json',reverse)
    check('synthetic_reverse_noise_no_candidate',not any(p['candidates'] for p in reverse['pairs'].values()))
    # Full-rate, band-limited synthetic source. Offset4411 is not divisible by7.
    raw=signal.sosfilt(signal.butter(4,1000,fs=44100,output='sos'),rng.normal(size=(44100*7,2)),axis=0)
    shift=4411;fullquery=raw[shift:shift+44100*5,::-1]*[-1.3,.6]+[.12,-.07]
    downq,downr=resample(fullquery),resample(raw)
    non=screen(downq,downr,RATE,out,'nongrid');save(out/'nongrid.json',non)
    check('nongrid_resampling_counts',len(downq)==31500 and len(downr)==44100)
    for key in ['C0-R1','C1-R0']:
        rows=non['pairs'][key]['blocks'][1:4]
        check(key+'_nongrid_recovered',all(p['eligible_best']['abs_r']>.95 and abs(p['eligible_best']['source_minus_C_s']-shift/44100)<=1/RATE for p in rows) and bool(non['pairs'][key]['candidates']))
    # Exhaustive interval rule must retain two overlapping runs if their union
    # violates lag tolerance; endpoint blocks excluded even with high scores.
    fake=[{'eligible_best':{'abs_r':1.,'polarity':1,'reference_sample':i*1000+o}} for i,o in enumerate([0,0,2,4,6,6])]
    seq=sequences(fake,6,1000)
    check('overlap_without_invalid_merge',[(s['first_block'],s['last_block']) for s in seq]==[(1,3),(2,4)])
    edgeprofile=np.zeros(401);edgeprofile[0]=1;edgeprofile[200]=.99
    es=summarize(edgeprofile,100,1,500)
    check('edge_peak_retained_but_ineligible',es['best']['reference_sample']==0 and es['eligible_best']['reference_sample']==200)
    details.update({'checks':checks,'all_pass':all(checks.values()),'nongrid_native_shift_samples':shift,
                    'synthetic_rate_other_tests':rate,'fullrate_lowpass':'Butterworth4 1000Hz fs44100 causal SOS',
                    'tonal_limit':'Competing perfect matches retained; sequence heuristic does not prove recording specificity'})
    save(out/'controls.json',details)
    return details


def decode(source,out,label,receipt):
    def run(cmd,suffix):
        result=subprocess.run(cmd,capture_output=True,timeout=60)
        with (out/f'{label}-{suffix}.stderr.txt').open('xb') as f:f.write(result.stderr)
        receipt.setdefault('commands',[]).append({'argv':cmd,'exit':result.returncode,'stderr_bytes':len(result.stderr)})
        if result.returncode or result.stderr:raise RuntimeError('Decode/probe diagnostics require review')
        return result.stdout
    meta=json.loads(run([str(FFPROBE),'-v','error','-select_streams','a:0','-show_entries','stream=sample_rate,channels,start_time,time_base,duration','-of','json',str(source)],'probe'))
    save(out/f'{label}-probe.json',meta)
    streams=meta['streams']
    if len(streams)!=1 or streams[0]['channels']!=2 or streams[0]['sample_rate']!='44100':raise ValueError('Native stereo44100 contract failed')
    raw=run([str(FFMPEG),'-nostdin','-v','error','-i',str(source),'-map','0:a:0','-vn','-c:a','pcm_f32le','-f','f32le','pipe:1'],'decode')
    if len(raw)%8:raise ValueError('Partial stereo float sample')
    with (out/f'{label}.f32').open('xb') as f:f.write(raw)
    x=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
    if not np.isfinite(x).all():raise ValueError('Nonfinite decoded source')
    return x


def historical(out,receipt):
    # This path is implemented but not run during synthetic-only authorization.
    before={key:identity(path) for key,(path,pin) in INPUTS.items()}
    if any(before[key]['sha256']!=pin for key,(path,pin) in INPUTS.items()):raise ValueError('Historical source pin mismatch')
    receipt['sources_before']=before
    decoded={key:decode(path,out,key,receipt) for key,(path,_) in INPUTS.items()}
    if len(decoded['query'])!=25*44100:raise ValueError('Query must be exact25 seconds')
    if len(decoded['reference'])>60*44100:raise ValueError('Reference duration cap')
    down={k:resample(v) for k,v in decoded.items()}
    receipt['decoded']={k:{'frames':len(v),'float32_sha256':array_hash(v),'resampled_frames':len(down[k]),'resampled_float64_sha256':array_hash(down[k])} for k,v in decoded.items()}
    for k,v in down.items():
        with (out/f'{k}-6300.npy').open('xb') as f:np.save(f,v,allow_pickle=False)
    save(out/'forward.json',screen(down['query'],down['reference'],RATE,out,'forward'))
    save(out/'reversed.json',screen(down['query'],down['reference'][::-1].copy(),RATE,out,'reversed'))
    receipt['sources_after']={key:identity(path) for key,(path,_) in INPUTS.items()}
    if receipt['sources_after']!=before:raise ValueError('Historical source changed')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['controls','historical'])
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    args.output.mkdir(exist_ok=False,parents=False)
    t=time.monotonic()
    controlled=[Path(__file__),HERE/'PROTOCOL.md']
    before={str(p):identity(p) for p in controlled}
    receipt={'mode':args.mode,'status':'started','inputs_before':before,
             'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
             'binary_pins':{str(p):identity(p) for p in [FFMPEG,FFPROBE]},
             'scope':'synthetic verification or exploratory correspondence only; no listening/authentication/cause finding'}
    save(args.output/'start.json',receipt)
    try:
        if args.mode=='controls':controls(args.output)
        else:historical(args.output,receipt)
        receipt['inputs_after']={str(p):identity(p) for p in controlled}
        if receipt['inputs_after']!=before:raise ValueError('Controlled input changed')
        receipt['binary_pins_after']={str(p):identity(p) for p in [FFMPEG,FFPROBE]}
        if receipt['binary_pins_after']!=receipt['binary_pins']:raise ValueError('Decoder binary changed')
        receipt['status']='complete'
    except Exception as exc:
        receipt.update(status='failed',failure_type=type(exc).__name__,failure=str(exc))
        raise
    finally:
        receipt['elapsed_s']=time.monotonic()-t
        receipt['maxrss_platform_units']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        receipt['products']={str(p.relative_to(args.output)):identity(p) for p in sorted(args.output.rglob('*')) if p.is_file() and p.name not in ['start.json','receipt.json']}
        save(args.output/'receipt.json',receipt)
    print(json.dumps({'status':receipt['status'],'mode':args.mode,'products':len(receipt['products'])}))


if __name__=='__main__':main()
