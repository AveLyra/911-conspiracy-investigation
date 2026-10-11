"""Synthetic dense-lane controls; no historical media, subprocess or scoring."""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import os
import platform
import shutil
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

import numpy as np
from PIL import Image

import dense_clip3 as d

p, s = d.p, d.s


def write(path, value):
    path.write_bytes(p.json_bytes(value))


def synthetic_log(source, directory):
    lines = [f"[info] Input #0, avi, from '{source['path']}':",
        '[info]   Stream #0:0: Video: dvvideo (dvsd / 0x64737664), yuv411p, 720x480 [SAR 8:9 DAR 4:3], 28771 kb/s, 29.97 fps, 29.97 tbr, 29.97 tbn',
        '[info]   Stream #0:1: Audio: pcm_s16le ([1][0][0][0] / 0x0001), 48000 Hz, 2 channels, s16, 1536 kb/s',
        '[info] Stream mapping:', '[info]   Stream #0:0 -> #0:0 (dvvideo (native) -> png (native))',
        '[Parsed_showinfo_1 @ 0x1] [info] config in time_base: 333673/10000000, frame_rate: 10000000/333673',
        '[Parsed_showinfo_1 @ 0x1] [info] config out time_base: 0/0, frame_rate: 0/0',
        f"[info] Output #0, image2, to '{directory/'native/frame-%06d.png'}':",
        '[info]   Stream #0:0: Video: png, rgb24(pc, gbr/unknown/unknown, bottom coded first (swapped)), 720x480 [SAR 8:9 DAR 4:3], q=2-31, 200 kb/s, 29.97 fps, 29.97 tbn']
    for index in range(189):
        lines += [f'[Parsed_showinfo_1 @ 0x1] [info] n: {index} pts: {index} pts_time:{float(index*Fraction(p.TIME_BASE)):.6f} duration: 1 duration_time:0.033367 fmt:yuv411p cl:topleft sar:8/9 s:720x480 i:B iskey:1 type:I checksum:00000000 plane_checksum:[00000000] mean:[0] stdev:[0.0]',
            '[Parsed_showinfo_1 @ 0x1] [info] color_range:unknown color_space:unknown color_primaries:unknown color_trc:unknown']
    lines += ['[out#0/image2 @ 0x1] [info] video:1KiB audio:0KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown',
              '[info] frame= 189 fps=0.0 q=-0.0 Lsize=N/A time=00:00:06.30 bitrate=N/A speed=1x']
    return ('\n'.join(lines)+'\n').encode()


