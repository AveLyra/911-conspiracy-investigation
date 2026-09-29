#!/usr/bin/env python3
"""Exact common-field comparison of separately frozen source extractions."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time

UNIT = Path(__file__).resolve().parent
INPUTS = {
    'independent-springs01.json': '0940e45f99999bb69bac8ee898c47dd967baae03a134a83be62fedd425520116',
    'independent-definition-presence01.json': '7377187b71fe0fc10a5483ed80424499555270708d02a61d2d2a991c14a939c7',
    'casea-root01.json': '27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
    'casea-root02.json': '4b1fff82bdb8778045bbe880d2bbf708d03788191480c0883b2bbd8fcfab4432',
}


def require(ok, code):
    if not ok:
        raise ValueError(code)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create(path, result):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')


def differences(a, b, path=''):
    """Exact numeric equality (int and float may equal); no tolerance/defaults."""
    if isinstance(a, dict) and isinstance(b, dict):
        found = []
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                found.append({'path': path + '/' + str(key), 'kind': 'missing_key'})
            else:
                found.extend(differences(a[key], b[key], path + '/' + str(key)))
        return found
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [{'path': path, 'kind': 'length', 'left': len(a), 'right': len(b)}]
        found = []
        for i, (x, y) in enumerate(zip(a, b)):
            found.extend(differences(x, y, path + '/' + str(i)))
        return found
    same = a == b
    if (isinstance(a, bool) or isinstance(b, bool)) and type(a) is not type(b):
        same = False
    return [] if same else [{'path': path, 'kind': 'value', 'left': a, 'right': b}]


def numeric_cards(cards):
    return [{'line': x['line'], 'values': x['values']} for x in cards]


def unique(records, key):
    index = {}
    for record in records:
        identity = str(key(record))
        require(identity not in index, 'DUPLICATE_COMPARISON_ID')
        index[identity] = record
    return index


def own_common(spring, definition):
    result = spring['result']
    blocks, elements, counts = {}, [], {}
    for chain in result['selected_part_chains']:
        pid = chain['effective_part']
        counts[str(pid)] = chain['full_part_element_count']
        for block in [chain['part'], chain['section_reference']['definition'], chain['material_reference']['definition']]:
            require(block is not None, 'COMMON_SELECTED_BLOCK_ABSENT')
            key = block['keyword'] + ':' + str(block['effective_id'])
            require(key not in blocks, 'DUPLICATE_COMMON_BLOCK')
            blocks[key] = {'source': block['source'], 'keyword': block['keyword'], 'keyword_line': block['keyword_line'],
                           'original_id': block['original_id'], 'effective_id': block['effective_id'],
                           'cards': numeric_cards(block['cards'])}
        for element in chain['selected_elements']:
            elements.append({k: element[k] for k in ['source', 'line', 'values']})
    curves = []
    for block in definition['result']['all_base_curves']:
        curves.append({'source': block['source'], 'keyword_line': block['keyword_line'], 'header_line': block['header_line'],
                       'curve_id': block['original_id'], 'values': block['cards'][0]['values'],
                       'points': numeric_cards(block['cards'][1:])})
    return {'elements': unique(elements, lambda x: (x['source'], x['line'], x['values'][0])),
            'blocks': blocks, 'full_part_counts': counts,
            'curves': unique(curves, lambda x: x['curve_id'])}


def root_common(report):
    raw = report['result']['springs_numeric_inventory']
    blocks = {}
    for key, block in raw['selected_cards'].items():
        original_id = block['cards'][0]['values'][0]
        require(original_id is not None and float(original_id).is_integer(), 'ROOT_BLOCK_ID_NOT_INTEGER')
        blocks[key] = {'source': block['source'], 'keyword': block['keyword'], 'keyword_line': block['keyword_line'],
                       'original_id': int(original_id), 'effective_id': int(original_id) + block['offset'],
                       'cards': numeric_cards(block['cards'])}
    # Use integral identifiers in tuple keys so 11343 and 11343.0 match;
    # the original complete arrays are nevertheless compared exactly below.
    elements = unique(raw['target_elements'], lambda x: (x['source'], x['line'], int(x['values'][0])))
    return {'elements': elements, 'blocks': blocks, 'full_part_counts': raw['selected_part_counts'],
            'curves': unique(raw['curve_inventory'], lambda x: x['curve_id'])}


def source_common_own(report):
    return {Path(x['compressed_before']['path']).name:
            {'compressed_bytes': x['compressed_before']['bytes'], 'compressed_sha256': x['compressed_before']['sha256'],
             'uncompressed_bytes': x['uncompressed_bytes'], 'uncompressed_sha256': x['uncompressed_sha256'],
             'lines': x['physical_lines'], 'eof': x['eof'],
             'pin_after': x['compressed_after']['sha256'] == x['compressed_before']['sha256']}
            for x in report['source_receipts']}


def controls():
    names = []
    base = {'elements': [{'line': 4, 'values': [1, None, 0, 2.0]}], 'points': [[0, 0], [1, 2]], 'count': 2}
    same = copy.deepcopy(base)
    same['elements'][0]['values'][0] = 1.0
    require(not differences(base, same), 'INT_FLOAT_EQUALITY_CONTROL')
    names.append('exact_numeric_integer_float_equality')
    for name, mutate in [
        ('blank_not_zero', lambda x: x['elements'][0]['values'].__setitem__(1, 0)),
        ('numeric_change', lambda x: x['elements'][0]['values'].__setitem__(3, 2.0000000000000004)),
        ('lineage_change', lambda x: x['elements'][0].__setitem__('line', 5)),
        ('point_order_change', lambda x: x['points'].reverse()),
        ('point_omission', lambda x: x['points'].pop()),
        ('count_change', lambda x: x.__setitem__('count', 3)),
        ('missing_field', lambda x: x.pop('count')),
    ]:
        changed = copy.deepcopy(base)
        mutate(changed)
        require(bool(differences(base, changed)), 'MUTATION_CONTROL')
        names.append(name)
    require(differences(0, False), 'BOOL_NUMERIC_CONTROL')
    names.append('boolean_not_numeric_zero')
    try:
        unique([{'id': 1}, {'id': 1}], lambda x: x['id'])
    except ValueError:
        names.append('duplicate_id_rejected')
    else:
        raise ValueError('DUPLICATE_CONTROL')
    with tempfile.TemporaryDirectory(prefix='spring-comparison-control-', dir='/private/tmp') as folder:
        path = Path(folder) / 'control.json'
        create(path, {'value': 1})
        try:
            create(path, {'value': 2})
        except FileExistsError:
            require(json.loads(path.read_bytes()) == {'value': 1}, 'CREATE_ONLY_PRESERVATION_CONTROL')
        else:
            raise ValueError('CREATE_ONLY_CONTROL')
    names.append('create_only')
    return {'status': 'passed', 'count': len(names), 'groups': names}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    require(args.output.resolve().parent == UNIT and args.output.name.startswith('spring-comparison') and args.output.suffix == '.json', 'OUTPUT_SCOPE')
    require(not args.output.exists(), 'OUTPUT_EXISTS')
    began = time.monotonic()
    receipt = {'command': sys.argv, 'code_sha256': digest(__file__), 'status': 'running'}
    try:
        receipt['controls'] = controls()
        if not args.controls_only:
            inputs, pins = {}, {}
            for name, expected in INPUTS.items():
                path = UNIT / name
                actual = digest(path)
                require(actual == expected, 'INPUT_PIN_MISMATCH')
                pins[name] = {'path': str(path), 'sha256': actual, 'bytes': path.stat().st_size}
                inputs[name] = json.loads(path.read_bytes())
                require(inputs[name]['status'] == 'passed', 'INPUT_NOT_PASSED')
            own_result = own_common(inputs['independent-springs01.json'], inputs['independent-definition-presence01.json'])
            comparisons = {}
            for name in ['casea-root01.json', 'casea-root02.json']:
                root_result = root_common(inputs[name])
                comparisons['independent_vs_' + name] = differences(own_result, root_result)
                source_root = inputs[name]['result']['sources']
                own_sources = source_common_own(inputs['independent-springs01.json'])
                comparisons['source_pins_vs_' + name] = differences(own_sources, {k: source_root[k] for k in own_sources})
            comparisons['root_repeat_spring_inventory'] = differences(inputs['casea-root01.json']['result']['springs_numeric_inventory'], inputs['casea-root02.json']['result']['springs_numeric_inventory'])
            comparisons['independent_repeated_source_pass_pins'] = differences(source_common_own(inputs['independent-springs01.json']), source_common_own(inputs['independent-definition-presence01.json']))
            receipt['pins_before'] = pins
            receipt['result'] = {'comparisons': comparisons, 'all_common_fields_equal': all(not x for x in comparisons.values()),
                                 'scope_counts': {'selected_elements': len(own_result['elements']), 'element_numeric_fields': sum(len(x['values']) for x in own_result['elements'].values()),
                                                  'selected_blocks': len(own_result['blocks']), 'selected_cards': sum(len(x['cards']) for x in own_result['blocks'].values()),
                                                  'selected_card_fields': sum(len(c['values']) for x in own_result['blocks'].values() for c in x['cards']),
                                                  'selected_part_counts': len(own_result['full_part_counts']), 'all_inventory_curves': len(own_result['curves']),
                                                  'all_curve_header_fields': sum(len(x['values']) for x in own_result['curves'].values()),
                                                  'all_curve_points': sum(len(x['points']) for x in own_result['curves'].values())},
                                 'selected_curve_dependency_finding': inputs['independent-definition-presence01.json']['result']['selected_reference_presence'],
                                 'limits': ['All-curve equality is inventory verification, not selected law evaluation: selected602/803 absent.',
                                            'No numeric tolerance or implicit defaults; JSON integer/float representations compare by exact numeric value.',
                                            'Title hashes, numeric lexemes, full selected-PID membership lists and selection-list lineage lack matching root schema and are not independently certified here.',
                                            'Element keyword-line locators are not in root schema; element source/card line and all8fields are compared.',
                                            'Only common spring/source fields are compared; no certification of CaseA geometry or unrelated root fields.',
                                            'No source execution, physical calibration, activation, unit assignment or historical-run inference.']}
            receipt['pins_after'] = {name: digest(UNIT / name) for name in INPUTS}
            require(all(receipt['pins_after'][k] == v for k, v in INPUTS.items()), 'POST_PIN_MISMATCH')
            require(receipt['result']['all_common_fields_equal'], 'COMMON_FIELD_DIFFERENCE')
        receipt['status'] = 'passed'
    except Exception as error:
        receipt['status'] = 'failed'
        receipt['failure_code'] = str(error) if type(error) is ValueError else type(error).__name__
    receipt['elapsed_seconds'] = time.monotonic() - began
    create(args.output, receipt)
    print(json.dumps({'status': receipt['status'], 'output': str(args.output), 'sha256': digest(args.output), 'failure_code': receipt.get('failure_code')}))
    return 0 if receipt['status'] == 'passed' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'status': 'failed_before_receipt', 'failure_code': str(error) if type(error) is ValueError else type(error).__name__}))
        sys.exit(1)
