"""Compare published mono excerpts against the archival Position 15 left channel."""
import json
from pathlib import Path
import subprocess
import sys
from fractions import Fraction

import numpy as np
from scipy.signal import butter, correlate, resample_poly, sosfiltfilt

RATE = 4000
FILTER = butter(5,(320,1650),btype="bandpass",fs=RATE,output="sos")
SPECS = {
    "082924": (820,1080,(2,19,42)),
    "083053": (930,1170,(2,18,31)),
    "083940": (1410,1770,(2,18,34)),
    "090608": (2930,3360,(0.35,)),
}
SCALES = (0.98,0.985,0.99,0.995,1.0,1.005,1.01,1.015,1.02)

def decode(path, channel, start=0, duration=None):
    command = ["ffmpeg","-nostdin","-v","error","-i",str(path),"-ss",str(start),
               "-af",f"pan=mono|c0=c{channel}","-ar",str(RATE),"-f","f32le"]
    if duration is not None:
        command.extend(("-t",str(duration)))
    raw = subprocess.check_output(command+["-"])
    return sosfiltfilt(FILTER,np.frombuffer(raw,dtype="<f4").astype(float))

def match(reference, template, start, clip_offset, length):
    clip = template[round(clip_offset*RATE):round((clip_offset+length)*RATE)]
    energy = np.r_[0,np.cumsum(reference*reference)]
    peaks=[]
    for scale in SCALES:
        ratio=Fraction(str(scale))
        query=resample_poly(clip,ratio.numerator,ratio.denominator)
        size=len(query)
        weights=np.sqrt(np.maximum(energy[size:]-energy[:-size],1e-14)*np.dot(query,query))
        values=np.abs(correlate(reference,query,mode="valid",method="fft"))/weights
        i=int(np.argmax(values))
        exclude=round(2*RATE)
        other=max(values[:max(i-exclude,0)].max(initial=0),values[i+exclude:].max(initial=0))
        peaks.append({"scale":scale,"correlation":float(values[i]),"off_target_peak":float(other),
                      "file_offset":start+i/RATE,"clip_offset":clip_offset})
    return max(peaks,key=lambda p:p["correlation"])

if __name__=="__main__":
    main=Path(sys.argv[1])
    source=Path(sys.argv[2])
    results={}
    for key,(start,end,offsets) in SPECS.items():
        clip=decode(source/f"excerpt-{key}.mp3",0)
        reference=decode(main,0,start,end-start)
        length=2.7 if key=="090608" else 8
        results[key]=[match(reference,clip,start,offset,length) for offset in offsets]
    early=decode(main,0,820,260)
    negative=match(early,decode(source/"excerpt-090608.mp3",0),820,.35,2.7)
    print(json.dumps({"main_matches":results,"090608_in_early_window_control":negative},indent=2))
