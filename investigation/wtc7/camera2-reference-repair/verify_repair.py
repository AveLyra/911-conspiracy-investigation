"""Independent verification for the one-reference Camera 2 repair.

Numerical audits import only the frozen reviewer's oracles. The optional bounded
tamper test calls the actual wrapper entry with a sentinel forbidding later-frame
analysis. Completed scopes must be explicitly released before review.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import shutil

import numpy as np
import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
V1 = HERE.parent/'reference-motion'
BASE = HERE.parent/'multiview-onset-review'
ROOT = HERE.parents[2]
SUBJECT_SHA = 'adb48c18a928ab44bba0f30cc8b6cdffbdd3a60918464600a568249b7822640e'
ORACLE_SHA = 'b19d4692706e47f29ce9356342c12dcd6821c21dd7124de58d6570f38cc1ed0f'
FIT_ORACLE_SHA = 'e2bb15bb6dfc9317b51db40602e53191570c888205cf26640c0b40197340c912'
RETAINED = ('C2-R1','C2-R2','C2-R4','C2-R5','C2-R6')
MODELS = ('translation','similarity','affine')
HALVES = (9,13)
EVALUATIONS = (6593,6654,6751,6931,7013,7104)


def require(condition,label):
    if not condition:
        raise AssertionError(label)


def fp(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':path.stat().st_size,'sha256':digest}


def read_json(path):
    def invalid(value):
        raise ValueError('nonfinite JSON token')
    return json.loads(path.read_text(),parse_constant=invalid)


def load_oracles():
    require(fp(V1/'measure.py')['sha256']==SUBJECT_SHA,'frozen v1 subject changed')
    require(fp(V1/'verify.py')['sha256']==ORACLE_SHA,'frozen v1 verifier changed')
    require(fp(V1/'independent_tests.py')['sha256']==FIT_ORACLE_SHA,'frozen independent fit dependency changed')
    sys.path.insert(0,str(V1))
    spec = importlib.util.spec_from_file_location('frozen_reference_review',V1/'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_single_replacement(config,original):
    require(config['half_widths']==[9,13] and config['radius']==24,'frozen matching parameters')
    features = config['camera2']
    require(len(features)==6 and len({row['id'] for row in features})==6,'six unique reference IDs')
    expected_order = ['C2-R1','C2-R2',features[2]['id'],'C2-R4','C2-R5','C2-R6']
    require([row['id'] for row in features]==expected_order,'reference order')
    require(features[2]['id'] in ('C2-R7','C2-R8','C2-R9'),'replacement new ID')
    for old,new in zip(original['camera2'],features):
        if old['id'] != 'C2-R3':
            require(new==old,'retained reference configuration changed')
        require(len(new['xy'])==2 and all(type(value) is int for value in new['xy']),'integer reference centers')
    return features[2]['id']


def input_arrays(baseline_only=False):
    manifest_path = BASE/'refine01/camera2/selection.json'
    require(fp(manifest_path)['sha256']=='dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e','original Camera 2 selection pin')
    manifest = read_json(manifest_path)
    refinement_path = BASE/'refinement.json'
    require(fp(refinement_path)['sha256']=='700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a','frozen refinement declaration')
    wanted = read_json(refinement_path)['rules']['camera2']['groups']['event']
    rows = [row for row in manifest['images'] if int(row['frame_index_zero_based']) in wanted]
    require(len(rows)==71 and [int(row['frame_index_zero_based']) for row in rows]==wanted,'same 71 declared Camera 2 frames')
    prior_paths = {
        BASE/'refine01/receipt.json':'c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503',
        V1/'features.json':'19ab4b1cd47e51a93e757efae5faf5281c68125855dd5b64fa3724053f4e89b2',
    }
    arrays,pins = [],{str(manifest_path):fp(manifest_path),str(refinement_path):fp(refinement_path)}
    for path,digest in prior_paths.items():
        require(fp(path)['sha256']==digest,'previous source/configuration pin')
        pins[str(path)] = fp(path)
    allowed = {
        ROOT/'research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov',
        HERE.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv',
        HERE.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frames.json',
        HERE.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/source-identity.json',
    }
    source_pins = {ROOT/name:identity for name,identity in manifest['input_pins'].items()}
    require(set(source_pins)==allowed,'original source/map pin scope')
    for path,identity in source_pins.items():
        require(fp(path)==identity,'original source/map integrity')
        pins[str(path)] = identity
    if baseline_only:
        rows = rows[:1]
    previous = None
    for row in rows:
        index = int(row['frame_index_zero_based'])
        require(row['png']==f'f{index:06d}.png','native input filename')
        path = manifest_path.parent/row['png']
        require(fp(path)==row['png_identity'],'native PNG identity')
        with Image.open(path) as image:
            require(image.format=='PNG' and image.mode=='L' and image.size==(640,480),'native Camera 2 geometry/mode')
            array = np.array(image)
        require(hashlib.sha256(array.tobytes()).hexdigest()==row['luma_sha256'],'native luma identity')
        exact = Fraction(row['source_time_seconds_exact'])
        require(exact==int(row['source_pts'])*Fraction(row['source_time_base']),'exact input PTS')
        require(previous is None or exact>previous,'strict input PTS order')
        previous = exact
        pins[str(path)] = fp(path)
        arrays.append(array)
    return rows,arrays,pins


def historical_rows(scope,config,oracles,rows,arrays):
    original = read_json(V1/'run01/features.json')
    replacement = validate_single_replacement(config,original)
    old_rows = [row for row in read_json(V1/'run01/matches.json') if row['camera']=='camera2']
    old_map = {(row['index'],row['half'],row['reference']):row for row in old_rows}
    matches = read_json(scope/'matches.json')
    transforms = read_json(scope/'transforms.json')
    require(len(matches)==852 and len(transforms)==426,'complete repair row counts')
    features = config['camera2']
    match_keys = [(row['index'],row['half'],row['reference']) for row in matches]
    model_keys = [(row['index'],row['half'],row['model']) for row in transforms]
    expected_match_order = [(int(row['frame_index_zero_based']),half,feature['id']) for row in rows for half in HALVES for feature in features]
    expected_model_order = [(int(row['frame_index_zero_based']),half,model) for row in rows for half in HALVES for model in MODELS]
    require(match_keys==expected_match_order and len(set(match_keys))==852,'frame-major repair match ordering')
    require(model_keys==expected_model_order and len(set(model_keys))==426,'frame-major repair model ordering')
    match_lookup = dict(zip(match_keys,matches))
    model_lookup = dict(zip(model_keys,transforms))
    points = np.array([feature['xy'] for feature in features],float)
    cursor = model_cursor = unchanged = new_grids = values = computed = folds = 0
    maximum_error = 0.
    expected_keys = []
    counts,flags = Counter(),Counter()
    differences,near = [],[]
    with np.load(scope/'score-grids.npz',allow_pickle=False) as grids, np.load(V1/'run01/score-grids.npz',allow_pickle=False) as old_grids:
        for half in HALVES:
            templates = []
            for feature in features:
                x,y = feature['xy']
                template = arrays[0][y-half:y+half+1,x-half:x+half+1]
                require(template.shape==(2*half+1,2*half+1),'fixed baseline template support')
                templates.append(template)
            for stamp,frame in zip(rows,arrays):
                index = int(stamp['frame_index_zero_based'])
                current = []
                for feature,template in zip(features,templates):
                    row = match_lookup[(index,half,feature['id'])]
                    cursor += 1
                    key = f'camera2_{index}_{half}_{feature["id"]}'
                    expected_keys.append(key)
                    metadata = {'camera':'camera2','index':index,'pts':stamp['source_pts'],
                        'time_base':stamp['source_time_base'],'seconds_exact':stamp['source_time_seconds_exact'],
                        'half':half,'reference':feature['id'],'baseline_xy':feature['xy'],'score_grid':key}
                    require(all(row.get(name)==value for name,value in metadata.items()),'repair row order/metadata')
                    score = grids[key]
                    if feature['id'] in RETAINED:
                        require(row==old_map[(index,half,feature['id'])],'unchanged reference record differs from v1')
                        before = old_grids[key]
                        require(score.dtype==before.dtype and score.shape==before.shape and score.tobytes()==before.tobytes(),'unchanged complete score grid differs from v1')
                        unchanged += 1
                    else:
                        expected,bounds,std = oracles.fft_scores(frame,template,feature['xy'])
                        require(score.shape==expected.shape and np.array_equal(np.isnan(score),np.isnan(expected)),'replacement grid shape/undefined mask')
                        finite = np.isfinite(score)
                        error = float(np.max(np.abs(score[finite]-expected[finite]))) if finite.any() else 0.
                        require(error<=1e-8,'replacement full independent NCC grid')
                        maximum_error = max(maximum_error,error)
                        values += score.size
                        new_grids += 1
                        derived = oracles.derive_match(score,bounds,std)
                        require(set(row)==set(metadata)|set(derived),'replacement match schema')
                        for name,value in derived.items():
                            if name=='template_std':
                                oracles.close(row[name],value,'replacement seed std',atol=1e-12)
                            else:
                                require(row[name]==value,'replacement grid-derived '+name)
                        alternate = oracles.derive_match(expected,bounds,std)
                        changed = [name for name in ('candidate_xy','competitor_xy','tied_best_count','flags','status') if derived.get(name)!=alternate.get(name)]
                        if changed:
                            differences.append({'grid':key,'fields':changed,'stored':derived,'independent':alternate})
                        if 'ncc' in derived and (abs(derived['ncc']-.8)<=1e-8 or (derived['margin'] is not None and abs(derived['margin']-.02)<=2e-8)):
                            near.append({'grid':key,'ncc':derived['ncc'],'margin':derived['margin']})
                    counts[f'side{2*half+1}/{feature["id"]}/{row["status"]}'] += 1
                    for flag in row['flags']:
                        flags[f'side{2*half+1}/{feature["id"]}/{flag}'] += 1
                    current.append(row)
                failed = [row['reference'] for row in current if row['status']!='candidate']
                for model in MODELS:
                    row = model_lookup[(index,half,model)]
                    model_cursor += 1
                    metadata = {'camera':'camera2','index':index,'half':half,'model':model,
                        'seconds_exact':stamp['source_time_seconds_exact'],'reference_order':[feature['id'] for feature in features]}
                    require(all(row.get(name)==value for name,value in metadata.items()),'repair model order/metadata')
                    if failed:
                        require(row==dict(metadata,status='reference_quality_failure',passes_consistency_screen=False,failed_references=failed),'repair all-six admission')
                    else:
                        outcome = oracles.audit_fit(row,points,np.array([item['candidate_xy'] for item in current],float),model)
                        if outcome['computed']:
                            computed += 1
                            folds += 6
                        if outcome['threshold_near']:
                            targets = np.array([item['candidate_xy'] for item in current],float)
                            near.append({'model':f'{index}/{half}/{model}',
                                'arithmetic_audit':threshold_arithmetic(row,points,targets,model,oracles)})
                    counts[f'side{2*half+1}/{model}/{row["status"]}'] += 1
                    if row['passes_consistency_screen']:
                        counts[f'side{2*half+1}/{model}/passes_consistency_screen'] += 1
        require(set(grids.files)==set(expected_keys) and len(expected_keys)==len(set(expected_keys))==852,'complete repair grid keys')
    require(cursor==852 and model_cursor==426 and unchanged==710 and new_grids==142,'final repair coverage')
    return {'replacement_id':replacement,'unchanged_records_and_grids_exactly_equal_to_v1':unchanged,
        'replacement_grids_independently_recomputed':new_grids,'replacement_grid_values':values,
        'max_independent_NCC_difference':maximum_error,'match_rows_checked':cursor,'model_rows_checked':model_cursor,
        'admitted_models_recomputed':computed,'LOO_folds_recomputed':folds,'counts':dict(counts),'flags':dict(flags),
        'independent_grid_decision_differences':differences,'near_thresholds':near}


def threshold_arithmetic(row,points,targets,model,oracles):
    """Report floating decision sensitivity without changing any stored gate."""
    whole = oracles.independent_fit(points,targets,model)
    errors,positive = [],[]
    for index in range(6):
        keep = np.arange(6)!=index
        fit = oracles.independent_fit(points[keep],targets[keep],model)
        require(fit['status']=='computed','near-boundary LOO rank')
        error = targets[index]-(points[index]@fit['matrix'].T+fit['offset'])
        errors.append(float(np.sqrt(error@error)))
        positive.append(bool(fit['positive_nonsingular']))
    independent_screen = bool(whole['positive_nonsingular'] and all(positive) and whole['max_residual']<=2 and max(errors)<=2)
    result = {'scope':'Post-result arithmetic sensitivity of the unchanged exact 2-pixel screen; not a revised threshold.',
        'stored_max_residual':row['max_residual'],'stored_max_loo':row['max_loo_error'],
        'stored_screen':row['passes_consistency_screen'],'independent_max_residual':whole['max_residual'],
        'independent_loo_norms':errors,'independent_screen':independent_screen}
    changed = np.flatnonzero(np.any(points!=targets,axis=1))
    if len(changed)==1 and np.equal(points,np.rint(points)).all() and np.equal(targets,np.rint(targets)).all():
        omitted = int(changed[0])
        keep = points[np.arange(6)!=omitted].astype(int)
        a,b,c = keep[:3]
        area = int((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
        if area!=0:
            exact_error = (targets[omitted]-points[omitted]).astype(int).tolist()
            result['exact_identity_fold'] = {'omitted_reference':omitted,'five_retained_pairs_identical':True,
                'integer_twice_area_of_three_retained_points':area,'error_xy':exact_error,
                'squared_error_norm':sum(value*value for value in exact_error),
                'reason':'Three noncollinear identical point pairs identify the identity affine map; the translation and proper-similarity identity maps are likewise unique. This exact fold error does not depend on floating solver rounding.'}
    return result


def inventory(scope,stage,input_pins,preflight=None):
    require(scope.parent==HERE and scope.is_dir(),'released scope must be a direct local child')
    require(scope.resolve()==scope,'released scope must not alias another directory')
    require(not (scope/'failure.json').exists(),'failed scope cannot be accepted')
    receipt = read_json(scope/'receipt.json')
    require(receipt['stage']==stage and receipt['status']=='complete','completed stage receipt')
    listed = receipt['products']
    require(all(path.is_file() for path in scope.iterdir()),'unexpected nested stage product')
    require({path.name for path in scope.iterdir()}==set(listed)|{'receipt.json'},'exact stage inventory')
    for name,identity in listed.items():
        require(Path(name).name==name and fp(scope/name)==identity,'stage product integrity')
    procedure = [HERE/'repair.py',HERE/'PROTOCOL.md',HERE/'candidate-seeds.json',HERE/'test_repair.py',V1/'measure.py']
    if stage!='prepare':
        procedure.append(HERE/'visual-review.json')
    expected_names = {f'snapshot-{index}-{path.name}' for index,path in enumerate(procedure)}|{'initial.json','input-pins.json'}
    if stage=='preflight':
        expected_names |= {'baseline-scores.json','baseline-grids.npz','selection.json'}
    elif stage=='run':
        expected_names |= {'preflight-receipt.json','preflight-selection.json','matches.json','transforms.json','score-grids.npz'}
        expected_names |= {f'overlay-{index}-{half}.png' for index in EVALUATIONS for half in HALVES}
    require(set(listed)==expected_names,'declared exact product names/count')
    initial = read_json(scope/'initial.json')
    expected_procedure = {str(path):fp(path) for path in procedure+[Path(sys.executable)]}
    require(initial['stage']==stage and initial['pins']==expected_procedure,'stage initial procedure/runtime pins')
    require((initial['python'],initial['numpy'],initial['pillow'])==(sys.version,np.__version__,PIL.__version__),'recorded runtime versions')
    for index,path in enumerate(procedure):
        require(fp(scope/f'snapshot-{index}-{path.name}')==expected_procedure[str(path)],'stage source snapshot')
    expected_all = dict(expected_procedure,**input_pins)
    parent_pin_spellings = {}
    if stage=='run':
        require(preflight is not None,'explicit parent preflight')
        for name in ('receipt.json','selection.json'):
            path = preflight/name
            allowed_spellings = {str(path),str(path.relative_to(ROOT))}
            recorded = allowed_spellings & set(receipt['pins'])
            require(len(recorded)==1,'one exact absolute or repository-relative parent pin')
            spelling = next(iter(recorded))
            parent_pin_spellings[name] = spelling
            expected_all[spelling] = fp(path)
            require(fp(scope/f'preflight-{name}')==expected_all[spelling],'run parent-preflight snapshot')
    require(receipt['pins']==expected_all,'complete stage input/procedure lineage')
    require(read_json(scope/'input-pins.json')==input_pins,'complete stage input pin inventory')
    return receipt,{'stage':stage,'scope':scope.name,'receipt':fp(scope/'receipt.json'),
        'listed_products':len(listed),'files_including_receipt':len(listed)+1,
        'initial_procedure_pins':expected_procedure,'parent_pin_spellings':parent_pin_spellings,
        'runtime':{key:initial[key] for key in ('python','numpy','pillow')}}


def baseline_review(scope,oracles,frame):
    candidate_path = HERE/'candidate-seeds.json'
    declaration = read_json(candidate_path)
    baseline = declaration['baseline']
    baseline_path = BASE/'refine01/camera2/f006593.png'
    baseline_stamp = next(row for row in read_json(BASE/'refine01/camera2/selection.json')['images'] if int(row['frame_index_zero_based'])==6593)
    require(baseline['camera']=='camera2' and baseline['source_id']=='VID-WTC7-001' and baseline['index']==6593,'declared baseline identity')
    require((HERE/baseline['path']).resolve()==baseline_path and baseline['sha256']==fp(baseline_path)['sha256'],'declared baseline path/hash')
    require(baseline['source_time_seconds_exact']==baseline_stamp['source_time_seconds_exact'] and baseline['mode']=='L' and baseline['stored_size']==[640,480],'declared baseline PTS/mode/geometry')
    candidates = declaration['candidates']
    require(1<=len(candidates)<=3,'bounded candidate count')
    require([row['id'] for row in candidates]==['C2-R7','C2-R8','C2-R9'][:len(candidates)],'ordered candidate IDs')
    for candidate in candidates:
        require(isinstance(candidate['xy'],list) and len(candidate['xy'])==2 and all(type(value) is int for value in candidate['xy']),'candidate coordinate contract')
        require(13<=candidate['xy'][0]<627 and 13<=candidate['xy'][1]<467,'candidate both-size support')
        require(isinstance(candidate['description'],str) and candidate['description'].strip(),'candidate description')
        x,y = candidate['xy']
        require(candidate['template_bounds_inclusive_xyxy']=={str(2*half+1):[x-half,y-half,x+half,y+half] for half in HALVES},'declared native template bounds')
    visual_path = HERE/'visual-review.json'
    visual = read_json(visual_path)
    require(visual['review_kind']=='computational_baseline_visual_check_not_human','explicit computational visual-review kind')
    require(visual['candidate_file']==fp(candidate_path),'visual candidate-file pin')
    require(set(visual['candidate_acceptance'])=={row['id'] for row in candidates} and all(type(value) is bool for value in visual['candidate_acceptance'].values()),'visual review complete boolean dispositions')
    original = read_json(V1/'features.json')
    retained = [row for row in original['camera2'] if row['id']!='C2-R3']
    features = retained+candidates
    records = read_json(scope/'baseline-scores.json')
    expected_order = [(feature['id'],half) for feature in features for half in HALVES]
    require([(row['reference'],row['half']) for row in records]==expected_order,'complete ordered preflight score records')
    maximum = 0.
    differences = []
    keys = []
    with np.load(scope/'baseline-grids.npz',allow_pickle=False) as grids:
        for feature in features:
            x,y = feature['xy']
            for half in HALVES:
                key = f'{feature["id"]}_{half}'
                keys.append(key)
                row = next(row for row in records if (row['reference'],row['half'])==(feature['id'],half))
                template = frame[y-half:y+half+1,x-half:x+half+1]
                expected,bounds,std = oracles.fft_scores(frame,template,feature['xy'])
                scores = grids[key]
                require(scores.shape==expected.shape and np.array_equal(np.isnan(scores),np.isnan(expected)),'preflight full-grid shape/mask')
                finite = np.isfinite(scores)
                error = float(np.max(np.abs(scores[finite]-expected[finite]))) if finite.any() else 0.
                require(error<=1e-8,'preflight full independent NCC grid')
                maximum = max(maximum,error)
                derived = oracles.derive_match(scores,bounds,std)
                require(set(row)==set(derived)|{'reference','half','baseline_xy'},'preflight score schema')
                require(row['baseline_xy']==feature['xy'],'preflight coordinate association')
                for name,value in derived.items():
                    if name=='template_std':
                        oracles.close(row[name],value,'preflight template std',atol=1e-12)
                    else:
                        require(row[name]==value,'preflight recorded grid-derived '+name)
                alternate = oracles.derive_match(expected,bounds,std)
                changed = [name for name in ('candidate_xy','competitor_xy','tied_best_count','flags','status') if derived.get(name)!=alternate.get(name)]
                if changed:
                    differences.append({'grid':key,'fields':changed})
        require(set(grids.files)==set(keys),'exact preflight grid inventory')
    require(all(row['status']=='candidate' for row in records if row['reference'] in RETAINED),'all retained baseline references pass')
    allowed = [candidate['id'] for candidate in candidates if visual['candidate_acceptance'][candidate['id']] and all(row['status']=='candidate' for row in records if row['reference']==candidate['id'])]
    chosen = allowed[0] if allowed else None
    selection = read_json(scope/'selection.json')
    require(selection['selected']==chosen,'first ordered jointly qualified candidate')
    if chosen is None:
        require(selection=={'status':'no_candidate_qualified','selected':None},'bounded no-qualified-candidate record')
        config = None
    else:
        require(selection['status']=='selected_baseline_only_not_validated_track','baseline-only selection label')
        require(selection['visual_review']==fp(visual_path) and selection['candidate_file']==fp(candidate_path),'selection parent hashes')
        replacement = next(row for row in candidates if row['id']==chosen)
        expected_features = [replacement if row['id']=='C2-R3' else row for row in original['camera2']]
        require(selection['features']==expected_features,'exact chosen candidate object and retained references')
        config = {'camera2':selection['features'],'half_widths':selection['half_widths'],'radius':selection['radius']}
        require(validate_single_replacement(config,original)==chosen,'selected configuration contract')
    return config,{'candidate_file':fp(candidate_path),'visual_review':fp(visual_path),
        'candidate_ids_in_order':[row['id'] for row in candidates],'qualified_ids_in_order':allowed,'selected':chosen,
        'full_preflight_grids_recomputed':len(keys),'max_independent_NCC_difference':maximum,
        'independent_grid_decision_differences':differences,
        'baseline_records':records,'interpretation':'Baseline construction-image suitability; not physical identity/stationarity or later-frame accuracy.'}


def prior_integrity():
    path = V1/'run01/receipt.json'
    require(fp(path)['sha256']=='3e84b93f588ba329a122ee6ac8ef0ac7daf67a9ba6451503c75ff968682eaf17','frozen v1 run receipt')
    receipt = read_json(path)
    for name,identity in receipt['products'].items():
        require(Path(name).name==name and fp(path.parent/name)==identity,'unchanged v1 result product')
    return {'receipt':fp(path),'products_rehashed':len(receipt['products'])}


def overlay_pixels(scope,stamps,arrays):
    matches = read_json(scope/'matches.json')
    checked = 0
    for stamp,array in zip(stamps,arrays):
        index = int(stamp['frame_index_zero_based'])
        if index not in EVALUATIONS:
            continue
        for half in HALVES:
            expected = Image.new('RGB',(640,514),'white')
            expected.paste(Image.fromarray(array).convert('RGB'),(0,0))
            draw = ImageDraw.Draw(expected)
            for row in matches:
                if row['index']!=index or row['half']!=half or 'candidate_xy' not in row:
                    continue
                x,y = row['candidate_xy']
                color = 'lime' if row['status']=='candidate' else 'red'
                draw.rectangle((x-4,y-4,x+4,y+4),outline=color)
                draw.text((x+5,y),row['reference'],fill=color)
            draw.text((4,482),f'Camera2 repair frame {index}, half {half}',fill='black')
            draw.text((4,497),'ANALYTICAL DERIVATIVE; candidates are not physical tracks',fill='black')
            with Image.open(scope/f'overlay-{index}-{half}.png') as actual:
                require(actual.format=='PNG' and actual.mode=='RGB' and actual.size==expected.size,'overlay format/geometry')
                require(actual.tobytes()==expected.tobytes(),'all overlay source/marker/label/footer pixels')
            checked += 1
    require(checked==12,'declared overlay coverage')
    return {'fully_reconstructed_overlays':checked,'meaning':'Checks rendering lineage, not visual material-point identity.'}


def tampered_entry(preflight,fixture_name,failure_name):
    """Actual file-level mutation, with later-frame analysis forbidden."""
    fixture = HERE/fixture_name
    failure = HERE/failure_name
    require(fixture.parent==HERE and fixture.name.startswith('preflight-tamper'),'tamper fixture scope')
    require(failure.parent==HERE and failure.name.startswith('verification-failure'),'negative output scope')
    require(not fixture.exists() and not failure.exists(),'preserve prior tamper attempts')
    parent_before = fp(preflight/'receipt.json')
    procedure_before = fp(HERE/'repair.py')
    shutil.copytree(preflight,fixture)
    selection = read_json(fixture/'selection.json')
    original_xy = list(selection['features'][2]['xy'])
    selection['features'][2]['xy'][0] += 1
    (fixture/'selection.json').write_text(json.dumps(selection,indent=2,sort_keys=True,allow_nan=False)+'\n')
    receipt = read_json(fixture/'receipt.json')
    receipt['products']['selection.json'] = fp(fixture/'selection.json')
    (fixture/'receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n')
    require(all(fp(fixture/name)==identity for name,identity in receipt['products'].items()),'tamper products internally rehashed')
    spec = importlib.util.spec_from_file_location('repair_negative_contract_subject',HERE/'repair.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    later_calls = []
    def forbid_later(*args,**kwargs):
        later_calls.append(True)
        raise RuntimeError('negative test reached forbidden historical frame analysis')
    module.frame_analysis = forbid_later
    try:
        module.execute('run',failure,fixture)
    except ValueError as error:
        require(str(error)=='exact-approved-reference-set','wrong actual tamper-entry rejection')
    else:
        raise AssertionError('actual tampered selection accepted')
    require(not later_calls,'later-frame analysis was called')
    error_record = read_json(failure/'failure.json')
    require(error_record=={'stage':'run','exception_type':'ValueError','message':'exact-approved-reference-set'},'preserved exact tamper failure')
    require(not any((failure/name).exists() for name in ('matches.json','transforms.json','score-grids.npz','receipt.json')),'tamper produced accepted historical outputs')
    require(not list(failure.glob('overlay-*.png')),'tamper produced historical overlays')
    require(fp(preflight/'receipt.json')==parent_before and fp(HERE/'repair.py')==procedure_before,'negative control changed legitimate preflight/procedure')
    return {'scope':'Actual execute run-entry with copied selection and rehashed receipt, not only a pure-function mutation; frame-analysis sentinel prevents any later-frame scoring.',
        'procedure':procedure_before,'original_preflight_receipt':parent_before,
        'fixture':fixture.name,'fixture_receipt':fp(fixture/'receipt.json'),
        'mutation':{'field':'features[2].xy[0]','original_xy':original_xy,'altered_xy':selection['features'][2]['xy']},
        'historical_frame_analysis_calls':len(later_calls),'failure_scope':failure.name,'failure':error_record,
        'failure_products':{path.name:fp(path) for path in sorted(failure.iterdir()) if path.is_file()},
        'status':'pass'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preflight',required=True)
    parser.add_argument('--runs',nargs=2)
    parser.add_argument('--tamper-contract',nargs=2,metavar=('FIXTURE','FAILURE_OUTPUT'))
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    output_path = args.out.absolute()
    require(output_path.parent==HERE and output_path.name.startswith('verification') and output_path.suffix=='.json','verification output scope')
    require(not output_path.exists(),'preserve previous verification receipts')
    result = {'verifier':fp(Path(__file__)),'python':platform.python_version(),'numpy':np.__version__,'pillow':PIL.__version__,
        'command':sys.argv,'frozen_subject_sha256':SUBJECT_SHA,'frozen_oracle_sha256':ORACLE_SHA,
        'frozen_fit_oracle_sha256':FIT_ORACLE_SHA,
        'scope':'Independent one-reference repair artifact and numerical review; no video decode or physical/causal validation.'}
    try:
        oracles = load_oracles()
        result['v1_preservation'] = prior_integrity()
        preflight = (HERE/args.preflight).absolute()
        _,baseline_arrays,baseline_pins = input_arrays(baseline_only=True)
        _,result['preflight_inventory'] = inventory(preflight,'preflight',baseline_pins)
        config,result['preflight_numerics'] = baseline_review(preflight,oracles,baseline_arrays[0])
        if args.tamper_contract:
            require(not args.runs,'negative control is separate from accepted historical review')
            result['actual_file_level_tamper_contract'] = tampered_entry(preflight,*args.tamper_contract)
        if args.runs:
            require(config is not None,'cannot verify historical run without qualified baseline reference')
            scopes = [(HERE/name).absolute() for name in args.runs]
            require(len({scope.resolve() for scope in scopes})==2,'two distinct historical run directories required')
            rows,arrays,pins = input_arrays()
            stages = [inventory(scope,'run',pins,preflight) for scope in scopes]
            result['historical_inventories'] = [entry[1] for entry in stages]
            require(stages[0][0]==stages[1][0] and fp(scopes[0]/'receipt.json')==fp(scopes[1]/'receipt.json'),'repeat-stage receipt identity')
            result['reproduction'] = {'all_files_byte_identical':True,'receipt_listed_products':len(stages[0][0]['products']),
                'files_including_receipt':len(stages[0][0]['products'])+1,'numerics_checked_on_first_identical_copy':True}
            result['historical_numerics'] = historical_rows(scopes[0],config,oracles,rows,arrays)
            result['overlay_integrity'] = overlay_pixels(scopes[0],rows,arrays)
            require(all(fp(Path(path))==identity for path,identity in pins.items()),'post-verification input pins')
        else:
            result['historical_status'] = 'not_read_or_reviewed'
        require(fp(V1/'measure.py')['sha256']==SUBJECT_SHA and fp(V1/'verify.py')['sha256']==ORACLE_SHA,'post-verification frozen algorithms')
        require(fp(V1/'independent_tests.py')['sha256']==FIT_ORACLE_SHA,'post-verification frozen fit oracle')
        result['status'] = 'pass'
    except Exception as error:
        result.update(status='fail',error_type=type(error).__name__,error=str(error))
    with output_path.open('x') as stream:
        stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({key:result[key] for key in ('status','error_type','error','historical_status') if key in result},sort_keys=True))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':
    raise SystemExit(main())
