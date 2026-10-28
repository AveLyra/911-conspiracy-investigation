"""Read-only lexical accounting; no telemetry, sensor or historical-clock validation."""
from pathlib import Path
import argparse,collections,hashlib,json,re

p=argparse.ArgumentParser()
p.add_argument('--candidate',type=Path,required=True)
p.add_argument('--directory-index',type=Path,required=True)
p.add_argument('--capture-index',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
root=Path(__file__).parent
pins={x['id']:x for x in json.loads((root/'SOURCES.json').read_text())}
paths={'C01':a.candidate,'IDX-DIRECTORY':a.directory_index,'IDX-CAPTURE':a.capture_index}
checks=[]
for sid,path in paths.items():
 b=path.read_bytes()
 assert len(b)==pins[sid]['bytes']
 assert hashlib.sha256(b).hexdigest()==pins[sid]['sha256'],sid
 checks.append(dict(id=sid,bytes=len(b),sha256=pins[sid]['sha256']))
b=a.candidate.read_bytes();text=b.decode('utf-8',errors='strict');lines=text.splitlines()
c=collections.Counter(lines)
numeric=[i+1 for i,x in enumerate(lines) if re.fullmatch(r'[+-]?(?:[0-9]+(?:[.][0-9]*)?|[.][0-9]+)',x.strip())]
times=[i+1 for i,x in enumerate(lines) if re.fullmatch(r'(?:[0-9]{1,2}:)?[0-9]{2}:[0-9]{2}(?:[.][0-9]+)?',x.strip())]
index=json.loads(a.directory_index.read_text())
rows=[dict(zip(index[0],x)) for x in index[1:]]
capture=json.loads(a.capture_index.read_text())
assert any(x['original'].endswith('/AA77_ParamsTabular.txt') for x in rows)
assert len(capture)==2 and capture[1][1].endswith('/AA77_ParamsTabular.txt')
selected=[1,2,3,4,48]
result=dict(source_checks=checks,lines=len(lines),distinct_line_strings=len(c),repeated_string_types=sum(n>1 for n in c.values()),duplicate_occurrences_beyond_first=len(lines)-len(c),blank_lines=sum(not x.strip() for x in lines),numeric_whole_line_positions=numeric,time_literal_whole_line_positions=times,tab_bytes=b.count(b'\t'),comma_bytes=b.count(b','),crlf_pairs=b.count(b'\r\n'),lf_bytes=b.count(b'\n'),cr_bytes=b.count(b'\r'),selected_lines=[dict(line=i,text=lines[i-1]) for i in selected],most_repeated_strings=[dict(text=k,occurrences=v) for k,v in c.most_common(8)],directory_index_rows=len(rows),exact_url_digest_variant_rows=len(capture)-1,source_hashes_unchanged=all(hashlib.sha256(path.read_bytes()).hexdigest()==pins[sid]['sha256'] for sid,path in paths.items()),limitations=['Lexical counts are not sensor/channel counts or validated measurements','No full NTSB CSV/layout/Time Correlation Report acquired','Observed filtered archive rows are not complete historical site holdings','No inference about source editing,clock calibration or aircraft/custody'])
assert result['source_hashes_unchanged']
a.out.mkdir(parents=True,exist_ok=False)
with (a.out/'RESULT.json').open('x') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
