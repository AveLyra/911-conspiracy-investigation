#!/usr/bin/env python3
"""Bounded artifact/pin/replay checks, not scientific or legal validation."""
import argparse
import ast
import csv
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parent
PINS = {
    BASE/'report.md': '9b4d9c4b6a3a54b2abb4d1751fbc46d325d7ea981f76c832425c293c03c6e1ff',
    BASE/'report-before-source-context-review.md': 'ffd69a6903be6726cc66fa87d92a1a3ccfb0aa7b4605060cf6a51e3c7440c243',
    BASE/'nist-validation-review.md': '7391cceb80134aff4981208d4e433d6c77a54b6acb3ecf5548d1a1d12f98a92a',
    BASE/'final-inference-review.md': 'e4f8b9c6508b3ad514708d18e192b02fb0e134c3d02292467324bc17773304e5',
    BASE/'paper-source-review.md': '4fcbe40f6b35efad49b6ab12b7a14d7ba20d60a07b5cba19100977c8be3f8258',
    BASE/'retrospective-context.md': 'e96dd97311cdd4be9e980cce23c4effe41698563f8cb310a674837857782e681',
    BASE.parent/'material-run-crosswalk/report.md': 'a9afca6aa6221db2f96bb0d2720cadb7094532105f5e86661fb591b9315babcf',
    Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf'): '30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f',
    Path('/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf'): 'cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4',
    BASE/'retrospective-sources/nist-tn-1749-july2012-corrected-feb2013.pdf': '5d7461f298654ffb0c9f8df319298330d155fc2d8155d85abcd5391a4d748caf',
}
MANIFEST = Path('/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv')


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(name):
    return json.loads((BASE/name).read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    if Path(args.output).name != args.output or not args.output.endswith('.json'):
        ap.error('Use a new JSON basename')
    dest = BASE/args.output
    if dest.exists():
        ap.error('Refusing existing output')
    files = sorted(p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    before = {str(p.relative_to(BASE)): digest(p) for p in files}
    pins = {str(p): digest(p) for p in PINS}
    assert all(pins[str(p)] == value for p,value in PINS.items())
    counts = Counter()
    for p in files:
        if p.suffix == '.json':
            json.loads(p.read_text())
            counts['json_parsed'] += 1
        elif p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(p))
            counts['python_asts'] += 1
        elif p.suffix == '.md':
            s = p.read_text()
            assert all(line == line.rstrip() for line in s.splitlines()), p.name
            counts['markdown_whitespace_checked'] += 1
            for link in re.findall(r'\]\(([^)]+)\)', s):
                if link.startswith(('http:', 'https:', '#')):
                    continue
                target = link.split('#')[0].strip('<>')
                if not target:
                    continue
                resolved = Path(target) if target.startswith('/') else p.parent/target
                assert resolved.exists(), (p.name, target)
                counts['local_links_resolved'] += 1
    assert (BASE/'root-results01.json').read_bytes() == (BASE/'root-results02.json').read_bytes()
    a,b = read('capacity-independent-results01.json'), read('capacity-independent-root-replay02.json')
    assert a['result'] == b['result']
    assert [k for k in a if a[k] != b[k]] == ['command']
    a,b = read('capacity-comparison02.json'), read('capacity-comparison-root01.json')
    assert a['comparison'] == b['comparison']
    assert [k for k in a if a[k] != b[k]] == ['command']
    assert b['comparison']['status'] == 'PASS'
    assert b['comparison']['exact_rational_checks'] == 468
    assert b['comparison']['failures'] == []
    manifest_hash = digest(MANIFEST)
    assert manifest_hash == '30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf'
    with MANIFEST.open() as f:
        rows = list(csv.DictReader(f))
    ext = Counter(row['extension'] for row in rows)
    assert len(rows) == 25643
    assert ext == {'.int':25188, '.nod':173, '.png':272, '.apdl':3,
                   '[no extension]':3, '.pdf':1, '.zip':1, '.ppt':1, '.pptx':1}
    refusal = subprocess.run([sys.executable, str(BASE/'calc_capacity.py'), '--output',
                             str(BASE/'root-results01.json')], capture_output=True, text=True)
    assert refusal.returncode == 2 and 'Refusing to overwrite output' in refusal.stderr
    assert not refusal.stdout
    after = {str(p.relative_to(BASE)): digest(p) for p in files}
    assert before == after
    assert pins == {str(p): digest(p) for p in PINS}
    receipt = {'status':'PASS','runtime':sys.version,'command':[sys.executable,*sys.argv],
               'scope':'Pins, artifact syntax/links, consumer equality, extension counts and overwrite refusal; not physical validation.',
               'coverage':dict(counts), 'preserved_unit_files':len(files),
               'unchanged_unit_sha256':before, 'source_and_review_pins':pins,
               'manifest_sha256':manifest_hash,'manifest_rows':len(rows),
               'manifest_extension_counts':dict(ext),'refusal_exit_code':refusal.returncode,
               'root_outputs_byte_equal':True,'independent_result_replayed':True,
               'comparison_result_replayed':True}
    with dest.open('x') as f:
        json.dump(receipt,f,indent=2,sort_keys=True)
        f.write('\n')
    print(json.dumps({'status':'PASS','coverage':dict(counts),
                      'preserved_files':len(files),'sha256':digest(dest)}))


if __name__ == '__main__':
    main()
