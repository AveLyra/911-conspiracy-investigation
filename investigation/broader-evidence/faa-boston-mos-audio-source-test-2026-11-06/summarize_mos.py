"""Summarize timing-code frames and left-channel levels on a pinned MOS transfer."""
import argparse
from hashlib import file_digest
import json
from pathlib import Path
import subprocess

import numpy as np

RATE=44100
LABELS=["1237:50","1238:15","1239:00","1242:15","1252:00","1253:05"]

def time_of_day(fields):
    return 3600*fields["hour"]+60*fields["minute"]+fields["second"]

def label_to_seconds(label):
    return int(label[:2])*3600+int(label[2:4])*60+int(label[5:])

def timing_summary(right):
    selection=right["0.15"]
    code=np.array([time_of_day(frame) for frame in selection])
    samples=np.array([frame["sample"] for frame in selection])
    assert len(code)==161 and np.all(np.diff(code)==10)
    assert all(frame["day"]==254 for frame in selection)
    assert (int(code[0]),int(code[-1]))==(label_to_seconds("1232:10"),label_to_seconds("1258:50"))
    for t in ["0.125","0.17","0.2"]:
        assert [time_of_day(f) for f in right[t]]==code.tolist()
        assert all(f["day"]==254 for f in right[t])
    values=[label_to_seconds(label) for label in LABELS]
    playback={t:np.interp(values,[time_of_day(f) for f in fs],[f["sample"]/RATE for f in fs])
              for t,fs in right.items()}
    mapped=playback["0.15"]
    rates=np.diff(samples/RATE)
    slope,intercept=np.polyfit(code-code[0],samples/RATE,1)
    fit_residual=samples/RATE-(slope*(code-code[0])+intercept)
    delta=max(abs(playback[t]-mapped).max() for t in playback)
    return dict(code_start="12:32:10",code_end="12:58:50",day=254,
                counts={t:len(fs) for t,fs in right.items()},
                playback_start_s=samples[0]/RATE,playback_end_s=samples[-1]/RATE,
                playback_step_s=dict(min=float(min(rates)),median=float(np.median(rates)),max=float(max(rates))),
                global_fit_playback_s_per_code_s=float(slope),
                global_fit_residual_rms_s=float(np.sqrt(np.mean(fit_residual**2))),
                global_fit_residual_max_abs_s=float(abs(fit_residual).max()),
                boundaries=[dict(sheet_label=k,playback_s=float(v)) for k,v in zip(LABELS,mapped)],
                max_boundary_delta_threshold_s=float(delta)),np.rint(mapped*RATE).astype(int)

def audio_levels(audio, edges):
    # Analyze decoded playback samples between the code-derived boundaries.
    power=np.zeros(len(edges)-1)
    peak=np.zeros(len(edges)-1)
    count=np.zeros(len(edges)-1,dtype=np.int64)
    cmd=["ffmpeg","-nostdin","-v","error","-xerror","-i",str(audio),"-map","0:a:0","-af","pan=mono|c0=c0","-f","f32le","-"]
    offset=0
    with subprocess.Popen(cmd,stdout=subprocess.PIPE) as p:
        while raw:=p.stdout.read(20*RATE*4):
            a=np.frombuffer(raw,dtype="<f4")
            for i,(start,end) in enumerate(zip(edges,edges[1:])):
                lo=max(0,start-offset)
                hi=min(len(a),end-offset)
                if lo<hi:
                    part=a[lo:hi].astype(np.float64)
                    power[i]+=np.dot(part,part)
                    peak[i]=max(peak[i],abs(part).max())
                    count[i]+=len(part)
            offset+=len(a)
        assert p.wait()==0
    assert np.array_equal(count,np.diff(edges))
    return [dict(interval_id=label,playback_samples=int(n),rms_dbfs=float(10*np.log10(total/n)),peak_dbfs=float(20*np.log10(pk)))
            for label,n,total,pk in zip(["clip1","between1and2","clip2","between2and3","clip3"],count,power,peak)],offset

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("audio",type=Path)
    p.add_argument("sha256")
    p.add_argument("right",type=Path)
    p.add_argument("left",type=Path)
    args=p.parse_args()
    with args.audio.open("rb") as f:
        assert file_digest(f,"sha256").hexdigest()==args.sha256
    right=json.loads(args.right.read_text())
    left=json.loads(args.left.read_text())
    assert set(left)==set(right) and all(not fs for fs in left.values())
    timing,edges=timing_summary(right)
    levels,total=audio_levels(args.audio,edges)
    print(json.dumps(dict(timing=timing,left_channel_control_counts={t:len(fs) for t,fs in left.items()},
                          left_levels=levels,decoded_samples_per_channel=total,decoded_duration_s=total/RATE),indent=2))
