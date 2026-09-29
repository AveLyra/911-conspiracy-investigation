#!/usr/bin/env python3
"""Read-only pin/configuration arithmetic; writes one new local receipt.

The floor pairs below are explicit transcriptions from the already inspected
public sheet, not identified image endpoints or a historical trajectory.
No original project XML is parsed or emitted by this checker.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911')
PUBLIC = SOURCE / 'research/sherlock-wtc7-investigation'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = HERE / args.out
    if output.parent != HERE or output.exists():
        raise ValueError('Output must be a new file in this audit directory')
    checks = []

    def check(path, expected, role, size=None):
        actual = sha(path)
        ok = actual == expected and (size is None or path.stat().st_size == size)
        checks.append(dict(path=str(path), role=role, expected=expected,
                           sha256=actual, bytes=path.stat().st_size, match=ok))

    pins = json.loads((HERE / 'clock-source-pins.json').read_text())
    for row in pins['inputs']:
        check(Path(row['path']), row['sha256'], 'clock_source_pin', row['bytes'])
    nist_manifest = PUBLIC / 'nist-camera-method-audit/lineage-v1.json'
    nist = json.loads(nist_manifest.read_text())['sources'][0]
    check(SOURCE / nist['source'], nist['sha256_before'], 'primary_nist_pdf')
    selected = {306, 307, 308, 666, 667, 668, 669, 746, 749, 750}
    pages = [p for p in nist['pages'] if p['physical_pdf_page'] in selected]
    assert len(pages) == len(selected)
    for page in pages:
        for kind in ('png', 'text'):
            check(nist_manifest.parent / page[kind], page[kind + '_sha256'],
                  'previously_viewed_nist_' + kind)
    kit_manifest = PUBLIC / 'camera3-provenance/reading-products.json'
    kit = json.loads(kit_manifest.read_text())
    for source in kit['sources']:
        check(kit_manifest.parent / source['source'], source['source_sha256'],
              'public_calibration_pdf')
        for page in source['pages']:
            check(kit_manifest.parent / page['path'], page['sha256'],
                  'public_calibration_page_integrity_not_read_attestation')

    settings_path = PUBLIC / 'camera3-provenance/kit-inventory/run-v1/saved-tracker-settings.json'
    settings = json.loads(settings_path.read_text())

    def scalar(name, family):
        rows = [r for r in settings['selected_scalar_properties']
                if r['xml_path'].endswith('/property:' + name)
                and family in r['xml_path']]
        assert len(rows) == 1
        return Decimal(rows[0]['saved_text'])

    tapes = [r for r in settings['selected_array_summaries']
             if r['xml_path'].endswith('/property:worldlengths')]
    assert len(tapes) == 1 and len(tapes[0]['leaf_values']) == 1
    length = Decimal(tapes[0]['leaf_values'][0]['saved_text'])
    with localcontext() as context:
        context.prec = 40
        dx = scalar('x2', 'TapeMeasure') - scalar('x1', 'TapeMeasure')
        dy = scalar('y2', 'TapeMeasure') - scalar('y1', 'TapeMeasure')
        pixels = (dx * dx + dy * dy).sqrt()
        calculated_scale = pixels / length
        saved_scale = scalar('xscale', 'ImageCoordSystem')
        assert saved_scale == scalar('yscale', 'ImageCoordSystem')
        residual = calculated_scale - saved_scale
        assert abs(residual) < Decimal('1e-14')
        configuration = dict(assigned_metres=str(length), pixel_length=str(pixels),
                             pixels_per_assigned_metre=str(calculated_scale),
                             assigned_metres_per_pixel=str(1 / saved_scale),
                             scale_residual=str(residual))
    assigned_feet = Fraction(length) / Fraction('0.3048')
    # Three non-unique, sheet-level examples; not a complete pair census.
    pairs = [(30, 45, '688.250', '879.500'),
             (29, 44, '675.500', '866.750'),
             (28, 43, '662.750', '854.000')]
    pair_checks = []
    for low, high, low_ft, high_ft in pairs:
        distance = Fraction(high_ft) - Fraction(low_ft)
        assert distance == assigned_feet
        pair_checks.append(dict(lower_floor=low, upper_floor=high,
                                exact_feet=str(distance)))
    assert assigned_feet == 15 * Fraction('12.75')
    root = json.loads((HERE / 'independent-root01.json').read_text())
    reviewer = json.loads((HERE / 'independent-runs01.json').read_text())
    root.pop('command')
    reviewer.pop('command')
    assert root == reviewer and root['status'] == 'pass'
    result = dict(status='pass' if all(c['match'] for c in checks) else 'pin_mismatch',
                  python=platform.python_version(), script_sha256=sha(Path(__file__)),
                  checks=checks, configuration=configuration,
                  assigned_length_exact_feet=str(assigned_feet),
                  three_nonunique_floor_pairs=pair_checks,
                  metric_reviewer_root_equal_except_command=True,
                  limit='Integrity and assigned-configuration arithmetic only; no physical calibration or new motion fit')
    with output.open('x') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps(dict(status=result['status'], pin_checks=len(checks),
                          mismatches=[c['path'] for c in checks if not c['match']],
                          assigned_feet=str(assigned_feet),
                          configuration=configuration)))
    if result['status'] != 'pass':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
