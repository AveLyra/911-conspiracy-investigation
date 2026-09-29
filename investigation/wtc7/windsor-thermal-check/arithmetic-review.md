# Independent arithmetic and implication review

2026-09-20 UTC. Research only. Scope: current `calculate.py`,
`calculation02.json`, `PROTOCOL.md`, `SCOPE-EXPANSION.md`, and the already
frozen `root-notes.md`. No observer note was read. No PDF page or image was
displayed, no source acquired, and no thermal or structural solver was run.
The source numbers were transcribed independently from the root freeze for
the numerical check; this is not an independent visual transcription or
historical experiment. Only this new review file was written.

## Result

All 16 saved derived values pass an independent standard-library Fraction
check without importing or executing the producer as the oracle: 12 values
were compared to exact rational results and four positive depths were
checked through their exact squared relations. All three ordering flags,
10 source-input strings, source/script/Python identities and Python version
also match. Maximum normalized numerical residual was approximately
8.55431e-50, below the declared comparison threshold 1e-47. This is a check
of decimal representation of calculations, not physical uncertainty.

The producer's nine unittest methods were separately rerun and passed.
Eight known-answer relation assertions were executed in the independent
checker before the saved values were compared. Seven checked input/runtime
paths had identical SHA256 values before and after that checker.

There is no material calculation error in `calculation02.json`. One small
wording correction is needed when composing the report; do not rewrite the
frozen root record:

- Root notes lines 88–89 call the discrepancy a “factor-of-about3.4 time
  difference between these curves.” The normalized-50.3-mm curve gives
  4786.549095... s; dividing by the source's approximate 1400 s gives
  3.418963639..., whereas dividing by the illustrative 2sqrt(alpha*t)
  result, 1475.438596... s, gives 3.244153370.... Use “about 3.42 relative
  to the printed 1400 s” or “about 3.24 between the two illustrative
  conventions.” This denominator distinction does not remove the mismatch.

## Exact relations and units

Let `a = (6/5)/(2400*880) = 1/1760000 m²/s`, printed
`ap = 57/100000000 m²/s`, `d = 503/10 mm`, `t = 3600 s`,
`p = 230/4 = 115/2 mm`, and target depth `q` in mm.

| Check | Independent relation / result | Meaning |
|---|---|---|
| Property arithmetic | `a = 1/1760000`; `100*(ap-a)/a = 8/25 = 0.32%` | Printed diffusivity is 0.32% larger than the calculated value, relative to that calculated value; ordinary displayed rounding is compatible. |
| Endpoint spacing | `230/(5-1) = 57.5 mm` | Conditional on five equally spaced endpoint values. Does not establish the actual shell-node/integration/temperature scheme. |
| Same-curve ordering | `(1400-3600)*(58-50.3) = -16940 s mm` | These central points cannot lie on the same nondecreasing depth function with the same definition/time origin. No square-root assumption needed. |
| Normalized square-root depth | `D(s)^2 = d²*s/t`, with positive `D` | Conditional illustration, not an equation recovered from the paper. |
| Normalized square-root time | `T(q) = t*q²/d²` | 58 mm: 4786.549095... s; 57.5 mm: 4704.378105... s; 10 mm: 142.287428... s. |
| Dimensionless coefficient | `C² = (depth_mm/1000)²/(ap*time_s)` | 1.232987329... from the figure pair versus 4.215538847... from the prose pair; no common coefficient for those central pairs. |
| Hypothetical `D=2sqrt(ap*s)` | `D_mm² = 4000000*ap*s`; `T(q)=q²/(4000000*ap)` | 58 mm: 1475.438596... s; 57.5 mm: 1450.109649... s. Not an attributed author method. |

`k/(rho*cp)` has dimensions `(J/(s m K))/(kg/m³ * J/(kg K)) = m²/s`.
The factor 1,000 converts mm to m before squaring; the squared-depth oracle
therefore uses 1,000,000, and the factor-two convention adds a factor four.
Time ratios and `C²` are dimensionless. No unit-conversion defect was found.

## Interpretation and strongest alternatives

The code, JSON limits and root freeze properly label both square-root
relations as conditional/hypothetical. Their reproduction must not be
described as reproducing the authors' actual Figure 4 formula or worksheet.
This reviewer has not independently verified the root's full-draft finding
that no explicit definition was located; that is a source-reading claim.

The strongest ordinary explanations remain a different penetration
threshold/convention, different time origin or boundary history, different
geometry/material inputs, or a prose/figure/draft transcription error.
`2sqrt(ap*t)` is numerically near the prose time and demonstrates a possible
different-convention explanation; it does not prove that explanation or
repair the figure value under that same convention. Cooling or other
transient forcing could invalidate a monotonic-depth assumption; whether
the paper actually supplies such a case is for the source readers.

The central depth difference is 7.7 mm. As an explicitly assumed rounding
illustration only, nearest-0.1-mm reporting of 50.3 gives [50.25,50.35) and
nearest-1-mm reporting of 58 gives [57.5,58.5); those intervals do not
overlap. This is not a source-supplied error model. In particular, “about
1400 s” has no declared uncertainty interval here; it must not become a
statistical confidence limit or a universally falsified error allowance.
The calculated-versus-printed diffusivity changes the illustrative 58-mm
time only from 1475.438596... to 1480.16 s. That specific rounding change
does not reconcile the 4786.549095... s normalized-curve prediction.

