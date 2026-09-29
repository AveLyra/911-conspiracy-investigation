#!/usr/bin/env python3
"""Independent contact-selector/set-membership trace. Never initializes contacts."""
import argparse
from collections import Counter,defaultdict
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import time

import verify_restraint as graph

BASE=Path(__file__).resolve().parent
PROTOCOL_SHA='f367dab9cf29f4958afed5a354a37bfcf1d5cb0f92e8fc39aab3009c2e529c80'
SEED_SHA='d4f0c4107b2162c540fbb90fd61b1a90d42860cbcf3cd17903f22ba7e46379d7'
GRAPH_CODE_SHA='5587e88d786d4e3fa7bfbe21823a54a54c97e289d5d7c90b2d9c72200408028a'
MANUAL=Path('/private/tmp/lsdyna-keyword-source-review.6f36b5/ls-dyna_971_manual_k-ansys.pdf')
MANUAL_SHA='f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d'
CONTACTS={'CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET',
          'CONTACT_TIED_SURFACE_TO_SURFACE_ID_OFFSET',
          'CONTACT_AUTOMATIC_SINGLE_SURFACE_ID'}
SETS={'SET_NODE_LIST':'node','SET_SEGMENT':'segment','SET_PART_LIST':'part'}
ROW_CAP=2000000
PROGRESS=[]


def require(ok,code,source=0,line=0):
    graph.require(ok,code,source,line)


def contact_id(line):
    body=line.rstrip('\r\n')
    first,heading=body.split(',',1) if ',' in body else (body[:10],body[10:])
    cid=graph.scalar(first,True)
    require(cid>=0,'negative_contact_id')
    return {'id':cid,'id_heading_card_sha256':hashlib.sha256(body.encode('ascii')).hexdigest(),
            'heading_only_sha256':hashlib.sha256(heading.strip().encode('ascii')).hexdigest()}


def admit(token):
    if token.startswith('CONTACT'):
        require(token in CONTACTS,'unexpected_contact_variant')
        return 'contact'
    if token.startswith(('SET_NODE','SET_SEGMENT','SET_PART')):
        require(token in SETS,'unexpected_set_variant')
        return SETS[token]
    return None


def seed_index(seed):
    ordered,unordered=defaultdict(list),defaultdict(list)
    for row in seed['seed_elements']:
        require(row['kind']=='shell','non_shell_seed')
        ref={'source':row['source'],'line':row['line'],'element_id':row['id']}
        ordered[tuple(row['physical_nodes'])].append(ref)
        unordered[frozenset(row['physical_nodes'])].append(ref)
    return ordered,unordered


