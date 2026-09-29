#!/usr/bin/env python3
"""Bounded independent definition-family/curve pass; source text is never run."""
import argparse
import collections
import gzip
import hashlib
import io
import json
from pathlib import Path
import resource
import sys
import time

import independent_springs as own

OWN_SHA = 'e816725d3cbd6bf919dac8809559d993c3b89551b8f70165dd48d536468432ca'
UNIT = Path(__file__).resolve().parent
FAMILIES = ['CURVE', 'TABLE', 'FUNCTION']
KNOWN = {b'*DEFINE_' + x.encode() + suffix for x in FAMILIES for suffix in (b'', b'_TITLE')}
KNOWN |= {b'*DEFINE_CURVE_3858', b'*DEFINE_CURVE_5434A', b'*DEFINE_CURVE_FUNCTION'}


def new_state():
    return {'family_counts': {x: 0 for x in FAMILIES}, 'variants': collections.Counter(),
            'blocks': [], 'curves': {}, 'keyword_blocks': 0, 'alternatives': []}


def finish(state, block):
    if block is None:
        return
    block['payload_sha256'] = block.pop('payload_digest').hexdigest()
    own.require(not block.pop('title_pending'), 'UNFINISHED_DEFINITION_TITLE')
    if block['parsed_as'] == 'base_curve':
        own.require(len(block['cards']) >= 2, 'CURVE_NO_POINTS')
        identifier = own.integer(block['cards'][0]['values'][0])
        own.require(identifier not in state['curves'], 'DUPLICATE_CURVE_ID')
        block['original_id'] = block['effective_id'] = identifier
        block['header_line'] = block['cards'][0]['line']
        own.require(all(all(v is not None for v in c['values']) for c in block['cards'][1:]), 'CURVE_BLANK_POINT')
        state['curves'][identifier] = block
    else:
        state['alternatives'].append(block)
    state['blocks'].append({k: block[k] for k in ['source', 'keyword_line', 'family', 'keyword', 'keyword_sha256', 'parsed_as', 'payload_line_count', 'payload_sha256']})


def scan(stream, source, state):
    digest, size, line, current = hashlib.sha256(), 0, 0, None
    counts = {x: 0 for x in FAMILIES}
    while True:
        raw = stream.readline(own.LINE_CAP + 1)
        if not raw:
            break
        line += 1
        own.require(len(raw) <= own.LINE_CAP, 'LINE_CAP')
        size += len(raw)
        own.require(size <= own.BYTE_CAP, 'BYTE_CAP')
        digest.update(raw)
        head = raw.lstrip()
        if head.startswith(b'*'):
            finish(state, current)
            current = None
            state['keyword_blocks'] += 1
            token = head.split(None, 1)[0].upper()
            matched = [x for x in FAMILIES if token.startswith(b'*DEFINE_' + x.encode())]
            if not matched:
                continue
            own.require(len(matched) == 1, 'FAMILY_AMBIGUOUS')
            family = matched[0]
            counts[family] += 1
            state['family_counts'][family] += 1
            token_sha = hashlib.sha256(token).hexdigest()
            keyword = token.decode('ascii') if token in KNOWN else None
            state['variants'][(family, keyword or 'unreviewed:' + token_sha)] += 1
            base_curve = token in {b'*DEFINE_CURVE', b'*DEFINE_CURVE_TITLE'}
            current = {'source': source, 'keyword_line': line, 'family': family,
                       'keyword': keyword, 'keyword_sha256': token_sha,
                       'parsed_as': 'base_curve' if base_curve else 'header_presence_only',
                       'title_pending': token.endswith(b'_TITLE'), 'title_sha256': None,
                       'title_line': None, 'cards': [], 'payload_digest': hashlib.sha256(),
                       'payload_line_count': 0, 'header_candidate': None}
            continue
        if current is None:
            continue
        current['payload_digest'].update(raw)
        current['payload_line_count'] += 1
        if not head.strip() or head.startswith(b'$'):
            continue
        if current['title_pending']:
            current['title_sha256'] = hashlib.sha256(raw).hexdigest()
            current['title_line'] = line
            current['title_pending'] = False
        elif current['parsed_as'] == 'base_curve':
            widths = [20, 20] if current['cards'] else [10] * 8
            card = own.fields(raw, widths)
            current['cards'].append({'line': line, 'ordinal': len(current['cards']) + 1, **card})
        elif current['header_candidate'] is None:
            # No expression/name export and no invented syntax. Only a numeric
            # leading token is retained, explicitly as an uninterpreted candidate.
            first = raw.split(b',', 1)[0] if b',' in raw else raw[:10]
            try:
                value = own.fields(first, [max(10, len(first))])
                number = own.integer(value['values'][0])
                current['header_candidate'] = {'line': line, 'status': 'numeric_leading_field_only', 'value': number}
            except own.SafeFailure:
                current['header_candidate'] = {'line': line, 'status': 'uninterpreted_non_numeric_or_blank', 'value': None}
    finish(state, current)
    return {'source': source, 'uncompressed_bytes': size, 'physical_lines': line,
            'uncompressed_sha256': digest.hexdigest(), 'eof': True, 'family_counts': counts}


