from pathlib import Path
from fractions import Fraction as F
import hashlib, json, sys
N=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/multipoint-joint-consistency')
sys.path.insert(0,str(N/'oracle'))
import chain_oracle as q
seen={}
def data(path,pin=None):
    b=path.read_bytes()
    h=hashlib.sha256(b).hexdigest()
    if pin is not None: assert h==pin, path.name
    if path in seen: assert h==seen[path]
    seen[path]=h
    return b
root_bytes=data(N/'run01.json','1ef82cb48b3b688b35acafed4458873657eaf9d237678508b0d9ba7cb23fd86c')
assert root_bytes==data(N/'run02.json')
ours_bytes=data(N/'oracle/run01/results.json','9774f906fe3fc3f3f6fcd7462bd4b454acdfaee0e05a33c6cf3e0903964492a7')
assert ours_bytes==data(N/'oracle/run02/results.json')
data(N/'calculate.py','92c729a5c3cde640351551d0ce655545dc9069b8b19d61d1efcd9d59a1ef55a1')
data(N/'oracle/chain_oracle.py','0cb2814e9811ca384ea49df9c90c1089823fdcb6e534ea58cfea7484b424fedf')
for run in ('run01','run02'):
    p=N/'oracle'/run
    receipt=json.loads(data(p/'receipt.json'))
    assert receipt['pins_before']==receipt['pins_after']
    for path,item in receipt['pins_before'].items():
        b=data(Path(path),item['sha256'])
        assert len(b)==item['bytes']
    assert {f.name for f in p.iterdir()}==set(receipt['products'])|{'receipt.json'}
    for name,item in receipt['products'].items():
        b=data(p/name,item['sha256'])
        assert len(b)==item['bytes']
root=json.loads(root_bytes)
ours=json.loads(ours_bytes)
rows=json.loads(data(q.OLD/'transcription-independent/table47.json',q.PINS[q.OLD/'transcription-independent/table47.json']))['rows']
roots={(c['track'].upper(),F(c['span'])):c for c in root['cases']}
assert len(roots)==len(ours['cases'])==12
checks=[]; total_edges=0; root_witnesses=0; root_cycles=0; oracle_certificates=0
for oc in ours['cases']:
    point,span=oc['point'],F(oc['span'])
    rc=roots[(point,span)]
    bounds,links,unsupported=q.problem(rows,q.POINTS[point],span)
    assert rc['feasible']==oc['feasible']
    assert oc['position_count']==len(bounds)==len(rc['vertex_rows'])-1
    assert oc['velocity_constraints']==len(links)==len(rc['supported'])
    assert rc['unsupported']==[u['source_row'] for u in unsupported]
    assert oc['unsupported_velocities']==unsupported
    assert rc['vertex_rows']==[None]+[i+1 for i in sorted(bounds)]
    vertex={row:i for i,row in enumerate(rc['vertex_rows']) if row is not None}
    # Every producer edge independently reconstructed from the frozen alternate table.
    expected={}
    for i,(lo,hi) in bounds.items():
        row=i+1; v=vertex[row]
        expected[f'position:{row}:upper']=(0,v,hi)
        expected[f'position:{row}:lower']=(v,0,-lo)
    for e in links:
        row=e['center']+1; u=vertex[e['left']+1]; v=vertex[e['right']+1]
        expected[f'velocity:{row}:upper']=(u,v,e['hi'])
        expected[f'velocity:{row}:lower']=(v,u,-e['lo'])
    actual={e['label']:(e['u'],e['v'],F(e['bound'])) for e in rc['edges']}
    assert len(actual)==len(rc['edges'])==len(expected) and actual==expected
    assert rc['supported']==[{'row':e['center']+1,'previous_row':e['left']+1,
                              'following_row':e['right']+1,
                              'printed':rows[e['center']][q.POINTS[point]+'_v']} for e in links]
    assert {int(i):tuple(map(F,b)) for i,b in oc['position_bounds'].items()}==bounds
    assert [{**e,'lo':F(e['lo']),'hi':F(e['hi'])} for e in oc['difference_constraints']]==links
    total_edges+=len(actual)
    if rc['feasible']:
        assert len(rc['vertices'])==len(rc['vertex_rows']) and F(rc['vertices'][0])==0
        witness={row-1:F(rc['vertices'][i]) for i,row in enumerate(rc['vertex_rows']) if row is not None}
        q.validate_witness(bounds,links,witness)
        q.validate_witness(bounds,links,oc['witness'])
        root_witnesses+=1
    else:
        cycle=rc['cycle_edge_indices']; edges=rc['edges']
        assert cycle and all(type(i) is int and 0<=i<len(edges) for i in cycle)
        assert all(edges[a]['v']==edges[b]['u'] for a,b in zip(cycle,cycle[1:]+cycle[:1]))
        atoms=[]
        for i in cycle:
            kind,row,side=edges[i]['label'].split(':')
            atoms.append(('p' if kind=='position' else 'd')+f':{int(row)-1}:{side}')
        cert={'atoms':atoms,'sum_rhs':rc['cycle_bound_sum']}
        q.validate_certificate(bounds,links,cert)
        root_cycles+=1
        for chain in oc['chains']:
            if not chain['feasible']:
                q.validate_certificate(bounds,links,chain['contradiction']['certificate'])
                oracle_certificates+=1
    checks.append({'point':point,'span':str(span),'positions':len(bounds),
                   'supported':len(links),'unsupported':rc['unsupported'],
                   'feasible':rc['feasible'],'oracle_boundary_only':oc['boundary_only'],
                   'root_negative_cycle_sum':rc.get('cycle_bound_sum')})
for path,pin in seen.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
print(json.dumps({'status':'PASS','case_comparisons':len(checks),
                  'all_root_input_inequalities_reconstructed':total_edges,
                  'root_witnesses_checked_against_independent_inputs':root_witnesses,
                  'root_negative_cycles_checked_against_independent_inputs':root_cycles,
                  'oracle_contradiction_certificates_rechecked':oracle_certificates,
                  'captured_pins_rehashed_unchanged':len(seen),'cases':checks},indent=2,sort_keys=True))
