# Prospective bounded projection/uncertainty test

2026-09-20 UTC. Declared after both eight-page reading notes were frozen,
before writing or running new numerical geometry code. This is an exact
synthetic geometry check, not measurement of a historical image, recovery of
NIST's formula, or validation of its 11 m +/- 3 m. The original source-reading
protocol and both frozen notes remain unchanged.

Coordinates: east x, north y, up z. All following lengths use an arbitrary
synthetic unit u, **not calibrated WTC 7 metres or pixels**. Unit horizontal
normals n1,n2 define signed distances q1,q2 from the original vertical-edge
viewing planes. We assume known normals, simultaneous observations of the
same point and independent bounded residual errors; these assumptions are
not established for the historical data. No stochastic/confidence meaning.

Calculate d = inverse(N) q, with N's rows n1,n2. For each residual rectangle
[q1-e1,q1+e1] x [q2-e2,q2+e2], calculate exact extrema of x and y and test
whether (0,0) is feasible and, separately, whether any y=0 is feasible. These
are different questions. Fraction arithmetic is required; no fitted parameter,
unknown camera calibration, historical error bound or parameter optimization.

Fixed conditioning fixtures: n2=(1,0), truth d=(0,2), e1=e2=1/5, and n1 in
this order: (3/5,4/5), (4/5,3/5), (12/13,5/13), (99/101,20/101),
(9999/10001,200/10001). Each row is a unit vector; q=N d. Test how the exact
north interval changes as the directions become nearly parallel. These five
geometries are selected synthetic sensitivity cases, not actual camera angles.
No expanded sweep after seeing results.

General inverse fixture: n1=(3/5,4/5), n2=(-4/5,3/5), truth=(2,-3),
e1=1/5,e2=1/10. Singular negative control: n1=n2=(1,0), which must reject
unique inversion rather than invent a displacement. Invalid negative-error
input must be rejected. Zero-width errors must reproduce the exact point.

Independent pinhole check: cameras C1=(-4,3,1), C2=(0,8,2); right axes
r1=(3/5,4/5,0), r2=(1,0,0); forward axes f1=(4/5,-3/5,0), f2=(0,-1,0);
up=(0,0,1), unit focal length and zero principal point. Projection is
(right dot (P-C), up dot (P-C)) / (forward dot (P-C)). Test horizontal
locations (0,0),(0,2),(1,-1), each at z=0,2,5: nine points, two cameras.
Verify unchanged projected horizontal position over vertical descent;
zero offset from the projected original vertical edge for (0,0); and recovery
of signed plane distances as image-horizontal-coordinate times depth. The
normal directions and camera centers were chosen to make this identity exact.
This check has no historical lens, pixel, pose or registration claim.

Falsifiers: any failed exact forward/inverse identity, a displacement extreme
outside the corner-derived feasible range, mismatched zero-feasibility result,
pure vertical motion leaving its original edge in these ideal cameras, or
unrejected singular inversion invalidates the corresponding method claim.
Passing cannot validate real camera registration, feature identity, time join,
uncertainty bounds or cause. The independent checker should derive extrema
via the four residual-box vertices rather than import the producer algorithm.

Root produces a small standalone standard-library calculation and create-only
JSON receipt. A separate agent derives its oracle from this protocol before
reading the producer, freezes results, and then compares. Root separately
checks all source-render pins and PNG decodes. No browser/UI, installation,
network, new source acquisition, main/raw/legal or accepted-engine mutation.

Editorial correction to the frozen root-reading.md: its phrase
`identity,+a fixed` should read `identity, a fixed`; the saved note/hash are
preserved. The correction does not change its mathematical assumptions.
