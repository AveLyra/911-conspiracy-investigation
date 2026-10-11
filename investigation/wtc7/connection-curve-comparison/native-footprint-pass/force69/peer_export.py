"""Bounded force69 peer export; manual selections only, no RGB selection."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE/'../force45/reader-F4-Im4-peer.py'
OLD_SHA = '919186992631e9f6176c2db6513521fdb6035aae6a30ec02e521cb69a15e1e0d'
PINS = {
    'PROTOCOL.md':'558eb117125fc3df1458e2c153e3a9635b67ed931df15e9114c26b507e209ff7',
    '../PROTOCOL.md':'2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json':'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../force45/reader-F4-Im4-peer.py':OLD_SHA,
    'read_context.py':'ee266545221eb4ed63faa04c59e48fbcd69571092621c38d3d57d84e67af6a90',
    'context01.json':'ac65b18cb58bbe1e7f003163e2b8dde55baddc4c1ef061655e202caef2820cb1',
    'context02.json':'ac65b18cb58bbe1e7f003163e2b8dde55baddc4c1ef061655e202caef2820cb1',
    '../../native-strips01/Im0.jpg':'b5b279bbdc7de4c0be4165ac9bc70086c736cdca557859460da35a4c3406f1d4',
    '../../native-strips01/Im1.jpg':'929f5d00d2f9ab1eba27a4aad8af37320a4fd37f2455f9b51d750ec7e15e8139',
    '../../native-strips01/Im2.jpg':'9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png':'0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}

def pin(path):
    b=path.read_bytes()
    return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

if pin(OLD)['sha256'] != OLD_SHA:
    raise ValueError('Frozen expansion helper changed')
spec=importlib.util.spec_from_file_location('force45_peer_representation',OLD)
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
expand,flags,union,require=old.expand,old.flags,old.union,old.require

def candidates(cfg,x,pieces):
    owners=cfg['unassigned_candidates'].get(x,[])
    require(owners==sorted(set(owners)) and set(owners)<= {'solid','dash'},'candidate routes')
    require(bool(pieces)==(x in cfg['unassigned_candidates']),'explicit ownership per material column')
    return owners

def coverage(cfg,context):
    rid=cfg['region_id']; cb=cfg['context']; src=cfg['source_image']
    target={(x,y):rgb for x,y,rgb in ((r['x'],r['y'],r['rgb']) for r in context['cells'][rid])}
    seen=set()
    for item in cfg['raw_blocks']:
        other=item['display_region']; x0,y0,x1,y1=item['box']
        require(context['sources'][other]==src,'reading source identity')
        ob=context['context_boxes'][other]
        require(ob[0]<=x0<x1<=ob[2] and ob[1]<=y0<y1<=ob[3],'display in context')
        require(item['untruncated'] is True and item['receipt'],'actual finite block receipt')
        for r in context['cells'][other]:
            p=(r['x'],r['y'])
            if x0<=p[0]<x1 and y0<=p[1]<y1 and p in target:
                require(r['rgb']==target[p],'reused overlap equality')
                seen.add(p)
    require(seen==set(target),'incomplete actual reader coverage')
    require(len(target)==(cb[2]-cb[0])*(cb[3]-cb[1]),'context count')
    return target

def build(cfg,script):
    before={name:pin(HERE/name) for name in PINS}
    require(all(before[k]['sha256']==v for k,v in PINS.items()),'frozen inputs changed')
    require((HERE/'context01.json').read_bytes()==(HERE/'context02.json').read_bytes(),'context repeat')
    context=json.loads((HERE/'context01.json').read_text())
    rid=cfg['region_id']; box=cfg['target']; cb=cfg['context']; x0,y0,x1,y1=box
    require(context['target_boxes'][rid]==box and context['context_boxes'][rid]==cb and context['sources'][rid]==cfg['source_image'],'region contract')
    px=coverage(cfg,context)
    prefix=rid+'-peer-'
    maps={k:expand(cfg[k],box,prefix) for k in ('solid','dash','unassigned')}
    require(set(cfg['unassigned_candidates'])==set(maps['unassigned']),'ownership coverage')
    routes={'solid':[],'dash':[]}; bands=[]
    for x in range(x0,x1):
        pieces=maps['unassigned'].get(x,[])
        uc,uf=union(pieces,'core'),union(pieces,'fringe')
        require(not pieces or uc+uf,'empty material band')
        owners=candidates(cfg,x,pieces)
        bid=prefix+'unassigned-'+str(x) if pieces else None
        band={'x':x,'core':uc,'fringe':uf,'status':'identity_conflict' if pieces else 'no_attributable_cells',
              'fragment_id':pieces[0]['fragment_id'] if len(pieces)==1 else None,
              'band_id':bid,'model':None,'candidate_routes':owners,'boundary_flags':flags(x,uc+uf,box),
              'note':cfg['unassigned_reasons'].get(x,'Inspected column; no unassigned cells selected, not a physical absence claim.'),
              'competing_identities':(['listed route edge or body','compression/background or another fragment'] if pieces else [])}
        if len(pieces)>1: band['fragments']=pieces
        bands.append(band)
        for route in ('solid','dash'):
            members=maps[route].get(x,[])
            core,fringe=union(members,'core'),union(members,'fringe')
            selected=core+fringe; boundary=flags(x,selected,box)
            refs=[{'band_id':bid,'x':x}] if route in owners else []
            status=(('boundary_truncated' if boundary else 'identified_local_fragment' if core else 'fringe_only') if selected else ('identity_conflict' if refs else 'no_attributable_cells'))
            record={'x':x,'core':core,'fringe':fringe,'status':status,
                    'fragment_id':members[0]['fragment_id'] if len(members)==1 else None,
                    'boundary_flags':boundary,'unassigned_band_refs':refs,
                    'note':('Local visible style attribution; fringe is tentative and not a calibrated bound. Selected crop-edge cells are flagged, not physical endpoints.' if selected else 'No model cells selected after actual inspection; empty does not imply zero, absence, or support across a gap.')}
            if len(members)>1: record['fragments']=members
            require(not set(selected)&set(uc+uf),'band/model duplicate')
            routes[route].append(record)
        require(not set(routes['solid'][-1]['core']+routes['solid'][-1]['fringe'])&set(routes['dash'][-1]['core']+routes['dash'][-1]['fringe']),'model duplicate')
    whites=[]; selected=0
    for route,rows in [*routes.items(),('unassigned',bands)]:
        for row in rows:
            for kind in ('core','fringe'):
                for y in row[kind]:
                    selected+=1
                    if px[row['x'],y]==[255,255,255]: whites.append([route,kind,row['x'],y])
    after={name:pin(HERE/name) for name in PINS}
    require(before==after,'changed during export')
    return {'pair':cfg['pair'],'region_id':rid,'reader':'peer','reader_identity':'force69_peer; separately frozen prior-informed AI reader',
            'source_image':cfg['source_image'],'status':'frozen_manual_native_annotation_not_accepted_measurement',
            'target_box':box,'context_box':cb,'inputs':before,'inputs_after':after,'script_pin':pin(Path(script)),'expander_pin':pin(Path(__file__)),
            'literal_manual_transcription':{k+'_runs_inclusive':cfg[k] for k in ('solid','dash','unassigned')},
            'coverage':{'full_native_strip_viewed':True,'full_composed_page_viewed':True,
                        'view_receipt':'force69_peer tool image view: original full Im0/Im1/Im2 741x88; full 1700x2200 composed page displayed at1376x1780. Native coordinates taken from numeric contexts only.',
                        'raw_blocks':cfg['raw_blocks'],'raw_context_cells':len(px),'all_blocks_untruncated':True,
                        'exact_white_omission_rule':'Only exact RGB (255,255,255) omitted; every other cell displayed and read.',
                        'overlap_reuse':'Only this reader own displayed cells on exactly equal pinned source positions may cover overlap; reuse is not new corroboration.',
                        'target_columns':x1-x0,'model_route_records':2*(x1-x0),'unassigned_band_records':x1-x0,
                        'uncompleted':'Outside fixed target; all physical coordinates, source-native bounds, support inventory, seams and human curve acceptance remain separate.'},
            'identity_basis':cfg['identity_basis'],'notes':cfg['notes'],
            'independence':'Prior-informed AI; plots and prior inventory known. No matching primary literal/output or discrepancy was inspected before this freeze. Old force45 helper reused only for expansion/flags/union, not old cell selections.',
            'limits':['Subjective visible ink, not calibrated mathematical curve containment.','Every unspecified route column is empty only after actual full context reading.','No detector, threshold, interpolation, RGB-based selection, physical ordinate or causal conclusion.'],
            'pre_freeze_transcription_checks':{'selected_cells_checked_for_exact_white':selected,'selected_exact_white_cells':whites,'post_export_corrections':[]},
            'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands}

def controls():
    n=old.controls()
    require(candidates({'unassigned_candidates':{2:['dash']}},2,[{'x':2}])==['dash'],'dash-only')
    require(candidates({'unassigned_candidates':{2:[]}},2,[{'x':2}])==[],'neither route')
    for c,p in [({'unassigned_candidates':{}},[1]),({'unassigned_candidates':{2:['bad']}},[1]),({'unassigned_candidates':{2:['solid','solid']}},[1])]:
        try: candidates(c,2,p)
        except ValueError: pass
        else: raise AssertionError('bad candidate ownership accepted')
    return n+5

def run(cfg,script):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--output',choices=['reader-'+cfg['region_id']+'-peer.json','reader-'+cfg['region_id']+'-peer-repeat.json'])
    args=parser.parse_args(); n=controls(); result=build(cfg,script)
    check=result['pre_freeze_transcription_checks']
    summary={'region_id':cfg['region_id'],'controls':n,'route_records':result['coverage']['model_route_records'],
             'selected_cells':check['selected_cells_checked_for_exact_white'],'selected_exact_white_cells':check['selected_exact_white_cells'],
             'script_pin':result['script_pin'],'expander_pin':result['expander_pin'],
             'status_counts':{k:dict(Counter(r['status'] for r in v)) for k,v in result['routes'].items()}}
    require(not check['selected_exact_white_cells'],'Exact-white transcription diagnostic; inspect and preserve rather than erase algorithmically.')
    if not args.check:
        require(args.output is not None,'output required')
        with (HERE/args.output).open('xb') as f: f.write((json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n').encode())
        summary['output_pin']=pin(HERE/args.output)
    print(json.dumps(summary,sort_keys=True))
