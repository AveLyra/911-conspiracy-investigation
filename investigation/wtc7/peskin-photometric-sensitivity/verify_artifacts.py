"""Final local artifact integrity; not a physical or disclosure approval."""
import ast
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

BASE=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output=BASE/'verification01.json'
    if output.exists():raise FileExistsError('preserved closeout receipt')
    files=[p for p in BASE.rglob('*') if p.is_file()]
    assert not any(p.is_symlink() for p in BASE.rglob('*'))
    py=[p for p in files if p.suffix=='.py'];js=[p for p in files if p.suffix=='.json'];md=[p for p in files if p.suffix=='.md']
    for p in py:ast.parse(p.read_text())
    for p in js:json.loads(p.read_text())
    links=0
    for p in md:
        source=p.read_text()
        assert all(line.rstrip()==line for line in source.splitlines()),'trailing whitespace'
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',source):
            target=target.strip().strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://',target) or target.startswith('#'):continue
            target=unquote(target.split('#',1)[0]);q=Path(target) if target.startswith('/') else p.parent/target
            assert q.exists(),f'broken link in {p.name}: {target}'
            links+=1
    manifests=0
    for run in ['controls01','run01','run02']:
        folder=BASE/run;r=json.loads((folder/'receipt.json').read_text())
        assert r['status']=='completed' and r['script_sha256']==sha(BASE/'measure.py') and r['protocol_sha256']==sha(BASE/'PROTOCOL.md')
        assert r['elapsed_seconds']<300
        assert set(p.name for p in folder.iterdir())==set(r['outputs'])|{'receipt.json'}
        for name,pin in r['outputs'].items():
            p=folder/name;assert p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256'];manifests+=1
    assert json.loads((BASE/'controls01/controls.json').read_text())['passed']
    source=json.loads((BASE/'run01/results.json').read_text())
    for name,pin in source['inputs'].items():
        p=Path(name);assert p.stat().st_size==pin['bytes'] and sha(p)==pin['sha256']
    summary=json.loads((BASE/'summary01.json').read_text())
    assert summary['status']=='passed' and summary['script_sha256']==sha(BASE/'summarize.py')
    assert summary['source_sha256']==sha(BASE/'run01/results.json')
    assert summary['coverage']=={'pair_count':12,'branch_count':48,'fit_attempts':672}
    assert summary['reproduction']['arrays_compared']==208
    for run,pin in summary['reproduction']['run_receipt_pins'].items():assert sha(BASE/run/'receipt.json')==pin
    assert (BASE/'run01/results.json').read_bytes()==(BASE/'run02/results.json').read_bytes()
    assert sha(BASE/'run01/arrays.npz')==sha(BASE/'run02/arrays.npz')
    controls=json.loads((BASE/'independent-controls01.json').read_text())
    a=json.loads((BASE/'independent-check01.json').read_text());b=json.loads((BASE/'independent-root01.json').read_text())
    for r in [controls,a,b]:assert r['passed'] and r['checker_sha256']==sha(BASE/'independent_check.py') and r['protocol_sha256']==sha(BASE/'PROTOCOL.md')
    omitted={'argv','elapsed_seconds'}
    assert {k:v for k,v in a.items() if k not in omitted}=={k:v for k,v in b.items() if k not in omitted}
    size=sum(p.stat().st_size for p in files);assert size<100*1024**2
    result={'status':'passed','script_sha256':sha(Path(__file__)),'python_AST_count':len(py),'JSON_parse_count':len(js),
            'Markdown_count':len(md),'local_links_checked':links,'manifest_output_files_checked':manifests,
            'source_inputs_rehashed':len(source['inputs']),'unit_bytes_before_receipt':size,
            'final_document_pins':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in md},
            'limits':'Artifact integrity and previously completed numerical checks; not historical, physical, causal, legal or disclosure validation.'}
    with output.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='final_document_pins'},indent=2))


if __name__=='__main__':main()
