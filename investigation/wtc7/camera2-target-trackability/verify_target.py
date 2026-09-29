"""Independent presentation, synthetic geometry and released-result checks.

Presentation reconstruction never imports present.py. The optional reviewed
numerical subject is exercised only on synthetic inputs. Historical verification
uses the separate Fraction/closed-form oracle, never the producer implementation.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform

import numpy as np
import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MEDIA = HERE.parent/'multiview-onset-review'
FRAMES = (6593,6654,6751,6841,6886,6916,6931,6946,6961,6976,6991,7006,7021,7036,7051,7081,7104)
PROTOCOL_SHA = 'a5c8382402a1afec577b6e1d3c862b0d1a4bd4bac0f5511d5983547686eaf934'
EARLIER_REVIEWED_PROTOCOL_SHA = 'b3cd1d4dc5c9cc8acb4da999bb0b8315bb98ff0df1b79318476f45b24e9766a5'
PRESENT_SHA = 'a4b3ca69b2d8704b9f799bd009136fdac91bd32c5c9227c07a4c906a02f3df5c'
RELEASE_SHA = '8331cdcffc3b4c1d3eeecac8c85361e05d7026b4310dafd3d932635a6970bcde'
SELECTION_SHA = 'bd87f75f8a0677aa9e8edbf62d0f868eb341088d838c6ec3e3358f36f897190c'
CONTRACT_SHA = '0e723d512950d37b1aa28238d8d4e209c7b2c1e2c74675b262cd8d6d7a39bdae'
ANALYZE_SHA = 'ac495eecb98845cf5a11cd6d27161cd051ea367cc7cb6a9e186b57329ef10ed6'
REFERENCE_SHA = 'd2b8ae21b6fe3b0190538142b1db37be9f5a31b80d581d5ac6c39e90a952f320'
PRESENT_RECEIPT_SHA = '7ca7abe5bc9d67511213a627a5ae65b1e506952b88896f780779d5fbf7c63f29'
ANNOTATION_SHAS = {'root-annotations.json':'1a6e6b4dc0b34b9f0e33746cc6a568c137311e65493c7e612cd5fa3f3eb72e0f',
    'annotator-annotations.json':'885b9ca6ef2d762efe44ada1572e56962f81e7e53452f903471949c8e3eeeb2a'}
TARGETS = ('C2-T1','C2-T2')
MODELS = ('translation','similarity','affine')


def require(condition,label):
    if not condition:
        raise AssertionError(label)


def fp(path):
    with path.open('rb') as stream:
        return {'bytes':path.stat().st_size,'sha256':hashlib.file_digest(stream,'sha256').hexdigest()}


def read_json(path):
    def invalid(value):
        raise ValueError('nonfinite JSON token')
    return json.loads(path.read_text(),parse_constant=invalid)


def source_inputs(source_root=None):
    source_root = ROOT if source_root is None else source_root
    media = source_root/'research/sherlock-wtc7-investigation/multiview-onset-review'
    declared = {
        media/'refine01/camera2/selection.json':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e',
        media/'refinement.json':'700d1b1dfd5a6008e1def0ee82f8cbfd42d4dc9e8a9cfea922f7f2c802ae213a',
        media/'refine01/receipt.json':'c90814c0fbb7d08c5663b29b7dcdee679c812ebc984814f02636ae1d0f0c4503',
    }
    pins = {str(path):fp(path) for path in declared}
    require(all(pins[str(path)]['sha256']==digest for path,digest in declared.items()),'frozen source declarations')
    manifest = read_json(media/'refine01/camera2/selection.json')
    event = read_json(media/'refinement.json')['rules']['camera2']['groups']['event']
    require(len(event)==71 and len(set(FRAMES))==17 and set(FRAMES)<=set(event),'declared 17-of-71 frame subset')
    allowed = {
        source_root/'research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov',
        media.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frame-map.csv',
        media.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/frames.json',
        media.parent/'timing-audit/run-2026-09-08-v1.1/VID-WTC7-001/source-identity.json',
    }
    source_pins = {source_root/path:identity for path,identity in manifest['input_pins'].items()}
    require(set(source_pins)==allowed,'exact original source/map scope')
    for path,identity in source_pins.items():
        require(fp(path)==identity,'original source/map byte identity')
        pins[str(path)] = identity
    rows = [row for row in manifest['images'] if int(row['frame_index_zero_based']) in FRAMES]
    require(tuple(int(row['frame_index_zero_based']) for row in rows)==FRAMES,'exact presentation frame order')
    arrays,previous = [],None
    for row in rows:
        index = int(row['frame_index_zero_based'])
        require(row['png']==f'f{index:06d}.png','native frame name')
        path = media/'refine01/camera2'/row['png']
        require(fp(path)==row['png_identity'],'native PNG byte identity')
        with Image.open(path) as image:
            require(image.format=='PNG' and image.mode=='L' and image.size==(640,480),'native PNG mode/geometry')
            array = np.array(image)
        require(array.dtype==np.uint8 and array.shape==(480,640),'native luma array')
        require(hashlib.sha256(array.tobytes()).hexdigest()==row['luma_sha256'],'native luma identity')
        exact = Fraction(row['source_time_seconds_exact'])
        require(exact==int(row['source_pts'])*Fraction(row['source_time_base']),'exact source PTS')
        require(previous is None or exact>previous,'strict source PTS order')
        previous = exact
        pins[str(path)] = fp(path)
        arrays.append(array)
    return rows,arrays,pins


def inventory(scope,stage,source_pins):
    require(scope.parent==HERE and scope.resolve()==scope and scope.is_dir(),'direct non-aliased presentation scope')
    require(not (scope/'failure.json').exists(),'failed stage cannot be accepted')
    receipt = read_json(scope/'receipt.json')
    require(receipt['stage']==stage and receipt['status']=='complete','completed stage receipt')
    expected = {'present.py','PROTOCOL.md','initial.json','detail.json'}
    if stage=='prepare':
        expected |= {'input-pins.json'}|{f'f{index:06d}-target-panel.png' for index in FRAMES}
    else:
        require(stage=='controls','known stage')
        expected |= {'synthetic-source.png','synthetic-panel.png'}
    require(set(receipt['products'])==expected,'exact declared presentation product inventory')
    require(all(path.is_file() for path in scope.iterdir()),'no nested unexpected stage products')
    require({path.name for path in scope.iterdir()}==expected|{'receipt.json'},'exact stage filesystem inventory')
    for name,identity in receipt['products'].items():
        require(fp(scope/name)==identity,'stage product byte identity')
    procedure = {str(path):fp(path) for path in (HERE/'present.py',HERE/'PROTOCOL.md',Path(sys.executable))}
    require(procedure[str(HERE/'present.py')]['sha256']==PRESENT_SHA,'frozen presentation source')
    require(procedure[str(HERE/'PROTOCOL.md')]['sha256']==PROTOCOL_SHA,'frozen presentation protocol')
    if stage=='controls':
        recorded_protocol = fp(scope/'PROTOCOL.md')
        require(recorded_protocol['sha256'] in (PROTOCOL_SHA,EARLIER_REVIEWED_PROTOCOL_SHA),'known reviewed control protocol version')
        procedure[str(HERE/'PROTOCOL.md')] = recorded_protocol
    for name in ('present.py','PROTOCOL.md'):
        require(fp(scope/name)==procedure[str(HERE/name)],'procedure snapshots')
    initial = read_json(scope/'initial.json')
    require(initial['stage']==stage and initial['pins']==procedure,'exact initial procedure/runtime pins')
    require((initial['python'],initial['numpy'],initial['pillow'])==(sys.version,np.__version__,PIL.__version__),'recorded runtime identity')
    final = dict(procedure,**source_pins) if stage=='prepare' else procedure
    require(receipt['pins']==final,'exact final source/procedure pin union')
    if stage=='prepare':
        require(read_json(scope/'input-pins.json')==source_pins,'complete source pin inventory')
    return {'scope':scope.name,'receipt':fp(scope/'receipt.json'),'listed_products':len(expected),
        'files_including_receipt':len(expected)+1,'procedure':procedure,'runtime':{name:initial[name] for name in ('python','numpy','pillow')}},receipt


def independent_panel(array,title):
    # NumPy cell replication is independent of the producer's PIL crop/resize.
    crop = array[95:400,270:475]
    expanded = np.repeat(np.repeat(crop,3,axis=0),3,axis=1)
    if expanded.ndim==2:
        expanded = np.repeat(expanded[:,:,None],3,axis=2)
    require(expanded.shape==(915,615,3),'independent crop/scale geometry')
    canvas = np.full((983,665,3),255,dtype=np.uint8)
    canvas[28:943,40:655] = expanded
    result = Image.fromarray(canvas)
    draw = ImageDraw.Draw(result)
    for x in range(270,475,10):
        u = 40+3*(x-270)
        draw.line((u,24,u,27),fill='black')
        draw.text((u-8,11),str(x),fill='black')
    for y in range(100,400,10):
        v = 28+3*(y-95)
        draw.line((36,v,39,v),fill='black')
        draw.text((3,v-5),str(y),fill='black')
    draw.text((3,946),title,fill='black')
    draw.text((3,961),'3x NEAREST ANALYTICAL DISPLAY; ticks are source pixels; no feature marks',fill='black')
    return result


def panel_check(path,array,title):
    expected = independent_panel(array,title)
    with Image.open(path) as actual:
        require(actual.format=='PNG' and actual.mode=='RGB' and actual.size==(665,983),'panel PNG geometry/mode')
        require(actual.tobytes()==expected.tobytes(),'every crop/replicated cell/tick/label/footer pixel')
        pixels = np.array(actual)
    require(np.array_equal(pixels[28:943,40:655],np.array(expected)[28:943,40:655]),'unmarked native crop region')
    for x in range(270,475,10):
        u = 40+3*(x-270)
        require(np.all(pixels[24:28,u]==0),'all x tick pixels at source-cell origin')
    for y in range(100,400,10):
        v = 28+3*(y-95)
        require(np.all(pixels[v,36:40]==0),'all y tick pixels at source-cell origin')


def presentations(scopes,rows,arrays,pins):
    require(len(scopes)==2 and len({scope.resolve() for scope in scopes})==2,'two distinct presentation runs')
    inventories = [inventory(scope,'prepare',pins) for scope in scopes]
    require(inventories[0][1]==inventories[1][1] and fp(scopes[0]/'receipt.json')==fp(scopes[1]/'receipt.json'),'identical complete presentation receipt')
    expected_detail = {'rows':rows,'displays':[{'frame':int(row['frame_index_zero_based']),
        'path':f'f{int(row["frame_index_zero_based"]):06d}-target-panel.png','parent_png':row['png_identity']} for row in rows],
        'crop_xyxy_exclusive':[270,95,475,400],'scale':3,'pixel_origin_in_panel':[40,28],'display_size':[665,983]}
    require(read_json(scopes[0]/'detail.json')==expected_detail,'exact frame/PTS/geometry display manifest')
    for row,array in zip(rows,arrays):
        index = int(row['frame_index_zero_based'])
        title = f'Camera2 source index {index}; exact PTS seconds {row["source_time_seconds_exact"]}'
        panel_check(scopes[0]/f'f{index:06d}-target-panel.png',array,title)
    return {'inventories':[entry[0] for entry in inventories],'all_files_byte_identical':True,
        'fully_reconstructed_panels':17,'panels_in_second_identical_copy':17,
        'native_crop_pixels_per_panel':62525,'display_crop_pixels_per_panel':562725,
        'x_ticks_per_panel':21,'y_ticks_per_panel':30,
        'tick_convention':'Ticks mark the left/top origins of 3x3 source-pixel cells. Their displayed cell centers are one display pixel right/down; no subpixel historical precision is implied.',
        'interpretation':'Pixel/display lineage only; no material-feature visual interpretation or annotation read.'}


def presentation_controls(scopes):
    require(len(scopes)==2 and len({scope.resolve() for scope in scopes})==2,'two distinct presentation controls')
    inventories = [inventory(scope,'controls',{}) for scope in scopes]
    equal_names = ('present.py','detail.json','synthetic-source.png','synthetic-panel.png')
    require(all(fp(scopes[0]/name)==fp(scopes[1]/name) for name in equal_names),'same control code/scientific products across protocol amendment')
    y,x = np.indices((480,640))
    source = np.stack((x%256,y%256,x//256+4*(y//256)),axis=2).astype(np.uint8)
    with Image.open(scopes[0]/'synthetic-source.png') as stored:
        require(stored.mode=='RGB' and stored.size==(640,480) and np.array_equal(np.array(stored),source),'synthetic coordinate-source identity')
    panel_check(scopes[0]/'synthetic-panel.png',source,'SYNTHETIC COORDINATE CONTROL; not historical imagery')
    require(read_json(scopes[0]/'detail.json')=={'every_pixel_block_equal':True,'coordinate_points_checked':4,'x_ticks':21,'y_ticks':30,
        'scope':'Deterministic display geometry, not feature localization or material identity.'},'exact reported synthetic control coverage')
    return {'inventories':[entry[0] for entry in inventories],'byte_identical_products':list(equal_names),
        'protocol_versions_differ':inventories[0][0]['procedure'][str(HERE/'PROTOCOL.md')]!=inventories[1][0]['procedure'][str(HERE/'PROTOCOL.md')],
        'synthetic_source_and_entire_panel_reconstructed':True,'scope':'No producer functions imported or called.'}


def fraction_number(value):
    if isinstance(value,(bool,np.bool_)):
        raise ValueError('boolean is not a coordinate')
    if isinstance(value,(int,np.integer,Fraction)):
        return Fraction(value)
    if not np.isfinite(value):
        raise ValueError('nonfinite coordinate')
    return Fraction.from_float(float(value))


def exact_box(xy,halfwidth):
    if len(xy)!=2 or len(halfwidth)!=2:
        raise ValueError('coordinate shape')
    center = list(map(fraction_number,xy))
    half = list(map(fraction_number,halfwidth))
    if min(half)<0:
        raise ValueError('negative halfwidth')
    return [[c-h,c+h] for c,h in zip(center,half)]


def exact_subtract(current,baseline):
    return [[current[i][0]-baseline[i][1],current[i][1]-baseline[i][0]] for i in range(2)]


def exact_inverse_point(point,matrix,offset):
    a,b = map(fraction_number,matrix[0])
    c,d = map(fraction_number,matrix[1])
    x,y = (fraction_number(point[i])-fraction_number(offset[i]) for i in range(2))
    determinant = a*d-b*c
    if determinant==0:
        raise ValueError('singular matrix')
    return [(d*x-b*y)/determinant,(-c*x+a*y)/determinant]


def exact_inverse_box(bbox,matrix,offset):
    corners = [exact_inverse_point((x,y),matrix,offset) for x in bbox[0] for y in bbox[1]]
    return [[min(point[i] for point in corners),max(point[i] for point in corners)] for i in range(2)]


def geometry_controls(subject=None):
    checks = []
    def case(name,fn):
        try:
            detail = fn()
            checks.append({'name':name,'status':'pass','detail':detail})
        except Exception as error:
            checks.append({'name':name,'status':'fail','error_type':type(error).__name__,'error':str(error)})
    def equality(actual,expected,label):
        a,b = np.asarray(actual,dtype=float),np.asarray(expected,dtype=float)
        require(a.shape==b.shape and np.isfinite(a).all() and np.isfinite(b).all(),label+' shape/finite')
        require(np.allclose(a,b,atol=1e-9,rtol=1e-12),label+' arithmetic')
    def boxes():
        a = exact_box([10,-3],[2,5])
        b = exact_box([15,4],[1,2])
        require(a==[[8,12],[-8,2]] and b==[[14,16],[2,6]],'hand-computed asymmetric boxes')
        require(exact_subtract(b,a)==[[2,8],[0,14]],'hand-computed conservative difference')
        require(exact_subtract(a,a)==[[-4,4],[-10,10]],'conservative interval dependency not silently canceled')
        if subject:
            equality(subject.box([10,-3],[2,5]),a,'subject box')
            equality(subject.box([15,4],[1,2]),b,'subject second box')
            equality(subject.subtract_boxes(b,a),exact_subtract(b,a),'subject subtract')
            equality(subject.subtract_boxes(a,a),exact_subtract(a,a),'subject conservative self-subtract')
        return {'boxes':[[[8,12],[-8,2]],[[14,16],[2,6]]],'difference':[[2,8],[0,14]],'conservative_self_difference':[[-4,4],[-10,10]]}
    case('asymmetric_boxes_and_conservative_differences',boxes)
    fixtures = [
        ('identity',[[1,3],[2,4]],[[1,0],[0,1]],[0,0],[[1,3],[2,4]]),
        ('translation',[[5,9],[-7,-3]],[[1,0],[0,1]],[3,-2],[[2,6],[-5,-1]]),
        ('rotation',[[1,3],[2,4]],[[0,-1],[1,0]],[10,-5],[[7,9],[7,9]]),
        ('shear',[[1,3],[2,4]],[[1,2],[0,1]],[-1,1],[[-4,2],[1,3]]),
        ('anisotropic_scale',[[4,8],[-4,0]],[[2,0],[0,Fraction(1,2)]],[2,1],[[1,3],[-10,-2]]),
        ('inverse_amplification',[[0,1],[0,1]],[[1,0],[0,Fraction(1,1000000)]],[0,0],[[0,1],[0,1000000]]),
    ]
    for name,bbox,matrix,offset,expected in fixtures:
        def inverse_fixture(name=name,bbox=bbox,matrix=matrix,offset=offset,expected=expected):
            actual = exact_inverse_box(bbox,matrix,offset)
            require(actual==expected,'hand-computed inverse enclosure '+name)
            for x in bbox[0]:
                for y in bbox[1]:
                    p = exact_inverse_point([x,y],matrix,offset)
                    q = [sum(fraction_number(matrix[i][j])*p[j] for j in range(2))+fraction_number(offset[i]) for i in range(2)]
                    require(q==[x,y],'exact inverse/forward round trip '+name)
            if subject:
                if name=='inverse_amplification':
                    try:
                        subject.inverse_box(np.array(bbox,float),np.array(matrix,float),np.array(offset,float))
                    except ValueError:
                        pass
                    else:
                        raise AssertionError('condition-over-10000 consumer map accepted')
                else:
                    equality(subject.inverse_box(np.array(bbox,float),np.array(matrix,float),np.array(offset,float)),expected,'subject inverse '+name)
            return {'input_box':bbox,'matrix':[[str(v) for v in row] for row in matrix],'offset':offset,'expected_algebraic_enclosure':expected,
                'consumer_policy':'reject condition-over-10000' if name=='inverse_amplification' else 'admit valid positive inverse',
                'all_four_exact_round_trips':True}
        case('inverse_'+name,inverse_fixture)
    def wrong_inverse():
        q,m,b = [2,3],[[1,2],[0,1]],[-1,1]
        correct = exact_inverse_point(q,m,b)
        subtraction_only = [q[i]-b[i] for i in range(2)]
        require(correct==[-1,2] and subtraction_only==[3,2] and correct!=subtraction_only,'offset subtraction is not general inverse')
        require(exact_inverse_box([[1,3],[2,4]],m,b)==[[-4,2],[1,3]],'shear requires changed envelope width')
        return {'correct':[-1,2],'offset_only_wrong':[3,2],'center_with_unchanged_halfwidth_would_miss_corners':True}
    case('offset_only_and_center_only_negative_controls',wrong_inverse)
    def eligibility():
        results = []
        for loc in ('localized','ambiguous','unavailable'):
            for identity in ('appearance_consistent','uncertain','changed','not_assessable'):
                expected = loc=='localized' and identity=='appearance_consistent'
                if subject:
                    require(bool(subject.eligible({'localization':loc,'correspondence':identity}))==expected,'subject eligibility state table')
                results.append({'localization':loc,'correspondence':identity,'eligible_for_same_feature_displacement':expected})
        return {'all_twelve_state_combinations':results,'scope':'This predicate is not a substitute for annotation schema/coordinate validation.'}
    case('localized_but_changed_and_all_visibility_states',eligibility)
    def shared_error():
        wrong_a=wrong_b=exact_box([100,100],[1,1])
        truth=[0,0]
        overlap=all(max(wrong_a[i][0],wrong_b[i][0])<=min(wrong_a[i][1],wrong_b[i][1]) for i in range(2))
        truth_inside=all(wrong_a[i][0]<=truth[i]<=wrong_a[i][1] for i in range(2))
        require(overlap and not truth_inside,'shared image error must not become accuracy')
        if subject:
            row={'frame':1,'xy':[100,100],'halfwidth_xy':[1,1],'localization':'localized','correspondence':'appearance_consistent'}
            require(all(subject.compare_rows(row,row)['overlap_per_axis']),'subject shared-error overlap')
        return {'annotator_rectangles_overlap':True,'known_synthetic_truth_inside':False,'physical_accuracy_inferred':False}
    case('shared_wrong_coordinate_agreement_is_not_truth',shared_error)
    def selected_downward():
        fixtures=[([-3,-1],False),([-1,1],False),([0,3],False),([1,3],True)]
        require([interval[0]>0 for interval,_ in fixtures]==[wanted for _,wanted in fixtures],'downward lower-endpoint predicate')
        return {'cases':[{'interval':interval,'definitely_downward':wanted} for interval,wanted in fixtures],
            'previous_scheduled_sample':{'status':'unavailable','coordinate':None},
            'first_selected_positive_sample_is_not_an_onset_bracket':True}
    case('zero_exclusion_direction_and_visibility_limit',selected_downward)
    def baselines():
        first=exact_subtract(exact_box([20,20],[1,1]),exact_box([10,10],[1,1]))
        second=exact_subtract(exact_box([19,19],[1,1]),exact_box([12,12],[2,2]))
        require(first==[[8,12],[8,12]] and second==[[4,10],[4,10]],'separate annotator/frame baselines')
        if subject:
            equality(subject.subtract_boxes([[19,21],[19,21]],[[9,11],[9,11]]),first,'subject first baseline')
            equality(subject.subtract_boxes([[18,20],[18,20]],[[10,14],[10,14]]),second,'subject second baseline')
        return {'first_displacement':first,'second_displacement':second,'same_baseline_not_imposed':True}
    case('different_baselines_not_a_shared_consensus',baselines)
    def rejections():
        calls = [
            lambda: exact_box([0,0],[-1,1]),
            lambda: exact_box([float('nan'),0],[1,1]),
            lambda: exact_inverse_box([[0,1],[0,1]],[[1,2],[2,4]],[0,0]),
            lambda: exact_inverse_box([[0,1],[0,1]],[[1,float('inf')],[0,1]],[0,0]),
        ]
        if subject:
            calls += [lambda: subject.box([0,0],[-1,1]),lambda: subject.box([float('nan'),0],[1,1]),
                lambda: subject.inverse_box([[0,1],[0,1]],[[1,2],[2,4]],[0,0]),
                lambda: subject.inverse_box([[0,1],[0,1]],[[1,float('inf')],[0,1]],[0,0]),
                lambda: subject.inverse_box([[0,1],[0,1]],[[1,0],[0,-1]],[0,0]),
                lambda: subject.inverse_box([[2,1],[0,1]],[[1,0],[0,1]],[0,0]),
                lambda: subject.inverse_box([[0,1],[0,1]],[[1,0],[0,1]],[float('nan'),0])]
        for call in calls:
            try:
                call()
            except (ValueError,AssertionError,np.linalg.LinAlgError):
                pass
            else:
                raise AssertionError('invalid/singular synthetic input accepted')
        return {'invalid_calls_rejected':len(calls)}
    case('negative_width_nonfinite_and_singular_rejected',rejections)
    if subject:
        def annotation(xy=[10,10],half=[2,3],frame=1,loc='localized',corr='appearance_consistent'):
            return {'frame':frame,'xy':xy,'halfwidth_xy':half,'localization':loc,'correspondence':corr}
        def cross_annotator():
            a=annotation()
            touch=annotation([14,10],[2,3])
            result=subject.compare_rows(a,touch)
            require(result=={'both_localized':True,'localization_agrees':True,'correspondence_agrees':True,
                'separate_minus_root_xy':[4,0],'overlap_per_axis':[True,True],'root_center_in_separate':False,'separate_center_in_root':False},'inclusive touching rectangles')
            separated=subject.compare_rows(a,annotation([15,10],[2,3]))
            require(separated['overlap_per_axis']==[False,True],'disjoint axis preserved')
            changed=subject.compare_rows(a,annotation([11,10],[1,1],corr='changed'))
            require(changed['both_localized'] and not changed['correspondence_agrees'],'localized coordinate agreement not identity agreement')
            unavailable=subject.compare_rows(a,annotation(None,None,loc='unavailable',corr='not_assessable'))
            require(unavailable=={'both_localized':False,'localization_agrees':False,'correspondence_agrees':False},'nonlocalized pair has no invented difference')
            return {'touching':result,'disjoint':separated,'changed_identity':changed,'unavailable':unavailable}
        case('actual_comparison_inclusive_disjoint_changed_and_missing',cross_annotator)
        def actual_displacement():
            baseline=annotation([10,10],[3,4])
            same=subject.displacement(baseline,baseline)
            require(same=={'center_xy':[0.,0.],'enclosure_xy':[[0.,0.],[0.,0.]],'self_baseline':True},'shared-variable baseline exactly zero')
            current=annotation([20,19],[2,1],frame=2)
            moved=subject.displacement(current,baseline)
            expected=exact_subtract(exact_box(current['xy'],current['halfwidth_xy']),exact_box(baseline['xy'],baseline['halfwidth_xy']))
            equality(moved['enclosure_xy'],expected,'separate-frame exact displacement')
            require(moved['center_xy']==[10,9] and not moved['self_baseline'],'separate-frame center difference')
            for loc,corr in (('localized','changed'),('localized','uncertain'),('ambiguous','uncertain'),('unavailable','not_assessable')):
                item=annotation([20,19] if loc=='localized' else None,[2,1] if loc=='localized' else None,2,loc,corr)
                require(subject.displacement(item,baseline) is None,'noneligible current has no displacement')
                require(subject.displacement(current,item) is None,'noneligible baseline has no displacement')
            try:
                subject.displacement(annotation([11,10],[3,4]),baseline)
            except ValueError:
                pass
            else:
                raise AssertionError('different same-frame observation silently treated as baseline identity')
            return {'exact_self_baseline':same,'separate_frame':moved,'uncertain_changed_ambiguous_unavailable_both_endpoints_checked':True}
        case('actual_baseline_identity_and_eligibility',actual_displacement)
        def scheduled_downward():
            records=[{'frame':index,'seconds_exact':str(index),'displacement':None if interval is None else {'enclosure_xy':[[0,0],interval]}}
                for index,interval in ((1,[-5,-1]),(2,[0,3]),(3,None),(4,[1,5]))]
            result=subject.first_downward(records)
            require(result['first_selected_frame']==4 and result['preceding_scheduled_sample']==records[2],'immediate unavailable preceding sample retained')
            require('not first physical motion or an onset bracket' in result['meaning'],'selected sampling limitation retained')
            none=subject.first_downward(records[:3])
            require(none['first_selected_frame'] is None,'upward and zero-touching samples not downward evidence')
            return {'first':result,'none':none}
        case('actual_first_downward_with_unavailable_predecessor',scheduled_downward)
        def hull_boundary():
            vertices=subject.hull([[0,0],[2,0],[2,2],[0,2],[1,1],[0,0]])
            require(vertices==[(0,0),(2,0),(2,2),(0,2)],'independent square hull with duplicate/interior')
            cases=[([1,1],False),([0,1],False),([-2e-9,1],False),([-1e-8,1],True),([3,3],True)]
            require(all(bool(subject.outside_hull(point,vertices))==expected for point,expected in cases),'cross-product tolerance boundary classification')
            try:
                subject.hull([[0,0],[1,1],[2,2]])
            except ValueError:
                pass
            else:
                raise AssertionError('collinear hull accepted')
            return {'vertices':vertices,'point_outside_cases':cases,'tolerance_is_cross_product_not_a_uniform_distance_bound':True}
        case('actual_hull_extrapolation_and_degenerate_rejection',hull_boundary)
        def map_admission():
            baseline=annotation([1,1],[1,1])
            row=annotation([2,3],[1,1],frame=2)
            fit={'status':'computed','passes_consistency_screen':True,'index':2,'half':9,'model':'affine','matrix':[[1,0],[0,1]],'offset':[0,0]}
            basefit=dict(fit,index=1)
            vertices=[(0,0),(4,0),(4,4),(0,4)]
            failed=dict(fit,passes_consistency_screen=False)
            require(subject.mapped_record(row,baseline,failed,basefit,vertices)['status']=='stored_map_not_admitted','failed current map withheld')
            require(subject.mapped_record(row,baseline,fit,dict(basefit,passes_consistency_screen=False),vertices)['status']=='stored_map_not_admitted','failed baseline map withheld')
            require(subject.mapped_record(row,baseline,dict(fit,matrix=[[1,0],[0,-1]]),basefit,vertices)['status']=='inverse_not_admitted','reversed map withheld')
            require(subject.mapped_record(annotation(None,None,2,'unavailable','not_assessable'),baseline,fit,basefit,vertices)['status']=='annotation_not_eligible','unavailable observed point not mapped')
            mapped=subject.mapped_record(row,baseline,fit,basefit,vertices)
            equality(mapped['mapped_center_xy'],[2,3],'known mapped center')
            equality(mapped['mapped_displacement_enclosure_xy'],exact_subtract(exact_box([2,3],[1,1]),exact_box([1,1],[1,1])),'known mapped enclosure')
            return {'current_and_baseline_admission_required':True,'invalid_and_unavailable_not_zero_filled':True,'known_identity_case':mapped}
        case('actual_map_consumer_admission_and_missing_values',map_admission)
    return {'checks':checks,'passed':sum(row['status']=='pass' for row in checks),'failed':sum(row['status']=='fail' for row in checks),
        'subject_imported':subject is not None,'scope':'Exact closed-form/Fraction fixtures; no historical identity, annotation or camera validation.'}


def exact_eligible(row):
    return row['localization']=='localized' and row['correspondence']=='appearance_consistent'


def floats(value):
    if isinstance(value,list):
        return [floats(item) for item in value]
    return float(value)


def independent_displacement(row,baseline):
    if not exact_eligible(row) or not exact_eligible(baseline):
        return None
    if row['frame']==baseline['frame']:
        require(row==baseline,'same-frame observation must be exact shared baseline')
        return {'center_xy':[0.,0.],'enclosure_xy':[[0.,0.],[0.,0.]],'self_baseline':True}
    return {'center_xy':[row['xy'][i]-baseline['xy'][i] for i in range(2)],
        'enclosure_xy':floats(exact_subtract(exact_box(row['xy'],row['halfwidth_xy']),exact_box(baseline['xy'],baseline['halfwidth_xy']))),
        'self_baseline':False}


def independent_comparison(one,two):
    both=one['localization']==two['localization']=='localized'
    result={'both_localized':both,'localization_agrees':one['localization']==two['localization'],
        'correspondence_agrees':one['correspondence']==two['correspondence']}
    if both:
        a,b=exact_box(one['xy'],one['halfwidth_xy']),exact_box(two['xy'],two['halfwidth_xy'])
        result.update(separate_minus_root_xy=[two['xy'][i]-one['xy'][i] for i in range(2)],
            overlap_per_axis=[max(a[i][0],b[i][0])<=min(a[i][1],b[i][1]) for i in range(2)],
            root_center_in_separate=all(b[i][0]<=one['xy'][i]<=b[i][1] for i in range(2)),
            separate_center_in_root=all(a[i][0]<=two['xy'][i]<=a[i][1] for i in range(2)))
    return result


def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def supporting_edge_hull(points):
    """Exhaustive directed supporting edges, unlike producer's monotone chain."""
    points=sorted(set(tuple(map(fraction_number,point)) for point in points))
    edges=[]
    for a in points:
        for b in points:
            if a==b or any(cross(a,b,c)<0 for c in points):
                continue
            collinear=[c for c in points if cross(a,b,c)==0]
            length=sum((b[i]-a[i])**2 for i in range(2))
            if any(sum((c[i]-a[i])*(b[i]-a[i]) for i in range(2))<0 or
                   sum((c[i]-a[i])*(b[i]-a[i]) for i in range(2))>length for c in collinear):
                continue
            edges.append((a,b))
    require(len(edges)>=3,'independent reference hull nondegenerate')
    chain=[min(a for a,b in edges)]
    for _ in range(len(points)):
        outgoing=[b for a,b in edges if a==chain[-1]]
        require(len(outgoing)==1,'unique directed reference hull edge')
        if outgoing[0]==chain[0]:
            require(len(chain)==len(edges),'complete directed reference hull')
            return chain
        require(outgoing[0] not in chain,'nonclosing hull cycle')
        chain.append(outgoing[0])
    raise AssertionError('reference hull did not close')


