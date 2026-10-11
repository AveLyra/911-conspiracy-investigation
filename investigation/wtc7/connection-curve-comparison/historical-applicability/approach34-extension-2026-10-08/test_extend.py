"""Synthetic adapter and preservation controls, not historical validation."""
import copy
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
import extend as e


def entry(x=200, core=None, fringe=None, fragment='one', **extra):
    core = [40] if core is None else core
    fringe = [39, 41] if fringe is None else fringe
    result = {'x': x, 'core': core, 'fringe': fringe, 'fragment_id': fragment,
              'fragment_membership': [{'fragment_id': fragment, 'core': core.copy(), 'fringe': fringe.copy()}]
              if core or fringe else [], 'status': 'identified_local_fragment' if core else 'no_attributable_cells',
              'boundary_flags': [], 'reason': 'synthetic only', 'unassigned_band_refs': []}
    result.update(extra)
    return result


def fixture():
    data = {'pair': 'E3', 'region_id': 'E3-Im10', 'reader': 'primary', 'source': 'Im10.jpg',
        'target_box': [195,35,365,92], 'context_box': [193,33,367,92],
        'human_accepted': False, 'physical_support': None,
        'coverage': {'full_context_inspected': True, 'raw_context_cells': 10266,
                     'raw_blocks': [{'columns': [193,366], 'receipt': 'synthetic'}]},
        'routes': {}, 'unassigned_bands': []}
    for route, y in [('solid',60), ('dash',70)]:
        data['routes'][route] = [entry(x,core=[],fringe=[],fragment=None) for x in range(195,365)]
        row = data['routes'][route][5]
        row.update(status='identity_conflict', unassigned_band_refs=[route])
        band = entry(200, core=[y], fringe=[], fragment=route)
        band.update(band_id=route, candidate_routes=[route])
        data['unassigned_bands'].append(band)
    return data


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calc = e.import_pinned(e.OLD+'calculate.py', e.FIXED[e.OLD+'calculate.py'])
        cls.validator = e.import_pinned(e.APP+'compare.py', e.FIXED[e.APP+'compare.py'])

    def test_exact_deep_copy_and_membership(self):
        raw = entry()
        saved = copy.deepcopy(raw)
        out = e.row_adapter(raw)
        self.assertEqual(raw, saved)
        self.assertNotIn('fragment_membership', out)
        self.assertEqual(out['fragments'], raw['fragment_membership'])
        normalized, _ = self.calc.normalize(out, 'solid', 92)
        self.assertEqual(normalized['fragment_membership'], {'one': {'core_rows':[40], 'fringe_rows':[39,41]}})
        out['fragments'][0]['core'].append(44)
        self.assertEqual(raw, saved)

    def test_ambiguous_aliases_rejected(self):
        for key in ('column','core_rows','fringe_rows','fragments','band_refs'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                e.row_adapter(entry(**{key: []}))

    def test_malformed_and_lost_memberships_rejected(self):
        cases = [entry(x=True), entry(core=[True]), entry(core=[92]), entry(core=[40,40]),
                 entry(core=[41,40]), entry(fringe=[40]), entry(fragment_membership=[]),
                 entry(fragment_membership={}), entry(fragment_membership=[{'fragment_id':'x','core':[40],'fringe':[]}])]
        raw = entry(); raw['fragment_membership'] *= 2; cases.append(raw)
        for raw in cases:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                e.row_adapter(raw)

    def test_multiple_fragments_retained_and_excluded(self):
        raw = entry(core=[40,41], fringe=[], fragment=None,
                    fragment_membership=[{'fragment_id':'a','core':[40],'fringe':[]},
                                         {'fragment_id':'b','core':[41],'fringe':[]}])
        normalized,_ = self.calc.normalize(e.row_adapter(raw), 'solid', 92)
        self.assertEqual(len(normalized['fragment_membership']),2)
        self.assertIn('multiple_fragment_members', self.calc.screen.classify(normalized)['reasons'])

    def test_multiple_bands_and_original_preservation(self):
        data=fixture(); saved=copy.deepcopy(data)
        routes=e.adapt_original(data,self.validator)
        self.assertEqual(data,saved)
        self.assertEqual(len(data['unassigned_bands']),2)
        self.assertEqual(routes['solid'][5]['unassigned_band_refs'],['solid'])
        self.assertEqual(routes['dash'][5]['unassigned_band_refs'],['dash'])

    def test_broken_reciprocal_and_wrong_candidate_rejected(self):
        for mode in ('reciprocal','candidate','duplicate_band','coverage'):
            data=fixture()
            if mode=='reciprocal':
                data['routes']['solid'][5].update(status='no_attributable_cells',unassigned_band_refs=[])
            elif mode=='candidate': data['unassigned_bands'][0]['candidate_routes']=['dash']
            elif mode=='duplicate_band': data['unassigned_bands'].append(copy.deepcopy(data['unassigned_bands'][0]))
            else: data['coverage']['raw_blocks'][0]['columns']=[193,365]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                e.adapt_original(data,self.validator)

    def test_neighbor_and_band_exclusion_not_bridged(self):
        strip=self.calc.geometry.Strip('synthetic',100,100,(36,0,0,36,180,540))
        routes={r:[e.row_adapter(entry(x,core=[30,31],fringe=[29,32])) for x in range(10,17)] for r in ('solid','dash')}
        rows=self.calc.process(routes,strip,[10,10,17,90],'F')
        self.assertEqual([r['column'] for r in rows if r['route']=='solid' and r['conditional_window']],[12,13,14])
        routes['solid'][3]['unassigned_band_refs']=['unresolved']
        rows=self.calc.process(routes,strip,[10,10,17,90],'F')
        self.assertFalse(any(r['conditional_window'] for r in rows if r['route']=='solid'))
        self.assertTrue(all(r['curve_support_established'] is False for r in rows))

    def test_exclusive_save_and_exact_fraction_serialization(self):
        with tempfile.TemporaryDirectory(prefix='approach-extension-') as directory:
            target=Path(directory)/'result.json'
            raw=e.encode({'conditional':Fraction(1,3),'support':None})
            e.save(target,raw)
            with self.assertRaises(FileExistsError): e.save(target,b'altered')
            self.assertEqual(target.read_bytes(),raw)
        with self.assertRaises(TypeError): e.encode({'bad':object()})


if __name__=='__main__': unittest.main()
