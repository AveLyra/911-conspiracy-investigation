#!/usr/bin/env python3
"""Independent packet consistency checks; never decodes video or judges images.

--self-test uses synthetic arrays only. --runs RUN1 RUN2 prints a deterministic
receipt. Optional --roster JSON validates explicit classifications structurally.
No output files are written. Producer code is pinned but never imported.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
OLD = HERE.parent
HELPER = OLD/'verify_independent.py'
HELPER_SHA = '08fcdb4b90b8abab364fed0350012ab05af3d1b2c3564e1a41a255f79ffd989e'
PRODUCER_SHA = 'f261b0f516c90b3ae274b8d3d49e7453e7a2c80eb323f9cdcf3ca176067ae68a'
PROTOCOL_SHA = '230777a8aff939d2fcc76386fcdc18e26449305c8ba1da34874cdf387af9b970'
OLD_RECEIPT_SHA = '72eefba7acb6fbd2970d6aaef6ae8b274056170a805b467f1ad178a723c772c4'
ORDINALS = list(range(274, 412))
FIELDS = ('index', 'stored_pts', 'best_effort_timestamp', 'stored_pts_seconds_exact', 'best_effort_seconds_exact')
INPUT_NAMES = ['source/DistantViewWTC7.avi', 'probe02/selection.json', 'probe02/probe.json',
               'views01/frames.json', 'views01/receipt.json', 'source/receipt.json',
               'independent-verification.json', 'ordinal_screen.py', 'prepare.py',
               'PROTOCOL.md', 'ORDINAL-ADDENDUM.md', '../tilted-camera-source-join/prepare_media.py']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'bytes': path.stat().st_size, 'sha256': digest}


def read(path):
    return json.loads(Path(path).read_bytes())


def helpers():
    require(pin(HELPER)['sha256'] == HELPER_SHA, 'independent helper changed')
    spec = importlib.util.spec_from_file_location('pinned_independent_png_reader', HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rectangle(pixels, width, height, box):
    x0, y0, x1, y1 = box
    require(len(pixels) == width*height and all(type(v) is int for v in box), 'rectangle data/type')
    require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height, 'rectangle bounds')
    result = bytearray((x1-x0)*(y1-y0))
    for row in range(y1-y0):
        result[row*(x1-x0):(row+1)*(x1-x0)] = pixels[(y0+row)*width+x0:(y0+row)*width+x1]
    return bytes(result)


def check_crop(native, crop, box=(350, 90, 630, 380), width=704, height=480):
    require(crop == rectangle(native, width, height, box), 'crop pixels differ from source rectangle')


def stamp(canvas, size, box, pixels):
    x0, y0, x1, y1 = box
    require(len(pixels) == (x1-x0)*(y1-y0) and 0 <= x0 < x1 <= size[0]
            and 0 <= y0 < y1 <= size[1], 'stamp extent')
    for row in range(y1-y0):
        canvas[(y0+row)*size[0]+x0:(y0+row)*size[0]+x1] = pixels[row*(x1-x0):(row+1)*(x1-x0)]


def expected_cell(page, slot):
    n = 274+(page-1)*12+slot
    blank = n > 411
    column, row = slot % 4, slot // 4
    x, y = 12+column*292, 12+row*324
    box = [x, y+22, x+280, y+312]
    return {'slot': slot, 'row': row, 'column': column, 'index': None if blank else n,
            'blank': blank, 'label': 'BLANK - no frame' if blank else 'frame '+str(n),
            'label_origin': [x, y], 'page_box': box,
            'source_box': None if blank else [350, 90, 630, 380],
            'crop_path': None if blank else f'crops/crop-{n:04d}.png',
            'mapping': None if blank else {'source_to_crop_translation': [-350, -90],
                                          'crop_to_page_translation': [x, y+22], 'scale': [1, 1]}}


def check_cell(actual, page, slot, crops):
    expected = expected_cell(page, slot)
    n = expected['index']
    expected['crop_pixel_sha256'] = None if n is None else sha(crops[n])
    require(actual == expected, 'page placement/order/mapping differs')


def expected_page(page, crops):
    # Image-bearing regions use independent byte-row placement. Labels use the
    # documented Pillow default font, not independent font-rendering machinery.
    from PIL import Image, ImageDraw, ImageFont
    pixels = bytearray(b'\xff'*(1180*984))
    for slot in range(12):
        cell = expected_cell(page, slot)
        x, y = cell['label_origin']
        label = Image.new('L', (280, 22), 255)
        draw = ImageDraw.Draw(label)
        font = ImageFont.load_default(size=12)
        bbox = draw.textbbox((0, 0), cell['label'], font=font)
        require(0 <= bbox[0] <= bbox[2] <= 280 and 0 <= bbox[1] <= bbox[3] <= 22, 'label extent')
        draw.text((0, 0), cell['label'], fill=0, font=font)
        stamp(pixels, (1180, 984), [x, y, x+280, y+22], label.tobytes())
        if cell['index'] is not None:
            stamp(pixels, (1180, 984), cell['page_box'], crops[cell['index']])
    return bytes(pixels)


def check_times(actual, expected):
    require({key: actual[key] for key in FIELDS} == expected, 'nullable timestamp/index change')


def product_names():
    names = ['inputs-before.json', 'inputs-after.json', 'decoded-checks.json', 'frames.json',
             'pages.json', 'receipt.json', 'diagnostics/execution.json',
             'diagnostics/stdout-prefix.bin', 'diagnostics/stderr-prefix.bin']
    names += [f'native/frame-{i:04d}.png' for i in ORDINALS]
    names += [f'crops/crop-{i:04d}.png' for i in ORDINALS]
    names += [f'pages/page-{i:02d}.png' for i in range(1, 13)]
    return names


def verify_png(path, item, size, helper, cache):
    require(item == {'path': item['path'], **pin(path), 'pixel_sha256': item['pixel_sha256'],
                     'mode': 'L', 'size': list(size)}, 'PNG record schema/file pin')
    data = path.read_bytes()
    digest = sha(data)
    if digest not in cache:
        geometry, pixels = helper.gray_png(data)
        cache[digest] = (data, geometry, pixels)
    prior_data, geometry, pixels = cache[digest]
    require(data == prior_data and geometry == size and sha(pixels) == item['pixel_sha256'], 'PNG pixel/geometry pin')
    return pixels


def check_packet(run, expected_inputs, old_frames, time_rows, helper, cache):
    require(read(run/'inputs-before.json') == expected_inputs == read(run/'inputs-after.json'), 'complete required input closure')
    checks = read(run/'decoded-checks.json')
    prior_receipt = read(OLD/'views01/receipt.json')
    require(checks == {'frames_checked': 962, 'all_hashes_match': True,
                       'raw_bytes': 487618560, 'raw_sha256': prior_receipt['execution']['raw_sha256'],
                       'frames': old_frames}, 'all decoded hash/timestamp records')
    frames = read(run/'frames.json')
    require(len(frames) == 138, 'native/crop frame count')
    crops = {}
    for item, n in zip(frames, ORDINALS):
        require(set(item) == set(FIELDS) | {'decoded_sha256', 'luma_sha256', 'source_box', 'native', 'crop'}, 'frame record schema')
        check_times(item, time_rows[n])
        require(item['source_box'] == [350, 90, 630, 380] and
                item['decoded_sha256'] == old_frames[n]['decoded_sha256'] and
                item['luma_sha256'] == old_frames[n]['luma_sha256'], 'source frame identity')
        native_name, crop_name = f'native/frame-{n:04d}.png', f'crops/crop-{n:04d}.png'
        require(item['native']['path'] == native_name and item['crop']['path'] == crop_name, 'frame paths/order')
        native = verify_png(run/native_name, item['native'], (704, 480), helper, cache)
        crop = verify_png(run/crop_name, item['crop'], (280, 290), helper, cache)
        require(sha(native) == old_frames[n]['luma_sha256'], 'native pixels vs previous decoded hash')
        check_crop(native, crop)
        crops[n] = crop
    pages = read(run/'pages.json')
    require(len(pages) == 12, 'page count')
    for page, number in zip(pages, range(1, 13)):
        require(set(page) == {'page', 'size', 'cells', 'png'} and page['page'] == number
                and page['size'] == [1180, 984] and len(page['cells']) == 12, 'page roster')
        for slot, cell in enumerate(page['cells']):
            check_cell(cell, number, slot, crops)
        name = f'pages/page-{number:02d}.png'
        require(page['png']['path'] == name, 'page file order')
        pixels = verify_png(run/name, page['png'], (1180, 984), helper, cache)
        require(pixels == expected_page(number, crops), 'entire page pixels: crops, labels, blank cells and gutters')
    ex = read(run/'diagnostics/execution.json')
    require(ex['argv'] == prior_receipt['execution']['argv'] and ex['status'] == 'returned'
            and ex['returncode'] == 0 and ex['capture_complete'] is True and ex['error'] is None,
            'decoder command/status')
    require(ex['timeout_seconds'] == 60 and 0 <= ex['elapsed_seconds'] <= 61
            and ex['stdout_limit'] == 487618560 and ex['diagnostic_prefix_limit'] == 1048576, 'capture bounds')
    for field in ('stdout', 'stderr'):
        prefix = (run/f'diagnostics/{field}-prefix.bin').read_bytes()
        rec = ex[field]
        total = 487618560 if field == 'stdout' else 0
        digest = prior_receipt['execution']['raw_sha256'] if field == 'stdout' else sha(b'')
        require(rec == {'captured_bytes': total, 'captured_sha256': digest,
                        'saved_prefix': field+'-prefix.bin', 'saved_bytes': len(prefix),
                        'saved_sha256': sha(prefix), 'saved_prefix_truncated': field == 'stdout'}, 'captured diagnostic pin')
        require(len(prefix) == min(total, 1048576), 'diagnostic prefix length')
    rec = read(run/'receipt.json')
    require(rec['producer'] == pin(HERE/'derive.py') and rec['status'] == 'derived_only_not_visually_reviewed', 'receipt producer/status')
    for key, value in {'inputs_unchanged': True, 'decoded_frames_checked': 962,
                       'selected_interval_inclusive': [274, 411], 'native_frames': 138, 'crops': 138,
                       'pages': 12, 'blank_cells': 6, 'source_box': [350, 90, 630, 380],
                       'page_size': [1180, 984], 'context_ordinals': [274, 342, 411],
                       'timestamps': 'nullable fields copied exactly; ordinal only',
                       'no_classifications_generated': True, 'no_source_acceptance_implied': True}.items():
        require(rec[key] == value, 'receipt field '+key)
    for key, name in [('execution', 'diagnostics/execution.json'), ('decoded_checks', 'decoded-checks.json'),
                      ('frames', 'frames.json'), ('page_mapping', 'pages.json')]:
        require(rec[key] == pin(run/name), 'receipt artifact pin')
    return rec


def check_roster(document):
    frames, links = document['frames'], document['links']
    require(type(frames) is list and type(links) is list and len(frames) == 138 and len(links) == 137, 'roster count/gap')
    for row, n in zip(frames, ORDINALS):
        require(set(row) == {'ordinal', 'status', 'reason'} and type(row['ordinal']) is int
                and row['ordinal'] == n, 'frame roster order/schema')
        require(row['status'] in ('V', 'A', 'O', 'X') and isinstance(row['reason'], str)
                and row['reason'].strip(), 'frame judgment missing/invalid')
    supported = []
    for i, row in enumerate(links):
        n = 274+i
        require(set(row) == {'from', 'to', 'status', 'reason'} and type(row['from']) is int
                and type(row['to']) is int and (row['from'], row['to']) == (n, n+1), 'link roster order/schema')
        require(row['status'] in ('supported', 'uncertain', 'broken') and isinstance(row['reason'], str)
                and row['reason'].strip(), 'link judgment missing/invalid')
        if row['status'] == 'supported':
            require(frames[i]['status'] == frames[i+1]['status'] == 'V', 'supported link beside non-V')
            supported.append(n)
    groups = []
    for n in supported:
        if groups and groups[-1][1] == n:
            groups[-1][1] = n+1
        else:
            groups.append([n, n+1])
    return {'frames': 138, 'links': 137, 'supported_runs_inclusive': groups,
            'uninterrupted_observational_candidate': len(supported) == 137,
            'semantic_or_human_acceptance_implied': False,
            'O_reason_distinction': 'semantic reviewer obligation; not machine certified'}


def verify(run_names, roster_names):
    helper = helpers()
    require(pin(HERE/'PROTOCOL.md')['sha256'] == PROTOCOL_SHA and
            pin(HERE/'derive.py')['sha256'] == PRODUCER_SHA, 'frozen method pin')
    old_receipt = OLD/'independent-verification.json'
    require(pin(old_receipt)['sha256'] == OLD_RECEIPT_SHA, 'old receipt pin')
    closure = read(old_receipt)['input_pins_unchanged']
    require(len(closure) == 59, 'old dependency closure')
    for path, expected in closure.items():
        require(pin(path) == expected, 'inherited dependency '+path)
    expected_inputs = {str((OLD/name).resolve()): pin(OLD/name) for name in INPUT_NAMES}
    expected_inputs.update({str(HERE/'PROTOCOL.md'): pin(HERE/'PROTOCOL.md'),
                            str(HERE/'derive.py'): pin(HERE/'derive.py'),
                            '/opt/homebrew/bin/ffmpeg': pin('/opt/homebrew/bin/ffmpeg')})
    require(len(expected_inputs) == 15, 'direct dependency roster')
    require(len(run_names) == 2 and len(set(run_names)) == 2, 'two distinct runs required')
    runs = []
    for name in run_names:
        require(re.fullmatch('[a-z][a-z0-9_-]*', name), 'run path')
        run = HERE/name
        require(run.is_dir() and not run.is_symlink(), 'run directory')
        require(sorted(str(p.relative_to(run)) for p in run.rglob('*') if p.is_file()) == sorted(product_names()), 'exact product roster')
        require(not any(p.is_symlink() for p in run.rglob('*')), 'symlink output')
        runs.append(run)
    roster_paths = []
    for name in roster_names:
        p = Path(name).resolve()
        require(p.parent == HERE and p.suffix == '.json' and not Path(name).is_symlink(), 'roster must be local JSON')
        roster_paths.append(p)
    paths = set(closure) | set(expected_inputs) | {str(old_receipt), str(Path(__file__).resolve())}
    paths |= {str(run/name) for run in runs for name in product_names()} | {str(p) for p in roster_paths}
    before = {name: pin(name) for name in sorted(paths)}
    # Repeat-byte check precedes cached PNG decoding. Equal bytes permit one
    # lossless decode per unique PNG while checking both complete file sets.
    variable = {'receipt.json', 'diagnostics/execution.json'}
    for name in product_names():
        if name not in variable:
            require((runs[0]/name).read_bytes() == (runs[1]/name).read_bytes(), 'repeat bytes '+name)
    old_frames = read(OLD/'views01/frames.json')
    raw = read(OLD/'probe02-diagnostics/probe-stdout.json')
    time_rows, _ = helper.row_map(raw)
    require(len(time_rows) == 962, 'source row count')
    for row, frame in zip(time_rows, old_frames):
        check_times(frame, row)
    cache = {}
    receipts = [check_packet(run, expected_inputs, old_frames, time_rows, helper, cache) for run in runs]
    require({k:v for k,v in receipts[0].items() if k != 'execution'} ==
            {k:v for k,v in receipts[1].items() if k != 'execution'}, 'repeat receipt differences')
    roster_results = {str(p): check_roster(read(p)) for p in roster_paths}
    require(before == {name: pin(name) for name in sorted(paths)}, 'inputs or checker changed during verification')
    from PIL import __version__ as pillow_version
    return {'status': 'passed_with_explicit_scope_limits', 'checker': pin(__file__),
            'python': platform.python_version(), 'runtime': str(Path(sys.executable).resolve()),
            'pillow_label_renderer': pillow_version, 'runs': run_names,
            'counts': {'native_PNG_files': 276, 'crop_PNG_files': 276, 'page_PNG_files': 24,
                       'losslessly_decoded_unique_PNGs': len(cache), 'frames_per_run': 138,
                       'adjacent_link_slots': 137, 'cells_per_run': 144, 'blank_cells_per_run': 6,
                       'source_timestamp_rows': 962, 'saved_decoded_hash_rows_per_run': 962,
                       'required_pins_before_and_after': len(before)},
            'rosters': roster_results, 'input_pins_unchanged': before,
            'limits': ['No producer imports, video decode, image viewing, classification, clock recovery or human acceptance.',
                       'All selected native/crop/page pixels checked; unselected decoded pixels remain hash-record checks.',
                       'PNG parsing/filter reversal uses pinned independent checker; labels share Pillow default-font renderer.',
                       'Rosters, when supplied, receive structural checks only; judgment/reason meaning and actual viewing are not certified.']}


class Controls(unittest.TestCase):
    def roster(self):
        return {'frames': [{'ordinal': n, 'status': 'V', 'reason': 'synthetic'} for n in ORDINALS],
                'links': [{'from': n, 'to': n+1, 'status': 'supported', 'reason': 'synthetic'} for n in ORDINALS[:-1]]}

    def test_crop_literal_oracle(self):
        source = bytes(range(20))
        self.assertEqual(rectangle(source, 5, 4, [1, 1, 4, 3]), bytes([6,7,8,11,12,13]))
        check_crop(source, bytes([6,7,8,11,12,13]), (1,1,4,3),5,4)

    def test_changed_crop_rejected(self):
        with self.assertRaisesRegex(ValueError, 'crop pixels'):
            check_crop(bytes(range(20)),bytes([6,7,9,11,12,13]),(1,1,4,3),5,4)

    def test_shifted_crop_rejected(self):
        with self.assertRaisesRegex(ValueError, 'crop pixels'):
            check_crop(bytes(range(20)),bytes([5,6,7,10,11,12]),(1,1,4,3),5,4)

    def test_page_mapping_mutation(self):
        crops = {274: b'x'}
        cell = expected_cell(1,0); cell['crop_pixel_sha256'] = sha(b'x')
        check_cell(cell,1,0,crops)
        cell['page_box'][0] += 1
        with self.assertRaisesRegex(ValueError, 'placement'): check_cell(cell,1,0,crops)

    def test_page_roster_and_blanks(self):
        cells = [expected_cell(p,s) for p in range(1,13) for s in range(12)]
        self.assertEqual([c['index'] for c in cells if not c['blank']], ORDINALS)
        self.assertEqual(sum(c['blank'] for c in cells),6)
        self.assertEqual(expected_cell(12,5)['index'],411)
        self.assertEqual(expected_cell(1,0)['page_box'],[12,34,292,324])
        self.assertEqual(expected_cell(12,11)['page_box'],[888,682,1168,972])

    def test_page_pixels_and_blank_oracle(self):
        crops = {n: bytes([n%251])*(280*290) for n in ORDINALS}
        pixels = expected_page(12,crops)
        self.assertEqual(rectangle(pixels,1180,984,[304,358,584,648]),bytes([411%251])*(280*290))
        self.assertEqual(rectangle(pixels,1180,984,[596,358,876,648]),b'\xff'*(280*290))
        self.assertEqual(rectangle(pixels,1180,984,[0,0,12,984]),b'\xff'*(12*984))

    def test_null_timestamp_mutation(self):
        row = {'index':0,'stored_pts':None,'best_effort_timestamp':0,
               'stored_pts_seconds_exact':None,'best_effort_seconds_exact':'0'}
        check_times(row,row)
        bad = dict(row,stored_pts=0)
        with self.assertRaisesRegex(ValueError,'timestamp'): check_times(bad,row)

    def test_full_roster(self):
        result = check_roster(self.roster())
        self.assertEqual(result['supported_runs_inclusive'],[[274,411]])
        self.assertTrue(result['uninterrupted_observational_candidate'])

    def test_roster_gap_duplicate(self):
        for kind in ('frames','links'):
            d = self.roster(); d[kind].pop(3)
            with self.assertRaisesRegex(ValueError,'count/gap'): check_roster(d)
            d = self.roster(); d[kind][4] = copy.deepcopy(d[kind][3])
            with self.assertRaisesRegex(ValueError,'order'): check_roster(d)

    def test_non_v_supported_rejected(self):
        for status in ('A','O','X'):
            d = self.roster(); d['frames'][5]['status'] = status
            with self.assertRaisesRegex(ValueError,'non-V'): check_roster(d)

    def test_no_link_inference_and_no_bridge(self):
        d = self.roster(); d['links'][5]['status'] = 'uncertain'
        r = check_roster(d)
        self.assertEqual(r['supported_runs_inclusive'],[[274,279],[280,411]])
        self.assertFalse(r['uninterrupted_observational_candidate'])

    def test_empty_reason_and_boolean_identity(self):
        d = self.roster(); d['frames'][0]['reason'] = ' '
        with self.assertRaises(ValueError): check_roster(d)
        d = self.roster(); d['links'][0]['from'] = True
        with self.assertRaises(ValueError): check_roster(d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--runs',nargs=2)
    parser.add_argument('--roster',action='append',default=[])
    args = parser.parse_args()
    if args.self_test:
        require(args.runs is None and not args.roster,'synthetic/historical modes separated')
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    require(args.runs is not None,'explicit --runs required')
    print(json.dumps(verify(args.runs,args.roster),indent=2,sort_keys=True))
