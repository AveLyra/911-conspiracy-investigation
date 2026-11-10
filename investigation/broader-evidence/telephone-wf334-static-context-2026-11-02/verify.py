"""Passive bytes/structure reproduction; no Flash/ActionScript execution."""
from pathlib import Path
import argparse,hashlib,json,struct,zipfile
from structural_context import analyze,check_controls

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--court-zip',type=Path);p.add_argument('--native-inputs',type=Path);a=p.parse_args();root=Path(__file__).resolve().parent
    mf=json.loads((root/'BUNDLE-HASHES.json').read_text())
    for x in mf['files']:
        b=(root/x['name']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['name']
    obs=json.loads((root/'OBSERVATIONS.json').read_text());expected=obs['structural_result'];sources=json.loads((root/'SOURCES.json').read_text())
    assert [x['id'] for x in obs['observations']]==['SC01','SC02','SC03']
    assert all(x['distinction'] and x['missing_discriminator'] for x in obs['observations'])
    for t,n in [('FAA',4),('TEL',4),('REC',3),('MAT',3),('STL',4)]:
        for i in range(1,n+1):assert '**'+t+f'{i:02}'+':**' in (root/'OPEN-TODOS.md').read_text()
    controls=check_controls();native_count=0;sampled=0
    if a.native_inputs:
        n=json.loads(a.native_inputs.read_text())
        for x in n['files']:
            b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['role'];native_count+=1
        before=Path(n['preceding']).read_bytes();assert before==Path(n['preserved']).read_bytes()
        assert Path(n['combined']).read_bytes()==before+b'\n\n'+(root/'README.md').read_bytes()
    if a.court_zip:
        s=sources['court_archive'];b=a.court_zip.read_bytes();assert len(b)==s['bytes'] and sha(b)==s['sha256']
        with zipfile.ZipFile(a.court_zip) as z:
            assert z.namelist().count('AA77.swf')==1
            raw=z.read('AA77.swf')
        assert len(raw)==s['member_bytes'] and sha(raw)==s['member_sha256']
        actual=analyze(raw);assert actual==expected,'full selected structural reproduction'
        # Separate direct tag-header/prefix sampling, without recursive tag iterator.
        for x in expected['selected_placements']:
            o=x['placement_offset'];h=int.from_bytes(raw[o:o+2],'little');assert h>>6==26
            length=h&63;start=o+2
            if length==63:length=int.from_bytes(raw[start:start+4],'little');start+=4
            body=raw[start:start+length]
            assert length==x['body_length'] and sha(body)==x['body_sha256']
            assert body[0]==x['flags'] and int.from_bytes(body[1:3],'little')==x['depth']
            assert body[0]&2 and int.from_bytes(body[3:5],'little')==x['character_id']
            assert body[:x['prefix_bytes']].hex()==x['encoded_prefix_hex'];sampled+=1
    print(json.dumps({'status':'passed','body_files_verified':len(mf['files']),'byte_vector_controls':controls,'court_archive_redecoded':bool(a.court_zip),'selected_placements_reproduced':18 if a.court_zip else 0,'direct_sampled_tag_prefixes':sampled,'all98_sprite_and159_root_frame_count_checks':bool(a.court_zip),'native_file_identities_checked':native_count,'scope':'Bytes, field controls, explicit static references/labels/local frame counts, source preservation and18TODO retention. No independent full decoder, runtime/action/button, actual photograph, identity/message/caller/manifest/carrier/canvass authentication or whole-goal acceptance.'},indent=2))
if __name__=='__main__':main()
