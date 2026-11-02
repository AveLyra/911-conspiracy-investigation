"""Declared-byte/navigation checks; no hidden extraction or identity reconstruction."""
from pathlib import Path
import argparse,hashlib,json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native-inputs',type=Path);a=ap.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        data=(root/item['name']).read_bytes()
        assert len(data)==item['bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    obs=json.loads((root/'OBSERVATIONS.json').read_text())['observations']
    assert [x['id'] for x in obs]==[f'OC{i:02}' for i in range(1,5)]
    for x in obs:
        assert x['distinction'] and x['missing_discriminator']
        for p in x['pins']:
            n=p['physical_page'];assert n in (18,19)
            assert p['internal_page']==n-17 and p['production_footer']==f'{n+352:09d}'
            assert p['url'].endswith('#page='+str(n))
    sources=json.loads((root/'SOURCES.json').read_text())
    assert sources['official_counterpart']['physical_pages_newly_read']==[18,19]
    assert sources['prior_mirror']['physical_pages']==[23,24]
    assert obs[1]['source_values']['official_part02_visible_recollection']=='United flight 99'
    assert obs[1]['comparison']['previously_read_value']=='United Airlines Flight 93'
    assert obs[2]['visible_fields']['referenced_serial']=='3255'
    count=0
    if a.native_inputs:
        native=json.loads(a.native_inputs.read_text())
        # Exclusion terms remain in a local review input, never published here.
        for item in manifest['files']:
            text=(root/item['name']).read_text().upper()
            for term in native.get('excluded_public_tokens',[]):
                assert term.upper() not in text,item['name']
        for item in native['files']:
            data=Path(item['path']).read_bytes()
            assert len(data)==item['bytes'],item['role']
            assert hashlib.sha256(data).hexdigest()==item['sha256'],item['role']
            count+=1
        before=Path(native['preceding_review']).read_bytes()
        assert before==Path(native['preserved_copy']).read_bytes()
        assert Path(native['combined_review']).read_bytes().startswith(before+b'\n\n')
    print(json.dumps({'status':'passed','body_files_checked':len(manifest['files']),'source_navigation_entries':len(obs),'native_file_identities_checked':count,'scope':'Declared source/derivative/raster bytes, manually entered navigation and conflicting strings, exclusion of named-source imports into the new text and predecessor preservation only. No independent pixel transcription, native identity, call/session/clock/custody/engineering validation, cause resolution or original-goal acceptance.'},indent=2))

if __name__=='__main__':main()
