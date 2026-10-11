"""Compare fixed E4/E5 reader records without converting ink to physical curves."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
TARGETS={'E4':[440,72,690,92],'E5':[395,18,690,47]}
E4_PINS={'root':'b1ad179b8cbd256e0cb01c9d79ac54778dccc6312698e38008399db6a93c9326',
'independent':'f7545fea9317bc7c24ec7b5f6e5d63bc5158e1a11b31b361fa29099d39976a01'}


def require(ok,message):
    if not ok:raise ValueError(message)


def pin(p):
    b=p.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}


def rows(record):
    c,f=record['core'],record['fringe']
    for v in (c,f):
        require(type(v) is list and all(type(y) is int and 0<=y<92 for y in v),'row type/range')
        require(v==sorted(set(v)),'row order/duplicates')
    require(not set(c)&set(f),'core/fringe overlap')
    return set(c),set(f)


def check_flags(record,box):
    c,f=rows(record); selected=c|f;x=record['x']; x0,y0,x1,y1=box
    require(all(y0<=y<y1 for y in selected),'target row bounds')
    expected=[]
    if selected:
        if x==x0:expected.append('target_left')
        if x==x1-1:expected.append('target_right')
        if y0 in selected:expected.append('target_top')
        if y1-1 in selected:expected.append('target_bottom')
    require(record['boundary_flags']==expected,'selected-cell boundary flags')


def validate(data):
    require(data['pair'] in TARGETS,'pair')
    target=TARGETS[data['pair']];x0,y0,x1,y1=target
    box=data.get('target_box',data.get('coverage',{}).get('target_box'))
    require(box==target,'target')
    require(set(data['routes'])=={'solid','dash'},'routes')
    bands={};seen=set();last_x=x0-1
    for b in data['unassigned_bands']:
        x=b['x'];require(type(x) is int and x0<=x<x1 and x>last_x,'band coverage/order');last_x=x
        check_flags(b,box)
        band_id=b.get('band_id',b.get('fragment_id'))
        require(not(rows(b)[0]|rows(b)[1]) or isinstance(band_id,str),'band identity')
        bands[x]=b
        if band_id is not None:
            require((x,band_id) not in seen,'duplicate band');seen.add((x,band_id))
    for route,entries in data['routes'].items():
        require([r['x'] for r in entries]==list(range(x0,x1)),'complete route columns')
        for r in entries:
            require(type(r['x']) is int,'column type');check_flags(r,box)
            c,f=rows(r);bid=r['fragment_id']
            require(r['status'] in ['identified_local_fragment','boundary_truncated','fringe_only','identity_conflict','no_attributable_cells'],'status')
            if r['status']=='no_attributable_cells':require(not c and not f and bid is None,'nonempty no-attribution')
            if r['status']=='fringe_only':require(not c and bool(f),'fringe-only classes')
            if r['status']=='identified_local_fragment':require(bool(c) and isinstance(bid,str),'identified fragment')
            if r['status']=='boundary_truncated':require(bool(c|f) and isinstance(bid,str),'truncated selected fragment')
            if r['status']=='boundary_truncated':require(bool(r['boundary_flags']),'unflagged truncation')
            refs=r.get('band_refs',r.get('unassigned_band_refs',[]))
            require(not ('band_refs' in r and 'unassigned_band_refs' in r),'ambiguous ref schema')
            for ref in refs:
                pair=(r['x'],ref) if isinstance(ref,str) else (ref['x'],ref['band_id'])
                require(pair[0]==r['x'] and pair in seen,'band reference same column')
            b=bands.get(r['x'])
            if b is not None:require(not(c|f)&(rows(b)[0]|rows(b)[1]),'duplicate model/unassigned attribution')
    for a,b in zip(data['routes']['solid'],data['routes']['dash']):
        require(not(rows(a)[0]|rows(a)[1])&(rows(b)[0]|rows(b)[1]),'duplicated model ink')
    return bands


def operations(a,b):
    return {'intersection':sorted(a&b),'union':sorted(a|b),'root_only':sorted(a-b),
            'peer_only':sorted(b-a),'symmetric_difference':sorted(a^b)}


def compare_records(a,b):
    ac,af=rows(a);bc,bf=rows(b)
    return {k:operations(x,y) for k,x,y in [('core',ac,bc),('fringe',af,bf),('outer',ac|af,bc|bf)]}


def run(pair, reading_pins):
    require(pair in TARGETS,'pair')
    require(set(reading_pins)=={'root','independent'},'reading pin roles')
    x0,y0,x1,y1=TARGETS[pair]
    names=[f'reader-{pair}-{who}.json' for who in reading_pins]
    data={who:json.loads((HERE/name).read_text()) for who,name in zip(reading_pins,names)}
    before={name:pin(HERE/name) for name in names}
    dependencies={}
    for who,d in data.items():
        require(before[f'reader-{pair}-{who}.json']['sha256']==reading_pins[who],'frozen reading changed')
        declared=d.get('inputs',d.get('pins'))
        require(isinstance(declared,dict) and {'PROTOCOL.md','IDENTITY-CLARIFICATION.md','context01.json','context02.json','../../native-strips01/Im9.jpg'}<=set(declared),'missing required pins')
        for name,value in declared.items():
            current=pin(HERE/name); expected=value['sha256'] if isinstance(value,dict) else value
            require(current['sha256']==expected,'input pin '+name)
            dependencies[name]=current
        script=HERE/f'reader-{pair}-{who}.py';expected=d.get('script_pin',{}).get('sha256',d.get('annotation_script_sha256'))
        require(pin(script)['sha256']==expected,'reader script pin')
        dependencies[script.name]=pin(script)
    bands={who:validate(d) for who,d in data.items()}
    a,b=data['root'],data['independent'];comparisons=[]
    for route in ('solid','dash'):
        for ra,rb in zip(a['routes'][route],b['routes'][route]):
            comparisons.append({'route':route,'x':ra['x'],'root_original':ra,'peer_original':rb,
                                'sets':compare_records(ra,rb)})
    # Compare visible selections independently from route assignment. No missing
    # band record is fabricated; originals are retained as null when not supplied.
    geometry=[]
    for x in range(x0,x1):
        selections=[]
        for who,d in data.items():
            members=[d['routes'][r][x-x0] for r in ('solid','dash')]
            if x in bands[who]:members.append(bands[who][x])
            core=set();fringe=set()
            for record in members:
                c,f=rows(record);core|=c;fringe|=f
            selections.append({'core':sorted(core),'fringe':sorted(fringe)})
        geometry.append({'x':x,'root_unassigned_original':bands['root'].get(x),
            'peer_unassigned_original':bands['independent'].get(x),
            'sets':compare_records(*selections)})
    context=json.loads((HERE/'context01.json').read_text())
    pixels={(r['x'],r['y']):r['rgb'] for r in context['cells'][pair]}
    context_box={'E4':[438,70,692,92],'E5':[393,16,692,49]}[pair]
    cx0,cy0,cx1,cy1=context_box
    require(len(pixels)==len(context['cells'][pair])==(cx1-cx0)*(cy1-cy0),'context coverage or duplicates')
    require(set(pixels)=={(x,y) for x in range(cx0,cx1) for y in range(cy0,cy1)},'context coordinate coverage')
    selected_white={}
    for who,d in data.items():
        selected_white[who]=[]
        collections=list(d['routes'].items())+[('unassigned',d['unassigned_bands'])]
        for scope,records in collections:
            for r in records:
                for label in ('core','fringe'):
                    for y in r[label]:
                        if pixels[r['x'],y]==[255,255,255]:
                            selected_white[who].append({'scope':scope,'class':label,'x':r['x'],'y':y})
    def totals(records):
        return {'entries':len(records),'outer_different':sum(bool(r['sets']['outer']['symmetric_difference']) for r in records),
                'class_different':sum(bool(r['sets']['core']['symmetric_difference'] or r['sets']['fringe']['symmetric_difference']) for r in records)}
    require(before=={n:pin(HERE/n) for n in names},'reading changed during comparison')
    require(all(v==pin(HERE/n) for n,v in dependencies.items()),'dependency changed during comparison')
    return {'status':'comparison_preserves_disagreement_not_physical_measurement','input_pins':before,
        'dependencies':dependencies,'script_pin':pin(Path(__file__)),'test_pin':pin(HERE/'test_compare_e45.py'),'pair':pair,'reviewer_independence':'Comparator author also authored peer E4 annotation; not independent verification','literal_readings':data,
        'route_comparisons':comparisons,'visible_ink_comparisons':geometry,
        'summary':{'routes':totals(comparisons),'visible_ink':totals(geometry),
            'route_status_different':sum(r['root_original']['status']!=r['peer_original']['status'] for r in comparisons),
            'selected_exact_white_cells':selected_white},
        'limits':'Schema checks and set differences do not certify source accuracy, model identity, containment or support. White selections are flagged, not erased or accepted as visible ink. Reader-local IDs are not equated. Empty unassigned records differ from missing records; neither means absent historical curves.',
        'human_accepted':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pair',choices=list(TARGETS),required=True);p.add_argument('--root-sha');p.add_argument('--peer-sha');p.add_argument('--output',required=True);args=p.parse_args()
    require(args.output in [f'comparison-{args.pair}-01.json',f'comparison-{args.pair}-02.json'],'output name')
    pins=E4_PINS if args.pair=='E4' else {'root':args.root_sha,'independent':args.peer_sha}
    require(all(isinstance(h,str) and len(h)==64 for h in pins.values()),'explicit frozen reading hashes required')
    result=run(args.pair,pins)
    target=HERE/args.output
    with target.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':pin(target),'summary':result['summary']}))
