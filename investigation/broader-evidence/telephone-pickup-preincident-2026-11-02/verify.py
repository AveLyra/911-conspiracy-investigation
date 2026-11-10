"""Declared bytes/navigation/preservation checks, not tape-custody authentication."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--native-inputs',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
    mf=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for x in mf['files']:
        b=(root/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
        assert not re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',b.decode()),'networkaddress in body'
    obs=json.loads((root/'OBSERVATIONS.json').read_text())['observations'];assert [x['id'] for x in obs]==[f'MP{i:02}' for i in range(1,5)]
    footer={51:'000000739',52:'000000740',55:'000000743',56:'000000744'}
    for x in obs:
        assert x['distinction'] and x['missing_discriminator']
        for q in x['pins']:
            assert q['physical_page'] in footer
            assert q['production_footer']==footer[q['physical_page']]
            assert q['url'].endswith('#page='+str(q['physical_page']))
    assert obs[0]['literal_values']['reported_action']=='the tape was picked up by a female FBI Agent'
    assert obs[1]['literal_values']['timing_belief']=='before the plane was hijacked'
    assert obs[2]['literal_values']['typed_control']=='HQ366'
    assert obs[2]['literal_values']['lead_required']=='NO'
    assert obs[2]['literal_values']['information_received_time']=='7:50 PM'
    assert obs[3]['literal_values']['page52_page_number']=='1'
    s=json.loads((root/'SOURCES.json').read_text());assert s['source']['new_full_faces']==[52,55,56] and s['source']['reused_full_face']==[51]
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
    print(json.dumps({'status':'passed','derivative_body_files_checked':len(mf['files']),'related_manual_observation_entries_checked':4,'native_source_raster_preservation_files_checked':count,'new_full_faces':3,'reused_context_faces':1,'original_requirements_retained':18,'network_literal_check':'No IPv4literals in body, not general sensitivity clearance.','scope':'Declared source/raster/body bytes, manual source-value/navigation consistency and exact predecessor/TODO preservation. No independent pixel transcription, collector identity, tape/media receipt, voice/caller/aircraft/carrier/clock/custody/analysis/disposition authentication, full-file/canvass census, independent audit or original-goal acceptance.'},indent=2))
if __name__=='__main__':main()
