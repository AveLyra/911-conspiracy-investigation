#!/usr/bin/env python3
"""Declared native frames and separately marked saved-coordinate queries."""
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
INDICES = list(range(138,349,30))
SIZE = (720,480)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':digest(data)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    args=p.parse_args()
    if not re.fullmatch(r'[a-z0-9_-]+',args.out):
        raise ValueError('invalid_output_name')
    output=HERE/args.out
    if output.exists(): raise ValueError('output_exists')
    inputs={'source':SOURCE,'binary':BIN,'prior_receipt':OLD/'receipt.json',
            'map':OLD/'default-frames.json','points':HERE/'extraction01/points.json',
            'point_receipt':HERE/'extraction01/receipt.json',
            'protocol':HERE/'PROTOCOL.md','producer':Path(__file__)}
    before={k:pin(v) for k,v in inputs.items()}
    assert before['source']['sha256']=='48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722'
    old=json.loads(inputs['prior_receipt'].read_text())
    frame_map=json.loads(inputs['map'].read_text())
    point_receipt=json.loads(inputs['point_receipt'].read_text())
    assert before['map']['sha256']=='8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2'
    assert before['binary']['sha256']==old['binaries'][str(BIN)]['sha256']
    assert before['points']==point_receipt['points']
    assert before['protocol']==point_receipt['inputs_before']['protocol']
    points=json.loads(inputs['points'].read_text())
    argv=[str(BIN),'-nostdin','-nostats','-hide_banner','-loglevel',
          'repeat+level+info','-debug_ts','-copyts','-noautorotate',
          '-i',str(SOURCE),'-map','0:v:0','-an','-noautoscale',
          '-pix_fmt','gray','-fps_mode','passthrough',
          '-enc_time_base:v','demux','-f','rawvideo','-']
    assert argv==[c for c in old['commands'] if c['label']=='default'][0]['argv']
    output.mkdir()
    completed=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    raw=completed.stdout
    count=SIZE[0]*SIZE[1]
    hashes=[digest(raw[i:i+count]) for i in range(0,len(raw),count)]
    execution={'returncode':completed.returncode,'argv':argv,'raw_bytes':len(raw),
               'raw_sha256':digest(raw),'all_frame_hashes_match':hashes==frame_map['pixel_hashes'],
               'stderr_bytes':len(completed.stderr),'stderr_sha256':digest(completed.stderr),
               'corrupt_decoded_frame_mentions':completed.stderr.count(b'corrupt decoded frame'),
               'stderr_not_exported':True}
    if completed.returncode or len(raw)!=442*count or digest(raw)!=frame_map['raw_sha256'] or hashes!=frame_map['pixel_hashes']:
        (output/'failure.json').write_text(json.dumps(execution,indent=2)+'\n')
        raise RuntimeError('diagnostic_decode_identity_failed')
    selected=[]
    for index in INDICES:
        pixels=raw[index*count:(index+1)*count]
        im=Image.frombytes('L',SIZE,pixels)
        native=output/f'frame-{index:04d}.png'
        im.save(native)
        assert Image.open(native).tobytes()==pixels
        overlay=im.convert('RGB')
        draw=ImageDraw.Draw(overlay)
        marks=[]
        for track,color in zip(points['tracks'],[(0,255,255),(255,255,0)]):
            row=[q for q in track['points'] if q['frame']==index]
            assert len(row)==1
            x,y=row[0]['x'],row[0]['y']
            cx,cy=round(x),round(y)
            # Raster-centre query; cross arms leave the central 7x7 area unmarked.
            for a,b,c,d in [(cx-12,cy,cx-4,cy),(cx+4,cy,cx+12,cy),
                            (cx,cy-12,cx,cy-4),(cx,cy+4,cx,cy+12)]:
                draw.line((a,b,c,d),fill=color,width=1)
            marks.append({'track':track['track'],'x':x,'y':y,'raster_center':[cx,cy],
                          'rgb':list(color),'within_native_bounds':0<=x<720 and 0<=y<480,
                          'cross_box_inside':12<=cx<708 and 12<=cy<468})
        marked=output/f'queries-{index:04d}.png'
        overlay.save(marked)
        selected.append({'index':index,'native':{'name':native.name,**pin(native)},
                         'overlay':{'name':marked.name,**pin(marked)},
                         'pixel_sha256':hashes[index],'marks':marks})
    after={k:pin(v) for k,v in inputs.items()}
    assert before==after
    receipt={'status':'pass_diagnostic_view_only','python':platform.python_version(),
             'pillow':pillow_version,'inputs_before':before,'inputs_after':after,
             'execution':execution,'selected':selected,
             'overlay_convention':'native integer pixel centres; nearest integer query; cyan track01, yellow track02; no source annotation or localization claim'}
    (output/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'selected':INDICES,'full_raw_match':True}))


if __name__=='__main__': main()
