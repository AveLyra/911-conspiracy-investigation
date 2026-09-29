"""Retrospective encoded-gray sensitivity; no thermometry or image authentication."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import signal
import sys
import time

import numpy as np
import PIL
from PIL import Image

BASE = Path(__file__).resolve().parent
OLD = BASE.parent / 'peskin-figure-correspondence'
PINS = {
    'match_screen.py': '06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8',
    'check_regions.py': '6990064d77887e245b6843c0580679c5e5c9b5e5a262e1f5e8287fb7411a196b',
    'primary-summary.json': 'c34061bdc218dfd9c818766066ed5aecc636a39f815ef1340ca57dae769327b3',
}
GAMMAS = [.5, .75, 1., 1.25, 1.5, 2., 3.]
LEVELS = [64, 128, 192, 224]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def load_dependencies():
    for name, pin in PINS.items():
        if sha(OLD/name) != pin:
            raise ValueError('prior dependency pin: '+name)
    sys.path.insert(0, str(OLD))
    import match_screen as core
    import check_regions as regions
    if Path(core.__file__).resolve() != OLD/'match_screen.py':
        raise ValueError('wrong core import')
    return core, regions


def mask_for(boxes, factor):
    xs = (np.arange(180*factor)+.5)*720/(180*factor)
    ys = (np.arange(120*factor)+.5)*478/(120*factor)
    mask = np.zeros((120*factor, 180*factor), bool)
    for x0,y0,x1,y1 in boxes:
        mask |= (xs[None,:]>=x0)&(xs[None,:]<x1)&(ys[:,None]>=y0)&(ys[:,None]<y1)
    return mask


def scene_masks(key, factor, core, regions):
    excluded=mask_for([(x0-4,y0-4,x1+4,y1+4) for x0,y0,x1,y1 in regions.EXCLUSIONS[key]],factor)
    inside=mask_for([(3,3,717,475)],factor)&~excluded
    masks={name:mask_for([box],factor)&inside for name,box in regions.REGIONS[key].items()}
    evaluation=np.logical_or.reduce(list(masks.values()))
    masks['F']=mask_for(core.TARGETS[key][2],factor)&inside&~evaluation
    if np.any(masks['F']&evaluation):raise ValueError('photometric fit/evaluation overlap')
    return masks


def midranks(values):
    values = np.asarray(values, float)
    unique, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    ends = np.cumsum(counts)
    return ((ends-counts+1+ends)/2)[inverse]


def support(x, y, tx, ty):
    a,b = x>=tx, y>=ty
    union = int((a|b).sum())
    return {'source_fraction': float(a.mean()), 'target_fraction': float(b.mean()),
            'source_ties': int((x==tx).sum()), 'target_ties': int((y==ty).sum()),
            'intersection': int((a&b).sum()), 'union': union,
            'iou': float((a&b).sum()/union) if union else None}


def information(x, y):
    if len(x)<32 or np.var(x)<=1e-8 or np.var(y)<=1e-8:
        return {'spearman': None, 'quantiles': None, 'reason': 'insufficient or flat gray values'}
    a,b = midranks(x), midranks(y)
    a-=a.mean(); b-=b.mean()
    rho = float(np.dot(a,b)/np.sqrt(np.dot(a,a)*np.dot(b,b)))
    qs = {}
    for q in [.1,.2,.3]:
        tx,ty = float(np.quantile(x,1-q)), float(np.quantile(y,1-q))
        qs[str(q)] = {'source_threshold': tx, 'target_threshold': ty, **support(x,y,tx,ty)}
    return {'spearman': rho, 'quantiles': qs, 'reason': None}


def errors(x, y):
    d=x-y
    return {'bias':float(d.mean()),'mae':float(np.abs(d).mean()),'rmse':float(np.sqrt(np.mean(d*d))),
            'abs_residual_gt_25_5':float((np.abs(d)>25.5).mean()),
            'abs_residual_gt_51':float((np.abs(d)>51).mean()),
            'source_low':float((x<=5).mean()),'source_high':float((x>=250).mean()),
            'target_low':float((y<=5).mean()),'target_high':float((y>=250).mean()),
            'source_zero':float((x==0).mean()),'source_255':float((x==255).mean()),
            'target_zero':float((y==0).mean()),'target_255':float((y==255).mean()),
            'levels':{str(t):support(x,y,t,t) for t in LEVELS}}


def select(mask, valid):
    selected = int(mask.sum()); actual = mask & valid
    n = int(actual.sum()); coverage = n/selected if selected else 0.
    return actual, {'selected':selected,'observed':n,'coverage':coverage,
                    'eligible':n>=32 and coverage>=.85}


def fit_curve(x, y, gamma):
    if len(x)<32 or np.var(x)<=1e-8 or np.var(y)<=1e-8:
        return {'status':'uninformative','reason':'insufficient or flat training values'}
    u=(x/255)**gamma; v=y/255
    a0=u-u.mean(); b0=v-v.mean(); denominator=float(np.dot(a0,a0))
    if denominator/len(x)<=1e-14:
        return {'status':'uninformative','reason':'powered source variance'}
    a=float(np.dot(a0,b0)/denominator); b=float(v.mean()-a*u.mean())
    if not np.isfinite([a,b]).all() or a<=0:
        return {'status':'rejected','reason':'nonpositive or nonfinite slope'}
    return {'status':'fitted','a':a,'b':b,'gamma':gamma}


def extrapolation(x, training):
    lo,hi=float(training.min()),float(training.max())
    qlo,qhi=map(float,np.quantile(training,[.01,.99]))
    return {'training_min':lo,'training_max':hi,'training_p01':qlo,'training_p99':qhi,
            'outside_min_max':float(((x<lo)|(x>hi)).mean()),
            'outside_p01_p99':float(((x<qlo)|(x>qhi)).mean())}


def aligned(im, geometry, factor, kernel):
    w,h=180*factor,120*factor
    work=np.asarray(im.convert('L').resize((w,h),kernel))
    sw,sh=geometry['raster_width']*factor,geometry['raster_height']*factor
    scaled=np.asarray(Image.fromarray(work).resize((sw,sh),kernel))
    canvas=np.zeros((h+50*factor,w+50*factor),float); valid=np.zeros_like(canvas,bool)
    cx,cy=geometry['canvas_x']*factor,geometry['canvas_y']*factor
    canvas[cy:cy+sh,cx:cx+sw]=scaled; valid[cy:cy+sh,cx:cx+sw]=True
    x,y=geometry['left']*factor,geometry['top']*factor
    return canvas[y:y+h,x:x+w], valid[y:y+h,x:x+w]


def calculate(view, target, valid, masks, factor):
    ys,xs=np.indices(view.shape)
    parity=((xs//(8*factor))+(ys//(8*factor)))%2
    baseline={}; ranks={}
    for name,mask in masks.items():
        chosen,meta=select(mask,valid)
        baseline[name]={**meta,'metrics':errors(view[chosen],target[chosen]) if meta['eligible'] else None}
        ranks[name]=information(view[chosen],target[chosen]) if meta['eligible'] else None
    fits=[]
    for fold in [0,1]:
        train,meta=select(masks['F']&(parity==fold),valid)
        hold,hmeta=select(masks['F']&(parity!=fold),valid)
        evaluation={**masks,'F_train':masks['F']&(parity==fold),'F_hold':masks['F']&(parity!=fold)}
        for gamma in GAMMAS:
            fit=fit_curve(view[train],target[train],gamma) if meta['eligible'] else {'status':'uninformative','reason':'training coverage'}
            row={'fold':fold,'gamma':gamma,'training':meta,'fit':fit,'regions':{},
                 'baseline_train':errors(view[train],target[train]) if meta['eligible'] else None,
                 'baseline_hold':errors(view[hold],target[hold]) if hmeta['eligible'] else None}
            if fit['status']=='fitted':
                unclipped=(fit['a']*(view/255)**gamma+fit['b'])*255
                pred=np.clip(unclipped,0,255)
                for name,mask in evaluation.items():
                    chosen,m=select(mask,valid)
                    row['regions'][name]={**m,'metrics':errors(pred[chosen],target[chosen]) if m['eligible'] else None,
                        'clipped_below':float((unclipped[chosen]<0).mean()) if m['eligible'] else None,
                        'clipped_above':float((unclipped[chosen]>255).mean()) if m['eligible'] else None,
                        'extrapolation':extrapolation(view[chosen],view[train]) if m['eligible'] else None}
            fits.append(row)
    return {'baseline':baseline,'rank_diagnostics':ranks,'fits':fits}


def controls():
    checks={}; x=np.linspace(10,230,80); xx=x/255
    for gamma in GAMMAS:
        y=(.8*xx**gamma+.05)*255; f=fit_curve(x,y,gamma)
        checks['gamma_'+str(gamma)]=f['status']=='fitted' and max(abs(f['a']-.8),abs(f['b']-.05))<=1e-10 and np.max(np.abs(f['a']*xx**gamma+f['b']-y/255))<=1e-10
    f=fit_curve(x,x,1.); checks['identity']=abs(f['a']-1)<1e-10 and abs(f['b'])<1e-10
    y=np.rint((.8*xx**1.5+.05)*255); f=fit_curve(x,y,1.5)
    checks['quantization']=errors((f['a']*xx**1.5+f['b'])*255,y)['mae']<=2
    checks['flat_rejected']=fit_curve(np.ones(80),x,1.)['status']=='uninformative'
    checks['negative_slope_rejected']=fit_curve(x,255-x,1.)['status']=='rejected'
    checks['midranks']=np.array_equal(midranks([9,2,2,7]),[4,1.5,1.5,3])
    checks['empty_union']=support(np.zeros(32),np.zeros(32),64,64)['iou'] is None
    checks['rank_invariant']=abs(information(x,xx**3)['spearman']-1)<1e-10
    checks['flat_rank_null']=information(np.ones(80),x)['spearman'] is None
    q1=information(x,x)['quantiles'];q2=information(x,xx**3)['quantiles']
    checks['quantile_invariant']=all(q1[q]['iou']==q2[q]['iou']==1 for q in q1)
    clipped=np.clip(x*2,0,255)
    checks['clipping_ties']=len(np.unique(clipped))<len(np.unique(x)) and information(x,clipped)['spearman']<1
    sample=np.array([0.,10.,20.,30.]); training=np.array([10.,20.])
    checks['extrapolation']=extrapolation(sample,training)['outside_min_max']==.5
    mask=np.ones((8,8),bool);valid=mask.copy();valid[:2]=False
    checks['coverage_rejected']=not select(mask,valid)[1]['eligible']
    checks['mask_centers']=int(mask_for([(0,0,4,478)],1).sum())==120
    checks['mask_scaling']=int(mask_for([(0,0,4,478)],2).sum())==480
    scene=np.arange(120*180,dtype=np.uint8).reshape(120,180)
    geometry={'raster_width':180,'raster_height':120,'canvas_x':25,'canvas_y':25,'left':28,'top':23}
    moved,good=aligned(Image.fromarray(scene),geometry,1,Image.Resampling.BILINEAR)
    expected=np.zeros((120,180),bool);expected[2:,:177]=True
    checks['signed_shift_padding']=np.array_equal(good,expected) and np.array_equal(moved[2:,:177],scene[:118,3:])
    truth=np.zeros(80);truth[10:20]=200;shift=np.zeros(80);shift[30:40]=200
    checks['displaced_patch_detected']=support(truth,shift,128,128)['iou']==0 and errors(truth,shift)['mae']==50
    foreground=np.linspace(10,230,80);f=fit_curve(foreground,foreground,1.)
    changed=truth.copy();changed[10:20]=100
    pred=(f['a']*(changed/255)+f['b'])*255
    checks['local_change_not_erased']=errors(pred,truth)['mae']>12 and abs(f['a']-1)<1e-10
    core,regions=load_dependencies()
    for key in ['148','149']:
        for factor in [1,2]:
            masks=scene_masks(key,factor,core,regions)
            evaluation=np.logical_or.reduce([m for name,m in masks.items() if name!='F'])
            checks[f'disjoint_{key}_{factor}']=not np.any(masks['F']&evaluation) and masks['F'].sum()>=64
    return {'checks':{k:bool(v) for k,v in checks.items()},'passed':all(checks.values()),'count':len(checks)}


def run(folder):
    core,regions=load_dependencies(); summary=json.loads((OLD/'primary-summary.json').read_text())
    results=[]; arrays={}; inputs={}; masks_pins={}; pairs=0
    for key in ['148','149']:
        rows={r['source_pts']:r for group in summary['results'][key].values() for r in group['top_four']}
        asset,pin,sboxes,_=core.TARGETS[key]
        target_path=core.MAIN/'fire-annotation/assets/run-01/images'/f'{asset}.jpg'
        if sha(target_path)!=pin:raise ValueError('target identity')
        inputs[str(target_path)]={'sha256':pin,'bytes':target_path.stat().st_size}
        with Image.open(target_path) as im: target_image=im.copy()
        for pts,row in sorted(rows.items()):
            pairs+=1;native=Path(row['native_png']); receipt_path=OLD/row['run']/'receipt.json'
            if native.parent!=receipt_path.parent or native.name!=f"native-{row['frame_index']:04d}.png":raise ValueError('native membership')
            if sha(receipt_path)!=summary['chunk_receipt_pins'][row['run']]:raise ValueError('receipt identity')
            receipt=json.loads(receipt_path.read_text()); pin=receipt['outputs'][native.name]
            if sha(native)!=pin['sha256'] or native.stat().st_size!=pin['bytes']:raise ValueError('native identity')
            inputs[str(native)]=pin
            with Image.open(native) as im: source_image=im.copy()
            geometry=row['geometry_candidates'][0]
            for factor in [1,2]:
                for label in ['BILINEAR','BOX']:
                    kernel=getattr(Image.Resampling,label);bid=f'{180*factor}_{label}'
                    target=np.asarray(target_image.convert('L').resize((180*factor,120*factor),kernel),float)
                    view,valid=aligned(source_image,geometry,factor,kernel)
                    if factor==1 and label=='BILINEAR':
                        canvas,ok,_=core.canvas_for(core.working(source_image),geometry['requested_scale'])
                        x,y=geometry['left'],geometry['top']
                        if not np.array_equal(view,canvas[y:y+120,x:x+180]) or not np.array_equal(valid,ok[y:y+120,x:x+180].astype(bool)):
                            raise ValueError('baseline geometry mismatch')
                    masks=scene_masks(key,factor,core,regions)
                    tag=f'T{key}_{pts}_{bid}';arrays[tag+'_source']=view;arrays[tag+'_target']=target;arrays[tag+'_valid']=valid
                    for name,mask in masks.items():
                        mtag=f'T{key}_{bid}_{name}';arrays[mtag]=mask
                        masks_pins[mtag]=hashlib.sha256(mask.tobytes()).hexdigest()
                    results.append({'target':key,'source_pts':pts,'frame_index':row['frame_index'],
                        'branch':bid,'factor':factor,'geometry':geometry,'array_prefix':tag,
                        **calculate(view,target,valid,masks,factor)})
    if pairs!=12 or len(results)!=48:raise ValueError('coverage')
    for path,pin in inputs.items():
        if sha(path)!=pin['sha256']:raise ValueError('input changed')
    np.savez_compressed(folder/'arrays.npz',**arrays)
    save(folder/'results.json',{'results':results,'inputs':inputs,'mask_hashes':masks_pins,
         'pair_count':pairs,'branch_count':len(results),'fit_attempts':sum(len(r['fits']) for r in results)})


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--controls',action='store_true');a=p.parse_args()
    if a.run not in ['controls01','run01','run02']:raise ValueError('undeclared run')
    if a.controls!=(a.run=='controls01'):raise ValueError('run mode mismatch')
    folder=BASE/a.run
    if folder.exists():raise FileExistsError('create-only output')
    before=sum(f.stat().st_size for f in BASE.rglob('*') if f.is_file())
    if before>80*1024**2:raise ValueError('baseline disk bound')
    folder.mkdir();started=time.monotonic()
    def timeout(signum,frame):raise TimeoutError('300-second cap')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(300)
    try:
        if a.controls:
            result=controls();save(folder/'controls.json',result)
            if not result['passed']:raise ValueError('failed synthetic controls')
        else:
            prior=json.loads((BASE/'controls01'/'receipt.json').read_text())
            if prior['status']!='completed' or prior['script_sha256']!=sha(__file__):raise ValueError('controls version')
            if prior['protocol_sha256']!=sha(BASE/'PROTOCOL.md'):raise ValueError('controls protocol version')
            if sha(BASE/'controls01'/'controls.json')!=prior['outputs']['controls.json']['sha256']:raise ValueError('control output pin')
            run(folder)
        size=sum(f.stat().st_size for f in BASE.rglob('*') if f.is_file())
        if size>100*1024**2:raise ValueError('aggregate disk bound')
        outputs={f.name:{'sha256':sha(f),'bytes':f.stat().st_size} for f in folder.iterdir()}
        save(folder/'receipt.json',{'status':'completed','script_sha256':sha(__file__),'protocol_sha256':sha(BASE/'PROTOCOL.md'),
            'prior_pins':PINS,'python':platform.python_version(),'numpy':np.__version__,'pillow':PIL.__version__,
            'argv':sys.argv,'elapsed_seconds':time.monotonic()-started,'unit_bytes_before_receipt':size,'outputs':outputs})
        print(json.dumps({'status':'completed','run':a.run,'outputs':outputs}))
    except BaseException as error:
        save(folder/'failure.json',{'status':'failed','error_type':type(error).__name__,'message':str(error),'script_sha256':sha(__file__)})
        raise
    finally:signal.alarm(0)


if __name__=='__main__':main()
