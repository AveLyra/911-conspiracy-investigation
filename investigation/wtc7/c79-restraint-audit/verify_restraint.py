#!/usr/bin/env python3
"""Independent typed extraction of a first shared-node neighborhood; no solver."""
from __future__ import annotations

import argparse
from array import array
from collections import Counter, defaultdict
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import resource
import sys
import time

import numpy as np

BASE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PROTOCOL_PIN = 'b7bcdf096a31ffca12a5c25f0f34cf2cc3247018502c9d6320a315f90f61d72d'
PRIOR_READER = BASE.parent / 'model-member-map/verify_member_map.py'
PRIOR_PIN = 'de7ee2aa5f4a2aedd4a9446561322aa5e14e688d1c72a57aa96e593df1f148cc'
PINS = {
    119: ('discrete_mass.k.gz', 70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7', 508372, '8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
    120: ('elem_thick_to-renum.k.gz', 23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59', 232959541, '7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
    121: ('wtc7_global_8a_no-conn-matl.k.gz', 47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d', 333947423, '8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf'),
}
INCLUDE_IDS = {v[0][:-3]: k for k, v in PINS.items()}
INCLUDE_IDS['WTC7_CaseB_400pm.int'] = 118  # Record, never follow this thermal include.
CAP, LINE_CAP, MEMORY_CAP = 512 * 1024**2, 65536, 768 * 1024**2
NUM = re.compile(r'^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[EeDd][+-]?[0-9]+)?$')
INTEGER = re.compile(r'^[+-]?[0-9]+$')
GEOMETRY = {'ELEMENT_SHELL_THICKNESS': 'shell', 'ELEMENT_BEAM': 'beam',
            'ELEMENT_DISCRETE': 'discrete', 'ELEMENT_SOLID': 'solid'}
DEFINITIONS = {'MAT_PIECEWISE_LINEAR_PLASTICITY', 'MAT_PLASTICITY_COMPRESSION_TENSION',
               'MAT_RIGID', 'MAT_ELASTIC', 'MAT_ELASTIC_VISCOPLASTIC_THERMAL',
               'MAT_SPRING_NONLINEAR_ELASTIC', 'SECTION_BEAM', 'SECTION_SHELL',
               'SECTION_SOLID', 'SECTION_DISCRETE', 'HOURGLASS'}
KNOWN = set(GEOMETRY) | DEFINITIONS | {'NODE', 'PART', 'SET_PART_LIST',
         'DATABASE_CROSS_SECTION_PLANE_ID', 'INCLUDE', 'INCLUDE_TRANSFORM'}
PROGRESS = []


class AuditError(Exception):
    def __init__(self, code, source=0, line=0):
        self.code, self.source, self.line = code, source, line
        super().__init__(code)


def require(condition, code, source=0, line=0):
    if not condition:
        raise AuditError(code, source, line)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def peak_memory():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)


def scalar(token, integer=False):
    token = token.strip()
    require(bool((INTEGER if integer else NUM).fullmatch(token)), 'nonnumeric_field')
    value = int(token) if integer else float(token.replace('d', 'e').replace('D', 'E'))
    require(integer or math.isfinite(value), 'nonfinite_field')
    return value


def fields(line, widths, ints=(), required=0):
    """Own prior reader's fixed/free numeric-card method; blanks stay None."""
    s = line.split('$', 1)[0].rstrip('\r\n')
    if ',' in s:
        tokens = s.split(',')
        require(len(tokens) <= len(widths), 'extra_fields')
    else:
        require(not s[sum(widths):].strip(), 'fixed_card_overflow')
        starts = [0]
        for width in widths:
            starts.append(starts[-1] + width)
        tokens = [s[starts[i]:starts[i + 1]] for i in range(len(widths))]
        if not all(not t.strip() or (INTEGER if i in ints else NUM).fullmatch(t.strip())
                   for i, t in enumerate(tokens)):
            tokens = s.split()
            require(required <= len(tokens) <= len(widths), 'free_card_length')
    require(len(tokens) >= required and all(t.strip() for t in tokens[:required]), 'missing_required_field')
    tokens += [''] * (len(widths) - len(tokens))
    return [None if not t.strip() else scalar(t, i in ints) for i, t in enumerate(tokens)]


def zeroed(values):
    return [0 if x is None else x for x in values]


def column_label(heading):
    clean = ' '.join(heading.strip().lower().split())
    m = re.fullmatch(r'col(?:umn)?[ _-]*([0-9]+)(?:[ _-]+x[ _-]*sect(?:ion)?)?', clean)
    return int(m.group(1)) if m else None


class Stream:
    """Hash every byte; expose only selected typed numeric events."""
    def __init__(self, source, binary, phase):
        self.source, self.binary, self.phase = source, binary, phase
        self.stats = {'source': source, 'phase': phase, 'bytes': 0, 'lines': 0, 'eof': False}
        if source in PINS:
            PROGRESS.append(self.stats)

    def events(self):
        name, keyword_line, index, pending = None, 0, 0, None
        counts, unknown = Counter(), Counter()
        digest = hashlib.sha256()
        while True:
            raw = self.binary.readline(LINE_CAP + 1)
            if not raw:
                require(pending is None, 'missing_element_continuation', self.source, self.stats['lines'])
                self.stats.update(eof=True, sha256=digest.hexdigest(), keywords=dict(counts), unknown_keyword_hash_counts=dict(unknown))
                return
            self.stats['lines'] += 1
            line = self.stats['lines']
            self.stats['bytes'] += len(raw)
            require(len(raw) <= LINE_CAP and self.stats['bytes'] <= CAP and b'\0' not in raw,
                    'stream_cap_or_nul', self.source, line)
            if line % 100000 == 0:
                require(peak_memory() <= MEMORY_CAP, 'memory_cap', self.source, line)
            digest.update(raw)
            try:
                text = raw.decode('ascii')
            except UnicodeDecodeError:
                raise AuditError('nonascii_source', self.source, line) from None
            s = text.strip()
            meaningful_blank = (name == 'PART' and index == 0) or (name == 'DATABASE_CROSS_SECTION_PLANE_ID' and index == 2)
            if s.startswith('$') or (not s and not meaningful_blank):
                continue
            if s.startswith('*'):
                require(pending is None, 'missing_element_continuation', self.source, line)
                token = s[1:].split('$', 1)[0].strip().upper()
                if token.startswith(('ELEMENT_', 'PART_', 'NODE_')) and token not in KNOWN:
                    raise AuditError('unsupported_geometry_or_part_variant', self.source, line)
                if token.startswith(('MAT_', 'SECTION_', 'INCLUDE', 'SET_PART')) and token not in KNOWN:
                    raise AuditError('unsupported_reference_variant', self.source, line)
                if token.startswith('KEYWORD') and token != 'KEYWORD':
                    raise AuditError('unsupported_global_format', self.source, line)
                name = token if token in KNOWN else None
                if name:
                    counts[name] += 1
                else:
                    unknown[hashlib.sha256(token.encode('ascii')).hexdigest()] += 1
                keyword_line, index = line, 0
                continue
            if name is None:
                continue
            i, index = index, index + 1
            try:
                if name == 'NODE' and self.phase == 'metadata_nodes':
                    yield 'node', line, fields(text, [8,16,16,16,8,8], [0], 4)
                elif name in GEOMETRY and self.phase != 'metadata_nodes':
                    kind = GEOMETRY[name]
                    if kind == 'shell':
                        if pending is None:
                            v = fields(text, [8]*10, range(10), 6)
                            require(not any(zeroed(v[6:])), 'higher_order_shell')
                            pending = (line, v)
                        else:
                            thickness = fields(text, [16]*5, (), 4)
                            yield kind, pending[0], {'card':pending[1], 'continuation_line':line, 'thickness':thickness}
                            pending = None
                    elif kind == 'beam':
                        yield kind, line, {'card':fields(text, [8]*10, range(10), 4)}
                    elif kind == 'discrete':
                        yield kind, line, {'card':fields(text, [8]*5+[16,8,16], [0,1,2,3,4,6], 4)}
                    else:
                        clean = text.split('$',1)[0].rstrip()
                        used = len(clean.split(',')) if ',' in clean else len(clean.split())
                        if pending is not None:
                            nodes = fields(text, [8]*10, range(10), 4)
                            require(not any(zeroed(nodes[8:])), 'ten_node_solid')
                            yield kind, pending[0], {'card':pending[1]+nodes[:8], 'continuation_line':line}
                            pending = None
                        elif used == 2:
                            pending = (line, fields(text, [8]*2, range(2), 2))
                        else:
                            yield kind, line, {'card':fields(text, [8]*10, range(10), 10)}
                elif self.phase == 'metadata_nodes':
                    if name == 'PART':
                        if i == 0:
                            continue
                        require(i == 1, 'extra_part_card')
                        yield 'part', line, {'keyword_line':keyword_line,'card':fields(text,[10]*8,range(8),3)}
                    elif name in DEFINITIONS and i == 0:
                        first = text.split(',')[0] if ',' in text else text[:10]
                        yield 'definition', line, {'keyword':name,'id':scalar(first,True),'keyword_line':keyword_line}
                    elif name == 'SET_PART_LIST':
                        if i == 0:
                            set_id = fields(text,[10]*8,[0],1)[0]
                            yield 'set', line, {'id':set_id,'keyword_line':keyword_line}
                        else:
                            yield 'set_members', line, {'id':set_id,'members':[x for x in fields(text,[10]*8,range(8),1) if x not in (None,0)]}
                    elif name == 'DATABASE_CROSS_SECTION_PLANE_ID':
                        if i == 0:
                            first, heading = text.split(',',1) if ',' in text else (text[:10],text[10:])
                            yield 'plane', line, {'id':scalar(first,True),'column':column_label(heading),
                                'keyword_line':keyword_line,'heading_sha256':hashlib.sha256(heading.strip().encode()).hexdigest()}
                        elif i in (1,2):
                            v=fields(text,[10]*8,[0] if i==1 else [5,6],0)
                            require(i==1 or v[7] is None,'unused_plane_slot')
                            yield 'plane_card',line,{'index':i,'card':v}
                        else:
                            raise AuditError('extra_plane_card')
                    elif name in ('INCLUDE','INCLUDE_TRANSFORM'):
                        if i==0:
                            require(s in INCLUDE_IDS,'unallowlisted_include')
                            yield 'include',line,{'keyword':name,'keyword_line':keyword_line,'target_source':INCLUDE_IDS[s]}
                        else:
                            require(name=='INCLUDE_TRANSFORM' and i<=4,'extra_transform_card')
                            n=7 if i==1 else 1 if i in (2,4) else 5
                            yield 'transform',line,{'index':i,'card':fields(text,[10]*n,range(n) if i!=3 else [],1)}
            except AuditError as e:
                raise AuditError(e.code,self.source,line) from None


def source_events(source, phase):
    with gzip.open(SOURCE/PINS[source][0],'rb') as f:
        stream=Stream(source,f,phase)
        yield from stream.events()
        pin=PINS[source]
        require(stream.stats['eof'] and stream.stats['bytes']==pin[3] and stream.stats['sha256']==pin[4],
                'decompressed_pin',source)


class Nodes:
    def __init__(self, ids, xyz, sources, lines):
        a=np.asarray(ids,dtype=np.int64)
        order=np.argsort(a)
        self.ids=a[order]
        self.xyz=np.asarray(xyz,dtype=np.float64).reshape(-1,3)[order]
        self.sources=np.asarray(sources,dtype=np.int32)[order]
        self.lines=np.asarray(lines,dtype=np.int64)[order]
        require(len(a)>0 and np.all(self.ids>0),'empty_or_invalid_nodes')
        require(not np.any(self.ids[1:]==self.ids[:-1]),'duplicate_node_id')

    def get(self, nid):
        i=int(np.searchsorted(self.ids,nid))
        require(i<len(self.ids) and int(self.ids[i])==nid,'missing_node')
        return {'id':nid,'source':int(self.sources[i]),'line':int(self.lines[i]),'xyz':self.xyz[i].tolist()}


def physical(kind, card):
    """Preserve order/repeats; zero is not a physical node."""
    stop=6 if kind=='shell' else 10 if kind=='solid' else 4
    return [n for n in card[2:stop] if n not in (None,0)]


def part_namespace(source, pid):
    require(pid>0,'nonpositive_part')
    return pid+(1000 if source==120 else 0)


def element(source,line,kind,raw):
    v=raw['card']
    require(v[0]>0,'nonpositive_element',source,line)
    vertices=physical(kind,v)
    require(vertices and all(n>0 for n in vertices),'invalid_physical_nodes',source,line)
    return {'source':source,'line':line,'kind':kind,'id':v[0],
            'original_part':v[1],'effective_part':part_namespace(source,v[1]),
            'physical_nodes':vertices,'orientation_node':v[4] if kind=='beam' else None,
            'connectivity_card':v,'continuation_line':raw.get('continuation_line'),
            'thickness_card':raw.get('thickness')}


def shared(element_record, seed_parts, seed_nodes):
    if element_record['effective_part'] in seed_parts:
        return []
    return sorted(set(element_record['physical_nodes']) & seed_nodes)


def enrich(record, nodes, seed_nodes):
    record=dict(record)
    record['coordinates']=[nodes.get(n)['xyz'] for n in record['physical_nodes']]
    record['matched_seed_nodes']=sorted(set(record['physical_nodes']) & seed_nodes)
    return record


def extract():
    ids,xyz,sources,lines=array('q'),array('d'),array('i'),array('q')
    parts,sets,definitions={}, {}, defaultdict(list)
    planes,includes=[],[]
    for src in (119,120,121):
        for kind,line,v in source_events(src,'metadata_nodes'):
            if kind=='node':
                ids.append(v[0]);xyz.extend(v[1:4]);sources.append(src);lines.append(line)
            elif kind=='part':
                card=v['card'];pid=part_namespace(src,card[0]);off=1000 if src==120 else 0
                require(pid not in parts,'duplicate_part',src,line)
                parts[pid]={'source':src,'line':line,**v,'effective_part':pid,
                            'effective_section':card[1]+off,'effective_material':card[2]+off}
            elif kind=='definition':
                off=1000 if src==120 else 0
                family='material' if v['keyword'].startswith('MAT_') else 'section' if v['keyword'].startswith('SECTION_') else 'hourglass'
                definitions[(family,v['id']+off)].append({'source':src,'line':line,**v,'effective_id':v['id']+off})
            elif kind=='set':
                key=(src,v['id']);require(key not in sets,'duplicate_part_set',src,line)
                sets[key]={'source':src,'line':line,**v,'members':[],'member_rows':[]}
            elif kind=='set_members':
                key=(src,v['id']);require(key in sets,'missing_set_header',src,line)
                sets[key]['members'].extend(v['members']);sets[key]['member_rows'].append({'line':line,'ids':v['members']})
            elif kind=='plane':
                planes.append({'source':src,'line':line,**v,'cards':[]})
            elif kind=='plane_card':
                require(planes and planes[-1]['source']==src,'missing_plane_header',src,line)
                planes[-1]['cards'].append({'line':line,**v})
            elif kind=='include':
                includes.append({'source':src,'line':line,**v,'transform_cards':[]})
            elif kind=='transform':
                require(includes and includes[-1]['keyword']=='INCLUDE_TRANSFORM','missing_transform_include',src,line)
                includes[-1]['transform_cards'].append({'line':line,**v})
    transformed=[i for i in includes if i['keyword']=='INCLUDE_TRANSFORM']
    require(len(transformed)==1 and transformed[0]['target_source']==120,'transform_target')
    require([c['card'] for c in transformed[0]['transform_cards']]==
            [[0,0,1000,1000,0,0,0],[1000],[1.,1.,1.,1.,0.],[0]],'transform_metadata')
    require(sorted(i['target_source'] for i in includes)==[118,119,120],'active_include_graph')
    selected_planes=[p for p in planes if p['column']==79]
    require(len(selected_planes)==1,'column_diagnostic_ambiguity')
    plane=selected_planes[0]
    require(len(plane['cards'])==2,'plane_card_count')
    psid=plane['cards'][0]['card'][0]
    require((plane['source'],psid) in sets,'missing_diagnostic_part_set')
    part_set=sets[(plane['source'],psid)]
    require(len(part_set['members'])==len(set(part_set['members'])),'duplicate_part_set_member')
    seed_parts=set(part_set['members'])
    require(seed_parts and seed_parts<=parts.keys(),'missing_seed_part')
    nodes=Nodes(ids,xyz,sources,lines)
    del ids,xyz,sources,lines
    seeds,seed_nodes=[],set()
    coverage=defaultdict(Counter)
    element_ids=defaultdict(lambda:array('q'))
    for src in (119,120,121):
        for kind,line,raw in source_events(src,'seed_elements'):
            if kind not in GEOMETRY.values():
                continue
            e=element(src,line,kind,raw)
            element_ids[kind].append(e['id']);coverage[src][kind]+=1
            if e['effective_part'] in seed_parts:
                seeds.append(e);seed_nodes.update(e['physical_nodes'])
    require(seeds and seed_nodes,'empty_seed_geometry')
    for kind,values in element_ids.items():
        a=np.sort(np.asarray(values,dtype=np.int64))
        require(not np.any(a[1:]==a[:-1]),'duplicate_element_id_by_family')
    del element_ids
    neighbors=[]
    second_coverage=defaultdict(Counter)
    orientation_only=0
    for src in (119,120,121):
        for kind,line,raw in source_events(src,'neighbor_elements'):
            if kind not in GEOMETRY.values():
                continue
            e=element(src,line,kind,raw);second_coverage[src][kind]+=1
            matched=shared(e,seed_parts,seed_nodes)
            if matched:
                neighbors.append(e)
            elif e['effective_part'] not in seed_parts and kind=='beam' and e['orientation_node'] in seed_nodes:
                orientation_only+=1
    require(coverage==second_coverage,'element_pass_coverage_changed')
    all_selected=seeds+neighbors
    selected_ids=sorted(set(n for e in all_selected for n in e['physical_nodes']))
    selected_nodes=[nodes.get(n) for n in selected_ids]
    seeds=[enrich(e,nodes,seed_nodes) for e in seeds]
    neighbors=[enrich(e,nodes,seed_nodes) for e in neighbors]
    selected_parts=sorted(set(e['effective_part'] for e in all_selected))
    references=[]
    for pid in selected_parts:
        if pid not in parts:
            references.append({'effective_part':pid,'status':'missing_part_definition'})
        else:
            p=dict(parts[pid]);p['status']='supplied_part_definition'
            for family,key in [('section','effective_section'),('material','effective_material')]:
                defs=definitions[(family,p[key])]
                p[family+'_definitions']=defs
                p[family+'_status']='resolved' if len(defs)==1 else 'missing' if not defs else 'ambiguous'
            references.append(p)
    seed_xyz=[nodes.get(n)['xyz'] for n in sorted(seed_nodes)]
    bbox=[[min(x[i] for x in seed_xyz),max(x[i] for x in seed_xyz)] for i in range(3)]
    return {'diagnostic':plane,'part_set':part_set,'seed_parts':sorted(seed_parts),
            'seed_nodes':sorted(seed_nodes),'seed_coordinate_bounds_by_axis':bbox,
            'seed_elements':seeds,'neighbor_elements':neighbors,'selected_nodes':selected_nodes,
            'incident_part_references':references,'include_graph':includes,
            'coverage':{str(k):dict(v) for k,v in coverage.items()},
            'counts':{'all_input_nodes':len(nodes.ids),'seed_elements':len(seeds),'seed_nodes':len(seed_nodes),
                      'neighbor_elements':len(neighbors),'selected_coordinate_nodes':len(selected_nodes),
                      'seed_parts':len(seed_parts),'incident_parts_including_seed':len(selected_parts),
                      'orientation_only_beams_excluded':orientation_only},
            'scope':'Exact first shared-node graph only. No coincident-node matching, restraint stiffness, directional/story/unit assignment, thermal or damage reads, solver or historical state.'}


def controls():
    passed=[]
    def ok(name,condition):
        require(condition,'control_'+name);passed.append({'name':name,'status':'PASS'})
    def reject(name,fun):
        try:fun()
        except AuditError:passed.append({'name':name,'status':'PASS'});return
        raise AuditError('control_no_rejection_'+name)
    def e(kind,card,src=121):return element(src,1,kind,{'card':card})
    seed={1,2};parts={179}
    b=e('beam',[10,98,3,4,1,0,0,0,0,0])
    ok('beam_orientation_not_endpoint',physical('beam',b['connectivity_card'])==[3,4] and shared(b,parts,seed)==[])
    b=e('beam',[11,98,1,4,3,0,0,0,0,0])
    ok('actual_endpoint_incidence',shared(b,parts,seed)==[1])
    shell=e('shell',[12,98,1,2,2,1,0,0,0,0])
    ok('ordered_repeated_vertices_unique_matches',shell['physical_nodes']==[1,2,2,1] and shared(shell,parts,seed)==[1,2])
    n=Nodes([1,2,3],[0.,0.,0., 1.,0.,0., 0.,0.,0.],[121]*3,[10,11,12])
    ok('coincident_distinct_id_not_edge',n.get(1)['xyz']==n.get(3)['xyz'] and shared(e('beam',[13,98,3,2,0]),parts,{1})==[])
    ok('outside_part_namespace_not_seed',part_namespace(120,179)==1179 and shared(e('beam',[14,179,1,2,0],120),parts,seed)==[1,2])
    ok('seed_part_excluded_from_neighbors',shared(e('beam',[15,179,1,2,0]),parts,seed)==[])
    ok('no_neighbor_empty',shared(e('beam',[16,98,3,4,0]),parts,seed)==[])
    ok('ground_discrete_omitted',physical('discrete',[17,1,1,0,999])==[1])
    reject('missing_node',lambda:n.get(99))
    reject('duplicate_node',lambda:Nodes([1,1],[0.]*6,[121]*2,[1,2]))
    reject('missing_required_card',lambda:fields('1,2,3',[8]*10,range(10),6))
    raw=b'*ELEMENT_SHELL_THICKNESS\n1,179,1,2,3,3,0,0,0,0\n0.5,0.6,0.7,0.8\n*END\n'
    stream=Stream(0,io.BytesIO(raw),'seed_elements');rows=list(stream.events())
    ok('shell_thickness_two_cards',len(rows)==1 and rows[0][1]==2 and rows[0][2]['continuation_line']==3 and rows[0][2]['thickness']==[.5,.6,.7,.8,None] and stream.stats['eof'])
    reject('missing_shell_continuation',lambda:list(Stream(0,io.BytesIO(b'*ELEMENT_SHELL_THICKNESS\n1,179,1,2,3,3\n*END\n'),'seed_elements').events()))
    ok('column_label_not_identifier',column_label('Col79 x-sect')==79 and column_label('79') is None)
    # Output preservation is tested without any filesystem mutation.
    reject('existing_output_guard',lambda:require(not Path(__file__).exists(),'output_exists'))
    return passed


def pin_inputs():
    pins={}
    for src,p in PINS.items():
        path=SOURCE/p[0];got=sha(path)
        require(path.stat().st_size==p[1] and got==p[2],'source_pin',src)
        pins[str(src)]={'bytes':p[1],'sha256':got}
    require(sha(BASE/'PROTOCOL.md')==PROTOCOL_PIN,'protocol_pin')
    require(sha(PRIOR_READER)==PRIOR_PIN,'prior_reader_pin')
    pins['protocol']=PROTOCOL_PIN;pins['prior_reader']=PRIOR_PIN;pins['code']=sha(Path(__file__))
    return pins


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output')
    ap.add_argument('--selftest',action='store_true')
    args=ap.parse_args()
    if args.selftest:
        print(json.dumps({'status':'PASS','controls':controls()}));return 0
    if not args.output or Path(args.output).name!=args.output or not args.output.endswith('.json'):
        ap.error('create-only JSON basename required')
    destination=BASE/args.output
    require(not destination.exists(),'output_exists')
    start=time.monotonic();tests=controls();before=pin_inputs()
    try:
        result=extract()
        status='PASS';error=None
    except AuditError as exc:
        result=None;status='FAIL';error={'code':exc.code,'source':exc.source,'line':exc.line}
    after=pin_inputs();require(before==after,'pins_changed')
    require(peak_memory()<=MEMORY_CAP,'memory_cap')
    receipt={'status':status,'error':error,'controls':tests,'pins_before':before,'pins_after':after,
             'streams':PROGRESS,'elapsed_seconds':time.monotonic()-start,'peak_rss_bytes':peak_memory(),
             'python':sys.version,'numpy':np.__version__,'command':[sys.executable,*sys.argv],
             'independence':'Own prior numeric-card semantics adapted; new stream selector and shared-node graph. Protocol/prior knowledge acknowledged. New root code/results not accessed before this output freeze.'}
    with destination.open('x',encoding='utf-8') as f:
        json.dump({'receipt':receipt,'result':result},f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'status':status,'sha256':sha(destination),'counts':result['counts'] if result else None,
                      'error':error,'controls':len(tests),'elapsed_seconds':receipt['elapsed_seconds'],'peak_rss_bytes':receipt['peak_rss_bytes']}))
    return 0 if status=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except AuditError as exc:
        print(json.dumps({'status':'FAIL','code':exc.code,'source':exc.source,'line':exc.line}));raise SystemExit(1)
