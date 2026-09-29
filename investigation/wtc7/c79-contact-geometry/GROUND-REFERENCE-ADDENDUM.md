# Discrete ground-reference admission

September 13, 2026; after the synthetic preflight failure and before the first
geometry-source read. The original producer and failed-command record remain
preserved. Root personally read complete physical pages758–759 (printed14.14–15)
of the admitted May2007 Version971 manual, SHA
f65ba6238860e2f8c821e776a7539abde8210966e79c2ebbac424e3262fce48d.
Full page renders are `/private/tmp/c79-ground-review.qWU1is/p758.png` and
`p759.png`, both Poppler commands completed at exit0.

The ELEMENT_DISCRETE definition expressly assigns N2=0 to a spring/damper
between N1 and ground. The revised source reader will retain a counter for
this explicit endpoint form, require N1 positive, exclude only that N2 zero
from geometric node membership/coordinate lookup, and continue rejecting
invalid zeros in other physical vertex slots. A ground reference is not a
missing mesh node and not a coordinate at the origin. It supplies no new
stiffness, load, contact or historical behavior by itself.

The same page warns about unique element identifiers relative to visualization
null beams, masses, stiffness/damping and orientation conventions. The reader's
typed-family ID tests do not certify an arbitrary same-number combination as
a valid solver deck. The following page defines S/PF/OFFSET separately; this
ground fix does not implement or reinterpret those force/output/state fields.
No claim is made yet that a ground-reference element occurs in the supplied
source, and earlier frozen source outputs are not modified.
