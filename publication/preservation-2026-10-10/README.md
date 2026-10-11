# Research preservation, October 10, 2026

This export preserves later research working states before redundant local
checkouts are removed. It consolidates the published model-comparison,
released-file discrepancy, Sherlock technical-feedback, and Wayback capture
branches, and adds subsequent source captures, analyses, draft designs,
reviews, and recorded runs.

## Entry points

- [WTC 7 status and limits](../../investigation/wtc7/STATUS.md)
- [Sherlock feedback requirements](../../investigation/wtc7/feedback-technical-record-2026-10-09/README.md)
- [Feedback coverage audit](../../investigation/wtc7/feedback-completeness-audit-2026-10-09/README.md)
- [FBI van laboratory-release study](../../investigation/urban-moving-systems/fbi-van-lab-release-2026-10-06/README.md)
- [Faraday model-comparison drafts and reviews](../../research/faraday-wtc7-model-compare/README.md)
- [File-level preservation manifest](manifest.json)

## What the manifest checks

The manifest describes 52,079 exported file and symlink records. Source
working-file bytes and their public copies were checked against SHA-256 values
during preparation. Source commit pins refer to the source checkout's preserved
working snapshot where one was required; source Git history was not merged
into this public repository. Existing public history remains intact.

Thirty local absolute test-fixture links were relocated to portable targets
or neutral missing-target fixtures. When a prior public capture occupied the
same path as a directory, it was retained and the link variant was placed
alongside it with a dated suffix. The manifest records original link hashes,
published targets, and the transformations. Original links remain in the
private source snapshots.

Binary assets use Git LFS where specified by `.gitattributes`. The manifest
distinguishes ordinary source files from source files that were already LFS
pointers. Git/LFS representation and remote download availability are checked
separately before local cleanup; this note is not a claim that every historical
scientific result or reproduction has been rerun.

## Scope and omissions

These are unfinished research records. Their original protocols, reports,
independent reviews, failures, and limitations remain controlling. Copying a
model, capture, or draft does not authenticate the historical event it depicts,
validate the model for WTC 7, or establish a conspiracy or a collapse cause.

Private case-management material, correspondence, case-specific legal strategy,
and twelve internal chat delivery records remain in private storage. The
captured YouTube HTML containing embedded client-key material remains omitted;
its existing public source note preserves the original hash and size. Source
files were not redacted or overwritten to create this public export.

## Download without materializing every asset

For a small initial checkout:

```sh
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/AveLyra/911-conspiracy-investigation.git
```

Fetch the particular assets needed for a study using `git lfs pull --include`
with that study's paths. Avoid fetching all LFS assets into every new worktree.
