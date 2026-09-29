#!/usr/bin/env python3
"""Read-only numeric control inventory; never initializes/executes source inputs.

Prospective scope: three pinned gzip streams to EOF; CONTROL_CONTACT, plain
PART_CONTACT, and the three already observed headed CONTACT variants. Unknown
related variants are hashed and retained, not interpreted. Zero != blank.
Output is create-only; failed computations retain a safe error receipt.
"""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
MANUAL = Path('/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf')
PRIOR = HERE.parent / 'c79-restraint-audit/contacts-root01.json'
PINS = {
    'PROTOCOL.md': (HERE/'PROTOCOL.md', 'b18a519ba88e7d61d331d821232e269c3e3f9a5e690a3e25e3e108e1e70df1ea'),
    'manual': (MANUAL, 'f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d'),
    'prior_contacts': (PRIOR, '04193c154495a37e7603e72ad32668ee28383ff9471b4baeee7f93b257c56859'),
    'prior_method': (HERE.parent/'c79-restraint-audit/contact-method-review.md', 'b720e2330f46efc75e527db2aa3154147e36fa0210eee4eecb6597d3a128bb55'),
}
FILES = [
    ('SRC-119', 'discrete_mass.k.gz', 70199, '2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7'),
    ('SRC-120', 'elem_thick_to-renum.k.gz', 23162693, 'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59'),
    ('SRC-121', 'wtc7_global_8a_no-conn-matl.k.gz', 47520888, 'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d'),
]
CONTACT = {
    b'*CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET',
    b'*CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET',
    b'*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID',
}
GLOBAL_FIELDS = [
    'SLSFAC RWPNAL ISLCHK SHLTHK PENOPT THKCHG ORIEN ENMASS'.split(),
    'USRSTR USRFRC NSBCS INTERM XPENE SSTHK ECDT TIEDPRJ'.split(),
    'SFRIC DFRIC EDC VFC TH TH_SF PEN_SF UNUSED8'.split(),
    'IGNORE FRCENG SKIPRWG OUTSEG SPOTSTP SPOTDEL SPOTHIN UNUSED8'.split(),
    'ISYM NSEROD RWGAPS RWGDTH RWKSF ICOV SWRADF ITHOFF'.split(),
    'SHLEDG UNUSED2 UNUSED3 UNUSED4 UNUSED5 UNUSED6 UNUSED7 UNUSED8'.split(),
]
CONTACT_FIELDS = [
    'SSID MSID SSTYP MSTYP SBOXID MBOXID SPR MPR'.split(),
    'FS FD DC VC VDC PENCHK BT DT'.split(),
    'SFS SFM SST MST SFST SFMT FSF VSF'.split(),
    'SOFT SOFSCL LCIDAB MAXPAR SBOPT DEPTH BSORT FRCFRQ'.split(),
    'PENMAX THKOPT SHLTHK SNLOG ISYM I2D3D SLDTHK SLDSTF'.split(),
    'IGAP IGNORE DPRFAC DTSTIF UNUSED5 UNUSED6 FLANGL UNUSED8'.split(),
]
PART_FIELDS = [
    'PID SECID MID EOSID HGID GRAV ADPOPT TMID'.split(),
    'FS FD DC VC OPTT SFT SSF UNUSED8'.split(),
]
NUMERIC = re.compile(rb'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?\Z')


class CheckError(Exception):
    pass