def independent_outside(point,vertices):
    p=tuple(map(fraction_number,point))
    return any(cross(a,b,p)<-Fraction.from_float(1e-8) for a,b in zip(vertices,vertices[1:]+vertices[:1]))


def independent_condition(matrix):
    a,b,c,d=(float(value) for row in matrix for value in row)
    determinant=a*d-b*c
    trace=a*a+b*b+c*c+d*d
    gap=math.hypot(a*a+c*c-b*b-d*d,2*(a*b+c*d))
    maximum_squared=(trace+gap)/2
    condition=maximum_squared/abs(determinant) if determinant else math.inf
    return determinant,condition


def independent_mapped(row,baseline,fit,basefit,vertices):
    result={'stored_fit_status':fit['status'],'stored_fit_screen':fit['passes_consistency_screen'],
        'baseline_fit_status':basefit['status'],'baseline_fit_screen':basefit['passes_consistency_screen']}
    if not exact_eligible(row) or not exact_eligible(baseline):
        return dict(result,status='annotation_not_eligible')
    if not fit['passes_consistency_screen'] or not basefit['passes_consistency_screen']:
        return dict(result,status='stored_map_not_admitted',known_cutoff_rounding_case=fit['index']==7021 and fit['half']==9 and fit['model']=='affine')
    determinant,condition=independent_condition(fit['matrix'])
    bdeterminant,bcondition=independent_condition(basefit['matrix'])
    if not (determinant>0 and bdeterminant>0 and math.isfinite(condition) and math.isfinite(bcondition) and condition<=10000 and bcondition<=10000):
        return dict(result,status='inverse_not_admitted',reason='admissible inverse matrix')
    center=exact_inverse_point(row['xy'],fit['matrix'],fit['offset'])
    bcenter=exact_inverse_point(baseline['xy'],basefit['matrix'],basefit['offset'])
    current=exact_inverse_box(exact_box(row['xy'],row['halfwidth_xy']),fit['matrix'],fit['offset'])
    base=exact_inverse_box(exact_box(baseline['xy'],baseline['halfwidth_xy']),basefit['matrix'],basefit['offset'])
    enclosure=[[0.,0.],[0.,0.]] if row['frame']==baseline['frame'] else floats(exact_subtract(current,base))
    delta=[center[i]-bcenter[i] for i in range(2)]
    raw=independent_displacement(row,baseline)
    return dict(result,status='computed_conditional_image_map',inverse_condition=condition,baseline_inverse_condition=bcondition,
        mapped_center_xy=floats(center),mapped_box_xy=floats(current),baseline_mapped_center_xy=floats(bcenter),
        baseline_mapped_box_xy=floats(base),mapped_displacement_xy=floats(delta),mapped_displacement_enclosure_xy=enclosure,
        mapped_minus_raw_displacement_xy=floats([delta[i]-raw['center_xy'][i] for i in range(2)]),
        center_outside_reference_hull=independent_outside(center,vertices),baseline_center_outside_reference_hull=independent_outside(bcenter,vertices))


