# Human review of the conditional graph mappings

Prepared October 8, 2026. **No responses have been supplied for this packet.**
This is a local graphical check of a published connection benchmark, not an
opinion about the collapse or an acceptance of either model.

Viewer: [127.0.0.1:61594](http://127.0.0.1:61594/).
This is a loopback server for this session, not a permanent hosted link. If it
stops, ask for it to be restarted. The preserved packet and scripts remain
available; the server never saves your browser-session notes.

Packet SHA256:
`cb0f9da2f36e384eeeb046528696bba4f379fc8419f393a18ae2f809b05829cc`.
All 42 paired slots / 84 spring-and-shell entries remain listed. The CE prefix
distinguishes this conditional sample from the original accepted-support
sample, which remains uncreated. Axes/legend confirmation need not be repeated.

## What to inspect

1. Select a CE slot. F is force, E is dissipated energy; the number is the bolt
   count. The viewer names its trace color. Solid is spring; dashed is shell.
2. For each model, inspect the primary and peer source-strip proposals. Open
   the complete original page for context. Toggle the outlines off if they
   hide the ink. Zoom changes display size, not source precision.
3. Ask whether the outlined region plausibly belongs to that named trace, or
   instead contains a crossing, different curve, gap, unreadable edge or other
   ambiguity. You are not asked to verify hidden subpixel curves or engineering
   accuracy. A proposed label is not something you must agree with.
4. Record which proposals you actually inspected: primary, peer or both.
   Choose agreement, correction, unreadable or unresolved, and describe the
   cue. For corrections, give the Im source name and native x/y range.
5. Copy the inspection table into chat before closing/reloading. You may send
   a partial review; leave everything you did not inspect uninspected.

Native coordinates start at the upper-left cell (0,0). A rectangle
`[x0,y0,x1,y1]` uses outer cell edges: the included pixel indices end at
`x1−1,y1−1`. The purple target line can fall between pixel centers. Hover or
click gives native pixel indices; arrows move one native pixel and Escape
clears the lock. A click never fills a human response automatically.

The ten boundary slots are F4Q1–Q3, F8Q1–Q3, E3Q1–Q3 and E8Q2, all with
the CE prefix. You can assess their nearby graphical mapping, but correct
location alone cannot establish the excluded boundary value. All three F7
slots are unavailable in the primary paired coverage: **do not invent points**.

Synthetic TEST-ONLY is a coordinate/control demonstration, never evidence.
Software tests left all 84 real entries uninspected. See [report](report.md)
and [verification](validation.md) for the limits and independent checks.

## Restart command

From this directory, using the bundled runtime:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B serve_review.py --port 61594
```

If that port is occupied, omit `--port` and use the URL actually printed.
Do not bind to a public interface or substitute a general repository server.
