"""Fixed approach reconciliation, preserving original annotations and disputes."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPERS = {
 '../force45/compare_force45.py':'932792f49797c4034beb1124d8174a56c911319e17fa536e199f0709950557be',
 '../force69/compare_force69.py':'f332359911f4d7bf5e768bf9e36b37ddb6995e857f6cf7ae5fa5456bb6dd4a6e',
}
TARGETS = {'E3-Im10':[195,35,365,92],'E4-Im10':[195,0,440,92]}
CONTEXTS = {'E3-Im10':[193,33,367,92],'E4-Im10':[193,0,442,92]}


def pin(path):
    raw=path.read_bytes()
    return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}


def require(ok,reason):
    if not ok: raise ValueError(reason)


def load_code(path):
    spec=importlib.util.spec_from_file_location(path.stem+'_'+path.parent.name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def rows(r):
    for key in ('core','fringe'):
        a=r[key]
        require(type(a) is list and all(type(y) is int and 0<=y<92 for y in a),'92-row bounds')
        require(a==sorted(set(a)),'sorted unique rows')
    c,f=set(r['core']),set(r['fringe'])
    require(not c&f,'class overlap')
    return c,f


def helpers():
    for name,sha in HELPERS.items():
        require(isinstance(sha,str) and pin(HERE/name)['sha256']==sha,'helper pin '+name)
    h=load_code(HERE/'../force45/compare_force45.py')
    h.rows=rows;h.TARGETS=TARGETS;h.CONTEXTS=CONTEXTS
    v=load_code(HERE/'../force69/compare_force69.py')
    return h,v


def adapted(data):
    """Field-name adapter on a deep copy, not a rewrite of preserved readers."""
    result=copy.deepcopy(data)
    require('source_image' not in result,'ambiguous source fields')
    result['source_image']=result['source']
    for records in list(result['routes'].values())+[result['unassigned_bands']]:
        for r in records:
            require('note' not in r and 'fragments' not in r,'ambiguous adapted fields')
            r['note']=r['reason'];r['fragments']=r['fragment_membership']
    # READERS permits the parent cell/status vocabulary for unassigned ink.
    # The older band validator requires identity_conflict for all material.
    # Validate the original local-ink status first, then adapt only this copy.
    # Band placement/candidate refs, not this remapping, express nonassignment.
    for r in result['unassigned_bands']:
        core,fringe=rows(r);status=r['status']
        require(status in ('identity_conflict','no_attributable_cells',
            'identified_local_fragment','boundary_truncated','fringe_only'),'band status vocabulary')
        if status=='no_attributable_cells':require(not(core|fringe),'nonempty empty band')
        if status=='identified_local_fragment':require(bool(core),'identified band without core')
        if status=='fringe_only':require(not core and bool(fringe),'fringe-only band classes')
        if status=='boundary_truncated':require(bool(core|fringe) and bool(r['boundary_flags']),'band truncation')
        r['status']='identity_conflict' if core|fringe else 'no_attributable_cells'
    return result


def coverage(data,region):
    cv=data['coverage'];x0,y0,x1,y1=CONTEXTS[region]
    if 'raw_blocks' in cv:
        require(cv['full_context_inspected'] is True,'uninspected context')
        blocks=[(*r['columns'],r['receipt']) for r in cv['raw_blocks']]
        count=cv['raw_context_cells']
    elif 'blocks_inclusive_and_receipt' in cv:
        require(cv['all_context_cells_actually_read'] is True and cv['uncompleted_context']==[],'uninspected context')
        require(cv['row_range_inclusive']==[y0,y1-1],'read rows')
        blocks=cv['blocks_inclusive_and_receipt'];count=cv['context_cell_count']
    elif 'read_receipts' in cv:
        require(cv['uncompleted_context_columns']==[] and cv['actual_complete_context_columns']==[x0,x1-1],'read columns')
        require(cv['actual_rows']==[y0,y1-1] and all(r['truncated'] is False for r in cv['read_receipts']),'read rows/truncation')
        blocks=[(r['first'],r['last'],r['exec_chunk_id']) for r in cv['read_receipts']];count=cv['context_cells']
    else:
        require(cv['actual_read'] is True and cv['uncompleted_context_columns']==[],'uninspected context')
        require(cv['context_columns_inclusive']==[x0,x1-1] and cv['context_rows_inclusive']==[y0,y1-1],'read bounds')
        blocks=cv['finite_untruncated_receipts'];count=cv['raw_context_cells']
    require(count==(x1-x0)*(y1-y0),'read cell count')
    require(all(type(a) is int and type(b) is int and a<=b and isinstance(r,str) and r for a,b,r in blocks),'read block record')
    require([x for a,b,_ in blocks for x in range(a,b+1)]==list(range(x0,x1)),'complete finite read coverage')


def validate(data,region,role,h,v):
    normalized=adapted(data);box=TARGETS[region]
    require(data['region_id']==region and data['pair']==region.split('-')[0] and data['source']=='Im10.jpg','region identity')
    require(data['reader']==role and data['target_box']==box and data['context_box']==CONTEXTS[region],'reader geometry')
    require(data['human_accepted'] is False and data['physical_support'] is None,'native-only boundary')
    require(set(data['routes'])=={'solid','dash'},'routes')
    coverage(data,region)
    indexed={};by_column={};occupied={};references=set()
    # The frozen old helper validates local rows, flags and exact membership.
    # The current contract allows MULTIPLE disjoint bands in a column, so do
    # not call its one-band-per-column index or silently collapse originals.
    for b,original in zip(normalized['unassigned_bands'],data['unassigned_bands']):
        h.flags(b,box);h.members(b);key=(b['x'],b['band_id']);c,f=rows(b)
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
            h.flags(r,box);h.members(r);c,f=rows(r);status=r['status']
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


def run(pair,reading_pins):
    region=pair+'-Im10';require(region in TARGETS,'pair')
    h,v=helpers();deps={name:pin(HERE/name) for name in HELPERS}
    readings={};inputs={};repeats={};bands={}
    for role in ('primary','peer'):
        name=f'reader-{pair}-{role}.json';path=HERE/name
        inputs[name]=pin(path)
        require(inputs[name]['sha256']==reading_pins[role],'frozen reader hash')
        data=json.loads(path.read_text());readings[role]=data
        require({'PROTOCOL.md','READERS.md','context01.json','context02.json',
                 '../../native-strips01/Im10.jpg'} <= set(data['inputs']),'required reader inputs')
        for filename,expected in data['inputs'].items():
            require(pin(HERE/filename)==expected,'reader dependency '+filename)
            deps[filename]=expected
        script=HERE/f'reader-{pair}-{role}.py'
        require(pin(script)==data['script_pin'],'literal script hash before import')
        deps[script.name]=pin(script)
        repeated=load_code(script).build()
        require(repeated==data,'literal expansion reproduction')
        repeats[role]=True
        bands[role]=validate(data,region,role,h,v)
    ctx_raw=(HERE/'context01.json').read_bytes()
    require(ctx_raw==(HERE/'context02.json').read_bytes(),'context repeat')
    ctx=json.loads(ctx_raw)
    require(ctx['target_boxes'][pair]==TARGETS[region] and ctx['context_boxes'][pair]==CONTEXTS[region],'context geometry')
    pixels={(r['x'],r['y']):r['rgb'] for r in ctx['cells'][pair]}
    x0,y0,x1,y1=CONTEXTS[region]
    require(len(ctx['cells'][pair])==len(pixels)==(x1-x0)*(y1-y0),'context count')
    require(set(pixels)=={(x,y) for x in range(x0,x1) for y in range(y0,y1)},'context coordinates')
    routes=[]
    for route in ('solid','dash'):
        for a,b in zip(readings['primary']['routes'][route],readings['peer']['routes'][route]):
            routes.append({'route':route,'x':a['x'],'primary_original':a,'peer_original':b,'sets':h.comparison(a,b)})
    x0,_,x1,_=TARGETS[region]
    geometry=[]
    for x in range(x0,x1):
        selections=[]
        for role in ('primary','peer'):
            records=[readings[role]['routes'][r][x-x0] for r in ('solid','dash')]+bands[role].get(x,[])
            selections.append({label:sorted({y for r in records for y in r[label]}) for label in ('core','fringe')})
        geometry.append({'x':x,'primary_unassigned_originals':bands['primary'].get(x,[]),
            'peer_unassigned_originals':bands['peer'].get(x,[]),'sets':h.comparison(*selections)})
    whites={}
    for role,data in readings.items():
        whites[role]=[{'scope':scope,'class':label,'x':r['x'],'y':y}
            for scope,rs in list(data['routes'].items())+[('unassigned',data['unassigned_bands'])]
            for r in rs for label in ('core','fringe') for y in r[label]
            if pixels[r['x'],y]==[255,255,255]]
    require(inputs=={n:pin(HERE/n) for n in inputs},'readers unchanged')
    require(deps=={n:pin(HERE/n) for n in deps},'dependencies unchanged')
    return {'status':'native_ink_reconciliation_not_physical_measurement','pair':pair,
       'region_id':region,'input_pins':inputs,'dependencies':deps,'script_pin':pin(Path(__file__)),
       'test_pin':pin(HERE/'test_compare.py'),'literal_readings':readings,
       'literal_reproductions':repeats,'route_comparisons':routes,'visible_ink_comparisons':geometry,
       'summary':{'routes':v.totals(routes),'visible_ink':v.totals(geometry),
          'status_different':sum(r['primary_original']['status']!=r['peer_original']['status'] for r in routes),
          'selected_exact_white_cells':whites},'human_accepted':False,'physical_support':None,
       'limits':['Original reader-local identities remain distinct; no voting or averaging.',
                 'Copy-only legacy schema adapter validates local band status before normalizing unassigned material to conflict; originals retain their statuses.',
                 'Multiple disjoint bands retain separate same-column IDs and route-specific references; no dictionary overwrite or forced band merger.',
                 'Matched RGB and set arithmetic do not authenticate historical curves.',
                 'No seam joins, support union, physical envelope, model discrepancy or human acceptance.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pair',choices=['E3','E4'],required=True)
    p.add_argument('--primary-sha',required=True);p.add_argument('--peer-sha',required=True)
    p.add_argument('--run',choices=['01','02'],required=True);args=p.parse_args()
    result=run(args.pair,{'primary':args.primary_sha,'peer':args.peer_sha})
    target=HERE/f'comparison-{args.pair}-{args.run}.json'
    with target.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'output':pin(target),'summary':result['summary']}))
