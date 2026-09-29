"""Independent batch-2 validation and arithmetic; no producer import or images."""
import argparse
import ast
from collections import Counter
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
SOURCE = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation/fire-annotation')
PROTOCOL_SHA = '8ea3df6a4550e55de334ac20ce45a8fb05aa00f47800a6ca7b874f74803d94ff'
KEY_SHA = 'c0361c5a3ae52c2663a6772db6078824b4b123e59d8e50d2e24b26d85855afa3'
MAIN_SHA = '63100450901d2358ee14f253a95b154f038091a88e0d3cf1c81e56126a0c2c2b'
REVIEWER_SHA = '2f31b1db855ec6533cd6bb9e7a43670ecc54520fa179a7b2ae4f8e55aa404ac7'
PRIOR_MAIN_SHA = 'd7673cc50ebca454ea30a0d2c45e44041e9d06de9f586e32dd27a65818f535ce'
PRIOR_REVIEWER_SHA = '03c671cfb383e939509e0008101a81e4954141c8c8f680596bbecde573f128f0'
IDS = ['A-873f87e7149b', 'A-e1b0c06ad11d', 'A-9e7b4935c8aa', 'A-0b722775db93',
       'A-fa6f410444bb', 'A-ffe3726a0312', 'A-0e60b82a1a4c', 'A-6902e91e39ee',
       'A-671f312eade8', 'A-69d899e75343', 'A-8bc36f05fe38', 'A-7b61385d1373',
       'A-f1e2fa01e344']
FIELDS = {'asset_id', 'image_sha256', 'dimensions', 'complete_native_image_inspected',
          'target_rect', 'target_evaluability', 'target_reason', 'luminous_features',
          'smoke', 'nondetection_regions', 'visibility_limits', 'overlay_regions'}
AXES = ('target_evaluability', 'any_flame_like', 'any_ambiguous_glow',
        'smoke_status', 'any_nondetection_region')
FROZEN_CONTROL_SHA = 'f35841710ded5b2c7770c40630ac4bd3d706e3ff9475248fb5233ab3f8c108a7'
FROZEN_RESULT_SHA = '75deedc4ab184c9eb079a3f011439479517856005fbca0e58a5fbd6142770ade'
PRODUCT_SHA = 'f6934003b585a3d2f43e5ae5c7965b9a5b687247c0c5fa590117e7ddcf8e3cfb'


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    need(not path.is_symlink(), 'input_symlink')
    return sha_bytes(path.read_bytes())


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate_json_key')
            result[key] = value
        return result
    def bad_constant(value):
        raise ValueError('nonfinite_json_constant')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad_constant)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def rectangle(rect, dimensions):
    need(isinstance(rect, list) and len(rect) == 4, 'rect_shape')
    need(all(finite_number(v) for v in rect), 'rect_numeric')
    x0, y0, x1, y1 = rect
    need(0 <= x0 < x1 <= dimensions[0] and 0 <= y0 < y1 <= dimensions[1], 'rect_bounds')


