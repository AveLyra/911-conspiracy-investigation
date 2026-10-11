# Job 1854 follow-up locator preservation check

October 4, 2026 America/New_York / October 5 UTC. PASS for the bounded checks:
ten exact request contracts, twenty request/response JSON integrity pins, and
forty complete acquisition-file pairs plus one separately added diagnostic pair.
No response or diagnostic JSON was parsed and no candidate
results were interpreted, ranked or exchanged by this checker. Transport-record
limitations and the failed first acquisition are retained below.

## Scope and authority

The complete PROTOCOL and source-of-truth/evidence-falsification skills were
read before actions (`4561f5`, exit 0). Main AGENTS, WORKFLOW, START-HERE and
investigation CHARTER had already been fully read; their current hashes were
rechecked unchanged (`d0ef82`, exit 0). These skills keep preservation and
request conformance distinct from historical authenticity or source truth.
The sole repository write is this new derivative receipt. No raw file, old
note, main/legal file or source was changed; no acquisition, network, PDF/image
view, Git, send or engine action occurred.

Protocol SHA-256: `4d80c5e158fb35be8bd569ecd6ea4824bd860275bd54c36b1332353b4e4ff37d`.

```text
U=/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/municipal-originals-2026-10-04/job1854-followup-locator
R=/private/tmp/wtc7-job1854-locator.c4IvYO
```

The checker waited for the acquisition-complete notice before inspecting
requests or completed transport files. Bounded filename discovery used
`rg --files --hidden --no-ignore` restricted to request/response JSON, headers,
stderr and transport filenames in U and R. The previous lookup's exact
`test-acceptance-locator/control-request.json` was read only to confirm its
incorporated eleven-field request shape; no preceding results were read.

## Request contracts

A stdout-only `python3 -` check (`f0ffdf`, exit 0) parsed only the ten
`U/<label>-request.json` files. `json.loads(..., object_pairs_hook=unique_pairs)`
rejected duplicate keys. Each whole object had to equal the independently
constructed expected object, including all nested keys and ordered properties;
extra keys were not allowed. Exact integer types were required for count=50
and content_sample_length=0, and the eleven property names were distinct.
All ten passed; zero response JSONs parsed.

The property list was exactly `mes:key`, `title`, `source`, `agency`,
`box_name`, `folder_name`, `page_count`, `pdf_size`, `production_volume`,
`production_end`, `mes:date`, each shaped as
`{"name": "<name>", "formats": ["VALUE"]}`.
The query was exactly `user.query.unparsed`; all other fields were exactly
the count, sample length and properties above. Checked query strings:

| Label | Exact query |
|---|---|
| penn | `ALL extension:pdf source:"WTC 7" Penn` |
| penn_phrase | `ALL extension:pdf source:"WTC 7" "H.O. Penn"` |
| apt | `ALL extension:pdf source:"WTC 7" APT` |
| transient | `ALL extension:pdf source:"WTC 7" transient` |
| date_slash | `ALL extension:pdf source:"WTC 7" "7/31/99"` |
| date_words | `ALL extension:pdf source:"WTC 7" "July 31"` |
| load_shedding | `ALL extension:pdf source:"WTC 7" "load shedding"` |
| fuel_pump | `ALL extension:pdf source:"WTC 7" "fuel oil pump"` |
| break_glass | `ALL extension:pdf source:"WTC 7" "break glass"` |
| control | `ALL extension:pdf source:"WTC 7" box_name:"7DCAS" folder_name:"SKP-3 & SKP-4 AND REVISED S-TS-7 FOR YOUR USE"` |

The current and preceding exact control-request files also matched with
`cmp -s` (`6ebd11`, exit 0). This validates the request bytes, not whether the
known record appears in the response; content/result checking belongs to the
separate extraction review.

## Byte preservation and twenty JSON pins

The comparison started 2026-10-05T02:00:55Z (`b94a76`, handle 89225), then
the original handle was polled to terminal (`c39ca2`, exit 0). No comparison
process was restarted. For all ten labels above, these actual commands were
expanded over suffixes `-response.json`, `.headers`, `-transport.txt`, `.stderr`:

```sh
shasum -a 256 "$U/<label>-request.json"
wc -c "$U/<label>-request.json"
cmp -s "$U/<label><suffix>" "$R/<label><suffix>"
shasum -a 256 "$U/<label><suffix>"
wc -c "$U/<label><suffix>"
```

Every `cmp` status was 0: ten responses, ten headers, ten transport logs,
ten stderr files, forty pairs total, zero comparison/read failures. The
hash/size tables describe the preserved files; their byte-identical scratch
partners necessarily have the same hashes and lengths. Requests exist in U
and were validated/pinned there, not claimed to be separately acquired copies.

