#!/usr/bin/env python3
"""Minimized follow-up, not an APDL interpreter or executable dependency graph."""
import argparse
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re
import resource
import sys
import time
import unittest
import zipfile
import scan_transfer as base

HERE = Path(__file__).resolve().parent
ROOT_SHA = 'c6e69416a50a20a26ac15da70fdd3cc6fb56178c07b50a35c06b4b3fb6c3cd53'
RUN_SHA = '4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117'
EXTRA = set('''A K L AL LARC LSTR BSPLIN FLST FITEM P51X AATT LATT KATT
LESIZE AESIZE ESIZE AMESH LMESH KMESH ARSYM ASYM ARSCALE ARTRAN AGLUE AADD
ASBA ASBL ASBW ASBV ASUB AOVLAP AROTAT AGEN ADELE ASUM ATAN ANORM AREVERSE
ASEL VSEL KSEL LSEL V VEXT VATT VDRAG VMESH VSWEEP VOVLAP VGLUE VADD VGEN
VDELE VSBV VSBA VSBW VROTAT VTRAN VSCALE VSUM LSLA NSLA NSLL LSSEL KSLN
KSLL KSL LDELE KDELE LANG LTAN LCOMB LDIV LSBL LSLK LSSCALE LTRAN
/PNUM /PBC /PSF /PLOPTS /TRIAD /GFILE /NUMBER /REPLOT /COLOR /DEVICE /ERASE
/RESET /UIS /UI /MENU /UNIT /UNITS /PMACRO /UCMD /PSEARCH /MKDIR /COPY
/RENAME /DELETE /ASSIGN /WAIT /GO /REP *ASK *MSG *ABBR *AFUN *REPEAT
*CFCLOSE *VITRP *VPUT BOPT BTOL ASOL NCNV NLDIAG RESCONTROL MONITOR PRED
LNSRCH STABILIZE SSTIF SABS SFGRAD FCUM DCUM LSCLEAR LSDELE LSREAD
CLOCAL LOCAL WPCSYS WPOFFS WPROTA WPLAN MSHKEY MSHAPE MSHMID MSHCOPY NUMOFF
SFDELE SFEDELE EINTF EALIVE EKILL /AUX2 /AUX12 /AUX15 /POST7 /POSTTS /RUNST
RLIST PRERR PRENERGY /EXPAND /CPLANE CKEY CEDELE CPDELE CESEL CPSEL ARCLEN
ARCTRM SLOAD SFCUM SFECUM SFTRAN /GST /FILNAM MOVE MV'''.split())
ASSIGN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*(?:\([^=]*\))?\s*=')
PUNCT = set('* / , ; : ( )'.split())
CONTEXT = {'alias':None,'line':0,'completed':0}
INDEX_CACHE = None

def candidate_index(inventory):
    global INDEX_CACHE
    if INDEX_CACHE is not None and INDEX_CACHE[0] is inventory:
        return INDEX_CACHE[1], INDEX_CACHE[2]
    by_name={};parents={}
    for alias,name in inventory.items():
        path=PurePosixPath(name)
        by_name.setdefault(path.name,[]).append(alias)
        parents[alias]=str(path.parent)
    INDEX_CACHE=(inventory,by_name,parents)
    return by_name,parents

def fields(s):
    result=[]; part=[]; quote=None; i=0
    while i<len(s):
        ch=s[i]
        if quote:
            part.append(ch)
            if ch==quote:
                if i+1<len(s) and s[i+1]==quote:
                    part.append(s[i+1]); i+=1
                else: quote=None
        elif ch in "\"'": quote=ch;part.append(ch)
        elif ch==',': result.append(''.join(part).strip());part=[]
        else: part.append(ch)
        i+=1
    base.need(quote is None,'unclosed_field_quote')
    result.append(''.join(part).strip())
    return result

def unquote(v):
    if len(v)>=2 and v[0] in "\"'" and v[-1]==v[0]:
        return v[1:-1].replace(v[0]*2,v[0])
    return v

