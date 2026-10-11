# Preserved FSK-56 artifact integrity verification

October 4, 2026. Independent local integrity check completed. All eight
preserved source/configuration/image/diagnostic files match their root
temporary counterparts byte for byte. All four preserved images also match
this checker's earlier independent renders. Source and image pins, page count,
dimensions, two empty diagnostic files, and four frozen-note pins agree.
No renderer or image viewer ran during this verification.

## Preserved artifacts

Working directory was this `fsk56-followup` unit. `shasum -a 256` and
`wc -c` were run on exactly these eight files (`a5a411` initial output;
terminal `356423`, exit 0):

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `NYC-WTC_000174022.pdf` | 135742 | `a2d7dc4ce0e26ac431e98691d387161657f989d1d685a300731aec3b8d79735f` |
| `fonts.conf` | 233 | `6ba64cd31e9b9080bb4dc654ce045dfa20691fe6bd86077bb7429df78f3d3e9c` |
| `page-1.png` | 65514 | `a40a3125d96a90e5f03bb19eeb10c270bf24aa3e6852e7b5e5753f63d795fde6` |
| `page-2.png` | 133902 | `4a8277c344339c5c3e92e5cc71876df1d3d1b567e22ae0557cad732bf9abc180` |
| `page-3.png` | 111977 | `5eebe37c8b9657b497886ab3d1b56687ee76db77b71b74d86949452a951972a3` |
| `readability-2.png` | 945816 | `63e3559dbfd6763a2895f45306e80fede115b73a78b55d556d22fc5bfe3d7028` |
| `render.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `readability.stderr` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

These total 1393184 bytes. Source and four image hashes agree with the earlier
independent derivative-check pins; the preserved configuration is root's
configuration, not this checker's different-cache-path copy.

## Actual comparisons and metadata checks

An explicit eight-filename loop ran
`cmp -s <unit-file> /private/tmp/wtc7-fsk56.4NS5KF/<same-filename>`.
A second loop compared `page-1.png` through `page-3.png` with
`/private/tmp/fsk56-derivative.57ESnp/physical-1.png` through `physical-3.png`.
A final `cmp -s` compared the two `readability-2.png` copies. Every status
was recorded: `checked_pairs=12 failures=0`, terminal `8212fe`, exit 0.
This accounts for every requested file and every independent image pair.

The following command inspected PNG headers only (`a5a411` / `356423`):

```sh
file page-1.png page-2.png page-3.png readability-2.png
```

| Saved raster | Dimensions |
| --- | --- |
| `page-1.png` | 1633 x 2200 |
| `page-2.png` | 1641 x 2200 |
| `page-3.png` | 1648 x 2200 |
| `readability-2.png` | 3281 x 4400 |

All four headers report 8-bit/color RGB, non-interlaced. Dimensions agree with
the earlier independent check. No pixel-content view was performed.

With shell `pipefail` enabled, the exact metadata command below completed
with terminal exit 0 (`356423`):

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo NYC-WTC_000174022.pdf | rg '^(Pages|Encrypted|File size|PDF version):'
```

It reported 3 pages, no encryption, 135742 bytes and PDF 1.5. No full PDF
content, contacts or annotations were printed.

`diff -u /private/tmp/fsk56-derivative.57ESnp/fonts.conf fonts.conf` returned
1 (`19d6c8`) because exactly the cache-directory line differs: this checker's
`/private/tmp/fsk56-derivative.57ESnp/font-cache` versus root's
`/private/tmp/wtc7-fsk56.4NS5KF/font-cache`. Both retain the same two declared
font directories and all other lines. This expected difference is recorded,
not a failed source-copy or rendering check; unit/root-temporary configuration
copies were byte-identical in the eight-file comparison above.

## Frozen-note pins

`shasum -a 256 PROTOCOL.md root-observations.md review.md derivative-check.md`
returned these same values at the beginning (`05eeda`, exit 0) and end
(`20ac1e`, exit 0; UTC 18:48:44) of the check. Protocol and derivative-check
match this checker's earlier recorded pins. Root expressly confirmed the two
reader-note hashes against its previously frozen pins; those notes were
hashed without reading their contents.

| Frozen file | Matching SHA-256 |
| --- | --- |
| `PROTOCOL.md` | `4552522ed7f5f54502ee4b864f94cda0e5ef5da70be3005edf450b511bd93bca` |
| `root-observations.md` | `de081ef05651a148a175d30b64ad33eed8505b35e1d3ee670660f62d982b0052` |
| `review.md` | `6d55ac425d5c424d944448e43fef09deb406c4f6d0b51b0617e3f34747436c1d` |
| `derivative-check.md` | `68d28b63524fc7323d9ec68bb826992e91a5742d4a6e8c956bd1b60d9eb926b4` |

## Limits and preservation

No integrity mismatch or command error occurred; the sole nonzero result was
the expected configuration diff described above. Earlier derivation diagnostics
remain in the frozen derivative check and were not rewritten. Empty stderr
files alone do not establish process success; actual render statuses remain
the earlier execution receipts. This check verifies saved rasters, not the
reader's resized display or its legibility.

Only this new verification note was written. Frozen files, synthesis,
source-log, raw source and earlier records were not modified. No network,
new source view, renderer rerun, engine action or Git mutation occurred. Root's
separate Git, Markdown and synthesis checks are not claimed as independent
checks here. Local integrity is not historical authenticity, source
completeness, an engineering conclusion, or human acceptance.
