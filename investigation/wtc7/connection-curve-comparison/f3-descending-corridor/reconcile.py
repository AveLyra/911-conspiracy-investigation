"""Preserve and reconcile frozen manual corridor readings without fitting curves."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import platform
import tempfile

HERE=Path(__file__).resolve().parent
SOURCE='53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd'
PROTOCOL='12525bcb149368f18d85e3611f32137ccdeef723cc95df93cf2b5d9b13f2aa27'
TARGETS=[(route,x) for route in ['solid','dash'] for x in range(270,360)]
STATUSES={'identified_local_fragment','fringe_only','no_attributable_cells','identity_conflict','boundary_truncated'}


def pin(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def read(path):
    return json.loads(path.read_text())


def save(path,value):
    with path.open('x') as f:
        json.dump(value,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')


def rowset(values):
    if (not isinstance(values,list) or any(type(y) is not int or not 0<=y<=87 for y in values)
            or values!=sorted(set(values))):
        raise ValueError('Invalid native row set')
    return set(values)


def validate(record):
    if record.get('source_sha256')!=SOURCE or record.get('protocol_sha256')!=PROTOCOL:
        raise ValueError('Source/protocol mismatch')
    if not isinstance(record.get('reader'),str) or not record['reader'].strip():
        raise ValueError('Missing reader')
    entries=record.get('observations')
    if not isinstance(entries,list) or len(entries)!=180:
        raise ValueError('Wrong coverage')
    keys=[]
    for e in entries:
        if e.get('route') not in ['solid','dash'] or type(e.get('column')) is not int:
            raise ValueError('Invalid route/column')
        keys.append((e['route'],e['column']))
        c,f=rowset(e.get('core_rows')),rowset(e.get('fringe_rows'))
        if c&f: raise ValueError('Core/fringe overlap')
        if e.get('status') not in STATUSES or not isinstance(e.get('note'),str) or not e['note'].strip():
            raise ValueError('Missing status/explanation')
        flags=[]
        if 0 in c|f: flags.append('strip_top')
        if 87 in c|f: flags.append('strip_bottom')
        if c|f:
            if e['column']==270: flags.append('target_left')
            if e['column']==359: flags.append('target_right')
        if e.get('boundary_flags')!=flags: raise ValueError('Boundary flags disagree with selected cells')
        fragments=e.get('fragment_membership')
        if fragments is not None:
            if not isinstance(fragments,dict): raise ValueError('Invalid fragment mapping')
            cs,fs=set(),set()
            for name,piece in fragments.items():
                if not isinstance(name,str) or not name.strip(): raise ValueError('Missing fragment ID')
                pc,pf=rowset(piece.get('core_rows')),rowset(piece.get('fringe_rows'))
                if pc&pf: raise ValueError('Fragment class overlap')
                cs|=pc; fs|=pf
            if cs!=c or fs!=f: raise ValueError('Fragment union mismatch')
        elif (c|f) and (not isinstance(e.get('fragment_id'),str) or not e['fragment_id']):
            raise ValueError('Missing local fragment attribution')
    if keys!=TARGETS: raise ValueError('Missing/duplicate/reordered column')
    return entries


def family(a,b):
    return {'intersection':sorted(a&b),'union':sorted(a|b),'symmetric_difference':sorted(a^b),
            'root_only':sorted(a-b),'independent_only':sorted(b-a)}


def compare(left,right):
    out=[]
    for a,b in zip(validate(left),validate(right)):
        ca,cb=set(a['core_rows']),set(b['core_rows'])
        fa,fb=set(a['fringe_rows']),set(b['fringe_rows'])
        out.append({'route':a['route'],'column':a['column'],'root':a,'independent':b,
                    'core':family(ca,cb),'fringe':family(fa,fb),'outer':family(ca|fa,cb|fb),
                    'core_equal':ca==cb,'fringe_equal':fa==fb,'outer_equal':ca|fa==cb|fb,
                    'partition_equal':ca==cb and fa==fb,'status_text_equal':a['status']==b['status']})
    return out


def overlap(old,new):
    out=[]
    lookup={(r['route'],r['column']):r for r in new['observations']}
    for row in old['observations']:
        route,x=row['fragment'],row['column']
        newer=lookup[(route,x)]
        roi=set(range(32,49) if route=='solid' else range(4,15))
        item={'route':route,'column':x,'old_row_roi_inclusive':[min(roi),max(roi)],'classes':{}}
        for field in ['core_rows','fringe_rows']:
            a,b=set(row[field]),set(newer[field])
            item['classes'][field]={'old':sorted(a),'new_inside_old_roi':sorted(b&roi),
                                   'symmetric_difference_in_common_roi':sorted(a^(b&roi)),
                                   'new_outside_old_roi':sorted(b-roi)}
        out.append(item)
    return out


def controls():
    fixture={'reader':'synthetic','source_sha256':SOURCE,'protocol_sha256':PROTOCOL,
             'observations':[{'route':r,'column':x,'core_rows':[],'fringe_rows':[],
              'status':'no_attributable_cells','note':'Synthetic.','fragment_id':None,'boundary_flags':[]}
              for r,x in TARGETS]}
    checks={'complete_empty_coverage':len(validate(fixture))==180,
            'shared_columns_across_routes':all(r['partition_equal'] for r in compare(fixture,fixture))}
    def reject(name,change):
        t=copy.deepcopy(fixture); change(t)
        try: validate(t)
        except ValueError: checks[name]=True
        else: checks[name]=False
    for name,value in [('duplicate_rows',[2,2]),('unsorted_rows',[3,2]),('boolean_row',[True]),
                       ('fractional_row',[2.5]),('out_of_bounds',[88])]:
        reject(name,lambda t,v=value:t['observations'][1].update(core_rows=v))
    reject('boolean_column',lambda t:t['observations'][1].update(column=True))
    reject('duplicate_column',lambda t:t['observations'][1].update(column=270))
    reject('missing_column',lambda t:t['observations'].pop())
    reject('wrong_route',lambda t:t['observations'][1].update(route='other'))
    reject('changed_source',lambda t:t.update(source_sha256='0'*64))
    reject('changed_protocol',lambda t:t.update(protocol_sha256='0'*64))
    reject('overlap',lambda t:t['observations'][1].update(core_rows=[2],fringe_rows=[2]))
    reject('missing_boundary',lambda t:t['observations'][1].update(core_rows=[0],fragment_id='one'))
    reject('bad_fragment_union',lambda t:t['observations'][1].update(core_rows=[2],fragment_membership={}))
    a,b=copy.deepcopy(fixture),copy.deepcopy(fixture)
    a['observations'][1].update(core_rows=[2],fringe_rows=[4],fragment_id='left')
    b['observations'][1].update(core_rows=[4],fringe_rows=[2],fragment_id='other_name')
    r=compare(a,b)[1]
    checks['equal_outer_unequal_partition']=r['outer_equal'] and not r['partition_equal']
    checks['holes_retained']=r['outer']['union']==[2,4]
    b['observations'][1].update(core_rows=[6],fringe_rows=[8])
    r=compare(a,b)[1]
    checks['disjoint']=r['outer']['intersection']==[] and r['outer']['union']==[2,4,6,8]
    old={'observations':[{'fragment':'dash','column':300,'core_rows':[7],'fringe_rows':[]}]}
    new={'observations':[{'route':'dash','column':300,'core_rows':[7,20],'fringe_rows':[]}]}
    r=overlap(old,new)[0]['classes']['core_rows']
    checks['old_roi_does_not_exclude_unseen']=r['symmetric_difference_in_common_roi']==[] and r['new_outside_old_roi']==[20]
    with tempfile.TemporaryDirectory(prefix='corridor-control-') as d:
        p=Path(d)/'result.json'; save(p,{'synthetic':True}); before=pin(p)
        try: save(p,{'replacement':True})
        except FileExistsError: checks['overwrite_refused']=pin(p)==before
        else: checks['overwrite_refused']=False
    if not all(checks.values()): raise AssertionError(checks)
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['controls','run01','run02']); args=parser.parse_args()
    target=HERE/(args.mode+'.json')
    if target.exists(): raise FileExistsError('Existing output preserved')
    state={'script':pin(Path(__file__)),'protocol':pin(HERE/'PROTOCOL.md'),'python':platform.python_version()}
    if state['protocol']['sha256']!=PROTOCOL: raise ValueError('Changed protocol')
    if args.mode=='controls':
        tests=controls(); save(target,{'state':state,'status':'complete','checks':tests})
        print(json.dumps({'checks':len(tests),'passed':True})); return
    gate=read(HERE/'controls.json')
    if gate['state']!=state or len(gate['checks'])!=21 or not all(gate['checks'].values()):
        raise ValueError('Stale/incomplete controls')
    inputs=[HERE/n for n in ['reader-root.json','reader-independent.json','reader-root.py','raw-context.json','read_context.py','method-review.json','controls.json']]
    inputs += [HERE.parent/'native-strips01/Im4.jpg']
    inputs += [HERE.parent/'f3-native-footprints'/n for n in ['reader-root.json','reader-independent.json']]
    before={str(p):pin(p) for p in inputs}
    if pin(inputs[7])['sha256']!=SOURCE: raise ValueError('Changed raster')
    review=read(HERE/'method-review.json')
    if review['protocol_sha256']!=PROTOCOL or review['decision']!='proceed_with_boundaries': raise ValueError('Review mismatch')
    left,right=read(inputs[0]),read(inputs[1]); raw=read(HERE/'raw-context.json')
    for r in [left,right]:
        if r['raw_context_sha256']!=pin(HERE/'raw-context.json')['sha256']: raise ValueError('Context mismatch')
    if raw['source_pin']['sha256']!=SOURCE or raw['protocol_pin']['sha256']!=PROTOCOL: raise ValueError('Context lineage')
    if [(c['x'],c['y']) for c in raw['cells']]!=[(x,y) for y in range(88) for x in range(268,362)]: raise ValueError('Raw coverage')
    table={(c['x'],c['y']):c['rgb'] for c in raw['cells']}
    for r in [left,right]:
        for e in validate(r):
            for y in e['core_rows']+e['fringe_rows']:
                if table[(e['column'],y)]==[255,255,255]: raise ValueError('Selected exact-white cell')
    result=compare(left,right)
    summary={}
    for route in ['all','solid','dash']:
        selected=[r for r in result if route=='all' or r['route']==route]
        summary[route]={'entries':len(selected),**{k+'_disagreeing_entries':sum(not r[k+'_equal'] for r in selected) for k in ['core','fringe','outer','partition']},
                        'both_outer_empty_entries':sum(not r['outer']['union'] for r in selected)}
    coverage={name:{route:dict(Counter(e['status'] for e in record['observations'] if e['route']==route)) for route in ['solid','dash']}
              for name,record in [('root',left),('independent',right)]}
    old_new={'root':overlap(read(inputs[8]),left),'independent':overlap(read(inputs[9]),right)}
    after={str(p):pin(p) for p in inputs}
    if before!=after: raise ValueError('Inputs changed')
    output={'state':state,'status':'complete','inputs':before,'inputs_after':after,'rows':result,
            'disagreement_summary':summary,'reader_status_coverage':coverage,'old_new_prior_informed_consistency':old_new,
            'limits':'Manual raster membership only. Reader-local fragment names are not cross-reader identity keys. Empty sets are not absent physical support. No confidence interval, original centerline, physical ordinate or model comparison.',
            'human_accepted':False}
    save(target,output); print(json.dumps({'status':'complete','summary':summary,'sha256':pin(target)['sha256']}))


if __name__=='__main__': main()