def validate_asset(record, metadata):
    need(isinstance(record, dict) and set(record) == FIELDS, 'asset_fields')
    need(record['asset_id'] == metadata['asset_id'], 'asset_identity')
    view = metadata['extracted_view']
    dims = record['dimensions']
    need(isinstance(dims, list) and len(dims) == 2 and
         all(type(d) is int and d > 0 for d in dims), 'dimensions_type')
    need(dims == metadata['native_pdf_dimensions'] == view['dimensions'], 'dimension_pin')
    need(record['image_sha256'] == view['sha256'], 'image_pin')
    need(record['complete_native_image_inspected'] is True, 'inspection_declaration')
    evaluation = record['target_evaluability']
    need(evaluation in ('partial_detail', 'limited_detail', 'unresolved_target'), 'target_enum')
    if evaluation == 'unresolved_target':
        need(record['target_rect'] is None, 'unresolved_target_rectangle')
        need(record['nondetection_regions'] == [], 'unresolved_target_nondetection')
    else:
        rectangle(record['target_rect'], dims)
    need(nonempty(record['target_reason']), 'target_reason')
    need(isinstance(record['luminous_features'], list), 'luminous_list')
    for feature in record['luminous_features']:
        need(isinstance(feature, dict) and set(feature) ==
             {'rect', 'appearance', 'target_relation', 'reason', 'alternatives'}, 'luminous_fields')
        rectangle(feature['rect'], dims)
        need(feature['appearance'] in ('flame_like', 'ambiguous_glow'), 'appearance_enum')
        need(feature['target_relation'] in ('on_candidate_facade', 'uncertain'), 'relation_enum')
        need(nonempty(feature['reason']), 'luminous_reason')
        alternatives = feature['alternatives']
        need((nonempty(alternatives) or (isinstance(alternatives, list) and bool(alternatives)
              and all(nonempty(a) for a in alternatives))), 'luminous_alternatives')
    smoke = record['smoke']
    need(isinstance(smoke, dict) and set(smoke) == {'status', 'regions', 'reason'}, 'smoke_fields')
    need(smoke['status'] in ('visible', 'uncertain', 'not_identified'), 'smoke_enum')
    need(isinstance(smoke['regions'], list) and nonempty(smoke['reason']), 'smoke_regions_reason')
    for rect in smoke['regions']:
        rectangle(rect, dims)
    if smoke['status'] == 'visible':
        need(bool(smoke['regions']), 'visible_smoke_requires_locator')
    if smoke['status'] == 'not_identified':
        need(not smoke['regions'], 'unidentified_smoke_has_locator')
    need(isinstance(record['nondetection_regions'], list), 'nondetection_list')
    for region in record['nondetection_regions']:
        need(isinstance(region, dict) and set(region) == {'rect', 'reason'}, 'nondetection_fields')
        rectangle(region['rect'], dims)
        need(nonempty(region['reason']), 'nondetection_reason')
    limits = record['visibility_limits']
    need(isinstance(limits, list) and bool(limits) and all(nonempty(v) for v in limits), 'visibility_limits')
    need(isinstance(record['overlay_regions'], list), 'overlay_list')
    for rect in record['overlay_regions']:
        rectangle(rect, dims)


def validate_document(document, metadata):
    need(isinstance(document, dict), 'document_object')
    need({'reviewer', 'independence', 'protocol_sha256', 'provenance_key_sha256', 'assets'} <= set(document), 'document_fields')
    need(nonempty(document['reviewer']), 'reviewer')
    independent = document['independence']
    need(nonempty(independent) or (isinstance(independent, dict) and bool(independent)), 'independence')
    need(document['protocol_sha256'] == PROTOCOL_SHA and document['provenance_key_sha256'] == KEY_SHA, 'document_pins')
    records = document['assets']
    need(isinstance(records, list), 'assets_array')
    need(len(records) == len(IDS) and all(isinstance(r, dict) for r in records), 'record_count')
    need([r.get('asset_id') for r in records] == IDS, 'membership_or_order')
    for record in records:
        validate_asset(record, metadata[record['asset_id']])


def axes(record):
    return dict(zip(AXES, [record['target_evaluability'],
        any(f['appearance'] == 'flame_like' for f in record['luminous_features']),
        any(f['appearance'] == 'ambiguous_glow' for f in record['luminous_features']),
        record['smoke']['status'], bool(record['nondetection_regions'])]))


def differences(left, right, pointer=''):
    """Exact unforced ordered-list and string differences, beyond coarse axes."""
    if type(left) is not type(right):
        return [{'pointer': pointer, 'kind': 'type', 'main': left, 'reviewer': right}]
    if isinstance(left, dict):
        output = []
        for key in sorted(set(left) | set(right)):
            child = pointer+'/'+key.replace('~', '~0').replace('/', '~1')
            if key not in left or key not in right:
                output.append({'pointer': child, 'kind': 'missing_key',
                    'main_present': key in left, 'reviewer_present': key in right,
                    'main': left.get(key), 'reviewer': right.get(key)})
            else:
                output.extend(differences(left[key], right[key], child))
        return output
    if isinstance(left, list):
        output = []
        if len(left) != len(right):
            output.append({'pointer': pointer, 'kind': 'list_length', 'main': len(left), 'reviewer': len(right)})
        for index in range(max(len(left), len(right))):
            child = pointer+'/'+str(index)
            if index >= len(left) or index >= len(right):
                output.append({'pointer': child, 'kind': 'unpaired_list_item',
                    'main_present': index < len(left), 'reviewer_present': index < len(right),
                    'main': left[index] if index < len(left) else None,
                    'reviewer': right[index] if index < len(right) else None})
            else:
                output.extend(differences(left[index], right[index], child))
        return output
    return [] if left == right else [{'pointer': pointer, 'kind': 'value', 'main': left, 'reviewer': right}]


