> **Historical research:** This record presents idealized mechanics and computational checks, not a building-specific reconstruction or causal determination. Filesystem output paths are omitted where indicated. See [provenance](../structural-bounds-PROVENANCE.json).

# Independent main-agent mechanics review

2026-09-08. This is mathematical/code review of explicitly idealized equations, not a licensed structural review or physical experiment. The preserved module contains no WTC 7 mass, capacity, temperature or geometry inputs.

The main analyst read the complete derivation, protocol, implementation and fifteen tests. Work-energy signs are consistent with downward positive displacement: resistance removes work, while gravity continues adding work during deformation. The plateau first-stop criterion is `R/(Mg) >= 1+h/delta` under the specified sustained-resistance model. The early-barrier example correctly prevents skipping an unreachable negative-energy interval. An exact endpoint stop remains only a first zero of speed; removal of resistance afterward can restart motion. Permanent arrest is not established.

The collision equations conserve the specified subsystem momentum only under negligible external impulse. Their energy-loss expression and inelastic mass-accretion recurrence are correct for that assumption; attached floor supports can invalidate it. Separating collision loss from later resistance work avoids algebraic double counting, but physical application would still have to demonstrate that those are genuinely distinct processes.

The ideal Euler ratio and dimensions are correct; it concerns a reduced instability threshold, not necessarily increased applied axial load. Applying a uniform effective-length ratio to the report's directional, partly retained Column 79 restraints would exceed the model. The gravity travel calculations also use correctly stated initial conditions and cannot establish a real propagation schedule or unconditional lower bound.

Verification actually performed:

- All fifteen original unit/invariance tests passed on the main rerun.
- Regenerated all six tables plus manifest into `[local temporary output path omitted]`; `diff -qr` against `run-v1/` returned no differences.
- [Separate velocity recurrence](main_review.py) agreed with the work-energy implementation on a declared additional 42-case arithmetic-check grid and 252 visited stages. It uses constant-acceleration `v²` updates, momentum-based pickup and first-zero stopping; this is a separate implementation of the same ideal mechanics, not independent physical evidence.
- Every preserved table hash matched. [Machine-readable review receipt](main-review.json) identifies code versions and scope.

No must-fix mathematical defect was found for this finite illustrative module. Important limits remain: repeated identical target properties make this grid's stopping cases stop at the first target; no realistic lower strengthening floor is tested; no actual floor area/mass distribution, slab bridging, contact duration, fracture law, partial pickup, mass loss or residual bracing is known from the toy inputs. A runnable general-purpose structural solver and arbitrary-input numerical robustness are not claimed.

The highest-value next step is the separately pinned regional cascade/handoff audit: recover the actual initial state and floor-by-floor energy/reaction/contact histories, include the reported 3.5-hour non-collapse control, and test residual capacity and directional restraint with competent review. The toy results neither establish fire initiation nor exclude intentional support removal.
