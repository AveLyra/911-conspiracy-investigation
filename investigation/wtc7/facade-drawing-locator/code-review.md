# Independent locator code review

2026-09-24; research-only. Reviewer: separate computational agent, not a
professional engineering review or a source-authentication authority. Read
main `AGENTS.md`, `WORKFLOW.md`, `START-HERE.md`, charter, this unit's
`PROTOCOL.md` and `IDENTIFIER-ADDENDUM.md`, and applicable evidence,
source-of-truth and development-verification skills before testing. No source
payloads, source archive contents, network, canonical files or implementation
edits were involved. This review concerns tool behavior, not WTC 7 physics.

## Material finding before repair

**The ZIP64 exclusion had a reproducible bypass.** A ZIP64 end record and
locator can coexist with nonsentinel legacy EOCD fields. Python's `ZipFile`
recognizes that locator and adopts the ZIP64 counts/size, but the producer
checked only legacy sentinel fields. A tiny valid synthetic fixture was
accepted as `members_listed_no_payload_read`. A second fixture declared a
64 MiB ZIP64 central directory while the guarded legacy directory was small;
the producer proceeded into `ZipFile`. The test intercepted that constructor
before a large read. This disproves the original broad resource-guard claim;
it does **not** establish that any real inspected archive used the bypass.

Reported to root before repair/conclusions. Suggested minimum correction:
before `ZipFile`, bounded-read the 20 bytes immediately before the actual
legacy EOCD and reject a `PK\x06\x07` ZIP64 locator even when legacy fields
are nonsentinel. An absolute offset is needed when the comment puts those
20 bytes outside the first tail window.

Tested original producer SHA-256:
`eff900720a56dbf026df8f9dcc60571803b7ece70f04ff1d8a4918279f64aa8d`
(8,698 bytes). Tested wrapper SHA-256:
`e77b6eff0b58ecb66e1b8914735abd8e4217978ddc92853766356ceffeccd116`
(2,185 bytes). Runtime: Python 3.13.7; ripgrep 15.2.0 on the local macOS host.

## Coverage and wording corrections

- The original unsupported-suffix set is exactly `.7z`, `.rar`, `.tar`,
  `.tgz`, `.gz`, `.bz2`, `.xz`. It omits `.iso`, `.zst`, `.lz4`, `.cab` and
  other possible containers. An archive-count statement means recognized
  suffixes, not all containers. The identifier search can independently hit
  an ISO filename without opening its filesystem.
- `rg --files` without `--follow` omits file symlinks as well as directory
  symlinks. The direct archive function rejects a supplied symlink, but this
  does not make the normal enumeration a symlink inventory. Symlink targets
  are outside this enumeration; do not count their absence as negative search.
- `pin(path)` reads every archive byte for hashing. Thus the legacy status
  `members_listed_no_payload_read` means no member payload **decoded or
  extracted**, not literally that compressed payload bytes were never read.
- The 100,000-entry safeguard checks the declared EOCD count before the
  standard library parses entries. A corrupt count is rejected afterward;
  this is not a hardened parser with an independent pre-allocation bound on
  actual central-directory entry count. Do not advertise adversarial archive
  security certification. Byte limits still bound a declared legitimate
  directory; hashed file reads are streamed.
- Initial path count is a file-name count, not substantive content coverage,
  unique sources, semantic completeness, or all versions. The whole locator
  unit is deliberately excluded, and archived/nested payloads are not recursively
  searched. Empty/nonmatching names can contain relevant drawings.
- Identifier predicates follow the declared patterns. They are candidate
  locators, not exact-record authentication: no left boundary is required,
  and FOIA/export-folder right boundaries exclude digits only. For example,
  `9120806_1247` and `FOIA_12-178x` match. This broadness can yield false positives
  but does not invalidate the requested negatives below. Resolve a match before
  using it as a source.
- Hashed path/member outputs, selected term labels, safe inventory IDs and
  field names avoid emitting raw notes/member names. Deterministic hashes are
  not encryption or permission for sensitive transmission. Filename exclusions
  do not automatically recognize every renamed alias of a gated packet.
- Output creation is refusal-on-existing at ordinary sequential invocation;
  simultaneous conflicting invocations are not a supported transaction model.
  Missing/unreadable paths or non-UTF-8 filenames may abort rather than silently
  certify full coverage. Stability asserts require normal, non-optimized Python.

## Synthetic checks actually executed

Command: `python3 -B -` with the inline harness described below. It imported
the two scripts without calling either CLI/main scan, generated only synthetic
fixtures in `tempfile.TemporaryDirectory(prefix='wtc7-locator-review-',
dir='/private/tmp')`, and removed that private temporary fixture directory on
exit. No source-root enumeration was run by this reviewer.

