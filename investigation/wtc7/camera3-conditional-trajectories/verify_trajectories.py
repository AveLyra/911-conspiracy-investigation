#!/usr/bin/env python3
"""Independent allowlisted extraction/artifact and exact polynomial checks.

No producer imports; no raw XML, arbitrary source strings, or private paths
are emitted. The original project is inert data, never application input.
"""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import sys
import xml.etree.ElementTree as ET
from PIL import Image, __version__ as PILLOW

HERE = Path(__file__).resolve().parent
PUBLIC = Path('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
KIT = PUBLIC / 'camera3-provenance/kit-inventory/run-v1'
OLD = PUBLIC / 'camera3-recording-comparison/wmv-diagnostic/run02'
MASS = 'org.opensourcephysics.cabrillo.tracker.PointMass'
NUMBER = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z')
FRAMES = list(range(138, 349, 3))
VIEWS = list(range(138, 349, 30))
CONFIG = {'xorigin', 'yorigin', 'angle', 'xscale', 'yscale', 'delta_t',
          'startframe', 'stepsize', 'stepcount', 'starttime', 'video_framecount'}
FIXED = {
    'project': '955d1c2d00d7c287f4f235063eb603a0080cf0941595a5419aa7c94726c1a41c',
    'settings': 'ccfd9c4de098539680caf9f296eb5ea784ade27497d860a32284285e577cefeb',
    'map': '8afdf759ecc45215b9212699ef2adb72de553c52667d82b39c9382df8e6b36c2',
    'source': '48323b680259b1a9eaf60cc11e11a4b254e8d255e1b73bb9d0cd23bfa5622722',
    'protocol': 'd7fd79c3269155a06225346273aab4a6352c14c233beda4fa88989d244d3ec01',
    'points': 'f85e6f0ddbb55e3ef142a62e774237c69a59b9bbcbc31a92f93a37b9a9099df3',
    'extraction_code': '08a851c45103516015b07c291ff06ca8e4596c7d9b7b60831515becdb9ea4c2f',
    'views_code': 'ea8f3d1b156db207c4e8d9ff9eb96ed27511792d6f2e739b80f7edc976ef13e4',
}
COEFFICIENT_TOLERANCE = Q(1, 10**9)
SSE_TOLERANCE = Q(1, 10**8)


class AuditFailure(ValueError):
    """Only fixed programmer-authored check labels are allowed here."""


def require(condition, label):
    if not condition:
        raise AuditFailure(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha(data)}


def numeric(text):
    require(isinstance(text, str) and len(text) <= 64 and
            NUMBER.fullmatch(text) is not None, 'numeric_literal_shape')
    require(math.isfinite(float(text)), 'numeric_literal_finite')
    return text


def one(items, label):
    require(len(items) == 1, label)
    return items[0]


def property_child(node, key):
    return one([p for p in node if p.tag == 'property' and
                p.attrib.get('name') == key], 'expected_single_property')


def independent_source(data):
    require(len(data) <= 10_000_000 and b'<!DOCTYPE' not in data.upper()
            and b'<!ENTITY' not in data.upper(), 'xml_envelope')
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        raise ValueError('xml_parse_failed') from None
    collection = property_child(root, 'tracks')
    masses = []
    for sibling in collection:
        if sibling.tag != 'property':
            continue
        masses.extend(obj for obj in sibling if obj.tag == 'object' and
                      obj.attrib.get('class') == MASS)
    require(len(masses) == 2, 'pointmass_count')
    tracks = []
    for ordinal, mass in enumerate(masses, 1):
        entries = property_child(mass, 'framedata')
        result = []
        for entry in entries:
            match = re.fullmatch(r'\[([0-9]+)\]', entry.attrib.get('name', ''))
            require(entry.tag == 'property' and match is not None,
                    'frame_entry_shape')
            frame = int(match[1])
            obj = one(list(entry), 'frame_single_object')
            require(obj.tag == 'object' and obj.attrib.get('class') == MASS + '$FrameData',
                    'frame_object_class')
            row = {'frame': frame}
            for axis in ('x', 'y'):
                field = property_child(obj, axis)
                require(field.attrib.get('type') == 'double', 'frame_numeric_type')
                value = numeric((field.text or '').strip())
                row[axis + '_text'] = value
                row[axis] = float(value)
            result.append(row)
        require([r['frame'] for r in result] == FRAMES, 'frame_indices')
        tracks.append({'pointmass_ordinal': ordinal, 'track': f'track{ordinal:02d}',
                       'points': result})
    # Read only the pre-approved scalar property names; never output any
    # surrounding names, paths, comments, or other XML values.
    config = {}
    for key in sorted(CONFIG):
        field = one([p for p in root.iter('property') if p.attrib.get('name') == key],
                    'configuration_uniqueness')
        config[key] = numeric((field.text or '').strip())
    return tracks, config


def solve(matrix, rhs):
    """Exact Gauss-Jordan elimination, independent of numerical lstsq."""
    size = len(rhs)
    rows = [[Q(x) for x in a] + [Q(b)] for a, b in zip(matrix, rhs)]
    for k in range(size):
        pivot = next((r for r in range(k, size) if rows[r][k]), None)
        require(pivot is not None, 'rank_deficient')
        rows[k], rows[pivot] = rows[pivot], rows[k]
        d = rows[k][k]
        rows[k] = [v / d for v in rows[k]]
        for r in range(size):
            if r != k:
                d = rows[r][k]
                rows[r] = [v - d*w for v, w in zip(rows[r], rows[k])]
    return [r[-1] for r in rows]


def exact_fit(times, values, degree):
    times, values = list(map(Q, times)), list(map(Q, values))
    require(len(times) == len(values) and len(times) > degree,
            'fit_sample_count')
    require(all(b > a for a, b in zip(times, times[1:])), 'fit_clock_order')
    center = (times[0] + times[-1]) / 2
    halfspan = (times[-1] - times[0]) / 2
    z = [(t - center) / halfspan for t in times]
    rows = [[t**k for k in range(degree + 1)] for t in z]
    normal = [[sum(row[i]*row[j] for row in rows)
               for j in range(degree + 1)] for i in range(degree + 1)]
    rhs = [sum(row[i]*v for row, v in zip(rows, values))
           for i in range(degree + 1)]
    coefficients = solve(normal, rhs)
    predicted = [sum(a*b for a, b in zip(coefficients, row)) for row in rows]
    residuals = [v-p for v, p in zip(values, predicted)]
    result = {'center': center, 'halfspan': halfspan, 'coefficients': coefficients,
              'predicted': predicted, 'residuals': residuals,
              'sse': sum(r*r for r in residuals),
              'velocity': coefficients[1]/halfspan if degree >= 1 else Q(0),
              'acceleration': 2*coefficients[2]/halfspan**2 if degree >= 2 else Q(0)}
    if degree == 2:
        dual = solve(normal, [Q(0), Q(0), 2/halfspan**2])
        weights = [sum(a*b for a, b in zip(dual, row)) for row in rows]
        require(sum(w*v for w, v in zip(weights, values)) == result['acceleration'],
                'exact_weight_identity')
        result.update(weights=weights, max_weight=max(map(abs, weights)),
                      l1_weight=sum(map(abs, weights)))
    return result


@lru_cache(maxsize=None)
def cached_fit(times, values, degree):
    return exact_fit(times, values, degree)


@lru_cache(maxsize=None)
def gram_condition(times, degree):
    """Independent Jacobi diagonalization of the normalized Gram matrix."""
    center, half = (times[0]+times[-1])/2, (times[-1]-times[0])/2
    z = [(t-center)/half for t in times]
    n = degree+1
    a = [[float(sum(t**(i+j) for t in z)) for j in range(n)] for i in range(n)]
    for unused in range(200):
        p, q = max(((i,j) for i in range(n) for j in range(i+1,n)),
                   key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < 1e-15:
            break
        angle = math.atan2(2*a[p][q], a[q][q]-a[p][p])/2
        c, s = math.cos(angle), math.sin(angle)
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = c*c*app-2*s*c*apq+s*s*aqq
        a[q][q] = s*s*app+2*s*c*apq+c*c*aqq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k != p and k != q:
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c*akp-s*akq
                a[k][q] = a[q][k] = s*akp+c*akq
    else:
        raise AuditFailure('independent_eigen_convergence')
    eigenvalues = [a[i][i] for i in range(n)]
    require(min(eigenvalues)>0, 'independent_positive_gram')
    return math.sqrt(max(eigenvalues)/min(eigenvalues))


@lru_cache(maxsize=None)
def rotation(angle):
    """Decimal Taylor sine/cosine, not producer math trig or matrix code."""
    with localcontext() as ctx:
        ctx.prec = 70
        pi = Decimal('3.141592653589793238462643383279502884197169399375105820974944592307816')
        r = Decimal(angle.numerator)/Decimal(angle.denominator)*pi/180
        cosine = ct = Decimal(1)
        sine = st = r
        for k in range(1, 120):
            ct *= -r*r/((2*k-1)*(2*k))
            st *= -r*r/((2*k)*(2*k+1))
            cosine += ct
            sine += st
            if max(abs(ct),abs(st)) < Decimal('1e-65'):
                return Q(cosine), Q(sine)
    raise AuditFailure('independent_trig_convergence')


def assigned(vector, angle, scale, count):
    c, s = rotation(angle)
    x, y = vector
    factor = Q(count,15)/scale
    return [(c*x-s*y)*factor, (s*x+c*y)*factor]


class Comparisons:
    def __init__(self):
        self.counts = {}
        self.max_errors = {}
        self.failures = []

    def near(self, actual, expected, family, location, tolerance=COEFFICIENT_TOLERANCE):
        require(isinstance(actual,(int,float)) and not isinstance(actual,bool)
                and math.isfinite(actual), 'finite_fit_scalar')
        error = abs(Q(actual)-Q(expected))
        self.counts[family] = self.counts.get(family,0)+1
        self.max_errors[family] = max(self.max_errors.get(family,Q(0)),error)
        if error > tolerance:
            self.failures.append({'location':location,'family':family,
                                  'actual':actual,'expected':float(expected),
                                  'absolute_error':float(error),'tolerance':float(tolerance)})

    def vector(self, actual, expected, family, location, tolerance=COEFFICIENT_TOLERANCE):
        require(isinstance(actual,list) and len(actual)==len(expected), 'fit_vector_shape')
        for i,(a,e) in enumerate(zip(actual,expected)):
            self.near(a,e,family,f'{location}/{i}',tolerance)

    def result(self):
        return {'scalar_comparisons':self.counts,
                'maximum_absolute_errors':{k:float(v) for k,v in self.max_errors.items()},
                'discrepancies':self.failures}


def exact_controls():
    t = [Q(i, 5) for i in range(9)]
    result = []
    for degree in range(4):
        y = [sum(Q(k+1)*v**k for k in range(degree+1)) for v in t]
        f = exact_fit(t, y, max(1, degree))
        require(f['sse'] == 0, 'polynomial_control')
        center = f['center']
        v = sum(Q(k*(k+1))*center**(k-1) for k in range(1, degree+1))
        a = sum(Q(k*(k-1)*(k+1))*center**(k-2) for k in range(2, degree+1))
        require(f['velocity'] == v and f['acceleration'] == a, 'derivative_control')
        result.append(f'exact_polynomial_degree_{degree}')
    irregular = [Q(0), Q(1,7), Q(2,5), Q(1), Q(13,8)]
    f = exact_fit(irregular, [2+3*v+5*v*v for v in irregular], 2)
    require(f['sse'] == 0 and f['acceleration'] == 10, 'irregular_clock_control')
    result.append('irregular_quadratic')
    try:
        exact_fit([0, 1, 1, 2, 3], [0]*5, 2)
    except ValueError:
        result.append('duplicate_clock_rejected')
    else:
        raise ValueError('duplicate_clock_control')
    values = [3+2*v+5*v*v for v in t]
    f = exact_fit(t, values, 2)
    translated = exact_fit([v+100 for v in t], [v+50 for v in values], 2)
    require(translated['acceleration'] == f['acceleration'] and
            translated['velocity'] == f['velocity'], 'translation_control')
    result.append('space_time_translation')
    perturbed = values.copy()
    perturbed[3] += 1
    f2 = exact_fit(t, perturbed, 2)
    require(f2['acceleration']-f['acceleration'] == f['weights'][3], 'weight_control')
    result.append('unit_point_response')
    dilated = exact_fit([2*v for v in t], [3*v for v in values], 2)
    require(dilated['acceleration'] == Q(3,4)*f['acceleration'], 'scale_clock_control')
    result.append('length_linear_clock_inverse_square')
    return result


def artifacts():
    paths = {'project': KIT/'nested/Camera3-test_Camera3-test.trk',
             'settings': KIT/'saved-tracker-settings.json', 'map': OLD/'default-frames.json',
             'source': KIT/'outer/The Kit/WTC7-Camera 3/videos/Camera3.wmv',
             'protocol': HERE/'PROTOCOL.md', 'points': HERE/'extraction01/points.json',
             'extraction_code': HERE/'extract_points.py', 'views_code': HERE/'prepare_views.py',
             'extraction_receipt': HERE/'extraction01/receipt.json',
             'views_receipt': HERE/'views01/receipt.json', 'prior_receipt': OLD/'receipt.json',
             'binary': Path('/opt/homebrew/bin/ffmpeg'), 'verifier': Path(__file__).resolve(),
             'python': Path(sys.executable).resolve()}
    for i in VIEWS:
        paths[f'native_{i}'] = HERE/f'views01/frame-{i:04d}.png'
        paths[f'overlay_{i}'] = HERE/f'views01/queries-{i:04d}.png'
    before = {k: pin(p) for k, p in paths.items()}
    for k, h in FIXED.items():
        require(before[k]['sha256'] == h, 'fixed_subject_hash')
    points = json.loads(paths['points'].read_text())
    er = json.loads(paths['extraction_receipt'].read_text())
    vr = json.loads(paths['views_receipt'].read_text())
    old = json.loads(paths['prior_receipt'].read_text())
    fmap = json.loads(paths['map'].read_text())
    settings = json.loads(paths['settings'].read_text())
    emap = {'source_project': 'project', 'sanitized_settings': 'settings',
            'frame_map': 'map', 'protocol': 'protocol', 'producer': 'extraction_code'}
    vmap = {'source': 'source', 'binary': 'binary', 'prior_receipt': 'prior_receipt',
            'map': 'map', 'points': 'points', 'point_receipt': 'extraction_receipt',
            'protocol': 'protocol', 'producer': 'views_code'}
    for receipt, mapping in ((er, emap), (vr, vmap)):
        expected = {k: before[v] for k, v in mapping.items()}
        require(receipt['inputs_before'] == expected == receipt['inputs_after'],
                'receipt_dependency_join')
    require(er['status'] == 'pass_numeric_only_extraction' and
            er['track_counts'] == [71,71] and er['points'] == before['points'] and
            er['arbitrary_source_names_paths_comments_exported'] is False,
            'extraction_receipt_shape')
    source_tracks, source_config = independent_source(paths['project'].read_bytes())
    require(set(points) == {'configuration','current_diagnostic_clock','source_sha256',
                           'status','tracks'}, 'points_allowlist')
    require(points['source_sha256'] == FIXED['project'] and
            points['status'] == 'conditional_saved_annotations_not_validated_material_tracks',
            'points_identity')
    require(points['tracks'] == source_tracks, 'all_source_point_values')
    require(set(points['configuration']) == CONFIG, 'configuration_allowlist')
    for key in sorted(CONFIG):
        sanitized = one([v['saved_text'] for v in settings['selected_scalar_properties']
                         if v['xml_path'].endswith('/property:'+key)],
                        'sanitized_configuration_count')
        require(sanitized == source_config[key], 'original_sanitized_configuration')
        require(points['configuration'][key] == {'text':sanitized,'value':float(sanitized)},
                'extracted_configuration')
    clock = points['current_diagnostic_clock']
    require(len(clock) == 304, 'clock_count')
    for i, row in zip(range(138,442), clock):
        expected = {k: fmap['records'][i][k] for k in ('index','pts','time_base','seconds_exact')}
        require(row == expected and row['index'] == i, 'clock_record')
        require(Q(row['pts'])*Q(row['time_base']) == Q(row['seconds_exact']), 'clock_rational')
    nominal_equal = [Q(fmap['records'][i]['seconds_exact'])-
                     Q(fmap['records'][138]['seconds_exact']) == Q(i-138,15) for i in FRAMES]
    require(all(nominal_equal), 'saved_row_clock_equality')
    require(vr['status'] == 'pass_diagnostic_view_only' and
            [r['index'] for r in vr['selected']] == VIEWS, 'view_coverage')
    ex = vr['execution']
    old_command = one([c for c in old['commands'] if c['label']=='default'], 'old_default_command')
    require(ex['argv'] == old_command['argv'] and ex['returncode'] == 0 and
            ex['all_frame_hashes_match'] is True and ex['raw_bytes'] == 442*720*480 and
            ex['raw_sha256'] == fmap['raw_sha256'], 'recorded_full_decode_join')
    require(before['binary']['sha256'] == old['binaries'][str(paths['binary'])]['sha256'],
            'old_binary_join')
    product_results = []
    for item in vr['selected']:
        index = item['index']
        native_path, marked_path = paths[f'native_{index}'], paths[f'overlay_{index}']
        require(item['native'] == {'name':native_path.name,**before[f'native_{index}']} and
                item['overlay'] == {'name':marked_path.name,**before[f'overlay_{index}']},
                'selected_product_hash')
        with Image.open(native_path) as im:
            require(im.format == 'PNG' and im.mode == 'L' and im.size == (720,480), 'native_image_shape')
            native = im.tobytes()
        require(sha(native) == item['pixel_sha256'] == fmap['pixel_hashes'][index],
                'native_old_pixel_hash')
        expected = bytearray(channel for value in native for channel in (value,value,value))
        marks = []
        locations = set()
        for ordinal, color in enumerate(((0,255,255),(255,255,0))):
            row = source_tracks[ordinal]['points'][FRAMES.index(index)]
            x, y = row['x'], row['y']
            cx, cy = round(x), round(y)
            marks.append({'track':f'track{ordinal+1:02d}', 'x':x,'y':y,
                          'raster_center':[cx,cy],'rgb':list(color),
                          'within_native_bounds':0<=x<720 and 0<=y<480,
                          'cross_box_inside':12<=cx<708 and 12<=cy<468})
            # Independent integer pixel-set construction; no drawing API.
            cross = {(cx+d,cy) for d in list(range(-12,-3))+list(range(4,13))}
            cross |= {(cx,cy+d) for d in list(range(-12,-3))+list(range(4,13))}
            for px, py in cross:
                if 0<=px<720 and 0<=py<480:
                    offset = 3*(py*720+px)
                    expected[offset:offset+3] = bytes(color)
                    locations.add((px,py))
        require(item['marks'] == marks, 'query_mark_metadata')
        with Image.open(marked_path) as im:
            require(im.format == 'PNG' and im.mode == 'RGB' and im.size == (720,480),
                    'overlay_shape')
            require(im.tobytes() == bytes(expected), 'all_overlay_pixels')
        product_results.append({'index':index,'native_pixel_sha256':sha(native),
                                'overlay_pixels_checked':720*480,
                                'analytical_mark_pixel_union':len(locations)})
    after = {k:pin(p) for k,p in paths.items()}
    require(before == after, 'independent_inputs_unchanged')
    return {'pins_before':before,'pins_after':after,'point_pairs':142,
            'source_numeric_coordinate_literals':284,'configuration_fields':11,
            'clock_records':304,'unique_saved_clock_comparisons':71,
            'clock_rows_used_by_tracks':142,'nominal_vs_pts_all_saved_rows_equal':True,
            'native_images':8,'overlay_images':8,'overlay_pixels_checked':8*720*480,
            'products':product_results,
            'scope':'Source numeric allowlist and artifact integrity; no second decode, image interpretation, physical track identity, historic exposure authentication or fit-result comparison.'}


def check_control_records(records, comparison):
    names = ['constant','linear','quadratic','cubic','irregular_clock_quadratic',
             'duplicate_time','insufficient_rank_domain','transform_basis_signs',
             'length_and_clock_rate_laws','time_and_position_translation',
             'one_pixel_response','continuous_piecewise_acceleration_average']
    require([r.get('name') for r in records] == names and
            all(r.get('pass') is True for r in records), 'declared_control_records')
    for i,r in enumerate(records):
        expected_keys = {'name','pass'}
        if i == 11:
            expected_keys |= {'true_acceleration_before','true_acceleration_after',
                             'straddling_window_acceleration'}
        require(set(r) == expected_keys, 'control_fieldset')
    t = [Q(i,5) for i in range(21)]
    for degree,coef in [(2,[4,0,0]),(2,[4,3,0]),(2,[4,3,2]),(3,[4,3,2,Q(2,5)])]:
        y = [sum(c*v**k for k,c in enumerate(coef)) for v in t]
        for factor in (1,-2):
            f = exact_fit(t,[factor*v for v in y],degree)
            require(f['sse'] == 0, 'matching_control_polynomial')
            expected_v = factor*sum(k*c*Q(2)**(k-1) for k,c in enumerate(coef) if k>=1)
            expected_a = factor*sum(k*(k-1)*c*Q(2)**(k-2) for k,c in enumerate(coef) if k>=2)
            require(f['velocity'] == expected_v and f['acceleration'] == expected_a,
                    'matching_control_derivatives')
    irregular = list(map(Q,['0','.13','.4','.9','1.35','2.1','3.0']))
    ys = [[3+2*v+4*v*v for v in irregular],[7-3*v+2*v*v for v in irregular]]
    bases = [exact_fit(irregular,y,2) for y in ys]
    require([f['acceleration'] for f in bases] == [8,4], 'matching_irregular_control')
    for times in ([0,1,1,2],[0,1]):
        try:
            exact_fit(times,[0]*len(times),2)
        except AuditFailure:
            pass
        else:
            raise AuditFailure('matching_rejection_control')
    for angle, expected in [(Q(0),[[Q(1,2),0],[0,Q(1,2)]]),
                            (Q(90),[[0,Q(1,2)],[-Q(1,2),0]])]:
        for vec,e in zip(([Q(1),Q(0)],[Q(0),Q(1)]),expected):
            require(all(abs(a-b)<COEFFICIENT_TOLERANCE
                        for a,b in zip(assigned(vec,angle,Q(2),15),e)), 'matching_sign_control')
    for factor in (Q(14,15),Q(16,15)):
        for axis in range(2):
            fit = exact_fit([Q(5,4)*v for v in irregular],[factor*v for v in ys[axis]],2)
            require(fit['acceleration'] == bases[axis]['acceleration']*factor/Q(5,4)**2,
                    'matching_scale_clock_control')
    for axis, offset in enumerate((80,-40)):
        shifted = exact_fit([v+37 for v in irregular],[v+offset for v in ys[axis]],2)
        require(shifted['acceleration'] == bases[axis]['acceleration'], 'matching_origin_control')
    altered = ys[0].copy()
    altered[2] += 1
    require(exact_fit(irregular,altered,2)['acceleration']-bases[0]['acceleration'] ==
            bases[0]['weights'][2], 'matching_unit_response_control')
    piecewise = [max(v-2,0)**2 for v in t]
    piecewise_fit = exact_fit(t,piecewise,2)
    require(piecewise_fit['acceleration'] == 1, 'matching_piecewise_control')
    last = records[-1]
    require(last['true_acceleration_before'] == 0 and last['true_acceleration_after'] == 2,
            'piecewise_true_values')
    comparison.near(last['straddling_window_acceleration'],Q(1),'control_value','piecewise')
    return {'matched_record_names':names,'independent_analytic_control_cases':12,
            'limit':'Independent analogues verify the declared mathematics; sparse producer control flags do not preserve all original control intermediate arrays.'}


def verify_fit_run(run_name, source_result):
    require(re.fullmatch(r'fit[0-9]{2}',run_name) is not None, 'fit_run_name')
    folder = HERE/run_name
    product_names = ['clocks.json','controls.json','fits.json','summary.json','trajectories.json']
    require({p.name for p in folder.iterdir()} == set(product_names+['receipt.json']),
            'fit_product_inventory')
    paths = {n:folder/n for n in product_names+['receipt.json']}
    paths.update(producer=HERE/'fit_trajectories.py', points=HERE/'extraction01/points.json',
                 extraction_receipt=HERE/'extraction01/receipt.json',protocol=HERE/'PROTOCOL.md',
                 verifier=Path(__file__).resolve())
    before = {k:pin(p) for k,p in paths.items()}
    require(before['producer']['sha256'] == 'dd8bbcb594d71f8d5085b7322e8292035127b4860112595c850fe0c41a2f32b4',
            'fit_producer_subject_hash')
    require(before['points'] == source_result['pins_after']['points'] and
            before['protocol'] == source_result['pins_after']['protocol'] and
            before['extraction_receipt'] == source_result['pins_after']['extraction_receipt'],
            'fit_source_verification_join')
    receipt = json.loads(paths['receipt.json'].read_text())
    deps = {n:before[n] for n in ('producer','points','extraction_receipt','protocol')}
    require(receipt['inputs_before'] == deps == receipt['inputs_after'], 'fit_dependency_pins')
    require(receipt['products'] == {n:before[n] for n in product_names}, 'fit_product_pins')
    require(receipt['status'] == 'conditional_saved_point_reconstruction' and
            receipt['controls_passed'] == 12 and receipt['record_count'] == 964 and
            receipt['failed_count'] == 0, 'fit_receipt_coverage')
    compare = Comparisons()
    control_result = check_control_records(json.loads(paths['controls.json'].read_text()),compare)
    # Source points and all historical results are opened only after the
    # independent exact controls and fixed pre-output tolerances are in place.
    source = json.loads(paths['points'].read_text())
    clocks = json.loads(paths['clocks.json'].read_text())
    exact_clocks = {'nominal':[Q(n-138,15) for n in FRAMES]}
    source_clock = {r['index']:Q(r['pts'])*Q(r['time_base']) for r in source['current_diagnostic_clock']}
    exact_clocks['encoded'] = [source_clock[n]-source_clock[138] for n in FRAMES]
    require(clocks == {k:list(map(str,v)) for k,v in exact_clocks.items()}, 'all_fitted_clock_rows')
    scale = Q(source['configuration']['xscale']['value'])
    require(scale>0 and source['configuration']['xscale']==source['configuration']['yscale'],
            'equal_positive_scale')
    angle = Q(source['configuration']['angle']['value'])
    scenarios = [(label,a,count) for label,a in [('zero',Q(0)),('saved',angle)] for count in (14,15,16)]
    trajectories = json.loads(paths['trajectories.json'].read_text())
    require(len(trajectories)==2, 'trajectory_count')
    source_values = {}
    for item,track in zip(trajectories,source['tracks']):
        require(set(item)=={'track','frames','image_displacement_xy_pixels','geometry_scenarios'} and
                item['track']==track['track'] and item['frames']==FRAMES, 'trajectory_shape')
        xy = [[Q(p['x']),Q(p['y'])] for p in track['points']]
        source_values[track['track']] = xy
        delta = [[p[axis]-xy[0][axis] for axis in range(2)] for p in xy]
        require(len(item['image_displacement_xy_pixels'])==71, 'pixel_trajectory_length')
        for i,(actual,expected) in enumerate(zip(item['image_displacement_xy_pixels'],delta)):
            compare.vector(actual,expected,'image_displacement',f"{track['track']}/{i}")
        require(len(item['geometry_scenarios'])==6, 'trajectory_geometry_coverage')
        for g,(label,a,count) in zip(item['geometry_scenarios'],scenarios):
            require(set(g)=={'angle','intervals','angle_degrees','length_factor','displacement_X_D_assigned_m'} and
                    g['angle']==label and g['intervals']==count, 'trajectory_geometry_identity')
            compare.near(g['angle_degrees'],a,'geometry_parameters',label+'/angle')
            compare.near(g['length_factor'],Q(count,15),'geometry_parameters',label+'/factor')
            require(len(g['displacement_X_D_assigned_m'])==71, 'assigned_trajectory_length')
            for i,(actual,v) in enumerate(zip(g['displacement_X_D_assigned_m'],delta)):
                compare.vector(actual,assigned(v,a,scale,count),'assigned_displacement',
                               f"{track['track']}/{label}/{count}/{i}")
    windows = [(s,s+n) for n in (5,9,13,21) for s in range(71-n+1)]+[(0,71)]
    require(len(windows)==241, 'independent_declared_window_count')
    records = json.loads(paths['fits.json'].read_text())
    identities = [(track['track'],clock,start,stop) for track in source['tracks']
                  for clock in ('nominal','encoded') for start,stop in windows]
    require(len(records)==len(identities)==964, 'all_window_records')
    independent_rows = []
    residual_count = 0
    weight_count = 0
    expected_fields = {'track','clock','start_mark','stop_mark_exclusive','first_frame',
                       'last_frame','count','time_exact','status','fits','geometry_scenarios'}
    for row_number,(row,(track,clock,start,stop)) in enumerate(zip(records,identities)):
        require(set(row)==expected_fields and row['status']=='pass', 'window_status_shape')
        require((row['track'],row['clock'],row['start_mark'],row['stop_mark_exclusive']) ==
                (track,clock,start,stop) and row['count']==stop-start and
                row['first_frame']==FRAMES[start] and row['last_frame']==FRAMES[stop-1],
                'exact_window_identity')
        exact_t = exact_clocks[clock][start:stop]
        require(row['time_exact']==list(map(str,exact_t)), 'exact_window_times')
        times = tuple(Q(float(v)) for v in exact_t)
        values = tuple(tuple(v[axis] for v in source_values[track][start:stop]) for axis in range(2))
        require(set(row['fits'])=={'1','2','3'}, 'polynomial_degree_coverage')
        independent = {}
        conditions = []
        for degree in (1,2,3):
            fits = [cached_fit(times,axis,degree) for axis in values]
            independent[degree] = fits
            actual = row['fits'][str(degree)]
            fieldset = {'degree','center_seconds','halfspan_seconds','coefficients_xy',
                        'residual_xy_pixels','sse_xy_pixels2','rmse_xy_pixels',
                        'max_abs_residual_xy_pixels','condition_2','rank','center_velocity_xy_pixels_per_s'}
            if degree>=2:
                fieldset.add('center_acceleration_xy_pixels_per_s2')
            if degree==2:
                fieldset |= {'acceleration_response_weights_per_s2',
                             'single_point_unit_response_max_per_s2',
                             'simultaneous_unit_response_bound_per_s2'}
            require(set(actual)==fieldset and actual['degree']==degree and
                    actual['rank']==degree+1, 'fit_fieldset_rank')
            location = f'{row_number}/degree{degree}'
            compare.near(actual['center_seconds'],fits[0]['center'],'time_parameters',location+'/center')
            compare.near(actual['halfspan_seconds'],fits[0]['halfspan'],'time_parameters',location+'/halfspan')
            require(len(actual['coefficients_xy'])==degree+1, 'coefficient_count')
            for k,pair in enumerate(actual['coefficients_xy']):
                compare.vector(pair,[f['coefficients'][k] for f in fits],'coefficients',location+f'/coef{k}')
            require(len(actual['residual_xy_pixels'])==stop-start, 'all_residual_rows')
            for i,pair in enumerate(actual['residual_xy_pixels']):
                compare.vector(pair,[f['residuals'][i] for f in fits],'residuals',location+f'/residual{i}')
                residual_count += 2
            compare.vector(actual['sse_xy_pixels2'],[f['sse'] for f in fits],'sse',location,SSE_TOLERANCE)
            compare.vector(actual['rmse_xy_pixels'],[math.sqrt(float(f['sse']/(stop-start))) for f in fits],
                           'rmse',location)
            compare.vector(actual['max_abs_residual_xy_pixels'],[max(map(abs,f['residuals'])) for f in fits],
                           'max_residual',location)
            condition = gram_condition(times,degree)
            conditions.append(condition)
            compare.near(actual['condition_2'],condition,'condition_2',location)
            compare.vector(actual['center_velocity_xy_pixels_per_s'],[f['velocity'] for f in fits],
                           'velocity',location)
            if degree>=2:
                compare.vector(actual['center_acceleration_xy_pixels_per_s2'],[f['acceleration'] for f in fits],
                               'acceleration',location)
            if degree==2:
                weights = fits[0]['weights']
                compare.vector(actual['acceleration_response_weights_per_s2'],weights,'response_weights',location)
                weight_count += len(weights)
                compare.near(actual['single_point_unit_response_max_per_s2'],max(map(abs,weights)),
                             'response_max',location)
                compare.near(actual['simultaneous_unit_response_bound_per_s2'],sum(map(abs,weights)),
                             'response_l1',location)
        require(len(row['geometry_scenarios'])==6, 'quadratic_geometry_count')
        qfits = independent[2]
        velocity = [f['velocity'] for f in qfits]
        acceleration = [f['acceleration'] for f in qfits]
        assigned_saved = None
        for g,(label,a,count) in zip(row['geometry_scenarios'],scenarios):
            require(set(g)=={'angle','intervals','velocity_X_D_assigned_m_per_s',
                            'acceleration_X_D_assigned_m_per_s2'} and
                    g['angle']==label and g['intervals']==count, 'quadratic_geometry_identity')
            expected_v = assigned(velocity,a,scale,count)
            expected_a = assigned(acceleration,a,scale,count)
            compare.vector(g['velocity_X_D_assigned_m_per_s'],expected_v,'assigned_velocity',
                           f'{row_number}/{label}/{count}')
            compare.vector(g['acceleration_X_D_assigned_m_per_s2'],expected_a,'assigned_acceleration',
                           f'{row_number}/{label}/{count}')
            if label=='saved' and count==15:
                assigned_saved = expected_a
        independent_rows.append({'row':row_number,'track':track,'clock':clock,'start_mark':start,
                                 'stop_mark_exclusive':stop,'count':stop-start,
                                 'quadratic_acceleration_xy_pixels_per_s2':list(map(float,acceleration)),
                                 'saved15_acceleration_X_D_assigned_m_per_s2':list(map(float,assigned_saved)),
                                 'sse_by_degree_xy_pixels2':{str(d):[float(f['sse']) for f in independent[d]] for d in (1,2,3)},
                                 'conditions_by_degree':conditions})
    summary = json.loads(paths['summary.json'].read_text())
    require(set(summary)=={'status','record_count','failed_count','clock_rows_equal_exactly',
                          'conventional_gravity_reference_m_per_s2','groups'} and
            summary['status']=='conditional_saved_point_reconstruction' and
            summary['record_count']==964 and summary['failed_count']==0 and
            summary['clock_rows_equal_exactly'] is (exact_clocks['nominal']==exact_clocks['encoded']),
            'summary_shape_counts')
    compare.near(summary['conventional_gravity_reference_m_per_s2'],Q('9.80665'),'gravity_reference','summary')
    expected_groups = []
    for track in ('track01','track02'):
        for count in (5,9,13,21,71):
            items = [r for r in independent_rows if r['track']==track and r['clock']=='nominal' and r['count']==count]
            vals = [r['saved15_acceleration_X_D_assigned_m_per_s2'][1] for r in items]
            expected_groups.append({'track':track,'window_points':count,'windows':len(vals),
                                    'min_D_acceleration':min(vals),'max_D_acceleration':max(vals)})
    require(len(summary['groups'])==10, 'summary_group_count')
    for actual,expected in zip(summary['groups'],expected_groups):
        require(set(actual)==set(expected) and all(actual[k]==expected[k] for k in ('track','window_points','windows')),
                'summary_group_identity')
        for key in ('min_D_acceleration','max_D_acceleration'):
            compare.near(actual[key],expected[key],'summary_extrema',str(expected['window_points'])+'/'+key)
    after = {k:pin(p) for k,p in paths.items()}
    require(before==after, 'fit_inputs_unchanged')
    return {'pins_before':before,'pins_after':after,'control_review':control_result,
            'coverage':{'window_records':964,'polynomial_fit_axis_cases':5784,
                        'residual_scalars':residual_count,'quadratic_weight_entries':weight_count,
                        'quadratic_geometry_cases':964*6,'trajectory_geometry_cases':12,
                        'all_failed_windows':0},
            'comparisons':compare.result(),'independent_windows':independent_rows,
            'independent_summary_groups':expected_groups,
            'scope':'Conditional saved-annotation/clock/affine geometry arithmetic. No feature identity, exposure authentication, projection bound, g equivalence threshold, force or mechanism inference.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit-run')
    parser.add_argument('--out')
    args = parser.parse_args()
    output = None
    if args.out:
        require(re.fullmatch(r'independent-[a-z0-9_-]+\.json',args.out) is not None, 'receipt_name')
        output = HERE/args.out
        require(not output.exists(), 'receipt_already_exists')
    result = {'status':'pass','python':platform.python_version(),'pillow':PILLOW,
              'command':sys.argv,
              'verifier':pin(Path(__file__)),
              'prospective_tolerances':{'coefficients_and_derivatives':'1e-9 absolute',
                                        'sse':'1e-8 absolute','source_windows':'exact'},
              'independent_exact_controls':exact_controls(),
              'artifacts':artifacts()}
    if args.fit_run:
        result['fits'] = verify_fit_run(args.fit_run,result['artifacts'])
        if result['fits']['comparisons']['discrepancies']:
            result['status'] = 'fail_numeric_discrepancies'
    encoded = json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if output:
        output.write_text(encoded)
        print(json.dumps({'status':result['status'],'source_pairs':142,
                          'fit_windows':964 if args.fit_run else 0,
                          'receipt':output.name,'receipt_sha256':sha(encoded.encode())}))
    else:
        print(encoded)
    if result['status'] != 'pass':
        raise SystemExit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # No source-derived exception text or traceback is exported.
        failure = {'status':'fail','exception_type':type(exc).__name__}
        if isinstance(exc, AuditFailure):
            failure['check'] = str(exc)
        failure['verifier'] = pin(Path(__file__))
        failure['python'] = platform.python_version()
        failure['command'] = sys.argv
        if '--out' in sys.argv:
            pos = sys.argv.index('--out')+1
            if pos < len(sys.argv) and re.fullmatch(r'independent-[a-z0-9_-]+\.json',sys.argv[pos]):
                target = HERE/sys.argv[pos]
                if not target.exists():
                    target.write_text(json.dumps(failure,indent=2,sort_keys=True)+'\n')
        print(json.dumps(failure))
        raise SystemExit(1) from None