class SetBuilder:
    def __init__(self,source,keyword,keyword_line,seed):
        self.source,self.keyword,self.keyword_line=source,keyword,keyword_line
        self.kind=SETS[keyword]
        self.seed_nodes=set(seed['seed_nodes']);self.seed_parts=set(seed['seed_parts'])
        self.ordered,self.unordered=seed_index(seed)
        self.header=None;self.rows=0;self.entries=0
        self.member_counts=Counter();self.full_rows=Counter();self.ordered_rows=Counter();self.unordered_rows=Counter()
        self.node_ids=set();self.matches=[];self.matched_ids=set();self.triangle_rows=0
        self.matched_occurrences=0;self.ordered_match_rows=0;self.unordered_match_rows=0

    def add(self,line,text):
        if self.header is None:
            values=graph.fields(text,[10]*8,[0],1)
            require(values[0]>=0,'negative_set_id',self.source,line)
            self.header={'source':self.source,'keyword':self.keyword,'kind':self.kind,
                         'keyword_line':self.keyword_line,'header_line':line,'set_id':values[0],
                         'header_card':values}
            return
        self.rows+=1
        require(self.rows<=ROW_CAP,'membership_row_cap',self.source,line)
        if self.kind=='segment':
            values=graph.fields(text,[10]*8,range(4),4)
            nodes=values[:4];attributes=values[4:]
            require(all(n>0 for n in nodes),'invalid_segment_node',self.source,line)
            self.entries+=4;self.node_ids.update(nodes)
            self.member_counts.update(nodes);self.full_rows[tuple(values)]+=1
            self.ordered_rows[tuple(nodes)]+=1;self.unordered_rows[frozenset(nodes)]+=1
            self.triangle_rows+=int(nodes[2]==nodes[3])
            hits=sorted(set(nodes)&self.seed_nodes)
            if hits:
                ordered=self.ordered.get(tuple(nodes),[])
                unordered=self.unordered.get(frozenset(nodes),[])
                self.ordered_match_rows+=bool(ordered);self.unordered_match_rows+=bool(unordered)
                self.matched_occurrences+=sum(n in self.seed_nodes for n in nodes)
                self.matched_ids.update(hits)
                self.matches.append({'line':line,'membership_row':self.rows,'nodes':nodes,'attributes':attributes,
                    'matched_seed_nodes':hits,'ordered_seed_shell_matches':ordered,
                    'unordered_seed_shell_matches':unordered})
        else:
            raw=graph.fields(text,[10]*8,range(8),0)
            # Blank/zero list slots are padding, not nodes/parts; preserve the
            # occurrence's original slot number, rather than reindexing hits.
            for slot,value in enumerate(raw,1):
                if value in (None,0):continue
                require(value>0,'negative_set_member',self.source,line)
                effective=value+(1000 if self.source==120 and self.kind=='part' else 0)
                self.entries+=1;self.member_counts[effective]+=1
                wanted=self.seed_parts if self.kind=='part' else self.seed_nodes
                if effective in wanted:
                    self.matched_ids.add(effective);self.matched_occurrences+=1
                    self.matches.append({'line':line,'membership_row':self.rows,'slot':slot,
                                         'original_id':value,'effective_id':effective})

    def finish(self):
        require(self.header is not None,'missing_set_header',self.source,self.keyword_line)
        common={**self.header,'membership_rows':self.rows,'member_occurrences':self.entries,
                'unique_member_ids':len(self.member_counts),
                'duplicate_member_occurrences':self.entries-len(self.member_counts),
                'distinct_repeated_member_ids':sum(n>1 for n in self.member_counts.values()),
                'matched_seed_ids':sorted(self.matched_ids),'matched_member_occurrences':self.matched_occurrences,
                'matching_records':self.matches,'has_seed_intersection':bool(self.matched_ids)}
        if self.kind=='segment':
            common.update({'unique_node_ids':len(self.node_ids),'triangle_rows_N3_equals_N4':self.triangle_rows,
                           'unique_full_segment_records':len(self.full_rows),'duplicate_full_segment_rows':self.rows-len(self.full_rows),
                           'unique_ordered_node_lists':len(self.ordered_rows),'duplicate_ordered_node_rows':self.rows-len(self.ordered_rows),
                           'unique_unordered_node_sets':len(self.unordered_rows),'duplicate_unordered_node_rows':self.rows-len(self.unordered_rows),
                           'ordered_seed_shell_matching_rows':self.ordered_match_rows,
                           'unordered_seed_shell_matching_rows':self.unordered_match_rows})
        return common


class ContactBuilder:
    def __init__(self,source,keyword,keyword_line):
        self.source,self.keyword,self.keyword_line=source,keyword,keyword_line
        self.header=None;self.cards=[]

    def add(self,line,text):
        if self.header is None:
            self.header={'source':self.source,'keyword':self.keyword,'keyword_line':self.keyword_line,
                         'header_line':line,**contact_id(text)}
        else:
            require(len(self.cards)<1000,'contact_card_cap',self.source,line)
            # Blank optional rows are retained, not skipped or interpreted as
            # physical zeros. Only Card1's eight declared fields are integer.
            card=graph.fields(text,[10]*8,range(8) if not self.cards else [],4 if not self.cards else 0)
            self.cards.append({'line':line,'card_index':len(self.cards)+1,'card':card})

    def finish(self):
        require(self.header is not None and len(self.cards)>=3,'missing_contact_header_or_required_cards',self.source,self.keyword_line)
        return {**self.header,'numeric_cards':self.cards,'numeric_card_count':len(self.cards)}


