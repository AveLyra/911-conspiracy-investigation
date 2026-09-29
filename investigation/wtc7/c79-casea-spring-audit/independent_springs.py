#!/usr/bin/env python3
"""Independent numeric-only source reader. No source commands are executed."""
import argparse
import collections
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re
import resource
import sys
import tempfile
import time

UNIT = Path(__file__).resolve().parent
RAW = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PROTOCOL_SHA = 'b616114713bdfb20765bc033adc12d38cf888ae95704a41c17f705c3e791ea41'
SELECTION = UNIT.parent / 'c79-contact-geometry/contact-damage01.json'
SELECTION_SHA = 'e43d8922c511debb4a004f6342fbdb8c16e76ff26cdb306fbd161c77a536d479'
SOURCES = [
 (119, 'discrete_mass.k.gz', 70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7', 508372, '8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601', 7905),
 (120, 'elem_thick_to-renum.k.gz', 23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59', 232959541, '7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda', 4088491),
 (121, 'wtc7_global_8a_no-conn-matl.k.gz', 47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d', 333947423, '8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf', 7196443),
]
TARGET_PARTS = {820, 821, 859}
LINE_CAP, BYTE_CAP = 16384, 512 * 1024 * 1024
NUM = re.compile(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EDed][+-]?\d+|[+-]\d+)?\Z')
INTEGER = re.compile(r'[+-]?\d+\Z')
KINDS = {'*PART': 'part', '*SECTION_DISCRETE': 'section',
         '*MAT_SPRING_NONLINEAR_ELASTIC': 'material', '*DEFINE_CURVE': 'curve',
         '*DEFINE_SD_ORIENTATION': 'orientation'}


class SafeFailure(Exception):
    pass


def require(condition, code):
    if not condition:
        raise SafeFailure(code)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def pin(path, expected=None):
    result = {'path': str(path), 'bytes': Path(path).stat().st_size, 'sha256': sha(path)}
    require(expected is None or result['sha256'] == expected, 'PIN_MISMATCH')
    return result


def integer(value):
    require(value is not None and float(value).is_integer(), 'EXPECTED_INTEGER')
    return int(value)


def fields(raw, widths):
    """Keep nulls and validated numeric lexemes; support fixed and comma cards."""
    try:
        text = raw.decode('ascii').rstrip('\r\n')
    except UnicodeError:
        raise SafeFailure('NONASCII_NUMERIC_CARD') from None
    if ',' in text:
        items = text.split(',')
        require(len(items) <= len(widths), 'TOO_MANY_FREE_FIELDS')
        items += [''] * (len(widths) - len(items))
    else:
        require(not text[sum(widths):].strip(), 'NONBLANK_CARD_OVERFLOW')
        items, at = [], 0
        for width in widths:
            items.append(text[at:at + width])
            at += width
    tokens, values = [], []
    for item in items:
        token = item.strip()
        if not token:
            tokens.append(None)
            values.append(None)
            continue
        require(NUM.fullmatch(token) is not None, 'NONNUMERIC_CARD_FIELD')
        normalized = token.replace('D', 'E').replace('d', 'e')
        if 'e' not in normalized.lower():
            normalized = re.sub(r'(?<=[\d.])([+-]\d+)$', r'e\1', normalized)
        value = int(token) if INTEGER.fullmatch(token) else float(normalized)
        require(math.isfinite(value), 'NONFINITE_CARD_FIELD')
        tokens.append(token)
        values.append(value)
    return {'values': values, 'numeric_tokens': tokens}


def new_state(selection):
    return {'registries': {x: {} for x in KINDS.values()}, 'elements': [],
            'selected_part_elements': [], 'discrete_eids': set(), 'selected': selection,
            'discrete_counts': collections.Counter(), 'block_counts': collections.Counter(),
            'ignored_keyword_blocks': 0}


def store_block(state, block):
    if block is None or block['kind'] == 'element':
        return
    require(not block['title_pending'], 'MISSING_TITLE')
    require(block['cards'], 'EMPTY_ADMITTED_BLOCK')
    original_id = integer(block['cards'][0]['values'][0])
    effective_id = original_id + (1000 if block['source'] == 120 and block['kind'] in {'part', 'section', 'material'} else 0)
    block['original_id'], block['effective_id'] = original_id, effective_id
    kind = block['kind']
    if kind == 'curve':
        require(len(block['cards']) >= 2, 'CURVE_NO_POINTS')
        require(all(c['values'][0] is not None and c['values'][1] is not None for c in block['cards'][1:]), 'CURVE_BLANK_POINT')
    registry = state['registries'][kind]
    require(effective_id not in registry, 'DUPLICATE_' + kind.upper() + '_ID')
    block.pop('title_pending')
    registry[effective_id] = block


def parse_stream(stream, source, state):
    digest, size, line, current = hashlib.sha256(), 0, 0, None
    while True:
        raw = stream.readline(LINE_CAP + 1)
        if not raw:
            break
        line += 1
        require(len(raw) <= LINE_CAP, 'LINE_CAP')
        size += len(raw)
        require(size <= BYTE_CAP, 'BYTE_CAP')
        digest.update(raw)
        leading = raw.lstrip()
        if not leading.strip() or leading.startswith(b'$'):
            continue
        if leading.startswith(b'*'):
            store_block(state, current)
            current = None
            keyword = leading.split(None, 1)[0].rstrip(b'\r\n').upper().decode('ascii', errors='replace')
            base = keyword[:-6] if keyword.endswith('_TITLE') else keyword
            if base == '*ELEMENT_DISCRETE':
                require(keyword == base, 'UNSUPPORTED_DISCRETE_VARIANT')
                current = {'kind': 'element', 'keyword': keyword, 'source': source, 'keyword_line': line}
                state['block_counts']['element'] += 1
            elif base in KINDS:
                kind = KINDS[base]
                require(not (kind == 'part' and keyword != base), 'UNSUPPORTED_PART_VARIANT')
                current = {'kind': kind, 'keyword': keyword, 'source': source, 'keyword_line': line,
                           'title_pending': kind == 'part' or keyword.endswith('_TITLE'),
                           'title_sha256': None, 'title_line': None, 'cards': []}
                state['block_counts'][kind] += 1
            else:
                require(not any(keyword.startswith(k + '_') for k in KINDS if k != '*PART'), 'UNSUPPORTED_CHAIN_VARIANT')
                require(not keyword.startswith('*ELEMENT_DISCRETE_'), 'UNSUPPORTED_DISCRETE_VARIANT')
                state['ignored_keyword_blocks'] += 1
            continue
        if current is None:
            continue
        if current['kind'] == 'element':
            card = fields(raw, [8, 8, 8, 8, 8, 16, 8, 16])
            values = card['values']
            eid, original_pid = integer(values[0]), integer(values[1])
            pid = original_pid + (1000 if source == 120 else 0)
            require(eid not in state['discrete_eids'], 'DUPLICATE_DISCRETE_EID')
            state['discrete_eids'].add(eid)
            state['discrete_counts'][(source, original_pid, pid)] += 1
            if pid in TARGET_PARTS or eid in state['selected']:
                record = {'source': source, 'line': line, 'keyword_line': current['keyword_line'],
                          'keyword': current['keyword'], 'eid': eid, 'original_part': original_pid,
                          'effective_part': pid, **card}
                if pid in TARGET_PARTS:
                    state['selected_part_elements'].append(record)
                if eid in state['selected']:
                    wanted = state['selected'][eid]
                    require((source, line, original_pid, pid) == (wanted['source'], wanted['element_line'], wanted['original_part'], wanted['effective_part']), 'ELEMENT_LINEAGE_MISMATCH')
                    require(all(n in values[2:4] for n in wanted['matched_node_ids']), 'MATCHED_NODE_NOT_ENDPOINT')
                    state['elements'].append(record)
            continue
        if current['title_pending']:
            current['title_sha256'] = hashlib.sha256(raw).hexdigest()
            current['title_line'] = line
            current['title_pending'] = False
            continue
        widths = [20, 20] if current['kind'] == 'curve' and current['cards'] else [10] * 8
        card = fields(raw, widths)
        current['cards'].append({'line': line, 'ordinal': len(current['cards']) + 1, **card})
    store_block(state, current)
    return {'source': source, 'uncompressed_bytes': size, 'physical_lines': line,
            'uncompressed_sha256': digest.hexdigest(), 'eof': True}


def dependency(registry, identifier):
    if identifier is None:
        return {'status': 'blank', 'id': None, 'definition': None}
    number = integer(identifier)
    if number == 0:
        return {'status': 'explicit_zero', 'id': 0, 'definition': None}
    return {'status': 'supplied' if number in registry else 'not_in_admitted_registry',
            'id': number, 'definition': registry.get(number)}


def assemble(state):
    require(len(state['elements']) == len(state['selected']), 'SELECTED_COVERAGE')
    reg, chains = state['registries'], []
    for pid in sorted(TARGET_PARTS):
        part = reg['part'].get(pid)
        require(part is not None, 'SELECTED_PART_ABSENT')
        first = part['cards'][0]['values']
        shift = 1000 if part['source'] == 120 else 0
        sid, mid = integer(first[1]) + shift, integer(first[2]) + shift
        section, material = dependency(reg['section'], sid), dependency(reg['material'], mid)
        curves = []
        if material['status'] == 'supplied':
            for ordinal in (2, 3):
                curves.append({'material_card': 1, 'field_ordinal': ordinal,
                               **dependency(reg['curve'], material['definition']['cards'][0]['values'][ordinal - 1])})
        selected = [x for x in state['elements'] if x['effective_part'] == pid]
        full = [x for x in state['selected_part_elements'] if x['effective_part'] == pid]
        orientations = [dependency(reg['orientation'], n) for n in sorted({integer(x['values'][4]) for x in selected if x['values'][4] is not None})]
        chains.append({'effective_part': pid, 'part': part,
                       'section_reference': {'original': first[1], 'effective': sid, **section},
                       'material_reference': {'original': first[2], 'effective': mid, **material},
                       'curve_references': curves, 'orientation_references': orientations,
                       'selected_element_count': len(selected), 'full_part_element_count': len(full),
                       'full_part_membership': [{k: x[k] for k in ['source', 'line', 'eid', 'original_part', 'effective_part']} for x in full],
                       'selected_elements': sorted(selected, key=lambda x: (x['source'], x['line']))})
    return {'selected_count': len(state['elements']), 'selected_part_chains': chains,
            'selection_lineage': [state['selected'][k] for k in sorted(state['selected'])],
            'internal_inventory_counts': {'discrete_elements': len(state['discrete_eids']),
                                          'registry_counts': {k: len(v) for k, v in reg.items()},
                                          'admitted_keyword_blocks': dict(state['block_counts']),
                                          'ignored_keyword_blocks': state['ignored_keyword_blocks']},
            'scope': 'Numeric source-card extraction only; no law evaluation, units, physical identity, activation or historical execution finding.'}


def create_only(path, obj):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(obj, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')


def fixture_card(values, widths):
    return (''.join(('' if x is None else str(x)).rjust(w) for x, w in zip(values, widths)) + '\n').encode()


def synthetic_tests():
    passed = []
    def test(name, fn):
        fn()
        passed.append(name)
    def expect(code, fn):
        try:
            fn()
        except SafeFailure as error:
            require(str(error) == code, 'WRONG_SYNTHETIC_FAILURE')
        else:
            raise SafeFailure('MISSING_SYNTHETIC_FAILURE')
    def blanks():
        a = fields(fixture_card([1, None, 0, '0.', None, '1D-3', None, '-2.5-2'], [10] * 8), [10] * 8)
        require(a['values'] == [1, None, 0, 0.0, None, .001, None, -.025], 'BLANK_TEST')
        require(a['numeric_tokens'][2:4] == ['0', '0.'], 'LEXEME_TEST')
        require(fields(b'1,,0,0.,,1D-3,,-2.5-2\n', [10] * 8) == a, 'COMMA_TEST')
    test('fixed_comma_blanks_zeros_and_numeric_lexemes', blanks)
    test('nonnumeric_payload_rejected_without_echo', lambda: expect('NONNUMERIC_CARD_FIELD', lambda: fields(b'not data', [10] * 8)))
    test('nonblank_overflow_rejected', lambda: expect('NONBLANK_CARD_OVERFLOW', lambda: fields(b'1         2', [10])))
    def basic(order='forward', duplicate=False, source=121):
        part = b'*PART\nprivate synthetic title\n' + fixture_card([820, 820, 820, 0, 0, 0, None, None], [10] * 8)
        section = b'*SECTION_DISCRETE\n' + fixture_card([820, 0, None, 1, 0, 0, None, None], [10] * 8) + fixture_card([None, 0, None, None, None, None, None, None], [10] * 8)
        material = b'*MAT_SPRING_NONLINEAR_ELASTIC\n' + fixture_card([820, 42, 0, None, None, None, None, None], [10] * 8)
        curve = b'*DEFINE_CURVE_TITLE\nhash this title only\n' + fixture_card([42, 0, 1, 1, 0, 0, 0, None], [10] * 8) + fixture_card([0, 0], [20, 20]) + fixture_card([1, 2], [20, 20])
        payload = part + section + (material + curve if order == 'forward' else curve + material) + (curve if duplicate else b'')
        state = new_state({})
        receipt = parse_stream(io.BytesIO(payload), source, state)
        require(receipt['eof'] and receipt['uncompressed_bytes'] == len(payload) and receipt['uncompressed_sha256'] == hashlib.sha256(payload).hexdigest(), 'EOF_TEST')
        return state
    def forward():
        a, b = basic(), basic('reverse')
        require(a['registries']['curve'][42]['cards'][1]['values'] == b['registries']['curve'][42]['cards'][1]['values'], 'FORWARD_REFERENCE_TEST')
        require(dependency(a['registries']['curve'], 42)['status'] == 'supplied', 'CURVE_REFERENCE_TEST')
        require(dependency(a['registries']['curve'], 99)['status'] == 'not_in_admitted_registry', 'MISSING_CURVE_TEST')
        require(dependency(a['registries']['curve'], 0)['status'] == 'explicit_zero' and dependency(a['registries']['curve'], None)['status'] == 'blank', 'ZERO_BLANK_REFERENCE_TEST')
        require(a['registries']['part'][820]['title_sha256'] == hashlib.sha256(b'private synthetic title\n').hexdigest(), 'TITLE_HASH_TEST')
    test('forward_backward_missing_zero_blank_curves_title_hash_eof', forward)
    test('duplicate_curve_rejected', lambda: expect('DUPLICATE_CURVE_ID', lambda: basic(duplicate=True)))
    def transform():
        a = basic(source=120)
        require(1820 in a['registries']['part'] and 1820 in a['registries']['material'] and 1820 in a['registries']['section'], 'NAMESPACE_TRANSFORM_TEST')
        require(42 in a['registries']['curve'] and 1042 not in a['registries']['curve'], 'CURVE_NOT_TRANSFORMED_TEST')
    test('part_material_section_only_transform', transform)
    def element_test(bad=False, duplicate=False):
        selection = {7: {'source': 121, 'element_line': 2, 'original_part': 820, 'effective_part': 820, 'matched_node_ids': [22 if not bad else 99]}}
        raw = b'*ELEMENT_DISCRETE\n' + fixture_card([7, 820, 22, 0, 99, '1.25', 0, None], [8, 8, 8, 8, 8, 16, 8, 16])
        if duplicate:
            raw += raw.splitlines(keepends=True)[1]
        s = new_state(selection)
        parse_stream(io.BytesIO(raw), 121, s)
        require(s['elements'][0]['values'] == [7, 820, 22, 0, 99, 1.25, 0, None], 'DISCRETE_MIXED_WIDTH_TEST')
    test('mixed_width_element_lineage_ground_zero_and_orientation', element_test)
    test('orientation_only_not_endpoint', lambda: expect('MATCHED_NODE_NOT_ENDPOINT', lambda: element_test(bad=True)))
    test('duplicate_discrete_eid_rejected', lambda: expect('DUPLICATE_DISCRETE_EID', lambda: element_test(duplicate=True)))
    test('unsupported_curve_variant_rejected', lambda: expect('UNSUPPORTED_CHAIN_VARIANT', lambda: parse_stream(io.BytesIO(b'*DEFINE_CURVE_UNKNOWN\n'), 121, new_state({}))))
    test('line_cap_rejected', lambda: expect('LINE_CAP', lambda: parse_stream(io.BytesIO(b' ' * (LINE_CAP + 1)), 121, new_state({}))))
    def creation():
        with tempfile.TemporaryDirectory(prefix='independent-springs-control-', dir='/private/tmp') as folder:
            path = Path(folder) / 'control.json'
            create_only(path, {'n': 1})
            try:
                create_only(path, {'n': 2})
            except FileExistsError:
                pass
            else:
                raise SafeFailure('CREATE_ONLY_TEST')
            require(json.loads(path.read_text()) == {'n': 1}, 'OVERWRITE_TEST')
            expect('PIN_MISMATCH', lambda: pin(path, '0' * 64))
    test('create_only_and_changed_pin_rejected', creation)
    return {'status': 'passed', 'count': len(passed), 'groups': passed}


def load_selection():
    pin(SELECTION, SELECTION_SHA)
    selected = {}
    for row in json.loads(SELECTION.read_bytes())['result']['matches']:
        if row['actual_family'] != 'discrete' or row['effective_part'] not in TARGET_PARTS:
            continue
        eid = row['eid']
        identity = {k: row[k] for k in ['source', 'element_line', 'eid', 'original_part', 'effective_part']}
        if eid not in selected:
            selected[eid] = {**identity, 'matched_node_ids': [], 'match_rows': []}
        require(all(selected[eid][k] == v for k, v in identity.items()), 'SELECTION_ID_COLLISION')
        selected[eid]['matched_node_ids'] = sorted(set(selected[eid]['matched_node_ids']) | set(row['matched_node_ids']))
        selected[eid]['match_rows'].append({k: row[k] for k in ['cid', 'e', 'geometry_class', 'set_id', 'setting_index', 'list_source', 'list_header_line', 'list_membership_ordinals', 'matched_node_ids', 'contact_relations']})
    require(len(selected) == 17, 'SELECTION_EXPECTATION_CHANGED')
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    require(args.output.resolve().parent == UNIT and args.output.name.startswith('independent-springs') and args.output.suffix == '.json', 'OUTPUT_SCOPE')
    require(not args.output.exists(), 'OUTPUT_EXISTS')
    started = time.monotonic()
    report = {'command': sys.argv, 'code_sha256': sha(__file__), 'status': 'running'}
    try:
        report['controls'] = synthetic_tests()
        if not args.controls_only:
            report['pins_before'] = {'protocol': pin(UNIT / 'PROTOCOL.md', PROTOCOL_SHA), 'selection': pin(SELECTION, SELECTION_SHA)}
            state = new_state(load_selection())
            receipts = []
            for source, name, compressed_size, compressed_sha, raw_size, raw_sha, lines in SOURCES:
                path = RAW / name
                before = pin(path, compressed_sha)
                require(before['bytes'] == compressed_size, 'COMPRESSED_SIZE_MISMATCH')
                with gzip.open(path, 'rb') as stream:
                    receipt = parse_stream(stream, source, state)
                require(receipt['uncompressed_bytes'] == raw_size and receipt['uncompressed_sha256'] == raw_sha and receipt['physical_lines'] == lines, 'FULL_STREAM_PIN_MISMATCH')
                receipt['compressed_before'] = before
                receipt['compressed_after'] = pin(path, compressed_sha)
                receipts.append(receipt)
            report['source_receipts'] = receipts
            report['result'] = assemble(state)
            report['pins_after'] = {'protocol': pin(UNIT / 'PROTOCOL.md', PROTOCOL_SHA), 'selection': pin(SELECTION, SELECTION_SHA)}
        report['status'] = 'passed'
    except Exception as error:
        report['status'] = 'failed'
        report['failure_code'] = str(error) if isinstance(error, SafeFailure) else type(error).__name__
    report['elapsed_seconds'] = time.monotonic() - started
    report['peak_rss_bytes_macos'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report['limits'] = {'line_bytes': LINE_CAP, 'uncompressed_bytes_per_source': BYTE_CAP, 'truncate': False}
    create_only(args.output, report)
    print(json.dumps({'status': report['status'], 'output': str(args.output), 'sha256': sha(args.output), 'failure_code': report.get('failure_code'), 'elapsed_seconds': report['elapsed_seconds']}))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'status': 'failed_before_receipt', 'failure_code': str(error) if isinstance(error, SafeFailure) else type(error).__name__}))
        sys.exit(1)
