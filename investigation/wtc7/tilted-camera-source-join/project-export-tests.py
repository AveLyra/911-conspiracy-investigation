#!/usr/bin/env python3
"""Synthetic controls for project-export.py; no real project point values."""
import copy
import importlib.util
import json
from pathlib import Path
import stat
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('project_export', Path(__file__).with_name('project-export.py'))
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


def prop(parent, name, kind, value=None):
    node = ET.SubElement(parent, 'property', name=name, type=kind)
    if value is not None:
        node.text = str(value)
    return node


def fixture():
    root = ET.Element('object', {'class': subject.TRACKER+'TrackerPanel'})
    video = ET.SubElement(prop(root, 'videoclip', 'object'), 'object', {'class': subject.MEDIA+'VideoClip'})
    for k, v in [('video_framecount', 7), ('startframe', 0), ('stepsize', 3), ('stepcount', 3)]:
        prop(video, k, 'int', v)
    prop(video, 'starttime', 'double', '-200.0')
    prop(video, 'private_payload', 'string', 'DO_NOT_EXPORT /private/person@example.invalid')
    tracks = prop(root, 'tracks', 'collection')
    obj = ET.SubElement(prop(tracks, 'item', 'object'), 'object', {'class': subject.MASS})
    prop(obj, 'name', 'string', 'DO_NOT_EXPORT')
    prop(obj, 'mass', 'double', '1.0')
    frames = prop(obj, 'framedata', 'array')
    for frame in [0, 6]:
        row = ET.SubElement(prop(frames, f'[{frame}]', 'object'), 'object', {'class': subject.MASS+'$FrameData'})
        prop(row, 'x', 'double', str(frame+0.125))
        prop(row, 'y', 'double', str(8-frame))
    keys = prop(obj, 'keyFrames', 'array')
    keys.set('class', '[I')
    prop(keys, 'array', 'string', '{0}')
    return root, obj, frames


def parse(root):
    return subject.parse_project(ET.tostring(root))


def first_track(root):
    return parse(root)['pointmass_tracks'][0]


