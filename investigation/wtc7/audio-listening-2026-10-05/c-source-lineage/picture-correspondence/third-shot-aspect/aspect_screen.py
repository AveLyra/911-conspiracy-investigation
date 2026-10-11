"""Fixed two-arm, held-image sensitivity; controls and method freeze precede scoring.

The imported parent supplies source checks/masks/scalar scoring and the pinned
core supplies working images and FFT surfaces. No source decoding or refitting
on evaluation masks. These are retrieval diagnostics, not authenticated events.
"""
import argparse
import contextlib
from fractions import Fraction
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import re
import signal
import sys
import time
import unittest

import numpy as np
from PIL import Image, _imaging

HERE = Path(__file__).resolve().parent
PARENT_DIR = HERE.parent
CORE_PATH = PARENT_DIR.parents[2] / 'peskin-figure-correspondence/match_screen.py'
CHARTER = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md')
ARMS = {'baseline': Fraction(1), 'native_relative_aspect': Fraction(133, 144)}
SCALES = [round(.75 + .05 * i, 2) for i in range(21)]
SECONDS = [14, 19, 24]
EARLY_INDICES = [(30000 * i + 1000) // 1001 for i in range(38)]
REFERENCE_INDICES = [(430 + s) * 30 for s in SECONDS]
METRICS = ('fit', 'static_evaluation', 'dynamic')
FROZEN = {
    PARENT_DIR / 'config.json': '56efd21495ef21b37df9137438f0b53183a120b59b1b43eb0f498b4ac47d65b2',
    PARENT_DIR / 'PROTOCOL.md': 'd0609694559608ffa87ab517e4b4ca3ea2c0e5bc9556a0458ee0faee103fd120',
    PARENT_DIR / 'picture_screen.py': 'f5d2c75f758da5f3bdf63bd4b8b38d2eba1897aa6a52c37e93f6f91559d44f86',
    PARENT_DIR / 'test_picture_screen.py': '8225adf3e4fbc15292e9e439927a8e581a4c15a1ad819c625d584674e67f7c43',
    PARENT_DIR / 'picture01/receipt.json': 'c459b4009d011291144086581c90afed3181328c63bfc54318ca5c8755a721ae',
    PARENT_DIR / 'picture02/receipt.json': '6ecd59e3d6f7a8d27f39ff1367c17f2ba9abb923de0fc22afc41d865efc63835',
    PARENT_DIR / 'independent-check.json': '6e8f7907f9bacc9ed99b92c01c5cd3986ccf4b7a82bcae8e0b5e66ed90729392',
    CORE_PATH: '06a400fbb378dfa710dd86799792f8f615a40eea19e82c23b9f3e0592a3b64a8',
    HERE / 'PROTOCOL.md': 'bc369159ff6aa3f71e204e72f9c01eb8749e81008f8271b83f8f31d0ca7ddc25',
    HERE / 'preparation-review.json': '3abb5b6a30e2bb371b51ca7b6b6c2853d4a647ded9bcec3a7ead20b8e6a3f078',
    CHARTER: '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd',
}


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'sha256': digest, 'bytes': path.stat().st_size}


def require_pins(pins):
    for path, digest in pins.items():
        if pin(path)['sha256'] != digest:
            raise ValueError(f'fixed input pin mismatch: {path}')


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dependencies():
    # Authenticate reusable executable bytes before import.
    require_pins(FROZEN)
    parent = module(PARENT_DIR / 'picture_screen.py', 'aspect_pinned_parent')
    config = parent.config_load()
    if Path(config['core']['path']) != CORE_PATH or config['scales'] != SCALES:
        raise ValueError('core/scales changed')
    return parent, module(parent.checked(config['core']), 'aspect_pinned_core'), config


