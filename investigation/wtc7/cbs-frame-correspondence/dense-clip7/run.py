"""The 39 declared serial Clip7 jobs; no automatic retries or partial ranking."""
import argparse
from pathlib import Path
import sys

import dense as d
import guard

HERE = LANE = Path(__file__).resolve().parent
p = d.p
JOBS = ['extract01', 'extract02'] + [f'score-{r}-{i:02d}' for r in 'ab' for i in range(1,19)] + ['aggregate-a']
POLICY = dict(lane_cap=3584*guard.MIB, lane_reserve=128*guard.MIB, free_floor=4096*guard.MIB)


def job_spec(job, controls, pilot_controls, plan_sha, manifest_sha):
    p.require(job in JOBS, 'undeclared Clip7 job')
    common = ['--controls', str(controls), '--pilot-controls', str(pilot_controls),
              '--plan-sha256', plan_sha, '--manifest-sha256', manifest_sha]
    if job.startswith('extract'):
        argv = [sys.executable, '-B', str(d.sample_v2.__file__), '--manifest', str(HERE/'manifest.json'),
                '--manifest-sha256', manifest_sha, '--plan', str(HERE/'PLAN.md'), '--plan-sha256', plan_sha,
                '--out', str(HERE/job)]
        cap, reserve = 1280, 64
    elif job.startswith('score'):
        _, repeat, chunk = job.split('-')
        argv = [sys.executable, '-B', str(HERE/'dense.py'), 'score', '--repeat', repeat,
                '--chunk', str(int(chunk)), *common]
        cap, reserve = 256, 32
    else:
        argv = [sys.executable, '-B', str(HERE/'dense.py'), 'aggregate', '--repeat', 'a', *common]
        cap, reserve = 64, 2
    return dict(argv=argv, target=HERE/job, records=HERE/('guard-'+job), lane=LANE,
                seconds=240, job_cap=cap*guard.MIB, reserve=reserve*guard.MIB, **POLICY)


def check_serial_order(job, controls, pilot_controls, plan_sha, manifest_sha, current_pins):
    """Receipt checks only; no partial result arrays, ranks or images are opened."""
    p.require(job in JOBS, 'undeclared Clip7 job')
    position = JOBS.index(job)
    pins = {}
    for future in JOBS[position:]:
        p.require(not (HERE/future).exists() and not (HERE/('guard-'+future)).exists(),
                  'current/future job already attempted; no retry or overlap')
    for prior in JOBS[:position]:
        spec = job_spec(prior, controls, pilot_controls, plan_sha, manifest_sha)
        receipt_path = spec['records']/'receipt.json'
        end_path = spec['records']/'wrapper-end-checks.json'
        for path in (receipt_path, end_path): d.snapshot(path, pins)
        receipt, end = p.load(receipt_path), p.load(end_path)
        p.require(receipt['status'] == 'completed' and receipt['returncode'] == 0 and
            receipt['argv'] == spec['argv'] and receipt['target'] == str(spec['target']) and
            receipt['supervisor_sha256'] == p.sha(guard.__file__) and
            end['status'] == 'passed' and end['changed_dependencies'] == [] and
            end['supervisor_status'] == 'completed' and end['runner_sha256'] == p.sha(__file__) and
            end['supervisor_sha256'] == p.sha(guard.__file__) and end['parent_lane'] == str(LANE) and
            end['before_pins'] == current_pins, 'prior job receipt/code/control mismatch')
        terminal = spec['target']/('run-receipt.json' if prior.startswith('extract') else 'receipt.json')
        d.snapshot(terminal, pins)
        result = p.load(terminal)
        p.require(result['status'] == ('descriptive_candidates_only' if prior.startswith('extract') else 'completed'),
                  'prior inner result did not complete')
    return pins


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job', required=True)
    parser.add_argument('--controls', type=Path, required=True)
    parser.add_argument('--pilot-controls', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    p.require(args.plan_sha256 == d.PLAN_SHA and args.manifest_sha256 == d.MANIFEST_SHA,
              'undeclared Clip7 plan/manifest')
    controls, pilot_controls = args.controls.resolve(), args.pilot_controls.resolve()
    job = job_spec(args.job, controls, pilot_controls, args.plan_sha256, args.manifest_sha256)
    pins = {}
    d.gate(controls, pilot_controls, pins)
    p.pin(HERE/'PLAN.md', args.plan_sha256, pins)
    p.pin(HERE/'manifest.json', args.manifest_sha256, pins)
    predecessors = check_serial_order(args.job, controls, pilot_controls,
                                      args.plan_sha256, args.manifest_sha256, pins)
    result = guard.supervise(**job)
    all_pins = dict(pins)
    d.merge_dependencies(all_pins, predecessors)
    changed = [path for path, digest in all_pins.items() if not Path(path).is_file() or p.sha(path) != digest]
    end = dict(before_pins=pins, predecessor_pins=predecessors, changed_dependencies=changed,
        status='passed' if not changed else 'failed', runner_sha256=p.sha(__file__),
        supervisor_sha256=p.sha(guard.__file__), supervisor_status=result['status'],
        parent_lane=str(LANE), scientific_acceptance=False)
    guard.save(job['records']/'wrapper-end-checks.json', end)
    print(p.json_bytes(dict(supervisor_status=result['status'], end_checks=end['status'])).decode(), end='')
    return 0 if result['status'] == 'completed' and not changed else 1


if __name__ == '__main__':
    raise SystemExit(main())
