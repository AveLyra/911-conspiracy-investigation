"""Post-producer numeric verification; no decoder, producer imports or PNG writes."""
import argparse
import ast
import copy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys

from PIL import Image

BASE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
RUNS = ('dense00', 'dense11', 'dense12', 'dense13')
INTERVALS = ((2502, 2510), (2510, 2518), (2518, 2526), (2526, 2534))
TARGETS = {
    '148': ('A-370a6ef2789a', '8afb62b6dce6e4618075c66576ef9fdf88295d636427893dc36064afb37a1253'),
    '149': ('A-e43e4088a4a2', '6129afd898a56282579832595715ef2e1093b55d299b693810ac05c72af53469'),
}
PINS = {
    'summarize_dense.py': 'c53783179e50851616a35d12c4f5f05403ea2cb54112df961c439ecce29297d9',
    'check_regions.py': '6990064d77887e245b6843c0580679c5e5c9b5e5a262e1f5e8287fb7411a196b',
    'CANDIDATE-REVIEW-01.md': '860b87a847365de05ed3dc0cedccd788f55a9230da9bdc7a10e110c1bb881784',
    'independent-target-review.md': 'ceee2c6607f33a16225fb8c01aa876f076a382f3ce54d7b0776d266ca7ab6b9f',
    'DENSE-CONTINUATION-02.md': 'f532f8376db02f01f5943ea7f1df99719a016a57eecaee2185db079b320f5156',
    'match_screen.py': '06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8',
}
RUNNER_PINS = ('8c5c92932c43183d0861e16282f95e7be360a36bd9ee016c639e638ebed82bb1',
               'b76788bf65e74fa464c060ee0a5831aba27eb864f6139f2c6c2f5a604bf2ce59')
TOLERANCE = 1e-12


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            digest.update(block)
    return digest.hexdigest()


def require(condition, label):
    if not condition:
        raise ValueError(label)


def read_pinned(path, pin, byte_count=None):
    require(not path.is_symlink(), 'symlink input')
    require(sha(path) == pin, 'input hash mismatch')
    if byte_count is not None:
        require(path.stat().st_size == byte_count, 'input byte mismatch')
    return json.loads(path.read_text())


def bands(rows):
    """Keep every disconnected run of eligible global frame positions."""
    ordered = sorted(rows, key=lambda row: row['global_index'])
    answer = []
    previous = None
    for row in ordered:
        require(previous is None or row['global_index'] > previous, 'duplicate band frame')
        if previous is None or row['global_index'] - previous != 1:
            answer.append({'first_pts': row['source_pts'], 'last_pts': row['source_pts'], 'count': 1})
        else:
            answer[-1]['last_pts'] = row['source_pts']
            answer[-1]['count'] += 1
        previous = row['global_index']
    return answer


def rankings(all_rows):
    output = {}
    for target in TARGETS:
        output[target] = {}
        for metric in ('static_score', 'dynamic_score'):
            scored = []
            for row in all_rows:
                if row['target'] != target or not row['geometry_candidates']:
                    continue
                score = row['geometry_candidates'][0][metric]
                if score is not None:
                    require(math.isfinite(score), 'nonfinite eligible score')
                    scored.append(row)
            scored.sort(key=lambda row: (-row['geometry_candidates'][0][metric], row['source_pts']))
            best = scored[0]['geometry_candidates'][0][metric] if scored else None
            output[target][metric] = {'eligible_count': len(scored), 'top_four': scored[:4],
                'best_score': best, 'descriptive_score_bands': {
                    str(delta): bands([row for row in scored
                        if row['geometry_candidates'][0][metric] >= best-delta]) if scored else []
                    for delta in (0.005, 0.01, 0.02)}}
    return output


def masks_for(regions, exclusions, width=180, height=120):
    """Exact target-coordinate pixel centers; rectangles are attributed inputs."""
    expanded = [(x0-4, y0-4, x1+4, y1+4) for x0, y0, x1, y1 in exclusions]
    def inside(x, y, box):
        return box[0] <= x < box[2] and box[1] <= y < box[3]
    answer = {name: [] for name in regions}
    for j in range(height):
        y = Fraction((2*j+1)*478, 2*height)
        for i in range(width):
            x = Fraction((2*i+1)*720, 2*width)
            admissible = inside(x, y, (3, 3, 717, 475)) and not any(inside(x, y, box) for box in expanded)
            for name, box in regions.items():
                answer[name].append(admissible and inside(x, y, box))
    return answer


