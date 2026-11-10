# Reproduce the separate tests

Use FFprobe7.1.1, with its installed MOV options checked before running. Resolve the historical movie through the repository media guard and verify SOURCE-PINS.json's exact source hash. Obtain the earlier11607row native map from its linked public report; its LF copy parses to the same row values as the retained CRLF original. Neither a map nor this code authenticates the camera or steel origin.

The new procedural control was generated with FFmpeg7.1.1 using these arguments (CONTROL.mov is a new guarded output):

```sh
ffmpeg -n -v error -f lavfi -i testsrc2=size=32x32:rate=1:duration=3 -frames:v 3 -an -c:v libx264 -preset ultrafast -tune zerolatency -bf 0 -g 1 -pix_fmt yuv420p CONTROL.mov
```

Its exact3182byte/hash and all-three-keyframe observation are pinned. Binary media are not in this public bundle; reproducing the exact fixture requires matching that hash, rather than assuming a different encoder/build produces identical bytes. A different fixture requires a separately labelled experiment.

Run the successful separate tail test into a new metadata directory:

```sh
python3 -B probe_tail_keyframe_control.py --source SOURCE.mov --control CONTROL.mov --native-map SAMPLE-MAP-LF.csv --output-dir NEW-TAIL-RESULTS --ffprobe ffprobe
```

The script imports the shared mode/hash/save functions from probe_editlist_options.py; keep the three code files together. Its source window is774%800 and control window2%4. The absolute end times exceed each source duration. Actual returned indices are the measurement scope, because seeking can start earlier. Each subprocess cap is120seconds. JSON/status logs are metadata; no image/audio output is requested. Do not run against a source whose bytes/hash or storage authority is uncertain.

The original full-source probe_editlist_options.py and unsuitable-control probe_tail_editlist_options.py are retained for method accountability. They did not complete the historical comparisons described in FAILED-ATTEMPTS. Do not describe their failures or partial counters as accepted counts. The first timeout's partial stdout was not retained; no invented replacement is supplied.

Every returned tail address/size is compared with the native map, common compressed packet hashes are compared across modes, and only the final three native payloads are independently read/hashed. This is not an independent whole-source decoder, calibrated camera clock or image-content comparison. On any failure preserve its log and leave the relevant acceptance open.
