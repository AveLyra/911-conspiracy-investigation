# Reproduction and reading scope

Use Python with PyMuPDF. Download the six exact official URLs in SOURCES.json to a new source directory using the pinned filenames; obtain the pinned prior F04 PDF separately. Verify the entity SHA-256 values. Run:

```sh
python compare_sources.py --sources SOURCE_DIRECTORY --f04 AWA658.pdf --output NEW_OUTPUT_DIRECTORY
```

The script creates COMPARISONS.json, EXCERPTS.json and REPRODUCIBILITY.json and refuses a mismatched source, non-unique selected utterance or existing output directory. It does not access the network, edit inputs or listen to audio. The page-local sorted text lines are extraction locators; retained text-layer errors are not corrected. Compare selected results with actual page images; handwritten note/airbill readings and the qualifier comparisons were separately visually checked and are not an automated handwriting-authentication result.

All23 new pages and six relevant prior F04 page images were visually inspected. Original response entities, headers, full extractions, signature/contact/logistics details, source/page hashes and execution failures remain local. Raw transport headers and full pages are outside this public payload. No concealed field recovery was attempted.

Six frozen command/check-in candidate events are compared across four document/position versions; a seventh cross-position example is the second short Indy call within the local1256 sequence. Five relay/source candidates retain both sides. The associations are manual inferences from words, flight and sequence, not authenticated native event IDs. A selected sample cannot certify completeness or quantify the frequency of errors throughout the archive.

Text addition diffs and source/page integrity are independent from image reading, audio validation and remote publication verification. Source version dates, receipt requested, dispatch reported, sender airbill, delivered contents and corrected Commission response are different events. Keep every unresolved chain open.
