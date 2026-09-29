#!/usr/bin/env python3
"""Synthetic adapter controls run before alternate historical project parse."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


adapter = module('alternate_adapter', Path(__file__).with_name('alternate-export.py'))
parser = adapter.load_parser()
oldtests = module('frozen_controls', adapter.PARSER_TEST)


def archive(entries):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as saved:
        for name, payload in entries:
            saved.writestr(name, payload)
    return stream.getvalue()


def source_fixture():
    root, _, _ = oldtests.fixture()
    project = ET.tostring(root)
    nested = archive([(f'entry{i}.bin', b'x') for i in range(4)] + [('project.trk', project)])
    parent = archive([('safe.trz', nested)])
    options = {'parent_sha': adapter.digest(parent), 'member': 'safe.trz',
               'member_sha': adapter.digest(nested), 'project_sha': adapter.digest(project),
               'project_size': len(project)}
    return project, nested, parent, options


class AdapterControls(unittest.TestCase):
    def test_valid_selection_and_fifth_entry(self):
        project, _, parent, options = source_fixture()
        actual, receipt = adapter.select_source(parent, parser, **options)
        self.assertEqual(actual, project)
        self.assertEqual(receipt['nested_project_entry_index_zero_based'], 4)
        self.assertFalse(receipt['raw_project_or_media_written'])

    def test_each_hash_and_size_guard(self):
        _, _, parent, options = source_fixture()
        for key in ['parent_sha', 'member_sha', 'project_sha', 'project_size']:
            altered = dict(options)
            altered[key] = '0'*64 if key.endswith('sha') else options[key]+1
            with self.assertRaises(ValueError):
                adapter.select_source(parent, parser, **altered)

    def test_wrong_ordinal_and_count_rejected(self):
        project, _, _, options = source_fixture()
        for entries in [[('project.trk', project)] + [(f'e{i}', b'x') for i in range(4)],
                        [(f'e{i}', b'x') for i in range(4)]]:
            nested = archive(entries)
            parent = archive([('safe.trz', nested)])
            changed = dict(options, parent_sha=adapter.digest(parent), member_sha=adapter.digest(nested))
            with self.assertRaises(ValueError):
                adapter.select_source(parent, parser, **changed)

    def test_path_traversal_refused_without_extraction(self):
        _, nested, _, options = source_fixture()
        parent = archive([('../safe.trz', nested)])
        with self.assertRaisesRegex(ValueError, 'rejected_archive_member'):
            adapter.select_source(parent, parser, **dict(options, member='../safe.trz', parent_sha=adapter.digest(parent)))

    def test_direct_oracle_sparse_key_state_and_no_text_disclosure(self):
        project, _, _, _ = source_fixture()
        exported = parser.parse_project(project)
        verified = adapter.direct_oracle(project, exported)
        self.assertEqual(verified['pointmass_rows'], 2)
        self.assertEqual(verified['pointmass_coordinates'], 4)
        self.assertEqual(verified['keyframe_membership_flags'], 2)
        self.assertNotIn('DO_NOT_EXPORT', json.dumps(exported))

    def test_oracle_detects_numeric_locator_key_missing_and_omission_mutation(self):
        project, _, _, _ = source_fixture()
        pristine = parser.parse_project(project)
        for variant in range(6):
            changed = copy.deepcopy(pristine)
            track = changed['pointmass_tracks'][0]
            row = track['framedata'][0]['rows'][0]
            field = row['objects'][0]['coordinates']['x']['occurrences'][0]
            if variant == 0:
                field['value'] += 1
            elif variant == 1:
                field['xml_path'] = '/*[1]'
            elif variant == 2:
                row['saved_keyFrame_member'] = False
            elif variant == 3:
                track['missing_clip_step_indices'] = []
            elif variant == 4:
                track['framedata'][0]['rows'].pop()
            else:
                changed['pointmass_tracks'].clear()
            with self.assertRaises(ValueError):
                adapter.direct_oracle(project, changed)

    def test_oracle_envelope_guard(self):
        with self.assertRaisesRegex(ValueError, 'oracle_rejected_envelope'):
            adapter.direct_oracle(b'<!DOCTYPE object><object/>', {})

    def test_output_allowlist(self):
        for name in ['../alternate-export01.json', '/tmp/alternate-export01.json', 'project01.json', 'alternate-export03.json']:
            with self.assertRaisesRegex(ValueError, 'invalid_output_name'):
                adapter.target_path(name)


if __name__ == '__main__':
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(oldtests.ExportControls),
                               unittest.defaultTestLoader.loadTestsFromTestCase(AdapterControls)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
