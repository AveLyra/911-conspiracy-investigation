#!/usr/bin/env python3
"""Read-only, minimized lexical source audit. Never interprets or runs APDL."""
import argparse
from collections import Counter
import csv
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
BASE = Path('/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539')
MANIFEST = Path('/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv')
MANIFEST_SHA = '30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf'
ZIP_SHA = '2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181'
ZIP = BASE / 'ANSYS Thermal Data.zip'
MEMBER_CAP, LINE_CAP, TOTAL_CAP = 4*1024**2, 16384, 512*1024**2
OPS = set('''*CFOPEN *CFCLOS *CFWRITE *VWRITE *MWRITE /OUTPUT CDWRITE NWRITE EWRITE
EDWRITE LSWRITE *VREAD *MREAD *SREAD /INPUT *USE *ULIB CDREAD NREAD EREAD LDREAD
RESUME FILE SET *CREATE *END /SYS'''.split())
VOCAB = OPS | set('''BF BFE BFDELE BFEDELE BFUNIF TUNIF BFCUM BFECUM BFINT BFTRAN
BFSCALE BFESCAL BFLIST BFELIST EDLOAD EDREAD EDSTART EDOPT EDTERM
NSEL ESEL CMSEL ALLSEL SELTOL CM CMBLOCK CMDELE N E EN ET KEYOPT TYPE REAL MAT
R RMORE MP MPDATA MPTEMP TB TBTEMP TBDATA SECTYPE SECDATA SECNUM SECOFFSET
*IF *ELSE *ELSEIF *ENDIF *DO *ENDDO *DOWHILE *CYCLE *EXIT *GO *GET *VGET
*VFUN *VOPER *DIM *SET *VSCFUN *VLEN *VMASK *TREAD /PREP7 /SOLU /SOLUTION
/POST1 /POST26 FINISH SOLVE LSSOLVE ANTYPE NLGEOM TIME NSUBST DELTIM KBC
AUTOTS OUTRES OUTPR NEQIT CNVTOL EQSLV NROPT PSTRES SAVE PARSAV PARRES
/CLEAR /FILNAME /TITLE /COM /GOPR /NOPR /BATCH /CONFIG /FORMAT /GRAPHICS
D DDELE F FDELE SF SFE SFA SFL ACEL CGLOC OMEGA IRLF TREF CSYS ESYS
NUMMRG NUMCMP NUMSTR NGEN EGEN NDELE EDELE NMODIF EMODIF ESEL NSLE ESLN
NROTAT CP CE CERIG RBE3 CECYC CEINTF DLIST ELIST NLIST PRNSOL PRRSOL PRNLD
PRESOL PRETAB ETABLE *STATUS /SHOW /VIEW /VUP /ANG /DIST /FOCUS /AUTO
PLNSOL PLESOL PLDISP EPLOT NPLOT /ESHAPE /DSCALE /CWD /EOF /EXIT'''.split())
FORMAT_COMMANDS = {'*VWRITE','*MWRITE','*VREAD','*MREAD'}
MARKERS = {'thermal_keyword': b'*LOAD_THERMAL_VARIABLE_NODE',
           'thermal_basename': b'WTC7_CASEB_400PM'}
TOKEN = re.compile(r'^([*/]?[A-Za-z][A-Za-z0-9_]*)\s*(?=,|$|\s)')
NUMERIC_START = re.compile(r'^[+-]?(?:\d|\.\d)')
CONTEXT = {'alias':None,'line':0,'completed_files':0}


class ScanError(Exception):
    def __init__(self, code): self.code = code


def need(condition, code):
    if not condition: raise ScanError(code)


def sha(data): return hashlib.sha256(data).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024**2), b''): h.update(b)
    return h.hexdigest()


def split_line(text):
    """Quote-aware ! comment and $ command separation; no macro execution."""
    pieces, current, quote, i = [], [], None, 0
    comment = ''
    while i < len(text):
        c = text[i]
        if quote:
            current.append(c)
            if c == quote:
                if i+1 < len(text) and text[i+1] == quote:
                    current.append(text[i+1]); i += 1
                else: quote = None
        elif c in ('\"', "'"):
            quote = c; current.append(c)
        elif c == '!':
            comment = text[i+1:]; break
        elif c == '$':
            pieces.append(''.join(current)); current = []
        else: current.append(c)
        i += 1
    pieces.append(''.join(current))
    return pieces, comment, quote is not None