The corrected harness completed **32 assertions, exit 0**. The first attempt
failed because the reviewer used the EOCD offset index instead of the directory
size index in a fixture, not because of a producer regression. That failed
attempt was corrected and the entire suite rerun; it is not counted as a pass.

| Test(s) | Observed result |
|---|---|
| WTCI-000120-I.PDF; FOIA_12-178_NIST_WTC_Investigation_WTCI-120-I.iso_mount; wtci_120_i.pdf | All three match `wtci_120_i`. |
| WTCI-120-II.PDF; WTCI-120-I2.PDF | Both do not match. |
| NIST_FOIA_12-178_Jul_12_2012; FOIA12_178 | Both match `foia_12_178`. |
| FOIA_12-1780.zip | Does not match. |
| 120806_1247; 120806-1247/ | Both match export-folder predicate. |
| 120806_12470 | Does not match. |
| 9120806_1247; FOIA_12-178x | Both match: documented partial-token limits. |
| `.iso`, `.zst` membership in original OTHER_CONTAINERS | Both false. |
| Ordinary two-member deflated ZIP; patch `ZipFile.open` to throw if called | Metadata succeeds; 2 members; 1 term hit; 1 nested-container count; no raw fixture name in JSON. Five assertions. |
| Non-ZIP bytes | `no_bounded_eocd`. |
| Valid ZIP plus trailing bytes | `ambiguous_or_trailing_eocd`. |
| Nonzero EOCD disk | `multidisk_not_listed`. |
| Legacy directory-size sentinel 0xffffffff | `zip64_not_listed`. |
| Legacy directory size 32 MiB + 1 | `directory_cap`. |
| Fixture named NIST_WTC7_FOIA_11-209.zip | `prior_approval_boundary_not_opened`. |
| Direct archive call on file symlink | `symlink_not_opened`. |
| Sparse fixture of 1 GiB + 1 byte | `over_byte_cap`. |
| ZIP64 locator with nonsentinel legacy fields | Incorrectly accepted for member listing. |
| ZIP64 effective directory size, inspected through stdlib `_EndRecData` | 67,108,864 bytes despite small legacy value. |
| Same large-size ZIP64, intercepted `ZipFile` constructor | Constructor entered: guard bypass confirmed without allocating that directory. |
| Separate real.txt, symlink to it, and directory symlink; producer `listed` | Only real.txt returned. |

The ordinary fixture was generated with `ZipFile(..., 'w',
compression=ZIP_DEFLATED)` and two members:
`drawings/North-Elevation.txt` containing `synthetic fixture only`, and
`nested.zip` containing `not opened`. Names above are synthetic, not source
metadata. EOCD mutations use `struct.unpack('<4s4H2LH', ...)`, where index 5
is directory size, index 6 is its offset, indices 3/4 are the two counts.

### Standalone reproduction of the consequential ZIP64 finding

Use the preserved original producer matching the hash above for the
before-repair result. Replace only the `source` path if its preserved filename
differs. The post-repair expected result is `zip64_not_listed` and constructor
not entered, not acceptance. The fixture never requests or opens real sources.

```python
import importlib.util, io, pathlib, struct, tempfile, zipfile
from unittest.mock import patch

source = pathlib.Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/facade-drawing-locator/locate.py')
spec = importlib.util.spec_from_file_location('review_locator', source)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
b = io.BytesIO()
with zipfile.ZipFile(b, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('drawings/North-Elevation.txt', 'synthetic fixture only')
    z.writestr('nested.zip', b'not opened')
data = b.getvalue()
e = data.rfind(b'PK\x05\x06')
f = struct.unpack('<4s4H2LH', data[e:e+22])
locator = struct.pack('<4sLQL', b'PK\x06\x07', 0, e, 1)
with tempfile.TemporaryDirectory(prefix='wtc7-locator-review-', dir='/private/tmp') as d:
    p = pathlib.Path(d) / 'synthetic64.zip'
    normal = struct.pack('<4sQ2H2L4Q', b'PK\x06\x06', 44, 45, 45,
                         0, 0, f[3], f[4], f[5], f[6])
    p.write_bytes(data[:e] + normal + locator + data[e:])
    print(m.archive_metadata(p)['status'])
    oversized = struct.pack('<4sQ2H2L4Q', b'PK\x06\x06', 44, 45, 45,
                            0, 0, f[3], f[4], 64*1024**2, f[6])
    p.write_bytes(data[:e] + oversized + locator + data[e:])
    with p.open('rb') as stream:
        print(zipfile._EndRecData(stream)[zipfile._ECD_SIZE])
    entered = []
    def intercept(*args, **kwargs):
        entered.append(True)
        raise ValueError('synthetic stop before read')
    with patch.object(zipfile, 'ZipFile', side_effect=intercept):
        print(m.archive_metadata(p)['status'])
    print(entered)
```

## Acceptance ceiling