def save(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def state(config):
    require_pins(FROZEN)
    versions = {'python': platform.python_version(), 'numpy': np.__version__, 'pillow': Image.__version__}
    if versions != {'python': '3.13.7', 'numpy': '2.3.4', 'pillow': '12.0.0'}:
        raise ValueError('runtime version mismatch')
    files = [*FROZEN, Path(__file__).resolve(), HERE / 'test_aspect_screen.py',
             Path(sys.executable), Path(np.__file__), Path(Image.__file__), Path(_imaging.__file__),
             Path(np._core._multiarray_umath.__file__), Path(np.fft._pocketfft_umath.__file__)]
    return {'schema_version': 1, **versions, 'platform': platform.platform(),
            'pins': {str(p): pin(p) for p in files},
            'source_specs': {k: config[k] for k in ('early_video', 'c_video', 'early_map', 'c_map')}}


def masks(parent, config):
    arm = config['third']
    fit, dynamic = parent.masks({'crop': arm['crop'], 'static': arm['static'][:1], 'dynamic': arm['dynamic']})
    evaluation, again = parent.masks({'crop': arm['crop'], 'static': arm['static'][1:], 'dynamic': arm['dynamic']})
    if (fit & evaluation).any() or not np.array_equal(dynamic, again):
        raise ValueError('fit/evaluation mask overlap/change')
    result = dict(zip(METRICS, (fit, evaluation, dynamic)))
    if [int(m.sum()) for m in result.values()] != [4784, 1363, 1886]:
        raise ValueError('fixed mask counts changed')
    return result


def canvas(parent, image, scale, factor):
    """Two-stage canvas; exact rational unrounded sizes, Python ties-to-even."""
    if type(factor) is not Fraction or factor not in ARMS.values() or scale not in SCALES:
        raise ValueError('unsupported fixed scale/factor')
    s = Fraction(str(scale))
    sw, sh = round(180 * s), round(120 * s * factor)
    if factor == 1:
        out, valid, transform = parent.canvas(image, scale)
        if (transform['raster_width'], transform['raster_height']) != (sw, sh):
            raise ValueError('baseline rounding mismatch')
    else:
        a = np.asarray(image)
        if a.shape != (120, 180) or not np.isfinite(a).all() or a.min() < 0 or a.max() > 255:
            raise ValueError('working geometry/range')
        x, y = 25 + (180 - sw) // 2, 25 + (120 - sh) // 2
        left, top, right, bottom = max(0, x), max(0, y), min(230, x + sw), min(170, y + sh)
        raster = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((sw, sh), Image.Resampling.BILINEAR))
        out = np.zeros((170, 230), float)
        valid = np.zeros_like(out, bool)
        out[top:bottom, left:right] = raster[top-y:bottom-y, left-x:right-x]
        valid[top:bottom, left:right] = True
        transform = {'requested_scale': scale, 'raster_width': sw, 'raster_height': sh,
                     'scale_x': sw/180, 'scale_y': sh/120, 'canvas_x': x, 'canvas_y': y,
                     'canvas_intersection': [left, top, right, bottom],
                     'scaled_raster_intersection': [left-x, top-y, right-x, bottom-y]}
    transform.update(height_factor=str(factor), requested_scale_exact=str(s),
                     unrounded_width=str(180*s), unrounded_height=str(120*s*factor),
                     native_magnification_x=str(Fraction(950*sw, 180*320)),
                     native_magnification_y=str(Fraction(720*sh, 120*224)))
    return out, valid, transform


def register(parent, core, image, target, regions, factor, scales=SCALES):
    scores, coverages, proposals = [], [], []
    for scale in scales:
        a, valid, transform = canvas(parent, image, scale, factor)
        score, coverage = core.pearson_surface(a, target, regions['fit'], valid)
        if score.shape != (51, 51) or coverage.shape != (51, 51):
            raise ValueError('translation grid changed')
        scores.append(score)
        coverages.append(coverage)
        ids = np.flatnonzero(np.isfinite(score))
        for index in ids[np.lexsort((ids, -score.flat[ids]))[:2]]:
            top, left = map(int, np.unravel_index(index, score.shape))
            patch = a[top:top+120, left:left+180]
            patch_valid = valid[top:top+120, left:left+180]
            evaluations = {name: parent.dynamic_score(core, patch, target, regions[name], patch_valid)
                           for name in METRICS[1:]}
            proposals.append({'fit_score': float(score[top, left]), 'fit_coverage': float(coverage[top, left]),
                              'fit_pixels': int((regions['fit'] & patch_valid).sum()),
                              'evaluations': evaluations, 'top': top, 'left': left,
                              'dx': left-25, 'dy': top-25,
                              'translation_boundary': top in (0, 50) or left in (0, 50),
                              'scale_boundary': scale in (.75, 1.75), **transform})
    proposals.sort(key=lambda r: (-r['fit_score'], r['requested_scale'], r['top'], r['left']))
    return proposals[:2], np.array(scores), np.array(coverages)


