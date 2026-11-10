"""Check declared bytes/navigation; do not authenticate an alleged saved message."""
from pathlib import Path
import argparse,hashlib,json

def main():
    p=argparse.ArgumentParser();p.add_argument('--native-inputs',type=Path);a=p.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for item in manifest['files']:
        data=(root/item['name']).read_bytes()
        assert len(data)==item['bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    obs=json.loads((root/'OBSERVATIONS.json').read_text())['observations']
    assert [x['id'] for x in obs]==[f'IL{i:02}' for i in range(1,6)]
    for x in obs:
        assert x['distinction'] and x['missing_discriminator']
        for loc in x['pins']:
            n=loc['physical_page'];assert n in (68,69,70)
            assert loc['analyst_record_ordinal']==n-67
            assert loc['production_footer']==f'{n+698:09d}'
            assert loc['url'].endswith('#page='+str(n))
    assert obs[0]['literal_source_values']['reported_name']=='TODD RUBEN'
    assert obs[0]['literal_source_values']['reported_flight']=='#77'
    assert obs[1]['literal_source_values']['lead_control']=='WF334'
    assert obs[2]['literal_source_values']['event_time']=='blank'
    assert obs[3]['literal_source_values']['handwritten_reading']=='WF8406'
    sources=json.loads((root/'SOURCES.json').read_text())
    assert sources['intake_unit']['physical_pages']==[68,69,70]
    count=0
    if a.native_inputs:
        native=json.loads(a.native_inputs.read_text())
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
    print(json.dumps({'status':'passed','body_files_checked':len(manifest['files']),
        'source_navigation_entries':len(obs),'native_file_identities_checked':count,
        'scope':'Declared derivative/source/raster bytes, manually entered navigation/values, exclusion of rejected preliminary associations and exact predecessor preservation only. No independent pixel transcription, actual message/caller/flight/session/clock/custody/disposition verification, full canvass replication or original-goal acceptance.'},indent=2))

if __name__=='__main__':main()
