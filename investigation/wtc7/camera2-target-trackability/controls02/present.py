"""Source-pinned coordinate aids, not automated historical measurements."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MEDIA = HERE.parent/'multiview-onset-review'
FRAMES = (6593,6654,6751,6841,6886,6916,6931,6946,6961,6976,6991,7006,7021,7036,7051,7081,7104)
CROP = (270,95,475,400)
SCALE, LEFT, TOP = 3, 40, 28


def require(condition, label):
    if not condition:
        raise ValueError(label)


def fp(path):
    with path.open('rb') as stream:
        return {'bytes':path.stat().st_size, 'sha256':hashlib.file_digest(stream,'sha256').hexdigest()}


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def panel(source, title):
    x0,y0,x1,y1 = CROP
    enlarged = source.crop(CROP).resize(((x1-x0)*SCALE,(y1-y0)*SCALE),Image.Resampling.NEAREST).convert('RGB')
    result = Image.new('RGB',(LEFT+enlarged.width+10,TOP+enlarged.height+40),'white')
    result.paste(enlarged,(LEFT,TOP))
    draw = ImageDraw.Draw(result)
    for x in range(x0,x1,10):
        u = LEFT+(x-x0)*SCALE
        draw.line((u,TOP-4,u,TOP-1),fill='black')
        draw.text((u-8,TOP-17),str(x),fill='black')
    for y in range(100,y1,10):
        v = TOP+(y-y0)*SCALE
        draw.line((LEFT-4,v,LEFT-1,v),fill='black')
        draw.text((3,v-5),str(y),fill='black')
    draw.text((3,TOP+enlarged.height+3),title,fill='black')
    draw.text((3,TOP+enlarged.height+18),'3x NEAREST ANALYTICAL DISPLAY; ticks are source pixels; no feature marks',fill='black')
    return result


def inputs():
    fixed = {
        MEDIA/'refine01/camera2/selection.json':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e',
        MEDIA/'refinement.json':'700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a',
        MEDIA/'refine01/receipt.json':'c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503',
    }
    pins = {str(p):fp(p) for p in fixed}
    require(all(pins[str(p)]['sha256']==digest for p,digest in fixed.items()),'frozen parent inputs')
    selection = read(MEDIA/'refine01/camera2/selection.json')
    event = read(MEDIA/'refinement.json')['rules']['camera2']['groups']['event']
    require(len(event)==71 and set(FRAMES)<=set(event),'declared event subset')
    allowed_sources = {
        ROOT/'research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov',
        HERE.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv',
        HERE.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frames.json',
        HERE.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/source-identity.json',
    }
    source_pins = {ROOT/p:identity for p,identity in selection['input_pins'].items()}
    require(set(source_pins)==allowed_sources,'source-map path scope')
    for path,identity in source_pins.items():
        require(fp(path)==identity,'source-map identity')
        pins[str(path)] = identity
    rows = [r for r in selection['images'] if int(r['frame_index_zero_based']) in FRAMES]
    require(tuple(int(r['frame_index_zero_based']) for r in rows)==FRAMES,'exact ordered frame set')
    images,previous = [],None
    for row in rows:
        index = int(row['frame_index_zero_based'])
        require(row['png']==f'f{index:06d}.png','native filename')
        path = MEDIA/'refine01/camera2'/row['png']
        require(fp(path)==row['png_identity'],'PNG identity')
        with Image.open(path) as image:
            require(image.format=='PNG' and image.mode=='L' and image.size==(640,480),'native geometry and mode')
            image.load()
            image = image.copy()
        require(hashlib.sha256(image.tobytes()).hexdigest()==row['luma_sha256'],'native luma identity')
        seconds = Fraction(row['source_time_seconds_exact'])
        require(seconds==int(row['source_pts'])*Fraction(row['source_time_base']),'exact PTS')
        require(previous is None or seconds>previous,'ordered source clock')
        previous = seconds
        images.append(image)
        pins[str(path)] = fp(path)
    return rows,images,pins


def controls(out):
    y,x = np.indices((480,640))
    source = Image.fromarray(np.stack((x%256,y%256,x//256+4*(y//256)),axis=2).astype('uint8'))
    result = panel(source,'SYNTHETIC COORDINATE CONTROL; not historical imagery')
    actual = np.array(result)[TOP:TOP+915,LEFT:LEFT+615]
    expected = np.repeat(np.repeat(np.array(source)[95:400,270:475],3,axis=0),3,axis=1)
    require(np.array_equal(actual,expected),'every nearest source-pixel block')
    source.save(out/'synthetic-source.png')
    result.save(out/'synthetic-panel.png')
    for x,y in ((270,95),(474,399),(424,144),(454,156)):
        u,v = LEFT+(x-270)*3,TOP+(y-95)*3
        require(result.getpixel((u,v))==source.getpixel((x,y)),'coordinate origin and endpoints')
    for x in range(270,475,10):
        u = LEFT+(x-270)*3
        require(result.getpixel((u,TOP-2))==(0,0,0),'x tick coordinate')
    for y in range(100,400,10):
        v = TOP+(y-95)*3
        require(result.getpixel((LEFT-2,v))==(0,0,0),'y tick coordinate')
    return {'every_pixel_block_equal':True,'coordinate_points_checked':4,'x_ticks':21,'y_ticks':30,
            'scope':'Deterministic display geometry, not feature localization or material identity.'}


def execute(stage,out):
    out.mkdir(parents=True,exist_ok=False)
    before = {str(p):fp(p) for p in (Path(__file__),HERE/'PROTOCOL.md',Path(sys.executable))}
    try:
        for name,p in (('present.py',Path(__file__)),('PROTOCOL.md',HERE/'PROTOCOL.md')):
            (out/name).write_bytes(p.read_bytes())
        save(out/'initial.json',{'stage':stage,'pins':before.copy(),'python':sys.version,'numpy':np.__version__,'pillow':PIL.__version__})
        if stage=='controls':
            detail = controls(out)
        else:
            rows,images,pins = inputs()
            before.update(pins)
            detail = {'rows':rows,'displays':[],'crop_xyxy_exclusive':CROP,'scale':SCALE,
                      'pixel_origin_in_panel':[LEFT,TOP],'display_size':[665,983]}
            for row,image in zip(rows,images):
                index = int(row['frame_index_zero_based'])
                name = f'f{index:06d}-target-panel.png'
                panel(image,f'Camera2 source index {index}; exact PTS seconds {row["source_time_seconds_exact"]}').save(out/name)
                detail['displays'].append({'frame':index,'path':name,'parent_png':row['png_identity']})
            save(out/'input-pins.json',pins)
        save(out/'detail.json',detail)
        require(all(fp(Path(p))==identity for p,identity in before.items()),'inputs changed during generation')
        save(out/'receipt.json',{'stage':stage,'status':'complete','pins':before,
                               'products':{p.name:fp(p) for p in sorted(out.iterdir()) if p.is_file()}})
        print(json.dumps({'stage':stage,'status':'complete','products':len(list(out.iterdir()))}))
    except Exception as error:
        save(out/'failure.json',{'stage':stage,'error_type':type(error).__name__,'error':str(error)})
        raise


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=('controls','prepare'))
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    execute(args.stage,args.out)
