# Independent acquisition-wrapper and failed-attempt review

September20,2026 UTC. Bounded working-research review under the unchanged
[protocol](PROTOCOL.md), [pre-execution controls](ACQUISITION-CONTROLS.md),
main AGENTS/WORKFLOW/START-HERE and the complete investigation charter.
Evidence-falsification, source-preservation and development-verification
instructions governed this review. No legal or accepted-engine authority
changed.

**The failed attempt's integrity record reconciles; media acquisition and
admission were not achieved.** The downloader returned exit1, not a timeout.
The destination contains only start.json, stdout.local.txt, stderr.local.txt
and receipt.json. There is no acquired media, source.info.json, partial-media
file or fragment in that destination. No visual measurement can follow from
these outputs.

This reviewer made no network request, ran no acquisition main function or
historical decoder, displayed no media, opened no excluded PDF, and made no
retry or alternative-source attempt. The only new project write is this note.
Raw diagnostics remain local; their embedded URLs and paths are not copied
into the diagnostic summary.

## Pre-execution review, corrections and actual test scope

The initial wrapper, SHA-256
`a14161bc9a79734e479c274762f3d246105a087a6b74ef7b9b46235dabed8022`,
was independently read before the historical invocation. Four concrete issues
were raised:

1. Ignoring configuration did not exclude inherited/system proxy routing or
   inherited Python import environment.
2. The pinned yt-dlp file was a Python launcher; the wrapper's own Python
   executable was not the downloader's actual shebang runtime or package.
3. Default automatic file fixups could alter the preserved downloaded copy.
4. Default unavailable-fragment skipping could shorten a fragmented edition
   rather than stop its retrieval.

The installed primary code was inspected locally, without a web lookup:
yt_dlp/options.py lines569–573,1017–1027,1749–1756; YoutubeDL.py
lines3537–3559 and4122–4135; and downloader/fragment.py lines432–437.
The options and implementation support explicit direct routing, warning-only
fixups and aborting unavailable fragments. No historical behavior is inferred
from these software defaults.

The repaired wrapper uses an explicit empty proxy, a declared minimal child
environment, disabled config/plugins/cache, `--fixup warn`,
`--abort-on-unavailable-fragments` and `--keep-fragments`. It pins the
launcher, actual downloader Python, separate wrapper Python, and all installed
yt_dlp Python source files before and after the attempted acquisition.
The launcher contents are **244 bytes**; an interim review message's approximate
230-byte description was corrected before acquisition and is not used here.

The first repaired version, SHA-256
`f681ed90144fdd04b6e2c28ad80cf01eb1e2f3690fed5e13c12cf394a0fcb095`,
incorrectly required nonexistent extractor/youtube.py. This reviewer's syntax
compilation succeeded, but the read-only required-member assertion failed.
The installed package instead has extractor/youtube/__init__.py and
extractor/youtube/_video.py. The blocker was reported before any historical
invocation; it was not an acquisition failure or evidence about the source.

The final wrapper, SHA-256
`50676c016235530b9b1373623224d97a7cf7b6fb8929ba9abcd60e9b83ef7526`,
was reread completely. This reviewer's fresh syntax compilation, exact hash,
actual shebang, corrected required-member checks,1111-file membership count,
and unchanged protocol/control pins passed. Acquisition01 did not yet exist
at that pre-execution check. The four substantive safeguards were confirmed
in code and scoped pre-execution review found no remaining blocker.

**Control execution attribution:** root reports initial harmless timeout,
nonzero-exit and existing-output-refusal controls passed, then reran controls
for the repaired version. Root's first final-control attempt preserved the
incorrect package-member failure. Root subsequently reported timeout/nonzero
and fresh-output refusal passes, and five installed synthetic match-filter
cases covering an admissible case, wrong ID, live item, excessive duration
and missing duration. An initial environment assertion rejected macOS's
runtime-added `__CF_USER_TEXT_ENCODING`; root reports a keys-only diagnosis
and corrected test passing with no proxy/PYTHONPATH/PYTHONHOME inheritance.
These subprocess/filter controls were **not independently executed by this
reviewer**. Their reported success is not substituted for the independent
code/pin checks above or a general all-failure-path certification.

No historical invocation used either superseded code version. That execution
chronology is supported by the reviewed final receipt and root's contemporaneous
reports, not reconstructed as a global audit of every host process.

## Independent final receipt, pin and membership checks

One read-only inline Python check (full recipe below) returned exit0:

- The receipt, start record and process argv agree on the requested public
  item83cFWPY07dI and fixed command. The receipt has process status
  `returned`, exit1, timeout allowance120s and no exception_class entry.
  Its started/finished timestamps differ by2.456083s. That is a recorded
  wrapper interval, not independently measured server time.
- Actual destination membership is exactly four regular files, without
  additional subdirectories. The receipt lists the other three products;
  it appropriately does not list its own subsequently written hash.
- All three product byte counts/hashes match. All six top-level pinned files
  and all1111 package Python source files match start, before, after and
  current bytes. Actual current *.py package membership exactly equals the
  declared set, including the corrected YouTube package files.
