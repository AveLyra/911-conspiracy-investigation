"""Read-only checks of four captured catalog records and one reused comparison.

Resolve inputs through the repository media guard before running. This checks
captured bytes and statements, not physical origin, current custody or science.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

EXPECTED = {
    'd7.txt': {'bytes': 9764911, 'sha256': 'becdf5286dcef508ac034c9d79c60216072272cb1337bb3532965294054172ca',
               'key': 'edanmdm:nmah_1182945', 'line': 2836, 'offset': 5059984,
               'line_bytes': 3666, 'line_sha256': 'f11897e46be7db1985cea8a0c9f24c5e36058144ae20fe7410868614b54ebeb9'},
    '75.txt': {'bytes': 9817092, 'sha256': '3d3e62737098084970fe51d0ec47ac541aa41b9474df9d9aa0393b94c6fca6c8',
               'key': 'edanmdm:nmah_1182948', 'line': 407, 'offset': 708223,
               'line_bytes': 3260, 'line_sha256': '3b825dd166a41731600ef0ef4745605c8f65d45bac2b691c339483cd9632e247'},
    '9a.txt': {'bytes': 9739321, 'sha256': '6bc96aa1140e86be87e4f50ffcf99d42c9e1ecd9c2acc0acbc4fc5849987cc7e',
               'key': 'edanmdm:nmah_1182953', 'line': 3133, 'offset': 5586432,
               'line_bytes': 3464, 'line_sha256': '2103e3f4a9a1bb0779c4ee88071b711f4be5b2e43ebe905490230782a4b58107'},
    'cf.txt': {'bytes': 9716526, 'sha256': '66843c9bf963c5023dc176082cf547eb4d8a475c44c3a95c83442f664f312f91',
               'key': 'edanmdm:nmah_1182954', 'line': 3209, 'offset': 5715292,
               'line_bytes': 3289, 'line_sha256': '32160fcaf6611dcb5c77a611ca33cd0362f361dde41dc7b1d9cb83f832e771e0'}}


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--shard-dir', type=Path, required=True)
    parser.add_argument('--comparison-record', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'records': {},
              'new_physical_custody_or_image_verified': False,
              'new_source_bodies': 4, 'reused_comparison_bodies': 1}
    parsed = {}
    for name, expected in EXPECTED.items():
        path = args.shard_dir / name
        before = path.stat()
        h = hashlib.sha256()
        with path.open('rb') as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b''):
                h.update(block)
        assert before.st_size == expected['bytes'] and h.hexdigest() == expected['sha256']
        offset, hits = 0, []
        with path.open('rb') as handle:
            for number, line in enumerate(handle, 1):
                if expected['key'].split(':', 1)[1].encode() in line:
                    row = json.loads(line)
                    if row.get('url') == expected['key']:
                        assert number == expected['line'] and offset == expected['offset']
                        assert len(line) == expected['line_bytes']
                        assert hashlib.sha256(line).hexdigest() == expected['line_sha256']
                        assert hashlib.sha1(row['url'].encode()).hexdigest() == row['hash']
                        assert row['content']['descriptiveNonRepeating']['metadata_usage']['access'] == 'CC0'
                        assert row['content']['indexedStructured']['online_media_type'] == ['Images']
                        hits.append(row)
                offset += len(line)
        assert len(hits) == 1
        parsed[expected['key']] = hits[0]
        assert (before.st_size, before.st_mtime_ns) == (path.stat().st_size, path.stat().st_mtime_ns)
        result['records'][expected['key']] = dict(expected, exact_matches_in_shard=1,
                                                   image_flag_present=True, metadata_usage='CC0')
    comparison_raw = args.comparison_record.read_bytes()
    assert hashlib.sha256(comparison_raw).hexdigest() == '3c19ae0c6bedb5ca011ffbc168b0915701fe4d1e8309bdcc911573d4861f4bde'
    comparison = json.loads(comparison_raw)
    assert comparison['url'] == 'edanmdm:nmah_1182951'
    result['comparison_record'] = {'key': comparison['url'],
                                  'line_sha256': hashlib.sha256(comparison_raw).hexdigest(),
                                  'new_acquisition_claimed': False}
    assembly = parsed['edanmdm:nmah_1182945']['content']
    stub = parsed['edanmdm:nmah_1182948']['content']
    bracket = parsed['edanmdm:nmah_1182953']['content']
    cladding = parsed['edanmdm:nmah_1182954']['content']
    checks = {
        'assembly_description_has_70th_floor_south_tower_and_two_stubs':
            '70th floor of the south tower, and two short column stubs' in assembly['freetext']['notes'][0]['content'],
        'assembly_exhibit_flag_and_title': assembly['indexedStructured']['onPhysicalExhibit'] == ['Yes'] and
            assembly['indexedStructured']['exhibition'] == [{'building': 'NMAH', 'exhibitionTitle': 'Price of Freedom'}],
        'stub_floor_belief_retained': 'It is believed' in stub['freetext']['notes'][0]['content'] and
            'a floor in the 90s' in stub['freetext']['notes'][0]['content'],
        'negative_reference_exact': stub['freetext']['notes'][2]['content'] == 'SI Neg. #2002-5979',
        'loan_label_exact': bracket['freetext']['notes'][3]['content'] == 'Currently on loan',
        'cladding_material_exact': cladding['freetext']['physicalDescription'][0]['content'] == 'aluminum alloy (overall material)',
        'five_observed_accession_values_same': all(any(p['label'] == 'accession number' and p['content'] == '2002.0205'
            for p in obj['content']['freetext']['identifier']) for obj in [*parsed.values(), comparison])}
    assert all(checks.values())
    result['reported_field_checks'] = checks
    result['relationship_scope'] = 'Catalog identifier relationship only; no physical-piece grouping, donor, shipment, floor/tower or original loan/negative authentication.'
    result['all_checks_passed'] = True
    with args.output.open('x') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'all_checks_passed': True, 'new_bodies': 4, 'reused_bodies': 1,
                      'negative_and_loan_statements_verified_in_source': True,
                      'original_negative_loan_or_physical_origin_authenticated': False}))


if __name__ == '__main__':
    main()