class ExportControls(unittest.TestCase):
    def test_sparse_retained_with_explicit_missing_and_key_membership(self):
        root, _, _ = fixture()
        track = first_track(root)
        self.assertEqual(track['saved_indices'], [0, 6])
        self.assertEqual(track['missing_video_frame_indices'], [1, 2, 3, 4, 5])
        self.assertEqual(track['missing_clip_step_indices'], [3])
        self.assertEqual(track['saved_indices_without_keyFrames'], [6])
        self.assertEqual(track['framedata'][0]['finite_complete_count'], 2)

    def test_duplicate_indices_retained_and_flagged(self):
        root, _, frames = fixture()
        frames.append(copy.deepcopy(frames[0]))
        track = first_track(root)
        self.assertEqual(track['saved_indices'], [0, 6, 0])
        self.assertEqual(track['framedata'][0]['duplicate_indices'], [0])

    def test_duplicate_coordinate_is_not_single_usable_value(self):
        root, _, frames = fixture()
        frames[0][0].append(copy.deepcopy(frames[0][0][0]))
        row = first_track(root)['framedata'][0]['rows'][0]
        self.assertFalse(row['finite_complete'])
        self.assertEqual(row['objects'][0]['coordinates']['x']['status'], 'duplicate')
        self.assertEqual(len(row['objects'][0]['coordinates']['x']['occurrences']), 2)

    def test_missing_coordinate_preserved(self):
        root, _, frames = fixture()
        frames[0][0].remove(frames[0][0][1])
        row = first_track(root)['framedata'][0]['rows'][0]
        self.assertFalse(row['finite_complete'])
        self.assertEqual(row['objects'][0]['coordinates']['y']['status'], 'missing')

    def test_nonfinite_and_private_literals_not_values(self):
        for value in ['NaN', 'Infinity', '-Infinity', '1e999', 'DO_NOT_EXPORT']:
            with self.subTest(value=value):
                root, _, frames = fixture()
                frames[0][0][0].text = value
                result = parse(root)
                row = result['pointmass_tracks'][0]['framedata'][0]['rows'][0]
                self.assertFalse(row['finite_complete'])
                exported = row['objects'][0]['coordinates']['x']['occurrences'][0]
                self.assertNotIn('value', exported)
                self.assertNotIn('saved_text', exported)
                self.assertNotIn('DO_NOT_EXPORT', json.dumps(result, allow_nan=False))

    def test_unexpected_frame_object_class_retained_unusable(self):
        root, _, frames = fixture()
        frames[0][0].set('class', 'private/DO_NOT_EXPORT')
        row = first_track(root)['framedata'][0]['rows'][0]
        self.assertFalse(row['finite_complete'])
        self.assertEqual(row['objects'][0]['status'], 'unexpected_class')

    def test_bad_and_negative_indices_preserved_unusable(self):
        for name in ['[-1]', '[bad]', '[000000000000000000001]', '/DO_NOT_EXPORT']:
            root, _, frames = fixture()
            frames[0].set('name', name)
            row = first_track(root)['framedata'][0]['rows'][0]
            self.assertIsNone(row['index'])
            self.assertFalse(row['finite_complete'])

    def test_duplicate_arrays_and_missing_arrays(self):
        root, obj, frames = fixture()
        obj.append(copy.deepcopy(frames))
        self.assertEqual(first_track(root)['framedata_array_count'], 2)
        obj.remove(frames)
        obj.remove(obj[-1])
        self.assertEqual(first_track(root)['framedata_array_count'], 0)

    def test_duplicate_missing_or_bad_keyframes(self):
        root, obj, _ = fixture()
        keys = obj.find("./property[@name='keyFrames']")
        keys[0].text = '{0,0,6}'
        self.assertEqual(first_track(root)['duplicate_keyFrames'], [0])
        keys[0].text = '{NaN}'
        self.assertEqual(first_track(root)['keyFrames_status'], 'missing_or_unexpected')
        obj.remove(keys)
        self.assertEqual(first_track(root)['keyFrames_status'], 'missing_or_unexpected')

    def test_ddt_entities_utf16_and_malformed_xml_rejected(self):
        root, _, _ = fixture()
        good = ET.tostring(root)
        for bad in [b'<!DOCTYPE object>'+good, b'<!ENTITY x "foo">'+good,
                    '<!DOCTYPE object><object/>'.encode('utf-16'), b'<bad>']:
            with self.assertRaises(ValueError):
                subject.parse_project(bad)

    def test_root_schema_rejected_and_duplicate_track_container_flagged(self):
        with self.assertRaisesRegex(ValueError, 'unexpected_root_schema'):
            subject.parse_project(b'<object class="private/DO_NOT_EXPORT"/>')
        root, _, _ = fixture()
        root.append(copy.deepcopy(root.find("./property[@name='tracks']")))
        result = parse(root)
        self.assertIn('track_container_count_not_one', result['anomalies'])
        self.assertEqual(len(result['pointmass_tracks']), 2)

    def test_ordinal_paths_resolve_every_numeric_value(self):
        root, _, _ = fixture()
        result = parse(root)
        def inspect(item):
            if isinstance(item, dict):
                if 'saved_text' in item and 'xml_path' in item and 'value' in item:
                    import re
                    indices = [int(v) for v in re.findall(r'\[(\d+)\]', item['xml_path'])]
                    self.assertEqual(indices[0], 1)
                    node = root
                    for index in indices[1:]:
                        node = list(node)[index-1]
                    self.assertEqual(item['saved_text'], node.text)
                for value in item.values():
                    inspect(value)
            elif isinstance(item, list):
                for value in item:
                    inspect(value)
        inspect(result)

    def test_filter_referenceframe_and_time_source_visibility(self):
        root, _, _ = fixture()
        filters = prop(root, 'filters', 'object')
        obj = ET.SubElement(filters, 'object', {'class': 'private/DO_NOT_EXPORTFilter'})
        prop(obj, 'angle', 'double', '90.0')
        prop(obj, 'private/DO_NOT_EXPORT', 'string', 'DO_NOT_EXPORT')
        prop(root, 'referenceframe', 'int', 3)
        prop(root, 'timesource', 'int', 2)
        result = parse(root)
        self.assertGreater(result['special_state']['filters']['candidate_count'], 0)
        self.assertEqual(result['special_state']['referenceframes']['candidate_count'], 1)
        self.assertEqual(result['special_state']['time_sources']['candidate_count'], 1)
        self.assertNotIn('DO_NOT_EXPORT', json.dumps(result))

    def test_source_metadata_and_labels_allowlist(self):
        root, obj, _ = fixture()
        result = parse(root)
        self.assertNotIn('DO_NOT_EXPORT', json.dumps(result))
        self.assertNotIn('person@example.invalid', json.dumps(result))
        obj.find("./property[@name='name']").text = 'NW Corner'
        self.assertEqual(first_track(root)['names'][0]['source_name']['label'], 'NW Corner')
        self.assertEqual(first_track(root)['track_id'], 'pointmass01')

    def test_archive_paths_symlinks_sizes_and_encryption_rejected(self):
        for path in ['../project.trk', '/project.trk', 'C:/project.trk', 'a\\project.trk', 'a/../../project.trk']:
            info = zipfile.ZipInfo(path)
            info.file_size = 100
            with self.assertRaisesRegex(ValueError, 'rejected_archive_member'):
                subject.validate_member(info, 1000)
        for kind in ['symlink', 'oversize', 'encrypted', 'empty']:
            info = zipfile.ZipInfo('project.trk')
            info.file_size = 100
            if kind == 'symlink':
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
            elif kind == 'oversize':
                info.file_size = 1001
            elif kind == 'encrypted':
                info.flag_bits = 1
            else:
                info.file_size = 0
            with self.assertRaisesRegex(ValueError, 'rejected_archive_member'):
                subject.validate_member(info, 1000)

    def test_output_path_guard(self):
        for value in ['/tmp/project01.json', '../project01.json', 'subdir/project01.json', 'project00.json']:
            with self.assertRaisesRegex(ValueError, 'invalid_output_name'):
                subject.output_path(value)

    def test_deterministic_result(self):
        root, _, _ = fixture()
        self.assertEqual(json.dumps(parse(root), sort_keys=True), json.dumps(parse(root), sort_keys=True))


if __name__ == '__main__':
    unittest.main(verbosity=2)
