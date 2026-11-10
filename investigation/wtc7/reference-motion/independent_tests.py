"""Deterministic independent controls for the reference-motion diagnostic.

The expected NCC and transform arithmetic below do not import the implementation.
Synthetic implementation adapters and historical artifact checks are added after
the declared analytic plan; no source video is decoded by this reviewer.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def fingerprint(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def oracle_ncc(template, candidate):
    a = np.asarray(template,dtype=np.float64).ravel()
    b = np.asarray(candidate,dtype=np.float64).ravel()
    check(a.shape == b.shape and np.isfinite(a).all() and np.isfinite(b).all(), 'oracle NCC inputs')
    a, b = a-a.mean(), b-b.mean()
    denominator = np.sqrt(np.dot(a,a)*np.dot(b,b))
    return None if denominator == 0 else float(np.dot(a,b)/denominator)


def oracle_grid(base, image, center, size, radius):
    x,y = center
    half = size//2
    template = base[y-half:y+half+1,x-half:x+half+1]
    check(template.shape == (size,size), 'oracle template support')
    lower_x, upper_x = max(half,x-radius), min(image.shape[1]-half-1,x+radius)
    lower_y, upper_y = max(half,y-radius), min(image.shape[0]-half-1,y+radius)
    grid = np.empty((upper_y-lower_y+1,upper_x-lower_x+1),dtype=np.float64)
    for row,target_y in enumerate(range(lower_y,upper_y+1)):
        for col,target_x in enumerate(range(lower_x,upper_x+1)):
            score = oracle_ncc(template,image[target_y-half:target_y+half+1,target_x-half:target_x+half+1])
            grid[row,col] = np.nan if score is None else score
    return grid, (lower_x,upper_x,lower_y,upper_y)


def oracle_transform(source, target, model):
    """Independent translation/complex-similarity/direct-QR affine prediction.

    Returns A and b for row-vector points: prediction = source @ A.T + b.
    This helper deliberately does not use the implementation's normalized SVD fit.
    Rank/condition acceptance is separately checked against the declared protocol.
    """
    p,q = np.asarray(source,dtype=float),np.asarray(target,dtype=float)
    check(p.ndim == q.ndim == 2 and p.shape == q.shape and p.shape[1] == 2, 'oracle point shapes')
    check(np.isfinite(p).all() and np.isfinite(q).all(), 'oracle finite points')
    if model == 'translation':
        matrix = np.eye(2)
        offset = (q-p).mean(axis=0)
    elif model == 'similarity':
        z = p[:,0]+1j*p[:,1]
        w = q[:,0]+1j*q[:,1]
        centered_z, centered_w = z-z.mean(),w-w.mean()
        denominator = np.vdot(centered_z,centered_z).real
        check(denominator > 0, 'oracle similarity identifiable')
        coefficient = np.vdot(centered_z,centered_w)/denominator
        constant = w.mean()-coefficient*z.mean()
        matrix = np.array([[coefficient.real,-coefficient.imag],[coefficient.imag,coefficient.real]])
        offset = np.array([constant.real,constant.imag])
    elif model == 'affine':
        design = np.column_stack((p,np.ones(len(p))))
        check(np.linalg.matrix_rank(design) == 3, 'oracle affine identifiable')
        orthogonal, triangular = np.linalg.qr(design,mode='reduced')
        coefficients = np.linalg.solve(triangular,orthogonal.T@q)
        matrix,offset = coefficients[:2].T,coefficients[2]
    else:
        raise ValueError('unknown model')
    residuals = q-(p@matrix.T+offset)
    lengths = np.sqrt(np.sum(residuals*residuals,axis=1))
    return {'matrix':matrix,'offset':offset,'residuals':residuals,
        'rms':float(np.sqrt(np.mean(lengths*lengths))),'max':float(lengths.max())}


def oracle_loo(source,target,model):
    p,q = np.asarray(source,dtype=float),np.asarray(target,dtype=float)
    results = []
    for held in range(len(p)):
        keep = np.arange(len(p)) != held
        try:
            fitted = oracle_transform(p[keep],q[keep],model)
            difference = q[held]-(p[held]@fitted['matrix'].T+fitted['offset'])
            results.append(float(np.linalg.norm(difference)))
        except (AssertionError,np.linalg.LinAlgError):
            results.append(None)
    return results


def point_fixture():
    return np.array([[10.,10.],[80.,15.],[25.,65.],[95.,90.],[45.,120.],[130.,45.]])


def image_fixture(seed=4107):
    # Even-valued texture allows an exact positive contrast/brightness control.
    rng = np.random.default_rng(seed)
    return (rng.integers(20,100,size=(128,128),dtype=np.uint8)*2)


def displaced(source,dx,dy):
    return np.roll(np.roll(source,dy,axis=0),dx,axis=1)


def insert(image,patch,center):
    x,y = center
    half = patch.shape[0]//2
    image[y-half:y+half+1,x-half:x+half+1] = patch


def plain(value):
    if isinstance(value,np.ndarray):
        return value.tolist()
    if isinstance(value,np.generic):
        return value.item()
    if isinstance(value,dict):
        return {key:plain(item) for key,item in value.items()}
    if isinstance(value,(list,tuple)):
        return [plain(item) for item in value]
    return value


def self_check_oracles():
    source = point_fixture()
    displacement = np.array([9.,12.])
    target = source.copy()
    target[-1] += displacement
    fit = oracle_transform(source,target,'translation')
    check(np.allclose(fit['offset'],displacement/6,atol=1e-12), 'analytic mean displacement')
    check(abs(fit['rms']-np.sqrt(5)*15/6) < 1e-12, 'analytic Euclidean RMS')
    check(np.allclose(oracle_loo(source,target,'translation'),[3]*5+[15],atol=1e-12), 'analytic LOO errors')
    for model,matrix in [('similarity',np.array([[.96,-.72],[.72,.96]])),
                         ('affine',np.array([[1.1,.2],[-.1,.9]]))]:
        target = source@matrix.T+np.array([7.5,-3.25])
        fit = oracle_transform(source,target,model)
        check(np.allclose(fit['matrix'],matrix,atol=1e-12), 'analytic exact matrix')
        check(fit['rms'] < 1e-10 and max(oracle_loo(source,target,model)) < 1e-10, 'analytic exact map residuals')
    texture = image_fixture()[50:69,50:69]
    check(abs(oracle_ncc(texture,texture//2+40)-1) < 1e-12, 'analytic NCC contrast invariance')
    check(oracle_ncc(texture,np.zeros_like(texture)) is None, 'analytic undefined constant NCC')
    return {'status':'pass','translation_outlier_loo':[3]*5+[15],
        'translation_outlier_rms':float(np.sqrt(5)*15/6)}


def exercise_subject(subject):
    results = []

    def run(name,callback):
        try:
            detail = callback()
            results.append({'name':name,'status':'pass','detail':plain(detail)})
        except Exception as error:
            results.append({'name':name,'status':'fail','error_type':type(error).__name__,'error':str(error)})

    def matched(base,image,center=(64,64),size=19,radius=24):
        x,y = center
        half = size//2
        return subject.match(image,base[y-half:y+half+1,x-half:x+half+1].copy(),list(center),radius)

    def rejected_call(callback):
        try:
            callback()
        except (ValueError,TypeError):
            return True
        return False

    def grid_control():
        base = image_fixture()
        target = displaced(base,2,-1)
        result,actual = matched(base,target,radius=4)
        expected,bounds = oracle_grid(base,target,(64,64),19,4)
        check(result['search_bounds'] == list(bounds), 'full-grid search support')
        check(np.array_equal(np.isnan(actual),np.isnan(expected)), 'full-grid undefined masks')
        error = float(np.nanmax(np.abs(actual-expected)))
        check(error < 1e-11, 'every synthetic NCC differs from oracle')
        check(result['candidate_xy'] == [66,63] and result['status'] == 'candidate', 'oracle-grid winner')
        return {'windows_checked':int(actual.size),'maximum_ncc_difference':error}
    run('all_windows_against_direct_zero_mean_NCC',grid_control)

    def translation_control(size):
        base = image_fixture()
        result,_ = matched(base,displaced(base,17,-13),size=size)
        check(result['candidate_xy'] == [81,51] and result['status'] == 'candidate', 'unique translation')
        check(abs(result['ncc']-1) < 1e-11, 'true translation NCC')
        return result
    for size in (19,27):
        run(f'integer_translation_{size}',lambda size=size:translation_control(size))

    def contrast_control():
        base = image_fixture()
        result,_ = matched(base,displaced(base//2+40,7,-4))
        check(result['candidate_xy'] == [71,60] and result['status'] == 'candidate', 'positive contrast localization')
        check(abs(result['ncc']-1) < 1e-11, 'positive contrast NCC')
        return result
    run('positive_contrast_brightness_invariance',contrast_control)

    def negative_contrast():
        base = image_fixture()
        result,grid = matched(base,255-base)
        check(abs(grid[24,24]+1) < 1e-11, 'negative contrast must be negative NCC')
        check(result['status'] == 'rejected' and 'low_ncc' in result['flags'], 'negative contrast rejection')
        return {'true_center_ncc':float(grid[24,24]),'flags':result['flags']}
    run('negative_contrast_is_not_a_positive_match',negative_contrast)

    def template_dependence():
        base = image_fixture()
        target = image_fixture(777)
        insert(target,base[51:78,51:78],(78,64))
        insert(target,base[55:74,55:74],(50,64))
        small,_ = matched(base,target,size=19)
        large,_ = matched(base,target,size=27)
        check(small['status'] == 'rejected' and small['tied_best_count'] >= 2 and 'ambiguous_competitor' in small['flags'], 'identical small-patch distractor')
        check(large['status'] == 'candidate' and large['candidate_xy'] == [78,64], 'larger contextual patch')
        return {'small':small,'large':large,'meaning':'Larger context resolves this construction; no rule for preferring one historical size.'}
    run('identical_distractor_and_template_size_dependence',template_dependence)

    def nearby_tie():
        rng = np.random.default_rng(202)
        base,target = image_fixture(),image_fixture(203)
        profile = rng.integers(20,200,size=(19,1),dtype=np.uint8)
        base[55:74,55:74] = np.repeat(profile,19,axis=1)
        target[55:74,55:75] = np.repeat(profile,20,axis=1)
        result,_ = matched(base,target)
        check(result['tied_best_count'] >= 2 and 'tied_best' in result['flags'] and result['status'] == 'rejected', 'nearby tie not rejected')
        check(result['margin'] > .02, 'construction should distinguish tie gate from distant margin gate')
        return result
    run('nearby_tie_inside_exclusion_still_rejects',nearby_tie)

    def flat_control():
        base = image_fixture()
        uniform = np.full_like(base,120)
        flat_seed,grid_seed = matched(uniform,base)
        flat_target,grid_target = matched(base,uniform)
        check(flat_seed['status'] == flat_target['status'] == 'rejected', 'constant patch acceptance')
        check('low_seed_texture' in flat_seed['flags'] and 'no_defined_score' in flat_seed['flags'], 'constant seed flags')
        check('no_defined_score' in flat_target['flags'], 'constant candidate flag')
        check(np.isnan(grid_seed).all() and np.isnan(grid_target).all(), 'undefined masks')
        return {'seed_flags':flat_seed['flags'],'target_flags':flat_target['flags'],'windows_each':int(grid_seed.size)}
    run('constant_seed_and_candidate_masks',flat_control)

    def boundary_control():
        base = image_fixture()
        full,_ = matched(base,displaced(base,24,0))
        clipped,_ = matched(base,displaced(base,-3,0),center=(12,64))
        check(full['candidate_xy'] == [88,64] and 'search_boundary' in full['flags'], 'nominal radius boundary')
        check(clipped['candidate_xy'] == [9,64] and 'search_boundary' in clipped['flags'], 'image-clipped boundary')
        check(full['status'] == clipped['status'] == 'rejected', 'boundary status')
        return {'nominal':full,'image_clipped':clipped}
    run('nominal_and_image_clipped_boundaries',boundary_control)

    def fractional_control():
        base = image_fixture()
        target = ((base.astype(np.uint16)+np.roll(base,1,axis=1).astype(np.uint16))//2).astype(np.uint8)
        result,_ = matched(base,target,size=27)
        check(result['status'] == 'rejected' and 'low_ncc' in result['flags'], 'fixed half-pixel white-texture limitation')
        return {'candidate':result,'meaning':'A constructed 0.5-pixel horizontal blend fails this integer-template gate; no subpixel precision is established.'}
    run('fractional_shift_is_not_a_subpixel_track',fractional_control)

    def ramp_control():
        y,x = np.indices((128,128))
        base = ((x+y)//2).astype(np.uint8)
        result,_ = matched(base,base)
        check(result['status'] == 'rejected' and result['tied_best_count'] > 2, 'nonunique textured ramp')
        return result
    run('textured_smooth_ramp_is_still_ambiguous',ramp_control)

    def invalid_matcher():
        base = image_fixture()
        template = base[55:74,55:74]
        cases = [lambda:subject.match(base.astype(float),template,[64,64]),
            lambda:subject.match(base,np.full((19,19),np.nan),[64,64]),
            lambda:subject.match(base,template,[64.0,64]),
            lambda:subject.match(base,template,[True,64]),
            lambda:subject.match(base,template,[1,1]),
            lambda:subject.match(base,template[:18],[64,64]),
            lambda:subject.match(base,template,[64,64],3)]
        check(all(rejected_call(case) for case in cases), 'invalid matcher contract accepted')
        return {'rejected_contracts':len(cases)}
    run('matcher_invalid_contracts',invalid_matcher)

    def check_fit(source,target,model):
        result = subject.fit_with_loo(source,target,model)
        expected = oracle_transform(source,target,model)
        check(result['status'] == 'computed', 'expected computed transform')
        for field,oracle_field in [('matrix','matrix'),('offset','offset'),('residual_xy','residuals'),
                                    ('rms_residual','rms'),('max_residual','max')]:
            check(np.allclose(result[field],expected[oracle_field],rtol=1e-10,atol=1e-9), 'independent transform '+field)
        expected_loo = oracle_loo(source,target,model)
        check(len(result['leave_one_out']) == len(source), 'every reference held out')
        for index,(fold,expected_error) in enumerate(zip(result['leave_one_out'],expected_loo)):
            check(fold['omitted_reference'] == index, 'LOO reference order')
            if expected_error is None:
                check(fold['status'] != 'computed', 'unidentifiable fold predicted')
            else:
                check(fold['status'] == 'computed' and abs(fold['error_norm']-expected_error) < 1e-8, 'independent held-out error')
        return result

    def exact_map(model):
        source = point_fixture()
        matrices = {'translation':np.eye(2),'similarity':np.array([[.96,-.72],[.72,.96]]),
                    'affine':np.array([[1.1,.2],[-.1,.9]])}
        target = source@matrices[model].T+[7.5,-3.25]
        result = check_fit(source,target,model)
        check(result['passes_consistency_screen'] and result['max_loo_error'] < 1e-9, 'exact model screen')
        return result
    for model in ('translation','similarity','affine'):
        run('exact_'+model,lambda model=model:exact_map(model))

    def outlier_translation():
        source = point_fixture()
        target = source.copy()
        target[-1] += [9,12]
        result = check_fit(source,target,'translation')
        check(np.allclose(result['offset'],[1.5,2],atol=1e-12), 'outlier retained in mean')
        check(np.allclose([fold['error_norm'] for fold in result['leave_one_out']],[3]*5+[15],atol=1e-12), 'analytic outlier LOO')
        check(not result['passes_consistency_screen'], 'outlier screen')
        return result
    run('nonrigid_outlier_is_retained',outlier_translation)

    def collinear_geometry():
        source = np.column_stack((np.arange(6,dtype=float),2*np.arange(6,dtype=float)+3))
        target = source@np.array([[.8,-.6],[.6,.8]]).T+[4,-7]
        similarity = check_fit(source,target,'similarity')
        affine = subject.fit_with_loo(source,target,'affine')
        check(similarity['passes_consistency_screen'], 'collinear similarity incorrectly rejected')
        check(affine['status'] == 'rank_or_condition_failure' and not affine['passes_consistency_screen'], 'collinear affine accepted')
        return {'similarity':similarity,'affine':affine}
    run('model_specific_collinear_geometry',collinear_geometry)

    def loo_geometry():
        source = np.array([[0.,0.],[10.,0.],[20.,0.],[30.,0.],[40.,0.],[20.,30.]])
        target = source.copy()
        target[-1] += [9,12]
        result = check_fit(source,target,'affine')
        check(result['max_residual'] < 1e-9, 'full affine should exactly absorb off-line displacement')
        check(result['leave_one_out'][-1]['status'] == 'rank_or_condition_failure', 'unique off-line fold rank')
        check(result['max_loo_error'] is None and not result['passes_consistency_screen'], 'invalid LOO must prevent consistency')
        return result
    run('zero_training_error_with_unidentifiable_LOO',loo_geometry)

    def degenerate_condition():
        coincident = np.ones((6,2))*25
        repeated = {model:subject.fit_with_loo(coincident,coincident,model) for model in ('similarity','affine')}
        check(all(result['status'] == 'degenerate_source_geometry' for result in repeated.values()), 'coincident geometry')
        near = np.column_stack((np.arange(6,dtype=float),np.array([0,1,-1,2,-2,0])*1e-6))
        narrow = subject.fit_with_loo(near,near,'affine')
        check(narrow['status'] == 'rank_or_condition_failure' and narrow['condition'] > 10000, 'declared condition threshold')
        return {'coincident':repeated,'near_collinear':narrow}
    run('coincident_and_poor_conditioning_reject',degenerate_condition)

    def singular_reflection():
        source = point_fixture()
        reflected = source@np.array([[-1.,0.],[0.,1.]]).T+[150,0]
        affine = check_fit(source,reflected,'affine')
        check(affine['determinant'] < 0 and not affine['passes_consistency_screen'], 'folded affine accepted')
        similarity = check_fit(source,reflected,'similarity')
        check(similarity['max_residual'] > 2 and not similarity['passes_consistency_screen'], 'reflection fitted as proper similarity')
        collapsed = subject.fit_with_loo(source,np.ones_like(source)*42,'similarity')
        check(not collapsed['positive_nonsingular'] and not collapsed['passes_consistency_screen'], 'zero-scale similarity accepted')
        return {'affine_reflection':affine,'proper_similarity_mismatch':similarity,'collapsed_similarity':collapsed}
    run('reflection_and_singular_maps_do_not_pass_camera_screen',singular_reflection)

    def invalid_points():
        source = point_fixture()
        bad = source.copy()
        bad[0,0] = np.nan
        cases = [lambda:subject.fit_points(source,bad,'affine'),
            lambda:subject.fit_points(source,source[:-1],'translation'),
            lambda:subject.fit_points(source,source,'unknown'),
            lambda:subject.fit_points(source[:1],source[:1],'translation')]
        check(all(rejected_call(case) for case in cases), 'invalid point contracts')
        return {'rejected_contracts':len(cases)}
    run('invalid_point_contracts',invalid_points)

    def common_mode():
        source = point_fixture()
        result = check_fit(source,source+[9,12],'translation')
        check(result['passes_consistency_screen'] and result['max_loo_error'] < 1e-10, 'common displacement screen')
        return {'fit':result,'meaning':'Identical common correspondence error would produce these same zero residuals.'}
    run('common_mode_error_is_not_detectable_from_internal_fit',common_mode)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    output_path = args.out.absolute()
    check(output_path.parent == HERE and output_path.name.startswith('independent-tests') and output_path.suffix == '.json', 'review output scope')
    check(not output_path.exists(), 'preserve prior review runs')
    module_path = HERE/'measure.py'
    initial_code = fingerprint(module_path)
    spec = importlib.util.spec_from_file_location('reference_motion_subject',module_path)
    subject = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(subject)
    output = {'reviewer_code':fingerprint(Path(__file__)),'subject_code':initial_code,
        'protocol':fingerprint(HERE/'PROTOCOL.md'),'python':platform.python_version(),'numpy':np.__version__,
        'command':sys.argv,'oracle_self_checks':self_check_oracles(),
        'scope':'Finite synthetic implementation tests; no historical image or video decode.'}
    output['tests'] = exercise_subject(subject)
    check(fingerprint(module_path) == initial_code, 'subject changed during tests')
    output['status'] = 'pass' if all(row['status']=='pass' for row in output['tests']) else 'fail'
    output['passed'] = sum(row['status']=='pass' for row in output['tests'])
    output['failed'] = sum(row['status']=='fail' for row in output['tests'])
    with output_path.open('x') as stream:
        stream.write(json.dumps(plain(output),sort_keys=True,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':output['status'],'passed':output['passed'],'failed':output['failed'],
        'failures':[row for row in output['tests'] if row['status']=='fail']},sort_keys=True))
    return 0 if output['status']=='pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
