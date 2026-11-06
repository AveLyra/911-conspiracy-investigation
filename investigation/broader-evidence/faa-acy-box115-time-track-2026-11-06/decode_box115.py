"""Decode candidate IRIG-B BCD time-of-year from a pinned 44.1 kHz stereo ACY recording."""
import argparse
from hashlib import file_digest
import json
from pathlib import Path
import subprocess

import numpy as np

RATE = 44100
MARKERS = np.array([0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99])
WEIGHTS = {
    "second": ((1,2,3,4,6,7,8),(1,2,4,8,10,20,40)),
    "minute": ((10,11,12,13,15,16,17),(1,2,4,8,10,20,40)),
    "hour": ((20,21,22,23,25,26),(1,2,4,8,10,20)),
    "day": ((30,31,32,33,35,36,37,38,40,41),(1,2,4,8,10,20,40,80,100,200)),
}
MASK = np.zeros(100,dtype=bool)
MASK[MARKERS] = True

def frames(envelope, threshold, origin, earlier):
    high = envelope >= threshold
    rising = np.flatnonzero(high[1:] & ~high[:-1]) + 1
    falling = np.flatnonzero(~high[1:] & high[:-1]) + 1
    if not len(falling):
        return
    rising = rising[rising < falling[-1]]
    width_ms = (falling[np.searchsorted(falling,rising)] - rising) * 1000 / RATE
    symbols = np.select([width_ms < 1.3,width_ms < 3.8,width_ms < 7,width_ms <= 9.8],
                        [-1,0,1,2],default=-1)
    candidates = np.flatnonzero((symbols[1:] == 2) & (symbols[:-1] == 2)) + 1
    for i in candidates:
        sample = int(rising[i] + origin)
        if sample <= earlier or i + 100 >= len(rising):
            continue
        frame = symbols[i:i+100]
        if not np.array_equal(frame == 2,MASK) or np.any(frame < 0):
            continue
        spacings = np.diff(rising[i:i+101])*1000/RATE
        if np.any(spacings < 8.8) or np.any(spacings > 11.5):
            continue
        fields = {key:int(np.dot(frame[list(indices)],weights))
                  for key,(indices,weights) in WEIGHTS.items()}
        if not (1 <= fields["day"] <= 366 and fields["hour"] < 24
                and fields["minute"] < 60 and fields["second"] < 60):
            continue
        yield dict(sample=sample, **fields)

def decode(path, expected_hash, channel, thresholds):
    with path.open("rb") as file:
        assert file_digest(file,"sha256").hexdigest() == expected_hash
    decoded = {str(threshold):[] for threshold in thresholds}
    cmd = ["ffmpeg","-nostdin","-v","error","-xerror","-i",str(path),"-map","0:a:0",
           "-af",f"pan=mono|c0=c{channel}","-f","f32le","-"]
    carry = np.empty(0,dtype="float32")
    offset = 0
    kernel = np.ones(35,dtype="float64")/35
    with subprocess.Popen(cmd,stdout=subprocess.PIPE) as decoder:
        while data := decoder.stdout.read(20*RATE*4):
            current = np.frombuffer(data,dtype="<f4")
            block = np.concatenate((carry,current))
            envelope = np.sqrt(np.convolve(block*block,kernel,mode="same"))
            origin = offset-len(carry)
            for threshold in thresholds:
                output = decoded[str(threshold)]
                earlier = output[-1]["sample"] if output else -1
                output.extend(frames(envelope,threshold,origin,earlier))
            offset += len(current)
            carry = block[-2*RATE:]
        assert decoder.wait() == 0
    return decoded

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("sha256")
    parser.add_argument("channel", type=int, choices=(0, 1))
    parser.add_argument("thresholds", nargs="+", type=float)
    args = parser.parse_args()
    print(json.dumps(decode(args.audio, args.sha256, args.channel, args.thresholds)))
