"""Fixed-reference candidate matching and image-map diagnostics, not physical motion."""
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
BASE = HERE.parent/'multiview-onset-review'
ROOT = HERE.parents[2]
PINS = {
    BASE/'refine01/receipt.json':'c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503',
    BASE/'refine01/camera2/selection.json':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e',
    BASE/'refine01/camera4/selection.json':'143aa3759d516299b508ddd81545f981797f58382b39f1c2a9a6189ff90faf1e',
    BASE/'refinement.json':'700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a',
}
EVALUATION = {'camera2':[6654,6751,6931,7013,7104], 'camera4':[960,1042,1162,1259,1350]}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fp(path):
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':value}


def save(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def match(frame, template, center, radius=24):
    require(isinstance(frame,np.ndarray) and frame.dtype==np.uint8 and frame.ndim==2, 'frame-contract')
    require(isinstance(template,np.ndarray) and template.dtype==np.uint8 and template.ndim==2, 'template-contract')
    side = template.shape[0]
    require(side==template.shape[1] and side>=3 and side%2==1, 'template-geometry')
    require(len(center)==2 and all(type(c) is int for c in center) and type(radius) is int and radius>=4, 'center-contract')
    half=side//2
    x,y=center
    require(half<=x<frame.shape[1]-half and half<=y<frame.shape[0]-half, 'seed-bounds')
    x0,x1=max(half,x-radius),min(frame.shape[1]-half-1,x+radius)
    y0,y1=max(half,y-radius),min(frame.shape[0]-half-1,y+radius)
    region=frame[y0-half:y1+half+1,x0-half:x1+half+1].astype(np.float64)
    windows=np.lib.stride_tricks.sliding_window_view(region,template.shape)
    t=template.astype(np.float64)
    tc=t-t.mean()
    te=float(np.sum(tc*tc))
    sums=windows.sum(axis=(-2,-1))
    energy=(windows*windows).sum(axis=(-2,-1))-sums*sums/template.size
    require(np.all(np.isfinite(energy)) and np.all(energy>=-1e-7), 'energy-contract')
    denom=np.sqrt(np.maximum(energy,0)*te)
    numerator=np.einsum('ijkl,kl->ij',windows,tc)
    scores=np.full(denom.shape,np.nan,dtype=np.float64)
    np.divide(numerator,denom,out=scores,where=denom>1e-12)
    defined=np.isfinite(scores)
    flags=[]
    result={'search_bounds':[x0,x1,y0,y1], 'template_std':float(t.std()),
            'undefined_windows':int((~defined).sum()), 'flags':flags}
    if t.std()<2:
        flags.append('low_seed_texture')
    if not defined.any():
        flags.append('no_defined_score')
        result['status']='rejected'
        return result,scores
    ranking=np.where(defined,scores,-np.inf)
    iy,ix=np.unravel_index(np.argmax(ranking),scores.shape)
    best=float(scores[iy,ix])
    ties=int(np.sum(defined & (np.abs(scores-best)<=1e-12)))
    others=ranking.copy()
    others[max(0,iy-3):iy+4,max(0,ix-3):ix+4]=-np.inf
    cy,cx=np.unravel_index(np.argmax(others),others.shape)
    competitor=float(others[cy,cx])
    boundary=ix in (0,scores.shape[1]-1) or iy in (0,scores.shape[0]-1)
    if best<0.8:
        flags.append('low_ncc')
    if ties>1:
        flags.append('tied_best')
    if not np.isfinite(competitor):
        flags.append('no_competitor')
        competitor=None
    elif best-competitor<0.02:
        flags.append('ambiguous_competitor')
    if boundary:
        flags.append('search_boundary')
    result.update(candidate_xy=[int(x0+ix),int(y0+iy)],ncc=best,
        competitor_xy=[int(x0+cx),int(y0+cy)] if competitor is not None else None,
        competitor_ncc=competitor,margin=best-competitor if competitor is not None else None,
        tied_best_count=ties,at_search_boundary=bool(boundary),status='candidate' if not flags else 'rejected')
    return result,scores


def fit_points(p,q,model):
    p=np.asarray(p,dtype=np.float64)
    q=np.asarray(q,dtype=np.float64)
    require(p.ndim==2 and p.shape==q.shape and p.shape[1]==2 and len(p)>=2, 'point-shapes')
    require(np.isfinite(p).all() and np.isfinite(q).all(), 'point-finite')
    require(model in ('translation','similarity','affine'), 'model')
    n=len(p)
    if model=='translation':
        matrix=np.eye(2)
        offset=(q-p).mean(axis=0)
        rank,condition=2,1.0
    else:
        center=p.mean(axis=0)
        scale=float(np.sqrt(np.mean(np.sum((p-center)**2,axis=1))))
        if scale<=1e-12:
            return {'status':'degenerate_source_geometry'}
        u=(p-center)/scale
        if model=='similarity':
            design=np.zeros((2*n,4))
            design[0::2,:]=np.column_stack((u[:,0],-u[:,1],np.ones(n),np.zeros(n)))
            design[1::2,:]=np.column_stack((u[:,1],u[:,0],np.zeros(n),np.ones(n)))
            solution,_,rank,s=np.linalg.lstsq(design,q.reshape(-1),rcond=1e-12)
            expected_rank=4
            matrix=np.array([[solution[0],-solution[1]],[solution[1],solution[0]]])/scale
            offset=solution[2:4]-matrix@center
        else:
            design=np.column_stack((u,np.ones(n)))
            solution,_,rank,s=np.linalg.lstsq(design,q,rcond=1e-12)
            expected_rank=3
            matrix=solution[:2,:].T/scale
            offset=solution[2,:]-matrix@center
        condition=float(s[0]/s[-1]) if s[-1]>0 else None
        if rank!=expected_rank or condition is None or condition>10000:
            return {'status':'rank_or_condition_failure','rank':int(rank),'condition':condition}
    prediction=p@matrix.T+offset
    residual=q-prediction
    norms=np.linalg.norm(residual,axis=1)
    determinant=float(np.linalg.det(matrix))
    return {'status':'computed','matrix':matrix.tolist(),'offset':offset.tolist(),'rank':int(rank),
        'normalized_design_condition':condition,'determinant':determinant,
        'positive_nonsingular':bool(determinant>1e-12), 'residual_xy':residual.tolist(),
        'rms_residual':float(np.sqrt(np.mean(norms**2))),'max_residual':float(norms.max())}


def fit_with_loo(p,q,model):
    p,q=np.asarray(p,float),np.asarray(q,float)
    fit=fit_points(p,q,model)
    if fit['status']!='computed':
        fit['passes_consistency_screen']=False
        return fit
    loo=[]
    for omitted in range(len(p)):
        keep=np.arange(len(p))!=omitted
        test=fit_points(p[keep],q[keep],model)
        if test['status']!='computed':
            loo.append({'omitted_reference':omitted,'status':test['status']})
        else:
            delta=q[omitted]-(np.array(test['matrix'])@p[omitted]+test['offset'])
            loo.append({'omitted_reference':omitted,'status':'computed','error_xy':delta.tolist(),
                        'error_norm':float(np.linalg.norm(delta)),'positive_nonsingular':test['positive_nonsingular']})
    fit['leave_one_out']=loo
    complete=all(r['status']=='computed' for r in loo)
    fit['max_loo_error']=max(r['error_norm'] for r in loo) if complete else None
    fit['passes_consistency_screen']=bool(complete and fit['positive_nonsingular'] and
        all(r['positive_nonsingular'] for r in loo) and fit['max_residual']<=2 and fit['max_loo_error']<=2)
    return fit


def load_inputs(config):
    input_pins={}
    for path,value in PINS.items():
        require(fp(path)['sha256']==value,'prior-pin')
        input_pins[str(path)]=fp(path)
    refinement=json.loads((BASE/'refinement.json').read_text())
    groups={}
    for camera in ('camera2','camera4'):
        selection=json.loads((BASE/'refine01'/camera/'selection.json').read_text())
        input_pins.update({str(ROOT/path):identity for path,identity in selection['input_pins'].items()})
        wanted=refinement['rules'][camera]['groups']['event']
        rows=[r for r in selection['images'] if int(r['frame_index_zero_based']) in wanted]
        require([int(r['frame_index_zero_based']) for r in rows]==wanted, 'input-selection')
        require(len(config[camera])==6 and len({f['id'] for f in config[camera]})==6, 'reference-ids')
        arrays=[]
        previous=None
        for row in rows:
            index=int(row['frame_index_zero_based'])
            path=BASE/'refine01'/camera/row['png']
            require(row['png']==f'f{index:06d}.png','frame-name')
            require(fp(path)==row['png_identity'],'png-pin')
            with Image.open(path) as image:
                require(image.mode=='L' and list(image.size)==selection['geometry'],'png-geometry')
                array=np.array(image)
            require(sha(array.tobytes())==row['luma_sha256'],'luma-pin')
            time=Fraction(row['source_time_seconds_exact'])
            require(time==int(row['source_pts'])*Fraction(row['source_time_base']), 'pts')
            require(previous is None or time>previous,'pts-order')
            previous=time
            arrays.append(array)
            input_pins[str(path)]=fp(path)
        groups[camera]=(rows,arrays)
    require(all(fp(Path(path))==value for path,value in input_pins.items()), 'input-integrity')
    return groups,input_pins


def run(out):
    out.mkdir(parents=True,exist_ok=False)
    sources=[Path(__file__),HERE/'PROTOCOL.md',HERE/'features.json',HERE/'test_measure.py']
    pins={str(p):fp(p) for p in sources+[Path(sys.executable)]}
    for path in sources:
        (out/path.name).write_bytes(path.read_bytes())
    save(out/'initial.json',{'pins':pins,'python':sys.version,'executable':sys.executable,
                            'numpy':np.__version__,'pillow':PIL.__version__})
    try:
        config=json.loads((HERE/'features.json').read_text())
        require(config['half_widths']==[9,13] and config['radius']==24,'config-method')
        groups,input_pins=load_inputs(config)
        allrows,models,grids=[],[],{}
        for camera,(stamps,arrays) in groups.items():
            features=config[camera]
            points=np.array([f['xy'] for f in features],float)
            for half in config['half_widths']:
                templates=[]
                for feature in features:
                    xy=feature['xy']
                    require(len(xy)==2 and all(type(c) is int for c in xy),'seed-integer')
                    x,y=xy
                    template=arrays[0][y-half:y+half+1,x-half:x+half+1].copy()
                    require(template.shape==(2*half+1,2*half+1),'seed-template')
                    templates.append(template)
                for stamp,frame in zip(stamps,arrays):
                    index=int(stamp['frame_index_zero_based'])
                    matches=[]
                    for feature,template in zip(features,templates):
                        result,scores=match(frame,template,feature['xy'],config['radius'])
                        key=f'{camera}_{index}_{half}_{feature["id"]}'
                        grids[key]=scores
                        row=dict(result,camera=camera,index=index,pts=stamp['source_pts'],time_base=stamp['source_time_base'],
                                 seconds_exact=stamp['source_time_seconds_exact'],half=half,reference=feature['id'],
                                 baseline_xy=feature['xy'],score_grid=key)
                        matches.append(row)
                        allrows.append(row)
                    for model in ('translation','similarity','affine'):
                        row={'camera':camera,'index':index,'half':half,'model':model,'seconds_exact':stamp['source_time_seconds_exact'],
                             'reference_order':[f['id'] for f in features]}
                        if any(r['status']!='candidate' for r in matches):
                            row.update(status='reference_quality_failure',passes_consistency_screen=False,
                                       failed_references=[r['reference'] for r in matches if r['status']!='candidate'])
                        else:
                            row.update(fit_with_loo(points,[r['candidate_xy'] for r in matches],model))
                        models.append(row)
                    if index in EVALUATION[camera] or stamp is stamps[0]:
                        overlay=Image.new('RGB',(frame.shape[1],frame.shape[0]+34),'white')
                        overlay.paste(Image.fromarray(frame).convert('RGB'),(0,0))
                        draw=ImageDraw.Draw(overlay)
                        for r in matches:
                            if 'candidate_xy' not in r:
                                continue
                            x,y=r['candidate_xy']
                            color='lime' if r['status']=='candidate' else 'red'
                            draw.rectangle((x-4,y-4,x+4,y+4),outline=color,width=1)
                            draw.text((x+5,y),r['reference'],fill=color)
                        draw.text((4,frame.shape[0]+2),f'ANALYTICAL CANDIDATES {camera} frame {index} half {half}',fill='black')
                        draw.text((4,frame.shape[0]+17),'Green=screen passed; red=rejected; not physical tracks',fill='black')
                        overlay.save(out/f'overlay-{camera}-{index}-{half}.png')
        save(out/'matches.json',allrows)
        save(out/'transforms.json',models)
        np.savez_compressed(out/'score-grids.npz',**grids)
        save(out/'input-pins.json',input_pins)
        require(all(fp(Path(p))==v for p,v in input_pins.items()),'post-inputs')
        require(all(fp(Path(p))==v for p,v in pins.items()),'post-procedure')
        save(out/'receipt.json',{'status':'complete_diagnostic_not_camera_calibration','match_rows':len(allrows),
            'model_rows':len(models),'score_grids':len(grids),
            'products':{p.name:fp(p) for p in sorted(out.iterdir()) if p.is_file()}})
        print(json.dumps({'status':'complete','match_rows':len(allrows),'model_rows':len(models)}))
    except Exception as error:
        save(out/'failure.json',{'status':'failed','exception':type(error).__name__})
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    run(parser.parse_args().out)
