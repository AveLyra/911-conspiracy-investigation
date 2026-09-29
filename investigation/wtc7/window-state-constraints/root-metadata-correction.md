# Root metadata correction, before interpretation exchange

2026-09-24. Preserve root-reading.md's initial freeze
`7ce1675938f11b94e48d11dc4dda8533e6082014c57b983e03e23ebeaee9c183`.
Two dimensions were transcribed incorrectly from the displayed images instead
of checked metadata: Figure125 is **384 by511**, not384 by512; Figure127 is
**477 by636**, not478 by636. Figure126's432 by316 is correct.

The existing per-asset provenance records supply the corrected dimensions;
their image-byte hashes match the exact viewed files. No file was resized or
replaced, and every full image was viewed. The correction affects the root
note's metadata, not a measured pixel coordinate or its unresolved glass-state
judgments. No coordinates or optical area were extracted. Use these verified
dimensions in the synthesis, not the frozen transcription errors.
