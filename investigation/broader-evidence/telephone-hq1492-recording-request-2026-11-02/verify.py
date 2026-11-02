"""Verify declared bytes/navigation/preservation; not an alleged call or collection."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--native-inputs',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
    mf=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for x in mf['files']:
        b=(root/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
        assert not re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',b.decode()),'network address in public body'
    obs=json.loads((root/'OBSERVATIONS.json').read_text())['observations'];assert [x['id'] for x in obs]==[f'HR{i:02}' for i in range(1,6)]
    footer={57:'000000753',58:'000000754',59:'000000755'}
    for x in obs:
        assert x['distinction'] and x['missing_discriminator']
        for q in x['pins']:
            assert q['physical_page'] in footer
            assert q['production_footer']==footer[q['physical_page']]
            assert q['url'].endswith('#page='+str(q['physical_page']))
    assert obs[0]['literal_values']['reported_name']=='TODD REUBEN'
    assert obs[1]['literal_values']['lead_control']=='HQ1492'
    assert 'OBTAIN RECORDING' in obs[1]['literal_values']['directive_excerpt']
    assert obs[2]['literal_values']['information_received_time']=='7:49 AM'
    assert obs[2]['literal_values']['prior_WF334_information_received_time']=='7:49 PM'
    assert obs[2]['literal_values']['event_date']==obs[2]['literal_values']['event_time']=='blank'
    assert obs[3]['literal_values']['handwritten_reading']=='HQ3060'
    s=json.loads((root/'SOURCES.json').read_text());assert s['intake_unit']['new_full_faces']==[57,58,59]
    todo=(root/'OPEN-TODOS.md').read_text()
    for t,n in [('FAA',4),('TEL',4),('REC',3),('MAT',3),('STL',4)]:
        for i in range(1,n+1):assert '**'+t+f'{i:02}'+':**' in todo
    count=0
    if a.native_inputs:
        native=json.loads(a.native_inputs.read_text())
        for x in native['files']:
            b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['role'];count+=1
        before=Path(native['preceding']).read_bytes();assert before==Path(native['preserved']).read_bytes()
        assert Path(native['combined']).read_bytes()==before+b'\n\n'+(root/'README.md').read_bytes()
    print(json.dumps({'status':'passed','derivative_body_files_checked':len(mf['files']),'related_manual_observation_entries_checked':5,'native_source_raster_preservation_files_checked':count,'original_requirements_retained':18,'network_address_literal_scan':'no IPv4 literals in body; not a general sensitivity clearance','scope':'Declared source/raster/body identities, manually entered source values/navigation and exact predecessor preservation/TODO retention. No independent pixel transcription, message/caller/flight/cellular/voice/clock/custody/collection/disposition authentication, native ICF or whole-canvass replication, independent audit or original-goal acceptance.'},indent=2))
if __name__=='__main__':main()
