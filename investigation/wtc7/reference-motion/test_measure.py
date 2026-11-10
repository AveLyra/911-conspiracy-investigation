"""Root synthetic controls; all generated scenes are explicitly nonhistorical."""
import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
import measure as subject

HERE = Path(__file__).resolve().parent
POINTS = [[40,40],[100,35],[150,40],[40,120],[95,125],[150,120]]


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def dump(path, value):
    path.write_text(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n')


def rejected(callback, expected):
    try:
        callback()
    except ValueError as error:
        check(str(error)==expected, 'wrong failure: '+str(error))
        return
    raise AssertionError('invalid input accepted')


def fixture(root):
    """Two cameras, exact shift, then one reference removed: no real source read."""
    root.mkdir(parents=True,exist_ok=False)
    base = root/'multiview-onset-review'
    here = root/'method'
    here.mkdir()
    config = {'half_widths':[9,13],'radius':24}
    refinement = {'rules':{}}
    rng = np.random.default_rng(39171)
    native = rng.integers(30,200,size=(180,200),dtype=np.uint8)
    moved = np.roll(np.roll(native,2,axis=0),3,axis=1)
    one_missing = moved.copy()
    # Blank the entire search support for the first reference only.
    one_missing[3:78,3:78] = 90
    source = root/'synthetic-source.bin'
    source.write_bytes(b'SYNTHETIC ONLY: deterministic fixture; not historical media.\n')
    for camera in ('camera2','camera4'):
        config[camera] = [{'id':camera+'-R'+str(i+1),'xy':xy} for i,xy in enumerate(POINTS)]
        target = base/'refine01'/camera
        target.mkdir(parents=True)
        rows = []
        for index,array in enumerate([native,moved,one_missing]):
            png = target/f'f{index:06d}.png'
            Image.fromarray(array).save(png)
            rows.append({'frame_index_zero_based':index,'png':png.name,'png_identity':subject.fp(png),
                'luma_sha256':subject.sha(array.tobytes()),'source_pts':index*1001,
                'source_time_base':'1/30000','source_time_seconds_exact':str(subject.Fraction(index*1001,30000))})
        dump(target/'selection.json',{'geometry':[200,180],'images':rows,
            'input_pins':{'synthetic-source.bin':subject.fp(source)}})
        refinement['rules'][camera] = {'groups':{'event':[0,1,2]}}
    dump(base/'refinement.json',refinement)
    dump(base/'refine01/receipt.json',{'scope':'SYNTHETIC ONLY'})
    dump(here/'features.json',config)
    (here/'PROTOCOL.md').write_text('Synthetic fixture for wrapper and integrity controls; no historical content.\n')
    (here/'test_measure.py').write_bytes(Path(__file__).read_bytes())
    pins = {p:subject.fp(p)['sha256'] for p in [base/'refinement.json',base/'refine01/receipt.json',
        base/'refine01/camera2/selection.json',base/'refine01/camera4/selection.json']}
    return config, {'ROOT':root,'BASE':base,'HERE':here,'PINS':pins,
                    'EVALUATION':{'camera2':[1,2],'camera4':[1,2]}}


def suite(out):
    out.mkdir(parents=True,exist_ok=False)
    sources = [Path(__file__),HERE/'measure.py',HERE/'PROTOCOL.md',HERE/'features.json']
    pins = {str(p):subject.fp(p) for p in sources}
    for p in sources:
        (out/p.name).write_bytes(p.read_bytes())
    results = []

    def case(name, callback):
        try:
            detail = callback()
            results.append({'name':name,'status':'pass','detail':detail})
        except Exception as error:
            results.append({'name':name,'status':'fail','error_type':type(error).__name__,'error':str(error)})

    def actual_matching():
        rng = np.random.default_rng(7101)
        base = rng.integers(20,100,size=(120,140),dtype=np.uint8)*2
        checks = []
        for half in (9,13):
            seed = base[60-half:61+half,70-half:71+half].copy()
            image = np.roll(np.roll(base//2+30,-8,axis=0),11,axis=1)
            result,grid = subject.match(image,seed,[70,60])
            check(result['status']=='candidate' and result['candidate_xy']==[81,52],'shift and gain')
            check(abs(result['ncc']-1)<1e-11 and grid.shape==(49,49),'score and grid')
            checks.append({'half':half,'coordinate':result['candidate_xy'],'ncc':result['ncc']})
        return checks
    case('integer_matching_with_positive_gain_and_offset',actual_matching)

    def point_maps():
        p = np.array(POINTS,float)
        details = []
        for model,matrix in [('translation',np.eye(2)),('similarity',np.array([[.9,-.3],[.3,.9]])),
                             ('affine',np.array([[1.1,.2],[-.1,.85]]))]:
            offset = np.array([7.,-11.])
            result = subject.fit_with_loo(p,p@matrix.T+offset,model)
            check(result['passes_consistency_screen'],'exact map acceptance')
            check(np.max(np.abs(np.array(result['matrix'])-matrix))<1e-10,'known map matrix')
            check(np.max(np.abs(np.array(result['offset'])-offset))<1e-9,'known map offset')
            details.append({'model':model,'maximum_loo':result['max_loo_error']})
        q = p.copy()
        q[-1] += [9,12]
        result = subject.fit_with_loo(p,q,'translation')
        check(not result['passes_consistency_screen'],'nonrigidity rejected')
        check(np.allclose([r['error_norm'] for r in result['leave_one_out']],[3]*5+[15]),'analytic LOO errors')
        return details
    case('known_point_maps_and_nonrigid_reference',point_maps)

    def full_wrapper():
        config,bindings = fixture(out/'wrapper-fixture')
        with patch.multiple(subject,**bindings):
            groups,inputs = subject.load_inputs(config)
            check(len(groups)==2 and all(len(v[0])==3 for v in groups.values()),'complete input loading')
            for name in ('run01','run02'):
                with redirect_stdout(io.StringIO()):
                    subject.run(out/'wrapper-fixture'/name)
            run1,run2 = [out/'wrapper-fixture'/name for name in ('run01','run02')]
            matches = json.loads((run1/'matches.json').read_text())
            models = json.loads((run1/'transforms.json').read_text())
            check(len(matches)==72 and len(models)==36,'full wrapper row counts')
            with np.load(run1/'score-grids.npz',allow_pickle=False) as grids:
                check(len(grids.files)==72,'all grids retained')
                for row in matches:
                    x,y = row['baseline_xy']
                    half = row['half']
                    expected_bounds = [max(half,x-24),min(199-half,x+24),
                                       max(half,y-24),min(179-half,y+24)]
                    check(row['search_bounds']==expected_bounds,'grid bounds')
                    x0,x1,y0,y1 = expected_bounds
                    check(grids[row['score_grid']].shape==(y1-y0+1,x1-x0+1),'grid support')
            for row in models:
                if row['index']<2:
                    check(row['status']=='computed' and row['passes_consistency_screen'],'valid model admission')
                    check(np.allclose(row['offset'],[0,0] if row['index']==0 else [3,2],atol=1e-9),'wrapper displacement')
                else:
                    check(row['status']=='reference_quality_failure' and not row['passes_consistency_screen'],'one missing prevents all models')
                    check(len(row['failed_references'])==1,'fixture loses exactly one reference')
            product_names = sorted(p.name for p in run1.iterdir())
            check(product_names==sorted(p.name for p in run2.iterdir()),'repeat file membership')
            check(all(subject.fp(run1/n)==subject.fp(run2/n) for n in product_names),'all repeat bytes')
            before = {n:subject.fp(run1/n) for n in product_names}
            try:
                subject.run(run1)
            except FileExistsError:
                pass
            else:
                raise AssertionError('overwrite allowed')
            check(before=={n:subject.fp(run1/n) for n in product_names},'overwrite refusal changes nothing')
            receipt = json.loads((run1/'receipt.json').read_text())
            check(all(subject.fp(run1/n)==pin for n,pin in receipt['products'].items()),'receipt inventory')
            check(len(list(run1.glob('overlay-*.png')))==12,'fixed sample overlays')
            for png in run1.glob('overlay-*.png'):
                with Image.open(png) as im:
                    check(im.size==(200,214) and im.mode=='RGB','analytical overlay geometry')
        return {'match_rows':72,'model_rows':36,'score_grids':72,'identical_products':len(product_names),
                'single_reference_failure_model_rows':12,'overlay_count':12,'input_count':len(inputs)}
    case('full_synthetic_pipeline_repetition_admission_and_overwrite',full_wrapper)

    def bad_input(name, mutate, message, refresh_manifest=False):
        config,bindings = fixture(out/name)
        selection = bindings['BASE']/'refine01/camera2/selection.json'
        mutate(config,bindings,selection)
        if refresh_manifest:
            bindings['PINS'][selection] = subject.fp(selection)['sha256']
        with patch.multiple(subject,**bindings):
            rejected(lambda:subject.load_inputs(config),message)
        return {'rejected_with':message}

    def duplicate(config,bindings,selection):
        config['camera2'][1]['id'] = config['camera2'][0]['id']
    case('duplicate_reference_ids_reject',lambda:bad_input('duplicate-ids',duplicate,'reference-ids'))

    def stale(config,bindings,selection):
        selection.write_bytes(selection.read_bytes()+b' ')
    case('modified_manifest_rejects',lambda:bad_input('manifest-tamper',stale,'prior-pin'))

    def png_tamper(config,bindings,selection):
        png = selection.parent/'f000001.png'
        png.write_bytes(png.read_bytes()+b'extra')
    case('modified_png_rejects',lambda:bad_input('png-tamper',png_tamper,'png-pin'))

    def wrong_luma(config,bindings,selection):
        data = json.loads(selection.read_text())
        data['images'][0]['luma_sha256'] = '0'*64
        dump(selection,data)
    case('luma_hash_rejects',lambda:bad_input('wrong-luma',wrong_luma,'luma-pin',True))

    def wrong_pts(config,bindings,selection):
        data = json.loads(selection.read_text())
        data['images'][1]['source_time_seconds_exact'] = '2'
        dump(selection,data)
    case('PTS_arithmetic_rejects',lambda:bad_input('wrong-pts',wrong_pts,'pts',True))

    def duplicate_pts(config,bindings,selection):
        data = json.loads(selection.read_text())
        data['images'][1]['source_time_seconds_exact'] = '0'
        data['images'][1]['source_pts'] = 0
        dump(selection,data)
    case('nonincreasing_PTS_rejects',lambda:bad_input('duplicate-pts',duplicate_pts,'pts-order',True))

    def missing_selection(config,bindings,selection):
        data = json.loads(selection.read_text())
        data['images'].pop()
        dump(selection,data)
    case('missing_selected_frame_rejects',lambda:bad_input('missing-frame',missing_selection,'input-selection',True))

    def source_tamper(config,bindings,selection):
        (bindings['ROOT']/'synthetic-source.bin').write_bytes(b'changed synthetic source')
    case('changed_source_pin_rejects',lambda:bad_input('source-tamper',source_tamper,'input-integrity'))

    check(all(subject.fp(Path(p))==pin for p,pin in pins.items()),'procedure changed during controls')
    receipt = {'scope':'root synthetic controls only; not historical image or physical validation',
        'python':sys.version,'numpy':np.__version__,'procedure_pins':pins,'tests':results,
        'passed':sum(r['status']=='pass' for r in results),'failed':sum(r['status']=='fail' for r in results),
        'products':{str(p.relative_to(out)):subject.fp(p) for p in sorted(out.rglob('*')) if p.is_file()}}
    dump(out/'receipt.json',receipt)
    print(json.dumps({'passed':receipt['passed'],'failed':receipt['failed'],
        'failures':[r for r in results if r['status']=='fail']}))
    return receipt['failed']


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    sys.exit(bool(suite(parser.parse_args().out)))
