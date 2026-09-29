#!/usr/bin/env python3
"""Independent determinant-inverse / rational-clock table correspondence check.

Method saved before converting historical points or reading another comparison.
Only the fixed source/data correspondence tests in TABLE-ADDENDUM.md are run.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
PINS = {
    'project': (HERE/'project01.json', '4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8'),
    'table': (HERE.parent/'multipoint-table-reproduction/transcription-root/table47.json', 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc'),
    'probe': (HERE/'probe01/probe.json', '778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de'),
    'selection': (HERE/'probe01/selection.json', 'afd9abc4bd64a0422a749715a8dbb727f7e23447f1c6bf45e9c93d32030f7f6b'),
    'addendum': (HERE/'TABLE-ADDENDUM.md', 'f5597785cac2a11a7680bd9f051df8455a5f190387544ac6ef675ee907a108e1'),
    'source_review': (HERE/'source-semantics-review.md', 'f2a62ac0826e64b60f59aede09c00ff703c1c1a48c549d4f7d42be41ff50b2e1'),
}
PAIRS = [('X','ref_x'),('Y','ref_y'),('Y','ne_y'),('Y','ec_y'),('Y','wc_y'),('Y','nw_y')]
ABS_BOUND = F(5,1000)
CHANGE_BOUND = F(1,100)
ARITH_TOL = F(1,10**9)


def pin(path):
    raw = path.read_bytes()
    return {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()}


def inverse_point(x, y, config):
    """Generic 2x2 inverse of the literal source's forward affine matrix."""
    angle = float(config['angle']) * math.pi / 180
    sx,sy = float(config['xscale']),float(config['yscale'])
    c,s = math.cos(angle),math.sin(angle)
    a,b,c2,d = sx*c,-sx*s,-sy*s,-sy*c
    determinant = a*d-b*c2
    if not math.isfinite(determinant) or determinant == 0:
        raise ValueError('singular_or_nonfinite_transform')
    u,v = float(x)-float(config['xorigin']),float(y)-float(config['yorigin'])
    result = ((d*u-b*v)/determinant,(-c2*u+a*v)/determinant)
    if not all(math.isfinite(q) for q in result):
        raise ValueError('nonfinite_world_point')
    return result


def nearest_grid(t):
    units = abs(t) / F(1,5)
    whole = (2*units.numerator+units.denominator)//(2*units.denominator)
    return (-1 if t<0 else 1)*F(whole,5)


def nominal_clock(frame, config):
    return (F(config['starttime'])+(frame-int(config['startframe']))*F(config['delta_t']))/1000


def stretched_clock(frame, config, engine_ms, a, b):
    stretch = F(config['delta_t'])*(b-a)/(engine_ms[b]-engine_ms[a])
    return (F(config['starttime'])+stretch*(engine_ms[frame]-engine_ms[a]))/1000


def diagnostic(residual, bound):
    return {'residual':float(residual), 'residual_exact_from_binary_world':str(residual),
            'inside_print_enclosure':abs(residual)<=bound,
            'compatible_with_arithmetic_tolerance':abs(residual)<=bound+ARITH_TOL}


def finite_field(field):
    values = field['occurrences']
    assert len(values)==1
    item = values[0]
    numeric = float(item['saved_text'])
    assert math.isfinite(numeric) and numeric==item['value']
    return {'saved_text':item['saved_text'], 'value':numeric, 'xml_path':item['xml_path']}


