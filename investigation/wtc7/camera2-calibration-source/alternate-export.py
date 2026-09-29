#!/usr/bin/env python3
"""Pinned alternate-project adapter; inert safe export and separate DOM oracle."""
import argparse
from decimal import Decimal
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import re
import sys
from xml.dom import minidom
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PARSER = HERE.parent / 'tilted-camera-source-join/project-export.py'
PARSER_SHA = '872d37a02cbbad8c8e80e2f40068e0f8e0606411c4494173bf7f3c9f24b36181'
PARSER_TEST = PARSER.with_name('project-export-tests.py')
PARSER_TEST_SHA = '62f72f9566a3b606d22b7e52ef2d44ee9020dcc5058933bd0edcecf9e655c4e1'
SOURCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
PARENT_SHA = 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
MEMBER = 'The Kit/WTC7-Dan Rather/DistantViewWTC7.trz'
MEMBER_SHA = '8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e'
PROJECT_SHA = '5aa2bea2b6532713bc9abae647e0486c937892a96d33a3892fc0f6109a11a693'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(data):
    return {'bytes': len(data), 'sha256': digest(data)}


def load_parser():
    if digest(PARSER.read_bytes()) != PARSER_SHA or digest(PARSER_TEST.read_bytes()) != PARSER_TEST_SHA:
        raise ValueError('frozen_parser_identity_mismatch')
    spec = importlib.util.spec_from_file_location('pinned_saved_state_parser', PARSER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def select_source(parent, parser, *, parent_sha, member, member_sha, project_sha, project_size):
    """No extraction: only the unique named archive and fixed entry 4, hash gated."""
    if digest(parent) != parent_sha:
        raise ValueError('parent_identity_mismatch')
    with zipfile.ZipFile(io.BytesIO(parent)) as archive:
        selected = [(i, e) for i, e in enumerate(archive.infolist()) if e.filename == member]
        if len(selected) != 1:
            raise ValueError('outer_member_not_unique')
        index, entry = selected[0]
        parser.validate_member(entry, 40_000_000)
        nested = archive.read(entry)
    if digest(nested) != member_sha:
        raise ValueError('nested_identity_mismatch')
    with zipfile.ZipFile(io.BytesIO(nested)) as archive:
        entries = archive.infolist()
        if len(entries) != 5:
            raise ValueError('nested_entry_count_mismatch')
        entry = entries[4]
        parser.validate_member(entry, 200_000)
        if entry.file_size != project_size or sum(e.filename == entry.filename for e in entries) != 1:
            raise ValueError('project_entry_mismatch')
        data = archive.read(entry)
    if len(data) != project_size or digest(data) != project_sha:
        raise ValueError('project_identity_mismatch')
    return data, {'parent': pin(parent), 'nested_archive': pin(nested), 'project': pin(data),
                  'outer_member': member, 'outer_entry_index_zero_based': index,
                  'nested_project_entry_index_zero_based': 4,
                  'nested_project_name_sha256': digest(entry.filename.encode()),
                  'raw_project_or_media_written': False}


def children(node):
    return [n for n in node.childNodes if n.nodeType == n.ELEMENT_NODE]


def body(node):
    return ''.join(n.data for n in node.childNodes if n.nodeType in {n.TEXT_NODE, n.CDATA_SECTION_NODE})


def props(node, name):
    return [n for n in children(node) if n.tagName == 'property' and n.getAttribute('name') == name]


def direct_oracle(data, result):
    """Separate minidom traversal; no parser helpers, no transformed values."""
    if len(data) > 2_000_000 or b'\0' in data or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('oracle_rejected_envelope')
    dom = minidom.parseString(data.decode('utf-8-sig'))
    root = dom.documentElement
    if root.tagName != 'object' or root.getAttribute('class') != 'org.opensourcephysics.cabrillo.tracker.TrackerPanel':
        raise ValueError('oracle_wrong_root')
    counters = {'resolved_locators': 0, 'scalar_lexical_values': 0, 'serialized_arrays': 0,
                'pointmass_tracks': 0, 'pointmass_rows': 0, 'pointmass_coordinates': 0,
                'keyframe_membership_flags': 0}

    def require(test, code):
        if not test:
            raise ValueError('oracle_' + code)

    def locate(path):
        require(bool(re.fullmatch(r'/\*\[1\](?:/\*\[[1-9][0-9]*\])*', path)), 'invalid_locator')
        node = root
        for ordinal in [int(x) for x in re.findall(r'\[(\d+)\]', path)][1:]:
            require(ordinal <= len(children(node)), 'locator_bounds')
            node = children(node)[ordinal - 1]
        counters['resolved_locators'] += 1
        return node

    def walk(item):
        if isinstance(item, list):
            for value in item:
                walk(value)
        elif isinstance(item, dict):
            if 'xml_path' in item:
                node = locate(item['xml_path'])
                if 'text_sha256' in item:
                    require(digest(body(node).strip().encode()) == item['text_sha256'], 'text_hash')
                if 'saved_text' in item and 'value' in item:
                    require(body(node).strip() == item['saved_text'], 'scalar_lexical')
                    saved = item['saved_text']
                    if type(item['value']) is bool:
                        require(item['value'] == (saved == 'true'), 'boolean_value')
                    else:
                        # Exact decimal lexical source, same representable binary numeric value.
                        require(float(Decimal(saved)) == item['value'], 'numeric_value')
                    counters['scalar_lexical_values'] += 1
            if 'serialized_xml_path' in item:
                node = locate(item['serialized_xml_path'])
                raw = body(node).strip()
                require(digest(raw.encode()) == item['serialized_text_sha256'], 'array_hash')
                if item.get('status') == 'valid_numeric_array':
                    require(raw == item['saved_text'], 'array_lexical')
                    values = [] if raw == '{}' else [Decimal(v.strip()) for v in raw[1:-1].split(',')]
                    require([float(v) for v in values] == item['values'], 'array_values')
                    counters['serialized_arrays'] += 1
            for value in item.values():
                walk(value)
    walk(result)

    source_tracks = []
    for collection in props(root, 'tracks'):
        for item in children(collection):
            source_tracks.extend(n for n in children(item) if n.tagName == 'object')
    require(len(source_tracks) == len(result['tracks']), 'all_track_count')
    source_mass = [n for n in source_tracks if n.getAttribute('class') == 'org.opensourcephysics.cabrillo.tracker.PointMass']
    require(len(source_mass) == len(result['pointmass_tracks']), 'pointmass_count')
    for raw_track, exported in zip(source_mass, result['pointmass_tracks']):
        counters['pointmass_tracks'] += 1
        require(locate(exported['xml_path']) is raw_track, 'track_locator')
        frame_arrays = props(raw_track, 'framedata')
        require(len(frame_arrays) == len(exported['framedata']), 'frame_array_count')
        saved = []
        for raw_array, array in zip(frame_arrays, exported['framedata']):
            require(len(children(raw_array)) == len(array['rows']), 'row_count')
            for raw_row, row in zip(children(raw_array), array['rows']):
                require(locate(row['xml_path']) is raw_row, 'row_locator')
                match = re.fullmatch(r'\[(\d+)\]', raw_row.getAttribute('name'))
                index = int(match.group(1)) if match else None
                require(index == row['index'], 'frame_index')
                saved.append(index)
                counters['pointmass_rows'] += 1
                raw_objects = [n for n in children(raw_row) if n.tagName == 'object']
                require(len(raw_objects) == len(row['objects']), 'frame_object_count')
                for raw_obj, obj in zip(raw_objects, row['objects']):
                    for axis in ('x', 'y'):
                        raw_fields = props(raw_obj, axis)
                        fields = obj['coordinates'][axis]['occurrences']
                        require(len(raw_fields) == len(fields), 'coordinate_count')
                        for raw_field, field in zip(raw_fields, fields):
                            require(locate(field['xml_path']) is raw_field, 'coordinate_locator')
                            require(body(raw_field).strip() == field.get('saved_text'), 'coordinate_lexical')
                            counters['pointmass_coordinates'] += 1
        require(saved == exported['saved_indices'], 'saved_index_list')
        raw_keys = props(raw_track, 'keyFrames')
        require(len(raw_keys) == len(exported['keyFrames']), 'key_array_count')
        if len(raw_keys) == 1 and exported['keyFrames_status'] == 'valid_integer_list':
            keys_text = body(props(raw_keys[0], 'array')[0]).strip()
            keys = [] if keys_text == '{}' else [int(v) for v in keys_text[1:-1].split(',')]
            require(keys == exported['keyFrames'][0]['values'], 'key_list')
            require(sorted(set(saved)-set(keys)) == exported['saved_indices_without_keyFrames'], 'nonkeys')
            require(sorted(set(keys)-set(saved)) == exported['keyFrames_without_saved_indices'], 'keys_without_rows')
            for array in exported['framedata']:
                for row in array['rows']:
                    require(row['saved_keyFrame_member'] == (row['index'] in keys), 'key_membership')
                    counters['keyframe_membership_flags'] += 1

    objects = list(root.getElementsByTagName('object'))
    clips = [n for n in objects if n.getAttribute('class') == 'org.opensourcephysics.media.core.VideoClip']
    require(len(clips) == 1, 'single_clip_required')
    values = {name: int(body(props(clips[0], name)[0])) for name in ['video_framecount', 'startframe', 'stepsize', 'stepcount']}
    video_domain = set(range(values['video_framecount']))
    step_domain = set(values['startframe'] + i*values['stepsize'] for i in range(values['stepcount']))
    require(result['saved_clip_domain']['video_frame_indices'] == sorted(video_domain), 'video_domain')
    require(result['saved_clip_domain']['saved_clip_step_indices'] == sorted(step_domain), 'step_domain')
    for track in result['pointmass_tracks']:
        saved = set(track['saved_indices'])
        for key, expected in [('missing_video_frame_indices', video_domain-saved),
                              ('missing_clip_step_indices', step_domain-saved),
                              ('indices_outside_saved_video_domain', saved-video_domain),
                              ('indices_outside_saved_clip_steps', saved-step_domain)]:
            require(track[key] == sorted(expected), key)
    return {'status': 'passed', 'method': 'distinct minidom DOM traversal and Decimal lexical checks; same archived evidence, not an independent witness', **counters}


def target_path(name):
    if name not in {'alternate-export01.json', 'alternate-export02.json'}:
        raise ValueError('invalid_output_name')
    target = HERE / name
    if target.exists() or target.is_symlink():
        raise ValueError('output_already_exists')
    return target


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--out', required=True)
    args = cli.parse_args()
    target = target_path(args.out)
    script_before = Path(__file__).read_bytes()
    tests_before = (HERE / 'alternate-tests.py').read_bytes()
    protocol_before = (HERE / 'PROTOCOL.md').read_bytes()
    parser = load_parser()
    parent = SOURCE.read_bytes()
    if len(parent) != 172774879:
        raise ValueError('parent_size_mismatch')
    data, provenance = select_source(parent, parser, parent_sha=PARENT_SHA, member=MEMBER,
                                      member_sha=MEMBER_SHA, project_sha=PROJECT_SHA, project_size=68489)
    result = parser.parse_project(data)
    result['direct_xml_verification'] = direct_oracle(data, result)
    provenance['source_unchanged_after_read'] = pin(SOURCE.read_bytes()) == pin(parent)
    if not provenance['source_unchanged_after_read']:
        raise ValueError('source_changed')
    if script_before != Path(__file__).read_bytes() or tests_before != (HERE/'alternate-tests.py').read_bytes() or protocol_before != (HERE/'PROTOCOL.md').read_bytes():
        raise ValueError('producer_or_protocol_changed')
    load_parser()
    result['provenance'] = provenance
    result['producer'] = {'adapter': pin(script_before), 'adapter_tests': pin(tests_before),
                          'parser': pin(PARSER.read_bytes()), 'parser_tests': pin(PARSER_TEST.read_bytes()),
                          'protocol': pin(protocol_before), 'python': platform.python_version()}
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
    with target.open('xb') as stream:
        stream.write(payload)
    print(json.dumps({'status': result['status'], 'output': target.name, 'receipt': pin(payload),
                      'pointmass_count': len(result['pointmass_tracks']),
                      'row_counts': [len(t['saved_indices']) for t in result['pointmass_tracks']],
                      'verification': result['direct_xml_verification']}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        code = str(error) if isinstance(error, ValueError) and re.fullmatch('[a-z_]+', str(error)) else 'source_or_output_operation_failed'
        print(json.dumps({'status': 'failed', 'code': code}), file=sys.stderr)
        sys.exit(1)
