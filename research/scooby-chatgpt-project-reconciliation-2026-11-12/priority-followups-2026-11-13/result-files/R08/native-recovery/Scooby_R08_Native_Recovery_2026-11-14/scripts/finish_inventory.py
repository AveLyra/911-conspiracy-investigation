#!/usr/bin/env python3
"""Consolidate completed read-only inventories; no recalculation or source edits."""
from pathlib import Path
import argparse,collections,csv,gzip,hashlib,json,re,zipfile
from inventory_native import json_write

parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,default=Path('r08_work/direct_get/native'));parser.add_argument('--out',type=Path,default=Path('r08_work/native_inventory'));args=parser.parse_args()
base=args.out;source=args.input
summary={'method':'Read-only ZIP/XML inventory. Timed records, used worksheet cells and native summary formulas are distinguished. All native files unchanged.','workbooks':[]}
sheet_rows=[];comment_rows=[];formula_summaries=[];style_reviews=[]
for name in ['drawings','CB-DA-AMB','CB-DA','CB-DA-SC','CB-SP','CB-SP-SC']:
    d=base/name;inv=json.loads((d/'inventory.json').read_text());original=source/(name+'.xlsx')
    if hashlib.sha256(original.read_bytes()).hexdigest()!=inv['sha256']:raise RuntimeError('Source changed: '+name)
    # Earlier completed sheets had no extra non-timed cells: their numeric A/B
    # sample count equals the full declared record span. Upgrade schema only.
    for sh in inv['sheets']:
        if sh.get('data_sheet_by_observed_time_headers'):
            at=sh['time_columns_derived']['A']['sample_count'];bt=sh['time_columns_derived']['B']['sample_count']
            if at!=bt or at!=sh['data_row_count']:raise RuntimeError('Timed row mismatch: '+name+' '+sh['sheet'])
            sh.setdefault('non_time_series_cells',[])
            sh.setdefault('time_series_formula_count',sum(c.get('formula_count',0) for c in sh['columns']))
            sh.setdefault('data_row_definition','Rows with both A timestamp/time-of-day and B elapsed-time stored numeric values; non-timed cells preserved separately')
            sh.setdefault('data_rows_contiguous',sh['data_row_count']==sh['data_rows_end']-sh['data_rows_start']+1)
            sh.setdefault('time_series_extent_including_header',f"A1:{sh['nonempty_extent'].split(':')[1].rstrip('0123456789')}{sh['data_rows_end']}")
            if any(c.get('blank_or_absent_count',0)<0 or c.get('absent_xml_count',0)<0 for c in sh['columns']):raise RuntimeError('Negative missingness count')
        sheet_rows.append({'workbook':name+'.xlsx','sheet':sh['sheet'],'visibility':sh['attributes'].get('state','visible (OOXML default)'),
                           'declared_dimension':sh['declared_dimension'],'xml_cell_extent':sh['xml_cell_extent'],'nonempty_extent':sh['nonempty_extent'],
                           'time_series_extent':sh.get('time_series_extent_including_header'),'timed_record_count':sh.get('data_row_count'),
                           'data_columns_including_clocks':sh.get('data_column_count'),'source_formula_count_all_cells':sh['formula_count'],
                           'source_formula_count_time_series':sh.get('time_series_formula_count'),
                           'non_timed_nonempty_cells':len(sh.get('non_time_series_cells',[])),
                           'missing_data_cells':sum(c.get('blank_or_absent_count',0) for c in sh.get('columns',[])),
                           'columns_with_missing_data':sum(c.get('blank_or_absent_count',0)>0 for c in sh.get('columns',[])),
                           'error_cells_time_series':sum(c.get('error_count',0) for c in sh.get('columns',[])),
                           'nonnumeric_time_series_cells':sum(c.get('non_numeric_count',0) for c in sh.get('columns',[]))})
    comments=[]
    for c in inv['comments']:
        sheets=[sh['sheet'] for sh in inv['sheets'] if any(rel['resolved']==c['part'] for rel in sh['relationships'].values())]
        comments.append({'sheets':sheets,**c})
        comment_rows.append({'workbook':name+'.xlsx','sheets':' | '.join(sheets),'part':c['part'],'cell':c['attributes'].get('ref'),'text':c['text']})
    styles={str(x['index']):x for x in inv['styles'].get('cell_formats',[])}
    review={'workbook':name+'.xlsx','comments':comments,'threaded_comment_parts':[],'data_sheets':[],
            'interpretation':'Comments and styling are source observations. Absence of blanks/errors or an explicit flag column does not establish sensor validity. Installation X markers in channel lists are not validity flags.'}
    with zipfile.ZipFile(original) as z:
        for p in z.namelist():
            if p.startswith(('xl/threadedComments/','xl/persons/')) and p.endswith('.xml'):
                b=z.read(p);review['threaded_comment_parts'].append({'part':p,'sha256':hashlib.sha256(b).hexdigest(),'xml':b.decode('utf-8')})
    for sh in inv['sheets']:
        if not sh.get('data_sheet_by_observed_time_headers'):continue
        used=sorted({i for c in sh['columns'] for i in c.get('styles',{})},key=int)
        st=[{'style_id':i,'attributes':styles[i]['attributes'],'fill_xml':inv['styles']['fills'][int(styles[i]['attributes']['fillId'])]} for i in used]
        hits=[c for c in sh['header_cells'] if re.search(r'std|stdev|standard.?deviation|sigma|uncert|quality|flag|calibr',str(c['resolved']),re.I)]
        review['data_sheets'].append({'sheet':sh['sheet'],'quality_or_deviation_header_pattern_matches':hits,
             'conditional_formatting':sh['conditional_formatting'],'data_validation':sh['data_validation'],
             'data_cell_styles':st,'hidden_rows':sh['hidden_rows'],'hidden_columns':sh['hidden_columns']})
    json_write(d/'comments_and_style_review.json',review);style_reviews.append({'workbook':name+'.xlsx','review':str((d/'comments_and_style_review.json').relative_to(base))})
    groups={};formcols={};total=0;null_shared=0;null_nonshared=0;missingcache=0
    with gzip.open(d/'formulas_and_cached_values.ndjson.gz','rt',encoding='utf-8') as f:
        for line in f:
            c=json.loads(line);total+=1;frm=c['formula'];attr=frm['attributes'];key=(c['sheet'],re.sub(r'\d','',c['cell']))
            stat=formcols.setdefault(key,{'sheet':key[0],'column':key[1],'formula_cells':0,'explicit_formula_text_cells':0,'shared_formula_followers':0,'cached_values_missing':0,'example_explicit_cells':[]})
            stat['formula_cells']+=1
            if c['raw_v'] is None:stat['cached_values_missing']+=1;missingcache+=1
            if frm['text'] is not None:
                stat['explicit_formula_text_cells']+=1
                if len(stat['example_explicit_cells'])<3:stat['example_explicit_cells'].append(c)
            elif attr.get('t')=='shared':stat['shared_formula_followers']+=1;null_shared+=1
            else:null_nonshared+=1
            if attr.get('t')=='shared':
                gkey=(c['sheet'],attr.get('si'));g=groups.setdefault(gkey,{'sheet':c['sheet'],'shared_index':attr.get('si'),'master_cells':[],'follower_count':0,'first_follower_cell':None,'last_follower_cell':None})
                if frm['text'] is not None:g['master_cells'].append({'cell':c['cell'],'reference_range':attr.get('ref'),'raw_master_formula':frm['text'],'raw_attributes':attr})
                else:
                    g['follower_count']+=1
                    if g['first_follower_cell'] is None:g['first_follower_cell']=c['cell']
                    g['last_follower_cell']=c['cell']
    group_result={'workbook':name+'.xlsx','formula_cells':total,'formula_without_cached_value_count':missingcache,
                  'shared_followers_without_text':null_shared,'nonshared_formula_without_text':null_nonshared,
                  'shared_groups_without_master':[g for g in groups.values() if not g['master_cells']],
                  'interpretation':'A shared follower has <f t="shared" si="..."/> without text by OOXML design. It is a formula, not a missing formula. Its master is keyed by worksheet plus shared index, with the raw master expression and ref range preserved here. No formulas were expanded or recalculated.',
                  'formula_columns':list(formcols.values()),'shared_groups':list(groups.values())}
    if total!=sum(s['formula_count'] for s in inv['sheets']):raise RuntimeError('Formula ledger count mismatch '+name)
    json_write(d/'shared_formula_groups.json',group_result)
    formula_summaries.append({k:group_result[k] for k in ['workbook','formula_cells','formula_without_cached_value_count','shared_followers_without_text','nonshared_formula_without_text','shared_groups_without_master']})
    inv['comment_review_file']=str((d/'comments_and_style_review.json').relative_to(base));inv['shared_formula_groups_file']=str((d/'shared_formula_groups.json').relative_to(base));json_write(d/'inventory.json',inv)
    summary['workbooks'].append({k:inv[k] for k in ['file_name','bytes','sha256','valid_xlsx','zip_crc_error_member']}|{'sheet_count':len(inv['sheets']),'timed_records':sum(s.get('data_row_count',0) for s in inv['sheets']),'formula_cells':total,'inventory':str((d/'inventory.json').relative_to(base))})
with (base/'sheet_inventory.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(sheet_rows[0]));w.writeheader();w.writerows(sheet_rows)
with (base/'source_comments.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(comment_rows[0]));w.writeheader();w.writerows(comment_rows)
json_write(base/'formula_summary.json',formula_summaries)
summary['ambient_duplicate_identical']=hashlib.sha256((source/'CB-DA-AMB-direct.xlsx').read_bytes()).hexdigest()==hashlib.sha256((source/'CB-DA-AMB.xlsx').read_bytes()).hexdigest() if (source/'CB-DA-AMB-direct.xlsx').exists() else None
summary['sheet_count']=len(sheet_rows);summary['timed_records_total']=sum(r['timed_record_count'] or 0 for r in sheet_rows);summary['source_formula_cells_total']=sum(r['source_formula_count_all_cells'] for r in sheet_rows)
json_write(base/'summary.json',summary)
print(json.dumps(summary,indent=2))