def direct_region(a, b, mask, valid):
    require(len(a) == len(b) == len(mask) == len(valid), 'regional dimensions')
    require(all(x in (0, 1, False, True) for x in mask+valid), 'nonbinary masks')
    selected = sum(mask)
    pairs = [(float(x), float(y)) for x, y, m, v in zip(a, b, mask, valid) if m and v]
    require(all(math.isfinite(x) and math.isfinite(y) for x, y in pairs), 'nonfinite region')
    count = len(pairs)
    coverage = count/selected if selected else 0
    rho = None
    if coverage >= .85 and count >= 32:
        am = math.fsum(p[0] for p in pairs)/count
        bm = math.fsum(p[1] for p in pairs)/count
        aa = math.fsum((x-am)*(x-am) for x, y in pairs)
        bb = math.fsum((y-bm)*(y-bm) for x, y in pairs)
        if aa/count > 1e-8 and bb/count > 1e-8:
            ab = math.fsum((x-am)*(y-bm) for x, y in pairs)
            rho = ab/math.sqrt(aa*bb)
    return {'selected_pixels': int(selected), 'valid_pixels': count,
            'coverage': coverage, 'grayscale_pearson': rho}


def fixed_view(image, transform):
    """Rebuild the declared Pillow raster, sampling directly without a canvas."""
    sw, sh = round(180*transform['requested_scale']), round(120*transform['requested_scale'])
    x0, y0 = 25+(180-sw)//2, 25+(120-sh)//2
    expect = {'raster_width': sw, 'raster_height': sh, 'scale_x': sw/180,
              'scale_y': sh/120, 'canvas_x': x0, 'canvas_y': y0}
    require(all(transform[k] == v for k, v in expect.items()), 'fixed transform fields')
    left, top = transform['left'], transform['top']
    require(isinstance(left, int) and isinstance(top, int) and 0 <= left <= 50 and 0 <= top <= 50,
            'fixed transform translation')
    require(transform['dx'] == left-25 and transform['dy'] == top-25, 'translation labels')
    small = image.convert('L').resize((180, 120), Image.Resampling.BILINEAR)
    scaled = small.resize((sw, sh), Image.Resampling.BILINEAR)
    data = list(scaled.getdata())
    pixels, valid = [], []
    for j in range(120):
        for i in range(180):
            x, y = left+i-x0, top+j-y0
            yes = 0 <= x < sw and 0 <= y < sh
            valid.append(yes)
            pixels.append(data[y*sw+x] if yes else 0)
    return pixels, valid


