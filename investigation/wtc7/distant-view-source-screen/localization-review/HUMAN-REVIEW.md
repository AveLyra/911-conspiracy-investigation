# DistantView six frame localization review

October 8, 2026. This is a new DistantView pilot, **not a repeat of the completed
R1 comparator review**. No historical coordinates are proposed or prefilled.
All six responses remain uninspected until you actually inspect and reply.

The local viewer is at <http://127.0.0.1:55462/>. It is a temporary localhost
server, not a permanent hosted link. If unavailable, ask for a restart; first
check whether the existing process is still alive. The [verification record](report.md)
documents the operating limits and restart command.

## What to inspect

Select frames **274, 300, 342, 365, 388 and 411**, one at a time. Look for the
junction of the dark target facade's outer **image-right top outline and
right-side outline**. Do not substitute the raised roof-step foot, bright
compression rim, plume, foreground roof or adjacent background building.
Image-right does not assign a compass direction or structural member.

Use **Fit for overview**. Use **100% or 200% and arrow-key refinement for final
endpoints**, checking both the displayed native coordinate and marker before
recording. A Fit-mode automated test intended for one cell landed in the
adjacent row; its cause remains unresolved. Zoom is not a guarantee of exact
targeting, and this is not a general one-pixel error bound. If precise selection
still seems unreliable, report **outside or display inadequate** instead of
forcing an answer.

For each frame, actually inspect the full image, check its inspection box,
choose a status, and give a short explanatory note:

- **Localizable:** supply an inclusive rectangle containing the junction
  positions you consider plausible from the adjoining contours.
- **Ambiguous:** explain competing positions or uncertain identity. A useful
  single region is optional; otherwise leave the box absent.
- **Obscured:** the target is hidden; no box.
- **Not located:** you cannot find it; no box. This does not assert physical absence.
- **Outside or display inadequate:** explain the specific display problem; no box.

Coordinates are zero-based native pixel cells: x is 0–703 and y is 0–479,
origin at the upper left. Box order is **xmin, ymin, xmax, ymax**, with both
ends included. Choose the upper-left endpoint first and lower-right second;
reversed endpoints are rejected. You can use two image clicks in New box mode,
or lock/nudge a point and use it as an endpoint. A one-cell box is allowed only
if it is your actual judgment. Do not adopt a default ±1 interval or call the
box a statistical confidence interval.

## Returning your observations

Click **Record session-only draft row** separately for each image. A point or
pending box alone records nothing. Switching images clears unrecorded inputs;
recorded rows remain only in browser memory. The synthetic practice image is
separate and never counts as a historical response.

Manually select and copy the read-only draft text into this chat, or give one
line per inspected frame with its status, box if applicable, and reason. Do
not reload before copying: there is no save, submission, upload, clipboard API
or persistent storage. A response sent in chat is not changed by later editing
the browser draft; send corrections separately.

These are subjective localization judgments, not a test of a collapse theory.
Six positive responses would not certify the remaining 132 frames, establish
a fixed material point, recover missing exposure timing, or authorize automated
historical tracking. The [frozen protocol](PROTOCOL.md) retains those separate gates.
