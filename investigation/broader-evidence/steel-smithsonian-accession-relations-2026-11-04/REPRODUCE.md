# Reproduce the source and field checks

The five EXPORT-*-2026-11-04-source.jsonl files are exact reviewed CC0catalog rows: four new inputs and one reused comparison. CATALOG-SOURCE-MANIFEST.json gives bytes, lineSHA256 and each sourceURL/entitySHA/line/offset. They are not the original accession/loan/negative or physicalsteel, and the source's metadata rights do not grant image rights.

Verify the small published copies without downloading bulk data:

```sh
python3 -B verify_catalog_copies.py --directory .
```

To reproduce the complete captured-entity checks, obtain the exact d7.txt/75.txt/9a.txt/cf.txt snapshot entities listed in SOURCE-PINS.json, resolve the stored inputs through the repository's Intelmedia guard, and use a new result path:

```sh
python3 -B verify_accession_records.py --shard-dir SHARD-DIRECTORY --comparison-record EXPORT-nmah_1182951-2026-11-04-source.jsonl --output NEW-VERIFICATION.json
```

The latter checks entire entitysize/SHA256, one exact targetkey and line/offset/length/SHA in each respective shard, metadataCC0/Images flags and the specific public statements reported here. The source URLs are mutable; a changed future snapshot must fail the frozen checks rather than be silently rehashed into agreement. Preserved exactrow copies permit record/field review even if the live snapshot changes; fullentity authentication then requires the matching original entity.

The prior32-sample identifier-routing test was reused, not rerun as fresh evidence. Sourcehash equals SHA1(identifier) for the selected records; that is not a content authenticity signature. No code writes sourcefiles, retrieves images, interprets historicalcause or authenticates currentcustody. A successful count/check proves only the stated capture/field correspondence.