def metric(row, name):
    if not row['transforms']:
        return {'score': None, 'coverage': None, 'pixels': None, 'missing_reason': 'all_fit_transforms_invalid'}
    t = row['transforms'][0]
    if name == 'fit':
        return {'score': t['fit_score'], 'coverage': t['fit_coverage'], 'pixels': t['fit_pixels'], 'missing_reason': None}
    return t['evaluations'][name]


def delta(baseline, alternative):
    available = [v['score'] is not None for v in (baseline, alternative)]
    return {'baseline': baseline, 'alternative': alternative,
            'availability': {(True, True): 'both', (True, False): 'baseline_only',
                             (False, True): 'alternative_only', (False, False): 'neither'}[tuple(available)],
            'score_delta': alternative['score'] - baseline['score'] if all(available) else None,
            'coverage_delta': alternative['coverage'] - baseline['coverage']
            if baseline['coverage'] is not None and alternative['coverage'] is not None else None}


def common_support(parent, core, target, mask, patches):
    if patches is None:
        return {'valid_sets_equal': None, 'baseline_pixels': None, 'alternative_pixels': None,
                'intersection_pixels': None, 'intersection_coverage': None,
                'diagnostic': None, 'missing_reason': 'one_or_both_primary_fit_transforms_missing'}
    (a, av), (b, bv) = patches
    first, second = mask & av, mask & bv
    common = first & second
    scores = [parent.dynamic_score(core, image, target, mask, common) for image in (a, b)]
    return {'valid_sets_equal': bool(np.array_equal(first, second)),
            'baseline_pixels': int(first.sum()), 'alternative_pixels': int(second.sum()),
            'intersection_pixels': int(common.sum()), 'intersection_coverage': float(common.sum()/mask.sum()),
            'diagnostic': delta(*scores), 'missing_reason': None}


def paired(parent, core, image, target, regions, baseline, alternative):
    patches = []
    for row in (baseline, alternative):
        if not row['transforms']:
            patches = None
            break
        t = row['transforms'][0]
        a, valid, _ = canvas(parent, image, t['requested_scale'], ARMS[row['arm']])
        top, left = t['top'], t['left']
        patches.append((a[top:top+120, left:left+180], valid[top:top+120, left:left+180]))
    return {'reference_index': baseline['reference_index'], 'source_index': baseline['source_index'],
            'metrics': {name: delta(metric(baseline, name), metric(alternative, name)) for name in METRICS},
            'common_support': {name: common_support(parent, core, target, regions[name], patches) for name in METRICS[1:]}}


def rank(rows):
    output, union = {}, set()
    for name in METRICS:
        valid = [r for r in rows if metric(r, name)['score'] is not None]
        valid.sort(key=lambda r: (-metric(r, name)['score'], r['source_index']))
        ids = [r['source_index'] for r in valid]
        union.update(ids[:2])
        output[name] = {'ranking': [{'source_index': r['source_index'], **metric(r, name),
                                    'sample_boundary': r['source_index'] in (EARLY_INDICES[0], EARLY_INDICES[-1])}
                                   for r in valid],
                        'unavailable': [{'source_index': r['source_index'], **metric(r, name)}
                                        for r in sorted(rows, key=lambda r: r['source_index']) if metric(r, name)['score'] is None],
                        'top_two': ids[:2],
                        'near_best': {str(d): [r['source_index'] for r in valid
                                             if metric(valid[0], name)['score']-metric(r, name)['score'] <= d]
                                      for d in (.005, .01, .02)}}
    output['shortlist_union'] = sorted(union)
    return output


def pair_keys():
    return [(arm, ref, early) for ref in REFERENCE_INDICES for early in EARLY_INDICES for arm in ARMS]


def selection(parent, early_map, c_map):
    early = parent.select_rows(early_map, EARLY_INDICES)
    refs = parent.select_rows(c_map, REFERENCE_INDICES)
    for i, row in enumerate(early):
        if (type(row['quarter_bin']) is not int or row['quarter_bin'] != i
                or Fraction(row['source_seconds_exact']) != Fraction(row['source_index']*1001, 30000)
                or not Fraction(i) <= Fraction(row['source_seconds_exact']) < Fraction(i)+Fraction(1001, 30000)):
            raise ValueError('early selection PTS')
    for second, row in zip(SECONDS, refs):
        if Fraction(row['source_seconds_exact']) != 430+second:
            raise ValueError('C selection PTS')
    return early, refs


