#!/usr/bin/env python3
"""Inert, sanitized export of one byte-pinned public Tracker project.

No media decode, archive extraction, project execution, coordinate conversion,
table selection, or network access. XML locators index *element children* from
the document root: /*[1]/*[7] is its seventh element child (XPath 1-based).
"""
import argparse
import collections
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
PARENT_HASH = 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
OUTER_NAME = 'The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz'
OUTER_HASH = '7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552'
TRK_HASH = 'babf332bd340c1e902870f14d4370eab4f3a54de388ce06c1ca85ae222b1b5da'
TRK_NAME_HASH = '40d861420e948192e232ab4bd5c6ae347211e14bd8cfc2a0d0a388f04aa08bf0'
TRACKER = 'org.opensourcephysics.cabrillo.tracker.'
MEDIA = 'org.opensourcephysics.media.core.'
MASS = TRACKER + 'PointMass'
COORD = MEDIA + 'ImageCoordSystem'
TAPE = TRACKER + 'TapeMeasure'
KNOWN_CLASSES = {TRACKER+'TrackerPanel', TRACKER+'CoordAxes', MASS,
                 MASS+'$FrameData', COORD, COORD+'$FrameData', TAPE,
                 TAPE+'$FrameData', MEDIA+'VideoClip', MEDIA+'StepperClipControl',
                 'org.opensourcephysics.media.xuggle.XuggleVideo',
                 MEDIA+'VideoClipControl', MEDIA+'ReferenceFrame',
                 TRACKER+'ParticleDataTrack', TRACKER+'DataTrack',
                 'java.awt.Color', 'java.util.ArrayList', '[I', '[D'}