def derive_point(frame, x, y, key, config, engine_ms, a, b, locator):
    X,Y = inverse_point(x['saved_text'],y['saved_text'],config)
    time = nominal_clock(frame,config)
    grid = nearest_grid(time)
    stepq = F(frame-int(config['startframe']),int(config['stepsize']))
    included = stepq.denominator==1 and 0<=stepq<int(config['stepcount'])
    return {'frame':frame,'step_exact':str(stepq),'step':int(stepq) if included else None,
            'selected_clip_step':included,'saved_keyFrame_member':key,
            'provenance_flag':'saved_key_manual_or_auto_marked' if key else 'saved_nonkey_history_unresolved',
            'source_row_locator':locator,'source_x':x,'source_y':y,'X':X,'Y':Y,
            'U_seconds_exact':str(time),'U_seconds':float(time),
            'nominal_grid_seconds_exact':str(grid),'nominal_grid_seconds':float(grid),
            'time_grid_residual_seconds_exact':str(time-grid),'time_grid_residual_seconds':float(time-grid),
            'printed_time_compatible_0_01s':abs(time-grid)<=F(5,1000),
            'current_pts_stretched_seconds_exact':str(stretched_clock(frame,config,engine_ms,a,b)),
            'U_minus_current_stretched_seconds_exact':str(time-stretched_clock(frame,config,engine_ms,a,b))}


def compare_pair(track_id, rows, paper, axis, column):
    bygrid = {}
    for row in rows:
        grid = F(row['nominal_grid_seconds_exact'])
        assert grid not in bygrid, 'duplicate_grid_mapping'
        bygrid[grid] = row
    shared = [(pr,bygrid[F(pr['time_s'])]) for pr in paper
              if F(pr['time_s']) in bygrid and pr[column] is not None]
    baseline = None
    if shared:
        pr,src = shared[0]
        baseline = {'paper_row':pr['row'],'page':pr['page'],'time_s':pr['time_s'],
                    'frame':src['frame'],'source_row_locator':src['source_row_locator'],
                    'source_world':src[axis],'printed_text':pr[column],
                    'original_offset':float(F.from_float(src[axis])-F(pr[column])),
                    'original_offset_exact':str(F.from_float(src[axis])-F(pr[column]))}
    compared = []
    for pr in paper:
        t = F(pr['time_s']); src = bygrid.get(t); printed = pr[column]
        status = ('compared' if src is not None and printed is not None else
                  'missing_source' if src is None and printed is not None else
                  'missing_published_value' if src is not None else 'missing_both')
        item = {'paper_locator':{'page':pr['page'],'row':pr['row'],'column':column},
                'printed_time_text':pr['time_s'],'printed_value_text':printed,'status':status,
                'source_frame':src['frame'] if src else None,
                'source_row_locator':src['source_row_locator'] if src else None,
                'saved_keyFrame_member':src['saved_keyFrame_member'] if src else None,
                'provenance_flag':src['provenance_flag'] if src else None,
                'source_world':src[axis] if src else None,
                'time_residual_seconds_exact':str(F(src['U_seconds_exact'])-t) if src else None,
                'printed_time_compatible_0_01s':abs(F(src['U_seconds_exact'])-t)<=F(5,1000) if src else None,
                'absolute':None,'position_change':None}
        if status=='compared':
            residual = F.from_float(src[axis])-F(printed)
            item['absolute'] = diagnostic(residual,ABS_BOUND)
            item['position_change'] = diagnostic(residual-F(baseline['original_offset_exact']),CHANGE_BOUND)
            item['position_change']['baseline_paper_row'] = baseline['paper_row']
            item['position_change']['source_change'] = float(F.from_float(src[axis])-F.from_float(baseline['source_world']))
            item['position_change']['printed_change_exact'] = str(F(printed)-F(baseline['printed_text']))
        compared.append(item)
    published_grid = {F(pr['time_s']) for pr in paper}
    outside = [{'status':'outside_publication_grid','frame':r['frame'],
                'nominal_grid_seconds_exact':r['nominal_grid_seconds_exact'],
                'source_world':r[axis],'source_row_locator':r['source_row_locator'],
                'saved_keyFrame_member':r['saved_keyFrame_member'],'provenance_flag':r['provenance_flag'],
                'U_seconds_exact':r['U_seconds_exact'],'time_grid_residual_seconds_exact':r['time_grid_residual_seconds_exact']}
               for r in rows if F(r['nominal_grid_seconds_exact']) not in published_grid]
    summary = {'status_counts':dict(sorted(Counter(r['status'] for r in compared).items())),
               'publication_rows':len(paper),'source_rows':len(rows),'outside_publication_grid':len(outside),
               'shared_rows':len(shared),'printed_finite_rows':sum(pr[column] is not None for pr in paper)}
    for key in ('absolute','position_change'):
        vals = [r[key] for r in compared if r[key] is not None]
        raw = [v['residual'] for v in vals]
        strict = sum(v['inside_print_enclosure'] for v in vals)
        compatible = sum(v['compatible_with_arithmetic_tolerance'] for v in vals)
        summary[key] = {'strict_compatible_count':strict,'compatible_count':compatible,
                        'all_shared_compatible':bool(vals) and compatible==len(vals),
                        'all_printed_finite_rows_available_and_compatible':bool(vals) and len(vals)==summary['printed_finite_rows'] and compatible==len(vals),
                        'max_abs_residual':max(map(abs,raw)) if raw else None,
                        'signed_residual_min':min(raw) if raw else None,
                        'signed_residual_max':max(raw) if raw else None}
    return {'track_id':track_id,'axis':axis,'paper_column':column,'baseline':baseline,
            'summary':summary,'published_rows':compared,'unjoined_source_rows':outside}


