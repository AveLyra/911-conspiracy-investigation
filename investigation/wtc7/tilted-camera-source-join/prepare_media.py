#!/usr/bin/env python3
"""Preserve one fixed public clip, probe it, and select eight unaltered Y planes."""
import argparse
from fractions import Fraction
import hashlib
import io
import json
import ntpath
from pathlib import Path
import platform
import re
import subprocess
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
PARENT = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip')
PARENT_HASH = 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'
MEMBER = 'The Kit/WTC7-Tilted Camera/WTC7TiltedCamera.trz'
MEMBER_HASH = '7eee39a3f9c802343204d7f3f595478ab4c5a7c6c54ca8e2928c46c7ed8b7552'
MEDIA_NAME = 'TiltedCameraWTC7Clip.mp4'
MEDIA_HASH = '393d76f986d0771c5ec38352bf29470a81a3c685bb8a1c7ea565ceefa334843f'
MEDIA = HERE/'source'/MEDIA_NAME
PROBE = Path('/opt/homebrew/bin/ffprobe')
DECODER = Path('/opt/homebrew/bin/ffmpeg')
LIMIT = 128*1024*1024


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(data): return hashlib.sha256(data).hexdigest()


def pin(path):
    with Path(path).open('rb') as f: h = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'bytes': Path(path).stat().st_size, 'sha256': h}


def write_json(path, data):
    with path.open('x') as f: json.dump(data, f, indent=2, sort_keys=True); f.write('\n')


