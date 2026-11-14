#!/usr/bin/env python3
"""Extract matched-pair stored values and audit clocks without modifying sources.

CSV adds source_excel_row. Numeric strings retain source XML lexical precision;
shared strings resolve to their original text; formulas use stored caches, not
recalculated values. Formula provenance remains in inventory's formula ledger.
Blank and absent cells both serialize as empty CSV fields; the source XLSX and
column inventory retain their distinction. Clock deltas/date conversions are
separate derived diagnostics. No values are filtered, filled, or interpolated.
"""
from pathlib import Path
import argparse,bisect,csv,gzip,hashlib,json,statistics,zipfile
import xml.etree.ElementTree as ET
from inventory_native import T,decode,col_index,safe_name,json_write

parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,default=Path('r08_work/direct_get/native'));parser.add_argument('--out',type=Path,default=Path('r08_work/native_inventory'));args=parser.parse_args()
base=args.input;out=args.out;exp=out/'matched_pair_csv';exp.mkdir(parents=True,exist_ok=True)
all_audit=[]
for name in ['CB-DA-AMB','CB-DA']:
    inv=json.loads((out/name/'inventory.json').read_text());path=base/(name+'.xlsx');original_sha=hashlib.sha256(path.read_bytes()).hexdigest()
    audit={'file':path.name,'sha256':original_sha,'sheets':[],'event_time_comparisons':[],'csv_export_policy':__doc__}
    with zipfile.ZipFile(path) as z:
        strings=[''.join(t.text or '' for t in el.iter(T('t'))) for el in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        for sh in inv['sheets']:
            if not sh.get('data_sheet_by_observed_time_headers'):continue
            n=sh['data_column_count'];records=[]
            target=exp/(name+'__'+safe_name(sh['sheet'])+'.csv.gz')
            with gzip.open(target,'wt',encoding='utf-8',newline='') as f,z.open(sh['part']) as stream:
                w=csv.writer(f);context=ET.iterparse(stream,events=('start','end'));_,root=next(context)
                for event,el in context:
                    if event!='end' or el.tag!=T('row'):continue
                    rn=int(el.get('r'));cs=[decode(c,strings) for c in el if c.tag==T('c')]
                    if rn>sh['data_rows_end']:el.clear();root.clear();continue
                    row=['']*n
                    for c in cs:
                        letters=''.join(ch for ch in c['cell'] if ch.isalpha());idx=col_index(letters)-1
                        if idx<n:row[idx]='' if c['resolved'] is None else c['resolved']
                    w.writerow((['source_excel_row'] if rn==1 else [rn])+row)
                    if rn>1 and row[0] and row[1]:records.append({'row':rn,'timestamp_cell':'A'+str(rn),'elapsed_cell':'B'+str(rn),'timestamp_lexical':row[0],'elapsed_lexical':row[1],'timestamp':float(row[0]),'elapsed':float(row[1])})
                    el.clear();root.clear()
            sa={'sheet':sh['sheet'],'csv':str(target.relative_to(out)),'data_rows':len(records),'derived_clock_diagnostics':{},'_records':records}
            for axis,scale in [('timestamp',86400),('elapsed',1)]:
                ds=[(records[i][axis]-records[i-1][axis])*scale for i in range(1,len(records))];median=statistics.median(ds)
                gaps=[{'from':records[i-1],'to':records[i],'delta_seconds':d} for i,d in enumerate(ds,start=1) if abs(d-median)>max(.01,abs(median)*.01)]
                sa['derived_clock_diagnostics'][axis]={'median_delta_seconds':median,'anomalous_intervals':gaps,'rule':'absolute deviation from median > max(0.01 s, 1% of median); identifies clock intervals, not proof of missing physical measurements'}
            audit['sheets'].append(sa)
        events=json.loads((out/name/'User_Events_observed_cells.json').read_text());ec={c['cell']:c['resolved'] for c in events}
        for row in sorted({int(c['cell'][1:]) for c in events if c['cell'].startswith('C') and c['cell']!='C1'}):
            event_stamp=float(ec['C'+str(row)]);event_elapsed=ec.get('B'+str(row))
            entry={'event_row':row,'timestamp_cell':'C'+str(row),'elapsed_cell':'B'+str(row),'timestamp_lexical':ec['C'+str(row)],'elapsed_lexical':event_elapsed,'description_cell':'D'+str(row),'description':ec.get('D'+str(row)),'matched_timestamp_candidates':[]}
            for sh in audit['sheets']:
                recs=sh['_records'];values=[r['timestamp'] for r in recs];i=bisect.bisect_left(values,event_stamp)
                cand=[recs[j] for j in {max(0,i-1),min(i,len(recs)-1)}];near=min(cand,key=lambda r:abs(r['timestamp']-event_stamp));dt=(event_stamp-near['timestamp'])*86400
                if abs(dt)<=.51:
                    entry['matched_timestamp_candidates'].append({'sheet':sh['sheet'],'source_record':near,'derived_event_timestamp_minus_data_timestamp_seconds':dt,
                        'derived_event_elapsed_minus_data_elapsed_seconds':float(event_elapsed)-near['elapsed'] if event_elapsed is not None else None})
            audit['event_time_comparisons'].append(entry)
    for sh in audit['sheets']:del sh['_records']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=original_sha:raise RuntimeError('source changed')
    json_write(out/name/'primary_time_audit.json',audit);all_audit.append(audit)
json_write(out/'matched_pair_time_audit.json',all_audit)
print(json.dumps({'exports':[str(p) for p in exp.glob('*.csv.gz')],'audit':str(out/'matched_pair_time_audit.json')}))
