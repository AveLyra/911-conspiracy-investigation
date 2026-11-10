"""Check declared bytes, source navigation and preservation, not historical truth."""
from pathlib import Path
import argparse,hashlib,json

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
    assert [o['id'] for o in observations]==[f'OJ{n:02}' for n in range(1,8)]
    for o in observations:
        assert o['distinction'] and o['missing_discriminator']
        for pin in o['pins']:
            n=pin['physical_page']
            assert n in (23,24) and pin['internal_page']==n-22
            assert pin['production_footer']==f'{n+347:09d}'
            assert pin['url'].endswith('#page='+str(n))
    sources=json.loads((root/'SOURCES.json').read_text())
    assert sources['new_reading']['physical_pages']==[23,24]
    assert sources['earlier_context_reused']['physical_pages_reviewed_again']==[4,5]
    assert observations[3]['source_values']['operator_recollection']=='United flight 99'
    assert observations[3]['comparison']['supervisor_record']=='United Airlines Flight 93'
    assert observations[4]['source_values']==['JOHNSON','JACKSON proceeded','JEFFERSON directed JACKSON']
    count=0
    if args.native_inputs:
        native=json.loads(args.native_inputs.read_text())
        for item in native['files']:
            data=Path(item['path']).read_bytes()
            assert len(data)==item['bytes'],item['role']
            assert hashlib.sha256(data).hexdigest()==item['sha256'],item['role']
            count+=1
        prior=Path(native['preceding_review']).read_bytes()
        assert prior==Path(native['preserved_copy']).read_bytes()
        assert Path(native['combined_review']).read_bytes().startswith(prior+b'\n\n')
    print(json.dumps({'status':'passed','body_files_checked':len(manifest['files']),
        'source_navigation_entries':len(observations),'native_file_identities_checked':count,
        'scope':'Declared derivative/source/raster bytes, manually entered page/footer navigation, retained conflicting strings and exact predecessor preservation only. No independent source transcription, original-note/voice/caller/session/clock/custody/engineering-result authentication, cause adjudication or substantive goal acceptance.'},indent=2))

if __name__=='__main__':main()
