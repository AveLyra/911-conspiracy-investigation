#!/usr/bin/env python3
"""Build only a deterministic localization UI packet; never decode or annotate.

--self-test uses synthetic bytes/metadata only.  `build --out packet01` is a
separate root-authorized operation after code review. Existing outputs are
never replaced. Original images are pinned routes, not copied or converted.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import struct
import tempfile
import unittest
import zlib

HERE = Path(__file__).resolve().parent
CONTINUITY = HERE.parent / 'continuity-274-411'
R1 = HERE.parent.parent / 'comparator-r1-replication'
PROTOCOL_HASH = '1846d0e0cc532009e7941608ef39af3444fb01b365c670a19a08325af6c5046d'
SOURCE_HASH = 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e'
VERIFICATION_HASH = '4d98bc4c4f26a0b889466071419a8f3edeb090c1798e1ccae0db325cf5e34325'
CORE_SOURCE_HASH = '38cc0cd9b0947e05072ec8656c58e4fc4ca95d968bd1a903af26afe43db0b05b'
CORE_HASH = '9cff4290fc41e27126b36402818b1ecb55057e003f819ecbe8cef53281d2e2c4'
HANDLER_HASH = '1ea233c4fa8074298f9791a305fa46f0b1ac3151ce00ce48c8edd7e99de48142'
CONTROL_HASH = 'f0a96bf21d7ec0d2b8b486050d111b803dd708645fb1b3ad1659c3eda2edaf48'
FRAME_ORDER = [274, 300, 342, 365, 388, 411]
COPY_FILES = ('review.html', 'review.mjs', 'response.mjs')
GENERATED_FILES = ('coordinate-core.mjs', 'assets.mjs')
TIMESTAMP_FIELDS = ('stored_pts', 'best_effort_timestamp',
                    'stored_pts_seconds_exact', 'best_effort_seconds_exact')
CODE_ROUTES = {'/': 'review.html', '/review.mjs': 'review.mjs',
               '/response.mjs': 'response.mjs', '/coordinate-core.mjs': 'coordinate-core.mjs',
               '/assets.mjs': 'assets.mjs'}
# This inherited executable alias is recorded twice in the frozen660-pin
# receipt. It is not a served asset/module/source exception or a path search.
INHERITED_BINARY_ALIASES = {
    Path('/opt/homebrew/bin/ffmpeg'): Path('/opt/homebrew/Cellar/ffmpeg/7.1.1_3/bin/ffmpeg'),
}


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(data):
    return {'bytes': len(data), 'sha256': digest(data)}


def read_pinned(path, expected=None):
    path = Path(path)
    require(not path.is_symlink() and path.is_file(), 'not a regular unsymlinked input: ' + str(path))
    data = path.read_bytes()
    actual = identity(data)
    if expected is not None:
        require(actual == expected if isinstance(expected, dict) else actual['sha256'] == expected,
                'input identity mismatch: ' + str(path))
    return data


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('utf-8')


def safe_output(name, root=HERE):
    require(isinstance(name, str) and re.fullmatch(r'packet[0-9]{2,}', name), 'unsafe packet directory name')
    out = root / name
    require(not out.exists() and not out.is_symlink(), 'packet directory already exists')
    return out


def extract_core(data):
    require(digest(data) == CORE_SOURCE_HASH, 'upstream coordinate helper hash mismatch')
    prefix = data[:2524]
    require(digest(prefix) == CORE_HASH and data[2524:].startswith(b'function initializeReview() {'),
            'pure helper boundary/hash mismatch')
    return prefix


def png_header(data, width, height, mode):
    """Header assertion only; byte pins preserve the earlier checked pixels."""
    require(mode in ('L', 'RGB'), 'unsupported declared PNG mode')
    require(len(data) >= 33 and data[:16] == b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR', 'PNG header missing')
    require(struct.unpack('>IIBBBBB', data[16:29]) ==
            (width, height, 8, 0 if mode == 'L' else 2, 0, 0, 0), 'PNG dimensions/mode mismatch')
    require(struct.unpack('>I', data[29:33])[0] == zlib.crc32(data[12:29]), 'PNG IHDR CRC mismatch')


def make_asset(row):
    ordinal = row['index']
    require(type(ordinal) is int and ordinal in FRAME_ORDER, 'unselected frame')
    native = row['native']
    require(native['path'] == f'native/frame-{ordinal:04d}.png'
            and native['mode'] == 'L' and native['size'] == [704, 480], 'native frame contract changed')
    require(type(native['bytes']) is int and native['bytes'] > 0
            and re.fullmatch(r'[0-9a-f]{64}', native['sha256']), 'invalid frame identity')
    result = {'url': f'/frames/{ordinal}.png', 'width': 704, 'height': 480, 'mode': 'L',
              'bytes': native['bytes'], 'sha256': native['sha256'], 'ordinal': ordinal, 'synthetic': False}
    for key in TIMESTAMP_FIELDS:
        value = row[key]  # A missing key is not silently turned into null.
        if key.endswith('_exact'):
            require(value is None or isinstance(value, str), 'exact timestamp must be string or null')
        else:
            require(value is None or type(value) is int, 'stored timestamp must be integer or null')
        result[key] = value
    for key, seconds in (('stored_pts', 'stored_pts_seconds_exact'),
                         ('best_effort_timestamp', 'best_effort_seconds_exact')):
        require((result[key] is None) == (result[seconds] is None), 'nullable timestamp pair mismatch')
    return result


def assets_module(assets):
    require(set(assets) == {'control', *(str(n) for n in FRAME_ORDER)}, 'exact seven assets required')
    # Client-facing metadata contains route URLs, never local filesystem paths.
    values = [('FRAME_ORDER', FRAME_ORDER), ('ASSETS', assets),
              ('SOURCE_HASH', SOURCE_HASH), ('PROTOCOL_HASH', PROTOCOL_HASH)]
    return ('// Generated from pinned records; no observations or acceptance.\n' +
            ''.join('export const ' + name + ' = ' + json.dumps(value, sort_keys=True, indent=2) + ';\n'
                    for name, value in values)).encode('utf-8')


def verify_binary_alias(path, expected, records, aliases=INHERITED_BINARY_ALIASES):
    path = Path(path)
    require(path in aliases and path.is_symlink(), 'unlisted or missing inherited binary alias')
    target = aliases[path]
    require(str(path) in records and str(target) in records
            and records[str(path)] == expected == records[str(target)], 'alias/target pins missing or unequal')
    require(not target.is_symlink() and target.is_file()
            and target.resolve(strict=True) == target, 'declared canonical binary target missing or aliased')
    link_before = path.readlink()
    require(path.resolve(strict=True) == target, 'inherited alias resolves to wrong canonical target')
    target_data = read_pinned(target, expected)
    alias_data = path.read_bytes()
    require(identity(alias_data) == expected and alias_data == target_data, 'inherited alias bytes mismatch')
    require(path.is_symlink() and path.readlink() == link_before
            and path.resolve(strict=True) == target, 'inherited binary alias changed during read')


def verify_closure(records):
    require(isinstance(records, dict) and len(records) == 660, 'expected exactly660 frozen input pins')
    for path, expected in records.items():
        require(Path(path).is_absolute(), 'closure path must be absolute')
        require(isinstance(expected, dict) and set(expected) == {'bytes', 'sha256'}, 'invalid closure pin')
        if Path(path) in INHERITED_BINARY_ALIASES:
            verify_binary_alias(path, expected, records)
        else:
            read_pinned(path, expected)


def expected_packet():
    """Read/hash existing bytes only. Does not open images in a decoder/viewer."""
    extra = {}

    def take(path, expected=None):
        data = read_pinned(path, expected)
        extra[str(path)] = identity(data)
        return data

    take(HERE / 'PROTOCOL.md', PROTOCOL_HASH)
    verification_path = CONTINUITY / 'final-verification.json'
    verification = json.loads(take(verification_path, VERIFICATION_HASH))
    require(verification['status'] == 'passed_with_explicit_scope_limits'
            and verification['counts']['required_pins_before_and_after'] == 660,
            'final verification contract changed')
    closure = verification['input_pins_unchanged']
    verify_closure(closure)
    for name in ('root-observations.json', 'peer-observations.json', 'run01/frames.json',
                 'run01/pages.json', 'run01/receipt.json'):
        require(str(CONTINUITY / name) in closure, 'required predecessor not in closure')
    media = HERE.parent / 'source/DistantViewWTC7.avi'
    require(closure[str(media)]['sha256'] == SOURCE_HASH, 'AVI provenance mismatch')
    frame_map = json.loads(take(CONTINUITY / 'run01/frames.json', closure[str(CONTINUITY / 'run01/frames.json')]))
    require([r['index'] for r in frame_map] == list(range(274, 412)), 'complete138-frame map required')
    core_source = R1 / 'coordinate.js'
    core = extract_core(take(core_source, CORE_SOURCE_HASH))
    take(R1 / 'serve_review.py', HANDLER_HASH)
    control = take(R1 / 'localization-control/fixture.png', CONTROL_HASH)
    png_header(control, 1280, 720, 'RGB')
    assets = {'control': {'url': '/control.png', 'width': 1280, 'height': 720, 'mode': 'RGB',
                         **identity(control), 'ordinal': None, 'synthetic': True,
                         **{key: None for key in TIMESTAMP_FIELDS}}}
    image_routes = {'/control.png': {'kind': 'source', 'path': str(R1 / 'localization-control/fixture.png'),
                                     **identity(control), 'mime': 'image/png'}}
    for ordinal in FRAME_ORDER:
        row = frame_map[ordinal - 274]
        asset = make_asset(row)
        path = CONTINUITY / 'run01' / row['native']['path']
        expected = {'bytes': asset['bytes'], 'sha256': asset['sha256']}
        require(closure[str(path)] == expected, 'selected image outside verified closure')
        data = take(path, expected)
        png_header(data, 704, 480, 'L')
        assets[str(ordinal)] = asset
        image_routes[asset['url']] = {'kind': 'source', 'path': str(path), **expected, 'mime': 'image/png'}
    products = {name: take(HERE / name) for name in COPY_FILES}
    products['coordinate-core.mjs'] = core
    products['assets.mjs'] = assets_module(assets)
    take(Path(__file__).resolve())
    take(HERE / 'serve_review.py')
    routes = {route: {'kind': 'packet', 'path': name, **identity(products[name]),
                      'mime': 'text/html; charset=utf-8' if name.endswith('.html') else 'text/javascript; charset=utf-8'}
              for route, name in CODE_ROUTES.items()}
    routes.update(image_routes)
    require(len(routes) == 12, 'route count mismatch')
    # Detect changes during preparation; all predecessor pins remain original.
    verify_closure(closure)
    for path, expected in extra.items():
        read_pinned(path, expected)
    manifest = {'schema': 'distantview-localization-packet-v1', 'scope': 'human pilot preparation only',
                'frame_order': FRAME_ORDER, 'assets': assets, 'routes': routes,
                'source_sha256': SOURCE_HASH, 'protocol_sha256': PROTOCOL_HASH,
                'closure_receipt': {'path': str(verification_path), 'sha256': VERIFICATION_HASH},
                'prior_input_pins_unchanged': closure, 'packet_input_pins_unchanged': extra,
                'inherited_binary_aliases': {str(alias): str(target)
                                             for alias, target in INHERITED_BINARY_ALIASES.items()},
                'mapping_helper': {'source': str(core_source), 'source_sha256': CORE_SOURCE_HASH,
                                   'byte_range_half_open': [0, 2524], 'generated_sha256': CORE_HASH},
                'copied_ui': {name: identity(products[name]) for name in COPY_FILES},
                'products': {name: identity(data) for name, data in products.items()},
                'source_images_copied_or_converted': False, 'historical_coordinates_generated': False,
                'human_observations_or_acceptance': False,
                'limits': ['PNG header checks and byte integrity, not a new pixel-decode audit.',
                           'Coordinate bookkeeping is not feature accuracy or original exposure timing.',
                           'A syntactically valid inspected boolean does not authenticate a human.']}
    products['manifest.json'] = json_bytes(manifest)
    return products, manifest


def write_products(directory, products):
    directory.mkdir()
    for name, data in products.items():
        require(Path(name).name == name and name in (*COPY_FILES, *GENERATED_FILES, 'manifest.json'), 'unexpected product')
        with (directory / name).open('xb') as stream:
            stream.write(data)
        require((directory / name).read_bytes() == data, 'saved product differs')


def build(name):
    output = safe_output(name)
    products, manifest = expected_packet()
    write_products(output, products)
    try:
        repeated, _ = expected_packet()
        require(repeated == products, 'inputs changed during packet save')
    except Exception as exc:
        with (output / 'failure.json').open('x') as stream:
            json.dump({'status': 'incomplete_not_admitted', 'error': str(exc)}, stream)
        raise
    return output, identity(products['manifest.json'])


def check_packet(directory):
    require(directory.parent == HERE and re.fullmatch(r'packet[0-9]{2,}', directory.name)
            and directory.is_dir() and not directory.is_symlink(), 'invalid packet directory')
    expected, manifest = expected_packet()
    require({p.name for p in directory.iterdir()} == set(expected), 'unexpected/missing packet products')
    for name, data in expected.items():
        require(read_pinned(directory / name, identity(data)) == data, 'packet differs')
    return manifest


class Controls(unittest.TestCase):
    def row(self):
        return {'index': 274, 'native': {'path': 'native/frame-0274.png', 'mode': 'L', 'size': [704, 480],
                                        'bytes': 123, 'sha256': 'a' * 64},
                'stored_pts': None, 'best_effort_timestamp': 0,
                'stored_pts_seconds_exact': None, 'best_effort_seconds_exact': '0'}

    def header(self, mode='L', width=704, height=480):
        payload = b'IHDR' + struct.pack('>IIBBBBB', width, height, 8, 0 if mode == 'L' else 2, 0, 0, 0)
        return b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + payload + struct.pack('>I', zlib.crc32(payload))

    def test_modes_and_crc(self):
        png_header(self.header(), 704, 480, 'L')
        png_header(self.header('RGB', 1280, 720), 1280, 720, 'RGB')
        for data, width, height, mode in ((self.header(), 704, 480, 'RGB'),
                                          (self.header(), 705, 480, 'L'),
                                          (self.header()[:-1] + b'\x00', 704, 480, 'L')):
            with self.assertRaises(ValueError): png_header(data, width, height, mode)

    def test_nullable_zero_preserved(self):
        row = self.row(); asset = make_asset(row)
        self.assertIsNone(asset['stored_pts'])
        self.assertEqual(asset['best_effort_timestamp'], 0)
        self.assertEqual(asset['best_effort_seconds_exact'], '0')
        self.assertFalse(asset['synthetic'])
        self.assertEqual(asset['url'], '/frames/274.png')

    def test_timestamp_missing_filled_or_wrong_type_rejected(self):
        row = self.row(); del row['stored_pts']
        with self.assertRaises(KeyError): make_asset(row)
        for changes in ({'stored_pts_seconds_exact': '0'}, {'best_effort_timestamp': True}):
            row = self.row(); row.update(changes)
            with self.assertRaises(ValueError): make_asset(row)

    def test_wrong_frame_path_mode_and_geometry_rejected(self):
        for key, value in (('path', '../../other.png'), ('mode', 'RGB'), ('size', [480, 704])):
            row = self.row(); row['native'][key] = value
            with self.assertRaises(ValueError): make_asset(row)
        row = self.row(); row['index'] = 275
        with self.assertRaises(ValueError): make_asset(row)

    def test_pins_wrong_missing_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory(prefix='localization-build-synthetic-') as temp:
            path = Path(temp) / 'input'; path.write_bytes(b'fixture')
            self.assertEqual(read_pinned(path, identity(b'fixture')), b'fixture')
            with self.assertRaises(ValueError): read_pinned(path, '0' * 64)
            link = Path(temp) / 'link'; link.symlink_to(path)
            with self.assertRaises(ValueError): read_pinned(link)
            with self.assertRaises(ValueError): read_pinned(Path(temp) / 'missing')

    def test_core_wrong_pin_rejected_before_use(self):
        with self.assertRaises(ValueError): extract_core(b'export const forged=true;')

    def alias_fixture(self, temp):
        root = Path(temp).resolve()
        target = root / 'canonical'; target.write_bytes(b'synthetic binary bytes')
        alias = root / 'alias'; alias.symlink_to(target)
        expected = identity(target.read_bytes())
        return alias, target, expected, {str(alias): expected, str(target): expected}, {alias: target}

    def test_inherited_alias_good_but_general_reader_still_refuses(self):
        with tempfile.TemporaryDirectory(prefix='localization-alias-synthetic-') as temp:
            alias, target, expected, records, aliases = self.alias_fixture(temp)
            verify_binary_alias(alias, expected, records, aliases)
            with self.assertRaises(ValueError): read_pinned(alias, expected)
            self.assertEqual(read_pinned(target, expected), b'synthetic binary bytes')

    def test_inherited_alias_bad_target_even_identical_bytes(self):
        with tempfile.TemporaryDirectory(prefix='localization-alias-synthetic-') as temp:
            alias, target, expected, records, aliases = self.alias_fixture(temp)
            other = target.with_name('other'); other.write_bytes(target.read_bytes())
            alias.unlink(); alias.symlink_to(other)
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, records, aliases)

    def test_inherited_alias_unlisted_refused(self):
        with tempfile.TemporaryDirectory(prefix='localization-alias-synthetic-') as temp:
            alias, _, expected, records, _ = self.alias_fixture(temp)
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, records, {})

    def test_inherited_alias_mismatched_pins_or_bytes_refused(self):
        with tempfile.TemporaryDirectory(prefix='localization-alias-synthetic-') as temp:
            alias, target, expected, records, aliases = self.alias_fixture(temp)
            altered = dict(records); altered[str(target)] = {'bytes': 1, 'sha256': '0' * 64}
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, altered, aliases)
            target.write_bytes(b'changed synthetic bytes')
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, records, aliases)

    def test_inherited_alias_missing_record_file_or_alias_refused(self):
        with tempfile.TemporaryDirectory(prefix='localization-alias-synthetic-') as temp:
            alias, target, expected, records, aliases = self.alias_fixture(temp)
            for omitted in (str(alias), str(target)):
                incomplete = dict(records); del incomplete[omitted]
                with self.assertRaises(ValueError): verify_binary_alias(alias, expected, incomplete, aliases)
            alias.unlink()
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, records, aliases)
            alias.write_bytes(target.read_bytes())
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, records, aliases)
            alias.unlink(); alias.symlink_to(target); target.unlink()
            with self.assertRaises(ValueError): verify_binary_alias(alias, expected, records, aliases)

    def test_exact_closure_count_required(self):
        for value in ({}, [], {'/fixture': {'bytes': 1, 'sha256': '0' * 64}}):
            with self.assertRaises(ValueError): verify_closure(value)

    def test_generated_api_deterministic_and_exact_assets(self):
        assets = {str(n): {} for n in FRAME_ORDER}; assets['control'] = {}
        output = assets_module(assets)
        for name in ('FRAME_ORDER', 'ASSETS', 'SOURCE_HASH', 'PROTOCOL_HASH'):
            self.assertIn(('export const ' + name).encode(), output)
        self.assertEqual(output, assets_module(copy.deepcopy(assets)))
        assets['extra'] = {}
        with self.assertRaises(ValueError): assets_module(assets)

    def test_write_products_repeatable_exclusive(self):
        products = {'review.html': b'synthetic', 'manifest.json': b'{}\n'}
        with tempfile.TemporaryDirectory(prefix='localization-build-synthetic-') as temp:
            root = Path(temp)
            for name in ('packet01', 'packet02'):
                write_products(safe_output(name, root), products)
            self.assertEqual((root / 'packet01/review.html').read_bytes(), (root / 'packet02/review.html').read_bytes())
            with self.assertRaises(ValueError): safe_output('packet01', root)
            with self.assertRaises(FileExistsError): write_products(root / 'packet01', products)

    def test_safe_names(self):
        for name in ('../packet01', '/tmp/packet01', 'packet1', 'run01', '', None, 'packet01/a'):
            with self.assertRaises(ValueError): safe_output(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('action', nargs='?', choices=['build'])
    parser.add_argument('--out')
    args = parser.parse_args()
    if args.self_test:
        require(args.action is None and args.out is None, 'self-test cannot build historical packet')
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    require(args.action == 'build' and args.out is not None, 'explicit build --out required')
    output, manifest = build(args.out)
    print(json.dumps({'status': 'packet_prepared_not_human_reviewed', 'output': str(output), 'manifest': manifest}))


if __name__ == '__main__':
    main()
