#!/usr/bin/env python3
"""Read-only artifact verification. No producer imports or video decoding.

Default: deterministic JSON receipt on stdout; --self-test: synthetic controls.
Only the selected PNGs are losslessly decoded, using the standard library.
"""
import copy
from fractions import Fraction
import hashlib
import io
import json
import ntpath
from pathlib import Path
import platform
import re
import struct
import sys
import unittest
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
WORKTREE = HERE.parents[2]
PARENT = MAIN / 'research/sherlock-wtc7-investigation/camera3-provenance/WTC-911-Motion-Lab.zip'
MEMBER = 'The Kit/WTC7-Dan Rather/DistantViewWTC7.trz'
MEDIA = HERE / 'source/DistantViewWTC7.avi'
BASE = HERE.parent / 'tilted-camera-source-join/prepare_media.py'
EMPTY = hashlib.sha256(b'').hexdigest()
FIXED = {
    'PROTOCOL.md': '47cd92e19bc8d2796e66efaf3e828ba9589d3d254da920de3a6802e7727c0daf',
    'ORDINAL-ADDENDUM.md': '930123e028a5c0feadf58b6967cf1d789f5bc8a5e0d6fc12e582c527b3dfd293',
    'prepare.py': 'f3a3be5e9335cdf50b336fe29acd7d5d92b6e6b3f7b726a1427796e365241a93',
    'ordinal_screen.py': '1c1a91e26062155c842908dd29f631f0da0868a34f6cf1eee4c3c3b7aa412b59',
    '../tilted-camera-source-join/prepare_media.py': 'b8d2010b99001dba79d10b887571ffdfa53b13d8b6800f26a1ed4442c11ba0d5',
    'source/DistantViewWTC7.avi': 'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e',
}
SELECTED = [0, 137, 274, 411, 549, 686, 823, 961]


def require(value, label):
    if not value:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def read(path):
    return json.loads(Path(path).read_bytes())


def row_map(raw):
    require(len(raw['streams']) == 1, 'stream count')
    s = raw['streams'][0]
    w, h = s['width'], s['height']
    require(type(w) is int and type(h) is int and 0 < w <= 2000 and
            0 < h <= 2000 and w % 2 == h % 2 == 0, 'geometry')
    require(s['pix_fmt'] == 'yuv420p', 'stream format')
    tick = Fraction(s['time_base'])
    require(tick > 0, 'time base')
    frames = raw['frames']
    require(8 <= len(frames) <= 10000, 'frame count')
    rows = []
    previous = {'pts': None, 'best_effort_timestamp': None}
    for i, f in enumerate(frames):
        require((f['width'], f['height'], f['pix_fmt']) == (w, h, 'yuv420p'), 'frame geometry')
        row = {'index': i}
        for source, dest, seconds in (
            ('pts', 'stored_pts', 'stored_pts_seconds_exact'),
            ('best_effort_timestamp', 'best_effort_timestamp', 'best_effort_seconds_exact'),
        ):
            value = f.get(source)
            require(value is None or type(value) is int, 'timestamp type')
            if value is not None:
                require(previous[source] is None or value > previous[source], 'timestamp order')
                previous[source] = value
            row[dest] = value
            row[seconds] = None if value is None else str(Fraction(value) * tick)
        p, b = row['stored_pts'], row['best_effort_timestamp']
        require(p is None or b is None or p == b, 'timestamp agreement')
        rows.append(row)
    # Integer division is a floor operation; no floating-point sample rounding.
    indices = [divmod(k * (len(rows) - 1), 7)[0] for k in range(8)]
    require(len(set(indices)) == 8, 'distinct eight samples')
    return rows, indices


