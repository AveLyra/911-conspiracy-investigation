# Root candidate source registration, frozen before exchange

2026-09-27. Prior-informed AI, not actual human review. I viewed the complete
1700x2200 `render01/page-076.png` at requested original detail, with both plots,
captions, legends and footer. I read the existing source reading and both
representation receipts, but not the other new registration. No historical
curve ordinate or model-discrepancy metric was extracted.

Source PDF SHA-256: `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`.
Complete page PNG: `0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6`.
The twelve transforms/dimensions are the unchanged
`pypdf-representation01.json` (SHA-256
`1cbb52b2e12a3d2b13d1a2ac008aab091bf64dc57deaf5b646fd6098521992e5`).

## Render coordinates and assessed axis registration

Coordinates below are zero-based **page-render pixels**, not native embedded
JPEG pixels. Origin is upper-left. Each proposed endpoint coordinate has an
assessed inclusive +/-3-render-pixel placement range on each axis. This is
an intentionally conservative candidate registration allowance, not measured
coverage, a statistical confidence interval or a curve-tracing error bound.
The whole pixel-cell footprint must also be retained during conversion.

| Panel / anchor | Render x | Render y | Printed axis values |
|---|---:|---:|---|
| Force origin |449|829|x=0m, y=0MN|
| Force right-bottom |1294|829|x=1.6m, y=0MN|
| Force left-top |449|224|x=0m, y=1.0MN|
| Energy origin |473|1669|x=0m, y=0N-m|
| Energy right-bottom |1297|1669|x=1.6m, y=0N-m|
| Energy left-top |473|1048|x=0m, y=800,000N-m|

Major x labels in both panels are 0,0.2,...,1.6m. Force major y labels are
0,0.2,...,1.0MN; energy major labels are 0,100,...,800 with the displayed
10^3 multiplier applying to the scale. The approximate expected major x
centers from these endpoint registrations are force
449,554.625,660.25,765.875,871.5,977.125,1082.75,1188.375,1294 and energy
473,576,679,782,885,988,1091,1194,1297. These interior coordinates are
**linear-registration predictions**, not independently clicked tick readings.
Human/source checks must detect nonlinearity or a misassigned endpoint;
do not use linear interpolation itself as evidence of an accurate axis fit.

Axis-pixel sanity check only: in visually selected narrow border strips,
RGB max<170 and max-min<25 was counted, without inspecting curve ordinates.
Force left columns448/449 each had580 dark cells of580 sampled; right1293/1294
each580/580; top rows223-225 each820/820. Bottom828/829 had525/583 of820
(colored tails obscure portions). Energy left472-474 each595/595; right
1296/1297 had560/566 of595; top1047-1049 each794/794; bottom1668-1670 had
753/761/752 of794. These counts support the visible border locations, not
unique mathematical centerlines or a physical calibration. Original image
and all pixels remain unchanged.

## Coordinate conversion and source-resolution ceiling

The page media box is612x792 PDF points, rotation0; the render is200dpi.
Render pixel cell(i,j) corresponds to X=[0.36i,0.36(i+1)] and
Y=[792-0.36(j+1),792-0.36j] PDF points, before any placement allowance.
For strip CTM[a,0,0,d,e,f] and dimensions(W,H), native edge coordinates are
u=W*(X-e)/a, v=H*(1-(Y-f)/d). A cell center is not an exact native sample.
Keep intersections with every strip; do not select one arbitrarily at seams.

Upper plot source x has741 cells at355.5269928points width: approximately
1.33276 render pixels per native x cell. Its first five strips have88 rows
at42.2400055points height; Im5 has88 rows at41.9400024points. Lower strips
have745x92 cells at357.7940063x44.1600037points. Their pitches are about
1.33406 and1.33333 rendered pixels per native cell. Thus neither enlarging
the view nor reporting fractional transformed coordinates creates new data.

Example force origin's render-cell center maps into Im5 to approximately
(u=69.7800,v=32.3548); force right-bottom maps to(703.8028,32.3548).
Force left-top maps into Im0 to(69.7800,18.3750). These are geometry examples
for axis anchors, not curve samples. All12 actual CTMs, including Im5, remain
the conversion authority; an assembled528-row upper image with a uniform
y scale would be wrong. Fractional coordinates are geometric values only.

## Published composition, labels and exclusions

Solid line = Spring Element Model; dashed = Shell Element Model. Bolt colors:
3black,4gold/yellow-orange,5blue,6red,7green,8cyan,9purple. This is a legend
assignment, not a claim that every colored fragment is uniquely identifiable.
The caption's word “shear” is not a third model. Both x axes are vertical
component displacement, not time. Force and energy must remain separate.

Conservative legend/context rectangles (render coordinates, inclusive):
force style labels x850-1280,y225-315; bolt key x1040-1160,y310-465;
energy style labels x470-900,y1055-1148; bolt key x575-695,y1138-1295.
These are exclusion/inspection regions, not fitted curve domains.

The representation receipt's white fills are explicit masks, PDF points:
force [307.74,679.44,458.52,710.28], energy [171,379.92,321.78,410.82].
On the page render their exact rectangular edges are approximately
force x854.833-1273.667,y227-312.667; energy x475-893.833,y1058.833-1144.667.
Retain those regions as unavailable for underlying curve recovery, plus
native text and legend ink. Recorded clipping rectangles lie inside these
label regions; no clipped pixels are treated as recovered visible evidence.
Clipping scope must follow PDF graphics-state order, not a page-wide mask.

No continuous curve identities/support are certified here. Crossings,
same-color near-overlap, dashed-versus-solid confusion, label coverage and
axis-merging tails are unresolved wherever they occur. Do not order colors by
height or extend a visible segment through an unseen segment. Initially do
not bridge ordinary dash gaps either. Later curve picks must encompass the
visible stroke and source quantization, with separately tested artifact and
horizontal uncertainty; these axis allowances cannot stand in for that work.

## Review target and limit

Ask the human to inspect both complete plots, the six axis-anchor mappings,
the scale/multiplier, model styles and bolt colors, reporting any unreadable
or mismatched item. Checking this page is not engineering certification or
agreement that either model matches an actual connection. Later selected
curve samples require their own human mapping spot-checks before consequential
metrics. This record alone does not close HUMAN-REVIEW-GATE.md.
