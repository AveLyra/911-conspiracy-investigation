# Finite local fire-input locator

2026-09-24. Read-only locator under this unit's `PROTOCOL.md` and the main
CHARTER. This agent did not perform the root's Chapter 9 reading, window-pixel
review, or web queries. No source acquisition, archive expansion, source-body
execution, solver run, or fire/window measurement was performed.

**Result:** No matching native FDS deck, Smokeview file, or named
window-breakage/removal schedule was identified by the finite filename and
index searches below. There are substantial held **structural thermal-load
inputs**, which are not the same quantity as the missing FDS ventilation
schedule. This is not a finding that such schedules were never created,
withheld, globally unavailable, or absent from every held archive/body.

## Search coverage and reproducible commands

Whole-root **filenames only** were enumerated in these two authorized roots:

1. `/Users/admin/docs/911`
2. `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation`

`rg --files --hidden --no-ignore -g '!.git/**' ROOT` included ignored and
hidden filesystem paths, excluded Git directory contents, and did not follow
symlinked directories. No correspondence or legal-document bodies were read.
Archive interiors are not filesystem leaves. Initial line-delimited counts
were 11,444 main and 23,071 worktree filenames; a later pass found 23,072 in
the worktree during concurrent authorized work. These are snapshots, not
immutable repository totals or numbers of independent evidence objects.

Initial filename predicates were:

```regex
\.(fds|smv|sf|bf|s3d|q|sz|prt|end)\z
window.*(break|schedule)|breakage|fire.*input|fds.*input|smokeview
```

Both searches were case-insensitive. No candidate matched. A second pass
also allowed compressed suffixes and the broader `fds`, `smokeview`, `_hrr.`
and `_devc.` names; again no candidate matched. These are filename heuristics,
not file-signature or full-content classification. Alternate names and
extensionless bodies can evade them.

The final null-delimited snapshot, **2026-09-24 14:44:48 UTC**, used this exact
read-only Ruby command. Only counts/hashes were printed, not an unrelated
path dump:

```sh
ruby -rjson -ropen3 -rdigest -rtime -e 'roots=["/Users/admin/docs/911","/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation"]; roots.each do |root|; out,err,s=Open3.capture3("rg","--files","--hidden","--no-ignore","-0","-g","!.git/**",root); files=out.split("\0").sort; relative=files.map{|p|p.delete_prefix(root+"/")}; hits=files.select{|p|File.basename(p).match?(/\.(fds|smv|sf|bf|s3d|q|sz|prt|end)(\.(gz|bz2|zip))?\z|window.*(break|schedule)|breakage|fire.*input|fds|smokeview|_hrr\.|_devc\./i)}; puts JSON.pretty_generate({utc:Time.now.utc.iso8601,root:root,exit:s.exitstatus,stderr:err,filename_count:files.size,sorted_relative_nul_list_sha256:Digest::SHA256.hexdigest(relative.join("\0")+"\0"),candidate_count:hits.size}); end'
```

| Root | Filenames | Candidate count | Sorted relative null-delimited list SHA-256 |
|---|---:|---:|---|
| Main | 11,444 | 0 | `201b25fcca5870b8ec36a0f49cefc64e9ac0114a6c213d00a574011bb51a079c` |
| Investigation worktree | 23,072 | 0 | `3ea2b71ce26846d0f029202a3de8b3d562009500729fe3146aa819a02e46f035` |

Both final `rg` subprocesses exited 0 with empty stderr. The list itself was
not saved; the hashes identify the enumerated snapshots and do not provide a
recoverable filesystem inventory. Adding this note necessarily changes the
next worktree filename count. No search of other projects, homes, mounts,
remote storage, archive contents, or symlink targets was conducted.

## Existing index check and positive held sources

The existing June production manifest was read as index metadata, not as
permission to expand or inspect its archive members:

`/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv`

Current manifest SHA-256 matched the earlier audit pin:
`30234d45e528fd5590314b3be7b0cabb632560ab56f8bbfba88c9a564139badf`.
Its **25,643 metadata rows** have the following recorded extensions:
25,188 `.int`, 173 `.nod`, 272 `.png`, three `.apdl`, three `[no extension]`,
one `.pdf`, one `.zip`, one `.pptx`, and one `.ppt`. The expanded filename
predicate above found zero candidates in those rows. These are index rows;
they must not be added to filesystem counts or treated as a fresh archive
integrity check. No archive interior was newly opened in this locator.

Positive source locations:

| Held source | Current direct check | What it can and cannot supply |
|---|---|---|
| `/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539/ANSYS Thermal Data.zip` | Exists; 86,819,483 compressed bytes; SHA-256 `2fdb4a54008a00cfdf6d272044090139bd1ad8b0fe71e5b1c1ed3d76caa10181`, matching manifest row at physical CSV line 7 and prior audit. Only compressed file bytes were hashed. | Previously admitted thermal material. The prior full-body audit identifies ANSYS-compatible BF/BFE temperature loading; it is not thereby an FDS window-removal input. |
| Three APDL entries at physical CSV lines 3, 4, 5 of that exact manifest, rooted in the same June production directory | All three actual files exist and match their recorded sizes and hashes; details below. Their private/raw names are not recopied beyond the earlier engineering-minimization boundary. | Positive model-script holdings, not merely missing-file claims. The prior thermal-transfer audit did not establish an LS-DYNA temperature exporter or complete FDS-to-thermal derivation. |
| `/Users/admin/docs/911/exhibits/raw/SupplementaryResponse - DOC-NIST-2024-00023320260911014653/WTC7_CaseB_400pm.int.gz` / SRC-118 | Exact leaf is present among seven files in the user-named directory. No gzip body or new magnitude calculation performed in this locator. | Prior admitted audits identify nodal thermal assignments used by the released LS-DYNA deck. This is downstream structural loading, not a source-window schedule, heat-release history, or measurement of historical steel temperature. |
| `/Users/admin/docs/911/authority/nist/wtc7/ncstar-1-9.pdf` and existing source-input-review derivatives | Already held public report and prior source audit; root is independently inspecting the pilot's selected full pages. | Published method/figures and attributable window-state prose, not the exact implemented native schedule. |

The three selected APDL entries were verified without printing bodies,
comments, arbitrary argument strings, or embedded paths:

| Manifest CSV line | Bytes | Verified file SHA-256 |
|---|---:|---|
| 3 | 212,384 | `e79112addea5bd623c5a213de9d4e5c89725331309746f48d48a6505e7417f64` |
| 4 | 328,852 | `e96f23597454737ca3177d22e8cd857561b937658189b5d9e1b49ae5bdbdf8f9` |
| 5 | 165,093 | `bb07af3ff1537348f87a6ea95123d3620d588766d278649829c9f35247c33e5a` |

The actual verification command was:

```sh
ruby -rcsv -rjson -rdigest -e 'manifest="/Users/admin/docs/911/facts/production-reconciliation/production-2025-06-05-file-manifest-sha256.csv"; base="/Users/admin/docs/911/exhibits/raw/ResponsiveFiles for DOC-NIST-2024-000233 - Interi20250605122539"; rows=CSV.read(manifest,headers:true); selected=[]; rows.each_with_index do |r,i|; next unless r["extension"].to_s.downcase==".apdl" || r["filename"]=="ANSYS Thermal Data.zip"; p=File.join(base,r["relative_path"]); exist=File.file?(p); selected << {manifest_line:i+2,kind:r["extension"],filename_sha256:Digest::SHA256.hexdigest(r["filename"]),exists:exist,bytes:(exist ? File.size(p) : nil),expected_sha256:r["sha256"],actual_sha256:(exist ? Digest::SHA256.file(p).hexdigest : nil)}; end; puts JSON.pretty_generate({manifest:manifest,manifest_sha256:Digest::SHA256.file(manifest).hexdigest,rows:rows.size,selected:selected})'
```

It exited 0. Existing audit provenance, not a fresh body review, supplies the
role claims above: `thermal-transfer-crosswalk/report.md` and `PROTOCOL.md`,
`thermal-assignment-trace/report.md`, and main
`lsdyna-supplement-content-audit/report.md`. The older supplementary reminder
is explicitly a locator with later review links; it is not used to reinstate
the obsolete claim that the six input bodies remain wholly uninspected.

A separate metadata-only scan of main `intake/source-inventory.csv` searched
title/original-filename/notes for `\bFDS\b|Smokeview|window.?break|ANSYS Thermal Data`.
It matched two existing archive rows, SRC-084 and SRC-085 at physical CSV
lines 85 and 86. Only source ID/type/extension were emitted. No letter,
correspondence, or archive body was opened through that lead, and the match
alone was not classified as an FDS payload.

## Search failures and exclusions retained

- A first public-research content search was too broad and returned repeated
  synthetic fixture/charter text; output was truncated. It was not treated as
  evidence of source completeness. The finite filename and exact-index
  checks above replaced that search for this conclusion.
