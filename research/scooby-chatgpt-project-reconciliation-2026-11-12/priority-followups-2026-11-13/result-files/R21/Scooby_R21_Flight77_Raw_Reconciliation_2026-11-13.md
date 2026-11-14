# Scooby R21 — Flight 77 raw candidate versus engineering export

**Audit date:** 13 November 2026. **Mode:** ordinary GPT-6 chat / local computation; no Deep Research. **Branch:** canonical R21 (not R20 WTC access).

**Outcome: partial.** This report independently verifies the three preserved input files, verifies a structured flash-memory envelope in the candidate raw bytes, reproduces selected engineering-export cells and pressure/barometer conversion sensitivities, and explicitly stops before raw-word-to-export comparison. The specialized modified-Huffman decompressor and a verified producing RAPS run were not executed. Accordingly, no raw ARINC word has been recovered and matched to a CSV engineering value in this continuation. The prior N03 audit was not a raw decode either.

## 1. Exact inputs and provenance

Starting package: `Flight77_Reproducible_Audit_2026-11-12.zip`, 55,468,480 bytes, **SHA-256 `528cdb88a2010a66af9fd6f30ddfb6b048a49b0b1da15f2c754e079ffa5fc442`**, personal Library ID `libfile_9afb870a0e8c81919153b878881eb102`. Link: <https://chatgpt.com/library?file_id=libfile_9afb870a0e8c81919153b878881eb102&account_id=personal>.

| Internal bytes | Size | Verified SHA-256 |
|---|---:|---|
| `sources/American_77.fdr` | 25,165,994 | `18ad30f72f3d30e5958480252469a1780b51469c903a18c47761ed41fb3ac0f6` |
| `sources/AAL77_tabular.csv` | 19,618,136 | `70740505826cf97b4fd376a8c225f78c87b7b245f46a4dbbd44ce8c356631138` |
| `sources/757-3b_1.TXT` | 656,359 | `374b269812aece0ad75f182f7864a324cadef04e735ebb296ad8b0ebba107e64` |

All lengths and hashes were independently computed on extracted bytes, not taken merely from filenames or the manifest. Their chain to an original NTSB-delivered disc remains a provenance inference; no 2001–2009 agency checksum certificate was acquired. The archived raw source is the Wayback 12 February 2008 capture of `aa77fdr.com/source/American_77.fdr`, identified in the bundled `source_manifest.json`; the engineering CSV is an archived extracted member of `AAL77_tabular.zip`, and the printout is an archived candidate American Airlines database. These are **not** interchangeable artifacts or independent measurements.

A second, standalone Library PDF has the same report name as the ZIP's internal PDF but distinct PDF bytes: the standalone is 123,828 bytes, SHA-256 `349919ca8d9e749bc214ba8dfb6f30ddfb6b048a49b0b1da15f2c754e079ffa5fc442`; the ZIP member is 98,866 bytes, SHA-256 `334c1247fb99c800b56c85a3deb916d49bec9aa0c3beed60f2382aa3157014a8`. Both have 11 PDF pages and identical `pdftotext -layout` extraction in this environment. The PDF byte difference therefore does not establish a substantive report revision. The recorder/CSV/TXT hashes above, not these PDF names, control input identity.

## 2. Native envelope probe — completed, not decompression

`r21_verify_and_probe.py` locates `;EOH\r\n` in the raw candidate, observes one following ASCII space, and finds an exactly aligned payload starting at **zero-based byte offset 170**:

- payload length **25,165,824 bytes** = 192 × 131,072 = 384 × 65,536;
- 382 pages have the repeated first little-endian words **`0xFE6B`, `0x0008`**, a 4/5 alternating value, a 0/1 half indicator, **`0xBEEF`**, and the expected block index 0–191;
- physical pages **58 and 59** are entirely `FF` and contain no marker; they correspond to **block 29**;
- block 28's pages 56 and 57 retain 38,266 and 37,682 non-`FF` bytes respectively, last non-`FF` offsets 38,641 and 38,073. Their pattern is consistent with partially written areas but **does not certify where the recording stopped**;
- there were **zero unexpected page-header patterns** among the 382 non-erased pages.

These are directly measured byte/offset checks, not a vendor-validated interpretation of the page header fields. In particular the raw textual header's `CUR_INDEX = 28 19328 28 19072` is preserved as metadata, not converted into an event time or used to claim the two empty pages contain missing data. No Huffman codebook, bitstream-to-word map, memory read ordering or ARINC sync series was independently recovered. No checksum or ECC meaning is assigned to unidentified header bytes.

## 3. Reproduced exported cells and conditional conversion checks

