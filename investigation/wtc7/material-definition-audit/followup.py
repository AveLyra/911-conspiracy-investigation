#!/usr/bin/env python3
"""Five fixed fields; no source execution or expression evaluation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
PRIOR_SHA = '16f87f8e123a2f8a702f68985ce206660282c942479a662d9ca70c8b77e7f12a'
HEX = re.compile(r'[0-9a-f]{64}\Z')
UNSIGNED_NUMBER = r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[EeDd][+-]?[0-9]+)?'
NUMBER = re.compile(r'[+-]?' + UNSIGNED_NUMBER + r'\Z')
IDENTIFIER = re.compile(r'[A-Za-z_][A-Za-z0-9_]{0,31}\Z')
LEX = re.compile(r'(?P<number>' + UNSIGNED_NUMBER + r')|(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)|(?P<operator>\*\*|[+*/()\-])')
ELEMENT = re.compile(r'[A-Za-z]+[0-9]+\Z')


class Refused(Exception):
    def __init__(self, code):
        self.code = code


def require(ok, code):
    if not ok:
        raise Refused(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pinned(name, expected):
    path = HERE / name
    require(not path.is_symlink() and path.is_file(), 'control_type')
    data = path.read_bytes()
    require(sha(data) == expected, 'control_pin')
    return data


def prior_module():
    pinned('parse_material.py', PRIOR_SHA)
    spec = importlib.util.spec_from_file_location('material_prior_followup', HERE / 'parse_material.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def element_shape(text, names):
    value = text.strip()
    if len(value) <= 64 and ELEMENT.fullmatch(value) and value.upper() in names:
        return {'classification': 'official_name_match', 'name': value.upper()}
    return {'classification': 'unresolved'}


def density_shape(text):
    value = text.strip()
    if not value:
        return 'blank'
    if len(value) > 256:
        return 'over_cap'
    if "'" in value or '"' in value:
        return 'quote_bearing'
    if len(value) <= 64 and NUMBER.fullmatch(value):
        return 'numeric_literal'
    if IDENTIFIER.fullmatch(value):
        return 'identifier'
    cursor, count, depth = 0, 0, 0
    operand, has_identifier = True, False
    while cursor < len(value):
        if value[cursor] in ' \t\r\n':
            cursor += 1
            continue
        match = LEX.match(value, cursor)
        if not match:
            return 'unsupported'
        token, kind = match[0], match.lastgroup
        cursor, count = match.end(), count + 1
        if count > 128:
            return 'unsupported'
        if kind == 'number' and len(token) > 64:
            return 'unsupported'
        if kind == 'identifier' and len(token) > 32:
            return 'unsupported'
        if operand:
            if token in ('+', '-'):
                continue
            if token == '(':
                depth += 1
                if depth > 16:
                    return 'unsupported'
            elif kind in ('number', 'identifier'):
                operand = False
                has_identifier = has_identifier or kind == 'identifier'
            else:
                return 'unsupported'
        elif token == ')':
            if depth == 0:
                return 'unsupported'
            depth -= 1
        elif kind == 'operator' and token in ('+', '-', '*', '/', '**'):
            operand = True
        else:
            return 'unsupported'
    if operand or depth:
        return 'unsupported'
    return 'identifier_arithmetic' if has_identifier else 'numeric_arithmetic'


def extract(data, targets, names, prior, lexer):
    require(len(data) <= prior.CAP and b'\0' not in data, 'source_shape')
    lines = data.split(b'\n')
    if data.endswith(b'\n'):
        lines.pop()
    require(all(len(raw) + 1 <= prior.LINE_CAP for raw in lines), 'line_cap')
    rows = []
    for target in targets:
        line = target['line']
        require(1 <= line <= len(lines), 'target_line')
        raw = lines[line - 1]
        parts, _, unclosed = lexer.split_line(raw.rstrip(b'\r').decode('latin1'))
        require(not unclosed and 1 <= target['segment'] <= len(parts), 'segment_shape')
        segment = parts[target['segment'] - 1].strip()
        require(sha(segment.encode('latin1')) == target['segment_sha256'], 'segment_pin')
        fields, unclosed = prior.comma_fields(segment)
        require(not unclosed and len(fields) - 1 == target['argument_count'], 'field_count')
        require(fields[0].strip().upper() == target['command'], 'command')
        if target['command'] == 'ET':
            require(target['field_index'] == 2 and target['role'] == 'ENAME', 'target_role')
            require(fields[1].strip() == target['local_or_material_id'], 'type_id')
        elif target['command'] == 'MP':
            require(target['field_index'] == 3 and target['role'] == 'C0', 'target_role')
            require(fields[1].strip().upper() == 'DENS', 'property')
            require(fields[2].strip() == target['local_or_material_id'], 'material_id')
        else:
            raise Refused('command')
        value = fields[target['field_index']].strip()
        require(sha(value.encode('utf8')) == target['field_sha256'], 'field_pin')
        result = element_shape(value, names) if target['command'] == 'ET' else {'classification': density_shape(value)}
        rows.append({**target, **result})
    return rows


def output_path(name):
    require(bool(re.fullmatch(r'followup-producer-run[0-9]{2}\.json', name)), 'output_name')
    path = HERE / name
    require(not path.exists() and not path.is_symlink(), 'output_exists')
    return path


def run(args):
    require(len(args) == 5 and all(HEX.fullmatch(v) for v in args[1:]), 'arguments')
    name, protocol_pin, target_pin, allowlist_pin, code_pin = args
    output = output_path(name)
    controls = {'FOLLOWUP-PROTOCOL.md': protocol_pin, 'followup-targets.json': target_pin,
                'element-allowlist.json': allowlist_pin, 'followup.py': code_pin}
    receipt = {'schema': 'five-field-followup-v1', 'implementation': 'producer',
               'source_alias': 'APDL01', 'pins': controls, 'prior_sha256': PRIOR_SHA,
               'python': sys.version.split()[0]}
    try:
        initial = {key: pinned(key, value) for key, value in controls.items()}
        targets = json.loads(initial['followup-targets.json'])
        require([(r['line'], r['segment']) for r in targets] == [(27,1),(46,1),(281,1),(2453,1),(2654,1)], 'target_scope')
        name_list = json.loads(initial['element-allowlist.json'])['names']
        require(type(name_list) is list and name_list == sorted(set(name_list)), 'allowlist')
        require(all(type(n) is str and ELEMENT.fullmatch(n) and n == n.upper() for n in name_list), 'allowlist')
        prior = prior_module()
        lexer = prior.load_lexer()
        _, _, data = prior.read_candidate(lexer)
        require(len(data.split(b'\n')) == prior.SOURCE_LINES and not data.endswith(b'\n'), 'source_lines')
        rows = extract(data, targets, set(name_list), prior, lexer)
        prior.read_candidate(lexer)
        pinned('parse_material.py', PRIOR_SHA)
        require(sha(prior.LEXER.read_bytes()) == prior.LEXER_SHA, 'lexer_pin_after')
        for key, value in controls.items():
            pinned(key, value)
        receipt.update(status='PASS', source_sha256=prior.SOURCE_SHA, manifest_sha256=lexer.MANIFEST_SHA,
                       lexer_sha256=prior.LEXER_SHA, source_bytes=len(data), source_records=prior.SOURCE_LINES, rows=rows)
    except Exception as error:
        receipt.update(status='FAIL', code=error.code if isinstance(error, Refused) else 'dependency_or_unexpected')
    payload = json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=True) + '\n'
    with output.open('x') as stream:
        stream.write(payload)
    print(json.dumps({'status': receipt['status'], 'output': output.name}))
    return 0 if receipt['status'] == 'PASS' else 1


def main():
    try:
        return run(sys.argv[1:])
    except Exception as error:
        print(json.dumps({'status': 'REFUSED', 'code': error.code if isinstance(error, Refused) else 'output_error'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
