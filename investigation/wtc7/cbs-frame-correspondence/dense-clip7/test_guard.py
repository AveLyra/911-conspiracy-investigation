"""Inherited supervisor controls bound to the new module, plus Clip 7 policy tests.

The combined runner supplies OUT and preserves synthetic products and logs.
No historical source is decoded, scored, or viewed by these controls.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
PARENT_TESTS = HERE.parent/'dense-clip3/test_guard.py'
PARENT_TESTS_SHA256 = 'd6b24cf12ad0da7fcbc47785c6f428d91f040dc72ff22557a12787c303e45ee4'
OUT = None


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = load('clip7_guard_under_test', HERE/'guard.py')
if hashlib.sha256(PARENT_TESTS.read_bytes()).hexdigest() != PARENT_TESTS_SHA256:
    raise ValueError('parent guard controls pin mismatch')
# The inherited methods resolve their module-global `guard` to this derivative,
# never the old module. Restore the import slot after loading the test source.
previous_guard = sys.modules.get('guard')
sys.modules['guard'] = guard
try:
    parent_tests = load('clip7_inherited_guard_controls', PARENT_TESTS)
finally:
    if previous_guard is None:
        del sys.modules['guard']
    else:
        sys.modules['guard'] = previous_guard


class Controls(parent_tests.Controls):
    def unit(self):
        lane = OUT/self._testMethodName
        lane.mkdir()
        return lane


class GuardClip7Controls(unittest.TestCase):
    policy = dict(lane_cap=3584*guard.MIB, lane_reserve=128*guard.MIB,
                  free_floor=4096*guard.MIB)

    def unit(self):
        lane = OUT/self._testMethodName
        lane.mkdir()
        return lane

    def supervise(self, lane, **overrides):
        args = dict(seconds=3, job_cap=256*guard.MIB, reserve=32*guard.MIB,
                    interval=.01, free=lambda _: 8192*guard.MIB, **self.policy)
        args.update(overrides)
        code = 'import pathlib,sys; pathlib.Path(sys.argv[1]).mkdir(); print("synthetic")'
        return guard.supervise([sys.executable, '-B', '-c', code, str(lane/'product')],
                               lane/'product', lane/'records', lane, **args)

    def test_inherited_controls_use_new_module(self):
        self.assertIs(parent_tests.guard, guard)
        self.assertEqual(Path(parent_tests.guard.__file__).resolve(), HERE/'guard.py')
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(Controls).countTestCases(), 16)

    def test_clip7_exact_boundaries_all_jobs(self):
        m = guard.MIB
        for cap, reserve in [(1280, 64), (256, 32), (64, 2)]:
            with self.subTest(cap=cap):
                self.assertIsNone(guard.limits(239, (cap-reserve)*m-1, 3456*m-1,
                                              4096*m, 240, cap*m, reserve*m, **self.policy))
                self.assertEqual(guard.limits(0, (cap-reserve)*m, 0, 8192*m,
                    240, cap*m, reserve*m, **self.policy), 'job byte reserve reached')
                self.assertEqual(guard.limits(0, 0, 3456*m, 8192*m,
                    240, cap*m, reserve*m, **self.policy), 'lane byte reserve reached')
                self.assertEqual(guard.limits(240, 0, 0, 8192*m,
                    240, cap*m, reserve*m, **self.policy), 'elapsed threshold reached')
                self.assertEqual(guard.limits(0, 0, 0, 4096*m-1,
                    240, cap*m, reserve*m, **self.policy), 'free-space floor breached')

    def test_clip7_receipt_policy_and_parent_pin(self):
        lane = self.unit()
        result = self.supervise(lane)
        self.assertEqual(result['status'], 'completed')
        start = json.loads((lane/'records/start.json').read_text())
        saved = json.loads((lane/'records/receipt.json').read_text())
        self.assertEqual(saved, result)
        for receipt in [start, saved]:
            for field, expected in self.policy.items():
                self.assertEqual(receipt[field+'_bytes'], expected)
            self.assertEqual(receipt['supervisor_sha256'], hashlib.sha256((HERE/'guard.py').read_bytes()).hexdigest())
            self.assertEqual(receipt['parent_supervisor_sha256'], guard.PARENT_SHA256)
            self.assertEqual(receipt['termination_grace_seconds'], 1)
            self.assertFalse(receipt['scientific_acceptance'])

    def test_default_receipt_preserved(self):
        lane = self.unit()
        code = 'import pathlib,sys; pathlib.Path(sys.argv[1]).mkdir()'
        result = guard.supervise([sys.executable, '-B', '-c', code, str(lane/'product')],
            lane/'product', lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB,
            .01, lambda _: 8192*guard.MIB)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual([result[k] for k in ['lane_cap_bytes', 'lane_reserve_bytes', 'free_floor_bytes']],
                         [1536*guard.MIB, 32*guard.MIB, 4096*guard.MIB])

    def test_clip7_lane_prevents_launch(self):
        lane = self.unit()
        with patch.object(guard, 'size', return_value=3456*guard.MIB), patch.object(guard.subprocess, 'Popen') as spawn:
            result = self.supervise(lane)
        spawn.assert_not_called()
        self.assertIn('lane byte reserve', result['reason'])
        self.assertNotIn('child_pid', result)

    def test_clip7_lane_monitor(self):
        lane = self.unit(); calls = []
        def synthetic_size(path):
            if path == lane:
                calls.append(1)
                return 0 if len(calls) == 1 else 3456*guard.MIB
            return 0
        with patch.object(guard, 'size', side_effect=synthetic_size):
            result = self.supervise(lane)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('lane byte reserve', result['reason'])
        self.assertIn('child_pid', result)
        self.assertIsNotNone(result['returncode'])

    def test_configured_free_floor_boundaries(self):
        m = guard.MIB
        policy = dict(self.policy, free_floor=6000*m)
        self.assertIsNone(guard.limits(0, 0, 0, 6000*m, 240, 256*m, 32*m, **policy))
        self.assertEqual(guard.limits(0, 0, 0, 6000*m-1, 240, 256*m, 32*m, **policy),
                         'free-space floor breached')

    def test_configured_free_floor_prevents_launch(self):
        lane = self.unit()
        with patch.object(guard.subprocess, 'Popen') as spawn:
            result = self.supervise(lane, free_floor=9000*guard.MIB)
        spawn.assert_not_called()
        self.assertIn('free-space floor', result['reason'])
        self.assertEqual(result['free_floor_bytes'], 9000*guard.MIB)

    def test_configured_free_floor_monitor(self):
        lane = self.unit(); calls = []
        def free(_):
            calls.append(1)
            return (8192 if len(calls) == 1 else 6000)*guard.MIB
        result = self.supervise(lane, free=free, free_floor=7000*guard.MIB)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('free-space floor', result['reason'])
        self.assertIn('child_pid', result)

    def test_invalid_limits_refused(self):
        defaults = dict(elapsed=0, job_bytes=0, lane_bytes=0, free_bytes=8192*guard.MIB,
                        seconds=240, job_cap=256*guard.MIB, reserve=32*guard.MIB, **self.policy)
        cases = [dict(seconds=x) for x in [0, -1, float('nan'), float('inf'), True, '240']]
        cases += [dict(**{field: value}) for field in ['job_cap', 'reserve', 'lane_cap', 'lane_reserve', 'free_floor']
                  for value in [-1, float('nan'), float('inf'), True, 1.5, '32']]
        cases += [dict(job_cap=0), dict(reserve=256*guard.MIB), dict(lane_cap=0), dict(lane_reserve=3584*guard.MIB)]
        for change in cases:
            with self.subTest(change=change), self.assertRaises(ValueError):
                guard.limits(**dict(defaults, **change))

    def test_invalid_supervise_refuses_before_writes(self):
        lane = self.unit()
        cases = [dict(lane_cap=0), dict(lane_reserve=-1), dict(free_floor=float('nan')),
                 dict(lane_reserve=3584*guard.MIB), dict(reserve=-1), dict(seconds=float('inf')),
                 dict(interval=0), dict(interval=float('nan')), dict(interval=float('inf'))]
        for change in cases:
            with self.subTest(change=change), patch.object(guard.subprocess, 'Popen') as spawn:
                with self.assertRaises(ValueError):
                    self.supervise(lane, **change)
                spawn.assert_not_called()
                self.assertFalse((lane/'records').exists())
                self.assertFalse((lane/'product').exists())

    def test_parent_pin_mismatch_refuses_before_writes(self):
        lane = self.unit()
        with patch.object(guard, 'PARENT_SHA256', '0'*64), patch.object(guard.subprocess, 'Popen') as spawn:
            with self.assertRaisesRegex(ValueError, 'parent pin mismatch'):
                self.supervise(lane)
        spawn.assert_not_called()
        self.assertFalse((lane/'records').exists())

    def test_new_policy_parameters_keyword_only(self):
        with self.assertRaises(TypeError):
            guard.limits(0, 0, 0, 8192*guard.MIB, 240, 256*guard.MIB, 32*guard.MIB, 3584*guard.MIB)
