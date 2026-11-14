# R08 recovery ZIP parts

GitHub rejects individual files over 100 MB. The original Scooby_R08_Native_Recovery_2026-11-14.zip is 279,511,104 bytes, so it is preserved here as four ordered parts. The full extracted bundle is also preserved under `../native-recovery/Scooby_R08_Native_Recovery_2026-11-14/` for browsing.

Reassemble from this directory:

```sh
cat Scooby_R08_Native_Recovery_2026-11-14.zip.part-* > Scooby_R08_Native_Recovery_2026-11-14.zip
shasum -a 256 Scooby_R08_Native_Recovery_2026-11-14.zip
```

The expected SHA-256 is `513dd716ee4c7df578dcc1e514be0583cc134cee9b8d2405368b4ee602622e6a`. Each chunk's size and SHA-256 are in `parts-manifest.json`.
