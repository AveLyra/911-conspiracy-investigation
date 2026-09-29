# Independent candidate axis and legend registration

2026-09-27. Reader: `/root/curve_source`. **Candidate registration, not accepted
measurement.** Prior-informed AI with an earlier source-reading/checker role;
not a human reviewer, licensed engineer, blind reader or independent historical
source. This note is frozen before reading root's new registration. Earlier
source meanings were known and the previously frozen independent reading was
reread; it has not been changed.

## Actual coverage and pins

Read completely: REGISTRATION-STAGE, PROTOCOL, NUMERICAL-PROTOCOL,
HUMAN-REVIEW-GATE, technical-preparation and source-reading-independent.
Actually viewed **one complete** `render01/page-076.png` using
`view_image(detail="original")`, forwarded with original detail. No crop,
new render, enhancement, trace extraction or curve-value measurement was made.
The file is 1700×2200 RGB, 200 dpi. Original detail was requested; this record
does not certify a one-screen-pixel-to-render-pixel display scale. The full
page, both plots, axes, labels, legends and captions were visible. Placements
below are unaided assessed candidates, not exact clicked coordinates.

Rehashed the held source and listed inputs; read both stored representation
inventories and compared all twelve image invocation names, IDs, dimensions,
CTMs, unclipped boxes, encoded byte counts and encoded hashes: exact agreement.
This rechecks saved geometry, not a fresh JPEG extraction or pixel decoding.
Source 26,952,697 bytes, SHA-256
`cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
Physical page76 = printed25; media/crop box [0,0,612,792] PDF points, rotation0.
Main AGENTS/WORKFLOW/START-HERE/CHARTER pins remain unchanged.

| File | SHA-256 |
|---|---|
| REGISTRATION-STAGE.md | 18e212edcf4950f370bd30119597b20f786015d61da03fe4aeb19b23125f004c |
| PROTOCOL.md | 1ec6fedc9110f9ef2001f69fd1e13ad3a316a904f057345af26a0118d3216e19 |
| NUMERICAL-PROTOCOL.md | e03c47c1945b9eb9fd0a040d757d5f5f66bf76791ced8944323d3c92d1120df3 |
| HUMAN-REVIEW-GATE.md | 2e6f34d2e2d6d423c440c8a56b4a3c4796429d59f4d0baf0cf03609341a271ee |
| technical-preparation.md | a4d820f468dd80932f4144048eba545e70129f994c4b93e0f02f6a7f88e54550 |
| source-reading-independent.md | ef0f6f29f921cd27694f58412749390b1dad678c3f595d84fcd99a0fc75a985a |
| render01/page-076.png | 0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6 |
| pypdf-representation01.json | 1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5 |
| representation-check01.json | 517d657d206e6ac5b955be53bde63d5fecd9bc7b6fa05c971d6e88d7f111834b |

## Coordinate convention and assessed plot bounds

Render coordinates are continuous distances from the **upper-left page edge**
in rendered-pixel units, x rightward and y downward. Pixel cell (i,j) occupies
[i,i+1]×[j,j+1]; its centre is (i+0.5,j+0.5). Table locations estimate axis-line
centres in this convention. They are not integer pixel-array claims.

For **every listed axis/tick coordinate**, use an assessed **±6 render-pixel**
interval in the relevant direction; for a tick's two-dimensional source box,
also use ±6 around its carrying axis. This is a deliberately stated subjective
placement enclosure from the complete-page view, **not a calibrated confidence
interval**, native-line-width estimate, fitted error model or guarantee of
coverage. It must be checked rather than silently tightened. It includes
neither historical-model uncertainty nor a validated JPEG-artifact bound.

| Panel | Candidate left x | Right x | Top y | Bottom y | Axis labels/ranges |
|---|---:|---:|---:|---:|---|
| F, Figure3-4 upper | 449 | 1294 | 224 | 829 | x Vertical Displacement (m),0–1.6; y Applied Vertical Load (MN),0–1.0 |
| E, Figure3-5 lower | 474 | 1297 | 1048 | 1669 | x Vertical Displacement (m),0–1.6; y Dissipated Energy (N-m),0–800,000 |

These rectangles refer to the plotted axis frame, not the enclosing JPEG
box, title/caption, labels or page. The upper and lower x-axes must have
**separate registration**: their left edges/spans differ visibly. No fitted
shared warp or shift is proposed.

### Major ticks, candidate line-centre coordinates

All positions carry ±6, as above. Positions come from this reading of the
visible tick pattern; regular spacing is a plausibility check, not independent
evidence of subpixel recovery.

| x axis value (m) | F render x | E render x |
|---|---:|---:|
| 0.0 | 449 | 474 |
| 0.2 | 555 | 577 |
| 0.4 | 660 | 680 |
| 0.6 | 766 | 783 |
| 0.8 | 872 | 886 |
| 1.0 | 978 | 988 |
| 1.2 | 1083 | 1091 |
| 1.4 | 1189 | 1194 |
| 1.6 | 1294 | 1297 |

| F y value (MN) | Render y | E y value (N-m) | Render y |
|---|---:|---|---:|
| 0.0 | 829 | 0 | 1669 |
| 0.2 | 708 | 100,000 | 1591 |
| 0.4 | 587 | 200,000 | 1514 |
| 0.6 | 466 | 300,000 | 1436 |
| 0.8 | 345 | 400,000 | 1359 |
| 1.0 | 224 | 500,000 | 1281 |
| — | — | 600,000 | 1203 |
| — | — | 700,000 | 1126 |
| — | — | 800,000 | 1048 |

The lower-panel upper label visibly carries the ×10³ multiplier; the
intermediate printed numbers100–700 are therefore thousands of N-m, not
100–700 N-m. Tick values are axis labels, **not sampled curve ordinates**.
Top/right ticks duplicate axes; this note registers bottom/left major values
rather than pretending independent readings of every minor tick.

## Legend, native overlays and identity

Both panels visibly state **solid = Spring Element Model; dashed = Shell
Element Model**. The captions' “shear model” term is not a third plotted
style. All seven intended pairs remain included:

| Bolt count | Visually readable nominal color |
|---|---|
| 3 | black/dark gray |
| 4 | yellow/gold |
| 5 | blue |
| 6 | red |
| 7 | green |
| 8 | cyan/light blue |
| 9 | purple |

These are color names read from the keys, not exact RGB classifier thresholds.
Dark axis strokes are not automatically the three-bolt curve.

Candidate broad legend regions, assessed for navigation/initial exclusion:
F bolt key x[1040,1160], y[310,470]; E bolt key x[575,695], y[1138,1302].
These broad boxes include whitespace and do not identify historical support
underneath the key. The native model-label areas are within the exact
white-paint rectangles below. Visible text is composited with the raster
strips; bare JPEG extraction cannot preserve all label semantics.

The saved PDF path inventory records these **white painted rectangles**:

| Region | PDF x interval | PDF y interval | Render x interval | Render y interval |
|---|---|---|---|---|
| F model-style block | [307.74,458.52] | [679.44,710.28] | [854.833,1273.667] | [227.000,312.667] |
| E model-style block | [171.00,321.78] | [379.92,410.82] | [475.000,893.833] | [1058.833,1144.667] |

Rounded render bounds are geometric conversions, not pixel-exact painted
coverage. Native text glyphs occupy these areas. Do not use underlying raster
geometry as proof that any hypothetical curve is visible beneath a white
overlay; treat these areas as masked unless composition is explicitly resolved.
The header's black painted rectangle is outside either plot.

The two recorded narrow clipping requests have render bounding boxes
approximately F x[987.000,999.333], y[237.000,259.833] and
E x[607.167,619.500], y[1068.833,1091.667]. These are **clip requests**, not
proven global masks or a claim that all raster support outside them is removed.
Their graphics-state scope and compositing matter. The existing inventories'
unclipped image boxes do not adjudicate visibility.

### Support rule, before any curve sample

Identity requires visible compatible color **and** locally readable style,
with a supported segment connection that does not cross a gap or unresolved
crossing. Never infer spring/shell from vertical order, expected capacity,
smoothness, bolt-count ranking or desired agreement. Color alone identifies
at most an intended bolt family, not its model style.

Crossings, overlap of same-color styles, indistinguishable dark axes,
white/native-text/key overprints, clipping and axis-merging tails are
ambiguous/missing support. A disappearing trace is not zero or failure.
**No bridging even ordinary dash gaps is admitted in this stage.** Two
resolved segments remain disjoint until an independently declared/tested
interpolation rule is accepted. Enlarging a numerical error bar does not
repair unknown identity. A human axis/legend check will not accept future
curve samples or a model discrepancy automatically.

## Per-strip geometry, not extra source precision

For all twelve saved CTMs, b=c=0, with PDF mapping
X=e+a*u/W and Y=f+d*(1-v/H), where (u,v) are upper-left **source pixel-cell edge**
coordinates. Thus u=0..W and v=0..H bound cells; integer row/column centres
would be u=i+0.5,v=j+0.5. Render-to-PDF is X=0.36*x,
Y=792−0.36*y. Inverse mapping uses each strip's own a,d,e,f,W,H.

| Resource/object | Native W×H | a | d | e | f |
|---|---|---:|---:|---:|---:|
| Im0/1770 | 741×88 | 355.5269928 | 42.2400055 | 128.3399963 | 677.7599945 |
| Im1/1771 | 741×88 | 355.5269928 | 42.2400055 | 128.3399963 | 635.5200043 |
| Im2/1774 | 741×88 | 355.5269928 | 42.2400055 | 128.3399963 | 593.2799988 |
| Im3/1775 | 741×88 | 355.5269928 | 42.2400055 | 128.3399963 | 551.0399933 |
| Im4/1776 | 741×88 | 355.5269928 | 42.2400055 | 128.3399963 | 508.8000031 |
| Im5/1777 | 741×88 | 355.5269928 | **41.9400024** | 128.3399963 | 466.8600006 |
| Im6/1778 | 745×92 | 357.7940063 | 44.1600037 | 127.1399994 | 379.3800049 |
| Im7/1779 | 745×92 | 357.7940063 | 44.1600037 | 127.1399994 | 335.2200012 |
| Im8/1780 | 745×92 | 357.7940063 | 44.1600037 | 127.1399994 | 291.0599976 |
| Im9/1781 | 745×92 | 357.7940063 | 44.1600037 | 127.1399994 | 246.8999939 |
| Im10/1772 | 745×92 | 357.7940063 | 44.1600037 | 127.1399994 | 202.7400055 |
| Im11/1773 | 745×92 | 357.7940063 | 44.1600037 | 127.1399994 | 158.5800018 |

One source pixel spans about1.33276 render pixels horizontally for Im0–5,
1.33406 for Im6–11; vertical spans are about1.33333 except **Im5=1.32386**.
No uniform stitched-strip transform is valid. A render cell maps to a source
**footprint**, not to a new source sample or exact solver output. Resampling,
JPEG loss and unknown original plotting precision are not recovered by
decimal coordinates or increasing display zoom.

The conversion below intersects every assessed tick box with **all**
unclipped strip boxes and retains each intersection. The E200,000-N-m tick
box crosses Im9/Im10: both appear, rather than assigning the whole interval
to one strip. Other intervals can also cross seams when later enlarged.
Fractional source-cell coordinates printed to two decimals are rounded
arithmetic descriptions of the assessed boxes, not claimed0.01-source-pixel
localization. Quantization/line-width/antialiasing calibration remains pending.

## Actual geometry-only calculation

Executed `python3 -B -`, standard library only, exit0. No pixel data,
curve samples, regressions, ordinate values or discrepancy metrics were
calculated. The exact command follows, using this reader's own stated
candidate positions; it does not read root's registration.

```sh
python3 -B - <<'PY'
from pathlib import Path
from hashlib import sha256
import json
C=Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison')
a=json.loads((C/'pypdf-representation01.json').read_text())['image_invocations']
def mapbox(xl,xh,yl,yh):
 out=[]
 for p in a:
  aa,b,c,d,e,f=p['ctm'];w,h=p['native_dimensions']
  assert b==c==0 and aa>0 and d>0
  rx0=e/.36;rx1=(e+aa)/.36;ry0=(792-f-d)/.36;ry1=(792-f)/.36
  if xh<rx0 or xl>rx1 or yh<ry0 or yl>ry1: continue
  u=[max(0,(.36*xl-e)*w/aa),min(w,(.36*xh-e)*w/aa)]
  v=[max(0,(f+d-792+.36*yl)*h/d),min(h,(f+d-792+.36*yh)*h/d)]
  out.append(p['name']+':u['+','.join(f'{n:.2f}' for n in u)+'] v['+','.join(f'{n:.2f}' for n in v)+']')
 return '; '.join(out) or 'no image bounding-box intersection'