def body_scan(data):
    need(len(data) <= MEMBER_CAP, 'member_cap')
    physical = data.split(b'\n')
    if data.endswith(b'\n'): physical.pop()
    if not data: physical = []
    need(all(len(line)+1 <= LINE_CAP for line in physical), 'line_cap')
    result = {'bytes':len(data), 'sha256':sha(data), 'lines':len(physical),
              'nul_bytes':data.count(b'\x00'), 'status':'lexical',
              'commands':{}, 'unknown_tokens':{}, 'operations':[], 'markers':[],
              'line_kinds':{}, 'thermal_labels':{}, 'lexical_flags':{}}
    if result['nul_bytes']:
        result['status'] = 'nul_semantics_excluded'
        return result
    commands, unknown, kinds, labels, flags = (Counter() for _ in range(5))
    expect_format = False
    for line_no, raw in enumerate(physical,1):
        CONTEXT['line']=line_no
        text = raw.rstrip(b'\r').decode('latin-1')
        parts, comment, unclosed = split_line(text)
        if unclosed: flags['unclosed_quote_lines'] += 1
        if comment: kinds['lines_with_bang_comment'] += 1
        if not text.strip(): kinds['blank_lines'] += 1
        if text.lstrip().startswith('!'): kinds['bang_comment_only_lines'] += 1
        code_marker_parts = []
        comment_parts = [comment]
        if expect_format:
            kinds['format_rows'] += 1
            if not text.strip() or text.lstrip().startswith(('!', '*', '/')):
                flags['format_candidate_unexpected_start'] += 1
            code_marker_parts.append(text)
            expect_format = False
        else:
            for seg_no, piece in enumerate(parts,1):
                s = piece.strip()
                if not s: continue
                match = TOKEN.match(s)
                token = match[1].upper() if match else None
                if token == '/COM':
                    commands[token] += 1; kinds['com_comment_segments'] += 1
                    comment_parts.append(s); continue
                code_marker_parts.append(s)
                if token:
                    if token in VOCAB: commands[token] += 1
                    else: unknown[sha(token.encode('ascii'))] += 1
                    if token in OPS:
                        result['operations'].append({'line':line_no,'segment':seg_no,
                                                     'command':token,
                                                     'arguments_sha256':sha(s[len(match[1]):].encode('latin-1'))})
                    if token in ('BF','BFE'):
                        fields = [v.strip().upper() for v in s.split(',')]
                        label = fields[2] if len(fields)>2 else ''
                        labels[token+':'+('TEMP' if label=='TEMP' else 'other_or_unresolved')] += 1
                    if token in FORMAT_COMMANDS: expect_format = True
                elif NUMERIC_START.match(s): kinds['numeric_data_segments'] += 1
                else: kinds['noncommand_unresolved_segments'] += 1
        for role, texts in [('code',code_marker_parts),('comment',comment_parts)]:
            joined = '\n'.join(texts).upper().encode('latin-1')
            for marker, value in MARKERS.items():
                count = joined.count(value)
                if count: result['markers'].append({'line':line_no,'role':role,'marker':marker,'count':count})
        need(len(result['operations']) <= 10000, 'operation_cap')
    if expect_format: flags['missing_format_eof'] += 1
    result.update(commands=dict(sorted(commands.items())), unknown_tokens=dict(sorted(unknown.items())),
                  line_kinds=dict(sorted(kinds.items())), thermal_labels=dict(sorted(labels.items())),
                  lexical_flags=dict(sorted(flags.items())))
    return result


