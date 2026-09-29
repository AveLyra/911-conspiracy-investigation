#!/usr/bin/env python3
"""Independent bounded APDL lexical audit; never an interpreter or extractor."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import resource
import stat
import struct
import sys
import time
import warnings
import zipfile
import zlib

BASE=Path(__file__).resolve().parent
RAW=Path('/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539')
MANIFEST=Path('/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv')
MANIFEST_SHA='30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf'
ZIP=RAW/'ANSYS Thermal Data.zip'
ZIP_SHA='2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181'
APDL_SHAS=['e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64','e96f23597454737ca3177d22e8cd857561b937658189b5d9e1b49ae5bdbdf8f9','bb07af3ff1537348f87a6ea95123d3620d588766d278649829c9f35247c33e5a']
PROTOCOL_SHA='f79b1e78d01f7d4de1e994ed83d4f93b4a3a307714cdb53823be1e430ac0b34e'
MEMBER_CAP,LINE_CAP,TOTAL_CAP,ENTRY_CAP,OP_CAP,MEM_CAP=4*1024**2,16384,512*1024**2,30000,10000,768*1024**2
PROGRESS=[]
VOCAB={}
for role,names in {
    'input':'/INPUT *USE *VREAD *MREAD *TREAD CDREAD RESUME PARRES LSREAD',
    'output':'*CFOPEN *CFWRITE *CFCLOS *VWRITE *MWRITE /OUTPUT CDWRITE NWRITE EWRITE LSWRITE PARSAV *EXPORT',
    'input_load':'LDREAD',
    'body_load':'BF BFE BFUNIF BFDELE BFEDELE BFCUM BFECUM BFSCALE BFESCAL BFINT BFLIST BFELIST TUNIF TREF',
    'selection':'NSEL ESEL ALLSEL CMSEL NSLE ESLN ASLN NSLA ESLA ASEL LSEL KSEL VSEL',
    'control':'*IF *ELSE *ELSEIF *ENDIF *DO *DOWHILE *ENDDO *CYCLE *EXIT *GO *RETURN *CREATE *END *ULIB *ABBR *SET *DIM *GET *VGET *VOPER *VFUN *VSCFUN *VLEN *VMASK *VFACT *VABS *VCUM *MSG *STATUS /EOF /EXIT',
    'solver':'/PREP7 /SOLU /POST1 /POST26 FINISH SOLVE ANTYPE NLGEOM OUTRES DELTIM TIME NSUBST KBC NEQIT NROPT LSSOLVE EQSLV SOLCONTROL RESCONTROL UPGEOM UPCOORD',
    'model':'N E EN ET KEYOPT MP MPDATA MPTEMP R RMORE REAL MAT TYPE SECTYPE SECDATA SECNUM CSYS LOCAL D F SF SFE ACEL EKILL EALIVE EMODIF ESURF AMESH VMESH DK DDELE CM CMDELE',
    'context':'/TITLE /FILNAME /UNITS /NOPR /GOPR /GRAPHICS /VIEW /VUP /SHOW /REPLOT /CWD /GRA /COM',
}.items():
    for name in names.split():VOCAB[name]=role
FORMAT_COMMANDS={'*VWRITE','*MWRITE','*VREAD','*MREAD'}
OPERATIONS={n for n,r in VOCAB.items() if r in ('input','output','input_load')}
TOKEN=re.compile(r'[*/]?[A-Z][A-Z0-9_]*\Z')
NUM=re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[ED][+-]?[0-9]+)?\Z')
MARKERS={
    'lsdyna_thermal_keyword':re.compile(r'(?<![A-Z0-9_])\*LOAD_THERMAL_VARIABLE_NODE(?![A-Z0-9_])',re.I),
    'known_thermal_basename':re.compile(r'(?<![A-Z0-9_])WTC7_CaseB_400pm(?![A-Z0-9_])',re.I),
}


class AuditError(Exception):
    def __init__(self,code,source='',line=0):
        self.code,self.source,self.line=code,source,line
        super().__init__(code)


def need(ok,code,source='',line=0):
    if not ok:raise AuditError(code,source,line)


def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()


def split_syntax(line):
    """Quotes protect punctuation; doubled quote stays inside the same literal."""
    pieces=[]; start=0; quote=None; i=0; comment=None
    while i<len(line):
        ch=line[i]
        if quote:
            if ch==quote:
                if i+1<len(line) and line[i+1]==quote:i+=2;continue
                quote=None
        elif ch in "\"'":quote=ch
        elif ch=='!':
            pieces.append(line[start:i]);comment=line[i+1:];return pieces,comment,False
        elif ch=='$':pieces.append(line[start:i]);start=i+1
        i+=1
    pieces.append(line[start:])
    return pieces,comment,quote is not None


def first_field(segment):
    quote=None
    for i,ch in enumerate(segment):
        if quote:
            if ch==quote:quote=None
        elif ch in "\"'":quote=ch
        elif ch==',':return segment[:i].strip(),segment[i+1:]
    return segment.strip(),''


def lexical(data,source):
    """NUL makes the entire file uninterpreted, even if most bytes look like text."""
    lines=data.split(b'\n')
    if data.endswith(b'\n'):lines.pop()
    if not data:lines=[]
    base={'physical_lines':len(lines),'nul_bytes':data.count(b'\0'),'nonascii_bytes':sum(x>127 for x in data)}
    if base['nul_bytes']:
        return {**base,'status':'uninterpreted_nul','counts':None,'commands':None,'operations':None,'markers':None,'issues':None}
    counts=Counter(); commands=Counter(); operations=[]; markers=[]; issues=[]; pending=None
    def marker(text,context,line,segment=0):
        for name,pattern in MARKERS.items():
            for _ in pattern.finditer(text):
                markers.append({'marker':name,'context':context,'line':line,'segment':segment})
                need(len(markers)<=OP_CAP,'marker_locator_cap',source,line)
    for lineno,raw in enumerate(lines,1):
        need(len(raw)+(1 if lineno<len(lines) or data.endswith(b'\n') else 0)<=LINE_CAP,'line_cap',source,lineno)
        text=raw.decode('latin-1').rstrip('\r')
        if text.strip():counts['nonempty_lines']+=1
        else:counts['blank_lines']+=1
        pieces,comment,unclosed=split_syntax(text)
        if comment is not None:
            counts['lines_with_comment']+=1;marker(comment,'comment',lineno)
        if not any(p.strip() for p in pieces) and comment is not None:counts['comment_only_lines']+=1
        if unclosed:issues.append({'code':'unclosed_quote','line':lineno})
        if pending is not None:
            counts['format_records']+=1
            code='$'.join(pieces).strip()
            marker(code,'format',lineno)
            if not code or unclosed:issues.append({'code':'malformed_format_record','line':lineno})
            elif code.startswith('('):counts['fortran_format_candidates']+=1
            else:counts['c_format_candidates']+=1
            pending=None;continue
        for segment_index,segment in enumerate(pieces,1):
            segment=segment.strip()
            if not segment:continue
            counts['nonempty_segments']+=1
            token,arguments=first_field(segment)
            token=token.upper()
            if token=='/COM':
                commands[token]+=1;counts['comment_commands']+=1
                marker(arguments,'comment',lineno,segment_index);continue
            marker(segment,'code',lineno,segment_index)
            if unclosed:
                counts['uninterpreted_quote_segments']+=1;continue
            if segment.startswith('('):
                counts['standalone_format_records']+=1;continue
            if not token or NUM.fullmatch(token) or all(NUM.fullmatch(t) for t in token.split()):counts['numeric_data_segments']+=1;continue
            if '=' in token:
                counts['parameter_assignment_segments']+=1;continue
            if not TOKEN.fullmatch(token):
                commands['hash:'+sha_bytes(token.encode('latin-1'))]+=1
                counts['unknown_token_segments']+=1;continue
            commands[token if token in VOCAB else 'hash:'+sha_bytes(token.encode('latin-1'))]+=1
            counts['command_starts']+=1
            if token not in VOCAB:counts['unknown_command_starts']+=1
            if token in OPERATIONS:
                need(len(operations)<OP_CAP,'operation_locator_cap',source,lineno)
                operations.append({'line':lineno,'segment':segment_index,'command':token,'role':VOCAB[token],
                                   'arguments_sha256':sha_bytes(arguments.encode('latin-1'))})
            if token in FORMAT_COMMANDS:
                pending=token
                if segment_index<len(pieces):issues.append({'code':'format_command_condensed','line':lineno})
            args=[p.strip().upper() for p in arguments.split(',')]
            if token in ('BF','BFE','D') and len(args)>1 and args[1]=='TEMP':counts[token+'_TEMP_label']+=1
            if token in ('BFUNIF','LDREAD') and args and args[0]=='TEMP':counts[token+'_TEMP_label']+=1
    if pending is not None:issues.append({'code':'missing_format_record','line':len(lines)})
    rows=[]
    for token,n in sorted(commands.items()):
        if token.startswith('hash:'):rows.append({'token_sha256':token[5:],'name':None,'role':'unknown','count':n})
        else:rows.append({'token_sha256':sha_bytes(token.encode('ascii')),'name':token,'role':VOCAB[token],'count':n})
    return {**base,'status':'lexical','counts':dict(sorted(counts.items())),'commands':rows,
            'operations':operations,'markers':markers,'issues':issues}


def read_body(f,source,expected_size=None,expected_crc=None):
    h=hashlib.sha256(); crc=0; parts=[]; size=0
    rec={'source':source,'bytes_read':0,'eof':False}
    PROGRESS.append(rec)
    try:
        while True:
            b=f.read(65536)
            if not b:break
            size+=len(b);rec['bytes_read']=size
            need(size<=MEMBER_CAP,'member_cap',source)
            h.update(b);crc=zlib.crc32(b,crc);parts.append(b)
    except zipfile.BadZipFile:
        raise AuditError('archive_crc_or_structure',source) from None
    rec.update(eof=True,sha256=h.hexdigest(),crc32=crc&0xffffffff)
    need(expected_size is None or size==expected_size,'member_size',source)
    need(expected_crc is None or rec['crc32']==expected_crc,'member_crc',source)
    return b''.join(parts),rec


def approved_apdl():
    need(sha_file(MANIFEST)==MANIFEST_SHA,'manifest_pin')
    with MANIFEST.open(newline='') as f:rows=list(csv.DictReader(f))
    selected=[r for r in rows if r['extension'].lower()=='.apdl']
    need([r['sha256'] for r in selected]==APDL_SHAS,'apdl_manifest_selection')
    paths=[]
    for i,r in enumerate(selected,1):
        p=(RAW/r['relative_path']).resolve()
        need(p.is_relative_to(RAW.resolve()) and p.is_file(),'apdl_path_boundary','APDL%02d'%i)
        paths.append((p,r))
    return paths


def source_pins(paths):
    need(sha_file(MANIFEST)==MANIFEST_SHA,'manifest_pin')
    need(ZIP.stat().st_size==86819483 and sha_file(ZIP)==ZIP_SHA,'zip_pin')
    result={'manifest':MANIFEST_SHA,'zip':ZIP_SHA,'apdl':{}}
    for i,(p,r) in enumerate(paths,1):
        got=sha_file(p);need(got==r['sha256'] and p.stat().st_size==int(r['size_bytes']),'apdl_pin','APDL%02d'%i)
        result['apdl']['APDL%02d'%i]={'bytes':p.stat().st_size,'sha256':got}
    return result


def scan():
    paths=approved_apdl();before=source_pins(paths);files=[];total=0
    for i,(p,r) in enumerate(paths,1):
        alias='APDL%02d'%i
        with p.open('rb') as f:data,receipt=read_body(f,alias,int(r['size_bytes']))
        total+=len(data);need(total<=TOTAL_CAP,'aggregate_cap',alias)
        files.append({'source':alias,'source_kind':'apdl','name_sha256':sha_bytes(r['relative_path'].encode('utf-8')),
                      'receipt':receipt,'lexical':lexical(data,alias)})
    metadata=[];names=Counter();archivebytes=0
    with zipfile.ZipFile(ZIP) as z:
        entries=z.infolist();need(len(entries)<=ENTRY_CAP,'entry_cap')
        for ordinal,entry in enumerate(entries,1):
            alias='ZIP%05d'%ordinal;namehash=sha_bytes(entry.filename.encode('utf-8'));names[namehash]+=1
            mode=entry.external_attr>>16
            directory=entry.is_dir();png=not directory and entry.filename.lower().endswith('.png')
            need(directory or stat.S_IFMT(mode) in (0,stat.S_IFREG),'nonregular_zip_member',alias)
            meta={'source':alias,'name_sha256':namehash,'bytes':entry.file_size,'compressed_bytes':entry.compress_size,
                  'crc32':entry.CRC,'directory':directory,'png':png,'compression':entry.compress_type}
            metadata.append(meta)
            if directory or png:continue
            need(entry.file_size<=MEMBER_CAP,'member_cap',alias)
            with z.open(entry) as f:data,receipt=read_body(f,alias,entry.file_size,entry.CRC)
            total+=len(data);archivebytes+=len(data);need(total<=TOTAL_CAP,'aggregate_cap',alias)
            files.append({'source':alias,'source_kind':'archive','name_sha256':namehash,'receipt':receipt,'lexical':lexical(data,alias)})
    after=source_pins(paths);need(after==before,'changed_source_pins')
    totals=Counter();token_totals=Counter();role_totals=Counter();marker_totals=Counter()
    for f in files:
        lex=f['lexical'];totals[lex['status']+'_files']+=1;totals['physical_lines']+=lex['physical_lines']
        if lex['status']=='lexical':
            totals.update(lex['counts'])
            for row in lex['commands']:token_totals[row['token_sha256']]+=row['count'];role_totals[row['role']]+=row['count']
            for m in lex['markers']:marker_totals[m['context']+':'+m['marker']]+=1
    return {'pins_before':before,'pins_after':after,'files':files,'archive_metadata':metadata,
            'census':{'entries':len(metadata),'directories':sum(m['directory'] for m in metadata),
                      'regular_entries':sum(not m['directory'] for m in metadata),'png_entries':sum(m['png'] for m in metadata),
                      'archive_nonpng_bytes':archivebytes,'all_body_bytes':total,'apdl_files':len(paths),
                      'duplicate_name_groups':sum(n>1 for n in names.values()),'extra_duplicate_name_entries':sum(n-1 for n in names.values())},
            'totals':dict(totals),'command_hash_totals':dict(token_totals),'role_totals':dict(role_totals),'marker_totals':dict(marker_totals)}


def controls():
    names=[]
    def ok(name,value):need(value,'control_'+name);names.append(name)
    def reject(name,fn,code):
        try:fn()
        except AuditError as e:ok(name,e.code==code)
        else:raise AuditError('control_expected_rejection_'+name)
    def lex(b):return lexical(b,'SYNTHETIC')
    def count(x,n):return sum(r['count'] for r in x['commands'] if r['name']==n)
    x=lex(b'BF,1,TEMP,25 ! BF,2,TEMP,30\n! /INPUT,hidden\n')
    ok('comments',count(x,'BF')==1 and x['counts']['comment_only_lines']==1)
    ok('empty_comment',lex(b'!\n')['counts']['comment_only_lines']==1)
    x=lex(b"*CFOPEN,'x!y$z',txt $ BF,1,TEMP,2\n")
    ok('quoted_delimiters',count(x,'*CFOPEN')==1 and count(x,'BF')==1 and len(x['operations'])==1)
    x=lex(b"*CFOPEN,'x''!$y',txt\n")
    ok('doubled_quote',len(x['operations'])==1 and not x['issues'])
    x=lex(b'BFE,1,TEMP,1,25\nBFEEXTRA,1,TEMP,1,25\nBF=3\n')
    ok('full_token',count(x,'BFE')==1 and count(x,'BF')==0 and x['counts']['unknown_command_starts']==1)
    x=lex(b"*VWRITE,'*LOAD_THERMAL_VARIABLE_NODE'\n('*LOAD_THERMAL_VARIABLE_NODE')\n/COM,*LOAD_THERMAL_VARIABLE_NODE\n! WTC7_CaseB_400pm\n")
    ok('format_and_marker_context',x['counts']['format_records']==1 and Counter(m['context'] for m in x['markers'])=={'code':1,'format':1,'comment':2})
    ok('quoted_marker_not_command',sum(r['name']=='*LOAD_THERMAL_VARIABLE_NODE' for r in x['commands'])==0)
    x=lex(b"*VWRITE,1\nBF,1,TEMP,1\n")
    ok('immediate_c_format',count(x,'BF')==0 and x['counts']['c_format_candidates']==1)
    x=lex(b'*VREAD,X\n\nBF,1,TEMP,2\n')
    ok('empty_format_explicit',count(x,'BF')==1 and any(r['code']=='malformed_format_record' for r in x['issues']))
    ok('missing_format',lex(b'*VWRITE,1')['issues']==[{'code':'missing_format_record','line':1}])
    x=lex(b'BF,1,TEMP,2\n\x00BF,2,TEMP,3\n')
    ok('nul_discards_all_semantics',x['status']=='uninterpreted_nul' and x['commands'] is None)
    x=lex(b'! *LOAD_THERMAL_VARIABLE_NODE_EXTRA\n/COM,WTC7_CaseB_400pmOTHER\n')
    ok('marker_full_token',not x['markers'])
    x=lex(b"*CFOPEN,'%prefix%_400pm',txt\n")
    ok('dynamic_not_invented_literal',not x['markers'] and count(x,'*CFOPEN')==1)
    reject('line_cap',lambda:lex(b'A'*(LINE_CAP+1)),'line_cap')
    reject('member_cap',lambda:read_body(io.BytesIO(b'A'*(MEMBER_CAP+1)),'SYNTHETIC'),'member_cap')
    def small_operation_cap():
        global OP_CAP
        old=OP_CAP
        try:
            OP_CAP=1
            lex(b'/INPUT,x\n/INPUT,y\n')
        finally:OP_CAP=old
    reject('operation_locator_cap',small_operation_cap,'operation_locator_cap')
    x=lex(b'1,2,3\n-1.2E+3,4\nUNKNOWNOP,abc\n')
    ok('numeric_unknown',x['counts']['numeric_data_segments']==2 and x['commands'][0]['name'] is None)
    ok('numeric_whitespace',lex(b'1.0 2.0 3.0\n')['counts']['numeric_data_segments']==1)
    x=lex(b"*CFOPEN,'unfinished\n")
    ok('unclosed_quote',len(x['issues'])==1 and not x['operations'])
    archive=io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
            z.writestr('same',b'BF,1,TEMP,2\n');z.writestr('same',b'BF,2,TEMP,3\n')
    with zipfile.ZipFile(io.BytesIO(archive.getvalue())) as z:
        infos=z.infolist();bodies=[read_body(z.open(i),'SYNTHETIC',i.file_size,i.CRC)[0] for i in infos]
    ok('duplicate_names_by_ordinal',len(bodies)==2 and bodies[0]!=bodies[1])
    damaged=bytearray(archive.getvalue());name_len,extra_len=struct.unpack_from('<HH',damaged,26);damaged[30+name_len+extra_len]^=1
    def crc_failure():
        with zipfile.ZipFile(io.BytesIO(damaged)) as z:
            with z.open(z.infolist()[0]) as f:read_body(f,'SYNTHETIC')
    reject('archive_crc',crc_failure,'archive_crc_or_structure')
    PROGRESS.clear()
    return {'passed':len(names),'groups':names}


# INDEPENDENT_CORE_END

INDEPENDENT_SHA='20b397590bc7d2831fdc0230f045c1d42fe4a68b1f35ff1345cfea9c1eb3eab9'
CORE_SHA='0aff3dc9d8084b3b3002d3588e74c2cc61202e01f6def6ac8e5e8f5015424f9b'
ROOT_SHA='4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117'
ROOT_CODE_SHA='c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53'


def compare_frozen():
    """Post-schema comparisons only; no additional historical body inspection."""
    inputs={'independent':BASE/'independent01.json','root':BASE/'run01.json','root_code':BASE/'scan_transfer.py'}
    pins={k:sha_file(p) for k,p in inputs.items()}
    need(pins=={'independent':INDEPENDENT_SHA,'root':ROOT_SHA,'root_code':ROOT_CODE_SHA},'comparison_input_pins')
    need(sha_bytes(Path(__file__).read_bytes().split(b'# INDEPENDENT_CORE_END')[0])==CORE_SHA,'core_changed')
    own_doc=json.loads(inputs['independent'].read_text());root_doc=json.loads(inputs['root'].read_text())
    own=own_doc['result'];root=root_doc['result'];counts=Counter();failures=[];vocab_differences=[];line_differences=[];argument_hash_differences=[]
    def same(got,want,path):
        if type(got) is bool or type(want) is bool:kind='boolean'
        elif type(got) is int and type(want) is int:kind='integer'
        else:kind='value'
        counts[kind]+=1
        if type(got) is not type(want) or got!=want:failures.append({'path':path,'code':'not_equal'})
    same(own_doc['receipt']['status'],'PASS','independent_status');same(root_doc['status'],'PASS','root_status')
    same(root_doc['protocol_sha256'],PROTOCOL_SHA,'protocol');same(root_doc['code_sha256'],ROOT_CODE_SHA,'root_code')
    same(root['manifest_sha256'],MANIFEST_SHA,'manifest');same(root['zip_sha256'],ZIP_SHA,'zip')
    same(root['source_pins_after'],True,'root_pin_after');same(own['pins_before'],own['pins_after'],'independent_pin_stability')
    coverage={'body_read':len(own['files'])-3,'directories':own['census']['directories'],'entries':own['census']['entries'],
              'files':own['census']['regular_entries'],'png_excluded':own['census']['png_entries']}
    for k,v in coverage.items():same(root['coverage'][k],v,'coverage.'+k)
    same(root['total_read_bytes'],own['census']['all_body_bytes'],'total_read_bytes')
    body={f['source']:f for f in own['files']};meta={f['source']:f for f in own['archive_metadata'] if not f['directory']}
    expected_aliases=set(body)|set(meta);actual_aliases=[r['alias'] for r in root['records']]
    same(len(actual_aliases),len(set(actual_aliases)),'root_alias_unique');same(sorted(actual_aliases),sorted(expected_aliases),'alias_coverage')
    known_comparisons=operation_count=lexical_files=nul_files=0
    for r in root['records']:
        alias=r['alias'];s=r['scan'];b=body.get(alias);m=meta.get(alias)
        same(r['name_sha256'],(b or m)['name_sha256'],alias+'.name_hash')
        if m:
            same(r['declared_bytes'],m['bytes'],alias+'.declared_bytes');same(r['declared_crc32'],m['crc32'],alias+'.declared_crc')
        if b is None:
            same(s['status'],'pixels_not_read',alias+'.png_status');same(m['png'],True,alias+'.png_metadata');continue
        l=b['lexical'];receipt=b['receipt']
        for field,want in [('bytes',receipt['bytes_read']),('sha256',receipt['sha256']),('lines',l['physical_lines']),('nul_bytes',l['nul_bytes'])]:same(s[field],want,alias+'.'+field)
        same(receipt['eof'],True,alias+'.independent_eof')
        if m:same(r['crc_eof_pass'],True,alias+'.root_crc');same(receipt['crc32'],m['crc32'],alias+'.independent_crc')
        if l['status']=='uninterpreted_nul':
            nul_files+=1;same(s['status'],'nul_semantics_excluded',alias+'.nul_status')
            for key in ('commands','unknown_tokens','operations','markers','thermal_labels'):same(bool(s.get(key)),False,alias+'.nul_exclusion.'+key)
            continue
        lexical_files+=1;same(s['status'],'lexical',alias+'.lexical_status')
        our_tokens={x['token_sha256']:x['count'] for x in l['commands']}
        root_tokens=dict(s['unknown_tokens'])
        for token,n in s['commands'].items():
            h=sha_bytes(token.encode('ascii'));root_tokens[h]=root_tokens.get(h,0)+n
            same(our_tokens.get(h,0),n,alias+'.known_command.'+h);known_comparisons+=1
        differences=[{'token_sha256':h,'root':root_tokens.get(h,0),'independent':our_tokens.get(h,0)} for h in sorted(set(root_tokens)|set(our_tokens)) if root_tokens.get(h,0)!=our_tokens.get(h,0)]
        if differences:vocab_differences.append({'source':alias,'differences':differences})
        rootops=s['operations'];ops=l['operations'];same(len(rootops),len(ops),alias+'.operation_count')
        for i,(rop,op) in enumerate(zip(rootops,ops)):
            for key in ('line','segment','command'):same(rop[key],op[key],alias+'.operation.'+str(i)+'.'+key)
            operation_count+=1
            if rop['arguments_sha256']!=op['arguments_sha256']:
                argument_hash_differences.append({'source':alias,'line':op['line'],'segment':op['segment'],'root':rop['arguments_sha256'],'independent':op['arguments_sha256']})
        expected_labels={key.replace('_TEMP_label',':TEMP'):n for key,n in l['counts'].items() if key.endswith('_TEMP_label') and key.startswith(('BF_','BFE_'))}
        same(s['thermal_labels'],expected_labels,alias+'.thermal_labels')
        same(s['markers'],[],alias+'.root_markers');same(l['markers'],[],alias+'.independent_markers')
        same(s['lexical_flags'],{},alias+'.root_flags');same(l['issues'],[],alias+'.independent_issues')
        kinds=s['line_kinds']
        for key,ownkey in [('blank_lines','blank_lines'),('bang_comment_only_lines','comment_only_lines'),('com_comment_segments','comment_commands')]:same(kinds.get(key,0),l['counts'].get(ownkey,0),alias+'.'+key)
        for key,ownkey in [('lines_with_bang_comment','lines_with_comment'),('numeric_data_segments','numeric_data_segments')]:
            if kinds.get(key,0)!=l['counts'].get(ownkey,0):line_differences.append({'source':alias,'field':key,'root':kinds.get(key,0),'independent':l['counts'].get(ownkey,0)})
    for token,n in root['commands'].items():same(own['command_hash_totals'].get(sha_bytes(token.encode('ascii')),0),n,'aggregate_command.'+sha_bytes(token.encode('ascii')))
    same(root['thermal_labels'],{'BF:TEMP':own['totals']['BF_TEMP_label'],'BFE:TEMP':own['totals']['BFE_TEMP_label']},'aggregate_thermal_labels')
    same(root['markers'],[],'aggregate_markers');same(root['lexical_flags'],{},'aggregate_flags')
    same({k:sha_file(p) for k,p in inputs.items()},pins,'unchanged_derivatives')
    return {'status':'FAIL' if failures else 'PASS_COMPARABLE_SCOPE','comparison_counts':dict(counts),'failures':failures,
        'coverage':{'regular_records_plus_apdl':len(actual_aliases),'lexical_files':lexical_files,'nul_excluded_files':nul_files,
                    'png_metadata_only':coverage['png_excluded'],'operation_locators':operation_count,'perfile_recognized_command_counts':known_comparisons,
                    'body_bytes':own['census']['all_body_bytes']},
        'vocabulary_token_differences':vocab_differences,'line_counter_differences':line_differences,
        'argument_hash_recipe_differences':argument_hash_differences,
        'pins':pins,'core_sha256':CORE_SHA,
        'limits':['No new historical source body was reread for this comparison.',
                  'Root hashes operation suffix including the command delimiter; independent hashes argument tail excluding delimiter. Hash pairs are preserved, not asserted equivalent or independently rehashed to a common recipe.',
                  'Known command counts, operation locators, thermal labels, file hashes/bytes/lines/NUL and CRC evidence are compared; complete tokenizer equivalence is not claimed.',
                  'The root nonempty-comment counter excludes empty comment tails; independent counts every outside-quote comment delimiter. Numeric-data and unknown-token classifications also differ.',
                  'Root filename-shape classes/case labels are not independently reconstructed here; alias/name-hash identity is checked.',
                  'Neither lexer executes macros, resolves dynamic output names, authenticates historical dataflow or proves exporter absence.']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--controls-only',action='store_true');p.add_argument('--compare',action='store_true');p.add_argument('--output',default='independent01.json');a=p.parse_args()
    need(not(a.controls_only and a.compare),'exclusive_mode')
    need(bool(re.fullmatch(r'independent(?:[0-9]{2}|-(?:controls|failed|comparison)[0-9]{2})\.json',a.output)),'output_name')
    output=BASE/a.output;need(not output.exists(),'output_exists')
    start=time.monotonic();receipt={'command':sys.argv,'python':sys.version.split()[0],'code_sha256':sha_file(__file__),
        'core_sha256':sha_bytes(Path(__file__).read_bytes().split(b'# INDEPENDENT_CORE_END')[0]),'protocol_sha256':PROTOCOL_SHA}
    try:
        need(sha_file(BASE/'PROTOCOL.md')==PROTOCOL_SHA,'protocol_pin')
        receipt['controls']=controls();result=None if a.controls_only else compare_frozen() if a.compare else scan()
        receipt.update(status='FAIL' if a.compare and result['status']=='FAIL' else 'PASS',seconds=round(time.monotonic()-start,6),peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        need(receipt['peak_rss_bytes']<=MEM_CAP,'memory_cap')
    except (AuditError,OSError,ValueError,zipfile.BadZipFile,MemoryError) as e:
        receipt.update(status='FAIL',seconds=round(time.monotonic()-start,6),peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            error={'code':e.code,'source':e.source,'line':e.line} if isinstance(e,AuditError) else {'code':'runtime_'+type(e).__name__},progress=PROGRESS)
        result=None
        if not a.controls_only and re.fullmatch(r'independent[0-9]{2}\.json',output.name):output=BASE/output.name.replace('independent','independent-failed',1)
    with output.open('x') as f:json.dump({'receipt':receipt,'result':result},f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'status':receipt['status'],'output':output.name,'sha256':sha_file(output),'seconds':receipt['seconds'],'controls':receipt.get('controls'),'error':receipt.get('error')}))
    return 0 if receipt['status']=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except (AuditError,OSError,ValueError) as e:
        print(json.dumps({'status':'FAIL','code':e.code if isinstance(e,AuditError) else 'runtime_'+type(e).__name__}));raise SystemExit(1)
