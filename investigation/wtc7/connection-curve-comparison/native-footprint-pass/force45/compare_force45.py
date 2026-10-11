"""Region-specific reader set reconciliation, not physical curve comparison."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = {'F4-Im4':[330,0,425,88], 'F5-Im4':[375,0,475,88], 'F5-Im2':[225,50,350,88]}
CONTEXTS = {'F4-Im4':[328,0,427,88], 'F5-Im4':[373,0,477,88], 'F5-Im2':[223,48,352,88]}
ROLES = ('primary','peer')


def require(ok, reason):
    if not ok: raise ValueError(reason)


def pin(path):
    raw = path.read_bytes()
    return {'sha256':hashlib.sha256(raw).hexdigest(), 'bytes':len(raw)}


def rows(r):
    for key in ('core','fringe'):
        a = r[key]
        require(type(a) is list and all(type(y) is int and 0 <= y < 88 for y in a), 'row type/range')
        require(a == sorted(set(a)), 'sorted unique rows')
    c,f = set(r['core']),set(r['fringe'])
    require(not c&f, 'class overlap')
    return c,f


def members(r):
    c,f = rows(r)
    fid = r['fragment_id']
    if 'fragments' not in r:
        require(not(c|f) or (isinstance(fid,str) and bool(fid)), 'selected fragment identity')
        require(bool(c|f) or fid is None, 'empty fragment identity')
        return
    parts = r['fragments']
    require(type(parts) is list, 'fragment list')
    ids = set(); seen = set(); core = set(); fringe = set()
    for part in parts:
        pc,pf = rows(part); name = part['fragment_id']
        require(isinstance(name,str) and name and name not in ids, 'unique fragment identity')
        require(bool(pc|pf) and not seen&(pc|pf), 'nonempty disjoint pieces')
        ids.add(name); seen |= pc|pf; core |= pc; fringe |= pf
    require(c==core and f==fringe, 'exact membership union')
    require(fid == (parts[0]['fragment_id'] if len(parts)==1 else None), 'outer fragment identity')


def flags(r,box):
    c,f = rows(r); x = r['x']; x0,y0,x1,y1 = box
    require(type(x) is int and x0 <= x < x1, 'column type/bounds')
    require(all(y0 <= y < y1 for y in c|f), 'target row bounds')
    expected = []
    if c|f:
        expected = [label for label,yes in [('target_left',x==x0),('target_right',x==x1-1),
                    ('target_top',y0 in c|f),('target_bottom',y1-1 in c|f)] if yes]
    require(r['boundary_flags']==expected, 'selected-cell boundary flags')


def validate(data,region=None,role=None):
    rid = data['region_id']
    require(rid in TARGETS and (region is None or rid==region), 'exact region identity')
    require(data['pair']==rid.split('-')[0] and data['source_image']==rid.split('-')[1]+'.jpg', 'pair/source identity')
    require(data['reader'] in ROLES and (role is None or data['reader']==role), 'reader role')
    box = data['target_box']
    require(type(box) is list and all(type(n) is int for n in box) and box==TARGETS[rid], 'target box')
    cb = data['context_box']
    require(type(cb) is list and all(type(n) is int for n in cb) and cb==CONTEXTS[rid], 'context box')
    require(data['human_accepted'] is False and data['physical_support'] is None, 'unaccepted native data')
    require(set(data['routes'])=={'solid','dash'}, 'routes')
    x0,y0,x1,y1 = box
    bands = {}; refs = set(); previous = x0-1
    for b in data['unassigned_bands']:
        x = b['x']; flags(b,box); members(b)
        require(isinstance(b.get('note'),str) and bool(b['note'].strip()), 'band reason')
        require(x > previous, 'band order/duplicates'); previous = x
        bid = b.get('band_id',b['fragment_id'])
        c,f = rows(b)
        require(not(c|f) or (isinstance(bid,str) and bool(bid)), 'band identity')
        require(b['status'] in ('identity_conflict','no_attributable_cells'), 'band status')
        require(b['status']!='no_attributable_cells' or not(c|f), 'nonempty unassigned empty status')
        bands[x] = b
        if bid is not None and c|f: refs.add((x,bid))
    for route,records in data['routes'].items():
        require([r['x'] for r in records]==list(range(x0,x1)), 'complete route columns')
        for r in records:
            flags(r,box); members(r); c,f = rows(r); status = r['status']
            require(isinstance(r.get('note'),str) and bool(r['note'].strip()), 'route reason')
            require(status in ('identified_local_fragment','boundary_truncated','fringe_only','identity_conflict','no_attributable_cells'), 'status')
            if status=='no_attributable_cells': require(not(c|f), 'nonempty empty status')
            if status=='identified_local_fragment': require(bool(c), 'identified without core')
            if status=='fringe_only': require(not c and bool(f), 'fringe-only classes')
            if status=='boundary_truncated': require(bool(c|f) and bool(r['boundary_flags']), 'truncation')
            require(not('band_refs' in r and 'unassigned_band_refs' in r), 'ambiguous reference schema')
            references = r.get('band_refs',r.get('unassigned_band_refs',[]))
            require(type(references) is list, 'references list')
            for reference in references:
                key = (r['x'],reference) if isinstance(reference,str) else (reference['x'],reference['band_id'])
                require(type(key[0]) is int and key[0]==r['x'] and key in refs, 'real same-column band reference')
            if r['x'] in bands:
                bc,bf = rows(bands[r['x']]); require(not(c|f)&(bc|bf), 'model/unassigned overlap')
    for a,b in zip(data['routes']['solid'],data['routes']['dash']):
        ac,af = rows(a); bc,bf = rows(b)
        require(not(ac|af)&(bc|bf), 'duplicate model ink')
    return bands


def operations(a,b):
    return {'intersection':sorted(a&b),'union':sorted(a|b),'primary_only':sorted(a-b),
            'peer_only':sorted(b-a),'symmetric_difference':sorted(a^b)}


def comparison(a,b):
    ac,af = rows(a); bc,bf = rows(b)
    return {k:operations(x,y) for k,x,y in [('core',ac,bc),('fringe',af,bf),('outer',ac|af,bc|bf)]}


def visible_geometry(data,bands,x0,x1):
    result = []
    for x in range(x0,x1):
        selections = []
        for role in ROLES:
            rs = [data[role]['routes'][k][x-x0] for k in ('solid','dash')]
            if x in bands[role]: rs.append(bands[role][x])
            selections.append({key:sorted({y for r in rs for y in r[key]}) for key in ('core','fringe')})
        result.append({'x':x,'primary_unassigned_original':bands['primary'].get(x),
                       'peer_unassigned_original':bands['peer'].get(x),'sets':comparison(*selections)})
    return result


def run(region,reading_pins):
    require(region in TARGETS and set(reading_pins)==set(ROLES), 'region and explicit roles')
    names = {role:f'reader-{region}-{role}.json' for role in ROLES}
    reading_bytes = {role:(HERE/name).read_bytes() for role,name in names.items()}
    data = {role:json.loads(raw) for role,raw in reading_bytes.items()}
    before = {names[role]:{'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
              for role,raw in reading_bytes.items()}
    deps = {}
    for role,d in data.items():
        require(before[names[role]]['sha256']==reading_pins[role], 'frozen reading changed')
        declared = d['inputs']
        source = '../../native-strips01/'+region.split('-')[1]+'.jpg'
        require({'PROTOCOL.md','context01.json','context02.json',source} <= set(declared), 'required dependency pins')
        for name,value in declared.items():
            current = pin(HERE/name)
            require(current['sha256']==value['sha256'] and current['bytes']==value['bytes'], 'dependency pin '+name)
            deps[name] = current
        script = f'reader-{region}-{role}.py'
        require(pin(HERE/script)==d['script_pin'], 'reader script pin')
        deps[script] = pin(HERE/script)
        if 'expander_pin' in d:
            helper = 'reader-F4-Im4-peer.py'
            require(pin(HERE/helper)==d['expander_pin'], 'shared expander pin')
            deps[helper] = pin(HERE/helper)
    bands = {role:validate(data[role],region,role) for role in ROLES}
    comparisons = []
    for route in ('solid','dash'):
        for a,b in zip(data['primary']['routes'][route],data['peer']['routes'][route]):
            comparisons.append({'route':route,'x':a['x'],'primary_original':a,'peer_original':b,'sets':comparison(a,b)})
    x0,y0,x1,y1 = TARGETS[region]
    geometry = visible_geometry(data,bands,x0,x1)
    raw = json.loads((HERE/'context01.json').read_text())
    require(raw['target_boxes'][region]==TARGETS[region] and raw['context_boxes'][region]==CONTEXTS[region], 'context geometry')
    require(raw['sources'][region]==data['primary']['source_image'] and raw['pairs'][region]==data['primary']['pair'], 'context source identity')
    records = raw['cells'][region]
    pixels = {(r['x'],r['y']):r['rgb'] for r in records}
    cx0,cy0,cx1,cy1 = CONTEXTS[region]
    require(len(records)==len(pixels)==(cx1-cx0)*(cy1-cy0), 'complete unique context')
    require(set(pixels)=={(x,y) for x in range(cx0,cx1) for y in range(cy0,cy1)}, 'context coordinate set')
    white = {}
    for role,d in data.items():
        white[role] = []
        for scope,rs in list(d['routes'].items())+[('unassigned',d['unassigned_bands'])]:
            for r in rs:
                for label in ('core','fringe'):
                    for y in r[label]:
                        if pixels[r['x'],y]==[255,255,255]:
                            white[role].append({'scope':scope,'class':label,'x':r['x'],'y':y})
    def totals(rs):
        return {'entries':len(rs),'outer_different':sum(bool(r['sets']['outer']['symmetric_difference']) for r in rs),
                'class_different':sum(bool(r['sets']['core']['symmetric_difference'] or r['sets']['fringe']['symmetric_difference']) for r in rs)}
    require(before=={name:pin(HERE/name) for name in before}, 'reading changed')
    require(deps=={name:pin(HERE/name) for name in deps}, 'dependency changed')
    return {'status':'comparison_preserves_disagreement_not_physical_measurement','region_id':region,
            'pair':data['primary']['pair'],'source_image':data['primary']['source_image'],
            'input_pins':before,'dependencies':deps,'script_pin':pin(Path(__file__)),
            'test_pin':pin(HERE/'test_compare_force45.py'),'literal_readings':data,
            'route_comparisons':comparisons,'visible_ink_comparisons':geometry,
            'summary':{'routes':totals(comparisons),'visible_ink':totals(geometry),
                'route_status_different':sum(r['primary_original']['status']!=r['peer_original']['status'] for r in comparisons),
                'selected_exact_white_cells':white},
            'reviewer_independence':'Comparator author is primary F4 reader; producer check, not independent verification.',
            'limits':'Reader differences only. Original records retained; local IDs not equated; missing versus empty preserved. No cross-region coordinate fusion, curve containment, physical support, model accuracy or causal finding.',
            'human_accepted':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--region',choices=list(TARGETS),required=True)
    p.add_argument('--primary-sha',required=True); p.add_argument('--peer-sha',required=True)
    p.add_argument('--output',required=True)
    args = p.parse_args()
    require(args.output in [f'comparison-{args.region}-01.json',f'comparison-{args.region}-02.json'], 'output name')
    value = run(args.region,{'primary':args.primary_sha,'peer':args.peer_sha})
    out = HERE/args.output
    with out.open('x') as f:
        json.dump(value,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'output':pin(out),'summary':value['summary']}))
