# Independent PDF-to-PNG derivation check

2026-10-04. Research only. A separate agent independently executed the two
render commands against the held PDFs. Both source pins matched, both jobs
reached terminal exit 0, and all eleven resulting PNG files are byte-for-byte
identical to the corresponding saved `render/` files. This checks reproducible
derivation from these held bytes with the same renderer version; it does not
independently authenticate the records or their historical contents.

## Scope and acceptance

The declared scope was exactly one fresh render of page 1 of 153903 and pages
1-10 of 173529, at 150 dpi, followed by comparison of every generated PNG with
the saved set. Acceptance required exact source-pin agreement, terminal
statuses and warnings, eleven accounted-for pages, and a complete byte or
decoded-pixel comparison. No network, OCR, crop, enhancement, text extraction,
new source reading, or substantive interpretation was authorized or performed.
Only this new unit note was to be written; the original PDFs, saved renders,
protocols, source log and reader notes remained read-only.

The main repository's complete `AGENTS.md`, `WORKFLOW.md`, and `START-HERE.md`,
the PDF skill, and this unit's `PROTOCOL.md`, `DIRECT-RETRIEVAL.md`, and
`source-log.md` were read before rendering. The worktree's older `AGENTS.md`
diff was inspected; the current main controls were followed. No PDF authoring
occurred, so the PDF skill's authoring-start marker did not apply.

## Environment, input pins and execution

`command -v pdftoppm` resolved to
`/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm`;
`pdftoppm -v` reported Poppler 26.05.0 (`78c3b4`, exit 0). Environment:
macOS 26.6.2, build 25G83, arm64. `mktemp -d
/private/tmp/municipal-derivative-check.XXXXXX` created the fresh private
directory `/private/tmp/municipal-derivative-check.Y6aWag` at
2026-10-04T13:48:57Z (`aa5686`, exit 0).

`shasum -a 256` checked both held PDFs before rendering (`086b96`, exit 0)
and again afterward (`716958`, exit 0). Both checks produced the declared pins:

| Held PDF | SHA-256, before and after |
| --- | --- |
| `NYC-WTC_000153903.pdf` | `87daf254c97f818598eab7de77481048079c69b300338a5c7734719acb0b985d` |
| `NYC-WTC_000173529.pdf` | `143af40af3270048ef8b9afc501342f40341c2dc6b9256394396682900e1c2c6` |

