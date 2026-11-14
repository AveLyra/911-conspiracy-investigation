#!/usr/bin/env python3
"""Read-only XLSX channel-to-dictionary audit. No workbook edits or data conversion."""
from pathlib import Path
import argparse, collections, csv, json, posixpath, re, zipfile
import xml.etree.ElementTree as ET

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
COLS = ['A','B','C','D','E','F','G']
SPEC_COL = {'CB-DA':'H','CB-DA-SC':'I','CB-SP':'J','CB-SP-SC':'K'}

def text_of_cell(c, strings):
    v=c.find('m:v',NS)
    raw=v.text if v is not None else None
    typ=c.get('t','n')
    value=raw
    if typ=='s' and raw is not None: value=strings[int(raw)]
    elif typ=='inlineStr': value=''.join(t.text or '' for t in c.findall('.//m:t',NS))
    f=c.find('m:f',NS)
    return {'value':value,'raw':raw,'type':typ,'style':c.get('s'),'formula_present':f is not None,
            'formula':None if f is None else f.text,'formula_attributes':{} if f is None else f.attrib}

def read_sources(path):
    result={}
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(t.text or '' for t in si.findall('.//m:t',NS)) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={r.get('Id'):r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for s in ET.fromstring(z.read('xl/workbook.xml')).find('m:sheets',NS):
            name=s.get('name')
            is_data=('Loading' in name or name.endswith(' Data'))
            if 'Channel List' not in name and not is_data: continue
            target=rels[s.get(RID)]
            part=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
            rows={}
            with z.open(part) as f:
                for _,el in ET.iterparse(f,events=['end']):
                    if el.tag.endswith('}row'):
                        rn=int(el.get('r'))
                        rows[rn]={c.get('r'):text_of_cell(c,strings) for c in el}
                        if is_data and rn>=2: break
                        el.clear()
            result[name]={'part':part,'rows':rows,'is_data':is_data}
    return result

def dictionary(sheet):
    result={}
    for rn,row in sheet['rows'].items():
        lab=row.get(f'B{rn}',{}).get('value')
        if not lab or lab=='Legend/ID': continue
        values={c:row.get(f'{c}{rn}',{}).get('value','') for c in list('ABCDEFGHIJK')}
        result.setdefault(lab,[]).append({'row':rn,'values':values})
    return result

def header_parts(raw):
    if not isinstance(raw,str): return '', '', '', '',False
    m=re.fullmatch(r'(.*)\(([^()]*)\)(\s*)',raw)
    if m and not m[2].startswith('Date:'):
        pre=m[1];unit=m[2]
        id_without_normal_separator=pre[:-1] if pre.endswith(' ') else pre
        return pre.strip(),unit,pre,'',id_without_normal_separator!=id_without_normal_separator.strip()
    annotation=m[2] if m else ''
    return raw.strip(),'',raw,annotation,raw!=raw.strip()

def fill_definition(out,prefix,entry,filename,sheet):
    if entry is None: return
    rn=entry['row'];v=entry['values']
    out[prefix+'_workbook']=filename;out[prefix+'_sheet']=sheet
    out[prefix+'_row']=rn
    for col,label in [('A','description'),('B','legend'),('C','group'),('D','type'),('E','range_low'),('F','range_high'),('G','unit')]:
        out[prefix+'_'+label]=v[col]
        out[prefix+'_'+label+'_cell']=f'{col}{rn}'

def unit_status(a,b):
    if not b: return 'no_dictionary_unit'
    if a==b: return 'literal_match'
    if a=='µmm/mm' and b=='microstrain': return 'notation_difference_no_values_converted'
    return 'unit_mismatch_unresolved'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native-dir',default='r08_work/direct_get/native');ap.add_argument('--output-dir',default='r08_work');ap.add_argument('--retrieval-manifest',default='r08_work/direct_get/attempts.json');args=ap.parse_args()
    native=Path(args.native_dir);outdir=Path(args.output_dir);outdir.mkdir(parents=True,exist_ok=True)
    files=['drawings.xlsx','CB-DA-AMB.xlsx','CB-DA.xlsx','CB-DA-SC.xlsx','CB-SP.xlsx','CB-SP-SC.xlsx']
    manifest={r['label']+'.xlsx':r for r in json.loads(Path(args.retrieval_manifest).read_text()) if r.get('valid_xlsx')}
    all_sources={name:read_sources(native/name) for name in files}
    (outdir/'channel_crosswalk_sources.json').write_text(json.dumps(all_sources,ensure_ascii=False,indent=2))
    drawing_dicts={k:dictionary(v) for k,v in all_sources['drawings.xlsx'].items()}
    records=[];unjoined=[];checks=[];unrepresented=[]
    for filename in files[1:]:
        specimen=filename[:-5];sheets=all_sources[filename];local=dictionary(sheets['Channel List'])
        ds='Channel List-AmbientTest' if specimen=='CB-DA-AMB' else 'Channel List-FireTests';drawing=drawing_dicts[ds]
        observed_ids=set()
        for name,sheet in sheets.items():
            if not sheet['is_data']: continue
            phase='ambient_baseline_specimen' if specimen=='CB-DA-AMB' else ('ambient_loading_of_fire_specimen' if 'Ambient' in name else 'fire_loading')
            for cell,cv in sheet['rows'].get(1,{}).items():
                raw=cv['value']
                if raw is None: continue
                lab,unit,pre,date_ann,extra_ws=header_parts(raw);observed_ids.add(lab)
                loc=local.get(lab,[]);dr=drawing.get(lab,[])
                loc1=loc[0] if len(loc)==1 else None;dr1=dr[0] if len(dr)==1 else None
                col=re.sub(r'\d','',cell);s2=sheet['rows'].get(2,{}).get(col+'2',{})
                kind='time_coordinate' if col in ['A','B'] else ('native_formula_summary' if lab.startswith('Avg') and s2.get('formula_present') else ('summary_named_channel' if lab.startswith('Avg') else 'measurement_channel'))
                r={'record_type':kind,'specimen':specimen,'phase':phase,'workbook':filename,'sheet':name,'xml_part':sheet['part'],
                   'source_requested_url':manifest[filename]['requested_url'],'source_final_url':manifest[filename]['final_url'],'source_sha256':manifest[filename]['native_file_sha256'],
                   'drawings_source_requested_url':manifest['drawings.xlsx']['requested_url'],'drawings_source_final_url':manifest['drawings.xlsx']['final_url'],'drawings_source_sha256':manifest['drawings.xlsx']['native_file_sha256'],
                   'header_cell':cell,'header_raw':raw,'parsed_legend':lab,'text_before_unit_parenthesis':pre,
                   'header_unit':unit,'date_annotation_not_a_unit':date_ann,'header_extra_edge_whitespace':extra_ws,
                   'local_join_status':'exact_id_after_explicit_unit_suffix_parse' if loc1 else ('ambiguous_id' if loc else 'unjoined'),
                   'drawings_join_status':'exact_id_after_explicit_unit_suffix_parse' if dr1 else ('ambiguous_id' if dr else 'unjoined'),
                   'sample_cell':col+'2','sample_formula_present':s2.get('formula_present',False),'sample_formula':s2.get('formula'),'sample_formula_attributes':json.dumps(s2.get('formula_attributes',{}),ensure_ascii=False),
                   'sample_cached_raw':s2.get('raw'),'sample_type':s2.get('type'),
                   'analysis_transformation':'header suffix parsed; legend surrounding whitespace trimmed; source strings retained; no measurement transformation',
                   'publication_uncertainty':'not assigned from native cells; see publication crosscheck separately'}
                fill_definition(r,'local',loc1,filename,'Channel List');fill_definition(r,'drawings',dr1,'drawings.xlsx',ds)
                r['unit_vs_local']=unit_status(unit,r.get('local_unit',''));r['unit_vs_drawings']=unit_status(unit,r.get('drawings_unit',''))
                if specimen in SPEC_COL:
                    r['drawings_usage_flag_cell']=f'{SPEC_COL[specimen]}{dr1["row"]}' if dr1 else ''
                    r['drawings_usage_flag']=dr1['values'][SPEC_COL[specimen]] if dr1 else ''
                    r['drawings_usage_flag_status']=('marked_X' if r['drawings_usage_flag']=='X' else 'not_marked_X') if dr1 else 'unjoined'
                    if dr1:
                        for sp,c in SPEC_COL.items():r['drawings_flag_'+sp]=dr1['values'][c]
                else:r['drawings_usage_flag_status']='ambient_dictionary_has_no_per_specimen_X_columns'
                dif=[]
                if loc1 and dr1:
                    for c,label in [('A','description'),('B','legend'),('C','group'),('D','type'),('E','range_low'),('F','range_high'),('G','unit')]:
                        if loc1['values'][c]!=dr1['values'][c]:dif.append(label)
                r['local_vs_drawings_different_fields']=';'.join(dif)
                r['publication_distance_cm']='';r['native_figure_dimension_expression_in']='';r['derived_figure_distance_cm']='';r['spatial_conflict']='';r['provisional_location_by_diagram']=''
                if specimen!='CB-DA-AMB' and lab in ['VD2','VD3','VD4','VD5']:
                    geo={'VD2':('132',335.28,336),'VD3':('132+84',548.64,548),'VD4':('504-132-84',731.52,732),'VD5':('504-132',944.88,944)}[lab]
                    r['publication_distance_cm']=geo[2];r['publication_distance_source']='TN2055 Table13 printed p70; west-column centerline'
                    r['native_figure_dimension_expression_in']=geo[0];r['derived_figure_distance_cm']=geo[1]
                    r['native_figure_source']='drawings.xlsx xl/media/image12.emf; InstrumentationLayout-FireTests FigC1 caption B32; parent visually inspected'
                    r['native_figure_datum']='west drawing datum; equality to Table13 west-column centerline not established'
                    r['figure_distance_derivation']='dimension expression in inches times 2.54; not an observed numeric worksheet cell'
                    r['spatial_conflict']='native dictionary description conflicts with figure ordering; preserve source descriptions and use figure/table crosscheck separately'
                    r['provisional_location_by_diagram']={'VD2':'western outer slab point','VD3':'western inner slab point','VD4':'eastern inner slab point','VD5':'eastern outer slab point'}[lab]
                if lab in ['RotLT1','RotLT2','RotLT3']:
                    r['provisional_location_by_diagram']={'RotLT1':'west loading truss','RotLT2':'middle loading truss','RotLT3':'east loading truss'}[lab]
                    r['rotation_diagram_source']='drawings.xlsx xl/media/image11.emf B1(f) and xl/media/image19.emf C6(b); parent visually inspected'
                    if specimen!='CB-DA-AMB' and lab!='RotLT2':r['spatial_conflict']='fire channel-list east/west description reverses original figure; diagram supports RotLT1 west and RotLT3 east'
                if specimen!='CB-DA-AMB' and lab in ['TCC1','TCC13']:
                    r['diagram_label_conflict']='image16.emf C4(a) duplicates TCC1 at southeast interior; C4(b) corresponding elevated label TCC13 south; no header renamed'
                records.append(r)
                if not loc1 or not dr1:unjoined.append({k:r.get(k) for k in ['workbook','sheet','header_cell','header_raw','parsed_legend','record_type','local_join_status','drawings_join_status','local_description','local_description_cell']})
                if dif or r['unit_vs_local']=='unit_mismatch_unresolved' or r['unit_vs_drawings']=='unit_mismatch_unresolved' or r.get('drawings_usage_flag_status')=='not_marked_X':checks.append(r)
        for where,defs in [('local',local),('drawings',drawing)]:
            for lab,entries in defs.items():
                if lab in observed_ids:continue
                for entry in entries:
                    if where=='drawings' and specimen!='CB-DA-AMB' and entry['values'][SPEC_COL[specimen]]!='X':continue
                    unrepresented.append({'specimen':specimen,'dictionary_source':where,'workbook':filename if where=='local' else 'drawings.xlsx','sheet':'Channel List' if where=='local' else ds,'legend':lab,'legend_cell':f'B{entry["row"]}','description':entry['values']['A'],'header_status':'not_present_in_any_measurement_sheet_of_this_workbook','X_flag':entry['values'].get(SPEC_COL.get(specimen,''),'')})
    fields=list(dict.fromkeys(k for row in records for k in row))
    with (outdir/'corrected_instrument_map.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
    (outdir/'instrument_map_unjoined_channels.json').write_text(json.dumps(unjoined,ensure_ascii=False,indent=2))
    (outdir/'instrument_map_dictionary_channels_without_headers.json').write_text(json.dumps(unrepresented,ensure_ascii=False,indent=2))
    (outdir/'instrument_map_definition_discrepancies.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
    summary={'rows':len(records),'by_workbook':{},'rows_unjoined_to_local':sum(r['local_join_status']=='unjoined' for r in records),
             'rows_unjoined_to_drawings':sum(r['drawings_join_status']=='unjoined' for r in records),
             'definition_discrepancy_rows':len(checks),'dictionary_only_rows':len(unrepresented),
             'unit_mismatch_rows':[r for r in records if r['unit_vs_local']=='unit_mismatch_unresolved' or r['unit_vs_drawings']=='unit_mismatch_unresolved'],
             'rotation_header_units':dict(collections.Counter(r['header_unit'] for r in records if r['parsed_legend'].startswith('Rot') and not r['header_unit']=='°C')),
             'native_workbooks_modified':False}
    summary['row_kinds']=dict(collections.Counter(r['record_type'] for r in records))
    summary['counts_are_header_occurrences_not_unique_sensors']=True
    summary['local_unjoined_by_kind']=dict(collections.Counter(r['record_type'] for r in records if r['local_join_status']=='unjoined'))
    summary['drawings_unjoined_by_kind']=dict(collections.Counter(r['record_type'] for r in records if r['drawings_join_status']=='unjoined'))
    summary['definition_difference_patterns']=dict(collections.Counter(r['local_vs_drawings_different_fields'] for r in checks))
    for filename in files[1:]:
        rr=[r for r in records if r['workbook']==filename]
        summary['by_workbook'][filename]={'headers':len(rr),'local_unjoined':sum(r['local_join_status']=='unjoined' for r in rr),'drawings_unjoined':sum(r['drawings_join_status']=='unjoined' for r in rr),'drawings_X_blank_despite_header':sum(r.get('drawings_usage_flag_status')=='not_marked_X' for r in rr)}
    (outdir/'instrument_map_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in summary.items() if k!='unit_mismatch_rows'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
