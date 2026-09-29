"""Bounded literal-definition search; never executes supplied source programs."""
import argparse
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import resource
import sys
import time
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
JUNE = Path('/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539')
SEPT = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
MANIFEST = Path('/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv')
ZIP = JUNE / 'ANSYS Thermal Data.zip'
PINS = {
    MANIFEST: '30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf',
    ZIP: '2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181',
    HERE/'PROTOCOL.md': 'dfc4ecbf348066574c6d38b5b087272120f006d35bfb72a1920ff79c14189865',
    HERE/'SCAN-CONVENTIONS.md': '06d9f8921be5dd2994dcca74c56ca5104b3aa88be85048a34c1b476ea82c85be',
    HERE/'../c79-casea-spring-audit/casea-root01.json': '27e8905727fa8462724db70f6ce11f411391170a4a6636936491027eaba988a2',
    HERE/'../c79-casea-spring-audit/independent-definition-presence01.json': '7377187b71fe0fc10a5483ed80424499555270708d02a61d2d2a991c14a939c7',
}
SEPT_PINS = {
    116: ('Damage_Global_ANSYS_CaseB_4.0hr.k.gz', 5331, '982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da'),
    117: ('G6A_CaseA_El_Delete_List.k.gz', 103872, 'aa39ae4c977c51048fd267d890d98b66bd49dccaa965715b1cce1397a54c5273'),
    118: ('WTC7_CaseB_400pm.int.gz', 2702040, '51b1624338dce5da4dc5a91c13d1356338997af0d3fef9cd627b29ee3bbb9447'),
}
FAMILIES = ('DEFINE_CURVE', 'DEFINE_TABLE', 'DEFINE_FUNCTION')
ENCODINGS = ('ascii', 'utf-16-le', 'utf-16-be')
PATTERNS = {
    enc: [(family, ('*'+family).encode(enc)) for family in FAMILIES]
    for enc in ENCODINGS
}
MEMBER_CAP, LINE_CAP, STREAM_CAP = 4*1024**2, 16384, 512*1024**2
CONTEXT = {'alias': None, 'line': 0, 'completed_bodies': 0}
STARTED = None


class Refusal(Exception):
    pass


def need(ok, code):
    if not ok:
        raise Refusal(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def guards():
    if STARTED is not None:
        need(time.monotonic()-STARTED <= 300, 'wall_time_cap')
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= 768*1024**2, 'rss_cap')


def marker_rows(raw, line, offset):
    upper = raw.upper()
    rows = []
    for enc, patterns in PATTERNS.items():
        if enc != 'ascii' and b'\x00' not in raw:
            continue
        step = 1 if enc == 'ascii' else 2
        for family, pattern in patterns:
            pos = upper.find(pattern)
            while pos >= 0:
                prefix = raw[:pos]
                if offset == 0 and prefix.startswith(b'\xef\xbb\xbf'):
                    prefix = prefix[3:]
                try:
                    leading = all(c in ' \t\r' for c in prefix.decode(enc))
                except UnicodeError:
                    leading = False
                after = upper[pos+len(pattern):pos+len(pattern)+step]
                try:
                    following = after.decode(enc)
                except UnicodeError:
                    following = ''
                suffix = len(following) == 1 and following in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                rows.append({'line': line, 'byte_column0': pos, 'byte_offset0': offset+pos,
                             'family': family, 'encoding': enc,
                             'line_leading': leading, 'suffix_present': suffix})
                pos = upper.find(pattern, pos+1)
    return sorted(rows, key=lambda x: (x['byte_offset0'], x['encoding'], x['family']))


def scan(stream, byte_cap):
    h = hashlib.sha256()
    total = lines = nuls = nonascii = 0
    bom = False
    hits = []
    while True:
        raw = stream.readline(LINE_CAP+1)
        if not raw:
            break
        need(len(raw) <= LINE_CAP, 'line_cap')
        need(total+len(raw) <= byte_cap, 'byte_cap')
        lines += 1
        CONTEXT['line'] = lines
        if lines == 1:
            bom = raw.startswith(b'\xef\xbb\xbf')
        hits.extend(marker_rows(raw, lines, total))
        need(len(hits) <= 10000, 'marker_cap')
        h.update(raw)
        total += len(raw)
        nuls += raw.count(b'\x00')
        if not raw.isascii():
            nonascii += len(raw)-len(raw.decode('ascii', errors='ignore'))
        if lines % 20000 == 0:
            guards()
    return {'bytes': total, 'sha256': h.hexdigest(), 'lines': lines, 'eof': True,
            'nul_bytes': nuls, 'nonascii_bytes': nonascii,
            'all_nul': total > 0 and nuls == total, 'initial_utf8_bom': bom,
            'literal_hits': hits}


def pins():
    result = {}
    for path, expected in PINS.items():
        actual = file_sha(path)
        need(actual == expected, 'dependency_pin')
        result[path.name] = actual
    return result


def unique_names(names):
    need(len(names) == len(set(names)), 'duplicate_names')