The included `reproduce.py` was rerun and reproduced the N03 result. The CSV has **345 columns, 37,802 data rows**, of which **37,800 contain measurements**, and **4,725 populated one-second groups** with eight export rows per group. Physical lines 37,814 and 37,815 contain only the labels `09:37:45` and `09:37:46`: there are no populated measurement cells on these two lines. **The last populated group is `09:37:44`.** These are export-label seconds, not an independently measured impact clock. NTSB factual report pp. 3–4 distinguishes time correlation from recording and places its last recorded data at 09:37:44 EDT: <https://www.ntsb.gov/about/Documents/AAL77_fdr.pdf>.

| CSV physical line / group | Pressure altitude, col 5 | Baro no. 1, col 85 | Baro no. 2, col 86 | Basis |
|---|---:|---:|---:|---|
| 37,790 / 09:37:42 | 307 ft | 30.24 inHg | blank | actual export cells |
| 37,798 / 09:37:43 | 239 ft | blank | blank | actual export cells |
| 37,806 / 09:37:44 | 173 ft | blank | 30.23 inHg | actual export cells |
| 37,814 / 09:37:45 | blank | blank | blank | time-only row |
| 37,815 / 09:37:46 | blank | blank | blank | time-only row |

**Pressure altitude, conditional inverse mapping.** The database `ALT_COA` entry (TXT lines 1737–1752) gives signed 10-bit coarse ×128 feet at subframe 1–4, word 29 bits 3–12; `ALT_FIN` (lines 1754–1769) gives a separately signed 10-bit field at word 30 bits 3–12. Boeing's Rev G Note 3C, as recorded in N03 p. 5, directs omission of word 30 bits 10–12 for the usable fine part. The specification-aligned equation for an already-decoded 12-bit word pair is:

`pressure_ft = 128 * signed10((W29>>2)&1023) + ((W30>>2)&127)`.

**Illustrations, not observed raw words:** 307 ft could correspond to coarse=2, fine=51 (low-bit-zero example W29=8, W30=204); 239 ft to coarse=1, fine=111 (W29=4, W30=444); 173 ft to coarse=1, fine=45 (W29=4, W30=180). These pairs *invert the published CSV*, and thus **cannot establish any raw-to-CSV match**. Many alternative 12-bit words share the same relevant bits. For the last hypothetical pair, setting W30 bit 10 produces W30=692, which still yields **173 ft** under the Boeing-overlap rule but **301 ft** under a literal independent signed-10 fine-value sum: a **128-foot formula sensitivity**. The raw high bits are unknown. No runtime error is established.

**Barometer setting, conditional input encoding.** The CSV displays 30.24 and 30.23 inHg. Following the Boeing count/100 example (N03 p. 5), these correspond to hypothetical counts **3024** (`0xBD0`, octal `5720`) and **3023** (`0xBCF`, octal `5717`) respectively. Interpreting those *same bits* as literal three-nibble BCD yields nondecimal nibbles, at odds with a naïve reading of the database's `BCD` declaration (TXT lines 2812–2842). **Because no W147 raw words or production converter version are recovered, this is a potential mapping/version issue, not a demonstrated NTSB mistake.**

**Illustrative ISA calculation, not flight-height correction.** Applying the tropospheric standard pressure-altitude relationship with p0=29.9212598425 inHg, `H=145442.16 ft`, exponent `k=0.190263`, produces the following conditional *barometrically indicated* heights when a listed pressure altitude and barometer setting are treated as contemporaneous:

`station_pressure = p0*(1-pressure_alt/H)^(1/k)`;
`indicated_alt = H*(1-(station_pressure/baro_setting)^k)`.

| Input pressure altitude | Assumed contemporaneous baro setting | ISA-only indicated altitude |
|---:|---:|---:|
| 307 ft at 09:37:42 | 30.24 inHg | 599.310 ft |
| 173 ft at 09:37:44 | 30.23 inHg | 456.456 ft |
| 173 ft at 09:37:44 | 30.24 inHg (alternative/stale No.1) | 465.580 ft |

The last two illustrate about **9.12 ft sensitivity to a 0.01-inHg setting change**. This equation and values are a standard-atmosphere illustration only. They are *not* a calibrated aircraft height above the Pentagon or terrain, do not control static-system errors, altimeter temperature, sensor validity, ground elevation or sample phase, and cannot establish physical trajectory or impact timing.

## 4. Decoder/version gate and exact missing links

The original NTSB report (Sarah McComb, Jan. 31, 2002, DCA01MA064, printed p. 3) says the stream was compressed using a **modified Huffman encoding scheme** requiring manufacturer or equivalent software. It says the data were then processed by NTSB RAPS and correlated to EDT in a separate Time Correlation Report. That report was not available here. This prevents treating the engineering CSV's time labels as direct aircraft clock words.

