"""Independent reference-motion artifact/numerical verification; never runs measure.py.

Historical scopes must be explicitly supplied after completion. Writes a new
verification*.json receipt only. Prior review receipts and source outputs remain
unchanged. Uses the reviewer's previously tested mean/complex/QR fit oracle.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import PIL
from PIL import Image, ImageDraw
from independent_tests import oracle_transform, oracle_ncc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = HERE.parent/'multiview-onset-review'
TIMING = HERE.parent/'timing-audit/run-2026-09-08-v1.1'
MODELS = ('translation','similarity','affine')
HALVES = (9,13)
EVALUATIONS = {'camera2':(6654,6751,6931,7013,7104),'camera4':(960,1042,1162,1259,1350)}
CAMERAS = {
    'camera2':('VID-WTC7-001','NIST Camera 2_CBS-Net Dub6 48 (Converted).mov',71,(640,480)),
    'camera4':('VID-WTC7-003','NIST Camera 4.mp4',63,(480,360)),
}
PRIOR_PINS = {
    BASE/'refine01/receipt.json':'c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503',
    BASE/'refine01/camera2/selection.json':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e',
    BASE/'refine01/camera4/selection.json':'143aa3759d516299b508ddd81545f981797f58382b39f1c2a9a6189ff90faf1e',
    BASE/'refinement.json':'700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a',
}


def require(condition,label):
    if not condition:
        raise AssertionError(label)


def fp(path):
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':value}


def read_json(path):
    def invalid(value):
        raise ValueError('nonfinite JSON token')
    return json.loads(path.read_text(),parse_constant=invalid)


def close(actual,expected,label,atol=1e-8,rtol=1e-10):
    a,b = np.asarray(actual,dtype=float),np.asarray(expected,dtype=float)
    require(a.shape == b.shape and np.isfinite(a).all() and np.isfinite(b).all(),label+' shape/finite')
    require(np.allclose(a,b,atol=atol,rtol=rtol),label+' numeric mismatch')


def window_sums(array,side):
    integral = np.pad(np.cumsum(np.cumsum(array,axis=0),axis=1),((1,0),(1,0)))
    return integral[side:,side:]-integral[:-side,side:]-integral[side:,:-side]+integral[:-side,:-side]


def fft_scores(frame,template,center,radius=24):
    side = template.shape[0]
    half = side//2
    x,y = center
    bounds = [max(half,x-radius),min(frame.shape[1]-half-1,x+radius),
              max(half,y-radius),min(frame.shape[0]-half-1,y+radius)]
    x0,x1,y0,y1 = bounds
    region = frame[y0-half:y1+half+1,x0-half:x1+half+1].astype(np.float64)
    t = template.astype(np.float64)
    centered = t-t.mean()
    shape = tuple(1 << (length+side-2).bit_length() for length in region.shape)
    convolution = np.fft.irfft2(np.fft.rfft2(region,s=shape)*np.fft.rfft2(centered[::-1,::-1],s=shape),s=shape)
    numerator = convolution[side-1:region.shape[0],side-1:region.shape[1]]
    sums = window_sums(region,side)
    energy = window_sums(region*region,side)-sums*sums/(side*side)
    require(np.isfinite(energy).all() and (energy >= -1e-7).all(),'independent window energy')
    denominator = np.sqrt(np.maximum(energy,0)*np.sum(centered*centered))
    scores = np.full(numerator.shape,np.nan,dtype=np.float64)
    np.divide(numerator,denominator,out=scores,where=denominator>1e-12)
    return scores,bounds,float(np.sqrt(np.mean(centered*centered)))


def score_control():
    rng = np.random.default_rng(53179)
    frame = rng.integers(0,256,(80,80),dtype=np.uint8)
    maximum = 0.
    checked = 0
    for half,center in ((9,(40,40)),(13,(40,40)),(9,(12,12))):
        x,y = center
        side = 2*half+1
        template = frame[y-half:y+half+1,x-half:x+half+1]
        scores,bounds,_ = fft_scores(frame,template,center,4)
        x0,x1,y0,y1 = bounds
        for iy,cy in enumerate(range(y0,y1+1)):
            for ix,cx in enumerate(range(x0,x1+1)):
                expected = oracle_ncc(template,frame[cy-half:cy+half+1,cx-half:cx+half+1])
                difference = abs(scores[iy,ix]-expected)
                maximum = max(maximum,float(difference))
                require(difference <= 1e-10,'synthetic FFT oracle comparison')
                checked += 1
    flat = np.full((80,80),100,dtype=np.uint8)
    scores,_,_ = fft_scores(flat,flat[20:39,20:39],(29,29),4)
    require(np.isnan(scores).all(),'synthetic constant-window undefined mask')
    return {'windows_checked_against_direct_NCC':checked,'max_difference':maximum,'constant_mask_checked':True}


def derive_match(scores,bounds,texture_std):
    require(scores.dtype == np.float64 and scores.ndim == 2,'grid float64 matrix')
    require(not np.isinf(scores).any(),'infinite grid value')
    x0,x1,y0,y1 = bounds
    require(scores.shape == (y1-y0+1,x1-x0+1),'grid shape/coordinate support')
    flags = []
    valid = np.isfinite(scores)
    result = {'search_bounds':bounds,'template_std':texture_std,'undefined_windows':int((~valid).sum()),'flags':flags}
    if texture_std < 2:
        flags.append('low_seed_texture')
    if not valid.any():
        flags.append('no_defined_score')
        result['status'] = 'rejected'
        return result
    ranking = np.where(valid,scores,-np.inf)
    iy,ix = np.unravel_index(np.argmax(ranking),ranking.shape)
    best = float(scores[iy,ix])
    count = int(np.count_nonzero(valid & (np.abs(scores-best)<=1e-12)))
    yy,xx = np.indices(scores.shape)
    competitor_allowed = valid & (np.maximum(np.abs(yy-iy),np.abs(xx-ix))>3)
    competitors = np.where(competitor_allowed,scores,-np.inf)
    cy,cx = np.unravel_index(np.argmax(competitors),competitors.shape)
    competitor = float(competitors[cy,cx]) if competitor_allowed.any() else None
    boundary = int(ix) in (0,scores.shape[1]-1) or int(iy) in (0,scores.shape[0]-1)
    if best < .8:
        flags.append('low_ncc')
    if count > 1:
        flags.append('tied_best')
    if competitor is None:
        flags.append('no_competitor')
    elif best-competitor < .02:
        flags.append('ambiguous_competitor')
    if boundary:
        flags.append('search_boundary')
    result.update(candidate_xy=[x0+int(ix),y0+int(iy)],ncc=best,
        competitor_xy=[x0+int(cx),y0+int(cy)] if competitor is not None else None,
        competitor_ncc=competitor,margin=best-competitor if competitor is not None else None,
        tied_best_count=count,at_search_boundary=boundary,status='rejected' if flags else 'candidate')
    return result


def source_inputs(config):
    pins = {}
    for path,digest in PRIOR_PINS.items():
        identity = fp(path)
        require(identity['sha256'] == digest,'prior artifact pin')
        pins[str(path)] = identity
    refinement = read_json(BASE/'refinement.json')
    groups = {}
    for camera,(video,name,count,dimensions) in CAMERAS.items():
        manifest = read_json(BASE/'refine01'/camera/'selection.json')
        require(manifest['geometry'] == list(dimensions),'prior stored dimensions')
        source = ROOT/'research/wtc7-video-comparison/media/analysis-source'/name
        allowed = {source,TIMING/video/'frame-map.csv',TIMING/video/'frames.json',TIMING/video/'source-identity.json'}
        original = {ROOT/relative:identity for relative,identity in manifest['input_pins'].items()}
        require(set(original) == allowed,'prior source pin set')
        for path,identity in original.items():
            require(fp(path) == identity,'current original source/map pin')
            pins[str(path)] = identity
        wanted = refinement['rules'][camera]['groups']['event']
        rows = [row for row in manifest['images'] if int(row['frame_index_zero_based']) in wanted]
        require(len(rows) == count and [int(row['frame_index_zero_based']) for row in rows] == wanted,'declared event coverage')
        features = config[camera]
        require(len(features) == 6 and len({row['id'] for row in features}) == 6,'six unique configured references')
        for feature in features:
            require(isinstance(feature['id'],str) and len(feature['xy']) == 2 and all(type(value) is int for value in feature['xy']),'reference ID/coordinate contract')
        arrays = []
        previous = None
        for row in rows:
            index = int(row['frame_index_zero_based'])
            require(row['png'] == f'f{index:06d}.png','input native filename')
            path = BASE/'refine01'/camera/row['png']
            identity = fp(path)
            require(identity == row['png_identity'],'input PNG identity')
            with Image.open(path) as image:
                require(image.format == 'PNG' and image.mode == 'L' and image.size == dimensions,'input PNG mode/dimensions')
                array = np.array(image)
            require(array.dtype == np.uint8 and array.ndim == 2,'native array contract')
            require(hashlib.sha256(array.tobytes()).hexdigest() == row['luma_sha256'],'input luma identity')
            time = Fraction(row['source_time_seconds_exact'])
            require(time == int(row['source_pts'])*Fraction(row['source_time_base']),'exact source PTS')
            require(previous is None or time > previous,'strict event PTS order')
            previous = time
            pins[str(path)] = identity
            arrays.append(array)
        groups[camera] = (rows,arrays)
    return groups,pins


def rank_diagnostic(points,model):
    if model == 'translation':
        return {'status':'computed','rank':2,'normalized_design_condition':1.}
    centered = points-points.mean(axis=0)
    scale = float(np.sqrt(np.mean(np.sum(centered*centered,axis=1))))
    if scale <= 1e-12:
        return {'status':'degenerate_source_geometry'}
    if model == 'similarity':
        # Centered, radial-RMS-normalized proper-similarity columns are orthogonal,
        # each with squared norm n. Any positive source spread identifies all four.
        return {'status':'computed','rank':4,'normalized_design_condition':1.}
    design = np.column_stack((centered/scale,np.ones(len(points))))
    singular = np.linalg.svd(design,compute_uv=False)
    rank = int(np.count_nonzero(singular>singular[0]*1e-12))
    condition = float(singular[0]/singular[-1]) if singular[-1]>0 else None
    if rank != 3 or condition is None or condition > 10000:
        return {'status':'rank_or_condition_failure','rank':rank,'condition':condition}
    return {'status':'computed','rank':rank,'normalized_design_condition':condition}


def independent_fit(points,targets,model):
    diagnostic = rank_diagnostic(points,model)
    if diagnostic['status'] != 'computed':
        return diagnostic
    fitted = oracle_transform(points,targets,model)
    matrix,offset = fitted['matrix'],fitted['offset']
    determinant = float(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])
    diagnostic.update(matrix=matrix,offset=offset,residual_xy=fitted['residuals'],
        rms_residual=fitted['rms'],max_residual=fitted['max'],determinant=determinant,
        positive_nonsingular=determinant>1e-12)
    return diagnostic


def audit_fit(row,points,targets,model):
    expected = independent_fit(points,targets,model)
    require(row['status'] == expected['status'],'transform rank/condition disposition')
    if expected['status'] != 'computed':
        require(row['passes_consistency_screen'] is False,'uncomputed model passes screen')
        if 'rank' in expected:
            require(row['rank'] == expected['rank'],'rejected transform rank')
        return {'computed':False,'screen':False,'threshold_near':False}
    require(row['rank'] == expected['rank'],'transform rank')
    for name in ('matrix','offset','residual_xy','rms_residual','max_residual','determinant','normalized_design_condition'):
        close(row[name],expected[name],'transform '+name)
    require(row['positive_nonsingular'] == bool(expected['positive_nonsingular']),'transform orientation/degeneracy')
    folds = row['leave_one_out']
    require(len(folds) == 6,'six LOO folds')
    all_valid = True
    for index,fold in enumerate(folds):
        require(fold['omitted_reference'] == index,'LOO order/coverage')
        keep = np.arange(6) != index
        omitted = independent_fit(points[keep],targets[keep],model)
        require(fold['status'] == omitted['status'],'LOO rank/conditioning disposition')
        if omitted['status'] != 'computed':
            all_valid = False
            continue
        error = targets[index]-(points[index]@omitted['matrix'].T+omitted['offset'])
        close(fold['error_xy'],error,'LOO error vector')
        close(fold['error_norm'],np.sqrt(np.dot(error,error)),'LOO Euclidean error')
        require(fold['positive_nonsingular'] == bool(omitted['positive_nonsingular']),'LOO orientation/degeneracy')
    if all_valid:
        close(row['max_loo_error'],max(fold['error_norm'] for fold in folds),'maximum LOO error')
    else:
        require(row['max_loo_error'] is None,'undefined LOO maximum must remain null')
    # Audit published threshold bookkeeping exactly, distinct from tolerance-based
    # independent arithmetic comparison, and report closeness to the 2-pixel gate.
    screen = all_valid and row['positive_nonsingular'] and all(fold.get('positive_nonsingular',False) for fold in folds) and row['max_residual']<=2 and row['max_loo_error']<=2
    require(row['passes_consistency_screen'] == bool(screen),'consistency-screen bookkeeping')
    near = abs(row['max_residual']-2)<=1e-8 or (all_valid and abs(row['max_loo_error']-2)<=1e-8)
    return {'computed':True,'screen':bool(screen),'threshold_near':near}


def inventory(scope):
    require(scope.parent == HERE and scope.is_dir(),'explicit local run scope')
    require(not (scope/'failure.json').exists(),'failed historical run not accepted')
    receipt = read_json(scope/'receipt.json')
    require(receipt['status'] == 'complete_diagnostic_not_camera_calibration','historical receipt status')
    require((receipt['match_rows'],receipt['model_rows'],receipt['score_grids']) == (1608,804,1608),'declared run counts')
    listed = receipt['products']
    actual = {path.name for path in scope.iterdir() if path.is_file()}
    require(all(path.is_file() for path in scope.iterdir()),'unexpected nested run content')
    require(actual == set(listed)|{'receipt.json'},'exact run inventory')
    require(len(listed) == 33,'expected 33 deterministic products')
    for name,identity in listed.items():
        require(Path(name).name == name and fp(scope/name) == identity,'historical product pin')
    initial = read_json(scope/'initial.json')
    expected_sources = {HERE/name for name in ('measure.py','PROTOCOL.md','features.json','test_measure.py')}
    require(Path(initial['executable']).resolve() == Path(sys.executable).resolve(),'review runtime differs from run executable')
    expected_pins = expected_sources|{Path(initial['executable'])}
    require({Path(path) for path in initial['pins']} == expected_pins,'procedure/runtime pin set')
    for path in expected_pins:
        identity = initial['pins'][str(path)]
        require(fp(path) == identity,'current procedure/runtime identity')
        if path in expected_sources:
            require(fp(scope/path.name) == identity,'procedure snapshot identity')
    return receipt,{'scope':scope.name,'receipt':fp(scope/'receipt.json'),'products_checked':len(listed),
        'procedure_pins':initial['pins'],'runtime':{name:initial[name] for name in ('python','numpy','pillow')}}


def deep_review(scope,config,groups,pins):
    require(read_json(scope/'input-pins.json') == pins,'complete input pin inventory')
    matches = read_json(scope/'matches.json')
    transforms = read_json(scope/'transforms.json')
    match_cursor = model_cursor = 0
    expected_keys = []
    candidate_counts = Counter()
    flag_counts = Counter()
    model_counts = Counter()
    per_reference = Counter()
    near_gates = []
    numeric_gate_differences = []
    maximum_difference = 0.
    score_values = 0
    overlay_count = 0
    with np.load(scope/'score-grids.npz',allow_pickle=False) as grids:
        for camera,(stamps,arrays) in groups.items():
            features = config[camera]
            points = np.array([feature['xy'] for feature in features],dtype=float)
            for half in HALVES:
                templates = []
                for feature in features:
                    x,y = feature['xy']
                    template = arrays[0][y-half:y+half+1,x-half:x+half+1]
                    require(template.shape == (2*half+1,2*half+1),'baseline template support')
                    templates.append(template)
                for stamp,frame in zip(stamps,arrays):
                    index = int(stamp['frame_index_zero_based'])
                    current = []
                    for feature,template in zip(features,templates):
                        require(match_cursor < len(matches),'missing match row')
                        row = matches[match_cursor]
                        match_cursor += 1
                        key = f'{camera}_{index}_{half}_{feature["id"]}'
                        expected_keys.append(key)
                        metadata = {'camera':camera,'index':index,'pts':stamp['source_pts'],
                            'time_base':stamp['source_time_base'],'seconds_exact':stamp['source_time_seconds_exact'],
                            'half':half,'reference':feature['id'],'baseline_xy':feature['xy'],'score_grid':key}
                        require(all(row.get(name) == value for name,value in metadata.items()),'match declared row order/lineage')
                        scores = grids[key]
                        independent,bounds,std = fft_scores(frame,template,feature['xy'])
                        require(scores.shape == independent.shape and np.array_equal(np.isnan(scores),np.isnan(independent)),'independent grid shape/undefined mask')
                        finite = np.isfinite(scores)
                        difference = float(np.max(np.abs(scores[finite]-independent[finite]))) if finite.any() else 0.
                        require(difference <= 1e-8,'full independent NCC grid mismatch')
                        maximum_difference = max(maximum_difference,difference)
                        score_values += scores.size
                        expected = derive_match(scores,bounds,std)
                        require(set(row) == set(metadata)|set(expected),'match field schema')
                        for name,value in expected.items():
                            if name == 'template_std':
                                close(row[name],value,'baseline standard deviation',atol=1e-12)
                            else:
                                require(row[name] == value,'grid-derived match field '+name)
                        independent_decision = derive_match(independent,bounds,std)
                        compared = ('candidate_xy','competitor_xy','tied_best_count','flags','status')
                        differences = [name for name in compared if expected.get(name) != independent_decision.get(name)]
                        if differences:
                            numeric_gate_differences.append({'grid':key,'fields':differences,
                                'stored_status':expected['status'],'independent_status':independent_decision['status'],
                                'stored_xy':expected.get('candidate_xy'),'independent_xy':independent_decision.get('candidate_xy'),
                                'stored_flags':expected['flags'],'independent_flags':independent_decision['flags'],
                                'max_score_difference':difference})
                        if 'ncc' in expected and (abs(expected['ncc']-.8)<=1e-8 or (expected['margin'] is not None and abs(expected['margin']-.02)<=2e-8)):
                            near_gates.append({'grid':key,'ncc':expected['ncc'],'margin':expected['margin']})
                        candidate_counts[f'{camera}/side{2*half+1}/{row["status"]}'] += 1
                        per_reference[f'{camera}/side{2*half+1}/{feature["id"]}/{row["status"]}'] += 1
                        for flag in row['flags']:
                            flag_counts[f'{camera}/side{2*half+1}/{flag}'] += 1
                        current.append(row)
                    failed = [row['reference'] for row in current if row['status'] != 'candidate']
                    for model in MODELS:
                        require(model_cursor < len(transforms),'missing model row')
                        row = transforms[model_cursor]
                        model_cursor += 1
                        metadata = {'camera':camera,'index':index,'half':half,'model':model,
                            'seconds_exact':stamp['source_time_seconds_exact'],'reference_order':[feature['id'] for feature in features]}
                        require(all(row.get(name) == value for name,value in metadata.items()),'model declared row order/lineage')
                        if failed:
                            expected = dict(metadata,status='reference_quality_failure',passes_consistency_screen=False,failed_references=failed)
                            require(row == expected,'all-six admission or failed-reference coverage')
                        else:
                            outcome = audit_fit(row,points,np.array([item['candidate_xy'] for item in current],float),model)
                            if outcome['threshold_near']:
                                near_gates.append({'model':f'{camera}/{index}/{half}/{model}','max_residual':row['max_residual'],'max_loo_error':row['max_loo_error']})
                        model_counts[f'{camera}/side{2*half+1}/{model}/{row["status"]}'] += 1
                        if row['passes_consistency_screen']:
                            model_counts[f'{camera}/side{2*half+1}/{model}/passes_consistency_screen'] += 1
                    if index in EVALUATIONS[camera] or stamp is stamps[0]:
                        expected_image = Image.new('RGB',(frame.shape[1],frame.shape[0]+34),'white')
                        expected_image.paste(Image.fromarray(frame).convert('RGB'),(0,0))
                        draw = ImageDraw.Draw(expected_image)
                        for row in current:
                            if 'candidate_xy' in row:
                                x,y = row['candidate_xy']
                                color = 'lime' if row['status']=='candidate' else 'red'
                                draw.rectangle((x-4,y-4,x+4,y+4),outline=color,width=1)
                                draw.text((x+5,y),row['reference'],fill=color)
                        draw.text((4,frame.shape[0]+2),f'ANALYTICAL CANDIDATES {camera} frame {index} half {half}',fill='black')
                        draw.text((4,frame.shape[0]+17),'Green=screen passed; red=rejected; not physical tracks',fill='black')
                        with Image.open(scope/f'overlay-{camera}-{index}-{half}.png') as overlay:
                            require(overlay.format=='PNG' and overlay.mode=='RGB' and overlay.size==expected_image.size and overlay.tobytes()==expected_image.tobytes(),'overlay pixel/label reconstruction')
                        overlay_count += 1
        require(len(expected_keys)==len(set(expected_keys))==1608 and set(grids.files)==set(expected_keys),'exact complete score grid keys')
    require(match_cursor==len(matches)==1608 and model_cursor==len(transforms)==804,'exact row coverage')
    require(overlay_count==24,'overlay coverage')
    return {'match_rows_checked':match_cursor,'model_rows_checked':model_cursor,'full_grids_recomputed':len(expected_keys),
        'grid_values_compared':score_values,'max_independent_NCC_difference':maximum_difference,'overlays_rebuilt':overlay_count,
        'candidate_counts':dict(candidate_counts),'flag_counts':dict(flag_counts),'per_reference_counts':dict(per_reference),
        'model_counts':dict(model_counts),'near_screening_thresholds':near_gates,
        'independent_grid_decision_differences':numeric_gate_differences}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runs',nargs=2,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--self-check',action='store_true')
    args = parser.parse_args()
    destination = args.out.absolute()
    require(destination.parent == HERE and destination.name.startswith('verification') and destination.suffix=='.json','review output scope')
    require(not destination.exists(),'preserve prior verification receipts')
    output = {'verifier':fp(Path(__file__)),'independent_fit_oracle':fp(HERE/'independent_tests.py'),
        'python':platform.python_version(),'numpy':np.__version__,'pillow':PIL.__version__,'command':sys.argv,
        'scope':'Independent image-artifact and numerical bookkeeping verification; no video decode, measure.run(), physical accuracy or cause claim.'}
    try:
        output['FFT_controls'] = score_control()
        if not args.self_check:
            scopes = [(HERE/name).absolute() for name in args.runs]
            records = [inventory(scope) for scope in scopes]
            receipts = [record[0] for record in records]
            output['runs'] = [record[1] for record in records]
            require(receipts[0]['products'] == receipts[1]['products'],'repeat-run deterministic product equality')
            output['reproduction'] = {'products_compared':len(receipts[0]['products']),'all_byte_identical':True,
                'numeric_scope':'Full numerical audit on first run transfers to byte-identical products in second run.'}
            config = read_json(scopes[0]/'features.json')
            require(config['half_widths']==list(HALVES) and config['radius']==24,'fixed matching parameters')
            groups,pins = source_inputs(config)
            output['source_pins'] = pins
            require(read_json(scopes[1]/'input-pins.json') == pins,'second-run complete input pin inventory')
            output['numerical_review'] = deep_review(scopes[0],config,groups,pins)
            require(all(fp(Path(path)) == identity for path,identity in pins.items()),'post-review input pins')
            output['review_status'] = 'passed_declared_checks'
            output['independent_decision_stability'] = 'differences_recorded' if output['numerical_review']['independent_grid_decision_differences'] else 'all_compared_decisions_agree'
        else:
            output['review_status'] = 'self_check_only_no_historical_read'
        output['status'] = 'pass'
    except Exception as error:
        output.update(status='fail',error_type=type(error).__name__,error=str(error))
    with destination.open('x') as stream:
        stream.write(json.dumps(output,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({key:output[key] for key in ('status','review_status','error_type','error','independent_decision_stability') if key in output},sort_keys=True))
    return 0 if output['status']=='pass' else 1


if __name__=='__main__':
    raise SystemExit(main())