def synthetic_controls():
    cfg={'angle':'90','xscale':'2','yscale':'3','xorigin':'11','yorigin':'13',
         'startframe':'0','stepsize':'2','stepcount':'3','starttime':'-20','delta_t':'25'}
    X,Y=inverse_point(7,10,cfg); assert abs(X-1)<1e-12 and abs(Y-2)<1e-12
    zero=dict(cfg,angle='0'); assert inverse_point(13,16,zero)==(1,-1)
    assert all(nearest_grid(F(a))==F(b) for a,b in [('-0.1','-0.2'),('0.1','0.2'),('-0.3','-0.4'),('0.3','0.4'),('-0.099','0'),('0.099','0')])
    for bound in (ABS_BOUND,CHANGE_BOUND):
        assert diagnostic(bound,bound)['inside_print_enclosure']
        assert diagnostic(bound+ARITH_TOL,bound)['compatible_with_arithmetic_tolerance']
        assert not diagnostic(bound+2*ARITH_TOL,bound)['compatible_with_arithmetic_tolerance']
    irregular={0:F(100),1:F(110),2:F(130),3:F(160),4:F(200),5:F(300)}
    assert nominal_clock(2,cfg)==F(3,100)
    assert stretched_clock(2,cfg,irregular,0,4)==F(1,100)
    assert stretched_clock(2,cfg,irregular,0,5)!=stretched_clock(2,cfg,irregular,0,4)
    uniform={i:F(100+10*i) for i in range(6)}
    assert all(stretched_clock(i,cfg,uniform,0,4)==nominal_clock(i,cfg) for i in (0,2,4))
    field={'saved_text':'7','value':7.,'xml_path':'synthetic/x'}
    row=derive_point(2,field,dict(field,saved_text='10',value=10.,xml_path='synthetic/y'),False,cfg,irregular,0,4,'synthetic/row')
    assert row['step']==1 and row['saved_keyFrame_member'] is False and row['provenance_flag']=='saved_nonkey_history_unresolved'
    offgrid=derive_point(1,field,field,True,cfg,irregular,0,4,'synthetic/offgrid')
    assert offgrid['selected_clip_step'] is False and offgrid['step'] is None
    def src(t,x,key=True):
        return {'frame':int(F(t)*10),'nominal_grid_seconds_exact':t,'U_seconds_exact':t,'X':float(x),'Y':float(x),
                'source_row_locator':'synthetic','saved_keyFrame_member':key,'provenance_flag':'synthetic',
                'time_grid_residual_seconds_exact':'0'}
    paper=[{'page':0,'row':i+1,'time_s':t,'ref_x':v} for i,(t,v) in enumerate([('0','5'),('0.2',None),('0.4','7'),('0.6','9')])]
    test=compare_pair('synthetic',[src('0',15),src('0.2',17,False),src('0.8',99)],paper,'X','ref_x')
    assert test['summary']['status_counts']=={'compared':1,'missing_published_value':1,'missing_source':2}
    assert test['summary']['outside_publication_grid']==1 and test['baseline']['original_offset']==10
    assert test['published_rows'][0]['position_change']['residual']==0
    assert test['published_rows'][1]['saved_keyFrame_member'] is False
    missing=compare_pair('synthetic',[],paper,'X','ref_x'); assert missing['baseline'] is None and missing['summary']['shared_rows']==0
    shifted=compare_pair('synthetic',[src('0',15),src('0.4',17)],paper,'X','ref_x')
    assert shifted['summary']['position_change']['all_shared_compatible'] and not shifted['summary']['absolute']['all_shared_compatible']
    return {'status':'pass','tests':['degree_quarterturn_unequal_scales','zero_angle_y_sign','negative_grid_rounding','exact_halfgrid_ties_away_from_zero','absolute_and_change_enclosure_boundaries','irregular_vs_uniform_clocks','loaded_endpoint_selection','keyframe_flag_survives_conversion','offgrid_step_not_compacted','missing_source_published_and_outside_rows','no_baseline_without_overlap','common_baseline_offset_diagnostic']}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--controls-only',action='store_true'); parser.add_argument('--out',choices=['table-independent01.json','table-independent02.json']); args=parser.parse_args()
    controls=synthetic_controls()
    if args.controls_only:
        print(json.dumps(controls)); return
    if args.out is None: raise ValueError('explicit_output_required')
    target=HERE/args.out
    if target.exists(): raise ValueError('output_already_exists')
    before={key:pin(path) for key,(path,expected) in PINS.items()}
    assert all(before[key]['sha256']==expected for key,(path,expected) in PINS.items())
    project=json.loads(PINS['project'][0].read_text()); printed=json.loads(PINS['table'][0].read_text())
    probe=json.loads(PINS['probe'][0].read_text()); selection=json.loads(PINS['selection'][0].read_text())
    config={}; setting_locators={}
    classes={'VideoClip':('startframe','stepsize','stepcount','starttime','video_framecount'),
             'StepperClipControl':('delta_t','frame','rate'),
             'ImageCoordSystem$FrameData':('xorigin','yorigin','angle','xscale','yscale')}
    for short,fields in classes.items():
        objs=[o for o in project['settings_objects'] if o['class'].rsplit('.',1)[-1]==short]; assert len(objs)==1
        for key in fields:
            field=finite_field(objs[0]['fields'][key]); config[key]=field['saved_text']; setting_locators[key]=field['xml_path']
    expected={'startframe':'0','stepsize':'6','stepcount':'80','starttime':'-2020.0','video_framecount':'476','delta_t':'33.36666666666667','frame':'258','rate':'1.0','xorigin':'470.25','yorigin':'349.0','angle':'-2.5913472025433153','xscale':'1.4841091539439202','yscale':'1.4841091539439202'}
    assert config==expected
    assert printed['physical_and_printed_page']==47 and len(printed['rows'])==70
    paper=[{k:r[k] for k in ('page','row','time_s','ref_x','ref_y','ne_y','ec_y','wc_y','nw_y')} for r in printed['rows']]
    times=[F(r['time_s']) for r in paper]; assert times==sorted(set(times)) and all(t*5==int(t*5) for t in times)
    stream=probe['streams']; assert len(stream)==1
    tb=F(stream[0]['time_base']); frames=probe['frames']; assert len(frames)==476 and len(selection['frames'])==476
    engine_ms={}
    for i,(r,sel) in enumerate(zip(frames,selection['frames'])):
        assert sel['index']==i and sel['pts']==r['pts'] and F(sel['time_seconds_exact'])==r['pts']*tb
        engine_ms[i]=F(r['pts'])*tb*1000
    assert all(engine_ms[i+1]>engine_ms[i] for i in range(475))
    start,step,count=(int(config[k]) for k in ('startframe','stepsize','stepcount'))
    domain=list(range(start,start+step*count,step)); a,b=domain[0],domain[-1]
    assert [a,b]==[0,474] and domain==project['saved_clip_domain']['saved_clip_step_indices']
    clocks=[{'frame':n,'U_seconds_exact':str(nominal_clock(n,config)),
             'current_pts_seconds_exact':str(engine_ms[n]/1000),
             'current_stretched_seconds_exact':str(stretched_clock(n,config,engine_ms,a,b)),
             'U_minus_current_stretched_exact':str(nominal_clock(n,config)-stretched_clock(n,config,engine_ms,a,b))} for n in domain]
    tracks=[]; comparisons=[]
    for track in project['pointmass_tracks']:
        assert len(track['framedata'])==1 and len(track['keyFrames'])==1
        keys=set(track['keyFrames'][0]['values']); original=track['framedata'][0]['rows']; derived=[]
        for row in original:
            assert row['finite_complete'] and len(row['objects'])==1
            fields=row['objects'][0]['coordinates']; x,y=finite_field(fields['x']),finite_field(fields['y'])
            n=row['index']; key=n in keys; assert key==row['saved_keyFrame_member']
            result=derive_point(n,x,y,key,config,engine_ms,a,b,row['xml_path']); assert result['selected_clip_step']
            derived.append(result)
        derived.sort(key=lambda r:r['frame']); actual=[r['frame'] for r in derived]
        assert actual==sorted(set(actual)) and actual==track['saved_indices']
        missing=sorted(set(domain)-set(actual)); assert missing==track['missing_clip_step_indices']
        tracks.append({'track_id':track['track_id'],'pointmass_ordinal':track['pointmass_ordinal_one_based'],
                       'source_assigned_names':track['names'],'source_track_locator':track['xml_path'],
                       'saved_row_count':len(derived),'saved_keyframe_indices':sorted(keys),
                       'missing_selected_frame_indices':missing,'missing_video_frame_indices':track['missing_video_frame_indices'],
                       'rows':derived})
        comparisons.extend(compare_pair(track['track_id'],derived,paper,axis,column) for axis,column in PAIRS)
    assert len(tracks)==8 and sum(t['saved_row_count'] for t in tracks)==334 and len(comparisons)==48
    after={key:pin(path) for key,(path,unused) in PINS.items()}; assert before==after
    result={'schema':'tilted-table-independent-v1','status':'conditional_source_correspondence_only',
            'method':'generic_determinant_inverse_exact_fraction_clock_and_grid',
            'python':platform.python_version(),'script':pin(Path(__file__)),
            'input_pins':before,'input_pins_after':after,'synthetic_controls':controls,
            'paper_source':{'sha256':printed['source_sha256'],'physical_and_printed_page':47,'table_file_sha256':PINS['table'][1]},
            'config_literal':config,'config_field_locators':setting_locators,
            'rules':{'clock':'U_uniform_historical_engine_hypothesis','nominal_grid_exact':'1/5','grid_ties':'away_from_zero','printed_time_bound_exact':'1/200','absolute_bound_exact':str(ABS_BOUND),'position_change_bound_exact':str(CHANGE_BOUND),'separate_arithmetic_tolerance_exact':str(ARITH_TOL)},
            'current_probe_clock_comparison':{'expected_loaded_endpoints':[a,b],'source_frame_time_base':str(tb),'selected_frame_count':len(clocks),'rows':clocks,'all_U_equal_current_stretched_exact':all(r['U_minus_current_stretched_exact']=='0' for r in clocks)},
            'tracks':tracks,'comparisons':comparisons,
            'totals':{'tracks':len(tracks),'converted_saved_rows':sum(t['saved_row_count'] for t in tracks),'series_pairs':len(comparisons),'published_row_slots':sum(len(c['published_rows']) for c in comparisons),'nonkey_rows':sum(not r['saved_keyFrame_member'] for t in tracks for r in t['rows'])}}
    encoded=json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+'\n'
    with target.open('x') as out: out.write(encoded)
    print(json.dumps({'output':target.name,'sha256':pin(target)['sha256'],'totals':result['totals'],
                      'all_U_equal_current_stretched_exact':result['current_probe_clock_comparison']['all_U_equal_current_stretched_exact'],
                      'all_shared_absolute_pairs':[(c['track_id'],c['paper_column'],c['summary']['shared_rows']) for c in comparisons if c['summary']['absolute']['all_shared_compatible']],
                      'all_shared_change_pairs':[(c['track_id'],c['paper_column'],c['summary']['shared_rows']) for c in comparisons if c['summary']['position_change']['all_shared_compatible']]}))


