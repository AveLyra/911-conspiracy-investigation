"""Exact, explicit schema crosswalk between independently frozen transcriptions."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PINS = {
 'transcription-root/table47.json': 'a84e456e59cf0e84327b11ff803738bbc5c0263fde92e27abd428be1feada0bc',
 'transcription-root/table50.json': '2abee8fed8d2d1f7f75b55ec5d0699c3808fd414b39e39865db164fbace2032a',
 'transcription-independent/table47.json': 'fe5e566dff8cbff6aa80a00656820504b2542bc5468eef96eb9911d5e4aea2f8',
 'transcription-independent/table50.json': '9af054e9730915e35a429f2d846f3450120ea19b41a7c166b917b8f82e643c34',
}


def reconcile():
    for path, pin in PINS.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == pin, path
    results = []
    for page in [47,50]:
        a = json.loads((ROOT/f'transcription-root/table{page}.json').read_text())
        b = json.loads((ROOT/f'transcription-independent/table{page}.json').read_text())
        if page == 47:
            mapping = {'time_s':'time_s','ref_x':'ref_building_x','ref_y':'ref_building_y'}
            for short,long in [('ne','ne_corner'),('ec','ec_roofline'),('wc','wc_roofline'),('nw','nw_corner')]:
                mapping.update({short+'_'+suffix:long+'_'+suffix for suffix in ['y','v']})
        else:
            mapping = {k:k for k in a['columns']}
            mapping.update({'ref_y':'reference_point_y','nw_y':'nw_corner_y','nw_relative_y':'nw_corner_relative_y',
                            'sw_y':'sw_corner_y','sw_relative_y':'sw_corner_relative_y','sw_adjusted_y':'sw_corner_adjusted_y'})
        assert set(mapping) == set(a['columns'])
        assert len(a['rows']) == len(b['rows']) == (70 if page == 47 else 25)
        differences = []
        nonnull = 0
        for ar,br in zip(a['rows'],b['rows']):
            assert ar['row'] == br['source_row']
            for key,alias in mapping.items():
                nonnull += ar[key] is not None
                if ar[key] != br[alias]:
                    differences.append({'row':ar['row'],'column':key,'root':ar[key],'independent':br[alias]})
        results.append({'page':page,'rows':len(a['rows']),'columns':len(mapping),'numeric_tokens':nonnull,
                        'nulls':len(a['rows'])*len(mapping)-nonnull,'differences':differences,'mapping':mapping})
    return {'status':'exact_agreement' if all(not r['differences'] for r in results) else 'disagreement',
            'pins':PINS,'pages':results,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    result=reconcile()
    with (ROOT/'reconciliation.json').open('x') as f:
        json.dump(result,f,indent=2,allow_nan=False); f.write('\n')
    print(json.dumps({'status':result['status'],'pages':[{k:v for k,v in r.items() if k!='mapping'} for r in result['pages']]}))
    assert result['status']=='exact_agreement'
