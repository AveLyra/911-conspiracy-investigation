# K90-39: exploratory speech-recognition timing probe

2026-11-25. This bounded experiment follows [K90-39 audio acquisition](https://github.com/AveLyra/911-conspiracy-investigation/blob/636ebf4c24544338203528a18006ab5cdb662d8b/investigation/broader-evidence/faa-cape-audio-index-check-2026-11-25/README.md). **Neither the recognition output nor file duration establishes the recording's real-time coverage.**

## Method and observations

From the acquired [NARA K90-39 MP3](https://catalog.archives.gov/medialz/dc-metro/rg-237/7419198-9-11-faa/5-Miscellaneous/b-Voice-Recordings/5-K90-39-High-AR-1230-1400-UTC.mp3), SHA-256 `6c8c16d52e09fea2877dd798dbbffd6823e626f09f58cadf022d05b7425a9b37`, FFmpeg 7.1.1 extracted two 90-second mono 16-kHz WAV clips at file offsets **0** and **2700 seconds**. Clip hashes: `f79a65262375c862d1e5777051e7b57abece661f46c704ebe52a0f2bf05a7fa2` and `454995c25d5fab90602cf1099de2b53bc62616b964bf64779d75adf6cc879f01`. Both clips and source are retained in the verified project media store.

Whisper.cpp 1.9.2, CPU, `-ng -t 4 -l en`, using [ggml-tiny.en.bin](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin), SHA-256 `921e4cf8686fdd993dcd081a5da5b6c365bfde1162e72b08d75ac75289920b1f`, produced an opening segment that **appears in the model output** to describe a HIGH sector re-recording covering **1230 to 1600 UTC on September 11, 2001**. This is an automated hypothesis requiring direct listening and transcription, not a verified statement in the recording. Later model segments contain apparent recognition errors, demonstrating that the output cannot be treated as a reliable transcript. Raw model outputs are retained locally with the research notes.

The model's proposed **1230–1600** range, the NARA file title **1230–1400**, and its cassette description **1230–1315; 1345–1400** are distinct, potentially conflicting descriptions. Preserve all three and their provenance. The output may be a misrecognition, a general announcement for a larger collection or another explanation; none has been tested. A supposed announcement would not, even if verified, establish that this particular MP3 includes the entire announced period. The 2700-second file offset is not a demonstrated **1315 UTC** position.

## Next discriminating test

A human or independently validated transcription should listen to the opening and capture exact words and uncertainty, then identify timestamp announcements at multiple offsets and compare with the actual audio, original DAT/re-recordings and any tape index. Test whether the suspected 1315–1345 UTC interval is present, absent, repeated, or not alignable; do not equate silence with missing data. The model probe cannot determine these alternatives, resolve the separate 1538–1540 tape-change gap, or establish motive. The FAA corrected answer and administrative-disposition records remain open TODOs.

## Reproducibility

Clip extraction used `ffmpeg -ss OFFSET -t 90 -i SOURCE -ar 16000 -ac 1 CLIP`; the offsets above are seconds. Each clip was processed with `whisper-cli -ng -t 4 -l en -m MODEL -f CLIP`. Exact outputs, model and audio remain separate from this public analysis. This pass did not include human listening, clock synchronization, source-tape comparison, audio authentication or end-to-end continuity testing.
