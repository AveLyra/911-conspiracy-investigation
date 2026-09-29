"""Independent exact Taylor-jet oracle for synthetic metric-motion examples.

No historical sources and no producer implementation are imported or read.
Jets store polynomial coefficients [value, first derivative, second/2].
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = '2ef59293a4e7994929964878ace70cef3569b4b689008e7ef85c66dc1e00e800'
CHARTER_SHA = '54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd'
PRODUCER_SHA = 'bc59b8a9e6510a0e8a493636dff96907a500c047536c235e7840fb72bb09e3d0'
INPUTS_SHA = '6885b06d38a6ed1b3b55d6188df49c1c91caaa3460fb08b80740ec76dc8fb8f1'


def require(value,label):
    if not value:
        raise AssertionError(label)


def fp(path):
    with path.open('rb') as stream:
        return {'bytes':path.stat().st_size,'sha256':hashlib.file_digest(stream,'sha256').hexdigest()}


def multiply(a,b):
    return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(3)]


def reciprocal(a):
    if a[0]==0:
        raise ValueError('zero local projective denominator')
    out=[1/a[0]]
    for i in range(1,3):
        out.append(-sum(a[j]*out[i-j] for j in range(1,i+1))/a[0])
    return out


def projective_jet(z,v,a,A=1,B=0,C=0,D=1):
    z,v,a,A,B,C,D=map(Q,(z,v,a,A,B,C,D))
    if A*D-B*C==0:
        raise ValueError('degenerate projective map cannot identify a coordinate')
    numerator=[A*z+B,A*v,A*a/2]
    denominator=[C*z+D,C*v,C*a/2]
    return multiply(numerator,reciprocal(denominator))


def recorded_jet(physical_jet,rate,rate_derivative=0):
    rate,rate_derivative=Q(rate),Q(rate_derivative)
    if rate<=0:
        raise ValueError('clock must be locally increasing')
    # Solve ds = rate*dt + rate_derivative*dt²/2, to second order.
    dt=[Q(0),1/rate,-rate_derivative/(2*rate**3)]
    square=multiply(dt,dt)
    return [physical_jet[0]+physical_jet[1]*dt[0]+physical_jet[2]*square[0]]+[
        physical_jet[1]*dt[i]+physical_jet[2]*square[i] for i in (1,2)]


def chain_formula(z,v,a,A=1,B=0,C=0,D=1,rate=1,rate_derivative=0):
    z,v,a,A,B,C,D,rate,rate_derivative=map(Q,(z,v,a,A,B,C,D,rate,rate_derivative))
    denominator=C*z+D
    derivative=(A*D-B*C)/denominator**2
    second=-2*C*(A*D-B*C)/denominator**3
    return (second*v*v+derivative*a)/rate**2-derivative*v*rate_derivative/rate**3


def value_record(value):
    value=Q(value)
    return {'exact':str(value),'decimal':float(value)}


def examples():
    checks=[]
    rate_rows=[]
    for rate in (Q(95,100),Q(99,100),Q(1),Q(101,100),Q(105,100)):
        image=recorded_jet(projective_jet(5,10,10,A=20),rate)
        curvature=2*image[2]
        require(curvature==Q(200)/rate**2,'affine clock exact quadratic rate effect')
        require(curvature*rate**2/20==10,'independent correct calibration recovers acceleration')
        rate_rows.append({'rate':value_record(rate),'image_curvature':value_record(curvature),
            'naive_acceleration_with_khat_1':value_record(curvature/20),
            'naive_over_true_ratio':value_record(1/rate**2)})
    checks.append('five affine clock rates; quadratic direction and inverse recovery')
    scale_rows=[]
    for factor in (Q(9,10),Q(1),Q(11,10)):
        reported_length_scale=Q(1,20)*factor
        inferred=reported_length_scale*200
        require(inferred==10*factor,'length-per-pixel error linear, not its reciprocal')
        scale_rows.append({'reported_metres_per_pixel_factor':value_record(factor),'inferred_acceleration':value_record(inferred)})
    checks.append('three length-per-pixel factors with distinct pixels-per-metre convention')
    require(recorded_jet(projective_jet(5,10,10,A=20,B=0),Q(11,10))[1:]==
        recorded_jet(projective_jet(5,10,10,A=20,B=1000),Q(11,10))[1:],'spatial offset derivatives invariant')
    # Expand u(s)=100*((s-offset)/rate)² about s0=rate*1+offset.
    # Offsets enter the global polynomial and cancel at the same physical t=1.
    offset_rows=[]
    for offset in (Q(-50),Q(0),Q(23,7)):
        rate=Q(11,10);s0=rate+offset
        physical_time_jet=[(s0-offset)/rate,1/rate,Q(0)]
        global_image_jet=[100*value for value in multiply(physical_time_jet,physical_time_jet)]
        require(global_image_jet==recorded_jet(projective_jet(5,10,10,A=20),rate),'constant clock offset derivative invariance at same physical event')
        offset_rows.append({'clock_offset':value_record(offset),'recorded_event_time':value_record(s0),
            'image_first_derivative':value_record(global_image_jet[1]),'image_second_derivative':value_record(2*global_image_jet[2])})
    checks.append('constant spatial/time offsets; same physical evaluation event')
    projective_rows=[]
    for q in (Q(-1,20),Q(-1,50),Q(0),Q(1,50),Q(1,20)):
        c=q/5
        image=recorded_jet(projective_jet(5,10,10,A=20,C=c),1)
        ratio=2*image[2]/200
        expected=(1-3*q)/(1+q)**3
        require(ratio==expected,'projective from-rest acceleration ratio')
        require(2*image[2]==chain_formula(5,10,10,A=20,C=c),'projective chain formula versus rational series')
        require(min(Q(1),1+q)>0,'entire t in [0,1] denominator positive for z=5t²')
        projective_rows.append({'q_cz_at_t1':value_record(q),'c_per_metre':value_record(c),
            'image_curvature':value_record(2*image[2]),'baseline_scale_naive_over_true_ratio':value_record(ratio),
            'denominator_range_t_0_to_1':[value_record(min(Q(1),1+q)),value_record(max(Q(1),1+q))]})
    checks.append('five exact nonlinear-projective from-rest examples; bounded positive denominator')
    witnesses=[]
    for c in (Q(-1,10),Q(1,10)):
        image=recorded_jet(projective_jet(1,1,0,A=2,C=c),1)
        curvature=2*image[2]
        require(curvature==-4*c/(1+c)**3 and curvature!=0,'constant physical velocity has projective image curvature')
        witnesses.append({'kind':'projective_constant_velocity','c':value_record(c),'physical_acceleration':value_record(0),
            'image_curvature_t1':value_record(curvature),'domain':'0<=t<=1, z=t metres; denominator stays between 0.9 and 1.1; illustrative only'})
    checks.append('two bounded projective constant-velocity witnesses of opposite apparent signs')
    for rate_derivative in (Q(-1,10),Q(1,10)):
        rate=1+rate_derivative
        image=recorded_jet(projective_jet(1,1,0,A=2),rate,rate_derivative)
        curvature=2*image[2]
        require(curvature==-2*rate_derivative/rate**3 and curvature!=0,'nonlinear clock yields image curvature at zero physical acceleration')
        require(curvature==chain_formula(1,1,0,A=2,rate=rate,rate_derivative=rate_derivative),'nonlinear clock chain versus local series inversion')
        recovered=rate**2*curvature/2+rate_derivative*image[1]/2
        require(recovered==0,'clock correction recovers known zero physical acceleration')
        witnesses.append({'kind':'nonlinear_clock_constant_velocity','clock':'s=t+epsilon*t²/2',
            'epsilon_per_second':value_record(rate_derivative),'clock_rate_t1':value_record(rate),
            'physical_acceleration':value_record(0),'image_curvature_t1':value_record(curvature),
            'domain':'0<=t<=1; clock rate stays between 0.9 and 1.1 and is strictly positive; illustrative only'})
    checks.append('two bounded monotone nonlinear-clock witnesses and inverse correction')
    complex_jet=recorded_jet(projective_jet(Q(3,2),-2,Q(7,3),A=-4,B=3,C=Q(1,5),D=2),Q(6,5),Q(-1,7))
    require(2*complex_jet[2]==chain_formula(Q(3,2),-2,Q(7,3),A=-4,B=3,C=Q(1,5),D=2,rate=Q(6,5),rate_derivative=Q(-1,7)),'combined nonlinear terms and coordinate orientation')
    checks.append('combined nonlinear projection/clock with negative orientation and velocity')
    g=Q(981,100)
    image_curvature=Q(20)
    assumed_pixels_per_metre=image_curvature/g
    reported=image_curvature/assumed_pixels_per_metre
    require(reported==g and reported!=5,'gravity calibration creates false confirmation in known nongravitational example')
    same_curve=[]
    for recorded_time in (Q(0),Q(1,2),Q(1),Q(2)):
        one=4*Q(5,2)*recorded_time**2
        two=4*Q(20,2)*(recorded_time/2)**2
        require(one==two==10*recorded_time**2,'same observed curve, different physical clock and acceleration')
        same_curve.append({'s':value_record(recorded_time),'u':value_record(one)})
    checks.append('gravity circular calibration and two distinct physical parameterizations of one image curve')
    rejected=[]
    invalid=[('zero_denominator',lambda:projective_jet(1,1,1,A=1,C=-1)),
        ('degenerate_map',lambda:projective_jet(1,1,1,A=2,B=2,C=1,D=1)),
        ('zero_clock_rate',lambda:recorded_jet([Q(1),Q(1),Q(1)],0)),
        ('negative_clock_rate',lambda:recorded_jet([Q(1),Q(1),Q(1)],-1))]
    for label,call in invalid:
        try:call()
        except ValueError:rejected.append(label)
        else:raise AssertionError('invalid domain admitted: '+label)
    checks.append('four explicit inverse-domain rejections')
    return {'passed':len(checks),'checks':checks,'clock_rate_examples':rate_rows,'scale_examples':scale_rows,'offset_examples':offset_rows,
        'projective_examples':projective_rows,'nonlinear_witnesses':witnesses,
        'circular_calibration':{'synthetic_true_acceleration':value_record(5),'image_curvature':value_record(image_curvature),
            'assumed_gravity':value_record(g),'gravity_derived_pixels_per_metre':value_record(assumed_pixels_per_metre),
            'tautologically_reported_acceleration':value_record(reported),'same_curve_alternative_accelerations':[5,20],
            'same_curve_samples':same_curve},'domain_rejections':rejected,
        'scope':'Exact synthetic mathematics only; no historical geometry/rate bounds, observation, fit or cause conclusion.'}


def inverse_physical_acceleration(image,rate,rate_derivative=0,A=1,B=0,C=0,D=1):
    # Invert F by swapping projective coefficients, then change from s to t.
    # This uses reciprocal Taylor algebra, not the producer's f1/f2 formula.
    z_recorded=projective_jet(image[0],image[1],2*image[2],A=D,B=-B,C=-C,D=A)
    return 2*z_recorded[2]*Q(rate)**2+z_recorded[1]*Q(rate_derivative)


def expected_producer_result(data):
    a,alpha,t=[Q(data[name]) for name in ('acceleration_m_per_s2','pixels_per_metre','evaluation_physical_seconds')]
    z,v=a*t*t/2,a*t
    affine=[]
    for rate in map(Q,data['clock_stretch_factors']):
        image=recorded_jet(projective_jet(z,v,a,A=alpha),rate)
        recovered=inverse_physical_acceleration(image,rate,A=alpha)
        require(recovered==a,'independent affine inverse series recovers acceleration')
        for scale_factor in map(Q,data['assumed_metres_per_pixel_factors']):
            inferred=2*image[2]*scale_factor/alpha
            affine.append({'clock_s_per_physical_s':value_record(rate),'assumed_metres_per_pixel_factor':value_record(scale_factor),
                'image_speed_px_per_recorded_s':value_record(image[1]),'image_curvature_px_per_recorded_s2':value_record(2*image[2]),
                'naive_acceleration_m_per_s2':value_record(inferred),'naive_over_true':value_record(inferred/a),
                'recovered_acceleration_m_per_s2':value_record(recovered)})
    projective=[]
    for q in map(Q,data['projective_depth_fractions_q']):
        c=q/z
        image=recorded_jet(projective_jet(z,v,a,A=alpha,C=c),1)
        recovered=inverse_physical_acceleration(image,1,A=alpha,C=c)
        require(recovered==a,'independent projective inverse series recovers acceleration')
        projective.append({'q_c_times_z':value_record(q),'c_per_metre':value_record(c),
            'image_position_px':value_record(image[0]),'image_speed_px_per_s':value_record(image[1]),
            'image_curvature_px_per_s2':value_record(2*image[2]),
            'naive_baseline_scale_acceleration_m_per_s2':value_record(2*image[2]/alpha),
            'naive_over_true':value_record(2*image[2]/(alpha*a)),
            'recovered_acceleration_m_per_s2':value_record(recovered)})
    nonlinear=[]
    for eta in map(Q,data['nonlinear_clock_eta']):
        rate,rate_derivative=1+2*eta*t,2*eta
        image=recorded_jet(projective_jet(z,v,a,A=alpha),rate,rate_derivative)
        recovered=inverse_physical_acceleration(image,rate,rate_derivative,A=alpha)
        require(recovered==a,'independent nonlinear clock inverse series recovers acceleration')
        nonlinear.append({'eta_per_s':value_record(eta),'recorded_time_s':value_record(t+eta*t*t),
            'clock_first_derivative':value_record(rate),'clock_second_derivative_per_s':value_record(rate_derivative),
            'image_speed_px_per_recorded_s':value_record(image[1]),'image_curvature_px_per_recorded_s2':value_record(2*image[2]),
            'naive_over_true':value_record(2*image[2]/(alpha*a)),'recovered_acceleration_m_per_s2':value_record(recovered)})
    offsets=[]
    for offset in map(Q,data['time_offsets_seconds']):
        s0=t+offset
        time_jet=[s0-offset,Q(1),Q(0)]
        global_image=[alpha*a*value/2 for value in multiply(time_jet,time_jet)]
        offsets.append({'offset_s':value_record(offset),'recorded_time_s':value_record(s0),
            'image_curvature_px_per_recorded_s2':value_record(2*global_image[2])})
    circular=[]
    target=Q(data['circular_example_target_acceleration'])
    for actual in map(Q,data['circular_example_true_accelerations']):
        image=projective_jet(actual*t*t/2,actual*t,actual,A=alpha)
        measured=2*image[2]
        assigned_alpha=measured/target
        circular.append({'true_acceleration_m_per_s2':value_record(actual),'image_curvature_px_per_s2':value_record(measured),
            'pixels_per_metre_chosen_from_target':value_record(assigned_alpha),
            'tautological_returned_acceleration_m_per_s2':value_record(measured/assigned_alpha)})
    require(list(map(len,(affine,projective,nonlinear,offsets,circular)))==[15,5,2,2,2],'independent exact example denominator')
    return {'scope':data['scope'],'physical_time_s':value_record(t),'synthetic_position_m':value_record(z),
        'synthetic_velocity_m_per_s':value_record(v),'affine':affine,'projective':projective,
        'nonlinear_clock':nonlinear,'time_offsets':offsets,'circular_calibration':circular}


def verify_runs(scopes):
    require(len(scopes)==2 and len({scope.resolve() for scope in scopes})==2,'two distinct synthetic executions required')
    require(all(scope.parent==HERE and scope.resolve()==scope for scope in scopes),'local non-aliased synthetic run directories')
    require(fp(HERE/'calculate.py')['sha256']==PRODUCER_SHA and fp(HERE/'inputs.json')['sha256']==INPUTS_SHA,'reviewed producer and declared synthetic inputs')
    data=json.loads((HERE/'inputs.json').read_text())
    expected=expected_producer_result(data)
    sources=[HERE/'calculate.py',HERE/'PROTOCOL.md',HERE/'inputs.json',Path(sys.executable)]
    pins={str(path):fp(path) for path in sources}
    expected_names={'calculate.py','PROTOCOL.md','inputs.json','initial.json','result.json','controls.json'}
    expected_controls={'passed':6,'checks':['known affine scale and clock result',
        'positive true acceleration with negative image curvature','known nonlinear clock curvature and recovery',
        'degenerate coordinate or nonincreasing clock rejected','degenerate coordinate or nonincreasing clock rejected',
        'degenerate coordinate or nonincreasing clock rejected']}
    receipts=[]
    for scope in scopes:
        require(not (scope/'failure.json').exists(),'failed synthetic execution cannot pass')
        receipt=json.loads((scope/'receipt.json').read_text())
        require(receipt['status']=='complete' and receipt['pins']==pins,'exact current synthetic procedure/input/runtime pins')
        require(set(receipt['products'])==expected_names and {path.name for path in scope.iterdir()}==expected_names|{'receipt.json'},'exact synthetic run product coverage')
        require(all(fp(scope/name)==identity for name,identity in receipt['products'].items()),'all synthetic products unchanged')
        require(all(fp(scope/path.name)==fp(path) for path in sources[:-1]),'exact procedure/input snapshots')
        require(json.loads((scope/'initial.json').read_text())=={'pins':pins,'python':sys.version},'exact initial runtime/procedure record')
        require(json.loads((scope/'controls.json').read_text())==expected_controls,'complete six producer control outcomes')
        require(json.loads((scope/'result.json').read_text())==expected,'all 26 exact rational/decimal synthetic results independently reproduced')
        receipts.append(receipt)
    require(receipts[0]==receipts[1] and fp(scopes[0]/'receipt.json')==fp(scopes[1]/'receipt.json'),'two complete seven-file runs byte identical')
    for scope in scopes:
        pins.update({str(scope/name):fp(scope/name) for name in expected_names|{'receipt.json'}})
    require(all(fp(Path(path))==identity for path,identity in pins.items()),'synthetic inputs/products unchanged after review')
    return {'runs':[{'scope':scope.name,'receipt':fp(scope/'receipt.json'),'files_including_receipt':7,'listed_products':6} for scope in scopes],
        'producer_imported':False,'examples':26,'counts':{name:len(expected[name]) for name in ('affine','projective','nonlinear_clock','time_offsets','circular_calibration')},
        'exact_rational_and_decimal_equality':True,'all_files_byte_identical':True,'pins':pins,
        'independent_method':'Taylor-series projection, local clock inversion and inverse projective Taylor series; no producer derivative/recovery functions used.',
        'scope':'Synthetic transformation algebra, not historical calibration or acceleration.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);parser.add_argument('--runs',nargs=2)
    args=parser.parse_args();out=args.out.absolute()
    require(out.parent==HERE and out.name.startswith('independent') and out.suffix=='.json' and not out.exists(),'new scoped independent receipt')
    pins={str(path):fp(path) for path in (Path(__file__),HERE/'PROTOCOL.md',HERE.parent/'CHARTER.md',Path(sys.executable))}
    result={'command':sys.argv,'pins':pins,'python':platform.python_version(),'oracle':'exact rational second-order Taylor polynomial algebra and local clock-series inversion; no producer import'}
    try:
        require(fp(HERE/'PROTOCOL.md')['sha256']==PROTOCOL_SHA and fp(HERE.parent/'CHARTER.md')['sha256']==CHARTER_SHA,'frozen scope')
        result['examples']=examples()
        if args.runs:
            result['run_verification']=verify_runs([(HERE/name).absolute() for name in args.runs])
        require(all(fp(Path(path))==identity for path,identity in pins.items()),'procedures and scope unchanged')
        result['status']='pass'
    except Exception as error:
        result.update(status='fail',error_type=type(error).__name__,error=str(error))
    with out.open('x') as stream:stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({key:result[key] for key in ('status','error_type','error') if key in result}))
    return 0 if result['status']=='pass' else 1


if __name__=='__main__':
    raise SystemExit(main())