def require(condition, code):
    if not condition:
        raise CheckError(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with path.open('rb') as src:
        for block in iter(lambda: src.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def numeric_row(raw):
    data = raw.rstrip(b'\r\n')
    require(b'$' not in data and b'\t' not in data, 'unreviewed_inline_or_tab')
    if b',' in data:
        fields = data.split(b',')
        require(len(fields) <= 8, 'too_many_free_fields')
        layout = 'comma'
    else:
        require(not data[80:].strip(), 'nonblank_beyond_80')
        fields = [data[i:i+10] for i in range(0, 80, 10)]
        layout = 'fixed10'
    fields += [b''] * (8-len(fields))
    result, tokens = [], []
    for field in fields:
        token = field.strip()
        require(not token or NUMERIC.fullmatch(token), 'unreviewed_numeric_token')
        value = float(token.replace(b'd', b'e').replace(b'D', b'E')) if token else None
        require(value is None or math.isfinite(value), 'nonfinite_value')
        result.append(value)
        tokens.append(token.decode('ascii') if token else None)
    return {'values': result, 'numeric_tokens': tokens, 'format': layout, 'raw_sha256': sha(raw)}


def classify(keyword):
    if keyword == b'*CONTROL_CONTACT':
        return 'global', keyword.decode('ascii')
    if keyword == b'*PART_CONTACT':
        return 'part', keyword.decode('ascii')
    if keyword in CONTACT:
        return 'contact', keyword.decode('ascii')
    if keyword.startswith(b'*CONTROL_CONTACT') or keyword.startswith(b'*CONTACT') or (keyword.startswith(b'*PART') and b'CONTACT' in keyword):
        return 'unsupported_related', None
    return None, None


def scan(lines, source, output, receipt, start):
    active = None
    h = hashlib.sha256()
    count = size = 0
    for count, raw in enumerate(lines, 1):
        h.update(raw)
        size += len(raw)
        receipt.update(lines=count, uncompressed_bytes=size)
        require(count <= 12000000 and len(raw) <= 4096, 'stream_bound')
        if count % 100000 == 0:
            require(time.monotonic()-start < 180, 'time_bound')
        s = raw.strip()
        if s.startswith(b'$'):
            continue
        if s.startswith(b'*'):
            kind, allowed = classify(s.upper())
            active = None
            if kind:
                active = {'source': source, 'kind': kind, 'keyword': allowed,
                          'keyword_line': count, 'keyword_sha256': sha(raw), 'cards': []}
                output.append(active)
            continue
        if active is None:
            continue
        if active['kind'] == 'unsupported_related':
            active.setdefault('uninterpreted_rows', []).append({'line': count, 'raw_sha256': sha(raw)})
            require(len(active['uninterpreted_rows']) <= 32, 'unknown_row_bound')
            continue
        if active['kind'] in ('part', 'contact') and 'heading_line' not in active:
            active.update(heading_line=count, heading_sha256=sha(raw))
            if active['kind'] == 'contact':
                token = (raw.split(b',', 1)[0] if b',' in raw else raw[:10]).strip()
                require(re.fullmatch(rb'\+?\d+', token), 'contact_cid')
                active['cid'] = int(token)
            continue
        row = numeric_row(raw)
        row['line'] = count
        row['card_index'] = len(active['cards'])+1
        schema = {'global': GLOBAL_FIELDS, 'part': PART_FIELDS, 'contact': CONTACT_FIELDS}[active['kind']]
        names = schema[len(active['cards'])] if len(active['cards']) < len(schema) else None
        row['field_names'] = names
        row['schema_status'] = 'mapped_fields_not_effective_defaults' if names else 'unreviewed_additional_card'
        active['cards'].append(row)
        require(len(active['cards']) <= 16, 'card_bound')
    receipt.update(eof=True, lines=count, uncompressed_bytes=size, uncompressed_sha256=h.hexdigest())


def controls():
    checks = []
    def check(name, ok):
        require(ok, 'control_'+name)
        checks.append({'name': name, 'pass': True})
    r = numeric_row(b'0,,1,0.0D+00\n')
    check('zero_vs_null', r['values'][:4] == [0., None, 1., 0.])
    check('numeric_lexemes', r['numeric_tokens'][3] == '0.0D+00')
    check('blank_card_retained', numeric_row(b'\n')['values'] == [None]*8)
    check('fixed_width_slots', numeric_row(b'         0                   1\n')['values'][:3] == [0., None, 1.])
    for label, raw in [('unsafe_text', b'unknown\n'), ('wide', b'0,'*8+b'0\n'), ('nonfinite', b'1e999\n'), ('inline', b'0 $ unknown\n')]:
        try:
            numeric_row(raw)
        except CheckError:
            check(label+'_rejected', True)
        else:
            check(label+'_rejected', False)
    check('unknown_variant_not_absent', classify(b'*PART_CONTACT_PRINT')[0] == 'unsupported_related')
    out, rec = [], {}
    scan([b'*CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET\n', b'1,synthetic heading\n', b'$ synthetic comment\n', b'0,,1\n', b'\n', b'*END\n'], 'synthetic', out, rec, time.monotonic())
    check('id_middle_heading_separated', out[0]['cid'] == 1 and out[0]['cards'][0]['line'] == 4)
    check('blank_not_shifted', len(out[0]['cards']) == 2 and out[0]['cards'][1]['values'] == [None]*8)
    check('source_strings_suppressed', 'synthetic heading' not in json.dumps(out) and 'synthetic comment' not in json.dumps(out))
    check('complete_synthetic_eof', rec['eof'] and rec['lines'] == 6)
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    require(args.out.resolve().parent == HERE, 'output_outside_unit')
    with args.out.open('x', encoding='utf-8') as dst:
        start = time.monotonic()
        result = {'status': 'failed', 'producer_sha256': file_sha(Path(__file__)),
                  'command': sys.argv, 'python': sys.version.split()[0], 'records': [], 'sources': {}}
        try:
            result['controls'] = controls()
            result['pins_before'] = {key: file_sha(path) for key, (path, expected) in PINS.items()}
            require(all(result['pins_before'][key] == pin for key, (_, pin) in PINS.items()), 'dependency_pin')
            previous = json.loads(PRIOR.read_text())
            for source, name, size, expected in FILES:
                path = BASE/name
                rec = {'eof': False, 'compressed_bytes': path.stat().st_size, 'compressed_sha256': file_sha(path)}
                result['sources'][source] = rec
                require(rec['compressed_bytes'] == size and rec['compressed_sha256'] == expected, 'compressed_pin')
                with gzip.open(path, 'rb') as stream:
                    scan(stream, source, result['records'], rec, start)
                rec['pin_after'] = file_sha(path) == expected and path.stat().st_size == size
                require(rec['pin_after'], 'changed_source')
                require(all(rec[k] == previous['sources'][name][k] for k in ('lines', 'uncompressed_bytes', 'uncompressed_sha256')), 'eof_receipt_mismatch')
            result['selected_contact_comparison'] = []
            for record in result['records']:
                if record['kind'] == 'contact' and record['cid'] in (1, 2):
                    old = next(c for c in previous['result']['contacts'] if c['cid'] == record['cid'])
                    passed = old['cards'] == [{'line': c['line'], 'values': c['values']} for c in record['cards']]
                    require(passed, 'selected_contact_mismatch')
                    result['selected_contact_comparison'].append({'cid': record['cid'], 'pass': passed})
            result['pins_after'] = {key: file_sha(path) for key, (path, _) in PINS.items()}
            require(result['pins_before'] == result['pins_after'], 'changed_dependency')
            require(result['producer_sha256'] == file_sha(Path(__file__)), 'changed_producer')
            result['status'] = 'passed'
        except CheckError as exc:
            result['error_code'] = str(exc)
        except Exception as exc:
            result['error_type'] = type(exc).__name__
        result['elapsed_seconds'] = time.monotonic()-start
        result['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        json.dump(result, dst, indent=2, sort_keys=True, allow_nan=False)
        dst.write('\n')
    print(json.dumps({'status': result['status'], 'record_count': len(result['records']), 'output_sha256': file_sha(args.out)}))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
