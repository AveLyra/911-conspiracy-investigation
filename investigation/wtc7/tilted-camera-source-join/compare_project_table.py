#!/usr/bin/env python3
"""Frozen all-row saved-project/printed-table correspondence test.

TABLE-ADDENDUM.md controls formulas, time join, pairings and enclosures.
No fit, alternative lag, label assignment, physical calibration or causal test.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
UNIT = HERE.parent/'multipoint-table-reproduction'
PINS = {
    'project01.json': '4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8',
    'TABLE-ADDENDUM.md': 'f5597785cac2a11a7680bd9f051df8455a5f190387544ac6ef675ee907a108e1',
    'probe01/probe.json': '778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de',
    'source/receipt.json': 'a100331b8e5e66ebb41959811e3ff650750e8284fdba0e4c8dcebdd736ed8ea9',
    'source-semantics-pins.json': 'e32f24714f206f5fdbaad19fc1aa16dad278d66119c7ee88ef11201a02c37cc5',
    '../multipoint-table-reproduction/transcription-root/table47.json': 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc',
    '../multipoint-table-reproduction/reconciliation.json': '2aba8ca61b1ef8461654cfcab4b4cd86847660259576a9038aa6015e4ccc0fe6',
    '../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf': 'cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394',
}
PAIRINGS = [('X', 'ref_x'), ('Y', 'ref_y'), ('Y', 'ne_y'),
            ('Y', 'ec_y'), ('Y', 'wc_y'), ('Y', 'nw_y')]
TOLERANCE = Fraction(1, 10**9)


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def inverse(x, y, xo, yo, degrees, sx, sy):
    if not all(math.isfinite(v) for v in [x, y, xo, yo, degrees, sx, sy]) or sx == 0 or sy == 0:
        raise ValueError('invalid_transform')
    theta = math.radians(degrees)
    c, s = math.cos(theta), math.sin(theta)
    u, v = x-xo, y-yo
    return {'X': c*u/sx-s*v/sy, 'Y': -s*u/sx-c*v/sy}


def nearest_grid(value, spacing=Fraction(1, 5)):
    """Exact nearest multiple; exact half ties away from zero."""
    quotient = abs(value)/spacing
    index = (2*quotient.numerator+quotient.denominator)//(2*quotient.denominator)
    return (1 if value >= 0 else -1)*index*spacing


def uniform_clock(frame, duration_ms, origin_ms):
    return (origin_ms+frame*duration_ms)/1000


def endpoint_clock(frame, times_ms, a, b, duration_ms, origin_ms):
    if a >= b or a < 0 or b >= len(times_ms) or times_ms[b] <= times_ms[a] or not a <= frame <= b:
        raise ValueError('invalid_clock_domain')
    stretch = duration_ms*(b-a)/(times_ms[b]-times_ms[a])
    return (origin_ms+stretch*(times_ms[frame]-times_ms[a]))/1000


def rational(value):
    return {'exact_fraction': str(value), 'value': float(value)}


def enclosure(residual, width):
    magnitude = abs(Fraction(str(residual)))
    return {'residual': residual, 'printed_half_width': float(width),
            'print_enclosure_compatible': magnitude <= width,
            'with_arithmetic_tolerance_compatible': magnitude <= width+TOLERANCE,
            'arithmetic_tolerance': float(TOLERANCE)}


def stats(rows, diagnostic):
    values = [row[diagnostic] for row in rows if row.get(diagnostic) is not None]
    residuals = [v['residual'] for v in values]
    return {'available_count': len(values),
            'print_enclosure_pass_count': sum(v['print_enclosure_compatible'] for v in values),
            'with_arithmetic_tolerance_pass_count': sum(v['with_arithmetic_tolerance_compatible'] for v in values),
            'all_available_compatible': bool(values) and all(v['with_arithmetic_tolerance_compatible'] for v in values),
            'maximum_absolute_residual': max(map(abs, residuals)) if residuals else None,
            'signed_residual_minimum': min(residuals) if residuals else None,
            'signed_residual_maximum': max(residuals) if residuals else None}


def join_pair(track_id, saved, table_rows, axis, column, source_hash):
    saved_by_time = {}
    for row in saved:
        key = Fraction(row['nominal_grid_time_s']['exact_fraction'])
        if key in saved_by_time:
            raise ValueError('ambiguous_saved_grid_join')
        saved_by_time[key] = row
    paper_by_time = {}
    for row in table_rows:
        key = Fraction(row['time_s'])
        if key in paper_by_time:
            raise ValueError('duplicate_printed_time')
        paper_by_time[key] = row
    result = {'track_id': track_id, 'saved_axis': axis, 'printed_column': column,
              'pair_id': track_id+'_'+axis+'_'+column, 'baseline': None, 'rows': []}
    for time in sorted(set(saved_by_time)|set(paper_by_time)):
        save, paper = saved_by_time.get(time), paper_by_time.get(time)
        row = {'nominal_grid_time_s': rational(time), 'saved': None, 'printed': None,
               'status': None, 'absolute': None, 'displacement': None}
        if save is not None:
            row['saved'] = {'frame': save['frame'], 'step': save['step'],
                            'saved_keyFrame_member': save['saved_keyFrame_member'],
                            'source_row_xml_path': save['source_row_xml_path'],
                            'source_coordinate_xml_paths': save['source_coordinate_xml_paths'],
                            'value': save['world'][axis], 'uniform_time_s': save['uniform_time_s'],
                            'nominal_time_residual_s': save['nominal_time_residual_s'],
                            'printed_time_rounding_0_01s_compatible': save['printed_time_rounding_0_01s_compatible']}
        if paper is not None:
            row['printed'] = {'source_pdf_sha256': source_hash, 'physical_and_printed_page': 47,
                              'row': paper['row'], 'column': column, 'time_text': paper['time_s'],
                              'saved_text': paper[column],
                              'value': float(paper[column]) if paper[column] is not None else None}
        if save is None:
            row['status'] = 'published_row_missing_saved'
        elif paper is None:
            row['status'] = 'saved_row_outside_published_times'
        elif paper[column] is None:
            row['status'] = 'published_cell_missing'
        else:
            row['status'] = 'shared_finite_nominal_time'
            original_offset = save['world'][axis]-float(paper[column])
            row['absolute'] = enclosure(original_offset, Fraction(5, 1000))
            if result['baseline'] is None:
                result['baseline'] = {'frame': save['frame'], 'step': save['step'],
                                      'saved_keyFrame_member': save['saved_keyFrame_member'],
                                      'nominal_grid_time_s': rational(time), 'printed_row': paper['row'],
                                      'saved_value': save['world'][axis], 'printed_value': float(paper[column]),
                                      'original_saved_minus_printed_offset': original_offset}
            baseline = result['baseline']
            change_saved = save['world'][axis]-baseline['saved_value']
            change_printed = float(paper[column])-baseline['printed_value']
            row['displacement'] = dict(enclosure(change_saved-change_printed, Fraction(1, 100)),
                                       saved_change=change_saved, printed_change=change_printed)
        result['rows'].append(row)
    rows = result['rows']
    result['counts'] = {key: sum(row['status'] == key for row in rows) for key in
                        ['shared_finite_nominal_time', 'published_row_missing_saved',
                         'saved_row_outside_published_times', 'published_cell_missing']}
    result['counts'].update(saved_rows=len(saved), printed_rows=len(table_rows),
                            shared_finite_nonkey_rows=sum(row['status'] == 'shared_finite_nominal_time' and not row['saved']['saved_keyFrame_member'] for row in rows),
                            shared_finite_printed_time_0_01s_compatible=sum(row['status'] == 'shared_finite_nominal_time' and row['saved']['printed_time_rounding_0_01s_compatible'] for row in rows))
    result['absolute_summary'] = stats(rows, 'absolute')
    result['displacement_summary'] = stats(rows, 'displacement')
    result['complete_row_compatibility'] = {
        'absolute_position_and_strict_printed_time_count': sum(row['absolute'] is not None and row['absolute']['with_arithmetic_tolerance_compatible'] and row['saved']['printed_time_rounding_0_01s_compatible'] for row in rows),
        'displacement_and_strict_printed_time_count': sum(row['displacement'] is not None and row['displacement']['with_arithmetic_tolerance_compatible'] and row['saved']['printed_time_rounding_0_01s_compatible'] for row in rows),
        'all_70_published_rows_have_finite_saved_and_printed_values': len(table_rows) == result['counts']['shared_finite_nominal_time'],
    }
    return result


def scalar(objects, cls, key):
    candidates = [o for o in objects if o['class'] == cls]
    if len(candidates) != 1:
        raise ValueError('ambiguous_settings_object')
    field = candidates[0]['fields'][key]
    if field['status'] != 'present' or len(field['occurrences']) != 1:
        raise ValueError('missing_or_duplicate_setting')
    value = field['occurrences'][0]
    if value['status'] not in {'valid_finite', 'valid_boolean'}:
        raise ValueError('invalid_setting')
    return value


def convert_rows(track, config, duration, origin, current_times, a, b, step_size):
    converted = []
    if len(track['framedata']) != 1 or track['framedata'][0]['duplicate_indices']:
        raise ValueError('unexpected_framedata')
    for row in track['framedata'][0]['rows']:
        if not row['finite_complete'] or row['index'] is None or (row['index']-a)%step_size:
            raise ValueError('unexpected_saved_row')
        fields = row['objects'][0]['coordinates']
        frame = row['index']
        u = uniform_clock(frame, duration, origin)
        pts = endpoint_clock(frame, current_times, a, b, duration, origin)
        nominal = nearest_grid(u)
        converted.append({'frame': frame, 'step': (frame-a)//step_size,
                          'saved_keyFrame_member': row['saved_keyFrame_member'],
                          'source_row_xml_path': row['xml_path'],
                          'source_coordinate_xml_paths': {k: fields[k]['occurrences'][0]['xml_path'] for k in ['x', 'y']},
                          'source_coordinate_text': {k: fields[k]['occurrences'][0]['saved_text'] for k in ['x', 'y']},
                          'world': inverse(fields['x']['occurrences'][0]['value'], fields['y']['occurrences'][0]['value'], **config),
                          'uniform_time_s': rational(u), 'current_pts_stretched_time_s': rational(pts),
                          'current_pts_minus_uniform_s': rational(pts-u),
                          'nominal_grid_time_s': rational(nominal), 'nominal_time_residual_s': rational(u-nominal),
                          'printed_time_rounding_0_01s_compatible': abs(u-nominal) <= Fraction(5, 1000)})
    return converted


def execute():
    before = {name: pin(HERE/name) for name in PINS}
    if any(before[name]['sha256'] != value for name, value in PINS.items()):
        raise ValueError('input_hash_mismatch')
    project = json.loads((HERE/'project01.json').read_text())
    table = json.loads((UNIT/'transcription-root/table47.json').read_text())
    reconciliation = json.loads((UNIT/'reconciliation.json').read_text())
    if reconciliation['status'] != 'exact_agreement' or reconciliation['pins']['transcription-root/table47.json'] != PINS['../multipoint-table-reproduction/transcription-root/table47.json']:
        raise ValueError('table_reconciliation_pin_mismatch')
    if table['source_sha256'] != PINS['../luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf'] or table['physical_and_printed_page'] != 47 or len(table['rows']) != 70:
        raise ValueError('unexpected_table_schema')
    for i, row in enumerate(table['rows'], 1):
        if row['page'] != 47 or row['row'] != i:
            raise ValueError('unexpected_table_locator')
        for name in ['time_s']+[c for _, c in PAIRINGS]:
            if row[name] is not None and not math.isfinite(float(row[name])):
                raise ValueError('nonfinite_printed_cell')
    probe = json.loads((HERE/'probe01/probe.json').read_text())
    media_receipt = json.loads((HERE/'source/receipt.json').read_text())
    if media_receipt['media']['sha256'] != '393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f':
        raise ValueError('unexpected_media_identity')
    if len(probe['streams']) != 1 or len(probe['frames']) != 476:
        raise ValueError('unexpected_probe_schema')
    time_base = Fraction(probe['streams'][0]['time_base'])
    current_times = [Fraction(row['pts'])*time_base*1000 for row in probe['frames']]
    if any(y <= x for x, y in zip(current_times, current_times[1:])):
        raise ValueError('nonmonotonic_current_pts')
    settings = project['settings_objects']
    media = 'org.opensourcephysics.media.core.'
    coords = media+'ImageCoordSystem'
    raw_settings = {k: scalar(settings, coords+'$FrameData', k) for k in ['xorigin', 'yorigin', 'angle', 'xscale', 'yscale']}
    for key in ['fixedorigin', 'fixedangle', 'fixedscale']:
        if scalar(settings, coords, key)['value'] is not True:
            raise ValueError('nonfixed_transform')
    config = {out: raw_settings[key]['value'] for out, key in
              [('xo', 'xorigin'), ('yo', 'yorigin'), ('degrees', 'angle'), ('sx', 'xscale'), ('sy', 'yscale')]}
    clip = {k: scalar(settings, media+'VideoClip', k) for k in ['startframe', 'stepsize', 'stepcount', 'starttime', 'video_framecount']}
    d = scalar(settings, media+'StepperClipControl', 'delta_t')
    duration, origin = Fraction(d['saved_text']), Fraction(clip['starttime']['saved_text'])
    a = clip['startframe']['value']
    step_size = clip['stepsize']['value']
    b = a+(clip['stepcount']['value']-1)*step_size
    if (a, b, step_size) != (0, 474, 6):
        raise ValueError('unexpected_declared_endpoints')
    tracks = []
    for track in project['pointmass_tracks']:
        rows = convert_rows(track, config, duration, origin, current_times, a, b, step_size)
        tracks.append({'track_id': track['track_id'], 'pointmass_ordinal_one_based': track['pointmass_ordinal_one_based'],
                       'source_names': track['names'], 'rows': rows,
                       'missing_video_frame_indices': track['missing_video_frame_indices'],
                       'missing_clip_step_indices': track['missing_clip_step_indices']})
    if len(tracks) != 8 or sum(len(t['rows']) for t in tracks) != 334:
        raise ValueError('incomplete_saved_row_coverage')
    pairs = [join_pair(track['track_id'], track['rows'], table['rows'], axis, column, table['source_sha256'])
             for track in tracks for axis, column in PAIRINGS]
    clock_rows = [{'frame': n, 'step': (n-a)//step_size,
                   'current_pts': probe['frames'][n]['pts'],
                   'current_pts_time_ms': rational(current_times[n]),
                   'uniform_time_s': rational(uniform_clock(n, duration, origin)),
                   'current_pts_stretched_time_s': rational(endpoint_clock(n, current_times, a, b, duration, origin)),
                   'difference_s': rational(endpoint_clock(n, current_times, a, b, duration, origin)-uniform_clock(n, duration, origin))}
                  for n in range(a, b+1, step_size)]
    result = {'status': 'conditional_saved_state_to_printed_table_comparison', 'schema_version': 1,
              'transform': {'formula': 'X=cos(A)*u/sx-sin(A)*v/sy; Y=-sin(A)*u/sx-cos(A)*v/sy; A in degrees',
                            'literal_settings': raw_settings, 'physical_units_validated': False},
              'clock': {'hypothesis': 'U_uniform_historical_engine_clock', 'duration_ms': rational(duration),
                        'origin_ms': rational(origin), 'loaded_start_frame': a, 'loaded_end_frame': b,
                        'current_pts_time_base': str(time_base),
                        'current_pts_endpoint_stretch': rational(duration*(b-a)/(current_times[b]-current_times[a])),
                        'current_pts_historical_engine_identity_established': False,
                        'selected_frame_diagnostic': clock_rows,
                        'maximum_current_pts_minus_U_absolute_seconds': max(abs(r['difference_s']['value']) for r in clock_rows)},
              'tracks': tracks, 'pairs': pairs,
              'summary': {'saved_point_rows': 334, 'pair_count': len(pairs),
                          'pair_summaries': [{k: pair[k] for k in ['pair_id', 'track_id', 'saved_axis', 'printed_column', 'baseline', 'counts', 'absolute_summary', 'displacement_summary', 'complete_row_compatibility']} for pair in pairs]},
              'source_pins': before}
    after = {name: pin(HERE/name) for name in PINS}
    if before != after:
        raise ValueError('input_changed_during_calculation')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, choices=['table01', 'table02'])
    args = parser.parse_args()
    destination = HERE/args.out
    if destination.exists() or destination.is_symlink():
        raise ValueError('output_already_exists')
    checked = subprocess.run([sys.executable, str(HERE/'project-table-controls.py')], capture_output=True, text=True)
    if checked.returncode != 0:
        raise ValueError('synthetic_controls_failed')
    controls = json.loads(checked.stdout)
    result = execute()
    code_pin, tests_pin = pin(Path(__file__)), pin(HERE/'project-table-controls.py')
    destination.mkdir()
    def write(name, data):
        payload = (json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
        with (destination/name).open('xb') as stream:
            stream.write(payload)
        return {'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()}
    outputs = {'comparison.json': write('comparison.json', result),
               'summary.json': write('summary.json', result['summary']),
               'controls.json': write('controls.json', controls)}
    receipt = {'status': 'pass_declared_calculation_and_repeat_ready', 'python': platform.python_version(),
               'producer': code_pin, 'tests': tests_pin, 'inputs': result['source_pins'], 'outputs': outputs,
               'source_unchanged_after_calculation': True, 'historical_or_physical_validation': False}
    write('receipt.json', receipt)
    print(json.dumps({'status': receipt['status'], 'outputs': outputs,
                      'all_available_absolute_compatible_pairs': [p['pair_id'] for p in result['pairs'] if p['absolute_summary']['all_available_compatible']],
                      'all_available_displacement_compatible_pairs': [p['pair_id'] for p in result['pairs'] if p['displacement_summary']['all_available_compatible']],
                      'strict_time_compatible_shared_finite_rows_across_pairs': sum(p['counts']['shared_finite_printed_time_0_01s_compatible'] for p in result['pairs']),
                      'maximum_current_pts_U_clock_difference_seconds': result['clock']['maximum_current_pts_minus_U_absolute_seconds']}))


if __name__ == '__main__':
    main()