def compare_tree(actual,expected,path='result'):
    if isinstance(expected,dict):
        require(isinstance(actual,dict) and set(actual)==set(expected),path+' exact field set')
        for name,value in expected.items():
            compare_tree(actual[name],value,path+'/'+name)
    elif isinstance(expected,list):
        require(isinstance(actual,list) and len(actual)==len(expected),path+' exact list coverage')
        for index,(one,two) in enumerate(zip(actual,expected)):
            compare_tree(one,two,path+'/'+str(index))
    elif isinstance(expected,float):
        require(type(actual) in (int,float) and math.isfinite(actual) and math.isfinite(expected),path+' finite number')
        require(math.isclose(actual,expected,abs_tol=1e-8,rel_tol=1e-10),path+' independent arithmetic')
    else:
        require(type(actual)==type(expected) and actual==expected,path+' exact value/type')


def released_annotations():
    require(fp(HERE/'annotation-release.json')['sha256']==RELEASE_SHA,'pre-result release manifest identity')
    require(fp(HERE/'selection.json')['sha256']==SELECTION_SHA,'frozen accepted targets')
    release=read_json(HERE/'annotation-release.json')
    require(release['status']=='both_annotation_sets_frozen_before_comparison' and release['other_new_coordinates_seen_before_own_save']=={'root':False,'separate':False},'declared annotation release boundary')
    require(set(release['annotation_pins'])==set(ANNOTATION_SHAS),'exact released pair')
    annotations=[]
    for label,name in (('root','root-annotations.json'),('separate','annotator-annotations.json')):
        require(fp(HERE/name)['sha256']==ANNOTATION_SHAS[name] and fp(HERE/name)==release['annotation_pins'][name],'pre-result released annotation identity')
        data=read_json(HERE/name)
        expected={'protocol_sha256':PROTOCOL_SHA,'selection_sha256':SELECTION_SHA,
            'presentation_receipt_sha256':'7ca7abe5bc9d67511213a627a5ae65b1e506952b88896f780779d5fbf7c63f29',
            'source_manifest_sha256':'dda0cb2e9f17240562e2aafa9443f05df0c2047fd93d8a4e643233cf53e3175e'}
        require(all(data.get(key)==value for key,value in expected.items()),'annotation declared source/dependency identities')
        require(type(data['schema_version']) is int and data['schema_version']==1 and data['annotator']==label and data['review_kind']=='computational_AI_not_human','annotation version/reviewer')
        require(data['independence']=={'other_new_annotations_seen':False,'shared_proposal_known':True,'old_event_familiarity':True},'annotation independence boundary')
        require(data['viewing']['full_native_frames']==list(FRAMES) and data['viewing']['coordinate_panels']==list(FRAMES),'recorded annotation viewing coverage')
        require([(row['frame'],row['target']) for row in data['rows']]==[(frame,target) for frame in FRAMES for target in TARGETS],'34 exact ordered annotation keys')
        for row in data['rows']:
            require(type(row['frame']) is int,'integer annotation frame')
            require(row['localization'] in ('localized','ambiguous','unavailable') and row['correspondence'] in ('appearance_consistent','uncertain','changed','not_assessable'),'annotation localization/correspondence states')
            require(isinstance(row['note'],str) and row['note'].strip(),'annotation appearance/continuity note')
            if row['localization']=='localized':
                require(all(isinstance(row[key],list) and len(row[key])==2 and all(type(value) is int for value in row[key]) for key in ('xy','halfwidth_xy')),'native integer point and envelope')
                require(0<=row['xy'][0]<640 and 0<=row['xy'][1]<480 and min(row['halfwidth_xy'])>0,'valid native center and positive envelope')
            else:
                require(row['xy'] is None and row['halfwidth_xy'] is None,'unresolved coordinate/envelope not invented')
        annotations.append(data['rows'])
    return annotations