# BEGIN CROSS_IMPLEMENTATION_VERIFIER (added only after both independent runs)
def verify_existing_outputs():
    """Compare frozen outputs fieldwise; do not read or run the other producer."""
    own01=HERE/'table-independent01.json'; own02=HERE/'table-independent02.json'
    peer01=HERE/'table01/comparison.json'; peer02=HERE/'table02/comparison.json'
    own=json.loads(own01.read_text()); peer=json.loads(peer01.read_text())
    assert own01.read_bytes()==own02.read_bytes()
    assert peer01.read_bytes()==peer02.read_bytes()
    assert pin(peer01)['sha256']=='ee49c2628398d5b1009df9c8ef12dc51aa1ec74a4c4a697d894bad38dda3bf19'
    # Recover the initially frozen producer byte-for-byte: only this appended
    # verifier and the final dispatch have been added after that producer ran.
    frozen=Path(__file__).read_bytes().split(b'# BEGIN CROSS_IMPLEMENTATION_VERIFIER')[0]+b"if __name__=='__main__':\n    main()\n"
    assert len(frozen)==own['script']['bytes']
    assert hashlib.sha256(frozen).hexdigest()==own['script']['sha256']
    source_checks=0
    for relative,expected in peer['source_pins'].items():
        path=(HERE/relative).resolve(); assert path.is_relative_to(HERE.parent)
        assert pin(path)==expected; source_checks+=1
    assert own['paper_source']['sha256']==peer['source_pins']['../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf']['sha256']
    counts=Counter(); errors=Counter(); deltas={}; status_counts=Counter(); pair_results=[]
    def equal(category,left,right):
        counts[category]+=1
        if left!=right: errors[category]+=1
    def close(category,left,right):
        counts[category]+=1
        if left is None or right is None:
            if left is not None or right is not None: errors[category]+=1
            return
        distance=abs(left-right); deltas[category]=max(deltas.get(category,0),distance)
        if distance>float(ARITH_TOL): errors[category]+=1
    peer_tracks={t['track_id']:t for t in peer['tracks']}; bytrack={}
    for tr in own['tracks']:
        pt=peer_tracks[tr['track_id']]; prow={r['frame']:r for r in pt['rows']}
        bytrack[tr['track_id']]={r['frame']:r for r in tr['rows']}
        equal('track_frame_membership',set(bytrack[tr['track_id']]),set(prow))
        equal('missing_selected_frames',tr['missing_selected_frame_indices'],pt['missing_clip_step_indices'])
        equal('missing_video_frames',tr['missing_video_frame_indices'],pt['missing_video_frame_indices'])
        equal('source_assigned_names',tr['source_assigned_names'],pt['source_names'])
        for row in tr['rows']:
            pr=prow[row['frame']]
            for axis in ('X','Y'): close('world_coordinate',row[axis],pr['world'][axis])
            for ours,theirs in [('step','step'),('saved_keyFrame_member','saved_keyFrame_member'),('source_row_locator','source_row_xml_path'),('printed_time_compatible_0_01s','printed_time_rounding_0_01s_compatible')]:
                equal('source_index_key_locator_timeflag',row[ours],pr[theirs])
            for axis in ('x','y'):
                equal('source_coordinate_literal',row['source_'+axis]['saved_text'],pr['source_coordinate_text'][axis])
                equal('source_coordinate_locator',row['source_'+axis]['xml_path'],pr['source_coordinate_xml_paths'][axis])
            for ours,theirs in [('U_seconds_exact','uniform_time_s'),('nominal_grid_seconds_exact','nominal_grid_time_s'),('time_grid_residual_seconds_exact','nominal_time_residual_s'),('current_pts_stretched_seconds_exact','current_pts_stretched_time_s')]:
                equal('exact_clock_grid',F(row[ours]),F(pr[theirs]['exact_fraction']))
            equal('exact_clock_difference',F(row['U_minus_current_stretched_seconds_exact']),-F(pr['current_pts_minus_uniform_s']['exact_fraction']))
    peer_pairs={(p['track_id'],p['saved_axis'],p['printed_column']):p for p in peer['pairs']}
    equal('pair_membership',set(peer_pairs),{(p['track_id'],p['axis'],p['paper_column']) for p in own['comparisons']})
    for pair in own['comparisons']:
        pp=peer_pairs[(pair['track_id'],pair['axis'],pair['paper_column'])]
        ours={F(r['printed_time_text']):r for r in pair['published_rows']}
        ours.update({F(r['nominal_grid_seconds_exact']):r for r in pair['unjoined_source_rows']})
        theirs={F(r['nominal_grid_time_s']['exact_fraction']):r for r in pp['rows']}
        equal('pair_row_grid_membership',set(ours),set(theirs))
        for grid,row in ours.items():
            pr=theirs[grid]; saved=pr['saved']; printed=pr['printed']
            state=('outside_publication_grid' if printed is None else
                   'compared' if saved is not None and printed['saved_text'] is not None else
                   'missing_source' if saved is None and printed['saved_text'] is not None else
                   'missing_published_value' if saved is not None else 'missing_both')
            equal('normalized_missing_state',row['status'],state); status_counts[row['status']]+=1
            if saved is not None:
                frame=row['frame'] if state=='outside_publication_grid' else row['source_frame']
                sr=bytrack[pair['track_id']][frame]
                equal('pair_source_frame',frame,saved['frame'])
                equal('pair_source_key',row['saved_keyFrame_member'],saved['saved_keyFrame_member'])
                equal('pair_source_locator',row['source_row_locator'],saved['source_row_xml_path'])
                close('pair_source_world',row['source_world'],saved['value'])
                equal('pair_source_step',sr['step'],saved['step'])
                equal('pair_source_exact_time',F(sr['U_seconds_exact']),F(saved['uniform_time_s']['exact_fraction']))
                equal('pair_source_exact_time_residual',F(sr['time_grid_residual_seconds_exact']),F(saved['nominal_time_residual_s']['exact_fraction']))
                equal('pair_source_timeflag',sr['printed_time_compatible_0_01s'],saved['printed_time_rounding_0_01s_compatible'])
                for axis in ('x','y'): equal('pair_source_coordinate_locator',sr['source_'+axis]['xml_path'],saved['source_coordinate_xml_paths'][axis])
            if printed is not None:
                for ourskey,theirskey in [('page','physical_and_printed_page'),('row','row'),('column','column')]:
                    equal('printed_locator',row['paper_locator'][ourskey],printed[theirskey])
                equal('printed_literal',row['printed_value_text'],printed['saved_text'])
                equal('printed_time_literal',row['printed_time_text'],printed['time_text'])
                equal('printed_source_hash',own['paper_source']['sha256'],printed['source_pdf_sha256'])
            for ourskey,theirskey in [('absolute','absolute'),('position_change','displacement')]:
                if state!='compared': equal('missing_diagnostic_none',row.get(ourskey),pr[theirskey]); continue
                diag,pdiag=row[ourskey],pr[theirskey]
                close(ourskey+'_residual',diag['residual'],pdiag['residual'])
                equal(ourskey+'_strict_decision',diag['inside_print_enclosure'],pdiag['print_enclosure_compatible'])
                equal(ourskey+'_tolerated_decision',diag['compatible_with_arithmetic_tolerance'],pdiag['with_arithmetic_tolerance_compatible'])
        baseline,pbase=pair['baseline'],pp['baseline']
        equal('baseline_presence',baseline is None,pbase is None)
        if baseline is not None:
            equal('baseline_frame',baseline['frame'],pbase['frame']); equal('baseline_paper_row',baseline['paper_row'],pbase['printed_row'])
            close('baseline_offset',baseline['original_offset'],pbase['original_saved_minus_printed_offset'])
            close('baseline_source_world',baseline['source_world'],pbase['saved_value'])
            equal('baseline_printed_value',float(F(baseline['printed_text'])),pbase['printed_value'])
        for ourskey,theirskey in [('absolute','absolute_summary'),('position_change','displacement_summary')]:
            summary,psummary=pair['summary'][ourskey],pp[theirskey]
            equal('pair_summary_available',pair['summary']['shared_rows'],psummary['available_count'])
            for ok,pk in [('strict_compatible_count','print_enclosure_pass_count'),('compatible_count','with_arithmetic_tolerance_pass_count'),('all_shared_compatible','all_available_compatible')]:equal('pair_summary_counts_and_decisions',summary[ok],psummary[pk])
            for ok,pk in [('max_abs_residual','maximum_absolute_residual'),('signed_residual_min','signed_residual_minimum'),('signed_residual_max','signed_residual_maximum')]:close('pair_summary_residual',summary[ok],psummary[pk])
        shared=[r for r in pair['published_rows'] if r['status']=='compared']
        strict=sum(r['printed_time_compatible_0_01s'] for r in shared)
        equal('shared_time_count',strict,pp['counts']['shared_finite_printed_time_0_01s_compatible'])
        equal('shared_nonkey_count',sum(not r['saved_keyFrame_member'] for r in shared),pp['counts']['shared_finite_nonkey_rows'])
        equal('all_70_rows_available',len(shared)==70,pp['complete_row_compatibility']['all_70_published_rows_have_finite_saved_and_printed_values'])
        for ok,pk in [('absolute','absolute_position_and_strict_printed_time_count'),('position_change','displacement_and_strict_printed_time_count')]:
            equal('joint_position_time_count',sum(r['printed_time_compatible_0_01s'] and r[ok]['compatible_with_arithmetic_tolerance'] for r in shared),pp['complete_row_compatibility'][pk])
        pair_results.append({'track_id':pair['track_id'],'column':pair['paper_column'],'shared':len(shared),'strict_time':strict,
                             'absolute_compatible':pair['summary']['absolute']['compatible_count'],
                             'displacement_compatible':pair['summary']['position_change']['compatible_count'],
                             'absolute_max_residual':pair['summary']['absolute']['max_abs_residual'],
                             'displacement_max_residual':pair['summary']['position_change']['max_abs_residual'],
                             'baseline_offset':baseline['original_offset'] if baseline else None})
    result={'status':'pass' if not errors else 'disagreement','arithmetic_tolerance':float(ARITH_TOL),
            'initial_independent_producer_sha256':own['script']['sha256'],'initial_method_bytes_preserved':True,
            'independent01':pin(own01),'independent02':pin(own02),'peer01':pin(peer01),'peer02':pin(peer02),
            'peer_source_pins_currently_verified':source_checks,'checks_by_category':dict(counts),
            'disagreements_by_category':dict(errors),'maximum_numeric_differences':deltas,
            'normalized_comparison_row_status_counts':dict(status_counts),'pair_results':pair_results,
            'strict_time_pass_shared_comparison_rows':sum(p['strict_time'] for p in pair_results),
            'strict_grid_time_pass_source_rows':sum(r['printed_time_compatible_0_01s'] for t in own['tracks'] for r in t['rows'])}
    print(json.dumps(result,sort_keys=True,indent=2))
    if errors: raise ValueError('cross_implementation_disagreement')


if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--compare-existing']:
        verify_existing_outputs()
    else:
        main()
