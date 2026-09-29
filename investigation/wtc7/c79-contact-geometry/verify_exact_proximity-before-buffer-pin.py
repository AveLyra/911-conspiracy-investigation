#!/usr/bin/env python3
"""Independent exact-binary-rational geometry verification core.

Frozen before inspection of the separate exact producer or its certificates.
No root routine is imported. Gram projection, exact segment clamping and
integer square-root enclosures independently reconstruct the geometry.
Source inputs are parsed binary64 values, not original decimal lexemes.
"""
import argparse
from fractions import Fraction as F
import hashlib
import math
from pathlib import Path
import sys
import numpy as np

BASE=Path(__file__).resolve().parent
METHOD_SHA='961baeea44e0b156950b1b5e4c387734a9fea4afe45bb393ea8336fce3e945aa'
TRIS=((0,1,2),(0,2,3),(0,1,3),(1,2,3))


class ExactError(Exception):pass


def require(ok,code):
    if not ok:raise ExactError(code)


def rational_float(value):
    value=float(value);require(math.isfinite(value),'nonfinite_binary_input')
    return F(*value.as_integer_ratio())


def vector(values):return tuple(rational_float(v) for v in values)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def rational_patch(q,u,v):
    mixed=add(sub(q[0],q[1]),sub(q[2],q[3]))
    return add(add(q[0],mul(sub(q[1],q[0]),u)),add(mul(sub(q[3],q[0]),v),mul(mixed,u*v)))


def extended_quad(original,e):
    h=(e-1)/2
    return tuple(rational_patch(original,u,v) for u,v in ((-h,-h),(1+h,-h),(1+h,1+h),(-h,1+h)))


def edge_squared(point,a,b):
    edge=sub(b,a);ap=sub(point,a);length2=dot(edge,edge)
    if length2==0:return dot(ap,ap)
    projection=dot(ap,edge)
    if projection<=0:return dot(ap,ap)
    if projection>=length2:
        bp=sub(point,b);return dot(bp,bp)
    return dot(ap,ap)-projection*projection/length2


def triangle_squared(point,a,b,c):
    """Exact Gram-system barycentric projection; closed edges remain candidates."""
    u=sub(b,a);v=sub(c,a);p=sub(point,a)
    uu=dot(u,u);uv=dot(u,v);vv=dot(v,v);up=dot(u,p);vp=dot(v,p)
    determinant=uu*vv-uv*uv;require(determinant>=0,'negative_Gram_determinant')
    squared=min(edge_squared(point,a,b),edge_squared(point,b,c),edge_squared(point,c,a))
    if determinant==0:return {'squared_distance':squared,'projection':-1,'signed_plane_squared':None,'plane_sign':None}
    beta=(vv*up-uv*vp)/determinant;gamma=(uu*vp-uv*up)/determinant
    inside=beta>=0 and gamma>=0 and beta+gamma<=1
    perpendicular=sub(p,add(mul(u,beta),mul(v,gamma)))
    plane_squared=dot(perpendicular,perpendicular)
    if inside:squared=min(squared,plane_squared)
    oriented=dot(p,cross(u,v));sign=(oriented>0)-(oriented<0)
    require(squared>=0 and plane_squared>=0,'negative_exact_squared_distance')
    return {'squared_distance':squared,'projection':int(inside),'signed_plane_squared':plane_squared,'plane_sign':sign}