NUMBER = re.compile(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\Z')
INDEX = re.compile(r'\[(\d{1,7})\]\Z')
LABEL_WORDS = set('roof roofline penthouse east west north south left right upper lower corner edge point mass line top bottom building eph wph window nw ne sw se w e s n ur ul lr ll tower mid center'.split())
LABEL_ALLOWLIST = {'NW Corner', 'Mid E Penthouse', 'NE Corner', 'W Penthouse'}
NUMERIC_SETTINGS = {
    TRACKER+'TrackerPanel': ['width', 'height', 'magnification', 'center_x', 'center_y', 'units_visible'],
    MEDIA+'VideoClip': ['video_framecount', 'startframe', 'stepsize', 'stepcount', 'starttime', 'playallsteps'],
    MEDIA+'StepperClipControl': ['rate', 'delta_t', 'frame'],
    MEDIA+'VideoClipControl': ['rate', 'delta_t', 'frame'],
    COORD: ['fixedorigin', 'fixedangle', 'fixedscale', 'locked'],
    COORD+'$FrameData': ['xorigin', 'yorigin', 'angle', 'xscale', 'yscale'],
    TAPE: ['fixedtape', 'fixedlength', 'readonly', 'stickmode'],
    TAPE+'$FrameData': ['x1', 'y1', 'x2', 'y2'],
    MASS: ['mass', 'visible', 'trail', 'autofill', 'dependent', 'locked', 'start_frame', 'end_frame'],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(data):
    return {'bytes': len(data), 'sha256': sha(data)}


def identity(value, allow=()):
    value = value or ''
    out = {'sha256': sha(value.encode()), 'characters': len(value)}
    if value in allow:
        out['label'] = value
    return out


def validate_member(info, maximum):
    """Validate but never use an archive path as a filesystem destination."""
    name = info.filename
    parts = PurePosixPath(name).parts
    if (not name or '\\' in name or '\x00' in name or ':' in name or
            name.startswith('/') or '..' in parts or info.is_dir() or
            info.file_size < 1 or info.file_size > maximum or info.flag_bits & 1 or
            stat.S_ISLNK(info.external_attr >> 16)):
        raise ValueError('rejected_archive_member')


def load_source():
    before = SOURCE.read_bytes()
    if len(before) != 172774879 or sha(before) != PARENT_HASH:
        raise ValueError('parent_hash_or_size_mismatch')
    with zipfile.ZipFile(io.BytesIO(before)) as outer:
        selected = [(i, q) for i, q in enumerate(outer.infolist()) if q.filename == OUTER_NAME]
        if len(selected) != 1:
            raise ValueError('outer_member_not_unique')
        outer_index, info = selected[0]
        validate_member(info, 20_000_000)
        nested = outer.read(info)
    if len(nested) != 15608229 or sha(nested) != OUTER_HASH:
        raise ValueError('nested_hash_or_size_mismatch')
    with zipfile.ZipFile(io.BytesIO(nested)) as archive:
        entries = archive.infolist()
        if len(entries) != 5:
            raise ValueError('nested_entry_count_mismatch')
        info = entries[4]  # Explicitly zero-based: the fifth entry is the TRK.
        validate_member(info, 200_000)
        if (info.file_size != 161200 or sha(info.filename.encode()) != TRK_NAME_HASH or
                sum(sha(q.filename.encode()) == TRK_NAME_HASH for q in entries) != 1):
            raise ValueError('project_member_mismatch')
        data = archive.read(info)
    if len(data) != 161200 or sha(data) != TRK_HASH:
        raise ValueError('project_hash_or_size_mismatch')
    if pin(SOURCE.read_bytes()) != pin(before):
        raise ValueError('source_changed_during_read')
    return data, {'parent': pin(before), 'nested_archive': pin(nested),
                  'project': pin(data), 'outer_member': OUTER_NAME,
                  'outer_entry_index_zero_based': outer_index,
                  'nested_project_entry_index_zero_based': 4,
                  'nested_project_name_sha256': TRK_NAME_HASH,
                  'raw_project_or_media_written': False,
                  'source_unchanged_after_read': True}


def parse_xml(data):
    if len(data) > 2_000_000 or b'\x00' in data or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('rejected_xml_envelope')
    try:
        data.decode('utf-8-sig')
        root = ET.fromstring(data)
    except (UnicodeDecodeError, ET.ParseError):
        raise ValueError('invalid_utf8_xml') from None
    if root.tag != 'object' or root.get('class') != TRACKER+'TrackerPanel':
        raise ValueError('unexpected_root_schema')
    nodes, paths = list(root.iter()), {}
    if len(nodes) > 20000:
        raise ValueError('xml_node_limit')
    def locate(node, path, depth):
        if depth > 40:
            raise ValueError('xml_depth_limit')
        paths[node] = path
        for i, child in enumerate(node, 1):
            locate(child, path + f'/*[{i}]', depth+1)
    locate(root, '/*[1]', 0)
    return root, paths


def number(node, paths):
    text = (node.text or '').strip()
    out = {'xml_path': paths[node], 'type': identity(node.get('type'), {'double', 'int', 'boolean', 'string'}),
           'text_sha256': sha(text.encode())}
    if len(node):
        out['status'] = 'unexpected_children'
    elif node.get('type') == 'boolean' and text in {'true', 'false'}:
        out.update(status='valid_boolean', saved_text=text, value=text == 'true')
    elif node.get('type') not in {'double', 'int'}:
        out['status'] = 'unexpected_numeric_type'
    elif len(text) > 80 or not NUMBER.fullmatch(text):
        out['status'] = 'nonfinite' if text.lower() in {'nan', 'infinity', '-infinity', '+infinity', 'inf', '-inf', '+inf'} else 'invalid_numeric_literal'
    else:
        value = float(text)
        if not math.isfinite(value):
            out['status'] = 'nonfinite'
        elif node.get('type') == 'int' and not re.fullmatch(r'[+-]?\d+', text):
            out['status'] = 'invalid_integer_literal'
        else:
            out.update(status='valid_finite', saved_text=text,
                       value=int(text) if node.get('type') == 'int' else value)
    return out


def field(obj, name, paths):
    found = [n for n in obj if n.tag == 'property' and n.get('name') == name]
    return {'property': name, 'status': 'missing' if not found else 'present' if len(found) == 1 else 'duplicate',
            'occurrences': [number(n, paths) for n in found]}


def numeric_array(node, paths):
    """OSP serialized primitive array; reject arbitrary text, retain invalid state."""
    children = list(node)
    out = {'xml_path': paths[node], 'array_class': identity(node.get('class'), {'[I', '[D'}),
           'child_count': len(children), 'values': []}
    if len(children) == 1 and children[0].get('name') == 'array' and children[0].get('type') == 'string':
        child = children[0]
        text = (child.text or '').strip()
        out.update(serialized_xml_path=paths[child], serialized_text_sha256=sha(text.encode()))
        if len(text) < 500000 and re.fullmatch(r'\{[^{}]*\}', text):
            tokens = [] if text == '{}' else text[1:-1].split(',')
            if all(len(t.strip()) <= 80 and NUMBER.fullmatch(t.strip()) for t in tokens):
                values = [float(t.strip()) for t in tokens]
                if all(math.isfinite(v) for v in values):
                    if node.get('class') != '[I' or all(re.fullmatch(r'[+-]?\d+', t.strip()) for t in tokens):
                        out.update(status='valid_numeric_array', saved_text=text,
                                   values=[int(t.strip()) for t in tokens] if node.get('class') == '[I' else values)
                        return out
    # Arrays such as worldlengths may instead have index-named scalar children.
    if children and all(INDEX.fullmatch(c.get('name', '')) and c.get('type') in {'double', 'int'} for c in children):
        out.update(status='indexed_numeric_array', entries=[dict(index=int(INDEX.fullmatch(c.get('name')).group(1)), **number(c, paths)) for c in children])
    else:
        out['status'] = 'unexpected_or_nonfinite_numeric_array'
    return out


def framedata(node, paths, data_class, axes):
    out = {'xml_path': paths[node], 'entry_count': len(node), 'rows': []}
    for ordinal, entry in enumerate(node, 1):
        match = INDEX.fullmatch(entry.get('name', ''))
        row = {'entry_ordinal_one_based': ordinal, 'xml_path': paths[entry],
               'index': int(match.group(1)) if match else None,
               'index_name': identity(entry.get('name')),
               'status': 'saved_object', 'objects': []}
        objects = [c for c in entry if c.tag == 'object']
        if not match or entry.tag != 'property' or entry.get('type') != 'object' or len(objects) != 1 or len(entry) != 1:
            row['status'] = 'unexpected_entry_schema'
        for obj in objects:
            current = {'xml_path': paths[obj], 'class': identity(obj.get('class'), KNOWN_CLASSES),
                       'status': 'expected_class' if obj.get('class') == data_class else 'unexpected_class',
                       'coordinates': {axis: field(obj, axis, paths) for axis in axes},
                       'unexpected_field_count': sum(c.get('name') not in axes or c.tag != 'property' for c in obj)}
            current['finite_complete'] = current['status'] == 'expected_class' and all(
                f['status'] == 'present' and f['occurrences'][0]['status'] == 'valid_finite'
                for f in current['coordinates'].values())
            row['objects'].append(current)
        row['finite_complete'] = row['status'] == 'saved_object' and len(row['objects']) == 1 and row['objects'][0]['finite_complete']
        out['rows'].append(row)
    indices = [r['index'] for r in out['rows'] if r['index'] is not None]
    out['duplicate_indices'] = sorted(i for i, count in collections.Counter(indices).items() if count > 1)
    out['finite_complete_count'] = sum(r['finite_complete'] for r in out['rows'])
    return out


def parse_project(data):
    root, paths = parse_xml(data)
    result = {'schema_version': 1, 'status': 'sanitized_saved_state_only',
              'path_convention': 'Absolute XPath element-child positions; /*[1] is the document root; all brackets are one-based.',
              'settings_objects': [], 'coordinate_arrays': [], 'tape_arrays': [],
              'tracks': [], 'pointmass_tracks': [], 'special_state': {}, 'anomalies': []}
    for obj in root.iter('object'):
        cls = obj.get('class', '')
        if cls in NUMERIC_SETTINGS:
            result['settings_objects'].append({'xml_path': paths[obj], 'class': cls,
                                              'fields': {k: field(obj, k, paths) for k in NUMERIC_SETTINGS[cls]}})
        if cls in {COORD, TAPE}:
            arrays = [n for n in obj if n.get('name') == 'framedata']
            target = 'coordinate_arrays' if cls == COORD else 'tape_arrays'
            result[target].append({'object_xml_path': paths[obj], 'array_count': len(arrays),
                                   'arrays': [framedata(n, paths, cls+'$FrameData',
                                              ['xorigin', 'yorigin', 'angle', 'xscale', 'yscale'] if cls == COORD else ['x1', 'y1', 'x2', 'y2']) for n in arrays],
                                   'worldlengths': [numeric_array(n, paths) for n in obj if n.get('name') == 'worldlengths']})
    for name in ['semantic_version', 'length_unit', 'mass_unit']:
        candidates = [n for n in root if n.get('name') == name]
        allowed = {'m', 'kg', 'cm', 'mm', 'ft', 'g'}
        if name == 'semantic_version':
            allowed = {n.text for n in candidates if re.fullmatch(r'\d{1,3}\.\d{1,3}\.\d{1,3}', n.text or '')}
        result[name] = [{'xml_path': paths[n], 'value': identity(n.text, allowed)} for n in candidates]
    containers = [n for n in root if n.get('name') == 'tracks']
    result['track_container_count'] = len(containers)
    if len(containers) != 1:
        result['anomalies'].append('track_container_count_not_one')
    for container in containers:
        for item in container:
            objects = [n for n in item if n.tag == 'object']
            if item.tag != 'property' or item.get('name') != 'item' or item.get('type') != 'object' or len(objects) != 1:
                result['anomalies'].append({'kind': 'unexpected_track_item_schema', 'xml_path': paths[item]})
            for obj in objects:
                ordinal = len(result['tracks'])+1
                info = {'track_item_ordinal_one_based': ordinal, 'xml_path': paths[obj],
                        'class': identity(obj.get('class'), KNOWN_CLASSES)}
                result['tracks'].append(info)
                if obj.get('class') != MASS:
                    continue
                pmordinal = len(result['pointmass_tracks'])+1
                arrays = [n for n in obj if n.get('name') == 'framedata']
                keys = [numeric_array(n, paths) for n in obj if n.get('name') == 'keyFrames']
                info = dict(info, track_id=f'pointmass{pmordinal:02d}', pointmass_ordinal_one_based=pmordinal,
                            names=[{'xml_path': paths[n], 'source_name': identity(n.text, LABEL_ALLOWLIST)} for n in obj if n.get('name') == 'name'],
                            framedata_array_count=len(arrays),
                            framedata=[framedata(n, paths, MASS+'$FrameData', ['x', 'y']) for n in arrays],
                            keyFrames_array_count=len(keys), keyFrames=keys,
                            other_array_states=[{'xml_path': paths[n], 'property': identity(n.get('name')), 'child_count': len(n)} for n in obj if n.get('type') == 'array' and n.get('name') not in {'framedata', 'keyFrames'}])
                key_valid = len(keys) == 1 and keys[0]['status'] == 'valid_numeric_array' and all(isinstance(i, int) and i >= 0 for i in keys[0]['values'])
                keylist = keys[0]['values'] if key_valid else []
                info['keyFrames_status'] = 'valid_integer_list' if key_valid else 'missing_or_unexpected'
                info['duplicate_keyFrames'] = sorted(i for i, count in collections.Counter(keylist).items() if count > 1)
                saved = [r['index'] for a in info['framedata'] for r in a['rows'] if r['index'] is not None]
                info['saved_indices'] = saved
                info['saved_indices_without_keyFrames'] = sorted(set(saved)-set(keylist)) if key_valid else None
                info['keyFrames_without_saved_indices'] = sorted(set(keylist)-set(saved)) if key_valid else None
                for array in info['framedata']:
                    for row in array['rows']:
                        row['saved_keyFrame_member'] = row['index'] in keylist if key_valid else None
                result['pointmass_tracks'].append(info)
    if not result['pointmass_tracks']:
        result['anomalies'].append('no_pointmass_tracks')
    # Literal saved overrides or filters are kept separate from absent/default behavior.
    for group, predicate in {
        'filters': lambda n: 'filter' in n.get('name', '').lower() or 'filter' in n.get('class', '').lower(),
        'referenceframes': lambda n: 'referenceframe' in n.get('name', '').lower() or 'referenceframe' in n.get('class', '').lower(),
        'time_sources': lambda n: any(s in n.get('name', '').lower() or s in n.get('class', '').lower() for s in ['timesource', 'datatrack']),
        'autofill_or_dependent': lambda n: any(s in n.get('name', '').lower() for s in ['autofill', 'dependent']),
    }.items():
        found = [n for n in root.iter() if predicate(n)]
        result['special_state'][group] = {'candidate_count': len(found), 'status': 'absent_in_saved_xml' if not found else 'present_review_required',
            'candidates': [{'xml_path': paths[n], 'name': identity(n.get('name')), 'class': identity(n.get('class'), KNOWN_CLASSES),
                            'numeric_fields': [dict(property=identity(q.get('name')), **number(q, paths)) for q in n.iter() if q.get('type') in {'int', 'double', 'boolean'}],
                            'non_numeric_leaf_count': sum(not len(q) and q.get('type') not in {'int', 'double', 'boolean'} for q in n.iter())} for n in found]}
    # Missing state is relative to the literal saved clip domain, never interpolated.
    clips = [o for o in result['settings_objects'] if o['class'] == MEDIA+'VideoClip']
    domain = None
    if len(clips) == 1:
        values = {}
        for k in ['video_framecount', 'startframe', 'stepsize', 'stepcount']:
            f = clips[0]['fields'][k]
            if f['status'] == 'present' and f['occurrences'][0]['status'] == 'valid_finite':
                values[k] = f['occurrences'][0]['value']
        if len(values) == 4 and all(type(v) is int for v in values.values()) and 0 < values['video_framecount'] <= 100000 and 0 < values['stepsize'] <= 100000 and 0 < values['stepcount'] <= 100000 and values['startframe'] >= 0:
            domain = {'video_frame_indices': list(range(values['video_framecount'])),
                      'saved_clip_step_indices': [values['startframe']+i*values['stepsize'] for i in range(values['stepcount'])]}
    result['saved_clip_domain'] = domain
    for track in result['pointmass_tracks']:
        have = set(track['saved_indices'])
        track['missing_video_frame_indices'] = sorted(set(domain['video_frame_indices'])-have) if domain else None
        track['missing_clip_step_indices'] = sorted(set(domain['saved_clip_step_indices'])-have) if domain else None
        track['indices_outside_saved_video_domain'] = sorted(have-set(domain['video_frame_indices'])) if domain else None
        track['indices_outside_saved_clip_steps'] = sorted(have-set(domain['saved_clip_step_indices'])) if domain else None
    return result


def output_path(name):
    if name not in {'project01.json', 'project02.json'}:
        raise ValueError('invalid_output_name')
    path = HERE/name
    if path.exists() or path.is_symlink():
        raise ValueError('output_already_exists')
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    target = output_path(args.out)
    data, receipt = load_source()
    result = parse_project(data)
    result['provenance'] = receipt
    result['producer'] = {'script': pin(Path(__file__).read_bytes()), 'tests': pin((HERE/'project-export-tests.py').read_bytes()),
                          'python': platform.python_version()}
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
    with target.open('xb') as stream:
        stream.write(payload)
    print(json.dumps({'status': result['status'], 'output': target.name, 'output_receipt': pin(payload),
                      'pointmass_count': len(result['pointmass_tracks']),
                      'row_counts': [len(t['saved_indices']) for t in result['pointmass_tracks']]}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        # Do not echo exception text from archive, XML, or filesystem libraries.
        code = str(error) if isinstance(error, ValueError) and re.fullmatch('[a-z_]+', str(error)) else 'source_or_output_operation_failed'
        print(json.dumps({'status': 'failed', 'code': code}), file=sys.stderr)
        sys.exit(1)
