# What the published stable case comparison establishes

The reported 3.5-hour case is a meaningful **local-damage arrest control**:
some floors and connections fail, but the reported response does not progress
to interior-column instability and global collapse. This positively supports
the narrower proposition that the published model distinguishes different
damage states. It does not demonstrate that the real building crossed that
boundary, or that the inputs on either side were physically correct.

The newly checked figure captions make the timing more precise. They depict
states labelled stable at parenthetical times 12.2 s and 12.76 s. If those
labels and the stated 8.5 s damage application share the global simulation
clock, the displays are 3.70 s and 4.26 s afterward. **Neither
caption identifies the run's termination time or supplies a numeric stability
criterion.** These are displayed stable states, not proof that the run ended
then, stayed stable indefinitely, or would collapse later. The 3.5h label
refers to the antecedent ANSYS fire-damage state, not3.5hours of global
dynamic simulation.

Research only, October5,2026. The fixed [scope](SCOPE.md) covers four complete
pages of the held NCSTAR1-9, physical655–658/printed589–592. Two attributed
AI readings, source hashes and arithmetic are not a solver reproduction,
independent historical source or qualified engineering opinion. The main
[charter](/Users/admin/docs/911/research/sherlock-wtc7-investigation/CHARTER.md)
continues to control the full investigation.

## Exact source comparison

| Source location | What is actually supplied | Evidentiary limit |
|---|---|---|
| §12.4.5, printed589 | Describes the same loading sequence and parameters as§12.4.4, except earlier3.5h ANSYS fire-induced damage. Damage applied at8.5s; initial southeast floor failures8/13/14 and connection damage12; some girders on12–14 fall, without sufficient further progression below12 to initiate collapse. | A positive author-reported controlled comparison, not a native input diff. Exact thermal arrays, restart states, property versions and all active controls are not enumerated here. Do not silently decide which temperature field accompanied the changed damage. |
| Same page | Reports stability at analysis end and less extensive damage around columns76–81. Also reports west-core connection damage from the WTC1 debris-initialization step. | Stable does not mean undamaged. Lack of further cascading below12 does not mean all lower floors were intact. No quantitative run-end/stability definition supplied on these pages. |
| Figure12-64, printed590 | Framing damage around76–81 after stability, captioned−3.24s(12.76s), vertical displacement−39to0in (−1to0m). A callout reports a76–79 girder connection failing at76 and being stable afterward. | Local connection failure is not necessarily global instability, even in the published model. A contour or drawn surviving member supplies neither its reaction force nor residual capacity. |
| Figure12-65, printed590 | Lower-floor stable structure at−3.8s(12.2s), southwest view. Callouts distinguish impact-zone secondary collapse from limited progression around80–81. | A selected rendered state, not a continuous force/energy history or proof of long-term stability. |
| Figure12-63 above§12.4.5, printed589 | Exterior buckling from preceding discussion; caption says slabs removed from view. | It is not a stable-case figure simply because it shares the page. Visual omission is not physical deletion. |
| §12.4.6 and Figures12-66/67, printed591–592 | A different analysis omits WTC1 debris impact; describes shorter initialization and a13.3s penthouse reference instead of16s, similar early progression and different later westward progression. | These collapsing frames are not later frames of the3.5h stable run. They do not supply its missing end state or a thermal/damage-only matched pair. |

The published common-parameter statement deserves weight. It cannot be
dismissed merely because native records are unavailable. The strongest reason
not to treat it as independently verified is equally specific: a complete
case/input/state/output join is absent from this source and the inspected
release. A temperature-state mismatch, changed residual support or unintended
restart difference could change what the comparison isolates. None is shown
to have occurred by this review.

## Timing and display labels that require reconciliation

The two stable-case caption pairs imply the same16.0s time-reference offset:
12.76−(−3.24)=16.0 and12.2−(−3.8)=16.0. This is arithmetic on report labels,
not evidence that a penthouse kink occurred in the stable run. The source's
collapse-reference convention must not manufacture an event in a noncollapsing
case.

The adjacent no-debris case contains a specific one-second label inconsistency.
Printed591 gives the penthouse reference as13.3s and calls17.5s both4.2s after
that reference and3.2s. On printed592, five relative/parenthetical pairs imply
13.3s offset; the last,3.2(17.5), implies14.3s. Subtraction gives17.5−13.3=4.2.
This cannot be repaired by selecting whichever label improves a camera fit.
An editorial/caption error or an inconsistent event reference could explain it;
native output and the figure/time crosswalk would identify which label or event
needs correction. No numerical-run defect or intentional manipulation follows.

Figures 12-66/67 captions also describe resultant lateral displacement with
negative endpoints. Both readers clearly read the upper lateral (XY) legend
as zero to positive 0.5 m. Root read the lower legend as positive too; the
second reader found some leading tick characters cramped or clipped. The
upper figure therefore supplies the jointly clear caption/legend sign
discrepancy; the lower scale retains that legibility qualification. Neither
establishes a direction of physical motion. No force, signed trajectory or
uncertainty estimate is calculated from these colors.

These findings concern this pinned report edition. The existing complete
[two-page errata inventory](/Users/admin/docs/911/research/sherlock-wtc7-investigation/fuel-system-audit/equipment-source-followup/errata-review/report.md)
lists other corrections, not these page589–592 timing/caption fields. That is
a secondary version-control check, not a new reading of the errata or an
exhaustive search for subsequent corrections. A later applicable corrected
edition would change the current-publication assessment, not the contents of
this preserved edition.