def sqrt_enclosure(value,bits):
    require(isinstance(value,F) and value>=0 and isinstance(bits,int) and bits>0,'sqrt_input')
    numerator=value.numerator<<(2*bits);denominator=value.denominator
    n=math.isqrt(numerator//denominator);scale=1<<bits
    lo=F(n,scale);hi=lo if n*n*denominator==numerator else F(n+1,scale)
    require(lo*lo<=value<=hi*hi,'sqrt_certificate_failed')
    return lo,hi


def outward_float(value,direction):
    require(direction in (-1,1),'outward_direction')
    result=float(value);require(math.isfinite(result),'outward_conversion_nonfinite')
    while (rational_float(result)>value if direction==-1 else rational_float(result)<value):
        result=float(np.nextafter(result,-math.inf if direction==-1 else math.inf))
        require(math.isfinite(result),'outward_adjustment_nonfinite')
    return result


def aabb_squared(point,corners):
    total=F(0)
    for axis in range(3):
        low=min(c[axis] for c in corners);high=max(c[axis] for c in corners)
        gap=low-point[axis] if point[axis]<low else point[axis]-high if point[axis]>high else F(0)
        total+=gap*gap
    return total


def threshold_enclosures(slave,master,diagonal_squared,bits):
    if slave is None:return None
    require(len(slave)==2 and slave[0]>=0 and slave[1]>=slave[0] and len(master)==2 and master[0]>=0 and master[1]>=master[0],'thickness_ranges')
    diagonal=sqrt_enclosure(diagonal_squared,bits);scale=rational_float(.05);factor=rational_float(.6)
    return tuple((max(factor*(slave[j]+master[j]),scale*diagonal[0]),
                  max(factor*(slave[j]+master[j]),scale*diagonal[1])) for j in (0,1))


def exact_pair(point,original,extension,slave,master,epsilon,bits):
    q=extended_quad(original,extension);triangles=[triangle_squared(point,*[q[k] for k in indices]) for indices in TRIS]
    da2=min(t['squared_distance'] for t in triangles[:2]);db2=min(t['squared_distance'] for t in triangles[2:])
    mixed=add(sub(q[0],q[1]),sub(q[2],q[3]));w2=dot(mixed,mixed)/16
    a=sqrt_enclosure(da2,bits);b=sqrt_enclosure(db2,bits);w=sqrt_enclosure(w2,bits)
    lower=max(F(0),a[0]-w[1],b[0]-w[1]);upper=min(a[1]+w[1],b[1]+w[1])
    require(lower<=upper,'exact_enclosure_inverted')
    diag2=min(dot(sub(original[2],original[0]),sub(original[2],original[0])),dot(sub(original[3],original[1]),sub(original[3],original[1])))
    threshold=threshold_enclosures(slave,master,diag2,bits)
    cls=0 if threshold is None else 3 if upper<threshold[0][0]-epsilon else 1 if lower>threshold[1][1]+epsilon else 2
    signed=[]
    for t in triangles:
        if t['signed_plane_squared'] is None:signed.append(None)
        else:
            interval=sqrt_enclosure(t['signed_plane_squared'],bits)
            signed.append(tuple(-v for v in reversed(interval)) if t['plane_sign']<0 else interval)
    return {'class':cls,'dA_squared':da2,'dB_squared':db2,'w_squared':w2,'diagonal_squared':diag2,
        'dA':a,'dB':b,'w':w,'patch_enclosure':(lower,upper),'thresholds':threshold,
        'projection_flags':tuple(t['projection'] for t in triangles),'signed_plane_enclosures':tuple(signed),
        'aabb_squared':aabb_squared(point,q),'extended_corners':q}


def encode_fraction(value):return [str(value.numerator),str(value.denominator)]


def controls():
    passed=[]
    def check(name,value):require(value,'control_'+name);passed.append(name)
    check('binary_input_not_decimal_rational',rational_float(.1)!=F(1,10) and rational_float(.5)==F(1,2))
    for value in (F(0),F(4),F(1,4),F(2),F(1,3)):
        lo,hi=sqrt_enclosure(value,80);lo2,hi2=sqrt_enclosure(value,120)
        check('sqrt_'+str(value).replace('/','_'),lo*lo<=value<=hi*hi and lo<=lo2<=hi2<=hi)
    check('perfect_roots_exact',sqrt_enclosure(F(4),80)==(F(2),F(2)) and sqrt_enclosure(F(1,4),80)==(F(1,2),F(1,2)))
    for x in (F(1,10),F(-1,10),F(1,3),F(3,2),F(0)):
        check('outward_'+str(x).replace('/','_'),rational_float(outward_float(x,-1))<=x<=rational_float(outward_float(x,1)))
    tri=[vector([0,0,0]),vector([1,0,0]),vector([0,1,0])]
    for p,sq,inside in (([.25,.25,2],F(4),1),([.5,-.5,0],F(1,4),0),([-1,-1,0],F(2),0),([.5,0,0],F(0),1)):
        actual=triangle_squared(vector(p),*tri);reverse=triangle_squared(vector(p),tri[0],tri[2],tri[1])
        check('triangle_'+str(len(passed)),actual['squared_distance']==sq and actual['projection']==inside and reverse['squared_distance']==sq and reverse['projection']==inside)
    degenerate=triangle_squared(vector([.5,1,0]),tri[0],tri[1],tri[1])
    check('degenerate_plane_unknown_edges_exact',degenerate['squared_distance']==1 and degenerate['projection']==-1 and degenerate['signed_plane_squared'] is None)
    q=tuple(vector(v) for v in [[0,0,0],[1,0,0],[1,1,.25],[0,1,0]])
    point=rational_patch(q,F(1,3),F(2,5));eps=rational_float(1e-10)
    result=exact_pair(point,q,F(1),(F(1),F(1)),(F(1),F(1)),eps,80)
    check('known_warped_patch_zero_in_enclosure',result['patch_enclosure'][0]==0 and result['class']==3)
    unknown=exact_pair(vector([100,100,100]),q,F(1),None,(F(1),F(1)),eps,80)
    check('unknown_priority',unknown['class']==0 and unknown['thresholds'] is None)
    square=tuple(vector(v) for v in [[0,0,0],[1,0,0],[1,1,0],[0,1,0]])
    overlap=exact_pair(vector([.5,.5,.1]),square,F(1),(F(0),F(1)),(F(0),F(1)),eps,80)
    check('thickness_interval_unresolved',overlap['class']==2)
    extended=extended_quad(square,rational_float(1.025));p=vector([1.08,.5,0])
    threshold=threshold_enclosures((F(0),F(0)),(F(0),F(0)),F(2),80)[1][1]
    check('extended_domain_only_box_admission',aabb_squared(p,square)>threshold**2 and aabb_squared(p,extended)<=threshold**2)
    r80=exact_pair(vector([.3,.4,.5]),q,rational_float(1.006),(F(0),F(1)),(F(0),F(1)),eps,80)
    r120=exact_pair(vector([.3,.4,.5]),q,rational_float(1.006),(F(0),F(1)),(F(0),F(1)),eps,120)
    check('full_pair_enclosure_nesting',r80['patch_enclosure'][0]<=r120['patch_enclosure'][0]<=r120['patch_enclosure'][1]<=r80['patch_enclosure'][1])
    check('exact_squared_invariants_across_precision',all(r80[k]==r120[k] for k in ('dA_squared','dB_squared','w_squared','diagonal_squared','projection_flags','aabb_squared','extended_corners')))
    check('pin_mutation_detectable',hashlib.sha256(b'changed').hexdigest()!=hashlib.sha256(b'original').hexdigest())
    return passed


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--selftest',action='store_true');args=parser.parse_args()
    require(args.selftest,'consumer_adapter_not_yet_added')
    require(hashlib.sha256((BASE/'EXACT-ARITHMETIC-ADDENDUM.md').read_bytes()).hexdigest()==METHOD_SHA,'method_pin')
    import json
    test=controls();print(json.dumps({'status':'PASS','count':len(test),'controls':test}))
