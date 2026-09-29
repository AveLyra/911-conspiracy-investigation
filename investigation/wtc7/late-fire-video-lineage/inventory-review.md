# Bounded local media and lineage inventory

2026-09-16. Research only. This pass identifies preserved bytes and their metadata; it does not establish any match to NCSTAR 1-9 Figures 5-157/5-158, recording continuity, original camera timing, or physical cause.

All **19 selected local media paths** match both their previously recorded SHA-256 and byte size. They comprise **13 distinct byte sequences**, including one incomplete transfer and two comparator streams. There are no selected paths without metadata and no expected selected-media paths missing. The separate lab-kit ZIP also matches its recorded 172,774,879 bytes and SHA-256. The two Camera 3 duplicate groups have four paths each; repeated packaging and reproduction paths add no independent source.

## Coverage and method

The source files remain in `/Users/admin/docs/911`. Authored outputs reside only in this investigation worktree. [Machine-readable inventory](local-media-inventory.json) contains every selected path, actual/expected size and hash, provenance pointer, disposition, inherited encoding metadata, duplicate membership, excluded fixture path, and inventory-only archive lead. [Inventory script](inventory_local_media.py) reproduces the file accounting and hash checks without decoding, probing, network requests, or archive extraction:

```sh
python3 research/sherlock-wtc7-investigation/late-fire-video-lineage/inventory_local_media.py --main-root /Users/admin/docs/911
```

The script emits JSON to standard output and never modifies source files. File metadata is inherited from the declared acquisition/kit records, not freshly measured media timing. Streaming hashes use Python's SHA-256; all selected files also retained the same size, mtime and inode before/after hashing. The manifest and `SHA256SUMS` agree on all nine media-manifest hashes.

Filename enumeration used `rg --files --hidden --no-ignore` with media suffixes `.mp4`, `.wmv`, `.mov`, `.webm`, `.m4a`, `.mkv`, `.avi`, `.mpg`, and `.mpeg`, excluding `held-uninspected` and `confidential` descendants. Exact scanned roots:

| Source-root-relative path | Media paths enumerated | Accounting |
|---|---:|---|
| `research/wtc7-video-comparison/media` | 9 | Six WTC7 video files; one separate montage soundtrack; two comparator streams |
| `research/sherlock-wtc7-investigation/fire-originals` | 8 | Complete and incomplete Peskin transfers; six excluded synthetic fixtures |
| `research/sherlock-wtc7-investigation/camera3-provenance` | 8 | Eight extracted/reproduction paths for two Camera 3 encodings |
| `research/sherlock-wtc7-investigation/camera3-recording-comparison` | 3 | Three excluded synthetic diagnostic fixtures |

The Camera 3 expansion followed explicit links in the preserved media provenance notes; this was not a repository-wide media search. Existing saved `outer-entries.json` additionally supplied inventory-only archive member names and hashes. No new archive extraction or member-level rehash was performed for those unextracted items. Their hashes remain inherited pins; fresh ZIP integrity alone is not a fresh verification of each member's recorded hash.

Control/navigation reads were `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, `research/WORKTREES.md`, and the repository/source-of-truth/evidence skills. Provenance reads were the media README/acquisition manifest/checksums and source-manifest; fire-originals README and sanitized Peskin protocol/report/source-review/validation; Camera 3 README, kit-inspection, recording-comparison README/protocol; selected kit receipts/member inventories. Existing prose findings encountered in those notes were not adopted as new visual findings.

Excluded from inspection: personal/litigation/confidential packets, held-uninspected areas, raw HTTP headers and process logs, platform `.info.json` bodies and ephemeral media URLs, synthetic fixture contents, arbitrary repository directories, and original bytes of inventory-only archive members. No new media download, browser request, audio listening, video decode, frame inspection, or image interpretation occurred.

## Source-family accounting and target leads

The complete preserved WTC7 material has **nine distinct video encodings and one separate audio encoding** across seven catalog families: Camera 2, Camera 3, Camera 4, CNN archive segment, BBC archive segment, 27-angle montage, and joined Peskin copy. These seven labels are accounting groups, not an established count of independent original recordings. The Camera 3 WMV remains source bytes with a prior decode exclusion; this inventory does not readmit it to matching.

| Metadata-defined family | Preserved extent from existing metadata | Relevance ceiling for late-fire source discovery |
|---|---|---|
| Camera 2 CBS converted MOV | 268.335002 s; 208,810,910 bytes | Longest named single-camera access clip in the initial media directory; CBS/converted label alone does not identify target footage |
| Camera 3 old MP4 and kit MP4/WMV | Old 15.464467 s; kit video 29.533268/29.501 s | Three encoded files in an already-studied shared recording family; eight kit paths are only packaging/reproduction copies |
| Camera 4 MP4 | 47.949206 s; 1,341,523 bytes | Short access clip; target relationship unknown from metadata |
| CNN/BBC archive segments | 2501.935267/2501.901902 s | Broadcaster archive access segments; filenames supply labeled program windows, not proof of a shot or original clock |
| 27-angle montage MP4/M4A | 781.3/781.374694 s | Edited compilation and separate soundtrack of the same upload; no 27-source independence claim |
| Peskin complete joined WebM | 2967.201 s; 696,711,067 bytes | Joined source family already linked to earlier report figures; no match to Figures 5-157/5-158 follows |

The incomplete 432,152,249-byte Peskin transfer is an exact prefix of the completed file, confirmed by a fresh prefix hash. It is excluded as a separate source and as an analytical input.

Five unextracted WTC7 lab-kit members represent three inherited unique hashes: `DistantViewWTC7.mp4` appears twice, `DistantViewWTC7.avi` once, and `TiltedCameraWTC7Clip.mp4` twice. Their statuses remain `inventory_only`; neither content nor independence has been established here. Six other archive media members are WTC1/comparator material and are excluded from the target search. See the JSON for exact archive entry names, sizes, inherited hashes and indices.

No selected filename or inventory-only WTC7 member name identifies **Fox**, **Figure 5-157**, or **Figure 5-158**. This filename result cannot establish absence of the sought footage inside a broadcast, compilation, or misleadingly named clip. A target-shot decision requires the separately declared source/visual investigation. No file was promoted to the legal record, authenticated as an original, edited, deleted, exported, or sent by this inventory.

## Verification and limits

The reproducible accounting is **19/19 matching media hashes and sizes; 1/1 matching packaging ZIP; 0 unmatched media-metadata paths; 2 exact duplicate groups; 1 verified partial/full prefix relationship; 9 excluded synthetic fixture paths**. A fresh run of the saved script reproduced the saved inventory JSON exactly. This is same-code repeatability, not independent historical verification. Main-repository `git status --short` remained empty after the inventory. Existing investigation-worktree changes were preserved.

A hash match establishes current byte identity to the recorded pin. It does not establish provenance before acquisition, that metadata is accurate, independence of recordings, historical completeness, or correspondence to a report figure. The evidence-audit and source-of-truth rules therefore kept file identity, inherited source labels, and target-shot inference separate.
