#!/usr/bin/env python3
"""Fresh typed CaseA/contact join; numeric source data only, no solver."""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import resource
import sys
import time
import unittest
import numpy as np

BASE = Path(__file__).resolve().parent
OLD = BASE.parent / 'c79-contact-geometry'
HELPER = BASE.parent / 'model-member-map/map_members.py'
HELPER_SHA = 'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'
PINS = {
    BASE/'PROTOCOL.md': 'b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41',
    OLD/'exact-proximity80.json': '25cb6d5a71a5d34908368523725cfe8612a4d8cf37de616220cf36e9663a4324',
    OLD/'exact-proximity80.npz': '79bbdc475b2680034096092e207bdd95250e4e7191ae4275ace4106e526c5628',
    OLD/'independent-exact-reference80-root01.json': '4f5e0576ea843cd1640c2cac17ece0f44491f8ca19d88b7b38c24f45a47eacb8',
    OLD/'stage-root01.json': 'deae7314c487b13e84302eb60b53bffb461f63d286f8d596b96a67377e631963',
    OLD/'stage-root01.npz': '2324c9a606dbbf45fc593c5a69bbfc05d7ca538aca3db04031970a109db35bcf',
    OLD/'contact-damage01.json': 'e43d8922c511debb4a004f6342fbdb8c16e76ff26cdb306fbd161c77a536d479',
    HELPER: HELPER_SHA,
}
SOURCE_IDS = {'discrete_mass.k.gz':119, 'elem_thick_to-renum.k.gz':120,
              'wtc7_global_8a_no-conn-matl.k.gz':121, 'G6A_CaseA_El_Delete_List.k.gz':117}
