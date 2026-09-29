# WTC 7 video preservation notes

**Status:** Internal research preservation. The presence of a file here does not make it an authenticated or admissible exhibit and does not establish that it is complete, native, or unedited.

## Policy

Potentially relevant video should be preserved when technically obtainable. Copyright and licensing status are tracked as ownership and dissemination issues; they are not used here as a reason to omit relevant material from the internal case file.

The evidentiary work remains separate:

1. identify the recorder, broadcaster, agency custodian, and each transfer when possible;
2. compare the preserved copy with the highest-generation available source;
3. determine whether the file is complete, clipped, converted, stabilized, deinterlaced, or otherwise altered;
4. retain exact downloaded bytes and compute a cryptographic hash before analysis;
5. keep analysis derivatives in a separate directory and document every transformation; and
6. obtain testimony, certifications, production metadata, or other foundation needed for authentication before exhibit use.

## Current acquisition

`analysis-source/` contains the three files linked as reproduction materials for the Chandler/Walter/Szamboti multi-point motion analysis:

- `NIST Camera 2_CBS-Net Dub6 48 (Converted).mov`
- `NIST Camera 3.mp4`
- `NIST Camera 4.mp4`

These were downloaded on 2026-09-02 from the public Google Drive links supplied with that analysis. The naming and provenance matter: Camera 2 is expressly labeled **Converted**, and all three are secondary-hosted copies attributed to NIST camera footage. They are preserved for reproducibility and source comparison, not represented as original broadcast masters.

`broadcast-archive/` contains complete archive segments covering two pre-collapse reports:

- CNN, approximately 15:45-16:26 EDT; and
- BBC, approximately 16:54-17:36 EDT.

Both are 512 kb Internet Archive access derivatives, not broadcaster masters. Their downloaded bytes match the MD5 and SHA-1 values in the Internet Archive item metadata, and this repository separately records SHA-256 values. The broadcasts and exact file offsets are assessed in [`../collapse-warning-and-premature-reporting.md`](../collapse-warning-and-premature-reporting.md).

`compilations/` contains separate, unmuxed YouTube format streams for the 2024 upload “WTC Building 7 Collapse — 27 Angles.” The associated `.info.json` files retain platform metadata. The source is a 13-minute edited montage, not 27 continuous synchronized microphone records. Its audio findings and limitations are assessed in [`../27-angles-audio-audit.md`](../27-angles-audio-audit.md).

`comparators/explosive/` contains separate, unmuxed format streams for Astro95Media's Capital One/Hertz Tower recording. City of Lake Charles project material independently identifies that event as a planned implosion. The file remains a single, uncalibrated platform encode, so it is used only as a qualitative positive control.

The two YouTube acquisitions used `yt-dlp` 2026.08.19. Before use, the temporary downloader's SHA-256 (`1fa6733c37ea6fb51c99ad8fe785e7b7e5f3246c9b980230329d4fb72ed8d4d6`) was checked against the project's published release checksum. Format 136 and format 140 were retained separately to avoid a local remux or audio transcode. The associated `.info.json` files preserve the extractor metadata and ephemeral media URL returned at acquisition time.

File-level URLs, identifiers, formats, durations, dimensions, byte counts, and SHA-256 hashes are recorded in [`video-acquisition-manifest.csv`](video-acquisition-manifest.csv). The hashes are duplicated in [`SHA256SUMS`](SHA256SUMS) for direct verification. Local file modification times reflect acquisition, not September 11, 2001 capture time.

## Storage policy

The current media directory is approximately 683 MB. Repository-scoped Git LFS tracking covers MP4, MOV, and M4A files under this directory. Keep the acquisition manifest, checksum files, metadata JSON, and documentation in ordinary Git so the stored LFS objects remain independently identifiable. Verify `git lfs status` and object upload before treating a push as complete.

## Next acquisition priorities

1. The corresponding NIST-repository or agency-production copies of Cameras 2, 3, and 4, for hash and generation comparison.
2. The remaining NIST-selected camera files and their database metadata.
3. Highest-generation known-method comparator footage from official project owners or archives, plus multiple additional explosive and nonexplosive controls.
4. Native audio-bearing files with microphone/camera and location metadata.
5. The highest-generation CNN street-level clip containing the reported pre-collapse warning, together with the uncut lead-in, speaker identities, recording time, and camera location.
6. Contemporaneous CNN/BBC newsroom rundowns, assignment-desk logs, wire copy, corrections, and agency-to-media communications capable of identifying the source of the premature collapse reports.

Do not overwrite a preserved file. A new acquisition gets a new path and a new manifest row even if its title appears identical.