def inputs(parent, core, config):
    sources = {k: pin(parent.checked(config[k])) for k in ('early_video', 'c_video', 'early_map', 'c_map')}
    em, cm = Path(config['early_map']['path']), Path(config['c_map']['path'])
    early, refs = selection(parent, json.loads(em.read_text()), json.loads(cm.read_text()))
    images = [core.working(parent.frame(em, r, config['early_dimensions'])) for r in early]
    targets = [core.working(parent.frame(cm, r, config['c_dimensions']).crop(config['third']['crop'])) for r in refs]
    record = {'source_pins': sources, 'early': early, 'references': refs,
              'early_map': str(em), 'c_map': str(cm),
              'dimensions': {'early': config['early_dimensions'], 'C': config['c_dimensions']}}
    return record, images, targets


def screen(out, parent, core, config, start):
    before, images, targets = inputs(parent, core, config)
    regions = masks(parent, config)
    save(out/'input-map.json', before)
    results, comparisons = [], []
    for ref, target in zip(before['references'], targets):
        for row, image in zip(before['early'], images):
            members = []
            for arm, factor in ARMS.items():
                parent.budget(out, start, config)
                transforms, scores, coverage = register(parent, core, image, target, regions, factor)
                filename = f"surfaces-{arm}-C{ref['source_index']}-E{row['source_index']}.npz"
                with (out/filename).open('xb') as stream:
                    np.savez_compressed(stream, fit_scores=scores, fit_coverage=coverage)
                member = {'arm': arm, 'reference_index': ref['source_index'], 'source_index': row['source_index'],
                          'source_pts': row['source_pts'], 'source_time_base': row['source_time_base'],
                          'reference_pts': ref['source_pts'], 'reference_time_base': ref['source_time_base'],
                          'sample_boundary': row['source_index'] in (EARLY_INDICES[0], EARLY_INDICES[-1]),
                          'surface_file': filename, 'transforms': transforms,
                          'missing_reason': None if transforms else 'all_fit_transforms_invalid'}
                members.append(member)
                results.append(member)
            comparisons.append(paired(parent, core, image, target, regions, *members))
    if [(r['arm'], r['reference_index'], r['source_index']) for r in results] != pair_keys():
        raise ValueError('incomplete/duplicate pair coverage')
    save(out/'results.json', results)
    save(out/'paired-summary.json', comparisons)
    save(out/'rankings.json', {arm: {str(ref): rank([r for r in results if r['arm'] == arm and r['reference_index'] == ref])
                                          for ref in REFERENCE_INDICES} for arm in ARMS})
    # Full before/after map, rational PTS, PNG hash AND image geometry verification.
    after, after_images, after_targets = inputs(parent, core, config)
    if before != after or any(not np.array_equal(a, b) for a, b in zip(images+targets, after_images+after_targets)):
        raise ValueError('source/frame inputs changed')
    save(out/'input-map-after.json', after)
    parent.budget(out, start, config)
    return {'pairs': len(results), 'pairs_per_arm': 114, 'paired_comparisons': len(comparisons),
            'frames_verified_before_and_after': 41, 'surface_shape': [21, 51, 51],
            'mask_pixels': {k: int(v.sum()) for k, v in regions.items()}, 'human_accepted': False}


def control_gate(path, frozen):
    receipt = json.loads((path/'receipt.json').read_text())
    if receipt.get('mode') != 'controls' or receipt.get('status') != 'complete' or receipt.get('before') != frozen or receipt.get('after') != frozen:
        raise ValueError('stale/failed controls')
    products = receipt.get('products', {})
    if not {'controls.json', 'inherited/summary.json'} <= products.keys():
        raise ValueError('missing controls products')
    for name, expected in products.items():
        p = Path(name)
        if p.is_absolute() or '..' in p.parts or pin(path/p) != expected:
            raise ValueError('controls product mismatch')
    summary = json.loads((path/'controls.json').read_text())
    if (summary.get('pass') is not True or summary.get('inherited') != {'controls': 11, 'pass': True}
            or summary.get('adapter', {}).get('tests_run') != 9 or summary.get('adapter', {}).get('pass') is not True
            or summary.get('aspect', {}).get('tests_run') != 18 or summary.get('aspect', {}).get('pass') is not True):
        raise ValueError('incomplete controls')
    return pin(path/'receipt.json')


