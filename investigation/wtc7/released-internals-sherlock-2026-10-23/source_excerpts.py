#!/usr/bin/env python3
"""Publish only declared, nonsensitive engineering excerpts, never execute inputs."""
import argparse
import gzip
import hashlib
import json
import re
import zipfile
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def extract(root, here):
    june = root / 'exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539'
    sept = root / 'exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653'
    prior = json.loads((here / 'observations.json').read_text())
    result = {'scope': 'Selected engineering-source excerpts, not a new release of full original files',
              'line_convention': '1-based physical lines in decompressed text; ZIP member paths are exact',
              'full_input_public_download_url': None,
              'provenance_limit': 'Originals are held agency-production files; official full-input download URLs were not established. Hashes pin examined bytes, not historical execution.',
              'originals': [], 'excerpts': []}

    def record(label, source, rows, **metadata):
        result['excerpts'].append({'label': label, 'source': source,
                                  **metadata, 'lines': [{'physical_line': n, 'original_text': s} for n, s in rows]})

    zpath = june / 'ANSYS Thermal Data.zip'
    pin = digest(zpath.read_bytes())
    assert pin == prior['archive']['sha256']
    result['originals'].append({'source': zpath.name, 'stored_sha256': pin})
    with zipfile.ZipFile(zpath) as z:
        for case in 'ABC':
            members = {Path(n).name: n for n in z.namelist() if f'Case{case}_Temps/' in n and not n.endswith('/')}
            for step in range(1, 13):
                name = f'WTC7-{step}.int'
                data = z.read(members[name])
                record(f'{case}-step-driver-{step}', zpath.name,
                       list(enumerate(data.decode('ascii').splitlines(), 1)),
                       member=members[name], member_sha256=digest(data))
            for floor, step, nid in [(14, 10, 32223)] + ([(8, 1, 170516)] if case == 'B' else []):
                name = f'WTC7-Fl{floor:02}-{step}.int'
                data = z.read(members[name])
                text = data.decode('ascii')
                picks = [(n, s) for n, s in enumerate(text.splitlines(), 1)
                         if any(k in s for k in ['-CoreB-', '-1C137-', '-2C137-', '-1C101-', '-2C101-', '-SLNo-'])]
                record(f'{case}-Fl{floor:02}-step-{step}-selected-driver-calls', zpath.name, picks,
                       member=members[name], member_sha256=digest(data))
                components = ['CoreB', '1C137', '2C137'] if floor == 14 else ['1C101', '2C101', 'SLNo']
                for comp in components:
                    name = f'WTC7-Fl{floor:02}-{comp}-{step}.int'
                    data = z.read(members[name])
                    picks = [(n, s) for n, s in enumerate(data.decode('ascii').splitlines(), 1)
                             if s.startswith(f'BF,{nid},TEMP,')]
                    assert picks
                    record(f'{case}-Fl{floor:02}-step-{step}-node-{nid}-{comp}', zpath.name, picks,
                           member=members[name], member_sha256=digest(data))
        name = 'CaseB_Temps/INTFILES+10%14SEP07/mover'
        data = z.read(name)
        record('mover-complete', zpath.name, list(enumerate(data.decode('ascii').splitlines(), 1)),
               member=name, member_sha256=digest(data))
        name = prior['nul_members'][0]['path']
        data = z.read(name)
        assert data == b'\0' * 328
        result['nul_record'] = {'source': zpath.name, 'member': name, 'bytes': 328,
                                'byte_offsets_inclusive': [0, 327], 'all_bytes_hex': '00', 'sha256': digest(data)}
    assert digest(zpath.read_bytes()) == pin

    apdl_selection = {
        '1 Floor_8-16_15AUG07.apdl': {21, 23},
        '2 Floor_GR_TO_7-22AUG07.apdl': set(range(1, 6)),
        '3_LOADS AND SOLU_15AUG07_0.25LL-names_redacted.apdl': {15, 16, 585, 4416, 4417, 4435, 4451, 4570, *range(4275, 4281)}
    }
    for name, indices in apdl_selection.items():
        data = (june / name).read_bytes()
        result['originals'].append({'source': name, 'stored_sha256': digest(data)})
        record('APDL-' + name, name, [(n, s) for n, s in enumerate(data.decode('latin1').splitlines(), 1) if n in indices])

    master_name = 'wtc7_global_8a_no-conn-matl.k.gz'
    p = sept / master_name
    compressed_pin = digest(p.read_bytes())
    h = hashlib.sha256()
    controls, includes = [], []
    curves = {}
    current = None
    special_ranges = [(857, 871), (1047, 1058), (2163, 2170), (2360, 2369)]
    selected_numeric = []
    tail_capture = 0
    with gzip.open(p, 'rb') as stream:
        for n, raw in enumerate(stream, 1):
            h.update(raw)
            s = raw.decode('latin1').rstrip('\r\n')
            stripped = s.strip()
            if n <= 15:
                controls.append((n, s))
            if any(a <= n <= b for a, b in special_ranges):
                selected_numeric.append((n, s))
            if stripped.startswith(('*INCLUDE', '$*INCLUDE')) or ('Incorporate ANSYS Damage' in s):
                tail_capture = 18
            if tail_capture:
                includes.append((n, s))
                tail_capture -= 1
            if stripped.startswith('*'):
                if stripped.startswith('*DEFINE_CURVE'):
                    current = []
                else:
                    current = None
            elif current is not None and stripped and not stripped.startswith('$'):
                current.append((n, s))
                if len(current) == 1:
                    curveid = int(re.split(r'[,\s]+', stripped)[0])
                    curves[curveid] = current
    assert digest(p.read_bytes()) == compressed_pin
    expected = next(g for g in prior['gzip_sources'] if g['basename'] == master_name)
    assert expected['compressed_sha256'] == compressed_pin and expected['decompressed_sha256'] == h.hexdigest()
    result['originals'].append({'source': master_name, 'stored_sha256': compressed_pin, 'decompressed_sha256': h.hexdigest()})
    record('master-termination', master_name, controls)
    record('master-include-and-damage-hooks', master_name, includes)
    record('master-material-and-zero-stress-curve-locators', master_name, selected_numeric)
    for cid in [1, 2, 13, 27]:
        record(f'master-curve-{cid}', master_name, curves[cid])

    name = 'Damage_Global_ANSYS_CaseB_4.0hr.k.gz'
    data = gzip.decompress((sept / name).read_bytes())
    lines = data.decode('ascii').splitlines()
    picks = [(n, s) for n, s in enumerate(lines, 1) if s.startswith(('$', '*')) or n <= 8 or n > len(lines) - 12]
    result['originals'].append({'source': name, 'stored_sha256': digest((sept / name).read_bytes()), 'decompressed_sha256': digest(data)})
    record('damage-labels-and-penthouse-beams', name, picks)
    name = 'WTC7_CaseB_400pm.int.gz'
    with gzip.open(sept / name, 'rt', encoding='ascii') as stream:
        picks = [(n, s.rstrip('\r\n')) for n, s in zip(range(1, 10), stream)]
    record('lsdyna-first-node-cards-field-order', name, picks)
    result['originals'].extend({'source': g['basename'], 'stored_sha256': g['compressed_sha256'],
                               'decompressed_sha256': g['decompressed_sha256']}
                              for g in prior['gzip_sources'] if g['basename'] not in [r['source'] for r in result['originals']])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.root, Path(__file__).resolve().parent), indent=2, sort_keys=True))