def scan(source,binary,seed):
    digest=hashlib.sha256();stats={'source':source,'bytes':0,'lines':0,'eof':False}
    PROGRESS.append(stats)
    builder=None;ended=False;seen=Counter();records=[]
    while True:
        raw=binary.readline(graph.LINE_CAP+1)
        if not raw:break
        stats['lines']+=1;stats['bytes']+=len(raw);line=stats['lines'];digest.update(raw)
        require(len(raw)<=graph.LINE_CAP and stats['bytes']<=graph.CAP and b'\0' not in raw,'stream_cap_or_nul',source,line)
        if line%100000==0:require(graph.peak_memory()<=graph.MEMORY_CAP,'memory_cap',source,line)
        try:text=raw.decode('ascii')
        except UnicodeDecodeError:raise graph.AuditError('nonascii_source',source,line) from None
        s=text.strip()
        if s.startswith('$'):continue
        if s.startswith('*'):
            require(not ended,'keyword_after_END',source,line)
            if builder is not None:records.append(builder.finish());builder=None
            token=s[1:].split('$',1)[0].strip().upper()
            if token=='END':ended=True;continue
            try:kind=admit(token)
            except graph.AuditError as exc:raise graph.AuditError(exc.code,source,line) from None
            if kind is not None:
                seen[token]+=1
                builder=ContactBuilder(source,token,line) if kind=='contact' else SetBuilder(source,token,line,seed)
        elif builder is not None:
            try:builder.add(line,text)
            except graph.AuditError as exc:raise graph.AuditError(exc.code,source,line) from None
        elif ended:
            require(not s,'data_after_END',source,line)
    if builder is not None:records.append(builder.finish())
    stats.update(eof=True,sha256=digest.hexdigest(),typed_keyword_counts=dict(seen))
    return records,stats


def resolve_selector(contact,side,sets):
    card=contact['numeric_cards'][0]['card']
    sid,typ=(card[0],card[2]) if side=='slave' else (card[1],card[3])
    result={'side':side,'card_line':contact['numeric_cards'][0]['line'],'selector_id':sid,'selector_type':typ}
    automatic=contact['keyword']=='CONTACT_AUTOMATIC_SINGLE_SURFACE_ID'
    if side=='master' and automatic:
        require(sid==0,'unexpected_single_surface_master_id')
        return {**result,'status':'not_applicable_single_surface_master','set_kind':None,'set_exists':None}
    if side=='slave' and automatic and sid==0:
        return {**result,'status':'all_parts_single_surface','set_kind':None,'set_exists':None,
                'includes_seed_part_by_all_parts_selector':True}
    kind={0:'segment',2:'part',4:'node'}.get(typ)
    require(kind is not None and not(side=='master' and typ==4),'unsupported_contact_selector_type')
    key=(kind,sid)
    if key not in sets:return {**result,'status':'missing_typed_set','set_kind':kind,'set_exists':False}
    s=sets[key]
    return {**result,'status':'resolved_typed_set','set_kind':kind,'set_exists':True,
            'set_source':s['source'],'set_keyword_line':s['keyword_line'],'set_header_line':s['header_line'],
            'set_member_occurrences':s['member_occurrences'],'set_unique_member_ids':s['unique_member_ids'],
            'set_has_seed_intersection':s['has_seed_intersection'],'set_matched_seed_ids':s['matched_seed_ids'],
            'set_matched_member_occurrences':s['matched_member_occurrences']}


