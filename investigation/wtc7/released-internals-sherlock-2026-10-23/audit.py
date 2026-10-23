#!/usr/bin/env python3
"""Read-only static census. Never execute source content or follow its paths."""
import argparse
import collections
import gzip
import hashlib
import json
import re
import struct
import zipfile
from pathlib import Path

FLOOR = re.compile(r'^WTC7-Fl(\d{2})-')
STEP = re.compile(r'^WTC7-(\d+)\.int$')
REFERENCE = re.compile(r"^\s*(!?)\s*/input\s*,\s*['\"]?([^,'\"]+)['\"]?\s*,\s*['\"]?([^,'\"\s]+)", re.I)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def refs(text):
    result = []
    for line_no, line in enumerate(text.splitlines(), 1):
        m = REFERENCE.match(line)
        if m:
            result.append({'line': line_no, 'commented': bool(m[1]),
                           'target': m[2].strip() + '.' + m[3].strip()})
    return result


def thermal_values(text):
    """Literal BF/BFE rows only; no APDL evaluation or inferred solver semantics."""
    for line in text.splitlines():
        fields = [x.strip() for x in line.split('!', 1)[0].split(',')]
        if len(fields) >= 4 and fields[0].upper() == 'BF' and fields[2].upper() == 'TEMP':
            start, kind = 3, 'BF'
        elif len(fields) >= 5 and fields[0].upper() == 'BFE' and fields[2].upper() == 'TEMP':
            start, kind = 4, 'BFE'
        else:
            continue
        try:
            values = [float(v.replace('D', 'E').replace('d', 'e')) for v in fields[start:] if v]
        except ValueError as exc:
            raise ValueError('Nonliteral temperature field; do not silently skip') from exc
        yield kind, values


def reachable(roots, edges):
    seen, missing = set(), set()
    queue = list(roots)
    while queue:
        name = queue.pop()
        if name in seen:
            continue
        seen.add(name)
        if name not in edges:
            missing.add(name)
            continue
        queue.extend(r['target'] for r in edges[name] if not r['commented'])
    return seen - missing, missing


def thermal_node_row(s):
    # Released source uses comma-delimited free format, with optional spaces.
    f = re.split(r'[,\s]+', s.strip())
    if len(f) != 4:
        raise ValueError('Unsupported thermal node record')
    # Keyword field order is NID, TS, TB, LCID. Return named consumer order.
    return int(f[0]), float(f[2]), float(f[1]), int(f[3])


