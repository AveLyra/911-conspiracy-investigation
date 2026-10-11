"""Fresh inherited and version-specific controls; never runs historical jobs.

All inherited test bodies remain on disk unchanged. Module aliases select the
configured adapters. The original sampler's optimized child imports its original
module; this is disclosed and supplemented with an optimized v2 child below.
"""
import argparse
import copy
import io
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import dense as d
import test_dense as dense_tests
import test_guard as guard_tests
import run as runner
sample_v2 = d.sample_v2

p, s = d.p, sample_v2.api
OUT = None


def inherited(name, path, digest, aliases):
    with patch.dict(sys.modules, aliases):
        return d.import_pinned(name, path, digest)


sampler_tests = inherited('v2_sampler_tests', sample_v2.PARENT.with_name('test_sample_sequence.py'),
                          d.SAMPLER_TEST_SHA, {'sample_sequence': s})
pilot_tests = inherited('v2_pilot_tests', d.BASE/'test_pilot.py', d.PILOT_TEST_SHA, {'pilot': p})


def log_fixture(fps='0.0'):
    source = dict(path='/synthetic/nonhistorical.avi')
    dest = Path('/synthetic/output')
    raw = dense_tests.synthetic_log(source, dest).replace(b'fps=0.0', ('fps='+fps).encode())
    return raw, Path(source['path']), dest/'native/frame-%06d.png'


