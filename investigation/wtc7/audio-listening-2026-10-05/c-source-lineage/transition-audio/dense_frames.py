#!/usr/bin/env python3
"""All native frames in early-copy PTS [4,7), using the pinned extractor."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
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
SOURCE = HERE.parent / 'media/SIbqaybkbWI.f133.mp4'
EXPECTED = {'bytes': 758909, 'sha256': '3f6db089b0e89cdfc030f6aaaf81227931681d26e0bd3c801b98cdcf486ba0d7'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', choices=['dense01', 'dense02'])
    args = parser.parse_args()
    out = HERE / args.run
    if out.exists():
        raise FileExistsError('Refusing existing output')
    for path, pin in PINS.items():
        with path.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != pin:
                raise ValueError('Preserved implementation pin mismatch')
    spec = importlib.util.spec_from_file_location('preserved_av_extractor', EXTRACTOR)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    identity, save = helper.identity, helper.save
    if identity(SOURCE) != EXPECTED:
        raise ValueError('Source pin mismatch')
    controlled = [HERE / 'PROTOCOL.md', Path(__file__), EXTRACTOR, REFERENCE]
    before = {str(p): identity(p) for p in controlled}
    binaries = {p: identity(Path(p)) for p in (helper.FFMPEG, helper.FFPROBE)}
    out.mkdir()
    runner = helper.Runner(out)
    receipt = {'status': 'started', 'source': str(SOURCE), 'source_before': EXPECTED,
               'inputs_before': before, 'binary_pins': binaries, 'plan': [[4, 7, None]],
               'python': platform.python_version(), 'numpy': helper.np.__version__,
               'pillow': helper.Image.__version__}
    save(out / 'start.json', receipt)
    try:
        helper.synthetic(runner)
        video, frames = helper.probe(runner, SOURCE, 'early-dense')
        if (video['width'], video['height'], video['sample_aspect_ratio'], video['time_base']) != (320, 224, '1:1', '1/30000'):
            raise ValueError('Source geometry or time base differs')
        if Fraction(video['avg_frame_rate']) != Fraction(30000, 1001):
            raise ValueError('Source nominal frame rate differs')
        rows = helper.choose(frames, Fraction(video['time_base']), [(4, 7, None)])
        if [r['source_index'] for r in rows] != list(range(120, 210)):
            raise ValueError('Expected exactly source indices 120 through 209')
        rows = helper.extract(runner, SOURCE, 'early-dense', video, frames, [(4, 7, None)])
        helper.sheets(out, 'early-dense', rows)
        receipt['source_after'] = identity(SOURCE)
        receipt['inputs_after'] = {str(p): identity(p) for p in controlled}
        receipt['binary_pins_after'] = {p: identity(Path(p)) for p in (helper.FFMPEG, helper.FFPROBE)}
        if receipt['source_after'] != EXPECTED or receipt['inputs_after'] != before or receipt['binary_pins_after'] != binaries:
            raise ValueError('Controlled input or binary changed')
        receipt.update(status='complete', historical_frames=len(rows), overview_sheets=3)
    except Exception as error:
        receipt.update(status='failed', failure_type=type(error).__name__,
                       failure_category=str(error) if isinstance(error, ValueError) else 'Inspect retained local diagnostics')
        raise
    finally:
        receipt['commands'] = runner.commands
        receipt['products'] = {str(p.relative_to(out)): identity(p) for p in sorted(out.rglob('*'))
                               if p.is_file() and '.local.' not in p.name and p.name not in ('start.json', 'receipt.json')}
        save(out / 'receipt.json', receipt)
    print(f'{args.run}: complete; 90 native frames; 3 sheets; 6 synthetic checks')


if __name__ == '__main__':
    main()
