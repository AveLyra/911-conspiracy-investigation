"""Read-only independent checks; stdout JSON, no producer imports or writes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import scipy
from scipy.signal import resample_poly

T = Path(__file__).resolve().parent
def pin(p):
    return {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
def load(p):
    return json.loads(p.read_text())
out = {'reviewer': 'Separate AI, shared context and disclosed prior results; not blind/human review',
       'command': [sys.executable, '-B', str(Path(__file__).resolve())],
       'runtime': {'numpy': np.__version__, 'scipy': scipy.__version__},
       'checks': {}, 'limits': [], 'commands': []}
receipts = {n: load(T/n/'receipt.json') for n in ['controls01','controls02','audio01','audio02']}
product_count = 0
for n, r in receipts.items():
    assert r['status'] == 'complete'
    assert r['inputs_before'] == r['inputs_after']
    for path, expected in r['inputs_before'].items():
        if n == 'controls01' and Path(path).name == 'audio_screen.py':
            assert pin(T/'audio_screen.pre-hardening.py') == expected
            out['checks']['controls01_preserved_producer_pin_matched'] = True
            continue
        assert pin(Path(path)) == expected, (n,path)
    for field in ['binary_pins','binary_pins_after']:
        for path, expected in r.get(field,{}).items():
            assert pin(Path(path)) == expected, (n,field,path)
    for path, expected in r['products'].items():
        assert pin(T/n/path) == expected, (n,path)
        product_count += 1
out['checks']['product_pins'] = product_count
for n in ['audio01','audio02']:
    gate = receipts[n]['controls_gate']
    assert pin(T/'controls02/receipt.json') == gate['receipt']
    assert pin(T/'controls02/controls.json') == gate['controls']
    assert gate['checks'] == 17
    checks = load(T/'controls02/controls.json')['checks']
    assert len(checks) == 17 and all(v is True for v in checks.values())

paths = {'reference': T.parent/'media/SIbqaybkbWI.f140.unmodified.m4a',
         'query': Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/run01/edited-stereo.wav')}
arrays = {}
for label, source in paths.items():
    for n in ['audio01','audio02']:
        assert pin(source) == receipts[n]['sources_before'][label] == receipts[n]['sources_after'][label]
    cmd = ['/opt/homebrew/bin/ffmpeg','-nostdin','-v','error','-i',str(source),'-map','0:a:0','-vn','-c:a','pcm_f32le','-f','f32le','pipe:1']
    p = subprocess.run(cmd,capture_output=True,timeout=60)
    out['commands'].append({'argv':cmd,'exit':p.returncode,'stderr_bytes':len(p.stderr)})
    assert p.returncode == 0 and not p.stderr
    assert p.stdout == (T/'audio01'/f'{label}.f32').read_bytes() == (T/'audio02'/f'{label}.f32').read_bytes()
    raw = np.frombuffer(p.stdout,dtype='<f4').reshape(-1,2)
    assert np.isfinite(raw).all()
    a = resample_poly(raw.astype(np.float64),1,7,axis=0,window=('kaiser',5.0),padtype='constant')
    arrays[label] = a
    for n in ['audio01','audio02']:
        assert np.array_equal(a,np.load(T/n/f'{label}-6300.npy',allow_pickle=False))
        d = receipts[n]['decoded'][label]
        assert len(raw)==d['frames'] and len(a)==d['resampled_frames']
        assert hashlib.sha256(p.stdout).hexdigest()==d['float32_sha256']
        assert hashlib.sha256(a.tobytes()).hexdigest()==d['resampled_float64_sha256']
    out['checks'][label+'_fresh_decode_resample'] = {'native_frames':len(raw),'resampled_frames':len(a),'exact_equal':True}

maxerr=0.; tested=0; profiles=0; global_max={}; candidates={}
for direction in ['forward','reversed']:
    report=load(T/'audio01'/f'{direction}.json')
    assert report == load(T/'audio02'/f'{direction}.json')
    ref=arrays['reference'] if direction=='forward' else arrays['reference'][::-1]
    allmax=[]; candidates[direction]={}
    for ca in range(2):
        for rb in range(2):
            key=f'C{ca}-R{rb}'; rows=report['pairs'][key]['blocks']; eligible=[]
            for block in range(25):
                name=f'{direction}-{key}-block{block:02d}.npy'
                assert (T/'audio01'/name).read_bytes()==(T/'audio02'/name).read_bytes()
                scores=np.load(T/'audio01'/name,allow_pickle=False)
                assert scores.shape==(len(ref)-6300+1,)
                profiles+=1
                finite=np.isfinite(scores); assert int(finite.sum())==rows[block]['finite_scores']
                assert int((~finite).sum())==rows[block]['undefined_scores']
                best=int(np.nanargmax(np.abs(scores))); allmax.append(float(abs(scores[best])))
                assert best==rows[block]['best']['reference_sample']
                assert float(scores[best])==rows[block]['best']['r']
                q=arrays['query'][block*6300:(block+1)*6300,ca].astype(np.longdouble)
                qc=q-q.mean(); qe=np.dot(qc,qc)
                for lag in [0,len(scores)//2,len(scores)-1,best]:
                    w=ref[lag:lag+6300,rb].astype(np.longdouble); wc=w-w.mean()
                    we=np.dot(wc,wc)
                    floorw=max(np.longdouble(1e-18)*6300,64*np.finfo(float).eps*np.dot(w,w))
                    floorq=max(np.longdouble(1e-18)*6300,64*np.finfo(float).eps*np.dot(q,q))
                    if we<=floorw or qe<=floorq:
                        assert np.isnan(scores[lag])
                    else:
                        direct=float(np.dot(qc,wc)/np.sqrt(qe*we)); actual=float(scores[lag])
                        err=abs(direct-actual); maxerr=max(maxerr,err)
                        assert np.isclose(direct,actual,rtol=1e-9,atol=1e-9), (direction,key,block,lag,direct,actual)
                    tested+=1
                indices=np.arange(len(scores)); allowed=finite & (indices>=126) & (indices+6300<=len(ref)-126)
                ids=indices[allowed]; k=int(ids[np.argmax(np.abs(scores[ids]))])
                saved=rows[block]['eligible_best']; assert k==saved['reference_sample'] and float(scores[k])==saved['r']
                eligible.append((float(scores[k]),k-block*6300))
            intervals=[]
            for start in range(1,24):
                for end in range(start+2,24):
                    part=eligible[start:end+1]; rs=[v[0] for v in part]; offs=[v[1] for v in part]
                    if min(abs(v) for v in rs)<.95 or not (all(v>=0 for v in rs) or all(v<0 for v in rs)) or (max(offs)-min(offs))*200>6300:
                        continue
                    intervals.append((start,end,min(offs),max(offs),1 if rs[0]>=0 else -1))
            maximal=[x for x in intervals if not any(y[0]<=x[0] and y[1]>=x[1] and y[:2]!=x[:2] for y in intervals)]
            expected=[{'first_block':a,'last_block':b,'blocks':b-a+1,'lag_samples_min':lo,'lag_samples_max':hi,'lag_s_min':lo/6300,'lag_s_max':hi/6300,'polarity':s} for a,b,lo,hi,s in maximal]
            assert expected==report['pairs'][key]['candidates']
            candidates[direction][key]=expected
    global_max[direction]=max(allmax)
out['checks'].update({'profiles_exact_across_runs':profiles,'direct_positions':tested,'direct_max_abs_error':maxerr,'global_max_abs_r':global_max,'independently_regenerated_candidates':candidates,'forward_reversed_reports_exact_across_runs':True})
out['limits'] += ['Direct oracle independently checks 800 declared positions, not every lag; all 200 full profiles were checked for repeat equality, pins and maxima.', 'Decode uses same ffmpeg binary and resampling uses same scipy implementation; not independent decoder or resampler validation.', 'No listening, sound classification, acoustic detectability or original-recording authentication.', 'Single-scale dominant-peak .95 rule does not exclude shared audio altered by speed change, channel mixing, nonlinear processing, local edits or weak short segments.', 'Time reversal is temporal-order sensitivity, not a calibrated null distribution or false-positive rate.', 'Synthetic controls lack codec degradation, time-scale variation, realistic speech/music mixing, nonlinear dynamic processing and original-recording clock validation.']
out['conclusion']='Numerical checks passed within declared scope. No dominant scale-one candidate; no exclusion of transformed/shared audio or physical sound finding.'
out['review_script_pin']=pin(Path(__file__).resolve())
out['reviewed_receipts']={n:pin(T/n/'receipt.json') for n in receipts}
print(json.dumps(out,indent=2,allow_nan=False))
