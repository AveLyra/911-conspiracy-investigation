# HBI client follow-up: documented compatibility, unexecuted acquisition

September 20, 2026 UTC. Research only. **The proposed newer client is
documentation-compatible with available runtimes, but no client or historical
video was acquired or executed.** An unsafe-open refusal ended the new
release-integrity retrieval route. It does not establish that the recording
is absent, concealed or incompatible with a current client.

## Primary software documentation

Root and a separate reader checked the official
[latest-release page](https://github.com/yt-dlp/yt-dlp/releases/latest), which
redirected to [2026.08.19](https://github.com/yt-dlp/yt-dlp/releases/tag/2026.08.19),
published August19. This is the then-returned stable release, not a guarantee
of present platform compatibility. No nightly/master release was selected.

The [release-tagged README](https://raw.githubusercontent.com/yt-dlp/yt-dlp/2026.08.19/README.md)
describes a platform-independent Python zipimport executable, supports
CPython3.10+ and documents SHA-256/SHA-512 checksums and GPG signatures.
It provides explicit runtime selection and remote-component prohibition;
the latter is not a general network sandbox. Its dependency section separates
full YouTube support from optional merging/postprocessing tools.

The official [EJS guide](https://github.com/yt-dlp/yt-dlp/wiki/EJS) says the
official zipapp bundles the EJS scripts and specifies Node22.0.0 minimum,
with explicit enabling. It describes only partial Node permission restrictions,
not complete isolation. This mutable wiki was checked at access time, not
represented as release-tagged source code. Ordinary player-format/signature
processing would not authorize bypassing login, anti-bot, DRM or access denial.

Root's local version/hash checks returned:

| Existing runtime | Version | SHA-256 |
|---|---|---|
| Python executable | 3.13.7 | 7d29600aa971dfd764a15b113d5964b1e74a18176a6b70cb31646d45e9e5018e |
| Node executable | 22.16.0 | a45751fbfe88440bebff63cd44814e4ed6deb642bc3e3c4a14c4f8ae0ed9e019 |

Version floors are met; this is not a successful client/platform test or full
dependency attestation. No new runtime/package was installed.

## Failure boundary and local-copy check

The separate reader's two exact official release-asset requests were:

- `https://github.com/yt-dlp/yt-dlp/releases/download/2026.08.19/SHA2-256SUMS`
- `https://github.com/yt-dlp/yt-dlp/releases/download/2026.08.19/SHA2-256SUMS.sig`

Both returned an Internal Error with a release-asset redirect described as
not safe to open, non-retryable. Root received that report before attempting
any asset acquisition. Neither reader retried, changed tools to fetch these
assets, or used another distribution as a workaround. Signed redirect details
were not copied into this report. The separate reader could read the tagged
public key but did not verify a checksum or signature. Its eight official
document-open operations included two section reopens; they were software
documentation requests, not media retrievals. Root separately opened the
release, tagged README and EJS guide and used four within-page finds.

The existing main media README records an earlier checksum-verified temporary
2026.08.19 client, SHA-256
`1fa6733c37ea6fb51c99ad8fe785e7b7e5f3246c9b980230329d4fb72ed8d4d6`.
A scoped text search found that statement but no executable locator. Three
candidate top-level temporary filenames did not exist; an `rg --files --hidden
--maxdepth 3 /private/tmp -g '*yt-dlp*'` inventory with dependency-directory
exclusions returned no names. These bounded checks do not establish absence
everywhere, delete anything or authorize a fresh download. No binary was
located and rehashed against the prior record.

## Disposition

The [prospective protocol](PROTOCOL.md) remains intact; its historical invocation
was **not reached**, not a failed second video download. No wrapper, source
metadata, frames, sounds or feature measurements were produced in this unit.
The prior failed acquisition remains untouched. Node's documented compatibility
cannot establish the cause of that older client's failure.

The next useful action is the [joint printed-table consistency test](../multipoint-joint-consistency/PROTOCOL.md)
with already-held records, not repeated release-asset attempts. HBI's visual comparison remains
pending a safely available verified client or an approved, authenticated source
copy. No WTC7 ranking or accepted/legal finding changes. The full charter and
Luna follow-through remain active; the unsafe route is not a whole-goal blocker.
