#!/usr/bin/env python3
"""Selected contact populations and supplied mesh properties; no contact solver."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import unittest
import numpy as np

BASE = Path(__file__).resolve().parent
PRIOR = BASE.parent / 'c79-restraint-audit'
HELPER = BASE.parent / 'model-member-map/map_members.py'
HELPER_SHA = 'f63356778c544e4102aef34d9c92a49707315be4db5ae182fcee1cce5557720b'
CONTACT_SHA = '04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859'
assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == HELPER_SHA
spec = importlib.util.spec_from_file_location('pinned_mesh_geometry_helper', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
FILES = ((m.MASTER, 0, 121), (m.OUTSIDE, 1000, 120), (m.MASS, 0, 119))
SOURCE_IDS = {name: sid for name, _, sid in FILES}
KINDS = {'shell': 0, 'beam': 1, 'discrete': 2, 'solid': 3}


def padded(raw, width=10, count=8):
    row = m.values_card(raw, width, count)
    m.require(len(row) <= count, 'card_width')
    return row + [None] * (count-len(row))


def set_members(lines):
    active = None
    header = None
    ended = False
    headers, node_rows, segment_rows = {}, [], []
    for line, raw in lines:
        s = raw.strip()
        if s.startswith(b'$'):
            continue
        m.require(not ended or not s, 'post_end_data')
        if s.startswith(b'*'):
            active = s.upper()
            if active.startswith(b'*SET_NODE'):
                m.require(active == b'*SET_NODE_LIST', 'unsupported_nodeset')
            if active.startswith(b'*SET_SEGMENT'):
                m.require(active == b'*SET_SEGMENT', 'unsupported_segmentset')
            header = None
            keyword_line = line
            ended = active == b'*END'
            continue
        if active not in (b'*SET_NODE_LIST', b'*SET_SEGMENT') or not s:
            continue
        v = padded(raw)
        if header is None:
            m.require(v[0] is not None and int(v[0]) == v[0], 'set_header_ID')
            header = int(v[0])
            selected = (active == b'*SET_NODE_LIST' and header == 1) or (active == b'*SET_SEGMENT' and header == 2)
            if selected:
                key = 'node1' if header == 1 else 'segment2'
                m.require(key not in headers, 'duplicate_selected_set')
                headers[key] = {'keyword_line': keyword_line, 'header_line': line, 'values': v}
            continue
        if active == b'*SET_NODE_LIST' and header == 1:
            ids = [m.integer(str(x).encode(), 0) if x is not None else 0 for x in v]
            m.require(all(0 <= x < m.ID_CAP for x in ids), 'node_member_range')
            node_rows.append([line, *ids])
        elif active == b'*SET_SEGMENT' and header == 2:
            m.require(all(x is not None and x > 0 and int(x) == x and x < m.ID_CAP for x in v[:4]), 'segment_member_range')
            segment_rows.append((line, [int(x) for x in v[:4]], v[4:]))
    return headers, node_rows, segment_rows


class TrackingReader(m.Reader):
    def lines(self, name):
        for line, raw in super().lines(name):
            self.raw = raw
            self.current_line = line
            yield line, raw


def incidence_updates(kind, nodes, thickness):
    distinct = list(dict.fromkeys(n for n in nodes if n))
    samples = list(zip(nodes, thickness[:4])) if kind == 'shell' else []
    return distinct, samples


class Mesh(m.MemberMap):
    def __init__(self, target_ids, master_faces):
        self.cap = m.ID_CAP
        self.present = np.zeros(self.cap, dtype=bool)
        self.used = np.zeros(self.cap, dtype=bool)
        self.seen = {k: np.zeros(self.cap, dtype=bool) for k in KINDS}
        self.ids = np.asarray(sorted(target_ids), dtype=np.int64)
        self.index = {int(n): i for i, n in enumerate(self.ids)}
        size = len(self.ids)
        self.xyz_selected = np.full((size, 3), np.nan)
        self.node_locations = np.zeros((size, 2), dtype=np.int64)
        self.incidence_counts = np.zeros((size, 4), dtype=np.int64)
        self.thickness_min = np.full(size, np.inf)
        self.thickness_max = np.full(size, -np.inf)
        self.thickness_count = np.zeros(size, dtype=np.int64)
        self.thickness_zero = np.zeros(size, dtype=np.int64)
        self.part_incidence = Counter()
        self.counts, self.node_counts = {}, {}
        self.parts, self.partsets, self.planes = {}, {}, []
        self.includes, self.transforms, self.active_delete = [], [], []
        self.materials, self.sections = {}, set()
        self.section_shell_cards = {}
        self.aliases = {tuple(sorted(set(face))): [] for face in master_faces}
        self.reader = None

    def flush(self):
        pass

    def node(self, name, raw):
        row = m.fields(raw, [8, 16, 16, 16, 8, 8])
        nid = m.integer(row[0]); self.check_id(nid)
        xyz = [m.number(v) for v in row[1:4]]
        m.require(all(v is not None for v in xyz), 'missing_coordinate')
        m.require(not self.present[nid], 'duplicate_node')
        self.present[nid] = True
        self.node_counts[name] = self.node_counts.get(name, 0) + 1
        if nid in self.index:
            i = self.index[nid]
            self.xyz_selected[i] = xyz
            self.node_locations[i] = [SOURCE_IDS[name], self.reader.current_line]

    def element(self, name, line, kind, row, offset):
        eid, original_pid = row[:2]
        self.check_id(eid)
        m.require(not self.seen[kind][eid], 'duplicate_element')
        self.seen[kind][eid] = True
        key = name + ':' + kind
        self.counts[key] = self.counts.get(key, 0) + 1
        nodes = list(m.vertex_ids(kind, row))
        m.require(all(0 < n < self.cap for n in nodes), 'element_node_range')
        self.used[nodes] = True
        thickness = padded(self.reader.raw, 16, 5) if kind == 'shell' else []
        vertices, samples = incidence_updates(kind, nodes, thickness)
        pid = original_pid + offset
        for n in vertices:
            if n in self.index:
                i = self.index[n]
                self.incidence_counts[i, KINDS[kind]] += 1
                self.part_incidence[(n, KINDS[kind], pid)] += 1
        for n, value in samples:
            if n in self.index:
                m.require(value is not None and value >= 0, 'invalid_corner_thickness')
                i = self.index[n]
                self.thickness_min[i] = min(self.thickness_min[i], value)
                self.thickness_max[i] = max(self.thickness_max[i], value)
                self.thickness_count[i] += 1
                self.thickness_zero[i] += value == 0
        face = tuple(sorted(set(nodes)))
        if kind == 'shell' and face in self.aliases:
            self.aliases[face].append({'source': SOURCE_IDS[name], 'line': line, 'eid': eid,
                'original_pid': original_pid, 'pid': pid, 'nodes': nodes,
                'thickness_line': self.reader.current_line, 'thickness_card': thickness})

    def metadata(self, name, keyword, start, cards, offset):
        super().metadata(name, keyword, start, cards, offset)
        if keyword == b'*SECTION_SHELL':
            sid = m.integer(m.fields(cards[0][1], [10]*8)[0]) + offset
            m.require(sid not in self.section_shell_cards, 'duplicate_shell_section')
            self.section_shell_cards[sid] = {'source': SOURCE_IDS[name], 'keyword_line': start,
                'cards': [{'line': line, 'values': padded(raw)} for line, raw in cards]}


class Controls(unittest.TestCase):
    def test_header_and_fixed_members(self):
        h, n, s = set_members(enumerate([b'*SET_NODE_LIST', b'1,0,0,0,0', b'3,3,4', b'*SET_SEGMENT', b'2', b'1,2,3,3,7,8,9,10', b'*END'], 1))
        self.assertEqual(n[0][1:4], [3,3,4]); self.assertEqual(h['node1']['header_line'], 2)
        self.assertEqual(s[0][1], [1,2,3,3]); self.assertEqual(s[0][2], [7,8,9,10])

    def test_unknown_variant(self):
        with self.assertRaises(m.CardError): set_members(enumerate([b'*SET_NODE_GENERAL'], 1))

    def test_post_end(self):
        with self.assertRaises(m.CardError): set_members(enumerate([b'*END', b'1'], 1))

    def test_partial_card_and_null(self):
        self.assertEqual(padded(b'1,2,',16,5), [1,2,None,None,None])

    def test_incidence_vs_corner_and_fifth(self):
        nodes, samples = incidence_updates('shell', [1,2,3,3], [2,3,4,5,99])
        self.assertEqual(nodes, [1,2,3]); self.assertEqual(samples, [(1,2),(2,3),(3,4),(3,5)])

    def test_orientation_not_endpoint(self):
        self.assertEqual(m.vertex_ids('beam', [9,1,2,3,888]), [2,3])

    def test_namespace_and_face_order(self):
        self.assertNotEqual([1,2,3,4], [4,3,2,1])
        self.assertEqual(tuple(sorted(set([1,2,3,4]))), tuple(sorted(set([4,3,2,1]))))
        self.assertNotEqual(179, 179+1000)

    def tiny_mesh(self):
        mesh = Mesh({1,2,3,4}, [[1,2,3,3], [1,2,3,4]])
        mesh.reader = TrackingReader()
        mesh.reader.raw = b'2,3,4,5,99'
        mesh.reader.current_line = 20
        return mesh

    def test_actual_shell_incidence_alias_and_thickness_slots(self):
        mesh = self.tiny_mesh()
        mesh.element(m.OUTSIDE,19,'shell',[10,2,1,2,3,3],1000)
        i = mesh.index[3]
        self.assertEqual(mesh.incidence_counts[i].tolist(),[1,0,0,0])
        self.assertEqual([mesh.thickness_min[i],mesh.thickness_max[i],mesh.thickness_count[i]],[4,5,2])
        self.assertEqual(mesh.part_incidence[(3,0,1002)],1)
        alias = mesh.aliases[(1,2,3)][0]
        self.assertEqual((alias['source'],alias['pid'],alias['line'],alias['thickness_line']),(120,1002,19,20))
        self.assertEqual(alias['thickness_card'],[2,3,4,5,99])
        self.assertEqual(mesh.aliases[(1,2,3,4)],[])

    def test_actual_beam_orientation_and_duplicate_family(self):
        mesh = self.tiny_mesh()
        mesh.element(m.MASTER,1,'beam',[10,2,1,2,3],0)
        self.assertEqual(mesh.incidence_counts[mesh.index[3]].sum(),0)
        with self.assertRaises(m.CardError):mesh.element(m.MASTER,2,'beam',[10,2,1,2,3],0)
        mesh.element(m.MASTER,3,'discrete',[10,2,1,0],0)
        self.assertEqual(mesh.incidence_counts[mesh.index[1]].tolist(),[0,1,1,0])

    def test_actual_node_locator_and_duplicate(self):
        mesh = self.tiny_mesh()
        mesh.node(m.MASTER,b'1,2,3,4,0,0')
        self.assertEqual(mesh.xyz_selected[mesh.index[1]].tolist(),[2,3,4])
        self.assertEqual(mesh.node_locations[mesh.index[1]].tolist(),[121,20])
        with self.assertRaises(m.CardError):mesh.node(m.MASTER,b'1,2,3,4,0,0')
        with self.assertRaises(m.CardError):mesh.node(m.MASTER,b'2,2,,4,0,0')

    def test_missing_reference_condition_and_blank_thickness(self):
        mesh = self.tiny_mesh()
        mesh.element(m.MASTER,1,'beam',[10,2,1,2,3],0)
        self.assertFalse(np.all(mesh.present[mesh.used]))
        mesh.reader.raw=b'2,,4,5,0'
        with self.assertRaises(m.CardError):mesh.element(m.MASTER,3,'shell',[10,2,1,2,3,4],0)


def run(output):
    m.require(output.parent.resolve() == BASE and output.suffix == '.json' and not output.exists(), 'fresh_output_required')
    archive = output.with_suffix('.npz')
    m.require(not archive.exists(), 'fresh_array_output_required')
    start = time.monotonic()
    before = {'helper': m.digest(HELPER), 'contacts': m.digest(PRIOR/'contacts-root01.json'),
              'protocol': m.digest(BASE/'PROTOCOL.md'), 'producer': m.digest(Path(__file__))}
    m.require(before['contacts'] == CONTACT_SHA and before['helper'] == HELPER_SHA, 'dependency_pin')
    test = unittest.TestResult(); unittest.defaultTestLoader.loadTestsFromTestCase(Controls).run(test)
    m.require(test.wasSuccessful(), 'controls_failed')
    receipt = {'status': 'running', 'pins': before, 'controls': {'run': test.testsRun, 'failures': len(test.failures), 'errors': len(test.errors)},
               'python': sys.version.split()[0], 'numpy': np.__version__, 'sources': {}}
    readers = []
    try:
        prior = json.loads((PRIOR/'contacts-root01.json').read_text())['result']
        masters = {s['sid']: s['selected'] for s in prior['sets'] if s['kind']=='segment' and s['sid'] in (1,3)}
        first = m.Reader(); readers.append(first)
        headers, node_rows, segment_rows = {}, [], []
        for name, _, src in FILES:
            h, n, s = set_members(first.lines(name))
            m.require(not h or src == 121, 'selected_sets_wrong_source')
            for key, value in h.items():
                m.require(key not in headers, 'duplicate_set_across_sources'); headers[key] = {'source':src, **value}
            node_rows.extend(n); segment_rows.extend(s)
            print('set_source_complete:'+str(src), flush=True)
        m.require(set(headers) == {'node1','segment2'}, 'missing_selected_set')
        group1 = {n for row in node_rows for n in row[1:] if n}
        group2 = {n for _, nodes, _ in segment_rows for n in nodes}
        master_nodes = {sid:{n for r in rows for n in r['nodes']} for sid,rows in masters.items()}
        targets = group1 | group2 | master_nodes[1] | master_nodes[3]
        mapper = Mesh(targets, [r['nodes'] for rows in masters.values() for r in rows])
        second = TrackingReader(); readers.append(second); mapper.reader = second
        for name, offset, src in FILES:
            mapper.mesh(second, name, offset); print('mesh_source_complete:'+str(src), flush=True)
        m.require(np.all(mapper.present[mapper.used]), 'undefined_element_nodes')
        m.require(np.isfinite(mapper.xyz_selected).all(), 'missing_selected_coordinates')
        m.require(not mapper.active_delete, 'unexpected_active_deletion')
        rows = []
        for sid, selected in masters.items():
            for r in selected:
                aliases = mapper.aliases[tuple(sorted(set(r['nodes'])))]; indices=[mapper.index[n] for n in r['nodes']]
                rows.append({'set_id':sid, 'line':r['line'], 'nodes':r['nodes'], 'attributes':r['attributes'],
                    'xyz':mapper.xyz_selected[indices].tolist(),
                    'aliases':[{**a, 'ordered_match':a['nodes']==r['nodes']} for a in aliases]})
        usedparts = {pid for _,_,pid in mapper.part_incidence}
        partrefs = []
        for pid in sorted(usedparts):
            p = mapper.parts.get(pid)
            partrefs.append({'pid':pid, 'part':p, 'section_defined':p is not None and p['section_id'] in mapper.sections,
                'material_keyword':mapper.materials.get(p['material_id']) if p else None,
                'section_shell':mapper.section_shell_cards.get(p['section_id']) if p else None})
        tmin=mapper.thickness_min.copy(); tmax=mapper.thickness_max.copy()
        tmin[mapper.thickness_count==0]=np.nan; tmax[mapper.thickness_count==0]=np.nan
        arrays={'node_ids':mapper.ids, 'node_source_line':mapper.node_locations, 'xyz':mapper.xyz_selected,
            'roles':np.asarray([[n in group1,n in group2,n in master_nodes[1],n in master_nodes[3]] for n in mapper.ids],dtype=np.uint8),
            'incidence_counts':mapper.incidence_counts, 'corner_thickness_min_max':np.column_stack([tmin,tmax]),
            'corner_thickness_count_zero':np.column_stack([mapper.thickness_count,mapper.thickness_zero]),
            'node_part_incidence':np.asarray([[n,k,p,c] for (n,k,p),c in sorted(mapper.part_incidence.items())],dtype=np.int64),
            'nodeset1_rows':np.asarray(node_rows,dtype=np.int64),
            'segmentset2_rows':np.asarray([[line,*nodes] for line,nodes,_ in segment_rows],dtype=np.int64),
            'segmentset2_attributes':np.asarray([[np.nan if x is None else x for x in attrs] for _,_,attrs in segment_rows])}
        populations=[]
        for cid, group in [(1,group1),(2,group2)]:
            ix=np.asarray([mapper.index[n] for n in sorted(group)])
            has=mapper.thickness_count[ix]>0
            populations.append({'cid':cid, 'nodes':len(group), 'nodes_without_shell_incidence':int(np.sum(~has)),
                'nodes_with_unequal_corner_thickness':int(np.sum(tmin[ix][has]!=tmax[ix][has])),
                'supplied_corner_thickness_min':float(np.min(tmin[ix][has])) if has.any() else None,
                'supplied_corner_thickness_max':float(np.max(tmax[ix][has])) if has.any() else None,
                'element_node_incidence_by_kind':mapper.incidence_counts[ix].sum(axis=0).tolist()})
        with archive.open('xb') as stream: np.savez_compressed(stream, **arrays)
        receipt.update(status='complete', result={'headers':headers, 'slave_populations':populations,
            'master_segments':rows, 'part_references':partrefs, 'all_element_counts':mapper.counts,
            'all_node_counts':mapper.node_counts, 'unique_model_nodes':int(mapper.present.sum()),
            'include_graph':mapper.includes, 'transforms':mapper.transforms,
            'arrays':{key:{'shape':list(v.shape),'dtype':str(v.dtype),'sha256':hashlib.sha256(v.tobytes(order='C')).hexdigest()} for key,v in arrays.items()},
            'array_archive':archive.name, 'array_archive_sha256':m.digest(archive),
            'array_schema':{'roles':['CID1_slave','CID2_slave','SEG1_master','SEG3_master'],
                'kind_codes':KINDS, 'node_part_incidence':['node','kind','effective_part','unique_element_count'],
                'thickness_NaN':'no supplied shell-corner incidence or blank segment attribute; not zero stiffness'},
            'scope':'selected input geometry and supplied thickness, no proximity selection or initialized pairs'})
    except Exception as exc:
        receipt.update(status='failed', error=exc.code if isinstance(exc,m.CardError) else 'unexpected_'+type(exc).__name__)
    receipt['sources']={str(i+1):r.receipts for i,r in enumerate(readers)}
    receipt['elapsed_seconds']=time.monotonic()-start
    receipt['pins_after']={'helper':m.digest(HELPER), 'contacts':m.digest(PRIOR/'contacts-root01.json'),
        'protocol':m.digest(BASE/'PROTOCOL.md'), 'producer':m.digest(Path(__file__))}
    m.require(receipt['pins']==receipt['pins_after'],'changed_dependency')
    with output.open('x') as stream:json.dump(receipt,stream,indent=2,sort_keys=True,allow_nan=False);stream.write('\n')
    print(json.dumps({'status':receipt['status'],'error':receipt.get('error'),'sha256':m.digest(output),
        'slave_populations':receipt.get('result',{}).get('slave_populations')}),flush=True)
    return 0 if receipt['status']=='complete' else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls',action='store_true');parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.controls:unittest.main(argv=[sys.argv[0]])
    elif args.output:
        try:sys.exit(run(args.output.resolve()))
        except m.CardError as exc:print(json.dumps({'status':'rejected','error':exc.code}));sys.exit(2)
    else:parser.error('choose --controls or --output')
