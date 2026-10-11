#!/usr/bin/env python3
"""Fixed early-copy screen using the existing source-pinned PTS extractor."""
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
    parser.add_argument('run', choices=['screen01', 'screen02'])
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
    protocol = json.loads((HERE / 'screen-protocol.json').read_text())
    source = HERE / protocol['source']
    expected = {'sha256': protocol['sha256'], 'bytes': protocol['bytes']}
    if identity(source) != expected:
        raise ValueError('Source pin mismatch')
    controlled = [HERE / 'screen-protocol.json', Path(__file__), EXTRACTOR, REFERENCE]
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
        video, frames = helper.probe(runner, source, 'early-copy')
        for key in ('width', 'height', 'sample_aspect_ratio', 'time_base'):
            if video[key] != protocol[key]:
                raise ValueError('Source raster or clock contract differs')
        if Fraction(video['avg_frame_rate']) != Fraction(protocol['frame_rate']):
            raise ValueError('Source frame-rate contract differs')
        tick = Fraction(video['time_base'])
        plan = [(0, 38, 1)]
        selected = helper.choose(frames, tick, plan)
        if len(selected) != 38:
            raise ValueError('Expected all 38 integer-second bins')
        for target, row in enumerate(selected):
            index = row['source_index']
            t = Fraction(row['source_seconds_exact'])
            if not Fraction(target) <= t < target + 1:
                raise ValueError('Wrong target bin')
            if index > 0 and frames[index - 1]['pts'] * tick >= target:
                raise ValueError('Selected frame is not first after target')
        rows = helper.extract(runner, source, 'early-copy', video, frames, plan)
        helper.sheets(out, 'early-copy', rows)
        save(out / 'fixed-native-selection.json', [rows[t] for t in protocol['root_fixed_native_target_seconds']])
        receipt['source_after'] = identity(source)
        receipt['inputs_after'] = {str(path): identity(path) for path in controlled}
        receipt['binary_pins_after'] = {p: identity(Path(p)) for p in (helper.FFMPEG, helper.FFPROBE)}
        if receipt['source_after'] != expected or receipt['inputs_after'] != before or receipt['binary_pins_after'] != receipt['binary_pins']:
            raise ValueError('Controlled input or binary changed')
        receipt['status'] = 'complete'
        receipt['historical_frames'] = len(rows)
        receipt['overview_sheets'] = len(list((out / 'early-copy-overview').glob('*.png')))
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
    print(json.dumps({'run': args.run, 'status': 'complete', 'historical_frames': 38}))


if __name__ == '__main__':
    main()