def destination(name):
    out = HERE/name
    need(re.fullmatch(r'root-[0-9]+\.json', name) is not None, 'output_scope')
    need(not out.exists(), 'output_exists')
    return out


def historical():
    before = pins()
    with MANIFEST.open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    unique_names([r['relative_path'] for r in rows])
    by_path = {r['relative_path']: (n, r) for n, r in enumerate(rows, 2)}
    apdls = [(n, r) for n, r in enumerate(rows, 2) if r['extension'].lower() == '.apdl']
    need(len(apdls) == 3, 'apdl_selection')
    records = []
    total_june = 0
    for i, (manifest_line, row) in enumerate(apdls, 1):
        alias = f'APDL{i:02d}'
        CONTEXT.update(alias=alias, line=0)
        path = JUNE/row['relative_path']
        need(path.parent == JUNE and path.name == row['filename'], 'apdl_path_scope')
        need(path.stat().st_size == int(row['size_bytes'])
             and file_sha(path) == row['sha256'], 'apdl_pin_before')
        with path.open('rb') as stream:
            body = scan(stream, MEMBER_CAP)
        need(body['bytes'] == int(row['size_bytes']) and body['sha256'] == row['sha256'], 'apdl_body_pin')
        need(file_sha(path) == row['sha256'], 'apdl_pin_after')
        records.append({'alias': alias, 'kind': 'apdl', 'manifest_line': manifest_line,
                        'name_sha256': digest(row['filename'].encode()), 'body': body})
        total_june += body['bytes']
        CONTEXT['completed_bodies'] += 1
    counts = Counter()
    with zipfile.ZipFile(ZIP) as archive:
        entries = archive.infolist()
        need(len(entries) <= 30000, 'entry_cap')
        unique_names([i.filename for i in entries])
        for ordinal, info in enumerate(entries, 1):
            alias = f'ZIP{ordinal:05d}'
            CONTEXT.update(alias=alias, line=0)
            counts['entries'] += 1
            record = {'alias': alias, 'ordinal': ordinal,
                      'name_sha256': digest(info.filename.encode()),
                      'declared_bytes': info.file_size, 'declared_crc32': info.CRC}
            if info.is_dir():
                counts['directories'] += 1
                record['kind'] = 'directory_excluded'
            else:
                counts['files'] += 1
                manifest_line, row = by_path.get('ANSYS Thermal Data/'+info.filename, (None, None))
                need(row is not None, 'unmanifested_zip_member')
                need(info.file_size == int(row['size_bytes']), 'zip_manifest_size')
                record['manifest_line'] = manifest_line
                if info.filename.lower().endswith('.png'):
                    counts['png_excluded'] += 1
                    record['kind'] = 'png_body_excluded'
                else:
                    record['kind'] = 'zip_body'
                    need(info.file_size <= MEMBER_CAP, 'zip_member_cap')
                    total_june += info.file_size
                    need(total_june <= STREAM_CAP, 'june_total_cap')
                    with archive.open(info) as stream:
                        body = scan(stream, MEMBER_CAP)
                    need(body['bytes'] == info.file_size and body['sha256'] == row['sha256'], 'zip_member_body_pin')
                    record.update(body=body, crc_eof_pass=True)
                    counts['bodies_read'] += 1
                    CONTEXT['completed_bodies'] += 1
            records.append(record)
            if ordinal % 1000 == 0:
                guards()
    for src, (name, size, expected) in SEPT_PINS.items():
        alias = f'SRC{src}'
        CONTEXT.update(alias=alias, line=0)
        path = SEPT/name
        need(path.stat().st_size == size and file_sha(path) == expected, 'sept_pin_before')
        with gzip.open(path, 'rb') as stream:
            body = scan(stream, STREAM_CAP)
        need(path.stat().st_size == size and file_sha(path) == expected, 'sept_pin_after')
        records.append({'alias': alias, 'kind': 'gzip_body', 'name_sha256': digest(name.encode()),
                        'compressed_bytes': size, 'compressed_sha256': expected, 'body': body})
        CONTEXT['completed_bodies'] += 1
    after = pins()
    guards()
    return {'pins_before': before, 'pins_after': after, 'archive_counts': dict(counts),
            'june_read_bytes': total_june, 'records': records,
            'body_count': sum('body' in r for r in records),
            'literal_hit_count': sum(len(r.get('body', {}).get('literal_hits', [])) for r in records),
            'limits': ['Literal byte-pattern search, not source execution or a general solver-language parser.',
                       'PNG/PDF/presentation bodies, runtime-generated/binary/external inputs are not resolved.',
                       'A literal match does not supply typed curve identity or historical run provenance.']}


