"""Declared source/body byte and preservation checks; not a voicemail authentication."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--native-inputs',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
    mf=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for x in mf['files']:
        b=(root/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
        assert not re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',b.decode()),'networkaddress in publicbody'
    obs=json.loads((root/'OBSERVATIONS.json').read_text())['observations'];assert [x['id'] for x in obs]==[f'VM{i:02}' for i in range(1,5)]
    footer={63:'000000761',64:'000000762',65:'000000763'}
    for x in obs:
        assert x['distinction'] and x['missing_discriminator']
        for q in x['pins']:
            assert q['physical_page'] in footer
            assert q['production_footer']==footer[q['physical_page']]
            assert q['url'].endswith('#page='+str(q['physical_page']))
    assert obs[0]['literal_values']['control']=='WF1899'
    assert obs[1]['literal_values']['instruction_excerpt']=='FOR ACCESS TO MAIL OF OLSON'
    assert obs[1]['literal_values']['intake_wording']=='VOICE MAIL'
    assert obs[2]['literal_values']['information_received_time']=='10:30 AM'
    assert obs[2]['literal_values']['event_time']=='10:30 AM'
    assert obs[2]['literal_values']['assignment_time']=='2:15 AM'
    assert obs[3]['literal_values']['handwritten_reading']=='WF3089'
    s=json.loads((root/'SOURCES.json').read_text());assert s['unit']['new_full_faces']==[63,64,65]
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
    print(json.dumps({'status':'passed','derivative_body_files_checked':len(mf['files']),'related_manual_observation_entries_checked':4,'native_source_raster_preservation_files_checked':count,'original_requirements_retained':18,'network_literal_check':'No IPv4literals in body; not general sensitivity clearance.','scope':'Declared source/raster/body bytes, manually entered source values/navigation, exact predecessor preservation/TODO retention. No independent pixel transcription, sender/message/voice/flight/carrier/clock/custody/access/collection/disposition authentication, full-file/canvass census, independent audit or original-goal acceptance.'},indent=2))
if __name__=='__main__':main()
