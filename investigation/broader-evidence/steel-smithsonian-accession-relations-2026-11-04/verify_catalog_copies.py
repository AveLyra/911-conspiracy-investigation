"""Verify the five exact public catalog-row copies, not their historical claims."""
import argparse
import hashlib
import json
from pathlib import Path

HASHES = {
    'nmah_1182945': 'f11897e46be7db1985cea8a0c9f24c5e36058144ae20fe7410868614b54ebeb9',
    'nmah_1182948': '3b825dd166a41731600ef0ef4745605c8f65d45bac2b691c339483cd9632e247',
    'nmah_1182951': '3c19ae0c6bedb5ca011ffbc168b0915701fe4d1e8309bdcc911573d4861f4bde',
    'nmah_1182953': '2103e3f4a9a1bb0779c4ee88071b711f4be5b2e43ebe905490230782a4b58107',
    'nmah_1182954': '32160fcaf6611dcb5c77a611ca33cd0362f361dde41dc7b1d9cb83f832e771e0'}


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    records = []
    for object_id, expected in HASHES.items():
        filename = 'EXPORT-' + object_id + '-2026-11-04-source.jsonl'
        data = (args.directory / filename).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected
        obj = json.loads(data)
        assert obj['url'] == 'edanmdm:' + object_id
        assert hashlib.sha1(obj['url'].encode()).hexdigest() == obj['hash']
        assert obj['content']['descriptiveNonRepeating']['metadata_usage']['access'] == 'CC0'
        records.append({'record_ID': object_id, 'bytes': len(data), 'sha256': expected})
    print(json.dumps({'all_five_exact_source_copies_match': True,
                      'newly_acquired_in_this_unit': 4, 'reused_comparison': 1,
                      'records': records,
                      'historical_claims_or_custody_authenticated': False}, indent=2))


if __name__ == '__main__':
    main()
