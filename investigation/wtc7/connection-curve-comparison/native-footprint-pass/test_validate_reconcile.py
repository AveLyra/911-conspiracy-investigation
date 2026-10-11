"""Synthetic-only validator controls; no historical annotations loaded."""
import copy
import tempfile
import unittest
import json
from unittest.mock import patch
from pathlib import Path
import validate_reconcile as v


def fixture():
    return {'reader': 'synthetic', 'pair': 'E7', 'target_box': v.TARGETS['E7'][:],
            'routes': {r: [{'x': x, 'core': [], 'fringe': [], 'status': 'no_attributable_cells',
                           'note': 'synthetic', 'fragment_id': None, 'boundary_flags': []}
                          for x in range(580, 690)] for r in ['solid', 'dash']}}


class Tests(unittest.TestCase):
    def test_complete_empty_and_no_mutation(self):
        a = fixture(); old = copy.deepcopy(a)
        self.assertEqual(len(v.compare(a, a, 'E7')), 220)
        self.assertEqual(a, old)

    def test_holes_and_class_differences(self):
        a, b = fixture(), fixture()
        a['routes']['solid'][1].update(core=[20], fringe=[22], fragment_id='one', status='identified_local_fragment')
        b['routes']['solid'][1].update(core=[22], fringe=[20], fragment_id='different', status='identified_local_fragment')
        z = v.compare(a, b, 'E7')[1]
        self.assertEqual(z['outer']['union'], [20, 22])
        self.assertEqual(z['core']['symmetric_difference'], [20, 22])
        self.assertNotIn('identity_equal', z)

    def test_conflict_empty_and_nonempty(self):
        for fringe in [[], [20, 22]]:
            a = fixture(); a['routes']['dash'][1].update(fringe=fringe, status='identity_conflict')
            v.validate(a, 'E7')

    def test_invalid_rows(self):
        for bad in [[True], [20.0], [20, 20], [22, 20], [13], [30]]:
            a = fixture(); a['routes']['solid'][1].update(core=bad, fragment_id='one')
            with self.subTest(bad=bad), self.assertRaises(ValueError): v.validate(a, 'E7')

    def test_coverage_and_fields(self):
        for change in [lambda a:a['routes']['solid'].pop(),
                       lambda a:a['routes']['solid'][1].update(x=580),
                       lambda a:a['routes']['solid'][1].update(x=True),
                       lambda a:a.update(pair='E6'),
                       lambda a:a.update(target_box=[580,14,691,30]),
                       lambda a:a['routes']['solid'][1].update(note=' '),
                       lambda a:a['routes']['solid'][1].update(status='accepted')]:
            a = fixture(); change(a)
            with self.assertRaises(ValueError): v.validate(a, 'E7')

    def test_overlap_and_missing_id(self):
        for update in [dict(core=[20], fringe=[20], fragment_id='one'), dict(core=[20]), dict(fragment_id=True)]:
            a=fixture(); a['routes']['solid'][1].update(update)
            with self.assertRaises(ValueError): v.validate(a, 'E7')

    def test_membership_union(self):
        a=fixture(); e=a['routes']['dash'][1]
        e.update(core=[20,22], status='identified_local_fragment', fragment_membership={'a':{'core':[20],'fringe':[]},'b':{'core':[22],'fringe':[]}})
        v.validate(a, 'E7')
        e['fragment_membership']['b']['core']=[]
        with self.assertRaises(ValueError): v.validate(a, 'E7')

    def test_boundary(self):
        a=fixture(); e=a['routes']['solid'][0]
        e.update(core=[14,29], fragment_id='one', status='boundary_truncated', boundary_flags=['target_left','target_top','target_bottom'])
        v.validate(a, 'E7')
        e['boundary_flags'].pop()
        with self.assertRaises(ValueError): v.validate(a, 'E7')

    def test_exclusive_save(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'result.json';v.save(p, {'one':1});old=p.read_bytes()
            with self.assertRaises(FileExistsError):v.save(p, {'two':2})
            self.assertEqual(p.read_bytes(),old)

    def test_status_consistency(self):
        for status, core, fringe, okay in [('fringe_only',[],[20],True),
                ('fringe_only',[20],[21],False),('fringe_only',[],[],False),
                ('identified_local_fragment',[],[20],False),('no_attributable_cells',[],[20],False),
                ('boundary_truncated',[],[20],False)]:
            a=fixture();a['routes']['solid'][1].update(status=status,core=core,fringe=fringe)
            if okay:
                v.validate(a,'E7');self.assertTrue(v.identity(a['routes']['solid'][1])['unknown_attribution'])
            else:
                with self.assertRaises(ValueError):v.validate(a,'E7')

    def test_target_aliases(self):
        a=fixture();a['coverage']={'target_box':[515,57,690,85]}
        with self.assertRaises(ValueError):v.validate(a,'E7')

    def test_explicit_pin_adapter(self):
        a={'pair':'E6','pins':{'literal_script_sha256':'a'*64}}
        self.assertIn((v.HERE/'reader-E6-independent.py').resolve(),v.declared_paths(a))
        self.assertIn((v.HERE/'reader-E7-root.py').resolve(),v.declared_paths({'pair':'E7','script_pin':{'sha256':'a'*64,'bytes':1}}))
        for pins in [{'unknown':'a'*64},{'source_sha256':False},{'source_sha256':'wrong'}, {'x':{'path':'x','sha256':'a'*64,'bytes':True}}]:
            with self.assertRaises(ValueError):v.declared_paths({'pair':'E6','pins':pins})

    def test_full_run_pins_determinism_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            here=Path(tmp)/'unit';here.mkdir()
            for n in ['PROTOCOL.md','REGIONS.json','context01.json','literal.py']:(here/n).write_text('synthetic')
            for directory,name in [('native-strips01','Im8.jpg'),('render01','page-076.png')]:
                (Path(tmp)/directory).mkdir();(Path(tmp)/directory/name).write_text('synthetic')
            frozen={n:v.pin(here/n)['sha256'] for n in ['PROTOCOL.md','REGIONS.json','../native-strips01/Im8.jpg']}
            a=fixture();a['inputs']={n:v.pin(here/n) for n in [*frozen,'context01.json','literal.py']}
            rp,pp=here/'root.json',here/'peer.json'
            rp.write_text(json.dumps(a));pp.write_text(json.dumps(a))
            with patch.object(v,'HERE',here),patch.object(v,'FROZEN',frozen):
                v.run(rp,pp,'E7',here/'one.json');v.run(rp,pp,'E7',here/'two.json')
                self.assertEqual((here/'one.json').read_bytes(),(here/'two.json').read_bytes())
                with self.assertRaises(FileExistsError):v.run(rp,pp,'E7',here/'one.json')
                (here/'literal.py').write_text('changed')
                with self.assertRaises(ValueError):v.run(rp,pp,'E7',here/'bad.json')
                a['inputs'].pop('literal.py');a['inputs'].pop('PROTOCOL.md');rp.write_text(json.dumps(a))
                with self.assertRaises(ValueError):v.run(rp,pp,'E7',here/'missing.json')
                (here/'PROTOCOL.md').write_text('changed')
                with self.assertRaises(ValueError):v.run(rp,pp,'E7',here/'changed.json')


if __name__ == '__main__': unittest.main()