def compare(main, reviewer):
    output, pairs = [], {axis: [] for axis in AXES}
    for left, right in zip(main['assets'], reviewer['assets']):
        need(left['asset_id'] == right['asset_id'], 'comparison_order')
        la, ra = axes(left), axes(right)
        values = {axis: {'main': la[axis], 'reviewer': ra[axis], 'agree': la[axis] == ra[axis]} for axis in AXES}
        for axis in AXES:
            pairs[axis].append(values[axis])
        output.append({'asset_id': left['asset_id'], 'axes': values,
            'all_five_agree': all(value['agree'] for value in values.values()),
            'full_record_equal': left == right, 'full_field_differences': differences(left, right),
            'main_record': copy.deepcopy(left), 'reviewer_record': copy.deepcopy(right)})
    statistics = {}
    for axis in AXES:
        agree = sum(pair['agree'] for pair in pairs[axis])
        counts = Counter(json.dumps([pair['main'], pair['reviewer']]) for pair in pairs[axis])
        statistics[axis] = {'agree': agree, 'different': len(output)-agree,
            'pairs': [{'values': json.loads(value), 'count': count} for value, count in sorted(counts.items())],
            'different_assets': [row['asset_id'] for row in output if not row['axes'][axis]['agree']]}
    return {'asset_count': len(output), 'axes': statistics, 'per_asset': output,
            'all_five_agree_count': sum(row['all_five_agree'] for row in output),
            'full_record_equal_count': sum(row['full_record_equal'] for row in output),
            'original_records': {'main': copy.deepcopy(main), 'reviewer': copy.deepcopy(reviewer)}}


