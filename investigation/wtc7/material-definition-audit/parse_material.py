#!/usr/bin/env python3
"""Minimized literal APDL field audit; no source commands are executed."""
import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys

HERE = Path(__file__).resolve().parent
LEXER = HERE.parent / 'thermal-transfer-crosswalk/scan_transfer.py'
LEXER_SHA = 'c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53'
SOURCE_SHA = 'e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64'
NAME_SHA = 'ff5c9a2bc8d8822fa9e3a1acaeb1becbab49aa2d5675c12f98b44261c1e00135'
SOURCE_SIZE = 212384
SOURCE_LINES = 5474
CAP = 4 * 1024**2
LINE_CAP = 16384
ROW_CAP = 10000
SELECTED = frozenset('MP MPDATA MPTEMP TB TBTEMP TBDATA ET'.split())
PROPS = frozenset('C ENTH DENS KXX KYY KZZ EX EY EZ GXY GYZ GXZ PRXY PRYZ PRXZ NUXY NUYZ NUXZ ALPX ALPY ALPZ CTEX CTEY CTEZ THSX THSY THSZ REFT EMIS HF QRATE ALPD BETD DMPR DMPS MU'.split())
TABLES = frozenset('BISO BKIN MISO MKIN KINH PLASTIC ELASTIC MELAS CONCR CREEP DENS CTE THERM USER STATE COND ENTH SPHT FLSPHT LINEAR NONLINEAR'.split())
NUM = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[EeDd][+-]?[0-9]+)?\Z')
INTEGER = re.compile(r'[0-9]+\Z')
TOKEN = re.compile(r'^([*/]?[A-Za-z][A-Za-z0-9_]*)\s*(?=,|$|\s)')
SCHEMAS = {
    'MP': [('label','property'),('material','integer')] + [(f'c{i}','number') for i in range(5)],
    'MPDATA': [('label','property'),('material','integer'),('start','integer')] + [(f'c{i}','number') for i in range(1,7)],
    'MPTEMP': [('start','integer')] + [(f't{i}','number') for i in range(1,7)],
    'TB': [('label','table'),('material','integer'),('ntemp','integer'),('npts','integer'),('option','option'),('unused','blank'),('function','blank')],
    'TBTEMP': [('temperature','number'),('kmod','integer')],
    'TBDATA': [('start','integer')] + [(f'c{i}','number') for i in range(1,7)],
    'ET': [('local_type','integer'),('library_code','integer')] + [(f'kop{i}','integer') for i in range(1,7)] + [('inopr','integer')],
}


class Refused(Exception):
    def __init__(self, code):
        self.code = code


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise Refused('cli_arguments')


