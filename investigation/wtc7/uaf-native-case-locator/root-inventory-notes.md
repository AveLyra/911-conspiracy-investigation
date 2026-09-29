# Root path inventory — frozen before admission findings

2026-09-20. Research-only local locator, not primary model inspection. The
earlier goal turn completed its five-observable comparison; this turn tests
the declared native-file dependency. No causal inference from local absence.

## Executed search

`rg --files -uuu -0 ROOT` ran separately for the four roots in
[path-inventory.json](path-inventory.json), with exit0 and empty diagnostics
for every root. No symbolic-link-follow option was supplied. Python sorted
each relative path list and computed its UTF-8 newline-separated SHA-256;
these are **path-list snapshot hashes**, not source-content hashes or a
claim that the mutable research trees will retain the same counts.

Selected coverage at that snapshot:

| Root | Enumerated paths | Native-suffix hits | Named archive hits |
|---|---:|---:|---:|
| Main authority | 47 | 0 | 0 |
| Main research | 10,117 | 0 | 1 |
| Main exhibits | 215 | 0 | 0 |
| Investigation worktree research | 22,452 | 0 | 0 |

Native suffix search, case-insensitive: `.sdb`, `.s2k`, `.sdbk`, `.s$k`.
Name search, case-insensitive basename: `uaf`, `hulsey`, `penthouse49`,
`sap2000`. Six synthetic suffix controls passed: four expected positives
including uppercase/backup variants, and negatives for a misleading
`.sdb.html` and unrelated Markdown name. These controls validate only the
suffix predicate, not recursive search completeness or file semantics.

The sole named archive candidate is main
`research/sherlock-wtc7-investigation/model-access-audit/sources/uaf-direct-download.zip`.
No archive members were inspected by root before this freeze. The admission
reader's procedural request reported a sole bounded README and prompted the
protocol's explicit in-memory-read clarification; its substantive findings
were not exchanged. There are20 archive-named paths across the declared main
roots, not20 authenticated archives. Unnamed/other archive payloads, proprietary
embedded files, other worktrees and directories were not searched. Zero native
suffix hits does not mean no relevant bytes anywhere.

## Existing locator evidence

Read main `authority/independent/uaf-wtc7-notes.md` completely; inspected only
the UAF-related lines and their immediate context in `authority/source-index.md`
(including lines191–197 and218). They point to a2019 draft, its mirror and the
UAF project page. They do not identify the March2020 Figures4.17–4.20 native
case, member hash or acceleration-function definition. The authority-tier
language is legal-use guidance, not evidence that an institution's physics
deserves a higher scientific weight. No links were opened.

The current STATUS's older model-access summary already warns that the valid
ZIP is a redirect wrapper and that the advertised repaired dataset is labeled
2019 draft, with final equivalence unresolved. It also preserves prior tool
safety rejections. This unit must not repackage that known access limit as a
new model deficiency or retry the route. Fresh local format checks can verify
which bytes we hold, not supply the absent scientific result.

Source pins:

- Main source-index.md:
  `c8f942aeda021e7390a3609fff7eab554b32e58041243ae59595f4ebffddde3a`.
- Main authority/independent/uaf-wtc7-notes.md:
  `e732fb5bac42a097a557f73e01523842f83584a3cc3348eb1d198d5bd81b3d7e`.
- path-inventory.json:
  `c0b576ccdbca05376e5445b72d4083932d9db8976852b845a6b60e9e6e54000b`.

Initial ignore-respecting navigation was replaced with the explicit inclusive
pass before a suffix-nonlocation conclusion. A combined path listing returned
exit2 because model-access-audit does not exist in the worktree; its main
directory was found, and the fixed roots above all enumerated successfully.
That missing counterpart is not missing evidence. No primary records, native
content, software or legal files were changed. Root has not yet read the
admission reader's note.
