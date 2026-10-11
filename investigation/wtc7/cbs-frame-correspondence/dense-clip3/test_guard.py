"""Finite supervisor controls, using synthetic children only."""
import argparse
import json
import os
import signal
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch
import guard

OUT = None


class Controls(unittest.TestCase):
    def unit(self):
        lane = OUT/self._testMethodName
        lane.mkdir()
        return lane

    def launch(self, code, seconds=3, free=8*1024**3):
        lane = self.unit()
        argv = [sys.executable, '-B', '-c', code, str(lane/'product')]
        return guard.supervise(argv, lane/'product', lane/'records', lane,
            seconds, 256*guard.MIB, 32*guard.MIB, .01, lambda _: free), lane

    def test_normal(self):
        result, lane = self.launch('import pathlib,sys; pathlib.Path(sys.argv[1]).mkdir(); print("synthetic")')
        self.assertEqual(result['status'], 'completed')
        self.assertEqual((lane/'records/stdout').read_text(), 'synthetic\n')

    def test_nonzero(self):
        result, lane = self.launch('import sys; print("kept"); sys.exit(7)')
        self.assertEqual(result['returncode'], 7)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual((lane/'records/stdout').read_text(), 'kept\n')

    def test_timeout_group(self):
        code = ('import os,pathlib,signal,subprocess,sys,time; '
                'pathlib.Path(sys.argv[1]).mkdir(); '
                'p=subprocess.Popen([sys.executable,"-c",'
                '"import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)"]); '
                'pathlib.Path(sys.argv[1],"child-pid").write_text(str(p.pid)); '
                'time.sleep(30)')
        result, lane = self.launch(code, seconds=.5)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('elapsed threshold', result['reason'])
        self.assertLess(result['elapsed_seconds'], 4)
        self.assert_dead(int((lane/'product/child-pid').read_text()))

    def assert_dead(self, pid):
        for _ in range(100):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(.01)
        self.fail('synthetic descendant still exists after shutdown')

    def test_successful_leader_with_live_descendant_refused(self):
        code = ('import pathlib,subprocess,sys; pathlib.Path(sys.argv[1]).mkdir(); '
                'p=subprocess.Popen([sys.executable,"-c","import time; time.sleep(30)"]); '
                'pathlib.Path(sys.argv[1],"child-pid").write_text(str(p.pid))')
        result, lane = self.launch(code)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('live descendants', result['reason'])
        self.assert_dead(int((lane/'product/child-pid').read_text()))

    def test_snapshot_error_retains_receipt(self):
        code = ('import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.mkdir(); '
                '(p/"synthetic-link").symlink_to(p/"nonexistent")')
        result, lane = self.launch(code)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('job_bytes', result['snapshot_errors'])
        self.assertEqual(json.loads((lane/'records/receipt.json').read_text()), result)
        (lane/'product/synthetic-link').unlink()  # Remove only this synthetic fixture link.

    def test_free_floor_prevents_launch(self):
        result, lane = self.launch('raise Exception("must not launch")', free=4096*guard.MIB-1)
        self.assertIn('free-space floor', result['reason'])
        self.assertNotIn('returncode', result)
        self.assertFalse((lane/'product').exists())

    def test_midrun_free_floor(self):
        lane = self.unit(); calls = []
        def free(_):
            calls.append(1)
            return (8192 if len(calls) == 1 else 4095)*guard.MIB
        result = guard.supervise([sys.executable, '-c', 'import time; time.sleep(30)'],
            lane/'product', lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB, .01, free)
        self.assertIn('free-space floor', result['reason'])
        self.assertEqual(result['status'], 'failed')
        self.assertIsNotNone(result['returncode'])

    def test_monitor_job_threshold(self):
        lane = self.unit()
        def synthetic_size(path):
            return 224*guard.MIB if path == lane/'product' else 0
        with patch.object(guard, 'size', side_effect=synthetic_size):
            result = guard.supervise([sys.executable, '-c', 'import time; time.sleep(30)'],
                lane/'product', lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB,
                .01, lambda _: 8192*guard.MIB)
        self.assertIn('job byte reserve', result['reason'])

    def test_monitor_lane_threshold(self):
        lane = self.unit(); calls = []
        def synthetic_size(path):
            if path == lane:
                calls.append(1)
                return 0 if len(calls) == 1 else 1504*guard.MIB
            return 0
        with patch.object(guard, 'size', side_effect=synthetic_size):
            result = guard.supervise([sys.executable, '-c', 'import time; time.sleep(30)'],
                lane/'product', lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB,
                .01, lambda _: 8192*guard.MIB)
        self.assertIn('lane byte reserve', result['reason'])

    def test_interrupt_cleanup(self):
        lane = self.unit(); calls = []
        def free(_):
            calls.append(1)
            if len(calls) == 2:
                raise KeyboardInterrupt('synthetic interruption')
            return 8192*guard.MIB
        result = guard.supervise([sys.executable, '-c', 'import time; time.sleep(30)'],
            lane/'product', lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB, .01, free)
        self.assertIn('KeyboardInterrupt', result['reason'])
        self.assertEqual(result['status'], 'failed')
        self.assertIsNotNone(result['returncode'])

    def test_sigterm_cleanup(self):
        lane = self.unit(); calls = []; previous = signal.getsignal(signal.SIGTERM)
        def free(_):
            calls.append(1)
            if len(calls) == 2:
                os.kill(os.getpid(), signal.SIGTERM)
            return 8192*guard.MIB
        result = guard.supervise([sys.executable, '-c', 'import time; time.sleep(30)'],
            lane/'product', lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB, .01, free)
        self.assertIn('SIGTERM', result['reason'])
        self.assertEqual(result['status'], 'failed')
        self.assertIsNotNone(result['returncode'])
        self.assertEqual(signal.getsignal(signal.SIGTERM), previous)

    def test_exact_boundaries(self):
        m = guard.MIB
        self.assertIsNone(guard.limits(239, 224*m-1, 1504*m-1, 4096*m, 240, 256*m, 32*m))
        self.assertEqual(guard.limits(240, 0, 0, 8192*m, 240, 256*m, 32*m), 'elapsed threshold reached')
        self.assertEqual(guard.limits(0, 224*m, 0, 8192*m, 240, 256*m, 32*m), 'job byte reserve reached')
        self.assertEqual(guard.limits(0, 0, 1504*m, 8192*m, 240, 256*m, 32*m), 'lane byte reserve reached')
        self.assertIsNone(guard.limits(59, 15*m-1, 0, 8192*m, 60, 16*m, m))
        self.assertEqual(guard.limits(60, 0, 0, 8192*m, 60, 16*m, m), 'elapsed threshold reached')
        self.assertEqual(guard.limits(0, 15*m, 0, 8192*m, 60, 16*m, m), 'job byte reserve reached')

    def test_existing_output_preserved(self):
        lane = self.unit(); target = lane/'product'; target.mkdir()
        with self.assertRaises(FileExistsError):
            guard.supervise(['false'], target, lane/'records', lane, 3, 256*guard.MIB, 32*guard.MIB)
        self.assertTrue(target.is_dir()); self.assertFalse((lane/'records').exists())

    def test_existing_records_preserved(self):
        lane = self.unit(); records = lane/'records'; records.mkdir()
        with self.assertRaises(FileExistsError):
            guard.supervise(['false'], lane/'product', records, lane, 3, 256*guard.MIB, 32*guard.MIB)
        self.assertEqual(list(records.iterdir()), [])

    def test_missing_output(self):
        result, _ = self.launch('print("no product")')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('did not create', result['reason'])

    def test_tree_size(self):
        lane = self.unit(); nested = lane/'nested'; nested.mkdir()
        (nested/'synthetic').write_bytes(b'abc')
        self.assertEqual(guard.size(lane), 3)
        with patch.object(Path, 'is_symlink', return_value=True), self.assertRaises(ValueError):
            guard.size(lane)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(); OUT = args.out; OUT.mkdir()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Controls))
    guard.save(OUT/'summary.json', dict(tests_run=result.testsRun, failures=len(result.failures),
        errors=len(result.errors), passed=result.wasSuccessful(),
        code_sha256=guard.hashlib.sha256(Path(guard.__file__).read_bytes()).hexdigest(),
        tests_sha256=guard.hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    sys.exit(0 if result.wasSuccessful() else 1)
