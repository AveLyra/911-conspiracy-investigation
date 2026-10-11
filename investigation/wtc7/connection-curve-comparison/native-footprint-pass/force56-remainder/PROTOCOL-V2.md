# Source-width correction before any raw annotation

October 8, 2026. The v1 source-width assertion was wrong: Im1 and Im3 are
741 by88 RGB, not745 by88. Source hashes and target/context rectangles are
unchanged. `sips -g pixelWidth -g pixelHeight -g space` confirmed both complete
images (receipt a6d9a0). The first save01 and save02 attempts each failed before
saving any context with `Wrong source representation` (receipt320519, exit1).
V1's thirteen synthetic/context controls passed (535059); those controls did
not verify source dimensions. Neither failed save is scientific source reading.

The original protocol and runner remain intact as the failed configuration.
Use `read_context_v2.py` for controls, save01, save02 and show. It pins v1 and
this amendment, and checks741 by88. It invokes only the unchanged pin/module
helpers, not v1's historical main. Two-cell clipping at741 leaves both fixed
contexts exactly unchanged. V2 controls add a synthetic dimension rejection
and acceptance check. Original source bytes are never changed.

This amendment is declared before any new raw RGB block or annotation. Reader
roles, source selection, cell/status schema, full-coverage duties and exclusions
remain unchanged. Readers must include this amendment and both runner versions
in dependencies. No result is selected based on model fit or reader agreement.
