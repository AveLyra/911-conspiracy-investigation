"""Preservation/navigation checks, not authentication of the reported historical acts."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--native-inputs',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        data=(root/item['name']).read_bytes()
        assert len(data)==item['bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    observations=json.loads((root/'OBSERVATIONS.json').read_text())['observations']
    assert len({x['id'] for x in observations})==len(observations)
    assert all(x['id'].startswith('IR') for x in observations)
    for item in observations:
        assert item['distinction'] and item['test_or_input']
        for p in item['pins']:
            n=p['physical_page'];assert 38<=n<=41
            assert p['internal_page']==n-37 and p['footer']==f'{n+409:09d}'
            assert p['url'].endswith('#page='+str(n))
    pins=json.loads((root/'SOURCE-PINS.json').read_text())
    assert pins['record1']['physical_pages']==[38,39,40,41]
    assert pins['adjoining_record']['physical_pages']==[42,43]
    assert pins['next_boundary']['physical_page']==44
    native_count=0
    if args.native_inputs:
        native=json.loads(args.native_inputs.read_text())
        for item in native['files']:
            data=Path(item['path']).read_bytes()
            assert len(data)==item['bytes'],item['role']
            assert hashlib.sha256(data).hexdigest()==item['sha256'],item['role']
            native_count+=1
        before=Path(native['preceding_review']).read_bytes()
        after=Path(native['combined_review']).read_bytes()
        assert before==Path(native['preceding_preserved_copy']).read_bytes()
        assert after.startswith(before+b'\n\n')
    print(json.dumps({'status':'passed','body_files_checked':len(manifest['files']),
                      'native_file_identities_checked':native_count,'observation_navigation_entries':len(observations),
                      'scope':'Declared bytes, source/footer/page navigation and preservation only. Manual visible-image readings are separate; no native statement/system execution/call/clock/custody/motive authentication or original-goal acceptance.'},indent=2))


if __name__=='__main__':main()
