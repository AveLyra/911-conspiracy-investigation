"""Final saved-artifact/document checks, not a new historical source scan."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    pins = re.findall(r'^\| ([\w.-]+) \| ([a-f0-9]{64}) \|$',
                      (HERE/'validation.md').read_text(), re.M)
    assert len(pins) == 14 and len(dict(pins)) == len(pins)
    for name, expected in pins:
        assert sha(HERE/name) == expected, name
    python_files = sorted(HERE.glob('*.py'))
    json_files = sorted(HERE.glob('*.json'))
    for path in python_files:
        ast.parse(path.read_text(), filename=path.name)
    for path in json_files:
        json.loads(path.read_text())
    a, b = [json.loads((HERE/name).read_text()) for name in ('root-01.json','root-02.json')]
    assert a['status'] == b['status'] == 'PASS' and a['result'] == b['result']
    assert a['result']['body_count'] == 25368 and a['result']['literal_hit_count'] == 0
    coverage = json.loads((HERE/'coverage-check01.json').read_text())
    assert coverage['status'] == 'PASS' and coverage['result']['june_bodies_reconciled'] == 25365
    independent = json.loads((HERE/'independent-scan01.json').read_text())
    assert independent['status'] == 'PASS'
    assert len(independent['bodies']) == 25368 and len(independent['excluded']) == 277
    assert independent['result']['bytes_scanned'] == 513121900
    assert independent['result']['physical_lines'] == 8648698
    comparisons = [json.loads((HERE/name).read_text()) for name in
                   ('independent-comparison01.json','independent-comparison-root01.json')]
    left, right = comparisons
    assert left['result'] == right['result'] and left['controls'] == right['controls']
    assert left['pins_before'] == left['pins_after'] == right['pins_before'] == right['pins_after']
    for receipt in comparisons:
        assert receipt['status'] == 'PASS' and receipt['result']['passed'] is True
        assert receipt['code_sha256'] == sha(HERE/'independent_compare.py')
        controls = receipt['controls']
        assert controls['passed'] is True and controls['create_only_refused'] is True
        assert controls['cross_reader_fixture_count'] == len(controls['cross_reader_fixtures']) == 17
        assert controls['negative_count'] == len(controls['negative_variants']) == 29
        assert all(r['comparison']['equal'] is True for r in controls['cross_reader_fixtures'])
        assert all(r['comparison']['equal'] is False for r in controls['negative_variants'])
        result = receipt['result']
        assert result['counts'] == {'all_records':25645,'scanned_bodies':25368,'excluded':277,
            'record_leaves_compared':407801,'record_mismatches':0,
            'bytes_scanned':513121900,'physical_lines':8648698}
        assert len(result['per_record']) == 25645
        assert all(r['comparison']['equal'] is True and r['comparison']['mismatch_count'] == 0
                   for r in result['per_record'])
        assert len(result['summary_comparisons']) == 10
        assert all(r['equal'] is True for r in result['summary_comparisons'].values())
        assert all(r['equal'] is True for r in result['root_repeat_metadata'].values())
        assert result['full_root_result_repeat']['equal'] is True
        assert result['full_root_result_repeat']['leaves'] == 407824
    failed = json.loads((HERE/'independent-controls-failed01.json').read_text())
    assert failed['status'] == 'FAIL' and failed['bodies'] == [] and failed['excluded'] == []
    links = 0
    for name in ('report.md','validation.md'):
        content = (HERE/name).read_text()
        assert not any(line != line.rstrip() for line in content.splitlines()), name
        assert 'pending' not in content.lower(), 'unresolved_document_status'
        for path in re.findall(r'\]\(([^)]+)\)',content):
            if '://' in path or path.startswith('#'):
                continue
            assert (HERE/path.split('#',1)[0]).exists(), path
            links += 1
    return {'documented_pins':len(pins),'python_asts':len(python_files),
            'json_files':len(json_files),'report_validation_local_links':links,
            'complete_root_result_repeat':True,'retained_pre_source_failure':True,
            'independent_comparison_replayed':True,
            'document_sha256':{n:sha(HERE/n) for n in ('report.md','validation.md')},
            'limits':['Checks saved artifacts and final document status, not raw source or solver behavior.',
                      'Scientific comparison scope is established by the separate full adapter receipts.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    assert re.fullmatch(r'artifact-check[0-9]+\.json',args.output)
    out = HERE/args.output
    assert not out.exists()
    result = check()
    with out.open('x') as handle:
        json.dump({'status':'PASS','code_sha256':sha(Path(__file__)),'result':result},
                  handle,indent=2,sort_keys=True)
        handle.write('\n')
    print(json.dumps({'status':'PASS','counts':{k:v for k,v in result.items() if isinstance(v,int)}}))
