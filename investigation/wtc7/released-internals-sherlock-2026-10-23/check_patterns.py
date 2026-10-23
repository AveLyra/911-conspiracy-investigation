#!/usr/bin/env python3
"""Post-schema check; separate CSV reader, not an independent discovery."""
import collections
import csv
import gzip
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path('/Users/admin/docs/911')
HERE = Path(__file__).resolve().parent
j = json.loads((HERE / 'observations.json').read_text())
zpath = Path(j['archive']['path'])
with zipfile.ZipFile(zpath) as z:
    grouped = collections.defaultdict(list)
    for info in z.infolist():
        if not info.is_dir():
            grouped[hashlib.sha256(z.read(info)).hexdigest()].append(info.filename)
    groups36 = [names for names in grouped.values() if len(names) == 36]
    ambient_groups = 0
    floors = collections.Counter()
    for names in groups36:
        rows = list(csv.reader(z.read(names[0]).decode('ascii').splitlines()))
        assert rows and all(len(r) == 4 and r[0] == 'BF' and r[2] == 'TEMP' and float(r[3]) == 25.0 for r in rows)
        ambient_groups += 1
        for n in names:
            floors[re.search(r'Fl(\d{2})', n)[1]] += 1
    corrupt = j['nul_members'][0]
    assert z.read(corrupt['path']) == b'\0' * 328
    # Verify all 36 step drivers independently with literal line counting.
    driver_checks = []
    for case in 'ABC':
        names = [n for n in z.namelist() if f'Case{case}_Temps/' in n and re.fullmatch(r'WTC7-\d+\.int', Path(n).name)]
        assert len(names) == 12
        active, commented = collections.Counter(), collections.Counter()
        for n in names:
            for s in z.read(n).decode('ascii').splitlines():
                m = re.search(r'WTC7-Fl(\d{2})-', s)
                if m:
                    (commented if s.lstrip().startswith('!') else active)[m[1]] += 1
        driver_checks.append({'case': case, 'active_floor_reference_counts': dict(sorted(active.items())),
                              'commented_floor_reference_counts': dict(sorted(commented.items()))})

p = ROOT / 'exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653/WTC7_CaseB_400pm.int.gz'
values = collections.defaultdict(set)
counts = collections.Counter()
with gzip.open(p, 'rt', encoding='ascii', newline='') as f:
    for fields in csv.reader(f):
        if len(fields) != 4:
            continue
        nid = int(fields[0])
        counts[nid] += 1
        values[nid].add(float(fields[1]))  # NID, TS, TB, LCID
        assert float(fields[2]) == 0.0 and int(fields[3]) == 2
thermal = {'rows': sum(counts.values()), 'unique_ids': len(counts),
           'repeated_ids': sum(c > 1 for c in counts.values()),
           'unequal_coefficient_ids': sum(len(v) > 1 for v in values.values())}
expected = next(g['thermal'] for g in j['gzip_sources'] if 'thermal' in g)
assert all(expected[k] == v for k, v in thermal.items())
assert len(grouped) == j['archive']['unique_body_hashes']
result = {'status': 'pass', 'scope': 'post-schema alternate readers; not blinded or independent historical evidence',
          'thermal_csv_crosscheck': thermal, 'groups_with_36_identical_copies': len(groups36),
          'groups36_all_literal_BF_TEMP_25': ambient_groups, 'groups36_file_count_by_floor_prefix': dict(floors),
          'step_drivers': driver_checks, 'nul_body_verified_exactly': True,
          'retained_source_sha256': hashlib.sha256(zpath.read_bytes()).hexdigest()}
print(json.dumps(result, indent=2, sort_keys=True))