## What the released files can and cannot test

The [released-input audit](/Users/admin/docs/911/research/sherlock-wtc7-investigation/lsdyna-supplement-content-audit/report.md)
already establishes a gravity-stage master terminating at4.50s, a thermal
ramp beginning later, commented damage hooks naming4.1h, and a separately
supplied4.0h set2 list. It does not supply the3.5h control or native results.
Later [material/run work](../../material-run-crosswalk/report.md) and the
[curve search](../../curve-release-search/report.md) refine missing effective
properties and LCD602/803 dependencies. Original element-count interpretations
in the early audit were superseded by the later member/material audits; they
are not revived here.

A separate current read-only feasibility review confirmed these already known
facts in the inventory fields and later reports. No newly untested located
executable-case candidate emerged. Output/restart cards request files; they
are not the requested output files. The June short ANSYS driver is not an
authenticated substitute for a similarly named LS-DYNA input. Package-specific
absence does not establish that historical originals never existed or that
all public holdings have been exhausted.

## Minimal records and the actual discriminating test

This is a research requirements proposal, **not an outgoing records request or
an authorized solver run**. It makes the
[existing D5/D6 dependencies](../../synthesis-packet/reconciliation-2026-10-05/report.md)
concrete for this pair without
requiring every upstream fire question to be solved first.

| Required for each reported case | What the comparison would check |
|---|---|
| Exact case identifier, source/version manifest, active root/includes and complete effective properties | Whether the two cases really differ only in declared inputs; resolve4.0/4.1h and case-family labels without guessing. |
| Applied nodal temperature field and exact damage/deletion/state mapping, with application schedule | Whether temperature was held fixed or changed along with damage; identify the actual changed members/connections rather than treating30minutes as the sole causal variable. |
| Continuation/restart instructions and material state immediately before/after damage application | Retained coordinates, velocities, stresses/strains, mass, contact/restraint state and energy; detect accidental reinitialization or unexplained impulses. |
| Solver/build, complete input echo, numerical warnings and run end/termination reason | Establish execution semantics, actual duration and why the stable run was stopped; distinguish a plotted stable state from a stability criterion. |
| Native histories for the same selected floor/member/contact groups, including receiving floors and directional C79 restraints | Force, displacement, load redistribution, contact impulse, kinetic/internal/external work and numerical energy; determine whether propagation arrests and why. |
| Frame-to-case/time and display-variable crosswalk | Resolve the stable reference convention, adjacent one-second timing inconsistency and signed-caption/resultant-legend difference before quantitative media comparison. |

The first executable test would reproduce both reported outcomes **unchanged**,
with their stated initialization and verified identities. Only then compare
independently justified residual connection/restraint and handoff variants.
Document collapse and arrest, continuing motion, insufficient simulated
duration and numerical failure separately. Do not score an early snapshot as
permanent stability, or a solver crash as collapse.

Before running, freeze a competent, case-specific stability criterion and
observation horizon using actual dynamical scales, numerical resolution and
resource limits. Freeze the common sequence observables and tolerances before
seeing new outcomes. Arbitrary stop times or unsupported tolerances would
create a misleading pass/fail test. Native force/energy channels and appropriate
solver/expert resources are needed; no such execution is claimed here.

If materially different thermal/damage states are found, a later factor-separated
test may be useful. Mixing an earlier damage map with a later temperature
field is not automatically a physically reachable history; those crossed
states require explicit justification and must remain conditional sensitivity
cases. Failure to reproduce a specified historical model weakens that model,
not all fire mechanisms; successful prescribed support loss does not establish
its historical means or intent.

## Evidentiary assessment and completion

The strongest affirmative finding is the published retention of a noncollapse
outcome despite appreciable local damage. It counters a simplistic account
that any local failure or any damage input inevitably makes this model collapse.
The strongest limit is not rarity alone: neither the historical damaged states
nor their residual capacities, complete output histories and propagation
boundary are independently validated here.

Claim strength is layer-specific. **A, directly established**, applies to what
the pinned publication says and to the arithmetic inconsistency between its
printed labels, not to the actual building's behavior. **C, materially
assumption-dependent**, applies to treating the published common-parameter
statement as a genuinely matched model comparison until the native case
differences are checked. **D, underdetermined**, applies to identifying the
historical propagation boundary or collapse cause from this four-page unit.
The native manifests and force/state histories specified above could
strengthen or contradict those latter interpretations.

The new source detail narrows what the reported control demonstrates and
identifies a timing-label inconsistency to resolve. It does not change the
overall collapse-cause ranking. There is no new simulation result, empirical
force measurement, actual-human acceptance or causal identification.

The four-page reading stops here. No further image neighborhood, generic
missing-file scan, solver repair, records outreach or source promotion follows.
Full investigation remains active; its remaining media, fire, comparator,
documentary and expert/input dependencies are not replaced by this check.
Both frozen readings have been compared; the disclosed
[source-reader critique](review.md) is complete and its two wording corrections
are incorporated. Source integrity and exact label arithmetic checks passed;
the actual execution and final closeout checks are in [verification](verification.md).
