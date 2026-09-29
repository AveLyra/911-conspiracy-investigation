# 9/11 / WTC 7 Investigation Research

This standalone repository collects scientific and technical research on the
September 11 attacks, with an emphasis on World Trade Center 7. It is a
research archive, not a completed investigation, expert report, or finding of
cause. Individual reports state their own methods, provenance, limitations,
and validation status; do not treat inclusion here as endorsement or
independent confirmation.

## Layout

- `investigation/wtc7/` — the active WTC 7 investigation work, reports,
  protocols, source locators, data, and reproducibility artifacts.
- `research/` — related scientific synthesis, video comparison, reconstruction
  workbench, and source-review material.
- `faraday/` — the MIT-licensed Research Machine source snapshot used as the
  basis for Faraday-related integration work.

The WTC 7 integration notes and tests are under
`investigation/wtc7/sherlock-integration/`. They document an experimental
research bridge, not a completed Faraday scientific audit or a transfer of
case data.

## Provenance and limits

This is a copy, not a continuation of either source repository's Git history.
The WTC 7 material was copied from the research worktree at source commit
`2fab1389ba8529494dd206a948014cd41cbf97d2`, including its then-present working
changes. Faraday was copied from upstream commit
`8d87c078fae6dcbda1541c4979568d88aa1fb9ae`; its separate local, unpushed
Vindication Machine changes were not included.

The separate Luna case-management chat was excluded. Source media and
investigation materials are retained at the repository owner's direction.
LFS-managed assets are identified in `.gitattributes`. The captured YouTube
watch-page HTML is omitted because it contains embedded Google client-key
material; its original SHA-256 and size are retained in
`investigation/wtc7/release25-source-locator/sources/youtube-watch-source-note.md`.
Absolute symlink targets that pointed into the original local worktree were
relocated or replaced with path-neutral fixture targets; source files were not
modified.

Start with `investigation/wtc7/CHARTER.md` and `investigation/wtc7/STATUS.md`
for scope and current limitations. Preserve distinctions between source
observations, derived measurements, competing explanations, and causal claims.
