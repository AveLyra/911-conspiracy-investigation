"""Source-pinned native Y-plane screens; no scientific clock or cause inference."""
import argparse
import bisect
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import threading

import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TIMING = ROOT / 'research/sherlock-wtc7-investigation/timing-audit/run-2026-09-08-v1.1'
MEDIA = ROOT / 'research/wtc7-video-comparison/media/analysis-source'
FFMPEG = Path('/opt/homebrew/bin/ffmpeg')
SPECS = {
    'camera2': dict(id='VID-WTC7-001', name='NIST Camera 2_CBS-Net Dub6 48 (Converted).mov',
        source='84da90a48bdd710faf8b0a60c1a23a0927f22184216a1a631cbd77d4243b6730', size=208810910,
        map='ccc78c7ff933710f8e8e767dce5e05855fefb05bb75241d2bec01b4739c3b812',
        frames='424a2c27064548797ca9f4f0855781af490e4c912c7ccd5bc5340ee9a20524f0',
        identity='632c27b1ad4d04bddd991568a7c30206841ae3af5606fac801e61ffff561ca38',
        w=640, h=480, count=8042, tb='1/2997', selected=270),
    'camera4': dict(id='VID-WTC7-003', name='NIST Camera 4.mp4',
        source='af5c19dd597ecbe3cafbd163550fcd9c3ee9225d7f7b4f8e7000eb8ffb8232a3', size=1341523,
        map='8a4d55b65c866469b11b93e855ffe6886645d311bb823408e572e5ab731208bd',
        frames='9e6e7e940a63ac36f42b941db0527c3b18f58356e7cd8d911610b067f11afbe0',
        identity='03de2112746987b4f44b39626f7edda08d49c33fb24625cc05922ed737956681',
        w=480, h=360, count=1437, tb='1/90000', selected=49),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(path):
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': sha}


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def require(condition, code):
    if not condition:
        raise ValueError(code)


def integer(value):
    require(isinstance(value, str) and re.fullmatch(r'-?(0|[1-9][0-9]*)', value), 'integer')
    return int(value)


def read_map(text, tb):
    rows = list(csv.DictReader(io.StringIO(text)))
    require(bool(rows) and Fraction(tb) > 0, 'empty-or-timebase')
    previous = None
    for i, row in enumerate(rows):
        pts = integer(row['source_pts'])
        require(integer(row['frame_index_zero_based']) == i, 'index')
        require(row['source_time_base'] == tb, 'timebase')
        require(integer(row['best_effort_timestamp']) == pts, 'best-effort')
        exact = pts * Fraction(tb)
        require(Fraction(row['source_time_seconds_exact']) == exact, 'time')
        require(previous is None or exact > previous, 'nonmonotonic')
        require(re.fullmatch('[0-9a-f]{64}', row['decoded_sha256']), 'hash-format')
        previous = exact
    return rows


def selection(rows):
    times = [Fraction(row['source_time_seconds_exact']) for row in rows]
    selected = {}
    for second in range(0, int(times[-1] // 1) + 1):
        idx = bisect.bisect_left(times, Fraction(second))
        selected.setdefault(idx, []).append(f'first-at-or-after-{second}s')
    selected.setdefault(len(rows) - 1, []).append('last-frame')
    return selected


def consume(stream, rows, w, h, selected, out):
    require(w > 0 and h > 0 and w % 2 == h % 2 == 0, 'geometry')
    require(all(type(i) is int and 0 <= i < len(rows) for i in selected), 'selection-index')
    stride = w * h * 3 // 2
    products = []
    raw_digest = hashlib.sha256()
    for idx, row in enumerate(rows):
        chunks = bytearray()
        while len(chunks) < stride:
            part = stream.read(stride - len(chunks))
            require(bool(part), 'short-frame-stream')
            chunks.extend(part)
        require(digest(chunks) == row['decoded_sha256'], 'raw-frame-hash')
        raw_digest.update(chunks)
        if idx in selected:
            luma = bytes(chunks[:w * h])
            name = f'f{idx:06d}.png'
            im = Image.frombytes('L', (w, h), luma)
            im.save(out / name)
            with Image.open(out / name) as reopened:
                require(reopened.mode == 'L' and reopened.size == (w, h)
                        and reopened.tobytes() == luma, 'png-roundtrip')
            products.append(dict(row, selection_reasons=selected[idx], png=name,
                                 luma_sha256=digest(luma), png_identity=fingerprint(out / name)))
    require(not stream.read(1), 'extra-frame-stream')
    return {'checked_frames': len(rows), 'raw_stream_sha256': raw_digest.hexdigest(),
            'geometry': [w, h], 'images': products}


def command(source):
    return [str(FFMPEG), '-nostdin', '-nostats', '-hide_banner', '-v', 'warning',
            '-copyts', '-noautorotate', '-i', str(source), '-map', '0:v:0', '-an',
            '-noautoscale', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
            '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']


def classify_diagnostics(data):
    lines = data.splitlines()
    pattern = rb'\[aist#0:[0-9]+/pcm_s16le @ 0x[0-9a-f]+\] Guessed Channel Layout: stereo'
    require(all(re.fullmatch(pattern, line) for line in lines), 'decoder-diagnostics')
    return {'audio_layout_guess_stereo_lines': len(lines), 'unclassified_lines': 0,
            'raw_local_log': 'decoder.local-only.log'}


def decode(source, rows, w, h, selected, out):
    cmd = command(source)
    expired = threading.Event()
    with (out / 'decoder.local-only.log').open('xb') as diagnostic:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=diagnostic)
        def stop_child():
            expired.set()
            proc.kill()
        timer = threading.Timer(55, stop_child)
        timer.start()
        try:
            result = consume(proc.stdout, rows, w, h, selected, out)
            code = proc.wait(timeout=5)
        finally:
            timer.cancel()
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)
            proc.stdout.close()
    require(not expired.is_set(), 'decoder-watchdog')
    require(code == 0, 'decoder-exit')
    diagnostics = classify_diagnostics((out / 'decoder.local-only.log').read_bytes())
    result.update(command=cmd, exit_code=code, diagnostics=diagnostics)
    return result


def sheets(result, out):
    w, h = result['geometry']
    tw, th = w // 2, h // 2
    images = result['images']
    names = []
    for start in range(0, len(images), 16):
        sheet = Image.new('L', (4 * tw, 4 * (th + 26)), 255)
        draw = ImageDraw.Draw(sheet)
        for j, row in enumerate(images[start:start + 16]):
            x, y = (j % 4) * tw, (j // 4) * (th + 26)
            with Image.open(out / row['png']) as source:
                sheet.paste(source.resize((tw, th), Image.Resampling.BOX), (x, y))
            draw.text((x+3, y+th+2), f"frame {row['frame_index_zero_based']} | {float(Fraction(row['source_time_seconds_exact'])):.6f} s", fill=0)
        name = f'overview-{start // 16:02d}.png'
        sheet.save(out / name)
        names.append(name)
    return names


def inputs(spec):
    source = MEDIA / spec['name']
    old = TIMING / spec['id']
    expected = [(source, spec['source']), (old/'frame-map.csv', spec['map']),
                (old/'frames.json', spec['frames']), (old/'source-identity.json', spec['identity'])]
    for path, sha in expected:
        require(fingerprint(path)['sha256'] == sha, 'input-pin')
    require(source.stat().st_size == spec['size'], 'source-size')
    rows = read_map((old / 'frame-map.csv').read_text(), spec['tb'])
    frames = json.loads((old/'frames.json').read_text())['frames']
    require(len(rows) == len(frames) == spec['count'], 'map-count')
    for row, frame in zip(rows, frames):
        require((frame['width'], frame['height'], frame['pix_fmt']) == (spec['w'], spec['h'], 'yuv420p'), 'frame-format')
        require(type(frame['pts']) is int and frame['pts'] == int(row['source_pts']), 'frame-pts')
    return rows, {str(p.relative_to(ROOT)): fingerprint(p) for p, _ in expected}


def run(out, refinement=None):
    out.mkdir(parents=True, exist_ok=False)
    for source, name in [(Path(__file__), 'extract-snapshot.py'), (HERE/'PROTOCOL.md', 'protocol-snapshot.md')]:
        (out/name).write_bytes(source.read_bytes())
    if refinement:
        (out/'refinement-snapshot.json').write_bytes(refinement.read_bytes())
    initial = {str(p): fingerprint(p) for p in [Path(__file__), HERE/'PROTOCOL.md', FFMPEG, Path(sys.executable)]}
    if refinement:
        initial[str(refinement)] = fingerprint(refinement)
    config = json.loads(refinement.read_text()) if refinement else None
    write_json(out/'initial.json', dict(pins=initial, python=sys.version, executable=sys.executable,
        pillow=PIL.__version__, ffmpeg_version=subprocess.check_output([str(FFMPEG), '-version'], text=True).splitlines()[0],
        refinement=config))
    reports = {}
    try:
        for name, spec in SPECS.items():
            rows, before = inputs(spec)
            selected = selection(rows) if config is None else {i: ['declared-refinement'] for i in config[name]}
            if config is None:
                require(len(selected) == spec['selected'], 'selection-count')
            dest = out/name
            dest.mkdir()
            report = decode(MEDIA/spec['name'], rows, spec['w'], spec['h'], selected, dest)
            report['overview_sheets'] = sheets(report, dest)
            require(inputs(spec)[1] == before, 'post-input-pin')
            report['input_pins'] = before
            write_json(dest/'selection.json', report)
            reports[name] = dict(checked_frames=report['checked_frames'], selected=len(selected))
        require(all(fingerprint(Path(p)) == fp for p, fp in initial.items()), 'post-runtime-pin')
        products = {str(p.relative_to(out)): fingerprint(p) for p in sorted(out.rglob('*')) if p.is_file()}
        write_json(out/'receipt.json', dict(status='complete', cameras=reports, products=products))
    except Exception as exc:
        write_json(out/'failure.json', dict(status='failed', completed=reports, exception=type(exc).__name__))
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--refinement', type=Path)
    args = parser.parse_args()
    run(args.out, args.refinement)
