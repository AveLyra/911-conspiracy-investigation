"""Fixed-fit regional diagnostics; no new geometry fit or exposure threshold."""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

import match_screen as core

BASE=Path(__file__).resolve().parent
REGIONS={
 '148':{'W1':(296,123,377,175),'W2':(340,295,380,338),'W3':(426,294,456,339),'W4':(523,295,556,339),
        'D1':(388,143,417,169),'D2':(299,304,338,331),'D3':(388,304,416,332),'D4':(261,231,567,293)},
 '149':{'W1':(164,125,580,173),'W2':(281,204,580,247),
        'D1':(265,278,291,328),'D2':(315,278,414,337),'D3':(447,278,568,342),'D4':(280,15,592,87)},
}
EXCLUSIONS={
 '148':[(251,82,289,112),(408,87,447,118),(537,95,575,124),(602,43,648,79),(604,132,636,169),
        (603,219,635,255),(603,303,634,340),(600,398,634,433),(0,444,260,478)],
 '149':[(272,92,311,121),(423,99,462,131),(535,103,574,131),(611,53,656,89),(612,133,658,170),
        (612,214,658,250),(613,295,658,331),(615,366,660,406),(613,451,643,478),(0,449,264,478),
        (3,237,65,339),(683,210,717,266)],
}


def main():
    p=argparse.ArgumentParser();p.add_argument('--summary',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    summary=json.loads(a.summary.read_text());results=[];inputs={}
    for key in REGIONS:
        candidate_rows={r['source_pts']:r for item in summary['results'][key].values() for r in item['top_four']}
        asset,h,*_=core.TARGETS[key];target_path=core.MAIN/'fire-annotation/assets/run-01/images'/f'{asset}.jpg'
        if core.sha(target_path)!=h:raise ValueError('target pin')
        with Image.open(target_path) as im:target=core.working(im)
        excluded=core.mask_for([(x0-4,y0-4,x1+4,y1+4) for x0,y0,x1,y1 in EXCLUSIONS[key]])
        inside=core.mask_for([(3,3,717,475)])
        masks={name:core.mask_for([box])&inside&~excluded for name,box in REGIONS[key].items()}
        for pts,row in sorted(candidate_rows.items()):
            folder=BASE/row['run'];path=Path(row['native_png'])
            if path.parent!=folder or path.name!=f"native-{row['frame_index']:04d}.png":raise ValueError('native path')
            receipt_path=folder/'receipt.json'
            if core.sha(receipt_path)!=summary['chunk_receipt_pins'][row['run']]:raise ValueError('receipt pin')
            receipt=json.loads(receipt_path.read_text());pin=receipt['outputs'][path.name]
            if core.sha(path)!=pin['sha256'] or path.stat().st_size!=pin['bytes']:raise ValueError('native pin')
            inputs[str(path)]=pin
            with Image.open(path) as im:work=core.working(im)
            best=row['geometry_candidates'][0]
            canvas,valid,transform=core.canvas_for(work,best['requested_scale'])
            if any(best[k]!=v for k,v in transform.items()):raise ValueError('transform mismatch')
            x,y=best['left'],best['top'];view=canvas[y:y+120,x:x+180];good=valid[y:y+120,x:x+180].astype(bool)
            metrics={}
            for name,mask in masks.items():
                overlap=mask&good;coverage=float(overlap.sum()/mask.sum()) if mask.any() else 0
                rho=core.scalar_pearson(view,target,overlap) if coverage>=.85 else None
                metrics[name]={'selected_pixels':int(mask.sum()),'valid_pixels':int(overlap.sum()),'coverage':coverage,'grayscale_pearson':rho}
            results.append({'target':key,'source_pts':pts,'run':row['run'],'frame_index':row['frame_index'],
                'fixed_foreground_transform':best,'regions':metrics})
    core.save(a.output,{'status':'completed','script_sha256':core.sha(__file__),'core_sha256':core.sha(core.__file__),
        'declaration_sha256':core.sha(BASE/'CANDIDATE-REVIEW-01.md'),'summary_sha256':core.sha(a.summary),
        'inputs':inputs,'regions':REGIONS,'exclusions':EXCLUSIONS,'exclusion_expansion_pixels':4,'results':results,
        'limits':'Conditional grayscale diagnostics, not independent transform fits, pure-flame measures, probabilities or exposure identification.'})
    print(json.dumps({'status':'completed','candidate_target_pairs':len(results),'region_diagnostics':sum(len(r['regions']) for r in results)}))


if __name__=='__main__':main()
