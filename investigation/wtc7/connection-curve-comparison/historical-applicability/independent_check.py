"""Read-only independent annotation-geometry verification; exclusive report write."""
import hashlib
import json
from pathlib import Path
import platform
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def rowcheck(v):
    require(isinstance(v, list), 'rows not list')
    require(all(type(x) is int and 0 <= x < 88 for x in v), 'row type/bounds')
    require(all(a < b for a, b in zip(v, v[1:])), 'row order/duplicates')

def independently_check(e):
    c, f = e['core_rows'], e['fringe_rows']
    rowcheck(c); rowcheck(f)
    require(not any(y in f for y in c), 'class overlap')
    u = sorted(c + f)
    flags = []
    for y, flag in ((0, 'strip_top'), (87, 'strip_bottom')):
        if y in u: flags.append(flag)
    if u and e['column'] == 270: flags.append('target_left')
    if u and e['column'] == 359: flags.append('target_right')
    require(e['boundary_flags'] == flags, 'incorrect boundary flags')
    require(e['status'] in ('identified_local_fragment', 'fringe_only', 'no_attributable_cells', 'identity_conflict', 'boundary_truncated'), 'status')
    require(isinstance(e['note'], str) and e['note'].strip(), 'note')
    fid = e.get('fragment_id')
    named = isinstance(fid, str) and bool(fid.strip())
    m = e.get('fragment_membership')
    if m is not None:
        require(isinstance(m, dict), 'membership type')
        for k, v in m.items():
            require(isinstance(k, str) and k.strip(), 'member name')
            rowcheck(v['core_rows']); rowcheck(v['fringe_rows'])
            require(not set(v['core_rows']).intersection(v['fringe_rows']), 'member class overlap')
        require(set(c) == {y for v in m.values() for y in v['core_rows']}, 'core union')
        require(set(f) == {y for v in m.values() for y in v['fringe_rows']}, 'fringe union')
    elif u:
        require(isinstance(fid, str) and bool(fid), 'missing attribution')
    failed = []
    checks = [('nonidentified_status', e['status'] == 'identified_local_fragment'),
              ('empty_core', bool(c)), ('empty_outer', bool(u)),
              ('disconnected_outer', not u or all(b-a == 1 for a,b in zip(u,u[1:]))),
              ('boundary', not flags), ('missing_identifier', named)]
    failed.extend(name for name, good in checks if not good)
    if m is not None:
        if len(m) >= 2:
            failed.append('multiple_fragment_members')
        elif len(m) == 1:
            k = next(iter(m))
            if not (named and k == fid and m[k]['core_rows'] == c and m[k]['fringe_rows'] == f):
                failed.append('inconsistent_single_fragment_identity')
        elif u or named:
            failed.append('inconsistent_single_fragment_identity')
    rectangle = None if failed else [e['column'], min(u), e['column']+1, max(u)+1]
    return {'source_record': e, 'eligible': not failed, 'reasons': failed, 'native_cell_rectangle': rectangle}

def main():
    target = HERE / 'independent-check.json'
    require(not target.exists(), 'existing report refused')
    runs = [HERE/'run01.json', HERE/'run02.json']
    a, b = [json.loads(p.read_text()) for p in runs]
    require(runs[0].read_bytes() == runs[1].read_bytes(), 'run bytes differ')
    paths = runs + [HERE/'independent_check.py', BASE/'NUMERICAL-PROTOCOL.md', BASE/'HUMAN-REVIEW-GATE.md']
    paths += [BASE/p for p in a['inputs']]
    before = {str(p): pin(p) for p in paths}
    require(a['inputs'] == a['inputs_after'] == b['inputs'] == b['inputs_after'], 'recorded pins differ')
    for name, value in a['inputs'].items(): require(pin(BASE/name) == value, 'input pin '+name)
    totals = {}
    for reader in ('root', 'independent'):
        original = json.loads((BASE/'f3-descending-corridor'/('reader-'+reader+'.json')).read_text())
        require(original['source_sha256'] == '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd', 'source declaration')
        require(original['protocol_sha256'] == '12525bcb149368f18d85e3611f32137ccdeef723cc95df93cf2b5d9b13f2aa27', 'old protocol declaration')
        obs = original['observations']
        require([(e['route'],e['column']) for e in obs] == [(r,x) for r in ('solid','dash') for x in range(270,360)], 'coverage')
        require(all(type(e['column']) is int for e in obs), 'column type')
        derived = [independently_check(e) for e in obs]
        require(derived == a['readers'][reader]['rows'], 'literal rows/classifications differ')
        require(original['reader'] == a['readers'][reader]['reader'], 'reader attribution')
        summaries = {}
        for route in ('all','solid','dash'):
            selected = [v for v in derived if route == 'all' or v['source_record']['route'] == route]
            counts = {}
            for v in selected:
                for reason in v['reasons']: counts[reason] = counts.get(reason,0)+1
            yes = len([v for v in selected if v['eligible']])
            summaries[route] = {'entries':len(selected),'eligible':yes,'excluded':len(selected)-yes,'reason_counts_nonexclusive':counts}
        require(summaries == a['readers'][reader]['summary'], 'summary differs')
        totals[reader] = summaries
    require(before == {str(p):pin(p) for p in paths}, 'input modified')
    out = {'status':'passed_independent_geometry_check','records_checked':360,'literal_records_preserved':True,'all_classifications_reasons_rectangles_exact':True,'repeat_bytes_equal':True,'summaries':totals,'inspected_input_pins':before,'checker_self_pin':pin(Path(__file__)),'runtime':platform.python_version(),'executable':sys.executable,'command':str(sys.executable)+' -B independent_check.py','producer_or_validator_imported':False,'limits':'Prior-informed independent arithmetic implementation, not new source evidence. No historical pixels read, containment validation, physical support or human acceptance.'}
    with target.open('x') as stream:
        json.dump(out,stream,indent=2,sort_keys=True); stream.write('\n')
    print(json.dumps({'status':out['status'],'records':360,'report':pin(target)}))

if __name__ == '__main__': main()