N03's manifest identifies author-decoder source ZIP `Stutt_Decoder_Source.zip`, reported 803,666 bytes and SHA-256 `1f2322c484737fcd0263e4d5d8e0862c97da2c74121da883dd4238b443055548`, at <https://web.archive.org/web/20130205114141id_/http://warrenstutt.com/AAL77FDRDecoder/Source/AAL77FDRDecoder.zip>. Its main project reportedly identifies application version 1.10.0.0 with a backup 1.7.0.0. The original code was **not recovered as intact executable/source bytes in this runtime**, so no claim is made that this hash or code was independently verified or that either version was run. A browser retrieval returned an unusable binary-as-text rendering and was not treated as a source copy. A source-release link and a prior static inspection are not execution records. In particular, no exact input-hash → build → configuration → decoded-words → CSV-output evidence has been supplied.

**Version sensitivity:** N03 reports that the author changelog changed acceleration formulas in version 1.1 to better match the NTSB CSV, added a separate TXT-based pressure-altitude variant in version 1.4.1, and added raw coarse/fine pressure outputs in version 1.7. Thus even a numerical match from a later author build would not be an independent calibration of the original RAPS conversion. A numerical version-to-version delta cannot be attributed without the verified executable, exact revision and a logged run on this candidate input. The formula-level 128-foot example above is illustrative sensitivity, not an observed difference between versions.

The audit cannot yet perform its decisive raw-to-CSV comparison. The **first technical missing link** is executable/documented reconstruction of the modified-Huffman format and the flash-page chronological readout, including sync-loss/partial-page handling, followed by validation using known ARINC subframe sync patterns. Only then can a fully qualified word key (frame, subframe, word, bit range, raw value) be compared under both Boeing and AA conversion interpretations to the corresponding CSV cell. Even that *equivalent* decoder would not prove historical RAPS behavior without a matching production run.

**Separate installation and event gates:** the generic `D226A101-3`/AA database slots identify potential door SF3 W251 bit 1, barometer SF2/SF4 W147, and unconfirmed radio-height slots, not N644AA's actual installed switch, wiring, fault response or sensor calibration. The NTSB I-1–I-4 validated/I-5–I-13 unconfirmed distinction is controlling; door/GMT/radio height must not be inferred from a label or constant bit. The independent Time Correlation Report, radar clock/site/target joins and terminal physical-calibration chain are not obtained. The official 2002 Flight Path Study's impact estimate is partly FDR-dependent and is not an independent radar-only clock.

## 5. Discrepancy register and conclusions

| Item | Reproduced result | Evidentiary interpretation |
|---|---|---|
| Raw candidate structure | 384 equal-length aligned pages, 382 consistent markers, two erased pages | Native byte organization verified; **not decompressed** |
| Pressure formula overlap | Same hypothetical word pair can yield 173 or 301 ft under competing interpretations | **Conditional** 128-ft sensitivity; no observed production error |
| BARO printout | Hypothetical 3023/3024 counts conflict with naïve 3-nibble BCD | Runtime version/scaling question; not raw discrepancy |
| Pressure/setting sensitivity | ISA illustrative 456.456 vs 465.580 ft at the final export group | ~9.12-ft conditional sensitivity; not geometric height |
| Export endpoint | 09:37:44 populated; 09:37:45–46 empty | No extension of recorded measurements or derived impact time |
| Raw-to-export reconciliation | **0 independently matched raw words** | Decisive computation still outstanding |
| Door and radio height | Configuration labels only; I-8/I-10 unconfirmed | No physical sensor-state claim |
| Radar/FDR clock | Missing Time Correlation Report, radar dictionary and independently validated join | No validated terminal-time/trajectory inference |

**Bounded conclusion:** verified source bytes and a coherent flash-page envelope support the existence of substantial genuine-looking recorder-format content in the archived candidate; they do not authenticate original NTSB media independently, decode the flight, establish an impact trajectory/time, or validate the cockpit-door and radio-height installation. The remaining computation is technically specific and reproducible once a verified decompressor source and producing configuration can be obtained. Nothing in this audit establishes fabrication, suppression or an impossible path; neither does it establish full raw-to-engineering agreement.

## 6. Reproduction commands

```sh
# This report's independent byte-identity, raw page and conditional conversion probe:
python3 r21_verify_and_probe.py /path/to/Flight77_Reproducible_Audit_2026-11-12.zip --output r21_results.json

# The previously supplied N03 script was rerun separately from the ZIP's extracted directory:
python3 reproduce.py --output recalculated.json
```

`r21_results.json` is the actual machine-readable output. The script intentionally fails on any input checksum mismatch. No native decoder, historical RAPS, external contacts, records request or fee was used.