def require(ok, code):
    if not ok:
        raise Refused(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_lexer():
    require(not LEXER.is_symlink() and sha(LEXER.read_bytes()) == LEXER_SHA, 'lexer_pin')
    spec = importlib.util.spec_from_file_location('pinned_material_lexer', LEXER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scalar(raw, kind):
    """Never return arbitrary strings; preserve blanks and numeric lexemes."""
    value = raw.strip()
    if not value:
        return {'kind':'blank'}
    if kind == 'property' and value.upper() in PROPS:
        return {'kind':'label','value':value.upper()}
    if kind in ('table','option') and value.upper() in TABLES:
        return {'kind':'label','value':value.upper()}
    if kind in ('integer','option') and len(value) <= 64 and INTEGER.fullmatch(value):
        return {'kind':'integer','lexeme':value}
    if kind == 'number' and len(value) <= 64 and NUM.fullmatch(value):
        return {'kind':'number','lexeme':value}
    return {'kind':'unresolved','sha256':sha(value.encode('utf-8'))}


def comma_fields(text):
    """Preserve quoted commas/doubled quotes without interpreting their values."""
    fields, start, quote, i = [], 0, None, 0
    while i < len(text):
        char = text[i]
        if quote:
            if char == quote:
                if i + 1 < len(text) and text[i + 1] == quote:
                    i += 2
                    continue
                quote = None
        elif char in "\"'":
            quote = char
        elif char == ',':
            fields.append(text[start:i])
            start = i + 1
        i += 1
    fields.append(text[start:])
    return fields, quote is not None


def parse_row(command, text, line, segment, unclosed=False):
    out = {'line':line,'segment':segment,'command':command,
           'segment_sha256':sha(text.encode('latin-1')),'fields':[]}
    parts, unclosed_field = comma_fields(text)
    if parts[0].strip().upper() != command:
        out['status'] = 'unsupported_command_form'
        return out
    args = parts[1:]
    out['argument_count'] = len(args)
    if not args and command != 'MPTEMP':
        out['status'] = 'missing_arguments'
        return out
    if unclosed or unclosed_field:
        out['status'] = 'unclosed_quote'
        return out
    if command in ('MPDATA','MPTEMP') and args and args[0].strip().upper() == 'UNBL':
        out['status'] = 'unresolved_coded_database'
        return out
    schema = SCHEMAS[command]
    extra = args[len(schema):]
    if any(v.strip() for v in extra):
        out['status'] = 'extra_nonblank_arguments'
        return out
    out['trailing_extra_blanks'] = len(extra)
    supplied = args[:len(schema)]
    supplied += [''] * (len(schema)-len(supplied))
    for (role,kind),raw in zip(schema,supplied):
        out['fields'].append({'role':role,**scalar(raw,kind)})
    out['status'] = 'unresolved_fields' if any(f['kind']=='unresolved' for f in out['fields']) else 'literal_fields'
    # Blanks are literal observations, not resolved defaults or active values.
    return out


def scan(data, lexer):
    require(len(data)<=CAP, 'source_cap')
    require(b'\0' not in data, 'nul_bytes')
    lines = data.split(b'\n')
    if data.endswith(b'\n'):
        lines.pop()
    if not data:
        lines = []
    require(all(len(line)+1<=LINE_CAP for line in lines), 'line_cap')
    known = lexer.VOCAB | SELECTED | set('MPREAD MPTGEN MPDRES MPCOPY MPDELE TBMODIF TBFIELD TBPT'.split())
    commands, unknown, kinds, flags = Counter(),Counter(),Counter(),Counter()
    rows = []
    expect_format = False
    for line_number,raw in enumerate(lines,1):
        text = raw.rstrip(b'\r').decode('latin-1')
        parts,comment,unclosed = lexer.split_line(text)
        if unclosed:
            flags['unclosed_quote_lines'] += 1
        if comment:
            kinds['comment_lines'] += 1
        if expect_format:
            kinds['format_records'] += 1
            if not text.strip() or text.lstrip().startswith(('!','*','/')):
                flags['unexpected_format_start'] += 1
            expect_format = False
            continue
        for seg_number,part in enumerate(parts,1):
            s = part.strip()
            if not s:
                continue
            m = TOKEN.match(s)
            if not m:
                kinds['noncommand_segments'] += 1
                continue
            command = m[1].upper()
            if command in known:
                commands[command] += 1
            else:
                unknown[sha(command.encode('ascii'))] += 1
            if command in SELECTED:
                rows.append(parse_row(command,s,line_number,seg_number,unclosed))
                require(len(rows)<=ROW_CAP, 'row_cap')
            if command in lexer.FORMAT_COMMANDS:
                expect_format = True
    if expect_format:
        flags['missing_format_eof'] += 1
    return {'source_sha256':sha(data),'bytes':len(data),'lines':len(lines),
            'commands':dict(sorted(commands.items())), 'unknown_command_hashes':dict(sorted(unknown.items())),
            'line_kinds':dict(sorted(kinds.items())), 'lexical_flags':dict(sorted(flags.items())),
            'rows':rows,'selected_statuses':dict(sorted(Counter(r['status'] for r in rows).items()))}


def read_candidate(lexer):
    manifest = lexer.MANIFEST
    require(not manifest.is_symlink(), 'manifest_symlink')
    require(sha(manifest.read_bytes())==lexer.MANIFEST_SHA,'manifest_pin')
    with manifest.open(newline='') as f:
        rows = [row for row in csv.DictReader(f) if row['extension'].lower()=='.apdl']
    require(len(rows)==3,'manifest_selection_count')
    row=rows[0]
    require(sha(row['filename'].encode())==NAME_SHA,'candidate_name_pin')
    require(row['sha256']==SOURCE_SHA and int(row['size_bytes'])==SOURCE_SIZE,'candidate_manifest_pin')
    base=lexer.BASE
    target=base/row['relative_path']
    require(target.parent==base and target.name==row['filename'],'candidate_path')
    require(not target.is_symlink() and stat.S_ISREG(target.lstat().st_mode),'candidate_file_type')
    require(target.resolve().parent==base.resolve(),'candidate_resolved_path')
    require(target.stat().st_size==SOURCE_SIZE,'candidate_size')
    with target.open('rb') as f:
        data=f.read(CAP+1)
    require(len(data)==SOURCE_SIZE and sha(data)==SOURCE_SHA,'candidate_pin')
    return target,manifest,data


def output_path(name):
    require(bool(re.fullmatch(r'producer-run[0-9]{2}\.json',name or '')),'output_name')
    path=HERE/name
    require(not path.exists() and not path.is_symlink(),'output_exists')
    return path


def run(name):
    output=output_path(name)
    receipt={'schema':'literal-material-fields-v1','alias':'APDL01',
             'producer_sha256':sha(Path(__file__).read_bytes()),
             'protocol_sha256':sha((HERE/'PROTOCOL.md').read_bytes()),
             'lexer_sha256':LEXER_SHA,'python':sys.version.split()[0]}
    try:
        lexer=load_lexer()
        target,manifest,data=read_candidate(lexer)
        result=scan(data,lexer)
        require(result['lines']==SOURCE_LINES,'source_line_count')
        with target.open('rb') as f:
            after_data=f.read(CAP+1)
        require(len(after_data)==SOURCE_SIZE and sha(after_data)==SOURCE_SHA,'source_pin_after')
        require(sha(manifest.read_bytes())==lexer.MANIFEST_SHA,'manifest_pin_after')
        require(sha(LEXER.read_bytes())==LEXER_SHA,'lexer_pin_after')
        require(sha(Path(__file__).read_bytes())==receipt['producer_sha256'],'producer_pin_after')
        require(sha((HERE/'PROTOCOL.md').read_bytes())==receipt['protocol_sha256'],'protocol_pin_after')
        receipt.update(status='PASS',manifest_sha256=lexer.MANIFEST_SHA,result=result)
    except Exception as e:
        receipt.update(status='FAIL',code=e.code if isinstance(e,Refused) else 'unexpected_error')
    with output.open('x') as f:
        json.dump(receipt,f,sort_keys=True,indent=2,allow_nan=False)
        f.write('\n')
    print(json.dumps({'status':receipt['status'],'output':output.name}))
    return 0 if receipt['status']=='PASS' else 1


def main():
    try:
        parser=SafeParser(prog='parse_material',allow_abbrev=False)
        parser.add_argument('--output',required=True)
        args=parser.parse_args()
        return run(args.output)
    except Exception as e:
        print(json.dumps({'status':'REFUSED','code':e.code if isinstance(e,Refused) else 'output_error'}))
        return 2


if __name__=='__main__':
    sys.exit(main())
