"""Check disclosed manual transcriptions; does not read or validate tape data."""
from pathlib import Path
import argparse, hashlib, json

def seconds(text):
    h,m,s=map(int,text.split(':'))
    assert 0<=h<24 and 0<=m<60 and 0<=s<60
    return h*3600+m*60+s

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory',type=Path,default=Path(__file__).parent)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    raw=(args.directory/'LABELS.json').read_bytes(); data=json.loads(raw)
    checks=[]
    tables=data['tables']; reference=tables['7603836']['rows']
    assert len(reference)==7
    assert len({(x['channel'],x['printed_id']) for x in reference})==7
    checks.append('Seven unique LCN/BCN rows; DARC excluded from this count')
    comparisons={}
    for source in ['7603839','34916079']:
        rows=tables[source]['rows']
        assert len(rows)==len(reference)
        actual=[dict(index=i+1,matches=(a==b)) for i,(a,b) in enumerate(zip(reference,rows))]
        assert all(x['matches'] for x in actual)
        comparisons[source]=actual
    checks.append('Seven transcribed rows match in each of two repeated lists; dependence retained')
    overlaps={}
    for channel,expected in [('LCN',[9,10,9]),('BCN',[10,9])]:
        rows=[x for x in reference if x['channel']==channel]
        for row in rows: assert seconds(row['start'])<=seconds(row['stop'])
        values=[seconds(a['stop'])-seconds(b['start']) for a,b in zip(rows,rows[1:])]
        assert values==expected
        overlaps[channel]=[dict(first=a['printed_id'],second=b['printed_id'],label_overlap_seconds=n)
          for a,b,n in zip(rows,rows[1:],values)]
    checks.append('Five adjacent nominal label overlaps reproduced, without clock/continuity interpretation')
    first,later=data['host_impoundment']
    assert first['printed_ids']==['ID1633','ID1635','ID1636']
    assert later['printed_ids']==['ID1633','ID1635','ID1658']
    checks.append('1636 and1658 retained as different printed IDs; no selected correction')
    memo=data['memo_reel_labels']
    assert {r['date'] for r in memo['requested']}=={'9/11/01'}
    assert [r['date'] for r in memo['retrieved']]==['9/12/01','9/11/01','9/12/01']
    checks.append('Request and retrieved recording-label dates remain distinct')
    result=dict(input_sha256=hashlib.sha256(raw).hexdigest(),checks=checks,check_count=len(checks),
      repeated_list_comparisons=comparisons,nominal_adjacent_label_overlaps=overlaps,
      difference=dict(first_only=['ID1636'],later_only=['ID1658']),
      limits='Conditional on visible-source manual transcriptions; no native tape, physical continuity, independent clock calibration, cause or historical wrongdoing test')
    if args.output:
        with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
