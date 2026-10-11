#!/usr/bin/env python3
"""Pinned native [10,18) extraction; no scoring, source or clock inference."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import signal
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
EXTRACTOR = MAIN / 'research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/extract_frames.py'
REFERENCE = MAIN / 'research/sherlock-wtc7-investigation/fire-originals/peskin/sample_every_second.py'
PINS = {
    EXTRACTOR: '2fc45bb67ba656c3670fea188f2b71261a9ca315718aaf92e16010ef4bcceb6a',
    REFERENCE: 'a913be680052ceb61ddf1ed89ef675c9d21972f8869a62e9e038be2f8048d40b',
    HERE.parent / 'config.json': '56efd21495ef21b37df9137438f0b53183a120b59b1b43eb0f498b4ac47d65b2',
}


def pin(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=['extract01', 'extract02'])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError('Refusing existing output')
    for path, digest in PINS.items():
        if pin(path)['sha256'] != digest:
            raise ValueError('Preserved implementation/config pin mismatch')
    config = json.loads((HERE.parent / 'config.json').read_text())
    source = Path(config['early_video']['path'])
    expected = {k: config['early_video'][k] for k in ('bytes', 'sha256')}
    if pin(source) != expected:
        raise ValueError('Source pin mismatch')
    review = json.loads((HERE / 'preparation-review.json').read_text())
    if review.get('decision') != 'proceed_with_boundaries' or review.get('protocol_sha256') != pin(HERE / 'PROTOCOL.md')['sha256']:
        raise ValueError('Prospective review missing or stale')
    spec = importlib.util.spec_from_file_location('preserved_native_extractor', EXTRACTOR)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    if (platform.python_version(), helper.np.__version__, helper.Image.__version__) != ('3.13.7', '2.3.4', '12.0.0'):
        raise ValueError('Declared runtime differs')
    controlled = [Path(__file__), HERE / 'PROTOCOL.md', HERE / 'preparation-review.json', *PINS,
                  Path(sys.executable), Path(helper.np.__file__), Path(helper.Image.__file__),
                  Path(helper.FFMPEG), Path(helper.FFPROBE)]
    before = {str(p): pin(p) for p in controlled}
    out.mkdir()
    runner = helper.Runner(out)
    start = time.monotonic()
    receipt = {'status': 'started', 'source': str(source), 'source_before': expected,
               'before': before, 'plan': [[10, 18, None]], 'max_seconds': 600,
               'max_output_bytes': 402653184, 'python': platform.python_version(),
               'numpy': helper.np.__version__, 'pillow': helper.Image.__version__}
    helper.save(out / 'start.json', receipt)

    def budget():
        if time.monotonic() - start > 600:
            raise RuntimeError('Wall time cap')
        if sum(p.stat().st_size for p in out.rglob('*') if p.is_file()) > 402653184:
            raise RuntimeError('Output byte cap')

    def timeout(*_):
        raise RuntimeError('Wall time cap')

    old = signal.signal(signal.SIGALRM, timeout)
    signal.alarm(600)
    try:
        helper.synthetic(runner)
        budget()
        video, frames = helper.probe(runner, source, 'early-dense')
        if (video['width'], video['height'], video['sample_aspect_ratio'], video['time_base'], len(frames)) != (320, 224, '1:1', '1/30000', 1130):
            raise ValueError('Source geometry/clock/frame count differs')
        if Fraction(video['avg_frame_rate']) != Fraction(30000, 1001):
            raise ValueError('Nominal source rate differs')
        selected = helper.choose(frames, Fraction(video['time_base']), [(10, 18, None)])
        if [r['source_index'] for r in selected] != list(range(300, 540)):
            raise ValueError('Expected source indices 300 through 539')
        rows = helper.extract(runner, source, 'early-dense', video, frames, [(10, 18, None)])
        budget()
        helper.sheets(out, 'early-dense', rows)
        coarse_path = Path(config['early_map']['path'])
        if pin(coarse_path)['sha256'] != config['early_map']['sha256']:
            raise ValueError('Coarse map pin mismatch')
        coarse = {r['source_index']: r for r in json.loads(coarse_path.read_text())}
        overlaps = []
        for row in rows:
            if row['source_index'] not in range(300, 511, 30):
                continue
            original = coarse[row['source_index']]
            for key in ('source_pts', 'source_time_base', 'source_seconds_exact', 'bytes', 'sha256'):
                if row[key] != original[key]:
                    raise ValueError('Prior overlapping sample differs')
            if pin(coarse_path.parent / original['png']) != pin(out / row['png']):
                raise ValueError('Prior PNG differs')
            overlaps.append(row['source_index'])
        if overlaps != list(range(300, 511, 30)):
            raise ValueError('Eight coarse overlaps incomplete')
        helper.save(out / 'coarse-overlap-check.json', {'indices': overlaps, 'map': str(coarse_path), 'map_pin': pin(coarse_path), 'pass': True})
        receipt['source_after'] = pin(source)
        receipt['after'] = {str(p): pin(p) for p in controlled}
        if receipt['source_after'] != expected or receipt['after'] != before:
            raise ValueError('Controlled input changed')
        budget()
        receipt.update(status='complete', historical_frames=len(rows), overview_sheets=8)
    except Exception as exc:
        receipt.update(status='failed', failure_type=type(exc).__name__, failure_category=str(exc))
        raise
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        receipt['elapsed_s'] = time.monotonic() - start
        receipt['commands'] = runner.commands
        receipt['products'] = {str(p.relative_to(out)): pin(p) for p in sorted(out.rglob('*'))
                               if p.is_file() and '.local.' not in p.name and p.name not in ('start.json', 'receipt.json')}
        helper.save(out / 'receipt.json', receipt)
    print(json.dumps({'run': args.run, 'status': receipt['status'], 'frames': len(rows)}))


if __name__ == '__main__':
    main()