def synthetic():
    checks = []
    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
    def rejects(call):
        try:
            call()
        except (ValueError, TypeError, KeyError):
            return True
        return False
    metadata = {name: {'asset_id': name, 'native_pdf_dimensions': [100, 80],
        'extracted_view': {'dimensions': [100, 80], 'sha256': 'a'*64}} for name in IDS}
    record = {'asset_id': IDS[0], 'image_sha256': 'a'*64, 'dimensions': [100, 80],
        'complete_native_image_inspected': True, 'target_rect': [1, 2, 99, 79],
        'target_evaluability': 'partial_detail', 'target_reason': 'Synthetic limited visible frontage.',
        'luminous_features': [{'rect': [10, 20, 20, 30], 'appearance': 'flame_like',
          'target_relation': 'uncertain', 'reason': 'Synthetic irregular luminous form.',
          'alternatives': ['Synthetic reflection alternative.']}],
        'smoke': {'status': 'visible', 'regions': [[1, 3, 90, 60]], 'reason': 'Synthetic veil; source unresolved.'},
        'nondetection_regions': [{'rect': [30, 30, 50, 50], 'reason': 'No shape identified in this synthetic visible patch; resolution limited.'}],
        'visibility_limits': ['Synthetic resolution limitation.'], 'overlay_regions': [[90, 2, 99, 10]]}
    doc = {'reviewer': 'synthetic', 'independence': 'Synthetic controls only.',
        'protocol_sha256': PROTOCOL_SHA, 'provenance_key_sha256': KEY_SHA, 'assets': []}
    for name in IDS:
        item = copy.deepcopy(record); item['asset_id'] = name; doc['assets'].append(item)
    check('valid_full_membership', not rejects(lambda: validate_document(doc, metadata)))
    check('smoke_and_nondetection_coexist', axes(record)['smoke_status'] == 'visible' and axes(record)['any_nondetection_region'])
    altered = copy.deepcopy(doc); altered['assets'][0]['luminous_features'][0]['rect'] = [60, 20, 70, 30]
    result = compare(doc, altered)
    check('same_count_different_location_not_hidden', result['all_five_agree_count'] == 13 and
          not result['per_asset'][0]['full_record_equal'] and bool(result['per_asset'][0]['full_field_differences']))
    check('complete_records_retained', result['original_records'] == {'main': doc, 'reviewer': altered})
    altered['assets'][0]['luminous_features'][0]['reason'] = 'Changed synthetic description.'
    check('description_difference_retained', any(d['pointer'].endswith('/reason') for d in differences(doc, altered)))
    altered['assets'][0]['luminous_features'].append(dict(record['luminous_features'][0], appearance='ambiguous_glow'))
    mixed = axes(altered['assets'][0])
    check('two_luminous_axes_not_exclusive', mixed['any_flame_like'] and mixed['any_ambiguous_glow'])
    check('exact_axis_difference', compare(doc, altered)['axes']['any_ambiguous_glow']['different_assets'] == [IDS[0]])
    before = json.dumps(doc, sort_keys=True); compare(doc, altered)
    check('comparison_does_not_mutate_input', json.dumps(doc, sort_keys=True) == before)
    check('byte_mutation_detected', sha_bytes(b'original') != sha_bytes(b'changed'))
    check('duplicate_json_key_rejected', rejects(lambda: strict_json('{"x":1,"x":2}')))
    check('nonfinite_json_rejected', rejects(lambda: strict_json('{"x":NaN}')))
    check('malformed_json_rejected', rejects(lambda: strict_json('{')))
    changes = [
        ('bool_coordinate', ('target_rect',), [False, 2, 20, 30]),
        ('nonfinite_coordinate', ('target_rect',), [1, 2, float('inf'), 30]),
        ('degenerate_rect', ('target_rect',), [2, 2, 2, 30]),
        ('out_of_bounds_rect', ('target_rect',), [1, 2, 101, 30]),
        ('bool_dimension', ('dimensions',), [True, 80]),
        ('wrong_dimension', ('dimensions',), [101, 80]),
        ('wrong_image_pin', ('image_sha256',), 'b'*64),
        ('inspection_false', ('complete_native_image_inspected',), False),
        ('bad_target_enum', ('target_evaluability',), 'confirmed'),
        ('empty_reason', ('target_reason',), '  '),
        ('unresolved_nonnull', ('target_evaluability',), 'unresolved_target'),
        ('visible_smoke_without_locator', ('smoke', 'regions'), []),
        ('unidentified_smoke_with_locator', ('smoke', 'status'), 'not_identified'),
        ('empty_limits', ('visibility_limits',), []),
        ('bad_smoke_enum', ('smoke', 'status'), 'confirmed'),
        ('nonlist_luminous', ('luminous_features',), None),
    ]
    for name, path, value in changes:
        bad = copy.deepcopy(record); cursor = bad
        for part in path[:-1]:
            cursor = cursor[part]
        cursor[path[-1]] = value
        check(name+'_rejected', rejects(lambda bad=bad: validate_asset(bad, metadata[IDS[0]])))
    for name, change in [('missing_field', lambda d: d.pop('smoke')), ('extra_field', lambda d: d.update(extra=1))]:
        bad = copy.deepcopy(record); change(bad)
        check(name+'_rejected', rejects(lambda bad=bad: validate_asset(bad, metadata[IDS[0]])))
    for name, items in [('missing', doc['assets'][:-1]), ('duplicate', [doc['assets'][0]]*13), ('wrong_order', doc['assets'][::-1])]:
        bad = dict(doc, assets=items)
        check(name+'_membership_rejected', rejects(lambda bad=bad: validate_document(bad, metadata)))
    unresolved = copy.deepcopy(record); unresolved.update(target_rect=None,
        target_evaluability='unresolved_target', luminous_features=[], nondetection_regions=[])
    check('unresolved_accepted_without_absence_inference', not rejects(lambda: validate_asset(unresolved, metadata[IDS[0]])))
    uncertain = copy.deepcopy(record); uncertain['smoke'].update(status='uncertain', regions=[])
    check('uncertain_smoke_without_locator_accepted', not rejects(lambda: validate_asset(uncertain, metadata[IDS[0]])))
    return {'status': 'passed' if all(c['passed'] for c in checks) else 'failed', 'checks': checks, 'check_count': len(checks)}