for panel,xs,y0,ys,x0 in [
 ('F',[449,555,660,766,872,978,1083,1189,1294],829,[829,708,587,466,345,224],449),
 ('E',[474,577,680,783,886,988,1091,1194,1297],1669,[1669,1591,1514,1436,1359,1281,1203,1126,1048],474)
]:
 for n,x in enumerate(xs):
  print(panel+' X '+str(n/5),f'render x[{x-6},{x+6}] y[{y0-6},{y0+6}]',f'PDF X[{.36*(x-6):.2f},{.36*(x+6):.2f}] Y[{792-.36*(y0+6):.2f},{792-.36*(y0-6):.2f}]',mapbox(x-6,x+6,y0-6,y0+6))
 for n,y in enumerate(ys):
  label=n/5 if panel=='F' else n*100000
  print(panel+' Y '+str(label),f'render x[{x0-6},{x0+6}] y[{y-6},{y+6}]',f'PDF X[{.36*(x0-6):.2f},{.36*(x0+6):.2f}] Y[{792-.36*(y+6):.2f},{792-.36*(y-6):.2f}]',mapbox(x0-6,x0+6,y-6,y+6))
for rel,expected in {
 'AGENTS.md':'01e3fbd03120a2085520818cea0a843a8c6748b4c7bb8ef0e68547c634a963cc',
 'WORKFLOW.md':'17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a',
 'START-HERE.md':'30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72',
 'research/sherlock-wtc7-investigation/CHARTER.md':'54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd'
}.items():
 assert sha256((Path('/Users/admin/docs/911')/rel).read_bytes()).hexdigest()==expected
