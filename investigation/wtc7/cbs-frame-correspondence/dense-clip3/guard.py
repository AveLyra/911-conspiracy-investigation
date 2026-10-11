"""Small external supervisor; preserves child products, never certifies their science."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

MIB = 1024**2
LANE = Path(__file__).resolve().parent


def size(path):
    if not path.exists():
        return 0
    paths = [path] if path.is_file() else path.rglob('*')
    total = 0
    for p in paths:
        if p.is_symlink():
            raise ValueError('symbolic link in output tree')
        if p.is_file():
            total += p.stat().st_size
    return total


def save(path, data):
    with path.open('x') as handle:
        json.dump(data, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write('\n')


def limits(elapsed, job_bytes, lane_bytes, free_bytes, seconds, job_cap, reserve):
    if elapsed >= seconds:
        return 'elapsed threshold reached'
    if job_bytes >= job_cap-reserve:
        return 'job byte reserve reached'
    if lane_bytes >= 1536*MIB-32*MIB:
        return 'lane byte reserve reached'
    if free_bytes < 4096*MIB:
        return 'free-space floor breached'
    return None


def stop_group(proc):
    """The child leads a new session. Kill descendants even if its leader exits."""
    deadline = time.monotonic()+1
    # Retry only the same owned group inside the existing grace. An observed
    # permission error is not assumed to establish its cause or absence.
    while True:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            break
        except ProcessLookupError:
            proc.wait(timeout=2)
            return
        except PermissionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(.01)
    while time.monotonic() < deadline:
        proc.poll()  # Reap an exited leader before testing the remaining group.
        try:
            os.killpg(proc.pid, 0)
        except ProcessLookupError:
            break
        except PermissionError:
            # Do not equate a failed existence check with successful cleanup.
            time.sleep(.01)
            continue
        time.sleep(.01)
    proc.poll()
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait(timeout=2)


def group_exists(pid):
    try:
        os.killpg(pid, 0)
        return True
    except ProcessLookupError:
        return False


def supervise(argv, target, records, lane, seconds, job_cap, reserve,
              interval=.1, free=lambda p: shutil.disk_usage(p).free):
    if target.exists() or records.exists():
        raise FileExistsError('create-only output already exists')
    if not argv or seconds <= 0 or interval <= 0 or reserve >= job_cap:
        raise ValueError('invalid supervisor request')
    before = dict(lane_bytes=size(lane), free_bytes=free(lane))
    refusal = limits(0, 0, before['lane_bytes'], before['free_bytes'], seconds, job_cap, reserve)
    records.mkdir()
    start = time.monotonic()
    receipt = dict(argv=argv, target=str(target), requested_seconds=seconds,
        job_cap_bytes=job_cap, job_reserve_bytes=reserve, lane_cap_bytes=1536*MIB,
        lane_reserve_bytes=32*MIB, free_floor_bytes=4096*MIB, poll_seconds=interval,
        termination_grace_seconds=1, before=before, status='started',
        supervisor_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scientific_acceptance=False)
    save(records/'start.json', receipt)
    proc = None
    def interrupted(_signum, _frame):
        raise InterruptedError('supervisor received SIGTERM')
    previous_term = signal.signal(signal.SIGTERM, interrupted)
    try:
        if refusal:
            raise ValueError(refusal)
        with (records/'stdout').open('xb') as stdout, (records/'stderr').open('xb') as stderr:
            proc = subprocess.Popen(argv, stdout=stdout, stderr=stderr, start_new_session=True)
            receipt['child_pid'] = proc.pid
            while True:
                code = proc.poll()
                refusal = limits(time.monotonic()-start, size(target), size(lane), free(lane),
                                 seconds, job_cap, reserve)
                if refusal:
                    raise ValueError(refusal)
                if code is not None:
                    receipt['returncode'] = code
                    if code != 0:
                        raise ValueError('child returned nonzero')
                    if group_exists(proc.pid):
                        raise ValueError('leader exited with live descendants')
                    if not target.is_dir():
                        raise ValueError('child did not create declared output')
                    break
                time.sleep(interval)
        receipt['status'] = 'completed'
    except BaseException as exc:
        if proc is not None:
            try:
                stop_group(proc)
            except Exception as shutdown:
                receipt['shutdown_error'] = type(shutdown).__name__+': '+str(shutdown)
            receipt['returncode'] = proc.returncode
        receipt.update(status='failed', reason=type(exc).__name__+': '+str(exc))
    finally:
        signal.signal(signal.SIGTERM, previous_term)
    receipt['elapsed_seconds'] = time.monotonic()-start
    for name, check in [('job_bytes', lambda: size(target)),
                        ('lane_bytes_before_receipt', lambda: size(lane)),
                        ('free_bytes_after', lambda: free(lane))]:
        try:
            receipt[name] = check()
        except Exception as exc:
            receipt[name] = None
            receipt.setdefault('snapshot_errors', {})[name] = type(exc).__name__+': '+str(exc)
            receipt['status'] = 'failed'
    save(records/'receipt.json', receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job', required=True)
    parser.add_argument('--aggregate', action='store_true')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    permitted = ['extract01', 'extract02'] + [f'score-{r}-{i:02d}' for r in 'ab' for i in range(1, 4)]
    if args.aggregate:
        permitted = ['aggregate-a', 'aggregate-b']
    if args.job not in permitted:
        raise ValueError('undeclared job')
    argv = args.command[1:] if args.command[:1] == ['--'] else args.command
    result = supervise(argv, LANE/args.job, LANE/('guard-'+args.job), LANE,
        60 if args.aggregate else 240, (16 if args.aggregate else 256)*MIB,
        (1 if args.aggregate else 32)*MIB)
    print(json.dumps({k: result.get(k) for k in ('status', 'returncode', 'elapsed_seconds', 'job_bytes', 'reason')}))
    return 0 if result['status'] == 'completed' else 1


if __name__ == '__main__':
    sys.exit(main())