- The final wrapper, original protocol and prospective controls retain their
  pre-execution hashes. The recorded child-environment/version fields agree
  between start and receipt. The version strings are recorded values, not
  fresh independently executed runtime-version queries in this final pass.
- After the comparisons, all1121 captured paths were rehashed and remained
  unchanged:1111 package files, six pinned files, and four acquisition files.
- No source media or platform info-JSON exists in the destination. Therefore
  there is no acquired source-byte hash, returned format/codec/geometry,
  encoded clock, duration or original-camera identity to validate.

The receipt retains its literal provisional statement,
“unreviewed; process completion is not source admission.” This review supplies
the failed-acquisition disposition, not admission of a source.

| Preserved artifact | Bytes | SHA-256 |
|---|---:|---|
| acquisition01/start.json | 169273 | 0ec1977f9b4f70892ff9a25a1c25a4163c541fe25d3646d85120619064baddbc |
| acquisition01/stdout.local.txt | 354 | 25d3f68b0876e8fa9f2296a753c28cc626593f61dc639b8c59799a70b7775e44 |
| acquisition01/stderr.local.txt | 288 | d5e83101b059ebd80565cdbfb63b3105321a30a29eb10b535268537f69aa6787 |
| acquisition01/receipt.json | 338783 | 6afc285e32b57174c4ede633c6db768dcdb1539b7c4375eeea0f982dab986fb1 |
| acquire.py | 5255 | 50676c016235530b9b1373623224d97a7cf7b6fb8929ba9abcd60e9b83ef7526 |
| PROTOCOL.md | 7480 | 3499fbd932a56a64826f2c654e8641965b92fa8a38f5b0fd9df8eb8bd080faa2 |
| ACQUISITION-CONTROLS.md | 2249 | aca89883daa5bdac21dae4000536450bca48d42568f62a01138f79457e08adac |
| yt-dlp launcher | 244 | d6375f29058ce3bdd760e1d384e491a6dab454632bca7936dac045da1a6d93c1 |
| Wrapper Python executable | 33816 | 7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e |
| Downloader's actual shebang Python | 52640 | 62c1423a74bc0f3c044627a1a5c29e5b754ade3efd68e9ecf7db9ea981c5e591 |

The full1111-file manifest is preserved in start.json/receipt.json rather than
duplicated into another registry. This pin scope is not all transitive-library
or loaded-code attestation, an independent client implementation, or a proof
that every possible exceptional filesystem/process termination preserves a
complete final receipt.

## Complete diagnostic classification and inference ceiling

Every line was classified, with no remaining unknown line:

| Stream/category | Lines | Meaning within this attempt |
|---|---:|---|
| stdout: requested URL context | 1 | Extractor announced the requested public item, not authenticated returned media. |
| stdout: extractor fetch progress | 5 | Internal retrieval progress notices; not five independently verified HTTP transactions or successful source acquisitions. |
| stderr: skipped missing-URL / forced-SABR formats warning | 1 | Downloader reported that some formats lacked usable URLs and referenced SABR streaming. |
| stderr: page-reload error | 1 | Terminal extractor error reporting that the page needed reloading. |

The logs and receipt support **failure of this specific ordinary attempt using
the pinned installed client**. Old-client/platform incompatibility is a
plausible explanation, not an established root cause. Other transient,
extractor or platform-response issues have not been separated by a test.
The diagnostic does not establish that the public recording is absent,
permanently unavailable, behind authentication, concealed or historically
misidentified. No login/challenge circumvention or alternate client was used
by this reviewer; no additional route is authorized by this failure.

“One attempt” means the recorded single downloader invocation, not one HTTP
request. The logs themselves describe multiple internal fetch stages.
Directory membership alone cannot prove that no other process was ever run;
the one-invocation boundary also relies on root's execution record.

The acquisition path is closed under the declared one-attempt budget. The
proposed visual feature comparison remains **unperformed**, not a negative
feature finding or a successfully completed comparator measurement.
Documentary source-association work remains a separate evidence layer and
cannot supply the missing images.

## Actual command and scope of reproducibility

Fresh reads used cat/rg, selected receipt fields with jq, and shasum for the
declared method/code pins. A first attempt to read execution.md returned
ENOENT because it was not present then; no control success or absence of
evidence was inferred from that locator failure. The earlier initial combined
controls/skills return truncated; bounded rereads supplied the full selected
skills, charter and remaining navigation content before review.

