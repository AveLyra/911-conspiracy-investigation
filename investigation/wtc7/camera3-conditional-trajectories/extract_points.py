#!/usr/bin/env python3
"""Numeric-only inert extraction of two pinned public PointMass arrays."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PUBLIC = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
KIT = PUBLIC / 'camera3-provenance/kit-inventory/run-v1'
SOURCE = KIT / 'nested/Camera3-test_Camera3-test.trk'
SETTINGS = KIT / 'saved-tracker-settings.json'
MAP = PUBLIC / 'camera3-recording-comparison/wmv-diagnostic/run02/default-frames.json'
TRK_HASH = '955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c'
SET_HASH = 'ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb'
MAP_HASH = '8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2'
MASS = 'org.opensourcephysics.cabrillo.tracker.PointMass'
NUMERIC = re.compile(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\Z')


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def parse(data, expected):
    # No source-derived strings enter exceptions or output metadata.
    if len(data) > 10_000_000 or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('rejected_xml_envelope')
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        raise ValueError('invalid_xml') from None
    objects = root.findall("./property[@name='tracks']/property/object")
    masses = [obj for obj in objects if obj.get('class') == MASS]
    if len(masses) != 2:
        raise ValueError('pointmass_count_mismatch')
    result = []
    for ordinal, obj in enumerate(masses, 1):
        arrays = obj.findall("./property[@name='framedata']")
        if len(arrays) != 1:
            raise ValueError('array_count_mismatch')
        points = []
        for entry in arrays[0]:
            match = re.fullmatch(r'\[(\d+)\]', entry.get('name', ''))
            children = entry.findall('./object')
            if not match or len(children) != 1 or children[0].get('class') != MASS+'$FrameData':
                raise ValueError('frame_shape_mismatch')
            point = {'frame': int(match[1])}
            for axis in ('x', 'y'):
                fields = children[0].findall(f"./property[@name='{axis}']")
                if len(fields) != 1 or fields[0].get('type') != 'double':
                    raise ValueError('coordinate_shape_mismatch')
                literal = (fields[0].text or '').strip()
                if len(literal) > 64 or not NUMERIC.fullmatch(literal):
                    raise ValueError('non_numeric_coordinate')
                value = float(literal)
                if not math.isfinite(value):
                    raise ValueError('nonfinite_coordinate')
                point[axis+'_text'] = literal
                point[axis] = value
            points.append(point)
        if [p['frame'] for p in points] != expected:
            raise ValueError('frame_index_mismatch')
        result.append({'track': f'track{ordinal:02d}', 'pointmass_ordinal': ordinal,
                       'points': points})
    return result


def controls():
    root = ET.Element('object')
    tracks = ET.SubElement(root, 'property', name='tracks')
    for unused in range(2):
        item = ET.SubElement(tracks, 'property', name='item')
        obj = ET.SubElement(item, 'object', {'class': MASS})
        ET.SubElement(obj, 'property', name='private_synthetic_metadata').text = 'DO_NOT_EXPORT'
        arr = ET.SubElement(obj, 'property', name='framedata')
        for frame in (0, 3):
            entry = ET.SubElement(arr, 'property', name=f'[{frame}]')
            dat = ET.SubElement(entry, 'object', {'class': MASS+'$FrameData'})
            for axis in ('x', 'y'):
                ET.SubElement(dat, 'property', name=axis, type='double').text = str(frame+0.25)
    valid = ET.tostring(root)
    out = parse(valid, [0, 3])
    assert len(out) == 2 and out[1]['points'][1]['x_text'] == '3.25'
    assert 'DO_NOT_EXPORT' not in json.dumps(out) and 'private_synthetic_metadata' not in json.dumps(out)
    cases = [b'<!DOCTYPE a>'+valid, b'<!ENTITY a "b">'+valid,
             valid.replace(b'[3]', b'[0]'), valid.replace(b'3.25', b'NaN'),
             valid.replace(b'3.25', b'1e999'), valid.replace(b'3.25', b'not_numeric')]
    for data in cases:
        try:
            parse(data, [0, 3])
        except ValueError:
            continue
        raise AssertionError('negative_extraction_control_failed')
    return {'positive_numeric_allowlist': True, 'rejected_negative_cases': len(cases)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9_-]+', args.out):
        raise ValueError('invalid_output_name')
    output = HERE / args.out
    if output.exists():
        raise ValueError('output_already_exists')
    checks = controls()
    inputs = {'source_project': SOURCE, 'sanitized_settings': SETTINGS, 'frame_map': MAP,
              'protocol': HERE/'PROTOCOL.md', 'producer': Path(__file__)}
    before = {key: pin(path) for key, path in inputs.items()}
    assert before['source_project']['sha256'] == TRK_HASH
    assert before['sanitized_settings']['sha256'] == SET_HASH
    assert before['frame_map']['sha256'] == MAP_HASH
    tracks = parse(SOURCE.read_bytes(), list(range(138, 349, 3)))
    settings = json.loads(SETTINGS.read_text())
    allowed = ['xorigin','yorigin','angle','xscale','yscale','delta_t','startframe',
               'stepsize','stepcount','starttime','video_framecount']
    config = {}
    for key in allowed:
        values = [p['saved_text'] for p in settings['selected_scalar_properties']
                  if p['xml_path'].endswith('/property:'+key)]
        assert len(values) == 1 and NUMERIC.fullmatch(values[0])
        config[key] = {'text': values[0], 'value': float(values[0])}
    frames = json.loads(MAP.read_text())
    clock = []
    for index in range(138, 442):
        row = frames['records'][index]
        assert row['index'] == index
        clock.append({key: row[key] for key in ('index','pts','time_base','seconds_exact')})
    points = {'status':'conditional_saved_annotations_not_validated_material_tracks',
              'source_sha256':TRK_HASH, 'tracks':tracks, 'configuration':config,
              'current_diagnostic_clock':clock}
    after = {key: pin(path) for key, path in inputs.items()}
    assert before == after
    output.mkdir()
    point_path = output/'points.json'
    point_path.write_text(json.dumps(points,indent=2,sort_keys=True)+'\n')
    receipt = {'status':'pass_numeric_only_extraction', 'python':platform.python_version(),
               'inputs_before':before,'inputs_after':after,'controls':checks,
               'points':pin(point_path),'track_counts':[len(t['points']) for t in tracks],
               'arbitrary_source_names_paths_comments_exported':False}
    (output/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'track_counts':receipt['track_counts']}))


if __name__ == '__main__':
    main()