def gray_png(data):
    """Check PNG CRCs and reverse all five filters for 8-bit grayscale only."""
    require(data[:8] == b'\x89PNG\r\n\x1a\n', 'PNG signature')
    pos, chunks = 8, []
    while pos < len(data):
        require(pos + 12 <= len(data), 'PNG chunk header')
        size = struct.unpack('>I', data[pos:pos+4])[0]
        kind = data[pos+4:pos+8]
        end = pos + 12 + size
        require(end <= len(data), 'PNG chunk bounds')
        payload = data[pos+8:end-4]
        crc = struct.unpack('>I', data[end-4:end])[0]
        require(zlib.crc32(kind + payload) & 0xffffffff == crc, 'PNG CRC')
        chunks.append((kind, payload))
        pos = end
    require(chunks[0][0] == b'IHDR' and chunks[-1] == (b'IEND', b''), 'PNG structure')
    require([k for k, _ in chunks].count(b'IHDR') == 1 and
            all(k == b'IDAT' for k, _ in chunks[1:-1]), 'PNG supported chunks')
    w, h, depth, color, comp, filt, interlace = struct.unpack('>IIBBBBB', chunks[0][1])
    require(0 < w <= 2000 and 0 < h <= 2000, 'PNG bounded geometry')
    require((depth, color, comp, filt, interlace) == (8, 0, 0, 0, 0), 'PNG format')
    dec = zlib.decompressobj()
    raw = dec.decompress(b''.join(p for k, p in chunks if k == b'IDAT'), (w + 1) * h + 1)
    require(dec.eof and not dec.unused_data and not dec.unconsumed_tail and
            len(raw) == (w + 1) * h, 'PNG decompressed extent')
    pixels = bytearray(w * h)
    for y in range(h):
        mode = raw[y * (w + 1)]
        require(mode in range(5), 'PNG filter')
        for x in range(w):
            at = y * w + x
            left = pixels[at-1] if x else 0
            above = pixels[at-w] if y else 0
            upper_left = pixels[at-w-1] if x and y else 0
            if mode == 0:
                predictor = 0
            elif mode == 1:
                predictor = left
            elif mode == 2:
                predictor = above
            elif mode == 3:
                predictor = (left + above) // 2
            else:
                p = left + above - upper_left
                errors = [abs(p-left), abs(p-above), abs(p-upper_left)]
                predictor = [left, above, upper_left][errors.index(min(errors))]
            pixels[at] = (raw[y * (w + 1) + x + 1] + predictor) & 255
    return (w, h), bytes(pixels)


def required_paths():
    paths = [HERE / k for k in FIXED]
    paths += [Path(__file__), PARENT, MAIN/'AGENTS.md', MAIN/'WORKFLOW.md',
              MAIN/'START-HERE.md', MAIN/'research/sherlock-wtc7-investigation/CHARTER.md',
              WORKTREE/'AGENTS.md', Path('/opt/homebrew/bin/ffprobe'), Path('/opt/homebrew/bin/ffmpeg'),
              HERE/'source/receipt.json', HERE/'probe01/execution.json']
    for name in ('probe02', 'probe03'):
        paths += [HERE/name/f for f in ('execution.json', 'probe.json', 'selection.json',
                                        'ordinal-adapter-receipt.json')]
        paths += [HERE/(name+'-diagnostics')/f for f in ('execution.json', 'stderr.bin', 'probe-stdout.json')]
    for name in ('views01', 'views02'):
        paths += [HERE/name/f for f in ('execution.json', 'receipt.json', 'frames.json',
                                        'ordinal-adapter-receipt.json')]
        paths += [HERE/(name+'-diagnostics')/f for f in ('execution.json', 'stderr.bin')]
        paths += [HERE/name/f'frame-{i:04d}.png' for i in SELECTED]
    return sorted(set(p.resolve() for p in paths))


