"""Validate and compare two frozen manual pixel annotations, not curve models."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import tempfile

HERE = Path(__file__).resolve().parent
SOURCE_SHA = '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd'
PROTOCOL_SHA = '407c8f18f4202047aa01e573ceee2f5c1350ece9f9fb7961a3042881ea5e1fea'
TARGETS = [('solid', x) for x in range(300, 306)] + [('dash', x) for x in range(300, 308)]


def pin(path):
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def validate(record):
    if record.get('source_sha256') != SOURCE_SHA or record.get('protocol_sha256') != PROTOCOL_SHA:
        raise ValueError('Source/protocol pin mismatch')
    if not isinstance(record.get('reader'), str) or not record['reader'].strip():
        raise ValueError('Reader attribution required')
    rows = record.get('observations')
    if not isinstance(rows, list) or len(rows) != 14:
        raise ValueError('Exact fragment-column coverage required')
    keys = []
    for row in rows:
        if row.get('fragment') not in ('solid', 'dash') or type(row.get('column')) is not int:
            raise ValueError('Fragment/integer column required')
        keys.append((row['fragment'], row['column']))
        low, high = (32, 48) if row['fragment'] == 'solid' else (4, 14)
        for field in ('core_rows', 'fringe_rows'):
            values = row.get(field)
            if (not isinstance(values, list) or any(type(v) is not int or not low <= v <= high for v in values)
                    or values != sorted(set(values))):
                raise ValueError('Rows must be sorted unique in-target integer cells')
        if set(row['core_rows']) & set(row['fringe_rows']):
            raise ValueError('Core and fringe overlap')
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in ('status', 'note')):
            raise ValueError('Explicit status and explanation required')
    if keys != TARGETS:
        raise ValueError('Duplicate/missing/reordered fragment-column entries')
    return rows


def compare(left, right):
    output = []
    for a, b in zip(validate(left), validate(right)):
        ca, cb = set(a['core_rows']), set(b['core_rows'])
        fa, fb = set(a['fringe_rows']), set(b['fringe_rows'])
        oa, ob = ca | fa, cb | fb
        result = {'fragment': a['fragment'], 'column': a['column'],
                  'root': a, 'independent': b, 'core_equal': ca == cb,
                  'fringe_equal': fa == fb, 'outer_equal': oa == ob,
                  'partition_equal': ca == cb and fa == fb,
                  'status_text_equal': a['status'] == b['status']}
        for name, x, y in [('core', ca, cb), ('fringe', fa, fb), ('outer', oa, ob)]:
            result[name] = {'intersection': sorted(x & y), 'union': sorted(x | y),
                            'symmetric_difference': sorted(x ^ y),
                            'root_only': sorted(x - y), 'independent_only': sorted(y - x)}
        output.append(result)
    return output


def controls():
    fixture = {'source_sha256': SOURCE_SHA, 'protocol_sha256': PROTOCOL_SHA, 'reader': 'synthetic',
        'observations': [{'fragment': f, 'column': x, 'core_rows': [], 'fringe_rows': [],
                          'status': 'synthetic', 'note': 'No historical data.'} for f, x in TARGETS]}
    checks = {}
    checks['shared_column_distinct_fragments'] = len(validate(fixture)) == 14
    checks['empty_sets_retained'] = all(r['partition_equal'] for r in compare(fixture, fixture))
    def reject(name, change):
        item = copy.deepcopy(fixture)
        change(item)
        try:
            validate(item)
        except ValueError:
            checks[name] = True
        else:
            checks[name] = False
    for name, field, value in [('duplicate_rows', 'core_rows', [33,33]), ('unsorted_rows','core_rows',[34,33]),
                               ('boolean_row','core_rows',[True]),('fractional_row','core_rows',[33.5]),
                               ('out_of_bounds','core_rows',[31]),('boolean_column','column',True)]:
        reject(name, lambda r, f=field, v=value: r['observations'][0].__setitem__(f, v))
    reject('same_fragment_duplicate_column', lambda r: r['observations'][1].__setitem__('column',300))
    reject('missing_entry', lambda r: r['observations'].pop())
    reject('changed_source', lambda r: r.__setitem__('source_sha256','0'*64))
    reject('changed_protocol', lambda r: r.__setitem__('protocol_sha256','0'*64))
    reject('core_fringe_overlap', lambda r: r['observations'][0].update(core_rows=[33],fringe_rows=[33]))
    a, b = copy.deepcopy(fixture), copy.deepcopy(fixture)
    a['observations'][0].update(core_rows=[33],fringe_rows=[35])
    b['observations'][0].update(core_rows=[35],fringe_rows=[33])
    one = compare(a,b)[0]
    checks['equal_outer_unequal_partition'] = one['outer_equal'] and not one['partition_equal']
    checks['holes_not_filled'] = one['outer']['union'] == [33,35]
    b['observations'][0].update(core_rows=[37],fringe_rows=[39])
    one = compare(a,b)[0]
    checks['disjoint_sets'] = one['outer']['intersection'] == [] and one['outer']['union'] == [33,35,37,39]
    with tempfile.TemporaryDirectory(prefix='f3-footprint-control-') as directory:
        path = Path(directory) / 'test.json'
        save(path, {'synthetic': True})
        before = pin(path)
        try:
            save(path, {'replacement': True})
        except FileExistsError:
            checks['overwrite_refused'] = pin(path) == before
        else:
            checks['overwrite_refused'] = False
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['controls','run01','run02'])
    args = parser.parse_args()
    destination = HERE / (args.mode + '.json')
    if destination.exists():
        raise FileExistsError('Existing output preserved')
    state = {'script': pin(Path(__file__)), 'protocol': pin(HERE / 'PROTOCOL.md'),
             'python': platform.python_version()}
    if state['protocol']['sha256'] != PROTOCOL_SHA:
        raise ValueError('Protocol changed')
    if args.mode == 'controls':
        checks = controls()
        save(destination, {'status':'complete','state':state,'checks':checks})
        print(json.dumps({'controls':len(checks),'pass':True}))
        return
    gate = read(HERE / 'controls.json')
    if gate['state'] != state or gate['status'] != 'complete' or not all(gate['checks'].values()) or len(gate['checks']) != 17:
        raise ValueError('Missing/stale/incomplete synthetic controls')
    paths = [HERE/'reader-root.json', HERE/'reader-independent.json', HERE/'raw-context.json',
             HERE/'method-review.json', HERE/'read_context.py', HERE.parent/'native-strips01/Im4.jpg']
    before = {str(p):pin(p) for p in paths}
    if before[str(paths[-1])]['sha256'] != SOURCE_SHA:
        raise ValueError('Native source mismatch')
    review = read(HERE/'method-review.json')
    if review['decision'] != 'proceed_with_boundaries' or review['protocol_sha256'] != PROTOCOL_SHA:
        raise ValueError('Review gate mismatch')
    left, right = read(paths[0]), read(paths[1])
    raw = read(paths[2])
    if left['raw_context_sha256'] != pin(paths[2])['sha256']:
        raise ValueError('Root context pin mismatch')
    cells = raw['cells']
    if [(r['x'],r['y']) for r in cells] != [(x,y) for y in range(55) for x in range(298,310)]:
        raise ValueError('Context membership')
    if raw['source_pin']['sha256'] != SOURCE_SHA or raw['protocol_pin']['sha256'] != PROTOCOL_SHA:
        raise ValueError('Context lineage')
    rgbbytes = bytes(v for r in cells for v in r['rgb'])
    if hashlib.sha256(rgbbytes).hexdigest() != right['raw_context']['row_major_rgb_sha256']:
        raise ValueError('Independent context differs')
    rows = compare(left,right)
    after = {str(p):pin(p) for p in paths}
    if before != after:
        raise ValueError('Input changed')
    result = {'status':'complete','state':state,'inputs':before,'inputs_after':after,
              'controls_pin':pin(HERE/'controls.json'),'rows':rows,
              'summary':{k:sum(not r[k] for r in rows) for k in ('core_equal','fringe_equal','outer_equal','partition_equal')},
              'limits':'Counts are disagreeing fragment-column entries, not error rates or accepted curve support. No centerline or physical quantity.',
              'human_accepted':False}
    save(destination,result)
    print(json.dumps({'status':'complete','entries':len(rows),'disagreement_counts':result['summary']}))


if __name__ == '__main__':
    main()
