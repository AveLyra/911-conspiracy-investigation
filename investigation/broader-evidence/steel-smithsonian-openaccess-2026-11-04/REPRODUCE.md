# Reproduce the record extraction and integrity checks

The institution's public repository README links its AWS export and the NMAH index. Use only explicitly listed sources, not an API key or a retry of denied catalog pages. The three captured entities are00.txt(schema control),58.txt(column) and68.txt(photograph); SOURCE-PINS.json gives their exact URLs, bytes, checksums and snapshot headers. These are public metadata snapshots, not current custody or unrestricted image rights.

Resolve any stored data through the repository's verified Intel media guard before execution. Preserve the downloaded entities unchanged. The verifier performs no network access or media operations and creates a new result file:

```sh
python3 -B verify_export_records.py --sample-shard SAMPLE-00.txt --column-shard COLUMN-58.txt --photo-shard PHOTO-68.txt --output NEW-VERIFICATION.json
```

It checks complete entity size/SHA256;32sampled identifier-hash relationships; exact target key, line number, byte offset, line length and SHA256; single matching record in each respective shard; and each record's metadata-usage field. It also illustrates in a synthetic in-memory control why a hash computed only from the identifier cannot authenticate other content. No source record is rewritten and no historical alteration is implied.

Routing uses the observed namespace `edanmdm:` with a colon. SHA1 of`edanmdm:nmah_1182951` begins58; SHA1 of`edanmdm:nmah_1462757` begins68. This relationship was tested for the32samples and2targets, not certified for every institutional record. The source's`hash`, the uninterpreted`docSignature`, HTTPETag and our full-entity/lineSHA256 have different evidentiary roles.

Public EXTRACTED-FIELDS.json contains selected exact values/pointers and declared excerpts. It omits unrelated biography/name material and is not a complete source record. The raw matched lines remain local preservation originals. No image, object mark, physical specimen or signed transfer was examined. A passing metadata check does not establish the original attribution, recovery, custody, capture location or cause of damage.
