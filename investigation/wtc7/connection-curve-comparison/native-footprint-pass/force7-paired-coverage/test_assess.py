"""Synthetic checks of the finite adapter; no human or historical acceptance."""
import copy
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest

import assess as a


def row(x, ys=(), fragment='invented'):
    flags = [name for name, yes in [('target_left', x == 220), ('target_right', x == 329),
                                   ('target_top', 0 in ys), ('target_bottom', 87 in ys)] if ys and yes]
    return {'x': x, 'core': list(ys), 'fringe': [], 'fragment_id': fragment if ys else None,
            'fragment_membership': [{'fragment_id': fragment, 'core': list(ys), 'fringe': []}] if ys else [],
            'status': 'boundary_truncated' if flags else 'identified_local_fragment' if ys else 'no_attributable_cells',
            'reason': 'Invented synthetic fixture, not a source reading.',
            'boundary_flags': flags, 'unassigned_band_refs': []}


def fixture(role='primary'):
    return {'region_id': a.REGION, 'pair': 'F7', 'source': 'Im2.jpg', 'reader': role,
            'target_box': a.TARGET.copy(), 'context_box': a.CONTEXT.copy(),
            'coverage': {'full_context_inspected': True, 'raw_context_cells': 10032,
                         'raw_blocks': [{'columns': [218, 331], 'receipt': 'SYNTHETIC ONLY'}],
                         'rows': [0, 87], 'uncompleted_context': [],
                         'actual_views': [{'path':'../../native-strips01/Im2.jpg','receipt':'SYNTHETIC NOT A VIEW'},
                                          {'path':'../../render01/page-076.png','receipt':'SYNTHETIC NOT A VIEW'}],
                         'prior_knowledge': 'invented fixture'},
            'routes': {r: [row(x) for x in range(220, 330)] for r in ('solid', 'dash')},
            'unassigned_bands': [], 'human_accepted': False, 'physical_support': None}


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loaded = a.methods()

    def test_copy_alias_only(self):
        d = fixture(); saved = copy.deepcopy(d)
        out = a.validation_copy(d, 'primary')
        self.assertEqual(d, saved)
        self.assertEqual(out['region_id'], 'F7-Im2')
        out['region_id'] = a.REGION
        self.assertEqual(out, d)
        out['target_box'][0] = 0
        self.assertEqual(d['target_box'], a.TARGET)

    def test_complete_empty_fixture_is_not_accepted_support(self):
        d = fixture(); a.validate(d, 'primary', self.loaded)
        self.assertFalse(d['human_accepted'])
        self.assertIsNone(d['physical_support'])

    def test_wrong_identity_or_legacy_alias_rejected(self):
        for change in ({'region_id': 'F7-Im2'}, {'pair': 'F6'}, {'source': 'Im3.jpg'},
                       {'reader': 'force69_primary'}, {'reader': 'peer'}):
            d = fixture(); d.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                a.validate(d, 'primary', self.loaded)

    def test_geometry_exact_and_boolean_rejected(self):
        for box in ([True,0,330,88], [220.,0,330,88], [220,0,331,88]):
            d = fixture(); d['target_box'] = box
            with self.subTest(box=box), self.assertRaises(ValueError):
                a.validate(d, 'primary', self.loaded)

    def test_missing_or_duplicate_columns_rejected(self):
        for missing in (True, False):
            d = fixture()
            if missing: d['routes']['solid'].pop()
            else: d['routes']['solid'][2]['x'] = 221
            with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_field_alias_rejected(self):
        d = fixture(); d['routes']['solid'][4]['fragments'] = []
        with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_raw_coverage_gap_or_incomplete_rejected(self):
        for change in ({'full_context_inspected': False}, {'raw_context_cells': 10031},
                       {'rows': [False,87]}, {'rows': [1,87]}, {'actual_views': []},
                       {'uncompleted_context': [218]},
                       {'raw_blocks': [{'columns':[219,331], 'receipt':'synthetic'}]}):
            d = fixture(); d['coverage'].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                a.validate(d, 'primary', self.loaded)

    def test_native_bounds_and_class_disjointness(self):
        for ys in ([88], [True], [3,3]):
            d = fixture(); d['routes']['solid'][5] = row(225, ys)
            with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)
        d = fixture(); r = row(225, [3]); r['fringe'] = [3]
        r['fragment_membership'][0]['fringe'] = [3]; d['routes']['solid'][5] = r
        with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_wrong_source_views_and_explicit_truncation_rejected(self):
        for change in ({'actual_views': ['truthy but not a view']},
                       {'actual_views': [{'path':'../../native-strips01/Im3.jpg','receipt':'invented'}]},
                       {'raw_blocks': [{'columns':[218,331],'receipt':'invented','truncated':True}]},
                       {'prior_knowledge': True}, {'counterpart_new_annotations_read': True}):
            d = fixture(); d['coverage'].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                a.validate(d, 'primary', self.loaded)

    def test_distinct_bodies_retained(self):
        d = fixture(); r = row(225, [3,7]); r['fragment_id'] = None
        r['fragment_membership'] = [{'fragment_id': 'a', 'core':[3], 'fringe':[]},
                                    {'fragment_id': 'b', 'core':[7], 'fringe':[]}]
        d['routes']['dash'][5] = r
        a.validate(d, 'primary', self.loaded)
        copied = self.loaded[2].row_adapter(r, height=88)
        self.assertEqual([m['fragment_id'] for m in copied['fragments']], ['a','b'])
        self.assertIn('fragment_membership', r)

    def test_boundary_flags_checked(self):
        d = fixture(); d['routes']['solid'][0] = row(220,[0,87])
        a.validate(d, 'primary', self.loaded)
        d['routes']['solid'][0]['boundary_flags'].pop()
        with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_selected_route_overlap_rejected(self):
        d = fixture()
        for route in ('solid','dash'): d['routes'][route][5] = row(225,[12])
        with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_multiple_bands_and_reciprocity(self):
        d = fixture()
        for name, y, route in [('u1',3,'solid'), ('u2',7,'dash')]:
            b = row(225,[y],name); b.update(band_id=name,candidate_routes=[route],status='identity_conflict')
            d['unassigned_bands'].append(b)
            d['routes'][route][5]['unassigned_band_refs'] = [name]
            d['routes'][route][5]['status'] = 'identity_conflict'
        a.validate(d, 'primary', self.loaded)
        d['routes']['dash'][5]['unassigned_band_refs'] = ['u1']
        with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_band_to_band_or_string_candidates_rejected(self):
        for change in ({'candidate_routes': 'both'}, {'unassigned_band_refs':['another']}):
            d = fixture(); b = row(225,[3], 'u')
            b.update(band_id='u',candidate_routes=['solid'],status='identity_conflict'); b.update(change)
            d['unassigned_bands'] = [b]
            d['routes']['solid'][5].update(unassigned_band_refs=['u'],status='identity_conflict')
            with self.assertRaises(ValueError): a.validate(d, 'primary', self.loaded)

    def test_class_differences_not_lost_by_outer_equality(self):
        p, q = fixture(), fixture('peer')
        p['routes']['dash'][6] = row(226,[10])
        q['routes']['dash'][6] = row(226,[10])
        r = q['routes']['dash'][6]
        r.update(core=[],fringe=[10],status='fringe_only')
        r['fragment_membership'][0].update(core=[],fringe=[10])
        a.validate(p,'primary',self.loaded); a.validate(q,'peer',self.loaded)
        compared = a.compare_readers({'primary':p,'peer':q},self.loaded[4])
        self.assertEqual(len(compared['route_records']),220)
        self.assertEqual(len(compared['all_ink_columns']),110)
        self.assertNotEqual(compared['route_records'][116]['primary'],compared['route_records'][116]['peer'])

    def test_original_unchanged_after_validation(self):
        d = fixture(); saved = a.encode(d)
        a.validate(d,'primary',self.loaded)
        self.assertEqual(a.encode(d),saved)


class OutputTests(unittest.TestCase):
    def test_exact_rational_and_exclusive_output(self):
        with tempfile.TemporaryDirectory(prefix='f7-coverage-test-') as directory:
            p = Path(directory)/'invented.json'; raw = a.encode({'value':F(1,3)})
            a.save(p,raw)
            with self.assertRaises(FileExistsError): a.save(p,b'changed')
            self.assertEqual(p.read_bytes(),raw)

    def test_bad_or_conflicting_pin(self):
        with tempfile.TemporaryDirectory(prefix='f7-coverage-test-') as directory:
            p = Path(directory)/'invented'; a.save(p,b'abc'); pins={}
            a.add(pins,p)
            with self.assertRaises(ValueError): a.add(pins,p,'0'*64)
            with self.assertRaises(ValueError): a.add(pins,p,{'bytes':True,'sha256':a.pin(p)['sha256']})
            pins[next(iter(pins))]['bytes']=4
            with self.assertRaises(ValueError): a.add(pins,p)


if __name__ == '__main__': unittest.main()
