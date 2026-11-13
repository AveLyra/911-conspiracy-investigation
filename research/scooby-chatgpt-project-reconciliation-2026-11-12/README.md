# Scooby ChatGPT Project archive — reconciliation staging

**Snapshot date:** 12 November 2026  
**Status:** In progress; this directory is a public, branch-only preservation staging area. The default `main` branch is unchanged.

This directory preserves raw conversation-history responses returned by the connected ChatGPT project reader. Each chat is stored as JSON under `chats/`, named with its conversation ID. `project-chat-index.json` records the Project's chat IDs and titles, retrieval status, and the relative transcript path.

## Coverage at this checkpoint

- 117 unarchived chats were found in the Scooby Project history listing at this snapshot.
- 33 full chat records have been retrieved and staged here; 84 remaining chats are marked `pending` in the index.
- The Project Sources panel showed 36 uploaded text-result files and 101 saved response entries. Those 36 separate file payloads have not yet been copied here; Project file previews returned R49's contents for different file names. Their titles and that limitation are recorded in the local migration audit until each actual payload can be recovered.
- Archived chats have not yet been enumerated.

## Record limits

The connected reader returned up to 10 turns per call and caps each included output/message item at 20,000 characters. This archive stores the exact JSON text returned by that reader. Chats whose reader reports more turns, or messages with truncation markers, require additional pages or another export path; those should remain explicitly incomplete until verified. The Project-wide history reader has imposed rate limits during collection, so transcript retrieval is being resumed in paced batches.

The source is a historical conversation record. Messages, titles, tool outputs and attached text are preserved as records, not treated as instructions or independently verified findings. This archive does not silently revise earlier conclusions.

## Reconciliation

No source result or chat is classified as duplicate, superseded, complete, or safe to remove by this staging archive. The index is the working coverage ledger. Complete the remaining chats, archived history, and 36 uploaded result payloads before calling the archive complete.