def name_class(name):
    base = name.rsplit('/',1)[-1]
    case = next((c for c in 'ABC' if name.startswith('Case'+c+'_Temps/')), None)
    patterns = [('hour_driver',r'WTC7-\d+\.int'),('floor_driver',r'WTC7-Fl\d{2}-\d+\.int'),
                ('core',r'WTC7-Fl\d{2}-Core(?:B|[123])-\d+\.int'),
                ('slab',r'WTC7-Fl\d{2}-SLAB-\d+\.int'),
                ('slno',r'WTC7-Fl\d{2}-SLNo-\d+\.int'),
                ('member',r'WTC7-Fl\d{2}-[12]C\d+-\d+\.int')]
    for kind, pattern in patterns:
        if re.fullmatch(pattern,base,re.I): return case, kind
    suffix = Path(base).suffix.lower()
    return case, {'.png':'png','.nod':'node_list','.int':'other_int','':'extensionless'}.get(suffix,'other')


def selected_apdl():
    need(file_sha(MANIFEST)==MANIFEST_SHA,'manifest_pin')
    with MANIFEST.open(newline='') as f:
        rows=[r for r in csv.DictReader(f) if r['extension'].lower()=='.apdl']
    need(len(rows)==3,'apdl_count')
    for r in rows:
        p = BASE/r['relative_path']
        need(p.parent==BASE and p.name==r['filename'],'apdl_path')
        need(p.stat().st_size==int(r['size_bytes']) and file_sha(p)==r['sha256'],'apdl_pin')
    return rows


def historical():
    selected=selected_apdl()
    need(file_sha(ZIP)==ZIP_SHA,'zip_pin_before')
    records, total, counts = [], 0, Counter()
    for i,r in enumerate(selected,1):
        CONTEXT.update(alias=f'APDL{i:02d}',line=0)
        data=(BASE/r['relative_path']).read_bytes(); total+=len(data)
        result=body_scan(data)
        records.append({'alias':f'APDL{i:02d}','case':None,'class':'apdl',
                        'name_sha256':sha(r['filename'].encode()), 'scan':result})
        CONTEXT['completed_files']+=1
    with zipfile.ZipFile(ZIP) as z:
        entries=z.infolist(); need(len(entries)<=30000,'entry_cap')
        duplicates=Counter(i.filename for i in entries)
        need(all(v==1 for v in duplicates.values()),'duplicate_zip_names')
        for ordinal,info in enumerate(entries,1):
            CONTEXT.update(alias=f'ZIP{ordinal:05d}',line=0)
            counts['entries']+=1
            if info.is_dir(): counts['directories']+=1; continue
            case,kind=name_class(info.filename)
            rec={'alias':f'ZIP{ordinal:05d}','case':case,'class':kind,
                 'name_sha256':sha(info.filename.encode()),'declared_bytes':info.file_size,
                 'declared_crc32':info.CRC}
            counts['files']+=1
            if kind=='png':
                counts['png_excluded']+=1; rec['scan']={'status':'pixels_not_read'}
            else:
                need(info.file_size<=MEMBER_CAP,'zip_member_cap')
                total+=info.file_size; need(total<=TOTAL_CAP,'total_cap')
                with z.open(info) as f:
                    data=f.read(MEMBER_CAP+1)
                    need(len(data)==info.file_size and not f.read(1),'zip_eof_size')
                rec['scan']=body_scan(data); rec['crc_eof_pass']=True
                counts['body_read']+=1
                CONTEXT['completed_files']+=1
            records.append(rec)
    selected_apdl(); need(file_sha(ZIP)==ZIP_SHA,'zip_pin_after')
    agg=Counter(); labels=Counter(); unknown=Counter(); flags=Counter(); markers=[]
    for rec in records:
        s=rec['scan']; agg.update(s.get('commands',{})); labels.update(s.get('thermal_labels',{}))
        unknown.update(s.get('unknown_tokens',{})); flags.update(s.get('lexical_flags',{}))
        for marker in s.get('markers',[]): markers.append({'alias':rec['alias'],**marker})
    return {'manifest_sha256':MANIFEST_SHA,'zip_sha256':ZIP_SHA,'source_pins_after':True,
            'coverage':dict(counts),'total_read_bytes':total,'commands':dict(sorted(agg.items())),
            'thermal_labels':dict(sorted(labels.items())),'unknown_token_counts':dict(sorted(unknown.items())),
            'lexical_flags':dict(sorted(flags.items())),'markers':markers,'records':records}


