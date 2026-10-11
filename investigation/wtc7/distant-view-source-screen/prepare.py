#!/usr/bin/env python3
"""Pinned adapter for the existing native-media screen; never executes a TRK."""
import argparse
import hashlib
import importlib.util
import io
import json
import ntpath
from pathlib import Path
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'tilted-camera-source-join' / 'prepare_media.py'
BASE_SHA = 'b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5'
PROTOCOL_SHA = '47cd92e19bc8d2796e66efaf3e828ba9589d3d254da920de3a6802e7727c0daf'
MEMBER = 'The Kit/WTC7-Dan Rather/DistantViewWTC7.trz'
MEMBER_SHA = '8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e'
MEDIA_NAME = 'DistantViewWTC7.avi'
MEDIA_SHA = 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e'
MEDIA_SIZE = 4749520


def digest(data):
    return hashlib.sha256(data).hexdigest()


def exact(data, size, expected, label):
    if len(data) != size or digest(data) != expected:
        raise ValueError(label + ' identity mismatch')


if digest(BASE.read_bytes()) != BASE_SHA:
    raise ValueError('frozen producer changed')
spec = importlib.util.spec_from_file_location('frozen_native_media_screen', BASE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.HERE = HERE
base.MEMBER = MEMBER
base.MEMBER_HASH = MEMBER_SHA
base.MEDIA_NAME = MEDIA_NAME
base.MEDIA_HASH = MEDIA_SHA
base.MEDIA = HERE / 'source' / MEDIA_NAME


def source_bytes():
    parent_before = base.pin(base.PARENT)
    base.require(parent_before['sha256'] == base.PARENT_HASH, 'parent identity')
    with zipfile.ZipFile(base.PARENT) as outer:
        entries = [i for i in outer.infolist() if i.filename == MEMBER]
        base.require(len(entries) == 1, 'outer member must be unique')
        nested = base.bounded(outer, entries[0])
        exact(nested, 9477547, MEMBER_SHA, 'selected TRZ')
    with zipfile.ZipFile(io.BytesIO(nested)) as inner:
        infos = inner.infolist()
        base.require(len(infos) == 5, 'changed inner inventory')
        copies = []
        for ordinal in (2, 3):
            item = infos[ordinal]
            base.require(ntpath.basename(item.filename) == MEDIA_NAME, 'wrong media member')
            content = base.bounded(inner, item)
            exact(content, MEDIA_SIZE, MEDIA_SHA, 'selected media')
            copies.append(content)
        base.require(copies[0] == copies[1], 'duplicate media mismatch')
    base.require(base.pin(base.PARENT) == parent_before, 'parent changed during read')
    return copies[0], parent_before


def preserve():
    base.require(not base.MEDIA.parent.exists(), 'source destination already exists')
    content, parent_before = source_bytes()
    base.MEDIA.parent.mkdir()
    with base.MEDIA.open('xb') as stream:
        stream.write(content)
    base.require(base.pin(base.MEDIA)['sha256'] == MEDIA_SHA, 'output media identity')
    base.write_json(base.MEDIA.parent / 'receipt.json', {
        'parent': parent_before, 'outer_member': MEMBER,
        'outer_sha256': MEMBER_SHA, 'ordinals': [2, 3],
        'media': base.pin(base.MEDIA), 'output_name': MEDIA_NAME,
        'archive_path_used_as_output': False, 'adapter': base.pin(__file__),
        'base_producer': base.pin(BASE), 'protocol': base.pin(HERE / 'PROTOCOL.md'),
    })
    print(json.dumps({'status': 'preserved', 'media': base.pin(base.MEDIA)}))


def provenance(out):
    # The base receipt correctly pins the base producer. Add the adapter too.
    base.write_json(HERE / out / 'adapter-receipt.json', {
        'adapter': base.pin(__file__), 'base_producer': base.pin(BASE),
        'protocol': base.pin(HERE / 'PROTOCOL.md'),
        'source_receipt': base.pin(HERE / 'source' / 'receipt.json'),
    })


class AdapterControls(unittest.TestCase):
    def test_wrong_size(self):
        with self.assertRaises(ValueError):
            exact(b'abc', 4, digest(b'abc'), 'fixture')

    def test_wrong_hash(self):
        with self.assertRaises(ValueError):
            exact(b'abc', 3, digest(b'abd'), 'fixture')

    def test_exact(self):
        exact(b'abc', 3, digest(b'abc'), 'fixture')

    def test_selection_962(self):
        self.assertEqual(base.selected_indices(962), [0, 137, 274, 411, 549, 686, 823, 961])

    def test_frozen_source_routing(self):
        self.assertEqual(base.MEDIA.parent.parent, HERE)
        self.assertEqual(base.MEDIA.name, MEDIA_NAME)
        self.assertEqual(base.MEDIA_HASH, MEDIA_SHA)
        self.assertNotEqual(base.MEDIA, BASE.parent / 'source' / MEDIA_NAME)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['test', 'preserve', 'probe', 'decode'])
    parser.add_argument('--out')
    parser.add_argument('--probe')
    args = parser.parse_args()
    base.require(base.pin(HERE / 'PROTOCOL.md')['sha256'] == PROTOCOL_SHA, 'protocol changed')
    if args.stage == 'test':
        suite = unittest.TestSuite([
            unittest.defaultTestLoader.loadTestsFromTestCase(base.Controls),
            unittest.defaultTestLoader.loadTestsFromTestCase(AdapterControls),
        ])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(not result.wasSuccessful())
    if args.stage == 'preserve':
        preserve()
    elif args.stage == 'probe':
        base.stage_probe(args.out)
        provenance(args.out)
    else:
        base.stage_decode(args.probe, args.out)
        provenance(args.out)


if __name__ == '__main__':
    main()
