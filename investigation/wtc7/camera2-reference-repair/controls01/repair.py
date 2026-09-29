"""Versioned one-reference repair; fixed v1 numerics, no physical calibration."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import PIL
from PIL import Image, ImageDraw

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'reference-motion'
MEDIA = HERE.parent/'multiview-onset-review'
ROOT = HERE.parents[2]
EVALUATION = (6593,6654,6751,6931,7013,7104)


def require(value,label):
    if not value:
        raise ValueError(label)


def fp(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}


def save(path,value):
    with path.open('x') as stream:
        stream.write(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def read(path):
    return json.loads(path.read_text())


def numerical_module():
    path = PRIOR/'measure.py'
    require(fp(path)['sha256']=='adb48c18a928ab44bba0f30cc8b6cdffbdd3a60918464600a568249b7822640e','frozen-numerics')
    spec = importlib.util.spec_from_file_location('frozen_reference_numerics',path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def camera2_inputs(baseline_only=False):
    expected = {
        MEDIA/'refine01/receipt.json':'c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503',
        MEDIA/'refine01/camera2/selection.json':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e',
        MEDIA/'refinement.json':'700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a',
        PRIOR/'features.json':'19ab4b1cd47e51a93e757efae5faf5281c68125855dd5b64fa3724053f4e89b2',
    }
    pins = {str(p):fp(p) for p in expected}
    require(all(pins[str(p)]['sha256']==digest for p,digest in expected.items()),'prior-input-pin')
    selection = read(MEDIA/'refine01/camera2/selection.json')
    wanted = read(MEDIA/'refinement.json')['rules']['camera2']['groups']['event']
    rows = [r for r in selection['images'] if int(r['frame_index_zero_based']) in wanted]
    require([int(r['frame_index_zero_based']) for r in rows]==wanted and len(rows)==71,'declared-frame-set')
    require(int(rows[0]['frame_index_zero_based'])==6593,'baseline-frame')
    for path,identity in selection['input_pins'].items():
        actual = ROOT/path
        require(fp(actual)==identity,'source-map-pin')
        pins[str(actual)] = identity
    if baseline_only:
        rows = rows[:1]
    arrays = []
    previous = None
    for row in rows:
        index = int(row['frame_index_zero_based'])
        require(row['png']==f'f{index:06d}.png','image-name')
        path = MEDIA/'refine01/camera2'/row['png']
        require(fp(path)==row['png_identity'],'png-identity')
        with Image.open(path) as image:
            require(image.mode=='L' and image.size==(640,480),'stored-image-contract')
            array = np.array(image)
        require(hashlib.sha256(array.tobytes()).hexdigest()==row['luma_sha256'],'luma-identity')
        time = Fraction(row['source_time_seconds_exact'])
        require(time==int(row['source_pts'])*Fraction(row['source_time_base']),'exact-PTS')
        require(previous is None or time>previous,'PTS-order')
        previous = time
        pins[str(path)] = fp(path)
        arrays.append(array)
    return rows,arrays,pins


def candidates_and_visual(need_visual):
    candidates = read(HERE/'candidate-seeds.json')['candidates']
    require(1<=len(candidates)<=3,'candidate-count')
    require([c['id'] for c in candidates]==['C2-R7','C2-R8','C2-R9'][:len(candidates)],'candidate-order-identities')
    for c in candidates:
        require(isinstance(c['xy'],list) and len(c['xy'])==2 and all(type(v) is int for v in c['xy']),'integer-seed')
        require(13<=c['xy'][0]<627 and 13<=c['xy'][1]<467,'seed-support')
        require(isinstance(c['description'],str) and c['description'].strip(),'candidate-description')
    visual = read(HERE/'visual-review.json') if need_visual else None
    if visual is not None:
        require(visual['review_kind']=='computational_baseline_visual_check_not_human','visual-review-kind')
        require(visual['candidate_file']==fp(HERE/'candidate-seeds.json'),'visual-candidate-pin')
        require(set(visual['candidate_acceptance'])=={c['id'] for c in candidates},'visual-review-coverage')
        require(all(type(v) is bool for v in visual['candidate_acceptance'].values()),'visual-status-type')
    return candidates,visual


def selected_id(candidates,visual,records):
    allowed = []
    for candidate in candidates:
        rows = [r for r in records if r['reference']==candidate['id']]
        require(sorted(r['half'] for r in rows)==[9,13],'preflight-size-coverage')
        if visual['candidate_acceptance'][candidate['id']] and all(r['status']=='candidate' for r in rows):
            allowed.append(candidate['id'])
    return allowed[0] if allowed else None


def frame_analysis(module,features,templates,frame,stamp):
    index = int(stamp['frame_index_zero_based'])
    rows,models,grids = [],[],{}
    for half in (9,13):
        current = []
        for feature in features:
            result,scores = module.match(frame,templates[(feature['id'],half)],feature['xy'],24)
            key = f'camera2_{index}_{half}_{feature["id"]}'
            row = dict(result,camera='camera2',index=index,pts=stamp['source_pts'],time_base=stamp['source_time_base'],
                seconds_exact=stamp['source_time_seconds_exact'],half=half,reference=feature['id'],
                baseline_xy=feature['xy'],score_grid=key)
            rows.append(row)
            current.append(row)
            grids[key] = scores
        for model in ('translation','similarity','affine'):
            row = {'camera':'camera2','index':index,'half':half,'model':model,
                'seconds_exact':stamp['source_time_seconds_exact'],'reference_order':[f['id'] for f in features]}
            failed = [r['reference'] for r in current if r['status']!='candidate']
            if failed:
                row.update(status='reference_quality_failure',passes_consistency_screen=False,failed_references=failed)
            else:
                row.update(module.fit_with_loo([f['xy'] for f in features],[r['candidate_xy'] for r in current],model))
            models.append(row)
    return rows,models,grids


def template_arrays(frame,features):
    result = {}
    for feature in features:
        x,y = feature['xy']
        for half in (9,13):
            value = frame[y-half:y+half+1,x-half:x+half+1].copy()
            require(value.shape==(half*2+1,half*2+1),'template-shape')
            result[(feature['id'],half)] = value
    return result


def overlay(frame,rows,footer,path):
    image = Image.new('RGB',(frame.shape[1],frame.shape[0]+34),'white')
    image.paste(Image.fromarray(frame).convert('RGB'),(0,0))
    draw = ImageDraw.Draw(image)
    for row in rows:
        if 'candidate_xy' not in row:
            continue
        x,y = row['candidate_xy']
        color = 'lime' if row['status']=='candidate' else 'red'
        draw.rectangle((x-4,y-4,x+4,y+4),outline=color)
        draw.text((x+5,y),row['reference'],fill=color)
    draw.text((4,frame.shape[0]+2),footer,fill='black')
    draw.text((4,frame.shape[0]+17),'ANALYTICAL DERIVATIVE; candidates are not physical tracks',fill='black')
    image.save(path)


def execute(stage,out,preflight=None):
    out.mkdir(parents=True,exist_ok=False)
    pins = {}
    try:
        procedure = [Path(__file__),HERE/'PROTOCOL.md',HERE/'candidate-seeds.json',HERE/'test_repair.py',PRIOR/'measure.py']
        if stage!='prepare':
            procedure.append(HERE/'visual-review.json')
        pins = {str(p):fp(p) for p in procedure+[Path(sys.executable)]}
        for i,path in enumerate(procedure):
            (out/f'snapshot-{i}-{path.name}').write_bytes(path.read_bytes())
        save(out/'initial.json',{'stage':stage,'pins':pins,'python':sys.version,'numpy':np.__version__,'pillow':PIL.__version__})
        candidates,visual = candidates_and_visual(stage!='prepare')
        stamps,arrays,input_pins = camera2_inputs(baseline_only=stage!='run')
        pins.update(input_pins)
        baseline = arrays[0]
        if stage=='prepare':
            rows = [{'candidate_xy':c['xy'],'reference':c['id'],'status':'candidate'} for c in candidates]
            overlay(baseline,rows,'UNSCORED BASELINE PROPOSALS; green is position marker only',out/'baseline-markers.png')
            for c in candidates:
                for half in (9,13):
                    x,y = c['xy']
                    crop = Image.fromarray(baseline[y-half:y+half+1,x-half:x+half+1])
                    crop.save(out/f'patch-{c["id"]}-{half}.png')
                    zoom = crop.resize((crop.width*10,crop.height*10),Image.Resampling.NEAREST).convert('RGB')
                    panel = Image.new('RGB',(max(zoom.width,380),zoom.height+34),'white')
                    panel.paste(zoom,(0,0))
                    draw=ImageDraw.Draw(panel)
                    draw.rectangle((half*10,half*10,half*10+9,half*10+9),outline='red')
                    draw.text((3,zoom.height+3),f'{c["id"]} native center {c["xy"]}, side {2*half+1}',fill='black')
                    draw.text((3,zoom.height+17),'10x NEAREST DISPLAY ONLY; red marks seed pixel',fill='black')
                    panel.save(out/f'patch-display-{c["id"]}-{half}.png')
            save(out/'input-pins.json',input_pins)
        elif stage=='preflight':
            module = numerical_module()
            prior = read(PRIOR/'features.json')['camera2']
            retained = [f for f in prior if f['id']!='C2-R3']
            scored,grids = [],{}
            for feature in retained+candidates:
                for half in (9,13):
                    x,y = feature['xy']
                    record,scores = module.match(baseline,baseline[y-half:y+half+1,x-half:x+half+1],feature['xy'],24)
                    scored.append(dict(record,reference=feature['id'],half=half,baseline_xy=feature['xy']))
                    grids[f'{feature["id"]}_{half}'] = scores
            new_id = selected_id(candidates,visual,scored)
            save(out/'baseline-scores.json',scored)
            np.savez_compressed(out/'baseline-grids.npz',**grids)
            require(all(r['status']=='candidate' for r in scored if r['reference'] in {f['id'] for f in retained}),'retained-baseline-failure')
            if new_id is None:
                save(out/'selection.json',{'status':'no_candidate_qualified','selected':None})
            else:
                replacement = next(c for c in candidates if c['id']==new_id)
                features = [replacement if f['id']=='C2-R3' else f for f in prior]
                save(out/'selection.json',{'status':'selected_baseline_only_not_validated_track','selected':new_id,
                    'features':features,'half_widths':[9,13],'radius':24,'visual_review':fp(HERE/'visual-review.json'),
                    'candidate_file':fp(HERE/'candidate-seeds.json')})
            save(out/'input-pins.json',input_pins)
        else:
            require(preflight is not None and preflight.parent.resolve()==HERE,'preflight-scope')
            receipt = read(preflight/'receipt.json')
            require(receipt['stage']=='preflight' and receipt['status']=='complete','preflight-complete')
            require(all(fp(preflight/n)==identity for n,identity in receipt['products'].items()),'preflight-products')
            selection = read(preflight/'selection.json')
            require(selection['status']=='selected_baseline_only_not_validated_track','preflight-selected')
            require(selection['visual_review']==fp(HERE/'visual-review.json') and selection['candidate_file']==fp(HERE/'candidate-seeds.json'),'preflight-selection-pins')
            for name in ('receipt.json','selection.json'):
                pins[str(preflight/name)] = fp(preflight/name)
                (out/f'preflight-{name}').write_bytes((preflight/name).read_bytes())
            features = selection['features']
            prior = read(PRIOR/'features.json')['camera2']
            require(len(features)==6 and [f for f in features if f['id']!=selection['selected']]==[f for f in prior if f['id']!='C2-R3'],'single-reference-change')
            module = numerical_module()
            templates = template_arrays(baseline,features)
            matches,models,grids = [],[],{}
            for stamp,frame in zip(stamps,arrays):
                rows,fits,scores = frame_analysis(module,features,templates,frame,stamp)
                matches.extend(rows); models.extend(fits); grids.update(scores)
                index = int(stamp['frame_index_zero_based'])
                if index in EVALUATION:
                    for half in (9,13):
                        overlay(frame,[r for r in rows if r['half']==half],f'Camera2 repair frame {index}, half {half}',out/f'overlay-{index}-{half}.png')
            require((len(matches),len(models),len(grids))==(852,426,852),'historical-coverage')
            save(out/'matches.json',matches); save(out/'transforms.json',models)
            np.savez_compressed(out/'score-grids.npz',**grids)
            save(out/'input-pins.json',input_pins)
        require(all(fp(Path(p))==identity for p,identity in pins.items()),'post-input-procedure-pins')
        save(out/'receipt.json',{'stage':stage,'status':'complete','pins':pins,
            'products':{p.name:fp(p) for p in sorted(out.iterdir()) if p.is_file()}})
        print(json.dumps({'stage':stage,'status':'complete'}))
    except Exception as error:
        save(out/'failure.json',{'stage':stage,'exception_type':type(error).__name__,'message':str(error)})
        raise


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=['prepare','preflight','run'])
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--preflight',type=Path)
    args = parser.parse_args()
    execute(args.stage,args.out,args.preflight)