def controls():
    checks = []
    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed)})
    def rejected(call):
        try:
            call()
        except ValueError:
            return True
        return False
    rr = [{'global_index': i, 'source_pts': 1000+i*33} for i in (0, 1, 4, 8, 9)]
    check('all_disconnected_bands', bands(rr[::-1]) == [
        {'first_pts': 1000, 'last_pts': 1033, 'count': 2},
        {'first_pts': 1132, 'last_pts': 1132, 'count': 1},
        {'first_pts': 1264, 'last_pts': 1297, 'count': 2}])
    check('empty_band', bands([]) == [])
    check('duplicate_band_rejected', rejected(lambda: bands([rr[0], rr[0]])))
    empty = rankings([])
    check('all_empty_targets_metrics', all(v['eligible_count'] == 0 and v['best_score'] is None
          and v['top_four'] == [] and all(b == [] for b in v['descriptive_score_bands'].values())
          for target in empty.values() for v in target.values()))
    candidates = [{'target': '148', 'source_pts': 1000+i, 'global_index': i,
        'geometry_candidates': [] if i == 5 else [{'static_score': .9 if i < 5 else .7,
                                                  'dynamic_score': None if i == 0 else .8}]}
                  for i in range(7)]
    result = rankings(candidates[::-1])
    check('top_four_ties_by_pts', [r['source_pts'] for r in result['148']['static_score']['top_four']]
          == [1000, 1001, 1002, 1003])
    check('null_and_empty_dynamic_candidates', result['148']['dynamic_score']['eligible_count'] == 5)
    bad = copy.deepcopy(candidates); bad[0]['geometry_candidates'][0]['static_score'] = float('nan')
    check('nonfinite_score_rejected', rejected(lambda: rankings(bad)))
    a = list(range(100)); ones = [True]*100
    check('positive_linear_rho', abs(direct_region(a, [3*x+8 for x in a], ones, ones)['grayscale_pearson']-1) < 1e-14)
    check('negative_linear_rho', abs(direct_region(a, [-x for x in a], ones, ones)['grayscale_pearson']+1) < 1e-14)
    check('flat_rejected', direct_region(a, [4]*100, ones, ones)['grayscale_pearson'] is None)
    check('empty_mask', direct_region(a, a, [False]*100, ones) ==
          {'selected_pixels': 0, 'valid_pixels': 0, 'coverage': 0, 'grayscale_pearson': None})
    check('under_32', direct_region(a, a, [i < 31 for i in a], ones)['grayscale_pearson'] is None)
    check('exactly_32', direct_region(a, a, [i < 32 for i in a], ones)['grayscale_pearson'] == 1)
    check('coverage_below_85', direct_region(a, a, ones, [i < 84 for i in a])['grayscale_pearson'] is None)
    check('coverage_equal_85', direct_region(a, a, ones, [i < 85 for i in a])['grayscale_pearson'] == 1)
    varied = direct_region(a, a[:-1]+[100000], ones, [i != 99 for i in a])
    check('overlap_only_centering', abs(varied['grayscale_pearson']-1) < 1e-14)
    check('nonbinary_mask_rejected', rejected(lambda: direct_region(a, a, [2]*100, ones)))
    mask = masks_for({'all': (0, 0, 720, 478)}, [])['all']
    check('outer_three_pixel_mask_count', sum(mask) == 178*118)
    edge = masks_for({'edge': (2, 0, 6, 478)}, [])['edge']
    check('half_open_native_center', not any(edge))
    excluded = masks_for({'all': (0, 0, 720, 478)}, [(100, 100, 104, 104)])['all']
    check('expanded_exclusion_removes_pixels', sum(excluded) < sum(mask))
    image = Image.new('L', (180, 120))
    original_pixels = [i % 256 for i in range(180*120)]
    image.putdata(original_pixels)
    transform = {'requested_scale': 1., 'raster_width': 180, 'raster_height': 120,
                 'scale_x': 1., 'scale_y': 1., 'canvas_x': 25, 'canvas_y': 25,
                 'left': 25, 'top': 25, 'dx': 0, 'dy': 0}
    pixels, good = fixed_view(image, transform)
    check('fixed_view_identity_pixels', pixels == original_pixels and all(good))
    pixels, good = fixed_view(image, dict(transform, left=0, top=0, dx=-25, dy=-25))
    check('fixed_view_padding_unobserved', sum(good) == 155*95 and not good[0]
          and pixels[25*180+25] == original_pixels[0])
    check('changed_transform_fields_rejected', rejected(lambda: fixed_view(image, dict(transform, raster_width=181))))
    rng = random.Random(9132026); errors = []
    for _ in range(40):
        x = [rng.randrange(256) for i in range(70)]
        y = [rng.randrange(256) for i in range(70)]
        keep = [i < 65 for i in range(70)]
        got = direct_region(x, y, [True]*70, keep)['grayscale_pearson']
        n = 65; sx = sum(x[:n]); sy = sum(y[:n])
        vx = Fraction(sum(v*v for v in x[:n]))-Fraction(sx*sx, n)
        vy = Fraction(sum(v*v for v in y[:n]))-Fraction(sy*sy, n)
        cov = Fraction(sum(p*q for p, q in zip(x[:n], y[:n])))-Fraction(sx*sy, n)
        exact = float(cov)/math.sqrt(float(vx*vy))
        errors.append(abs(got-exact))
    check('40_fraction_raw_moment_oracles', max(errors) < 1e-14)
    return {'status': 'passed' if all(c['passed'] for c in checks) else 'failed',
            'checks': checks, 'check_count': len(checks), 'max_fraction_oracle_rho_error': max(errors)}


