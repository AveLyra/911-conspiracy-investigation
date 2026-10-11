# Version 2 extraction artifact review

2026-10-04 UTC. Reviewer `/root/stage2_audit`.

**Passed the bounded source/product consistency checks.** Both extractions
contain exactly indices 0–188, with identical frame records and received RGB
pixels. All nine prior pilot selections match their freshly extracted
counterparts. This establishes computational reproduction of the held source,
not historical source authentication, exact camera exposure, or human/scientific
acceptance. It says nothing about a collapse mechanism or the dense scores.

## Actual checks

Used two separate, stdout-only assertion scripts with
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -`.
Assertions were enabled; neither invocation used `-O`. The main check completed
with exit 0 (terminal 27980, final tool chunk `567a5c`); the exact log-difference
and outer-argument check completed with exit 0 (`f83710`).

Direct assertions checked the fixed source hash/23,621,148-byte size, complete
manifest and declaration copies, wrapper/parent identities, sampler/run
receipts, exact probe/decode arguments, successful statuses, saved FFmpeg and
FFprobe version records, complete probe inventory, and every index/PTS join.
PTS equals integer source index; time base is exactly 333673/10000000. All
frames retain 720×480, SAR 8:9, yuv411p probe format and bottom-field-first
interlaced metadata. These are encoded metadata, not an authenticated clock.

The configured, hash-verified sampler was reused **only** to reparse the
unaltered saved diagnostic streams and showinfo contract. Both probe streams
have zero diagnostic bytes. Both decode streams are clean with 189 frame and
189 color records, correct native geometry, PTS, SAR, field state and final
count. The auditor did not launch the sampler, FFmpeg, FFprobe or scoring.

Independent file/pixel loops verified **378 new PNG/RGB hash pairs**, plus
**nine pilot PNG/RGB pairs**: 387 in total. Both full 189-row manifests match
exactly. Pilot joins compare source indices and metadata/hashes, not output
PNG ordinals, which appropriately differ. All **460 dependency files** captured
by the audit had unchanged hashes at its end. Fresh root controls record the
14/22/25/9 passing groups; their inherited optimized-child limitation remains
as disclosed in that control record. The fresh supervisor record has 16 passes.

The raw decode logs are **not byte-identical**: each has 394 lines, with 383
unequal line pairs. An exact comparison classified 381 as runtime-address-only,
one as the declared output-directory change, and one as the final processing
throughput `fps= 84` versus `fps= 87`. No other differences were found. The
one-space formatting was checked as received; no saved log was normalized,
edited, or retrospectively admitted. Version 1's preserved receipt remains
`refused`, and no version-1 PNG entered these checks as a version-2 product.

## Execution records and limits

| Saved record | extract01 | extract02 |
| --- | ---: | ---: |
| Supervisor status / return code | completed / 0 | completed / 0 |
| Actual elapsed seconds | 4.568135750014335 | 4.646532000042498 |
| Actual extraction-directory bytes | 131095110 | 131095110 |
| Parent-lane bytes before terminal receipt | 265750599 | 396854760 |

Both request 240 seconds and 256 MiB with a 32-MiB reserve. Saved actual values
are below those thresholds; saved initial/final free space exceeds 4096 MiB.
Both end checks retain the parent dense directory as the cumulative lane and
report unchanged dependencies. These receipts and the reviewed monitor are
not an independent recording of every intermediate resource value or a hard
quota. Polling/shutdown limitations remain. Shell terminal IDs supplied by root
are not reconstructed from these files; the saved outer argument vectors were
checked independently.

## Selected artifact pins

| Artifact | SHA-256 |
| --- | --- |
| Version-2 PLAN | `e25d3568d8dbdd5f66d4d3004fb334d8eda2025cc3021860f64534d399902abe` |
| Version-2 manifest | `fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b` |
| Configured sampler wrapper | `62603c9ca8a8c5979b8faa00aacfe97a5361e289ae621f9b2c974c13d93084e4` |
| Sampler parent | `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d` |
| Root controls summary | `1f8e7edea24b1764851c5117ef6189b6c6690d29eb18bd57971da26313e4647d` |
| Both frame manifests | `224f41b92074b8b0c98dec6ec83e276da60a6af55c4907db0f308bb7c2bf7f90` |
| Both source receipts | `a918608d75dbf227f38a20e2395b5c7a30e9979c97cef2533c59b75e86a347d8` |
| Both probe stdout files | `51478357670208fac974078a2a453d1fbb23d144e05f567767e85745c1b431f5` |
| extract01 decode stderr | `d595de21a3e06a834b847d2d4b1f91596c41e3c3f4486fb6edd39cc7ada03e8e` |
| extract02 decode stderr | `41a67b421ad51497a0d73b4cbe70654ecb8a51bd883ac9db9cb2e680ef2a6ec1` |
| extract01 supervisor receipt | `3a6f8780ae4176664de2e473bd03f4bb101a9162021ec2925575ed302bd87a42` |
| extract02 supervisor receipt | `eef14ea69ddb031d4dfccf0e767b1646344a025977c4bb840d38912181c2ef95` |
| Both wrapper end checks | `ac70e31412c386ab67b1fd9cfddfc2fb05d9ce68a2dcdf48d1d4883704e5eb6a` |

Only this review was authored. No original, frozen code, prior receipt, image,
annotation or score was changed. PNGs were read computationally for byte/pixel
hash verification; no image was displayed, no visual judgment was made, and
no ranking or partial score output was accessed.