print('MAIN_CONTROL_PINS_PASS; GEOMETRY_CONVERSION_ONLY; NO_CURVE_SAMPLES')
PY
```

Exact stdout (rounded coordinate bounds only as declared above):

```text
F X 0.0 render x[443,455] y[823,835] PDF X[159.48,163.80] Y[491.40,495.72] Im5:u[64.90,73.91] v[27.44,36.51]
F X 0.2 render x[549,561] y[823,835] PDF X[197.64,201.96] Y[491.40,495.72] Im5:u[144.44,153.44] v[27.44,36.51]
F X 0.4 render x[654,666] y[823,835] PDF X[235.44,239.76] Y[491.40,495.72] Im5:u[223.22,232.22] v[27.44,36.51]
F X 0.6 render x[760,772] y[823,835] PDF X[273.60,277.92] Y[491.40,495.72] Im5:u[302.76,311.76] v[27.44,36.51]
F X 0.8 render x[866,878] y[823,835] PDF X[311.76,316.08] Y[491.40,495.72] Im5:u[382.29,391.29] v[27.44,36.51]
F X 1.0 render x[972,984] y[823,835] PDF X[349.92,354.24] Y[491.40,495.72] Im5:u[461.82,470.83] v[27.44,36.51]
F X 1.2 render x[1077,1089] y[823,835] PDF X[387.72,392.04] Y[491.40,495.72] Im5:u[540.61,549.61] v[27.44,36.51]
F X 1.4 render x[1183,1195] y[823,835] PDF X[425.88,430.20] Y[491.40,495.72] Im5:u[620.14,629.15] v[27.44,36.51]
F X 1.6 render x[1288,1300] y[823,835] PDF X[463.68,468.00] Y[491.40,495.72] Im5:u[698.93,707.93] v[27.44,36.51]
F Y 0.0 render x[443,455] y[823,835] PDF X[159.48,163.80] Y[491.40,495.72] Im5:u[64.90,73.91] v[27.44,36.51]
F Y 0.2 render x[443,455] y[702,714] PDF X[159.48,163.80] Y[534.96,539.28] Im4:u[64.90,73.91] v[24.50,33.50]
F Y 0.4 render x[443,455] y[581,593] PDF X[159.48,163.80] Y[578.52,582.84] Im3:u[64.90,73.91] v[21.75,30.75]
F Y 0.6 render x[443,455] y[460,472] PDF X[159.48,163.80] Y[622.08,626.40] Im2:u[64.90,73.91] v[19.00,28.00]
F Y 0.8 render x[443,455] y[339,351] PDF X[159.48,163.80] Y[665.64,669.96] Im1:u[64.90,73.91] v[16.25,25.25]
F Y 1.0 render x[443,455] y[218,230] PDF X[159.48,163.80] Y[709.20,713.52] Im0:u[64.90,73.91] v[13.50,22.50]
E X 0.0 render x[468,480] y[1663,1675] PDF X[168.48,172.80] Y[189.00,193.32] Im11:u[86.08,95.07] v[19.63,28.63]
E X 0.2 render x[571,583] y[1663,1675] PDF X[205.56,209.88] Y[189.00,193.32] Im11:u[163.29,172.28] v[19.63,28.63]
E X 0.4 render x[674,686] y[1663,1675] PDF X[242.64,246.96] Y[189.00,193.32] Im11:u[240.49,249.49] v[19.63,28.63]
E X 0.6 render x[777,789] y[1663,1675] PDF X[279.72,284.04] Y[189.00,193.32] Im11:u[317.70,326.70] v[19.63,28.63]
E X 0.8 render x[880,892] y[1663,1675] PDF X[316.80,321.12] Y[189.00,193.32] Im11:u[394.91,403.91] v[19.63,28.63]
E X 1.0 render x[982,994] y[1663,1675] PDF X[353.52,357.84] Y[189.00,193.32] Im11:u[471.37,480.36] v[19.63,28.63]
E X 1.2 render x[1085,1097] y[1663,1675] PDF X[390.60,394.92] Y[189.00,193.32] Im11:u[548.58,557.57] v[19.63,28.63]
E X 1.4 render x[1188,1200] y[1663,1675] PDF X[427.68,432.00] Y[189.00,193.32] Im11:u[625.79,634.78] v[19.63,28.63]
E X 1.6 render x[1291,1303] y[1663,1675] PDF X[464.76,469.08] Y[189.00,193.32] Im11:u[702.99,711.99] v[19.63,28.63]
E Y 0 render x[468,480] y[1663,1675] PDF X[168.48,172.80] Y[189.00,193.32] Im11:u[86.08,95.07] v[19.63,28.63]
E Y 100000 render x[468,480] y[1585,1597] PDF X[168.48,172.80] Y[217.08,221.40] Im10:u[86.08,95.07] v[53.13,62.13]
E Y 200000 render x[468,480] y[1508,1520] PDF X[168.48,172.80] Y[244.80,249.12] Im9:u[86.08,95.07] v[87.37,92.00]; Im10:u[86.08,95.07] v[0.00,4.38]
E Y 300000 render x[468,480] y[1430,1442] PDF X[168.48,172.80] Y[272.88,277.20] Im9:u[86.08,95.07] v[28.87,37.87]
E Y 400000 render x[468,480] y[1353,1365] PDF X[168.48,172.80] Y[300.60,304.92] Im8:u[86.08,95.07] v[63.12,72.12]
E Y 500000 render x[468,480] y[1275,1287] PDF X[168.48,172.80] Y[328.68,333.00] Im8:u[86.08,95.07] v[4.63,13.63]
E Y 600000 render x[468,480] y[1197,1209] PDF X[168.48,172.80] Y[356.76,361.08] Im7:u[86.08,95.07] v[38.13,47.13]
E Y 700000 render x[468,480] y[1120,1132] PDF X[168.48,172.80] Y[384.48,388.80] Im6:u[86.08,95.07] v[72.38,81.38]
E Y 800000 render x[468,480] y[1042,1054] PDF X[168.48,172.80] Y[412.56,416.88] Im6:u[86.08,95.07] v[13.88,22.88]
MAIN_CONTROL_PINS_PASS; GEOMETRY_CONVERSION_ONLY; NO_CURVE_SAMPLES
```

## What remains unfinished

These mapping candidates are ready for comparison and actual human
correction; they do not clear HUMAN-REVIEW-GATE or any historical numerical
stage. Human review should identify both panels' lower-left, lower-right and
upper-left axis intersections, check units/multiplier, solid/dashed identities,
the seven color assignments and any masking disagreement. A person need not
supply an engineering opinion. Later supported curve-to-coordinate samples,
their uncertainty controls and independent arithmetic are separate gates.

No root new registration, root curve results or other historical measurements
were read. No source was changed, new source acquired, solver run, matrix-save
permission inferred, accepted engine state created, or cause ranking made.

