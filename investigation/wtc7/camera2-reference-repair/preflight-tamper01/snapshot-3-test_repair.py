"""Synthetic wrapper controls for the one-reference repair."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import numpy as np

sys.dont_write_bytecode = True
import repair


def check(value,label):
    if not value:
        raise AssertionError(label)


def tests(out):
    out.mkdir(parents=True,exist_ok=False)
    procedure = [Path(__file__),Path(repair.__file__),repair.HERE/'PROTOCOL.md',repair.PRIOR/'measure.py']
    initial = {str(p):repair.fp(p) for p in procedure}
    for p in procedure:
        (out/p.name).write_bytes(p.read_bytes())
    results = []
    def case(name,fn):
        try:
            detail=fn()
            results.append({'name':name,'status':'pass','detail':detail})
        except Exception as error:
            results.append({'name':name,'status':'fail','type':type(error).__name__,'message':str(error)})
    def selection():
        candidates=[{'id':f'C2-R{i}'} for i in (7,8,9)]
        visual={'candidate_acceptance':{c['id']:True for c in candidates}}
        records=[{'reference':c['id'],'half':half,'status':'candidate'} for c in candidates for half in (9,13)]
        check(repair.selected_id(candidates,visual,records)=='C2-R7','ordered first passing')
        records[0]['status']='rejected'
        check(repair.selected_id(candidates,visual,records)=='C2-R8','both sizes necessary')
        visual['candidate_acceptance']['C2-R8']=False
        check(repair.selected_id(candidates,visual,records)=='C2-R9','visual gate necessary')
        records[-1]['status']='rejected'
        check(repair.selected_id(candidates,visual,records) is None,'bounded no-candidate failure')
        try:
            repair.selected_id(candidates,visual,records[:-1])
        except ValueError as error:
            check(str(error)=='preflight-size-coverage','wrong missing-size failure')
        else:
            raise AssertionError('missing size accepted')
        return {'situations_checked':5}
    case('selection_order_both_sizes_visual_and_missing_gate',selection)
    def selection_contract():
        candidates=[{'id':f'C2-R{i}','xy':[i*10,50],'description':'synthetic'} for i in (7,8)]
        visual={'candidate_acceptance':{c['id']:True for c in candidates}}
        records=[{'reference':c['id'],'half':half,'status':'candidate'} for c in candidates for half in (9,13)]
        prior=[{'id':f'C2-R{i}','xy':[i*10,20]} for i in range(1,7)]
        selected={'status':'selected_baseline_only_not_validated_track','selected':'C2-R7','half_widths':[9,13],
                  'radius':24,'features':[candidates[0] if f['id']=='C2-R3' else f for f in prior]}
        repair.validate_selection(selected,candidates,visual,records,prior)
        variants=[]
        bad=deepcopy(selected);bad['features'][2]['xy'][0]+=1;variants.append((bad,'exact-approved-reference-set'))
        bad=deepcopy(selected);bad['features'][2]['id']='C2-R9';variants.append((bad,'exact-approved-reference-set'))
        bad=deepcopy(selected);bad['selected']='C2-R8';bad['features'][2]=candidates[1];variants.append((bad,'first-qualified-selection'))
        bad=deepcopy(selected);bad['radius']=25;variants.append((bad,'preflight-method'))
        bad=deepcopy(selected);bad['half_widths']=[13];variants.append((bad,'preflight-method'))
        bad=deepcopy(selected);bad['features'][0]['xy'][1]+=1;variants.append((bad,'exact-approved-reference-set'))
        for value,expected in variants:
            try:
                repair.validate_selection(value,candidates,visual,records,prior)
            except ValueError as error:
                check(str(error)==expected,'wrong selection-contract failure')
            else:
                raise AssertionError('tampered selection accepted')
        return {'valid_selection':1,'rejected_mutations':len(variants)}
    case('exact_selection_contract_rejects_internally_rehashed_mutations',selection_contract)
    def frame():
        module=repair.numerical_module()
        rng=np.random.default_rng(11673)
        baseline=rng.integers(20,220,size=(200,220),dtype=np.uint8)
        points=[[45,45],[105,45],[170,45],[45,145],[105,145],[170,145]]
        features=[{'id':f'SYNTH-{i}','xy':xy} for i,xy in enumerate(points)]
        templates=repair.template_arrays(baseline,features)
        stamp={'frame_index_zero_based':2,'source_pts':2002,'source_time_base':'1/30000','source_time_seconds_exact':'1001/15000'}
        moved=np.roll(np.roll(baseline,4,axis=0),-3,axis=1)
        rows,models,grids=repair.frame_analysis(module,features,templates,moved,stamp)
        check((len(rows),len(models),len(grids))==(12,6,12),'full image coverage')
        check(all(r['status']=='candidate' and r['candidate_xy']==[r['baseline_xy'][0]-3,r['baseline_xy'][1]+4] for r in rows),'known matched shift')
        check(all(m['passes_consistency_screen'] and np.allclose(m['offset'],[-3,4],atol=1e-9) for m in models),'known wrapper fits')
        bad=moved.copy(); bad[8:83,8:83]=100
        rejected,fails,badgrids=repair.frame_analysis(module,features,templates,bad,stamp)
        check(all(m['status']=='reference_quality_failure' and m['failed_references']==['SYNTH-0'] for m in fails),'one failed reference blocks every model')
        check(len(rejected)==12 and len(badgrids)==12,'rejections retain full candidates')
        repair.save(out/'synthetic-match-rows.json',rows)
        repair.save(out/'synthetic-fit-rows.json',models)
        repair.save(out/'synthetic-rejected-rows.json',rejected)
        repair.save(out/'synthetic-rejected-fits.json',fails)
        np.savez_compressed(out/'synthetic-grids.npz',**grids)
        np.savez_compressed(out/'synthetic-rejected-grids.npz',**badgrids)
        return {'matched_rows':12,'fit_rows':6,'one_failure_rejects_models':6}
    case('actual_frame_wrapper_and_single_failure',frame)
    def preservation():
        target=out/'exclusive.json'
        repair.save(target,{'synthetic':True})
        before=repair.fp(target)
        try:
            repair.save(target,{'replacement':True})
        except FileExistsError:
            pass
        else:
            raise AssertionError('save overwrote prior output')
        check(repair.fp(target)==before,'exclusive save unchanged')
        try:
            repair.execute('prepare',out)
        except FileExistsError:
            pass
        else:
            raise AssertionError('stage overwrote prior directory')
        check(repair.fp(target)==before,'stage refusal unchanged')
        return 'both overwrite guards reject'
    case('existing_outputs_preserved',preservation)
    check(all(repair.fp(Path(p))==identity for p,identity in initial.items()),'procedure changed')
    result={'scope':'synthetic repair-wrapper controls, not historical or physical validation','pins':initial,
        'python':sys.version,'numpy':np.__version__,'tests':results,
        'passed':sum(r['status']=='pass' for r in results),'failed':sum(r['status']=='fail' for r in results),
        'products':{p.name:repair.fp(p) for p in sorted(out.iterdir()) if p.is_file()}}
    repair.save(out/'receipt.json',result)
    print(json.dumps({'passed':result['passed'],'failed':result['failed'],'failures':[r for r in results if r['status']=='fail']}))
    return result['failed']


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    sys.exit(bool(tests(parser.parse_args().out)))