The working directory for both commands was
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04`.
The two independent jobs were dispatched concurrently, once per PDF:

```sh
/usr/bin/time -p pdftoppm -f 1 -l 1 -r 150 -png NYC-WTC_000153903.pdf /private/tmp/municipal-derivative-check.Y6aWag/153903
/usr/bin/time -p pdftoppm -f 1 -l 10 -r 150 -png NYC-WTC_000173529.pdf /private/tmp/municipal-derivative-check.Y6aWag/173529
```

Each shell wrapper printed `date -u '+%Y-%m-%dT%H:%M:%SZ'` immediately before
and after rendering, captured the render status, then exited with that status.
The original live process handles were polled to completion; neither job was
restarted. Terminal evidence:

| PDF | UTC start / end | `/usr/bin/time -p` seconds (real / user / sys) | Terminal result |
| --- | --- | --- | --- |
| 153903 | 13:50:05 / 13:50:07 | 1.81 / 0.14 / 0.02 | Session 99596; `6776ae`, exit 0 |
| 173529 | 13:50:04 / 13:50:22 | 18.29 / 3.47 / 0.13 | Session 57909; `b556f4`, exit 0 |

No renderer warning or error text was returned. The output consisted only
of the wrapper's UTC timestamps and the timing utility's measurements.

## Complete comparison

The fresh and saved sets each contained exactly eleven `*.png` files.
The following comparison ran from the unit directory (`3deb07`, exit 0):

```sh
set -- /private/tmp/municipal-derivative-check.Y6aWag/*.png
printf 'generated_file_count=%s\n' "$#"
set -- render/*.png
printf 'saved_file_count=%s\n' "$#"
municipal_compare_failures=0
for municipal_image in 153903-1.png 173529-01.png 173529-02.png 173529-03.png 173529-04.png 173529-05.png 173529-06.png 173529-07.png 173529-08.png 173529-09.png 173529-10.png; do
  cmp -s "/private/tmp/municipal-derivative-check.Y6aWag/$municipal_image" "render/$municipal_image"
  municipal_cmp_exit=$?
  printf '%s cmp_exit=%s\n' "$municipal_image" "$municipal_cmp_exit"
  if [ "$municipal_cmp_exit" -ne 0 ]; then municipal_compare_failures=$((municipal_compare_failures + 1)); fi
done
printf 'comparison_failures=%s\n' "$municipal_compare_failures"
exit "$municipal_compare_failures"
```

Every listed comparison returned 0; `comparison_failures=0`. There were no
missing or extra images. SHA-256 was also computed for every fresh PNG
(`shasum -a 256 /private/tmp/municipal-derivative-check.Y6aWag/*.png`, `c351f2`,
exit 0) and every saved PNG before and after rendering (`2b5bdb` / `716958`,
both exit 0). All three sets and the source log's pins agree:

| Image / physical page | SHA-256 of both fresh and saved PNG | `cmp` exit |
| --- | --- | --- |
| `153903-1.png` / 1 | `8a83a742bf5ae93b2828ed718e878596ca6dd65ce51242c44028420163e0496a` | 0 |
| `173529-01.png` / 1 | `079b9a2e2eda9fd7f920c12956b3484d95f49e92d12cc75801a831e2857dc044` | 0 |
| `173529-02.png` / 2 | `7ccc0cc1a2c6a76195a13c6186fa8fccd3672029903ccce910fd0dbca05f2091` | 0 |
| `173529-03.png` / 3 | `4efa4c8a3ab4e083b6a3cee33c60d1f1c11f4f7840998c39a0b6dfcdae8c8ff2` | 0 |
| `173529-04.png` / 4 | `c54c2f10f2063a3e209fb3e5b39f6ecd0e051b4623d29701eb6a25ca8b15d983` | 0 |
| `173529-05.png` / 5 | `772db94a4f3311b339bedc089f2feec2a3c068abc9d0921da4940d609964e1e9` | 0 |
| `173529-06.png` / 6 | `6d9ffbbb5796601761871d9e11849d1b6870eff014d9e41ae07a0b0220e037ea` | 0 |
| `173529-07.png` / 7 | `11e9cfee707fa1727901393680a94679c5eb861e53bfc8e6231c0abc3236152f` | 0 |
| `173529-08.png` / 8 | `6118c9b1259fb5cf57f6142e404204fd41617dd88f46e8e023dca0b690b736cb` | 0 |
| `173529-09.png` / 9 | `6a8b00c44e9d3ae39c19b379bda01990c2e5546e27b9c72d93d6dcd00c1a2996` | 0 |
| `173529-10.png` / 10 | `bee9e26a1527fc229db3b7cb63a7504b9af52be9e82fbf20cc76b18b65b1ba92` | 0 |

Exact byte agreement made a fallback decoded-pixel comparison unnecessary.
There was no visual or textual source interpretation in this check.

## Preservation, deviations and limits

The two PDF pins and all eleven saved PNG pins remained unchanged. The following
control and reader-note hashes also matched before and after rendering:

| File | SHA-256 |
| --- | --- |
| `PROTOCOL.md` | `ba9f1aa7b2b785ec101e7f273dc064a7252fbdd4c4670526ec7df03ae075d82c` |
| `DIRECT-RETRIEVAL.md` | `ac22ba4f37a88cfb87b85ae172b0ce44a7367e858b92a7af93d43c189ae10105` |
| `source-log.md` | `fddbc6dce08893892370d5a72fd85129fe36b0f376d7ce90248ac51a269556e5` |
| `root-observations.md` | `1a7a6ce7a10765fcc47503e7c8c497f61eb27245235765814eb5e8e433b909c3` |
| `review.md` | `6e0ae6c36b1f5bfcf0a2f0329c82d4036e11d9d2881ac82144633cf935777c3f` |

An initial overly broad local filename enumeration produced truncated output;
it was replaced with a unit-scoped enumeration. A separate preliminary
`rg --files -g 'AGENTS.md' research` returned 1 because no nested instruction
file was found, so its `&&`-chained inventory/hash commands did not run
(`7b7686`). Those reads were then executed separately. Neither event was a
render attempt, source change, network failure, or successful verification.
There were no failed renders, retries, or failed PNG comparisons to discard.

The fresh PNGs remain in the named private temporary directory and were not
copied over the saved set. Temporary retention is not durable archival storage.
Same-runtime agreement does not test an independent rendering implementation,
prove that the PDFs contain complete historical records, validate the source
reader's interpretation, establish custody or first-release history, or resolve
the existing visual uncertainties. No source or finding was promoted to a
canonical legal record, accepted by a human, transmitted, committed, or pushed.
