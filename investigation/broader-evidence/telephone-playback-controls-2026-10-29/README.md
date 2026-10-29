# The two selected sound resources have explicit script references; their actual playback remains unverified

The selected **soundID1** resource in each of Lyles.swf and Ong.swf is exported, and each file contains a short action record that pushes that exact export symbol and the **attachSound** method label before a CallMethod instruction. This establishes a **stored presentation-level reference path**, beyond a filename association. It does not establish that the call site ran, who spoke, which historical call was recorded, or how much audio was played.

This follows the [preceding resource/decoder study](https://github.com/AveLyra/911-conspiracy-investigation/blob/3b1c9b18434e58faef2e7f22b4e457af387d856c/investigation/broader-evidence/telephone-court-audio-resources-2026-10-29/README.md). Its original audio/header/decoder counts remain unchanged. This unit advances **AUD016-A1 / TC05-B105 / TC06-B110 / TEL02** only at the court-presentation reference layer. Native carrier, recipient and custody joins remain open.

## Original and bounded method

Source: the unchanged [court-distributed flights.zip](https://coop.vaed.uscourts.gov/moussaoui/flights.zip), linked from the [P200054 exhibit page](https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200054.html). ZIP SHA-256 **3a1e08b2276dcf0f1bdf5a7071113314776aca4660d73d0cf42fd91f92296801**,28,304,524bytes; acquired October27,2026,13:40:38.310051UTC. Only **Lyles.swf and Ong.swf** were inspected in this unit; their complete source/member hashes are in [SOURCES.json](SOURCES.json). Every offset below is zero-based in the **uncompressed SWF**, not in the ZIP.

We parsed StartSound15, DefineButtonSound17, StartSound2-89 and ExportAssets56, including nested sprites. Optional SOUNDINFO flags/fields were decoded from the [mirrored AdobeSWF19 reference](https://open-flash.github.io/mirrors/swf-spec-19.pdf), printed179–181/199–200. Two table images were viewed; the other named passages were read as extracted text, not all243pages. The renderer emitted a Fontconfig warning but returned0 and produced legible pages. One later text-read command used a wrong local path; correction re-opened the existing, unchanged reference, without a new download or claimed source disappearance.

The28DoAction containers were then checked for exact export-name bytes; just one matching block in each file was selected, **79bytes and77bytes**. Only action boundaries, constant pools and serialized Push values were parsed. No ActionScript executed, stack/control flow was emulated, nested function expanded or button action decompiled. All non-whitelisted strings remain length/hash locators in the public data.

## Standard controls reference a different, shared sound resource

| Member | Standard StartSound / StartSound2 tags | DefineButtonSound records | Nonzero sound IDs in those records |
|---|---:|---:|---|
| Lyles.swf |0 /0|4|224 in all four|
| Ong.swf |0 /0|2|345 in both|

All six nonzero transitions use SOUNDINFO flags **00**: no explicit stop/no-multiple/in/out/loop/envelope flags. This statement concerns those records only. It neither establishes an unlimited recording nor excludes other script controls.

The referenced IDs224/345 correspond to the small byte-identical payload identified in the preceding study, not the selected large soundID1 resource. Their exact role is not assigned without a relevant state/semantic test. Thus the earlier resource count and these button records must not be counted as separate call recordings or independent evidence. The six button records do not provide an actual in/out interval for soundID1.

Locators: Lyles button IDs225/228 at offsets3028709/3028983 (root local frame32),245/246 at3034212/3034335 (frame36). Ong button IDs346/349 at680552/680759 (frame32). Each nonzero sound is transition-index2. [CONTROL-RESULTS.json](CONTROL-RESULTS.json) preserves every zero/nonzero transition, field, body hash and local frame locator. Button IDs and local frame ordinals do not prove which UI control was shown or clicked.

## Exact export and script-source associations

| Member | ExportAssets tag | Exported ID | Export-name SHA-256 | Matching DoAction tag / body bytes |
|---|---:|---:|---|---|
| Lyles.swf |540776|1|952773814e020b4cfa2841a910cd34afb8c79c82771315c538b8998a20721e77|540803 /79|
| Ong.swf |492897|1|a395b90e8233379313ed689cb99a1657ff127391caa9acda718f1771badf4745|492922 /77|

Both action blocks contain ten top-level records. Their constant pools include a variable-name string (hashed in the data), Sound, the exact exported symbol and attachSound. Lyles pushes the export symbol at **body-relative action offset58**; Ong at **56**. Each block then has GetVariable, a push of attachSound and CallMethod at respective body-relative offsets **76/74**. The export-string hashes are matched to the source export entries; the numeric argument-count literal1 and constructor field containing zero-valued double bytes are retained as serialized fields. We did not run or symbolically evaluate the instructions, infer a returned object, or certify runtime method success.

This is a real source-level association, with a concrete adverse limit: an exported resource and call site may exist even if a particular state was never entered or a later control changed/stopped playback. These files are court presentations and may contain prepared excerpts. The source association does not authenticate a native recorder/carrier master or original caller identity.

[EXPORT-ACTIONS.json](EXPORT-ACTIONS.json) supplies all20selected action records, serialized values, body hashes and relative source positions. The source-defined frame-rate field is12fps for both files; their root frame counts are589/2942, matching the walked ShowFrame counts. These are presentation fields, not calibrated historical clocks or measured audio/conversation durations.

## What the further start-reference check did and did not find

A prospective second-block filter looked only for the exact variable bytes from the selected block plus the literal start method name in those same28DoAction containers. **No matching block was found in either file**, so no additional block was parsed. That narrow literal criterion can miss inherited pools, differently formed names, button/function containers or dynamic dispatch. It is not evidence that no start call exists or no audio played. [START-REFERENCE.json](START-REFERENCE.json) records the exact scope and zero-candidate result. No broader decompilation or playback was substituted when this route ended.

## Earlier count difference remains unchanged

The earlier Lyles resource declares/decodes **1,987,200samples at44,100Hz**, with SeekSamples0. Ong still declares **2,726,784**, emits **2,729,664** in the separate standalone decoding procedure at11,025Hz, and separately stores **SeekSamples1669**. **This is not an independent codec implementation**: FFmpeg/ffprobe share libraries, as the preceding report explains.

The new standard-control and export-reference observations **do not explain or resolve** the2880sample difference. No in/out value, offset compensation, duration normalization or controlling sample count has been assigned. Source/codec/authoring/playback alternatives remain untested. We have neither listened to the audio nor measured the actual played interval. A valid format/reference path is not historical call authentication.

## Reproduction and actual checks

Known optional-field/envelope and stop-only fixtures passed; five malformed SOUNDINFO records were rejected. A known local constant-pool/push fixture passed; three malformed action streams were rejected. Source/member/tag counts matched the frozen preceding census. These check bounded parsing, not universal validity or historical truth. The parser does not interpret code and shares bounded traversal helpers with the preceding study.

The portable [reproduce_controls.py](reproduce_controls.py) takes the original archive plus the **unchanged preceding resource helper** from the linked study. With both research directories from the same repository:

```sh
python3 reproduce_controls.py /absolute/path/to/court-flights.zip --helper ../telephone-court-audio-resources-2026-10-29/reproduce_resources.py > result.json
```

It emits control/export/action fields and hashes only; no raw strings outside the API whitelist, media extraction, audio decoding, playback or external request. The helper's exact SHA-256 is checked before import. Compare its controls/actions/start arrays with the three corresponding JSON files here; timestamps and method prose are not comparison targets.

The full inherited TEL01–TEL04 conflicts and all five-track/eighteen original-input requirements remain in [OPEN-TODOS.json](OPEN-TODOS.json). The next strongest authenticity discriminator remains native source-recording, exhibit-preparation and custody material. A separately scoped passive button-state or original preparation-record test could clarify intended playback; that test is unperformed. We will also continue the steel operational-record queue rather than turn this missing input into a global block.

This is an additive study. Previous source bytes, decoded outputs and reports remain frozen; [TEXT-CHANGES.diff](TEXT-CHANGES.diff) shows the new notes/code. [REVIEW-AND-CHECKS.json](REVIEW-AND-CHECKS.json) separates completed tests from unperformed work. Only research numeric/hash/method notes are public; raw archive/audio/PDF/images, personal/contact/account fields, private correspondence/strategy and credentials are excluded. No contact, fee, request/filing, mailbox, deletion, private push, merge, history rewrite or substantive-goal completion occurred.
