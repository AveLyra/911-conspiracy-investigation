# Reproducibility correction: first P200055 SWF text IDs

November 16, 2026 · AUD016-A1 / TEL02–TEL04. The [previous report](https://github.com/AveLyra/911-conspiracy-investigation/blob/85f6ab2ff0e3ff9c90e645a899f6a63557ec823e/investigation/broader-evidence/telephone-p200055-sprite-placement-2026-11-16/README.md) says its supplied static-text probe associates character IDs with the selected strings. **Correction:** that published probe prints selected strings without character IDs, so the stated ID-to-text association cannot be verified from its printed output alone. The separate placement probe prints IDs and positions but does not itself establish the string for each ID. Preserve the earlier report unchanged.

## Reproducible follow-up

The accompanying `id-probe.py` adapts the [later second-member text probe](https://github.com/AveLyra/911-conspiracy-investigation/blob/e3ecb7eaf74ca07837ed0f6dbdf906610d880f56/investigation/broader-evidence/telephone-p200055-second-swf-2026-11-16/extract-static-text.py): it changes the ZIP member name and selected ID set only. It does not execute the SWF. Run `python3 id-probe.py /path/to/flights.zip` against the [court P200055 archive](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200055.html), ZIP SHA-256 `3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801` (archive previously acquired and hashed; source pin [here](https://github.com/AveLyra/911-conspiracy-investigation/blob/bf46236c949033a54d8ec6d52007ad95070388d1/investigation/broader-evidence/telephone-p200055-court-bundle-2026-11-16/README.md)). The run returned 15 fonts, 420 nonempty text tags and zero reported parsing errors, then:

```text
character 559 '3 SECONDS'
character 870 '09:42:25'
character 871 '09:42:03'
character 872 '2 SECONDS'
character 873 '09:42:45'
```

The supplemental run supplies the missing ID-to-text output and agrees with the earlier report’s stated association. It is not an independent decoder, visual playback, or a carrier record. The original report's **2/3/3** and the NPS account’s **2/3/2** remain separate observations, with the row join unverified; neither source establishes intent or falsification of call records. Source archive and earlier report were not modified.

## Checklist and open work

- [x] Re-run published probe and confirm it omits character IDs; preserve the original description and script.
- [x] Provide a separately named ID-printing probe and record results.
- [ ] Independently decode or safely render the court exhibit and establish stage visibility and source-to-exhibit chain.
- [ ] Obtain NPS source-to-row documentation and original carrier fields and clock information.

This report is additive. The earlier document is unchanged; this correction describes its reproducibility limitation rather than silently changing its wording. The supplemental probe was not independently validated against a certified decoder.