The general need to resolve a thermal gradient is distinct from proving
that this particular mesh is adequate or inadequate at a specified time.
No actual temperature interpolation, convergence study, integration rule,
temperature/strength error, historical exposure, as-built reserve capacity
or direction/magnitude of thermal bias has been computed. The proposed
10-mm resolution is not validated by this arithmetic. Penetration depth
must not be equated to a literal advancing front or to a 500°C isotherm
without a definition and applicable boundary conditions. No WTC7 causal
ranking or misconduct inference follows.

## Actual execution and control coverage

Commands used for reads were `cat`, selected `nl`/`sed`, and `shasum -a 256`.
The main controls and full charter had already been read; their fresh hashes
match those versions. Evidence-falsification, source-of-truth and narrow
development-verification skills were applied. They preserve the distinction
between successful arithmetic, source interpretation and physical validation.

Producer control command (exit 0; nine methods, 0.001 seconds reported):

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/windsor-thermal-check/calculate.py --test
```

The nine methods cover a diffusivity known answer; same-time depth;
fourfold-time/twofold-depth scaling; inverse; time-unit rescaling; a
roundtrip; zero/negative/infinite/NaN first arguments to `scaled_time`;
decreasing/increasing/constant ordering and duplicate-time behavior.
They do not constitute exhaustive invalid-input coverage for every argument
of every helper, mesh-physics controls or historical source validation.
The create-only `open('x')` output guard is present in inspected code; no
duplicate-output attempt or source-hash rejection was executed by this
reviewer. The earlier script/result edition was not read or rerun; its
history remains the root's recorded execution history.

The independent read-only command used the same explicit Python with
`PYTHONDONTWRITEBYTECODE=1`, reading JSON through `json` and using only
`Fraction`, `Path`, `hashlib` and `sys`. The essential comparison recipe is
below. These are the relations actually checked, not a producer import:

```python
from fractions import Fraction as F
# r is json.loads(Path('calculation02.json').read_text()).
a = F(6,5)/(2400*880); ap = F(57,100000000)
d,t,q,s,p = F(503,10),F(3600),F(58),F(1400),F(230,4)
expected = {
 'alpha_from_k_rho_cp_m2_per_s': a,
 'printed_alpha_relative_difference_percent': 100*(ap-a)/a,
 'equal_5_endpoint_node_spacing_mm': p,
 'sqrt_scaling_d_100s_mm': F(503,60),
 'sqrt_scaling_t_58mm_s': t*q*q/(d*d),
 'sqrt_scaling_t_57_5mm_s': t*p*p/(d*d),
 'sqrt_scaling_t_10mm_s': t*100/(d*d),
 'c_squared_from_50_3mm_3600s': d*d/(1000000*ap*t),
 'c_squared_from_58mm_1400s': q*q/(1000000*ap*s),
 'hypothetical_2sqrt_t_58mm_s': q*q/(4000000*ap),
 'hypothetical_2sqrt_t_57_5mm_s': p*p/(4000000*ap),
 'hypothetical_2sqrt_t_58mm_derived_alpha_s': q*q/(4000000*a),
}
squares = {
 'sqrt_scaling_d_1400s_mm': d*d*s/t,
 'sqrt_scaling_from_58mm_1400s_d_3600s_mm': q*q*t/s,
 'hypothetical_d_2sqrt_alpha_t_at_1400s_mm': 4000000*ap*s,
 'hypothetical_d_2sqrt_alpha_t_at_3600s_mm': 4000000*ap*t,
}
assert set(r['derived_values']) == set(expected) | set(squares)
for name, truth in expected.items():
    value = F(r['derived_values'][name])
    assert abs(value-truth)/max(abs(truth),F(1)) < F(1,10**47)
for name, truth in squares.items():
    value = F(r['derived_values'][name])
    assert value > 0
    assert abs(value*value-truth)/max(abs(truth),F(1)) < F(1,10**47)
```

The eight pre-comparison oracle assertions checked a diffusivity known
answer, exact squared-depth scaling, inverse, ratio invariance, squared
mm-to-m conversion, the factor-four convention, the exact negative
ordering product, and positive/constant ordering. Inputs were checked
against the 10 strings independently transcribed from the root freeze.
The captured tool output reports all these checks passing, the maximum
normalized residual, the two distinct time ratios, and seven unchanged
input/runtime hashes. No standalone oracle file or result artifact was
created in this bounded assignment.

## Pins at review

All SHA256 values below were freshly checked. The PDF was byte-hashed only;
no full-page interpretation or independent source/render authenticity is
claimed. Python executable size was 33,816 bytes, producer script 6,858
bytes, source PDF 195,207 bytes; each equals the JSON identity record.

| Artifact | SHA256 |
|---|---|
| PROTOCOL.md | d02efad11d2008aa65536547510d78110daae974693d4291d6c07c359573db05 |
| SCOPE-EXPANSION.md | 063d4c02ca135382ebab6c71ce3b005f29ba946acd5f16f59d2d7b85bae6f147 |
| calculate.py | 61c28ab16f55a2c9ba1003ea57ccc089f8c6f3bf5c26ed5fc26403fa58c6dbf7 |
| calculation02.json | f27147daca48b0b99c69d6cf025d9eb670925f1d9c15911b5d8277b7fb25e8f8 |
| root-notes.md | d85fc9a3767a009abf1642205fe6cad5a921bfd5273ecc976fd44560db7d32b1 |
| Main held fletcher-santander-2007-draft.pdf | 30de182736b632772a9d42b6178eea234ab60c54d7c8bd715bcccb72c637e007 |
| /Users/admin/.pyenv/versions/3.13.7/bin/python3 | 7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e |

No raw/main/other unit file, observer freeze, legal/canonical record or
accepted engine state was changed. Bounded arithmetic acceptance is not
whole-unit scientific acceptance or completion of the investigation.