| Label | Request bytes | Request SHA-256 | Response bytes | Response SHA-256 |
|---|---:|---|---:|---|
| penn | 1082 | `19267ec3e28801f7bb3afd37540cbe218e68d92307f0d594d9acbb03ca842df8` | 64684 | `1202cd667c7ce002ff231ef4b2e9460f01795b9b054a3dd935b2f131fac8efce` |
| penn_phrase | 1091 | `cf3e6a270efb84753bef19649dbe20e4241537d76e20e8eacd981e9c61c5996c` | 26105 | `54457b9032d4d1783ee38c5a9a2bd6b043ccc0334035af855928ef0c6acf3283` |
| apt | 1081 | `b34436ebe028a2c16303410c69a8aa1f272d7687288c7317db7503585d2aa7db` | 28606 | `edca6e7e2e4ce1fe9597e02ad43d73638e8c9143e2add8e2c6460f8fccefd7cc` |
| transient | 1087 | `32e70b05a723acaae1693e64e8cc010bf58d7556b1438ecc5efa2bb5fbcdf2ef` | 11619 | `37b9ecb12c0a722caf551f42398af6d80d336ea1bf92ad9100e981d4a0289ae3` |
| date_slash | 1089 | `ab3903796c66041a3a28a5d56d0a1058eff8ad7f8659dfa82b902ba7b8c98b4e` | 17739 | `4bc4695cb8e94616475a92f75b1cd748c4bfd25e0947696db73e04bb517f51de` |
| date_words | 1089 | `b9b83c9df9843ec5174ca81189c1998591980e97acc8bfb6219dc1c33b92bb80` | 29768 | `c062562ca7eb8931edd58ebefb9a29c5ef369ec75ffae98e98130860fc3dd2db` |
| load_shedding | 1095 | `7ac53ae0c5356f69b610c2c6d4acaa3cc04a7170b88b59dcab058ecc549c9343` | 15507 | `921d6ab1d95e67be18399c36e4931c98a6af842f5195266fb18a5b9a71f390bf` |
| fuel_pump | 1095 | `3e20572e4f4af8da85cc4d52597ee302f18b20fd5140d95573077995a689b0b6` | 17729 | `75efcf4871d44c4e20b85fa3f1dd812b092c20b8257a36d43e986fe0f909ee72` |
| break_glass | 1093 | `0b5babaad5fd69a986b4bc33838d6b9696af50bd281a5d9d458491d1ce855947` | 16556 | `440be5766c79591ae7dae03a1f3778e8330c75350f6cc611ebf70266dd0e7ae4` |
| control | 1158 | `05a0df86737b4efeaf9949051c23385e22ed46c16a4ddbca567511e1a45277ef` | 8451 | `bbdeb6f33a4e8d937d9b13e666f226b6fee5bfbdbf436763bfce250f864ca80a` |

Total request bytes: 10960. Total raw response bytes: 236764. All response
files are below the protocol's 10 MiB cap; this does not prove that acquisition
enforced the cap or that the search results are complete.

## Headers, transport logs and diagnostics

The complete ten transport files and header sets were checked (`f62fca`,
exit 0), then a stdout-only `python3 -` allowlisted correspondence check
(`94a1cc`, exit 0) verified each entire transport string against
`http=(three digits) bytes=(digits) content_type=(nonspace) redirects=(digits)`
plus final newline. All ten record HTTP 200, application/json;charset=utf-8,
zero redirects, and a byte count exactly equal to that response's actual
size. Each header set contains exactly one HTTP 200 status and matching
Content-Type, with no Location header. All ten stderr files are zero bytes.
The script emitted no candidate data or response contents; zero failures.

All headers are 558 bytes (5580 total). Transport files are 77 bytes each
except control, 76 bytes (769 total). All ten empty stderr files share
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

