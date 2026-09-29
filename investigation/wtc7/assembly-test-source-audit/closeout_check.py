#!/usr/bin/env python3
"""Scoped artifact/receipt checks, not experimental or physical validation."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    base=Path(__file__).resolve().parent
    if Path(args.output).name != args.output:
        ap.error('unit-local output basename required')
    output=base/args.output
    if output.exists():
        ap.error('refuse overwrite')
    files=[p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and not re.fullmatch(r'closeout\d+\.json',p.name)]
    counts={'python':0,'json':0,'markdown':0,'local_markdown_links':0}
    for p in files:
        if p.suffix=='.py':
            ast.parse(p.read_text(),filename=str(p)); counts['python']+=1
        elif p.suffix=='.json':
            json.loads(p.read_text()); counts['json']+=1
        elif p.suffix=='.md':
            text=p.read_text(); counts['markdown']+=1
            assert not any(line.rstrip()!=line for line in text.splitlines()),p.name
            assert not re.search(r'^<<<<<<< |^=======$|^>>>>>>> ',text,re.M),p.name
            for link in re.findall(r'\]\(([^)]+)\)',text):
                target=link.strip('<>').split('#',1)[0]
                if not target or re.match(r'\w+://',target):
                    continue
                assert (p.parent/target).exists(),(p.name,target)
                counts['local_markdown_links']+=1
    pairs=[('root-results01.json','root-results02.json'),
           ('root-stage-results01.json','root-stage-results02.json')]
    for a,b in pairs:
        assert (base/a).read_bytes()==(base/b).read_bytes(),(a,b)
    receipts=[('tn1749-independent-results01.json','tn1749-independent-root01.json'),
              ('tn1749-comparison01.json','tn1749-comparison-root01.json'),
              ('independent-stage-results01.json','independent-stage-root01.json'),
              ('stage-comparison01.json','stage-comparison-root01.json')]
    for a,b in receipts:
        x=json.loads((base/a).read_text()); y=json.loads((base/b).read_text())
        x.pop('command'); y.pop('command'); assert x==y,(a,b)
    result={'status':'PASS','scope':'Artifact syntax, local links, byte equality and consumer receipts only.',
            'counts':counts,'root_pairs_byte_equal':pairs,
            'consumer_receipts_equal_except_command':receipts,
            'files':{str(p.relative_to(base)):digest(p) for p in sorted(files)}}
    with output.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps({'status':'PASS','counts':counts,'pinned_files':len(files),
                      'output_sha256':digest(output)}))


if __name__=='__main__':
    main()
