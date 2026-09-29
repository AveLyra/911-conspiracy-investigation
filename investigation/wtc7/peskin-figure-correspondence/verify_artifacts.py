"""Closeout integrity/link checks, not additional historical measurements."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

BASE=Path(__file__).resolve().parent
RUNS=['dense00','dense11','dense12','dense13']


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError('frozen verification output')
    files=[f for f in BASE.rglob('*') if f.is_file()]
    assert not any(f.is_symlink() for f in BASE.rglob('*'))
    py=[f for f in files if f.suffix=='.py'];js=[f for f in files if f.suffix=='.json'];md=[f for f in files if f.suffix=='.md']
    for f in py:ast.parse(f.read_text())
    for f in js:json.loads(f.read_text())
    local_links=0
    for f in md:
        text=f.read_text()
        assert all(line.rstrip()==line for line in text.splitlines()),'trailing whitespace'
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            target=target.strip().strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://',target) or target.startswith('#'):continue
            target=unquote(target.split('#',1)[0])
            path=Path(target) if target.startswith('/') else f.parent/target
            assert path.exists(),f'broken local link in {f.name}'
            local_links+=1
    checked_files=0;receipts={};surface_pairs=native_pairs=frames=0
    for name in RUNS:
        pair=[]
        for run in [name,name.replace('dense','repro')]:
            folder=BASE/run;receipt=json.loads((folder/'receipt.json').read_text())
            assert receipt['status']=='completed'
            assert {f.name for f in folder.iterdir()}==set(receipt['outputs'])|{'receipt.json'}
            for filename,pin in receipt['outputs'].items():
                f=folder/filename
                assert f.resolve().parent==folder.resolve()
                assert f.stat().st_size==pin['bytes'] and sha(f)==pin['sha256']
                checked_files+=1
            receipts[run]=sha(folder/'receipt.json');pair.append(receipt)
        first,again=pair
        assert again['compare_to']==name
        for key in ['script_sha256','core_sha256','dependency_pins','interval','source_before','source_after','tools','python','numpy','pillow','frame_count','shortlist_indices']:
            assert first[key]==again[key],f'reproduction identity: {key}'
        for filename in ['frames.json','results.json']:
            assert (BASE/name/filename).read_bytes()==(BASE/name.replace('dense','repro')/filename).read_bytes()
        frames+=first['frame_count'];surface_pairs+=again['reproduction_surface_comparisons'];native_pairs+=again['reproduction_native_pixel_matches']
    s1=json.loads((BASE/'primary-summary.json').read_text());s2=json.loads((BASE/'reproduced-summary.json').read_text())
    assert s1['results']==s2['results'] and len(s2['reproductions'])==4
    assert (BASE/'regions01.json').read_bytes()==(BASE/'regions02.json').read_bytes()
    i1=json.loads((BASE/'independent-result-check01.json').read_text());i2=json.loads((BASE/'independent-result-root01.json').read_text())
    assert {k:v for k,v in i1.items() if k!='argv'}=={k:v for k,v in i2.items() if k!='argv'}
    assert (frames,surface_pairs,native_pairs)==(959,1918,59)
    assert len(list(BASE.rglob('native-*.png')))==59
    size=sum(f.stat().st_size for f in files);assert size<2*1024**3
    result={'status':'passed','script_sha256':sha(Path(__file__)),'python_AST_count':len(py),'JSON_parse_count':len(js),
        'markdown_count':len(md),'local_links_checked':local_links,'run_manifest_files_checked':checked_files,
        'frame_count':frames,'reproduced_surface_pairs':surface_pairs,'reproduced_native_pixel_pairs':native_pairs,
        'unit_bytes_before_this_receipt':size,'run_receipt_pins':receipts,
        'final_document_pins':{f.name:{'sha256':sha(f),'bytes':f.stat().st_size} for f in md},
        'limits':'File/recipe integrity and reported completed reproduction agreement; not physical/source-clock validation or disclosure clearance.'}
    with a.output.open('x') as stream:json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['run_receipt_pins','final_document_pins']}))


if __name__=='__main__':main()
