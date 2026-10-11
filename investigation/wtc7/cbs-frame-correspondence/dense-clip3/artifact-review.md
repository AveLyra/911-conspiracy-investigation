# Dense Clip 3 extraction: independent refusal audit

2026-10-04 UTC. Reviewer `/root/one_pixel_check`. The read-only audit reproduced
the recorded refusal. **`extract01` remains refused; there is no admitted dense
frame set or dense correspondence result.** No parser change, historical decode,
image opening/display, scoring or retry occurred during this review.

## Exact failure

The saved ffprobe and ffmpeg commands each exited **0**, with no launch error.
The unchanged sampler nevertheless refused its diagnostic gate. Independent
re-parsing of all **394 nonempty decode-log lines**, using the hash-pinned
original `decode_diagnostics`, reproduced the saved diagnostic object exactly:

- 393 accepted lines, including 189 `show_frame` and 189 `show_color` records;
- one rejected content line, **394**, classified `unparsed nonempty line`;
- one consequential cardinality failure: zero recognized `final_summary`
  records.

The rejected line is:

```text
[info] frame=  189 fps= 83 q=-0.0 Lsize=N/A time=00:00:00.00 bitrate=N/A speed=   0x    
```

The frozen final-summary expression requires `fps={NUMBER}` without whitespace
between `=` and the number; this line contains `fps= 83`. `83` itself matches
the existing number grammar. The absent *recognized* summary is therefore not
an independently absent log line: the final count line exists but was refused.
No whitespace was normalized, log rewritten, line suppressed or alternate
acceptance expression substituted.

No additional rejected content line or explicit warning/error/fatal/panic tag
was found in the saved decode stream. Probe stderr, decode stdout, both tool-
version stderr streams and supervisor stderr are empty. The supervisor's saved
stdout correctly reports the sampler's refusal. These are conclusions about
the preserved streams, not proof that the resulting image content is sound.

## What the independent check established

- The current complete source remains **23,621,148 bytes**, SHA-256
  `ced46b4c4318ef53c38eaf9485b76efa4d4d2c155b7194871a8479f0841a993d`, matching
  both saved before/after identities. Manifest and plan copies match their
  frozen declarations; exact probe/decode command arrays and statuses agree.
- The unchanged `inventory` function accepts the saved 189-record probe
  inventory. PTS values are exactly 0–188 at time base 333673/10000000, with
  native 720 × 480, SAR 8:9, interlaced bottom-field-first metadata.
- A separate **post-refusal, read-only** call to the unchanged `check_showinfo`
  passes the stored PTS, frame-count, geometry, SAR, format and interlace joins.
  The original sampler stopped before that check and before product validation;
  this diagnostic audit does not retroactively admit its run.
- Exactly 189 regular, non-symlink files named `frame-000001.png` through
  `frame-000189.png` were counted, totaling **130,737,499 bytes**. Only names,
  types and filesystem sizes were checked. No PNG pixels, headers, RGB hashes
  or image-derived measurements were inspected.
- `frames.json` is absent, as required when admission fails. At audit time
  `extract02`, scoring outputs and aggregation outputs were absent.

## Resource and status record

The extraction contains **209 files / 131,007,165 bytes**, exactly agreeing
with the supervisor's job-byte record. Its recorded elapsed time is
**3.530894458061084 seconds**, below 240 seconds. Job bytes are below the
224-MiB reserved stopping threshold. Recorded lane size before the terminal
receipt is **132,830,245 bytes**, below 1504 MiB. Recorded free space before/
after is **11,285,745,664 / 11,154,165,760 bytes**, both above 4096 MiB.

The supervisor reports `failed`, sampler returncode **1**, and `child returned
nonzero`, with no shutdown or snapshot error. This was a diagnostic refusal,
not a recorded time/storage-limit failure. Before/after free-space values and
elapsed time are verified receipt contents, not independently observed history
of every monitor poll. The sampler reports `structure=inventory_checked`, not
`inventory_and_products_checked`; scientific/human acceptance remains false.

## Verification and preservation

Actual commands: local `cat`, `sed`, `wc`, `shasum -a 256`, and a stdout-only
assertion script invoked using the bundled Python 3.12 runtime with `-B -`.
That script imported only the original sampler after verifying its hash and
called its manifest validation, diagnostic parser, inventory and showinfo
checks on saved text/JSON. It did **not** call a decoder or the extraction
runner. The audit exited **0**, tool chunk `0a28f5`, explicitly reporting
`AUDIT_PASS_RUN_REMAINS_REFUSED`.

| Preserved artifact | SHA-256 |
| --- | --- |
| Original sampler | `c07917382edec4d6ffa83add8d62beb4537b09657346aa18a96c60958e2eef7d` |
| PLAN.md | `f2c67fc6da18ba040448a479065a3d563a06843a91a606384addc3022f70f924` |
| manifest.json | `fc5b819e2079a2d7675e174f93b8584e733d5b735f9cc70f708ff1f2c54c752b` |
| extract01/run-receipt.json | `a061b18402e9d30e639bda4716d81e49753aeebc2cb657e8a7b00c74049692b8` |
| extract01/vince-clip3/receipt.json | `41d592cc774190e1f70e0e3250e92f53d44ee2d14dd8a08d836cb0e354848184` |
| extract01/vince-clip3/probe.stdout | `51478357670208fac974078a2a453d1fbb23d144e05f567767e85745c1b431f5` |
| extract01/vince-clip3/decode.stderr | `76ae78cabb327c0c7b9d18cccbf9d2366030d3396ebe02cc9138182db2213a98` |
| guard-extract01/receipt.json | `37dcdbccb50e9f2d8b1e3f0322504b283d76bf62794915207c1e1d79a71a3ac8` |

## Next boundary

Keep this failure, its partial workflow products, and the frozen protocol/code
unchanged. Continuing with different diagnostic acceptance requires a separately
declared and independently reviewed version, narrowly specified formatting
controls plus retained warning/error/unknown-line refusals, and a finite new
execution schedule that counts this failed run's bytes. This audit authorizes
neither a parser broadening nor another extraction. The retained files cannot
be used as an admitted dense input merely because ffmpeg returned zero or the
filenames count to 189. No historical-source, fire-state or causal conclusion
follows. Only this review file was added.
