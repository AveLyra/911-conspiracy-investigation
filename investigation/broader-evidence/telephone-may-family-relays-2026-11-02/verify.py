"""Declared bytes/navigation/preservation checks, not family/carrier authentication."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--native-inputs',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
    mf=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for x in mf['files']:
        b=(root/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
        assert not re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',b.decode()),'networkaddress in body'
    obs=json.loads((root/'OBSERVATIONS.json').read_text())['observations'];assert [x['id'] for x in obs]==[f'MR{i:02}' for i in range(1,6)]
    footer={53:'000000741',54:'000000742',60:'000000756',61:'000000757',62:'000000758'}
    for x in obs:
        assert x['distinction'] and x['missing_discriminator']
        for q in x['pins']:
            n=q['physical_page']
            if q['source']=='mirror':assert n in footer and q['production_footer']==footer[n]
            elif q['source']=='staff':assert n in (31,34,94) and q['printed_page']==n
            else:raise AssertionError('unknown source')
            assert q['url'].endswith('#page='+str(n))
    assert '6:05' in obs[0]['literal_values']['memo_time'] and '6:05' in obs[0]['literal_values']['DL99_time']
    assert 'PREPARE EC' in obs[1]['literal_values']['DL99_task']
    assert obs[1]['literal_values']['DL99_assignment_time']=='7:30 PM'
    assert obs[2]['literal_values']['memo_Flight77_phrase']=='crashed into the World Trade Towers'
    assert obs[2]['literal_values']['staff_Flight77_site']=='Pentagon'
    assert obs[3]['literal_values']['DL99_event_time']=='6:05 AM'
    assert obs[4]['literal_values']['DL99_control']=='DL99'
    assert 'Sept 12, 2001' in obs[4]['literal_values']['staff_note261']
    s=json.loads((root/'SOURCES.json').read_text());assert s['new_mirror_units']['new_full_faces']==[53,54,60,61,62]
    assert s['reused_staff_context']['reused_physical_printed_pages']==[31,34,94]
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
    print(json.dumps({'status':'passed','derivative_body_files_checked':len(mf['files']),'related_manual_observation_entries_checked':5,'native_source_raster_preservation_files_checked':count,'new_mirror_faces':5,'reused_staff_context_faces':3,'original_requirements_retained':18,'network_literal_check':'No IPv4literals in body, not general sensitivity clearance.','scope':'Declared source/raster/body identities, manually entered locators/values, predecessor/TODO preservation. No independent pixel transcription, family/source/aircraft/hijacker/call/carrier/service/clock/custody/interview/response authentication, native carrier/canvass replication, independent audit or original-goal acceptance.'},indent=2))
if __name__=='__main__':main()
