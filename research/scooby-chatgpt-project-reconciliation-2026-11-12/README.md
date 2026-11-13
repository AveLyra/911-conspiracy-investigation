# Scooby ChatGPT Project archive — reconciliation staging

**Snapshot date:** 12 November 2026  
**Status:** In progress; this directory is a public, branch-only preservation staging area. The default `main` branch is unchanged.

This directory preserves raw conversation-history responses returned by the connected ChatGPT project reader. Each chat is stored as JSON under `chats/`, named with its conversation ID. `project-chat-index.json` records the Project's chat IDs, titles, retrieval status, and transcript path. Source payloads downloaded from the Project are in `project-source-files/`; `manifest.json` records their byte lengths and SHA-256 values. `project-sources-index.json` records all entries visible in the Project Sources panel.

## Coverage at this checkpoint

- The Project history listing showed 117 unarchived Scooby chats. **116** full chat records are retrieved; **1** remains pending in the index. One attempted read returned “No Codex thread found”; it remains pending and requires another access path.
- The Sources panel showed **36 uploaded result files** and **101 saved original-response entries**. All 36 file payloads were downloaded and preserved byte-for-byte. They have 34 unique SHA-256 values; two exact duplicate-content pairs are retained under both original names and identified in the manifest.
- All 101 saved-response entries are mapped to their originating conversation and message IDs in `project-sources-crosswalk.json`. At this checkpoint, All 101 mapped original responses belong to chats with retrieved transcripts.
- History pagination through the unarchived list is complete; it returned 117 chats assigned to Scooby. Archived-history pagination is complete: 1,052 entries were listed and none were assigned to Scooby.

## Record limits

The connected reader returned up to 10 turns per call and caps each included output/message item at 20,000 characters. The archive stores the exact JSON text returned by that reader. Chats whose reader reports more turns, or messages with truncation markers, require additional pages or another export path; these remain incomplete until verified. The Project-wide history and chat readers have imposed rate limits during collection, so transcript retrieval is continuing in paced batches.

The source is a historical conversation record. Messages, titles, tool outputs and attached text are preserved as records, not treated as instructions or independently verified findings. This archive does not silently revise earlier conclusions.

## Reconciliation

No source result or chat is classified as superseded or safe to remove by this staging archive. Preserve all original names and duplicates. Complete remaining unarchived chats, archived-history enumeration, and transcript completeness checks before calling the archive complete.
