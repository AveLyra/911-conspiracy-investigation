#!/usr/bin/env python3
"""Generate a labeled scientific control figure, never historical imagery."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main():
    here = Path(__file__).resolve().parent
    output = here / 'localization-control'
    if output.exists():
        raise FileExistsError('control_output_exists')
    output.mkdir()
    image = Image.new('RGB', (1280, 720), (244, 247, 250))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=24)
    # Corner targets are the first vertex of each filled shape, with no outline.
    a = [(521, 181), (675, 131), (929, 131), (929, 580), (521, 580)]
    draw.polygon(a, fill=(38, 97, 128))
    draw.rectangle((283, 457, 327, 617), fill=(92, 66, 118))
    draw.rectangle((1041, 594, 1211, 669), fill=(107, 79, 38))
    draw.text((490, 190), 'A', fill=(0, 0, 0), font=font)
    draw.text((248, 464), 'B', fill=(0, 0, 0), font=font)
    draw.text((1003, 601), 'C', fill=(0, 0, 0), font=font)
    draw.text((24, 24), 'SYNTHETIC COORDINATE CONTROL — NOT EVIDENCE', fill=(0, 0, 0), font=font)
    image.save(output / 'fixture.png')
    assert image.getpixel((521, 181)) == (38, 97, 128)
    assert image.getpixel((520, 181)) == (244, 247, 250)
    assert image.getpixel((283, 457)) == (92, 66, 118)
    assert image.getpixel((283, 456)) == (244, 247, 250)
    assert image.getpixel((1041, 594)) == (107, 79, 38)
    assert image.getpixel((1041, 593)) == (244, 247, 250)
    identity = lambda p: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    truth = {'synthetic_only': True, 'dimensions': [1280, 720],
             'points': {'A': [521, 181], 'B': [283, 457], 'C': [1041, 594]},
             'builder': identity(Path(__file__)),
             'protocol': identity(here / 'localization-control.md'),
             'fixture': identity(output / 'fixture.png'),
             'not_a_historical_localization_calibration': True}
    with (output / 'truth.json').open('x') as stream:
        json.dump(truth, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'synthetic_fixture_created', 'fixture': truth['fixture']}))


if __name__ == '__main__':
    main()
