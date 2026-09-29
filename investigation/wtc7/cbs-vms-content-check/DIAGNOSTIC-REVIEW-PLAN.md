# Diagnostic follow-up before image admission

The initial probe was clean. Both RGB checksum decodes completed with13
warning lines apiece: no accelerated yuv420p-to-rgb24 conversion. The actual
logs remain preserved; identical output does not remove the warning.

Before admitting images, inspect the exact installed-version FFmpeg source
at the upstream n7.1.1 libswscale/yuv2rgb.c tag for the warning and fallback.
Two browser reads (raw GitHub and GitHub file view) failed cache access, not
source absence. A single direct HTTPS retrieval of that public file is now
declared. No arbitrary warning suppression or generic allowlist is authorized.
If the source confirms a software fallback, classify only the exact warning
as a conversion-performance notice; retain colorimetry uncertainty. A new
full-stream native-yuv420p checksum pair, with no RGB conversion, must also
have empty warning-level stderr and matching PTS/count/pixels. Other diagnostics
still refuse admission. All original diagnostic files remain unchanged.

Source metadata: ASF, video stream1 (v:0), WMV1,320x240,yuv420p,
timebase1/1000;4531 decoded video frames, PTS33 through302602. SAR is not
specified, frames are marked progressive. Two encoded timestamp gaps exceed
the ordinary66/67ms cadence; do not interpolate them or assume a camera clock.
This review is computational access validation, not historical authentication.