class Controls(unittest.TestCase):
    def body(self, data):
        return scan(io.BytesIO(data), MEMBER_CAP)

    def test_case_whitespace(self):
        a=self.body(b'  *define_curve\n602,0\n')
        self.assertEqual(a['lines'],2)
        self.assertEqual(a['literal_hits'][0]['family'],'DEFINE_CURVE')
        self.assertTrue(a['literal_hits'][0]['line_leading'])
    def test_embedded_comment_quote_repeated(self):
        h=self.body(b'$ *DEFINE_TABLE "*DEFINE_TABLE"\n*VWRITE,"*DEFINE_FUNCTION"\n')['literal_hits']
        self.assertEqual(len(h),3)
        self.assertFalse(any(x['line_leading'] for x in h))
    def test_suffix_boundary(self):
        h=self.body(b'*DEFINE_CURVE_TITLE\n*DEFINE_CURVE123\n*DEFINE_CURVE$comment\n')['literal_hits']
        self.assertEqual([x['suffix_present'] for x in h],[True,True,False])
    def test_no_unrelated_match(self):
        self.assertEqual(self.body(b'*COMMENT_DEFINE_TABLE\nDEFINE_CURVE\n')['literal_hits'],[])
    def test_byte_offsets(self):
        h=self.body(b'x\n *DEFINE_TABLE')['literal_hits'][0]
        self.assertEqual((h['line'],h['byte_column0'],h['byte_offset0']),(2,1,3))
    def test_utf16(self):
        for enc in ENCODINGS[1:]:
            h=self.body(' \t*define_function_foo'.encode(enc))['literal_hits']
            self.assertEqual(len(h),1)
            self.assertEqual(h[0]['encoding'],enc)
            self.assertTrue(h[0]['line_leading'])
            self.assertTrue(h[0]['suffix_present'])
    def test_odd_utf16_prefix(self):
        h=self.body(b'x'+'*DEFINE_CURVE'.encode('utf-16-le'))['literal_hits']
        self.assertEqual(len(h),1)
        self.assertFalse(h[0]['line_leading'])
    def test_bom(self):
        a=self.body(b'\xef\xbb\xbf*DEFINE_CURVE\n')
        self.assertTrue(a['initial_utf8_bom'])
        self.assertTrue(a['literal_hits'][0]['line_leading'])
        b=self.body(b'\xff\xfe'+'*DEFINE_CURVE'.encode('utf-16-le'))
        self.assertFalse(b['literal_hits'][0]['line_leading'])
    def test_nul_and_nonascii(self):
        self.assertTrue(self.body(b'\x00'*328)['all_nul'])
        a=self.body(b'\x00\xff\n')
        self.assertEqual((a['nul_bytes'],a['nonascii_bytes']),(1,1))
        self.assertFalse(a['all_nul'])
    def test_empty_final_line(self):
        for raw,lines in [(b'',0),(b'a',1),(b'a\n',1),(b'a\n\n',2)]:
            self.assertEqual(self.body(raw)['lines'],lines)
    def test_caps(self):
        with self.assertRaises(Refusal): self.body(b'x'*(LINE_CAP+1))
        with self.assertRaises(Refusal): scan(io.BytesIO(b'abc'),2)
    def test_duplicate_names(self):
        with self.assertRaises(Refusal): unique_names(['same','same'])
        unique_names(['CaseA/a','CaseB/a'])
    def test_crc(self):
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as z: z.writestr('synthetic',b'payload')
        with zipfile.ZipFile(io.BytesIO(buffer.getvalue().replace(b'payload',b'payloae'))) as z:
            with self.assertRaises(zipfile.BadZipFile): z.read('synthetic')
    def test_pin_and_output_guards(self):
        with self.assertRaises(Refusal): need(digest(b'a')==digest(b'b'),'synthetic_pin')
        with self.assertRaises(Refusal): destination('../root-01.json')
        with self.assertRaises(Refusal): destination('PROTOCOL.md')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    tests=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    if not tests.wasSuccessful(): sys.exit(1)
    if args.controls: sys.exit(0)
    try:
        out=destination(args.output or '')
    except Refusal as e:
        print(json.dumps({'status':'REFUSED','code':str(e)}));sys.exit(2)
    STARTED=time.monotonic()
    receipt={'code_sha256':file_sha(Path(__file__)), 'controls':tests.testsRun,
             'python':sys.version, 'command':sys.argv}
    try:
        CONTEXT.update(alias=None,line=0,completed_bodies=0)
        result=historical()
        receipt.update(status='PASS',result=result)
    except Exception as exc:
        receipt.update(status='FAIL',failure_code=str(exc) if isinstance(exc,Refusal) else type(exc).__name__,
                       progress=CONTEXT.copy())
    receipt.update(elapsed_seconds=time.monotonic()-STARTED,
                   maxrss_bytes_darwin=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with out.open('x') as handle:
        json.dump(receipt,handle,indent=2,sort_keys=True);handle.write('\n')
    print(json.dumps({'status':receipt['status'],'output':out.name,
                      'body_count':receipt.get('result',{}).get('body_count'),
                      'literal_hit_count':receipt.get('result',{}).get('literal_hit_count'),
                      'failure_code':receipt.get('failure_code')}))
    sys.exit(0 if receipt['status']=='PASS' else 1)
