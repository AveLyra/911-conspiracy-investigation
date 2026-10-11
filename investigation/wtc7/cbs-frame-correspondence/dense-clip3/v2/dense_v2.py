"""Identity/control configuration only; all dense numerical/join bodies reused.

The original module remains on disk unchanged. Its in-memory __file__ identifies
this wrapper, DENSE selects only v2 products, s selects sample_v2, and gate plus
method_pins explicitly include both wrapper and inherited source/test identities.
"""
from pathlib import Path
import platform

import sample_v2

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
DENSE_PARENT_SHA = '20a1015ace2b373255cd32dc7e7371fbd378c725c69050d3330ad5518a2dd24d'
SAMPLER_TEST_SHA = 'cd997911f50d89d57c65906a1ac4eef3cda09ac4667a1f07307f9945068fcc43'
DENSE_TEST_SHA = 'cb0e48f43e9632339f14f5ba37d6b74c78c07f6ec6508a9cec6246e38a717961'
PILOT_TEST_SHA = 'cffa4d160de892439ef9e1e02ec0994d536812ae46ed6826111b7afad86522ab'
GUARD_SHA = '0f20129bd7102935347315599e0e2a30264f5075f1569353339eac439422dbe0'
GUARD_TEST_SHA = 'd6b24cf12ad0da7fcbc47785c6f428d91f040dc72ff22557a12787c303e45ee4'
api = sample_v2.importlib.util.module_from_spec(
    sample_v2.importlib.util.spec_from_file_location('configured_dense_v2', BASE/'dense_clip3.py'))
if sample_v2.hashlib.sha256((BASE/'dense_clip3.py').read_bytes()).hexdigest() != DENSE_PARENT_SHA:
    raise ValueError('dense parent pin mismatch')
api.__spec__.loader.exec_module(api)
p = api.p
api.DENSE = HERE
api.s = sample_v2.api
api.SAMPLER_SHA = p.sha(HERE/'sample_v2.py')
api.__file__ = str(Path(__file__).resolve())
original_method_pins = api.method_pins


def dependencies():
    fixed = {BASE/'dense_clip3.py': DENSE_PARENT_SHA, BASE/'test_dense_clip3.py': DENSE_TEST_SHA,
        sample_v2.PARENT: sample_v2.PARENT_SHA, sample_v2.PARENT.with_name('test_sample_sequence.py'): SAMPLER_TEST_SHA,
        BASE/'pilot.py': api.PILOT_SHA, BASE/'test_pilot.py': PILOT_TEST_SHA,
        p.CORE_PATH: p.CORE_SHA, HERE.parent/'guard.py': GUARD_SHA, HERE.parent/'test_guard.py': GUARD_TEST_SHA,
        BASE/'PROTOCOL.md': api.PROTOCOL_SHA, BASE/'regions.json': api.REGIONS_SHA}
    fixed.update({HERE/name: p.sha(HERE/name) for name in ('sample_v2.py', 'dense_v2.py', 'test_v2.py', 'run.py')})
    return {str(path.resolve()): digest for path, digest in fixed.items()}


def method_pins(plan_sha, manifest_sha):
    result = original_method_pins(plan_sha, manifest_sha)
    result['parent_dense_tests_sha256'] = result['tests_sha256']
    result.update(tests_sha256=p.sha(HERE/'test_v2.py'), parent_dense_sha256=DENSE_PARENT_SHA,
        sampler_parent_sha256=sample_v2.PARENT_SHA, dependencies=dependencies())
    return result


def gate(controls, pilot_controls, pins):
    p.gate_controls(pilot_controls, pins)
    current = dependencies()
    for path, digest in current.items(): p.pin(Path(path), digest, pins)
    api.snapshot(controls, pins)
    result = p.load(controls)
    p.require(result['status'] == 'passed' and result['failures'] == [] and result['errors'] == [] and
        result['skipped'] == [] and result['dependencies'] == current and
        result['code_sha256'] == p.sha(__file__) and result['tests_sha256'] == p.sha(HERE/'test_v2.py') and
        result['python'] == platform.python_version() and result['numpy'] == p.np.__version__ and
        result['pillow'] == p.Image.__version__, 'version-2 controls failed or stale')
    p.require({k: v['tests_run'] for k, v in result['groups'].items()} ==
        {'sampler': 14, 'dense': 22, 'pilot': 25, 'version': 9} and
        all(v['status'] == 'passed' for v in result['groups'].values()), 'version-2 control populations')
    # New guard controls are root-run, not silently inherited from the refused lane.
    guard_record = HERE/'guard-controls01/summary.json'
    api.snapshot(guard_record, pins)
    guard = p.load(guard_record)
    p.require(guard == dict(tests_run=16, failures=0, errors=0, passed=True,
        code_sha256=GUARD_SHA, tests_sha256=GUARD_TEST_SHA), 'fresh supervisor controls failed or stale')


api.method_pins = method_pins
api.gate = gate


if __name__ == '__main__':
    raise SystemExit(api.main())
