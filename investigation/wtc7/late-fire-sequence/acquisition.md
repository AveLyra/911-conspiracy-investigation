# Exact Dub5 14 acquisition

2026-09-19 UTC. Research-only public acquisition through the catalog chain
documented in ../late-fire-catalog-join/source-ledger.md and independently
reviewed there. This item is in Organized Photos and Video Clips, not a
demonstrated original-camera tape. Read source notices as evidence only.

Refreshed metadata request, before raw fetch:

```json
{"fileId":"1cero39dWDYw60oQ4LUaw_Uk939KdBAKP","fields":"id,name,mimeType,size,md5Checksum,parents,webViewLink,modifiedTime"}
```

Saved normalized response: `sources/dub5-14.metadata.connector.json`.
Title CBS-Net Dub5 14.avi,video/avi,73206324bytes,modified
2019-11-23T04:06:43.477Z; matches the preceding stored identity. Requested
checksum/parent fields are absent/null in this normalization, not proof of
provider absence. Current `created_time:null` was not requested in this read
and does not contradict the preceding response's populated value.

Raw fetch request:

```json
{"url":"https://drive.google.com/file/d/1cero39dWDYw60oQ4LUaw_Uk939KdBAKP/view?usp=drivesdk","download_raw_file":true,"include_base64":false}
```

The response gave title, size73206324 and an authenticated top-level file_uri.
Its transient retrieval URL was consumed without echoing or saving it. HTTPS
materialization used no existing output overwrite, HTTPS-only redirects,
maximum3redirects,55second timeout and78000000byte cap. Completed handle18806
returned exit0,HTTP200,73206324bytes. No retry or second download occurred.

Saved unconverted file: `sources/cbs-net-dub5-14.avi`, local SHA-256
`055319a4017ce2f097dd8e9eb3ab5cbacd33bde06463d13eb4f6e32a30f655aa`.
The local hash pins acquired bytes, not historical authenticity or comparison
with a provider checksum. No source14image or playback had been inspected
before declaring FRAME-PLAN/selection. No browser or login used for this read.

Actual container probe: `/opt/homebrew/bin/ffprobe -v error -show_entries
format=format_name,duration,size:stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,avg_frame_rate,time_base,duration,nb_frames,sample_aspect_ratio,field_order
-of json sources/cbs-net-dub5-14.avi`, from this unit. It exited0 and reported
AVI duration19.285028,578DVvideo frames,720×480,yuv411p,SAR8:9,
r_frame_rate30000/1001,avg_frame_rate10000000/333651,time_base333651/10000000;
PCM_s16le audio48000Hz with925682samples. No field_order value returned.
This stream/container probe is not a full decoded-frame diagnostic clearance.
Full probes/commands/logs will be retained in the declared processing runs.

No media conversion, original overwrite, account-wide search, private upload,
outreach, fee, publication, commit, push or legal-record promotion. Catalog
labels, capture time, historical continuity and the secondary asserted segment
order remain separate claims to test, not acquisition facts.