| Label | Header SHA-256 | Transport-log SHA-256 |
|---|---|---|
| penn | `8cff3d4f6c3a587de6f7e29cd0ccf73401f763316601dd25b42d072b7320c6e1` | `15d8cb8d1e40072a80e451e310b40d1c96e3d577b075a62d661e42535e2d77da` |
| penn_phrase | `6b34b36f7abd7697e6e6fcaf43cfd10dad20835ac281c034050ca1fe0314dffe` | `f99d590cccad2d4eb839217712d08101cee92127a97ea0b5955ef78e5dfb2a7d` |
| apt | `0e4e0339353b31f10f429c0e8aea9b983656b40f0ae2d42c4cc11ef203d46605` | `244f2c6a42f091734879c78072b8fcbd144e9189b9aa251671eb9d0600f133d7` |
| transient | `34b930493aeee5a70ea8ad5d93ed17cc94aaf4582ddd14d4b691fe7052455ad9` | `7b4a88b4be38a9e7e3547961c9ffff6a59cf38beeb7565c06d2d9f523b2f6458` |
| date_slash | `5aad268962cd02784e82b8cae60cf7d30b305f28d0ba74597536bc0d7e6ef1c9` | `d872ca83cee0179dd1f9937f46855bcfaf942116d38a796e65b8ff9f130fb08c` |
| date_words | `41f089a8b55c19a36df6ecf321b546b8c1168a2ac96eec599184bb0065039647` | `ffef8c38aef54911a6146a1b5241d576629d3e3489ca836ad1cbc1cbd0e0e844` |
| load_shedding | `7dee2acf06a0a322ff8734768525dcaf1d3080c6908d3902620460119dfb546c` | `408f5a6d18aa6892c4785cf53c52b5e5ac1897d21c35b6ef750c47a688db2828` |
| fuel_pump | `991f6f218ef8e0f5f633e920ed6a504ea5abc3c23318553effa0ab0b6646bcbe` | `11640e57f80f1223a81f6fd912ba0367aea8ce636322039ea8dec50e879073f1` |
| break_glass | `6f9a7e0ab1311ab52fb7d8650b721002b0ff55be99ddc7cc2035742184f66d96` | `6ac81023503eb7c54b3c00efb823810c72704b074a609ebbd7e48fcd41988e21` |
| control | `06b94a6962396b8a252ac53dd99e8ced670c87730a084b3179657789790b9e8c` | `cf8b32a92f0aff2698c56da5afde90e8d48b5a92f8cd04e49a84d3524a0fd9cb` |

The first header-inspection command printed server-issued session-cookie
values into its local tool output. This was unnecessary for the correspondence
check; later output was restricted to allowlisted transport checks. Those
values are not reproduced here. No cookie was replayed and this checker made
no network request. Full raw headers are preserved locally, unchanged and not
silently sanitized; they are not eligible for publication or push. Root stated
it would add a unit header ignore guard and source-log restriction; this
checker did not edit or verify those controls.

## Added diagnostic preservation pair

Root separately declared `root-diagnostic.json` preserved from scratch via
copy receipt `3ad911`, exit 0. Bounded filename discovery (`d38bae`, exit 0)
identified that exact file in U and R; no diagnostic code or contents were read.
At 2026-10-05T02:04:53Z, `cmp -s`, `shasum -a 256` and `wc -c` on the two
exact `root-diagnostic.json` paths (`c3b046`, exit 0) confirmed byte equality,
114859 bytes each, and the declared SHA-256
`c6a80ecc100e77cc3d387e17fa032e8c4032e4e13cb761d20bffd6eaed51e7d8`.
This is the 41st verified pair, additional to the forty acquisition files and
the twenty request/response pins; its JSON was not parsed or substantively
endorsed. No acquisition or content review was added.

## Failures, attributed receipts and limits

Root reported the initial sandbox control attempt `2a29d7` exited 6 with DNS
failure, HTTP 000 and no response. This is not a server refusal or a successful
control result. This checker verified its scratch-only `control-sandbox.headers`
is zero bytes with the empty-file SHA-256 (`f62fca`), but did not independently
execute or observe that acquisition. No complete persistent failed-attempt
transport/stderr pair was supplied in the forty-file success copyset.

Root reported successful acquisition handle 54481, initial receipt `b505e8`,
terminal `d28070`, exit 0, with ten individual curl exits 0. Root's preservation
copy handle 90065, initial `214f7a`, terminal `b550dd`, also reportedly exited 0.
These are attributed operator receipts, not this checker's own subprocesses.
The ten saved transport logs are complete four-field logs, but they do not
contain curl exit codes, elapsed time, exact commands or effective URLs.
Thus the files alone do not independently prove timeout/config/cookie policy,
TLS details, actual command execution, one successful request per query, or
historical no-overwrite copying. Byte equality establishes current copy integrity.

Root also reported its strict extraction stopped (`24f118`, exit 1) because a
folder_name was absent. That separate schema finding is not a preservation
failure and is not resolved or verified by this note. No response parsing,
response-query-echo check, result/property validation, pagination assessment,
known-record hit verification or extraction completeness claim was performed
here. Those remain assigned to the independent extraction/method reviewers.

All actual request/preservation/correspondence checks in this note passed.
Integrity is not authenticity: local exact copies and internally consistent
transport records can still preserve incorrect, incomplete or unauthenticated
material. This receipt does not validate archive labels, OCR, historical facts,
source independence, installed conditions or cause. No file was deleted.
