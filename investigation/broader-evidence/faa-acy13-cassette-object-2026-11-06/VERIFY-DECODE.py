"""Verify the full timing-track decode, a synthetic frame and a channel control."""
from hashlib import file_digest
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import sys

import numpy as np

spec = importlib.util.spec_from_file_location("decoder",Path(__file__).with_name("DECODE-TIME-TRACK.py"))
decoder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decoder)
rows = json.loads(Path(sys.argv[2]).read_text())
path = Path(sys.argv[1])
with path.open("rb") as source:
    assert file_digest(source,"sha256").hexdigest() == "1b82e4f3df0d60c2c370c7bddeb8a426b136a9bcaea83e147740ac00f88efa3f"

def fields(row):
    return tuple(row[k] for k in ("day","hour","minute","second"))

def tod(row):
    return row["hour"] * 3600 + row["minute"] * 60 + row["second"]

def offset(row):
    return row["sample"] / decoder.RATE

def encode():
    """Construct day 254, 13:15:00 with independent decimal bit placements."""
    signal = np.zeros(100,dtype=int)
    signal[[0,9,19,29,39,49,59,69,79,89,99]] = 2
    signal[[10,12,15,20,21,25,32,35,37,41]] = 1
    return signal

def synthesize(symbols):
    slot = np.arange(441)
    frames = np.tile(symbols,4)
    signal = (slot[None,:] < np.array([88,221,353])[frames,None]).astype(float)
    return np.pad(signal.ravel(),(13,441))

pulse = encode()
ok = list(decoder.frames(synthesize(pulse),.22,0,-1))
assert len(ok)==2 and all(fields(r)==(254,13,15,0) for r in ok), ok
pulse[49] = 0
assert not list(decoder.frames(synthesize(pulse),.22,0,-1))

a,b = rows["0.22"],rows["0.25"]
assert len(a)==len(b)==2276
assert list(map(fields,a))==list(map(fields,b))
assert max(abs(x["sample"]-y["sample"]) for x,y in zip(a,b))<=2
assert len(rows["0.18"])==195
assert all(r["day"]==254 for r in a)
anomalies = [(x,y) for x,y in zip(a,a[1:]) if tod(y)-tod(x)!=1 or not .90<offset(y)-offset(x)<1.10]
assert [(fields(x),fields(y)) for x,y in anomalies]==[
    ((254,13,18,32),(254,13,2,20)),((254,13,15,0),(254,13,15,0))]
assert fields(a[0])==(254,12,57,9) and fields(a[-1])==(254,13,18,50)

def pcm(channel):
    cmd=["ffmpeg","-nostdin","-v","error","-i",str(path),"-ss","110","-t","20",
         "-af",f"pan=mono|c0=c{channel}","-f","f32le","-"]
    return np.frombuffer(subprocess.check_output(cmd),"<f4")

control = []
for channel in (0,1):
    samples=pcm(channel)
    env=np.sqrt(np.convolve(samples*samples,np.ones(35)/35,mode="same"))
    candidates=list(decoder.frames(env,.22,110*decoder.RATE,-1))
    control.append(len(candidates))
assert control[0] == 0 and control[1] >= 18,control

segments = []
for segment in (a[:1284],a[1284:]):
    step=[offset(y)-offset(x) for x,y in zip(segment,segment[1:]) if tod(y)-tod(x)==1]
    segments.append({"frames":len(segment),"first":segment[0],"last":segment[-1],
                     "median_file_seconds_per_one_coded_second":statistics.median(step)})
print(json.dumps({"accepted_frames_by_threshold":{k:len(v) for k,v in rows.items()},
 "synthetic_frames_accepted":len(ok),"bad_marker_control_accepted":0,
 "left_right_control_frames_at_110_to_130_s":control,
 "segments":segments,"transition_and_repeat":anomalies},indent=2))