def fixture(root):
    source_path = root/'synthetic.avi'
    source_path.write_bytes(b'synthetic placeholder, not an AVI')
    source = dict(id='vince-clip3', path=str(source_path), bytes=source_path.stat().st_size,
                  sha256=p.sha(source_path), count=189, indices=list(range(189)))
    manifest = dict(schema=s.SCHEMA, sources=[source])
    write(root/'manifest.json', manifest)
    (root/'PLAN.md').write_text('Synthetic fixture only.\n')
    manifest_sha, plan_sha = p.sha(root/'manifest.json'), p.sha(root/'PLAN.md')
    pins = dict(code_sha256=d.SAMPLER_SHA, parent_code_sha256=s.PARENT_SHA256,
        manifest_sha256=manifest_sha, plan_sha256=plan_sha, python=sys.version, pillow=Image.__version__)
    image = Image.new('RGB', (720, 480), (17, 39, 91)); image.save(root/'synthetic.png')
    png_sha, rgb_sha = p.sha(root/'synthetic.png'), hashlib.sha256(image.tobytes()).hexdigest()
    rows = [dict(source_index=i, pts=i, time_base=p.TIME_BASE, pts_seconds_exact=str(i*Fraction(p.TIME_BASE)),
        file=f'native/frame-{i+1:06d}.png', width=720, height=480, sample_aspect_ratio='8:9',
        interlaced_frame=1, top_field_first=0, png_sha256=png_sha, rgb_sha256=rgb_sha) for i in range(189)]
    probe = dict(streams=[dict(codec_type='video', codec_name='dvvideo', time_base=p.TIME_BASE,
        width=720, height=480, sample_aspect_ratio='8:9', pix_fmt='yuv411p')],
        frames=[dict(pts=i, width=720, height=480, sample_aspect_ratio='8:9', pix_fmt='yuv411p',
                     interlaced_frame=1, top_field_first=0) for i in range(189)])
    for repeat in (1, 2):
        run = root/f'extract{repeat:02d}'; directory = run/'vince-clip3'
        (directory/'native').mkdir(parents=True)
        for row in rows: os.link(root/'synthetic.png', directory/row['file'])
        write(run/'manifest.input.json', manifest)
        shutil.copyfile(root/'PLAN.md', run/'plan.input')
        write(run/'run-receipt.json', dict(schema=s.SCHEMA, status='descriptive_candidates_only', reasons=[],
            sources=[dict(id='vince-clip3', admission=d.ADMISSION)], pins=pins))
        for tool, binary in (('ffmpeg', s.FFMPEG), ('ffprobe', s.FFPROBE)):
            write(run/f'{tool}-version.command.json', [binary, '-version'])
            write(run/f'{tool}-version.status.json', dict(returncode=0, launch_error=None))
            (run/f'{tool}-version.stdout').write_bytes(f'{tool} version 7.1.1 synthetic\n'.encode())
            (run/f'{tool}-version.stderr').write_bytes(b'')
        for kind, argv in d.expected_commands(source, directory).items():
            write(directory/f'{kind}.command.json', argv)
            write(directory/f'{kind}.status.json', dict(returncode=0, launch_error=None))
        write(directory/'probe.stdout', probe)
        (directory/'probe.stderr').write_bytes(b'')
        (directory/'decode.stdout').write_bytes(b'')
        raw = synthetic_log(source, directory); (directory/'decode.stderr').write_bytes(raw)
        diagnostic = s.decode_diagnostics(raw, source_path, directory/'native/frame-%06d.png')
        identity = dict(bytes=source['bytes'], sha256=source['sha256'])
        receipt = dict(schema=s.SCHEMA, source=source, pins=pins, reasons=[],
            structure='inventory_and_products_checked', admission=d.ADMISSION, scientific_or_human_acceptance=False,
            source_identity=dict(before=identity, after=identity, status='matched_before_and_after'),
            probe_diagnostics=s.probe_diagnostics(b''), decode_diagnostics=diagnostic)
        write(directory/'receipt.json', receipt); write(directory/'frames.json', rows)
    return source, manifest_sha, plan_sha, rows


class DenseControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source, self.manifest, self.plan, self.rows = fixture(self.root)
        self.directory = self.root/'extract01/vince-clip3'

    def tearDown(self):
        self.temp.cleanup()

    def verify(self, repeat=1):
        return d.verify_extraction(self.root/f'extract{repeat:02d}', self.source, self.manifest, self.plan, {})

    def mutate_rows(self, mutation):
        rows = p.load(self.directory/'frames.json'); mutation(rows); write(self.directory/'frames.json', rows)

    def pilot_rows(self):
        return [dict(self.rows[i], file=f'native/frame-{ordinal:06d}.png') for ordinal, i in
                enumerate((0, 24, 47, 71, 94, 118, 141, 165, 188), 1)]

    def test_complete_native_receipts_repeat_and_pilot_joins(self):
        a, b = self.verify(), self.verify(2)
        d.check_repeat_and_pilot(a, b, self.pilot_rows())
        self.assertEqual(len(a), 189)

    def test_missing_index(self):
        self.mutate_rows(lambda rows: rows.pop())
        with self.assertRaisesRegex(ValueError, 'missing/duplicate'): self.verify()

    def test_duplicate_index(self):
        self.mutate_rows(lambda rows: rows.__setitem__(1, rows[0]))
        with self.assertRaisesRegex(ValueError, 'missing/duplicate'): self.verify()

    def test_wrong_out_of_range_index(self):
        self.mutate_rows(lambda rows: rows[1].update(source_index=189))
        with self.assertRaisesRegex(ValueError, 'missing/duplicate'): self.verify()

    def test_false_pts(self):
        self.mutate_rows(lambda rows: rows[1].update(pts=2))
        with self.assertRaisesRegex(ValueError, 'PTS/metadata'): self.verify()

    def test_probe_pts(self):
        path = self.directory/'probe.stdout'; value = p.load(path); value['frames'][1]['pts'] = 0; write(path, value)
        with self.assertRaisesRegex(ValueError, 'non-increasing PTS'): self.verify()

    def test_false_source_hash(self):
        Path(self.source['path']).write_bytes(b'altered synthetic bytes')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.verify()

    def test_false_manifest(self):
        path = self.root/'extract01/manifest.input.json'
        value = p.load(path); value['sources'][0]['count'] = 190; write(path, value)
        with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.verify()

    def test_false_png_hash(self):
        self.mutate_rows(lambda rows: rows[0].update(png_sha256='0'*64))
        with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.verify()

    def test_false_rgb_hash(self):
        self.mutate_rows(lambda rows: rows[0].update(rgb_sha256='0'*64))
        with self.assertRaisesRegex(ValueError, 'PNG/RGB'): self.verify()

    def test_mismatching_repeat_products(self):
        other = copy.deepcopy(self.rows); other[100]['rgb_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'repeat mismatch'):
            d.check_repeat_and_pilot(self.rows, other, self.pilot_rows())

    def test_pilot_hash_disagreement(self):
        pilot = self.pilot_rows(); pilot[1]['png_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'pilot/dense frame join'):
            d.check_repeat_and_pilot(self.rows, self.rows, pilot)

    def test_undeclared_diagnostic_rejected(self):
        with (self.directory/'decode.stderr').open('ab') as stream: stream.write(b'[warning] injected\n')
        with self.assertRaisesRegex(ValueError, 'diagnostics reparse'): self.verify()

    def test_nonzero_status(self):
        write(self.directory/'decode.status.json', dict(returncode=7, launch_error=None))
        with self.assertRaisesRegex(ValueError, 'command/status'): self.verify()

    def test_stale_code_plan_pins(self):
        path = self.root/'extract01/run-receipt.json'; value = p.load(path)
        value['pins']['plan_sha256'] = '0'*64; write(path, value)
        with self.assertRaisesRegex(ValueError, 'run receipt'): self.verify()

    def test_wrong_command(self):
        path = self.directory/'decode.command.json'; argv = p.load(path); argv[1] = '-invalid'; write(path, argv)
        with self.assertRaisesRegex(ValueError, 'command/status'): self.verify()

    def test_cross_chunk_ties_and_all_null_dynamic_groups(self):
        rows = [dict(target='143', clip=3, paired=True, source_index=i, arm=arm,
            best=[dict(static_score=.9 if i in (0, 63, 126) else .5, dynamic_score=None)])
            for i in range(189) for arm in p.ARMS]
        summary = p.summarize(rows)
        self.assertEqual(summary['shortlist'], [dict(clip=3, source_index=0), dict(clip=3, source_index=63)])
        dynamic = [g for g in summary['groups'] if g['metric'] == 'dynamic_score']
        self.assertEqual(len(dynamic), 3)
        self.assertTrue(all(g['reason'] and g['best_score'] is None and
                            all(v == [] for v in g['epsilon_sets'].values()) for g in dynamic))
        self.assertEqual(summary, p.summarize(list(reversed(rows))))

    def test_incomplete_duplicate_aggregate_rejected(self):
        rows = [dict(source_index=i, arm=arm) for i in range(189) for arm in p.ARMS]
        with self.assertRaisesRegex(ValueError, 'incomplete/duplicate'):
            d.validate_result_population(rows[:-1], range(189), self.rows)
        rows[1] = rows[0]
        with self.assertRaisesRegex(ValueError, 'incomplete/duplicate'):
            d.validate_result_population(rows, range(189), self.rows)
        with patch.object(d, 'DENSE', self.root), self.assertRaises(FileNotFoundError):
            d.collect_pass(p.Output(self.root/'incomplete'), 'a', self.rows, {}, {})

    def test_repeat_score_disagreement(self):
        rows = [dict(source_index=i, arm=arm, best=[]) for i in range(189) for arm in p.ARMS]
        other = copy.deepcopy(rows); other[200]['best'] = [dict(static_score=.1)]
        with self.assertRaisesRegex(ValueError, 'repeat score records'):
            d.reconcile(rows, other, [], p.Output(self.root/'repeat'), {}, dense=self.root, pilot_dir=self.root/'pilot')

    def test_array_repeat_disagreement(self):
        output = p.Output(self.root/'arrays')
        output.npz('a.npz', scores=np.array([1., np.nan])); output.npz('b.npz', scores=np.array([2., np.nan]))
        with self.assertRaisesRegex(ValueError, 'array values disagree'):
            d.equal_arrays(output.path/'a.npz', output.path/'b.npz')

    def test_finite_caps_and_create_only(self):
        output = p.Output(self.root/'cap', seconds=60, byte_cap=16*1024**2)
        with self.assertRaisesRegex(ValueError, 'byte cap'):
            output.write('oversized', b'x'*(15*1024**2+1))
        with patch.object(p.time, 'monotonic', return_value=output.started+61):
            with self.assertRaisesRegex(ValueError, 'time cap'): output.check()
        output.json('failure.json', dict(status='failed'), terminal=True)
        with self.assertRaises(FileExistsError): p.Output(output.path)

    def test_567_per_pass_mocked_wiring_complete_reconciliation(self):
        # All correlation calls are mocked. This checks orchestration, not numerical or historical validity.
        scores, coverage = np.full((13, 51, 51), np.nan), np.zeros((13, 51, 51))
        methods = dict(synthetic=True)
        with patch.object(p, 'register', return_value=([], scores, coverage)) as register:
            for repeat in ('a', 'b'):
                for chunk, indices in enumerate(d.CHUNKS, 1):
                    output = p.Output(self.root/f'score-{repeat}-{chunk:02d}')
                    frames = [dict(row, clip=3, path=str(self.root/'synthetic.png')) for row in self.rows
                              if row['source_index'] in indices]
                    results = p.comparisons(frames, {'143': dict(paired_clip=3, arrays=(None, None, None))}, output)
                    output.json('results.json', results)
                    output.json('verified-inputs.json', dict(pins={}, repeat_equal_frames=189, pilot_equal_frames=9))
                    output.npz('masks.npz', working_valid=p.working_validity())
                    output.json('receipt.json', dict(status='completed', mode='score', repeat=repeat,
                        chunk=chunk, method_pins=methods, result=dict(indices=list(indices), comparisons=189,
                            results_sha256=p.sha(output.path/'results.json'))))
        self.assertEqual(register.call_count, 1134)
        aggregate = p.Output(self.root/'aggregate', seconds=60, byte_cap=16*1024**2)
        with patch.object(d, 'DENSE', self.root):
            a = d.collect_pass(aggregate, 'a', self.rows, {}, methods)
            b = d.collect_pass(aggregate, 'b', self.rows, {}, methods)
        self.assertEqual(len(a), 567); self.assertEqual(len(b), 567)
        pilot_dir = self.root/'pilot'; pilot_dir.mkdir()
        selected = {r['source_index'] for r in self.pilot_rows()}
        pilot = []
        for row in a:
            if row['source_index'] in selected:
                name = Path(row['surfaces']).name
                os.link(self.root/row['surfaces'], pilot_dir/name)
                pilot.append(dict(row, surfaces=name))
        os.link(self.root/'score-a-01/masks.npz', pilot_dir/'masks.npz')
        d.reconcile(a, b, pilot, aggregate, {}, dense=self.root, pilot_dir=pilot_dir)
        self.assertEqual(len(pilot), 27)
        self.assertEqual(p.summarize(a)['shortlist'], [])
        self.assertEqual(len(p.summarize(a)['groups']), 6)
        bad = copy.deepcopy(pilot); bad[0]['best'] = [dict(static_score=.1)]
        with self.assertRaisesRegex(ValueError, 'pilot/dense score records'):
            d.reconcile(a, b, bad, aggregate, {}, dense=self.root, pilot_dir=pilot_dir)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # No supervisor substitute: this is a pre-write check for the small control logs.
    lane_size = sum(path.stat().st_size for path in d.DENSE.rglob('*') if path.is_file())
    p.require(lane_size < (1536-32)*1024**2 and shutil.disk_usage(d.DENSE).free >= 4096*1024**2,
              'lane capacity/free-space gate before controls')
    args.output.mkdir(exist_ok=False)
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DenseControls))
    with (args.output/'tests.log').open('x') as stream: stream.write(log.getvalue())
    summary = dict(scope='Synthetic dense orchestration and saved-log controls only; all 1134 wiring scores mocked',
        argv=sys.argv, code_sha256=p.sha(d.__file__), tests_sha256=p.sha(__file__), pilot_sha256=d.PILOT_SHA,
        sampler_sha256=d.SAMPLER_SHA, python=platform.python_version(), numpy=np.__version__, pillow=Image.__version__,
        tests_run=result.testsRun, failures=[str(t) for t, _ in result.failures], errors=[str(t) for t, _ in result.errors],
        skipped=[str(t) for t, _ in result.skipped], status='passed' if result.wasSuccessful() and not result.skipped else 'failed',
        log_sha256=p.sha(args.output/'tests.log'))
    with (args.output/'summary.json').open('xb') as stream: stream.write(p.json_bytes(summary))
    print(log.getvalue(), end=''); print(p.json_bytes(summary).decode(), end='')
    return 0 if summary['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
