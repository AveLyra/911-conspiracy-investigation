#!/usr/bin/env python3
"""Independent streaming, numeric-only property/ID audit. Never a solver."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import resource
import sys
import time

HERE = Path(__file__).resolve().parent
RAW = Path('/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653')
PROTOCOL_SHA = '4406af3500c495adc95edd1c86e07901f73e6cafa43a39bfc57a8920c34c552a'
PINS = {
    116: ('Damage_Global_ANSYS_CaseB_4.0hr.k.gz',5331,'982a0e4728ec54f84c44bf364ec34cae5f731e66da4bfad40a4b85ca4bd751da',17314,'876066eb62e4c849c6bb9fb1598cc0be8b700843483a6ddd3cf6aa9847ad2455'),
    119: ('discrete_mass.k.gz',70199,'2c3c350317f0c06c2aca2e9d9ae1e9b489d4a1c44c9268997e550d35c031d7d7',508372,'8e1c2c5e101ed133411acd905079fb128579ab48a591b508b8e9883fc7038601'),
    120: ('elem_thick_to-renum.k.gz',23162693,'c49dcb74d8559e0cbfa4302732dd2c1764bf161389be0ee8e8c3d9a3dbc55e59',232959541,'7ac5918eb9eb2368cffc84aeef29fb104314115cda5baab2a0b93788b46abfda'),
    121: ('wtc7_global_8a_no-conn-matl.k.gz',47520888,'f831290e6c0375dafc0bbeb684099d342ed8df29ab8560df82b21459c041483d',333947423,'8a00ca2ba51912837ff8960cdef2977d9cf4de3a7d2b13d8a4336c66ef5e4bbf'),
}
# Known aliases may identify a card without authorizing a body read.
INCLUDE_ALIASES = {v[0][:-3]: k for k,v in PINS.items()}
INCLUDE_ALIASES.update({'G6A_CaseA_El_Delete_List.k':117,'WTC7_CaseB_400pm.int':118})
MAT = set('MAT_PIECEWISE_LINEAR_PLASTICITY MAT_PLASTICITY_COMPRESSION_TENSION MAT_RIGID MAT_ELASTIC MAT_ELASTIC_VISCOPLASTIC_THERMAL MAT_SPRING_NONLINEAR_ELASTIC'.split())
SEC = set('SECTION_BEAM SECTION_SHELL SECTION_SOLID SECTION_DISCRETE'.split())
ELEM = {'ELEMENT_SHELL_THICKNESS':'shell','ELEMENT_BEAM':'beam','ELEMENT_DISCRETE':'discrete','ELEMENT_SOLID':'solid'}
SETS = {'SET_SHELL_LIST':'shell','SET_BEAM':'beam','SET_BEAM_LIST':'beam'}
OTHER = {'PART','INCLUDE','INCLUDE_TRANSFORM','KEYWORD','END','NODE','HOURGLASS'}
NUM = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eEdD][+-]?[0-9]+)?\Z')
INT = re.compile(r'[+-]?[0-9]+\Z')
CAP, LINE_CAP, MEM_CAP = 512*1024**2, 16384, 768*1024**2
PROGRESS = []
CONTEXT = {'source':0,'line':0}

class Stop(Exception):
    def __init__(self, code): self.code=code; super().__init__(code)
def need(ok, code):
    if not ok: raise Stop(code)
def digest(b): return hashlib.sha256(b).hexdigest()
def file_sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''): h.update(b)
    return h.hexdigest()
def pin_sources():
    r={}
    for src,(name,n,h,_,_) in PINS.items():
        p=RAW/name; got=file_sha(p)
        need(p.stat().st_size==n and got==h,'compressed_source_pin')
        r[src]={'bytes':n,'sha256':got}
    return r

def numeric(s):
    s=s.strip()
    if not s:return None
    need(NUM.fullmatch(s) is not None,'unsupported_numeric_token')
    n=Decimal(s.replace('D','E').replace('d','e'))
    need(n.is_finite(),'nonfinite_numeric_token')
    # Normalization stays a numeric string, avoiding binary-float precision loss.
    return str(n)
def integer(s, required=True):
    if s is None:
        need(not required,'missing_integer'); return None
    d=Decimal(s); need(d==d.to_integral_value(),'noninteger_id'); return int(d)
def fields(text,widths):
    text=text.split('$',1)[0].rstrip('\r\n')
    if ',' in text:
        parts=text.split(','); need(len(parts)<=len(widths),'too_many_csv_fields')
        parts += ['']*(len(widths)-len(parts))
    else:
        need(not text[sum(widths):].strip(),'fixed_field_overflow')
        parts=[];start=0
        for w in widths:parts.append(text[start:start+w]);start+=w
    return [numeric(p) for p in parts]
def ids(text,widths,required=()):
    v=fields(text,widths)
    return [integer(x,i in required) for i,x in enumerate(v)]
def effective(value,offset):
    return value+offset if value not in (None,0) else value
def append_unique(table,key,record,code):
    need(key not in table,code); table[key]=record

class Parser:
    def __init__(self):
        self.parts={};self.sections={};self.materials={};self.sets={};self.includes=[]
        self.counts=defaultdict(Counter);self.source_counts=defaultdict(Counter)
        self.seen={k:set() for k in ELEM.values()}
        self.damage_matches={'shell':[],'beam':[],'discrete':[],'solid':[]}
        self.damage_lookup={}
        self.metadata_blocks=[]

    def element(self,src,line,kind,v,offset,extra=None):
        eid,pid=v[:2];need(eid is not None and pid is not None,'element_required_id')
        need(eid>0 and pid>0,'nonpositive_element_id')
        need(eid not in self.seen[kind],'duplicate_element_family_id')
        self.seen[kind].add(eid)
        ep=pid+offset;self.counts[ep][kind]+=1;self.source_counts[src][kind]+=1
        targetkind='beam' if kind=='discrete' else kind
        lookupkey=(targetkind,2)
        if lookupkey not in self.damage_lookup:self.damage_lookup[lookupkey]=set(self.sets.get(lookupkey,{}).get('ids',[]))
        if eid in self.damage_lookup[lookupkey]:
            r={'source':src,'line':line,'kind':kind,'eid':eid,'raw_pid':pid,'effective_pid':ep,'numeric_connectivity_card':v}
            if extra is not None:r['numeric_continuation_card']=extra
            self.damage_matches[kind].append(r)

    def finish_block(self,block,src,offset):
        if block is None:return
        key=block['keyword']; cards=block['cards']
        if key=='PART':
            need(len(cards)==1,'part_card_count')
            v=cards[0]['values'];pid,sec,mid=[integer(x) for x in v[:3]]
            need(pid>0,'nonpositive_part_id')
            r={**block,'source':src,'raw_pid':pid,'effective_pid':pid+offset,
               'raw_secid':sec,'effective_secid':effective(sec,offset),
               'raw_mid':mid,'effective_mid':effective(mid,offset)}
            append_unique(self.parts,pid+offset,r,'duplicate_effective_part')
        elif key in SEC or key in MAT:
            need(cards and cards[0]['values'][0] is not None,'missing_property_id')
            ident=integer(cards[0]['values'][0]);need(ident>0,'nonpositive_property_id')
            r={**block,'source':src,'raw_id':ident,'effective_id':ident+offset}
            append_unique(self.sections if key in SEC else self.materials,ident+offset,r,'duplicate_effective_property')
        elif key=='INCLUDE_TRANSFORM':
            need(len(cards)==4,'transform_card_count')
            r={**block,'source':src};self.includes.append(r)
        elif key=='INCLUDE': self.includes.append({**block,'source':src})

    def parse(self,src,stream,offset=0):
        rec={'source':src,'bytes':0,'lines':0,'eof':False,'sha256':None};PROGRESS.append(rec)
        h=hashlib.sha256();known=Counter();unknown=Counter();key=None;kwline=0;block=None;pending=None;ordinal=0;setkey=None
        for raw in iter(lambda:stream.readline(LINE_CAP+1),b''):
            rec['lines']+=1;rec['bytes']+=len(raw);CONTEXT.update(source=src,line=rec['lines'])
            need(len(raw)<=LINE_CAP,'line_cap');need(rec['bytes']<=CAP,'file_cap');need(b'\0' not in raw,'nul_byte')
            h.update(raw)
            # Do not decode or display arbitrary comments/titles/filenames.
            strip=raw.strip()
            if strip.startswith(b'$'):continue
            if strip.startswith(b'*'):
                need(pending is None,'missing_element_continuation')
                self.finish_block(block,src,offset);block=None
                name=strip[1:].split(b'$',1)[0].strip()
                try:token=name.decode('ascii').upper()
                except UnicodeDecodeError: token=''
                if token in MAT|SEC|set(ELEM)|set(SETS)|OTHER:
                    key=token;known[key]+=1
                else:
                    unknown[digest(name.upper())]+=1;key=None
                    need(not token.startswith(('MAT_','SECTION_','PART_','ELEMENT_','INCLUDE')),'unsupported_required_keyword_variant')
                    need(not token.startswith('KEYWORD'),'unsupported_global_format')
                kwline=rec['lines'];ordinal=0;setkey=None
                if key in MAT|SEC|{'PART','INCLUDE','INCLUDE_TRANSFORM'}:
                    block={'keyword':key,'keyword_line':kwline,'cards':[]}
                continue
            if key is None:continue
            if not strip and key not in MAT|SEC|{'PART'}:continue
            ordinal+=1
            if key=='PART' and ordinal==1:
                block['title_sha256']=digest(raw.rstrip(b'\r\n'));continue
            if key in ('INCLUDE','INCLUDE_TRANSFORM') and ordinal==1:
                block['filename_sha256']=digest(strip)
                block['included_source']=next((i for n,i in INCLUDE_ALIASES.items() if strip==n.encode('ascii')),None)
                block['filename_line']=rec['lines'];continue
            if key in MAT|SEC|{'PART','INCLUDE_TRANSFORM'}:
                try:text=raw.decode('ascii')
                except UnicodeDecodeError:raise Stop('nonnumeric_metadata_encoding') from None
                if key=='INCLUDE_TRANSFORM':
                    need(2<=ordinal<=5,'extra_transform_card')
                    width=[10]*(7 if ordinal==2 else 5 if ordinal==4 else 1)
                else:width=[10]*8
                block['cards'].append({'line':rec['lines'],'values':fields(text,width)})
                continue
            if key=='INCLUDE':need(False,'extra_include_card')
            if key not in ELEM and key not in SETS:continue
            try:text=raw.decode('ascii')
            except UnicodeDecodeError:raise Stop('nonnumeric_element_encoding') from None
            if key in SETS:
                if ordinal==1:
                    header=fields(text,[10]*8);sid=integer(header[0]);setkey=(SETS[key],sid)
                    append_unique(self.sets,setkey,{'source':src,'keyword':key,'keyword_line':kwline,'header_line':rec['lines'],'header':header,'ids':[],'id_lines':[]},'duplicate_damage_set')
                else:
                    need(setkey is not None,'missing_damage_set_header')
                    row=ids(text,[10]*8)
                    for e in row:
                        if e not in (None,0):self.sets[setkey]['ids'].append(e);self.sets[setkey]['id_lines'].append(rec['lines'])
                continue
            kind=ELEM[key]
            if kind=='shell':
                if pending is None:pending=(rec['lines'],ids(text,[8]*10,range(6)))
                else:
                    thick=fields(text,[16]*5);need(all(x is not None for x in thick[:4]),'missing_shell_thickness')
                    self.element(src,pending[0],kind,pending[1],offset,thick);pending=None
            elif kind=='beam':self.element(src,rec['lines'],kind,ids(text,[8]*10,range(4)),offset)
            elif kind=='discrete':
                v=fields(text,[8]*5+[16,8,16])
                for i in (0,1,2,3,4,6):v[i]=integer(v[i],i in range(4))
                self.element(src,rec['lines'],kind,v,offset)
            elif kind=='solid':
                v=ids(text,[8]*10)
                if pending is not None:
                    need(all(x is not None for x in v[:4]),'solid_missing_nodes')
                    self.element(src,pending[0],kind,pending[1],offset,v);pending=None
                elif all(x is None for x in v[2:]):
                    need(v[0] is not None and v[1] is not None,'solid_missing_id');pending=(rec['lines'],v[:2])
                else:
                    need(all(x is not None for x in v),'ambiguous_solid_card')
                    self.element(src,rec['lines'],kind,v,offset)
        need(pending is None,'missing_element_continuation')
        self.finish_block(block,src,offset)
        rec.update(eof=True,sha256=h.hexdigest(),known_keywords=dict(known),uninterpreted_keyword_hashes=dict(unknown))
        return rec

    def assembly_offset(self):
        rows=[r for r in self.includes if r['source']==121 and r['keyword']=='INCLUDE_TRANSFORM']
        need(len(rows)==1,'transform_block_count')
        r=rows[0];need(r['included_source']==120,'transform_target')
        v=[[Decimal(x) if x is not None else None for x in c['values']] for c in r['cards']]
        need(v==[[0,0,1000,1000,0,0,0],[1000],[1,1,1,1,0],[0]],'unsupported_transform_values')
        return 1000

    def result(self):
        rows=[];missing_parts=[]
        for pid in sorted(set(self.parts)|set(self.counts)):
            p=self.parts.get(pid)
            counts=dict(self.counts[pid]);used=bool(counts)
            if p is None:missing_parts.append(pid)
            r={'effective_pid':pid,'used':used,'element_family_counts':counts}
            if p:
                r.update({k:p[k] for k in ('source','keyword_line','raw_pid','raw_secid','effective_secid','raw_mid','effective_mid')})
                r['part_card_line']=p['cards'][0]['line']
                r['material_definition_present']=p['effective_mid'] in self.materials
                r['section_definition_present']=p['effective_secid'] in self.sections
            rows.append(r)
        missing=[r for r in rows if r['used'] and r.get('material_definition_present') is False]
        selected_pids={r['effective_pid'] for r in missing}|{98}
        selected_raw={self.parts[p]['raw_pid'] for p in selected_pids if p in self.parts}
        selected_pids|={p for p,r in self.parts.items() if r['source']==120 and r['raw_pid'] in selected_raw}
        selected_parts=[self.parts[p] for p in sorted(selected_pids) if p in self.parts]
        secids={p['effective_secid'] for p in selected_parts}
        rawsecids={p['raw_secid'] for p in selected_parts}
        secids|={i for i,r in self.sections.items() if r['source']==120 and r['raw_id'] in rawsecids}
        # Raw ID counterparts are candidates, not substitutions for missing MID.
        mids={p['effective_mid'] for p in selected_parts}
        rawmids={p['raw_mid'] for p in selected_parts}
        mids|={i for i,r in self.materials.items() if r['source']==120 and r['raw_id'] in rawmids}
        references=[]
        for r in missing:
            m=r['effective_mid'];raw=self.parts[r['effective_pid']]['raw_mid']
            references.append({'effective_pid':r['effective_pid'],'raw_mid':raw,'effective_mid':m,
                               'same_raw_id_definitions':[{'source':v['source'],'raw_id':v['raw_id'],'effective_id':i,'keyword':v['keyword'],'keyword_line':v['keyword_line'],'first_card_line':v['cards'][0]['line']} for i,v in sorted(self.materials.items()) if v['raw_id']==raw]})
        damage=[]
        for (family,sid),s in sorted(self.sets.items()):
            need(len(s['ids'])==len(set(s['ids'])),'duplicate_damage_set_element')
            found={k:sorted(r['eid'] for r in v if r['eid'] in s['ids']) for k,v in self.damage_matches.items()}
            damage.append({**s,'family':family,'sid':sid,'found_by_card_family':found,
                           'absent_from_requested_explicit_family':sorted(set(s['ids'])-set(found.get(family,[]))),
                           'selected_gap_part_matches':[r for k,v in self.damage_matches.items() for r in v if r['eid'] in s['ids'] and r['effective_pid'] in {x['effective_pid'] for x in missing}]})
        return {'parts':rows,'source_element_counts':{s:dict(c) for s,c in self.source_counts.items()},
                'total_element_counts':dict(sum(self.source_counts.values(),Counter())),
                'missing_used_part_definitions':missing_parts,'missing_used_material_ids':sorted({r['effective_mid'] for r in missing}),
                'missing_used_material_parts':[r['effective_pid'] for r in missing],
                'missing_material_counterparts':references,
                'selected_parts':selected_parts,'selected_sections':[self.sections[i] for i in sorted(secids) if i in self.sections],
                'selected_materials':[self.materials[i] for i in sorted(mids) if i in self.materials],
                'all_section_ids':sorted(self.sections),'all_material_ids':sorted(self.materials),
                'includes':self.includes,'damage_sets':damage,'damage_id_matches':self.damage_matches,
                'definition_counts':{'parts':len(self.parts),'sections':len(self.sections),'materials':len(self.materials)},
                'limits':['Numeric-only static map; no solver or source instruction executed.',
                          'Missing refers only to actually used parts in the inspected typed sources, not every possible historical deck.',
                          'SRC116 damage lists are not activated; discrete matches are cross-family numeric candidates.',
                          'Full numeric cards preserve blank slots and original IDs; only declared namespace references are offset.',
                          'No material substitution, constitutive behavior, curve semantics or historical run identity is inferred.']}

def controls():
    names=[]
    def ok(name,value):need(value,'control_'+name);names.append(name)
    def reject(name,fn,code):
        try:fn()
        except Stop as e:ok(name,e.code==code)
        else:need(False,'control_expected_failure')
    ok('fixed_blanks',fields('%10d%10s%10d'%(1,'',25),[10]*3)==['1',None,'25'])
    ok('csv_blanks',fields('1,,25,',[10]*4)==['1',None,'25',None])
    ok('adjacent_fullwidth',ids('1234567812345679',[8]*2)==[12345678,12345679])
    ok('decimal_precision',numeric('1.23456D-20')=='1.23456E-20')
    reject('numeric_label_rejection',lambda:fields('private',[10]),'unsupported_numeric_token')
    reject('csv_extra_fields',lambda:fields('1,2,3',[10]*2),'too_many_csv_fields')
    a={};append_unique(a,1,{},'duplicate');reject('duplicate_metadata',lambda:append_unique(a,1,{},'duplicate'),'duplicate')
    ok('namespace_zero',effective(0,1000)==0 and effective(25,1000)==1025)
    p=Parser();text=b'*PART\n$ comment\n\n98,5,25,,,,,\n*SECTION_BEAM\n5,1,,,,,,\n*MAT_ELASTIC\n25,1,2,3,,,,\n'
    p.parse(121,io.BytesIO(text));ok('blank_title_and_unused',98 in p.parts and not p.counts[98] and p.parts[98]['cards'][0]['values'][3] is None)
    p=Parser();p.parse(120,io.BytesIO(text),1000)
    ok('definition_reference_offset',p.parts[1098]['effective_mid']==1025 and 1025 in p.materials and 1005 in p.sections and p.parts[1098]['cards'][0]['values'][2]=='25')
    p=Parser();p.parse(121,io.BytesIO(b'*ELEMENT_SHELL_THICKNESS\n1,98,1,2,3,4,,,,\n0.1,0.1,0.1,0.1,\n'))
    ok('shell_pair',p.counts[98]['shell']==1)
    reject('missing_shell_continuation',lambda:Parser().parse(121,io.BytesIO(b'*ELEMENT_SHELL_THICKNESS\n1,98,1,2,3,4,,,,\n')),'missing_element_continuation')
    reject('duplicate_element',lambda:Parser().parse(121,io.BytesIO(b'*ELEMENT_BEAM\n1,98,1,2,,,,,,\n1,98,2,3,,,,,,\n')),'duplicate_element_family_id')
    p=Parser();p.parse(116,io.BytesIO(b'*SET_BEAM\n2,,,,,,,\n7,8,,,,,,\n'));p.parse(121,io.BytesIO(b'*ELEMENT_BEAM\n7,98,1,2,55,,,,,\n*ELEMENT_DISCRETE\n8,25,1,0,0,1,0,0\n'))
    ok('beam_discrete_candidates',len(p.damage_matches['beam'])==1 and len(p.damage_matches['discrete'])==1 and p.damage_matches['beam'][0]['numeric_connectivity_card'][4]==55)
    reject('unsupported_element_family',lambda:Parser().parse(121,io.BytesIO(b'*ELEMENT_UNAPPROVED\n1,2\n')),'unsupported_required_keyword_variant')
    return {'passed':len(names),'groups':names}

def run():
    need(file_sha(HERE/'PROTOCOL.md')==PROTOCOL_SHA,'protocol_pin')
    before=pin_sources();p=Parser();receipts=[]
    for src in (116,121,119,120):
        off=p.assembly_offset() if src==120 else 0
        with gzip.open(RAW/PINS[src][0],'rb') as f:r=p.parse(src,f,off)
        need(r['bytes']==PINS[src][3] and r['sha256']==PINS[src][4],'decompressed_pin')
        receipts.append(r)
        print(json.dumps({'source':src,'eof':r['eof'],'lines':r['lines'],'bytes':r['bytes']}),flush=True)
    after=pin_sources();need(after==before,'source_changed')
    result=p.result();result.update(source_pins_before=before,source_pins_after=after,streams=receipts)
    return result

# INDEPENDENT_EXTRACTION_END
EXTRACTION_SHA='1cd998cff02b9cf4e947339fa1efbdaf1ae8bb6703fa644a61bab8ca26416a3c'
EXTRACTION_CORE='4caa98ce70e5eb78125052da7ee97c42e3aac415fe25a28dcf66a1a77072fca2'
ROOT_SHA='b69c12ec0668c9bdf5f5ea59dbf483d2a959de7bd477c172efe69c2f03e33594'
ROOT_REPEAT_SHA='7663fa0b97ea7f3177aca68de215115db77b499da97530250d382d0214b129b3'
ROOT_CODE_SHA='dede959bc9f440b6b0bab8784e8c8b7c7a461cd7bcfef820487b3ff2538bc469'

def compare():
    """Post-freeze schema adapter; no producer import or new source-body read."""
    pins={'independent01.json':EXTRACTION_SHA,'run01.json':ROOT_SHA,'run02.json':ROOT_REPEAT_SHA,'map_materials.py':ROOT_CODE_SHA}
    for name,wanted in pins.items():need(file_sha(HERE/name)==wanted,'comparison_dependency_pin')
    need(digest(Path(__file__).read_bytes().split(b'# INDEPENDENT_EXTRACTION_END')[0])==EXTRACTION_CORE,'frozen_extraction_core_pin')
    own=json.loads((HERE/'independent01.json').read_text())['result']
    root=json.loads((HERE/'run01.json').read_text());repeat=json.loads((HERE/'run02.json').read_text())
    failures=[];counts=Counter();max_error=Decimal(0);title_pairs=[]
    def same(path,a,b):
        nonlocal max_error
        if a is None or b is None:
            counts['null_checks']+=1
            if a is not b:failures.append({'path':path,'code':'null_mismatch'})
        elif isinstance(a,bool) or isinstance(b,bool):
            counts['boolean_checks']+=1
            if a!=b:failures.append({'path':path,'code':'boolean_mismatch'})
        elif isinstance(a,(int,float,Decimal)) or isinstance(b,(int,float,Decimal)):
            counts['numeric_scalar_checks']+=1
            try:e=abs(Decimal(str(a))-Decimal(str(b)))
            except InvalidOperation:failures.append({'path':path,'code':'numeric_type_mismatch'});return
            max_error=max(max_error,e)
            if e>Decimal('1e-8'):failures.append({'path':path,'code':'numeric_mismatch','absolute_error':str(e)})
        elif isinstance(a,dict) and isinstance(b,dict):
            counts['mapping_checks']+=1
            if set(a)!=set(b):failures.append({'path':path,'code':'mapping_keys_mismatch'})
            for k in sorted(set(a)&set(b)):same(path+'/'+str(k),a[k],b[k])
        elif isinstance(a,list) and isinstance(b,list):
            counts['list_checks']+=1
            if len(a)!=len(b):failures.append({'path':path,'code':'list_length_mismatch'})
            for i,(x,y) in enumerate(zip(a,b)):same(path+'/'+str(i),x,y)
        else:
            counts['value_checks']+=1
            if a!=b:failures.append({'path':path,'code':'value_mismatch'})
    def src(n):return 'SRC-%03d'%n
    def property_record(a,b,path):
        for key,x,y in [('source',src(a['source']),b['source']),('keyword','*'+a['keyword'],b['keyword']),
                        ('keyword_line',a['keyword_line'],b['keyword_line']),('raw_id',a['raw_id'],b['original_id']),
                        ('effective_id',a['effective_id'],b['effective_id']),('offset',1000 if a['source']==120 else 0,b['id_offset'])]:same(path+'/'+key,x,y)
        same(path+'/cards',a['cards'],b['cards'])
    ownparts={r['effective_pid']:r for r in own['parts']};rootparts={r['pid']:r for r in root['all_part_references']}
    same('all_part_ids',sorted(ownparts),sorted(rootparts))
    for pid,a in ownparts.items():
        b=rootparts[pid];path='part/'+str(pid)
        for key,x,y in [('source',src(a['source']),b['source']),('keyword_line',a['keyword_line'],b['keyword_line']),
                        ('card_line',a['part_card_line'],b['card_line']),('raw_pid',a['raw_pid'],b['original_pid']),
                        ('sid',a['effective_secid'],b['sid']),('mid',a['effective_mid'],b['mid'])]:same(path+'/'+key,x,y)
        same(path+'/original_first_three',[a['raw_pid'],a['raw_secid'],a['raw_mid']],b['values'][:3])
        same(path+'/offset',1000 if a['source']==120 else 0,b['id_offset'])
    same('used_part_ids',sorted(pid for pid,r in ownparts.items() if r['used']),sorted(r['pid'] for r in root['used_parts']))
    for b in root['used_parts']:
        a=ownparts[b['pid']];path='used_part/'+str(b['pid'])
        for key,x,y in [('elements',a['element_family_counts'],b['elements']),('material_present',a['material_definition_present'],b['material_defined']),
                        ('section_present',a['section_definition_present'],b['section_defined'])]:same(path+'/'+key,x,y)
    same('missing_used_material_ids',own['missing_used_material_ids'],root['missing_used_material_ids'])
    same('missing_used_parts',own['missing_used_material_parts'],root['missing_used_parts'])
    same('no_missing_part_defs',own['missing_used_part_definitions'],[])
    same('per_source_elements',{src(int(k)):v for k,v in own['source_element_counts'].items()},root['inventory']['per_source_elements'])
    for k in ('parts','sections','materials'):same('inventory/'+k,own['definition_counts'][k],root['inventory'][k])
    same('inventory/used_parts',sum(r['used'] for r in ownparts.values()),root['inventory']['used_parts'])
    same('all_material_ids',own['all_material_ids'],sorted(r['effective_id'] for r in root['material_id_index']))
    ownselected={r['effective_pid']:r for r in own['selected_parts']}
    for pid,a in ownselected.items():
        b=rootparts[pid];path='selected_full_part/'+str(pid)
        same(path+'/values',a['cards'][0]['values'],b['values'])
        same(path+'/keyword','*'+a['keyword'],b['keyword'])
        if a['title_sha256']!=b['title_sha256']:title_pairs.append({'pid':pid,'independent':a['title_sha256'],'root':b['title_sha256']})
    ownsec={r['effective_id']:r for r in own['selected_sections']}
    for r in root['selected_parts']:
        pid=r['part']['pid'];same('root_selection/'+str(pid),pid in ownselected,True)
        same('root_selected_elements/'+str(pid),ownparts[pid]['element_family_counts'],r['elements'])
        b=r['section'];property_record(ownsec[b['effective_id']],b,'selected_section/'+str(b['effective_id']))
    ownmat={r['effective_id']:r for r in own['selected_materials']}
    for b in root['selected_materials']:property_record(ownmat[b['effective_id']],b,'selected_material/'+str(b['effective_id']))
    matidx={r['effective_id']:r for r in root['material_id_index']}
    for ident,a in ownmat.items():
        b=matidx[ident]
        for key,x,y in [('source',src(a['source']),b['source']),('keyword','*'+a['keyword'],b['keyword']),('keyword_line',a['keyword_line'],b['keyword_line']),('original_id',a['raw_id'],b['original_id'])]:same('material_index/'+str(ident)+'/'+key,x,y)
    candidateids=sorted({v['effective_id'] for r in own['missing_material_counterparts'] for v in r['same_raw_id_definitions'] if v['source']==120})
    same('transformed_raw_mid_candidates',candidateids,root['transformed_same_original_id_candidates'])
    owninc={(src(r['source']),r['keyword_line']):r for r in own['includes']}
    same('include_locations',sorted(owninc),sorted((r['source'],r['keyword_line']) for r in root['include_cards']))
    for b in root['include_cards']:
        a=owninc[(b['source'],b['keyword_line'])];path='include/'+str(b['keyword_line'])
        same(path+'/keyword','*'+a['keyword'],b['keyword'])
        same(path+'/target',src(a['included_source']) if a['included_source'] is not None else None,b['included'])
        # Root pads the specified transform cardinalities to standard 8 slots.
        same(path+'/cards',[{'line':c['line'],'values':c['values']+[None]*(8-len(c['values']))} for c in a['cards']],b.get('cards',[]))
    allmatches={(r['kind'],r['eid']):r for values in own['damage_id_matches'].values() for r in values}
    same('damage_match_keys',sorted(allmatches),sorted((r['kind'],r['eid']) for r in root['damage_matches']))
    for b in root['damage_matches']:
        a=allmatches[(b['kind'],b['eid'])];path='damage/'+b['kind']+'/'+str(b['eid'])
        for key,x,y in [('source',src(a['source']),b['source']),('line',a['line'],b['line']),('pid',a['effective_pid'],b['pid']),
                        ('selection','cross_family_candidate' if a['kind']=='discrete' else 'same_family',b['selection']),
                        ('values',a['numeric_connectivity_card'],b['values'])]:same(path+'/'+key,x,y)
    for s in own['damage_sets']:
        same('damage_set_count/'+s['family'],len(s['ids']),root['damage_counts'][s['family']])
        allowed={'shell'} if s['family']=='shell' else {'beam','discrete'}
        same('damage_set_id_coverage/'+s['family'],sorted(s['ids']),sorted(r['eid'] for (k,_),r in allmatches.items() if k in allowed))
    for r in own['streams']:
        b=root['receipts'][src(r['source'])];pin=own['source_pins_before'][str(r['source'])];path='receipt/'+src(r['source'])
        for key,x,y in [('compressed_bytes',pin['bytes'],b['compressed_bytes']),('compressed_sha256',pin['sha256'],b['compressed_sha256']),
                        ('uncompressed_bytes',r['bytes'],b['uncompressed_bytes']),('uncompressed_sha256',r['sha256'],b['uncompressed_sha256']),
                        ('lines',r['lines'],b['lines']),('eof',r['eof'],b['eof'])]:same(path+'/'+key,x,y)
        for key in ('DELETE_ELEMENT_BEAM','DELETE_ELEMENT_SHELL'):
            same(path+'/active_keyword_hash_'+key,r['uninterpreted_keyword_hashes'].get(digest(key.encode()),0),0)
    same('active_delete_cards_within_two_tested_families',root['active_delete_cards'],[])
    independent_comparison_counts=dict(counts)
    repeat_common={k:v for k,v in root.items() if k!='elapsed_seconds'}
    same('root_repeat_except_elapsed',repeat_common,{k:v for k,v in repeat.items() if k!='elapsed_seconds'})
    for name,wanted in pins.items():need(file_sha(HERE/name)==wanted,'comparison_dependency_pin_after')
    return {'status':'PASS_COMPARABLE_SCOPE' if not failures else 'FAIL','failures':failures,'counts_including_root_repeat':dict(counts),'independent_comparison_counts':independent_comparison_counts,'max_absolute_numeric_error':str(max_error),
            'pins':pins,'core_sha256':EXTRACTION_CORE,'title_hash_recipe_differences':title_pairs,
            'coverage':{'part_reference_rows':len(ownparts),'used_part_family_rows':len(root['used_parts']),
                        'full_part_cards':len(ownselected),'full_section_blocks':len(root['selected_parts']),
                        'full_material_blocks':len(root['selected_materials']),'damage_matches':len(allmatches),'source_receipts':len(own['streams'])},
            'limits':['No new source-body read in this adapter. The frozen independent source pass is the reconstruction.',
                      'All 459 part PID/SEC/MID references and 47 selected complete PART cards are compared; remaining original PART property slots were not retained independently.',
                      'The 23 extra outside SECTION blocks and four extra outside MAT blocks are retained independently but have no full-card counterpart in root run01.',
                      'Root curve_inventory numeric arrays and curve field semantics were not independently extracted in this unit; repeat equality is not independent source verification.',
                      'Title hashes are not equated when their byte recipes differ; numeric cards and source locators are the comparison authority.',
                      'Static namespace/card agreement does not authenticate a historical run, authorize substitution or establish physical behavior.']}

def report_arithmetic():
    pins={'independent01.json':EXTRACTION_SHA,'crosswalk-summary01.json':'5c8c8c468670a9f7c5a91e245b24e2b694636533d7ce954978d565615ecfa757',
          'report.md':'a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf'}
    for name,wanted in pins.items():need(file_sha(HERE/name)==wanted,'report_input_pin')
    own=json.loads((HERE/'independent01.json').read_text())['result'];expected=json.loads((HERE/'crosswalk-summary01.json').read_text())
    ps={r['effective_pid']:r for r in own['parts']};full={r['effective_pid']:r for r in own['selected_parts']}
    sections={r['effective_id']:r for r in own['selected_sections']};materials={r['effective_id']:r for r in own['selected_materials']}
    gaps=set(own['missing_used_material_parts']);shell=Counter(r['effective_pid'] for r in own['damage_id_matches']['shell']);discrete=Counter(r['effective_pid'] for r in own['damage_id_matches']['discrete'])
    def nums(v):return [None if x is None else Decimal(str(x)) for x in v]
    rows=[]
    for pid in sorted(gaps):
        a=full[pid];b=full[pid+1000];av=nums(a['cards'][0]['values']);bv=nums(b['cards'][0]['values'])
        rows.append({'pid':pid,'mid':a['effective_mid'],'sid':a['effective_secid'],'shell_count':ps[pid]['element_family_counts'].get('shell',0),
                     'damage_set2_shell_count':shell[pid],'part_line':a['cards'][0]['line'],'section_line':sections[a['effective_secid']]['keyword_line'],
                     'counterpart_pid':b['effective_pid'],'counterpart_mid':b['effective_mid'],'counterpart_part_line':b['cards'][0]['line'],
                     'counterpart_used':ps[b['effective_pid']]['used'],'original_part_cards_equal':av==bv,
                     'title_hash_equal':a['title_sha256']==b['title_sha256'],'unequal_original_card_fields':[i+1 for i,(x,y) in enumerate(zip(av,bv)) if x!=y]})
    beams=[{'source':'SRC-%03d'%r['source'],'line':r['line'],'eid':r['eid'],'pid':r['effective_pid'],'kind':r['kind'],'selection':'same_family','values':r['numeric_connectivity_card']} for r in sorted(own['damage_id_matches']['beam'],key=lambda r:r['eid'])]
    derived={'missing_part_rows':rows,'damage_shell_by_part':{str(k):v for k,v in shell.items()},'damage_discrete_by_part':{str(k):v for k,v in discrete.items()},
             'missing_shells':sum(r['shell_count'] for r in rows),'damage_shell_missing_material':sum(shell[p] for p in gaps),
             'damage_shell_all':sum(shell.values()),'damage_discrete_missing_material':sum(discrete[p] for p in gaps),
             'material_counterpart_count':len({v['effective_id'] for r in own['missing_material_counterparts'] for v in r['same_raw_id_definitions'] if v['source']==120}),
             'same_part_title_hash':sum(r['title_hash_equal'] for r in rows),'same_raw_part_cards':sum(r['original_part_cards_equal'] for r in rows),
             'unequal_raw_part_cards':sum(not r['original_part_cards_equal'] for r in rows),'six_explicit_beams':beams,
             'total_lines':sum(r['lines'] for r in own['streams']),'total_uncompressed_bytes':sum(r['bytes'] for r in own['streams'])}
    comparisons=[]
    for k,v in derived.items():comparisons.append({'field':k,'equal':v==expected[k]})
    need(set(expected)==set(derived)|{'repeated_results_equal_excluding_elapsed'},'summary_field_coverage')
    # Root repeat is already tested in compare(); not re-labeled as source evidence.
    need(expected['repeated_results_equal_excluding_elapsed'] is True,'summary_repeat_flag')
    text=(HERE/'report.md').read_text()
    table=[[int(v) for v in m.groups()] for m in re.finditer(r'^\| (\d+) \| (\d+) \| ([\d,]+) \| (\d+) \| (\d+) \|$',text.replace(',',''),re.M)]
    comparisons.append({'field':'displayed_missing_reference_table','equal':table==[[r[k] for k in ('pid','mid','shell_count','damage_set2_shell_count','part_line')] for r in rows]})
    m=materials[50];s=sections[98]
    assertions={
        'curve_keyword_block_count':sum(r['uninterpreted_keyword_hashes'].get(digest(b'DEFINE_CURVE'),0) for r in own['streams'])==59,
        'part98_beams_1106':ps[98]['element_family_counts']=={'beam':1106},
        'material50_card_lines':[r['line'] for r in m['cards']]==[1759,1760,1761,1762],
        'material50_first_card_numeric':nums(m['cards'][0]['values'])==nums([50,12260.85,205000000000,.288,0,0,.084,0]),
        'material50_eight_pairs':len(m['cards'][2]['values'])==len(m['cards'][3]['values'])==8,
        'material50_first_pair':nums([m['cards'][2]['values'][0],m['cards'][3]['values'][0]])==nums([0,259000000]),
        'section98_card_lines':[r['line'] for r in s['cards']]==[2104,2106],
        'section98_numeric_first_card':nums(s['cards'][0]['values'])==nums([98,1,1,3,1,None,None,None]),
        'section98_numeric_second_card':nums(s['cards'][1]['values'])==nums([.2175,.2175,0,0,0,0,None,None]),
        'seven_gap_parts_in_shell_list':len(gaps&set(shell))==7,
        'nongap_shell_parts':set(shell)-gaps=={11,27},
        'title_difference_parts':{r['pid'] for r in rows if not r['title_hash_equal']}=={25,33},
        'changed_reference_parts':{r['pid'] for r in rows if not r['original_part_cards_equal']}=={722,752,753,782},
    }
    failures=[r['field'] for r in comparisons if not r['equal']]+[k for k,v in assertions.items() if not v]
    for name,wanted in pins.items():need(file_sha(HERE/name)==wanted,'report_input_pin_after')
    return {'status':'PASS_REPORT_ARITHMETIC' if not failures else 'FAIL','pins':pins,'failures':failures,'summary_comparisons':comparisons,
            'additional_assertions':assertions,'derived_summary':derived,
            'limits':['Report arithmetic and numeric card positions are checked, not primary-source semantic interpretations.',
                      '59 curve keyword blocks are counted independently by stored keyword hash; curve numeric arrays and reference meanings remain outside this extraction.',
                      'The report text was also read in full; exact pin limits this review to that version.']}

def main():
    a=argparse.ArgumentParser();a.add_argument('--controls',action='store_true');a.add_argument('--compare',action='store_true');a.add_argument('--report',action='store_true');a.add_argument('--output',required=True);args=a.parse_args()
    need(re.fullmatch(r'independent(?:-controls|-failed|-comparison|-report)?[0-9]{2}\.json',args.output) is not None,'output_name')
    dest=HERE/args.output;need(not dest.exists(),'create_only_output')
    raw=Path(__file__).read_bytes();receipt={'code_sha256':digest(raw),'core_sha256':digest(raw.split(b'# INDEPENDENT_EXTRACTION_END')[0]),'protocol_sha256':PROTOCOL_SHA,'command':sys.argv,'python':sys.version.split()[0]}
    start=time.monotonic();result=None
    try:
        receipt['controls']=controls();PROGRESS.clear();CONTEXT.update(source=0,line=0)
        if not args.controls:result=report_arithmetic() if args.report else compare() if args.compare else run()
        peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;need(peak<=MEM_CAP,'observed_memory_cap')
        receipt.update(status='FAIL' if (args.compare or args.report) and result and result['status']=='FAIL' else 'PASS',peak_rss_bytes=peak)
    except (Exception,KeyboardInterrupt) as e:
        receipt.update(status='FAIL',error={'code':e.code if isinstance(e,Stop) else type(e).__name__,**CONTEXT},progress=PROGRESS)
    receipt['seconds']=time.monotonic()-start
    with dest.open('x') as f:json.dump({'receipt':receipt,'result':result},f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'status':receipt['status'],'output':args.output,'sha256':file_sha(dest),'error':receipt.get('error'),'seconds':receipt['seconds']}))
    return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
