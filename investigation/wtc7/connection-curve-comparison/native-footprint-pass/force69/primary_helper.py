"""Bounded primary literal expansion for the six frozen force69 regions.

Only expands manually declared memberships. RGB is used solely to diagnose a
selected exact-white cell; it never selects, removes, or reassigns a cell.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'PROTOCOL.md': '558eb117125fc3df1458e2c153e3a9635b67ed931df15e9114c26b507e209ff7',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    'read_context.py': 'ee266545221eb4ed63faa04c59e48fbcd69571092621c38d3d57d84e67af6a90',
    'context01.json': 'ac65b18cb58bbe1e7f003163e2b8dde55baddc4c1ef061655e202caef2820cb1',
    'context02.json': 'ac65b18cb58bbe1e7f003163e2b8dde55baddc4c1ef061655e202caef2820cb1',
    '../../native-strips01/Im0.jpg': 'b5b279bbdc7de4c0be4165ac9bc70086c736cdca557859460da35a4c3406f1d4',
    '../../native-strips01/Im1.jpg': '929f5d00d2f9ab1eba27a4aad8af37320a4fd37f2455f9b51d750ec7e15e8139',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}

def pin(path):
    raw = Path(path).read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def parts(runs, x):
    result = []
    for first,last,core,fringe,name in runs:
        if type(first) is not int or type(last) is not int or first > last:
            raise ValueError('Literal column interval')
        if first <= x <= last:
            if not core and not fringe:
                raise ValueError('Empty literal fragment')
            result.append({'fragment_id':name,'core':core,'fringe':fringe})
    return result

def record(x, fragments, box, references, band=False, possible_routes=None):
    c = sorted(y for p in fragments for y in p['core'])
    f = sorted(y for p in fragments for y in p['fringe'])
    if c != sorted(set(c)) or f != sorted(set(f)) or set(c)&set(f):
        raise ValueError('Duplicate membership')
    if len({p['fragment_id'] for p in fragments}) != len(fragments):
        raise ValueError('Duplicate fragment ID within column')
    if any(type(y) is not int or not box[1] <= y < box[3] for y in c+f):
        raise ValueError('Row bounds')
    selected = c+f
    flags = [label for label,yes in [('target_left',x==box[0]),
             ('target_right',x==box[2]-1),('target_top',box[1] in selected),
             ('target_bottom',box[3]-1 in selected)] if selected and yes]
    if band:
        status = 'identity_conflict' if selected else 'no_attributable_cells'
        note = 'Manually retained unresolved material; possible route ownership is explicit per fragment. Stored once, without resolving crossings or fragment connectivity.'
    else:
        status = ('boundary_truncated' if flags else 'identified_local_fragment' if c else 'fringe_only') if selected else ('identity_conflict' if references else 'no_attributable_cells')
        note = 'Manual source-native local-style attribution. Core/fringe are subjective ink classes, not calibrated original-curve bounds. Empty means no attribution, not zero or absent physical support.'
    r = {'x':x,'core':c,'fringe':f,'fragment_id':fragments[0]['fragment_id'] if len(fragments)==1 else None,
         'fragments':fragments,'status':status,'boundary_flags':flags,'band_refs':references,'note':note}
    if band:
        r['band_id'] = 'unassigned-'+str(x) if selected else None
        r['possible_routes_by_fragment'] = possible_routes or {}
        r['candidate_routes'] = [name for name in ('solid','dash') if any(name in v for v in (possible_routes or {}).values())]
    return r

def build(spec, script):
    before = {k:pin(HERE/k) for k in EXPECTED}
    if any(before[k]['sha256'] != value for k,value in EXPECTED.items()):
        raise ValueError('Dependency changed')
    before['primary_helper.py'] = pin(__file__)
    raw = json.loads((HERE/'context01.json').read_text())
    rid = spec['region']; box = raw['target_boxes'][rid]
    pixels = {(r['x'],r['y']):r['rgb'] for r in raw['cells'][rid]}
    runs = spec['literal']; ownership = spec.get('ownership',{})
    routes = {'solid':[],'dash':[]}; bands = []
    for x in range(box[0],box[2]):
        u = parts(runs['unassigned'],x)
        own = {p['fragment_id']:ownership[p['fragment_id']] for p in u}
        if any(not set(value)<= {'solid','dash'} for value in own.values()):
            raise ValueError('Unresolved route ownership')
        b = record(x,u,box,[],True,own); bands.append(b)
        for route in routes:
            refs = [b['band_id']] if any(route in value for value in own.values()) else []
            r = record(x,parts(runs[route],x),box,refs)
            routes[route].append(r)
        selections = [set(r['core']+r['fringe']) for r in [routes['solid'][-1],routes['dash'][-1],b]]
        if selections[0]&selections[1] or selections[0]&selections[2] or selections[1]&selections[2]:
            raise ValueError('Duplicate attribution')
        for rows in selections:
            for y in rows:
                if pixels[x,y] == [255,255,255]:
                    raise ValueError(('Selected exact white',rid,x,y))
    if any(before[k] != pin(HERE/k) for k in before):
        raise ValueError('Dependency changed during expansion')
    return {'pair':rid.split('-')[0],'region_id':rid,'source_image':raw['sources'][rid],
      'reader':'primary','reader_agent':'force69_primary',
      'status':'frozen_manual_native_annotation_not_accepted_measurement',
      'target_box':box,'context_box':raw['context_boxes'][rid],'inputs':before,'script_pin':pin(script),
      'literal_instructions':runs,'unassigned_possible_routes':ownership,
      'coverage':spec['coverage'],'identity_basis':spec['identity_basis'],
      'independence':'Prior-informed AI primary designated before new force69 pixels. No peer selections or results inspected. Older F5 primary expansion code inspected only outside its selection literals.',
      'limits':'Native ink attribution only. No threshold selection, interpolation, original-curve containment, physical metric, cross-strip join, source authentication, human acceptance or cause result.',
      'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}

def save(spec,script,output):
    rid=spec['region']
    if output not in [f'reader-{rid}-primary.json',f'reader-{rid}-primary-repeat.json']:
        raise ValueError('Output name')
    result=build(spec,script)
    with (HERE/output).open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True,allow_nan=False); f.write('\n')
    print(json.dumps({'output':output,'pin':pin(HERE/output),'route_records':sum(map(len,result['routes'].values()))}))

def controls():
    p=parts([[2,3,[4],[5],'a'],[3,3,[7],[8],'b']],3)
    r=record(3,p,[2,4,4,9],[])
    assert r['core']==[4,7] and r['fringe']==[5,8] and r['fragment_id'] is None
    assert r['boundary_flags']==['target_right','target_top','target_bottom']
    assert parts([[2,3,[4],[],'a']],4)==[]
    for bad in [[[2,2,[4],[4],'a']],[[2,2,[True],[],'a']]]:
        try: record(2,parts(bad,2),[2,0,4,9],[])
        except ValueError: pass
        else: raise AssertionError('invalid membership accepted')
    b=record(2,[{'fragment_id':'u','core':[],'fringe':[4]}],[2,0,4,9],[],True,{'u':['dash']})
    assert b['band_id']=='unassigned-2' and b['possible_routes_by_fragment']=={'u':['dash']}
    print('primary helper synthetic literal/union/flags/ownership controls passed')

if __name__=='__main__': controls()