def independent_first(records):
    admitted = [index for index,row in enumerate(records)
        if row['displacement'] is not None and row['displacement']['enclosure_xy'][1][0]>0]
    if not admitted:
        return {'first_selected_frame':None,'meaning':'No selected eligible downward interval found; not evidence of no motion.'}
    index = min(admitted)
    row = records[index]
    return {'first_selected_frame':row['frame'],'seconds_exact':row['seconds_exact'],
        'downward_enclosure':row['displacement']['enclosure_xy'][1],
        'preceding_scheduled_sample':records[index-1] if index else None,
        'meaning':'First selected appearance-displacement interval wholly downward; not first physical motion or an onset bracket.'}


def independent_result(annotations,stamps,fits,vertices):
    raw,comparisons,between,mapped,firsts = [],[],[],[],[]
    for label,rows in zip(('root','separate'),annotations):
        baseline = {row['target']:row for row in rows if row['frame']==FRAMES[0]}
        analyst_raw = []
        for row in rows:
            item = {'annotator':label,'frame':row['frame'],'target':row['target'],
                'seconds_exact':stamps[row['frame']]['source_time_seconds_exact'],
                'observation':row,'displacement':independent_displacement(row,baseline[row['target']])}
            analyst_raw.append(item)
            for half in (9,13):
                for model in MODELS:
                    result = independent_mapped(row,baseline[row['target']],fits[(row['frame'],half,model)],fits[(FRAMES[0],half,model)],vertices)
                    mapped.append(dict(result,annotator=label,frame=row['frame'],target=row['target'],half=half,model=model,seconds_exact=item['seconds_exact']))
        raw.extend(analyst_raw)
        for target in TARGETS:
            firsts.append(dict(independent_first([row for row in analyst_raw if row['target']==target]),annotator=label,target=target))
        keyed = {(row['frame'],row['target']):row['displacement'] for row in analyst_raw}
        for frame in FRAMES:
            item = {'annotator':label,'frame':frame,'seconds_exact':stamps[frame]['source_time_seconds_exact'],'status':'not_both_eligible'}
            one,two = keyed[(frame,'C2-T1')],keyed[(frame,'C2-T2')]
            if one is not None and two is not None:
                difference = [
                    two['enclosure_xy'][1][0]-one['enclosure_xy'][1][1],
                    two['enclosure_xy'][1][1]-one['enclosure_xy'][1][0]]
                item.update(status='computed_appearance_difference',
                    T2_minus_T1_vertical_displacement=two['center_xy'][1]-one['center_xy'][1],enclosure=difference)
            between.append(item)
    for one,two in zip(*annotations):
        comparisons.append(dict(independent_comparison(one,two),frame=one['frame'],target=one['target'],root_observation=one,separate_observation=two))
    return {'scope':'Retrospective computational appearance annotations and conditional image-coordinate sensitivity; no physical trajectory or cause.',
        'raw':raw,'comparisons':comparisons,'between_targets':between,'mapped':mapped,'first_selected_downward':firsts,
        'reference_hull':[[int(value) for value in point] for point in vertices],
        'map_status_counts':dict(Counter(row['status'] for row in mapped))}


