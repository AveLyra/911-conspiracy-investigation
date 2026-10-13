"""Bounded descriptive samples; no measurement or visual-acceptance algorithm."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from PIL import Image, __version__ as pillow_version

BASE = Path(__file__).resolve().parent
FFMPEG = '/opt/homebrew/bin/ffmpeg'
FFPROBE = '/opt/homebrew/bin/ffprobe'
SOURCES = [
    ('cbs-net-dub5-15', '8a4e3e02105d65140c2a3dc0bc95af0d907866de85353d5c9f498636aea79781', 60183924, 475),
    ('cbs-net-dub6-44', 'c3a19c895f5bcacdb473745641dbbd500982219a6de57726920125477a12f90c', 104308572, 824),
]


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def save(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write('\n')


def identity(path, digest, size):
    assert path.stat().st_size == size, 'source size mismatch'
    assert sha(path) == digest, 'source hash mismatch'


def indices(count):
    assert count > 0
    return sorted(set(range(0, count, 60)) | {count - 1})


def inventory(doc, count):
    frames = doc['frames']
    assert len(frames) == count, 'decoded frame count mismatch'
    stream = doc['streams'][0]
    tb = Fraction(stream['time_base'])
    assert tb > 0
    previous = None
    for frame in frames:
        pts = frame.get('pts')
        assert type(pts) is int, 'missing/non-integer PTS'
        assert previous is None or pts > previous, 'non-increasing PTS'
        assert (frame['width'], frame['height']) == (stream['width'], stream['height']), 'changing geometry'
        previous = pts
    return frames, stream, tb


def run_command(args, dest, name, stdin=None):
    save(dest / (name + '.command.json'), args)
    result = subprocess.run(args, input=stdin, capture_output=True, check=False)
    (dest / (name + '.stdout')).write_bytes(result.stdout)
    (dest / (name + '.stderr')).write_bytes(result.stderr)
    assert result.returncode == 0, f'{name} failed: {result.returncode}; retained logs'
    return result.stdout, result.stderr.decode('utf-8', errors='replace')


def sample(source, digest, size, count, dest, guess=False):
    identity(source, digest, size)
    dest.mkdir()  # Refuse any existing destination; retain partial failure output.
    stdout, _ = run_command([FFPROBE, '-v', 'warning', '-select_streams', 'v:0',
                            '-show_frames', '-show_streams', '-show_format',
                            '-of', 'json', str(source)], dest, 'probe')
    doc = json.loads(stdout)
    frames, stream, tb = inventory(doc, count)
    selected = indices(count)
    native = dest / 'native'
    native.mkdir()
    selection = '+'.join(f'eq(n,{n})' for n in selected)
    command = [FFMPEG, '-nostdin', '-hide_banner', '-nostats', '-loglevel', 'level+info',
               '-n', '-copyts', '-noautorotate']
    if not guess:
        command += ['-guess_layout_max', '0']
    command += ['-i', str(source), '-map', '0:v:0', '-an', '-sn', '-dn',
                '-map_metadata', '-1', '-map_chapters', '-1',
                '-vf', f"select='{selection}',showinfo", '-noautoscale',
                '-pix_fmt', 'rgb24', '-fps_mode', 'passthrough',
                '-enc_time_base:v', 'demux', str(native / 'frame-%06d.png')]
    _, stderr = run_command(command, dest, 'decode')
    configs = re.findall(r'config in time_base: ([0-9]+/[0-9]+)', stderr)
    assert len(configs) == 1 and Fraction(configs[0]) == tb, 'showinfo time-base mismatch'
    logged = [(int(a), int(b)) for a, b in re.findall(r'\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:', stderr)]
    assert logged == [(i, frames[n]['pts']) for i, n in enumerate(selected)], 'showinfo/frame PTS mismatch'
    files = sorted(native.glob('*.png'))
    assert len(files) == len(selected), 'PNG count mismatch'
    rows = []
    for order, (n, file) in enumerate(zip(selected, files), 1):
        assert file.name == f'frame-{order:06d}.png'
        with Image.open(file) as im:
            im.load()
            assert im.mode == 'RGB' and im.size == (stream['width'], stream['height']), 'PNG native mode/size mismatch'
            pixel_hash = hashlib.sha256(im.tobytes()).hexdigest()
        frame = frames[n]
        rows.append({'source_index': n, 'pts': frame['pts'], 'time_base': str(tb),
                     'pts_seconds_exact': str(frame['pts'] * tb),
                     'file': str(file.relative_to(dest)), 'width': stream['width'],
                     'height': stream['height'], 'rgb_sha256': pixel_hash,
                     'png_sha256': sha(file), 'sample_aspect_ratio': frame.get('sample_aspect_ratio'),
                     'interlaced_frame': frame.get('interlaced_frame'),
                     'top_field_first': frame.get('top_field_first')})
    identity(source, digest, size)
    save(dest / 'frames.json', rows)
    warnings = [line for line in stderr.splitlines() if re.search(r'\[(warning|error|fatal)\]', line)]
    save(dest / 'receipt.json', {'source': str(source), 'source_sha256': digest, 'source_bytes': size,
         'count': count, 'selected': selected, 'code_sha256': sha(Path(__file__)),
         'frame_plan_sha256': sha(BASE / 'FRAME-PLAN.md'), 'python': sys.version,
         'pillow': pillow_version, 'guess_layout_disabled': not guess,
         'warnings_require_manual_review': warnings,
         'automatic_checks': 'passed; descriptive derivatives only, not visual/human acceptance'})
    return rows


def control(dest):
    source = dest / 'synthetic.avi'
    pixels = b''.join(bytes(color) * (96 * 64) for color in
                      [(255, 0, 0)] * 60 + [(0, 255, 0)] * 60 + [(0, 0, 255)] * 5)
    command = [FFMPEG, '-nostdin', '-hide_banner', '-loglevel', 'level+info', '-n',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-video_size', '96x64', '-framerate', '30',
               '-i', 'pipe:0', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
               '-vf', 'setsar=4/3', '-c:v', 'ffv1', '-pix_fmt', 'bgr0',
               '-c:a', 'pcm_s16le', '-shortest', str(source)]
    run_command(command, dest, 'create-control', pixels)
    digest, size = sha(source), source.stat().st_size
    off = sample(source, digest, size, 125, dest / 'guess-off')
    on = sample(source, digest, size, 125, dest / 'guess-on', guess=True)
    assert off == on, 'guess option changes control output'
    expected = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 255)]
    for row, color in zip(off, expected):
        with Image.open(dest / 'guess-off' / row['file']) as im:
            assert im.tobytes() == bytes(color) * (96 * 64), 'control color mismatch'
        assert Fraction(row['pts_seconds_exact']) == Fraction(row['source_index'], 30), 'control PTS mismatch'
        assert row['sample_aspect_ratio'] == '4:3', 'control SAR mismatch'
    failures = {}
    for label, action in [
        ('wrong-hash', lambda: identity(source, '0' * 64, size)),
        ('wrong-count', lambda: inventory(json.loads((dest / 'guess-off/probe.stdout').read_text()), 124)),
        ('existing-destination', lambda: sample(source, digest, size, 125, dest / 'guess-off')),
    ]:
        try:
            action()
        except (AssertionError, FileExistsError) as exc:
            failures[label] = type(exc).__name__
        else:
            raise AssertionError(f'negative control did not reject: {label}')
    save(dest / 'control-results.json', {'expected_indices': [0, 60, 120, 124],
         'exact_pixels_PTS_SAR_and_guess_option_comparison': 'passed',
         'negative_controls_rejected': failures})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--control', action='store_true')
    args = parser.parse_args()
    assert args.out.is_absolute(), 'absolute output path required'
    args.out.mkdir()  # Never overwrite prior outputs, including failed attempts.
    run_command([FFMPEG, '-version'], args.out, 'ffmpeg-version')
    run_command([FFPROBE, '-version'], args.out, 'ffprobe-version')
    if args.control:
        control(args.out)
    else:
        for name, digest, size, count in SOURCES:
            sample(BASE / 'sources' / (name + '.avi'), digest, size, count, args.out / name)


if __name__ == '__main__':
    main()