def selected_indices(n):
    require(type(n) is int and n > 0, 'positive frame count required')
    return sorted({k*(n-1)//7 for k in range(8)})


def safe_output(name):
    require(bool(re.fullmatch(r'[a-z][a-z0-9_-]*', name)), 'unsafe output name')
    out = HERE/name
    require(not out.exists(), 'output already exists')
    return out


def bounded(archive, info):
    require(not info.flag_bits & 1 and info.file_size <= LIMIT, 'archive bound/encryption')
    require(info.file_size/max(1, info.compress_size) <= 500, 'archive expansion bound')
    with archive.open(info) as f: data = f.read(LIMIT+1)
    require(len(data) == info.file_size, 'archive size mismatch')
    return data


def stage_preserve():
    parent_pin = pin(PARENT); require(parent_pin['sha256'] == PARENT_HASH, 'parent hash')
    require(not MEDIA.parent.exists(), 'source directory exists')
    with zipfile.ZipFile(PARENT) as outer:
        matches = [i for i in outer.infolist() if i.filename == MEMBER]
        require(len(matches) == 1, 'unique outer member required')
        nested = bounded(outer, matches[0]); require(sha(nested) == MEMBER_HASH, 'member hash')
        with zipfile.ZipFile(io.BytesIO(nested)) as inner:
            infos = inner.infolist(); require(len(infos) == 5, 'changed nested inventory')
            copies = []
            for ordinal in (2, 3):
                info = infos[ordinal]
                require(ntpath.basename(info.filename) == MEDIA_NAME, 'media basename')
                content = bounded(inner, info)
                require(len(content) == 7768869 and sha(content) == MEDIA_HASH, 'media identity')
                copies.append(content)
            require(copies[0] == copies[1], 'duplicate media differs')
    MEDIA.parent.mkdir()
    with MEDIA.open('xb') as f: f.write(copies[0])
    require(pin(MEDIA)['sha256'] == MEDIA_HASH and pin(PARENT) == parent_pin, 'preservation after-check')
    write_json(MEDIA.parent/'receipt.json', {'parent': parent_pin, 'outer_member': MEMBER,
               'outer_sha256': MEMBER_HASH, 'source_ordinal': 2, 'duplicate_ordinal': 3,
               'source_member_path_not_used_for_output': True, 'media': pin(MEDIA),
               'output_name': MEDIA_NAME, 'producer': pin(__file__), 'protocol': pin(HERE/'PROTOCOL.md')})
    print(json.dumps({'status': 'preserved_byte_identical_clip', 'bytes': len(copies[0])}))


def parse_map(data):
    require(len(data.get('streams', [])) == 1, 'one selected video stream required')
    stream = data['streams'][0]
    w, h = stream['width'], stream['height']
    require(type(w) is int and type(h) is int and 0 < w <= 2000 and 0 < h <= 2000, 'geometry bound')
    require(w % 2 == 0 and h % 2 == 0 and stream['pix_fmt'] == 'yuv420p', 'native Y420 contract')
    base = Fraction(stream['time_base']); require(base > 0, 'positive time base')
    rows = []
    for index, frame in enumerate(data.get('frames', [])):
        require(frame['width'] == w and frame['height'] == h and frame['pix_fmt'] == 'yuv420p', 'frame geometry/format changed')
        t = int(frame['best_effort_timestamp'])
        require('pts' not in frame or int(frame['pts']) == t, 'PTS/best-effort disagreement')
        rows.append({'index': index, 'pts': t, 'time_seconds_exact': str(t*base)})
    require(rows and len(rows) <= 10000, 'frame count outside bound')
    require(all(b['pts'] > a['pts'] for a, b in zip(rows, rows[1:])), 'non-increasing PTS')
    return stream, rows


def stage_probe(out_name):
    output = safe_output(out_name)
    require(pin(MEDIA)['sha256'] == MEDIA_HASH, 'media hash')
    argv = [str(PROBE), '-v', 'warning', '-select_streams', 'v:0', '-show_entries',
            'stream=index,codec_name,codec_type,width,height,pix_fmt,sample_aspect_ratio,display_aspect_ratio,r_frame_rate,avg_frame_rate,time_base,start_pts,start_time,duration_ts,duration,nb_frames:stream_side_data=side_data_type,rotation,displaymatrix:frame=stream_index,best_effort_timestamp,pts,duration,pkt_duration,width,height,pix_fmt,key_frame,pict_type',
            '-of', 'json', str(MEDIA)]
    run = subprocess.run(argv, capture_output=True, timeout=60)
    output.mkdir()
    diagnostics = {'returncode': run.returncode, 'stderr_bytes': len(run.stderr), 'stderr_sha256': sha(run.stderr)}
    write_json(output/'execution.json', {'argv': argv, 'diagnostics': diagnostics, 'binary': pin(PROBE),
               'media': pin(MEDIA), 'producer': pin(__file__), 'protocol': pin(HERE/'PROTOCOL.md')})
    require(run.returncode == 0 and not run.stderr, 'probe warning/error requires review')
    data = json.loads(run.stdout); stream, rows = parse_map(data)
    write_json(output/'probe.json', data)
    write_json(output/'selection.json', {'n': len(rows), 'geometry': [stream['width'], stream['height']],
               'time_base': stream['time_base'], 'indices': selected_indices(len(rows)), 'frames': rows,
               'selection_rule': 'floor(k*(N-1)/7), k=0..7, distinct indices, declared before viewing'})
    print(json.dumps({'status': 'probe_and_selection_saved', 'stream': stream, 'frames': len(rows),
                      'indices': selected_indices(len(rows))}))


def stage_decode(probe_name, out_name):
    from PIL import Image, __version__ as pillow_version
    require(bool(re.fullmatch(r'[a-z][a-z0-9_-]*', probe_name)), 'unsafe probe name')
    output = safe_output(out_name); probe_dir = HERE/probe_name
    prior = json.loads((probe_dir/'probe.json').read_text()); stream, rows = parse_map(prior)
    selection = json.loads((probe_dir/'selection.json').read_text())
    require(selection['frames'] == rows and selection['indices'] == selected_indices(len(rows)), 'selection changed')
    media_pin = pin(MEDIA); require(media_pin['sha256'] == MEDIA_HASH, 'media hash')
    w, h = stream['width'], stream['height']; frame_bytes = w*h*3//2
    require(frame_bytes*len(rows) <= 1024*1024*1024, 'raw memory bound')
    argv = [str(DECODER), '-nostdin', '-nostats', '-hide_banner', '-v', 'warning', '-copyts',
            '-noautorotate', '-i', str(MEDIA), '-map', '0:v:0', '-an', '-noautoscale', '-pix_fmt',
            'yuv420p', '-fps_mode', 'passthrough', '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']
    run = subprocess.run(argv, capture_output=True, timeout=60)
    output.mkdir()
    execution = {'argv': argv, 'returncode': run.returncode, 'stderr_bytes': len(run.stderr),
                 'stderr_sha256': sha(run.stderr), 'raw_bytes': len(run.stdout), 'raw_sha256': sha(run.stdout)}
    write_json(output/'execution.json', execution)
    require(run.returncode == 0 and not run.stderr, 'decode warning/error requires review')
    require(len(run.stdout) == frame_bytes*len(rows), 'probe/decode frame count mismatch')
    hashes, selected = [], []
    for index, row in enumerate(rows):
        frame = run.stdout[index*frame_bytes:(index+1)*frame_bytes]
        y = frame[:w*h]
        hashes.append({'index': index, 'decoded_sha256': sha(frame), 'luma_sha256': sha(y), **row})
        if index in selection['indices']:
            path = output/f'frame-{index:04d}.png'
            Image.frombytes('L', (w, h), y).save(path)
            with Image.open(path) as im: require(im.tobytes() == y and im.size == (w,h), 'native PNG mismatch')
            selected.append({**row, 'png': path.name, **pin(path), 'luma_sha256': sha(y)})
    require(pin(MEDIA) == media_pin, 'media changed')
    write_json(output/'frames.json', hashes)
    write_json(output/'receipt.json', {'media': media_pin, 'binary': pin(DECODER), 'producer': pin(__file__),
               'protocol': pin(HERE/'PROTOCOL.md'), 'probe': pin(probe_dir/'probe.json'),
               'selection': pin(probe_dir/'selection.json'), 'geometry': [w,h],
               'python': platform.python_version(), 'pillow': pillow_version, 'execution': execution,
               'selected': selected, 'no_visual_review_implied': True})
    print(json.dumps({'status': 'eight_native_Y_frames_prepared', 'n': len(rows), 'indices': selection['indices']}))


class Controls(unittest.TestCase):
    def test_selection(self): self.assertEqual(selected_indices(476), [0,67,135,203,271,339,407,475])
    def test_small_selection(self): self.assertEqual(selected_indices(3), [0,1,2])
    def test_bad_count(self):
        for n in (0,-1,True,2.5):
            with self.assertRaises(ValueError): selected_indices(n)
    def fixture(self):
        return {'streams':[{'width':4,'height':2,'pix_fmt':'yuv420p','time_base':'1/30'}],
                'frames':[{'width':4,'height':2,'pix_fmt':'yuv420p','best_effort_timestamp':i,'pts':i} for i in (0,1)]}
    def test_exact_times(self): self.assertEqual(parse_map(self.fixture())[1][1]['time_seconds_exact'], '1/30')
    def test_bad_pts(self):
        d=self.fixture(); d['frames'][1]['best_effort_timestamp']=0
        with self.assertRaises(ValueError): parse_map(d)
    def test_bad_format(self):
        d=self.fixture(); d['frames'][1]['pix_fmt']='gray'
        with self.assertRaises(ValueError): parse_map(d)
    def test_bad_output(self):
        for name in ('../bad','/tmp/bad','a/b','a b'):
            with self.assertRaises(ValueError): safe_output(name)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('stage', choices=['preserve','probe','decode','test'])
    parser.add_argument('--out'); parser.add_argument('--probe'); args=parser.parse_args()
    if args.stage == 'test':
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    elif args.stage == 'preserve': stage_preserve()
    elif args.stage == 'probe': stage_probe(args.out)
    else: stage_decode(args.probe, args.out)