def historical():
    pins = {}
    def load(path, expected):
        data = path.read_bytes(); need(not path.is_symlink() and sha_bytes(data) == expected, 'frozen_input_pin')
        pins[str(path)] = expected
        return strict_json(data)
    need(sha_file(BASE/'PROTOCOL.md') == PROTOCOL_SHA, 'protocol_file_pin')
    pins[str(BASE/'PROTOCOL.md')] = PROTOCOL_SHA
    key = load(SOURCE/'assets/run-01/reviewed-provenance-key.json', KEY_SHA)
    prior_main = load(SOURCE/'main-image-level.json', PRIOR_MAIN_SHA)
    prior_reviewer = load(SOURCE/'reviewer-image-level.json', PRIOR_REVIEWER_SHA)
    entries = key['assets']; need(len(entries) == 28, 'key_asset_count')
    need(len({item['asset_id'] for item in entries}) == 28, 'key_duplicate_asset')
    photos = {item['asset_id'] for item in entries if item['role'] == 'report_photographic_image'}
    graphics = {item['asset_id'] for item in entries if item['role'] == 'report_geometry_graphic'}
    need(len(photos) == 25 and len(graphics) == 3 and not photos & graphics, 'role_partition')
    pm = [r['asset_id'] for r in prior_main['images']]
    pr = [r['asset_id'] for r in prior_reviewer['assets']]
    need(len(pm) == len(pr) == len(set(pm)) == len(set(pr)) == 12 and set(pm) == set(pr), 'prior_membership')
    need(set(pm) <= photos and photos-set(pm) == set(IDS), 'remaining_membership')
    metadata = {item['asset_id']: item for item in entries}
    images = []
    for name in IDS:
        view = metadata[name]['extracted_view']
        relative = f'assets/run-01/images/{name}.jpg'
        need(view['path'] == relative, 'image_path_allowlist')
        path = SOURCE/relative
        need(sha_file(path) == view['sha256'] and path.stat().st_size == view['bytes'], 'image_byte_pin')
        pins[str(path)] = view['sha256']
        images.append({'asset_id': name, 'sha256': view['sha256'], 'bytes': view['bytes'],
                       'dimensions': view['dimensions']})
    main = load(BASE/'main.json', MAIN_SHA); reviewer = load(BASE/'reviewer.json', REVIEWER_SHA)
    validate_document(main, metadata); validate_document(reviewer, metadata)
    result = compare(main, reviewer)
    for path, pin in pins.items():
        need(sha_file(Path(path)) == pin, 'input_changed_during_check')
    result.update(status='passed', input_pins=pins, images=images,
        inventory={'key_assets': 28, 'photographic_assets': 25, 'geometry_graphics': sorted(graphics),
                   'prior_paired_assets': sorted(pm), 'new_declared_assets': IDS},
        limits='Schema and arithmetic verification, not visual correctness; same-count lists are not same-location observations. Source-key classifications and image-inspection declarations are not independently interpreted or authenticated.')
    return result


def project_comparison(own):
    """Adapter added after the independent raw calculation froze; no new axes."""
    names = {'target_evaluability': 'target_evaluability', 'any_flame_like': 'flame_like_identified',
             'any_ambiguous_glow': 'ambiguous_glow_identified', 'smoke_status': 'smoke_status',
             'any_nondetection_region': 'nondetection_region_identified'}
    output = []
    for row in own['per_asset']:
        left, right = row['main_record'], row['reviewer_record']
        paired = {}
        for key in ('target_rect', 'luminous_features', 'nondetection_regions', 'overlay_regions'):
            paired[key] = {'left': left[key], 'right': right[key], 'identical_json': left[key] == right[key]}
        paired['smoke_regions'] = {'left': left['smoke']['regions'], 'right': right['smoke']['regions'],
                                  'identical_json': left['smoke']['regions'] == right['smoke']['regions']}
        descriptions = {}
        for key in ('target_reason', 'visibility_limits'):
            descriptions[key] = {'left': left[key], 'right': right[key], 'identical_json': left[key] == right[key]}
        descriptions['smoke_reason'] = {'left': left['smoke']['reason'], 'right': right['smoke']['reason'],
                                      'identical_json': left['smoke']['reason'] == right['smoke']['reason']}
        output.append({'asset_id': row['asset_id'], 'regions_without_forced_matching': paired,
            'descriptions': descriptions, 'axes': {names[name]: {'left': value['main'],
                'right': value['reviewer'], 'comparison': 'same' if value['agree'] else 'different'}
                for name, value in row['axes'].items()}})
    return [{'left_reviewer': own['original_records']['main']['reviewer'],
             'right_reviewer': own['original_records']['reviewer']['reviewer'], 'assets': output}]


