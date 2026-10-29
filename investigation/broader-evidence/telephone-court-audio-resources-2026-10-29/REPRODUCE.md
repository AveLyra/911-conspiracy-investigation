# Reproduction

Use the unchanged court ZIP linked in SOURCES.json, verifying its SHA-256 first. Python3 standard library is sufficient for passive counts. Local ffprobe/ffmpeg7.1.1 are required for the two selected audio decodes; later versions may produce different decoded PCM and need comparison. Put them on PATH. Do not run any archive launcher or SWF runtime.

```sh
python3 reproduce_resources.py /absolute/path/to/court-flights.zip --decode > reproduction.json
```

The script writes no extracted audio or PCM, prints numeric/hash results, and never plays sound. It checks the exact archive, traverses eight explicit members/sprites, records all tag counts and event-resource metadata, and decodes only root event1 in Lyles/Ong. Decode is optional: omit --decode for resource inspection alone. Compare members/tag_counts/events with RESOURCE-COUNTS.json and decodes with DECODE-RESULTS.json. Frame-byte ranges are in decompressedSWF. The code ignores scripts/external resources and does not reconstruct display/playback state.

The performed native run also preserved exact MP3 extracts locally through the repository's media guard, used the prior parser for tuple cross-checks, and rejected three malformed fixtures. The portable run does not purport to repeat those extra implementation controls or make an independent codec implementation. Header sample counts and signedSeekSamples remain separate from untrimmed decoder samples. No inference about original conversation or authentication follows from successful reproduction.
