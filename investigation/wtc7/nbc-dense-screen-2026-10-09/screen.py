#!/usr/bin/env python3
"""Bounded picture screening; no audio analysis or historical clock inference."""
import hashlib
import json
import platform
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ACQ = Path('/Users/admin/docs/911-worktrees/nbc-media-acquisition-2026-10-09/research/sherlock-wtc7-investigation/nbc-media-acquisition-2026-10-09')
FFMPEG = '/opt/homebrew/bin/ffmpeg'
FFPROBE = '/opt/homebrew/bin/ffprobe'


def identity(path):
    with Path(path).open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': Path(path).stat().st_size, 'sha256': digest}


def save(path, data):
    with Path(path).open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def select(frames, tick, all_frames):
    if not frames:
        raise ValueError('No frames')
    times = [int(f['best_effort_timestamp']) * tick for f in frames]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError('Non-increasing best-effort timestamps')
    indices, occupied = [], set()
    for i, time in enumerate(times):
        cell = time // 1
        if all_frames or cell not in occupied:
            indices.append(i)
        occupied.add(cell)
    if indices[-1] != len(times) - 1:
        indices.append(len(times) - 1)
    return indices, times


def tests():
    frames = [{'best_effort_timestamp': p} for p in [1, 5, 10, 19, 30, 32]]
    assert select(frames, Fraction(1, 10), False)[0] == [0, 2, 4, 5]
    assert select(frames, Fraction(1, 10), True)[0] == list(range(6))
    assert select([{'best_effort_timestamp': 0}], Fraction(1), False)[0] == [0]
    for bad in [[], [{'best_effort_timestamp': 1}] * 2,
                [{'best_effort_timestamp': 2}, {'best_effort_timestamp': 1}], [{}]]:
        try:
            select(bad, Fraction(1), False)
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError('Invalid clock was admitted')
    print('7 selection checks passed')