def main(root):
    june = root / 'exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539'
    sept = root / 'exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653'
    archive = june / 'ANSYS Thermal Data.zip'
    before = file_sha(archive)
    result = {'scope': 'static input census; no solver; PNG pixels not interpreted',
              'archive': {'path': str(archive), 'sha256': before}, 'cases': {},
              'floor_prefixes': {}, 'nul_members': [], 'png_dimensions': {},
              'step_driver_records': [], 'apdl': [], 'gzip_sources': []}
    by_case, by_hash = collections.defaultdict(dict), collections.Counter()
    graphs, root_names = collections.defaultdict(dict), collections.defaultdict(list)
    png_dims = collections.Counter()
    with zipfile.ZipFile(archive) as z:
        result['archive']['directory_entries'] = sum(x.is_dir() for x in z.infolist())
        for info in z.infolist():
            if info.is_dir():
                continue
            data = z.read(info)  # ZIP reader validates CRC; no source path extraction.
            name = Path(info.filename).name
            cm = re.search(r'Case([ABC])_Temps/', info.filename)
            if not cm:
                raise ValueError('Unexpected case path: ' + info.filename)
            case = cm[1]
            h = sha(data)
            by_hash[h] += 1
            by_case[case][name] = h
            c = result['cases'].setdefault(case, {'files': 0, 'bytes': 0, 'types': {}})
            c['files'] += 1
            c['bytes'] += len(data)
            ext = Path(name).suffix or '(none)'
            c['types'][ext] = c['types'].get(ext, 0) + 1
            if ext == '.png':
                if not data.startswith(b'\x89PNG\r\n\x1a\n'):
                    raise ValueError('Bad PNG signature')
                png_dims['x'.join(map(str, struct.unpack('>II', data[16:24])))] += 1
                continue
            fm = FLOOR.match(name)
            key = case + '/Fl' + fm[1] if fm else None
            if key:
                f = result['floor_prefixes'].setdefault(key, {'files': 0, 'bytes': 0,
                    'BF_rows': 0, 'BFE_rows': 0, 'scalar_fields': 0,
                    'min': None, 'max': None, 'exact_25_fields': 0})
                f['files'] += 1
                f['bytes'] += len(data)
            if b'\0' in data:
                result['nul_members'].append({'path': info.filename, 'bytes': len(data),
                    'all_nul': not data.strip(b'\0'), 'sha256': h})
                # Retain an empty graph entry: file exists but cannot be parsed as APDL.
                graphs[case][name] = []
                continue
            text = data.decode('latin1')
            graphs[case][name] = refs(text)
            sm = STEP.match(name)
            if sm:
                root_names[case].append(name)
                result['step_driver_records'].append({'case': case, 'step': int(sm[1]),
                    'path': info.filename, 'sha256': h, 'references': refs(text)})
            if key:
                for kind, values in thermal_values(text):
                    f[kind + '_rows'] += 1
                    f['scalar_fields'] += len(values)
                    f['exact_25_fields'] += values.count(25.0)
                    if values:
                        lo, hi = min(values), max(values)
                        f['min'] = lo if f['min'] is None else min(f['min'], lo)
                        f['max'] = hi if f['max'] is None else max(f['max'], hi)
    for case, graph in graphs.items():
        seen, missing = reachable(root_names[case], graph)
        result['cases'][case]['static_reachable_files'] = len(seen)
        result['cases'][case]['static_missing_names'] = sorted(missing)
        result['cases'][case]['unreachable_non_png_files'] = sorted(set(graph) - seen)
        result['cases'][case]['unique_byte_hashes'] = len(set(by_case[case].values()))
    pairs = {}
    for a, b in [('A', 'B'), ('A', 'C'), ('B', 'C')]:
        names = set(by_case[a]) & set(by_case[b])
        same = [n for n in names if by_case[a][n] == by_case[b][n]]
        pairs[a + b] = {'shared_basenames': len(names), 'identical_bytes': len(same),
                        'different_bytes': len(names) - len(same),
                        'identical_by_floor_prefix': dict(collections.Counter(
                            FLOOR.match(n)[1] if FLOOR.match(n) else '(none)' for n in same))}
    result['same_basename_comparison'] = pairs
    result['archive']['regular_files'] = sum(c['files'] for c in result['cases'].values())
    result['archive']['unique_body_hashes'] = len(by_hash)
    result['archive']['duplicate_copies_beyond_one_per_hash'] = sum(by_hash.values()) - len(by_hash)
    result['archive']['hash_multiplicity'] = dict(sorted(collections.Counter(by_hash.values()).items()))
    result['archive']['sha256_after'] = file_sha(archive)
    assert before == result['archive']['sha256_after']
    result['png_dimensions'] = dict(png_dims)
    for p in sorted(june.glob('*.apdl')):
        data = p.read_bytes()
        text = data.decode('latin1')
        result['apdl'].append({'basename': p.name, 'bytes': len(data), 'sha256': sha(data),
            'references': refs(text),
            'literal_TIME_lines': [{'line': i, 'text': s.strip()} for i, s in enumerate(text.splitlines(), 1)
                                   if re.match(r'^\s*TIME\s*,', s, re.I)],
            'thermal_step_driver_mentions': len(re.findall(r'WTC7-\d+\.int', text, re.I))})
    for p in sorted(sept.glob('*.gz')):
        pin = file_sha(p)
        h = hashlib.sha256()
        total = lines = 0
        thermal = p.name == 'WTC7_CaseB_400pm.int.gz'
        node_rows, intervals, curve_ids, base_values = collections.Counter(), {}, set(), set()
        state = ''
        with gzip.open(p, 'rb') as stream:
            for line in stream:
                total += len(line)
                lines += 1
                h.update(line)
                if total > 512 * 1024 * 1024:
                    raise ValueError('Declared stream cap exceeded')
                if not thermal:
                    continue
                s = line.decode('ascii').strip()
                if not s or s.startswith('$'):
                    continue
                if s.startswith('*'):
                    state = s.upper()
                    continue
                if state == '*LOAD_THERMAL_VARIABLE_NODE':
                    node, base, coeff, curve = thermal_node_row(s)
                    node_rows[node] += 1
                    curve_ids.add(curve)
                    base_values.add(base)
                    if node not in intervals:
                        intervals[node] = (coeff, coeff)
                    else:
                        lo, hi = intervals[node]
                        intervals[node] = (min(lo, coeff), max(hi, coeff))
        item = {'basename': p.name, 'compressed_sha256': pin, 'decompressed_sha256': h.hexdigest(),
                'decompressed_bytes': total, 'physical_lines': lines, 'read_to_eof': True,
                'compressed_sha256_after': file_sha(p)}
        assert pin == item['compressed_sha256_after']
        if thermal:
            item['thermal'] = {'rows': sum(node_rows.values()), 'unique_ids': len(node_rows),
                'repeated_ids': sum(v > 1 for v in node_rows.values()),
                'unequal_coefficient_ids': sum(lo != hi for lo, hi in intervals.values()),
                'LCID_values': sorted(curve_ids), 'TB_values': sorted(base_values),
                'row_multiplicity': dict(sorted(collections.Counter(node_rows.values()).items()))}
        result['gzip_sources'].append(item)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(main(args.root), indent=2, sort_keys=True))
