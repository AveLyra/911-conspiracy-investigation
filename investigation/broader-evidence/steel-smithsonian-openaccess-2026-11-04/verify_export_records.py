"""Verify three published Smithsonian shards and extract two exact records.

This reads local inputs only. Resolve each through the repository media guard
before execution. No images, network requests or source writes occur.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

EXPECTED = {
    'sample': {'sha256': 'dab5eccc35289e7fc2b5008a2a3f93eac8d61b8ef78b49c4e45824fbf624456e',
               'bytes': 9775511},
    'column': {'sha256': '6369ba2936c52b16af0f81dba7fdd0d41cf0467c6aaf8e4e0a6071cca9f9935d',
               'bytes': 9780938, 'key': 'edanmdm:nmah_1182951', 'line': 3207,
               'offset': 5750284, 'line_bytes': 3881,
               'line_sha256': '3c19ae0c6bedb5ca011ffbc168b0915701fe4d1e8309bdcc911573d4861f4bde'},
    'photo': {'sha256': '4e24d2de5379a68c21a55f66538bdca061d3930d1ce25f7d12c8f004049d5343',
              'bytes': 9603142, 'key': 'edanmdm:nmah_1462757', 'line': 4941,
              'offset': 9340279, 'line_bytes': 3054,
              'line_sha256': '0f17507ee567d495b8adad5938b4e103a3abe534dc7e8024d6828d30be6cf793'}}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(__doc__)
    for item in ['sample', 'column', 'photo']:
        parser.add_argument('--' + item + '-shard', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    results = {'utc': datetime.now(timezone.utc).isoformat(), 'entities': {},
               'schema_routing_control': {}, 'exact_record_checks': {},
               'historical_provenance_authenticated': False}
    for label in ['sample', 'column', 'photo']:
        path = getattr(args, label + '_shard')
        assert path.stat().st_size == EXPECTED[label]['bytes']
        before = path.stat()
        hashed = digest(path)
        assert hashed == EXPECTED[label]['sha256']
        results['entities'][label] = {'bytes': before.st_size, 'sha256': hashed}
        if label == 'sample':
            count = 0
            with path.open('rb') as handle:
                for _ in range(32):
                    record = json.loads(handle.readline())
                    assert record['url'].startswith('edanmdm:nmah_')
                    assert hashlib.sha1(record['url'].encode()).hexdigest() == record['hash']
                    assert record['hash'].startswith('00')
                    count += 1
            results['schema_routing_control'] = {
                'sampled_records': count, 'all_sha1_url_equals_hash': True,
                'all_shard_prefix_matches': True,
                'unrelated_descriptive_content_semantically_read': False,
                'not_a_universal_export_schema_proof': True}
        else:
            expected = EXPECTED[label]
            position, hits = 0, []
            with path.open('rb') as handle:
                for number, line in enumerate(handle, 1):
                    if expected['key'].split(':', 1)[1].encode() in line:
                        record = json.loads(line)
                        if record.get('url') == expected['key']:
                            assert number == expected['line']
                            assert position == expected['offset']
                            assert len(line) == expected['line_bytes']
                            assert hashlib.sha256(line).hexdigest() == expected['line_sha256']
                            assert hashlib.sha1(record['url'].encode()).hexdigest() == record['hash']
                            assert record['unitCode'] == 'NMAH' and record['type'] == 'edanmdm'
                            assert record['content']['descriptiveNonRepeating']['metadata_usage']['access'] == 'CC0'
                            hits.append(record)
                    position += len(line)
            assert len(hits) == 1
            # The id-route hash is not a content checksum: a changed title leaves
            # this field calculation unchanged. This is a mathematical control,
            # never a rewrite of the source or a claim of historical alteration.
            modified = dict(hits[0], title='SYNTHETIC CONTROL ONLY')
            assert hashlib.sha1(modified['url'].encode()).hexdigest() == hits[0]['hash']
            results['exact_record_checks'][label] = {
                'dataset_key': expected['key'], 'exact_matches_in_its_shard': 1,
                'line': expected['line'], 'byte_offset': expected['offset'],
                'line_bytes': expected['line_bytes'], 'line_sha256': expected['line_sha256'],
                'id_hash_not_content_authentication_control_passed': True,
                'metadata_usage_field': 'CC0', 'source_record_modified': False}
        assert (before.st_size, before.st_mtime_ns) == (path.stat().st_size, path.stat().st_mtime_ns)
    results['all_checks_passed'] = True
    with args.output.open('x') as handle:
        json.dump(results, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'all_checks_passed': True, 'exact_records': 2,
                      'routing_schema_control_records': 32,
                      'historical_provenance_authenticated': False}))


if __name__ == '__main__':
    main()
