#!/usr/bin/env python3
"""Read-only comparison of two frozen observation tables; no image decoding.

Root abbreviations are expanded solely through its explicit bijective legend.
No semantic category is combined, voted on or recoded.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import re
import struct

HERE = Path(__file__).resolve().parent
PINS = {
    'PROTOCOL.md': '50785dd33e8543a0de76932be36e011693998cffa11a734040b3fb4f1ec3680d',
    'root-observations.md': 'e31b2f9cbc880872aec69201c155f27c0aa3d3bed9bb5cea8d7748976c853a76',
    'observer.md': '9fe612f5df31b4a37557b57cde83d9f979499a5bf48744c06726ef4873b3b117',
    'run01/manifest.json': 'e32a70c421e4df661d9a2eeb8d057109668276a29597d8dab03fcfdca06f6fb6',
    'run01/receipt.json': '18dd861e333aaea0675c06c56477b2c5442ae8e805ed6c7ba5895cb85ccca8a1',
    '../tilted-camera-source-join/project01.json':
        '4fa6fa6c6bc1c06802fae0fd4b0c8b8a07131e56729b4fad0f37471cb05e67f8',
}
LEGENDS = [
    {'B':'building', 'M':'mixed_or_unresolved', 'S':'smoke_or_background', 'F':'foreground'},
    {'J':'corner_or_junction', 'E':'roof_edge_only', 'T':'facade_texture',
     'N':'none_resolved', 'U':'uncertain'},
    {'C':'candidate', 'D':'different_feature', 'R':'unresolved'},
]
AXES = ['host', 'feature', 'lower_foot_relation']
SELECTION = list(range(150, 445, 6))
EXPECTED = sorted([(i,'PM05') for i in range(150,403,6)] +
                  [(i,'PM08') for i in range(210,445,6)])


def pin(path):
    with path.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'bytes':path.stat().st_size, 'sha256':digest}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def parse_note(name):
    rows, views = {}, {}
    for line in (HERE/name).read_text().splitlines():
        if not line.startswith('|'):
            continue
        cells = [part.strip() for part in line.strip('|').split('|')]
        if cells[0].isdigit():
            require(len(cells)==7, 'observation table width')
            frame,track,key,*other = cells
            host,feature,relation,reason = other
            index = (int(frame),track)
            require(index not in rows and track in ('PM05','PM08'), 'duplicate/unknown row')
            require(key in ('true','false') and bool(reason), 'key/reason invalid')
            raw = [host,feature,relation]
            if name=='root-observations.md':
                require(all(v in legend for v,legend in zip(raw,LEGENDS)), 'unknown root abbreviation')
                values = [legend[v] for v,legend in zip(raw,LEGENDS)]
            else:
                require(all(v in legend.values() for v,legend in zip(raw,LEGENDS)), 'unknown observer category')
                values = raw
            rows[index] = {'key':key=='true', 'categories':values, 'raw':raw, 'reason':reason}
        elif re.fullmatch(r'(?:panels/)?frame-[0-9]{4}\.png', cells[0]):
            require(len(cells)==2 and re.fullmatch('[0-9a-f]{64}',cells[1]), 'view hash syntax')
            path = cells[0] if cells[0].startswith('panels/') else 'panels/'+cells[0]
            require(path not in views, 'duplicate panel view entry')
            views[path] = cells[1]
    require(list(rows)==EXPECTED and len(rows)==83, 'exact 83 ordered row keys required')
    require(list(views)==[f'panels/frame-{i:04d}.png' for i in SELECTION], 'exact 50 ordered views required')
    return rows, views


def main():
    before = {name:pin(HERE/name) for name in PINS}
    for name,digest in PINS.items():
        require(before[name]['sha256']==digest, 'frozen input hash mismatch: '+name)
    manifest = json.loads((HERE/'run01/manifest.json').read_text())
    receipt = json.loads((HERE/'run01/receipt.json').read_text())
    require(receipt['products']['manifest.json']==before['run01/manifest.json'], 'receipt manifest pin')
    require(manifest['source_project_sha256']==PINS['../tilted-camera-source-join/project01.json'], 'project pin')
    require(manifest['selection_indices']==SELECTION and manifest['row_count']==83, 'manifest selection/count')
    manifest_rows = {}
    for row in manifest['points']:
        require(type(row['frame_index']) is int and type(row['key']) is bool, 'manifest index/key type')
        require(row['track_id'] in ('pointmass05','pointmass08'), 'manifest track')
        key = (row['frame_index'],row['track_id'].replace('pointmass','PM'))
        require(key not in manifest_rows, 'manifest duplicate')
        manifest_rows[key] = row['key']
    require(list(manifest_rows)==EXPECTED, 'manifest 83 ordered keys')
    project = json.loads((HERE/'../tilted-camera-source-join/project01.json').read_text())
    source_keys = {}
    for track_id, track_short, indices in [('pointmass05','PM05',list(range(150,403,6))),
                                           ('pointmass08','PM08',list(range(210,445,6)))]:
        tracks = [t for t in project['pointmass_tracks'] if t['track_id']==track_id]
        require(len(tracks)==1, 'source track count')
        track = tracks[0]
        require(len(track['framedata'])==len(track['keyFrames'])==1, 'source array count')
        rows = track['framedata'][0]['rows']
        keys = list(range(360,403,6)) if track_short=='PM05' else indices
        require([r['index'] for r in rows]==indices and track['keyFrames'][0]['values']==keys, 'source index/key membership')
        for row in rows:
            require(type(row['saved_keyFrame_member']) is bool and
                    row['saved_keyFrame_member']==(row['index'] in keys), 'source literal key flag')
            source_keys[row['index'],track_short] = row['saved_keyFrame_member']
    require(source_keys==manifest_rows, 'source/manifest key mismatch')
    root,root_views = parse_note('root-observations.md')
    observer,observer_views = parse_note('observer.md')
    for name,record in [('root',root),('observer',observer)]:
        require({k:v['key'] for k,v in record.items()}==source_keys, name+' source key mismatch')
    require([f['index'] for f in manifest['frames']]==SELECTION, 'manifest 50 ordered frames')
    panels = {}
    for frame in manifest['frames']:
        relative = f"panels/frame-{frame['index']:04d}.png"
        require(frame['panel_png']==relative, 'frame/panel path mapping')
        path = HERE/'run01'/relative
        actual = pin(path)
        require(actual==receipt['products'][relative], 'receipt panel pin')
        product = manifest['products'][relative]
        require(actual=={k:product[k] for k in ('bytes','sha256')}, 'manifest panel pin')
        require(root_views[relative]==observer_views[relative]==actual['sha256'], 'view panel pin')
        with path.open('rb') as handle:
            header = handle.read(24)
        require(header[:8]==b'\x89PNG\r\n\x1a\n' and header[12:16]==b'IHDR' and
                struct.unpack('>II',header[16:24])==(1128,648), 'PNG header geometry')
        panels[relative] = actual
    groups = {
        'all':EXPECTED, 'PM05':[k for k in EXPECTED if k[1]=='PM05'],
        'PM08':[k for k in EXPECTED if k[1]=='PM08'],
        'PM05_nonkeys':[k for k in EXPECTED if k[1]=='PM05' and not source_keys[k]],
        'PM05_keys':[k for k in EXPECTED if k[1]=='PM05' and source_keys[k]],
        'all_keys':[k for k in EXPECTED if source_keys[k]],
    }
    counts = {}
    for group,keys in groups.items():
        counts[group] = {'n':len(keys), **{axis:sum(root[k]['categories'][i]==observer[k]['categories'][i]
                         for k in keys) for i,axis in enumerate(AXES)},
                         'joint':sum(root[k]['categories']==observer[k]['categories'] for k in keys)}
    disagreements = []
    for k in EXPECTED:
        a,b = root[k]['categories'],observer[k]['categories']
        if a!=b:
            disagreements.append({'frame':k[0], 'track':k[1], 'key':source_keys[k],
                'root':a, 'observer':b, 'differing_axes':[axis for i,axis in enumerate(AXES) if a[i]!=b[i]],
                'root_reason':root[k]['reason'], 'observer_reason':observer[k]['reason']})
    pairs = {axis:{' / '.join(pair):count for pair,count in sorted(Counter(
                (root[k]['categories'][i],observer[k]['categories'][i]) for k in EXPECTED).items())}
             for i,axis in enumerate(AXES)}
    after = {name:pin(HERE/name) for name in PINS}
    require(before==after, 'frozen inputs changed during check')
    require(all(pin(HERE/'run01'/name)==value for name,value in panels.items()), 'panel bytes changed')
    print(json.dumps({'status':'PASS', 'python':platform.python_version(), 'script':pin(Path(__file__)),
          'pins_before':before, 'pins_after':after, 'frozen_inputs_unchanged':True,
          'source_manifest_observation_rows_each':83, 'view_log_entries_each':50,
          'all_50_panel_byte_pins_and_header_dimensions_match':True,
          'no_image_decode_or_view':True, 'agreement_counts':counts,
          'category_pair_counts':pairs, 'disagreement_rows':len(disagreements),
          'disagreements':disagreements},indent=2))


if __name__=='__main__':
    main()