def collect(seed):
    records=[]
    for src,pin in graph.PINS.items():
        with gzip.open(graph.SOURCE/pin[0],'rb') as f:rows,stats=scan(src,f,seed)
        require(stats['eof'] and stats['bytes']==pin[3] and stats['sha256']==pin[4],'decompressed_pin',src)
        records.extend(rows)
    sets={};contacts=[];cids=set()
    for r in records:
        if r['keyword'] in CONTACTS:
            require(r['id'] not in cids,'duplicate_contact_id',r['source'],r['header_line'])
            cids.add(r['id']);contacts.append(r)
        else:
            key=(r['kind'],r['set_id'])
            require(key not in sets,'duplicate_set_definition',r['source'],r['header_line']);sets[key]=r
    for c in contacts:
        c['selectors']=[resolve_selector(c,side,sets) for side in ('slave','master')]
    counts=Counter(r['kind'] for r in sets.values())
    matching_counts=Counter(r['kind'] for r in sets.values() if r['has_seed_intersection'])
    return {'seed':{'source_receipt_sha256':SEED_SHA,'node_count':len(seed['seed_nodes']),
                    'part_ids':seed['seed_parts'],'shell_count':len(seed['seed_elements'])},
            'sets':sorted(sets.values(),key=lambda r:(r['kind'],r['set_id'])),
            'contacts':sorted(contacts,key=lambda r:(r['source'],r['keyword_line'])),
            'counts':{'sets_by_kind':dict(counts),'intersecting_sets_by_kind':dict(matching_counts),
                      'contacts':len(contacts),'selector_records':len(contacts)*2,
                      'missing_typed_references':sum(s['status']=='missing_typed_set' for c in contacts for s in c['selectors'])},
            'namespace':'Set IDs and node IDs unchanged; outside-region PART members use+1000. Offset metadata was checked in the frozen seed extraction.',
            'ceiling':'Typed input membership only. No distance, projection, pair eligibility, filters, contact initialization, penalty stiffness, force, damage activation, historic tie success or directional restraint.'}


def controls():
    result=[]
    seed={'seed_nodes':[1,2,3],'seed_parts':[179],'seed_elements':[{'source':121,'line':11,'id':99,'kind':'shell','physical_nodes':[1,2,3,3]}]}
    def check(name,ok):require(ok,'control_'+name);result.append({'name':name,'status':'PASS'})
    def reject(name,fn):
        try:fn()
        except graph.AuditError:result.append({'name':name,'status':'PASS'});return
        raise graph.AuditError('control_no_rejection_'+name)
    check('fixed_ID_heading',contact_id('        17Synthetic heading')['id']==17)
    check('free_ID_heading_with_comma',contact_id('17,Synthetic, heading')['id']==17)
    reject('unknown_contact_variant',lambda:admit('CONTACT_SYNTHETIC'))
    reject('unknown_node_set_variant',lambda:admit('SET_NODE_LIST_GENERATE'))
    check('legal_ID_before_OFFSET',admit('CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET')=='contact')
    b=SetBuilder(121,'SET_NODE_LIST',1,seed);b.add(2,'179,0,0,0,0');b.add(3,'1,1,8,2,0,,,');s=b.finish()
    check('header_not_member',s['member_occurrences']==4 and s['matched_seed_ids']==[1,2])
    check('duplicates_slots_and_padding',s['duplicate_member_occurrences']==1 and [r['slot'] for r in s['matching_records']]==[1,2,4])
    a=SetBuilder(120,'SET_PART_LIST',1,seed);a.add(2,'1');a.add(3,'179');a=a.finish()
    check('outside_part_namespace_not_seed',a['member_occurrences']==1 and a['has_seed_intersection'] is False)
    b=SetBuilder(121,'SET_SEGMENT',1,seed);b.add(2,'5');b.add(3,'1,2,3,3,100,200,300,400');b.add(4,'3,2,1,3,100,200,300,400');t=b.finish()
    check('attributes_not_nodes',t['unique_node_ids']==3 and t['member_occurrences']==8)
    check('triangle_repeated_slot',t['triangle_rows_N3_equals_N4']==1 and t['matching_records'][0]['nodes']==[1,2,3,3])
    check('ordered_vs_unordered_shell',t['ordered_seed_shell_matching_rows']==1 and t['unordered_seed_shell_matching_rows']==2)
    check('different_orientation_not_duplicate_order',t['duplicate_ordered_node_rows']==0 and t['duplicate_unordered_node_rows']==1)
    a=SetBuilder(121,'SET_NODE_LIST',1,seed);a.add(2,'5');a.add(3,'8,9');a=a.finish()
    check('no_intersection_retained',not a['has_seed_intersection'] and a['matching_records']==[])
    c=ContactBuilder(121,'CONTACT_TIED_SHELL_EDGE_TO_SURFACE_ID_OFFSET',1)
    for n,txt in [(2,'7,Synthetic'),(3,'179,5,4,0,0,0,0,0'),(4,',,,,,,,'),(5,'0,0,0,0,0,0,0,0')]:c.add(n,txt)
    c=c.finish();sets={('node',179):s,('segment',5):t,('node',5):a}
    check('typed_namespaces_separate',resolve_selector(c,'slave',sets)['set_kind']=='node' and resolve_selector(c,'master',sets)['set_kind']=='segment')
    check('blank_numeric_contact_card',c['numeric_cards'][1]['card']==[None]*8)
    check('missing_reference_explicit',resolve_selector(c,'master',{})['status']=='missing_typed_set')
    c['keyword']='CONTACT_AUTOMATIC_SINGLE_SURFACE_ID';c['numeric_cards'][0]['card'][1]=0
    check('zero_single_surface_master_not_missing',resolve_selector(c,'master',{})['set_exists'] is None)
    raw=b'*SET_NODE_LIST\n5\n1,2\n*END\n'
    rows,stats=scan(0,io.BytesIO(raw),seed)
    check('actual_stream_EOF_hash',stats['eof'] and stats['sha256']==hashlib.sha256(raw).hexdigest() and rows[0]['matched_seed_ids']==[1,2])
    PROGRESS.clear()
    return result


