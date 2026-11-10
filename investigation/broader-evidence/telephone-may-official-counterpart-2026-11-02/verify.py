"""Integrity and exact-index reproduction; not independent historical authentication."""
from pathlib import Path
import argparse
import hashlib
import json
import re


def checked_bytes(path, expected):
    data = Path(path).read_bytes()
    assert len(data) == expected['bytes'], 'Byte count differs: ' + str(path)
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], 'SHA-256 differs: ' + str(path)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--official-pdf', type=Path)
    parser.add_argument('--mirror-pdf', type=Path)
    for number in ('01', '02', '08'):
        parser.add_argument('--index-' + number, type=Path)
    args = parser.parse_args()
    bundle = args.bundle
    manifest = json.loads((bundle / 'BUNDLE-HASHES.json').read_text())
    for entry in manifest['files']:
        checked_bytes(bundle / entry['name'], entry)
    assert len({entry['name'] for entry in manifest['files']}) == len(manifest['files'])
    sources = json.loads((bundle / 'SOURCES.json').read_text())
    observations = json.loads((bundle / 'OBSERVATIONS.json').read_text())
    mapping = {entry['id']: entry for entry in observations}
    assert len(mapping) == len(observations) == 8
    assert mapping['MC01']['investigation_raw'] == '06/05/2002'
    assert mapping['MC01']['transcription_raw'] == '06/06/2002'
    assert mapping['MC07']['investigation_raw'] == '06/10/2001'
    assert mapping['MC07']['transcription_raw'] == '06/28/2002'
    assert mapping['MC07']['preferred_year_selected'] is False
    assert sources['official']['faces_inspected_this_unit'] == [72, 73, 74, 75, 76]
    assert sources['mirror']['faces_inspected_this_unit'] == [71]
    assert mapping['MC02']['actual_notes_recovered'] is False
    supplied_source_checks = []
    for name in ('official', 'mirror'):
        path = getattr(args, name + '_pdf')
        if path is not None:
            checked_bytes(path, sources[name])
            supplied_source_checks.append(name)
    search = json.loads((bundle / 'SEARCH-SCOPE.json').read_text())
    reproduced = []
    for expected in search['results']:
        number = expected['source'].removeprefix('part')
        path = getattr(args, 'index_' + number)
        if path is None:
            continue
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected['index_sha256']
        rows = json.loads(data)
        assert len(rows) == expected['rows']
        hits = []
        for row in rows:
            matches = [name for name, pattern in search['terms'].items()
                       if re.search(pattern, row['ordinary_text'], re.IGNORECASE)]
            if matches:
                hits.append({'physical_page': row['physical_page'], 'terms': matches})
        assert hits == expected['hits'], 'Declared exact-index hits differ'
        reproduced.append({'source': expected['source'], 'rows': len(rows), 'hits': hits})
    return {'exit_code': 0, 'bundle_files_checked': len(manifest['files']),
            'source_bytes_verified': supplied_source_checks, 'index_results_reproduced': reproduced,
            'manual_readings_independently_verified_by_code': False,
            'source_originals_modified': False, 'historical_call_interview_custody_or_goal_authenticated': False,
            'limit': 'Manifest/byte checks and exact index reproduction; no image-text, speaker, clock, custody or completeness authentication.'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