def adapter_controls():
    left = {'asset_id': 'synthetic', 'target_evaluability': 'limited_detail', 'target_rect': [1, 2, 9, 10],
        'target_reason': 'Synthetic target reason.', 'visibility_limits': ['Synthetic visibility limit.'],
        'luminous_features': [], 'smoke': {'status': 'visible', 'regions': [[1, 3, 8, 9]], 'reason': 'Synthetic veil.'},
        'nondetection_regions': [{'rect': [1, 2, 3, 4], 'reason': 'Synthetic bounded visible patch.'}],
        'overlay_regions': [[0, 0, 1, 1]]}
    right = copy.deepcopy(left); right['target_rect'] = [2, 2, 10, 10]
    right['target_reason'] = 'A different synthetic target reason.'
    own = compare({'reviewer': 'left', 'assets': [left]}, {'reviewer': 'right', 'assets': [right]})
    row = project_comparison(own)[0]['assets'][0]
    checks = {
        'adapter_all_five_axes': set(row['axes']) == {'target_evaluability', 'flame_like_identified',
             'ambiguous_glow_identified', 'smoke_status', 'nondetection_region_identified'},
        'adapter_region_location_difference_preserved': row['regions_without_forced_matching']['target_rect'] ==
             {'left': [1, 2, 9, 10], 'right': [2, 2, 10, 10], 'identical_json': False},
        'adapter_description_difference_preserved': not row['descriptions']['target_reason']['identical_json'],
        'adapter_coexisting_smoke_nondetection': row['axes']['smoke_status']['left'] == 'visible' and
             row['axes']['nondetection_region_identified']['left'] is True,
        'adapter_all_region_fields': set(row['regions_without_forced_matching']) ==
             {'target_rect', 'luminous_features', 'smoke_regions', 'nondetection_regions', 'overlay_regions'},
        'adapter_all_description_fields': set(row['descriptions']) == {'target_reason', 'smoke_reason', 'visibility_limits'},
        'adapter_empty_list_retained': row['regions_without_forced_matching']['luminous_features'] ==
             {'left': [], 'right': [], 'identical_json': True},
    }
    changed = copy.deepcopy(row); changed['regions_without_forced_matching']['target_rect']['right'] = [1, 2, 9, 10]
    checks['adapter_mutated_location_detectable'] = bool(differences(row, changed))
    return [{'name': key, 'passed': value} for key, value in checks.items()]


