#!/usr/bin/env python3
"""Post-result direct-source locator checks; not blinded replication."""
import csv
import hashlib
import json
import zipfile
from pathlib import Path

here = Path(__file__).resolve().parent
base = json.loads((here / 'observations.json').read_text())
old = json.loads((here / 'bf-overlap.json').read_text())
new = json.loads((here / 'bf-overlap-with-ranges.json').read_text())
assert old['totals'] == new['totals']
assert old['motivating_example'] == new['motivating_example']
assert len(new['floor_steps']) == 288
for c in 'ABC':
    rows = [v for v in new['floor_steps'] if v['case'] == c]
    assert len(rows) == 96
    assert {(v['floor_prefix'], v['step_suffix']) for v in rows} == {(f, s) for f in range(7, 15) for s in range(1, 13)}
    assert sum(v['BF_rows'] for v in rows) == sum(v['BF_rows'] for k, v in base['floor_prefixes'].items() if k.startswith(c + '/'))
    for a, b in zip(old['floor_steps'], new['floor_steps']):
        assert all(a[k] == b[k] for k in a)

records = []
with zipfile.ZipFile(base['archive']['path']) as z:
    for case in 'ABC':
        rows = [v for v in new['floor_steps'] if v['case'] == case and v['top_driver_branch_active'] and v['largest_unequal_range']]
        chosen = max(rows, key=lambda x: x['largest_unequal_range']['range'])
        driver = f"WTC7-Fl{chosen['floor_prefix']:02}-{chosen['step_suffix']}.int"
        path = next(n for n in z.namelist() if f'Case{case}_Temps/' in n and Path(n).name == driver)
        text = z.read(path).decode('ascii')
        locators = []
        last = -1
        for r in chosen['largest_unequal_range']['rows_in_literal_include_order']:
            name = r['file']
            target = str(Path(path).parent / name)
            data = z.read(target)
            line = data.decode('ascii').splitlines()[r['physical_line'] - 1]
            f = next(csv.reader([line]))
            assert f[0] == 'BF' and f[2] == 'TEMP'
            assert int(f[1]) == chosen['largest_unequal_range']['node_id'] and float(f[3]) == r['value']
            pos = text.index(name.removesuffix('.int'))
            assert pos > last
            last = pos
            locators.append({'archive_path': target, 'body_sha256': hashlib.sha256(data).hexdigest(),
                             'physical_line': r['physical_line'], 'original_line': line})
        records.append({'case': case, 'driver': path, 'driver_sha256': hashlib.sha256(z.read(path)).hexdigest(),
                        'selected_as': 'largest within-driver range among active top-level branches; exploratory descriptive extreme',
                        'node_id': chosen['largest_unequal_range']['node_id'], 'source_rows': locators})
print(json.dumps({'status': 'pass', 'checks': ['all 288 case/floor/step cells present',
    'all previous overlap summary fields unchanged by range extension', 'BF row totals match full census',
    'three case maxima directly checked at raw physical lines', 'order matches original floor-driver text'],
    'limitations': 'post-result checker; not solver execution or complete independent regeneration of all overlap groups',
    'peak_examples': records}, indent=2, sort_keys=True))
