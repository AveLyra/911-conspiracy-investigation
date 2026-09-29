#!/usr/bin/env python3
"""Validate proposal records, source pins and simple box comparisons, not images' meaning."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
MAIN = Path('/Users/admin/docs/911')
EXPECTED = {(frame, label) for frame in (6593, 6841) for label in ('NE', 'EC', 'WC', 'NW')}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def validate(rows):
    result = {}
    for row in rows:
        key = row['frame'], row['label']
        require(key not in result, 'duplicate frame/label')
        bounds = row['bounds']
        require(len(bounds) == 4 and all(type(v) is int for v in bounds), 'integer bounds required')
        x0, y0, x1, y1 = bounds
        require(0 <= x0 <= x1 < 640 and 0 <= y0 <= y1 < 480, 'out-of-frame or reversed bounds')
        center = row['center']
        if row['kind'] == 'region':
            require(center is None, 'ambiguity region cannot be a measured center')
        else:
            require(row['kind'] == 'candidate', 'unknown kind')
            require(isinstance(center, list) and len(center) == 2
                    and all(type(v) is int for v in center), 'integer center required')
            require(x0 <= center[0] <= x1 and y0 <= center[1] <= y1, 'center outside bounds')
        result[key] = row
    require(set(result) == EXPECTED, 'missing or extra frame/label')
    return result


def normalize_root(doc):
    rows = []
    kinds = {'ambiguous_region_only': 'region', 'candidate_junction': 'candidate'}
    for r in doc['annotations']:
        require(r['status'] in kinds, 'unexpected root status')
        rows.append(dict(frame=r['frame_index'], label=r['label'], kind=kinds[r['status']],
                         center=r['center'], bounds=r['bounds']))
    return validate(rows)


def normalize_independent(doc):
    rows = []
    kinds = {'ambiguous_region': 'region', 'visible_projected_junction': 'candidate',
             'visible_corner_candidate': 'candidate'}
    for feature in doc['features']:
        for r in feature['observations']:
            require(r['status'] in kinds, 'unexpected reviewer status')
            rows.append(dict(frame=r['frame_index_zero_based'], label=feature['source_label'],
                             kind=kinds[r['status']], center=r['center'],
                             bounds=r.get('bounds', r.get('region'))))
    return validate(rows)


def compare(a, b):
    x0, y0, x1, y1 = a['bounds']
    u0, v0, u1, v1 = b['bounds']
    pair = a['center'] is not None and b['center'] is not None
    return dict(frame=a['frame'], label=a['label'], root_kind=a['kind'], reviewer_kind=b['kind'],
                status_agrees=a['kind'] == b['kind'],
                subjective_boxes_overlap=max(x0, u0) <= min(x1, u1) and max(y0, v0) <= min(y1, v1),
                reviewer_minus_root_center=[b['center'][i]-a['center'][i] for i in (0, 1)] if pair else None)


class Controls(unittest.TestCase):
    def fixture(self):
        return [dict(frame=f, label=l, kind='candidate', center=[10, 20], bounds=[8, 18, 12, 22])
                for f, l in sorted(EXPECTED)]

    def test_complete_and_signed_comparison(self):
        rows = self.fixture()
        validate(rows)
        other = copy.deepcopy(rows[0]); other['center'] = [9, 21]
        self.assertEqual(compare(rows[0], other)['reviewer_minus_root_center'], [-1, 1])

    def test_duplicate_rejected(self):
        rows = self.fixture(); rows.append(copy.deepcopy(rows[0]))
        with self.assertRaises(ValueError): validate(rows)

    def test_missing_rejected(self):
        with self.assertRaises(ValueError): validate(self.fixture()[1:])

    def test_bad_bounds_rejected(self):
        for box in ([12, 18, 8, 22], [8, 18, 640, 22], [8, -1, 12, 22], [True, 18, 12, 22]):
            rows = self.fixture(); rows[0]['bounds'] = box
            with self.assertRaises(ValueError): validate(rows)

    def test_outside_center_rejected(self):
        rows = self.fixture(); rows[0]['center'] = [13, 20]
        with self.assertRaises(ValueError): validate(rows)

    def test_region_has_no_point(self):
        rows = self.fixture(); rows[0]['kind'] = 'region'
        with self.assertRaises(ValueError): validate(rows)
        rows[0]['center'] = None; validate(rows)
        self.assertIsNone(compare(rows[0], rows[1])['reviewer_minus_root_center'])

    def test_disjoint_and_boundary_touch(self):
        a = self.fixture()[0]; b = copy.deepcopy(a)
        b['bounds'] = [12, 18, 16, 22]
        self.assertTrue(compare(a, b)['subjective_boxes_overlap'])
        b['bounds'] = [13, 18, 17, 22]
        self.assertFalse(compare(a, b)['subjective_boxes_overlap'])


def verify():
    from PIL import Image
    from pypdf import PdfReader
    root_path = HERE/'root-feature-proposal.json'
    reviewer_path = HERE/'independent-feature-proposal.json'
    root = json.loads(root_path.read_text())
    reviewer = json.loads(reviewer_path.read_text())
    require(root['independence']['independent_reviewer_coordinates_received_before_file_freeze'] is True,
            'root exposure must remain explicit')
    require(reviewer['independence']['root_new_annotations_read'] is False, 'independence changed')
    require(reviewer['independence']['old_target_coordinates_read'] is False, 'prior exposure changed')
    require(reviewer['independence']['native_frame_indices_viewed'] == [6593, 6841], 'coverage changed')
    require(reviewer['independence']['additional_native_frames_viewed'] == [], 'coverage expanded')
    a, b = normalize_root(root), normalize_independent(reviewer)
    pdf = (HERE/root['source_pdf']['path']).resolve()
    require(digest(pdf) == root['source_pdf']['sha256'] == reviewer['sources']['paper']['sha256'], 'PDF hash')
    images = [i for i in PdfReader(pdf).pages[12].images if i.name == 'Image76.jpg']
    require(len(images) == 1, 'unique embedded Figure4 image required')
    picture = images[0]
    require(hashlib.sha256(picture.data).hexdigest() == reviewer['sources']['paper']['extracted_image_sha256'],
            'embedded Figure4 hash')
    selection_path = Path(reviewer['sources']['selection']['path'])
    require(digest(selection_path) == root['selection_json_sha256'] == reviewer['sources']['selection']['sha256'],
            'selection hash')
    selection = json.loads(selection_path.read_text())
    selected = {int(r['frame_index_zero_based']): r for r in selection['images']}
    frame_checks = []
    for r in root['coverage']:
        index = r['frame_index']; s = selected[index]
        i = next(x for x in reviewer['sources']['frames'] if x['frame_index_zero_based'] == index)
        path = selection_path.parent/r['png']
        require(digest(path) == r['sha256'] == i['sha256'] == s['png_identity']['sha256'], 'frame hash')
        with Image.open(path) as im:
            require(im.size == (640, 480) and im.mode == 'L', 'native geometry/mode')
            require(hashlib.sha256(im.tobytes()).hexdigest() == s['luma_sha256'], 'luma hash')
        require(str(r['pts']) == s['source_pts'] == i['source_pts_from_selection'], 'PTS mismatch')
        require(r['time_base'] == s['source_time_base'] == i['source_time_base_from_selection'], 'timebase mismatch')
        require(r['time_seconds_exact'] == s['source_time_seconds_exact'], 'exact time mismatch')
        frame_checks.append(dict(frame=index, sha256=r['sha256'], png_luma_pts_checked=True))
    video = MAIN/'research/wtc7-video-comparison/media/analysis-source/NIST Camera 2_CBS-Net Dub6 48 (Converted).mov'
    require(digest(video) == root['source_video_sha256'], 'MOV hash')
    rows = [compare(a[key], b[key]) for key in sorted(EXPECTED)]
    return dict(status='record_and_arithmetic_checks_passed_not_visual_validation',
                scope='two frames/four source labels; root proposal was exposed before saved freeze',
                script_sha256=digest(__file__), root_sha256=digest(root_path), reviewer_sha256=digest(reviewer_path),
                pdf_sha256=digest(pdf), video_sha256=root['source_video_sha256'], frame_checks=frame_checks,
                candidate_pairs=sum(r['reviewer_minus_root_center'] is not None for r in rows),
                region_pairs=sum(r['root_kind'] == r['reviewer_kind'] == 'region' for r in rows),
                rows=rows, independently_blinded_root_replication=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', type=Path); args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
        raise SystemExit(not result.wasSuccessful())
    result = verify()
    payload = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        with args.output.open('x') as stream: stream.write(payload)
    else:
        print(payload, end='')
