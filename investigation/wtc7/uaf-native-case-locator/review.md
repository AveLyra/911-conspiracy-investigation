# Independent inventory and inference review

2026-09-20. Research-only. Reviewed report SHA-256
`452800466be3c617f5ebf521aa45f37c202166689069f9f96c781595b0f2a8c9`.
No material correction required within the checked scope.

## Independent path verification

Used `/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B` with a separate
`os.walk(..., topdown=True, followlinks=False)` implementation. Each root was
asserted to be a nonsymlink directory. `lstat` classified entries; symlink
directories were pruned and all symlink names recorded without following them.
There was no ignore-file filtering. Source payloads were not opened.

| Exact root | Recorded regular-path count | Independent count | Directories visited | Symlinks recorded, not followed |
|---|---:|---:|---:|---:|
| `/Users/admin/docs/911/authority` | 47 | 47 | 13 | 0 |
| `/Users/admin/docs/911/research` | 10117 | 10117 | 830 | 3 |
| `/Users/admin/docs/911/exhibits` | 215 | 215 | 14 | 0 |
| `/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research` | 22452 | 22455 | 971 | 12 |

There were no traversal/lstat errors or special-file entries. The three main
symlinks were runtime Python links; the twelve worktree links were prior test
fixtures. They were additional recorded path metadata, not traversed payloads;
none matched either candidate predicate. No content was inspected in runtime
or fixture trees.

Case-insensitive terminal suffixes `.sdb`, `.s2k`, `.sdbk`, `.s$k` yielded zero
candidates. Basename substring tests for `uaf`, `hulsey`, `penthouse49`,
`sap2000` exactly reproduced all four recorded candidate arrays. Six separately
executed suffix controls passed: the four ordinary/uppercase/backup positives
and the `.sdb.html`/unrelated-Markdown negatives. These test the predicate, not
format authenticity or complete discovery of embedded/native data.

Sorted relative regular-file names, UTF-8 encoded with a final newline,
reproduced all three main-root snapshot hashes. The worktree's three extra
files were precisely this unit's `path-inventory.json`, `root-inventory-notes.md`
and `source-admission.md`; excluding only those names reproduced its recorded
snapshot hash exactly. This reconciles the observed count change, not a
requirement that mutable trees remain frozen or a claim about source-content
hashes. Later report/review/navigation writes can change those counts again.

A separate path-only archive-name pass used endings `.zip`, `.7z`, `.rar`,
`.tar`, `.tgz`, `.gz`, `.bz2`, `.xz`. Counts matched 0/5/15/0: main research had
three ZIP and two GZ names; exhibits had nine ZIP and six GZ names. The sole
name-qualified archive candidate was the recorded
`model-access-audit/sources/uaf-direct-download.zip` under main research.
No archive members were read. Both independent traversals exited 0.

## Text review and disposition

Read the complete protocol, inventory JSON, root inventory notes, frozen
source-admission note and result report. Current main controls/charter hashes
matched the previously fully read versions. Source-of-truth and
evidence-falsification skills were applied to keep local path facts, inherited
payload checks and scientific inference separate.

The report accurately describes the independent count/candidate checks above.
The admission reader's nine source pins, ZIP layout, CRC/member hash and HTML
interpretation are **inherited reported checks**, not repetitions by this
reviewer. Root's separately reported payload checks likewise were not rerun.
I inspected no payload, PDF, media, archive member or native-model content, and
performed no network access, solver execution or engine change.

The result does not upgrade the README wrapper into a model archive, a draft
dataset label into final-case equivalence, or local non-location into public
unavailability. It explicitly says the wrapper limitation was previously
known. Its new contribution is scoped inclusive path coverage and a precise
unresolved case/function dependency—not a new physical finding or reason to
favor NIST.

The smallest-record specification usefully separates function definition and
case assignments from derivation/calibration history. A fitted input and a
computed response can coexist. The named case, removal bands, point identity
and clocks are requested rather than guessed. Even recovery of those records
would not by itself reproduce the model or authenticate cause.

Further checks of the same wrapper or denied access route would be redundant
without materially new input. The report's stop is appropriate. The strongest
unexcluded alternative is that the uninspected larger archive contains the
needed final-equivalent case and provenance.

The proposed Q05 handoff is expressly based on another reader's bounded
notes-only check, not this review's corpus audit. I did not verify that search
or locate imagery. Its requirement to establish attribution and capture/cleanup
time before treating rubble as WTC7 debris is appropriate; no new measurement
or causal conclusion is claimed.

## Reviewed input pins

Checked with `shasum -a 256`; originals and frozen notes were not edited.

| File | SHA-256 |
|---|---|
| PROTOCOL.md | `eb4ed64dd84fef456b2e59562ac6b5aebe4cd7119d833686f39bc2d0490b93a7` |
| path-inventory.json | `c0b576ccdbca05376e5445b72d4083932d9db8976852b845a6b60e9e6e54000b` |
| root-inventory-notes.md | `e2767e54cc847e3eb06afa49e1e50660239af4122eeef4ff24ebb85b8e2c0ecd` |
| source-admission.md | `42a56da71c3579b689ddc6451083f5fa7b897eca97db666a1b8434f93579c76f` |
