# Connection graphs: human source-mapping check

Research only. This is a location/label check, not an engineering opinion or
agreement with a collapse explanation. No human review is recorded yet.

## What to open

Current tested session: [open the local viewer](http://127.0.0.1:55918/).
It is not a permanent link; if unavailable, restart the server as below.

Use the local read-only connection review viewer and select **physical page76,
printed25**. It shows the complete source page, Figures3-4 and3-5. The server
address is session-local, not a permanent hosted link. Its launch command is:

```sh
python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/connection-curve-comparison/serve_review.py
```

Use the URL printed by that command. The full source is the preserved
[NCSTAR1-9A](/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9a.pdf).
Source SHA-256 `cde75ab6c5cadd972ef6fc9e1716bf6c9a50518bb31ad02f1b1b5d2b028bd5f4`;
page76 image SHA-256 `0835db6f0a138f5ddebfd6c4c81a857fda6e2da36379eeee1acbc3b5a9a6baf6`.

## Check these six axis anchors

The upper plot is force; the lower plot is energy. Coordinates are pixels in
the **1700x2200 rendered page**, not native graph-image pixels or screen pixels.
Table ranges are inclusive zero-based pixel-cell indices. Their continuous
page-edge footprint is [low,high+1] on each axis, not [low,high].
The proposed tolerance below is +/-3 rendered pixels in each direction. It is
an assessed registration allowance, not a statistical confidence interval.
These are root's navigational candidates. The separate reader used a broader
assessed +/-6-render-unit allowance and a continuous line-center convention;
both original records are preserved in the [comparison](registration-comparison.md).
Agreement between those readers has not narrowed either allowance.

| ID | Point to inspect | Proposed (x,y) | Proposed x range | Proposed y range |
|---|---|---|---|---|
| F0 | Upper plot: left-bottom axis intersection |(449,829)|446–452|826–832|
| FR | Upper plot: right-bottom axis intersection |(1294,829)|1291–1297|826–832|
| FT | Upper plot: left-top axis intersection |(449,224)|446–452|221–227|
| E0 | Lower plot: left-bottom axis intersection |(473,1669)|470–476|1666–1672|
| ER | Lower plot: right-bottom axis intersection |(1297,1669)|1294–1300|1666–1672|
| ET | Lower plot: left-top axis intersection |(473,1048)|470–476|1045–1051|

At100% or200% zoom, inspect the actual axis intersection, click to lock a
point, and use arrow keys for one-rendered-pixel adjustment if needed. Fit
mode helps locate the panel but can skip pixels. A proposed marker is an AI
suggestion, not your observation. Report a correction or a wider range if
appropriate; do not force a point into the suggested interval.
The optional jump buttons use `Fright/Ftop/Eright/Etop` for the table's
`FR/FT/ER/ET`; F0 andE0 are identical labels. Jumps bring the proposed point
into view but do not count as your own coordinate selection or agreement.

## Check the printed meanings

- Both horizontal axes: vertical displacement,0–1.6metres; major labels0.2apart.
- Upper vertical axis: applied vertical load,0–1.0MN.
- Lower vertical axis: dissipated energy,0–800x10^3N-m (800,000N-m).
- Solid line: spring element model. Dashed line: shell element model.
- Bolt colors:3black,4gold/yellow-orange,5blue,6red,7green,8cyan,9purple.

Please inspect both panels' labels and keys, not just this transcription.
White model-label areas, crossings and same-color overlaps can cover or
confuse traces; agreement with a legend does not identify every curve fragment.

## What to report

Name the anchors and labels you actually inspected. For each, report agreement
within the proposed range, a corrected point/range, or “unreadable.” You do
not need to certify numerical accuracy or decide which model is correct.
If all six anchors and both panels' labels were checked, a single statement
listing that coverage and any corrections is sufficient; no compulsory
wording or presumption of agreement applies.

This check concerns source axes/labels only. It does not transfer the prior
R1 approval, validate the models, or accept later historical curve measurements.
Before consequential comparison, selected curve-to-coordinate samples still
need attributable human spot-checks and tested treatment of linewidth,
JPEG artifacts, crossings and unsupported gaps. Nothing is saved or approved
by clicking in the viewer; your reply is the observation record.
