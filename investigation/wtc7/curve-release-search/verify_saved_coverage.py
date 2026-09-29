"""Reconcile complete saved source coverage; does not perform new source scans."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
PINS = {
    'root-01.json': 'b85f806373294697eb1dc15b2673c5d8d34f81890658c0a76937fec9a55f9b06',
    'root-02.json': 'e5eea54090c3215534e6c5f4ae776680b673769353fa12240ba2699368f91a49',
    '../thermal-transfer-crosswalk/run01.json': '4754a59f0628a3ed91e913ce9aa5215254a4e476dcd17d9ee32e964eda2f8117',
}
SEPT = {
    'SRC116': (17314, 1921, '876066eb62e4c849c6bb9fb1598cc0be8b700843483a6ddd3cf6aa9847ad2455'),
    'SRC117': (325983, 45156, 'a823cf4792694cb73ef77a5a29d6e52c1566bfb86b971687eb61fe3f1629be25'),
    'SRC118': (34808082, 870204, 'fa721837357cf7b7fd43e49d2a9d171973663e12399c503163ef56c3464b060d'),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def need(ok, code):
    if not ok:
        raise ValueError(code)


def compare_body(new, old):
    need(new['alias'] == old['alias'], 'alias')
    need(new['name_sha256'] == old['name_sha256'], 'name_hash')
    for key in ('bytes', 'sha256', 'lines', 'nul_bytes'):
        need(new['body'][key] == old['scan'][key], 'body_'+key)


def controls():
    old = {'alias':'X', 'name_sha256':'a',
           'scan':{'bytes':3,'sha256':'b','lines':1,'nul_bytes':0}}
    new = {'alias':'X','name_sha256':'a','body':copy.deepcopy(old['scan'])}
    compare_body(new, old)
    names = ['same']
    for field in ('alias','name_sha256','bytes','sha256','lines','nul_bytes'):
        changed = copy.deepcopy(new)
        target = changed if field in ('alias','name_sha256') else changed['body']
        target[field] = 'changed'
        try:
            compare_body(changed, old)
        except ValueError:
            names.append('reject_'+field)
        else:
            raise ValueError('missed_negative_'+field)
    return names


def check():
    for name, pin in PINS.items():
        need(sha(HERE/name) == pin, 'pin')
    a, b, prior = [json.loads((HERE/name).read_text()) for name in PINS]
    need(a['status'] == b['status'] == prior['status'] == 'PASS', 'status')
    need(a['result'] == b['result'], 'complete_repeat')
    r = a['result']
    oldrows = {x['alias']: x for x in prior['result']['records']}
    need(len(oldrows) == len(prior['result']['records']), 'prior_duplicate')
    june = [x for x in r['records'] if x['kind'] in ('apdl','zip_body')]
    prior_bodies = {x['alias'] for x in oldrows.values() if 'bytes' in x['scan']}
    need({x['alias'] for x in june} == prior_bodies, 'complete_june_alias_set')
    need(len(june) == len(prior_bodies), 'root_duplicate')
    for x in june:
        compare_body(x, oldrows[x['alias']])
    sep = {x['alias']: x for x in r['records'] if x['kind'] == 'gzip_body'}
    need(set(sep) == set(SEPT), 'sept_selection')
    for alias, (size, lines, expected) in SEPT.items():
        x = sep[alias]['body']
        need((x['bytes'],x['lines'],x['sha256']) == (size,lines,expected), 'sept_body_pin')
    bodies = [x for x in r['records'] if 'body' in x]
    need(all(x['body']['eof'] is True for x in bodies), 'eof')
    need(all(x['body']['literal_hits'] == [] for x in bodies), 'zero_markers')
    nul = [x for x in bodies if x['body']['nul_bytes']]
    need(len(nul) == 1 and nul[0]['body']['all_nul'] is True
         and nul[0]['body']['bytes'] == 328, 'nul_scope')
    need(all(x['body']['nonascii_bytes'] == 0 for x in bodies), 'nonascii_scope')
    return {'complete_root_result_repeat':True, 'june_bodies_reconciled':len(june),
            'june_fields_per_body':6, 'september_bodies_reconciled':len(sep),
            'all_bodies_eof':True, 'literal_hits':0,
            'all_nul_bodies':[{'alias':x['alias'],'bytes':x['body']['bytes']} for x in nul],
            'read_bytes':sum(x['body']['bytes'] for x in bodies),
            'physical_lines':sum(x['body']['lines'] for x in bodies),
            'limits':['Prior byte-coverage reconciliation is not independent marker detection.',
                      'All-NUL bytes are covered but are not a semantically interpreted program.',
                      'No solver, general-language evaluation, causal finding or raw export.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    need(re.fullmatch(r'coverage-check[0-9]+\.json',args.output) is not None,'output_scope')
    out = HERE/args.output
    need(not out.exists(),'output_exists')
    tests = controls()
    result = check()
    receipt = {'status':'PASS','code_sha256':sha(Path(__file__)),'pins':PINS,
               'controls':tests,'result':result}
    with out.open('x') as handle:
        json.dump(receipt,handle,indent=2,sort_keys=True);handle.write('\n')
    print(json.dumps({'status':'PASS','controls':len(tests),'result':result}))
