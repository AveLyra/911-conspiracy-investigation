#!/usr/bin/env python3
"""Fixed saved-point presentation under H0; no localization or physical inference.

Historical execution is a separate, explicitly code-pinned CLI stage. Importing
this module loads only the byte-pinned, inspected helper; it does not decode.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import sys
import types

from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
JOIN = HERE.parent / 'tilted-camera-source-join'
HELPER = JOIN / 'prepare_media.py'
HELPER_SHA = 'b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5'


def load_helper(path=HELPER, expected=HELPER_SHA):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('helper hash mismatch BEFORE import')
    module = types.ModuleType('held_tilted_media_helper')
    module.__file__ = str(path)
    # Execute exactly the checked bytes, with __main__ dispatch disabled.
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


held = load_helper()
require, sha, pin, write_json = held.require, held.sha, held.pin, held.write_json
TRACKS = ('pointmass05', 'pointmass08')
EXPECTED = {'pointmass05': list(range(150, 403, 6)),
            'pointmass08': list(range(210, 445, 6))}
INDICES = list(range(150, 445, 6))
PINS = {
    'project01.json': '4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8',
    'source/TiltedCameraWTC7Clip.mp4': '393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f',
    'source/receipt.json': 'a100331b8e5e66ebb41959811e3ff650750e8284fdba0e4c8dcebdd736ed8ea9',
    'probe01/probe.json': '778c35d099158ddc669316d88ee779cf89f5f5aa9c094cd5e1d5bed596bee1de',
    'probe01/selection.json': 'afd9abc4bd64a0422a749715a8dbb727f7e23447f1c6bf45e9c93d32030f7f6b',
    'probe01/execution.json': '548965fa3f7de60fd71fb42b2d211e63143502e041743db32d3df6a9b5ac25fd',
    'views01/frames.json': '2988d1347bd55cba704530c6d3996dcab1cfa6d5b4beebe6d0ad912ccd4d3a15',
    'views01/receipt.json': '4570095ea9c35fac86302f2443969a87261130175edb0de1b7eafa4eefefad29',
    'views01/execution.json': 'afc698e4f6215018fa821108270ba13012ae82459cc9893b747445a96003db59',
    'prepare_media.py': HELPER_SHA,
}
CONTROL_PINS = {
    HERE / 'PROTOCOL.md': '50785dd33e8543a0de76932be36e011693998cffa11a734040b3fb4f1ec3680d',
    HERE / 'method-review.md': 'cfe0b94704f419f18a8efb7992d03c38841242f3a369d21d877fba39f0e43fc6',
    Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md'):
        '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
}
BG, PAD, MARKER = (24, 24, 24), (255, 0, 255), (0, 255, 255)
LAYOUT = {
    'panel_size': [1128, 648], 'native_rect': [12, 72, 732, 552],
    'slots': {
        'pointmass05': {'plain_rect': [744, 140, 924, 320],
                        'marked_rect': [936, 140, 1116, 320], 'label_top': 56},
        'pointmass08': {'plain_rect': [744, 420, 924, 600],
                        'marked_rect': [936, 420, 1116, 600], 'label_top': 336},
    },
    'crop_size': [60, 60], 'scale': 3, 'padding_rgb': list(PAD),
    'mask_mode': 'L', 'mask_size': [60, 60], 'mask_valid': 255, 'mask_padding': 0,
    'background_rgb': list(BG), 'marker_rgb': list(MARKER),
    'marker_center': [91, 91], 'marker_arm_offsets_inclusive': [[-15, -6], [6, 15]],
    'marker_thickness': 1, 'marker_gap_offsets_inclusive': [-5, 5],
    'rounding': 'mathematical floor(exact saved binary value + 1/2)',
    'continuous_domain': '[0,720) x [0,480)',
    'rectangles': 'half-open integer pixel bounds',
    'labels': 'outside native/plain/marked rectangles; missing slots are background only',
}


def finite(value):
    require(type(value) in (int, float), 'coordinate must be numeric, not bool')
    require(math.isfinite(value), 'nonfinite coordinate')
    return value


def nearest(value):
    # Avoid addition-rounding at nextafter(0.5, 0); do not use Python round().
    return math.floor(Fraction(finite(value)) + Fraction(1, 2))


def geometry(x, y, width=720, height=480):
    x, y = finite(x), finite(y)
    r, s = nearest(x), nearest(y)
    rect = [r-30, s-30, r+30, s+30]
    left, top = max(0, rect[0]), max(0, rect[1])
    right, bottom = min(width, rect[2]), min(height, rect[3])
    valid = max(0, right-left) * max(0, bottom-top)
    return {'rounded': [r, s], 'source_rect': rect,
            'rounding_difference': [r-x, s-y],
            'rounding_difference_exact': [str(Fraction(r)-Fraction(x)),
                                          str(Fraction(s)-Fraction(y))],
            'original_coordinate_inside': 0 <= x < width and 0 <= y < height,
            'rounded_cell_inside': 0 <= r < width and 0 <= s < height,
            'valid_source_pixels': valid, 'padding_pixels': 3600-valid,
            'fully_in_source_crop': valid == 3600}


def crop_pair(native, x, y):
    require(native.size == (720, 480) and native.mode in ('L', 'RGB'), 'native raster contract')
    g = geometry(x, y)
    r0, s0, r1, s1 = g['source_rect']
    tile = Image.new('RGB', (60, 60), PAD)
    mask = Image.new('L', (60, 60), 0)
    box = (max(0, r0), max(0, s0), min(720, r1), min(480, s1))
    if box[2] > box[0] and box[3] > box[1]:
        dest = (box[0]-r0, box[1]-s0)
        tile.paste(native.crop(box).convert('RGB'), dest)
        mask.paste(255, (*dest, dest[0]+box[2]-box[0], dest[1]+box[3]-box[1]))
    plain = tile.resize((180, 180), Image.Resampling.NEAREST)
    marked = plain.copy()
    draw = ImageDraw.Draw(marked)
    for lo, hi in LAYOUT['marker_arm_offsets_inclusive']:
        draw.line((91+lo, 91, 91+hi, 91), fill=MARKER, width=1)
        draw.line((91, 91+lo, 91, 91+hi), fill=MARKER, width=1)
    return plain, marked, mask, g


def source_rows(project):
    """Parse every fixed source row without dropping nonkeys or compacting indices."""
    records = []
    for track_id in TRACKS:
        matches = [t for t in project['pointmass_tracks'] if t['track_id'] == track_id]
        require(len(matches) == 1, 'missing/duplicate track')
        track = matches[0]
        require(track['saved_indices'] == EXPECTED[track_id], 'saved index set changed')
        require(track['framedata_array_count'] == 1 and len(track['framedata']) == 1,
                'one frame array required')
        require(track['keyFrames_array_count'] == 1 and len(track['keyFrames']) == 1,
                'one key array required')
        expected_keys = list(range(360, 403, 6)) if track_id == 'pointmass05' else EXPECTED[track_id]
        require(track['keyFrames'][0]['values'] == expected_keys, 'key index set changed')
        array = track['framedata'][0]
        rows = array['rows']
        require(array['duplicate_indices'] == [] and len(rows) == len(EXPECTED[track_id]),
                'duplicate/missing/extra source row')
        require([r['index'] for r in rows] == EXPECTED[track_id], 'row indices/order changed')
        for ordinal, row in enumerate(rows, 1):
            require(type(row['index']) is int and row['entry_ordinal_one_based'] == ordinal,
                    'source index/ordinal type')
            require(row['status'] == 'saved_object' and row['finite_complete'] is True
                    and len(row['objects']) == 1, 'ambiguous/incomplete source row')
            obj = row['objects'][0]
            require(obj['status'] == 'expected_class' and obj['finite_complete'] is True,
                    'source object class/status')
            key = row['saved_keyFrame_member']
            require(type(key) is bool and key == (row['index'] in expected_keys), 'key flag mismatch')
            rec = {'track_id': track_id, 'frame_index': row['index'], 'key': key,
                   'entry_ordinal_one_based': ordinal, 'source_row_xml_path': row['xml_path'],
                   'source_track_xml_path': track['xml_path']}
            for axis in ('x', 'y'):
                coord = obj['coordinates'][axis]
                require(coord['status'] == 'present' and len(coord['occurrences']) == 1,
                        'coordinate missing/ambiguous')
                item = coord['occurrences'][0]
                value = finite(item['value'])
                require(item['status'] == 'valid_finite' and type(item['saved_text']) is str,
                        'coordinate status/text')
                require(sha(item['saved_text'].encode()) == item['text_sha256']
                        and float(item['saved_text']) == value, 'coordinate text/value/hash mismatch')
                rec[axis] = value
                rec[axis+'_saved_text'] = item['saved_text']
                rec[axis+'_saved_text_sha256'] = item['text_sha256']
                rec[axis+'_float_hex'] = float(value).hex()
                rec[axis+'_xml_path'] = item['xml_path']
            rec.update(geometry(rec['x'], rec['y']))
            records.append(rec)
    records.sort(key=lambda r: (r['frame_index'], r['track_id']))
    require(len(records) == 83 and len({(r['frame_index'], r['track_id']) for r in records}) == 83,
            '83 unique rows required')
    require(sorted({r['frame_index'] for r in records}) == INDICES, '50-frame union changed')
    return records


def panel(native, frame, points, synthetic=False):
    require(native.size == (720, 480) and native.mode in ('L', 'RGB'), 'native raster contract')
    require(len({p['track_id'] for p in points}) == len(points)
            and all(p['track_id'] in TRACKS for p in points), 'duplicate/unsupported panel slot')
    require(all(p['frame_index'] == frame['index'] and type(p['key']) is bool for p in points),
            'point/frame or key mismatch')
    out = Image.new('RGB', tuple(LAYOUT['panel_size']), BG)
    out.paste(native.convert('RGB'), (12, 72))
    draw = ImageDraw.Draw(out)
    font = ImageFont.load_default(size=12)

    def label(x, y, text, maximum=1104):
        # Reject label overflow instead of silently placing text onto source pixels.
        require(draw.textlength(text, font=font) <= maximum, 'label overflows declared band')
        draw.text((x, y), text, fill=(240, 240, 240), font=font)

    prefix = 'SYNTHETIC CONTROL | ' if synthetic else 'SOURCE-GUIDED H0 | '
    label(12, 8, prefix + f"frame {frame['index']} | PTS {frame['pts']} * {frame['time_base']} = {frame['time_seconds_exact']} s")
    label(12, 28, 'H0 conditional: native 720x480, x right/y down; no SAR correction, rotation, time shift or fitted transform.')
    caption = ('Complete synthetic RGB coordinate-pattern image, unmarked.'
               if synthetic and native.mode == 'RGB' else
               'Complete native image, unmarked (Y plane repeated as RGB for this panel).')
    label(12, 56, caption, 720)
    products, slots = {}, {}
    by_track = {p['track_id']: p for p in points}
    for track in TRACKS:
        slot = LAYOUT['slots'][track]
        top = slot['label_top']
        if track not in by_track:
            label(744, top, track.upper() + ': NO SAVED ROW', 372)
            label(744, top+16, 'No counterpart invented; blank slots are not data.', 372)
            slots[track] = {'status': 'missing_saved_row'}
            continue
        point = by_track[track]
        plain, marked, mask, g = crop_pair(native, point['x'], point['y'])
        label(744, top, f"{track.upper()} key={str(point['key']).lower()} | saved image-space", 372)
        label(744, top+16, 'x=' + point['x_saved_text'], 372)
        label(744, top+32, 'y=' + point['y_saved_text'], 372)
        label(744, top+48, f"cell={g['rounded']} inside: xy={g['original_coordinate_inside']} cell={g['rounded_cell_inside']}", 372)
        label(744, top+64, 'Unmarked / 3x nearest', 180)
        label(936, top+64, 'Marked / gap at (91,91)', 180)
        out.paste(plain, tuple(slot['plain_rect'][:2]))
        out.paste(marked, tuple(slot['marked_rect'][:2]))
        products[track] = {'plain': plain, 'marked': marked, 'mask': mask}
        slots[track] = {'status': 'saved_row', 'row_key': [frame['index'], track], **g}
    label(12, 568, 'Cyan arms mark a rounded cell; center/gap untouched. Unmarked crop remains alongside.', 720)
    label(12, 586, 'Magenta is outside-source padding, not evidence; separate 60x60 validity masks retained.', 720)
    label(12, 604, 'Saved key status does not establish manual marking. H0 does not establish material-point identity.', 720)
    label(12, 622, 'Encoded PTS are not authenticated exposure times or the assigned analysis clock.', 720)
    return out, products, slots


def output_path(name):
    require(type(name) is str and re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', name), 'unsafe output name')
    out = HERE / name
    require(not out.exists() and not out.is_symlink(), 'output already exists')
    return out


def png_save(path, im):
    with path.open('xb') as handle:
        im.save(handle, format='PNG')
    with Image.open(path) as check:
        require(check.mode == im.mode and check.size == im.size and check.tobytes() == im.tobytes(),
                'PNG lossless reread mismatch')
    return {**pin(path), 'mode': im.mode, 'size': list(im.size), 'pixel_sha256': sha(im.tobytes())}


def snapshot(paths):
    return {str(path): pin(path) for path in paths}


def require_pins(paths):
    result = snapshot(paths)
    for path, expected in paths.items():
        require(result[str(path)]['sha256'] == expected, 'input hash mismatch: '+path.name)
    return result


def validate_map(probe, baseline):
    stream, rows = held.parse_map(probe)
    require((stream['width'], stream['height'], stream['time_base'], stream['sample_aspect_ratio'])
            == (720, 480, '1/60000', '131:144'), 'fixed geometry/timebase/SAR changed')
    require(len(rows) == len(baseline) == 476, '476-frame coverage required')
    for i, (row, old) in enumerate(zip(rows, baseline)):
        require(type(old['index']) is int and old['index'] == i and
                {k: old[k] for k in row} == row, 'baseline PTS/index mismatch')
        for key in ('decoded_sha256', 'luma_sha256'):
            require(re.fullmatch(r'[0-9a-f]{64}', old[key]) is not None, 'invalid baseline hash')
    return stream, rows


def validate_decoded(raw, rows, baseline):
    frame_bytes, y_bytes = 720*480*3//2, 720*480
    require(len(raw) == frame_bytes*476 and len(rows) == len(baseline) == 476,
            'decoded byte/frame count mismatch')
    hashes = []
    for i, (row, old) in enumerate(zip(rows, baseline)):
        require(row['index'] == i and old['index'] == i, 'decode frame order mismatch')
        data = raw[i*frame_bytes:(i+1)*frame_bytes]
        entry = {**row, 'decoded_sha256': sha(data), 'luma_sha256': sha(data[:y_bytes])}
        require(entry == old, 'decoded YUV/luma/PTS mismatch at index '+str(i))
        hashes.append(entry)
    return hashes


def run_process(argv, output, stem):
    """Retain stderr even on successful calls; any warning blocks admission."""
    try:
        run = subprocess.run(argv, capture_output=True, timeout=60)
        stdout, stderr, code = run.stdout, run.stderr, run.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, code = error.stdout or b'', error.stderr or b'', None
    with (output/(stem+'.stderr')).open('xb') as handle:
        handle.write(stderr)
    if stem == 'probe':
        # Preserve malformed/changed probe output too, before parse/admission.
        with (output/'probe.stdout.json').open('xb') as handle:
            handle.write(stdout)
    execution = {'argv': argv, 'returncode': code, 'timeout_seconds': 60,
                 'stdout_bytes': len(stdout), 'stdout_sha256': sha(stdout),
                 'stderr_bytes': len(stderr), 'stderr_sha256': sha(stderr)}
    write_json(output/(stem+'-execution.json'), execution)
    require(code == 0 and not stderr, stem+' warning/error/timeout requires review')
    return stdout, execution


def historical(out_name, reviewed_sha):
    output = output_path(out_name)  # Refusal precedes all subprocess calls/writes.
    require(pin(__file__)['sha256'] == reviewed_sha, 'reviewed producer hash mismatch')
    fixed = {JOIN/name: digest for name, digest in PINS.items()} | CONTROL_PINS
    fixed[held.DECODER] = '7697b094387e2918821fe7480c73f5d44543817096e9d5b5fafe58ecd6912569'
    fixed[held.PROBE] = 'fd670257233c93c88608a62ed8b5ddeeb812bd341dfb39bbe0e1c654b91672ad'
    before = require_pins(fixed)
    dynamic = [Path(__file__), HERE/'test_prepare.py', Path(sys.executable),
               Path(Image.__file__), Path(Image.core.__file__), Path(ImageDraw.__file__),
               Path(ImageFont.__file__)]
    before.update(snapshot(dynamic))
    require(PILLOW_VERSION == '12.3.0' and platform.python_version() == '3.12.14',
            'reviewed Python/Pillow runtime changed')
    project = json.loads((JOIN/'project01.json').read_text())
    points = source_rows(project)
    prior_probe = json.loads((JOIN/'probe01/probe.json').read_text())
    baseline = json.loads((JOIN/'views01/frames.json').read_text())
    stream, rows = validate_map(prior_probe, baseline)
    prior_receipt = json.loads((JOIN/'views01/receipt.json').read_text())
    output.mkdir()
    write_json(output/'input-receipt.json', {'inputs_before': before, 'argv': sys.argv,
               'output_directory': str(output), 'python': platform.python_version(),
               'pillow': PILLOW_VERSION, 'status': 'started_not_admitted',
               'reviewed_producer_sha256': reviewed_sha, 'no_human_review_claim': True})
    try:
        probe_argv = json.loads((JOIN/'probe01/execution.json').read_text())['argv']
        probe_bytes, probe_execution = run_process(probe_argv, output, 'probe')
        fresh_probe = json.loads(probe_bytes)
        require(fresh_probe == prior_probe, 'fresh probe differs from held probe')
        stream, rows = validate_map(fresh_probe, baseline)
        write_json(output/'probe.json', fresh_probe)
        # Exactly the inspected held helper's start-to-end decode contract.
        argv = [str(held.DECODER), '-nostdin', '-nostats', '-hide_banner', '-v', 'warning',
                '-copyts', '-noautorotate', '-i', str(held.MEDIA), '-map', '0:v:0', '-an',
                '-noautoscale', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
                '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']
        require(argv == prior_receipt['execution']['argv'], 'held decode contract mismatch')
        raw, decode_execution = run_process(argv, output, 'decode')
        require(sha(raw) == prior_receipt['execution']['raw_sha256'], 'full raw stream mismatch')
        hashes = validate_decoded(raw, rows, baseline)
        write_json(output/'frames.json', hashes)
        for directory in ('native', 'crops', 'panels'):
            (output/directory).mkdir()
        products, frames, enriched = {}, [], []
        for index in INDICES:
            y = raw[index*518400:index*518400+345600]
            native = Image.frombytes('L', (720, 480), y)
            native_name = f'native/frame-{index:04d}.png'
            products[native_name] = png_save(output/native_name, native)
            selected_points = [p for p in points if p['frame_index'] == index]
            frame = {**rows[index], 'time_base': stream['time_base']}
            image, crops, slots = panel(native, frame, selected_points)
            panel_name = f'panels/frame-{index:04d}.png'
            products[panel_name] = png_save(output/panel_name, image)
            frame.update({'native_png': native_name, 'panel_png': panel_name, 'slots': slots,
                          'decoded_sha256': hashes[index]['decoded_sha256'],
                          'luma_sha256': hashes[index]['luma_sha256']})
            frames.append(frame)
            for point in selected_points:
                names = {}
                for kind, crop in crops[point['track_id']].items():
                    name = f"crops/{point['track_id']}-f{index:04d}-{kind}.png"
                    products[name] = png_save(output/name, crop)
                    names[kind+'_png'] = name
                enriched.append({**point, 'pts': frame['pts'],
                                 'time_base': frame['time_base'],
                                 'time_seconds_exact': frame['time_seconds_exact'], **names})
        require(len(frames) == 50 and len(enriched) == 83 and len(products) == 349,
                'presentation coverage changed')
        manifest = {'schema_version': 1, 'status': 'representation_only_not_visual_acceptance',
                    'hypothesis': 'H0 direct saved image xy to native720x480; no transform',
                    'sample_aspect_ratio_unapplied': stream['sample_aspect_ratio'],
                    'selection_indices': INDICES, 'row_count': 83, 'layout': LAYOUT,
                    'source_project_sha256': PINS['project01.json'],
                    'source_media_sha256': PINS['source/TiltedCameraWTC7Clip.mp4'],
                    'frames': frames, 'points': enriched, 'products': products}
        write_json(output/'manifest.json', manifest)
        after = snapshot(Path(path) for path in before)
        require(before == after, 'inputs/procedures/runtime changed during run')
        substantive = {str(p.relative_to(output)): pin(p) for p in sorted(output.rglob('*'))
                       if p.is_file() and p.name != 'input-receipt.json'}
        write_json(output/'receipt.json', {'status': 'prepared_pending_independent_checks_and_review',
                   'inputs_before': before, 'inputs_after': after, 'output_directory': str(output),
                   'argv': sys.argv, 'products': substantive, 'determinism_exceptions':
                   ['input-receipt.json', 'receipt.json'], 'no_historical_view_performed': True,
                   'no_new_coordinate_measurement': True, 'all_476_hashes_and_pts_match': True,
                   'probe_execution': probe_execution, 'decode_execution': decode_execution})
        print(json.dumps({'status': 'prepared_pending_independent_checks', 'frames': 50,
                          'rows': 83, 'pngs': 349, 'receipt': pin(output/'receipt.json')}))
    except Exception as error:
        write_json(output/'failure.json', {'status': 'failed_not_admitted',
                   'exception_type': type(error).__name__, 'message': str(error),
                   'inputs_after_failure': snapshot(Path(path) for path in before)})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['historical'])
    parser.add_argument('--out', required=True)
    parser.add_argument('--reviewed-producer-sha256', required=True,
                        help='root computational review freeze; not human/expert approval')
    args = parser.parse_args()
    historical(args.out, args.reviewed_producer_sha256)
