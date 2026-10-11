# Verification and limits

2026-09-24. [Report](report.md). No application build, legal release, model
execution, sender activation, commit, push or external handoff was performed.

## Selected record and independent replay

Local source: `/Users/admin/.codex/sessions/2026/09/18/rollout-2026-09-18T15-30-35-01a0b5ff-cdd4-7092-aacb-989d7d271428.jsonl`.
The attribution reviewer parsed 416 lines / 6,391,696 bytes through EOF.
Root independently reproduced the whole-file SHA256:
`647174b88ca1a19a6f9d8f4386610072f2ecebd0a10847eb06cdcf2df67952fc`.
Only allowlisted visible-message/model/action fields were used for findings;
reasoning and compaction payloads were not reproduced or treated as evidence.
The transcript was not copied into this research packet.

The app retrieval returned three completed turns, no older cursor, and eight
assistant messages. Their IDs are preserved in the separate review. Root read
all eight completely, matched their IDs/character lengths to the selected
rollout, and independently hashed the eight local visible message texts:

| Rollout line | Phase | Characters / UTF-8 bytes | SHA256 |
|---|---|---|---|
| 11 | commentary | 311 / 317 | c58f288a19cef903e2e8cdc69ab7f4b82d7e86add92865a08c978e77b6da2ae8 |
| 94 | commentary | 367 / 375 | b4ee75ee4c9c2ff6aa777fd18ee5c9d2e0fc55a193ab8975f9549d4ef1a2ed01 |
| 218 | commentary | 394 / 404 | b5714653797fc87e8fdfa78e960c3a09da8979012cd6398bb8a324b9089ebb93 |
| 346 | final | 11623 / 11675 | 50f3375f51aa5cdbb30cc8a9af3a004d53c2a334f6de1f20ef0162d8f407f4b3 |
| 360 | final | 408 / 410 | 9a38a0f10c4ae63927741381f5a349d0efd09f5a94f4b94b31a03d92039d07e2 |
| 372 | commentary | 198 / 202 | 2ea9424b356a24ae2a219fb43a2b968b6df0f9bf5e40f5f32bc339a619254c99 |
| 392 | commentary | 242 / 244 | 4270a512264a6f7ac6d8104b8c9cb06ae3d16d987b9c5797f8298c8b70e92423 |
| 410 | final | 5018 / 5018 | ade4c9413150b6d28dc76df7ebd8d39ba2d7c852d9b2d535a0f53ee849ffe273 |

The attribution reviewer also matched each final against its response-item
and task-complete copies (346/347/350; 360/361/364; 410/411/414). Root's three
final hashes match that review exactly. Identity checks are not substantive
validation. Root's initial parser assumed a different event schema and then
the wrong content discriminator: it produced no matches/empty hashes, then an
assertion failure. Those results were rejected. The final pass used the actual
`item_completed` / `AgentMessage` / single text-bearing content object, asserted
nonempty text, and produced the eight results above. No files were written by
these parsers.

Per-turn contexts at lines6,353,367 identify gpt-5.6-luna/max; the repeated
third context at386 agrees. Root reproduced SHA256 of the allowlisted sorted
compact JSON `{effort,model,turn_id}`:

- Turn `01a0b5ff-d0ce-7151-835d-cfff54f83254`:
  `0459f7e5949c29974c1ba0ee9d95e8c045676fa2e7fe0c03fedc7e1a1c60bed1`.
- Turn `01a0b608-caf3-7101-afac-0a89d3e026c1`:
  `1f0854b3b11348a1ab2f14c24ff6af43ea235055c9cd7c21aafacb79b03a9dcd`.
- Turn `01a0b60a-a54a-7db3-a250-af660b384c93`, both contexts:
  `5dbc643adddcb08efb4bc7deff8699a803a26bdd12654b2890e17d6ce865fe2d`.

## Historical action/census receipts

Attribution review found 128 command-execution records in turn1, none in
turn2, and three in turn3; 25 outer exec calls and three web records overall.
All 131 command records report completed/exit0 in the main checkout. No
explicit patch, file-output redirection, commit or push was identified.
This supports a limited no-observed-deliberate-edit conclusion, not an absolute
historical filesystem certificate. `repo_intake.py` was invoked at line46;
its historical bytes were not pinned. Root read its entire current source:
Git read/status/log calls and path enumeration, no explicit file writes. That
does not exclude historical helper/cache/index side effects. Dollar-parenthesis
census substitutions at167/177 were inspected; an interim reviewer description
as backticks was corrected before reliance.

Historical census support:

- Line167: tracked7186, README101, CSV66, Markdown779, EML184, wordish28,
  PDF204, ZIP13. Its recorded stdout SHA256:
  `c2697bff9164b5df941b28243bc0333ff09561780967c792214df70823813e8b`.
- Root additionally located the research6197 receipt at line101, stdout SHA256
  `dc16ab180e2f57f8f950723a079076ddc5c0e807b1ecae87d02987d7c65e6350`.
