#!/usr/bin/env python3
"""Fixed, hash-gated diagnostic viewing products; no motion estimation."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess

from PIL import Image, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
PUBLIC = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
KIT = PUBLIC / 'camera3-provenance/kit-inventory/run-v1'
SOURCE = KIT / 'outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv'
ALIAS = KIT / 'nested/videos/Camera3.wmv'
OLD = PUBLIC / 'camera3-recording-comparison/wmv-diagnostic/run02'
BIN = Path('/opt/homebrew/bin/ffmpeg')
INDICES = [138, 141, 168]
SIZE = (720, 480)
CROP = (300, 80, 510, 425)
FACTOR = 3
EXPECTED_SOURCE = '48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722'
EXPECTED_RAW = '1244ddf86418a17a1f4140c979268d33a5964a098da4fd6fd7817499bcb60b6b'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=digest(data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = HERE / args.out
    if output.parent != HERE or output.exists():
        raise ValueError('Only a fresh immediate output directory is permitted')
    paths = [SOURCE, ALIAS, BIN, OLD / 'receipt.json', OLD / 'default-frames.json',
             KIT / 'saved-tracker-settings.json', HERE / 'PROTOCOL.md', Path(__file__)]
    initial = [pin(p) for p in paths]
    assert initial[0]['sha256'] == initial[1]['sha256'] == EXPECTED_SOURCE
    old = json.loads((OLD / 'receipt.json').read_text())
    frames = json.loads((OLD / 'default-frames.json').read_text())
    assert initial[2]['sha256'] == old['binaries'][str(BIN)]['sha256']
    assert initial[4]['sha256'] == old['products']['default-frames.json']['sha256']
    assert frames['raw_frame_count'] == 442 and frames['raw_sha256'] == EXPECTED_RAW
    assert initial[5]['sha256'] == 'ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb'
    argv = [str(BIN), '-nostdin', '-nostats', '-hide_banner', '-loglevel',
            'repeat+level+info', '-debug_ts', '-copyts', '-noautorotate',
            '-i', str(SOURCE), '-map', '0:v:0', '-an', '-noautoscale',
            '-pix_fmt', 'gray', '-fps_mode', 'passthrough',
            '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']
    previous = [c for c in old['commands'] if c['label'] == 'default']
    assert len(previous) == 1 and argv == previous[0]['argv']

    # Roundtrip/crop contract on deterministic synthetic pixels, before source decode.
    synthetic = Image.frombytes('L', SIZE, bytes(i % 251 for i in range(SIZE[0]*SIZE[1])))
    zoom = synthetic.crop(CROP).resize((630, 1035), Image.Resampling.NEAREST)
    assert all(zoom.getpixel((3*x+1, 3*y+1)) == synthetic.getpixel((x+300,y+80))
               for y in range(345) for x in range(210))
    output.mkdir()
    (output / 'initial.json').write_text(json.dumps(initial, indent=2) + '\n')
    completed = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               check=False, timeout=120)
    raw = completed.stdout
    frame_bytes = SIZE[0]*SIZE[1]
    hashes = [digest(raw[i:i+frame_bytes]) for i in range(0, len(raw), frame_bytes)]
    raw_ok = (completed.returncode == 0 and len(raw) == 442*frame_bytes
              and digest(raw) == EXPECTED_RAW and hashes == frames['pixel_hashes'])
    execution = dict(returncode=completed.returncode, argv=argv, raw_bytes=len(raw),
                     raw_sha256=digest(raw), all_442_pixel_hashes_match=hashes == frames['pixel_hashes'],
                     stderr_bytes=len(completed.stderr), stderr_sha256=digest(completed.stderr),
                     corrupt_decoded_frame_mentions=completed.stderr.count(b'corrupt decoded frame'),
                     stderr_not_exported=True, new_warning_localization_claim=False)
    if not raw_ok:
        (output / 'failure.json').write_text(json.dumps(execution, indent=2) + '\n')
        raise RuntimeError('Decode did not match preserved diagnostic; images not admitted')
    selected = []
    for index in INDICES:
        pixels = raw[index*frame_bytes:(index+1)*frame_bytes]
        native = Image.frombytes('L', SIZE, pixels)
        path = output / f'frame-{index:04d}.png'
        native.save(path)
        assert Image.open(path).tobytes() == pixels
        enlarged = native.crop(CROP).resize((630, 1035), Image.Resampling.NEAREST)
        crop_path = output / f'crop-{index:04d}.png'
        enlarged.save(crop_path)
        assert Image.open(crop_path).tobytes() == enlarged.tobytes()
        record = frames['records'][index]
        assert record['index'] == index and record['warning_log_line'] is None
        selected.append(dict(index=index, inherited_diagnostic_pts=record['pts'],
                             inherited_time_base=record['time_base'],
                             inherited_seconds_exact=record['seconds_exact'],
                             pixel_sha256=hashes[index], native=pin(path),
                             crop=pin(crop_path), crop_box=list(CROP), scale=FACTOR))
    final = [pin(p) for p in paths]
    assert final == initial
    receipt = dict(status='pass_diagnostic_view_only', python=platform.python_version(),
                   pillow=pillow_version, initial=initial, final=final,
                   execution=execution, selected=selected, geometry=list(SIZE),
                   synthetic_crop_cells_checked=210*345,
                   limit='Identity/format checks only; no historical engine, exposure, physical-scale or acceleration validation')
    (output / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(status=receipt['status'], frames=INDICES,
                          full_raw_match=True, all_frame_hashes_match=True,
                          warning_mentions=execution['corrupt_decoded_frame_mentions'])))


if __name__ == '__main__':
    main()
