"""Verify bytes and reproduce selected static SWF text; never execute Flash."""
from pathlib import Path
import argparse,hashlib,json,zipfile
from static_swf_text import extract

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--court-zip',type=Path);p.add_argument('--native-inputs',type=Path);a=p.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for x in manifest['files']:
        b=(root/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
    sources=json.loads((root/'SOURCES.json').read_text());obs=json.loads((root/'OBSERVATIONS.json').read_text())
    assert [x['id'] for x in obs['observations']]==['NC01','NC02','NC03']
    assert all(x['distinction'] and x['missing_discriminator'] for x in obs['observations'])
    selected=obs['selected_definitions'];assert len(selected)==9
    assert len({x['id'] for x in selected})==9
    assert all(x['container']=='root' and x['tag']==11 for x in selected)
    for track,n in [('FAA',4),('TEL',4),('REC',3),('MAT',3),('STL',4)]:
        for i in range(1,n+1):assert '**'+track+f'{i:02}'+':**' in (root/'OPEN-TODOS.md').read_text()
    assert sources['court_index']['original_access_utc'] is None
    native_checks=0
    if a.native_inputs:
        native=json.loads(a.native_inputs.read_text())
        for x in native['files']:
            b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['role'];native_checks+=1
        prior=Path(native['prior']).read_bytes()
        assert prior==Path(native['preserved']).read_bytes()
        assert Path(native['combined']).read_bytes()==prior+b'\n\n'+(root/'README.md').read_bytes()
        html=Path(native['court_html']).read_text().splitlines()
        assert html[44].strip()=='P200054'
        assert 'Summary of Flight 77' in html[50] and 'other three flights' in html[50]
        assert 'http://coop.vaed.uscourts.gov/moussaoui/flights.zip' in html[72]
    decoded_count=None
    if a.court_zip:
        b=a.court_zip.read_bytes();s=sources['court_archive'];assert len(b)==s['bytes'] and sha(b)==s['sha256'],'court ZIP'
        with zipfile.ZipFile(a.court_zip) as z:
            assert z.namelist().count(s['member'])==1
            raw=z.read(s['member'])
        assert raw[:3]==b'FWS' and len(raw)==s['member_bytes'] and sha(raw)==s['member_sha256'],'SWF bytes'
        d=extract(raw);decoded_count=len(d['text_definitions']);assert decoded_count==548
        targets={x['id'] for x in selected}
        actual=[x for x in d['text_definitions'] if x['id'] in targets]
        assert actual==selected,'selected decoded tags, glyphs, text, offsets and bounds'
        for k,v in obs['selected_font_metadata'].items():
            assert {field:d['fonts'][int(k)][field] for field in v}==v,'font metadata'
    print(json.dumps({'status':'passed','derivative_body_files_checked':len(manifest['files']),'court_zip_redecoded':bool(a.court_zip),'full_static_definitions_decoded':decoded_count,'selected_definitions_reproduced':len(selected) if a.court_zip else 0,'native_file_identities_checked':native_checks,'scope':'Published bytes/navigation/TODO retention; optional exact source/member and same-parser static glyph extraction plus predecessor preservation. No independent decoder, runtime/display-list, manifest, identity, recording, carrier/session/clock/canvass/custody authentication or whole-goal acceptance.'},indent=2))
if __name__=='__main__':main()
