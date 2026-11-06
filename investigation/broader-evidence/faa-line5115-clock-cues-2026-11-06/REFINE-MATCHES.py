"""Refine the coarse waveform alignments and check the source-time bracket."""
import importlib.util
import json
from pathlib import Path
import statistics
import sys


here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("matcher",here/"MATCH-WAVEFORMS.py")
matcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matcher)
source,clip_dir,coarse_path=map(Path,sys.argv[1:])
coarse=json.loads(coarse_path.read_text())
matches={}
for key, rows in coarse["main_matches"].items():
    clip=matcher.decode(clip_dir/f"excerpt-{key}.mp3",0)
    length=2.7 if key=="090608" else 8
    out=[]
    for row in rows:
        start=row["file_offset"]-1
        ref=matcher.decode(source,0,start,length+2.3)
        matcher.SCALES=tuple(round(row["scale"]+i*.00025,5) for i in range(-20,21))
        result=matcher.match(ref,clip,start,row["clip_offset"],length)
        result["inferred_clip_start"]=result["file_offset"]-result["clip_offset"]*result["scale"]
        out.append(result)
    matches[key]=out
origins={k:statistics.median(r["inferred_clip_start"] for r in v) for k,v in matches.items()}
source_label={k:int(k[:2])*3600+int(k[2:4])*60+int(k[4:]) for k in matches}
target=8*3600+35*60
sensitivity=[]
for first in ("082924","083053"):
    last="083940"
    fit=(origins[last]-origins[first])/(source_label[last]-source_label[first])
    sensitivity.append({"brackets":[first,last],"file_seconds_per_label_second":fit,
                        "interpolated_0835_file_offset":origins[first]+(target-source_label[first])*fit})
assert all(max(r["inferred_clip_start"] for r in values)-min(r["inferred_clip_start"] for r in values)<0.7 for values in matches.values())
assert all(row["correlation"]>=.18 for values in matches.values() for row in values)
assert all(1285 < r["interpolated_0835_file_offset"] < 1310 for r in sensitivity)
print(json.dumps({"refined_matches":matches,"estimated_excerpt_origins":origins,
                  "label_interpolations":sensitivity},indent=2))