- At19:35:21UTC on September18, `wc -l` receipts at279,281,283,284,285 give
  131 source,38 fact,26 exhibit,38 timeline,39 correspondence physical lines.
  Subtracting one header matches the final's130/37/25/37/38 numbers. This does
  not independently validate parsed CSV record counts, multiline fields,
  duplicate IDs, complete source coverage or current inventory.

These are dated command snapshots, not an independent reconstruction of the
entire historical working tree. Present-day counts were not substituted.

## Source checks and reviewer boundaries

Root read the current authority/skills identified in the protocol, current
Case OS README/PLAN, stale status/queue/summary files, `validate_record.py`,
and relevant sender guard implementation. The sender was not invoked; no
configuration, credential store or confidential packet was accessed. No legal
statutory/case-law holding is advanced by this product audit. Vendor primary
URLs linked in the report were opened and searched September24; advertising
claims were not tested in accounts. The report preserves these limits.

Selected current main source SHA256:

| Path relative to main | SHA256 |
|---|---|
| AGENTS.md | 01e3fbd03120a2085520818cea0a843a8c6748b4c7bb8ef0e68547c634a963cc |
| WORKFLOW.md | 17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a |
| START-HERE.md | 30f3734a833d8737ee680b8f10c167e71f0151465df2b8db95d62f278ab3ab72 |
| apps/case-os/README.md | 8ac2adef3f1a09dc6f0ca484e6e160e0acda02a047e5fd60365ba8bc140225ea |
| apps/case-os/PLAN.md | a4841aee47303a79e6d4660b4d58d1318ee46cbd218e50baf3e84729349a0d54 |
| tools/proton_sender/sender.py | 4fdc081c9671b67cfe285b5f45249679fb2be4b15ce7fe68e76354cc2a02df18 |
| tools/validate_record.py | 6c53f04ddb1394e0021a90e5267f9d8e591d7921aeefd6e2fe793eb882c5d082 |
| document-status.md | ce2d7c1148ae4d7846deead3dcab2efe796505813498d69caa28798f664c4c7c |
| intake/to-process.md | bb2f3406bb47059fdb9abae99d02774879df369a99f41c351c1f5fbefd49b430 |
| meta/case/case-summary.md | c4ebd83ec800a227d492908dafe7982f6b7a747d89e85fb4e5bbb6598db4b5d5 |
| meta/strategy/repo-coherence-refactor-plan.md | dd9d075c978e91a841d5d626b9ec137bdf171e6f84f2f70e9989d034cd40ae94 |

Prior-informed substantive reviewer froze `independent-review.md` at
`e7ad6e04e90ccd559d67e2c575aadf8aa8d20f73a8d97a69d9b53b6adea7f020`.
Root froze `root-preexchange.md` at
`a9c2cc0f370140a3cbcaecf22d62a0b7d537a9e2564dd86d0e25291fb39a9432`
before reading that review. They independently agreed on the two principal
scope/recovery issues; additional privacy/baseline findings were reconciled
openly. The reviewer did not independently check vendor claims or model
metadata. Root did not independently redo every action-record classification.
These divisions of work do not constitute independent human expert review.

## Execution limitations

Some combined display outputs were truncated. Selected assistant messages
were then printed in full; unread surrounding tool/reasoning material is not
claimed as substantive coverage. Incorrect README/feedback filename guesses
and worktree-only paths queried from main failed read-only; actual files were
located with `rg --files` and explicit workdirs. Source hashes use the current
main versions and do not prove their historical contents on September18.

Final checks actually run:

- `git diff --check -- research/README.md research/sherlock-wtc7-investigation/STATUS.md research/sherlock-wtc7-investigation/SHERLOCK-FEEDBACK.md`:
  exit0, no whitespace diagnostics.
- A first `git diff --no-index --check /dev/null` loop returned1 for a new
  file without a diagnostic and stopped before its later checks. It was not
  counted as a completed unit validation. A separate read-only Python check
  then verified all five new Markdown files: no trailing whitespace, one
  final newline, all local Markdown targets present, and all three declared
  next-task report paths present. Exit0; five files passed. No application
  tests were run or implied.
- `shasum`/Python SHA256 reproduced the protocol and both frozen reviews
  unchanged. Final report SHA256:
  `cc5e971f462aad443ca2b5741fa7038cd585c3d3b9fce756a5a29a5fa7860dca`.
- Main `git status --short` retains the same seven pre-existing dirty tracked
  paths as at entry; HEAD remains `499cefc8a67f4870b62d181493560f0995e0e1ee`.
  Its AGENTS/WORKFLOW/START-HERE hashes match the source table. No commands in
  this audit wrote main, its legal record, raw evidence or accepted engines.
  Status sameness is not a whole-filesystem before/after byte comparison.
- Research branch/HEAD remain `research/sherlock-wtc7-investigation` /
  `e8d83d7ad979b0e9cda0373e8ab871b8d3cabc38`; this unit and navigation/feedback
  updates are intentionally uncommitted beside preserved prior WIP. No staging,
  commit, push, transmission, human acceptance or goal completion is claimed.
