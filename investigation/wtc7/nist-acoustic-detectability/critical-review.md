# Bounded wording and evidence review

2026-09-20 UTC. Research-only computational review, not an acoustic expert
opinion, historical-audio review, or third independent full-page reading.

## Scope and actual checks

Read current main AGENTS.md, WORKFLOW.md, START-HERE.md and the full investigation
CHARTER; applied evidence-falsification and source-of-truth skills. The PDF
skill's distinction between text inspection and complete-page visual verification
also applies: **no PNG was displayed by this reviewer**. I read PROTOCOL.md,
root-reading.md and report.md completely, then the existing text extracts for
physical pages 333, 400, 401, 772 and 775 (printed 289, 356, 357, 706 and 709).
I did not read the other reader's findings, open earlier Appendix D phases,
decode/hear media, run a solver, acquire sources, or change main/source files.
The page-text dumps included incidental operational context on selected pages;
that context was not used for this review and is not reproduced here.

Actual commands were read-only `cat` for those named controls/notes/extracts,
`rg --files` for this unit's inventory, `shasum -a 256` for the items below,
and `rg` for the exact reviewed phrases and render diagnostics. Initial combined
output was truncated, so controls and relevant notes were reread separately.
A broad diagnostic display was also truncated; the subsequent bounded commands
`rg --no-filename 'Fontconfig.*' render01/*-render.stderr | sort -u` and
`rg -l 'Fontconfig error' render01/*-render.stderr` completed, reporting the
default-configuration-file and nonwritable-cache categories in all nine render
stderr files. This is not an exhaustive diagnostic or pixel-integrity audit.
Root's recorded visual readability decision remains inherited, not independently
reproduced here. The warnings have not been erased or reclassified as clean.

Reviewed snapshots / SHA-256:

| File | SHA-256 |
|---|---|
| PROTOCOL.md | ea6bcc9ee92aeef7a1d89799401bc5ddfa82e19956d826853422abd65741fa55 |
| root-reading.md | b9098522cc426b592b9e12bdd30d63c51b0d43764ffbf017b1c5d23dfa80006f |
| report.md, before requested wording corrections | ef7cae90dca444f35ba8db1cbdba02f8bcca3956c2c2f95a074b3929926d8934 |
| render01/p333.txt | 1e71957e582b38937f154eedc31bd8ac2c83f88271d73ce36a0c75a74bfdbd6f |
| render01/p400.txt | 328d328ea7255d18e7c9d231d3dcd802e19b66b539dd5c19e20a4f7c6d625d95 |
| render01/p401.txt | ac5707cfdd1b265e017026953cea3f5cf5c5cb6d9d0032680fff9e6ae3690bbf |
| render01/p772.txt | 6820aa0333d79c94c2025f26f1bc99154aaada9d8a4a6cafa77548a2f2362b14 |
| render01/p775.txt | b80bb6ec07998ce6c12012256ea8dacbe543fadcf8c0b20ec97d4fcc6a7c7d45 |
| Main authority/nist/wtc7/ncstar-1-9.pdf | 30addb2699370f89e40bccfdcf4b4a18a7f4fb3bc1c0101bd3fcdec9b892b18f |

The held PDF hash matches the protocol. Hashing does not establish historical
authenticity, extraction fidelity or complete-page coverage. This review does
not certify the renderer, receipt inventory, plots or their digitization.

## Corrections

1. **Moderate, observation-versus-inference distinction.** The ledger rejects
   “No pre-global-collapse sound occurred anywhere in those recordings” because
   “The third recording's reported early reaction contradicts this reading.”
   Printed page 289 reports a listener response and attributes it to hearing the
   penthouse collapse. A reaction and NIST's hearing attribution do not by
   themselves establish a separately identified sound in the recording. Smallest
   correction: reject “NIST reports no pre-global-collapse audible activity or
   listener response at any reviewed location,” and explain that this conflicts
   with NIST's reported early response/hearing attribution. Keep that attribution
   distinct from independently verified recording content. Label this as a
   possible overbroad summary, not NIST's actual claim of no sound whatsoever.
2. **Minor, event definition.** Change the support paragraph's “pre-collapse
   event” to “pre-global-collapse event.” Penthouse descent and global collapse
   are different events in the cited discussion.
3. **Minor, source wording.** Replace “Quiet nearby background capture” with
   “Reported low-level background capture.” Page 289 includes distant sounds;
   nearby operators are described separately. The existing warning that this
   does not calibrate distant low-frequency detectability should remain.

## Substantive disposition

No other material objection to the central conditional conclusion within this
text-review scope. Its strongest support is the combination of identified
recordings, reported background capture, waveform/time-delay consideration and
an explicit modeled sound prediction. Lack of laboratory calibration does not
logically reduce all qualitative negative evidence to zero. Its strongest
objection is the unvalidated bridge from the simplified propagation prediction
to the actual obstructed receiver paths and recording chains. The report
correctly preserves the counterargument that the predicted signal might retain
a large detection margin despite attenuation; it has not measured that margin.

The report neither shows that an event could be hidden nor independently
validates the modeled source family as an exhaustive lower bound for every
intervention. Those two limitations must stay separate. Its model/observation
distinctions, rejection of causal identification from a rumble, and refusal to
infer concealment or numerical odds are appropriate. Narrowing an acoustic
exclusion is not affirmative evidence of intervention or a falsification of the
fire sequence. Same-report sections are not independent corroborating sources.

The next documentary test is warranted as a bounded lead, not established
availability: search already-held inventories/productions for the two exact
page-357 footnote references, Applied Research Associates to NIST dated
31 July 2008 and Loizeaux Group International to NIST dated 5 August 2008.
Then inspect any located non-operational urban-propagation/detectability support
with provenance. Evidence of relevant measurements or a validated receiver-path
bound could strengthen the negative inference; unsupported analogy or inapposite
conditions would leave or sharpen its limitation. A bounded failure to locate
the emails would not establish nonexistence. An acoustic-working-file extension
should remain explicitly limited to Phase III/detection questions, not earlier
operational derivations. No such search was performed in this review.

Only this new working review note was written. No authority promotion,
source modification, legal finding, release, or independent-reader exchange is
authorized or claimed by it. The report owner should record disposition and
pin the revised report; this review does not silently certify future revisions.
