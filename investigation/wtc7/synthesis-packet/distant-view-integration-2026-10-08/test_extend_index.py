#!/usr/bin/env python3
"""Finite synthetic wrapper tests; no candidate build or historical validation.

The unchanged legacy checker is loaded for its helpers. Dispatch tests mock its
validate() call; its existing separate tests and later real candidate check are
not represented as rerun here. Temporary fixture files are not source evidence.
"""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import extend_index as e

v = e.load_validator()


def pin_record(path='synthetic.txt'):
    return {'path': path, 'bytes': 0, 'sha256': '0' * 64}


def link(cid, aid, tid):
    return {'question': cid[:3], 'work_packages': [{'id': 'WP01', 'role': 'process'}],
            'dependencies': [], 'causal_links': [],
            'evidence': [{'artifact_id': aid, 'locator': 'synthetic row', 'role': 'synthetic test',
                          'family_id': 'F-DistantView-access-copy'}],
            'transforms': [tid], 'remaining_gap': 'synthetic unknown',
            'verification_status': {key: 'not supplied' for key in
                ('source_inspection', 'calculation_reproduction', 'human_acceptance', 'expert_review')},
            'absences': {field: {'kind': 'not_applicable', 'reason': 'synthetic scope',
                                 'consequence': 'no completion inferred'} for field in ('dependencies', 'causal_links')}}