def main(run):
    if run not in ('run01', 'run02'):
        raise ValueError('Use a declared fresh run')
    out = HERE / run
    out.mkdir()
    inputs = [HERE / 'PROTOCOL.md', Path(__file__), ACQ / 'manifest.json']
    before = {str(p): identity(p) for p in inputs}
    receipt = {'status': 'started', 'inputs_before': before,
               'python': platform.python_version(), 'pillow': Image.__version__,
               'binaries': {p: identity(p) for p in (FFMPEG, FFPROBE)}, 'commands': [], 'sources': {}}
    save(out / 'start.json', receipt)

    def command(argv, label):
        result = subprocess.run(argv, capture_output=True, timeout=180)
        (out / (label + '.stderr.txt')).write_bytes(result.stderr)
        (out / (label + '.stdout')).write_bytes(result.stdout)
        receipt['commands'].append({'argv': argv, 'exit_code': result.returncode, 'label': label})
        if result.returncode:
            raise RuntimeError(label + ' failed; preserved diagnostics')
        return result

    try:
        manifest = json.loads((ACQ / 'manifest.json').read_text())
        for label, source in zip(('small', 'large'), manifest['sources'], strict=True):
            path = ACQ / source['path']
            expected = {'bytes': source['acquired_size_bytes'], 'sha256': source['sha256']}
            if identity(path) != expected:
                raise ValueError('Source identity mismatch')
            receipt['sources'][label] = {'path': str(path), 'before': expected}
            result = command([FFPROBE, '-v', 'warning', '-select_streams', 'v:0', '-show_streams',
                              '-show_frames', '-show_entries',
                              'frame=pts,best_effort_timestamp,width,height:stream=width,height,time_base,sample_aspect_ratio,display_aspect_ratio',
                              '-of', 'json', str(path)], label + '-inventory')
            data = json.loads(result.stdout)
            stream, = data['streams']
            frames = data['frames']
            if (stream['width'], stream['height']) != (320, 240):
                raise ValueError('Unexpected raster')
            if any((f['width'], f['height']) != (320, 240) for f in frames):
                raise ValueError('Changing raster')
            tick = Fraction(stream['time_base'])
            indices, times = select(frames, tick, label == 'small')
            native = out / label
            native.mkdir()
            expr = '+'.join(f'eq(n,{i})' for i in indices)
            result = command([FFMPEG, '-hide_banner', '-nostdin', '-loglevel', 'info', '-n',
                              '-copyts', '-noautorotate', '-i', str(path), '-map', '0:v:0', '-an',
                              '-vf', f"select='{expr}',format=rgb24,showinfo", '-fps_mode', 'passthrough',
                              '-enc_time_base:v', 'demux', '-frames:v', str(len(indices)),
                              str(native / 'frame-%04d.png')], label + '-extract')
            log = result.stderr.decode(errors='replace')
            shown = re.findall(r'\[Parsed_showinfo_[^\]]+\]\s+n:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([^ ]+).*?\bs:(\d+)x(\d+)\b', log)
            bases = re.findall(r'config in time_base: (\d+/\d+)', log)
            if not bases or any(Fraction(b) != tick for b in bases):
                raise ValueError('Decode time base mismatch')
            paths = sorted(native.glob('frame-*.png'))
            if len(paths) != len(indices) or len(shown) != len(indices):
                raise ValueError('Selection/count mismatch')
            rows = []
            for slot, (i, png, display) in enumerate(zip(indices, paths, shown, strict=True)):
                n, pts, seconds, width, height = display
                if (int(n), int(pts), int(width), int(height)) != (slot, frames[i]['best_effort_timestamp'], 320, 240):
                    raise ValueError('Decoded identity mismatch')
                with Image.open(png) as im:
                    if im.size != (320, 240) or im.mode != 'RGB':
                        raise ValueError('PNG raster mismatch')
                rows.append({'source_index': i, 'pts': frames[i].get('pts'),
                             'best_effort_timestamp': frames[i]['best_effort_timestamp'],
                             'time_base': str(tick), 'seconds_exact': str(times[i]),
                             'png': str(png.relative_to(out)), **identity(png)})
            save(out / (label + '-selected.json'), rows)
            sheets = out / (label + '-sheets')
            sheets.mkdir()
            for start in range(0, len(rows), 20):
                group = rows[start:start + 20]
                image = Image.new('RGB', (1280, 268 * ((len(group) + 3) // 4)), 'white')
                draw = ImageDraw.Draw(image)
                for slot, row in enumerate(group):
                    x, y = slot % 4 * 320, slot // 4 * 268
                    with Image.open(out / row['png']) as im:
                        image.paste(im, (x, y))
                    draw.text((x + 3, y + 243), f"n={row['source_index']} PTS={float(Fraction(row['seconds_exact'])):.6f}s", fill='black')
                image.save(sheets / f'sheet-{start // 20:02d}.png')
            receipt['sources'][label].update({'after': identity(path), 'decoded_count': len(frames),
                'selected_count': len(rows), 'max_selected_gap_seconds': str(max((times[b] - times[a] for a, b in zip(indices, indices[1:])), default=Fraction(0))),
                'diagnostic_lines': [line for line in log.splitlines() if re.search(r'corrupt|damaged|warning|error|conceal|not available', line, re.I)]})
            if receipt['sources'][label]['after'] != expected:
                raise ValueError('Source changed')
        receipt['inputs_after'] = {str(p): identity(p) for p in inputs}
        if receipt['inputs_after'] != before:
            raise ValueError('Controlled input changed')
        receipt['status'] = 'complete'
    except Exception as error:
        receipt.update({'status': 'failed', 'failure': type(error).__name__ + ': ' + str(error)})
        raise
    finally:
        receipt['products'] = {str(p.relative_to(out)): identity(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'start.json'}
        save(out / 'receipt.json', receipt)
    print(json.dumps({key: {k: v for k, v in value.items() if k in ('decoded_count', 'selected_count', 'max_selected_gap_seconds')} for key, value in receipt['sources'].items()}))


if __name__ == '__main__':
    tests()
    if sys.argv[1:] != ['--test']:
        main(sys.argv[1])
