"""Exact synthetic coordinate/clock sensitivity, never a historical fit."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(value, label):
    if not value:
        raise ValueError(label)


def identity(path):
    with path.open('rb') as stream:
        return {'bytes': path.stat().st_size,
                'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def quantity(value):
    return {'exact': str(value), 'decimal': float(value)}


def image_derivatives(v, a, f1, f2, s1, s2):
    require(s1 > 0, 'monotonic clock required')
    require(f1 != 0, 'locally invertible image coordinate required')
    speed = f1*v/s1
    curvature = (f2*v*v+f1*a)/(s1*s1)-f1*v*s2/(s1*s1*s1)
    recovered = s1*s1*curvature/f1-f2*s1*s1*speed*speed/(f1*f1*f1)+s2*speed/f1
    return speed, curvature, recovered


def controls():
    checks = []
    require(image_derivatives(Q(3),Q(4),Q(2),Q(0),Q(5),Q(0)) ==
            (Q(6,5), Q(8,25), Q(4)), 'affine dimensional example')
    checks.append('known affine scale and clock result')
    # u=z/(1+z), z=t^2/2 at t=1: u_s=4/9, u_ss=-4/27.
    require(image_derivatives(Q(1),Q(1),Q(4,9),Q(-16,27),Q(1),Q(0)) ==
            (Q(4,9), Q(-4,27), Q(1)), 'projective curvature sign example')
    checks.append('positive true acceleration with negative image curvature')
    # s=t+t^2/2, z=t^2/2 at t=1; dz/ds=1/2, d2z/ds2=1/8.
    require(image_derivatives(Q(1),Q(1),Q(1),Q(0),Q(2),Q(1)) ==
            (Q(1,2), Q(1,8), Q(1)), 'nonlinear clock example')
    checks.append('known nonlinear clock curvature and recovery')
    for bad in ((Q(0),Q(1)), (Q(1),Q(0)), (Q(1),Q(-1))):
        try:
            image_derivatives(Q(1),Q(1),bad[0],Q(0),bad[1],Q(0))
        except ValueError:
            checks.append('degenerate coordinate or nonincreasing clock rejected')
        else:
            raise AssertionError('invalid transformation accepted')
    return checks


def calculate(data):
    a, alpha, t = (Q(data[name]) for name in
                  ('acceleration_m_per_s2','pixels_per_metre','evaluation_physical_seconds'))
    require(a>0 and alpha>0 and t>0, 'positive synthetic trajectory constants')
    z, v = a*t*t/2, a*t
    affine = []
    for k in map(Q, data['clock_stretch_factors']):
        for length_factor in map(Q, data['assumed_metres_per_pixel_factors']):
            speed, curvature, recovered = image_derivatives(v,a,alpha,Q(0),k,Q(0))
            inferred = length_factor*curvature/alpha  # analyst assumes k_hat=1
            require(recovered==a and inferred/a==length_factor/(k*k), 'affine recovery and sensitivity')
            affine.append({'clock_s_per_physical_s':quantity(k),
                'assumed_metres_per_pixel_factor':quantity(length_factor),
                'image_speed_px_per_recorded_s':quantity(speed),
                'image_curvature_px_per_recorded_s2':quantity(curvature),
                'naive_acceleration_m_per_s2':quantity(inferred),
                'naive_over_true':quantity(inferred/a),
                'recovered_acceleration_m_per_s2':quantity(recovered)})
    projective = []
    for q in map(Q, data['projective_depth_fractions_q']):
        c = q/z
        require(1+q>0, 'projective pole excluded throughout selected trajectory')
        f1, f2 = alpha/(1+q)**2, -2*alpha*c/(1+q)**3
        speed, curvature, recovered = image_derivatives(v,a,f1,f2,Q(1),Q(0))
        expected_ratio = (1-3*q)/(1+q)**3
        require(recovered==a and curvature/(alpha*a)==expected_ratio, 'projective exact ratio/recovery')
        projective.append({'q_c_times_z':quantity(q),'c_per_metre':quantity(c),
            'image_position_px':quantity(alpha*z/(1+q)),
            'image_speed_px_per_s':quantity(speed),
            'image_curvature_px_per_s2':quantity(curvature),
            'naive_baseline_scale_acceleration_m_per_s2':quantity(curvature/alpha),
            'naive_over_true':quantity(expected_ratio),
            'recovered_acceleration_m_per_s2':quantity(recovered)})
    nonlinear = []
    for eta in map(Q, data['nonlinear_clock_eta']):
        # s=t+eta*t^2. Parameters eta carry inverse seconds; t in [0,1].
        require(t==1 and min(Q(1),1+2*eta*t)>0, 'monotonic nonlinear clock over full interval')
        s1, s2 = 1+2*eta*t, 2*eta
        speed, curvature, recovered = image_derivatives(v,a,alpha,Q(0),s1,s2)
        require(recovered==a and curvature/(alpha*a)==1/s1**3, 'nonlinear-clock exact example')
        nonlinear.append({'eta_per_s':quantity(eta), 'recorded_time_s':quantity(t+eta*t*t),
            'clock_first_derivative':quantity(s1),'clock_second_derivative_per_s':quantity(s2),
            'image_speed_px_per_recorded_s':quantity(speed),
            'image_curvature_px_per_recorded_s2':quantity(curvature),
            'naive_over_true':quantity(curvature/(alpha*a)),
            'recovered_acceleration_m_per_s2':quantity(recovered)})
    offsets = [{'offset_s':quantity(offset),'recorded_time_s':quantity(t+offset),
                'image_curvature_px_per_recorded_s2':quantity(alpha*a)}
               for offset in map(Q,data['time_offsets_seconds'])]
    target = Q(data['circular_example_target_acceleration'])
    circular = []
    for actual in map(Q,data['circular_example_true_accelerations']):
        measured_curvature = alpha*actual
        assigned_alpha = measured_curvature/target
        confirmed = measured_curvature/assigned_alpha
        require(confirmed==target and actual!=target, 'wrong gravity calibration still confirms itself')
        circular.append({'true_acceleration_m_per_s2':quantity(actual),
            'image_curvature_px_per_s2':quantity(measured_curvature),
            'pixels_per_metre_chosen_from_target':quantity(assigned_alpha),
            'tautological_returned_acceleration_m_per_s2':quantity(confirmed)})
    require(tuple(map(len,(affine,projective,nonlinear,offsets,circular)))==(15,5,2,2,2),'fixed example counts')
    return {'scope':data['scope'],'physical_time_s':quantity(t),
            'synthetic_position_m':quantity(z),'synthetic_velocity_m_per_s':quantity(v),
            'affine':affine,'projective':projective,'nonlinear_clock':nonlinear,
            'time_offsets':offsets,'circular_calibration':circular}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    require(out.parent==HERE,'output confined to metric-audit unit')
    out.mkdir(exist_ok=False)
    sources = [Path(__file__).resolve(),HERE/'PROTOCOL.md',HERE/'inputs.json',Path(sys.executable)]
    pins = {str(p):identity(p) for p in sources}
    def save(name, value):
        with (out/name).open('x') as stream:
            stream.write(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')
    try:
        for p in sources[:-1]:
            (out/p.name).write_bytes(p.read_bytes())
        save('initial.json',{'pins':pins,'python':sys.version})
        checked = controls()
        data = json.loads((HERE/'inputs.json').read_text())
        result = calculate(data)
        save('result.json',result)
        save('controls.json',{'passed':len(checked),'checks':checked})
        require(all(identity(Path(p))==v for p,v in pins.items()),'procedure or inputs changed')
        save('receipt.json',{'status':'complete','pins':pins,
                            'products':{p.name:identity(p) for p in sorted(out.iterdir())}})
        print(json.dumps({'status':'complete','controls':len(checked),'examples':26}))
    except Exception as error:
        save('failure.json',{'type':type(error).__name__,'message':str(error)})
        raise


if __name__=='__main__':
    main()