class Controls(unittest.TestCase):
    def test_quotes_comments_and_dollars(self):
        p,c,u=split_line("*VWRITE,'a!b$c' $ BF,1,TEMP,2 ! BFE,2,TEMP,3")
        self.assertEqual(len(p),2); self.assertIn('BFE',c); self.assertFalse(u)
        a=body_scan(b"BF,1,TEMP,2 $ BFE,2,TEMP,1,3 ! BF,5,TEMP,5\n")
        self.assertEqual(a['commands'],{'BF':1,'BFE':1})
        self.assertEqual(a['thermal_labels'],{'BF:TEMP':1,'BFE:TEMP':1})
    def test_formats_and_quoted_markers(self):
        a=body_scan(b"*VWRITE,'*LOAD_THERMAL_VARIABLE_NODE'\n(A)\n/COM,*LOAD_THERMAL_VARIABLE_NODE\n")
        self.assertEqual(a['commands'],{'*VWRITE':1,'/COM':1})
        self.assertEqual(a['line_kinds']['format_rows'],1)
        self.assertEqual([v['role'] for v in a['markers']],['code','comment'])
    def test_nul_and_unknown(self):
        self.assertEqual(body_scan(b'BF,1,TEMP,2\n\x00')['status'],'nul_semantics_excluded')
        a=body_scan(b'BFWORD,1,2\nprivate_name=4\n')
        self.assertFalse(a['commands']); self.assertEqual(sum(a['unknown_tokens'].values()),1)
        self.assertNotIn('private_name',json.dumps(a))
    def test_quotes_escaped(self):
        p,c,u=split_line("*VWRITE,'a''!$b' ! stop")
        self.assertEqual(len(p),1); self.assertEqual(c,' stop'); self.assertFalse(u)
        self.assertTrue(split_line("*VWRITE,'abc")[2])
    def test_caps(self):
        with self.assertRaises(ScanError): body_scan(b'x'*(MEMBER_CAP+1))
        with self.assertRaises(ScanError): body_scan(b'x'*(LINE_CAP+1))
    def test_crc(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w',compression=zipfile.ZIP_STORED) as z:z.writestr('test',b'payload')
        value=b.getvalue().replace(b'payload',b'payloae')
        with zipfile.ZipFile(io.BytesIO(value)) as z:
            with self.assertRaises(zipfile.BadZipFile):z.read('test')
    def test_names(self):
        self.assertEqual(name_class('CaseB_Temps/a/WTC7-Fl08-1C137-2.int'),('B','member'))
        self.assertEqual(name_class('CaseA_Temps/WTC7-1.int'),('A','hour_driver'))
        self.assertEqual(name_class('secret/wrong-name.int'),(None,'other_int'))
        self.assertEqual(Counter(['same','same'])['same'],2)
    def test_empty_and_missing_format(self):
        self.assertEqual(body_scan(b'')['lines'],0)
        self.assertEqual(body_scan(b'*VWRITE,1\n')['lexical_flags'],{'missing_format_eof':1})


def main():
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--controls',action='store_true');a=p.parse_args()
    tests=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    if not tests.wasSuccessful():return 1
    if a.controls:return 0
    dest=HERE/(a.output or '')
    need(a.output and dest.parent==HERE and not dest.exists(),'create_only_output')
    start=time.monotonic()
    receipt={'code_sha256':file_sha(Path(__file__)),'protocol_sha256':file_sha(HERE/'PROTOCOL.md'),
             'python':sys.version,'command':sys.argv,'controls':tests.testsRun}
    try:
        CONTEXT.update(alias=None,line=0,completed_files=0)
        result=historical();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        need(peak<=768*1024**2,'memory_cap')
        receipt.update(status='PASS',peak_memory_bytes=peak,result=result)
    except Exception as e:
        receipt.update(status='FAIL',code=e.code if isinstance(e,ScanError) else type(e).__name__,
                       progress=CONTEXT.copy())
    receipt['seconds']=time.monotonic()-start
    with dest.open('x') as f:json.dump(receipt,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({k:receipt[k] for k in ('status','seconds')}))
    return 0 if receipt['status']=='PASS' else 1


if __name__=='__main__':
    try:sys.exit(main())
    except ScanError as e:print(json.dumps({'status':'REFUSED','code':e.code}));sys.exit(2)