def arg_role(s, alias, name, inventory):
    f=fields(s); args=[unquote(v) for v in f[1:]]
    filename=args[0] if args else ''
    extension=args[1] if len(args)>1 else ''
    directory=args[2] if len(args)>2 else ''
    dyn=any('%' in a for a in args)
    pathlike=any(c in filename for c in '/\\') or bool(directory)
    key=filename+('.'+extension if extension else '')
    literal=bool(filename) and not dyn and not pathlike
    candidates=[]; same=[]
    if literal:
        by_name,parents=candidate_index(inventory)
        candidates=by_name.get(key,[])
        if alias.startswith('ZIP'):
            parent=str(PurePosixPath(name).parent)
            same=[a for a in candidates if a.startswith('ZIP') and parents[a]==parent]
    return {'field_count':len(args),'field_hashes':[base.sha(v.encode('latin-1')) for v in f[1:]],
            'extension_class':extension.lower() if extension.lower() in ('','int','apdl','txt','out','log','k') else 'other',
            'dynamic_percent_syntax':dyn,'path_or_directory_present':pathlike,
            'literal_basename_candidate_search':literal,
            'exact_basename_candidates':candidates,'same_archive_parent_candidates':same}

def classify_segment(s, token):
    if ASSIGN.match(s): return 'parameter_assignment'
    if s in PUNCT: return 'standalone_punctuation'
    if token in EXTRA: return 'supplemental_vocabulary'
    return 'unresolved'

def inspect_body(data, alias, name, inventory):
    base.need(b'\x00' not in data,'nul_semantics_excluded')
    result={'unknown':[],'unresolved_segments':[],'operations':[]}
    pending=False
    for lineno,raw in enumerate(data.split(b'\n'),1):
        CONTEXT['line']=lineno
        text=raw.rstrip(b'\r').decode('latin-1')
        parts,comment,unclosed=base.split_line(text)
        base.need(not unclosed,'unclosed_quote')
        if pending: pending=False;continue
        for segno,part in enumerate(parts,1):
            s=part.strip()
            if not s:continue
            m=base.TOKEN.match(s);token=m[1].upper() if m else None
            if token=='/COM':continue
            loc={'line':lineno,'segment':segno}
            if token and token not in base.VOCAB:
                kind=classify_segment(s,token)
                row={**loc,'token_sha256':base.sha(token.encode('ascii')),'class':kind}
                if kind=='supplemental_vocabulary':row['command']=token
                if token=='MV':row['whitespace_token_count']=len(s.split())
                result['unknown'].append(row)
            elif not token and not base.NUMERIC_START.match(s):
                result['unresolved_segments'].append({**loc,'class':classify_segment(s,token),'segment_sha256':base.sha(s.encode('latin-1'))})
            if token in ('/INPUT','/OUTPUT'):
                result['operations'].append({**loc,'command':token,'arguments_sha256':base.sha(s[len(m[1]):].encode('latin-1')),
                                              **arg_role(s,alias,name,inventory)})
            if token in base.FORMAT_COMMANDS:pending=True
    return result