def verify(summary_path, summary_pin, region_path, region_pin):
    for name, pin in PINS.items():
        require(sha(BASE/name) == pin, 'reviewed code/declaration changed')
    summary = read_pinned(summary_path, summary_pin)
    regional = read_pinned(region_path, region_pin)
    require(summary['status'] == regional['status'] == 'completed', 'result status')
    require(summary['script_sha256'] == PINS['summarize_dense.py'], 'summary producer identity')
    require(regional['script_sha256'] == PINS['check_regions.py'] and regional['summary_sha256'] == summary_pin,
            'regional producer/summary identity')
    require(regional['core_sha256'] == PINS['match_screen.py'] and
            regional['declaration_sha256'] == PINS['CANDIDATE-REVIEW-01.md'], 'regional method identity')
    require(set(summary['chunk_receipt_pins']) == set(RUNS), 'accepted run set')
    all_rows, all_pts, receipts, input_pins, run_counts = [], [], {}, {}, {}
    reference = None
    for index, (run, interval) in enumerate(zip(RUNS, INTERVALS)):
        folder = BASE/run; receipt_pin = summary['chunk_receipt_pins'][run]
        receipt = read_pinned(folder/'receipt.json', receipt_pin); receipts[run] = receipt
        input_pins[f'{run}/receipt.json'] = receipt_pin
        require(receipt['status'] == 'completed' and receipt['compare_to'] is None and
                receipt['interval'] == list(interval), 'accepted production identity')
        require(receipt['script_sha256'] == RUNNER_PINS[bool(index)], 'runner identity')
        identity = {k: receipt[k] for k in ('source_before', 'source_after', 'core_sha256', 'tools', 'numpy', 'pillow', 'python')}
        require(identity['source_before'] == identity['source_after'], 'source unchanged')
        require(identity['source_before'] == {'bytes': 696711067,
            'sha256': '0f438006c27e3059e7a5a480d4a7ee5382c5a136945c2a0120e583e3456f324d'}, 'admitted source receipt pin')
        if reference is None:
            reference = identity
        require(identity == reference and identity['core_sha256'] == PINS['match_screen.py'], 'shared input/runtime identity')
        require(receipt['pillow'] == Image.__version__, 'Pillow runtime identity')
        data = {}
        for name in ('frames.json', 'results.json', 'frame-probe.json'):
            pin = receipt['outputs'][name]
            data[name] = read_pinned(folder/name, pin['sha256'], pin['bytes'])
            input_pins[f'{run}/{name}'] = pin['sha256']
        frames, rows = data['frames.json'], data['results.json']; n = len(frames)
        require(1 <= n <= 275 and n == receipt['frame_count'] and len(rows) == 2*n, 'chunk counts')
        require([f['frame_index'] for f in frames] == list(range(n)), 'frame indexing')
        pts = [f['source_pts'] for f in frames]
        require(pts == sorted(set(pts)) and all(interval[0]*1000 <= p < interval[1]*1000 for p in pts), 'chunk PTS interval/order')
        require(all(f['source_time_base'] == '1/1000' for f in frames), 'frame time base')
        probe = [r for r in data['frame-probe.json']['frames'] if interval[0]*1000 <= r['pts'] < interval[1]*1000]
        require([r['pts'] for r in probe] == pts and all(r['pts'] == r['best_effort_timestamp'] and
                (r['width'], r['height']) == (1620, 1080) for r in probe), 'independent stored probe join')
        require(receipt['frame_probe_matches'] == n and receipt['anchor_pixel_matches'] == 8 and
                receipt['first_pts'] == pts[0] and receipt['last_pts'] == pts[-1], 'receipt coverage fields')
        require({(r['frame_index'], r['target']) for r in rows} == {(i, t) for i in range(n) for t in TARGETS}, 'complete target-frame relation')
        native_ids = {r['frame_index'] for r in receipt['native_images']}
        for row in rows:
            frame = frames[row['frame_index']]
            require(row['source_pts'] == frame['source_pts'] and row['source_time_base'] == '1/1000', 'result-frame PTS join')
            copied = dict(row, run=run, global_index=len(all_pts)+row['frame_index'])
            if row['frame_index'] in native_ids:
                copied['native_png'] = str(folder/f"native-{row['frame_index']:04d}.png")
            all_rows.append(copied)
        all_pts.extend(pts); run_counts[run] = n
    require(len(all_pts) <= 1100 and all_pts == sorted(set(all_pts)), 'global PTS coverage')
    require((summary['frame_count'], summary['comparison_count'], summary['first_pts'], summary['last_pts'], summary['source_time_base']) ==
            (len(all_pts), len(all_rows), all_pts[0], all_pts[-1], '1/1000'), 'summary counts/PTS')
    ranked = rankings(all_rows)
    require(ranked == summary['results'], 'complete ranking/band comparison')
    # Literal source data only: definitions attributed to independent-target-review;
    # no producer functions or scoring code are imported or executed.
    definitions = {}
    for node in ast.parse((BASE/'check_regions.py').read_text()).body:
        if isinstance(node, ast.Assign):
            for name in node.targets:
                if isinstance(name, ast.Name) and name.id in ('REGIONS', 'EXCLUSIONS'):
                    definitions[name.id] = ast.literal_eval(node.value)
    require(json.loads(json.dumps(definitions['REGIONS'])) == regional['regions'] and
            json.loads(json.dumps(definitions['EXCLUSIONS'])) == regional['exclusions'] and
            regional['exclusion_expansion_pixels'] == 4, 'region definition identity')
    computed, native_inputs = [], {}
    for key, (asset, pin) in TARGETS.items():
        target_path = MAIN/'fire-annotation/assets/run-01/images'/f'{asset}.jpg'
        require(sha(target_path) == pin, 'target bytes')
        input_pins[str(target_path)] = pin
        with Image.open(target_path) as image:
            require(image.size == (720, 478), 'target raster size')
            target = list(image.convert('L').resize((180, 120), Image.Resampling.BILINEAR).getdata())
        masks = masks_for(definitions['REGIONS'][key], definitions['EXCLUSIONS'][key])
        candidates = {row['source_pts']: row for item in ranked[key].values() for row in item['top_four']}
        for pts, row in sorted(candidates.items()):
            path = BASE/row['run']/f"native-{row['frame_index']:04d}.png"
            require(str(path) == row['native_png'], 'selected native path')
            native_pin = receipts[row['run']]['outputs'][path.name]
            require(not path.is_symlink() and sha(path) == native_pin['sha256'] and
                    path.stat().st_size == native_pin['bytes'], 'selected native pin')
            native_inputs[str(path)] = native_pin
            with Image.open(path) as image:
                require(image.size == (1620, 1080), 'source raster size')
                view, valid = fixed_view(image, row['geometry_candidates'][0])
            metrics = {name: direct_region(view, target, mask, valid) for name, mask in masks.items()}
            computed.append({'target': key, 'source_pts': pts, 'run': row['run'], 'frame_index': row['frame_index'],
                'fixed_foreground_transform': row['geometry_candidates'][0], 'regions': metrics})
    require(native_inputs == regional['inputs'] and len(computed) == len(regional['results']), 'regional candidate/input coverage')
    max_rho = 0.; max_coverage = 0.; nulls = 0; metric_count = 0
    for own, other in zip(computed, regional['results']):
        require({k: v for k, v in own.items() if k != 'regions'} == {k: v for k, v in other.items() if k != 'regions'}, 'regional candidate/transform identity')
        require(set(own['regions']) == set(other['regions']), 'all regions compared')
        for name, metrics in own['regions'].items():
            expected = other['regions'][name]; metric_count += 1
            require(metrics['selected_pixels'] == expected['selected_pixels'] and metrics['valid_pixels'] == expected['valid_pixels'], 'regional pixel counts')
            delta = abs(metrics['coverage']-expected['coverage']); max_coverage = max(max_coverage, delta)
            require(delta <= TOLERANCE, 'regional coverage discrepancy')
            x, y = metrics['grayscale_pearson'], expected['grayscale_pearson']
            require((x is None) == (y is None), 'regional nullness discrepancy')
            if x is None:
                nulls += 1
            else:
                require(math.isfinite(y), 'producer nonfinite rho')
                delta = abs(x-y); max_rho = max(max_rho, delta)
                require(delta <= TOLERANCE, 'regional rho discrepancy')
    return {'status': 'passed', 'summary_sha256': summary_pin, 'regions_sha256': region_pin,
        'run_counts': run_counts, 'frame_count': len(all_pts), 'comparison_count': len(all_rows),
        'input_pins': input_pins, 'native_inputs': native_inputs, 'declaration_code_pins': PINS,
        'complete_rankings_and_bands': ranked, 'regional_results': computed,
        'region_count': metric_count, 'region_null_count': nulls, 'candidate_target_pairs': len(computed),
        'max_absolute_rho_error': max_rho, 'max_absolute_coverage_error': max_coverage,
        'absolute_tolerance': TOLERANCE,
        'limits': 'Post-producer verification of saved scores and fixed-transform pixels; shared Pillow rasterization, attributed source regions; no decoder, independent transform fit, FFT-surface reproduction, historical clock, physical or causal validation.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('controls', 'verify'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--summary-sha256')
    parser.add_argument('--regions-sha256')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('create-only output exists')
    result = controls()
    if args.mode == 'verify':
        require(result['status'] == 'passed', 'independent controls failed')
        require(args.summary_sha256 and args.regions_sha256, 'READY result pins required')
        result = verify(BASE/'primary-summary.json', args.summary_sha256, BASE/'regions01.json', args.regions_sha256)
    result.update(checker_sha256=sha(Path(__file__)), python=sys.version, pillow=Image.__version__, argv=sys.argv)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({k: result[k] for k in ('status', 'check_count', 'frame_count', 'region_count', 'max_absolute_rho_error') if k in result}))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