The following exact final command performs no network request or write, imports
no acquisition module, opens no media and prints no raw diagnostic URL/path.
Its assertions classify every saved diagnostic line and fail on an unknown
category. It reads captured bytes for hash/JSON checks and rehashes all checked
paths before the final result.

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/admin/.pyenv/versions/3.13.7/bin/python3 -B - <<'PY'
from pathlib import Path
from datetime import datetime
from collections import Counter
import hashlib, json, re
N = Path('/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/comparator-hbi-motion')
A = N/'acquisition01'
P = Path('/opt/homebrew/Cellar/yt-dlp/2025.6.9/libexec/lib/python3.13/site-packages/yt_dlp')
seen = {}
def identity(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def capture(path, expected=None):
    path=Path(path)
    data=path.read_bytes()
    item=identity(data)
    if expected is not None:
        assert item==expected, ('identity mismatch', path.name)
    if path in seen:
        assert item==seen[path], ('changed during check',path.name)
    seen[path]=item
    return data
r=json.loads(capture(A/'receipt.json'))
s=json.loads(capture(A/'start.json'))
expected_names={'start.json','stdout.local.txt','stderr.local.txt','receipt.json'}
assert {p.name for p in A.iterdir()}==expected_names
assert all(p.is_file() for p in A.iterdir())
assert set(r['products'])==expected_names-{'receipt.json'}
for name,item in r['products'].items():
    capture(A/name,item)
assert r['pins_before']==r['pins_after']==s['pins_before']
assert r['pins_unchanged'] is True
assert len(r['pins_before']['files'])==6
assert len(r['pins_before']['yt_dlp_python_files'])==1111
for path,item in r['pins_before']['files'].items():
    capture(path,item)
actual_package={str(p.relative_to(P)) for p in P.rglob('*.py')}
assert actual_package==set(r['pins_before']['yt_dlp_python_files'])
assert {'version.py','extractor/youtube/__init__.py','extractor/youtube/_video.py'}<=actual_package
for rel,item in r['pins_before']['yt_dlp_python_files'].items():
    capture(P/rel,item)
assert seen[N/'acquire.py']['sha256']=='50676c016235530b9b1373623224d97a7cf7b6fb8929ba9abcd60e9b83ef7526'
assert seen[N/'PROTOCOL.md']['sha256']=='3499fbd932a56a64826f2c654e8641965b92fa8a38f5b0fd9df8eb8bd080faa2'
assert seen[N/'ACQUISITION-CONTROLS.md']['sha256']=='aca89883daa5bdac21dae4000536450bca48d42568f62a01138f79457e08adac'
assert r['argv']==s['argv']==r['process']['argv']
assert r['requested_id']==s['requested_id']=='83cFWPY07dI'
assert r['url']==s['url']=='https://www.youtube.com/watch?v=83cFWPY07dI'
assert r['argv'][-1]==r['url']
assert r['process']['status']=='returned' and r['process']['exit']==1
assert r['process']['timeout_seconds']==120
assert 'exception_class' not in r
assert r['admission']=='unreviewed; process completion is not source admission'
assert r['child_environment']==s['child_environment']=={
    'PATH':'/opt/homebrew/bin:/usr/bin:/bin','LANG':'C.UTF-8',
    'PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
assert r['tool_version']==s['tool_version']=='2025.06.09'
assert r['tool_python_version']==s['tool_python_version']=='3.13.9'
# These are recorded version strings, not independently executed runtime queries.
started=datetime.fromisoformat(r['started_utc'])
finished=datetime.fromisoformat(r['finished_utc'])
assert r['started_utc']==s['started_utc'] and 0 <= (finished-started).total_seconds() < 120
counts=Counter()
stdout_lines=capture(A/'stdout.local.txt').decode('utf-8').splitlines()
stderr_lines=capture(A/'stderr.local.txt').decode('utf-8').splitlines()
for line in stdout_lines:
    if line.startswith('[youtube] Extracting URL: '):
        assert line.split('Extracting URL: ',1)[1]==r['url']
        counts['stdout_requested_url_context']+=1
    elif re.fullmatch(r'\[youtube\] '+re.escape(r['requested_id'])+r': Downloading .+',line):
        counts['stdout_extractor_fetch_progress']+=1
    else:
        raise AssertionError('Unclassified stdout line; retained locally, not printed')
for line in stderr_lines:
    low=line.lower()
    if line.startswith('WARNING: [youtube] ') and 'sabr' in low and 'missing a url' in low and 'skipped' in low:
        counts['stderr_missing_url_forced_sabr_formats_warning']+=1
    elif line.startswith('ERROR: [youtube] ') and 'page needs to be reloaded' in low:
        counts['stderr_page_reload_error']+=1
    else:
        raise AssertionError('Unclassified stderr line; retained locally, not printed')
assert counts['stdout_requested_url_context']==1
assert counts['stderr_missing_url_forced_sabr_formats_warning']==1
assert counts['stderr_page_reload_error']==1
for path,before in seen.items():
    assert identity(path.read_bytes())==before, ('changed before final pass',path.name)
print(json.dumps({
    'verification':'PASS for failed-attempt integrity; media admission not achieved',
    'process_status':r['process']['status'],'process_exit':r['process']['exit'],
    'receipt_elapsed_seconds':(finished-started).total_seconds(),
    'actual_file_count':len(expected_names),'listed_products':len(r['products']),
    'source_media_files':0,'source_info_json_files':0,'top_level_pin_files':6,
    'package_python_files':len(actual_package),'all_captured_paths_unchanged':len(seen),
    'diagnostic_categories':dict(counts),'stdout_lines':len(stdout_lines),'stderr_lines':len(stderr_lines),
    'receipt':seen[A/'receipt.json'],'products':r['products'],
    'acquisition_invoked_by_reviewer':False,'media_decoder_invoked':False,'images_viewed':0
},sort_keys=True,indent=2))
PY
```

