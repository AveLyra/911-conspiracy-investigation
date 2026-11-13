
## Follow-up recovery and publication — Nov. 12, 2026

This addendum supersedes the earlier “cannot retrieve payloads” and “upload blocked” statements above. The Project Sources row action menu exposed a working **Download** action even though the preview panel repeated R49's content. All 36 `.txt` payloads were downloaded locally with original filenames and SHA-256 hashes. They total 34 unique hashes; two pairs are exact byte-identical duplicates, preserved under both names and documented in `reconciliation/project-source-files/manifest.json`.

The raw preservation archive is being published to the separate GitHub branch `scooby-project-reconciliation-2026-11-12`, under `research/scooby-chatgpt-project-reconciliation-2026-11-12/`. The default branch was not changed. At this update, 52 of 117 unarchived project chats have complete reader responses staged; 65 remain pending or not yet attempted, including one history-listed ID that returned “No Codex thread found.” The chat reader has also rate-limited collection. Retrieved records report `hasMore: false`; the remaining records must still be retrieved and checked.

The Sources panel inventory contains 137 entries: 36 downloadable files and 101 saved original-response entries. Their titles and dates are in `project-sources-index.json`; saved responses point back to conversations and are represented in the conversation archive as those chats are retrieved.

History pagination found 117 Scooby-assigned unarchived chats. Archived-history pagination exhausted 1,052 entries with no Scooby-assigned chats. No Project files or local files were deleted. The two duplicate pairs are retained; this is preservation, not deduplication or reconciliation.

GitHub checkpoint commits on the branch were authored and committed as Avelyra and pushed after checking the AveLyra CLI identity and exact remote destination. The latest verified remote branch head is `ff6832f5c9e7f3d3c02f5e805d94bf802e0fb472`.
