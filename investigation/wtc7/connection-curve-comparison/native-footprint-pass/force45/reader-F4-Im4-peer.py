"""Prior-informed peer F4-Im4 reading; literal expansion, never RGB selection."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    'PROTOCOL.md': '4df4510ba5664888124512ab052cfe535fce23dba482e5021cc69d4d0c47f285',
    '../PROTOCOL.md': '2066edbe4f36d4eeb8e3be1695fdd72fe32f9649d779ea897e5e63358cb4fdbd',
    '../REGIONS.json': 'ad6ec930f70e367028624bb3e497944147902b9817e5690e4980ea2ebeb2c131',
    '../read_context.py': 'da7d46400de924b75773646f34b7fba1d2284b50736d25395bb0a1c71e629c18',
    'read_context.py': 'cfce638b10df652fd8a8273603e9dee12c71952f567d4c1f534d6cd12e2b05ab',
    'context01.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    'context02.json': '161dfadf26fb6d7db86e83b025b208747a931bc83e4696830d1193dabd372fa4',
    '../../native-strips01/Im4.jpg': '53804060d00794d59628d6406337a6db5568bf30df63913ff4888b63082913fd',
    '../../native-strips01/Im2.jpg': '9f527c50ac92ef12454c550c66699773465cdc9aecfea55ca4130403166ae8e9',
    '../../render01/page-076.png': '0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6',
}
# Every entry is [inclusive first x, inclusive last x, explicit core rows,
# explicit fringe rows, reader-local piece ID]. Values are manual judgments.
SOLID_RUNS = [
    [331,331,[],[0,1],'s01'], [332,332,[],[0,1,2],'s01'],
    [333,333,[0,1],[2,3],'s01'], [334,334,[0,1,2],[3,4],'s01'],
    [335,335,[1,2,3],[0,4,5],'s01'], [336,336,[3,4],[2,5,6],'s01'],
    [337,337,[4,5,6],[3,7,8],'s01'], [338,338,[6,7],[5,8,9],'s01'],
    [339,339,[7,8,9],[6,10,11],'s01'], [340,340,[8,9,10],[7,11,12],'s01'],
    [341,341,[10,11,12],[9,13,14],'s01'], [342,342,[11,12,13],[10,14,15],'s01'],
    [343,343,[13,14,15],[12,16,17],'s01'], [344,344,[14,15,16],[13,17,18],'s01'],
    [345,345,[16,17,18],[14,15,19,20],'s01'], [346,346,[17,18,19],[16,20,21],'s01'],
    [347,347,[19,20,21],[18,22,23],'s01'], [348,348,[20,21,22],[19,23,24],'s01'],
    [349,349,[22,23,24],[21,25,26],'s01'], [350,350,[23,24,25],[22,26,27],'s01'],
    [351,351,[25,26,27],[24,28,29],'s01'], [352,352,[26,27,28],[25,29,30],'s01'],
    [353,353,[28,29,30],[26,27,31,32],'s01'], [354,354,[29,30,31],[28,32,33],'s01'],
    [355,355,[31,32,33],[30,34,35],'s01'], [356,356,[33,34,35],[31,32,36,37],'s01'],
    [357,357,[34,35,36],[33,37,38],'s01'], [358,358,[35,36,37],[34,38,39,40],'s01'],
    [359,359,[37,38,39],[36,40,41],'s01'], [360,360,[38,39,40,41],[37,42,43],'s01'],
    [361,361,[40,41,42],[39,43,44],'s01'], [362,362,[42,43,44],[41,45,46],'s01'],
    [363,363,[43,44,45],[42,46,47],'s01'], [364,364,[45,46,47],[44,48,49],'s01'],
    [365,365,[46,47,48],[45,49,50,51],'s01'], [366,366,[48,49,50],[47,51,52,53],'s01'],
    [367,367,[49,50,51,52],[48,53,54],'s01'], [368,368,[51,52,53],[50,54,55],'s01'],
    [369,369,[53,54,55],[52,56,57],'s01'], [370,370,[54,55,56],[53,57,58],'s01'],
    [371,371,[55,56,57],[54,58,59],'s01'], [372,372,[56,57,58],[55,59,60],'s01'],
    [373,373,[57,58,59,60],[56,61,62],'s01'], [374,374,[59,60,61],[58,62,63],'s01'],
    [375,375,[60,61,62],[59,63,64],'s01'], [376,376,[61,62,63],[60,64,65],'s01'],
    [377,377,[62,63,64],[61,65,66],'s01'], [378,378,[63,64,65],[62,66,67],'s01'],
    [379,379,[64,65,66],[63,67,68],'s01'], [380,380,[65,66,67],[64,68,69],'s01'],
    [381,381,[67,68,69],[66,70,71],'s01'], [382,382,[68,69,70],[67,71,72],'s01'],
    [383,383,[69,70,71],[68,72,73],'s01'], [384,384,[70,71,72],[69,73,74],'s01'],
    [385,385,[72,73,74],[70,71,75,76],'s01'], [386,386,[73,74,75],[72,76,77],'s01'],
    [387,387,[74,75,76],[73,77,78],'s01'], [388,388,[75,76,77],[74,78,79],'s01'],
    [389,389,[76,77,78],[75,79,80],'s01'], [390,390,[78,79],[77,80,81],'s01'],
    [391,391,[79,80,81],[78,82,83],'s01'], [392,392,[80,81,82],[79,83,84],'s01'],
    [393,393,[81,82,83],[80,84,85],'s01'], [394,394,[82,83,84],[81,85,86],'s01'],
    [395,395,[83,84,85],[82,86,87],'s01'], [396,396,[85,86],[84,87],'s01'],
    [397,397,[85,86,87],[84],'s01'], [398,398,[86,87],[85],'s01'],
    [399,399,[87],[86],'s01'],
]
DASH_RUNS = [
    [356,356,[3,4],[2,5],'d01'], [357,357,[3,4,5],[2,6,7],'d01'],
    [358,358,[4,5],[3,6,7],'d01'], [359,359,[5,6],[4,7,8],'d01'],
    [360,360,[6],[5,7,8],'d01'], [361,361,[6,7],[5,8],'d01'],
    [362,362,[],[10,11,12,13,14],'d02'], [363,363,[11,12,13,14,15],[10,16,17],'d02'],
    [364,364,[15,16],[13,14,17],'d02'],
    [365,365,[19,20,21,22],[18,23,24],'d03'], [366,366,[21,22,23,24],[20,25,26],'d03'],
    [367,367,[24,25],[22,23,26],'d03'], [368,368,[],[24,25,26],'d03'],
    [369,369,[],[28,29,30,31],'d04'], [370,370,[28,29,30,31],[27,32,33],'d04'],
    [371,371,[29,30,31,32,33],[28,34,35],'d04'], [372,372,[32,33,34],[30,31,35],'d04'],
    [373,373,[37,38,39,40],[36,41,42],'d05'], [374,374,[39,40,41,42],[38,43,44],'d05'],
    [375,375,[41,42,43],[40,44,45],'d05'], [376,376,[42,43],[41,44],'d05'],
    [377,377,[],[42,43],'d05'],
    [379,379,[],[42,43,44],'d06'], [380,380,[42,43,44,45],[41,46,47],'d06'],
    [381,381,[44,45,46,47],[43,48],'d06'], [382,382,[47],[46,48,49],'d06'],
    [383,383,[51,52],[50,53],'d07'], [384,384,[51,52],[50,53],'d07'],
    [385,385,[51,52],[50,53],'d07'], [386,386,[51,52],[50,53],'d07'],
    [387,387,[50,51,52],[49,53],'d07'], [388,388,[51,52],[50,53],'d07'],
    [389,389,[],[51,52,53],'d07'],
    [390,390,[55,56,57,58,59],[54,60,61],'d08'], [391,391,[58,59,60,61],[57,62],'d08'],
    [392,392,[61],[60,62],'d08'],
    [395,395,[61],[60,62,63],'d09'], [396,396,[61,62],[60,63,64],'d09'],
    [397,397,[61,62,63,64,65],[60,66,67],'d09'], [398,398,[63,64,65,66],[62,67,68],'d09'],
    [399,399,[69,70,71],[68,72],'d10'], [400,400,[70,71,72],[69,73,74],'d10'],
    [401,401,[72],[70,71,73,74],'d10'], [402,402,[72],[71,73,74],'d10'],
    [403,403,[71,72],[70,73],'d10'], [404,404,[71],[70,72,73],'d10'],
    [405,405,[],[74,75],'d11'], [406,406,[74,75,76,77],[73,78,79],'d11'],
    [407,407,[75,76,77,78,79],[74,80],'d11'], [408,408,[78,79,80],[77,81],'d11'],
    [409,409,[],[80],'d11'],
    [410,410,[82,83],[81,84],'d12'], [411,411,[82,83],[81,84],'d12'],
    [412,412,[82,83],[81,84],'d12'], [413,413,[82,83],[81,84,85],'d12'],
    [414,414,[82,83,84,85],[81,86],'d12'], [415,415,[],[83,84,85],'d12'],
]
UNASSIGNED_RUNS = [
    [355,355,[],[1,2,3,4,5],'u-start'],
    [378,378,[],[42,43,44,45],'u-dashgap'],
    [393,393,[],[58,59,60,61],'u-dashgap2'],
    [394,394,[],[60,61,62,63],'u-dashgap2'],
]
RAW_BLOCKS = [
    [328,347,'c22fee',3459], [348,367,'0d8b51',4685],
    [368,387,'7506e6',5878], [388,407,'ee98ee',5909], [408,426,'bb4c9c',4839],
]
CONFIG = {
    'pair': 'F4', 'region_id': 'F4-Im4', 'source_image': 'Im4.jpg',
    'target': [330,0,425,88], 'context': [328,0,427,88],
    'solid': SOLID_RUNS, 'dash': DASH_RUNS, 'unassigned': UNASSIGNED_RUNS,
    'raw_blocks': RAW_BLOCKS, 'view_receipt': 'Image call accompanying b57d6b; full Im4 original 741x88, complete page resized1700x2200 to1376x1780.',
    'identity_basis': 'Gold continuous descending stroke and separate gold broken bodies are visible in the unchanged strip; confirmed page legend identifies four bolts, solid Spring and dashed Shell. Fragment IDs are local only and do not bridge gaps.',
    'notes': 'Selected pale interbody/start material stays unassigned where attribution is uncertain. Other background/compression and differently colored strokes are not target curves. The continuous stroke exits the bottom of this source; the crop edge is not a physical endpoint.',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def flags(x, rows, box):
    x0,y0,x1,y1 = box
    return ([v for v, ok in [('target_left',x == x0),('target_right',x == x1-1),
            ('target_top',y0 in rows),('target_bottom',y1-1 in rows)] if ok] if rows else [])


def expand(runs, box, prefix):
    x0,y0,x1,y1 = box
    result = {}
    for first,last,core,fringe,fragment in runs:
        require(type(first) is int and type(last) is int and x0 <= first <= last < x1, 'literal x')
        for rows in (core,fringe):
            require(type(rows) is list and rows == sorted(set(rows)), 'sorted unique rows')
            require(all(type(y) is int and y0 <= y < y1 for y in rows), 'literal y')
        require(not set(core)&set(fringe), 'disjoint classes')
        require(isinstance(fragment,str) and fragment, 'fragment identity')
        for x in range(first,last+1):
            pieces = result.setdefault(x, [])
            require(all(p['fragment_id'] != prefix+fragment for p in pieces), 'duplicate piece in column')
            require(not set(core+fringe)&set(y for p in pieces for k in ('core','fringe') for y in p[k]), 'overlapping pieces')
            pieces.append({'fragment_id':prefix+fragment,'core':list(core),'fringe':list(fringe)})
    return result


def union(pieces, key):
    return sorted({y for p in pieces for y in p[key]})


def build(cfg, script):
    before = {name:pin(HERE/name) for name in PINS}
    require(all(before[k]['sha256'] == v for k,v in PINS.items()), 'frozen input changed')
    require((HERE/'context01.json').read_bytes() == (HERE/'context02.json').read_bytes(), 'context repeat')
    box = cfg['target']; x0,y0,x1,y1 = box
    prefix = cfg['region_id']+'-peer-'
    maps = {k:expand(cfg[k],box,prefix) for k in ('solid','dash','unassigned')}
    routes = {'solid':[],'dash':[]}; bands = []
    for x in range(x0,x1):
        pieces = maps['unassigned'].get(x,[])
        uc,uf = union(pieces,'core'),union(pieces,'fringe')
        bid = prefix+'unassigned-'+str(x) if pieces else None
        band = {'x':x,'core':uc,'fringe':uf,'status':'identity_conflict' if pieces else 'no_attributable_cells',
                'fragment_id':pieces[0]['fragment_id'] if len(pieces)==1 else None,
                'band_id':bid,'model':None,'boundary_flags':flags(x,uc+uf,box),
                'note':'Selected unresolved ink retained once; no model identity.' if pieces else 'Inspected column with no selected unassigned cells; not proof of absent material.',
                'competing_identities':['nearby stroke edge','compression or background material'] if pieces else []}
        if len(pieces)>1:
            band['fragments']=pieces
        bands.append(band)
        refs = [{'band_id':bid,'x':x}] if pieces else []
        for route in ('solid','dash'):
            members = maps[route].get(x,[])
            core,fringe = union(members,'core'),union(members,'fringe')
            selected=core+fringe; boundary=flags(x,selected,box)
            status = ('boundary_truncated' if boundary else 'identified_local_fragment' if core else 'fringe_only') if selected else ('identity_conflict' if refs else 'no_attributable_cells')
            record={'x':x,'core':core,'fringe':fringe,'status':status,
                    'fragment_id':members[0]['fragment_id'] if len(members)==1 else None,
                    'boundary_flags':boundary,'unassigned_band_refs':refs,
                    'note':('Local visible style attribution; fringe is tentative, not a calibrated bound. Boundary flags denote selected cells at crop edges, not physical endpoints.' if selected else 'No attributable model cells selected after inspection; empty does not establish absence, zero or a bridged gap.')}
            if len(members)>1:
                record['fragments']=members
            require(not set(selected)&set(uc+uf),'unassigned duplicate')
            routes[route].append(record)
        require(not set(routes['solid'][-1]['core']+routes['solid'][-1]['fringe'])&set(routes['dash'][-1]['core']+routes['dash'][-1]['fringe']),'model duplicate')
    context=json.loads((HERE/'context01.json').read_text())
    rid=cfg['region_id']; cb=cfg['context']
    require(context['target_boxes'][rid]==box and context['context_boxes'][rid]==cb and context['sources'][rid]==cfg['source_image'],'region source contract')
    px={(r['x'],r['y']):r['rgb'] for r in context['cells'][rid]}
    require(len(px)==len(context['cells'][rid])==(cb[2]-cb[0])*(cb[3]-cb[1]),'context cardinality')
    require(set(px)=={(x,y) for x in range(cb[0],cb[2]) for y in range(cb[1],cb[3])},'context coverage')
    require([x for a,b,_,_ in cfg['raw_blocks'] for x in range(a,b+1)]==list(range(cb[0],cb[2])),'actual read coverage')
    whites=[]; count=0
    for scope,records in list(routes.items())+[('unassigned',bands)]:
        for row in records:
            for key in ('core','fringe'):
                for y in row[key]:
                    count+=1
                    if px[row['x'],y]==[255,255,255]:
                        whites.append({'scope':scope,'class':key,'x':row['x'],'y':y})
    after={name:pin(HERE/name) for name in PINS}
    require(before==after,'input changed during expansion')
    return {
        'pair':cfg['pair'],'region_id':rid,'source_image':cfg['source_image'],'reader':'peer',
        'reader_identity':'force45_peer; separately frozen prior-informed AI source reader',
        'status':'frozen_manual_native_annotation_not_accepted_measurement',
        'target_box':box,'context_box':cb,'inputs':before,'inputs_after':after,
        'script_pin':pin(Path(script)),'expander_pin':pin(Path(__file__)),
        'literal_manual_transcription':{k+'_runs_inclusive':cfg[k] for k in ('solid','dash','unassigned')},
        'coverage':{'full_native_strip_viewed':True,'full_composed_page_viewed':True,'view_receipt':cfg['view_receipt'],
                    'raw_blocks':cfg['raw_blocks'],'raw_rows_inclusive':[cb[1],cb[3]-1],
                    'raw_context_cells':len(px),'all_blocks_untruncated':True,
                    'exact_white_omission_rule':'Only RGB255,255,255 omitted; all other context values displayed and read.',
                    'target_columns':x1-x0,'model_route_records':2*(x1-x0),'unassigned_band_records':x1-x0,
                    'uncompleted':'Outside fixed region, cross-strip identities, physical ordinate/support recovery, calibration and human acceptance.'},
        'identity_basis':cfg['identity_basis'],'notes':cfg['notes'],
        'independence':'Same-source prior-informed AI; complete plot/prior inventory known. No matching-region primary annotation or discrepancy was read before this freeze. Not blind historical independence, human review or expert certification. Own prior peer script used for representation design.',
        'limits':['Core/fringe are subjective visible ink, not mathematical-curve containment or confidence intervals.',
                  'Missing and explicit empty remain different. Each target column was inspected; unspecified literal routes expand to explicit empty only after actual complete reading.',
                  'Fragment membership does not bridge dash gaps, seams, hidden portions or physical endpoints.',
                  'No RGB threshold, detector, fit, interpolation, physical metric, causal finding, acceptance or source editing.'],
        'pre_freeze_transcription_checks':{'selected_cells_checked_for_exact_white':count,'selected_exact_white_cells':whites,'post_export_corrections':[]},
        'human_accepted':False,'physical_support':None,'routes':routes,'unassigned_bands':bands,
    }


def controls():
    b=[2,3,5,7]
    require(flags(2,[],b)==[],'empty boundary')
    require(flags(2,[3,6],b)==['target_left','target_top','target_bottom'],'corner boundary')
    require(flags(4,[4],b)==['target_right'],'right boundary')
    require(flags(3,[4],b)==[],'interior boundary')
    m=expand([[2,2,[3],[4],'a'],[2,2,[6],[],'b']],b,'p-')
    require(union(m[2],'core')==[3,6] and union(m[2],'fringe')==[4],'multiple membership union')
    for bad in ([[True,2,[3],[],'a']],[[2,2,[3],[3],'a']],[[2,2,[7],[],'a']],[[2,2,[3],[],'a'],[2,2,[3],[],'b']]):
        try:
            expand(bad,b,'p-')
        except ValueError:
            pass
        else:
            raise AssertionError('invalid literal accepted')
    return 9


def run(cfg,script):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--output',choices=['reader-'+cfg['region_id']+'-peer.json','reader-'+cfg['region_id']+'-peer-repeat.json'])
    args=parser.parse_args(); n=controls(); result=build(cfg,script)
    check=result['pre_freeze_transcription_checks']
    summary={'region_id':cfg['region_id'],'controls':n,'route_records':result['coverage']['model_route_records'],
             'selected_cells':check['selected_cells_checked_for_exact_white'],'selected_exact_white_cells':check['selected_exact_white_cells'],
             'script_pin':result['script_pin'],'status_counts':{k:dict(Counter(r['status'] for r in rows)) for k,rows in result['routes'].items()}}
    if args.check:
        print(json.dumps(summary,sort_keys=True))
        require(not check['selected_exact_white_cells'],'preserve and inspect exact-white transcription issue')
        return
    require(args.output is not None,'output required')
    require(not check['selected_exact_white_cells'],'preserve and inspect exact-white transcription issue')
    with (HERE/args.output).open('xb') as f:
        f.write((json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n').encode())
    summary['output_pin']=pin(HERE/args.output)
    print(json.dumps(summary,sort_keys=True))


if __name__ == '__main__':
    run(CONFIG,__file__)
