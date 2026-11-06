"""Compare three published excerpts with two separately archived Command Center lines."""
import importlib.util
import json
from pathlib import Path
import sys

def read_matcher(path):
    spec=importlib.util.spec_from_file_location("matcher",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def compare(matcher, line, reference, clips, window):
    coarse_scales=matcher.SCALES
    result={}
    for key,offsets,length in (("090234",(2,12),7),("090322",(2,12),7),("090608",(.35,),2.7)):
        excerpt=matcher.decode(clips[key],0)
        probes=[]
        for offset in offsets:
            matcher.SCALES=coarse_scales
            coarse=matcher.match(reference,excerpt,window,offset,length)
            start=coarse["file_offset"]-1
            local=matcher.decode(line,0,start,length+2.3)
            matcher.SCALES=tuple(round(coarse["scale"]+i*.00025,5) for i in range(-20,21))
            fine=matcher.match(local,excerpt,start,offset,length)
            fine.pop("off_target_peak")
            fine["estimated_clip_start"]=fine["file_offset"]-offset*fine["scale"]
            probes.append({"coarse":coarse,"refined":fine})
        result[key]=probes
    matcher.SCALES=coarse_scales
    return result

def main(matcher_path,line_5114,line_5115,control_dir,target):
    matcher=read_matcher(matcher_path)
    clip_paths={k:control_dir/f"excerpt-{k}.mp3" for k in ("090234","090322")}
    clip_paths["090608"]=target
    start,end=2910,3350
    lines={"5114":line_5114,"5115":line_5115}
    matches={}
    negatives={}
    for name,line in lines.items():
        reference=matcher.decode(line,0,start,end-start)
        matches[name]=compare(matcher,line,reference,clip_paths,start)
        wrong=matcher.decode(line,0,820,260)
        negatives[name]=matcher.match(wrong,matcher.decode(target,0),820,.35,2.7)
    print(json.dumps({"search_window_file_s":[start,end],"matches":matches,
                      "early_wrong_window_file_s":[820,1080],"early_090608_control":negatives},indent=2))

if __name__=="__main__":
    main(*map(Path,sys.argv[1:]))