class Controls(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(fields("/INPUT,'a,b',int"),['/INPUT',"'a,b'",'int'])
        self.assertEqual(unquote("'a''b'"),"a'b")
        with self.assertRaises(base.ScanError):fields("/INPUT,'a")
    def test_candidates(self):
        inv={'ZIP00001':'CaseA_Temps/a.int','ZIP00002':'CaseB_Temps/a.int'}
        r=arg_role('/INPUT,a,int','ZIP00003','CaseA_Temps/driver.int',inv)
        self.assertEqual(len(r['exact_basename_candidates']),2)
        self.assertEqual(r['same_archive_parent_candidates'],['ZIP00001'])
        self.assertFalse(arg_role('/INPUT,%a%,int','x','x',inv)['literal_basename_candidate_search'])
        self.assertFalse(arg_role('/INPUT,a,int,folder','x','x',inv)['literal_basename_candidate_search'])
    def test_assignments(self):
        for s in ('name = 4','name(2) = 4','name=4'):
            self.assertEqual(classify_segment(s,None),'parameter_assignment')
        self.assertEqual(classify_segment('*',None),'standalone_punctuation')
        self.assertEqual(classify_segment('hidden,4','HIDDEN'),'unresolved')
    def test_suppression(self):
        r=inspect_body(b'private_name = 4\nhidden,4\n*\nK,1,2,3\n','TEST','x',{})
        self.assertNotIn('private_name',json.dumps(r))
        self.assertNotIn('hidden',json.dumps(r))
        self.assertEqual(r['unknown'][0]['class'],'parameter_assignment')
        self.assertEqual(r['unknown'][2]['command'],'K')
    def test_nul(self):
        with self.assertRaises(base.ScanError):inspect_body(b'BF,1,TEMP,2\n\x00','TEST','x',{})
    def test_index_equivalence(self):
        inv={'ZIP00001':'CaseA/x.int','ZIP00002':'CaseB/x.int','ZIP00003':'CaseA/y.int'}
        index,parents=candidate_index(inv)
        for key in ('x.int','y.int','absent.int'):
            self.assertEqual(index.get(key,[]),[a for a,n in inv.items() if PurePosixPath(n).name==key])
        self.assertEqual(parents['ZIP00001'],'CaseA')

def historical():
    base.need(base.file_sha(HERE/'scan_transfer.py')==ROOT_SHA,'root_code_pin')
    base.need(base.file_sha(HERE/'run01.json')==RUN_SHA,'root_result_pin')
    frozen=json.loads((HERE/'run01.json').read_text())['result']
    selected=[r for r in frozen['records'] if r['scan'].get('operations') or r['scan'].get('unknown_tokens') or r['scan'].get('line_kinds',{}).get('noncommand_unresolved_segments')]
    apdl=base.selected_apdl()
    base.need(base.file_sha(base.ZIP)==base.ZIP_SHA,'zip_pin')
    inventory={f'APDL{i:02d}':r['relative_path'] for i,r in enumerate(apdl,1)}
    output=[];total=0
    with zipfile.ZipFile(base.ZIP) as z:
        infos=z.infolist()
        inventory.update({f'ZIP{i:05d}':n.filename for i,n in enumerate(infos,1) if not n.is_dir()})
        for rec in selected:
            alias=rec['alias'];CONTEXT.update(alias=alias,line=0)
            if alias.startswith('APDL'):
                data=(base.BASE/inventory[alias]).read_bytes()
            else:
                info=infos[int(alias[3:])-1]
                with z.open(info) as f:
                    data=f.read(base.MEMBER_CAP+1);base.need(not f.read(1),'member_eof')
            total+=len(data);base.need(total<=base.TOTAL_CAP,'total_cap')
            base.need(len(data)<=base.MEMBER_CAP and base.sha(data)==rec['scan']['sha256'],'body_pin')
            result=inspect_body(data,alias,inventory[alias],inventory)
            base.need(Counter(r['token_sha256'] for r in result['unknown'])==Counter(rec['scan']['unknown_tokens']),'unknown_locator_count')
            base.need(len(result['unresolved_segments'])==rec['scan']['line_kinds'].get('noncommand_unresolved_segments',0),'unresolved_locator_count')
            expected=[v for v in rec['scan']['operations'] if v['command'] in ('/INPUT','/OUTPUT')]
            actual=[{k:r[k] for k in ('line','segment','command','arguments_sha256')} for r in result['operations']]
            base.need(actual==expected,'operation_locator_join')
            output.append({'alias':alias,'class':rec['class'],'case':rec['case'],'sha256':rec['scan']['sha256'],**result})
            CONTEXT['completed']+=1
    base.selected_apdl();base.need(base.file_sha(base.ZIP)==base.ZIP_SHA,'zip_pin_after')
    return {'selected_files':len(selected),'read_bytes':total,'records':output,'source_pins_after':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--controls',action='store_true');args=p.parse_args()
    t=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    if not t.wasSuccessful():return 1
    if args.controls:return 0
    dest=HERE/(args.output or '')
    base.need(args.output and dest.parent==HERE and not dest.exists(),'create_only_output')
    receipt={'code_sha256':base.file_sha(Path(__file__)),'protocol_sha256':base.file_sha(HERE/'DETAIL-PROTOCOL.md'),'root_code_sha256':ROOT_SHA,'root_result_sha256':RUN_SHA,'python':sys.version,'command':sys.argv,'controls':t.testsRun}
    start=time.monotonic()
    try:
        result=historical();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        base.need(peak<=768*1024**2,'memory_cap')
        receipt.update(status='PASS',result=result,peak_memory_bytes=peak)
    except (Exception, KeyboardInterrupt) as e:
        receipt.update(status='FAIL',code=e.code if isinstance(e,base.ScanError) else type(e).__name__,progress=CONTEXT.copy())
    receipt['seconds']=time.monotonic()-start
    with dest.open('x') as f:json.dump(receipt,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({k:receipt[k] for k in ('status','seconds')}))
    return 0 if receipt['status']=='PASS' else 1

if __name__=='__main__':
    try:sys.exit(main())
    except base.ScanError as e:print(json.dumps({'status':'REFUSED','code':e.code}));sys.exit(2)
