# Pre-execution acquisition review controls

September20,2026 UTC, before the one historical network invocation. The
original PROTOCOL.md remains unchanged at SHA-256
`3499fbd932a56a64826f2c654e8641965b92fa8a38f5b0fd9df8eb8bd080faa2`.
This adds explicit enforcement of its no-workaround/preservation requirements;
it does not change the selected event, requested format or analysis scope.

Independent review identified implicit defaults in the first, unexecuted
wrapper (SHA-256
`a14161bc9a79734e479c274762f3d246105a087a6b74ef7b9b46235dabed8022`):
inherited environment could supply proxy/import behavior; the pinned executable
was only a Python launcher, not the actual downloader runtime/package; default
fixups may modify a downloaded container; and unavailable fragments may be
skipped by default. These are acquisition-control issues, not historical
tampering findings. No real acquisition ran with that version.

Required implementation before acquisition:

- Direct routing via an explicit empty proxy option and a minimal declared
  child environment; no inherited configuration, proxy, authentication or
  Python import overrides. Keep config/plugins/cache disabled.
- Pin the launcher's actual shebang Python and all installed yt_dlp Python
  source files before/after, with wrapper Python separately identified.
  Actual read-only inspection reports downloader2025.06.09, its Python3.13.9.
  This is not full transitive-library or loaded-code attestation.
- `--fixup warn`: preserve rather than silently repair the access copy;
  review any warning before admission.
- `--abort-on-unavailable-fragments` and `--keep-fragments`: incomplete
  retrieval must not be silently shortened into a completed clip. Preserve
  partial/download fragment artifacts alongside diagnostics.

The separate reviewer checked these defaults against installed primary source
and option definitions; root must confirm the relevant local source before
relying on those semantics. Harmless timeout/nonzero/refusal controls on the
initial wrapper passed, but are not represented as tests of the final code.
The revised wrapper requires fresh controls and final review before network.
Any remaining source/runtime/error limits stay explicit in the execution log.
