"""Verify declared bytes and passage-map structure, not speech or historical truth."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native-inputs', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'BUNDLE-HASHES.json').read_text())
    checks = []
    for item in manifest['files']:
        data = (root / item['name']).read_bytes()
        assert len(data) == item['bytes'], item['name']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['name']
    checks.append({'check': 'Declared eight body-file bytes/hashes', 'result': 'matched'})
    mapping = json.loads((root / 'PASSAGE-MAP.json').read_text())
    groups = mapping['passages']
    expected = {f'A{i:02}' for i in range(16)} | {f'B{i:02}' for i in range(1, 13)}
    assert len(groups) == 28 and {p['id'] for p in groups} == expected
    for p in groups:
        page = p['physical_page']
        assert page in ([3, 4, 5, 6, 7] if p['record'] == 'A' else [11, 12, 13, 14])
        assert p['internal_page'] == (page if p['record'] == 'A' else page - 9)
        assert p['footer'] == f'{page + (399 if p["record"] == "A" else 447):09d}'
        assert p['url'].endswith('#page=' + str(page))
    checks.append({'check': 'Declared analyst group IDs/page/internal/footer navigation', 'result': 'consistent', 'limit': 'Not mechanical validation of manually read words or physical audio coverage.'})
    covered = set()
    for relation in mapping['candidate_relations']:
        ids = set(relation['A'] + relation['B'])
        assert ids <= expected
        covered.update(ids)
        assert relation['limit']
    assert covered == expected
    differences = json.loads((root / 'DIFFERENCES.json').read_text())
    assert {d['id'] for d in differences['differences']} == {f'D{i:02}' for i in range(1, 11)}
    assert next(d for d in differences['differences'] if d['id'] == 'D07')['novelty'] == 'previously documented, retained'
    assert all(d['limit'] for d in differences['differences'])
    checks.append({'check': 'Every declared group addressed; ten derivative observations have limits and prior/new labels', 'result': 'consistent', 'limit': 'No independent corroboration, actual call/voice count or validated sample match.'})
    source_count = 0
    if args.native_inputs:
        native = json.loads(args.native_inputs.read_text())
        path = Path(native['source_path'])
        assert path.stat().st_size == native['source_bytes']
        assert hashlib.file_digest(path.open('rb'), 'sha256').hexdigest() == native['source_sha256']
        source_count += 1
        for item in native['image_hash_checks']:
            data = Path(item['path']).read_bytes()
            assert len(data) == item['bytes']
            assert hashlib.sha256(data).hexdigest() == item['sha256']
            source_count += 1
        assert Path(native['predecessor']).exists()
        assert hashlib.file_digest(Path(native['predecessor']).open('rb'), 'sha256').hexdigest() == native['predecessor_sha256']
        checks.append({'check': 'Held PDF, eleven reused rasters and preceding report bytes', 'result': 'matched', 'limit': 'Byte identity, not original-source authenticity or manual reading accuracy.'})
    print(json.dumps({'status': 'passed', 'body_files_checked': len(manifest['files']),
                      'native_source_inputs_checked': source_count, 'checks': checks,
                      'scope': 'Publication payload integrity and declared navigation structure only. Actual comparison was manual page-image reading. No native-media, voice, clock, carrier, custody or historical-cause test.'}, indent=2))


if __name__ == '__main__':
    main()