class VersionControls(unittest.TestCase):
    def test_only_final_fps_fragment_changes(self):
        original = d.import_pinned('v2_original_sampler_check', sample_v2.PARENT, sample_v2.PARENT_SHA)
        self.assertEqual(s.BARE_INFO[:-1], original.BARE_INFO[:-1])
        self.assertEqual(s.BARE_INFO[-1], original.BARE_INFO[-1].replace('fps='+s.NUMBER, 'fps= ?'+s.NUMBER))
        self.assertEqual(s.NUMBER, original.NUMBER)
        for name in ('decode_diagnostics', 'probe_diagnostics', 'check_showinfo', 'inventory', 'execute'):
            self.assertEqual(getattr(s, name).__code__.co_code, getattr(original, name).__code__.co_code)
        for name in ('SHOW_FRAME', 'SHOW_CONFIG', 'SHOW_COLOR', 'OUT_INFO'):
            self.assertEqual(getattr(s, name).pattern, getattr(original, name).pattern)

    def test_positive_fps_forms(self):
        for fps in ('0.0', '9.9', ' 10', ' 83', ' 99', '100', '12.345', '1e+2'):
            with self.subTest(fps=fps):
                raw, source, destination = log_fixture(fps)
                before = bytes(raw)
                self.assertEqual(s.decode_diagnostics(raw, source, destination)['status'], 'clean')
                self.assertEqual(raw, before)

    def test_negative_fps_forms(self):
        for fps in ('  10', '\t10', '\n10', '\u00a010', '', 'nan', 'inf', '1e+', '1.2.3', '--1'):
            with self.subTest(fps=repr(fps)):
                raw, source, destination = log_fixture(fps)
                self.assertEqual(s.decode_diagnostics(raw, source, destination)['status'], 'refused')

    def test_other_diagnostics_and_summary_cardinality_unchanged(self):
        raw, source, destination = log_fixture(' 83')
        final = next(line for line in raw.splitlines(keepends=True) if line.startswith(b'[info] frame='))
        for bad in (raw+b'[warning] injected\n', raw+b'unknown line\n', raw+final, raw.replace(final, b''),
                    raw.replace(b'q=-0.0', b'q= -0.0')):
            with self.subTest(bad=bad[-120:]):
                self.assertEqual(s.decode_diagnostics(bad, source, destination)['status'], 'refused')

    def test_receipt_wrapper_and_parent_identity(self):
        receipt = p.load(OUT.parent/'sampler-controls/test_manifest_plan_pin_and_run_output/run/run-receipt.json')
        self.assertEqual(receipt['status'], 'descriptive_candidates_only')
        self.assertEqual(receipt['pins']['code_sha256'], p.sha(sample_v2.__file__))
        self.assertEqual(receipt['pins']['parent_code_sha256'], sample_v2.PARENT_SHA)
        self.assertEqual(Path(s.__file__), Path(sample_v2.__file__))

    def test_optimized_v2_negative(self):
        destination = OUT/'optimized-v2'; destination.mkdir()
        program = ('import sys; sys.path.insert(0, '+repr(str(Path(sample_v2.__file__).parent))+'); import sample_v2; '+
                   'm=sample_v2.api; m.validate_source({"id":"x","path":"/tmp/x",'+
                   '"sha256":"0"*64,"bytes":1,"count":2,"indices":[0,0]})')
        _, stderr, status = s.run_command([sys.executable, '-O', '-B', '-c', program], destination, 'negative')
        self.assertNotEqual(status['returncode'], 0)
        self.assertIn(b'Refusal', stderr)
        self.assertNotIn(b'ModuleNotFoundError', stderr)

    def test_dense_configuration_and_numerical_reuse(self):
        self.assertEqual(d.COUNT,1128); self.assertEqual(d.CLIP,7); self.assertEqual(d.TARGET,'142')
        self.assertIs(d.s, s)
        self.assertEqual(d.SAMPLER_SHA, p.sha(sample_v2.__file__))
        for name in ('comparisons','summarize','register','representations','guarded_canvas'):
            self.assertEqual(Path(getattr(p,name).__code__.co_filename), d.BASE/'pilot.py')
        methods = d.method_pins(d.PLAN_SHA,d.MANIFEST_SHA)
        self.assertEqual(methods['code_sha256'],p.sha(d.__file__))
        self.assertEqual(methods['tests_sha256'],p.sha(d.DENSE/'test_dense.py'))
        self.assertEqual(methods['parent_dense_sha256'],d.DENSE_PARENT_SHA)
        self.assertEqual(methods['parent_dense_tests_sha256'],d.DENSE_TEST_SHA)

    def test_stale_control_identity_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'stale.json'
            path.write_bytes(p.json_bytes(dict(status='passed', failures=[], errors=[], skipped=[],
                dependencies=d.dependencies(), changed_dependencies=[], code_sha256='0'*64, tests_sha256=p.sha(__file__),
                python=platform.python_version(), numpy=p.np.__version__, pillow=p.Image.__version__)))
            with patch.object(p, 'gate_controls'), self.assertRaisesRegex(ValueError, 'failed or stale'):
                d.gate(path, path, {})

    def test_exact_job_names_paths_and_parent_budget(self):
        names = ['extract01','extract02']+[f'score-{r}-{i:02d}' for r in 'ab' for i in range(1,19)]+['aggregate-a']
        self.assertEqual(runner.JOBS,names); self.assertEqual(len(names),39)
        for name in names:
            job=runner.job_spec(name,Path('/synthetic/controls'),Path('/synthetic/pilot'),'1'*64,'2'*64)
            self.assertEqual(job['target'],d.DENSE/name)
            self.assertEqual(job['records'],d.DENSE/('guard-'+name))
            self.assertEqual(job['lane'],d.DENSE); self.assertEqual(job['seconds'],240)
            cap,reserve=(1280,64) if name.startswith('extract') else (64,2) if name=='aggregate-a' else (256,32)
            self.assertEqual(job['job_cap'],cap*runner.guard.MIB)
            self.assertEqual(job['reserve'],reserve*runner.guard.MIB)
            self.assertEqual({k:job[k] for k in runner.POLICY},runner.POLICY)
            if name.startswith('extract'): self.assertIn(str(sample_v2.__file__),job['argv'])
        for name in ('../extract01','extract03','score-c-01','score-a-19','aggregate-b','score-a-1'):
            with self.assertRaises(ValueError): runner.job_spec(name,Path('/x'),Path('/y'),'1'*64,'2'*64)

    def test_serial_predecessor_and_existing_attempt_refusal(self):
        with tempfile.TemporaryDirectory() as temporary:
            lane=Path(temporary)
            with patch.object(runner,'HERE',lane),patch.object(runner,'LANE',lane):
                args=(Path('/controls'),Path('/pilot'),'1'*64,'2'*64,{})
                self.assertEqual(runner.check_serial_order('extract01',*args),{})
                with self.assertRaises(ValueError): runner.check_serial_order('../extract01',*args)
                with self.assertRaises(FileNotFoundError): runner.check_serial_order('extract02',*args)
                (lane/'guard-extract01').mkdir()
                with self.assertRaisesRegex(ValueError,'already attempted'):
                    runner.check_serial_order('extract01',*args)
                spec=runner.job_spec('extract01',*args[:-1])
                runner.guard.save(spec['records']/'receipt.json',dict(status='failed'))
                runner.guard.save(spec['records']/'wrapper-end-checks.json',dict(status='passed'))
                with self.assertRaisesRegex(ValueError,'prior job'):
                    runner.check_serial_order('extract02',*args)


