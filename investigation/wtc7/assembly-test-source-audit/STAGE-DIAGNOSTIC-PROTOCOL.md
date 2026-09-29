# Original reported-stage sensitivity diagnostic

Declared after full-page inspection of Thompson Tables4.2/4.3, but before
systematic original-stage calculation. Root has qualitatively inspected the
printed values and made rough mental comparisons suggesting that load/length
normalization might explain some differences from TN1749; this is not a blind
discovery or a preregistered historical validation. No such conversion is
admitted by this diagnostic, and numerical agreement must not select one.

The question here is narrower: how much does the choice of **reported failure
stage** change summaries of the original printed measurements? Retain all nine
tests and missing secondary stages. Use the frozen original root/independent
transcriptions, not digitized plots or reconstructed unrounded values.

For each bolt-size group, report both:

1. `initial`: the Table4.2 applied-shear value and associated rotation.
2. `maximum_reported_stage`: the larger applied shear among Tables4.2/4.3 for
   each test, retaining the rotation from that same stage. Choose initial for
   exact ties. When secondary is missing, retain initial and the source's
   missing-stage reason. This is not the global maximum of an acquired history,
   and a selected initial stage does not establish that later reserve is absent.

Show two explicitly labeled cohorts: all reported tests, and the TN-figure
subset excluding5ST1. The second is a membership sensitivity, not proof that
NIST excluded5ST1 from its tables. Do not exclude the whole3ST3 assembly merely
because its left-side derived-force data were questioned; the original's
controlling failure is on the right. Quality issues remain in the source ledger.

For each cohort/size/stage rule and for applied shear (kip) and rotation (rad),
calculate mean, sample and population variance/SD/COV. Use exact rational
mean/variance; high-precision square roots and COV. Report n and selected test/
stage values. Repeated unchanged cohorts are not independent evidence.
Also calculate secondary-minus-initial shear, percent change relative to initial
shear, and rotation difference for every test with a reported secondary stage.
Missing secondary entries remain missing, never zero or imputed.

No total-load factor, unit conversion, angular correction, Table4.1 moment-window
average, statistical significance, calibration threshold or NIST raw-series
membership is inferred. A later source-supported conversion requires a separate
prospectively stated diagnostic. This pass establishes endpoint sensitivity and
the limitations of treating unlike tables as the same validation target.

Freeze separate implementations before result cross-access. Require exact
mean/variance and stage-selection agreement, both source pins, two root runs,
independent consumer reproduction, and controls for initial/secondary/tie/null
selection, associated rotation (not independently maximized), singleton failure,
zero-mean rejection and sample/population variance. The independent check may
use its already frozen source schema; any cross-schema join is post-freeze.
