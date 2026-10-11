"""Compare fixed E3 reader records without converting ink to physical curves."""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
READINGS={
    'root':'b5a8133dc71a0b516d69a3283bc068d75ef083d91ad4727124f8c70a49fc217f',
    'independent':'245b5ffe99b0481ab86e57c3bb7d1fccd7d1539a6ce004de967ec118d2e6c243',
}


def require(ok,message):
    if not ok:raise ValueError(message)


def pin(p):
    b=p.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}


def rows(record):
    c,f=record['core'],record['fringe']
    for v in (c,f):
        require(type(v) is list and all(type(y) is int and 30<=y<60 for y in v),'row type/range')
        require(v==sorted(set(v)),'row order/duplicates')
    require(not set(c)&set(f),'core/fringe overlap')
    return set(c),set(f)


def check_flags(record):
    c,f=rows(record); selected=c|f;x=record['x']
    expected=[]
    if selected:
        if x==365:expected.append('target_left')
        if x==689:expected.append('target_right')
        if 30 in selected:expected.append('target_top')
        if 59 in selected:expected.append('target_bottom')
    require(record['boundary_flags']==expected,'selected-cell boundary flags')


def validate(data):
    require(data['pair']=='E3','pair')
    box=data.get('target_box',data.get('coverage',{}).get('target_box'))
    require(box==[365,30,690,60],'target')
    require(set(data['routes'])=={'solid','dash'},'routes')
    bands={};seen=set();last_x=364
    for b in data['unassigned_bands']:
        x=b['x'];require(type(x) is int and 365<=x<690 and x>last_x,'band coverage/order');last_x=x
        check_flags(b)
        band_id=b.get('band_id',b.get('fragment_id'))
        require(not(rows(b)[0]|rows(b)[1]) or isinstance(band_id,str),'band identity')
        bands[x]=b
        if band_id is not None:
            require((x,band_id) not in seen,'duplicate band');seen.add((x,band_id))
    for route,entries in data['routes'].items():
        require([r['x'] for r in entries]==list(range(365,690)),'complete route columns')
        for r in entries:
            require(type(r['x']) is int,'column type');check_flags(r)
            c,f=rows(r);bid=r['fragment_id']
            require(r['status'] in ['identified_local_fragment','boundary_truncated','fringe_only','identity_conflict','no_attributable_cells'],'status')
            if r['status']=='no_attributable_cells':require(not c and not f and bid is None,'nonempty no-attribution')
            if r['status']=='fringe_only':require(not c and bool(f),'fringe-only classes')
            if r['status'] in ['identified_local_fragment','boundary_truncated']:
                require(bool(c) and isinstance(bid,str),'identified fragment')
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


def run():
    names=[f'reader-E3-{who}.json' for who in READINGS]
    data={who:json.loads((HERE/name).read_text()) for who,name in zip(READINGS,names)}
    before={name:pin(HERE/name) for name in names}
    dependencies={}
    for who,d in data.items():
        require(before[f'reader-E3-{who}.json']['sha256']==READINGS[who],'frozen reading changed')
        declared=d.get('inputs',d.get('pins'))
        for name,value in declared.items():
            current=pin(HERE/name); expected=value['sha256'] if isinstance(value,dict) else value
            require(current['sha256']==expected,'input pin '+name)
            dependencies[name]=current
        script=HERE/f'reader-E3-{who}.py';expected=d.get('script_pin',{}).get('sha256',d.get('annotation_script_sha256'))
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
    for x in range(365,690):
        selections=[]
        for who,d in data.items():
            members=[d['routes'][r][x-365] for r in ('solid','dash')]
            if x in bands[who]:members.append(bands[who][x])
            core=set();fringe=set()
            for record in members:
                c,f=rows(record);core|=c;fringe|=f
            selections.append({'core':sorted(core),'fringe':sorted(fringe)})
        geometry.append({'x':x,'root_unassigned_original':bands['root'].get(x),
            'peer_unassigned_original':bands['independent'].get(x),
            'sets':compare_records(*selections)})
    context=json.loads((HERE/'context01.json').read_text())
    pixels={(r['x'],r['y']):r['rgb'] for r in context['cells']['E3']}
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
        'dependencies':dependencies,'script_pin':pin(Path(__file__)),'literal_readings':data,
        'route_comparisons':comparisons,'visible_ink_comparisons':geometry,
        'summary':{'routes':totals(comparisons),'visible_ink':totals(geometry),
            'route_status_different':sum(r['root_original']['status']!=r['peer_original']['status'] for r in comparisons),
            'selected_exact_white_cells':selected_white},
        'limits':'Schema checks and set differences do not certify source accuracy, model identity, containment or support. White selections are flagged, not erased or accepted as visible ink. Reader-local IDs are not equated. Empty unassigned records differ from missing records; neither means absent historical curves.',
        'human_accepted':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();result=run()
    target=HERE/args.output
    with target.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':pin(target),'summary':result['summary']}))
