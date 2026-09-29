"""Compare frozen visual annotations and conditional image maps, not physics."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REFERENCE = HERE.parent/'camera2-reference-repair/run01'
FRAMES = (6593,6654,6751,6841,6886,6916,6931,6946,6961,6976,6991,7006,7021,7036,7051,7081,7104)
TARGETS = ('C2-T1','C2-T2')
MODELS = ('translation','similarity','affine')


def require(value,label):
    if not value:
        raise ValueError(label)


def fp(path):
    with path.open('rb') as stream:
        return {'bytes':path.stat().st_size,'sha256':hashlib.file_digest(stream,'sha256').hexdigest()}


def read(path):
    return json.loads(path.read_text())


def save(path,value):
    with path.open('x') as stream:
        stream.write(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def array(value,shape):
    result = np.asarray(value,dtype=float)
    require(result.shape==shape and np.isfinite(result).all(),'finite array shape')
    return result


def box(xy,halfwidth):
    center,width = array(xy,(2,)),array(halfwidth,(2,))
    require((width>=0).all(),'nonnegative envelope')
    return np.stack((center-width,center+width),axis=1)


def checked_box(value):
    value = array(value,(2,2))
    require((value[:,0]<=value[:,1]).all(),'ordered envelope')
    return value


def subtract_boxes(current,baseline):
    current,baseline = checked_box(current),checked_box(baseline)
    return np.stack((current[:,0]-baseline[:,1],current[:,1]-baseline[:,0]),axis=1)


def inverse_parameters(matrix,offset):
    matrix,offset = array(matrix,(2,2)),array(offset,(2,))
    determinant = float(np.linalg.det(matrix))
    condition = float(np.linalg.cond(matrix))
    require(determinant>0 and np.isfinite(condition) and condition<=10000,'admissible inverse matrix')
    return np.linalg.inv(matrix),offset,condition


def inverse_box(bbox,matrix,offset):
    bbox = checked_box(bbox)
    inverse,offset,_ = inverse_parameters(matrix,offset)
    corners = np.array(list(itertools.product(*bbox)))
    mapped = (corners-offset)@inverse.T
    return np.stack((mapped.min(axis=0),mapped.max(axis=0)),axis=1)


def eligible(row):
    return row['localization']=='localized' and row['correspondence']=='appearance_consistent'


def displacement(row,baseline):
    if not eligible(row) or not eligible(baseline):
        return None
    if row['frame']==baseline['frame']:
        require(row==baseline,'same baseline observation')
        return {'center_xy':[0.,0.],'enclosure_xy':[[0.,0.],[0.,0.]],'self_baseline':True}
    return {'center_xy':(np.array(row['xy'])-np.array(baseline['xy'])).tolist(),
            'enclosure_xy':subtract_boxes(box(row['xy'],row['halfwidth_xy']),box(baseline['xy'],baseline['halfwidth_xy'])).tolist(),
            'self_baseline':False}


def compare_rows(one,two):
    result = {'both_localized':one['localization']==two['localization']=='localized',
              'localization_agrees':one['localization']==two['localization'],
              'correspondence_agrees':one['correspondence']==two['correspondence']}
    if result['both_localized']:
        a,b = box(one['xy'],one['halfwidth_xy']),box(two['xy'],two['halfwidth_xy'])
        result.update(separate_minus_root_xy=(np.array(two['xy'])-np.array(one['xy'])).tolist(),
                      overlap_per_axis=(np.maximum(a[:,0],b[:,0])<=np.minimum(a[:,1],b[:,1])).tolist(),
                      root_center_in_separate=bool(((b[:,0]<=one['xy'])&(one['xy']<=b[:,1])).all()),
                      separate_center_in_root=bool(((a[:,0]<=two['xy'])&(two['xy']<=a[:,1])).all()))
    return result


def hull(points):
    points = sorted(set(tuple(p) for p in points))
    def cross(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def chain(sequence):
        result=[]
        for p in sequence:
            while len(result)>1 and cross(result[-2],result[-1],p)<=0:
                result.pop()
            result.append(p)
        return result
    result=chain(points)[:-1]+chain(points[::-1])[:-1]
    require(len(result)>=3,'reference hull not degenerate')
    return result


def outside_hull(point,vertices):
    return any((b[0]-a[0])*(point[1]-a[1])-(b[1]-a[1])*(point[0]-a[0]) < -1e-8
               for a,b in zip(vertices,vertices[1:]+vertices[:1]))


def first_downward(records):
    for index,row in enumerate(records):
        delta=row['displacement']
        if delta is not None and delta['enclosure_xy'][1][0]>0:
            previous = None if index==0 else records[index-1]
            return {'first_selected_frame':row['frame'],'seconds_exact':row['seconds_exact'],
                    'downward_enclosure':delta['enclosure_xy'][1],
                    'preceding_scheduled_sample':previous,
                    'meaning':'First selected appearance-displacement interval wholly downward; not first physical motion or an onset bracket.'}
    return {'first_selected_frame':None,'meaning':'No selected eligible downward interval found; not evidence of no motion.'}


def validate_annotations(data,label,selection,presentation):
    expected_pins = {'protocol_sha256':fp(HERE/'PROTOCOL.md')['sha256'],
        'selection_sha256':fp(HERE/'selection.json')['sha256'],
        'presentation_receipt_sha256':fp(HERE/'present01/receipt.json')['sha256'],
        'source_manifest_sha256':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e'}
    require(all(data.get(k)==v for k,v in expected_pins.items()),'annotation dependency pins')
    require(data['schema_version']==1 and data['annotator']==label and data['review_kind']=='computational_AI_not_human','annotator identity')
    require(data['independence']=={'other_new_annotations_seen':False,'shared_proposal_known':True,'old_event_familiarity':True},'declared independence limits')
    require(data['viewing']['full_native_frames']==list(FRAMES) and data['viewing']['coordinate_panels']==list(FRAMES),'declared visual coverage')
    rows=data['rows']
    require([(r['frame'],r['target']) for r in rows]==list(itertools.product(FRAMES,TARGETS)),'exact annotation row set/order')
    for r in rows:
        require(r['localization'] in ('localized','ambiguous','unavailable'),'localization status')
        require(r['correspondence'] in ('appearance_consistent','uncertain','changed','not_assessable'),'correspondence status')
        require(isinstance(r['note'],str) and r['note'].strip(),'observation note')
        if r['localization']=='localized':
            require(all(isinstance(r[k],list) and len(r[k])==2 and all(type(v) is int for v in r[k]) for k in ('xy','halfwidth_xy')),'integer annotation')
            require(0<=r['xy'][0]<640 and 0<=r['xy'][1]<480 and all(v>0 for v in r['halfwidth_xy']),'native center/envelope')
        else:
            require(r['xy'] is None and r['halfwidth_xy'] is None,'unresolved coordinate absent')
    return rows


def mapped_record(row,baseline,fit,basefit,vertices):
    result={'stored_fit_status':fit['status'],'stored_fit_screen':fit['passes_consistency_screen'],
            'baseline_fit_status':basefit['status'],'baseline_fit_screen':basefit['passes_consistency_screen']}
    if not eligible(row) or not eligible(baseline):
        return dict(result,status='annotation_not_eligible')
    if not fit['passes_consistency_screen'] or not basefit['passes_consistency_screen']:
        return dict(result,status='stored_map_not_admitted',known_cutoff_rounding_case=fit['index']==7021 and fit['half']==9 and fit['model']=='affine')
    try:
        inverse,offset,condition=inverse_parameters(fit['matrix'],fit['offset'])
        binverse,boffset,bcondition=inverse_parameters(basefit['matrix'],basefit['offset'])
    except ValueError as error:
        return dict(result,status='inverse_not_admitted',reason=str(error))
    center=inverse@(np.array(row['xy'])-offset)
    basecenter=binverse@(np.array(baseline['xy'])-boffset)
    current_box=inverse_box(box(row['xy'],row['halfwidth_xy']),fit['matrix'],fit['offset'])
    base_box=inverse_box(box(baseline['xy'],baseline['halfwidth_xy']),basefit['matrix'],basefit['offset'])
    delta=displacement(row,baseline)
    enclosure=np.zeros((2,2)) if row['frame']==baseline['frame'] else subtract_boxes(current_box,base_box)
    change=center-basecenter
    return dict(result,status='computed_conditional_image_map',inverse_condition=condition,baseline_inverse_condition=bcondition,
                mapped_center_xy=center.tolist(),mapped_box_xy=current_box.tolist(),baseline_mapped_center_xy=basecenter.tolist(),
                baseline_mapped_box_xy=base_box.tolist(),mapped_displacement_xy=change.tolist(),mapped_displacement_enclosure_xy=enclosure.tolist(),
                mapped_minus_raw_displacement_xy=(change-np.array(delta['center_xy'])).tolist(),
                center_outside_reference_hull=outside_hull(center,vertices),baseline_center_outside_reference_hull=outside_hull(basecenter,vertices))


def controls():
    checks=[]
    def check(value,name):
        require(value,name);checks.append(name)
    check(np.array_equal(box([10,20],[2,3]),[[8,12],[17,23]]),'asymmetric center-location box')
    check(np.array_equal(subtract_boxes([[5,9],[10,20]],[[1,3],[4,8]]),[[2,8],[2,16]]),'conservative interval subtraction')
    check(np.allclose(inverse_box([[8,12],[17,23]],[[1,1],[0,1]],[3,-2]),[[-20,-10],[19,25]]),'inverse shear all corners')
    for value,half in (([float('nan'),0],[1,1]),([1,2],[-1,1])):
        try: box(value,half)
        except ValueError: checks.append('invalid box rejected')
        else: raise AssertionError('invalid box accepted')
    for a in ([[1,2],[2,4]],[[float('inf'),0],[0,1]],[[1,0],[0,-1]]):
        try: inverse_box([[0,1],[0,1]],a,[0,0])
        except ValueError: checks.append('invalid inverse rejected')
        else: raise AssertionError('invalid inverse accepted')
    baseline={'frame':1,'localization':'localized','correspondence':'appearance_consistent','xy':[10,10],'halfwidth_xy':[3,4]}
    changed=dict(baseline,frame=2,correspondence='changed')
    check(displacement(changed,baseline) is None,'visible changed definition excluded')
    check(displacement(dict(baseline,frame=2,localization='unavailable',xy=None,halfwidth_xy=None),baseline) is None,'unavailable coordinate not invented')
    check(displacement(baseline,baseline)['enclosure_xy']==[[0.,0.],[0.,0.]],'same-observation baseline exact zero')
    sample=[{'frame':1,'seconds_exact':'0','displacement':displacement(baseline,baseline)},
            {'frame':2,'seconds_exact':'1','displacement':None},
            {'frame':3,'seconds_exact':'5','displacement':{'enclosure_xy':[[0,0],[-5,-1]]}},
            {'frame':4,'seconds_exact':'6','displacement':{'enclosure_xy':[[0,0],[1,5]]}}]
    first=first_downward(sample)
    check(first['first_selected_frame']==4 and first['preceding_scheduled_sample']['frame']==3,'downward sign and preceding sample not onset')
    shared=compare_rows(baseline,baseline)
    truth=[100,100]
    check(all(shared['overlap_per_axis']) and baseline['xy']!=truth,'shared wrong coordinates can agree without truth')
    vertices=hull([[0,0],[2,0],[2,2],[0,2],[1,1]])
    check(not outside_hull([1,1],vertices) and outside_hull([1,-1],vertices),'hull extrapolation classification')
    return {'passed':len(checks),'checks':checks,'shared_error_truth_xy':truth,'scope':'Synthetic arithmetic and limits, not historical validation.'}


def run(out,stage,control_path=None):
    out.mkdir(parents=True,exist_ok=False)
    procedure=[Path(__file__),HERE/'PROTOCOL.md',HERE/'CALCULATION-CONTRACT.md']
    pins={str(p):fp(p) for p in procedure+[Path(sys.executable)]}
    try:
        for p in procedure:(out/p.name).write_bytes(p.read_bytes())
        save(out/'initial.json',{'stage':stage,'pins':pins.copy(),'python':sys.version,'numpy':np.__version__})
        if stage=='controls':
            result=controls()
        else:
            require(control_path is not None,'explicit controls')
            control=read(control_path/'receipt.json')
            require(control['stage']=='controls' and control['status']=='complete' and control['pins']==pins,'passing current-code controls')
            require(all(fp(control_path/n)==v for n,v in control['products'].items()),'control product integrity')
            pins[str(control_path/'receipt.json')]=fp(control_path/'receipt.json')
            selection=read(HERE/'selection.json')
            require(selection['accepted_target_ids']==list(TARGETS) and selection['protocol_sha256']==fp(HERE/'PROTOCOL.md')['sha256'],'frozen selection')
            require(selection['proposal_sha256']==fp(HERE/'targets-proposal.json')['sha256'],'frozen proposal')
            presentation=read(HERE/'present01/receipt.json')
            require(presentation['stage']=='prepare' and presentation['status']=='complete','complete presentation')
            require(all(fp(HERE/'present01'/n)==v for n,v in presentation['products'].items()),'presentation product integrity')
            require(all(fp(Path(p))==v for p,v in presentation['pins'].items()),'presentation source integrity')
            detail=read(HERE/'present01/detail.json')
            stamps={int(r['frame_index_zero_based']):r for r in detail['rows']}
            require(tuple(stamps)==FRAMES,'presentation timing coverage')
            reference_receipt=read(REFERENCE/'receipt.json')
            require(fp(REFERENCE/'receipt.json')['sha256']=='d2b8ae21b6fe3b0190538142b1db37be9f5a31b80d581d5ac6c39e90a952f320','frozen reference run')
            require(all(fp(REFERENCE/n)==v for n,v in reference_receipt['products'].items()),'reference product integrity')
            fitrows=read(REFERENCE/'transforms.json');fits={(r['index'],r['half'],r['model']):r for r in fitrows}
            require(len(fits)==len(fitrows)==426,'reference fit keys')
            vertices=hull([r['xy'] for r in read(REFERENCE/'preflight-selection.json')['features']])
            annotations=[]
            for label,name in (('root','root-annotations.json'),('separate','annotator-annotations.json')):
                data=read(HERE/name)
                annotations.append(validate_annotations(data,label,selection,presentation))
            consumed=['selection.json','targets-proposal.json','root-annotations.json','annotator-annotations.json','present01/receipt.json','present01/detail.json']
            pins.update({str(HERE/n):fp(HERE/n) for n in consumed})
            pins.update({str(REFERENCE/n):fp(REFERENCE/n) for n in ('receipt.json','transforms.json','preflight-selection.json')})
            raw,comparisons,pairs,mapped,firsts=[],[],[],[],[]
            for label,rows in zip(('root','separate'),annotations):
                lookup={(r['frame'],r['target']):r for r in rows}
                currentraw=[]
                for row in rows:
                    baseline=lookup[(6593,row['target'])]
                    item={'annotator':label,'frame':row['frame'],'target':row['target'],
                          'seconds_exact':stamps[row['frame']]['source_time_seconds_exact'],'observation':row,
                          'displacement':displacement(row,baseline)}
                    raw.append(item);currentraw.append(item)
                    for half in (9,13):
                        for model in MODELS:
                            result=mapped_record(row,baseline,fits[(row['frame'],half,model)],fits[(6593,half,model)],vertices)
                            mapped.append(dict(result,annotator=label,frame=row['frame'],target=row['target'],half=half,model=model,seconds_exact=item['seconds_exact']))
                for target in TARGETS:
                    firsts.append(dict(first_downward([r for r in currentraw if r['target']==target]),annotator=label,target=target))
                for frame in FRAMES:
                    a,b=[r['displacement'] for r in currentraw if r['frame']==frame]
                    item={'annotator':label,'frame':frame,'seconds_exact':stamps[frame]['source_time_seconds_exact'],'status':'not_both_eligible'}
                    if a is not None and b is not None:
                        item.update(status='computed_appearance_difference',T2_minus_T1_vertical_displacement=b['center_xy'][1]-a['center_xy'][1],
                                    enclosure=[b['enclosure_xy'][1][0]-a['enclosure_xy'][1][1],b['enclosure_xy'][1][1]-a['enclosure_xy'][1][0]])
                    pairs.append(item)
            for one,two in zip(*annotations):
                comparisons.append(dict(compare_rows(one,two),frame=one['frame'],target=one['target'],root_observation=one,separate_observation=two))
            require((len(raw),len(comparisons),len(pairs),len(mapped),len(firsts))==(68,34,34,408,4),'complete result coverage')
            result={'scope':'Retrospective computational appearance annotations and conditional image-coordinate sensitivity; no physical trajectory or cause.',
                    'raw':raw,'comparisons':comparisons,'between_targets':pairs,'mapped':mapped,'first_selected_downward':firsts,
                    'reference_hull':vertices,'map_status_counts':dict(Counter(r['status'] for r in mapped))}
        save(out/'result.json',result)
        require(all(fp(Path(p))==v for p,v in pins.items()),'consumed inputs changed')
        save(out/'receipt.json',{'stage':stage,'status':'complete','pins':pins,'products':{p.name:fp(p) for p in sorted(out.iterdir()) if p.is_file()}})
        print(json.dumps({'status':'complete','stage':stage}))
    except Exception as error:
        save(out/'failure.json',{'stage':stage,'type':type(error).__name__,'message':str(error)})
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('controls','analyze'))
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--controls',type=Path)
    args=parser.parse_args();run(args.out,args.stage,args.controls)
