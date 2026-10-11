"""Declared version-2 jobs through the unchanged, parent-lane resource guard."""
import argparse
from pathlib import Path
import sys

import dense_v2 as v

HERE = Path(__file__).resolve().parent
LANE = HERE.parent
p = v.p
guard = v.api.import_pinned('v2_parent_guard', LANE/'guard.py', v.GUARD_SHA)


def job_spec(job, controls, pilot_controls, plan_sha, manifest_sha):
    common = ['--controls', str(controls), '--pilot-controls', str(pilot_controls),
              '--plan-sha256', plan_sha, '--manifest-sha256', manifest_sha]
    if job in ('extract01', 'extract02'):
        argv = [sys.executable, '-B', str(HERE/'sample_v2.py'), '--manifest', str(HERE/'manifest.json'),
                '--manifest-sha256', manifest_sha, '--plan', str(HERE/'PLAN.md'), '--plan-sha256', plan_sha,
                '--out', str(HERE/job)]
    elif job in [f'score-{r}-{i:02d}' for r in 'ab' for i in range(1, 4)]:
        _, repeat, chunk = job.split('-')
        argv = [sys.executable, '-B', str(HERE/'dense_v2.py'), 'score', '--repeat', repeat,
                '--chunk', str(int(chunk)), *common]
    elif job == 'aggregate-a':
        argv = [sys.executable, '-B', str(HERE/'dense_v2.py'), 'aggregate', '--repeat', 'a', *common]
    else:
        raise ValueError('undeclared version-2 job')
    aggregate = job == 'aggregate-a'
    return dict(argv=argv, target=HERE/job, records=HERE/('guard-'+job), lane=LANE,
                seconds=60 if aggregate else 240, job_cap=(16 if aggregate else 256)*guard.MIB,
                reserve=(1 if aggregate else 32)*guard.MIB)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job', required=True)
    parser.add_argument('--controls', type=Path, required=True)
    parser.add_argument('--pilot-controls', type=Path, required=True)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    for digest in (args.plan_sha256, args.manifest_sha256): v.api.s.digest_string(digest)
    job = job_spec(args.job, args.controls.resolve(), args.pilot_controls.resolve(), args.plan_sha256, args.manifest_sha256)
    pins = {}
    v.gate(args.controls, args.pilot_controls, pins)
    p.pin(HERE/'PLAN.md', args.plan_sha256, pins)
    p.pin(HERE/'manifest.json', args.manifest_sha256, pins)
    # Same fixed complete source manifest as the original reviewed dense plan.
    p.require(args.manifest_sha256 == 'fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b',
              'version-2 manifest differs from declared source population')
    result = guard.supervise(**job)
    changed = [path for path, digest in pins.items() if not Path(path).is_file() or p.sha(path) != digest]
    end = dict(before_pins=pins, changed_dependencies=changed, status='passed' if not changed else 'failed',
               runner_sha256=p.sha(__file__), supervisor_sha256=v.GUARD_SHA,
               supervisor_status=result['status'], parent_lane=str(LANE), scientific_acceptance=False)
    guard.save(job['records']/'wrapper-end-checks.json', end)
    print(p.json_bytes(dict(supervisor_status=result['status'], end_checks=end['status'])).decode(), end='')
    return 0 if result['status'] == 'completed' and not changed else 1


if __name__ == '__main__':
    raise SystemExit(main())
