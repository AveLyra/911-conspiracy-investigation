"""Finite F5/F6 reconciliation: preserve originals and every reader difference."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = {'F5-Im3':[310,0,425,88], 'F6-Im1':[270,55,340,88]}
CONTEXTS = {'F5-Im3':[308,0,427,88], 'F6-Im1':[268,53,342,88]}
HELPERS = {
 '../force45/compare_force45.py':'932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
 '../force69/compare_force69.py':'f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e',
 '../approach34/compare.py':'cb4a2da60959a4b0a40ddb4a072c1cbedf4624da63daf1a50b37db0eb2dd5bac',
}


def pin(path):
    raw=path.read_bytes()
    return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}


def require(ok,reason):
    if not ok:raise ValueError(reason)


def load(path):
    spec=importlib.util.spec_from_file_location(path.stem+'_'+path.parent.name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def helpers():
    for name,sha in HELPERS.items():
        require(pin(HERE/name)['sha256']==sha,'helper pin '+name)
    h=load(HERE/'../force45/compare_force45.py')
    v=load(HERE/'../force69/compare_force69.py')
    a=load(HERE/'../approach34/compare.py')
    # Isolated module instances only; preserved helper files are unchanged.
    h.TARGETS=TARGETS;h.CONTEXTS=CONTEXTS
    a.rows=h.rows;a.CONTEXTS=CONTEXTS
    return h,v,a


def validate(data,region,role,h,a):
    require(region in TARGETS,'region')
    box=TARGETS[region];pair,source=region.split('-')
    require(data['region_id']==region and data['pair']==pair and data['source']==source+'.jpg','region/source identity')
    identities={'primary':('primary',),'peer':('peer','force56_peer')}
    require(role in identities and data['reader'] in identities[role],'fixed reader-role identity')
    require(data['target_box']==box and data['context_box']==CONTEXTS[region],'reader geometry')
    require(data['human_accepted'] is False and data['physical_support'] is None,'native-only boundary')
    require(set(data['routes'])=={'solid','dash'},'routes')
    a.coverage(data,region)
    require(data['coverage'].get('uncompleted_context',[])==[],'incomplete context')
    normalized=a.adapted(data)
    indexed={};by_column={};occupied={};references=set()
    for b,original in zip(normalized['unassigned_bands'],data['unassigned_bands']):
        h.flags(b,box);h.members(b);key=(b['x'],b['band_id']);c,f=h.rows(b)
        require(key not in indexed and isinstance(b['band_id'],str) and b['band_id'],'unique band key')
        require(isinstance(b['note'],str) and b['note'].strip(),'band reason')
        candidates=b['candidate_routes']
        require(type(candidates) is list and len(candidates)==len(set(candidates)) and all(r in ('solid','dash') for r in candidates),'candidate routes')
        require(bool(c|f)==bool(candidates),'band material/candidates')
        require(not occupied.get(b['x'],set())&(c|f),'duplicate band ink')
        occupied.setdefault(b['x'],set()).update(c|f)
        indexed[key]=b;by_column.setdefault(b['x'],[]).append(original)
    for route,rs in normalized['routes'].items():
        require([r['x'] for r in rs]==list(range(box[0],box[2])),'complete route columns')
        for r in rs:
            h.flags(r,box);h.members(r);c,f=h.rows(r);status=r['status']
            require(isinstance(r['note'],str) and r['note'].strip(),'route reason')
            require(status in ('identity_conflict','no_attributable_cells','identified_local_fragment','boundary_truncated','fringe_only'),'route status')
            if status=='identified_local_fragment':require(bool(c),'identified without core')
            if status=='fringe_only':require(not c and bool(f),'fringe-only classes')
            if status=='boundary_truncated':require(bool(c|f) and bool(r['boundary_flags']),'truncation')
            refs=r['unassigned_band_refs'];require(type(refs) is list,'reference list')
            seen=set()
            for ref in refs:
                key=(r['x'],ref) if isinstance(ref,str) else (ref['x'],ref['band_id'])
                require(key[0]==r['x'] and key in indexed and key not in seen,'real unique same-column reference')
                require(route in indexed[key]['candidate_routes'],'route-specific reference')
                seen.add(key);references.add((key,route))
            if status=='identity_conflict':require(bool(refs),'conflict needs reference')
            if not(c|f) and refs:require(status=='identity_conflict','empty attributed conflict')
            if status=='no_attributable_cells':require(not(c|f) and not refs,'empty status loses material/conflict')
            require(not occupied.get(r['x'],set())&(c|f),'duplicate selected ink')
            occupied.setdefault(r['x'],set()).update(c|f)
    for key,b in indexed.items():
        require(all((key,r) in references for r in b['candidate_routes']),'each candidate retains reference')
    return by_column


def collect(path,expected,deps):
    """Follow declared JSON inputs relative to their own file, retaining conflicts."""
    path=path.resolve();name=os.path.relpath(path,HERE)
    require(pin(path)==expected,'dependency '+name)
    if name in deps:
        require(deps[name]==expected,'conflicting dependency '+name);return
    deps[name]=expected
    if path.suffix=='.json':
        data=json.loads(path.read_text())
        if isinstance(data,dict) and isinstance(data.get('inputs'),dict):
            for child,value in data['inputs'].items():
                collect(path.parent/child,value,deps)


def run(pair,reading_pins):
    region={'F5':'F5-Im3','F6':'F6-Im1'}[pair]
    h,v,a=helpers();deps={}
    for name in HELPERS:collect(HERE/name,pin(HERE/name),deps)
    for name in ('PROTOCOL.md','PROTOCOL-V2.md','READERS.md','CONSUMER-COMPATIBILITY.md','context01.json','context02.json','compare.py','test_compare.py'):
        collect(HERE/name,pin(HERE/name),deps)
    readings={};bands={};input_pins={}
    for role in ('primary','peer'):
        name=f'reader-{pair}-{role}.json';path=HERE/name
        input_pins[name]=pin(path)
        require(input_pins[name]['sha256']==reading_pins[role],'frozen reader hash')
        data=json.loads(path.read_text());readings[role]=data
        required={'PROTOCOL.md','PROTOCOL-V2.md','READERS.md','context01.json','context02.json','../../native-strips01/'+region.split('-')[1]+'.jpg'}
        require(required<=set(data['inputs']),'required reader dependencies')
        collect(path,input_pins[name],deps)
        script=HERE/f'reader-{pair}-{role}.py'
        collect(script,data['script_pin'],deps)
        require(load(script).build()==data,'literal expansion reproduction')
        bands[role]=validate(data,region,role,h,a)
    raw=(HERE/'context01.json').read_bytes()
    require(raw==(HERE/'context02.json').read_bytes(),'context repeat')
    ctx=json.loads(raw)
    require(ctx['target_boxes'][pair]==TARGETS[region] and ctx['context_boxes'][pair]==CONTEXTS[region],'context geometry')
    require(ctx['sources'][pair]==region.split('-')[1]+'.jpg' and ctx['source_size']==[741,88],'context source')
    pixels={(r['x'],r['y']):r['rgb'] for r in ctx['cells'][pair]}
    cx0,cy0,cx1,cy1=CONTEXTS[region]
    require(len(ctx['cells'][pair])==len(pixels)==(cx1-cx0)*(cy1-cy0),'context count')
    require(set(pixels)=={(x,y) for x in range(cx0,cx1) for y in range(cy0,cy1)},'context coordinates')
    routes=[]
    for route in ('solid','dash'):
        for r,s in zip(readings['primary']['routes'][route],readings['peer']['routes'][route]):
            routes.append({'route':route,'x':r['x'],'primary_original':r,'peer_original':s,'sets':h.comparison(r,s)})
    geometry=[]
    for x in range(TARGETS[region][0],TARGETS[region][2]):
        selections=[]
        for role in ('primary','peer'):
            rows=[readings[role]['routes'][r][x-TARGETS[region][0]] for r in ('solid','dash')]+bands[role].get(x,[])
            selections.append({label:sorted({y for r in rows for y in r[label]}) for label in ('core','fringe')})
        geometry.append({'x':x,'primary_unassigned_originals':bands['primary'].get(x,[]),
            'peer_unassigned_originals':bands['peer'].get(x,[]),'sets':h.comparison(*selections)})
    whites={role:[{'scope':scope,'class':label,'x':r['x'],'y':y}
        for scope,rs in list(d['routes'].items())+[('unassigned',d['unassigned_bands'])]
        for r in rs for label in ('core','fringe') for y in r[label]
        if pixels[r['x'],y]==[255,255,255]] for role,d in readings.items()}
    require(deps=={name:pin(HERE/name) for name in deps},'all dependencies unchanged')
    return {'status':'native_ink_reconciliation_not_physical_measurement','pair':pair,'region_id':region,
        'input_pins':input_pins,'dependencies':deps,'script_pin':pin(Path(__file__)),
        'test_pin':pin(HERE/'test_compare.py'),'literal_readings':readings,
        'literal_reproductions':{'primary':True,'peer':True},'route_comparisons':routes,
        'visible_ink_comparisons':geometry,'summary':{'routes':v.totals(routes),'visible_ink':v.totals(geometry),
        'status_different':sum(r['primary_original']['status']!=r['peer_original']['status'] for r in routes),
        'selected_exact_white_cells':whites},'human_accepted':False,'physical_support':None,
        'limits':['Original reader-local identities are not voted, averaged or equated.',
                  'The prospectively named force56_peer identity maps only to the peer role; original serialization remains intact.',
                  'Copied field adapter validates original statuses; originals remain intact.',
                  'All declared JSON inputs recursively pinned with normalized paths and conflict rejection.',
                  'Numerical agreement does not validate semantic attribution or original-curve containment.',
                  'No seam join, supported-domain union, physical envelope, human acceptance or cause finding.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pair',choices=['F5','F6'],required=True)
    p.add_argument('--primary-sha',required=True);p.add_argument('--peer-sha',required=True)
    p.add_argument('--run',choices=['01','02'],required=True);args=p.parse_args()
    result=run(args.pair,{'primary':args.primary_sha,'peer':args.peer_sha})
    target=HERE/f'comparison-{args.pair}-{args.run}.json'
    with target.open('x') as f:json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':pin(target),'summary':result['summary']}))
