"""Persistent synthetic controls only: fake source bytes and mocked ffprobe, no media decode."""
import argparse
import copy
from fractions import Fraction
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import prepare_samples as m

ARTIFACTS = None


def documents(pts=(100, 101, 120, 160)):
    stream = {'index': 0, 'codec_type': 'video', 'codec_name': 'dvvideo', 'width': 96, 'height': 64,
              'time_base': '1001/30000', 'pix_fmt': 'yuv411p',
              'sample_aspect_ratio': '8:9', 'nb_frames': str(len(pts))}
    frames = [{'media_type': 'video', 'stream_index': 0, 'pts': p, 'width': 96, 'height': 64,
               'pix_fmt': 'yuv411p', 'sample_aspect_ratio': '8:9',
               'interlaced_frame': 1, 'top_field_first': 0} for p in pts]
    inventory = {'streams': [copy.deepcopy(stream)], 'frames': frames}
    container = {'format': {'format_name': 'avi'},
                 'streams': [stream, {'index': 1, 'codec_type': 'audio'}]}
    return inventory, container


def response(doc=None, stderr=b'', returncode=0):
    return SimpleNamespace(returncode=returncode, stdout=json.dumps(doc).encode(), stderr=stderr)


class Controls(unittest.TestCase):
    def setUp(self):
        self.case = ARTIFACTS / self._testMethodName
        self.case.mkdir()
        self.binary = self.case / 'synthetic-probe.bin'
        self.binary.write_bytes(b'SYNTHETIC executable identity only; never executed\n')
        self.plan = self.case / 'synthetic-protocol.md'
        self.plan.write_text('Synthetic adapter test; no historical or human acceptance.\n')
        self.items = []
        for n in (1, 2):
            path = self.case / f'synthetic-source-{n}.bin'
            path.write_bytes(f'SYNTHETIC SOURCE {n}\n'.encode())
            self.items.append({'id': f'clip-{n}', 'clip_number': n, 'path': str(path),
                               **m.sampler.observed_identity(path)})
        self.doc = {'schema': m.INPUT_SCHEMA, 'stage': 1, 'sources': self.items}
        self.manifest = self.case / 'declared.json'
        m.sampler.save(self.manifest, self.doc)
        self.binary_patch = patch.object(m.sampler, 'FFPROBE', str(self.binary))
        self.binary_patch.start()
        self.addCleanup(self.binary_patch.stop)

    def probe(self, dest='probe', item=None, effects=None):
        inventory, container = documents()
        replies = effects if effects is not None else [response(container), response(inventory)]
        with patch.object(m.sampler.subprocess, 'run', side_effect=replies) as mocked:
            result = m.probe_source(item or self.items[0], self.case / dest, {'synthetic': True})
        return result, mocked

    def prepare(self, effects=None, out='run', manifest_digest=None, plan_digest=None):
        inventory, container = documents()
        replies = effects if effects is not None else [
            SimpleNamespace(returncode=0, stdout=b'ffprobe version 7.1.1 synthetic\n', stderr=b''),
            response(container), response(inventory), response(container), response(inventory)]
        with patch.object(m.sampler.subprocess, 'run', side_effect=replies) as mocked:
            result = m.prepare(self.manifest, manifest_digest or m.file_sha(self.manifest),
                               self.plan, plan_digest or m.file_sha(self.plan), self.case / out)
        return result, mocked

    def test_irregular_rational_quantiles(self):
        inventory, container = documents()
        frames, stream, tb, counts = m.checked_inventory(inventory, container)
        rows, selected = m.quantile_targets(frames, tb)
        self.assertEqual([r['target_pts_exact'] for r in rows],
                         ['100', '215/2', '115', '245/2', '130', '275/2', '145', '305/2', '160'])
        self.assertEqual([r['selected_index'] for r in rows], [0, 2, 2, 3, 3, 3, 3, 3, 3])
        self.assertEqual(selected, [0, 2, 3])
        self.assertEqual(rows[1]['target_seconds_exact'], str(Fraction(215, 2) * Fraction(1001, 30000)))
        self.assertEqual(len(counts), 2)

    def test_small_clip_deduplicates_but_retains_nine_targets(self):
        for pts in ((0, 5), (-13,), (-7, -2, 6)):
            frames = [{'pts': p} for p in pts]
            rows, indices = m.quantile_targets(frames, Fraction(1, 25))
            self.assertEqual(len(rows), 9)
            self.assertEqual(indices, list(range(len(pts))))
            self.assertEqual(rows[0]['selected_index'], 0)
            self.assertEqual(rows[-1]['selected_index'], len(pts) - 1)

    def test_exact_target_uses_matching_frame_not_next(self):
        rows, selected = m.quantile_targets([{'pts': n} for n in range(9)], Fraction(1, 30))
        self.assertEqual(selected, list(range(9)))
        self.assertEqual([r['selected_pts'] for r in rows], list(range(9)))

    def test_nonincreasing_missing_or_bad_pts(self):
        for pts in ((0, 0), (1, 0), (0, True), (0, 1.0), (0, None)):
            inventory, container = documents(pts)
            with self.subTest(pts=pts), self.assertRaises(m.sampler.Refusal):
                m.checked_inventory(inventory, container)
        inventory, container = documents(); del inventory['frames'][0]['pts']
        with self.assertRaises(m.sampler.Refusal): m.checked_inventory(inventory, container)
        inventory['frames'] = []
        with self.assertRaises(m.sampler.Refusal): m.checked_inventory(inventory, container)

    def test_invalid_geometry(self):
        for field, value in [('width', 97), ('width', True), ('height', 0), ('height', '64')]:
            inventory, container = documents(); inventory['frames'][1][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(m.sampler.Refusal):
                m.checked_inventory(inventory, container)
        inventory, container = documents(); del inventory['frames'][0]['height']
        with self.assertRaises((m.sampler.Refusal, KeyError)): m.checked_inventory(inventory, container)

    def test_time_base_requires_positive_rational_string(self):
        for value in (None, True, 0.5, 'N/A', '0/30', '-1/30', '1/0', '1e-3', '1/2/3'):
            inventory, container = documents(); inventory['streams'][0]['time_base'] = value
            with self.subTest(value=value), self.assertRaises(m.sampler.Refusal):
                m.checked_inventory(inventory, container)
        inventory, container = documents(); container['streams'][0]['time_base'] = '1/25'
        with self.assertRaises(m.sampler.Refusal): m.checked_inventory(inventory, container)

    def test_native_metadata_missing_bad_or_mismatched(self):
        variants = [('sample_aspect_ratio', None), ('sample_aspect_ratio', '0:1'),
                    ('sample_aspect_ratio', '1:1'), ('pix_fmt', 'rgb24'),
                    ('interlaced_frame', True), ('interlaced_frame', 2),
                    ('top_field_first', None), ('stream_index', 1), ('media_type', 'audio')]
        for field, value in variants:
            inventory, container = documents(); inventory['frames'][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(m.sampler.Refusal):
                m.checked_inventory(inventory, container)

    def test_reported_counts_unknown_not_zero_and_mismatches_refused(self):
        for value in ('5', 3, 0, True, 'unknown', '1.5'):
            inventory, container = documents(); inventory['streams'][0]['nb_frames'] = value
            with self.subTest(value=value), self.assertRaises(m.sampler.Refusal):
                m.checked_inventory(inventory, container)
        inventory, container = documents()
        inventory['streams'][0]['nb_frames'] = 'N/A'; del container['streams'][0]['nb_frames']
        self.assertEqual(m.checked_inventory(inventory, container)[3], [])
        inventory['streams'][0]['nb_read_frames'] = '3'
        with self.assertRaises(m.sampler.Refusal): m.checked_inventory(inventory, container)

    def test_selected_video_and_container_contract(self):
        for kind in ('two-selected', 'no-format', 'wrong-index', 'wrong-geometry', 'not-video'):
            inventory, container = documents()
            if kind == 'two-selected': inventory['streams'] *= 2
            elif kind == 'no-format': container.pop('format')
            elif kind == 'wrong-index': container['streams'][0]['index'] = 2
            elif kind == 'wrong-geometry': container['streams'][0]['width'] = 97
            else: inventory['streams'][0]['codec_type'] = 'audio'
            with self.subTest(kind=kind), self.assertRaises(m.sampler.Refusal):
                m.checked_inventory(inventory, container)

    def test_unreviewed_container_or_codec_lane_stops_before_frame_probe(self):
        for i, (field, value) in enumerate((('format_name', 'mov'), ('codec_name', 'h264'),
                                           ('codec_name', None), ('pix_fmt', 'yuv420p'))):
            _, container = documents()
            if field == 'format_name': container['format'][field] = value
            else: container['streams'][0][field] = value
            (receipt, selection), called = self.probe(str(i), effects=[response(container)])
            self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
            self.assertEqual(called.call_count, 1)
            self.assertFalse((self.case / str(i) / 'frames.command.json').exists())

    def test_existing_synthetic_ffv1_lane_retained(self):
        inventory, container = documents()
        for stream in (inventory['streams'][0], container['streams'][0]):
            stream['codec_name'] = 'ffv1'; stream['pix_fmt'] = 'bgr0'
        for frame in inventory['frames']: frame['pix_fmt'] = 'bgr0'
        self.assertEqual(len(m.checked_inventory(inventory, container)[0]), 4)

    def test_declared_stage_schema_and_order(self):
        m.validate_input(self.doc)
        for kind in ('wrong-stage', 'bool-stage', 'one-source', 'reversed', 'duplicate-id',
                     'duplicate-path', 'extra-field', 'bad-size', 'relative', 'bad-hash'):
            doc = copy.deepcopy(self.doc)
            if kind == 'wrong-stage': doc['stage'] = 2
            elif kind == 'bool-stage': doc['stage'] = True
            elif kind == 'one-source': doc['sources'].pop()
            elif kind == 'reversed': doc['sources'].reverse()
            elif kind == 'duplicate-id': doc['sources'][1]['id'] = doc['sources'][0]['id']
            elif kind == 'duplicate-path': doc['sources'][1]['path'] = doc['sources'][0]['path']
            elif kind == 'extra-field': doc['sources'][0]['count'] = 99
            elif kind == 'bad-size': doc['sources'][0]['bytes'] = True
            elif kind == 'relative': doc['sources'][0]['path'] = 'relative.avi'
            else: doc['sources'][0]['sha256'] = 'A' * 64
            with self.subTest(kind=kind), self.assertRaises(m.sampler.Refusal): m.validate_input(doc)

    def test_json_duplicate_and_nonfinite_refused(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(m.sampler.Refusal): m.read_json(raw)

    def test_success_manifest_is_accepted_by_existing_executor_schema(self):
        result, called = self.prepare()
        self.assertEqual(result['status'], 'prepared_not_executed', result)
        self.assertEqual(called.call_count, 5)
        self.assertFalse(result['scientific_or_human_acceptance'])
        out = self.case / 'run'
        manifest = json.loads((out / 'sampling-manifest.json').read_bytes())
        m.sampler.validate_manifest(manifest)
        self.assertEqual([s['indices'] for s in manifest['sources']], [[0, 2, 3], [0, 2, 3]])
        self.assertEqual([s['count'] for s in manifest['sources']], [4, 4])
        target_doc = json.loads((out / 'selection-targets.json').read_bytes())
        self.assertEqual([len(s['targets']) for s in target_doc['sources']], [9, 9])
        for name, pin in result['products'].items():
            self.assertEqual((out / name).stat().st_size, pin['bytes'])
            self.assertEqual(m.file_sha(out / name), pin['sha256'])
        commands = [call.args[0] for call in called.call_args_list]
        self.assertEqual(commands[0], [str(self.binary), '-version'])
        self.assertTrue(all(c[0] == str(self.binary) for c in commands))
        self.assertTrue(all('-vf' not in c and 'ffmpeg' not in c for c in commands))
        self.assertEqual(commands[2], [str(self.binary), '-v', 'warning', '-select_streams', 'v:0',
                                     '-show_frames', '-show_streams', '-show_format', '-of', 'json', self.items[0]['path']])

    def test_wrong_hash_and_size_preserve_refusal_before_probe(self):
        for field, value in [('sha256', '0' * 64), ('bytes', 999)]:
            bad = dict(self.items[0]); bad[field] = value
            (receipt, selection), called = self.probe(field, bad)
            self.assertEqual(called.call_count, 0)
            self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
            self.assertIn('before', receipt['source_identity']); self.assertIn('after', receipt['source_identity'])
            self.assertTrue((self.case / field / 'receipt.json').is_file())

    def test_probe_diagnostics_no_allowlist(self):
        inventory, container = documents()
        for i, raw in enumerate((b'warning\n', b'\n', b' ', b'\xff')):
            (receipt, selection), called = self.probe(str(i), effects=[response(container, raw)])
            self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
            self.assertEqual(called.call_count, 1)
            self.assertEqual((self.case / str(i) / 'container.stderr').read_bytes(), raw)

    def test_frames_diagnostics_refused_separately(self):
        inventory, container = documents()
        (receipt, selection), _ = self.probe(effects=[response(container), response(inventory, b'unknown\n')])
        self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
        self.assertFalse((self.case / 'probe/targets.json').exists())

    def test_nonzero_and_launch_failure_persist_status(self):
        for i, failure in enumerate((response(None, b'failed\n', 7), OSError('synthetic launch refusal'))):
            (receipt, selection), _ = self.probe(str(i), effects=[failure])
            self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
            status = json.loads((self.case / str(i) / 'container.status.json').read_bytes())
            self.assertEqual(status['returncode'], 7 if i == 0 else None)
            self.assertEqual(bool(status['launch_error']), i == 1)

    def test_malformed_inventory_retains_raw_probe_files(self):
        inventory, container = documents()
        for i, raw in enumerate((b'not JSON', b'{"streams":[],"frames":[]}')):
            fake = SimpleNamespace(returncode=0, stdout=raw, stderr=b'')
            (receipt, selection), _ = self.probe(str(i), effects=[response(container), fake])
            self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
            self.assertEqual((self.case / str(i) / 'frames.stdout').read_bytes(), raw)

    def test_source_mutation_refuses_target_manifest(self):
        inventory, container = documents(); replies = iter([response(container), response(inventory)])
        def changed(*args, **kwargs):
            Path(self.items[0]['path']).write_bytes(b'SYNTHETIC MUTATED SOURCE\n')
            return next(replies)
        (receipt, selection), _ = self.probe(effects=changed)
        self.assertEqual(receipt['status'], 'refused'); self.assertIsNone(selection)
        self.assertNotEqual(receipt['source_identity']['before'], receipt['source_identity']['after'])
        self.assertFalse((self.case / 'probe/targets.json').exists())

    def test_source_mutation_after_its_probe_still_refuses_stage_manifest(self):
        inventory, container = documents(); replies = iter([
            SimpleNamespace(returncode=0, stdout=b'ffprobe version 7.1.1 synthetic\n', stderr=b''),
            response(container), response(inventory), response(container), response(inventory)])
        count = 0
        def changed(*args, **kwargs):
            nonlocal count
            count += 1
            if count == 5: Path(self.items[0]['path']).write_bytes(b'SYNTHETIC MUTATION AFTER FIRST CLIP\n')
            return next(replies)
        result, _ = self.prepare(effects=changed)
        self.assertEqual(result['status'], 'refused')
        self.assertFalse((self.case / 'run/sampling-manifest.json').exists())

    def test_existing_outputs_never_overwritten(self):
        for name in ('probe', 'run'):
            dest = self.case / name; dest.mkdir(); (dest / 'sentinel').write_text('preserve\n')
        with self.assertRaises(FileExistsError): self.probe()
        with self.assertRaises(FileExistsError): self.prepare()
        for name in ('probe', 'run'):
            self.assertEqual([p.name for p in (self.case / name).iterdir()], ['sentinel'])

    def test_declaration_and_helper_pins_refused_with_receipt(self):
        for name, kwargs in [('manifest', {'manifest_digest': '0' * 64}), ('protocol', {'plan_digest': '0' * 64})]:
            result, called = self.prepare(out=name, **kwargs)
            self.assertEqual(result['status'], 'refused'); called.assert_not_called()
            self.assertTrue((self.case / name / 'preparation-receipt.json').exists())
        with patch.object(m, 'HELPER_SHA256', '0' * 64): result, called = self.prepare(out='helper')
        self.assertEqual(result['status'], 'refused'); called.assert_not_called()

    def test_version_refusal_and_one_bad_clip_do_not_issue_stage_manifest(self):
        result, _ = self.prepare(out='version', effects=[SimpleNamespace(returncode=0, stdout=b'ffprobe version 8.0 ', stderr=b'')])
        self.assertEqual(result['status'], 'refused')
        inventory, container = documents()
        effects = [SimpleNamespace(returncode=0, stdout=b'ffprobe version 7.1.1 synthetic\n', stderr=b''),
                   response(container), response(inventory), response(container, b'warning\n')]
        result, _ = self.prepare(out='partial', effects=effects)
        self.assertEqual(result['status'], 'refused'); self.assertEqual(len(result['sources']), 2)
        self.assertTrue((self.case / 'partial/clip-1/targets.json').exists())
        self.assertFalse((self.case / 'partial/sampling-manifest.json').exists())

    def test_declaration_changed_during_probe_is_refused(self):
        inventory, container = documents(); replies = iter([
            SimpleNamespace(returncode=0, stdout=b'ffprobe version 7.1.1 synthetic\n', stderr=b''),
            response(container), response(inventory), response(container), response(inventory)])
        def changed(*args, **kwargs):
            self.plan.write_text('Synthetic changed declaration.\n')
            return next(replies)
        result, _ = self.prepare(effects=changed)
        self.assertEqual(result['status'], 'refused'); self.assertFalse(result['pins_unchanged'])
        self.assertFalse((self.case / 'run/sampling-manifest.json').exists())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); ARTIFACTS = m.sampler.absolute(str(args.out)); ARTIFACTS.mkdir()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    m.sampler.save(ARTIFACTS / 'test-results.json',
                   {'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
                    'successful': result.wasSuccessful(), 'synthetic_only': True,
                    'adapter_sha256': m.file_sha(Path(m.__file__)), 'tests_sha256': m.file_sha(Path(__file__)),
                    'helper_sha256': m.file_sha(m.HELPER), 'scientific_or_human_acceptance': False})
    sys.exit(0 if result.wasSuccessful() else 1)