def diagnostics(name, execution, raw_stdout=None):
    directory = HERE/(name+'-diagnostics')
    d = read(directory/'execution.json')
    err = (directory/'stderr.bin').read_bytes()
    require(d['status'] == 'returned' and d['returncode'] == 0, 'diagnostic return')
    require(not err and d['stderr_bytes'] == 0 and d['stderr_sha256'] == EMPTY and
            d['stderr_truncated'] is False, 'diagnostic warnings/truncation')
    require(d['argv'] == execution['argv'], 'diagnostic argv')
    if raw_stdout is not None:
        require((d['stdout_bytes'], d['stdout_sha256']) == (len(raw_stdout), sha(raw_stdout)), 'probe stdout pin')
    else:
        require((d['stdout_bytes'], d['stdout_sha256']) ==
                (execution['raw_bytes'], execution['raw_sha256']), 'decode stdout receipt')
    return d


def verify():
    paths = required_paths()
    before = {str(p): pin(p) for p in paths}
    for name, expected in FIXED.items():
        require(pin(HERE/name)['sha256'] == expected, 'fixed pin ' + name)
    require(pin(PARENT) == {'bytes': 172774879, 'sha256': 'c983bdfaff683ac51c50b2c3808c1f77ad04a2b947e942d1ded986924c919189'}, 'parent pin')
    # Recheck only the specified archive member bodies; no extraction or media decoding.
    with zipfile.ZipFile(PARENT) as z:
        matches = [i for i in z.infolist() if i.filename == MEMBER]
        require(len(matches) == 1 and matches[0].file_size == 9477547 and not matches[0].flag_bits & 1, 'outer member identity')
        nested = z.read(matches[0])
    require(sha(nested) == '8afe02fa78440768ff01bf4cd7cdcd27cbe872466f46be80d79115708c381c0e', 'TRZ pin')
    saved = MEDIA.read_bytes()
    with zipfile.ZipFile(io.BytesIO(nested)) as z:
        members = z.infolist()
        require(len(members) == 5, 'nested count')
        for i in (2, 3):
            f = members[i]
            require(ntpath.basename(f.filename) == MEDIA.name and f.file_size == 4749520 and not f.flag_bits & 1, 'nested media identity')
            require(z.read(f) == saved, 'source exact member equality')
    source = read(HERE/'source/receipt.json')
    for field, path in (('parent', PARENT), ('media', MEDIA), ('adapter', HERE/'prepare.py'),
                        ('base_producer', BASE), ('protocol', HERE/'PROTOCOL.md')):
        require(source[field] == pin(path), 'source receipt ' + field)
    require(source['ordinals'] == [2, 3] and source['outer_member'] == MEMBER and
            source['outer_sha256'] == sha(nested) and source['output_name'] == MEDIA.name and
            source['archive_path_used_as_output'] is False, 'source receipt routing')
    common_pins = {'adapter': HERE/'ordinal_screen.py', 'first_adapter': HERE/'prepare.py',
                   'base_producer': BASE, 'protocol': HERE/'PROTOCOL.md',
                   'addendum': HERE/'ORDINAL-ADDENDUM.md', 'source_receipt': HERE/'source/receipt.json'}
    for name in ('probe02', 'probe03', 'views01', 'views02'):
        rec = read(HERE/name/'ordinal-adapter-receipt.json')
        require(set(rec) == set(common_pins) | {'diagnostics', 'scope'}, 'adapter receipt schema')
        for key, path in common_pins.items():
            require(rec[key] == pin(path), 'adapter pin '+name+'/'+key)
        require(rec['diagnostics'] == pin(HERE/(name+'-diagnostics')/'execution.json'), 'diagnostic pin')
        require(rec['scope'] == 'ordinal screen only; missing timestamps remain missing', 'adapter scope')
    maps, raw_probes = [], []
    for name in ('probe02', 'probe03'):
        raw_bytes = (HERE/(name+'-diagnostics')/'probe-stdout.json').read_bytes()
        raw = json.loads(raw_bytes)
        require(raw == read(HERE/name/'probe.json'), 'raw/normalized metadata equality')
        rows, indices = row_map(raw)
        require(len(rows) == 962 and indices == SELECTED, 'historical selection')
        s = raw['streams'][0]
        require((s['width'], s['height'], s['codec_name'], s['codec_type'], s['sample_aspect_ratio'], s['display_aspect_ratio']) ==
                (704, 480, 'mpeg4', 'video', '1:1', '22:15'), 'historical stream metadata')
        require(s['time_base'] == '100/2997' and int(s['nb_frames']) == 962, 'historical time base/count')
        expected = {'n': 962, 'geometry': [704, 480], 'time_base': s['time_base'],
                    'indices': indices, 'frames': rows,
                    'selection_rule': 'floor(k*(N-1)/7), k=0..7, distinct indices, declared before viewing'}
        require(read(HERE/name/'selection.json') == expected, 'complete selection mapping')
        ex = read(HERE/name/'execution.json')
        for field, path in (('binary', '/opt/homebrew/bin/ffprobe'), ('media', MEDIA),
                            ('producer', BASE), ('protocol', HERE/'PROTOCOL.md')):
            require(ex[field] == pin(path), 'probe receipt pin')
        require(ex['diagnostics'] == {'returncode': 0, 'stderr_bytes': 0, 'stderr_sha256': EMPTY}, 'probe status')
        require(ex['argv'][0] == '/opt/homebrew/bin/ffprobe' and ex['argv'][-1] == str(MEDIA) and
                ex['argv'][1:6] == ['-v', 'warning', '-select_streams', 'v:0', '-show_entries'] and
                ex['argv'][-3:-1] == ['-of', 'json'] and len(ex['argv']) == 10, 'probe command')
        diagnostics(name, ex, raw_bytes)
        maps.append(rows)
        raw_probes.append(raw_bytes)
    require(raw_probes[0] == raw_probes[1] and maps[0] == maps[1], 'repeated raw metadata')
    for f in ('probe.json', 'selection.json', 'execution.json'):
        require((HERE/'probe02'/f).read_bytes() == (HERE/'probe03'/f).read_bytes(), 'probe byte repeat '+f)
    all_frames = []
    png_rows = []
    for view, probe in (('views01', 'probe02'), ('views02', 'probe03')):
        rows = maps[0]
        frame_rows = read(HERE/view/'frames.json')
        require(len(frame_rows) == len(rows), 'decoded row count')
        for f, expected in zip(frame_rows, rows):
            require(set(f) == set(expected) | {'decoded_sha256', 'luma_sha256'}, 'decoded row schema')
            require({k: f[k] for k in expected} == expected, 'decoded timestamp row')
            require(all(re.fullmatch('[0-9a-f]{64}', f[k]) for k in ('decoded_sha256', 'luma_sha256')), 'decoded hash format')
        rec = read(HERE/view/'receipt.json')
        for field, path in (('binary', '/opt/homebrew/bin/ffmpeg'), ('media', MEDIA), ('producer', BASE),
                            ('protocol', HERE/'PROTOCOL.md'), ('probe', HERE/probe/'probe.json'),
                            ('selection', HERE/probe/'selection.json')):
            require(rec[field] == pin(path), 'view receipt pin')
        require(rec['geometry'] == [704, 480] and rec['no_visual_review_implied'] is True, 'view scope/geometry')
        ex = read(HERE/view/'execution.json')
        require(ex == rec['execution'], 'decode execution repeat')
        require(ex['returncode'] == 0 and ex['stderr_bytes'] == 0 and ex['stderr_sha256'] == EMPTY, 'decode status')
        require(ex['raw_bytes'] == 962*704*480*3//2, 'decoded raw extent')
        expected_argv = ['/opt/homebrew/bin/ffmpeg', '-nostdin', '-nostats', '-hide_banner', '-v', 'warning',
                         '-copyts', '-noautorotate', '-i', str(MEDIA), '-map', '0:v:0', '-an', '-noautoscale',
                         '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough', '-enc_time_base:v', 'demux', '-f', 'rawvideo', '-']
        require(ex['argv'] == expected_argv, 'decode fixed command')
        diagnostics(view, ex)
        require([s['index'] for s in rec['selected']] == SELECTED, 'selected receipt indices')
        require(sorted(p.name for p in (HERE/view).glob('*.png')) == [f'frame-{i:04d}.png' for i in SELECTED], 'exact PNG roster')
        for item, i in zip(rec['selected'], SELECTED):
            path = HERE/view/f'frame-{i:04d}.png'
            geometry, pixels = gray_png(path.read_bytes())
            require(geometry == (704, 480) and len(pixels) == 704*480, 'PNG native extent')
            require(sha(pixels) == frame_rows[i]['luma_sha256'], 'PNG vs frame luma hash')
            expected = {**rows[i], 'png': path.name, **pin(path), 'luma_sha256': sha(pixels)}
            require(item == expected, 'complete selected PNG receipt')
            png_rows.append({'path': str(path.relative_to(HERE)), **pin(path), 'luma_sha256': sha(pixels)})
        all_frames.append(frame_rows)
    require(all_frames[0] == all_frames[1], 'all decoded hash rows repeat')
    for f in ('frames.json', 'execution.json', 'receipt.json', *[f'frame-{i:04d}.png' for i in SELECTED]):
        require((HERE/'views01'/f).read_bytes() == (HERE/'views02'/f).read_bytes(), 'view byte repeat '+f)
    failed = read(HERE/'probe01/execution.json')
    require(failed == read(HERE/'probe02/execution.json'), 'retained first probe execution record')
    require(sorted(p.name for p in (HERE/'probe01').iterdir()) == ['execution.json'], 'failed probe retained scope')
    null_counts = {k: sum(r[k] is None for r in maps[0]) for k in ('stored_pts', 'best_effort_timestamp')}
    require(null_counts['stored_pts'] > 0 and null_counts['best_effort_timestamp'] > 0, 'original timing criterion remains failed')
    require(before == {str(p): pin(p) for p in paths}, 'input/checker changed during verification')
    return {'schema_version': 1, 'status': 'passed_with_explicit_scope_limits',
            'checker': before[str(Path(__file__).resolve())], 'python': platform.python_version(),
            'runtime': str(Path(sys.executable).resolve()), 'zlib': zlib.ZLIB_RUNTIME_VERSION,
            'counts': {'probes': 2, 'frames_per_probe': 962, 'nullable_row_fields_checked_per_probe': 3848,
                       'decode_hash_rows_per_run': 962, 'decoded_hash_runs_compared': 2,
                       'selected_indices': SELECTED, 'PNG_files_checked': len(png_rows),
                       'required_pinned_paths_before_and_after': len(paths), 'missing_timestamps': null_counts},
            'original_complete_timing_test': 'failed; missing timestamps retained, not imputed',
            'diagnostics': {'probe02': 'returned 0; empty captured stderr', 'probe03': 'returned 0; empty captured stderr',
                            'views01': 'returned 0; empty captured stderr', 'views02': 'returned 0; empty captured stderr',
                            'probe01': 'execution metadata only; raw stdout and validator traceback not preserved'},
            'scope_limits': ['No producer imports, new video probe/decode, media viewing, network or source annotation.',
                             'All 962 decoded/luma hash records compared across runs; unselected pixels not independently rehashed.',
                             'Sixteen saved PNGs decoded independently from PNG chunks/filters; pixels compared to recorded luma hashes.',
                             'No independent video decoder, original camera authentication, exposure timing, human review, trajectory or cause finding.',
                             'Probe01 validation failure is documented by addendum; its original exception was not independently witnessed.'],
            'png_checks': png_rows, 'input_pins_unchanged': before}


class Controls(unittest.TestCase):
    def fixture(self):
        return {'streams': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p', 'time_base': '1/30'}],
                'frames': [{'width': 4, 'height': 2, 'pix_fmt': 'yuv420p', 'pts': i,
                            'best_effort_timestamp': i} for i in range(9)]}

    def test_zero_and_rational(self):
        rows, indices = row_map(self.fixture())
        self.assertEqual((rows[0]['stored_pts'], rows[0]['stored_pts_seconds_exact'], rows[1]['stored_pts_seconds_exact']), (0, '0', '1/30'))
        self.assertEqual(indices, [0, 1, 2, 3, 4, 5, 6, 8])

    def test_missing_unfilled(self):
        d = self.fixture(); del d['frames'][0]['pts']; d['frames'][-1].pop('best_effort_timestamp')
        rows, _ = row_map(d)
        self.assertIsNone(rows[0]['stored_pts']); self.assertIsNone(rows[0]['stored_pts_seconds_exact'])
        self.assertEqual(rows[0]['best_effort_timestamp'], 0)
        self.assertIsNone(rows[-1]['best_effort_timestamp']); self.assertEqual(rows[-1]['stored_pts'], 8)

    def test_disagreement(self):
        d = self.fixture(); d['frames'][3]['pts'] = 4
        with self.assertRaisesRegex(ValueError, 'agreement'): row_map(d)

    def test_known_order_across_gap(self):
        d = self.fixture(); d['frames'][3].pop('pts'); d['frames'][4]['pts'] = 1
        with self.assertRaisesRegex(ValueError, 'order'): row_map(d)

    def test_boolean_time(self):
        d = self.fixture(); d['frames'][0]['pts'] = False
        with self.assertRaisesRegex(ValueError, 'type'): row_map(d)

    def test_short(self):
        d = self.fixture(); d['frames'] = d['frames'][:7]
        with self.assertRaisesRegex(ValueError, 'count'): row_map(d)

    def test_geometry(self):
        d = self.fixture(); d['frames'][3]['width'] = 6
        with self.assertRaisesRegex(ValueError, 'geometry'): row_map(d)

    def test_time_base(self):
        d = self.fixture(); d['streams'][0]['time_base'] = '0'
        with self.assertRaisesRegex(ValueError, 'time base'): row_map(d)

    def png(self, filtered, w=3, h=5):
        def chunk(k, p):
            return struct.pack('>I', len(p))+k+p+struct.pack('>I', zlib.crc32(k+p)&0xffffffff)
        return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 0, 0, 0, 0))+chunk(b'IDAT', zlib.compress(filtered))+chunk(b'IEND', b'')

    def test_png_all_filters_literal_oracle(self):
        # Each literal row decodes to [10,20,30]; residuals manually specified.
        p = self.png(bytes([0,10,20,30, 1,10,10,10, 2,0,0,0, 3,5,5,5, 4,0,0,0]))
        self.assertEqual(gray_png(p), ((3,5), bytes([10,20,30]*5)))

    def test_png_modulo(self):
        self.assertEqual(gray_png(self.png(bytes([1,250,10,1]),3,1))[1], bytes([250,4,5]))

    def test_png_crc(self):
        p = bytearray(self.png(bytes([0,1]),1,1)); p[-1] ^= 1
        with self.assertRaisesRegex(ValueError, 'CRC'): gray_png(bytes(p))

    def test_png_bad_extent(self):
        with self.assertRaisesRegex(ValueError, 'extent'): gray_png(self.png(bytes([0,1]),2,1))

    def test_png_bad_filter(self):
        with self.assertRaisesRegex(ValueError, 'filter'): gray_png(self.png(bytes([5,1]),1,1))


if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(Controls)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(not result.wasSuccessful())
    require(not sys.argv[1:], 'usage: verify_independent.py [--self-test]')
    print(json.dumps(verify(), indent=2, sort_keys=True))
