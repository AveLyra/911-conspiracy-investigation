"""Synthetic integration controls; not new historical annotations."""
import copy
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest
import extend as e


def row(x, core=None, fringe=None, fid=None, **changes):
    core = [] if core is None else core
    fringe = [] if fringe is None else fringe
    value = {'x': x, 'core': core, 'fringe': fringe, 'fragment_id': fid,
             'fragment_membership': [{'fragment_id': fid, 'core': core.copy(), 'fringe': fringe.copy()}] if core or fringe else [],
             'status': 'identified_local_fragment' if core else 'no_attributable_cells',
             'reason': 'Synthetic only', 'boundary_flags': [], 'unassigned_band_refs': []}
    value.update(changes)
    return value


def fixture(pair='F5', role='primary'):
    source, box = e.REGIONS[pair]
    context = {'F5': [308,0,427,88], 'F6': [268,53,342,88]}[pair]
    x0,y0,x1,y1 = context
    data = {'pair': pair, 'region_id': pair+'-'+source, 'source': source+'.jpg', 'reader': role,
            'target_box': box.copy(), 'context_box': context, 'human_accepted': False, 'physical_support': None,
            'coverage': {'full_context_inspected': True, 'raw_context_cells': (x1-x0)*(y1-y0),
                         'raw_blocks': [{'columns': [x0,x1-1], 'receipt': 'synthetic'}], 'uncompleted_context': []},
            'routes': {r: [row(x) for x in range(box[0],box[2])] for r in ('solid','dash')}, 'unassigned_bands': []}
    x = box[0]+5
    for label, y in [('a',60), ('b',62)]:
        data['unassigned_bands'].append(row(x,[y],[],label,band_id=label,candidate_routes=['dash']))
    data['routes']['dash'][5].update(status='identity_conflict',unassigned_band_refs=['a','b'])
    return data


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = e.import_fixed(e.PRIOR+'extend.py')
        cls.calc = e.import_fixed(e.CALC+'calculate.py')
        cls.validator = e.import_fixed(e.SOURCE+'compare.py')

    def test_both_regions_and_peer_serialization_preserved(self):
        for pair in e.REGIONS:
            for role, serialized in [('primary','primary'),('peer','force56_peer'),('peer','peer')]:
                data=fixture(pair,serialized); saved=e.encode(data)
                result=e.adapt(data,pair,role,self.validator,self.adapter)
                self.assertEqual(e.encode(data),saved)
                self.assertEqual(data['reader'],serialized)
                self.assertEqual(len(result['solid']),e.REGIONS[pair][1][2]-e.REGIONS[pair][1][0])
                self.assertEqual(len(data['unassigned_bands']),2)
                self.assertEqual(result['dash'][5]['unassigned_band_refs'],['a','b'])

    def test_wrong_role_source_region_and_geometry_rejected(self):
        for change in ({'reader':'force56_peer'},{'reader':'unregistered'}, {'source':'Im10.jpg'},
                       {'region_id':'F5-Im4'}, {'target_box':[310,0,425,92]}):
            data=fixture();data.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):
                e.adapt(data,'F5','primary',self.validator,self.adapter)

    def test_membership_copy_and_exact_height(self):
        raw=row(315,[86],[87],'one');saved=copy.deepcopy(raw)
        converted=self.adapter.row_adapter(raw,height=88)
        converted['fragments'][0]['core'].append(85)
        self.assertEqual(raw,saved)
        with self.assertRaises(ValueError):self.adapter.row_adapter(row(315,[88],[],'one'),height=88)

    def test_ambiguous_and_malformed_memberships_rejected(self):
        for change in ({'fragments':[]},{'column':315},{'fragment_membership':[]},
                       {'core':[True]},{'fringe':[40]},{'x':True}):
            raw=row(315,[40],[],'one');raw.update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):
                self.adapter.row_adapter(raw,height=88)
        raw=row(315,[40],[],'one');raw['fragment_membership']*=2
        with self.assertRaises(ValueError):self.adapter.row_adapter(raw,height=88)

    def test_lost_bands_ref_coverage_and_boundary_rejected(self):
        for kind in ('ref','band','coverage','boundary'):
            data=fixture()
            if kind=='ref':data['routes']['dash'][5]['unassigned_band_refs'].pop()
            elif kind=='band':data['unassigned_bands'].pop()
            elif kind=='coverage':data['routes']['solid'].pop()
            else:data['routes']['solid'][7]=row(317,[87],[],'end')
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                e.adapt(data,'F5','primary',self.validator,self.adapter)

    def test_bands_withhold_only_their_route_and_no_neighbor_bridge(self):
        strip=self.calc.geometry.Strip('synthetic',100,100,(36,0,0,36,180,540))
        routes={r:[self.adapter.row_adapter(row(x,[30,31],[29,32],'one'),height=88)
                   for x in range(10,17)] for r in ('solid','dash')}
        first=self.calc.process(routes,strip,[10,10,17,88],'F')
        self.assertEqual([r['column'] for r in first if r['route']=='solid' and r['conditional_window']],[12,13,14])
        routes['dash'][3]['unassigned_band_refs']=['unresolved']
        second=self.calc.process(routes,strip,[10,10,17,88],'F')
        self.assertEqual(sum(r['conditional_window'] for r in second if r['route']=='solid'),3)
        self.assertFalse(any(r['conditional_window'] for r in second if r['route']=='dash'))
        self.assertTrue(all(r['curve_support_established'] is False for r in second))

    def test_recursive_dependency_graph_and_relative_aliases(self):
        with tempfile.TemporaryDirectory(prefix='force56-pins-') as folder:
            root=Path(folder); sub=root/'sub';sub.mkdir();leaf=root/'leaf';leaf.write_bytes(b'fixture')
            inner=sub/'inner.json';inner.write_text(json.dumps({'inputs':{'../leaf':e.pin(leaf)}}))
            outer=root/'outer.json';outer.write_text(json.dumps({'dependencies':{'sub/inner.json':e.pin(inner)}}))
            pins={};nodes=e.closure([outer],pins,root,set())
            self.assertEqual(set(pins),{'outer.json','sub/inner.json','leaf'})
            self.assertEqual(nodes,['outer.json','sub/inner.json'])
            e.include(pins,sub/'../leaf',e.pin(leaf),root,set())
            self.assertEqual(len(pins),3)

    def test_missing_changed_and_conflicting_dependencies_rejected(self):
        with tempfile.TemporaryDirectory(prefix='force56-pins-') as folder:
            root=Path(folder);leaf=root/'leaf';leaf.write_bytes(b'fixture');want=e.pin(leaf)
            parent=root/'parent.json';parent.write_text(json.dumps({'inputs':{'leaf':want}}))
            leaf.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.closure([parent],{},root,set())
            with self.assertRaises(ValueError):e.include({'leaf':want},leaf,root=root,allowed=set())
            parent.write_text(json.dumps({'inputs':{'missing':want}}))
            with self.assertRaises(FileNotFoundError):e.closure([parent],{},root,set())

    def test_only_exact_outside_authority_paths_allowed(self):
        for path in e.AUTHORITY:self.assertIsInstance(e.key(path),str)
        with self.assertRaises(ValueError):e.key(Path('/Users/admin/docs/911/unapproved.json'))
        self.assertEqual(len(e.AUTHORITY),6)

    def test_malformed_maps_and_before_after_rejected(self):
        with tempfile.TemporaryDirectory(prefix='force56-pins-') as folder:
            root=Path(folder);file=root/'case.json'
            for data in ({'inputs':[]},{'inputs':{},'inputs_after':{'x':{}}},{'script_pin':{}},[]):
                file.write_text(json.dumps(data))
                with self.subTest(data=data),self.assertRaises(ValueError):e.closure([file],{},root,set())

    def test_json_types_and_exclusive_output(self):
        self.assertFalse(e.exact(False,0))
        with tempfile.TemporaryDirectory(prefix='force56-save-') as folder:
            path=Path(folder)/'output';raw=e.encode({'value':Fraction(1,3),'support':None})
            e.save(path,raw)
            with self.assertRaises(FileExistsError):e.save(path,b'changed')
            self.assertEqual(path.read_bytes(),raw)
        with self.assertRaises(TypeError):e.encode({'unknown':object()})


if __name__=='__main__':unittest.main()