def controls():
    names = []
    curve = b'*DEFINE_CURVE_TITLE\nprivate test title\n' + own.fixture_card([42, 0, 1, 1, 0, 0, 0, None], [10] * 8) + own.fixture_card([0, 0], [20, 20]) + own.fixture_card([1, 2], [20, 20])
    state = new_state()
    data = b'$ *DEFINE_TABLE\n*KEYWORD\n' + curve + b'*END\n'
    receipt = scan(io.BytesIO(data), 121, state)
    own.require(state['family_counts'] == {'CURVE': 1, 'TABLE': 0, 'FUNCTION': 0}, 'FAMILY_COUNTS_CONTROL')
    own.require(receipt['eof'] and receipt['uncompressed_sha256'] == hashlib.sha256(data).hexdigest() and receipt['physical_lines'] == len(data.splitlines()), 'EOF_CONTROL')
    own.require(state['curves'][42]['title_sha256'] == hashlib.sha256(b'private test title\n').hexdigest(), 'TITLE_CONTROL')
    own.require(state['curves'][42]['cards'][0]['values'][-1] is None, 'BLANK_CONTROL')
    names.append('comments_titles_nulls_base_curve_and_complete_eof')
    state = new_state()
    data = b'*DEFINE_TABLE\n' + own.fixture_card([602], [10]) + b'*DEFINE_FUNCTION\nexpression must not be exported\n*DEFINE_CURVE_FUNCTION\n' + own.fixture_card([803], [10]) + b'*DEFINE_CURVE_PRIVATE_VARIANT\nprivate payload\n'
    scan(io.BytesIO(data), 120, state)
    own.require(state['family_counts'] == {'CURVE': 2, 'TABLE': 1, 'FUNCTION': 1}, 'ALTERNATIVE_COUNTS_CONTROL')
    own.require(state['alternatives'][0]['header_candidate']['value'] == 602 and state['alternatives'][2]['header_candidate']['value'] == 803, 'HEADER_CONTROL')
    own.require(state['alternatives'][3]['keyword'] is None, 'UNKNOWN_KEYWORD_HASH_CONTROL')
    encoded = json.dumps(state['alternatives'])
    own.require('expression must' not in encoded and 'private payload' not in encoded and 'PRIVATE_VARIANT' not in encoded, 'NO_TEXT_EXPORT_CONTROL')
    names.append('all_families_variants_unshifted_numeric_headers_and_hash_only_unknowns')
    try:
        scan(io.BytesIO(curve + curve), 121, new_state())
    except own.SafeFailure as error:
        own.require(str(error) == 'DUPLICATE_CURVE_ID', 'DUPLICATE_CONTROL')
    else:
        raise own.SafeFailure('DUPLICATE_NOT_CAUGHT')
    names.append('duplicate_curve_rejected')
    try:
        scan(io.BytesIO(b'x' * (own.LINE_CAP + 1)), 121, new_state())
    except own.SafeFailure as error:
        own.require(str(error) == 'LINE_CAP', 'LINE_CAP_CONTROL')
    else:
        raise own.SafeFailure('LINE_CAP_NOT_CAUGHT')
    names.append('line_cap_rejected')
    return {'status': 'passed', 'groups': names, 'count': len(names), 'shared_numeric_controls': own.synthetic_tests()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    own.require(args.output.resolve().parent == UNIT and args.output.name.startswith('independent-definition-presence') and args.output.suffix == '.json', 'OUTPUT_SCOPE')
    own.require(not args.output.exists(), 'OUTPUT_EXISTS')
    began = time.monotonic()
    report = {'command': sys.argv, 'code_sha256': own.sha(__file__), 'status': 'running'}
    try:
        report['dependencies_before'] = {'own_numeric_helper': own.pin(own.__file__, OWN_SHA), 'protocol': own.pin(UNIT / 'PROTOCOL.md', own.PROTOCOL_SHA)}
        report['controls'] = controls()
        if not args.controls_only:
            state, receipts = new_state(), []
            for source, name, compressed_size, compressed_sha, raw_size, raw_sha, lines in own.SOURCES:
                path = own.RAW / name
                before = own.pin(path, compressed_sha)
                own.require(before['bytes'] == compressed_size, 'COMPRESSED_SIZE_MISMATCH')
                with gzip.open(path, 'rb') as stream:
                    receipt = scan(stream, source, state)
                own.require((receipt['uncompressed_bytes'], receipt['uncompressed_sha256'], receipt['physical_lines']) == (raw_size, raw_sha, lines), 'FULL_STREAM_PIN_MISMATCH')
                receipt['compressed_before'], receipt['compressed_after'] = before, own.pin(path, compressed_sha)
                receipts.append(receipt)
            report['source_receipts'] = receipts
            report['result'] = {'family_counts': state['family_counts'],
                                'variants': [{'family': a, 'keyword_or_hash': b, 'count': n} for (a, b), n in sorted(state['variants'].items())],
                                'all_keyword_blocks': state['keyword_blocks'], 'family_block_locators': state['blocks'],
                                'all_base_curves': [state['curves'][k] for k in sorted(state['curves'])],
                                'alternative_definition_blocks': state['alternatives'],
                                'further_syntax_review_required': bool(state['alternatives']),
                                'selected_reference_presence': [{'id': k, 'base_curve_supplied': k in state['curves']} for k in [602, 803]],
                                'scope': 'Complete admitted-file keyword/header inventory and base-curve numeric data; no source execution, alternative semantics, curve evaluation or historical-run inference.'}
        report['dependencies_after'] = {'own_numeric_helper': own.pin(own.__file__, OWN_SHA), 'protocol': own.pin(UNIT / 'PROTOCOL.md', own.PROTOCOL_SHA)}
        report['status'] = 'passed'
    except Exception as error:
        report['status'] = 'failed'
        report['failure_code'] = str(error) if isinstance(error, own.SafeFailure) else type(error).__name__
    report['elapsed_seconds'] = time.monotonic() - began
    report['peak_rss_bytes_macos'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    own.create_only(args.output, report)
    print(json.dumps({'status': report['status'], 'output': str(args.output), 'sha256': own.sha(args.output), 'failure_code': report.get('failure_code')}))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'status': 'failed_before_receipt', 'failure_code': str(error) if isinstance(error, own.SafeFailure) else type(error).__name__}))
        sys.exit(1)