- An initial four-directory filename command included a nonexistent
  worktree `authority` directory and reported that error. Later whole-root
  enumerations succeeded; there is no claimed search coverage of that absent
  directory.
- Two guessed report/index paths did not exist:
  main `research/nist-supplementary-production-review-2026-09-11.md` and
  `research/sherlock-wtc7-investigation/SOURCE-INVENTORY.md`. Actual reports
  were found by `rg --files`, as cited above. The misses establish nothing
  about the underlying production.
- A narrow report-filename filter returned exit 1 with no match; it was a
  failed navigation aid, not a substantive absence check.
- No denied Dropbox item, approval-gated structural ZIP, architectural
  title-sheet image, held confidential packet, or archive-member payload was
  opened. No raw source was edited; no fresh sensitive transmission occurred.

## Same-observable comparison that remains possible

The pilot can preserve source-qualified glass-present/open/unresolved labels
for the specified windows, and conditional timing/order constraints, subject
to the separately frozen readers' actual visibility results. That is not yet
a model-input comparison. A matching native schedule would need the same
window identifiers and geometry, an explicit time origin, removal/opening
definition, interpolation rule, and actual prescribed state values. Then a
held-out visible-glass observation could test whether the modeled opening
preceded or followed the admissible observed interval. Shared imagery used
to prescribe the schedule would test transcription/consistency rather than
independent physical validation.

No such native schedule was identified by this locator. Therefore **zero
independent same-window model-state comparisons were completed here**. The
held ANSYS and LS-DYNA thermal assignments cannot be substituted for the
missing ventilation-state observable. This limitation does not establish
exaggerated fire severity, correct thermal exposure, fabricated modeling, or
any collapse mechanism.

## Correction: working-directory-sensitive Git exclusion — 2026-09-24

Root's replay exposed a real command-scope defect: the original
`-g '!.git/**'` did **not** consistently exclude Git metadata when an absolute
search root lay outside the command's working directory. The earlier blanket
description that this command excluded Git directory contents is therefore
superseded. The original observations, commands, and hashes above are preserved,
not silently rewritten. No source body or archive interior was involved.

At **14:59:55–14:59:56 UTC**, this agent ran both the original and corrected
command from each of the two root directories, against each root. All eight
subprocesses exited 0 with empty stderr and zero filename-predicate candidates:

| Working directory | Searched root | Original count / `.git`-component names | Corrected count / `.git`-component names |
|---|---|---:|---:|
| Main | Main | 11,444 / 0 | 11,444 / 0 |
| Main | Investigation worktree | 23,083 / 1 | 23,082 / 0 |
| Investigation worktree | Main | 18,698 / 7,254 | 11,444 / 0 |
| Investigation worktree | Investigation worktree | 23,083 / 1 | 23,082 / 0 |

The worktree's single `.git` name is its Git pointer file. The corrected
command explicitly excludes both Git directory contents and that pointer:

```sh
rg --files --hidden --no-ignore -0 -g '!**/.git/**' -g '!**/.git' ROOT
```

The existing case-insensitive candidate predicate is unchanged. The replay
asserted that **no returned root-relative path component equals `.git`** and
computed the same sorted, root-relative, null-terminated list hashes as before.
Both working directories produced identical corrected results for each root:

- Main, 11,444 names: `201b25fcca5870b8ec36a0f49cefc64e9ac0114a6c213d00a574011bb51a079c`.
- Investigation worktree, 23,082 names:
  `510ea038127c8ae2e98a4addc68d57a2224bf809f7fb436548d0800297493494`.

The original command's main-from-worktree hash was
`5a71be91ca76b5ea9c7a1d305969fa65abd162247445a77893b26b45f6bdc71c`;
its worktree hash from either working directory was
`018614c0cbaad4d58849ad031394f046d02afcc17946f0c11939fbb1b1468fbe`.
The extra 7,254 main names are exactly those with a `.git` component. The
worktree's growth since the earlier snapshot is separate from this defect.

The actual replay used `Open3.capture3` with `chdir:` explicitly set to each
root, the original/corrected glob arrays shown above, and this guard:

```ruby
git_count = relative.count { |p| p.split('/').include?('.git') }
raise 'corrected command admitted .git' if kind == 'corrected' && git_count != 0
```

This correction resolves the observed CWD-dependent scope difference, not
all possible search omissions. It does not convert a filename search into a
content or archive-interior search. The zero candidate result and positive
thermal-source findings remain unchanged; no native window schedule or
independent same-window model-state comparison was obtained.
