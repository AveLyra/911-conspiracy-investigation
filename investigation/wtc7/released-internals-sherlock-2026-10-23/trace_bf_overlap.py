#!/usr/bin/env python3
"""Literal active floor-driver BF order only; no source execution."""
import collections
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path
from audit import refs

root = Path('/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539')
archive = root / 'ANSYS Thermal Data.zip'
pin = hashlib.sha256(archive.read_bytes()).hexdigest()
result = {'archive_sha256': pin, 'scope': 'exploratory literal BF overlaps; not effective solver temperatures',
          'floor_steps': [], 'examples': []}
with zipfile.ZipFile(archive) as z:
    directories = collections.defaultdict(dict)
    for info in z.infolist():
        if info.is_dir() or not info.filename.endswith('.int'):
            continue
        m = re.search(r'Case([ABC])_Temps/', info.filename)
        directories[m[1]][Path(info.filename).name] = info.filename
    for case, members in sorted(directories.items()):
        for floor in range(7, 15):
            for step in range(1, 13):
                driver = f'WTC7-Fl{floor:02}-{step}.int'
                calls = refs(z.read(members[driver]).decode('ascii'))
                rows = collections.defaultdict(list)
                nul = []
                for call in calls:
                    if call['commented']:
                        continue
                    name = call['target']
                    data = z.read(members[name])
                    if b'\0' in data:
                        nul.append(name)
                        continue
                    for n, fields in enumerate(csv.reader(data.decode('ascii').splitlines()), 1):
                        if len(fields) == 4 and fields[0] == 'BF' and fields[2] == 'TEMP':
                            rows[int(fields[1])].append((float(fields[3]), name, n))
                repeated = {nid: v for nid, v in rows.items() if len(v) > 1}
                unequal = {nid: v for nid, v in repeated.items() if len({r[0] for r in v}) > 1}
                slno = {nid: v for nid, v in unequal.items() if any('-SLNo-' in r[1] for r in v)}
                largest = max(unequal, key=lambda nid: max(r[0] for r in unequal[nid]) - min(r[0] for r in unequal[nid])) if unequal else None
                result['floor_steps'].append({'case': case, 'floor_prefix': floor, 'step_suffix': step,
                    'top_driver_branch_active': not (case in 'AB' and floor == 7),
                    'BF_rows': sum(map(len, rows.values())), 'unique_BF_ids': len(rows),
                    'repeated_BF_ids': len(repeated), 'unequal_BF_ids': len(unequal),
                    'unequal_with_SLNo': len(slno), 'nul_inputs': nul,
                    'largest_unequal_range': None if largest is None else {
                        'node_id': largest, 'range': max(r[0] for r in unequal[largest]) - min(r[0] for r in unequal[largest]),
                        'rows_in_literal_include_order': [{'value': v, 'file': name, 'physical_line': n} for v, name, n in unequal[largest]]}})
                # Reproducible fixed locator selection, not largest differences.
                for nid in sorted(unequal)[:1]:
                    if step == 1:
                        result['examples'].append({'case': case, 'floor_prefix': floor, 'step_suffix': step,
                            'node_id': nid, 'literal_floor_driver_order': [
                                {'value': v, 'file': name, 'physical_line': n} for v, name, n in unequal[nid]]})
                if case == 'B' and floor == 8 and step == 1:
                    result['motivating_example'] = {'node_id': 170516, 'literal_floor_driver_order': [
                        {'value': v, 'file': name, 'physical_line': n} for v, name, n in rows[170516]]}
result['totals'] = {}
for case in 'ABC':
    selected = [v for v in result['floor_steps'] if v['case'] == case]
    result['totals'][case] = {k: sum(v[k] for v in selected) for k in
                            ['BF_rows', 'unique_BF_ids', 'repeated_BF_ids', 'unequal_BF_ids', 'unequal_with_SLNo']}
    result['totals'][case]['floor_steps_with_unequal_BF'] = sum(v['unequal_BF_ids'] > 0 for v in selected)
    result['totals'][case]['counting_unit'] = 'sum of per-floor/per-step IDs; not unique building nodes'
assert pin == hashlib.sha256(archive.read_bytes()).hexdigest()
print(json.dumps(result, indent=2, sort_keys=True))
