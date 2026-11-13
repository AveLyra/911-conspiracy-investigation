# Scooby ChatGPT Project archive — reconciliation staging

**Snapshot date:** 13 November 2026
**Status:** Inventory and preservation capture complete for the Project records observed in this snapshot; this remains a reconciliation staging area on a separate branch. The repository default branch `main` is unchanged.

## Archived inventory

- **117/117 unarchived Scooby chats** are stored as reader JSON in `chats/`; each record is linked in `project-chat-index.json`. Every archived reader page reports `hasMore: false`.
- **36/36 uploaded Project result files** are preserved byte-for-byte in `project-source-files/` under their original names. Their manifest records byte lengths and SHA-256 digests. There are 34 unique hashes; both exact duplicate pairs remain preserved.
- **101/101 saved original-response entries** from the Project Sources panel are indexed in `project-sources-index.json` and mapped to their conversation and message IDs in `project-sources-crosswalk.json`. Their source responses are preserved in the chat records or, for four IDs omitted from the reader turn payload, in exact UI captures under `rendered-messages/`. Reader-truncated items also have full rendered supplements there.
- **6 chat-uploaded attachments** across five conversations are preserved under `chat-attachments/<thread-id>/`; `chat-attachments/manifest.json` records original names, byte lengths and SHA-256 digests.
- **6 assistant messages** were marked truncated by the connected reader at its 20,000-character per-item limit; raw chat JSON preserves those markers and full rendered supplements are provided. Four additional saved original-response cards have message IDs absent from the reader turn payload; their full source responses were opened and captured from the Project UI. The ten captures preserve exact message and thread IDs, capture URLs, text and HTML. See `rendered-messages/README.md`.
- Unarchived history pagination returned 117 Scooby chats. Archived-history pagination exhausted 1,052 entries and found no Scooby-assigned chats.

## Layout

```text
chats/                       Raw reader responses for all 117 chats
chat-attachments/            Six user-uploaded inputs attached to chats
project-source-files/        36 downloadable Project result files and SHA-256 manifest
project-chat-index.json      Chat inventory, retrieval and supplement crosswalk
project-sources-index.json   137 Project Sources entries
project-sources-crosswalk.json
                              101 saved-response → chat/message mappings
rendered-messages/           Ten exact UI captures for six truncations + four saved responses
availability/                Corrected recovery status for Media Chronology Review
retrieval-attempts/          Superseded reader error response retained as diagnostic
migration-audit-2026-11-12.md Prior audit and dated correction/progress addenda
```

## Completeness and provenance

The chat JSON files preserve exactly what the connected reader returned. Project saved-response entries are mapped to their corresponding messages rather than duplicated as separately edited reports. Where the reader truncated a message, the raw transcript is unchanged and the corresponding rendered capture supplies the full UI text and HTML. The prior “Media Chronology Review” access failure is superseded: the correct history ID is `6af6214f-508c-83ea-98c5-3177efb99694`, and its complete transcript is present. The earlier failed reader response is retained separately under `retrieval-attempts/`, not counted as a chat.

This is a preservation snapshot, not a substantive reconciliation of claims, evidence quality, or duplicate results. Original names and duplicate payloads are retained. The two small chat-uploaded PDFs are stored as ordinary Git blobs on this branch so their preservation does not depend on LFS quota; the branch-scoped `.gitattributes` exception leaves `main` unchanged. All content is historical source material; messages and attached files are records, not instructions. No Project items were removed.