def exact_inventory(scope,stage,names,pins=None):
    require(scope.is_dir() and scope.resolve()==scope and not (scope/'failure.json').exists(),'direct complete non-aliased scope')
    receipt = read_json(scope/'receipt.json')
    require(receipt['stage']==stage and receipt['status']=='complete','complete stage receipt')
    require(set(receipt['products'])==set(names),'exact product receipt names')
    require({path.name for path in scope.iterdir()}==set(names)|{'receipt.json'},'exact product directory names')
    require(all((scope/name).is_file() and fp(scope/name)==identity for name,identity in receipt['products'].items()),'all product bytes verified')
    if pins is not None:
        require(receipt['pins']==pins,'exact consumed/procedure/runtime pin union: '+scope.name)
    return receipt


def historical_oracle_controls():
    checks = []
    annotations = []
    for analyst in range(2):
        rows = []
        for index,frame in enumerate(FRAMES):
            for target in TARGETS:
                rows.append({'frame':frame,'target':target,'localization':'localized',
                    'correspondence':'uncertain' if analyst==1 and frame==FRAMES[-1] and target=='C2-T2' else 'appearance_consistent',
                    'xy':[10+analyst,10+analyst+3*index],'halfwidth_xy':[1,1]})
        annotations.append(rows)
    stamps = {frame:{'source_time_seconds_exact':str(index)} for index,frame in enumerate(FRAMES)}
    fits = {(frame,half,model):{'index':frame,'half':half,'model':model,'status':'computed',
        'passes_consistency_screen':True,'matrix':[[1,0],[0,1]],'offset':[0,0]}
        for frame in FRAMES for half in (9,13) for model in MODELS}
    vertices = supporting_edge_hull([[0,0],[100,0],[100,100],[0,100],[50,50],[0,0]])
    require(vertices==[(0,0),(100,0),(100,100),(0,100)],'exact independent supporting-edge hull')
    checks.append('exact supporting-edge hull with duplicates/interior')
    require(independent_condition([[2,0],[0,1]])==(2.,2.),'analytic inverse condition diagonal')
    require(independent_condition([[1,2],[0,1]])[1]>5.8 and independent_condition([[1,2],[0,1]])[1]<5.9,'analytic shear condition')
    checks.append('closed-form condition known diagonal and shear')
    expected = independent_result(annotations,stamps,fits,vertices)
    require([len(expected[name]) for name in ('raw','comparisons','between_targets','mapped','first_selected_downward')]==[68,34,34,408,4],'synthetic full output denominators')
    require(expected['map_status_counts']=={'computed_conditional_image_map':402,'annotation_not_eligible':6},'synthetic uncertain identity excluded exactly six maps')
    require(all(row['first_selected_frame']==FRAMES[1] and row['downward_enclosure']==[1.,5.] and row['preceding_scheduled_sample']['frame']==FRAMES[0] for row in expected['first_selected_downward']),'known first selected downward sample and baseline predecessor')
    require(expected['between_targets'][0]['enclosure']==[0.,0.] and expected['between_targets'][1]['enclosure']==[-4.,4.] and expected['between_targets'][-1]['status']=='not_both_eligible','between-target error sums and missingness')
    require(expected['raw'][2]['displacement']=={'center_xy':[0,3],'enclosure_xy':[[-2.,2.],[1.,5.]],'self_baseline':False},'known raw displacement')
    checks.append('full synthetic paired-annotation result with known displacements and uncertain identity')
    compare_tree(expected,expected)
    mutations = []
    for kind in ('numeric','missing_row','extra_field','wrong_status','boolean_number'):
        wrong = json.loads(json.dumps(expected))
        if kind=='numeric':wrong['mapped'][6]['mapped_center_xy'][0]+=0.1
        elif kind=='missing_row':wrong['mapped'].pop()
        elif kind=='extra_field':wrong['raw'][0]['unsupported']=True
        elif kind=='wrong_status':wrong['mapped'][-1]['status']='computed_conditional_image_map'
        else:wrong['mapped'][0]['inverse_condition']=True
        try:
            compare_tree(wrong,expected)
        except AssertionError:
            mutations.append(kind)
        else:
            raise AssertionError('result mutation accepted: '+kind)
    checks.append('recursive result comparator rejects five known numeric/coverage/type/status mutations')
    return {'passed':len(checks),'checks':checks,'mutation_rejections':mutations,
        'scope':'Synthetic independent oracle/comparator only; no historical source or annotation opened, no producer import.'}


