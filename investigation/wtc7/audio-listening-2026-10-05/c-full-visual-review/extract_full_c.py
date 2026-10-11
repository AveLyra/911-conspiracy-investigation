#!/usr/bin/env python3
"""Bounded full-C extension using the preserved PTS-checked extractor."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
EXTRACTOR = MAIN / 'research/sherlock-wtc7-investigation/acoustic-audit/av-correspondence/extract_frames.py'
REFERENCE = MAIN / 'research/sherlock-wtc7-investigation/fire-originals/peskin/sample_every_second.py'
PINS = {
    EXTRACTOR: '2fc45bb67ba656c3670fea188f2b71261a9ca315718aaf92e16010ef4bcceb6a',
    REFERENCE: 'a913be680052ceb61ddf1ed89ef675c9d21972f8869a62e9e038be2f8048d40b',
}


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=['run01', 'run02'])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError('Refusing existing output')
    for path, pin in PINS.items():
        if digest(path) != pin:
            raise ValueError('Preserved implementation pin mismatch')
    spec = importlib.util.spec_from_file_location('preserved_av_extractor', EXTRACTOR)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    identity, save = helper.identity, helper.save
    source, pin, size = helper.SOURCES['compilation']
    expected = {'sha256': pin, 'bytes': size}
    if identity(source) != expected:
        raise ValueError('Source pin mismatch')
    controlled = [HERE / 'protocol.json', Path(__file__), EXTRACTOR, REFERENCE]
    before = {str(path): identity(path) for path in controlled}
    out.mkdir()
    runner = helper.Runner(out)
    receipt = {
        'status': 'started', 'source': str(source), 'source_before': expected,
        'inputs_before': before, 'python': platform.python_version(),
        'pillow': helper.Image.__version__, 'numpy': helper.np.__version__,
        'binary_pins': {p: identity(Path(p)) for p in (helper.FFMPEG, helper.FFPROBE)},
    }
    save(out / 'start.json', receipt)
    try:
        helper.synthetic(runner)
        video, frames = helper.probe(runner, source, 'compilation')
        if (video['width'], video['height'], video['sample_aspect_ratio']) != (1280, 720, '1:1'):
            raise ValueError('Source raster contract mismatch')
        plan = [(430, 455, None)]
        selected = helper.choose(frames, Fraction(video['time_base']), plan)
        if [row['source_index'] for row in selected] != list(range(12900, 13650)):
            raise ValueError('Declared full interval index coverage differs')
        if any(Fraction(row['source_seconds_exact']) != Fraction(row['source_index'], 30) for row in selected):
            raise ValueError('Declared cadence differs from source PTS')
        rows = helper.extract(runner, source, 'compilation', video, frames, plan)
        helper.sheets(out, 'compilation', rows)
        fixed = [row for row in rows if Fraction(row['source_seconds_exact']).denominator == 1]
        if len(rows) != 750 or len(fixed) != 25:
            raise ValueError('Historical count mismatch')
        save(out / 'fixed-native-selection.json', fixed)
        old_root = EXTRACTOR.parent / 'run01'
        old_map = old_root / 'compilation-selected.json'
        old_rows = json.loads(old_map.read_text())
        old = {row['source_index']: row for row in old_rows if Fraction(434) <= Fraction(row['source_seconds_exact']) < Fraction(443)}
        new = {row['source_index']: row for row in rows}
        if sorted(old) != list(range(13020, 13290)):
            raise ValueError('Old interval coverage differs')
        for index, row in old.items():
            if identity(old_root / row['png']) != {'sha256': new[index]['sha256'], 'bytes': new[index]['bytes']}:
                raise ValueError('Old/new overlapping frame bytes differ')
        receipt['old_overlap'] = {'count': len(old), 'map': identity(old_map), 'all_png_bytes_equal': True}
        receipt['source_after'] = identity(source)
        receipt['inputs_after'] = {str(path): identity(path) for path in controlled}
        receipt['binary_pins_after'] = {p: identity(Path(p)) for p in (helper.FFMPEG, helper.FFPROBE)}
        if receipt['source_after'] != expected or receipt['inputs_after'] != before or receipt['binary_pins_after'] != receipt['binary_pins']:
            raise ValueError('Controlled input or binary changed')
        receipt['status'] = 'complete'
        receipt['historical_frames'] = len(rows)
        receipt['overview_sheets'] = len(list((out / 'compilation-overview').glob('*.png')))
    except Exception as error:
        receipt['status'] = 'failed'
        receipt['failure_type'] = type(error).__name__
        receipt['failure_category'] = str(error) if isinstance(error, ValueError) else 'Inspect retained local diagnostics'
        raise
    finally:
        receipt['commands'] = runner.commands
        receipt['products'] = {str(p.relative_to(out)): identity(p) for p in sorted(out.rglob('*'))
                               if p.is_file() and '.local.' not in p.name and p.name not in ('start.json', 'receipt.json')}
        save(out / 'receipt.json', receipt)
    print(json.dumps({'run': args.run, 'status': 'complete', 'historical_frames': 750, 'old_overlap_equal': 270}))


if __name__ == '__main__':
    main()
