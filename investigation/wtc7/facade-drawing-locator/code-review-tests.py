"""Independent synthetic locator regressions; no real roots or source payloads.

Run with python3 -B code-review-tests.py [--source-version original|repaired].
The original replay expects and demonstrates the preserved ZIP64 defect.
All fixture writes are confined to a new TemporaryDirectory under /private/tmp.
"""
import argparse
import importlib.util
import io
import json
from pathlib import Path
import re
import struct
import sys
import tempfile
import zipfile
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def replay(original=False):
    base = HERE / 'source-v1' if original else HERE

    def load(name):
        spec = importlib.util.spec_from_file_location(name, base / (name + '.py'))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    m = load('locate')
    ids = load('check_identifiers')
    tests = []
    before = {n: m.pin(base / n) for n in ('locate.py', 'check_identifiers.py')}

    def check(label, actual, expected):
        assert actual == expected, (label, actual, expected)
        tests.append({'test': label, 'actual': actual})

    for name, case, expected in [
        ('wtci_120_i', 'WTCI-000120-I.PDF', True),
        ('wtci_120_i', 'FOIA_12-178_NIST_WTC_Investigation_WTCI-120-I.iso_mount', True),
        ('wtci_120_i', 'wtci_120_i.pdf', True),
        ('wtci_120_i', 'WTCI-120-II.PDF', False),
        ('wtci_120_i', 'WTCI-120-I2.PDF', False),
        ('foia_12_178', 'NIST_FOIA_12-178_Jul_12_2012', True),
        ('foia_12_178', 'FOIA12_178', True),
        ('foia_12_178', 'FOIA_12-1780.zip', False),
        ('export_folder', '120806_1247', True),
        ('export_folder', '120806-1247/', True),
        ('export_folder', '120806_12470', False),
    ]:
        check(case, bool(re.search(ids.PATTERNS[name], case, re.I)), expected)
    check('missing left boundary accepts prefix digit',
          bool(re.search(ids.PATTERNS['export_folder'], '9120806_1247')), True)
    check('FOIA trailing letter accepted',
          bool(re.search(ids.PATTERNS['foia_12_178'], 'FOIA_12-178x')), True)
    check('ISO presence in unsupported set', '.iso' in m.OTHER_CONTAINERS, not original)
    check('ZST presence in unsupported set', '.zst' in m.OTHER_CONTAINERS, not original)

    with tempfile.TemporaryDirectory(prefix='wtc7-locator-review-', dir='/private/tmp') as tmp:
        t = Path(tmp)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('drawings/North-Elevation.txt', 'synthetic fixture only')
            z.writestr('nested.zip', b'not opened')
        data = buf.getvalue()
        e = data.rfind(b'PK\x05\x06')
        fields = list(struct.unpack('<4s4H2LH', data[e:e+22]))
        valid = t / 'synthetic.zip'
        valid.write_bytes(data)
        with patch.object(zipfile.ZipFile, 'open', side_effect=AssertionError('payload opened')):
            r = m.archive_metadata(valid)
        check('normal ZIP metadata status', r['status'], 'members_listed_no_payload_read')
        check('normal ZIP member count', r['member_count'], 2)
        check('normal ZIP hit count', len(r['matches']), 1)
        check('normal ZIP nested count', r['nested_container_count'], 1)
        check('raw name not exported', 'North-Elevation' in json.dumps(r), False)

        bad = t / 'notzip.zip'
        bad.write_bytes(b'not a zip')
        check('no EOCD', m.archive_metadata(bad)['status'], 'no_bounded_eocd')
        trailing = t / 'trailing.zip'
        trailing.write_bytes(data + b'extra')
        check('trailing EOCD', m.archive_metadata(trailing)['status'], 'ambiguous_or_trailing_eocd')

        def legacy_variant(name, idx, value):
            fs = fields.copy()
            fs[idx] = value
            p = t / name
            p.write_bytes(data[:e] + struct.pack('<4s4H2LH', *fs))
            return p

        check('multidisk', m.archive_metadata(legacy_variant('multi.zip', 1, 1))['status'],
              'multidisk_not_listed')
        check('ZIP64 sentinel',
              m.archive_metadata(legacy_variant('sentinel.zip', 5, 0xffffffff))['status'],
              'zip64_not_listed')
        check('directory cap',
              m.archive_metadata(legacy_variant('cap.zip', 5, 32*1024**2+1))['status'],
              'directory_cap')
        blocked = t / 'NIST_WTC7_FOIA_11-209.zip'
        blocked.write_bytes(data)
        check('pending packet', m.archive_metadata(blocked)['status'],
              'prior_approval_boundary_not_opened')
        sym = t / 'link.zip'
        sym.symlink_to(valid)
        check('file symlink direct guard', m.archive_metadata(sym)['status'], 'symlink_not_opened')
        huge = t / 'huge.zip'
        with huge.open('wb') as f:
            f.truncate(1024**3+1)
        check('sparse over-byte cap', m.archive_metadata(huge)['status'], 'over_byte_cap')

        z64 = struct.pack('<4sQ2H2L4Q', b'PK\x06\x06', 44, 45, 45, 0, 0,
                          fields[3], fields[4], fields[5], fields[6])
        locator = struct.pack('<4sLQL', b'PK\x06\x07', 0, e, 1)
        p64 = t / 'nonsentinel64.zip'
        p64.write_bytes(data[:e] + z64 + locator + data[e:])
        check('ZIP64 nonsentinel result', m.archive_metadata(p64)['status'],
              'members_listed_no_payload_read' if original else 'zip64_not_listed')
        oversized = struct.pack('<4sQ2H2L4Q', b'PK\x06\x06', 44, 45, 45, 0, 0,
                                fields[3], fields[4], 64*1024**2, fields[6])
        oversized_path = t / 'oversized64.zip'
        oversized_path.write_bytes(data[:e] + oversized + locator + data[e:])
        with oversized_path.open('rb') as f:
            effective = zipfile._EndRecData(f)
        check('ZIP64 effective size', effective[zipfile._ECD_SIZE], 64*1024**2)
        entered = []

        def reject_after_entry(*args, **kwargs):
            entered.append(True)
            raise ValueError('synthetic stop before read')

        with patch.object(zipfile, 'ZipFile', side_effect=reject_after_entry):
            result = m.archive_metadata(oversized_path)
        check('oversized ZIP64 constructor entry', entered, [True] if original else [])
        if not original:
            check('oversized ZIP64 revised status', result['status'], 'zip64_not_listed')

        root = t / 'paths'
        root.mkdir()
        (root / 'real.txt').write_text('synthetic')
        (root / 'symbolic.txt').symlink_to(root / 'real.txt')
        (root / 'dirlink').symlink_to(root, target_is_directory=True)
        listed, status = m.listed(root)
        check('rg file and directory symlink omission', [p.name for p in listed], ['real.txt'])

        if not original:
            long_fields = fields.copy()
            long_fields[7] = 65535
            long_eocd = struct.pack('<4s4H2LH', *long_fields) + b'C'*65535
            p_long = t / 'maxcomment.zip'
            p_long.write_bytes(data[:e] + long_eocd)
            check('max-comment ordinary ZIP accepted', m.archive_metadata(p_long)['status'],
                  'members_listed_no_payload_read')
            p_long64 = t / 'maxcomment64.zip'
            p_long64.write_bytes(data[:e] + z64 + locator + long_eocd)
            check('max-comment ZIP64 rejected', m.archive_metadata(p_long64)['status'],
                  'zip64_not_listed')
            entered.clear()
            with patch.object(zipfile, 'ZipFile', side_effect=reject_after_entry):
                m.archive_metadata(p_long64)
            check('max-comment ZIP64 stops before ZipFile', entered, [])
            check('EOCD disk count mismatch',
                  m.archive_metadata(legacy_variant('countdisk.zip', 3, 3))['status'],
                  'multidisk_not_listed')
            fs = fields.copy()
            fs[3] = fs[4] = 1
            mismatch = t / 'badcount.zip'
            mismatch.write_bytes(data[:e] + struct.pack('<4s4H2LH', *fs))
            check('central actual count mismatch', m.archive_metadata(mismatch)['status'],
                  'metadata_read_failed')

    after = {n: m.pin(base / n) for n in before}
    if not original:
        check('source unchanged during replay', after, before)
    else:
        # Additional stability assertion is kept outside the original 32-case ledger.
        assert before == after
    assert len(tests) == (32 if original else 39)
    return {'source_version': 'original' if original else 'repaired',
            'test_count': len(tests), 'tests': tests, 'before_after_pins': before,
            'harness_pin': m.pin(Path(__file__)), 'python': sys.version}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-version', choices=('original', 'repaired'), default='repaired')
    args = parser.parse_args()
    print(json.dumps(replay(original=args.source_version == 'original'), indent=2))