def freeze_gate(path, frozen, controls_pin):
    record = json.loads(path.read_text())
    if (record.get('schema_version') != 1 or record.get('status') != 'ready_for_historical'
            or record.get('method_state') != frozen or record.get('controls_receipt') != controls_pin):
        raise ValueError('method freeze mismatch')
    return pin(path)


def run_suite(tests):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
    text = stream.getvalue()
    print(text, end='')
    return {'pass': result.wasSuccessful() and not result.skipped,
            'tests_run': result.testsRun, 'output': text}


def controls(out, parent, core):
    inherited_dir = out/'inherited'
    inherited_dir.mkdir()
    inherited = core.controls(inherited_dir)
    adapter_tests = module(PARENT_DIR/'test_picture_screen.py', 'aspect_parent_tests')
    adapter_tests.ADAPTER, adapter_tests.CORE = parent, core
    adapter = run_suite(adapter_tests)
    own_tests = module(HERE/'test_aspect_screen.py', 'aspect_tests')
    own_tests.SUBJECT, own_tests.PARENT, own_tests.CORE = sys.modules[__name__], parent, core
    own = run_suite(own_tests)
    summary = {'pass': inherited['pass'] and adapter['pass'] and own['pass'],
               'inherited': inherited, 'adapter': adapter, 'aspect': own}
    save(out/'controls.json', summary)
    if not summary['pass'] or adapter['tests_run'] != 9 or own['tests_run'] != 18:
        raise ValueError('synthetic controls failed/count changed')
    return summary


def output_path(mode, name):
    pattern = r'controls[0-9]{2}' if mode == 'controls' else r'aspect0[12]'
    if not re.fullmatch(pattern, name):
        raise ValueError('out-of-scope run name')
    path = HERE/name
    if path.exists() or path.is_symlink():
        raise FileExistsError(path)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['controls', 'screen'])
    parser.add_argument('--run', required=True)
    parser.add_argument('--controls')
    args = parser.parse_args()
    out = output_path(args.mode, args.run)
    parent, core, config = dependencies()
    frozen = state(config)
    controls_pin = freeze_pin = None
    if args.mode == 'screen':
        if not args.controls or not re.fullmatch(r'controls[0-9]{2}', args.controls):
            raise ValueError('fresh controls required')
        controls_pin = control_gate(HERE/args.controls, frozen)
        freeze_pin = freeze_gate(HERE/'method-freeze.json', frozen, controls_pin)
    elif args.controls is not None:
        raise ValueError('controls does not consume --controls')
    out.mkdir(exist_ok=False)
    start = time.monotonic()
    receipt = {'schema_version': 1, 'mode': args.mode, 'status': 'started', 'before': frozen,
               'command': [sys.executable, '-B', str(Path(__file__).resolve()), *sys.argv[1:]],
               'controls_receipt': controls_pin, 'method_freeze': freeze_pin}
    save(out/'start.json', receipt)
    def timeout(*_):
        raise RuntimeError('wall time cap')
    old = signal.signal(signal.SIGALRM, timeout)
    signal.alarm(config['max_seconds'])
    try:
        receipt['result'] = controls(out, parent, core) if args.mode == 'controls' else screen(out, parent, core, config, start)
        receipt['after'] = state(config)
        if receipt['after'] != frozen:
            raise ValueError('method/runtime inputs changed')
        if args.mode == 'screen':
            if control_gate(HERE/args.controls, frozen) != controls_pin or freeze_gate(HERE/'method-freeze.json', frozen, controls_pin) != freeze_pin:
                raise ValueError('controls/freeze changed')
        parent.budget(out, start, config)
        receipt['status'] = 'complete'
    except Exception as exc:
        receipt.update(status='failed', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
        receipt['elapsed_s'] = time.monotonic()-start
        receipt['products'] = {str(p.relative_to(out)): pin(p) for p in sorted(out.rglob('*'))
                               if p.is_file() and p.name not in ('start.json', 'receipt.json')}
        save(out/'receipt.json', receipt)
    print(json.dumps({'status': receipt['status'], 'result': receipt['result'] if args.mode == 'screen'
                      else {'pass': receipt['result']['pass'], 'core_checks': 11, 'adapter_tests': 9, 'aspect_tests': 18}}))


if __name__ == '__main__':
    main()
