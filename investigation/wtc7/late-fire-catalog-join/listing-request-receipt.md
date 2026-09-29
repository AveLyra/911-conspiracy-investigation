# Scoped listing request receipt

2026-09-19. This receipt is reconstructed from the root tool-call history
after acquisition. It is not a provider-native request log or an earlier
preregistration. The connector response captures remain separate, unmodified
files under `sources/`; null `parent_ids` in them are not populated by inference.

The official NIST landing HTML links the Organized Photos and Video Clips
folder `17lDS4YslnUaOHv-x2CEhWLVzmceNllk1`. The saved
`nist-organized-root.connector.json` response lists its VideoClips child as
`1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn`.

The exact connector search arguments were:

```json
{"query":"CBS","item_type":"folder","best_effort_fetch":false,"special_filter_query_str":"'1mKqRTrMFX4VDnxW_-VU3pByhfqqs1uwn' in parents and trashed = false","topn":100}
```

Response capture: `sources/nist-cbs-folder-search.connector.json`. Its returned
folder entries explicitly identify the parent VideoClips ID. The next two
Google Drive `list_folder` requests were:

```json
{"url":"https://drive.google.com/drive/folders/1eCHR_lbdScxLb2F-LUJo_FOdXpo5kzFK","top_k":200}
```

Response: `sources/nist-dub5-listing.connector.json` (24 returned file entries).

```json
{"url":"https://drive.google.com/drive/folders/1h4A6pKPMjdJKyF4fQfkjmCOylQzeWAIB","top_k":200}
```

Response: `sources/nist-dub6-listing.connector.json` (49 returned file entries).
The response bodies do not themselves preserve those request URLs or explicit
file-parent mappings; this receipt supplies the recorded request context.
Returned counts are not proof that no other files or pages exist.

Individual metadata requests used the four exact returned IDs, with fields:
`id,name,mimeType,size,md5Checksum,sha1Checksum,sha256Checksum,parents,webViewLink,createdTime,modifiedTime,version,description,videoMediaMetadata,capabilities(canDownload)`.
The normalized output omitted several requested fields, including provider
checksums and video metadata. That is a limit of this captured connector
response, not proof that the provider has no such fields. Locally computed
SHA-256 values authenticate the acquired local bytes only, not a comparison
with an independently supplied historical or provider checksum.