def run_group(name, suite, directory, cwd=None):
    before = resource_check()
    directory.mkdir()
    log = io.StringIO(); prior = Path.cwd()
    try:
        if cwd is not None: os.chdir(cwd)
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    finally:
        os.chdir(prior)
    after = resource_check()
    with (directory/'tests.log').open('x') as stream: stream.write(log.getvalue())
    summary = dict(tests_run=result.testsRun, failures=[str(t) for t, _ in result.failures],
        errors=[str(t) for t, _ in result.errors], skipped=[str(t) for t, _ in result.skipped],
        status='passed' if result.wasSuccessful() and not result.skipped else 'failed',
        log_sha256=p.sha(directory/'tests.log'), resource_before=before, resource_after=after)
    if name == 'pilot':
        summary.update(pilot_sha256=d.PILOT_SHA, tests_sha256=d.PILOT_TEST_SHA, core_sha256=p.CORE_SHA)
    with (directory/'summary.json').open('xb') as stream: stream.write(p.json_bytes(summary))
    print(name+': '+summary['status']+' ('+str(result.testsRun)+' tests)', flush=True)
    if summary['status'] != 'passed': print(log.getvalue(), end='', flush=True)
    resource_check()
    return summary


def resource_check():
    sample = dict(lane_bytes=runner.guard.size(d.DENSE),free_bytes=shutil.disk_usage(d.DENSE).free)
    refusal = runner.guard.limits(0,0,sample['lane_bytes'],sample['free_bytes'],
        240,256*runner.guard.MIB,32*runner.guard.MIB,**runner.POLICY)
    p.require(refusal is None, 'Clip7 synthetic resource gate: '+str(refusal))
    return sample


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); output = args.output.resolve()
    p.require(output.parent == d.DENSE and output.name.startswith('controls'), 'controls output must be new Clip7 controls directory')
    resource_check()
    dependencies = d.dependencies()
    for path, digest in dependencies.items(): p.require(p.sha(path) == digest, 'control dependency pin mismatch')
    output.mkdir(exist_ok=False)
    loader = unittest.defaultTestLoader
    sampler_tests.ARTIFACTS = output/'sampler-controls'
    groups = {'sampler': run_group('sampler', loader.loadTestsFromTestCase(sampler_tests.Controls),
        sampler_tests.ARTIFACTS, cwd=sample_v2.PARENT.parent)}
    temporary = output/'temporary'; temporary.mkdir()
    old_temp = tempfile.tempdir
    tempfile.tempdir = str(temporary)
    groups['pilot'] = run_group('pilot',loader.loadTestsFromModule(pilot_tests),output/'pilot-controls')
    guard_tests.OUT = output/'guard-controls'
    groups['guard'] = run_group('guard',loader.loadTestsFromTestCase(guard_tests.Controls),guard_tests.OUT)
    guard_tests.OUT = output/'guard_clip7-controls'
    groups['guard_clip7'] = run_group('guard_clip7',loader.loadTestsFromTestCase(guard_tests.GuardClip7Controls),guard_tests.OUT)
    try:
        tempfile.tempdir = str(temporary)
        dense_tests.SYNTHETIC_ROOT = temporary
        groups['dense'] = run_group('dense',loader.loadTestsFromTestCase(dense_tests.DenseControls),output/'dense-controls')
        OUT = output/'version-controls'
        groups['version'] = run_group('version',loader.loadTestsFromTestCase(VersionControls),OUT)
    finally:
        tempfile.tempdir = old_temp
    counts = {name:group['tests_run'] for name,group in groups.items()}
    population_error = counts != d.EXPECTED_GROUPS
    changed = [path for path, digest in dependencies.items() if p.sha(path) != digest]
    failures = [f'{name}: {item}' for name, group in groups.items() for item in group['failures']]
    errors = [f'{name}: {item}' for name, group in groups.items() for item in group['errors']]
    skipped = [f'{name}: {item}' for name, group in groups.items() for item in group['skipped']]
    summary = dict(argv=sys.argv, code_sha256=p.sha(d.__file__), tests_sha256=p.sha(__file__), dependencies=dependencies,
        python=platform.python_version(), numpy=p.np.__version__, pillow=p.Image.__version__, groups=groups,
        failures=failures, errors=errors, skipped=skipped, changed_dependencies=changed,
        status='passed' if not (failures or errors or skipped or changed or population_error) else 'failed',
        population_error=population_error, expected_counts=d.EXPECTED_GROUPS,
        scope='Synthetic execution and saved-log controls; no historical decoding/scoring or image viewing.',
        optimized_child_attribution='All 14 sampler test bodies use the configured module. The inherited optimized child imports the original sampler; version.test_optimized_v2_negative separately imports the configured wrapper.',
        temporary_fixture_cleanup='Dense/version TemporaryDirectory fixtures are cleaned within this lane; inherited pilot temporary fixtures are cleaned; logs, guard products and sampler synthetic products are retained.')
    with (output/'summary.json').open('xb') as stream: stream.write(p.json_bytes(summary))
    print(p.json_bytes(dict(status=summary['status'], counts={name: group['tests_run'] for name, group in groups.items()})).decode(), end='')
    return 0 if summary['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
