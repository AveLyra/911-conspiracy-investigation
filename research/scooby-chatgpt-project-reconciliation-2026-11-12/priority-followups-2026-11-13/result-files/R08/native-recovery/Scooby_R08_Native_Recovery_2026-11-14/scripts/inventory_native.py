#!/usr/bin/env python3
"""Read-only OOXML inventory. Python standard library; originals never resaved.

Stored XML values and formula/cached-value provenance are preserved separately.
All statistics, date conversions, time deltas and joins are DERIVED, not cells.
Excel numeric dates are interpreted with the workbook epoch, without inventing
a timezone. A data sheet is identified here by its observed row-1 time headings.
No filtering, interpolation, value correction, or structural model is performed.
"""
from pathlib import Path
import argparse,collections,csv,datetime,gzip,hashlib,io,json,math,posixpath,re,statistics,zipfile
import xml.etree.ElementTree as ET

S='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='http://schemas.openxmlformats.org/package/2006/relationships'
X='http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
T=lambda n:f'{{{S}}}{n}'

def col_index(s):
    v=0
    for c in s:v=v*26+ord(c)-64
    return v
def col_label(n):
    r=''
    while n:n,d=divmod(n-1,26);r=chr(65+d)+r
    return r
def bounds(ref):
    m=re.fullmatch(r'([A-Z]+)(\d+)',ref);return int(m[2]),col_index(m[1])
def range_of(refs):
    if not refs:return None
    rr=[bounds(r) for r in refs];return f'{col_label(min(c for r,c in rr))}{min(r for r,c in rr)}:{col_label(max(c for r,c in rr))}{max(r for r,c in rr)}'
def add_extent(e,ref):
    r,c=bounds(ref)
    if not e:return [r,c,r,c]
    return [min(e[0],r),min(e[1],c),max(e[2],r),max(e[3],c)]
def fmt_extent(e):
    return None if not e else f'{col_label(e[1])}{e[0]}:{col_label(e[3])}{e[2]}'
def rels(z,name):
    relname=posixpath.join(posixpath.dirname(name),'_rels',posixpath.basename(name)+'.rels')
    if relname not in z.namelist():return {}
    return {x.get('Id'):{**x.attrib,'resolved':posixpath.normpath(posixpath.join(posixpath.dirname(name),x.get('Target','')))} for x in ET.fromstring(z.read(relname))}
def text_of(el):
    if el is None:return None
    return ''.join(x.text or '' for x in el.iter() if x.tag in [T('t'),f'{{{A}}}t'])
def decode(c,strings):
    typ=c.get('t','n');v=c.find(T('v'));f=c.find(T('f'));inline=c.find(T('is'))
    raw=None if v is None else v.text
    resolved=raw
    if typ=='s' and raw is not None:resolved=strings[int(raw)]
    elif typ=='inlineStr':resolved=text_of(inline)
    return {'cell':c.get('r'),'type':typ,'style_id':int(c.get('s','0')),
            'raw_v':raw,'resolved':resolved,'formula':None if f is None else {'text':f.text,'attributes':dict(f.attrib)},
            'cached_v_element_present':v is not None if f is not None else None,
            'cached_value_present':(v is not None and v.text is not None) if f is not None else None}
def json_write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def date_str(value,date1904=False):
    base=datetime.datetime(1904,1,1) if date1904 else datetime.datetime(1899,12,30)
    return (base+datetime.timedelta(days=float(value))).isoformat(timespec='microseconds')
def safe_name(x):return re.sub(r'[^\w.-]+','_',x)