def historical_results(scopes,control_scope,source_root):
    require(len(scopes)==2 and len({scope.resolve() for scope in scopes})==2,'two distinct historical run directories')
    require(all(scope.parent==HERE for scope in scopes) and control_scope.parent==HERE,'local historical/control scopes')
    require(source_root in (ROOT,Path('/Users/admin/docs/911')) and source_root.resolve()==source_root,'explicit known read-only source checkout')
    frozen = {'analyze.py':ANALYZE_SHA,'PROTOCOL.md':PROTOCOL_SHA,'CALCULATION-CONTRACT.md':CONTRACT_SHA}
    require(all(fp(HERE/name)['sha256']==digest for name,digest in frozen.items()),'reviewed historical producer/protocol/contract')
    procedure = {str(path):fp(path) for path in [HERE/name for name in frozen]+[Path(sys.executable)]}
    control_names = set(frozen)|{'initial.json','result.json'}
    control_receipt = exact_inventory(control_scope,'controls',control_names,procedure)
    expected_initial = {'stage':'controls','pins':procedure,'python':sys.version,'numpy':np.__version__}
    require(read_json(control_scope/'initial.json')==expected_initial,'exact control runtime/initial binding')
    require(all(fp(control_scope/name)==procedure[str(HERE/name)] for name in frozen),'control procedure snapshots')
    controls = read_json(control_scope/'result.json')
    expected_checks = ['asymmetric center-location box','conservative interval subtraction','inverse shear all corners',
        'invalid box rejected','invalid box rejected','invalid inverse rejected','invalid inverse rejected','invalid inverse rejected',
        'visible changed definition excluded','unavailable coordinate not invented','same-observation baseline exact zero',
        'downward sign and preceding sample not onset','shared wrong coordinates can agree without truth','hull extrapolation classification']
    require(controls=={'passed':14,'checks':expected_checks,'shared_error_truth_xy':[100,100],
        'scope':'Synthetic arithmetic and limits, not historical validation.'},'complete expected producer control result')
    rows,arrays,pins = source_inputs(source_root)
    # Arrays were byte/luma checked, not visually interpreted in this numerical review.
    del arrays
    original_here = source_root/'research/sherlock-wtc7-investigation/camera2-target-trackability'
    presentation_pins = {str(original_here/name):fp(HERE/name) for name in ('present.py','PROTOCOL.md')}
    presentation_pins[str(Path(sys.executable))] = fp(Path(sys.executable))
    presentation_pins.update(pins)
    present_names = {'present.py','PROTOCOL.md','initial.json','detail.json','input-pins.json'}|{f'f{frame:06d}-target-panel.png' for frame in FRAMES}
    presentation = exact_inventory(HERE/'present01','prepare',present_names,presentation_pins)
    require(fp(HERE/'present01/receipt.json')['sha256']==PRESENT_RECEIPT_SHA,'frozen presentation receipt')
    require(read_json(HERE/'present01/detail.json')['rows']==rows,'independent source-manifest to presentation rows/PTS join')
    require(read_json(HERE/'present01/input-pins.json')==pins,'complete presentation source pins')
    require(all(fp(Path(path))==identity for path,identity in presentation['pins'].items()),'original absolute presentation dependencies unchanged')
    reference = HERE.parent/'camera2-reference-repair/run01'
    require(fp(reference/'receipt.json')['sha256']==REFERENCE_SHA,'frozen reference receipt')
    reference_receipt = read_json(reference/'receipt.json')
    require(reference_receipt['stage']=='run' and reference_receipt['status']=='complete' and len(reference_receipt['products'])==25,'reference stage and coverage')
    exact_inventory(reference,'run',reference_receipt['products'])
    reference_input_paths = {str(Path(path) if Path(path).is_absolute() else source_root/path):identity
        for path,identity in reference_receipt['pins'].items()}
    require(all(fp(Path(path))==identity for path,identity in reference_input_paths.items()),'reference dependency identities unchanged; no refit')
    pins.update(reference_input_paths)
    fit_rows = read_json(reference/'transforms.json')
    fits = {(row['index'],row['half'],row['model']):row for row in fit_rows}
    event = read_json(source_root/'research/sherlock-wtc7-investigation/multiview-onset-review/refinement.json')['rules']['camera2']['groups']['event']
    require(len(fits)==len(fit_rows)==426 and set(fits)=={(frame,half,model) for frame in event for half in (9,13) for model in MODELS},'complete exact reference map-key denominator')
    preflight = read_json(reference/'preflight-selection.json')
    require(len(preflight['features'])==6,'six reference hull inputs')
    vertices = supporting_edge_hull([row['xy'] for row in preflight['features']])
    selection = read_json(HERE/'selection.json')
    require(selection['accepted_target_ids']==list(TARGETS) and selection['protocol_sha256']==PROTOCOL_SHA,'frozen accepted target declarations')
    require(selection['proposal_sha256']==fp(HERE/'targets-proposal.json')['sha256'],'proposal identity bound by frozen selection')
    annotations = released_annotations()
    stamps = {int(row['frame_index_zero_based']):row for row in rows}
    consumed = ['selection.json','targets-proposal.json','root-annotations.json','annotator-annotations.json',
        'annotation-release.json','present01/receipt.json','present01/detail.json']
    expected_pins = dict(procedure)
    # Producer preserves the explicit CLI spelling of --controls. Admit only the
    # exact selected absolute path or its exact repository-relative spelling.
    control_spellings = {str(control_scope/'receipt.json'),str((control_scope/'receipt.json').relative_to(ROOT))}
    recorded_control = control_spellings & set(read_json(scopes[0]/'receipt.json')['pins'])
    require(len(recorded_control)==1,'one exact selected control receipt path spelling')
    expected_pins[recorded_control.pop()] = fp(control_scope/'receipt.json')
    expected_pins.update({str(HERE/name):fp(HERE/name) for name in consumed})
    expected_pins.update({str(reference/name):fp(reference/name) for name in ('receipt.json','transforms.json','preflight-selection.json')})
    run_names = set(frozen)|{'initial.json','result.json'}|{f'input-{index}-{Path(name).name}' for index,name in enumerate(consumed)}
    receipts = [exact_inventory(scope,'analyze',run_names,expected_pins) for scope in scopes]
    for scope in scopes:
        require(read_json(scope/'initial.json')==dict(expected_initial,stage='analyze'),'historical initial procedure/runtime binding')
        require(all(fp(scope/name)==procedure[str(HERE/name)] for name in frozen),'historical procedure snapshots')
        require(all(fp(scope/f'input-{index}-{Path(name).name}')==fp(HERE/name) for index,name in enumerate(consumed)),'all seven consumed input snapshots')
    require(receipts[0]==receipts[1] and fp(scopes[0]/'receipt.json')==fp(scopes[1]/'receipt.json'),'all historical repeat files including receipt byte identical')
    expected = independent_result(annotations,stamps,fits,vertices)
    actual = read_json(scopes[0]/'result.json')
    compare_tree(actual,expected)
    require(tuple(len(actual[name]) for name in ('raw','comparisons','between_targets','mapped','first_selected_downward'))==(68,34,34,408,4),'independent complete result denominators')
    pins.update({str(Path(path) if Path(path).is_absolute() else ROOT/path):identity for path,identity in expected_pins.items()})
    pins.update({str(scope/name):fp(scope/name) for scope in scopes for name in run_names|{'receipt.json'}})
    require(all(fp(Path(path))==identity for path,identity in pins.items()),'all consumed source/reference/annotation/procedure/products unchanged after review')
    computed = [row for row in actual['mapped'] if row['status']=='computed_conditional_image_map']
    return {'runs':[{'scope':scope.name,'receipt':fp(scope/'receipt.json'),'listed_products':len(run_names),'files_including_receipt':len(run_names)+1} for scope in scopes],
        'producer_controls':{'scope':control_scope.name,'receipt':fp(control_scope/'receipt.json'),'passed':14},
        'historical_producer_imported':False,'all_files_byte_identical':True,
        'coverage':{name:len(actual[name]) for name in ('raw','comparisons','between_targets','mapped','first_selected_downward')},
        'independent_oracle':'Fraction exact box/subtraction/closed-form 2x2 inverse at all corners; analytic condition formula; exhaustive supporting-edge hull; independent eligibility/comparison/selected-sample construction.',
        'comparison_tolerance':{'absolute':1e-8,'relative':1e-10,'scope':'Numeric arithmetic comparisons only; statuses/row order/fields/annotations exact. Not a physical uncertainty interval.'},
        'map_status_counts':actual['map_status_counts'],'mapped_records_with_current_extrapolation':sum(row['center_outside_reference_hull'] for row in computed),
        'mapped_records_with_baseline_extrapolation':sum(row['baseline_center_outside_reference_hull'] for row in computed),
        'first_selected_downward':actual['first_selected_downward'],
        'stored_cutoff_rounding_rows':[row for row in actual['mapped'] if row.get('known_cutoff_rounding_case')],
        'source_pins':pins,'scope':'All released result arithmetic and byte lineage; no visual reannotation, material identity, calibration, continuous onset, acceleration or cause.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--presentations',nargs=2)
    parser.add_argument('--presentation-controls',nargs=2)
    parser.add_argument('--geometry-controls',action='store_true')
    parser.add_argument('--oracle-controls',action='store_true')
    parser.add_argument('--subject',type=Path)
    parser.add_argument('--historical',nargs=2)
    parser.add_argument('--calculation-controls')
    parser.add_argument('--source-root',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    out = args.out.absolute()
    require(out.parent==HERE and out.name.startswith(('verification','independent-controls')) and out.suffix=='.json','independent receipt scope')
    require(not out.exists(),'preserve independent review receipts')
    result = {'command':sys.argv,'verifier':fp(Path(__file__)),'python':platform.python_version(),
        'numpy':np.__version__,'pillow':PIL.__version__,
        'scope':'Independent presentation/source lineage, synthetic checks and explicitly released historical arithmetic; no physical interpretation.'}
    try:
        require(args.presentations or args.presentation_controls or args.geometry_controls or args.oracle_controls or args.historical,'at least one declared check')
        require(not args.historical or (not args.subject and args.calculation_controls and args.source_root),'historical oracle never imports subject; explicit control/source scopes')
        pins = {}
        if args.presentations:
            rows,arrays,pins = source_inputs()
            result['presentations'] = presentations([(HERE/name).absolute() for name in args.presentations],rows,arrays,pins)
        if args.presentation_controls:
            result['presentation_controls'] = presentation_controls([(HERE/name).absolute() for name in args.presentation_controls])
        if args.geometry_controls:
            subject = None
            if args.subject:
                path = args.subject.resolve()
                require(path==HERE/'analyze.py','only explicitly reviewed analysis subject permitted')
                result['subject'] = fp(path)
                spec = importlib.util.spec_from_file_location('target_synthetic_subject',path)
                subject = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(subject)
            result['geometry_controls'] = geometry_controls(subject)
            require(result['geometry_controls']['failed']==0,'independent synthetic geometry failures')
            if args.subject:
                require(fp(args.subject.resolve())==result['subject'],'subject changed during synthetic checks')
        if args.historical:
            result['oracle_controls'] = historical_oracle_controls()
            result['historical'] = historical_results([(HERE/name).absolute() for name in args.historical],
                (HERE/args.calculation_controls).absolute(),args.source_root.absolute())
        elif args.oracle_controls:
            result['oracle_controls'] = historical_oracle_controls()
        require(all(fp(Path(path))==identity for path,identity in pins.items()),'source pins unchanged after review')
        require(fp(HERE/'present.py')['sha256']==PRESENT_SHA and fp(HERE/'PROTOCOL.md')['sha256']==PROTOCOL_SHA,'presentation procedure unchanged after review')
        require(fp(Path(__file__))==result['verifier'],'verifier unchanged during review')
        result['source_pins'] = pins
        result['status'] = 'pass'
    except Exception as error:
        result.update(status='fail',error_type=type(error).__name__,error=str(error))
    with out.open('x') as stream:
        stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False,default=lambda value:str(value) if isinstance(value,Fraction) else value)+'\n')
    print(json.dumps({key:result[key] for key in ('status','error_type','error') if key in result}))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':
    raise SystemExit(main())
