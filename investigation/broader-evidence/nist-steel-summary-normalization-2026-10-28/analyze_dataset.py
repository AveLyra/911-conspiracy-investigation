from pathlib import Path
from decimal import Decimal,InvalidOperation
import argparse,csv,hashlib,io,json,collections,statistics,re

TARGETS={'W14A','W14B','C12A','C12B','M4','M14','M10A','M10B'}
def normalized_lookup(value):
    return re.sub(r'[-\s]','',value).upper()

def number(value):
    if value in ('','NA'):return None
    try:
        result=Decimal(value)
        return result if result.is_finite() else None
    except InvalidOperation:return None

def analyze(data_path,attribute_path):
    data_bytes=Path(data_path).read_bytes()
    attribute_bytes=Path(attribute_path).read_bytes()
    stream=io.StringIO(data_bytes.decode('utf-8-sig'))
    reader=csv.DictReader(stream)
    fields=reader.fieldnames
    rows=[]
    for row in reader:
        rows.append({'csv_line_end':reader.line_num,**row})
    attributes=list(csv.DictReader(io.StringIO(attribute_bytes.decode('utf-8-sig'))))
    assert len(set(fields))==len(fields)==22
    assert [r['Variable'] for r in attributes]==fields
    sources=[]
    residual_rows=[]
    matches=[]
    for source in sorted({r['Source'] for r in rows}):
        selected=[r for r in rows if r['Source']==source]
        valid=[]
        excluded=[]
        for row in selected:
            values=[number(row[k]) for k in ['RFy','FY002','FY20']]
            if any(v is None for v in values) or values[2]==0:
                excluded.append(row['csv_line_end']);continue
            reported,strength,denominator=values
            recomputed=strength/denominator
            delta=recomputed-reported
            out={'csv_line_end':row['csv_line_end'],'Source':source,
                 'Reference':row['Reference'],'Sample':row['Sample'],'specimen':row['specimen'],
                 'T':row['T'],'RFy':row['RFy'],'FY002':row['FY002'],'FY20':row['FY20'],
                 'conditional_recomputed_RFy':str(recomputed),'residual_recomputed_minus_reported':str(delta)}
            valid.append(out);residual_rows.append(out)
        values=[abs(Decimal(r['residual_recomputed_minus_reported'])) for r in valid]
        maxima=sorted(valid,key=lambda r:abs(Decimal(r['residual_recomputed_minus_reported'])),reverse=True)[:5]
        temperatures=[number(r['T']) for r in selected if number(r['T']) is not None]
        sample_values=[r['Sample'] for r in selected if r['Sample'] not in ('','NA')]
        sources.append({'Source':source,'rows':len(selected),
                        'references':dict(collections.Counter(r['Reference'] for r in selected)),
                        'specimen_values':sorted({r['specimen'] for r in selected}),
                        'Sample_nonmissing_rows':len(sample_values),'Sample_unique_nonmissing':len(set(sample_values)),
                        'Year_values':sorted({r['Year'] for r in selected}),
                        'tensile_test_T_range':[str(min(temperatures)),str(max(temperatures))],
                        'ratio_eligible_rows':len(valid),'ratio_excluded_csv_lines':excluded,
                        'max_abs_residual':str(max(values)) if values else None,
                        'median_abs_residual':str(statistics.median(values)) if values else None,
                        'largest_residual_rows':maxima})
    for row in rows:
        for key in ['Sample','specimen']:
            if normalized_lookup(row[key]) in TARGETS:
                matches.append({'csv_line_end':row['csv_line_end'],'field':key,'original_value':row[key],
                                'lookup_only_value':normalized_lookup(row[key])})
    return {'data_file_sha256':hashlib.sha256(data_bytes).hexdigest(),
            'attribute_file_sha256':hashlib.sha256(attribute_bytes).hexdigest(),
            'data_rows':len(rows),'columns':fields,'attribute_definitions':len(attributes),
            'attribute_order_exactly_matches_data_header':True,
            'source_groups':sources,'selected_candidate_field_matches':matches,
            'candidate_search_scope':'Sample/specimen fields only; strip hyphens/whitespace and uppercase for lookup, preserve original values. Not a custody/alias join or global absence search.',
            'ratio_scope':'Conditional RFy=FY002/FY20 recomputation with original inputs retained. No pass tolerance, baseline/rounding explanation, raw curve validation or scientific-error finding.',
            'RFy02_test_performed':False,
            'historical_temperature_or_custody_test':False},residual_rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',required=True)
    parser.add_argument('--attributes',required=True)
    parser.add_argument('--residuals-output',required=True)
    args=parser.parse_args()
    results,residuals=analyze(args.data,args.attributes)
    with Path(args.residuals_output).open('x') as f:
        json.dump(residuals,f,indent=2);f.write('\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__':
    main()
