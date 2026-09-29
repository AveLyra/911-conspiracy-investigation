#!/usr/bin/env python3
"""Source-pinned, unmarked dense image products; no original point access."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
from PIL import Image, ImageDraw, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
PUBLIC = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
SOURCE = PUBLIC/'camera3-provenance/kit-inventory/run-v1/outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv'
OLD = PUBLIC/'camera3-recording-comparison/wmv-diagnostic/run02'
BIN = Path('/opt/homebrew/bin/ffmpeg')
INDICES = [258] + list(range(288,349,3))
CROP = (295,125,535,375)
REFS = [('R1',272,400),('R2',168,348),('R3',673,292)]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':digest(data)}

def ruler(image, box, factor):
    left,top,right,bottom=box
    patch=image.crop(box).resize(((right-left)*factor,(bottom-top)*factor),Image.Resampling.NEAREST)
    out=Image.new('RGB',(patch.width+50,patch.height+35),'white')
    out.paste(patch,(50,35))
    draw=ImageDraw.Draw(out)
    for x in range(left,right):
        cx=50+(x-left)*factor+(factor-1)//2
        draw.line((cx,31 if x%5==0 else 33,cx,34),fill='black')
        if x%10==0: draw.text((cx-8,15),str(x),fill='black')
    for y in range(top,bottom):
        cy=35+(y-top)*factor+(factor-1)//2
        draw.line((45 if y%5==0 else 48,cy,49,cy),fill='black')
        if y%5==0: draw.text((15,cy-5),str(y),fill='black')
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    if not re.fullmatch('[a-z0-9_-]+',args.out): raise ValueError('invalid_output_name')
    out=HERE/args.out
    if out.exists(): raise ValueError('output_exists')
    inputs={'source':SOURCE,'binary':BIN,'map':OLD/'default-frames.json',
            'old_receipt':OLD/'receipt.json','protocol':HERE/'PROTOCOL.md','code':Path(__file__)}
    before={k:pin(p) for k,p in inputs.items()}
    assert before['source']['sha256']=='48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722'
    assert before['map']['sha256']=='8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2'
    old=json.loads(inputs['old_receipt'].read_text())
    mapping=json.loads(inputs['map'].read_text())
    assert before['binary']['sha256']==old['binaries'][str(BIN)]['sha256']
    argv=[c['argv'] for c in old['commands'] if c['label']=='default']
    assert len(argv)==1
    expected=[str(BIN),'-nostdin','-nostats','-hide_banner','-loglevel','repeat+level+info',
              '-debug_ts','-copyts','-noautorotate','-i',str(SOURCE),'-map','0:v:0','-an',
              '-noautoscale','-pix_fmt','gray','-fps_mode','passthrough',
              '-enc_time_base:v','demux','-f','rawvideo','-']
    assert argv[0]==expected
    out.mkdir()
    proc=subprocess.run(expected,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    raw=proc.stdout
    size=720*480
    frame_hashes=[digest(raw[i:i+size]) for i in range(0,len(raw),size)]
    execution={'argv':expected,'returncode':proc.returncode,'raw_bytes':len(raw),
               'raw_sha256':digest(raw),'stderr_bytes':len(proc.stderr),'stderr_sha256':digest(proc.stderr),
               'corrupt_mentions':proc.stderr.count(b'corrupt decoded frame'),'stderr_not_exported':True,
               'all_frames_match':frame_hashes==mapping['pixel_hashes']}
    if proc.returncode or len(raw)!=442*size or digest(raw)!=mapping['raw_sha256'] or not execution['all_frames_match']:
        (out/'failure.json').write_text(json.dumps(execution,indent=2)+'\n')
        raise RuntimeError('decode_identity_failure')
    products=[]
    rows=[]
    def save(im,name,role):
        p=out/name
        im.save(p)
        products.append({'name':name,'role':role,**pin(p)})
    for index in INDICES:
        pixels=raw[index*size:(index+1)*size]
        im=Image.frombytes('L',(720,480),pixels)
        save(im,f'frame-{index:04d}.png','native_unmarked')
        save(ruler(im,CROP,3),f'target-{index:04d}.png','fixed_crop_nearest_x3_margin_rulers')
        rows.append({'index':index,'clock':mapping['records'][index],
                     'pixel_sha256':frame_hashes[index]})
        if index==288:
            overlay=im.convert('RGB')
            draw=ImageDraw.Draw(overlay)
            for name,x,y in REFS:
                draw.rectangle((x-15,y-15,x+15,y+15),outline=(255,0,255))
                draw.text((x-15,y-28),name,fill=(255,0,255))
                for side in (21,31):
                    h=side//2
                    save(ruler(im,(x-h,y-h,x+h+1,y+h+1),8),f'baseline-{name}-{side}.png','reference_preflight_crop_nearest_x8')
            save(overlay,'reference-baseline.png','analytical_reference_boxes')
    after={k:pin(p) for k,p in inputs.items()}
    assert before==after
    receipt={'status':'pass_diagnostic_only','python':platform.python_version(),'pillow':pillow_version,
             'inputs_before':before,'inputs_after':after,'execution':execution,'rows':rows,
             'products':products,'crop_box_half_open':CROP,'factor':3,
             'references':[{'name':n,'x':x,'y':y} for n,x,y in REFS],
             'ruler_convention':'source integer pixel centers; tick at center of nearest-neighbor replicated block; image pixels untouched'}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'native_frames':len(rows),'products':len(products),'all_442_match':True}))

if __name__=='__main__': main()