RAW_PINS = {
    117:(325983,45156,'a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25'),
    119:(508372,7905,'8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
    120:(232959541,4088491,'7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
    121:(333947423,7196443,'8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf'),
}

def require(ok, code):
    if not ok: raise ValueError(code)

def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

require(sha(HELPER)==HELPER_SHA,'helper_pin')
spec=importlib.util.spec_from_file_location('casea_frozen_mesh_reader',HELPER)
mesh=importlib.util.module_from_spec(spec); spec.loader.exec_module(mesh)

def check_pins():
    values={str(p.relative_to(BASE.parent)):sha(p) for p in PINS}
    require(all(values[str(p.relative_to(BASE.parent))]==h for p,h in PINS.items()),'dependency_pin')
    return values

def numbers(raw, widths):
    cells=mesh.fields(raw,widths)
    require(len(cells)<=len(widths),'too_many_csv_fields')
    return [mesh.number(v) for v in cells]+[None]*(len(widths)-len(cells))

def int_id(v, zero=False):
    require(v is not None and int(v)==v and (v>=0 if zero else v>0) and v<mesh.ID_CAP,'invalid_id')
    return int(v)

def casea_list(lines):
    header=None; members=[]; cards=[]; ended=False; key=None; keyline=None
    for line,raw in lines:
        s=raw.split(b'$',1)[0].strip()
        if not s: continue
        require(not ended,'CaseA_after_END')
        if s.startswith(b'*'):
            token=s.upper(); require(token in (b'*KEYWORD',b'*SET_SHELL_LIST',b'*END'),'CaseA_keyword')
            if token==b'*SET_SHELL_LIST': require(header is None and key!=token,'CaseA_duplicate_set')
            if token==b'*KEYWORD': require(key is None,'CaseA_misplaced_KEYWORD')
            key=token; keyline=line; ended=token==b'*END'; continue
        require(key==b'*SET_SHELL_LIST','CaseA_data_outside_set')
        vals=numbers(raw.split(b'$',1)[0],[10]*8)
        if header is None:
            require(vals[0]==1,'CaseA_set_id')
            header={'source':117,'set_id':1,'keyword_line':keyline,'header_line':line,'values':vals}
        else:
            cards.append({'line':line,'values':vals})
            for slot,v in enumerate(vals,1):
                if v in (0,None): continue
                members.append({'line':line,'slot':slot,'ordinal':len(members)+1,'eid':int_id(v)})
    require(header is not None and ended,'CaseA_incomplete')
    counts=Counter(r['eid'] for r in members)
    return {'header':header,'cards':cards,'members':members,'unique_ids':len(counts),
            'duplicate_ids':{str(k):v for k,v in sorted(counts.items()) if v>1},
            'zero_slots':sum(v==0 for r in cards for v in r['values']),
            'blank_slots':sum(v is None for r in cards for v in r['values'])}

class Reader(mesh.Reader):
    """Same pinned stream guard, with a fresh curve/discrete-card observer."""
    def __init__(self, targets):
        super().__init__(); self.targets=targets; self.curves={}; self.discretes=[]
    def curve(self,name,start,cards):
        require(cards,'curve_empty'); vals=numbers(cards[0][1],[10]*8); cid=int_id(vals[0])
        require(cid not in self.curves,'duplicate_curve')
        self.curves[cid]={'source':SOURCE_IDS[name],'keyword_line':start,'header_line':cards[0][0],
            'values':vals,'points':[{'line':n,'values':numbers(v,[20]*2)} for n,v in cards[1:]]}
    def lines(self,name):
        key=b''; start=0; cards=[]
        for line,raw in super().lines(name):
            require(b'\0' not in raw and raw.isascii(),'nonascii_or_NUL')
            s=raw.strip()
            if s and not s.startswith(b'$'):
                if s.startswith(b'*'):
                    if key==b'*DEFINE_CURVE': self.curve(name,start,cards)
                    key=s.upper(); start=line; cards=[]
                    require(not key.startswith(b'*DEFINE_CURVE') or key==b'*DEFINE_CURVE','curve_variant')
                elif key==b'*DEFINE_CURVE':
                    cards.append((line,raw)); require(len(cards)<=10000,'curve_cap')
                elif key==b'*ELEMENT_DISCRETE':
                    vals=numbers(raw,[8]*5+[16,8,16]); eid=int_id(vals[0])
                    if eid in self.targets:
                        self.discretes.append({'source':SOURCE_IDS[name],'line':line,'values':vals})
            yield line,raw
        if key==b'*DEFINE_CURVE': self.curve(name,start,cards)
        r=self.receipts[name]
        require((r['uncompressed_bytes'],r['lines'],r['uncompressed_sha256'])==RAW_PINS[SOURCE_IDS[name]],'uncompressed_pin')

class Collector(mesh.MemberMap):
    def __init__(self,reader,ids,targetnodes,masterids,cap=mesh.ID_CAP):
        self.reader=reader; self.ids=set(ids); self.targetnodes=set(targetnodes); self.masterids=set(masterids)
        self.cap=cap; self.seen={k:np.zeros(cap,dtype=bool) for k in ('shell','beam','discrete','solid')}
        self.nseen=np.zeros(cap,dtype=bool); self.nodes={}; self.shells=[]; self.masters={}
        self.counts=Counter(); self.node_counts=Counter(); self.cross=defaultdict(list); self.active_delete=[]
        self.parts={}; self.partsets={}; self.planes=[]; self.includes=[]; self.transforms=[]; self.materials={}; self.sections=set()
        self.selected_cards={}; self.spring_part_counts=Counter()
    def node(self,name,raw):
        vals=numbers(raw,[8,16,16,16,8,8]); nid=int_id(vals[0])
        require(nid<self.cap and not self.nseen[nid],'duplicate_or_out_of_scope_node')
        require(all(v is not None for v in vals[1:4]),'missing_coordinate')
        self.nseen[nid]=True; self.node_counts[str(SOURCE_IDS[name])]+=1
        if nid in self.targetnodes:
            self.nodes[nid]={'nid':nid,'source':SOURCE_IDS[name],'line':self.reader.line,'xyz':vals[1:4]}
    def element(self,name,line,kind,row,offset):
        eid,pid=row[:2]; int_id(eid); int_id(pid); require(eid<self.cap,'id_cap')
        require(not self.seen[kind][eid],'duplicate_typed_element'); self.seen[kind][eid]=True
        nodes=mesh.vertex_ids(kind,row)
        for pos,n in enumerate(nodes): int_id(n,zero=(kind=='discrete' and pos==1))
        self.counts[f'{SOURCE_IDS[name]}:{kind}']+=1
        if kind=='discrete' and pid+offset in (820,821,859): self.spring_part_counts[str(pid+offset)]+=1
        out={'source':SOURCE_IDS[name],'line':line,'kind':kind,'eid':eid,'original_pid':pid,'pid':pid+offset,'nodes':nodes}
        if eid in self.ids:
            if kind=='shell': self.shells.append(out)
            else: self.cross[kind].append(out)
        if kind=='shell' and eid in self.masterids: self.masters[eid]=out
    def metadata(self,name,key,start,cards,offset):
        super().metadata(name,key,start,cards,offset)
        if key not in (b'*PART',b'*SECTION_DISCRETE',b'*MAT_SPRING_NONLINEAR_ELASTIC'): return
        ncards=cards[1:] if key==b'*PART' else cards
        vals=[{'line':n,'values':numbers(v,[10]*8)} for n,v in ncards]
        require(vals,'empty_selected_metadata'); idx=int_id(vals[0]['values'][0])+offset
        if idx not in (820,821,859): return
        k=key.decode('ascii')+':'+str(idx); require(k not in self.selected_cards,'duplicate_selected_definition')
        self.selected_cards[k]={'source':SOURCE_IDS[name],'keyword':key.decode('ascii'),'keyword_line':start,
                               'offset':offset,'cards':vals}
    def flush(self): pass

def check_coordinates(actual,expected):
    require(actual.keys()==expected.keys(),'selected_coordinate_coverage')
    for n in expected: require(actual[n]==expected[n],'selected_coordinate_or_locator_mismatch')

def group_join(shells,pairs,masters,settings):
    bynode=defaultdict(list)
    for r in shells:
        for n in set(r['nodes']):
            if n: bynode[n].append(r['eid'])
    groups=[]; relations=[]
    for ei in range(len(settings)):
        for cid in (1,2):
            for cls in (0,2,3):
                rows=pairs[(pairs[:,0]==ei)&(masters[pairs[:,1],0]==cid)&(pairs[:,3]==cls)]
                matches=[]
                for row in rows:
                    for eid in bynode[int(row[2])]:
                        matches.append([ei,cid,cls,int(row[1]),int(row[2]),eid])
                relations.extend(matches)
                groups.append({'setting_index':ei,'cid':cid,'geometry_class':cls,'selected_nodes':sorted(set(map(int,rows[:,2]))),
                    'matching_nodes':sorted({r[4] for r in matches}),'matching_eids':sorted({r[5] for r in matches}),
                    'relation_count':len(matches)})
    return groups,sorted(relations)

def alias_check(segments,actual,listed):
    result=[]
    for mi,segment in enumerate(segments):
        for alias in segment['aliases']:
            require(alias['eid'] in actual,'master_alias_missing')
            r=actual[alias['eid']]
            require([r['source'],r['line'],r['pid'],r['original_pid'],r['nodes']]==
                    [alias['source'],alias['line'],alias['pid'],alias['original_pid'],alias['nodes']], 'master_alias_version')
            result.append({'master_index':mi,'eid':r['eid'],'source':r['source'],'line':r['line'],'listed':r['eid'] in listed})
    return result

class Tests(unittest.TestCase):
    def source(self,raw): return casea_list(enumerate(raw.splitlines(),1))
    def test_header_members_padding(self):
        r=self.source(b'*KEYWORD\n*SET_SHELL_LIST\n1\n7,0,,8,7\n*END')
        self.assertEqual([m['eid'] for m in r['members']],[7,8,7]); self.assertEqual(r['duplicate_ids'],{'7':2})
        self.assertEqual((r['zero_slots'],r['blank_slots']),(1,4)); self.assertEqual(r['header']['header_line'],3)
    def test_invalid_set(self):
        for raw in (b'*SET_SHELL_LIST\n2\n*END',b'*SET_SHELL_LIST\n1\n7.5\n*END',b'*SET_SHELL_LIST\n1\n*END\n8'):
            with self.assertRaises(ValueError): self.source(raw)
    def collector(self): return Collector(type('R',(),{'line':2})(),{7},{1},{7},100)
    def test_typed_collision_and_transform(self):
        m=self.collector(); m.element(mesh.MASTER,5,'shell',[7,3,1,2,3,3],1000);m.element(mesh.MASTER,8,'beam',[7,4,4,5,1],0)
        self.assertEqual(m.shells[0]['pid'],1003);self.assertEqual(m.cross['beam'][0]['nodes'],[4,5])
        with self.assertRaises(ValueError):m.element(mesh.MASTER,6,'shell',[7,3,1,2,3,3],0)
    def test_shell_pair(self):
        m=self.collector(); r=type('R',(),{'lines':lambda self,name:enumerate([b'*ELEMENT_SHELL_THICKNESS',b'7,3,1,2,3,3',b'.1,.1,.1,.1',b'*END'],1)})()
        m.mesh(r,mesh.MASTER);self.assertEqual(len(m.shells),1)
    def test_shell_missing(self):
        m=self.collector();r=type('R',(),{'lines':lambda self,name:enumerate([b'*ELEMENT_SHELL_THICKNESS',b'7,3,1,2,3,3',b'*END'],1)})()
        with self.assertRaises(mesh.CardError):m.mesh(r,mesh.MASTER)
    def test_join_zeros_unknown_orientation_and_identity(self):
        rows=[{'eid':7,'nodes':[1,1,2,3],'orientation':8},{'eid':8,'nodes':[9,0]}]
        pairs=np.array([[0,0,1,3,0,0],[0,0,8,0,0,0],[0,1,4,3,0,0]])
        groups,rels=group_join(rows,pairs,np.array([[1],[2]]),[1])
        self.assertEqual(len(groups),6);self.assertEqual(rels,[[0,1,3,0,1,7]])
        self.assertEqual(sum(g['relation_count']==0 for g in groups),5)
    def test_coordinate_guard(self):
        check_coordinates({1:[0,0,0]},{1:[0,0,0]})
        with self.assertRaises(ValueError):check_coordinates({1:[0,0,0]},{1:[1,0,0]})
        with self.assertRaises(ValueError):check_coordinates({},{1:[0,0,0]})
    def test_blank_csv(self):self.assertEqual(numbers(b'1,,0',[10]*4),[1,None,0,None])
    def test_duplicate_curve(self):
        r=Reader(set());r.curve(mesh.MASTER,1,[(2,b'1'),(3,b'0,0')])
        with self.assertRaises(ValueError):r.curve(mesh.MASTER,1,[(2,b'1')])
    def test_curve_forward_order(self):
        r=Reader(set());r.curve(mesh.OUTSIDE,5,[(6,b'2,,1,2,3,4'),(7,b'0,1')]);self.assertEqual(list(r.curves),[2])
    def test_alias_namespace(self):
        alias={'eid':7,'source':121,'line':1,'pid':3,'original_pid':3,'nodes':[1,2,3,3]}
        good={7:{**alias,'kind':'shell'}}
        self.assertTrue(alias_check([{'aliases':[alias]}],good,{7})[0]['listed'])
        good[7]['pid']=1003
        with self.assertRaises(ValueError):alias_check([{'aliases':[alias]}],good,{7})
    def test_pin_and_output_guard(self):
        with self.assertRaises(ValueError):require('a'=='b','pin')
        with self.assertRaises(ValueError):require(not BASE.exists(),'output_exists')

def controls():
    r=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    require(r.wasSuccessful(),'controls_failed');return {'count':r.testsRun,'failures':len(r.failures),'errors':len(r.errors)}

def calculate():
    require(json.loads((OLD/'independent-exact-reference80-root01.json').read_text())['status']=='PASS','exact_gate')
    stage=json.loads((OLD/'stage-root01.json').read_text())['result']
    with np.load(OLD/'exact-proximity80.npz',allow_pickle=False) as z:
        pairs=z['pairs'];masterids=z['master_identity'];settings=z['settings'];master_nodes=z['master_nodes']
    selected=set(map(int,pairs[np.isin(pairs[:,3],[0,2,3]),2]))|set(map(int,master_nodes.ravel()))
    with np.load(OLD/'stage-root01.npz',allow_pickle=False) as z:
        ids=z['node_ids']; ix=np.searchsorted(ids,sorted(selected)); require(np.array_equal(ids[ix],sorted(selected)),'stage_node_index')
        expected={int(n):{'nid':int(n),'source':int(loc[0]),'line':int(loc[1]),'xyz':xyz.tolist()}
                  for n,xyz,loc in zip(ids[ix],z['xyz'][ix],z['node_source_line'][ix])}
    prior=json.loads((OLD/'contact-damage01.json').read_text())['result']['matches']
    targets={r['eid'] for r in prior if r['actual_family']=='discrete'}
    reader=Reader(targets);listing=casea_list(reader.lines(mesh.CASEA));listed={r['eid'] for r in listing['members']}
    master_eids={a['eid'] for r in stage['master_segments'] for a in r['aliases']}
    collect=Collector(reader,listed,selected,master_eids)
    for name,offset in ((mesh.MASTER,0),(mesh.OUTSIDE,1000),(mesh.MASS,0)):
        collect.mesh(reader,name,offset)
    check_coordinates(collect.nodes,expected)
    groups,relations=group_join(collect.shells,pairs,masterids,settings)
    aliases=alias_check(stage['master_segments'],collect.masters,listed)
    actual={r['eid'] for r in collect.shells}
    require(len(reader.discretes)==len(targets) and {int(r['values'][0]) for r in reader.discretes}==targets,'spring_target_coverage')
    return {'casea':listing,'shells':sorted(collect.shells,key=lambda r:r['eid']),
        'unmatched_shell_ids':sorted(listed-actual),
        'cross_family':{k:sorted(collect.cross[k],key=lambda r:r['eid']) for k in ('beam','discrete','solid')},
        'selected_coordinates':[collect.nodes[n] for n in sorted(collect.nodes)],
        'source_element_counts':dict(sorted(collect.counts.items())),'source_node_counts':dict(sorted(collect.node_counts.items())),
        'groups':groups,'relations':relations,'relation_columns':['setting_index','cid','geometry_class','master_index','nid','eid'],
        'master_alias_membership':aliases,'sources':reader.receipts,'includes':collect.includes,'transforms':collect.transforms,
        'springs_numeric_inventory':{'target_elements':sorted(reader.discretes,key=lambda r:r['values'][0]),
            'selected_part_counts':dict(sorted(collect.spring_part_counts.items())),
            'selected_cards':collect.selected_cards,'curve_inventory':[dict(curve_id=k,**v) for k,v in sorted(reader.curves.items())]},
        'limits':['static_typed_incidence_not_activation','no_solver_execution_or_historical_identity',
                  'curve_inventory_not_yet_semantically_interpreted','selected_coordinate_version_check_only']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--controls',action='store_true');p.add_argument('--output');a=p.parse_args()
    if a.controls:print(json.dumps(controls()));return
    require(a.output is not None and re.fullmatch(r'casea-root[0-9]+\.json',a.output),'output_scope')
    out=BASE/a.output;require(not out.exists(),'output_exists');start=time.monotonic();before=check_pins();tests=controls()
    try:
        result=calculate(); after=check_pins();require(before==after,'changed_pins')
        receipt={'status':'PASS','code_sha256':sha(Path(__file__)),'command':sys.argv,'pins_before':before,'pins_after':after,
            'controls':tests,'elapsed_seconds':time.monotonic()-start,'maxrss_bytes_darwin':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'dependency_reuse':'Root-owned frozen MemberMap mesh/card stream; fresh CaseA collector and contact join. No new independent outputs read.',
            'result':result}
    except (ValueError,mesh.CardError,KeyError,IndexError,AssertionError) as e:
        receipt={'status':'FAIL','error_type':type(e).__name__,'error_code':e.code if isinstance(e,mesh.CardError) else str(e),
            'code_sha256':sha(Path(__file__)),'controls':tests,'pins_before':before,'elapsed_seconds':time.monotonic()-start}
    with out.open('x') as f:json.dump(receipt,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
    info={'status':receipt['status'],'output':out.name,'sha256':sha(out)}
    if receipt['status']=='PASS':info.update(shells=len(result['shells']),relations=len(result['relations']),master_hits=sum(r['listed'] for r in result['master_alias_membership']))
    else:info.update(error_code=receipt['error_code'])
    print(json.dumps(info));sys.exit(0 if receipt['status']=='PASS' else 1)

if __name__=='__main__':main()