def products():
    need(sha_file(BASE/'independent-controls01.json') == FROZEN_CONTROL_SHA, 'frozen_control_receipt_pin')
    control = strict_json((BASE/'independent-controls01.json').read_bytes())
    prior_tree = ast.parse(control['frozen_implementation_source'])
    now_tree = ast.parse(Path(__file__).read_text())
    prior_functions = {n.name: ast.dump(n, include_attributes=False) for n in prior_tree.body if isinstance(n, ast.FunctionDef) and n.name != 'main'}
    now_functions = {n.name: ast.dump(n, include_attributes=False) for n in now_tree.body if isinstance(n, ast.FunctionDef)}
    need(all(now_functions.get(name) == value for name, value in prior_functions.items()), 'frozen_independent_functions_changed')
    need(sha_file(BASE/'independent-check01.json') == FROZEN_RESULT_SHA, 'independent_result_pin')
    own = strict_json((BASE/'independent-check01.json').read_bytes())
    for path, pin in own['input_pins'].items():
        need(sha_file(Path(path)) == pin, 'frozen_source_changed')
    expected_comparison = project_comparison(own)
    records = [own['original_records']['main'], own['original_records']['reviewer']]
    hashes = {'code_sha256': sha_file(BASE/'summarize.py'), 'protocol_sha256': PROTOCOL_SHA,
        'provenance_key_sha256': KEY_SHA, 'labels': [{'reviewer': records[0]['reviewer'], 'sha256': MAIN_SHA},
        {'reviewer': records[1]['reviewer'], 'sha256': REVIEWER_SHA}],
        'images': [dict(row, path=f"assets/run-01/images/{row['asset_id']}.jpg") for row in own['images']]}
    products_read = []
    for name in ('comparison01.json', 'comparison02.json'):
        path = BASE/name; data = path.read_bytes(); need(sha_bytes(data) == PRODUCT_SHA, 'producer_product_pin')
        product = strict_json(data)
        need(product['sample_asset_ids'] == IDS, 'producer_sample_membership')
        need(product['source_hashes'] == hashes, 'producer_source_hashes')
        need(product['raw_records'] == records, 'full_raw_records_not_retained')
        need(product['comparisons'] == expected_comparison, 'producer_full_comparison_discrepancy')
        products_read.append({'path': name, 'sha256': sha_bytes(data), 'bytes': len(data)})
    need((BASE/'comparison01.json').read_bytes() == (BASE/'comparison02.json').read_bytes(), 'producer_replays_differ')
    for path, pin in own['input_pins'].items():
        need(sha_file(Path(path)) == pin, 'source_changed_during_product_check')
    for item in products_read:
        need(sha_file(BASE/item['path']) == item['sha256'], 'product_changed_during_check')
    region_summary = {}
    for section in ('regions_without_forced_matching', 'descriptions'):
        region_summary[section] = {name: sum(row[section][name]['identical_json'] for row in expected_comparison[0]['assets'])
            for name in expected_comparison[0]['assets'][0][section]}
    return {'status': 'passed', 'independent_input_result_sha256': FROZEN_RESULT_SHA,
        'frozen_initial_implementation_sha256': control['checker_sha256'],
        'all_frozen_functions_ast_unchanged': sorted(prior_functions),
        'products': products_read, 'producer_source_hashes_verified': hashes,
        'asset_count': len(IDS), 'axis_comparisons_per_product': len(IDS)*len(AXES),
        'region_pairs_per_product': len(IDS)*5, 'description_pairs_per_product': len(IDS)*3,
        'full_raw_documents_per_product': 2, 'identical_pair_counts': region_summary,
        'independent_axis_summary': own['axes'], 'all_five_agree_count': own['all_five_agree_count'],
        'full_record_equal_count': own['full_record_equal_count'],
        'limits': 'Full data-field equality and pinned bytes; producer prose/schema-version not independently validated; source classifications and visual accuracy not inferred.'}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('mode', choices=('controls', 'run', 'products'))
    parser.add_argument('--output', type=Path, required=True); args = parser.parse_args()
    need(args.output.parent.resolve() == BASE and args.output.name.startswith('independent-'), 'output_scope')
    if args.output.exists():
        raise FileExistsError('create_only_output_exists')
    controls = synthetic(); need(controls['status'] == 'passed', 'synthetic_controls_failed')
    controls['checks'].extend(adapter_controls()); controls['check_count'] = len(controls['checks'])
    need(all(row['passed'] for row in controls['checks']), 'adapter_controls_failed')
    result = controls if args.mode == 'controls' else historical() if args.mode == 'run' else products()
    result.update(checker_sha256=sha_file(Path(__file__)), python=sys.version, argv=sys.argv)
    if args.mode == 'controls':
        result['frozen_implementation_source'] = Path(__file__).read_text()
    else:
        result['synthetic_control_count'] = controls['check_count']
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False); stream.write('\n')
    print(json.dumps({key: result[key] for key in ('status', 'check_count', 'asset_count', 'all_five_agree_count', 'full_record_equal_count') if key in result}))


if __name__ == '__main__':
    main()
