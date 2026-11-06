"""Decode candidate IRIG Format E time-of-year from stereo 44.1 kHz audio."""
import argparse
from hashlib import file_digest
import json
from pathlib import Path
import subprocess

import numpy as np

RATE = 44100
MARKERS = np.arange(9,100,10)
MASK = np.zeros(100,dtype=bool)
MASK[0] = True
MASK[MARKERS] = True
WEIGHTS = {
    "second": ((6,7,8),(10,20,40)),
    "minute": ((10,11,12,13,15,16,17),(1,2,4,8,10,20,40)),
    "hour": ((20,21,22,23,25,26),(1,2,4,8,10,20)),
    "day": ((30,31,32,33,35,36,37,38,40,41),(1,2,4,8,10,20,40,80,100,200)),
}

def frames(envelope, threshold, origin, earlier):
    high = envelope >= threshold
    rising = np.flatnonzero(high[1:] & ~high[:-1]) + 1
    falling = np.flatnonzero(~high[1:] & high[:-1]) + 1
    if not len(falling):
        return
    rising = rising[rising < falling[-1]]
    ends = falling[np.searchsorted(falling,rising)]
    # Bridge brief envelope dips within one high-amplitude symbol.
    join = np.diff(rising) > 0
    join &= rising[1:]-ends[:-1] <= round(RATE*.005)
    width_ms = (ends[np.r_[~join,True]]-rising[np.r_[True,~join]])*1000/RATE
    rising = rising[np.r_[True,~join]]
    symbols = np.select([width_ms < 12,width_ms < 38,width_ms < 68,width_ms <= 94],
                        [-1,0,1,2],default=-1)
    starts = np.flatnonzero((symbols[1:] == 2) & (symbols[:-1] == 2)) + 1
    for i in starts:
        sample = int(rising[i]+origin)
        if sample <= earlier or i+100 >= len(rising):
            continue
        frame = symbols[i:i+100]
        if not np.array_equal(frame == 2,MASK) or np.any(frame < 0):
            continue
        spacings = np.diff(rising[i:i+101])*1000/RATE
        if np.any(spacings<90) or np.any(spacings>115):
            continue
        fields = {key:int(np.dot(frame[list(indices)],weights)) for key,(indices,weights) in WEIGHTS.items()}
        if not (1 <= fields["day"] <= 366 and fields["hour"] < 24
                and fields["minute"] < 60 and fields["second"] < 60):
            continue
        yield dict(sample=sample, **fields)

def decode(path, expected_hash, channel, thresholds):
    with path.open("rb") as file:
        assert file_digest(file,"sha256").hexdigest() == expected_hash
    out = {str(t):[] for t in thresholds}
    cmd = ["ffmpeg","-nostdin","-v","error","-xerror","-i",str(path),"-map","0:a:0",
           "-af",f"pan=mono|c0=c{channel}","-f","f32le","-"]
    carry = np.empty(0,dtype=np.float32)
    offset = 0
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        while data := proc.stdout.read(30*RATE*4):
            current = np.frombuffer(data,dtype="<f4")
            block = np.concatenate((carry,current))
            square = np.pad(block.astype(np.float64)**2,(225,224))
            total = np.r_[0., np.cumsum(square)]
            envelope = np.sqrt((total[450:]-total[:-450])/450)
            origin = offset-len(carry)
            for t in thresholds:
                found = out[str(t)]
                found.extend(frames(envelope,t,origin,found[-1]["sample"] if found else -1))
            offset += len(current)
            carry = block[-12*RATE:]
        assert proc.wait()==0
    return out

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("audio",type=Path)
    p.add_argument("sha256")
    p.add_argument("channel",type=int,choices=(0,1))
    p.add_argument("thresholds",type=float,nargs="+")
    args=p.parse_args()
    print(json.dumps(decode(args.audio,args.sha256,args.channel,args.thresholds)))
