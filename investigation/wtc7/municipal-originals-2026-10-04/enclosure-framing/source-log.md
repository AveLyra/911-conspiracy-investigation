# Enclosure framing source and verification receipt

October 4, 2026. Research-only worktree, branch
`research/sherlock-wtc7-investigation`, HEAD `ca1c2233`. Current main controls
retain the hashes checked in the preceding unit (`4e14ff`, exit 0). Full main
charter and applicable PDF/evidence/source-preservation instructions were read.
The preceding coordinate reply confirmed existing work; this is the next new
source check, not a repeated blocker. Existing worktree changes were preserved.

## Prospective acquisition

[PROTOCOL.md](PROTOCOL.md) froze before retrieval at SHA-256
`53468027e199431d5bd50a4558f312a687924c05d5183b38158420a44eca1bf8`
(`3516a4`, exit 0). The target was located in the existing September16 catalog
memo and current STATUS, not guessed. A separate reader inspected the protocol
before admission and reported no material issue. Capture window:
**14:33:16-14:33:56 UTC**.

Exactly one request ran with curl8.7.1 (version checked `267d74`, exit 0):

```sh
curl -q --silent --show-error --proto '=https' --no-location --retry 0 \
  --connect-timeout 10 --max-time 40 --max-filesize 10485760 \
  --output /private/tmp/wtc7-enclosure-framing.I6hrDq/NYC-WTC_000172233.response \
  --write-out '{"http_code":"%{http_code}","url_effective":"%{url_effective}","content_type":"%{content_type}","size_download":%{size_download}}\n' \
  https://sept11documents.cityofnewyork.us/apps/content/September11_MD/NYC-WTC_000172233.pdf
```

Terminal receipt `ee54bd`: exit 0, HTTP200, application/pdf, **145877 bytes**;
effective URL unchanged. No credentials, redirect, retry or captured response
headers. `file`, `shasum -a 256` and `pdfinfo` (`d9712e`, exit 0) confirmed a
two-page PDF1.5, no encryption, form or JavaScript. ABBYY/iText processing and
August2026 modification metadata do not establish historical creation or first
release. The approved `cp -n` preserved the original without overwrite
(`a05e98`, exit 0).

Held [NYC-WTC_000172233.pdf](NYC-WTC_000172233.pdf) SHA-256:
`0c1a0d8ea7c269d297e1d5374c4fa2118b848293a8f6cf49c263c82a6830b3f1`.
The visually inspected Bates172233/172234 and body content match this item.

## Page derivation and independent reproduction

Bundled Poppler26.05.0 was checked (`4f459e`, exit 0). Exactly one full render:

```sh
/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm -f 1 -l 2 -r 150 -png /private/tmp/wtc7-enclosure-framing.I6hrDq/NYC-WTC_000172233.response /private/tmp/wtc7-enclosure-framing.I6hrDq/render/172233
```

Original handle99960 reached terminal exit 0 (`d97a2a`), no warnings; no restart.
Approved `cp -R -n` preserved the two renders (`13b52b`, exit 0).

| Saved render | SHA-256 |
| --- | --- |
| render/172233-1.png | `df32ceda93b84dd08a84b802b7c2e3c42f973f828f5c5815e6c9883471af3513` |
| render/172233-2.png | `6cd6caac18cb208ca4cb9c6be56d4a7b9c1b4313ca35c6a7f1c06c46c228fa78` |

The [independent derivative check](derivative-check.md) rendered the held PDF
once in a fresh temporary directory with the same renderer. Both pages matched
bytes/hashes; terminal exit 0, no warnings. Root read its entire receipt
(`631629`; the later unrelated path search in that compound command failed,
so the compound exit was 1, not a derivative-check failure). Receipt SHA-256:
`15b734ab180574ceff3a0e0d4e2a0f1c1f5afbf24680939e056207cb8398278d`.
This is independent local derivation, not historical authentication.

## Reading and synthesis controls

Root displayed both complete saved pages at original detail, once each. No
repeat, crop, OCR, enhancement, other-source image or measurement was used.
[Root observations](root-observations.md) froze before receiving peer findings
(`bb04cc`, exit 0), SHA-256:
`9061e9ba16f7e037bf9e560639b9f5f50c351e09bfb8575a4f2671f6df0a0277`.
The literal `,+C15x50` in that preserved note is a formatting typo, not a new
source symbol. The synthesis uses ordinary punctuation; the frozen note is
not silently rewritten. Earlier SK-58 reading was consulted as prior-source
context, not counted as a new inspection of that original.

Historical contact details stay in the local
source. The document-role and nonidentical-version issues are covered by
existing SFB-005 fixtures; no new product bug or duplicate issue is asserted.
The designated feedback task remains archived with routing unresolved. No
outgoing payload, main/legal change, engine action, human acceptance, stage,
commit or push occurs in this unit.

## Independent reading and comparison

The separate reader inspected both complete pages once, no repeats, after
independently confirming PDF/render pins (`d970c3`, exit 0). Its
[review.md](review.md) froze before receiving root's findings (`a97981`, exit 0),
SHA-256 `27330e382e8bf2f1db7fa50e9b0466d1768b71ab3a9651a7daf7cbd880c8ad24`.
Root read the complete frozen review (`a43127`, exit 0); both readings identify
the conduit-size difference, relative routing and missing exact segment/floor
join. Both preserve title-block uncertainty. The report additionally clarifies
that drawing north is not geodetically verified and unreadable markings cannot
prove the absence of approval. Four complete first-view displays total are
two readings of one source, not additional historical sources.

After both freezes the separate reader completely read root's note (`439c89`)
and the draft synthesis (`ee865c`), both exit 0. Hash check `926489` confirmed
both frozen readings unchanged. Draft report SHA-256:
`a4797756b02f9d8b41552bce40b40d17e03cfa5f2fceb61a0c46964a3477607d`.
No material correction was found in that text-only review. It did not review
the derivative receipt. Root's subsequent changes record completed review,
clarify unreadable markings/drawing north, and name the existing local source
lead for the next comparison; they do not add historical findings.

The already-held main equipment-audit report and its selection were read as
navigation leads (`a43127`). They locate NCSTAR1-1J OEM physical pages59-61
and referenced submittal/specifications for a future prospective comparison.
No fresh reading of that primary PDF or validation of its claims occurred
in this unit. An earlier inventory command mistakenly tried the fuel-audit
path in this worktree; the explicit main read-only path succeeded (`42d195`).
The failed local path is not an unavailable source or an archive search result.

One finalization patch failed because its expected text omitted the preceding
word on the same line. A read-back (`36e116`, exit 0) confirmed no partial
change; the exact-context correction then succeeded. No frozen input changed.

## Final verification and handoff

The stdout-only `python3 -B -` integrity/navigation check (`9e6285`, exit 0)
verified all five frozen source/note pins listed above, both render pins and
exact two-file membership, the PDF byte count, thirteen local links, and
newline/trailing-whitespace checks for all six unit Markdown files. These
checks cover the declared source unit, not the rest of the investigation or
historical authenticity. Final report SHA-256:
`60affd797ca2c644c4ea908c77e854eda23b739fd715a9fc90c5a393fd78acba`.

`git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/enclosure-framing`
completed with exit 0 (`ff0cf0`, original handle27763 polled to completion).
Untracked Markdown was checked separately above, not claimed as covered by
Git diff. Current STATUS and research-map changes retire the acquisition and
identify a finite held-source OEM comparison; they preserve preceding units
as history. Full goal remains active. This work did not modify the legal
record or settle the separate model-input, audio-listening or human gates.
