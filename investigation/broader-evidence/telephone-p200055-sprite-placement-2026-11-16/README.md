# Static placement audit of the court Flight 93 call-summary file

November 16, 2026 · TEL02–TEL04 / AUD016-A1. A static inspection of the court's `UA 93 Calls.swf` finds three time characters and two duration characters placed on matching horizontal coordinates inside one sprite. This supports a **2/3/3** sequence in that file's static structure; it is not a played-back or visually rendered court frame, an authenticated carrier record, or proof of a particular historical call.

## Input and method

The [court's P200055 archive](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200055.html) was [previously acquired and pinned](https://github.com/AveLyra/911-conspiracy-investigation/blob/bf46236c949033a54d8ec6d52007ad95070388d1/investigation/broader-evidence/telephone-p200055-court-bundle-2026-11-16/README.md). ZIP SHA-256 `3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801`; uncompressed `UA 93 Calls.swf` SHA-256 `9b6703c286cc4e5be8de36728c10bc0fc60dc54e4b732898ba4d4fbfda2fec5e`. Both were re-used without running the archive's launchers or SWF scripts.

The supplied [static-text probe](extract-static-text.py) reads DefineFont2 and DefineText tags and associates character IDs **870, 871, 873** with time strings **09:42:25, 09:42:03, 09:42:45**, and IDs **559, 872** with **3 SECONDS, 2 SECONDS**, respectively. The [placement probe](inspect-sprite-882.py) reads PlaceObject2 records inside DefineSprite **882**, at its local **frame 20**. In SWF twips, it finds:

| Time character | Time | Time translation (x, y) | Duration character | Duration translation (x, y) | Decoded duration |
| ---: | --- | --- | ---: | --- | --- |
| 871 | 09:42:03 | −3677, 10983 | 872 | −2302, 10983 | 2 seconds |
| 870 | 09:42:25 | −3677, 11361 | 559 | −2302, 11361 | 3 seconds |
| 873 | 09:42:45 | −3677, 11739 | 559 | −2302, 11739 | 3 seconds |

Each time and duration shares the same local y coordinate, and duration labels are to the right. This is a structural placement relationship in the source file. The earlier [third-party exhibit image](https://github.com/AveLyra/911-conspiracy-investigation/blob/a554abb6f2957b23c9d455b1bca204ca289d7578/investigation/broader-evidence/telephone-grandcolas-exhibit-image-2026-11-16/README.md) independently supplies a visual layout comparison and shows the same times and values; the image's chain to this exact file remains unverified. It is not an independent carrier measurement.

## Limits and reproducibility

The parser is a small, purpose-limited research tool, not a certified Flash implementation. Local frame 20 and placement coordinates do not prove that this sprite was played or visible at a particular court session. The probes do not execute ActionScript, validate parent transforms, identify a stage screenshot, or compare native call data. `python3 extract-static-text.py /path/to/flights.zip` and `python3 inspect-sprite-882.py /path/to/flights.zip` reproduce the selected text and placements. Original file bytes, earlier reports and both **2/3/3** briefing/image and **2/3/2** NPS values remain preserved. The NPS entries provide only minute-level headings; the row-by-row relationship and reason for the difference remain open. [Prior comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/2b5dc2a71fda41aee52b9e1f1a5bc7eb5bcd1fba/investigation/broader-evidence/telephone-grandcolas-short-attempts-2026-11-16/README.md).

**TODO:** independently validate the court file through a safely rendered frame and locate the source-to-exhibit, NPS, carrier-field and clock records. No original call audio or network record was obtained; this test cannot establish conversation, fabrication, suppression or motive. The report is additive and leaves earlier source records unchanged.
