"""Verify the public bundle; optionally reproduce selected source references."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip', type=Path,
                        help='Unchanged court-distributed flights.zip')
    args = parser.parse_args()
    manifest = json.loads((HERE/'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        raw = (HERE/item['name']).read_bytes()
        assert len(raw) == item['bytes'], item['name']
        assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['name']
    result = dict(bundle_hashes_match=True, hashed_files=len(manifest['files']),
                  source_reproduced=False,
                  scope='Integrity only unless --zip is supplied; neither mode authenticates historical calls.')
    if args.zip:
        from trace_zero_entry import analyze
        actual = analyze(args.zip)
        expected = json.loads((HERE/'STRUCTURE.json').read_text())
        assert actual == expected
        assert len(actual['selected_text_definitions']) == 22
        assert actual['independently_rechecked_placement_prefixes'] == 43
        assert len(actual['selected_sprite_definitions']) == 6
        assert len(actual['selected_button_definitions']) == 9
        result.update(source_reproduced=True,
                      all_548_prior_text_definitions_match=True,
                      selected_text_definitions=22,
                      selected_placement_prefixes=43,
                      selected_sprites=6,
                      selected_button_definitions=9,
                      all_98_sprite_frame_counts_match=True,
                      all_253_button_layouts_parsed=True,
                      runtime_or_historical_call_verification=False)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
