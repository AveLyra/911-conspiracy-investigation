from pathlib import Path
from decimal import Decimal
import argparse,csv,io,json,hashlib,collections

def analyze(path):
    data=Path(path).read_bytes()
    reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
    fields=reader.fieldnames
    rows=[{'csv_line':reader.line_num,**row} for row in reader]
    study=[r for r in rows if r['Source']=='This study']
    room=[r for r in study if Decimal(r['T'])==20]
    groups=[]
    for specimen in sorted({r['specimen'] for r in room}):
        selected=[r for r in room if r['specimen']==specimen]
        groups.append({'specimen':specimen,'rows':len(selected),
                       'csv_lines':[r['csv_line'] for r in selected],
                       'RFy_values':sorted({r['RFy'] for r in selected}),
                       'FY20_values':sorted({r['FY20'] for r in selected}),
                       'mean_FY002':str(sum(Decimal(r['FY002']) for r in selected)/len(selected)),
                       'meaning':'Exploratory descriptive mean; not the authenticated author baseline.'})
    c65=[r for r in room if r['specimen']=='C65_FL']
    rate_groups=[]
    for rate in sorted({r['dedt'] for r in c65},key=Decimal):
        selected=[r for r in c65 if r['dedt']==rate]
        rate_groups.append({'dedt':rate,'rows':len(selected),'mean_FY002':str(sum(Decimal(r['FY002']) for r in selected)/len(selected)),
                            'FY20_values':sorted({r['FY20'] for r in selected}),
                            'original_FY002_values':[r['FY002'] for r in selected]})
    original={'Specimen':'C65','T':'20','rate':'8.75e-5','S002':'264','S02':'370','Su':'469','Elt':'38','RA':'63.1','lm':'0'}
    matches=[]
    for r in study:
        if (r['specimen']=='C65_FL' and Decimal(r['T'])==20
            and Decimal(r['dedt'])==Decimal(original['rate'])
            and abs(Decimal(r['FY002'])-Decimal(original['S002']))<=Decimal('0.5')
            and all(Decimal(r[k])==Decimal(original[v]) for k,v in [('FY02','S02'),('TS','Su'),('Elt','Elt'),('RA','RA')])):
            matches.append({k:r[k] for k in ['csv_line','Sample','specimen','T','dedt','RFy','FY002','FY20','FY02','TS','Elt','RA']})
    low=Decimal('3.30e-5');high=Decimal('1.35e-4')
    within=[r for r in study if low<Decimal(r['dedt'])<high]
    outside=[r for r in study if not low<Decimal(r['dedt'])<high]
    return {'data_sha256':hashlib.sha256(data).hexdigest(),'This_study_rows':len(study),
            'room_temperature_rows':len(room),'all_room_RFy_unity':all(Decimal(r['RFy'])==1 for r in room),
            'room_groups':groups,'C65_all_room_mean_FY002':str(sum(Decimal(r['FY002']) for r in c65)/len(c65)),
            'C65_rate_groups':rate_groups,
            'original_report_tuple':original,'conditional_C65_table_to_CSV_matches':matches,
            'join_scope':'Tentative label cross-reference and explicit numeric precision allowance only. Not authenticated coupon identity.',
            'CSV_has_lm_field':'lm' in fields,
            'literal_Figure2_caption_rate_check':{'lower_exclusive':str(low),'upper_exclusive':str(high),'within_rows':len(within),'outside_rows':len(outside),'outside_csv_lines':[r['csv_line'] for r in outside]},
            'not_established':['Author-specific RFy baseline rule and implementation','Exact 2011 figure-to-current-CSV point identity','Candidate C65 coupon custody','Exclusion from analyses beyond Equation10','Effect on original 2005 collapse analysis']}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--data',required=True);args=parser.parse_args()
    print(json.dumps(analyze(args.data),indent=2))
if __name__=='__main__':main()
