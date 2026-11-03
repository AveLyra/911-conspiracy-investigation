"""Check published bundle and optionally reproduce the scoped court-pair result."""
from pathlib import Path
import argparse
import hashlib
import json
from compare_pair import analyze, check_controls


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--archive', type=Path)
    args = ap.parse_args()
    manifest = json.loads((args.bundle / 'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        data = (args.bundle / item['name']).read_bytes()
        assert len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], item['name']
    result = {'exit_code': 0, 'bundle_files_checked': len(manifest['files']),
              'controls': check_controls(), 'scoped_result_reproduced_from_archive': False,
              'independent_reader_or_history_authenticated': False}
    if args.archive:
        expected = json.loads((args.bundle / 'RESULTS.json').read_text())
        actual = json.loads(json.dumps(analyze(args.archive)))  # Compare the published JSON representation, including tag-code keys.
        assert actual == expected
        result.update(scoped_result_reproduced_from_archive=True,
                      exact_matching_decoded_text_occurrences=actual['common_text_occurrences'],
                      selected_members=len(actual['selected_members']),
                      standard_sound_tags=sum(len(x['standard_sound_tags']) for x in actual['selected_members']))
    result['limit'] = 'Preservation and reproducibility through the same passive parser plus comparator controls; no runtime, audio/caller, native tape/custody or substantive-goal authentication.'
    return result


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