def inventory(path,out):
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest();dest=out/path.stem;dest.mkdir(parents=True,exist_ok=True)
    inv={'file':str(path),'file_name':path.name,'bytes':len(raw),'sha256':sha,'method':'read-only ZIP/XML; all summaries derived; source lexical values retained in metadata/header/formula exports',
         'sheets':[],'zip_members':[],'warnings':[]}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        inv['zip_crc_error_member']=z.testzip();inv['valid_xlsx']='xl/workbook.xml' in z.namelist() and '[Content_Types].xml' in z.namelist() and inv['zip_crc_error_member'] is None
        inv['zip_members']=[{'name':x.filename,'uncompressed_bytes':x.file_size,'compressed_bytes':x.compress_size,'crc32':f'{x.CRC:08x}'} for x in z.infolist()]
        wb=ET.fromstring(z.read('xl/workbook.xml'));wbr=rels(z,'xl/workbook.xml')
        inv['workbook_properties']=wb.find(T('workbookPr')).attrib if wb.find(T('workbookPr')) is not None else {}
        inv['calculation_properties']=wb.find(T('calcPr')).attrib if wb.find(T('calcPr')) is not None else {}
        inv['defined_names']=[{'attributes':x.attrib,'text':x.text} for x in wb.findall(T('definedNames')+'/'+T('definedName'))]
        inv['document_properties']={}
        for pn in ['docProps/core.xml','docProps/app.xml','docProps/custom.xml']:
            if pn in z.namelist():
                pr=ET.fromstring(z.read(pn));inv['document_properties'][pn]=[{'tag':x.tag,'attributes':x.attrib,'text':x.text,'nested_xml':ET.tostring(x,encoding='unicode') if len(x) else None} for x in pr]
        date1904=inv['workbook_properties'].get('date1904') in ['1','true']
        strings=[text_of(x) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in z.namelist() else []
        inv['shared_string_count']=len(strings)
        styles={}
        if 'xl/styles.xml' in z.namelist():
            sty=ET.fromstring(z.read('xl/styles.xml'))
            styles['number_formats']=[x.attrib for x in sty.findall(T('numFmts')+'/'+T('numFmt'))]
            styles['cell_formats']=[{'index':i,'attributes':x.attrib,'xml':ET.tostring(x,encoding='unicode')} for i,x in enumerate(sty.find(T('cellXfs')) or [])]
            styles['fills']=[ET.tostring(x,encoding='unicode') for x in sty.find(T('fills')) or []]
            styles['differential_formats']=[ET.tostring(x,encoding='unicode') for x in sty.find(T('dxfs')) or []]
        inv['styles']=styles
        inv['comments']=[]
        for n in z.namelist():
            if re.match(r'xl/comments\d*\.xml$',n):
                for c in ET.fromstring(z.read(n)).iter(T('comment')):
                    inv['comments'].append({'part':n,'attributes':c.attrib,'text':text_of(c)})
        formula_path=dest/'formulas_and_cached_values.ndjson.gz'
        errors_path=dest/'error_and_marker_cells.ndjson.gz'
        all_meta=[];sheet_summary=[]
        with gzip.open(formula_path,'wt',encoding='utf-8') as formout,gzip.open(errors_path,'wt',encoding='utf-8') as errout:
            for sh in wb.find(T('sheets')):
                sheet_name=sh.get('name');part=wbr[sh.get(f'{{{R}}}id')]['resolved'];srels=rels(z,part)
                sinv={'sheet':sheet_name,'attributes':sh.attrib,'part':part,'relationships':srels,'declared_dimension':None,
                      'xml_cell_count':0,'nonempty_cell_count':0,'formula_count':0,'formula_without_cached_value_count':0,
                      'type_counts':collections.Counter(),'style_counts':collections.Counter(),'merged_ranges':[],
                      'hidden_rows':[],'hidden_columns':[],'column_dimensions':[],'conditional_formatting':[],
                      'data_validation':[],'drawing_anchors':[],'header_cells':[],'nondata_cells_file':None,'non_time_series_cells':[]}
                declared_e=[];nonempty_e=[];cols={};data_sheet=False;first_rows=[];last_rows=collections.deque(maxlen=3);meta=[];timestamps=[];seconds=[];record_rows=[]
                with z.open(part) as stream:
                    context=ET.iterparse(stream,events=('start','end'))
                    _,root=next(context)
                    for event,el in context:
                        if event!='end':continue
                        tag=el.tag
                        if tag==T('dimension'):sinv['declared_dimension']=el.get('ref')
                        elif tag==T('col'):
                            sinv['column_dimensions'].append(el.attrib)
                            if el.get('hidden')=='1':sinv['hidden_columns'].append(el.attrib)
                        elif tag==T('mergeCell'):sinv['merged_ranges'].append(el.get('ref'))
                        elif tag==T('conditionalFormatting'):sinv['conditional_formatting'].append(ET.tostring(el,encoding='unicode'))
                        elif tag==T('dataValidation'):sinv['data_validation'].append(ET.tostring(el,encoding='unicode'))
                        elif tag==T('row'):
                            rown=int(el.get('r'));cells=[decode(c,strings) for c in el if c.tag==T('c')]
                            if el.get('hidden')=='1':sinv['hidden_rows'].append(rown)
                            if rown==1:
                                headers={c['cell']:c for c in cells if c['resolved'] is not None}
                                data_sheet=any(c['cell']=='B1' and c['resolved']=='Test Time (s)' for c in cells) and any(c['cell']=='A1' and isinstance(c['resolved'],str) and c['resolved'].strip().startswith(('Test Time','Time')) for c in cells)
                                sinv['data_sheet_by_observed_time_headers']=data_sheet
                                sinv['header_cells']=list(headers.values())
                            is_record=False
                            if data_sheet and rown>1:
                                clock={c['cell']:c for c in cells if c['cell'] in ['A'+str(rown),'B'+str(rown)]}
                                try:
                                    is_record=all(math.isfinite(float(clock[cc+str(rown)]['resolved'])) for cc in ['A','B'])
                                except (ValueError,TypeError,KeyError):is_record=False
                                if is_record:record_rows.append(rown)
                            for c in cells:
                                ref=c['cell'];r,ci=bounds(ref);cl=col_label(ci);value=c['resolved'];formula=c['formula'];nonempty=value is not None or formula is not None
                                declared_e=add_extent(declared_e,ref);sinv['xml_cell_count']+=1;sinv['type_counts'][c['type']]+=1;sinv['style_counts'][str(c['style_id'])]+=1
                                if nonempty:nonempty_e=add_extent(nonempty_e,ref);sinv['nonempty_cell_count']+=1
                                if formula is not None:
                                    sinv['formula_count']+=1
                                    if not c['cached_value_present']:sinv['formula_without_cached_value_count']+=1
                                    formout.write(json.dumps({'sheet':sheet_name,**c},ensure_ascii=False)+'\n')
                                if not data_sheet:
                                    if nonempty:meta.append(c)
                                    continue
                                if rown==1:continue
                                if not is_record:
                                    if nonempty:sinv['non_time_series_cells'].append(c)
                                    continue
                                st=cols.setdefault(cl,{'column':cl,'header_cell':cl+'1','header':headers.get(cl+'1',{}).get('resolved'),
                                    'xml_present_count':0,'nonempty_count':0,'numeric_count':0,'formula_count':0,'formula_cached_numeric_count':0,
                                    'blank_explicit_count':0,'error_count':0,'non_numeric_count':0,'nonfinite_count':0,'text_value_counts':collections.Counter(),
                                    'first_nonempty_cell':None,'last_nonempty_cell':None,'minimum':None,'maximum':None,'zeros':0,'styles':collections.Counter(),
                                    'first_numeric_lexical':None,'last_numeric_lexical':None,'first_nonempty_row':None,'last_nonempty_row':None,'missing_internal_runs':[]})
                                st['xml_present_count']+=1;st['styles'][str(c['style_id'])]+=1
                                if formula is not None:st['formula_count']+=1
                                if not nonempty:st['blank_explicit_count']+=1;continue
                                st['nonempty_count']+=1
                                if st['first_nonempty_cell'] is None:st['first_nonempty_cell']=ref;st['first_nonempty_row']=rown
                                if st['last_nonempty_row'] is not None and rown>st['last_nonempty_row']+1:st['missing_internal_runs'].append([st['last_nonempty_row']+1,rown-1])
                                st['last_nonempty_cell']=ref;st['last_nonempty_row']=rown
                                if c['type']=='e':
                                    st['error_count']+=1;errout.write(json.dumps({'sheet':sheet_name,'kind':'excel_error',**c},ensure_ascii=False)+'\n')
                                elif c['type'] in ['n','b'] and value is not None:
                                    try:
                                        num=float(value)
                                        if not math.isfinite(num):st['nonfinite_count']+=1
                                        else:
                                            st['numeric_count']+=1
                                            if formula is not None:st['formula_cached_numeric_count']+=1
                                            if st['first_numeric_lexical'] is None:st['first_numeric_lexical']=value
                                            st['last_numeric_lexical']=value
                                            st['minimum']=num if st['minimum'] is None else min(st['minimum'],num)
                                            st['maximum']=num if st['maximum'] is None else max(st['maximum'],num)
                                            st['zeros']+=num==0
                                            if cl=='A':timestamps.append((ref,num,value))
                                            if cl=='B':seconds.append((ref,num,value))
                                    except ValueError:st['non_numeric_count']+=1;st['text_value_counts'][str(value)]+=1
                                else:
                                    st['non_numeric_count']+=1;st['text_value_counts'][str(value)]+=1
                                    if value is not None:errout.write(json.dumps({'sheet':sheet_name,'kind':'nonnumeric_in_data',**c},ensure_ascii=False)+'\n')
                            if data_sheet:
                                if rown<=4:first_rows.extend(cells)
                                if any(c['resolved'] is not None for c in cells):last_rows.append(cells)
                            el.clear();root.clear()
                sinv['xml_cell_extent']=fmt_extent(declared_e);sinv['nonempty_extent']=fmt_extent(nonempty_e)
                if data_sheet:
                    sinv['data_rows_start']=min(record_rows) if record_rows else None;sinv['data_rows_end']=max(record_rows) if record_rows else None
                    sinv['data_row_count']=len(record_rows)
                    sinv['data_row_definition']='Rows with both A timestamp/time-of-day and B elapsed-time stored numeric values; non-timed cells preserved separately'
                    sinv['data_rows_contiguous']=len(record_rows)==max(record_rows)-min(record_rows)+1 if record_rows else None
                    sinv['data_column_count']=nonempty_e[3] if nonempty_e else 0
                    sinv['time_series_extent_including_header']=f"A1:{col_label(sinv['data_column_count'])}{sinv['data_rows_end']}" if record_rows else None
                    for ci in range(1,sinv['data_column_count']+1):
                        cl=col_label(ci)
                        if cl not in cols:cols[cl]={'column':cl,'header':headers.get(cl+'1',{}).get('resolved'),'nonempty_count':0,'xml_present_count':0}
                        st=cols[cl];st['blank_or_absent_count']=sinv['data_row_count']-st['nonempty_count'];st['absent_xml_count']=sinv['data_row_count']-st['xml_present_count']
                    sinv['columns']=[cols[col_label(c)] for c in sorted(col_index(c) for c in cols)]
                    sinv['time_series_formula_count']=sum(c.get('formula_count',0) for c in sinv['columns'])
                    sinv['time_columns_derived']={}
                    for col,vals,isdate in [('A',timestamps,True),('B',seconds,False)]:
                        ds=[(vals[i][1]-vals[i-1][1])*(86400 if isdate else 1) for i in range(1,len(vals))]
                        td={'header_cell':col+'1','sample_count':len(vals),'first':vals[0] if vals else None,'last':vals[-1] if vals else None,
                            'delta_units':'seconds (Excel serial day differences multiplied by 86400)' if isdate else 'seconds',
                            'delta_count':len(ds),'minimum_delta':min(ds) if ds else None,'median_delta':statistics.median(ds) if ds else None,
                            'maximum_delta':max(ds) if ds else None,'nonpositive_delta_count':sum(d<=0 for d in ds),
                            'delta_frequency_rounded_6_decimal_seconds':collections.Counter(round(d,6) for d in ds)}
                        if isdate and vals:
                            if vals[0][1]>=1:
                                td['derived_first_datetime_unspecified_timezone']=date_str(vals[0][1],date1904)
                                td['derived_last_datetime_unspecified_timezone']=date_str(vals[-1][1],date1904)
                            else:
                                td['derived_first_time_of_day']=date_str(vals[0][1],date1904).split('T')[1]
                                td['derived_last_time_of_day']=date_str(vals[-1][1],date1904).split('T')[1]
                                td['date_not_encoded_in_numeric_clock_column']=True
                                td['observed_clock_header']=headers.get(col+'1',{}).get('resolved')
                        median=statistics.median(ds) if ds else 0
                        td['non_nominal_delta_pairs']=[{'from_cell':vals[i-1][0],'to_cell':vals[i][0],'from_lexical_value':vals[i-1][2],'to_lexical_value':vals[i][2],'derived_delta_seconds':d} for i,d in enumerate(ds,start=1) if abs(d-median)>max(0.01,abs(median)*0.01)]
                        sinv['time_columns_derived'][col]=td
                    preview={'first_rows_observed':first_rows,'last_three_rows_observed':list(last_rows)}
                    json_write(dest/(safe_name(sheet_name)+'_preview.json'),preview)
                    if len(timestamps)==len(seconds) and timestamps:
                        diffs=[(a[1]-timestamps[0][1])*86400-(b[1]-seconds[0][1]) for a,b in zip(timestamps,seconds)]
                        sinv['timestamp_vs_elapsed_offset_derived_seconds']={'minimum':min(diffs),'maximum':max(diffs),'first':diffs[0],'last':diffs[-1],'method':'(A-A_first)*86400-(B-B_first); no timezone inferred'}
                else:
                    mp=dest/(safe_name(sheet_name)+'_observed_cells.json');json_write(mp,meta);sinv['nondata_cells_file']=str(mp.relative_to(out));all_meta.extend({'sheet':sheet_name,**c} for c in meta)
                for rid,rel in srels.items():
                    if not rel['Type'].endswith('/drawing'):continue
                    dpart=rel['resolved'];drels=rels(z,dpart)
                    if dpart not in z.namelist():continue
                    for anchor in ET.fromstring(z.read(dpart)):
                        ai={'part':dpart,'anchor_type':anchor.tag.rsplit('}',1)[-1],'attributes':anchor.attrib,'from':None,'to':None,'pictures':[],'texts':[]}
                        for bound in ['from','to']:
                            ar=anchor.find(f'{{{X}}}{bound}')
                            if ar is not None:ai[bound]={v.tag.rsplit('}',1)[-1]:v.text for v in ar}
                        for pic in anchor.findall(f'{{{X}}}pic'):
                            pr=pic.find(f'{{{X}}}nvPicPr/{{{X}}}cNvPr');blip=pic.find(f'{{{X}}}blipFill/{{{A}}}blip');rid2=blip.get(f'{{{R}}}embed') if blip is not None else None
                            ai['pictures'].append({'properties':pr.attrib if pr is not None else {},'relationship':drels.get(rid2),'crop':pic.find(f'{{{X}}}blipFill/{{{A}}}srcRect').attrib if pic.find(f'{{{X}}}blipFill/{{{A}}}srcRect') is not None else None})
                        ai['texts']=[t.text for t in anchor.iter(f'{{{A}}}t')];sinv['drawing_anchors'].append(ai)
                inv['sheets'].append(sinv)
                print(json.dumps({'file':path.name,'sheet':sheet_name,'range':sinv['nonempty_extent'],'formulas':sinv['formula_count'],'data_rows':sinv.get('data_row_count'),'columns':sinv.get('data_column_count')}),flush=True)
        json_write(dest/'observed_metadata_cells.json',all_meta)
        json_write(dest/'inventory.json',inv)
        with (dest/'channel_headers_and_quality.csv').open('w',newline='',encoding='utf-8') as f:
            fields=['sheet','column','header_cell','header','first_nonempty_cell','last_nonempty_cell','numeric_count','formula_count','formula_cached_numeric_count','blank_or_absent_count','blank_explicit_count','absent_xml_count','error_count','non_numeric_count','nonfinite_count','minimum','maximum','zeros']
            w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
            for sh in inv['sheets']:
                for c in sh.get('columns',[]):w.writerow({'sheet':sh['sheet'],**c})
    if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise RuntimeError('Source changed during audit')
    return {k:inv[k] for k in ['file_name','bytes','sha256','valid_xlsx','zip_crc_error_member']}|{'sheet_count':len(inv['sheets']),'inventory':str((dest/'inventory.json').relative_to(out))}

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path('r08_work/direct_get/native'));p.add_argument('--out',type=Path,default=Path('r08_work/native_inventory'));p.add_argument('--only',nargs='*');args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    found=[]
    for name in ['drawings.xlsx','CB-DA-AMB.xlsx','CB-DA.xlsx','CB-DA-SC.xlsx','CB-SP.xlsx','CB-SP-SC.xlsx']:
        if args.only and name not in args.only:continue
        path=args.input/name
        if path.exists():found.append(inventory(path,args.out))
    dup=args.input/'CB-DA-AMB-direct.xlsx';canonical=args.input/'CB-DA-AMB.xlsx'
    summary={'workbooks':found,'ambient_duplicate_identical':hashlib.sha256(dup.read_bytes()).hexdigest()==hashlib.sha256(canonical.read_bytes()).hexdigest() if dup.exists() and canonical.exists() else None}
    json_write(args.out/'summary.json',summary)

if __name__=='__main__':main()