The original implementation is **not cleared** for its broad ZIP64 guard
claim. The predicate checks and ordinary metadata behavior passed within the
cases above; coverage claims require the listed limitations. A repaired script
requires its own pin and replay, including a maximum-comment ZIP64 fixture.
Root's real-source repeated runs and other reviewers' independent enumeration
are separate evidence; this review does not substitute for either, authenticate
the architectural collection, or establish the absence of a drawing.

## Repair replay — 2026-09-24

Root preserved original code in `source-v1/` and applied the absolute-offset
20-byte preceding-locator check documented in `GUARD-CORRECTION.md`. This
reviewer read that correction and the changed implementation, then reran the
complete original synthetic suite with corrected expectations, adding boundary
cases. **39 assertions passed, exit 0**, using `python3 -B -` and the same
fixture strategy; source hashes were checked before and after and were equal.

Revised producer SHA-256:
`d44c4c741cdf588d0f06c1f9849e12ed6f6ef2ae3c99039d34606f795675ef9d`
(9,301 bytes). Revised wrapper SHA-256:
`83ca0191e868ea419e9b3cdaaccb73656b201d399d47c0f9d2f46259f765b264`
(2,230 bytes). No implementation files were changed by this reviewer.

The replay retains every original test, with these changed expectations:

- `.iso` and `.zst` are now present in the explicit unsupported-format set.
- Nonsentinel ZIP64 now returns `zip64_not_listed`.
- The 64 MiB effective-size fixture no longer enters `ZipFile`; it also
  explicitly returns `zip64_not_listed`. The stdlib effective-size check still
  confirms that this is a consequential rejection, not an inert fixture.

Seven assertions distinguish the 39-test run from the earlier 32: the revised
oversized-fixture status assertion; three maximum-comment checks; declared
disk-entry mismatch; actual central-directory-entry mismatch; before/after
implementation-pin equality. The maximum-comment tests are:

1. Set legacy EOCD comment length to 65,535; append exactly that many ASCII
   `C` bytes, with the ordinary central directory unchanged: accepted for
   metadata listing.
2. Insert the nonsentinel ZIP64 end record and locator immediately before that
   long EOCD: `zip64_not_listed`.
3. Intercept `ZipFile` on the long-comment ZIP64 call: constructor not entered.

Reproduction extension for the standalone code above, inside its temporary
directory block:

```python
long_fields = list(f)
long_fields[7] = 65535
long_eocd = struct.pack('<4s4H2LH', *long_fields) + b'C' * 65535
p.write_bytes(data[:e] + long_eocd)
assert m.archive_metadata(p)['status'] == 'members_listed_no_payload_read'
p.write_bytes(data[:e] + normal + locator + long_eocd)
assert m.archive_metadata(p)['status'] == 'zip64_not_listed'
entered.clear()
with patch.object(zipfile, 'ZipFile', side_effect=intercept):
    assert m.archive_metadata(p)['status'] == 'zip64_not_listed'
assert entered == []
```

For the declared disk-entry mismatch fixture, set legacy EOCD index 3 to 3
while leaving index 4 at 2: `multidisk_not_listed`. For actual-count mismatch,
set both indices 3 and 4 to 1 while retaining both actual central entries:
`metadata_read_failed` after the standard-library parse. This confirms the
documented limitation's rejection behavior, not an allocation-security bound.

**Bounded disposition:** the found ZIP64 defect is repaired in the pinned
version and the regression/boundary cases passed. No residual issue found in
this review prevents using the finite known-input locator with the stated
limitations and a separate real-input metadata comparison. The review did not
inspect those real inputs itself and does not clear arbitrary hostile archives,
unrecognized container formats, renamed gated-source aliases, unobserved
symlink targets, source authenticity, or any physical inference.

## Preserved runnable harness

At root's request, the corrected inline harness was preserved as
`code-review-tests.py`, parameterized only to replay the original 32-case
behavior against `source-v1/` or the repaired 39-case behavior against current
producer files. New temporary fixtures remain confined to `/private/tmp`;
neither mode calls the producer's real-root `run()` or CLI. The original mode
expects the unsafe admission as a reproduced defect, not a safety pass. Both
modes also check unchanged source pins; in original mode that additional
stability assertion is outside the historical 32-case ledger.

Saved harness SHA-256:
`0b92b2d7ce2fe059b82f01c5c2687d068b27a48f85fc5ff80dba0a6664169d26`
(8,945 bytes). Both commands were then run from the saved file, exit 0:

```sh
python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/facade-drawing-locator/code-review-tests.py --source-version original
python3 -B /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/facade-drawing-locator/code-review-tests.py --source-version repaired
```

Output case counts were 32 and 39 respectively; original and repaired source
pins match those recorded above. This saved version preserves the corrected
EOCD indexing. It does not erase or include the initial failed harness attempt
as an additional success. The original/repaired runs are regression checks on
the same fixtures, not 71 independent source observations.
