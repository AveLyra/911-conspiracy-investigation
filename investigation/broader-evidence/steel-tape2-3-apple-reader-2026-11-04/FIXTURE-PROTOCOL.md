# Actual fixture and execution protocol

The positive fixture was generated with installed FFmpeg7.1.1/libx264, with this exact argument template (the output was a fresh guard-resolved Intel MOV pathname):

```
ffmpeg -n -v error -f lavfi -i testsrc2=size=32x32:rate=1:duration=3 -frames:v 3 -an -c:v libx264 -preset ultrafast -tune zerolatency -bf 0 -pix_fmt yuv420p NEW_CONTROL.mov
```

A separate FFprobe run used `-select_streams v:0 -count_frames -count_packets -show_entries stream=codec_name,codec_tag_string,nb_frames,nb_read_frames,nb_read_packets,time_base,duration -of json`; it reported h264/avc1,3.000000s,and3/3/3. The deliberately invalid fixture contains the22ASCIIbytes `NOT_A_QUICKTIME_MOVIE` followed by LF. Fixtures were created only on verified Intel storage; no raw MOV is included publicly. Exact-byte reproduction with a different encoder build is not assumed.

Compile using the installed Apple toolchain:

```
swiftc -swift-version 5 -parse-as-library -module-cache-path NEW_LOCAL_CACHE -framework AVFoundation -framework CoreMedia -framework CoreVideo AppleReader.swift -o NEW_READER_BINARY
```

First resolve each input using repository tools/media_path.py. Invoke `NEW_READER_BINARY GUARDED_INPUT nil NEW_JSON` and `NEW_READER_BINARY GUARDED_INPUT argb NEW_JSON`. The actual harness bounded each process to240s, and code bounds output to20000buffers and metadata to16MiB. Actual source runs did not time out or hit the buffer limit. Preserve reader status and complete-versus-partial counts. Source/controls use video only; no media output is written. JSON output refuses an existing pathname.

Run `python3 -B analyze_reader_results.py RUN_DIRECTORY RESTORED_PREVIOUS_NATIVE_MAP NEW_ANALYSIS_JSON` against the five named raw logs and the previous original CRLF map recovered using its published envelope/restore script. The analysis expects the source/control filenames retained here. The byte hash in COUNTS-AND-TIMES.json identifies that exact map. No single software/interface result authenticates historical footage or completes the independent source decode.

Control identities:
[
  {
    "kind": "procedural3framepositive",
    "bytes": 2320,
    "sha256": "4d99495157834a3913d610c0868086adf05c7088bff41f315ce57fc6728e0bc1"
  },
  {
    "kind": "deliberatelyinvalidnegative",
    "bytes": 22,
    "sha256": "5ccc68b7a7c5148025fd220afb10a72c6ccbf0504cb3aea03d7d05edd132fb3e"
  }
]