def pins():
    result=graph.pin_inputs()
    require(result['code']==GRAPH_CODE_SHA,'graph_code_pin')
    for name,expected in [('CONTACT-TRACE-PROTOCOL.md',PROTOCOL_SHA),('independent01.json',SEED_SHA)]:
        require(graph.sha(BASE/name)==expected,'contact_input_pin');result[name]=expected
    require(graph.sha(MANUAL)==MANUAL_SHA,'manual_pin');result['manual']=MANUAL_SHA
    result['contact_code']=graph.sha(Path(__file__))
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output');ap.add_argument('--selftest',action='store_true');args=ap.parse_args()
    if args.selftest:print(json.dumps({'status':'PASS','controls':controls()}));return 0
    require(args.output is not None and Path(args.output).name==args.output and args.output.endswith('.json'),'output_basename')
    dest=BASE/args.output;require(not dest.exists(),'output_exists')
    started=time.monotonic();tests=controls();before=pins()
    seed_receipt=json.loads((BASE/'independent01.json').read_text())
    require(seed_receipt['receipt']['status']=='PASS','seed_not_passed')
    seed=seed_receipt['result'];require(len(seed['seed_nodes'])==873 and seed['seed_parts']==[179],'frozen_seed_scope')
    try:result=collect(seed);status='PASS';error=None
    except graph.AuditError as exc:result=None;status='FAIL';error={'code':exc.code,'source':exc.source,'line':exc.line}
    after=pins();require(before==after,'pins_changed');require(graph.peak_memory()<=graph.MEMORY_CAP,'memory_cap')
    receipt={'status':status,'error':error,'controls':tests,'pins_before':before,'pins_after':after,'streams':PROGRESS,
             'elapsed_seconds':time.monotonic()-started,'peak_rss_bytes':graph.peak_memory(),'python':sys.version,
             'command':[sys.executable,*sys.argv],
             'independence':'Own new typed source extraction using own frozen seed. New root contact producer/results not read before this freeze. Prior metadata counts/variants and direct-graph results were known.',
             'manual_pages_fully_viewed':[364,366,367,370,371,402,403,1161,1162,1171,1172,1173,1174]}
    with dest.open('x') as f:json.dump({'receipt':receipt,'result':result},f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    print(json.dumps({'status':status,'error':error,'counts':result['counts'] if result else None,
                      'sha256':graph.sha(dest),'controls':len(tests),'seconds':receipt['elapsed_seconds'],'peak_rss_bytes':receipt['peak_rss_bytes']}))
    return 0 if status=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except graph.AuditError as exc:
        print(json.dumps({'status':'FAIL','code':exc.code,'source':exc.source,'line':exc.line}));raise SystemExit(1)
