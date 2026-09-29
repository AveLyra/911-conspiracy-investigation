#!/usr/bin/env python3
"""Fixed comparator window; reuse the pinned full-decode A/V extraction route."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess

HERE = Path(__file__).resolve().parent
DEPENDENCY = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/extract_frames.py')
REFERENCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-originals/peskin/sample_every_second.py')
PINS = {
    DEPENDENCY: '2fc45bb67ba656c3670fea188f2b71261a9ca315718aaf92e16010ef4bcceb6a',
    REFERENCE: 'a913be680052ceb61ddf1ed89ef675c9d21972f8869a62e9e038be2f8048d40b',
    HERE / 'PROTOCOL.md': '1d1d1993a6d9a27f66037d5abef449ffe685e7238c20a81a9b85f97ae240883c',
}
for dependency, pin in PINS.items():
    if hashlib.sha256(dependency.read_bytes()).hexdigest() != pin:
        raise ValueError('Declared dependency/protocol pin mismatch')
spec = importlib.util.spec_from_file_location('held_av_helper', DEPENDENCY)
x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(x)


class PreservingRunner(x.Runner):
    def run(self, command, label, input_bytes=None, timeout=60):
        try:
            result = subprocess.run(command, input=input_bytes, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            (self.out / f'{label}.stderr.local.txt').write_bytes(exc.stderr or b'')
            (self.out / f'{label}.stdout.local.bin').write_bytes(exc.stdout or b'')
            self.commands.append({'argv':command, 'label':label, 'exit':None,
                                  'status':'timeout', 'timeout_seconds':timeout,
                                  'stderr_bytes':len(exc.stderr or b''), 'stdout_bytes':len(exc.stdout or b'')})
            raise
        (self.out / f'{label}.stderr.local.txt').write_bytes(result.stderr)
        self.commands.append({'argv':command, 'label':label, 'exit':result.returncode,
                              'stderr_bytes':len(result.stderr)})
        if result.returncode:
            (self.out / f'{label}.stdout.local.bin').write_bytes(result.stdout)
            raise RuntimeError(f'{label} failed; retain local diagnostics')
        return result


def boundary_plan(frames, tick, start, end):
    """Exact interval/index selection; floats only adapt the old JSON contract.

    The old helper records plan endpoints in JSON. Represent open inter-frame
    midpoints as floats only after requiring them strictly between the exact
    adjacent PTS. Then require identical selected indices. Measurement clocks
    remain the original exact rational PTS, never these selection sentinels.
    """
    tick, start, end = Fraction(tick), Fraction(start), Fraction(end)
    if tick <= 0 or end <= start or not frames:
        raise ValueError('Invalid interval or clock')
    times = [Fraction(f['pts']) * tick for f in frames]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError('Non-increasing PTS')
    interior = [i for i, t in enumerate(times) if start <= t < end]
    if not interior or interior[0] == 0 or interior[-1] == len(times) - 1:
        raise ValueError('Missing interval or immediate boundary frame')
    first, last = interior[0] - 1, interior[-1] + 1
    lower_neighbor = times[first - 1] if first else times[first] - tick
    upper_neighbor = times[last + 1] if last + 1 < len(times) else times[last] + tick
    low_exact = (lower_neighbor + times[first]) / 2
    high_exact = (times[last] + upper_neighbor) / 2
    low, high = float(low_exact), float(high_exact)
    if not lower_neighbor < low < times[first] or not times[last] < high < upper_neighbor:
        raise ValueError('Selection sentinel loses inter-frame precision')
    plan = [(low, high, None)]
    expected = list(range(first, last + 1))
    actual = [r['source_index'] for r in x.choose(frames, tick, plan)]
    if actual != expected:
        raise ValueError('Adapted helper selection differs from exact indices')
    return plan, expected, {'start': str(start), 'end': str(end),
                          'lower_sentinel_exact': str(low_exact),
                          'upper_sentinel_exact': str(high_exact)}


def selection_controls():
    def frames(values):
        return [{'pts': p} for p in values]
    checks = {}
    _, indices, _ = boundary_plan(frames([0, 2, 5, 9, 12, 20]), Fraction(1, 3), 1, 4)
    checks['irregular_half_open_with_neighbors'] = indices == [1, 2, 3, 4]
    _, indices, _ = boundary_plan(frames([50, 52, 55, 59, 62, 70]), Fraction(1, 3), 18, 20)
    checks['nonzero_start_with_neighbors'] = indices == [1, 2, 3, 4]
    for name, values, tick, start, end in [
        ('missing_left', [0, 1, 2], 1, 0, 1),
        ('missing_right', [0, 1, 2], 1, 2, 3),
        ('empty_interval', [0, 1, 2], 1, 3, 4),
        ('duplicate_clock', [0, 1, 1, 2], 1, 1, 2),
        ('backwards_clock', [0, 2, 1, 3], 1, 1, 2),
        ('zero_tick', [0, 1, 2, 3], 0, 1, 2),
        ('reversed_interval', [0, 1, 2, 3], 1, 2, 1),
        ('float_precision_collapse', [2**60 + k for k in range(6)], 1, 2**60+2, 2**60+4),
    ]:
        try:
            boundary_plan(frames(values), tick, start, end)
        except ValueError:
            checks[name + '_rejected'] = True
        else:
            checks[name + '_rejected'] = False
    if not all(checks.values()):
        raise ValueError('Boundary selection controls failed')
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=['run02', 'run03'])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError('Refusing existing output')
    source, pin, size = x.SOURCES['comparator']
    before = x.identity(source)
    if before != {'sha256': pin, 'bytes': size}:
        raise ValueError('Historical source pin mismatch')
    controls = selection_controls()
    out.mkdir()
    runner = PreservingRunner(out)
    receipt = {'status': 'started', 'source_path': str(source), 'source_before': before,
               'script': x.identity(Path(__file__)), 'dependencies': {str(p): x.identity(p) for p in PINS},
               'python': platform.python_version(), 'python_executable': x.identity(Path(__import__('sys').executable)),
               'pillow': x.Image.__version__, 'numpy': x.np.__version__,
               'binaries': {p: x.identity(Path(p)) for p in (x.FFMPEG, x.FFPROBE)}}
    x.save(out / 'start.json', receipt)
    # Generated snapshots preserve the exact implementation behind each receipt.
    (out / 'extract_window.py.snapshot').write_bytes(Path(__file__).read_bytes())
    try:
        x.save(out / 'selection-controls.json', controls)
        x.synthetic(runner)
        pixels = x.np.zeros((36, 48, 64, 3), dtype=x.np.uint8)
        for n in range(36):
            pixels[n, :, :, :] = [n*7 % 256, n*11 % 256, n*13 % 256]
            pixels[n, 4:20, 5:30, :] = [255-n, n, 90]
        for offset in (0, 5):
            label = f'synthetic-{offset}'
            video = json.loads((out / f'{label}-stream.json').read_text())['streams'][0]
            frames = json.loads((out / f'{label}-all-frame-pts.json').read_text())['frames']
            plan, indices, sentinels = boundary_plan(frames, video['time_base'], Fraction(offset)+Fraction(1,2), Fraction(offset)+Fraction(5,2))
            rows = x.extract(runner, out / f'{label}.mkv', label+'-boundary', video, frames, plan, pixels)
            if indices != list(range(5, 31)) or [r['source_index'] for r in rows] != indices:
                raise ValueError('Synthetic boundary coverage differs')
        video, frames = x.probe(runner, source, 'comparator')
        expected = {'width':1280, 'height':720, 'sample_aspect_ratio':'1:1', 'time_base':'1/30000', 'pix_fmt':'yuv420p'}
        if any(video.get(k) != v for k,v in expected.items()) or len(frames) != 1350:
            raise ValueError('Historical stream differs from declared contract')
        if video.get('side_data_list') or any(f['pts'] != f['best_effort_timestamp'] for f in frames):
            raise ValueError('Unexpected transform or frame clock ambiguity')
        for label in ('comparator-stream','comparator-frames'):
            if (out / f'{label}.stderr.local.txt').read_bytes().strip():
                raise ValueError('Probe diagnostic requires review')
        plan, indices, sentinels = boundary_plan(frames, video['time_base'], 8, 16)
        if indices != list(range(239,481)):
            raise ValueError('Historical index window differs from declared coverage')
        rows = x.extract(runner, source, 'comparator', video, frames, plan)
        if [r['source_index'] for r in rows] != indices:
            raise ValueError('Historical output mapping differs')
        x.save(out / 'selection-sentinels.json', sentinels)
        receipt['source_after'] = x.identity(source)
        if receipt['source_after'] != before:
            raise ValueError('Source changed')
        receipt['script_after'] = x.identity(Path(__file__))
        receipt['dependencies_after'] = {str(p):x.identity(p) for p in PINS}
        receipt['binaries_after'] = {p:x.identity(Path(p)) for p in (x.FFMPEG,x.FFPROBE)}
        receipt['python_executable_after'] = x.identity(Path(__import__('sys').executable))
        if any(receipt[a] != receipt[b] for a,b in [('script','script_after'), ('dependencies','dependencies_after'),
                                                  ('binaries','binaries_after'), ('python_executable','python_executable_after')]):
            raise ValueError('Implementation or runtime changed during extraction')
        receipt['status'] = 'complete'
        receipt['historical_frames'] = len(rows)
    except Exception as exc:
        receipt.update(status='failed', failure_type=type(exc).__name__)
        raise
    finally:
        receipt['commands'] = runner.commands
        receipt['products'] = {str(p.relative_to(out)): x.identity(p) for p in sorted(out.rglob('*'))
                               if p.is_file() and p.name not in ('start.json','receipt.json')}
        x.save(out / 'receipt.json', receipt)
    print(json.dumps({'run':args.run, 'status':receipt['status'], 'historical_frames':len(rows)}))


if __name__ == '__main__':
    main()