def fixture():
    baseline = {'version': 2, 'date': 'prior', 'scope': 'prior scope', 'remaining_index_work': 'prior gap',
                'status': 'research', 'critical_review': {'old_hash': 'historical'},
                'cause_ranking_changed': False, 'canonical_promotion': False,
                'primary_source_joins': [{'adverse': 'retained'}],
                'integration': {'version': 1, 'artifacts': {}, 'families': {}, 'transforms': {},
                                'claim_links': {}, 'additional_claims': [],
                                'status_updates': {'Q03-observed-sequence': {'correction': 'StageC preserved'}},
                                'traversals': ['Q04-body-boundary', 'Q06-native-state', 'Q09-SEC-access'],
                                'protocol': {'original': True}, 'baseline': {'version': 1},
                                'limits': {'accepted': False}}}
    prior = baseline['integration']
    prior['artifacts'] = {f'A{i:03d}': {**pin_record(f'old-{i}.txt'), 'role': 'old'} for i in range(207)}
    prior['families'] = {f'F-old-{i}': {'old': i} for i in range(19)}
    prior['transforms'] = {f'T-old-{i}': {'old': i} for i in range(23)}
    prior['claim_links'] = {f'old-{i}': {'old': i, 'acceptance': False} for i in range(58)}
    prior['additional_claims'] = [{'id': f'old-{40 + i}', 'content': i} for i in range(18)]
    additions = {'artifacts': {}, 'families': {}, 'transforms': {}, 'additional_claims': [], 'claim_links': {}}
    units = []
    for i, (uid, (cids, tid)) in enumerate(e.UNITS.items()):
        aid = f'N{i}'
        additions['artifacts'][aid] = {**pin_record(f'new-{i}.txt'), 'role': 'selected entry point'}
        additions['transforms'][tid] = {**{field: [aid] for field in e.ARTIFACT_FIELDS},
                                        'status': 'previous result', 'missing': [], 'limit': 'synthetic only'}
        units.append({'id': uid, 'claim_ids': list(cids), 'transform_ids': [tid]})
        for cid in cids:
            additions['additional_claims'].append({'id': cid, 'parent_claim': e.PARENTS[cid[:3]],
                                                   'claim': 'synthetic claim', 'layer': 'synthetic', 'grade': 'test',
                                                   'ceiling': 'no evidence', 'alternative': 'unknown',
                                                   'would_change_with': 'actual record'})
            additions['claim_links'][cid] = link(cid, aid, tid)
    additions['families'] = {fid: {'description': 'synthetic source', 'basis': [{'artifact_id': 'N0', 'locator': 'row'}],
                                   'independence_limit': 'no independence claim', 'origin_status': 'unknown'}
                              for fid in e.FAMILIES}
    manifest = {'version': 1, 'controls': {k: pin_record(k + '.txt') for k in ('baseline', 'protocol', 'old_validator')},
                'root_updates': {'version': 3, 'date': '2026-10-08', 'scope': 'bounded extension',
                                 'remaining_index_work': 'physical and human gaps'},
                'additions': additions,
                'revision': {'date': '2026-10-08', 'units': units,
                             'status_supplements': {parent: {'disposition': 'qualified supplement',
                                  'supporting_claim_ids': [cid for cid in e.CLAIMS if e.PARENTS[cid[:3]] == parent],
                                  'limit': 'not question closure'} for parent in e.PARENTS.values()},
                             'limits': {key: False for key in e.LIMIT_FLAGS}, 'scope': 'four completed units'}}
    return baseline, manifest, pin_record('extension.json')


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.baseline, self.manifest, self.extension_pin = fixture()

    def apply(self):
        return e.apply_extension(v, self.baseline, self.manifest, self.extension_pin)

    def test_exact_append_counts_and_no_input_mutation(self):
        before = v.encoded([self.baseline, self.manifest])
        result = self.apply()
        self.assertEqual(v.encoded([self.baseline, self.manifest]), before)
        integration = result['integration']
        self.assertEqual([len(integration[k]) for k in ('artifacts', 'families', 'transforms', 'claim_links', 'additional_claims')],
                         [211, 21, 27, 63, 23])
        self.assertEqual(integration['additional_claims'][:18], self.baseline['integration']['additional_claims'])
        self.assertEqual(result['critical_review'], self.baseline['critical_review'])
        self.assertEqual(integration['status_updates'], self.baseline['integration']['status_updates'])
        self.assertEqual(integration['distant_view_revision']['extension'], self.extension_pin)
        e.assert_candidate(v, result, self.apply())

    def test_every_old_container_rewrite_and_old_prefix_reorder_rejected(self):
        expected = self.apply()
        paths = [('critical_review',), ('status',), ('primary_source_joins',),
                 ('integration', 'status_updates'), ('integration', 'traversals'),
                 ('integration', 'protocol'), ('integration', 'baseline'), ('integration', 'limits'),
                 ('integration', 'artifacts', 'A000'), ('integration', 'families', 'F-old-0'),
                 ('integration', 'transforms', 'T-old-0'), ('integration', 'claim_links', 'old-0')]
        for path in paths:
            candidate = copy.deepcopy(expected)
            row = candidate
            for key in path[:-1]:
                row = row[key]
            row[path[-1]] = {'rewritten': True}
            with self.subTest(path=path), self.assertRaises(v.Invalid):
                e.assert_candidate(v, candidate, expected)
        candidate = copy.deepcopy(expected)
        candidate['integration']['additional_claims'][:18] = reversed(candidate['integration']['additional_claims'][:18])
        with self.assertRaises(v.Invalid):
            e.assert_candidate(v, candidate, expected)

    def test_boolean_integer_substitution_never_preserves_baseline(self):
        expected = self.apply()
        candidate = copy.deepcopy(expected)
        candidate['cause_ranking_changed'] = 0
        with self.assertRaises(v.Invalid):
            e.assert_candidate(v, candidate, expected)
        for field in ('version',):
            self.manifest[field] = True
            with self.assertRaises(v.Invalid):
                self.apply()
        self.manifest['version'] = 1
        self.manifest['root_updates']['version'] = 3.0
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_every_acceptance_flag_true_or_integer_rejected(self):
        for key in e.LIMIT_FLAGS:
            for value in (True, 0, 1, None):
                self.manifest['revision']['limits'][key] = value
                with self.subTest(key=key, value=value), self.assertRaises(v.Invalid):
                    self.apply()
            self.manifest['revision']['limits'][key] = False

    def test_unknown_manifest_root_revision_and_row_keys_rejected(self):
        candidates = [self.manifest, self.manifest['root_updates'], self.manifest['revision'],
                      self.manifest['additions'], self.manifest['controls'],
                      self.manifest['additions']['artifacts']['N0'],
                      self.manifest['additions']['claim_links'][e.CLAIMS[0]],
                      self.manifest['additions']['families']['F-DistantView-access-copy']]
        for row in candidates:
            row['independent_source_count'] = 1
            with self.assertRaises(v.Invalid):
                self.apply()
            del row['independent_source_count']

    def test_missing_five_claims_and_duplicate_claim_ids_rejected(self):
        claims = self.manifest['additions']['additional_claims']
        last = claims.pop()
        with self.assertRaises(v.Invalid):
            self.apply()
        claims.append(last)
        claims[-1] = copy.deepcopy(claims[0])
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_registry_collisions_and_extra_links_rejected(self):
        additions = self.manifest['additions']
        additions['artifacts']['A000'] = additions['artifacts']['N0']
        with self.assertRaisesRegex(v.Invalid, 'collision'):
            self.apply()
        del additions['artifacts']['A000']
        additions['claim_links']['old-0'] = additions['claim_links'][e.CLAIMS[0]]
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_exact_family_transform_unit_coverage(self):
        for field in ('families', 'transforms'):
            items = self.manifest['additions'][field]
            key, row = items.popitem()
            with self.assertRaises(v.Invalid):
                self.apply()
            items[key] = row
        units = self.manifest['revision']['units']
        saved = units.pop()
        with self.assertRaises(v.Invalid):
            self.apply()
        units.append(saved)
        units[-1] = copy.deepcopy(units[0])
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_wrong_unit_claim_transform_and_parent_rejected(self):
        unit = self.manifest['revision']['units'][0]
        unit['claim_ids'] = [e.CLAIMS[1]]
        with self.assertRaises(v.Invalid):
            self.apply()
        unit['claim_ids'] = [e.CLAIMS[0]]
        unit['transform_ids'] = ['T-DistantView-encoded-timing']
        with self.assertRaises(v.Invalid):
            self.apply()
        unit['transform_ids'] = ['T-DistantView-source-screen']
        self.manifest['additions']['additional_claims'][0]['parent_claim'] = e.PARENTS['Q10']
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_missing_unit_transform_reachability_rejected(self):
        self.manifest['additions']['claim_links'][e.CLAIMS[0]]['transforms'] = []
        with self.assertRaisesRegex(v.Invalid, 'not reachable'):
            self.apply()

    def test_orphan_new_artifact_rejected(self):
        self.manifest['additions']['artifacts']['orphan'] = {**pin_record('orphan.txt'), 'role': 'unused'}
        with self.assertRaisesRegex(v.Invalid, 'unreachable'):
            self.apply()

    def test_wrong_supplement_support_or_dates_rejected(self):
        row = self.manifest['revision']['status_supplements'][e.PARENTS['Q03']]
        row['supporting_claim_ids'] = [e.CLAIMS[2]]
        with self.assertRaises(v.Invalid):
            self.apply()
        row['supporting_claim_ids'] = [e.CLAIMS[0]]
        self.manifest['revision']['date'] = 'changed'
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_no_new_mechanical_support_or_implicit_absence(self):
        row = self.manifest['additions']['claim_links'][e.CLAIMS[0]]
        row['causal_links'] = [{'id': '1', 'relation': 'supports', 'scope': 'new', 'basis': 'new'}]
        with self.assertRaises(v.Invalid):
            self.apply()
        row['causal_links'] = []
        row['absences']['causal_links']['kind'] = 'missing'
        with self.assertRaises(v.Invalid):
            self.apply()

    def test_invalid_pin_bytes_bool_or_digest(self):
        row = self.manifest['controls']['baseline']
        row['bytes'] = False
        with self.assertRaises(v.Invalid):
            self.apply()
        row['bytes'] = 0
        row['sha256'] = 'not a pin'
        with self.assertRaises(v.Invalid):
            self.apply()


class FilesystemTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='extension-synthetic-')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name).resolve()
        baseline, manifest, pin = fixture()
        self.expected = e.apply_extension(v, baseline, manifest, pin)

    def test_duplicate_safe_loader_rejects_nonfinite_and_duplicate_keys(self):
        path = self.directory / 'bad.json'
        for content in ('{"version":1,"version":2}', '{"value":NaN}', '{"value":Infinity}'):
            path.write_text(content)
            with self.assertRaises(v.Invalid):
                v.load_json(path)

    def test_exclusive_outputs_deterministic_and_refuse_unsafe_names(self):
        first = e.write_exclusive(v, self.expected, 'candidate01.json', self.directory)
        second = e.write_exclusive(v, self.expected, 'candidate02.json', self.directory)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with self.assertRaises(FileExistsError):
            e.write_exclusive(v, self.expected, 'candidate01.json', self.directory)
        for name in ('../candidate01.json', 'material-claim-index.json', '/tmp/candidate01.json'):
            with self.assertRaises(v.Invalid):
                e.write_exclusive(v, self.expected, name, self.directory)

    def test_output_symlink_directory_and_existing_symlink_refused(self):
        directory = self.directory / 'alias'
        directory.symlink_to(self.directory, target_is_directory=True)
        with self.assertRaises(v.Invalid):
            e.write_exclusive(v, self.expected, 'candidate01.json', directory)
        (self.directory / 'candidate01.json').symlink_to(self.directory / 'missing')
        with self.assertRaises(FileExistsError):
            e.write_exclusive(v, self.expected, 'candidate01.json', self.directory)

    def test_preimport_hash_and_symlink_guard(self):
        path = self.directory / 'code.py'
        path.write_text('raise RuntimeError("must not execute")')
        with self.assertRaisesRegex(ValueError, 'hard-pinned'):
            e.bootstrap_bytes(path, '0' * 64)
        alias = self.directory / 'alias.py'
        alias.symlink_to(path)
        with self.assertRaises(ValueError):
            e.bootstrap_bytes(alias)

    def test_duplicate_resolved_paths_rejected_without_rewriting(self):
        path = self.directory / 'source.txt'
        path.write_text('synthetic')
        candidate = {'integration': {'artifacts': {'old': {'path': str(path)}, 'new': {'path': 'source.txt'}}}}
        before = copy.deepcopy(candidate)
        with self.assertRaisesRegex(v.Invalid, 'duplicate resolved'):
            e.unique_artifact_paths(v, candidate, self.directory, (self.directory,))
        self.assertEqual(candidate, before)

    def test_legacy_dispatch_original_controls_and_full_bracket(self):
        path = e.write_exclusive(v, self.expected, 'candidate01.json', self.directory)
        control = self.directory / 'control.txt'
        control.write_text('unchanged')
        before = {str(control): v.file_state(control)}
        counts = {'claim_links': 63, 'additional_claims': 23, 'families': 21, 'transforms': 27}
        with mock.patch.object(v, 'APPROVED_ROOTS', (self.directory,)), \
                mock.patch.object(e, 'unique_artifact_paths'), mock.patch.object(v, 'validate', return_value=counts) as old:
            result = e.check_prepared(v, path, self.expected, before)
            self.assertEqual(result['status'], 'pass')
            old.assert_called_once_with(path, e.FIXED['original_baseline'][0], e.FIXED['original_inputs'][0])
            def mutate_control(*args):
                control.write_text('changed during legacy validation')
                return counts
            old.side_effect = mutate_control
            with self.assertRaisesRegex(v.Invalid, 'control/candidate changed'):
                e.check_prepared(v, path, self.expected, before)

    def test_candidate_mutation_in_legacy_call_rejected(self):
        path = e.write_exclusive(v, self.expected, 'candidate01.json', self.directory)
        def mutate(*args):
            path.write_text('{}')
            return {'claim_links': 63, 'additional_claims': 23, 'families': 21, 'transforms': 27}
        with mock.patch.object(v, 'APPROVED_ROOTS', (self.directory,)), \
                mock.patch.object(e, 'unique_artifact_paths'), mock.patch.object(v, 'validate', side_effect=mutate):
            with self.assertRaisesRegex(v.Invalid, 'control/candidate changed'):
                e.check_prepared(v, path, self.expected, {})

    def test_failed_legacy_check_propagates_not_wrapper_pass(self):
        path = e.write_exclusive(v, self.expected, 'candidate01.json', self.directory)
        with mock.patch.object(v, 'APPROVED_ROOTS', (self.directory,)), \
                mock.patch.object(e, 'unique_artifact_paths'), mock.patch.object(v, 'validate', side_effect=v.Invalid('legacy fails')):
            with self.assertRaisesRegex(v.Invalid, 'legacy fails'):
                e.check_prepared(v, path, self.expected, {})

    def test_production_placeholder_refuses_before_control_reads_or_writes(self):
        with mock.patch.object(e, 'EXTENSION_SHA', 'PENDING_ROOT_FROZEN_REVIEW'), \
                mock.patch.object(e, 'bootstrap_bytes') as read, mock.patch.object(e, 'write_exclusive') as write:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(e.main(['build', '--out', 'candidate01.json']), 1)
            self.assertIn('PENDING_ROOT_FROZEN_REVIEW', output.getvalue())
            read.assert_not_called()
            write.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
