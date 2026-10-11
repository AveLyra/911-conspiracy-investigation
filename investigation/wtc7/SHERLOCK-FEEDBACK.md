# Sherlock investigation feedback

**Purpose:** Actionable, deduplicated software feedback encountered under the [investigation charter](CHARTER.md), not a second product roadmap or a repository of case evidence.

**Destination:** Existing SHERLOCK task **Define Phase 0 invariants**, task ID `01a074ee-3dc0-7821-9125-aa8d9ffc2f8c`. Record notes there; do not create new tasks, external issues, or unsolicited implementation instructions by default.

**Current routing:** On October 9, 2026, the user expressly authorized sending the sanitized queue to the existing destination and recording acknowledgment. The direct send succeeded. The consolidated 27-item batch is **delivered and acknowledged in the destination log**, not implemented or verified fixed. Details and exact payload are in the delivery entry below. Earlier dated local-only statements remain accurate history, not the current routing state.

<!-- feedback-delivery-2026-10-09:start -->
## October 9 authorized feedback delivery

Batch **SFB-BATCH-2026-10-09** contains 27 consolidated acceptance extensions under existing SFB-002 through SFB-005, retaining SFB-001's resolved status. All 2,455 pre-delivery log lines were read in three complete partitions; root consolidated the themes and reviewed the exact outbound text, with a separate privacy/scope check. The raw log, case material, real source identifiers, private paths and attachments were not sent. Logging/triage only was requested, not implementation or investigation access.

- [Exact sent text](feedback-delivery-2026-10-09/outbound.txt): 28,070 bytes; SHA-256 `bd3f148bdfb1c5c4c55a33afbba0bedad7e3d3258c224754a12566925d61a740`.
- [Delivery and acknowledgment receipt](feedback-delivery-2026-10-09/receipt.json): send requested 12:55:56 UTC / 08:55:56 EDT. The app returned success for the exact destination; a subsequent snapshot confirmed turn `01a120bc-17ad-7c22-9d65-f95d545e7b2b`. Root then read the [saved acknowledgment](/Users/admin/dev/sherlock/FEEDBACK.md:6) and verified all 27 item IDs exactly once: 24 acknowledged extensions and items 15, 16 and 27 reported already covered. Those three coverage classifications are the recipient's dispositions, not independently verified implementation coverage. No clarification item was reported in the saved batch.
- The reopen attempt returned “no archived rollout found”; no successful unarchive is claimed. The subsequent successful send and running target establish actual delivery independently.
- Prior source-log SHA-256: `b15c8252d1de66034bd6778ef6185c9a345d1f597f358e5e412085ed3cd39c78`. Detailed dated recurrences remain preserved below; delivery of this consolidated digest does not mean the raw log was transmitted or every original sentence copied.

The destination turn completed with an explicit [acknowledgment reply](feedback-delivery-2026-10-09/acknowledgment.txt) covering items 01–27. Its reported repository checks included a timing-sensitive suite failure that passed when rerun alone; root does not certify a fully passing suite or feature fix from that report. The exact sent-file hash/size/item checks, pre-delivery source-log reconstruction, destination-history reconstruction and `git diff --check` passed. No fix, feature retest, activation, case transfer or scientific finding follows from delivery or acknowledgment. Other source-handling and human-review gates are unchanged.
<!-- feedback-delivery-2026-10-09:end -->

**October 8 reference-only acquisition recurrence, SFB-005, local only:** A
native raw-file fetch can return success, stated size/MIME and a `file_uri`
object containing an expiring download locator without a local materialized
file. The observed tool set supplied no identified native materialization
action. Extend existing acquisition-state and redact-before-display fixtures:
use a dummy reference-only response and require acquired-bytes=false until a
supported transfer produces a checked local artifact. Do not expose reference
values in diagnostics, infer source refusal from this local capability gap,
or mark an unattempted second item failed. Desired behavior is a supported,
privacy-preserving file-reference-to-local-artifact path with size/hash checks
and distinct referenced/materialized/admitted states. This is an observed
integration need, not a demonstrated Sherlock defect or tested product fix.
Generic response shape only; no real locators, file IDs, titles, case material
or private paths. Deduplicated locally, not sent, acknowledged or activated.

**October 8 byte-boundary and diagnostic-status recurrence, SFB-004/SFB-005,
local only:** A local append-log verifier falsely reported a changed snapshot
because it added a newline to a prefix that already retained its final newline.
Its shell wrapper then ran a successful final check, masking the first process
failure in the aggregate status. Synthetic reproduction: append a heading to
`"x\n"`, split immediately before that heading, and compare the exact prefix
with the original; adding another newline must fail. Separately, a failing
first command followed by a successful command must not become overall verified
success. These behaviors were reproduced locally; the corrected real check
preserved all source bytes. Acceptance: compare literal byte boundaries and
retain each operation's result or propagate failure explicitly, without
relaxing expected hashes. This extends existing provenance/diagnostic fixtures,
not a demonstrated Sherlock defect or product fix. Generic examples only;
queued locally, not sent, acknowledged or activated.

**October 8 claim-link integration recurrence, SFB-004/SFB-005, local only:**
A local synthetic check initially accepted complete ID rosters with every
evidence/transform edge erased. Require applicable joins or field-specific
consequential gaps, and test actual traversal reachability; counts alone are
not coverage. The corrected local controls reject erased/unreachable links.
Separate content review also caught analysis-section locators copied onto
upstream inputs and two modalities of one uploaded item assigned unjoined
families. Synthetic acceptance must distinguish input, derivation and output
locators, preserve shared origins without asserting original synchronization,
and keep semantic review separate from structural validation. A reviewer also
withdrew an apparent file-change warning after binary/UTF-8 string equality
was corrected: compare byte-normalized data/hashes and file state, not string
encoding metadata. These are reproduced local workflow/checker issues, not
inspected Sherlock defects or implemented product fixes. Generic examples
only; no case payload, external transmission, new destination or acknowledgment.

October 8 additive-revision recurrence, same SFB-004/SFB-005 note: a verifier
bound to an initial baseline does not automatically protect later additions.
For a synthetic baseline-plus-extension update, retain the complete latest
reviewed objects and ordered additions, not only their IDs or original subset.
Reject undeclared new rows and changed old qualifications/acceptance flags;
bracket the full delegated validation call with control-integrity checks.
The local wrapper's mutation/reordering/flag fixtures pass, with its real
selected-file check separately executed. This is a local versioned-preservation
requirement, not a demonstrated Sherlock defect or product fix. The existing
Ruby byte-versus-encoding diagnostic lesson recurred and was resolved without
changing data. Generic examples only; queued locally, not sent or acknowledged.

October 8 reading-provenance recurrence, same SFB-004/SFB-005 fixtures:
a later complete small-block observation can resolve an earlier truncated-read
gap without retrospectively certifying rejected displays. Preserve the pinned
partial snapshot; append attributable new reading receipts and version any
completed output/consumer binding. Test that a new observation does not silently
flip old completion or human-acceptance flags. This is an observed local workflow
requirement, not a demonstrated product defect or fix. No case content, private
path or new destination is included; queued locally under unchanged routing.

**October 7 annotation partition extension, SFB-004/SFB-005, local only:**
Two readers can choose the same outer pixel set while assigning different
cells to a confident core and tentative fringe. Extend the existing
annotation/dependence fixture to retain these classifications separately.
Synthetic case: reader A core {1}, fringe {3}; reader B core {3}, fringe {1}.
Acceptance: outer-set equality must not become complete agreement, row 2
must not be filled, and neither the intersection nor union may be labeled a
calibrated original-source confidence bound. Require unambiguous names for
agreement versus disagreement counts. Priority: prevent scientific overclaim
from a reproducible annotation. This is an observed local workflow need,
not an inspected Sherlock defect. Generic synthetic data only; no source
images, case details or private paths. Queued locally, not sent or fixed.

Extend that same annotation fixture to fragment membership: two separately
named pieces can have a contiguous combined row set without becoming one
identified stroke. A single identifier without an optional membership map
must also remain distinguishable from missing attribution. Synthetic acceptance:
preserve original schemas/labels, reject automatic multi-piece fusion, and
report geometry eligibility separately from source containment or acceptance.
Both forms are exercised by local synthetic controls. This is an observed
workflow need, not an inspected Sherlock defect; no new issue, case payload,
delivery or claimed fix. Routing remains pending locally.

The same fixture now also covers uncertainty vocabulary and provenance
adapters. One reader can label unassigned tentative cells `fringe_only`,
another `identity_conflict`; preserve the literal labels and represent unknown
fragment membership separately. A known-label fringe can remain distinct from
either. Accept only documented pin/target schema aliases, reject contradictory
aliases, and distinguish an originally declared source pin from a verifier's
later additional pin. Synthetic controls exercise these cases and changed
dependencies before comparing actual records. This is a reproduced local
workflow need, not a demonstrated Sherlock defect or a delivered fix. No new
issue family or sensitive payload; pending under the same routing boundary.

The same schema fixture now has a reproduced silent-field-loss hazard: an old
normalizer recognized a membership map under one coordinate schema but ignored
a list-valued membership field under another. In a synthetic two-piece record,
unadapted classification admitted a single-fragment rectangle; an explicit
copy-only adapter retained both memberships and excluded it. Acceptance:
dispatch only declared schemas, preserve all originals and membership unions,
reject conflicting aliases, and prevent an unsupported field combination from
silently weakening the single-fragment rule. The new local integration uses
the tested adapter; no saved historical result is shown affected. This is a
local-method hazard, not an inspected Sherlock bug or product fix. Generic
synthetic example only; deduplicated under SFB-004/SFB-005, queued locally.

October 8 qualification-preservation recurrence, same SFB-004/SFB-005 fixture:
a versioned inventory can preserve all old measurements exactly while its
rewritten summary drops a still-applicable limitation. Generic reproduction:
an older annotation batch has broad conflict references; a later batch has
precise references, but both remain in the combined dataset. Acceptance:
preserve each batch's qualifier and scope in current summaries; do not imply
that the newer schema retroactively repairs old data. Review semantic changes
alongside object/hash equality. If found after output freeze, preserve that
version and make an explicit, narrowly checked narrative correction without
changing numerical arrays. This was a local authoring lapse caught by separate
review, not a demonstrated Sherlock defect or product fix. Generic fixture
only, no case values, identities, paths or source payload. Queued locally
under unchanged archived routing; not sent or acknowledged.

Related local dependency-test recurrence, same SFB-005 fixture: resolving a
child path but not its root can misconstruct a relative dependency key across
an operating-system alias. Test canonical and aliased temporary roots, normalize
both sides consistently, and retain strict allowed-path boundaries rather than
widening them to make a test pass. The local synthetic failure was repaired
before historical output; no Sherlock implementation was inspected or changed.
No real paths or diagnostics are proposed for transmission.

October 8 owner-map recurrence, same SFB-005 fixture: a local consumer assumed
two manifests used one relative-path base, although each declared a different
owner. It failed before sample selection. Resolve each map against its own
owner before normalizing the combined keys; synthetic parent/child aliases
must resolve to one unchanged artifact, and before/after drift must fail.
Both new regression checks pass locally. This is a reproduced local integration
error, not an inspected Sherlock defect; no source payload or real path is
included, and delivery remains pending under the existing routing boundary.

The same closure fixture recurred at the next verification layer: checking
every listed pin still missed four dependencies of an already pinned receipt.
An independently reconstructed required closure rejected the candidate before
release. Preserve it and its code, extend the complete receipt dependency map
under a separate output identity, and assert every non-dependency scientific
field is unchanged. Do not relabel a successful listed-pin hash check as full
closure. This local repair and retained failure are not a Sherlock product fix.

Related versioned-review recurrence under SFB-004/SFB-005: stable sample labels
can identify different coordinates after a declared input extension. Bind
display and copied human responses to the packet ID and full byte hash, preserve
the old packet and all uninspected states, and prohibit automatic acceptance
transfer based on label equality. A generic same-label/two-version fixture is
the proposed product test, not a request for case access or a delivered fix.

October 8 closure-cache recurrence, same SFB-005 fixture: a local wrapper
pre-pinned a JSON input, then a recursive helper's already-pinned early return
skipped that file's dependencies. Generic reproduction: pre-pin A and B where
A declares B and B declares C, then require a complete dependency closure.
Acceptance must include C and reject changed C bytes despite A/B being cached;
keep traversal expansion state separate from the byte-pin map. The local fix
and nested-map/script regressions passed before historical output. This is not
an inspected Sherlock defect or product fix. Generic fixture only; no case
payload or new issue family. Routing remains pending locally, not delivered.

The same fixture family should distinguish one visible band from two
independently identified series: an overplotted pair and a single remaining
series can look alike. Acceptance must preserve unknown membership rather
than duplicate one observation into apparent two-series agreement. Keep a
later correction alongside the original reading, including when every
checklist field was filled. This is an observed annotation/inference risk,
not a verified Sherlock defect. No new issue family, case payload, delivery
or implementation approval is implied.

The same fixture now has a reproduced transcription failure: a compact manual
run included exactly white cells as tentative visible ink. Synthetic acceptance
must compare every selected cell to the preserved source, distinguish an
explicit uncertainty envelope from an ink annotation, and flag a mismatch
without silently editing the frozen reading. A versioned erratum must identify
its parent, exact membership changes, unchanged remainder and post-exchange
status; retain the original freeze as history, not a new independent reading.
Repeatable correction does not validate the remaining annotations. This extends
the existing fixture, not a new product-defect claim. Generic data only;
pending locally under the same archived-destination boundary.

The same fixture now covers fringe-only boundary truncation: a selected faint
edge can touch the crop boundary while its confidently visible core lies
outside the target. A prior local checker required a nonempty core for every
truncated fragment; the next checker removes that unnecessary restriction
without rewriting the earlier frozen outputs, which were unaffected. Synthetic
acceptance must permit a nonempty fringe-only identified boundary fragment,
reject empty truncation and invented flags, and keep the unknown outside-crop
continuation separate from a true endpoint. This is a demonstrated local
validator limitation and tested fixture, not an inspected Sherlock defect.
Generic coordinates only; no case payload or new transmission. Queued under
the unchanged archived-destination routing boundary.

October 8 extension to that same comparison fixture: reader roles must not
depend on dictionary insertion order. A newly tested local adapter explicitly
selects the named primary and secondary reader before forming directional
differences. Synthetic acceptance reverses the input mapping order and requires
identical output, with primary-only and secondary-only cells still attributed
to the correct reader. This addresses a potential API-order weakness observed
in the preceding local implementation; its saved runs used the expected order
and are not shown wrong. The local adapter/control passes, not a verified
Sherlock product fix. Generic synthetic roles and cells only; no source data,
case payload or transmission. Pending under the same archived destination.

The same fixture now includes two source regions for one named series. Native
coordinates can coincide while the source images and transforms differ.
Synthetic acceptance keeps both region/source keys, rejects swapping or
collapsing them, and never infers a seam join from the shared series label.
An overlapping region may reuse an actual prior reading only after exact
source-cell equality and explicit coverage/receipt linkage; that is not a
second observation. A local mutation also demonstrated that a named but empty
unassigned band could receive a seemingly valid reference. The corrected local
validator requires a nonempty same-column band and a recorded reason, while
still preserving empty records separately from missing records. The new
controls pass; no original source annotation was changed. Priority: attribution
and missingness integrity. These are observed local workflow needs, not
verified Sherlock defects or fixes. Generic synthetic examples only, no case
payload, new destination, delivery or acknowledgment; routing remains local.

Extend this same region-coverage fixture to completion scope: every item in a
fixed crop roster can be finished while broader source-region obligations
remain. Preserve separate states for qualitative inspection, literal footprint,
justified measurement bounds, admitted support and actual human acceptance.
Synthetic acceptance joins completed crops to the original full-scope inventory,
retains unmeasured and unresolved portions separately, and refuses to convert
unknown common support to an empty domain. A context halo does not enlarge
the target and overlapping older work is not new evidence. This recurrence
is a local workflow risk, not a demonstrated Sherlock defect. Generic fixtures
only; the archived destination remains unresolved and no note was transmitted.

October 8 continuation of that completion-scope fixture: repeated successful
recovery batches can defer the actual measurement-admission decision even when
the controlling protocol permits partial domains. Require a named limiting
condition and expected decision impact before adding another recovery batch;
do not infer completion from more annotations or relabel accessible unmeasured
regions unreadable. A proposed synthetic acceptance case has two completed
local regions and one unresolved contact: the next action must assess the
existing regions' admission, or explain which specific prerequisite the next
recovery resolves. This transition is adopted locally; the proposed product
test has not been implemented or run. Deduplicated workflow feedback, not a
verified Sherlock defect. Generic fixture only, queued locally; no delivery.

The shared-source attribution fixture also now includes two different series,
each read twice, using overlapping source cells. Local synthetic checks cover
all four reader pairings, both confidence classes and unassigned material;
same row numbers in different columns must not intersect. Preserve every
cross-series intersection as a candidate attribution conflict, not corroboration
or permission to overwrite either original. These tests pass in the local
comparison harness, not Sherlock. No case payload, new issue family or delivery;
the archived routing boundary is unchanged.

The same fixture now separates a conditional coordinate window from established
curve support. A visible dash cap may occupy a pixel without its generating
path covering the entire column; a selected-cell enclosure does not establish
an error bound for omitted halo. Synthetic acceptance preserves identity,
full-column existence and enclosure assumptions separately, retains competing
reader/axis alternatives, and prevents marginal boxes sharing one calibration
from becoming independent errors or automatic support. Local synthetic and
complete arithmetic checks exercise the conversion, not those assumptions.
This is an observed workflow need, not a verified Sherlock defect. No new
issue family or case payload; queued locally under the same archived routing.

October 8 candidate-admission extension to the same fixture: presence of both
series somewhere does not establish overlapping comparison support. Compute
overlap in shared source geometry before uncertain coordinate mapping; two
disjoint intervals shifted by one shared uncertain offset can have overlapping
marginal hulls without ever intersecting together. Also check cross-route
ownership even within one reader: a tentative edge cell can appear in both
series although each route's core/fringe sets are individually disjoint.
Synthetic acceptance preserves the original selections, flags the shared
cell, retains unaffected local intervals and does not convert conditional
coverage or an empty candidate set into accepted support or a zero curve.
Twenty local producer controls exercise these safeguards, including all four
reader combinations; 26 separate checker controls and full calculation replay
also pass. These are not a Sherlock product test or verified fix.
Generic fixture only; deduplicated SFB-004/SFB-005 note, queued locally under
unchanged archived routing, not delivered.

Scope-of-claim review adds a recurrence to the same completion-scope fixture:
a prerequisite for full physical-system validation must not silently become
a gate for a narrower published-graph comparison. Preserve different claims
and their actual dependencies in separate rows. Synthetic acceptance should
reject both automatic physical promotion from graph agreement and blanket
withholding of graphical analysis pending a system-level test. This was a
local report wording issue corrected by review, not an inspected product bug;
no new issue, sensitive payload, external delivery or product fix is claimed.

The same fixture now needs distinct namespaces for a conditional review sample
and an originally required accepted-support sample. A length-quantile target
can lie on an excluded shared endpoint even when adjacent intervals merge for
length bookkeeping. Synthetic acceptance must retain that target as unresolved,
keep missing primary coverage rather than substitute a peer, display all
same-position alternatives, and never treat a UI click as a human response.
Separately, finite-renderer controls can have identical pixels but different
subpixel support/extrema: preserve the renderer-specific limitation without
claiming historical error rates. These local controls were exercised; this is
a workflow need, not an inspected Sherlock defect or product fix. Deduplicated
under SFB-004/SFB-005; generic examples only, pending locally under unchanged
archived-destination routing. No new payload or destination is authorized.

That same fixture now distinguishes route-specific uncertainty from a generic
same-column conflict. A band tentatively belonging to route B must not make
an unrelated empty route A conflicted. Require explicit candidate-route labels
(including an explicit empty list), reciprocal same-column references, and
nonempty material for a conflict status. Local synthetic tests exposed missing
labels silently defaulting to empty and empty bands carrying conflict status;
the pre-fix code is preserved and the repaired checks pass. Also verify any
separately recorded expansion-helper pin, not only files in a primary input
map. A changed-helper fixture must fail even when the frozen annotation bytes
are unchanged. These are local provenance/representation safeguards, not
verified Sherlock product defects or source-reading corrections. Generic
fixtures only; queued locally under the same unresolved archived destination.

One remaining representation limit in that fixture: prose may assign two
pieces of an aggregate uncertainty band to different candidate routes while
both machine references target the entire band. Do not describe that as
machine-enforced fragment ownership. Synthetic acceptance must preserve the
original aggregate schema and notes, distinguish it from explicit member-level
references, and prevent downstream support construction from silently assigning
all band cells to each route. Existing all-ink set comparisons can remain
valid without that stronger identity claim. This is an observed local encoding
limit, not a verified Sherlock defect; no frozen observation is rewritten.

Extend that same fixture to multiple disjoint uncertainty bands in one column.
A local legacy validator/index assumed a single band; a later frozen reading
legitimately supplied two, with different candidate routes. Synthetic example:
at one x, band U selects row1 for route A and band V selects row4 for route B.
Acceptance: retain both original records under (x,band_id), preserve each
reciprocal reference, union both only for an explicitly all-visible-ink
comparison, reject cross-route references, and never overwrite by x alone.
An explicit schema adapter may validate and translate local-ink status labels
without rewriting originals or silently changing ownership. Local synthetic
tests now cover both-band retention and rejection of a wrong-route reference.
This is a demonstrated local workflow limitation, not an inspected Sherlock
defect or product fix. Deduplicated SFB-004/SFB-005 extension, generic cells
only; queued locally under the unchanged archived-destination boundary.

The same provenance fixture now covers an incomplete replay command: a local
partial audit saved the executable and script but omitted the required scope
argument. Its external receipt preserves the working command without rewriting
the original output. Acceptance: commands reproduce the exact declared scope;
saved partial code and outputs remain immutable when later scope is added;
an expanded version has a distinct identity and complete dependency pins.
A generic synthetic fixture must distinguish one-region from all-region
replays and fail before reading inputs when the required frozen scope is
missing. This is a demonstrated local receipt defect, not an inspected Sherlock
product defect. Keep it deduplicated under provenance/replay safeguards; no
case payload, transmission, acknowledgment or product fix is claimed.

The same reproducibility safeguard must cover inert source reconstruction:
an independent local checker read an initial configuration literal but ignored
later explicit data-only updates, then failed its historical equality check.
Preserve that failure and implementation. A versioned correction must handle
only declared data operations, retain list order and update semantics, reject
unsupported mutations, and pass synthetic fixtures before replay. Do not
execute producer code or copy its result to manufacture independence. This
extends the existing replay fixture, not the source observation or a verified
Sherlock defect. Generic example: a declared map, a literal submap update and
a literal list append must reconstruct all three; an unknown operation fails
closed. Queued locally, with no case payload or transmission.

The same fixture also needs explicit coverage-schema dispatch: a later local
checker supported direct column blocks but failed on declared same-source
shared rectangles. Preserve that failed version. A separate repair must check
exact schema, source identity, typed bounds, referenced-context containment,
receipts, complete source-cell union and equality; counts or overlapping areas
alone cannot establish coverage. Reject ambiguous schemas and gaps. Passing
these checks verifies the recorded coverage, not independently witnessed
perception. The repaired local full audit passes without rewriting source
annotations; this is not a verified Sherlock fix. Same queued-only routing.

Extend the existing reader-independence safeguard to metadata: a permitted
integrity manifest can expose truth-related filenames and equal hashes even
when the actual answer file is withheld. A minimal synthetic test gives a
reader two unnamed candidate images plus a manifest containing alternative
labels and hashes. Acceptance: a truth-withheld packet uses only its own
allowlisted artifact manifest, and any exposure is retained as a blinding
limitation rather than retroactively called independent discovery. This is
an observed local workflow issue, not an inspected product defect. Generic
fixture only; pending locally under the same archived-destination boundary.

**October 7 shared exclusion rule extension, SFB-004/SFB-005, local only:**
An exploratory detector sweep changed contrast thresholds while retaining one
color exclusion. A continuous synthetic nonwhite band then produced identical
artificial gaps in every run. Reproducibility and parameter agreement did not
validate the detected topology. Desired behavior: retain shared preprocessing
and exclusion dependencies when presenting sensitivity or validation results;
do not label correlated runs independent evidence. Minimal synthetic fixture:
alternate pale and saturated colored pixels along an uninterrupted band,
apply a fixed color cutoff with several contrast cutoffs, and retain the
known-continuous ground truth alongside the broken detections. Acceptance:
the record preserves the failed control, shared rule and narrowed claim; a
passing replay cannot promote line identity or erase the control. Priority:
scientific-validity safeguard before consequential measurement. This is an
observed workflow need, not a demonstrated Sherlock implementation defect.
No case imagery, names, private paths or physical measurements are included.
Queued locally; not sent, acknowledged, implemented or verified fixed. The
latest destination turn read supplies no newer acknowledgment and its
notLoaded status alone does not independently establish archival status.

October 5 current-state routing check: two archived-task pages of fifty were
queried using the returned cursor; page two again contained the exact target
ID/title. Only the relevant target metadata was surfaced. No send, unarchive,
new task or rerouting occurred. This confirms the same pending decision, not
scientific progress or feedback delivery.

**October 5 human-sample selection extension, SFB-004/SFB-005, local only:**
An observation workflow can require selected human checks while failing to
specify how the samples are selected. Extend the existing candidate-freeze,
review-coverage and partial-admission fixtures: freeze an outcome-independent
selection rule and complete target census before discrepancy results; preserve
unavailable targets, boundary ties, coincident native footprints and original
failed selections rather than replacing them with convenient points. Retain
the source/registration version, actual inspected coverage and attributable
response. Acceptance requires deterministic replay from the frozen inventory
and rejects a passed spot-check as whole-source validation or a calibrated
confidence interval. Priority: evidence integrity before consequential use.
This is an observed local method gap, not an inspected Sherlock defect or a
new issue family. Generic synthetic fixture only; no case names, sources,
measurements or private paths proposed for transfer. Pending locally under
the archived-destination decision, not sent, acknowledged or fixed.

September28 current-state recheck: `read_thread` returned the designated task
"Define Phase 0 invariants" with its last completed triage turn; `notLoaded`
alone was not interpreted as archived. A fresh `list_archived_threads` result
then included the exact designated task ID. The first listing request's100
limit was rejected (maximum50); the corrected50-item call succeeded and found
the target without pagination. No send, unarchive, replacement or implementation
request occurred. New source-display feedback remains locally pending.

**States:** observed/proposed → sent → acknowledged/triaged → fix-reported → locally verified. Acknowledgment is not a fix. Include a date, source/version when available, impact, safe reproduction, and acceptance check. Before every send, apply the repository privacy rule to the exact payload and destination. Case-sensitive and sensitive security details stay local pending specific approval; an apparently harmless synthetic example is preferred.

**October 5 audio access recurrence, SFB-002/SFB-005, local only:** A valid
synthetic speech file was forwarded through an available audio-content helper,
but the returned content explicitly stated that audio input was omitted because
the recipient did not support it. File-generation and byte-delivery checks
passed; auditory perception did not occur. This is an observed caller workflow
limit, not an inspected Sherlock defect. Priority: prevent fabricated media
review and unblock the human-listening handoff. Generic acceptance fixture:
retain separate file-ready, emitted, perceptually-accessible, listened and
human-reviewed states; an unsupported-modality response must leave events
unknown, not an empty list interpreted as no events. Preserve the failed route,
offer a local human-review packet, and do not loop without changed capability.
Even a successful clean-speech control must not certify noisy-event detection
or causal timing. This extends existing representation/admission feedback;
no new issue family or implementation authorization. No case data, paths or
historical audio are proposed for transfer. Pending locally under the existing
routing question; no new send, acknowledgment or claimed fix.

October 4 routing recheck: two actual archived-task pages of fifty entries
were inspected using the returned cursor. The second page contained the exact
designated task ID/title. Archived status is established by that listing,
not its `notLoaded` field. No send, unarchive or replacement was performed;
new minimized notes remain queued locally under the existing routing question.

**October 4 acquisition and document-role recurrence, SFB-005, local only:**
The existing access-response/representation fixtures should retain a reader-only
failure followed by a separately declared successful direct acquisition, without
rewriting the failure or calling it server refusal. Extend the catalog-cover
fixture with a later request that encloses earlier design comments: request,
attachment, agency response, revision and installed-state acceptance must remain
separate. Acceptance rejects both a folder label promoted to an instruction and
a review comment promoted to an unresolved historical defect. The same fixture
now distinguishes a document's own date
from the earlier documents it modifies, and listed sheets from selected issued
sheets or completed work. These are source-role checks, not separate product
issues. This is workflow feedback, not an inspected Sherlock bug; no sources, real values,
private paths or attachments are proposed for transfer. Deduplicated locally;
archived-task routing unchanged, nothing sent or claimed fixed.

October 8 reader-projection recurrence, same SFB-005 fixture: a reader can
display selected source passages while direct acquisition returns an error
body. Preserve the exact projection, requested windows and failed response
as different artifact roles; a hash of either is not a hash of the unavailable
original. Synthetic acceptance uses a partial text view, an HTTP403 HTML body
and a second reviewer who can inspect only the shared view. Reject original-
acquisition, whole-document coverage and independent-corroboration claims;
allow a separately labeled interpretation review. This is a workflow need,
not an inspected Sherlock defect or implemented fixture. P2 under existing
SFB-005, generic payload only, pending locally under the unchanged archived
destination; no new delivery, acknowledgment or verified fix.

October 4 identifier-search recurrence, same SFB-005 fixture: a synthetic
catalog uses `A.B.C.` while an initial literal search uses `ABC`. Preserve
the original zero/match coverage and prospectively declared normalization
pass separately; report token, line, logical-record and source-family counts
as different quantities. A known original can lack its drawing number in
metadata, so a metadata nonmatch must not become original-record absence.
Acceptance includes that counterexample and rejects both retroactive query
rewriting and double-counting link labels/URLs. This is a reproducible workflow
need, not an inspected product defect. No case payload or new delivery;
existing archived-destination boundary remains.

October 5 follow-through, same identifier-search fixture: a short token such
as `Q-1` can match inside `A-Q-1` or `Q-1.1`. Preserve the complete original
field and distinguish token leads from exact identifiers; exercise these
compound cases before selection. Another local run again found a known source
under a generic, nonmatching label. These extend the existing acceptance
fixture, not a new product issue or verified fix. Synthetic labels only;
no case payload, transfer or new delivery. Routing remains pending locally.

October 4 catalog-grain recurrence, same SFB-005 fixture: an introduction
defines counts as folder totals and links as the first document, while a row
alone appears to describe a multi-page download. Our row-only intake initially
misread the grain; the introduction corrected it. Synthetic acceptance must
carry the parent count/link definitions into selection, retain the original
expectation and correction, and distinguish complete-file from complete-folder
coverage. Do not report expected first-document length as a failed download
or missing evidence. This is a local workflow error and fixture extension,
not an inspected Sherlock defect or fixed product behavior. No real source
values, names, paths or attachments proposed for transfer; pending locally.

October 4 search-extraction recurrence, same SFB-005 fixture: a saved metadata
result can remain identical while a live local-filename join changes after
new acquisition. Preserve the acquisition-time inventory or label that join
as current-state enrichment; do not call its change a source mutation or a
failed historical reproduction. Synthetic acceptance also preserves capped
queries, previous-page availability, missing termination evidence, absent
empty-result keys and inconsistent reported counts. Local parser defects
were corrected without changing the frozen real extraction; these are workflow
requirements, not inspected Sherlock bugs. The split-cover recurrence is already
covered by the existing document-role fixture. No new case payload, delivery
or acknowledgment; archived routing remains pending.

The same search-extraction fixture now includes an omitted descriptive field.
Keep the strict-contract failure, supplied fields and quarantined occurrences;
do not fill the omission with a literal sentinel or discard its identifier.
Acceptance reconciles total, strict-valid and quarantined counts at occurrence
and unique-ID grain, while a separate diagnostic success cannot become a
full-contract pass. Include a known-positive content item that one terminated
keyword query misses but another retrieves; a successful locator control does
not certify OCR/index coverage. Generic workflow extension only, not an inspected
product defect. Pending locally, with no case payload or new delivery.

The same fixture includes a keyword-positive catalog precaution and an actual
measurement report that the query misses. Acceptance requires source-context
roles before either a match becomes a measured event or a nonmatch becomes
absence. A related cover explicitly says an enclosure will follow upon receipt;
preserve that pending state and a separate review request without promoting
either to later delivery or completed review. Generic extension of the existing
search/source-role fixture only; no new product defect, case payload or delivery.

October 4 attachment-label recurrence, same SFB-005 fixture: a synthetic
cover promises drawings A/D but the supplied title blocks say C/F and concern
another subsystem of the same project. Preserve both descriptions and classify
the actual attachments; do not rewrite them to match the catalog or infer
intent from the mismatch. Acceptance also rejects joining an equal numerical
dimension when one is a platform height and the other a conduit diameter.
This extends existing attachment/quantity-role checks, not a new defect or
product fix. Generic example only; no case payload. Pending locally under the
unchanged archived-destination boundary, not sent or acknowledged.

The same attachment-role fixture now includes one unmarked copy saying
"included" and related copies with a handwritten "consult separate file".
Preserve the annotation, unknown author/date and shared source family; neither
overwrite the text silently nor count versions as independent events. Acceptance
rejects treating every copy as promising an enclosure or the annotation alone
as suppression. This is a generic workflow extension, not an inspected product
bug. No case details or new delivery; the existing routing decision is pending.

**2026-09-27 experimental-endpoint extension — local only, SFB-004/SFB-005:**
Extend existing quantity-definition, nominal/realized-input and version fixtures.
Synthetic reproduction: an assembly earns a temperature-limited rating, a later
loaded run stops for safety before support failure, an instrument stops earlier
than heating, and an abstract misassigns the longest run to another boundary
condition. Acceptance: retain rating, damage, observed support, observation stop,
heating stop and unknown later behavior as separate events; record interventions
and valid sensor intervals; never sum separately analyzed load cases into an
invented performed load. Correct current summaries from detailed records while
preserving conflicting source statements and favorable design rationale.
This is an observed investigation-workflow need, not an inspected Sherlock bug
or verified fix. Generic fixture only; no actual case values, sources, names,
private paths or attachments proposed for transfer. Archived-destination routing
is unchanged: queued locally, not sent or acknowledged.

September28 validation-role extension, same SFB-004/SFB-005 fixture, local
only: a report labels a code-translation check validation, separately uses
physical connector tests to choose a capacity/interface, and compares reduced
and detailed models before changing a downstream material law. Synthetic
acceptance: preserve reference type, response metric, experimental denominator,
calibration role and model version at each step. Close displacement agreement
must not erase divergent forces or become heated-system validation; physical
component support must not disappear because the system-level comparison is
unlocated. Keep reported, executed, reproduced and independently validated
states distinct. A wrong page-offset probe must leave already-made derivatives
excluded until properly scoped, not silently call them reviewed. This extends
existing provenance/metric/scope contracts, not a new defect claim or roadmap.
No case data or attachments included; not sent, acknowledged or fixed.

September28 thermal-metric recurrence under that same fixture: a measured
boundary input must stay distinct from an evaluated interior output; a fitted
event history must not be promoted to a held-out forecast. Synthetic acceptance:
flag a statistic that exceeds one of two claimed thresholds, preserve null
table cells, and attach units/denominators and run/channel identity to every
comparison. Agreement at selected sensors must coexist with retained failures.
This is a deduplicated workflow requirement, not a newly verified product bug.
No source payload proposed; archived routing unchanged, pending locally only.

Same fixture, earlier-report recurrence: a fuller source has two explicitly
labeled test tables where a later paper cross-references only one; identical
printed values establish shared reporting, not identical native runs. A graph
shows a positive property where a coarse table rounds to zero. Acceptance:
retain source/version/channel joins, distinguish rounded display from executable
input, and let clarifying counterevidence narrow the critique without erasing
earlier uncertainty. These extend existing lineage/precision requirements;
no new product-defect or delivery claim. Generic local note only.

Same fixture, property-domain recurrence: a source prints a property table
beyond the range it explicitly calls valid, while a downstream table repeats
the shape at different precision. Synthetic acceptance: preserve property-
specific validity domains, measurement-versus-calculation roles, formulation
identity and native-input status; distinguish a resolved rounding question
from an unresolved domain/assignment question. Similar values must neither
erase the qualification nor automatically become an executed model defect.
Generic extension of SFB-004/SFB-005 only; no case payload, inspected software
defect, delivery or fix claim. Archived-destination boundary unchanged.

Same fixture, material/version/heat-storage extension: a method cites a source
with a validity limit covering several materials, publishes different material
curves and an alternative heat-storage representation, but explains that earlier
validation runs used an older dataset. Synthetic acceptance: do not import one
material's numbers into another, drop a shared qualification merely because the
label differs, or infer the active solver property from a plotted curve. Preserve
validation run/property versions and explicit older-data chronology; require an
execution link before transferring validation or assigning a downstream error.
This is a reproducible evidence-modeling requirement, not a source-inspected
Sherlock defect. Generic local extension of SFB-004/SFB-005 only; no case values,
source attachments or private paths proposed for transfer. Archived routing is
unchanged; not sent, acknowledged or fixed.

September28 role/activation recurrence under that same fixture: a deliberately
low-capacity replacement represents selected damaged regions, while an inventory
records material-command names but not arguments. Acceptance: preserve intended
region/role, actual assignment, active formulation and execution as distinct
joins; neither an extreme replacement property nor a command count establishes
an erroneous intact-material law. This extends the existing material/version
fixture, not a new product-defect claim. Generic local note only; routing and
delivery status remain unchanged.

September28 typed-parser recurrence under the same SFB-004/SFB-005 fixture:
a synthetic quoted field containing a comma must not shift subsequent numeric
roles even when the whole row is unresolved. Invalid CLI arguments must not
echo a private sentinel through default error handling. Both defects were caught
in the local research parser before native reading; they are not demonstrated
Sherlock defects. Acceptance: preserve quoted/doubled-quote field boundaries,
blank-versus-zero and unresolved status; test success and failure output for
sentinel leakage before source execution. Generic workflow note only, queued
locally under the unchanged archived-destination boundary; no delivery or
Sherlock fix claimed.

Same parser fixture, metadata-cap extension: a legitimate inventory can exceed
the intentionally smaller per-source byte limit. Acceptance: retain failed
receipts, give pinned metadata its own exact-size/hash allowance, and prove the
native-source cap is unchanged. Do not relabel this local guard mistake a bad
source or weaken all limits to obtain a pass. Local-only workflow requirement;
unchanged routing and no inspected Sherlock defect or delivery claim.

Same parser fixture, selected-field versus source-integrity extension: a reader
can correctly restrict field decoding yet accidentally restrict a promised
whole-file guard to those selected lines. A synthetic overlong unselected line
exposed that local mismatch before native reading. Acceptance: distinguish
integrity coverage from interpretation coverage, enforce each declared cap at
its declared scope, and retain the failed check plus adjacent-boundary repair
tests. This is a deduplicated local workflow lesson, not a demonstrated Sherlock
defect; no source contents, identifiers, case results or paths are outbound.
Archived routing remains unresolved; nothing sent or claimed fixed in Sherlock.

**2026-09-24 request/recovery/context supplement — local only, SFB-004/SFB-005:**
Extend the existing completion, authority and provenance fixtures, not a new
product roadmap. Synthetic reproduction: a user requests organization of
existing work; an assistant substitutes future feature stages; a disposable
index contains unique reviewer decisions; a handoff forbids data uploads but
requires private source context. Acceptance: preserve the requested object and
report undelivered work separately from valid transmission gates; reconstruct
decisions from a durable versioned source, not new inference; distinguish
application network behavior from agent-provider context disclosure and require
an approved context packet. Record per-turn authorship/effort and inspected
coverage rather than attributing a whole project from one model label. These
are observed workflow needs/design gaps, not demonstrated Sherlock defects,
data loss or disclosure. Generic fixture only, with no case payload, private
paths, message text or identities proposed for transmission. Local queue only;
the archived destination has not been reopened or replaced, and no delivery,
acknowledgment or fix is claimed.

**2026-09-24 current-state verification extension — local only, SFB-005:**
An actual documentation/runtime mismatch motivates one additional synthetic
case under the existing completion/state fixture: a README names an older
release than the lock and installed byte inventory, while a case contains
only setup questions and no admitted evidence. Acceptance: report those
states separately, date old security receipts, and distinguish fresh raw-file
counts from engine replay and scientific acceptance. No engine defect or
adapter failure is established by stale documentation. Generic fixture only;
no case payload, paths, identifiers or source data proposed for transmission.
Queued under the unchanged archived-destination boundary, not sent or fixed.

October 4 export-boundary extension, same SFB-005 fixture: distinguish an
export's read-only scientific projection from its new output files and expected
audit-log append. Use synthetic records to check these categories separately;
a false authority-merger flag is not proof that no state changed. Destination
IDs and well-formed hashes also need actual endpoint/byte verification before
being called resolved. Test whole-object metadata minimization before real
payload selection. This is a source-inspected integration requirement, not a
run-verified defect or scientific validation. Generic note only; no case data,
private paths or attachments proposed. Queued locally, not sent or fixed.

October 5 execution follow-up to the same SFB-005 export fixture: the bounded
pilot did not reach export. Its harness missed a test-runner stream interface
and supplied an unsupported evidence-direction literal. Preserve a distinction
between launch/configuration failure, fixture-setup refusal, executed target
case and verified result. Zero collected tests with zero reported test failures
is not a pass; absent post-run inventory is not an empty successful inventory.
Acceptance for a future generic fixture: check the actual CLI enum and stream
contract before target execution, preserve all attempts, retain explicit
synthetic/pending/non-scientific fields, and never rename an unexecuted export
case as a product failure or passing capability. The single repair allowance
was exhausted, so no automatic corrective loop follows. These are our harness
defects and review misses, not verified Sherlock defects or bridge-result
findings. Existing endpoint/metadata/export-event requirements above remain
source-inspected, not runtime-verified. No case payload, private path or source
document is proposed for transmission; locally queued, not sent or acknowledged.

October 7 executed export follow-up, same SFB-005 fixture, local only:
separately authorized synthetic retries now reached export. Two runs retained
synthetic/pending/non-scientific flags and matched declared semantic results.
They also accepted a nonexistent destination with a syntactically valid digest,
and allowed exploratory evidence export after its raw file changed or went
missing. Local artifact locators remained in exported metadata. These are
observed scope limits, not proof of a violated product contract, a successful
Sherlock admission, or valid scientific evidence. Earlier unexecuted states
remain preserved as history.

Desired integration behavior: distinguish serialized, destination-resolved,
current-source-verified, admitted and human-accepted states explicitly. Before
reliance on a real export, independently resolve its destination and digest,
recheck selected source bytes, review the exact metadata payload for disclosure,
and retain any unresolved state rather than silently upgrading it. Synthetic
acceptance tests should include valid and missing destinations, matching and
mismatched digests, changed and missing source bytes, and locator disclosure;
test the declared enforcement layer without retroactively changing exporter
requirements. No automatic product patch or real-case transfer is authorized.
The reproduction and limits are in the local control-retry result. This
deduplicated note contains no case payload and remains queued, not delivered,
acknowledged or fixed, pending the archived-destination routing decision.

**2026-09-24 quantifier/review-role supplement — local only, SFB-004/SFB-005:**
Extend the existing quantity-definition and completion fixtures, not a new
issue. Synthetic reproduction: a question asks whether motion was mostly
vertical; a subtest finds one fragment outside an outline; a self-review is
followed by a later separately authored review. Acceptance: preserve the
mapping from user question to tested proposition; failure of universal
containment must not become a mass-fraction, motion-phase or mechanism finding.
Store reviewer identity/role, source coverage, prior exposure and actual
freeze/receipt times; a later summary cannot become an original-time freeze.
Test logical compatibility before labelling differently qualified assertions
contradictory (for example, upper/lower bounds sharing the same endpoint).
For a derived force bound, retain weighted versus instantaneous force, point
versus COM, assigned versus calibrated units and lower-bound versus equality
semantics; exact independent arithmetic must not become historical validation.
These are observed local workflow failures/needs, not inspected Sherlock
defects or verified fixes. This generic fixture includes no case identities,
actual values, source material or private paths. Queued under the unchanged
archived-destination boundary; not sent, acknowledged or activated.

Same-day body-bound extension to that fixture: distinguish a required physical
constraint from one optional route to establish it. A normalized force ratio
need not require absolute mass if pose/COM geometry is independently bounded;
an attached material subset is not an invalid body merely because it remains
attached. Synthetic acceptance: preserve body membership and external-force
boundary, compare a necessary lower threshold with an independently justified
upper bound, and reject cross-camera transfer without a material/time/geometry
join. Point-only observation-equivalent examples must not be called full-image
or structurally feasible reconstructions. These are additional observed local
reasoning-workflow needs, not demonstrated Sherlock defects. Generic-only
content, unchanged local queue; no new transmission or acknowledgment.

Same-day locator/guard extension, SFB-005: a generic catalog advertises a large
collection while the tool returns only a partial item list; source identifiers
may appear in none of the initial semantic filename terms. Acceptance: preserve
catalog assertion versus inspected coverage, permit an explicitly versioned
identifier query, and never turn a name nonmatch into content absence. A local
archive guard also trusted one header while the library used another effective
format header; synthetic tests exposed that mismatch. Require safeguards to
track the parser's effective format, preserve failed-version source/results,
replay boundary controls and distinguish finite-input verification from general
hostile-input certification. Byte hashing, payload decoding and interpretation
are different operations. Header-only previews must not print a first data row;
test allowlisted output with a deliberately sensitive dummy field. These are
observed local workflow/tool defects and needs, not inspected Sherlock defects.
Generic synthetic fixture only, deduplicated under the existing coverage/
acquisition contract; no case data, identities, paths or findings transmitted.
Queued locally, not sent, acknowledged or fixed in Sherlock.

**September 27 search-restriction extension, same SFB-005 fixture — local only:**
A source locator used `site.example.org` where `site:example.org` was intended;
later narrative must not claim a domain-restricted search from that malformed
request. Synthetic acceptance: preserve literal query and explicit domain
fields, validate recognized operator syntax, distinguish requested restrictions
from observed result coverage, retain truncated displays and count failed or
malformed attempts against declared search limits. Use generic domains and
dummy IDs only. This is an observed analyst-workflow error and improvement
request, not an inspected Sherlock defect. Existing failure-capture fixtures
also cover setup before receipt initialization and logger-versus-direct-stderr
gaps; no duplicate issue or verified product fix is claimed. Queued under the
unchanged archived-destination routing boundary; no case payload or new send.

**October 4 batched-search attribution extension, same SFB-005 — local only:**
A two-query request returned one combined result list without per-result query
membership. Preserve both requested queries and their combined returned set;
do not invent per-query hit counts, rankings or zero-hit claims. Synthetic
acceptance: a mock two-query union with one shared result must either retain
explicit query-result joins or label them unknown; both queries still consume
the declared budget. Separate calls can preserve attribution prospectively,
but a missing join does not authorize an extra historical search after the
budget is used. This is an observed tool/workflow limitation, not an inspected
Sherlock defect or verified fix. Generic dummy queries only, locally queued;
no real identifiers, returned personal information or new transmission.

**October 4 delayed search-result extension, same SFB-005 — local only:**
A submitted search first exposed a heading without entries or an explicit
zero-result state; a later same-page observation showed results. Synthetic
acceptance: distinguish typed, submitted, pending/unknown, populated and explicit
zero-result states; record the selected category, not just the query; allow a
declared bounded readiness observation without a second submission. An empty
temporary container must not become a negative source finding. Preserve both
states and label an inferred delay when no loading marker was observed.
This extends the search-coverage and loading-state fixtures, not a demonstrated
Sherlock defect or verified fix. Generic dummy query/UI only; no case data or
paths proposed for transfer. Locally queued under the unchanged archived-task
routing boundary, not sent or acknowledged.

September27 extraction-scope extension, same SFB-005 fixture: a coordinate-
filtered header/footer locator admitted entire scanned-page OCR objects,
including content outside the declared reading scope. It was stopped; a
known-page allowlist was used for the subsequent decisive review. Acceptance:
restrict pages before parsing content; test giant single text objects,
transformed/misleading coordinates and image-only pages; fail closed when a
region cannot be reliably isolated. A first/last text line is not necessarily
a header/footer. Preserve the failure and actual exposed scope rather than
calling the attempt compliant. This is an observed analyst-tool boundary
failure, not an inspected Sherlock defect or a generally fixed extractor.
Generic fixture only: no exposed text, case names, identifiers or private
paths. Deduplicated local queue; no delivery while routing remains unresolved.

Same fixture, HTML recurrence: a line-oriented search returned an entire
single-line body, while a fixed-character preview ran into the next section.
Require checked heading boundaries and bounded visible-text output; preserve
truncation and spill as incomplete/over-scope reading, not successful isolation.
This extends the existing analyst-tool fixture, not a new Sherlock defect.

Same fixture, split-volume locator recurrence: a declared first-page range
intended for front matter encountered substantive chapters immediately after
a cover. A numeric allowlist alone did not satisfy the purpose restriction.
Acceptance: identify volume/edition and section boundaries before batch text
extraction; use a paired volume's contents/page labels when appropriate;
record unexpectedly exposed pages without silently widening the review or
using them as evidence. Test a generic split report beginning its second
volume with body text. This is an observed analyst-workflow failure, not an
inspected Sherlock defect. No case names, text, values or private paths in
the synthetic fixture. Deduplicated local queue; archived routing unchanged,
no new delivery, acknowledgment or verified fix claimed.

Same-day quantity-definition recurrence, SFB-004/SFB-005: independent review
caught prose that turned a thinner continuous-layer comparison into a spatial-
nonuniformity claim. The local wording was corrected. Synthetic acceptance:
distinguish thickness, covered area, spatial pattern and complete absence;
never describe a sweep over one as a tested sweep over the others. This is
an analyst-inference error, not a demonstrated engine defect or historical
result. Generic fixture only, queued locally under unchanged routing.

Same-day response-metric/source-family extension, SFB-004/SFB-005: a summary
cites a numerical study for system insensitivity, while the detailed study
reports local hotspots and a separate integrated-deformation equivalence.
Acceptance: bind equivalence to its actual geometry/loading/metric and profile
set; do not promote a local or integrated metric to connection/system failure
without a justified transfer. Two reports summarizing one calculation remain
one evidence family. Preserve conflicting distribution labels as source
assertions pending input verification, not automatic execution-error or intent
findings. A harmless summary typo and metric-dependent equivalence are required
countercases. This is an observed analyst-workflow need, not an inspected
Sherlock defect. Generic synthetic fixture only; no source material, names,
actual values or private paths proposed for transmission. Local queue only;
unchanged archived routing, no delivery, acknowledgment or verified fix.

Same fixture, nominal-versus-realized profile extension: a stochastic model
declares a mean/distribution, then maps draws to a finite discretized layer
using surrogate material cells. Synthetic acceptance: retain intended law,
tail handling, seed, spatial profile, realized moments, mesh and cell-property
mapping as distinct fields; do not infer a truncation rule, deleted element,
calibrated ensemble or executed run from prose. Preserve a harmless label typo
as a countercase to automatic model-error attribution. This is an observed
research-workflow need, not an inspected Sherlock defect. Generic fixture
only, without case values, source text or private paths. Deduplicated locally
under SFB-004/SFB-005; delivery and routing remain unresolved, not retried.

September 27 addition to the existing quantity/reference and response-transfer
fixtures: independent review found that an "increment" could subtract either
a probe's own baseline or a common preloaded baseline. Synthetic acceptance:
store initial state, controlled load/displacement, sign, normalization and
increment reference separately; reject an unlabeled comparison across them.
A sufficiency statement must retain its antecedent: equal compliance does not
alone imply equal thermal response; the accompanying one-load match must not
vanish in a compressed table. Preserve pre-execution clarification and distinguish
program self-consistency, independent arithmetic and physical validation.
This is an observed analyst-workflow need, not an inspected Sherlock defect.
Generic fixture only; no case data, real values, source text or private paths.
Deduplicated under SFB-004/SFB-005; archived routing unchanged, not sent or fixed.

**2026-09-20 follow-through/completion extension — local only, SFB-004/SFB-005:**
The local investigation needed a consolidated reassessment after many completed
subtests: old next-action paragraphs can remain actionable-looking long after
their follow-ups finish, while source/version checks can accumulate without
changing the central inference. Extend existing provenance/state fixtures,
not a new product-defect claim. Synthetic acceptance: one original summary,
three completed follow-ups, one unresolved calibration gate and one catalog-only
version lead. Preserve the original; show the current claim disposition and
actual verification ceiling; suppress completed next actions without erasing
history; require a remaining action's expected discriminating result and
prerequisites. Neither report count, a later publication date, nor paired
readers of one source may become scientific completion or independent evidence.
Distinguish completed access checking from an unmet content comparison and
retain uninspected alternatives. This is an observed workflow need, not an
inspected Sherlock defect or verified fix. Generic synthetic content only;
no case identities, paths, findings or source payloads. Queued locally under
the unchanged archived-destination boundary; not sent or acknowledged.

**2026-09-20 quantity-definition extension — local only, SFB-004/SFB-005:**
Extend existing model-configuration/provenance fixtures: a synthetic report
plots a penetration depth, then compares a mesh spacing to a differently
normalized depth without stating a threshold or boundary condition. Acceptance:
bind each number to its quantity definition, equation or missing-equation
status, units, geometry and time origin. Preserve a monotonic ordering conflict
without silently choosing a correction; label post-hoc algebraic reconciliations
as hypotheses, not recovered author methods. An approximate word is not an
error bar. One depth/spacing crossing is not convergence evidence or a universal
temperature-error sign. Independent readers must freeze definitions before
comparison; different rounded/unrounded input choices remain explicit.
Extend test controls so expected conclusions are actually computed, with
positive/negative cases, rather than a test merely checking a stored constant.
That last weakness was caught and corrected in our local investigation code;
no inspected Sherlock defect or product fix is claimed. Generic synthetic
content only; no actual source, result, identity, private path or metadata.
Queued locally under the archived-destination boundary; not transmitted.

September27 validation-cache recurrence, local only under SFB-004/SFB-005:
a new synthetic checker validated numeric types inside a memoized function.
After a valid integer tuple populated the cache, numerically equal boolean
or float tuples bypassed validation. Root reproduced both invalid acceptances,
then rechecked their rejection after validation moved outside the cache.
Acceptance addition: warm the cache with valid data before exercising invalid
but equality-colliding inputs; cached and uncached paths must enforce the same
contract. This was a local checker defect corrected before fixture outcomes,
not an inspected Sherlock defect, historical-data error or product-wide fix.
Generic reproduction only; no case payload or private paths proposed for
transfer. Deduplicated local queue; the archived destination remains unchanged.

**2026-09-20 parent/exhibit and diagnostic-field extension — local only, SFB-004/SFB-005:**
Extend existing source-chain fixtures with a synthetic adjudication that
describes an undated equipment invoice and a separately dated service invoice.
Acceptance: keep parent-page and exhibit-page namespaces, document versus
transaction dates, adjudicated description versus inspected original, and
group-level payment notation versus individual-check observation separate.
Do not move the neighboring date or general notation onto the uninspected
record; retain qualifiers on the source's explanatory inference. Multiple
readers of one decision are not additional historical source paths.

Extend diagnostic-output fixtures, not a new issue: a generic transfer command
can emit network/certificate metadata through its comprehensive JSON summary
even when the file transfer succeeds. Allowlist status, declared source,
type, size and integrity fields before displaying results; preserve detailed
local records without copying them into reports or feedback. Separately record
warning origin by operation: reproducible pixels and clean extraction must not
erase a render-stage warning. These are observed investigation-workflow needs,
not demonstrated Sherlock defects or fixes. Only generic synthetic content is
proposed; no actual names, case facts, paths, headers or network metadata.
Queued locally while the designated destination remains archived; not sent.

September28 bounded-diagnostic recurrence, same local fixture: an intact local
render log was printed wholesale and overwhelmed the tool's display limit.
Retain the full log, but display bounded warning classes, counts, byte size and
integrity pointer; cap output before emitting it. A truncated console view must
not be presented as complete log review or a clean run. This is an observed
investigation-workflow need, not an inspected Sherlock defect or verified fix.
No source/case payload is proposed. Existing archived routing remains unchanged;
this deduplicated recurrence is local only, not delivered or acknowledged.

**2026-09-20 case-configuration extension — local only, SFB-004/SFB-005:**
Extend existing claim/provenance fixtures: a synthetic report describes general
nonlinear capability, excludes an effect in a named result family, and displays
a later scenario with the same case label in a different file. Acceptance:
preserve the exclusion's stated scope; don't infer identical configuration from
shared case names, software capability or nearby prose. Separate prescribed
initial failures, computed responses, inferred subsequent failures and observed
historical events. A result-view screenshot is not a settings dialog. Two
different hidden configurations can yield the same chosen observable without
either uniquely identifying history. The real review exposed an attribution
trap too: a prior agent's verification question must not become that agent's
factual claim. No Sherlock defect or fix was tested. Generic synthetic content
only; no source title, case facts, named people, private paths or raw metadata
proposed for transmission. Queued locally under the archived-destination
boundary, not sent, acknowledged or activated.

**2026-09-20 project-state extension — local only, SFB-004/SFB-005:**
Extend the existing quantity/state fixture, not a new issue: one synthetic
announcement reports a completed sale, ongoing general work and future
structural alteration affecting different objects. A later completion notice
for the project must not automatically complete each earlier item; a sale
must not become measured mass removal; general structural wording must retain
unknown member/object assignment. Acceptance: preserve assertion date,
described phase, object, evidence type and unresolved joins, including both
material and harmless alternatives. Two source readers exposed this workflow
need; no Sherlock defect or fix was tested. Generic fixture only, no real
source, person, location, case data or raw response metadata. Queued locally
under the archived-destination limit, not sent or acknowledged.

**2026-09-20 model-grid/covariance extension — local only, SFB-004/SFB-005:**
Extend the existing synthetic provenance/certificate controls rather than open
a duplicate issue. An off-grid generated step can fit a sampled ramp family
better than the grid's step family; therefore lowest residual must not be
promoted to a physical mechanism/duration label. Preserve grid definitions,
all candidates, ground truth and model-discrepancy versus measurement-error
status. A second fixture changes time units in a constrained optimization:
primal parameters and active-bound dual multipliers require consistent scaling,
not only rescaling plotted time. Include both interior and active-bound optima;
exact primal feasibility plus a matching dual lower bound must survive the
coordinate change. A real local implementation initially failed that boundary
control and passed after a preserved correction. This is an investigation-tool
finding and proposed generic acceptance fixture, not an inspected Sherlock
defect or verified product fix. Proposed feedback contains only synthetic
variables/data, no case coordinates, identities, sources or private paths.
Pending locally under the archived-destination routing question; not delivered,
acknowledged or activated.

September27 shared-calibration supplement to the covariance item, local only:
synthetic paired curves demonstrate that a truly shared ordinate offset cancels
from their difference, while separate local errors do not; common horizontal
error need not cancel for different slopes. Preserve named shared calibration,
local-error sets, exact-versus-uncertain knot status and full demanded support.
Acceptance: retain an interior extremum missed by endpoint-only evaluation;
return unresolved if any admitted location reaches a gap; distinguish a valid
conservative marginal enclosure from an exact shared-parameter bound, and a
uniform-query hull from a joint distribution or integral-error result. These
extend the existing measurement/covariance requirements, not a newly inspected
Sherlock defect or product fix. Generic synthetic content only, no source or
case payload. Queued under the existing unresolved destination-routing question;
no new delivery, acknowledgment or accepted-engine update is claimed.

**2026-09-20 acquisition-default extension — local only, SFB-002/SFB-005:**
Extend the existing preservation/runtime/partial-acquisition fixtures. Local
downloader source inspection showed that a launcher hash alone omits the
actual interpreter/package, default container fixups may modify downloaded
bytes, and unavailable fragments may be skipped. Generic synthetic acceptance:
pin launcher plus actual runtime/package; distinguish that from full dependency
attestation; disable automatic repair; refuse missing fragments while retaining
partials and diagnostics; exclude inherited proxy/import configuration.
An environment control should inspect key names without disclosing values and
distinguish runtime-added platform keys from inherited user overrides. A stale-
client retrieval error must remain a failed attempt, not source absence or
authentication denial. Preserve it before any separately scoped maintenance
test; do not silently broaden the historical-source search. Root exercised
local child-process/filter controls; independent code and receipt checks do
not mean those controls were independently rerun. These are inspected local
tool defaults and investigation-workflow requirements, not demonstrated
Sherlock defects or verified fixes. No real IDs, URLs, case material, environment
values or private paths belong in the proposed payload. Queued locally under
the existing archived-destination limit; not transmitted or acknowledged.

October 7 recurrence, same acquisition-default fixture: an ordinary download
again invoked an automatic container repair after a prose-only no-remux plan.
The changed copy was retained, a separate repair-disabled acquisition obtained,
and native decoded audio compared equal under the tested decoder. This is an
execution lapse against a known default, not a new historical-evidence claim
or proven Sherlock defect. The existing acceptance requirement should be
fail-closed in acquisition preflight: a raw-preservation job must explicitly
disable repair before execution; a subsequently matching decoded stream must
not retroactively relabel changed container bytes as raw. Deduplicated here;
no case payload, paths, source IDs or new external message. Routing remains
pending at the existing archived-destination boundary.

**2026-09-20 failure/display/baseline extension — local only, SFB-002/SFB-005:**
Extend the existing diagnostic and truncated-display fixtures. A subprocess
timeout can raise before a wrapper preserves captured output; a diagnostic
with warning severity need not contain the literal word “warning.” Synthetic
acceptance: short-timeout and nonzero-exit children with separate known
stdout/stderr; preserve command/status/output on both paths; classify every
diagnostic category or reject unknowns; compare code/dependency/runtime pins
before and after execution. These failure-path controls were exercised in a
local research driver, not in Sherlock. Current completed runs did not time out.
The PDF-source follow-up also returned exit0 and complete decodable images
while emitting configuration/cache errors. Preserve diagnostics and distinguish
byte integrity, visual usability, clean font configuration and numerical-figure
fidelity; none automatically proves the others. A missing-glyph fixture should
fail visual admission even when PNG decoding succeeds. A warned but apparently
complete page requires a documented bounded admission decision, not automatic
promotion to a clean render. This remains a local workflow observation, not a
verified engine defect; no build paths or raw diagnostic payload are proposed
for transfer.
For visual review, distinguish attempted, reliably returned, actually reviewed,
repeated and recovered images. A truncated batch is not complete review;
permit only logged recovery within the frozen coverage. Save quantitative
baseline/reference envelopes before long sequential review or context changes;
approximate feature locators cannot later substitute for measurements. A
reader lacking those records must report an annotation shortfall, not invent
an onset or blame missing source evidence. These are observed local workflow
needs, not inspected Sherlock defects or verified engine fixes. Generic
fixtures only; no case values, source names, images, private paths or diagnostic
metadata are proposed for transfer. Queued locally under the unchanged
archived-destination routing boundary; not delivered or acknowledged.

**2026-10-08 prerequisite-gating recurrence — local only, same SFB-002/SFB-005:**
A failed output-directory prerequisite was followed by dependent render jobs,
which all failed. This was an observed local orchestration defect, not an
inspected Sherlock defect. Extend the existing failure fixture: an explicitly
denied output-directory setup must launch zero dependent children; preserve
the failing setup result. Recovery must confirm earlier children terminal,
create only an authorized scoped destination, and pass one bounded preflight
before fan-out. Retain original failure receipts separately from successful
recovery and distinguish truncated projections from complete stdout/stderr.
Priority: prevent avoidable repeated failures and false processing claims.
Generic synthetic fixture only; no case source, private path or raw diagnostic
payload. This acceptance test is proposed, not implemented or engine-verified.
Queued locally under the unchanged archived-destination boundary; not sent.

**2026-10-04 image-forwarding recurrence — local only, same SFB-002/SFB-005:**
An image loader received an explicit original-detail request, but the caller
forwarded its image through a helper without preserving that detail argument.
A second reader explicitly preserved it. Recorded displays differed; the
invocation difference does not prove the sole cause of resizing or a product
defect. Extend the existing display-integrity fixture with a synthetic fine-text
page, both forwarding paths, and a larger saved raster that may still be
displayed smaller. Acceptance: retain loader request, forwarding request,
saved geometry and actual returned geometry separately; never call these
matched-resolution reviews merely because source hashes match. Preserve
frozen readings and disagreements; do not assume effects are confined to
known disputed glyphs or silently rerun a failed representation contract.
Priority: evidence-integrity reporting. Generic local workflow note only;
no case images, measurements, names, source IDs or private paths proposed for
transfer. Archived-destination routing remains unchanged; not sent, acknowledged,
implemented or verified fixed.

Same-day local follow-through: both readers explicitly carried the original-
detail request through loader and forwarding helper on the next fixed page
set. No explicit resize notice returned. This verifies the recorded invocation
change only, not matched displayed geometry, an A/B causal test, calibrated
fine-text accuracy or a Sherlock product fix. No case examples are transmitted.

October5 local follow-through on the same fixture: both readers preserved
the original-detail flag at both stages, yet the larger representation
explicitly reported resizing. Record that as a display limitation, not a
failed source hash or proof that the invocation repair had no effect. A larger
delivered image still did not resolve the selected fine-detail relationship.
This updates the existing workflow observation, not a new product issue or
verified Sherlock fix. No real images, identifiers, dimensions or case findings
are proposed for transfer; archived routing remains pending locally.

October8 source-dimension recurrence, same SFB-002/SFB-005 fixture: copying a
neighboring raster's width into a new protocol can pass synthetic display
checks while the actual-source preflight rejects it. The guard correctly
stopped the local run before output or annotation; this is an analyst setup
error, not an inspected Sherlock defect. Generic reproduction: two image
families share height and color mode but have different stored widths.
Acceptance: obtain geometry from each pinned source before freezing its
protocol, test wrong-width rejection, preserve failed configurations, and
record a prospective amendment rather than quietly revising source metadata.
Keep orientation-display size separate from stored-pixel size. No real image,
dimension, source identifier, path or case result is proposed for transfer.
Queued locally under the existing archived-destination routing boundary;
not sent, acknowledged or verified as an engine change.

**Same provenance fixture, note-order recurrence, local only:** A repeated
patch anchor placed a final observation section before intermediate sections,
although the actual view/save operations followed the declared sequence.
Preserve the frozen artifact and disclose the layout error; do not treat
heading order as independent evidence of acquisition/observation chronology.
Synthetic acceptance: reject ambiguous insertion anchors, verify expected
section membership/order before freezing, and retain an append-only operation
sequence separately from the editable presentation. This is an observed local
authoring error and improvement need, not an inspected Sherlock defect.
An interruption extension is now needed: a source view followed by an unrelated
user request and context handoff can leave the note unsaved until resumption.
Synthetic acceptance should retain the view/save sequence and delayed-note
attribution, prevent an automatic immediate-recording compliance claim, and
require preservation before the next source view. Independent agreement may
support the content but cannot retroactively cure the timing deviation.
Generic fixture only; no real sources, case values, personal fields, private
paths or images proposed for transfer. Deduplicated under SFB-002/SFB-005;
archived routing remains pending, not sent, acknowledged or fixed.

Same fixture, source-version transcription extension: a later schedule has a
numeric value where an earlier schedule is blank; a reader accidentally carries
the value backward. Another miscopied numeral creates an apparent subtotal
discrepancy. Synthetic acceptance must bind each transcription to its exact
source version, page, row and field; preserve blank/zero/unknown separately;
and require a source check before calling an arithmetic mismatch a source
anomaly. Keep frozen readings, initial failed arithmetic and a prospectively
declared post-exchange correction distinct. Arithmetic agreement alone must
not choose the preferred numeral or retroactively manufacture independent
agreement. Priority: evidence integrity. This is an observed local workflow
failure, not a demonstrated Sherlock product defect or verified fix. Generic
fixture only, with no case sources, values, identities or private paths;
deduplicated under SFB-002/SFB-005, local only while routing remains unresolved.

**2026-10-04 validation-order recurrence — local only, same SFB-002/SFB-005:**
Separate method and source reviews caught a local adapter branch that rejected
short output before recording a completed subprocess's return code and byte
count/hash. Extend the existing failure fixture: capture basic status/partial
output diagnostics before shape/content validation, including timeout paths;
test the full publication/failure path, not only helper functions. A repaired
local adapter passes synthetic success, short/nonzero, timeout, changed-input
and anchor-mismatch controls. This is not a Sherlock defect or verified engine
fix. The interpreter-selection issue is already covered by the runtime fixture
above. No case data, source names, private paths or raw diagnostics are proposed
for transfer. Deduplicated and queued locally; no archived-task reopen, send,
acknowledgment or reroute is claimed.

The same diagnostic fixture also needs labeled counts: one warning category's
count must not be presented as the count of all warnings. A synthetic mixed-log
test should retain each category and severity, report the aggregate separately,
and preserve a checker's failed assertion when an overlooked category is found.
The local producer's frozen result was qualified, not rewritten to hide its
ambiguous label; no new Sherlock test or fix is claimed. This extends the same
queued generic fixture, without source identifiers or diagnostic payloads.

**2026-10-03 content-quality recurrence — local only, same SFB-002/SFB-005:**
A received video frame can contain severe visual banding while its decoder
reports no warnings and repeated extraction yields identical pixels. Extend
the existing integrity-versus-usability fixture, rather than open a duplicate
issue: a synthetic clip with intentionally embedded stripes and an opaque
banner should pass byte/decoder repeatability while retaining a separate
visual-quality flag and an unobservable-region mask. A passing technical
receipt must not clear historical authenticity or physical-measurement gates.
This is a research-workflow lesson, not an inspected Sherlock defect or claimed
fix. No real image, source identifier, private path or case detail is proposed
for transfer. Queued locally under the existing archived-destination routing
boundary; not delivered or acknowledged.

**2026-09-24 human-coordinate-viewer follow-up — same SFB-002/SFB-005:**
A required human spot-check cannot be fulfilled when the available image
viewer lacks reliable native-pixel coordinates. The user explicitly reported
that limitation; it is not reviewer approval or a negative scientific finding.
A bounded local review surface is now implemented and tested separately from
immutable annotations; human review remains pending. Generic reproduction:
display a known-size synthetic image at
fit/native/doubled size and with scrolling; click a known pixel and move it
with arrow keys. Acceptance: report native rather than CSS coordinates,
preserve pixel-center and boundary conventions, clear stale selection on
image/load failure, distinguish hover/locked points, and never turn an agent
UI test or generic permission into human acceptance. Serve only allowlisted
assets locally, with no writes, uploads, analytics or automatic disclosure.
Actual application tests and human observations remain separate. This is an
observed workflow need, not a demonstrated Sherlock implementation defect;
no case assets, actual annotations, private paths or user data are proposed
for transfer. Queued locally under the unchanged archived-destination limit.

Local follow-through passed coordinate unit tests, allowlist-server tests and
synthetic browser zoom/scroll/keyboard checks. Reduced-scale mouse pointing
can skip native pixels; disclose that limitation and provide native/doubled
scale or single-pixel keyboard adjustment. Preserve loading states and stale
geometry/tool-action failures rather than calling them successful selections.
These local results are not a Sherlock implementation or verified Sherlock fix.

October8 recurrence, same SFB-002/SFB-005, local only: an automated synthetic
click aimed at a cell center in a reduced view reached the adjacent native
row. Delivered event coordinates were not logged; do not diagnose input
quantization or exonerate mapping from marker alignment alone. Retain intended
and reported cells separately. Require fine-view/keyboard checking and explicit
abstention when precise selection remains unreliable; never infer a universal
one-pixel bound. Acceptance for a future diagnostic fixture: preserve source
size, displayed rectangle, DPR, intended input, delivered event coordinates,
reported cell and marker location through zoom/scroll/resize, keeping automated
practice separate from actual human review. This adds diagnostic detail to the
existing reduced-scale fixture, not a new issue or demonstrated engine defect.
No case examples or private paths are proposed for transfer. Still queued
locally under the archived-destination routing boundary; not sent or acknowledged.

October8–9 diagnostic follow-through, same SFB-002/SFB-005, local only:
a separate synthetic-only logger preserved requested versus delivered pointer
coordinates and event-time geometry across twelve fixed Fit/native/doubled
targets. One intended reduced-view miss recurred: adjacent intended rows received
the same delivered position. The independently authored cell-boundary oracle
agreed with all twelve selected cells; recorded geometry was stable. This
supports delivery change as the explanation for the **new** miss, not the
unlogged earlier event, a particular stack layer or a universal rounding rule.
No production mapping repair is indicated by this sample. Six fine-view hits
are not a general accuracy guarantee; retain fine-view/keyboard checks and
explicit abstention. No historical annotation or human acceptance was generated.
The local diagnostic and computational review are complete, not a verified
Sherlock implementation/fix. Preparation failures, a source-pin race and the
replacement packets remain documented; no failed case was silently replaced.
This is a deduplicated workflow result, with no case examples/private paths
proposed for transfer. Still queued under the unchanged archived-destination
routing boundary; not sent, acknowledged or activated.

**2026-09-20 display-integrity extension — local only, SFB-002/SFB-004:**
Extend the existing image/annotation fixtures, not a new engine-defect claim.
Identical first-frame luminance bytes can coexist with animation or rendering
metadata that changes the displayed image. Acceptance: validate frame count and
render-affecting metadata as well as pixels; hash and parse/decode the same
captured byte buffer; independently check each crop/enlargement pixel without
calling the producer transform. Freeze the display transform before viewing.
The next source-association pass exposed a scope error in reusing a normalized
output rule for unchanged older RGB inputs: their source-specific aspect/gamma/
chromaticity metadata differ. Extend the synthetic fixture to distinguish
producer-owned metadata contracts from preserved input metadata; record actual
properties and restrict unsupported photometric/metric comparisons. Do not
silently strip source metadata or claim display equivalence. This is an observed
local-check error and workflow requirement, not an inspected Sherlock defect.
Preserve larger-display visibility separately from physical-component identity,
local crossing separately from final disappearance, and an unresolved endpoint
after a declared hard stop. Actual synthetic animated/transparency and altered-
pixel controls were exercised in the local research helper; no Sherlock engine
fix was inspected or verified. Proposed payload contains generic synthetic
images/states only, no case media, source identities, measurements or private
paths. Pending locally under the unchanged archived-task routing boundary.

**2026-09-20 document-render/admission extension — local only, SFB-002/SFB-004/SFB-005:**
Deduplicate under display integrity and partial acquisition. A completed PDF
renderer can omit a language's text when a CMap/font dependency is missing,
while another installed renderer shows it and the original bytes are unchanged.
Acceptance: preserve diagnostics and both derivatives; reject the incomplete
render as full-page inspection; record renderer/runtime and actual page review,
not just exit status or legible text extraction. A separate local error read a
download before its live transfer completed. Require terminal successful
transfer plus complete size/hash/type checks before parser/admission work;
do not classify an in-flight parse failure as source corruption. Proposed
fixtures use only generic synthetic documents/transfers, no case content,
source identities, personal paths or transport headers. These are observed
local workflow needs, not inspected Sherlock defects or verified engine fixes.
Pending locally; no transmission under the archived-destination boundary.

September27 recurrence: a local caller again attempted PDF parsing while a
transfer handle was still live. Waiting on that same handle to completion and
checking the complete bytes resolved the parse failure. Deduplicate this under
the existing terminal-transfer-before-admission acceptance requirement above;
no new product-defect or verified-fix claim, payload, destination, or delivery.

The final local integrity check also exposed a mistyped expected hash in a
handwritten checker; the captured source still matched an earlier frozen
receipt. Extend the existing fixture with separate source-change and expected-
value-transcription failures. Preserve the first failure; verify the independent
receipt before correcting a checker, never silently rebaseline the source.
Where possible, consume pinned manifest values instead of transcribing them.
This is a local workflow error, not a newly inspected engine defect or fix;
only generic synthetic fixtures are proposed and nothing additional was sent.

**2026-09-20 separate-annotation/censoring extension — local only, SFB-002/SFB-004:**
Extend the existing event fixture, not a new issue. Require both annotation
records and their hashes before exchanging candidate findings; procedural
status may pass without revealing observations. Preserve actual viewed-index
sets separately from extracted sets, overlap/union counts and repeat displays.
Synthetic acceptance: two observers share a last-visible object but have
different nested onset brackets; neither can trace the final crossing through
an occluder. Report their separate one-sided bounds and conservative envelope,
without treating persistent nondetection as a positive post-event state,
shared annotations as independent sources, or the extraction window's end as
an upper bound. Agreement cannot authenticate component identity. A later
lossless enlargement is a disclosed sensitivity pass, not added resolution or
a new blind replication. These are observed workflow needs, not inspected
Sherlock defects or verified fixes. Proposed payload is generic only, excluding
case values, source identities, media and private paths. Pending locally;
the archived destination and unanswered routing boundary remain unchanged.

**2026-09-20 event-threshold and access-state extension — local only, SFB-002/SFB-004/SFB-005:**
Extend the existing event-definition fixture with two cameras whose different
occlusion edges make the same object disappear at different times, while the
reference edge itself moves. Acceptance: retain viewpoint, threshold and moving
reference; distinguish last visible, bracketed disappearance and physical
failure; keep opaque intervening frames censored. A nearby figure's timestamp
or uncertainty must not silently become that of the prose claim. Separately,
a rate-limited availability query must remain a deferred access attempt, not
an empty catalog response or missing source. Stop that route without blocking
unrelated local evidence work. These are observed workflow needs, not verified
Sherlock defects or fixes. Only generic synthetic geometry and response states
are proposed; no case values, media, source identifiers or private paths.
Pending locally under the unchanged archived-task routing boundary.

**2026-09-24 composite-image supplement to the display-integrity fixture —
local only, SFB-002/SFB-005:** Use a synthetic PDF figure split across image
strips whose page-space joins align but whose final strip has a different
pixel scale. Acceptance: distinguish one figure from its component objects;
freeze the allowed transform/tolerance before observation; reject a proposed
lossless common-grid assembly when that criterion fails; retain the unscored
figure instead of dropping it from coverage or treating it as nondetection.
Page-layout rendering may supply context but must not silently replace a
native-image contract. Pin imported dependencies as well as the producer;
a later independent calculation can corroborate a result without repairing
the original run's missing dependency closure. The same fixture now includes
recorded dependencies of dependencies: A pins B, whose map pins C. Acceptance
traverses declared maps with explicit relative-path bases, rejects conflicting
pins and missing descendants, and distinguishes required execution inputs from
separately pinned narrative/navigation context. Preserve the incomplete first
run; a versioned before/after repair must retain identical substantive outputs
or explicitly explain any difference. This recurred in local analysis and was
repaired/tested there, not verified in Sherlock. Keep ciphertext, decrypted
encoded-image bytes and rendered pixels distinct. This extends existing
fixtures after an observed local-method limitation, not a demonstrated
Sherlock defect or verified fix. No real image, measurement, source identity,
private path or case material is in the proposed generic payload. Queued
locally under the unchanged archived-task routing boundary; not sent or
acknowledged.

**2026-09-20 access-response follow-up (same SFB-002/SFB-005, local only):**
Add a synthetic transport-success/HTTP-denial fixture: process exit0 with
HTTP403 and HTML must never admit a PDF, while a DNS failure is a distinct
transport state. Preserve exact-target attempt history across clients rather
than counting each client as a first attempt; a stop rule must explicitly
define whether any cross-client retry is allowed. Raw response headers may
carry server cookies and should not be copied into feedback payloads. The
local source check exercised these states, not a Sherlock engine test; no
verified product defect/fix is claimed. No real URLs, headers, identities or
case content are proposed for transmission. Existing destination remains
archived; this deduplicated extension is not delivered or acknowledged.

October 4 recurrence: a local checker printed complete raw response headers
unnecessarily. Use allowlisted header/transport fields for diagnostics and
retain raw headers as local-only preservation material with an explicit staging
guard. Acceptance checks that logs and proposed feedback omit cookie values;
byte-preservation success alone is not disclosure clearance. This records a
workflow error and mitigation, not a demonstrated Sherlock implementation bug.

October 7 recurrence, same SFB-002/SFB-005 fixture: a provider operation returned
successful remote artifact references, but local byte transfers returned
HTTP403 and produced no file. Preserve listed, referenced, transferred and
media-verified as separate states. Requested fields omitted by a normalized
metadata response must not become provider absence. Signed transport links
were also echoed in diagnostic output before saved-response redaction; this
recurs under the existing redact-before-display requirement. Acceptance uses
dummy temporary URLs and synthetic responses to test redaction before output,
stable-ID preservation, stop-on-denial behavior and a public query-parameter
control that must not be misclassified as a secret. Later saved-file redaction
does not erase earlier output. These are observed workflow failures/needs, not
an inspected Sherlock defect or verified product fix. No actual URLs, source
IDs, metadata, case content or private paths are proposed for transfer. Local
only under the unchanged archived-task routing boundary; not sent or acknowledged.

**2026-09-20 archived-link identity extension — local only, SFB-004/SFB-005:**
Extend the existing provenance fixture with an anchor whose displayed URL
differs from its actual archived href, parent links changing capture context,
and repeated partial identifiers across distinct full folder labels. Acceptance:
retain exact observed links and composite names; distinguish a restored index
from independent corroboration, an archived filename from acquired bytes, and
a declared processed upload from a continuous source. A failed metadata route
must not become absent media. Generic synthetic URLs/names only; no case
payload or actual source identifiers proposed for transfer. Observed workflow
requirements, not inspected Sherlock defects or verified fixes. Pending locally
under the unchanged archived-task routing boundary.

**2026-09-20 reviewed-warning prerequisite extension — local only, SFB-002/SFB-005:**
Extend the existing stage-status fixture, not a new feedback item. A known
software color-conversion fallback can emit a warning while native-format
decoding is clean; an unrelated corrupt-frame message must still reject.
Acceptance: retain warned originals, pin the narrow version/source assessment,
test a mixed known-plus-unknown log, and distinguish conversion uncertainty
from corrupted input. Link prior controls, native checks and reference-inventory
identity as explicit prerequisites; a derivative-only receipt must not imply
all prerequisites or human review. A returned signed retrieval link was also
echoed before redaction, recurring under the existing redact-before-display
requirement: saved-file redaction does not erase earlier tool output. Use only
generic synthetic logs and dummy expiring references for a reproduction, no
actual sources, credentials, measurements, private paths or case payload.
These are observed local-workflow needs, not inspected Sherlock defects or
verified engine fixes. Pending locally; unchanged archived-task routing.

**2026-09-20 catalog-semantics extension — local only, SFB-004/SFB-005:**
Deduplicate under existing source/representation fixtures. A dated schema
defines an everyday-sounding tag narrowly, while later public folders return
filenames without the historical attributes. Acceptance: retain field meaning,
edition and actual populated-row status; a schema or screenshot is not an
inventory export, and a no-hit tag/name search is not absent source content.
A below-limit normalized listing with no pagination metadata is not proven
exhaustive. Keep partial-word OCR, missing image-table text and a full-page
visual reading distinct. A successful bounded raw retrieval after a browser
size failure closes only that access gap, not historical authenticity. Generic
synthetic examples only; no case sources, values, identifiers, names or paths
proposed for transfer. These are workflow requirements, not inspected Sherlock
defects or verified engine fixes. Unsent under the unchanged archived-task
routing boundary; no new acknowledgment.

September28 recurrence, same catalogue/schema fixture: a folder-search response
can store entries under `results`, while a child listing uses `files`. A failed
selector must be recorded as a parser/schema error, not zero results. Synthetic
acceptance: preserve one populated example of each response shape, reject an
unknown/missing collection field, and test that neither error becomes a source-
absence claim. Keep an earlier explicit parent link, a later null parent field
and the exact scoped listing request separate. A newly enumerated candidate set
does not retroactively make a prior unrelated scene-screen its content review.
This is an observed workflow recurrence, not an inspected Sherlock defect or
implemented fix. No actual source names, IDs, payloads or private paths are
proposed for transfer. Locally pending under the unchanged archived routing.

**2026-09-27 snapshot-pair supplement to the same fixture, local only:**
A folder index and its neighboring summary can point to different dated
snapshots with different upstream hashes and totals. Acceptance: pin each
retrieved artifact and declared upstream version separately; do not pool counts,
silently repair differences or infer removals from the mismatch. A zero-hit
folder-label search must remain separate from an unrun document-body search.
Use a synthetic two-snapshot catalog to test this. This is an observed workflow
need, not a source-inspected Sherlock defect or implemented fix. No actual case
names, counts, URLs, paths or payloads proposed for transfer. Deduplicated under
the existing catalog-semantics note; delivery remains pending the unresolved
archived-destination routing decision, with no new acknowledgment.

**2026-09-20 encoded-text follow-up — local only, same SFB-004/SFB-005:**
A real locator searched stored email bytes before MIME transfer decoding; a
separate decoded-inline-text pass was required to assess that blind spot.
Extend the existing coverage fixture with synthetic plain, base64 and
quoted-printable inline parts containing the same marker, plus an excluded
attachment containing another marker. Acceptance: preserve raw/decoded scopes,
encoding/error counts and attachment exclusions; find the inline markers without
printing private bodies or claiming attachment coverage. ZIP-name search and
PDF text-layer search need similarly explicit unsearched-content and sparse-page
limits. This is a local-method gap/correction, not an inspected Sherlock defect
or verified engine fix. No actual messages, names, dates, identifiers, file paths
or source text are proposed for transfer. Queued locally under archived routing.

**2026-09-19 boundary/freeze extension — local only, SFB-002/SFB-004/SFB-005:**
Extend existing source-clock fixtures with adjacent-numbered excerpts whose
endpoint scenes differ and a second excerpt that begins with the phenomenon
already visible. Acceptance: reject a seamless join without inventing elapsed
time, onset, extinction or editing intent; source naming and shared landmarks
are not positive continuity. Preserve positive appearances and obscured samples
separately. Extend the paired-review fixture with an asynchronous observer
summary arriving before the lead reviewer freezes: retain the observer's
pre-exchange status but explicitly mark the lead's completed record as
post-exchange. A private earlier impression is not a saved independent record.
The new local helper now separates stage diagnostics/status and descriptive
admission; that tested prototype revision does not establish a Sherlock engine
fix. Generic synthetic scenarios only, no source media, identifiers, actual
results, private paths or case details proposed for transfer. Pending locally
under the unchanged archived-task routing boundary; no new delivery.

**2026-09-19 catalog-normalization and stage-status extension — local only, SFB-002/SFB-005:**
Extend existing provenance fixtures with an official wrapper linking a catalog,
a normalized response that drops requested checksums/parents, and a separately
reconstructed request scope. Acceptance: distinguish provider absence from
connector omission, preserve request/response/version identity and retrospective
receipt status, and separate repository-original from camera-original. A text
extractor's missing link or failed access route must not become source absence.
Deduplicate decode-integrity lessons under the existing media fixture: matching
pixels and correct timestamps can coexist with reproducible concealment errors;
probe and decode diagnostics need separate status, not one automatic-pass label
or decode-only warning list. A tested input option may resolve an audio-metadata
inference without admitting unrelated video errors. Retain full logs and
partial/refused outputs, with independent stage-level admission. Acquisition
logging must redact transient retrieval credentials by construction rather
than dumping a whole raw connector response. These are observed workflow and
local-helper needs, not newly source-inspected Sherlock defects or verified
fixes. Generic synthetic scenarios only; no case files, names, source IDs,
measurements, URLs, local paths or raw diagnostics proposed for transfer.
Pending locally under the unchanged archived-task routing boundary.

**2026-09-19 partial-admission and candidate-review extension — local only, SFB-002/SFB-004/SFB-005:**
Extend existing media fixtures with three distinct outcomes: a recognized
terminal serialization token, an audio-layout inference during video-only
processing, and an unsupported coded-stream feature. Acceptance: diagnose
each separately; preserve failed attempts and partial outputs; require narrow
revision controls before new admission; do not let a harmless syntax repair
whitelist unrelated warnings. A refusal is not proof of corrupt pixels, while
zero exit and generated files are not fidelity validation. Keep whole decoded
inventories, selected samples, overview derivatives and duplicated receipt
references as separate counts. Synthetic sparse sampling of a shorter event
must not be reported as an absence test. For paired reviews, freeze candidate
choices before exchange; retain different maybe thresholds even when final
outcomes agree, and mark later shared follow-ups as post-exchange rather than
independent first passes. These are observed workflow needs, not inspected
Sherlock defects or verified fixes. Generic synthetic examples only; no case
names, images, source identifiers, private paths or raw diagnostics proposed
for transfer. Unsent under the unchanged archived-task routing boundary.

**2026-09-19 annotation-coordinate extension — local only, SFB-002/SFB-004/SFB-005:**
Extend existing provenance/calibration fixtures with an annotated application
screenshot copied into two example folders. Keep author labels, screenshot
pixels, source graph coordinates and native-video queries distinct; folder
placement and duplicate bytes do not establish a geometric mapping or independent
corroboration. Save descriptive observations before showing newly acquired labels,
while disclosing prior familiarity. Count typed motion histories separately from
axes/tape utility objects; differing counts exclude only complete saved-state
substitution, not subset use or proof of deleted data. Acceptance: retain the
unresolved transformations and dimensional source; report exactly what each
independent review checked, and close finite inventories without inventing a
universal gate on fresh measurements. These are observed workflow needs, not
inspected Sherlock defects or verified fixes. Generic synthetic examples only;
no case data, identities, files, images or private paths proposed for transfer.
Unsent under the existing archived-task routing boundary.

**2026-09-19 sampled-branch and saved-row extension — local only, SFB-002/SFB-004/SFB-005:**
Extend existing measurement/source fixtures, not a new issue. Synthetic
reproduction: two resize filters differ on full images but become identical
on a fixed sampling grid; another filter changes which adjacent frame wins.
Acceptance: retain full-versus-sampled identities, dependence and neighboring
alternatives; do not count nominally separate branches as independent checks
or score gaps as exposure confidence. A saved position series may agree after
first-shared-row subtraction while absolute positions and fine printed times
disagree. Keep all pairings, original offsets, coarse-join and strict-time
decisions, rounding bounds and missing states; a baseline zero is automatic.
Test sparse numeric rows before the first surviving key: preserve them without
calling them independent manual marks or confirmed between-key interpolation.
Positive membership outside a publication's time domain must not reverse a
negative result restricted to actual joined rows. Use explicit zero-/one-based
archive and XML namespaces, and retain guard failures before corrected parsing.
These are observed local workflow requirements, not source-inspected Sherlock
defects or verified product fixes. Generic synthetic examples only; no case
values, sources, identities, images, private paths or research reports are
proposed for transmission. Unsent under the unchanged archived-task routing
boundary; no new acknowledgment or bridge activity.

Same-fixture target-exclusion extension (2026-09-24, local only): a similarity
search must not use the transient it will later claim to corroborate as its
matching target. Freeze a broad exclusion before scoring, check both target
locations, and test native-source perturbations through the actual resize
kernel. Keep all cutoff ties and neighboring alternatives; top-k is a review
budget, not a calibrated confidence set. Static and changing regions can select
different or repeated frames without either being silently discarded. Synthetic
acceptance includes blended/duplicate frames, a tie spanning the rank cutoff,
and masked changes that leave scores invariant while unmasked changes affect
them. These extend existing candidate/branch controls, not a new Sherlock bug
or tested engine fix. Generic scenarios only; no case media, coordinates,
identifiers, paths or results are proposed for transfer. Queued locally under
the unchanged archived-destination routing boundary, not sent or acknowledged.

**2026-09-24 parsed-metadata supplement, same SFB-004/SFB-005 fixture:**
A synthetic XML check reproduces a source-coverage trap: an ordinary element
parser drops comments/processing instructions, and reading only node.text
loses immediate text after child elements. A ten-character mixed description
can therefore look five characters long. Acceptance: declare parsed-element
versus lexical-token coverage; retain all immediate text segments, unknown
attribute/tag identities and structured-string cases; preserve root versus
track ownership, duplicates and missing/empty/whitespace/nonempty distinctions.
Hash-only metadata inventory is not plaintext content review, and a display-
visibility flag is not evidence of concealment. Test with generic dummy strings
before real sources and do not emit arbitrary text in errors. This is an
observed local workflow pitfall and acceptance supplement, not a demonstrated
Sherlock implementation defect or verified fix. No case data, source titles,
paths, identities or metadata are proposed for transfer. Locally queued under
the unchanged archived-destination boundary; no send or acknowledgment.

**2026-09-19 summary-lineage extension — local only, SFB-004/SFB-005:**
**2026-09-20 tested joint-feasibility extension:** The local workflow now tests
one shared hidden-precision variable per sample, not separate values for each
overlapping row. Extend the generic fixture with individually feasible
differences that conflict when chained. Require a complete input-checked witness
or a certificate made from valid inequalities summing to an impossibility;
cross-check with a different exact implementation. Keep closed display bounds,
strict interior existence and a selected witness touching a bound distinct.
A computational witness is not a recovered historical observation. Local
synthetic controls and historical arithmetic exercise this requirement; no
Sherlock implementation or fix is claimed. Generic examples only, no actual
table values, case source, identifiers or private paths; remains queued locally
under the same archived-destination boundary, not delivered.

The subsequent printed-table audit adds an acceptance case to the existing
measurement/provenance fixture: a displayed time grid differs slightly from a
nearby encoded rate, and derivative residuals exceed printing bounds under one
clock assumption. Preserve the original failed test; declare source-motivated
alternatives before testing; recompute bounds rather than widening them by hand;
and distinguish individual-row compatibility from a jointly reconstructed
hidden-precision dataset or identified historical settings. A graph's drawn
fit line and an onset label must not become an undocumented fit mask. Two
transcriptions and two arithmetic implementations share their source's errors;
record the exact independence layer. This is generic workflow feedback, not an
inspected Sherlock defect or verified fix. No case values, source documents,
identities or paths are proposed for transmission; the note remains local while
the designated task's archived routing is unresolved.

A summarizer can accurately copy an obsolete output whose quantity semantics
were corrected in another checkout. A report count can also silently exclude
that checkout, and a planning note can label reported cases as completed tests.
Synthetic acceptance: bind each summary claim to source version, quantity type,
execution state and later correction; distinguish row counts from typed objects,
attributed outcomes from independently run experiments, and subset inventories
from the declared corpus. Preserve the original statement and authorship edit
receipts without making model identity a truth criterion. A matching hash must
not clear a false interpretation. These extend observed workflow requirements,
not an inspected Sherlock defect or verified product fix. Generic only; no case
values, identities, source documents, private paths or raw logs are proposed for
transfer. Pending locally under the unchanged archived-task routing boundary.

**2026-09-13 cross-unit synthesis extension — local only, SFB-004/SFB-005:**
Several verified audits can depend on the same missing input or experimental
family. Preserve a dependency identity across reports so repetition cannot
multiply evidentiary weight. Distinguish a changed aggregate confidence statement
from a new measurement, a falsified mechanism, a new ranking or equal odds.
Synthetic acceptance: three reports share one unresolved source edge; one later
report resolves only its byte-search scope. Show the updated edge once, retain
positive and contrary evidence and the old dated assessment, and never promote
conditional technical plausibility to comparative probability automatically.
This is an observed workflow requirement, not an inspected Sherlock defect or
verified fix. Generic only; no case material or sensitive payload. Unsent under
the unchanged archived-destination routing boundary.

**2026-09-13 extension to the existing typed-reference fixture — local only,
SFB-004/SFB-005:** All selected parent cards can be present while their
referenced leaf tables remain absent from the checked files. Acceptance:
preserve consumer/type/source/version edges, distinguish supplied fields from
dependency closure, and state exact negative-search coverage rather than
global absence. Same-number material and curve IDs are not substitutes.
Blank/zero defaults belong to specific fields and consumers, not a global
normalizer. Producer status labels and count-versus-list schema errors are
harness failures, not mathematical disagreements; retain failed attempts and
verify fixed replay inputs separately from output destinations. This extends
the fixture to overlapping byte patterns: a match in two encoding alignments
does not authenticate either encoding, and normalized zero-/one-based ordinals
must retain both original aliases and source identity. Negative literal coverage
must remain distinct from absent generated or externally supplied definitions.
These extend
existing observed workflow requirements, not an inspected Sherlock defect or
verified fix. Generic only, without case data or source payload; unsent under
the unchanged archived-destination routing boundary.

**2026-09-13 numeric-decision reliability supplement — local only,
SFB-004/SFB-005:** Two independent numeric methods can agree within a value
tolerance yet disagree on exact downstream classes or projection flags.
An unresolved category may reflect arithmetic inversion rather than empirical
uncertainty, and including it in a candidate union can change that union.
Synthetic acceptance: preserve numeric values, decision predicates, failed
exact comparisons and uncertainty origin separately; do not promote close
numbers to reproduced decisions. Test a fixed-input rational/outward-interval
reference without tuning physical parameters, preserving the failed floating
runs and original boundary buffer. Unknown input stays distinct from an
outside result. Completeness of a faster broad phase must be tested independently
of agreement among its retained rows. This is an observed workflow requirement,
not a source-inspected Sherlock defect or a verified fix. The generic note
contains no case data or source payload and remains unsent under the existing
archived-destination routing boundary.

**2026-09-13 relation-type and bounded-parser supplement — local only,
SFB-004/SFB-005:** A finite-element-style synthetic graph can connect distinct
node IDs through an interface definition. Preserve separate relation types:
shared node, selected surface, candidate counterpart, initialized pair and
surviving force path. Equal numeric IDs in node/element/part/set namespaces
must not join without an explicit type. A zero direct-graph intersection cannot
exclude indirect transfer; a positive selection cannot establish stiffness or
historical activation. Acceptance fixture: one non-shared interface, one
same-number/different-namespace decoy, one excluded candidate and one unresolved
initialization state; reject promotions between those relation types and retain
all explicit zeros. Keyword-option order and numeric-card order are separate
contracts; reordered options must not discard a heading or shift blank cards.
For large scans, preserve the original error's source/line and a partial receipt
if a later memory-limit check also fails; do not mask the first failure or
invent its missing measurements. Compare compact representations with synthetic
ordered/repeated/null fixtures before using them after a resource failure.
These are observed investigation workflow needs, not source-inspected Sherlock
defects or verified fixes. This generic note contains no case inputs or real
source payload and remains unsent under the archived-destination routing limit.

**2026-09-13 paired-event and measurement-definition supplement — local only,
SFB-004/SFB-005:** A source reports initial failure, later failure, and a
maximum-moment averaging window. A later comparison reports ultimate load and
rotation at that load. Preserve the event/observable pair: selecting the larger
load must carry its associated rotation, not an independently maximized value.
An omitted plot is not automatic exclusion from a summary table; a defective
channel is not automatically a defective whole specimen. Distinguish an
explicit sensor sum/mean recipe from a numerical factor that happens to make
results agree, and a printed-equation defect from proven execution of that
defect. Publication date is not experiment date. Synthetic acceptance: retain
null secondary stages, test membership and channel lineage; reject unsupported
normalization, paired-event substitutions and date promotion; preserve exact
definitions alongside any declared exploratory diagnostic. Also verify that a
named control actually exercises the claimed production branch, rather than
only a separate helper. These are observed investigation workflow needs, not
source-inspected Sherlock defects or verified fixes. No case example, source
payload or result is sent; the designated task remains archived with routing
unresolved.

**2026-09-10 quantity/state and disclosure supplement — local only:** Deduplicate under SFB-004/SFB-005. Synthetic example: a source lists installed capacity, assumes initial contents, reports later recovery, and a downstream model treats an available quantity as an input; another edition retains removed equipment and changes a unit pair. Acceptance: preserve equipment/date/quantity-state/unit/source-family joins and flag unresolved differences, without converting availability into consumption or model input into independent validation. Separately, a publicly downloadable document can carry confidentiality markings: acquisition, inspection, summary, transfer and publication must have distinct permission states. Public HTTP success, a catalog access label or a hash must not clear sensitive contents or transport metadata automatically. These are observed workflow needs, not source-inspected Sherlock defects or verified fixes. Keep the note generic; no source packet, case examples, diagnostics or local paths are proposed attachments. Nothing sent while the designated task remains archived and routing unresolved.

**2026-09-11 revision/quantity-semantics supplement — local only, SFB-004/SFB-005:** A PDF text extractor can flatten deleted and replacement values into the same sequence, losing which value supersedes which. A matching aggregate can also result from different component sets, and the same unit label can conceal different conversion conventions. Synthetic acceptance: retain source-rendered deletion/insertion roles and revision dates; require verified component membership before reconciling totals; preserve the original unit label and declare conversion basis without claiming which value a downstream model used. A source author's statement that a correction never affected calculations must remain an attributed claim until inputs/outputs are checked. Log rejected reviewer misreadings separately from source discrepancies. These are demonstrated investigation-workflow needs, not inspected Sherlock defects or verified fixes. No case values, pages, files, local paths or raw diagnostics are outbound attachments. Pending locally under the existing archived-destination routing limit; no send or acknowledgment claimed.

**2026-09-11 embedded-source qualifier supplement — local only, SFB-004/SFB-005:** Extend the existing source-scope acceptance fixture with a public wrapper whose prose generalizes beyond an attached source's sampling limit, and a footnote naming an interview without its date or transcript. Preserve wrapper and embedded-source page namespaces, the narrower underlying observation, and unresolved interview-identity joins. A shared wrapper or matching person's name must not become independent corroboration. This adds a synthetic workflow acceptance case, not a newly tested Sherlock defect. No real source names, case details, files, paths or raw diagnostics are sent; the designated archived-task routing question remains unresolved.

**2026-09-12 dataflow and lexical-comparison extension — local only, SFB-004/SFB-005:** A synthetic upstream field generator supplies two downstream solvers, while one solver separately supplies damage state to the other. Preserve quantity and direction for each edge; temporal interpolation is not spatial interpolation, and a matching destination input is not proof of its generating program. Add two parsers that hash the same argument with and without a delimiter, classify spaced assignments differently, and leave a shared first-line syntax unresolved. Acceptance: source-locator reconstruction may reconcile hash/count recipes without declaring complete semantic equivalence; retain a tested negative encoding hypothesis and candidate-name ambiguity. Literal-marker absence must not become absence of a generator or historical execution. These extend existing source-role and provenance fixtures, not a newly inspected Sherlock defect or verified fix. Only generic synthetic scenarios are proposed; no case values, source names, arguments, private paths or raw payloads. Pending locally while the designated task remains archived and routing unresolved; no transmission or acknowledgment.

**2026-09-12 calibration/precision extension — local only, SFB-004/SFB-005:** A synthetic model is fit to another model's accumulated work while their force histories differ; a later experimental comparison tunes an unloading choice, and the available experimental curve ends before the simulated failure tail. Acceptance: track the particular matched observable, fit/selection versus untouched evaluation, study date and measured support interval; do not turn one matched quantity or later evidence into general historical validation. A separate printed table has apparent division discrepancies that fit display-rounding intervals, while one formula retains a small precision mismatch. Preserve every row, actual displayed precision, the explicit rounding hypothesis and unresolved inputs; interval compatibility is neither authenticated hidden data nor evidence of fabrication. These extend existing workflow requirements, not inspected Sherlock defects or verified fixes. Only generic synthetic scenarios are proposed; no case values, documents, URLs, private paths or raw diagnostics are sent. Pending locally under the existing archived-destination boundary.

**2026-09-24 calibration/precision addendum — local only, SFB-004/SFB-005:**
Extend the existing calibration fixture with raster graph strips whose model
labels are separate PDF text overlays. Bare image extraction must not become
complete figure evidence; retain clipping versus unclipped placement and
native-resolution uncertainty. Two same-unit outputs need verified quantity
definitions before imposing a work/dissipation identity. Actual human mapping
checks must precede consequential automated graph findings, not only later
application to a real system. Synthetic arithmetic passes and AI agreement
cannot satisfy that gate. These are observed workflow needs, not inspected
Sherlock defects or verified fixes. Generic example only; no case payload,
attachment or transmission. Archived destination/routing remains unresolved.

**2026-09-24 state-ontology/source-key extension — local only, SFB-004/SFB-005:**
A generic source can call an aperture open while retaining some barrier
material; a binary intact/removed schema would silently alter that observation.
Preserve state definition, partial extent and unresolved classification
separately from object identity. A locally held naming key discovered after
annotation must be a versioned context extension, not an unavailable-record
claim or a retroactive blind-reading assertion. Source-inferred order from a
state change must not become independent clock corroboration of that change.
For provenance checks, test filename-exclusion rules from both the target root
and another working directory, asserting excluded path components rather than
assuming a successful search applied them. These are observed workflow needs,
not inspected Sherlock defects or verified fixes. Generic examples only;
no case data or files sent. Existing archived-destination routing remains.

September28 appearance-review recurrence, same state-ontology fixture: two
readers can agree on visible irregular edges and unresolved material while
using different descriptors such as opening-like versus dark framed pattern.
Preserve the raw descriptors, mapping uncertainty, material uncertainty and
display/occlusion limits separately; do not summarize agreement on unresolved
state as agreement on absence. Human review should name the exact target,
record what was actually checked, and leave unchecked targets unaccepted.
Acceptance fixture: one locally surface-like patch in an otherwise obscured
band cannot assign the whole band, and a clearer neighboring object's image
cannot silently replace the declared target. Generic local recurrence only;
no source names, images, case values or private paths proposed for transfer.
This is not a newly inspected Sherlock defect or verified fix. Delivery remains
pending the unchanged archived-destination decision.

Same-day source-display extension: a combined map can prioritize one field
over another, and the same color can encode different classes in adjacent
representations. Synthetic acceptance: retain each panel's codebook and
display-priority rule; do not reconstruct a masked field from the composite
or count a smaller repeated exposure as a second observation. Record a
partly legible embedded workbook title as a locator with explicit glyph
uncertainty, not an acquired native file. This is an observed workflow need,
not a demonstrated Sherlock defect. Generic fixture only, locally queued.

September28 recurrence, same source-display fixture: a cumulative label meaning
"A or B observed at any sampled time" cannot become "B observed at this time,"
and its complement cannot become a resolved negative of B. Synthetic acceptance:
two different event histories yielding the same union display must retain their
different time/phenomenon evidence; an unknown input must not turn into an intact
or absent state. Preserve the separate underlying layers when available. This
extends the existing panel-codebook and coverage lesson, not a new product bug.
No source payload; local only under the unchanged archived-destination boundary.

## SFB-001 — Complete charter creation/versioning

**Observed:** 2026-09-08. **Priority:** P1, real-case setup limitation. **State:** acknowledged; no fix reported.

`sherlock/workspace.py:create_case` accepts question/decision/owner/standard/change criterion, but stores a generic scope, empty exclusions, and empty legal/ethical/privacy/source-safety/retention constraints. `sherlock/cli.py` does not expose a full charter input. `schemas/sherlock/charter.schema.json` already defines these fields. This is verified source inspection, not a runtime exploit or a finding about evidence.

**Impact:** A detailed investigation cannot enter the supported creation path with its actual scope and constraints intact. A separate governing charter must remain visible; do not hand-edit frozen case state to bypass the limitation.

**Requested improvement:** Schema-validated full-charter creation plus append-only charter amendments with visible version/reference history. Preserve backward compatibility without silently dropping explicitly supplied fields.

**Synthetic reproduction:** Create a generic document-comparison case whose intended scope excludes outreach and whose retention/privacy fields contain non-sensitive placeholders. Verify whether the supported creation path can preserve those fields. No real case examples required.

**Acceptance:** Exact field round-trip; malformed/omitted required fields rejected; scope/constraints visible in auditable case state and relevant report views; amendments preserve earlier bytes and ledger history; tests show no silent defaults replacing supplied restrictions.

## SFB-002 — Measurement add-on boundary and media lineage

**2026-10-05 same local ASR route, output-state and runtime extension:**
Preserve ellipsis-only segments and untranscribed intervals separately from
silence or no-event findings, even when repeated machine outputs match exactly.
Keep nearby self-corrections and alternative explanations with event-related
speech. Synthetic acceptance: punctuation-only output cannot become a sound
absence claim, and quotation extraction must not discard a following qualifying
clause. Also name the verified interpreter: an ambient older Python passed
validator-only tests but failed the shared hashing helper before inference.
Preflight must exercise required runtime capabilities, not just imports or
unrelated unit tests. This extends SFB-002/SFB-005; no new product defect,
sensitive example, external send or claimed fix. Archived routing is unchanged.

**2026-10-05 local speech-model route extension — local only, also SFB-005:**
A conversational audio-input failure does not establish that an already cached
local speech-recognition model is unavailable. Inventory authorized local
routes separately from perceptual access. Existing project wrappers may add
domain vocabulary prompts, read unrelated manifests/credentials, or rewrite
transcripts; inspect those side effects before reuse. A neutral investigation
adapter should expose model/source/runtime identities, exact preprocessing,
prompt use, raw text/timing outputs and repeat disagreement, while preserving
human observations as a separate layer. Synthetic acceptance: an adapter
invocation omits an unrelated wrapper lexicon, leaves its project unchanged,
records downmix/resampling, and never converts a spoken report about an event
into detection of that event. This is an observed workflow opportunity, not
a demonstrated Sherlock defect or a claim that ASR supplies human listening.
No private source text, files or paths are part of this generic note. Queued
locally under the unresolved archived-destination routing; not sent or fixed.

**2026-10-04 native-metadata and probe-scope extension — local only, also SFB-005:**
A generic probe/normalized catalogue can omit native source-name/timecode tags
that a bounded container-header check recovers. Synthetic acceptance: preserve
the returned projection separately from field absence; retain raw offsets,
payloads, NUL-terminated text prefixes and uninterpreted binary tails; never
promote editable metadata to an authenticated event clock. Repeated alternate
fields in one file are not independent corroboration. A metadata-output command
may internally decode while discovering stream information, so verify that
behavior before promising zero decoding. Separate output type from execution
scope. Preserve oversized/truncated captures and index-skip defects; cap displays
without converting missing capture into a complete receipt. These extend the
existing provenance/probe and failure-scope fixtures, not a verified Sherlock
bug or fix. No actual names, clocks, case text, source files or private paths in
the proposed generic payload. Queued locally under unchanged archived routing;
no delivery, acknowledgment or new project task.

**Same fixture, eight-item follow-through:** Original and alternate metadata
lanes must remain independently comparable; disagreement should not suppress
both usable values. Prefix equality must not be reported as complete-payload
equality when binary tails differ. A source-order conflict can survive every
within-clip frame choice while still depending on unverified camera-versus-
edited-master semantics. Synthetic acceptance must preserve that conditional
conflict, test both interpretations, retain mixed lossless byte encodings, and
neither authenticate chronology nor erase the conflict merely because an edit
is possible. This is a workflow/test requirement, not a verified engine defect.
Only generic examples are queued locally; archived routing and no-send status
remain unchanged.

**Same fixture, display conversion versus evidence validation:** A primary
library's display helper maps invalid counter digits to zero. An investigation
adapter must preserve invalid/unknown components and raw bytes instead of
inheriting that convenient display fallback. Synthetic acceptance: malformed
digits, omitted counter labels, changing counting modes, repeated/skipped
values and day-wrap candidates stay explicit; an accidental one-step difference
across a mode change is not continuous timing in one convention. Matching a
stream counter to an editable file label supplies internal consistency, not two
independent clocks. This is an observed integration risk and tested local
contract, not a source-inspected Sherlock defect or product fix. Generic note
only; no case values, files or private paths, and no send under archived routing.

**Same fixture, visual-clock dependency extension (also SFB-004):** A source
image can be dated using an observed object's state; an enlargement or derived
map may inherit that time. Neither the extra representation nor its new label
creates an independent clock or validation observation. Synthetic acceptance:
retain the image-to-state-to-inferred-time dependency graph, shared offsets and
unexplained travel/dwell assumptions; do not convert overlapping marginal
ranges into an independent relative-time confidence interval. Permit explicit
joint reconstruction but reject an independent-validation label when it reuses
the state that supplied its clock. A primary workflow description is not proof
of its application to a particular file. This is a method-contract need, not
an inspected Sherlock defect or fix. Only generic examples remain locally queued;
no case imagery, clocks, source IDs or private paths are proposed for transfer.
No send or acknowledgment under unchanged archived routing.

**Same fixture, executable search-specification check:** A saved pattern map
can contain extra escaping even when the recorded search results are correct.
Preserve that original, publish the exact executable pattern/flag map separately,
and reproduce every declared source/page count before calling the search
reproducible. A display representation is not automatically executable syntax.
The local investigation corrected and checked its own artifact; no Sherlock
implementation or product fix is claimed, and no new payload was delivered.

**Same fixture, metadata-storage recurrence:** A whole-item compressed-output
allowance rejected completed raw-metadata inventories. Synthetic uniform data
had not predicted the historical bytes' storage size. Do not discard unexplained
padding or selected metadata fields to force a pass. A versioned correction may
partition lossless metadata at fixed frame boundaries, with explicit per-artifact
and total bounds, exact gap-free coverage, strict decompression and byte equality,
exclusive output creation and final source checks. Preserve the original refusals
and distinguish a newly enlarged total storage contract from meeting the old
limit. This is a local pipeline design issue and a generic regression-test need,
not a verified Sherlock defect or fix. No case files or raw values are queued
for transmission; unchanged archived routing keeps the note local and unsent.

Local retest: the revised storage implementation passed boundary, corruption,
collision and incomplete-output controls, including a high-entropy synthetic
fixture and a real synthetic container-to-artifact round trip. The new bounded
historical collection also completed; the old cap failures remain recorded.
This verifies the investigation's local correction only, not a Sherlock product
change. Byte-consistent metadata still requires a separate provenance/clock
interpretation; storage success must not auto-promote it to historical truth.

**2026-10-03 diagnostic-format recurrence — local only, same fixture:** A strict
producer-specific parser accepted a zero-valued runtime throughput field but
refused a space-padded integer form during a larger run. Synthetic acceptance
should cover supported producer formatting independently from encoded media
timing, while still rejecting unknown lines, warnings and changed frame joins.
Preserve the original failed log and admission; a diagnostic-only in-memory
normalization is not permission to relabel it clean. Any grammar correction
requires a new pinned version, negative controls and a declared execution
schedule. This is an observed local investigation-parser defect, not an
inspected Sherlock defect or verified fix. No case media, raw logs, values or
private paths are proposed for transfer. Queued locally under the unchanged
archived-destination boundary; no send or acknowledgment.

**October 4 local verification follow-through, same recurrence:** Checked the
producer's tagged primary source before permitting exactly its single-ASCII-
space padding at one named field. A separately identified wrapper preserves
the original module and refused output, records both parent and wrapper hashes,
and keeps cumulative resource accounting across versions. Author and independent
fresh controls passed; new paired extractions also passed while earlier products
remained excluded. Tests distinguish inherited child-process coverage from
actual configured-wrapper coverage. This verifies the narrow local correction,
not a Sherlock implementation or fix, historical source authenticity, or a
general diagnostic normalizer. No new payload, send or acknowledgment.

**2026-10-03 resampling exclusion extension — local only, same fixture:**
During method preparation, both reviewers identified that a nearest-resized
validity mask can admit values contaminated by bilinear mixing from excluded
pixels. Mask disjointness alone does not test this. Add a synthetic pair with
identical permitted content and contrasting excluded content; require identical
values at every declared-valid output location through every allowed resize
and field-selection branch. A conservative buffer is acceptable only in its
tested domain, with lost coverage explicit. Priority: before relying on scored
measurements. This is a diagnosed local method-design risk, not an inspected
Sherlock bug or verified product fix. No case imagery, coordinates, paths or
results belong in the proposed payload. It remains unsent under the existing
archived-destination routing boundary.

**Photometric fit/evaluation supplement — local only:** A rectangle labeled
"background evaluation" can overlap a separately named training rectangle.
Require an actual mask-intersection assertion after resampling/exclusions,
not independence inferred from role names. Preserve the original geometry fit
and version any new photometric mask. Synthetic acceptance should include
global tone changes and local/displaced bright patches, empty threshold unions,
clipping ties, and bright values outside the training intensity range. Report
that extrapolation and distinguish encoded-bright-pixel support from physical
fire area. These are observed investigation-workflow needs, not an inspected
Sherlock defect or fix; no case examples or attachments are proposed. Delivery
remains pending the existing archived-destination routing decision.

**Reviewer-disclosure clarification, same pending item:** Record which parent
observations, candidate labels and scores were available before each qualitative
checkpoint. A hint arriving mid-review changes the remaining interpretation's
independence; a later note must not relabel the whole pass blind. This generic
acceptance requirement is local only, not a new delivery or implementation claim.

**2026-09-19 freeze-receipt extension, same pending item:** A reviewer can save
an independent annotation and immediately send its coordinates while the other
reviewer's estimates still exist only in reasoning. Synthetic acceptance:
release comparison payloads only after both saved-artifact hashes/receipts exist;
otherwise retain the exact exposure order and downgrade only the affected
independence claim. Numerical agreement cannot retroactively satisfy the gate.
Also preserve upper-versus-lower endpoint definitions when similarly named
features from separate studies are joined, and distinguish an archive-name
search from semantic inspection of differently named members. These are
deduplicated workflow requirements, not inspected Sherlock defects or verified
fixes. No real coordinates, source names, files, paths or case details are in
the proposed payload; it remains local under the unchanged routing boundary.

**2026-09-24 label-boundary extension, same SFB-002/SFB-004 fixture:** Two
readers can both reject a distinctive landmark while one calls its visible
host edge ambiguous and the other calls the landmark unavailable. Preserve
host-region visibility, landmark localization and correspondence/change as
separate fields; do not turn overlapping label semantics into apparent
physical disagreement or retroactively recode to manufacture consensus.
Synthetic acceptance must also distinguish a visible candidate from a
measurement-suitable point. An explicitly source-guided saved-point overlay
must not be advertised as independent point selection. This is an observed
local annotation-contract weakness, not an inspected Sherlock defect. Generic
only; no case names, data, coordinates, images or private paths proposed for
transmission. Still queued locally, not delivered, acknowledged or fixed.

**2026-09-24 rounding/domain supplement, same SFB-002/SFB-004 fixture:**
A synthetic value immediately below a half-cell boundary can cross that
boundary when floating addition rounds before `floor` is applied. The local
reproduction returned different cells for float-add-then-floor and exact
half-up arithmetic on the same binary input. Declare the rounding convention,
test adjacent-to-tie values, and distinguish original continuous-domain
membership from rounded-cell membership and crop padding. Preserve a plain
crop, a separately marked copy, validity masks and exact saved coordinates;
a display convention is not a physical localization error bound. This is a
reproduced generic numerical/display pitfall, not an inspected Sherlock bug
or a demonstrated historical measurement error. No case values, images,
names, paths or source payloads are proposed for transfer. Local queue only;
archived-destination routing is unchanged and no delivery/fix is claimed.

**2026-09-13 scene-plane and seek-coverage extension — local only, SFB-002/SFB-004:**
A synthetic scene can retain highly correlated foreground buildings while its
background and dynamic regions differ. Keep registration regions, background
checks and post-fit dynamic diagnostics separate; retain repeated-grid aliases,
full candidate coverage and prior-viewed versus unused evidence. A score band
is not a confidence interval or unique exposure. In a second fixture, seeking
preserves an earlier keyframe lead-in and a short input-duration allowance
omits a selected interval's final frames despite successful decoding. Require
exact per-frame PTS-list coverage and known-anchor pixel agreement, not merely
exit status or one sample per second. Preserve the failed partial output and
version the read-window correction without changing the selected interval.
Reproduction must verify the completed prior recipe, actual arrays and saved
native pixels, including recomputed shortlist membership; sharded limits need
aggregate accounting that includes failed runs. Nonfinite timestamp strings
must fail explicitly. These extend existing local workflow acceptance tests,
not a source-inspected Sherlock defect or a claimed Sherlock fix. Only these
generic synthetic cases are proposed for later triage; no case values, media,
private paths or raw diagnostics. Not sent while the designated task remains
archived and routing is unresolved.

October 7 extension to the same SFB-002/SFB-004 scene-correspondence fixture:
reversing a list of scored rows is not a test of changing-image sequence order.
Use invented image sequences with identical stationary scenery and distinct
changing regions, then reorder the reference images. Acceptance preserves
ambiguous stationary assignments while recovering the reordered changing-detail
candidates; it must not issue an original-clock or soundtrack certificate.
Keep candidate-set alternatives, coarse-sampling endpoints, mask-dependent
detail and aspect normalization explicit. A good candidate can justify a dense
test without authorizing post-result threshold/region tuning. The local
synthetic control was added and passed before historical execution; this is a
workflow correction, not an inspected Sherlock implementation defect or
verified engine fix. Generic invented examples only; no source images,
identities, measurements, private paths or case data proposed for transmission.
Unsent under the unchanged archived-destination routing boundary.

Dense-refinement clarification for that same fixture: reject duplicate index
entries, not distinct presented indices carrying identical pictures. A new
synthetic control retains all such entries. A top-two visual shortlist can
sample only one near-identical cluster while other near-best bands remain
unviewed; retain those alternatives and forbid a uniqueness certificate.
Refining a previously selected time window is not independent corroboration.
These are local workflow safeguards, not an inspected product defect or new
issue family; no case payload or delivery is added.

**October 8 common-support recurrence, same SFB-002/SFB-004 fixture, local only:**
Two fitted transforms can admit equally many pixels at different positions.
Comparing scores on those different sets can misattribute a support change to
geometry. A synthetic fixture now explicitly gives equal-cardinality but
unequal-position valid sets. Acceptance records both sets and their intersection,
evaluates the already selected transforms on that common set without refitting,
and applies coverage against the original full-mask denominator. Preserve
missing-transform and coverage/variance failures rather than replacing them
with zero. Independent controls pass for the differing-position fixture and
common-support gates. This extends the existing scene-correspondence contract,
not an inspected Sherlock defect or a verified product fix. Only this generic
synthetic lesson is queued; no case images, values, identities, private paths
or raw diagnostics are proposed for transfer. Unsent while the designated
destination remains archived and routing unresolved.

**Observed need:** 2026-09-08. **Priority:** P2, required before quantitative media work. **State:** acknowledged; no fix reported.

The README documents specialist processing only for deterministic text comparison. A separate media workbench currently preserves bytes and derivatives; a validated motion/audio-measurement bridge is not established here. This is a capability request, not a claim that every underlying schema field is missing.

**Requested improvement:** A documented add-on contract for time-based measurements: original presentation timestamps and edit/duplicate/drop maps, source/derivative IDs and hashes, units and coordinate transforms, calibration, uncertainty, procedure/environment hashes, diagnostic failures, and a limited claim ceiling. Keep measured motion separate from inferred event cause.

**Synthetic reproduction:** Import a known-trajectory video and synchronized test tone with deliberate edits, variable frame timing, and duplicate frames. No real footage or case records required.

**Acceptance:** Timestamp/lineage preservation; error within declared calibration/tracking tolerances; unsupported/unaligned input fails visibly; equivalent reruns reproduce results or meet declared numeric tolerances; reports retain uncertainty and do not promote a measurement into a causal finding automatically.

**2026-09-08 technical supplement acknowledged:** Synthetic review of the local timing prototype exposed default autorotation/autoscaling and output clock normalization. The corrected diagnostic disables implicit transforms, validates per-frame geometry/format, checks exact rational source/output PTS alignment, rejects malformed hashes, and preserves initial/sanitized failure provenance. These generic acceptance lessons were sent under SFB-002, without historical footage, case results or private metadata. The destination turn completed and direct inspection of its FEEDBACK.md confirmed the requirements were appended under SFB-002. This supplements the same issue; it does not claim Sherlock has implemented or validated the method.

**2026-09-11 acoustic-method supplement — local only, SFB-002:** A measured default downmix can differ from an arithmetic mean; independent-channel content can cancel; direct seeking can return different decoded samples than full-file decoding at the same requested interval. Plot limits can hide retained numeric peaks, and machine transcript segment offsets can be mistaken for sound or visual event times. Synthetic acceptance: left-only/right-only/in-phase/antiphase fixtures; measured mixing coefficients; full-decode versus seek comparisons with retained residuals; explicit plotted-versus-numeric range checks; separate audio sample clock, video PTS, transcript navigation and independently reviewed event annotations. A successful rerun must not imply source authenticity or detection calibration. These are observed workflow needs, not demonstrated Sherlock defects. No case files, values, source names, paths or raw diagnostics are proposed for transfer. Delivery remains pending under the archived-destination routing limit.

**October 7 waveform-specificity extension, same SFB-002/SFB-005, local only:**
A synthetic repeated tone produces multiple perfect waveform matches, whereas
a shifted nonperiodic passage has a recoverable offset. Acceptance: retain full
signed search profiles, competing peaks, undefined low-energy scores, channel
pairs and explicit candidate selection; separate sample-grid resolution from
timing accuracy. A scale-one failed screen must not exclude shared material
after speed or other processing changes, and reversal is not a calibrated
independent null. Historical execution should require a successful controls
receipt tied to the actual code, protocol, runtime and decoder pins. These are
tested local workflow needs, not newly inspected Sherlock defects or fixes.
No case payload or real results proposed for transfer. Deduplicated here;
not sent while the designated archived-task routing remains unresolved.

**2026-09-11 visual-coverage supplement — local only, SFB-002:** Extend the existing media fixture with endpoint samples separated by an uninspected interval, later refinement that starts after a visible change, and two synthetic containers with identical decoded pixels/timestamps but unequal container bytes. Acceptance: a negative claim requires explicit temporal and resolution coverage; refinement keeps its original declared selection and cannot become earliest-onset coverage retrospectively; distinguish byte identity from decoded-product identity and record runtime pins for each execution. Separate shot changes, foreground actions, camera movement, transcript pointers and structural features instead of assigning a generic event-onset field. This records demonstrated workflow needs, not inspected Sherlock defects or verified fixes. Only the generic fixture is proposed for later transfer; no case frames, values, names, paths or local diagnostics. Not delivered while the archived destination's routing remains unresolved.

**2026-09-24 spatial-versus-temporal addition to the same SFB-002 note:**
A spatially visible region is not a calibrated transient-detection opportunity;
a hidden source may illuminate another exposed region. Synthetic acceptance:
retain separate source-region visibility, observable outward effects, exposure/
sampling coverage and detector sensitivity. Distinguish an unseen boundary
behind foreground from an unlocated boundary possibly outside the frame.
Preserve categorical reviewer disagreements without translating them into
area fractions. In a later sequential fixture, retain an isolated one-frame
bright change as a descriptive candidate rather than requiring persistence
that deletes it automatically; neither that candidate nor its absence identifies
a mechanism. This extends the existing generic coverage contract, not a new
Sherlock defect/fix claim. No case data or images proposed for transfer;
local-only pending the unchanged archived-destination routing decision.

September28 persistent-state extension to that same SFB-002 coverage fixture:
observing a lower region earlier and an upper region later must not create
unobserved lower-region/later coverage. Conversely, a resolved post-event image
may test a persistent effect without continuous footage; a transient or newly
occurring transition has a different temporal contract. Acceptance: preserve
joint place/time/quantity support, distinguish absent index tags from absent
pixels, and never relabel a negative observation of one phenomenon as a negative
observation of another. This is a generic workflow need, not a verified product
defect. No case payload; queued locally, not sent under the archived routing gate.

Sequential-page follow-through, same note: synthetic overlapping batches
should distinguish a reader's first-frame missing incoming context from a
poor-quality-image uncertainty. Preserve both readers' shared boundary rows;
repeated context is not another vote. When several images are displayed
together, record saving before the next page, not before the next already-seen
frame. Acceptance also requires row-scoped coverage parsing: an index repeated
in explanatory prose must not become an extra observation. A local bookkeeping
check initially made that mistake and was corrected without changing the
observations. Fixed-sample reannotation and result-selected follow-up remain
separate states. Generic fixture only, no case payload or new transmission;
this is a workflow lesson, not a verified Sherlock defect or fix.

The same fixture should distinguish a newly selected candidate, continuation
of an existing candidate, and no additional candidate. Otherwise equal scene
descriptions can receive different codes without being contradictory physical
observations. Include a brief separate point inside a longer changing-edge
interval: grouping consecutive positive rows must not erase that nested
candidate or turn every retained row into a separate event. Acceptance preserves
original descriptions, candidate identity/location and initiation/continuation
uncertainty without post-result relabeling or vote-derived confidence. This is
a generic schema/workflow improvement, not an inspected product defect; it is
queued locally under SFB-002 with the same no-transmission boundary.

Source-copy follow-through, same SFB-002 contract: a PNG fixture should encode
the same pixels through two byte-distinct valid streams. Verify each against
its own receipt before comparing complete decoded arrays; unequal file hashes
are a check trigger, not by themselves corruption or a new historical source.
Stored pixel-hash agreement alone is not a fresh decode check. Include a
full-frame metadata list with only a sparse set of actual image products;
report metadata rows, existing images and reviewed images separately. These
extend the existing representation/coverage fixtures, not a new product-defect
claim. Generic synthetic examples only; queued locally, not transmitted.

**2026-09-11 decoder-localization supplement — local only, SFB-002:** A diagnostic warning without a timestamp cannot be attached to the nearest message from a concurrent pipeline. Synthetic acceptance: nested context prefixes, interleaved unrelated stages, repeated/suppressed messages, terminal warnings and unrelated fatal errors; require complete same-context association and source/output clock/count checks. Preserve a marked preamble separately from later measurement selections: disjoint indices neither prove those selections damaged nor certify them clean. Keep exact source-copy bytes distinct from executable-equivalent text and separately label analyst annotations in machine-result summaries. These are demonstrated local workflow needs, not inspected Sherlock defects or verified fixes. Only generic fixtures are proposed for later feedback; no case values, images, source names, paths or diagnostics. Pending locally while destination routing remains unresolved.

**2026-09-11 intensity/time non-identifiability supplement — local only, SFB-002:** Add a synthetic acceptance witness where distinct acquisition and postprocessing histories have identical sampled arrays and presentation times. Preserve both histories rather than treating a classifier tie as an implementation defect. An image-space interpolation coefficient is not an exposure fraction; retain unclipped coefficients, native-clock versus fitted residuals, zero-span undefined values, and ordinary motion/noise counterexamples. A fixed screen region may become foreground or occlusion and must not silently remain a material track. These are demonstrated local measurement-workflow needs, not verified Sherlock defects. No case identifiers, values, images, paths or operational metadata are included in the proposed generic note. Not sent while the designated destination remains archived and routing unresolved.

**2026-09-11 sampling/diagnostic clarification — local only, SFB-002:** Further observed acceptance cases for the existing visual-coverage and diagnostic notes: a video with orderly PTS and clean video decoding can already contain mixed/banded image interruptions; an unmapped audio-layout diagnostic should remain a separately classified, preserved warning rather than silently invalidate or certify video pixels. Synthetic acceptance: insert degraded mixed frames into a regular-clock fixture, verify that byte identity does not become continuity, retain unsampled gaps and nonblind reviewer hints, and reject all diagnostics outside a prospectively declared narrow grammar. Separate raw address-bearing logs from deterministic image/selection outputs. These extend existing workflow needs, not newly inspected Sherlock defects. No case examples or diagnostics are proposed for transfer; delivery remains local-only under the unanswered archived-destination routing boundary.

**2026-09-11 reference-identity/registration supplement — local only, SFB-002/SFB-004:** A textual landmark description can be paired with the wrong pixel coordinate; repeated nominal manual coordinates and self-correlation do not verify the intended feature. Synthetic acceptance: place a bright corner beside a low-texture region, supply a misplaced annotation, and require a baseline marker/patch overlay with separately recorded identity and texture checks before freezing a reference set. Preserve the original annotation and post-output correction as distinct records; do not silently replace evaluation points or confuse coarse envelope agreement with verified material identity. Also retain nearby tied peaks even when a distant-competitor margin is large; image-clipped search support; all-reference admission failures; and a flexible fit whose omitted-reference prediction worsens despite smaller training error. A common coordinate error can pass both training and leave-one-out checks, so those are not independent validation sources. These are demonstrated local workflow needs, not inspected Sherlock defects or verified fixes. Only generic synthetic fixtures are proposed; no case values, frames, source names, private paths or operational metadata. No transmission while the designated task remains archived and routing unresolved.

**Additive repair-contract acceptance, same SFB-002/SFB-004 item — local only:** A copied preflight can be internally rehashed yet disagree with the approved candidate object or first-qualified choice. Bind the consumer to the exact declaration, visual review, parameters, procedure and source identities; test an actual altered/rehashed file through the entry point, not only a pure validation function. Preserve the finite rejected calculations before failing. A result at a numerical cutoff can change its binary flag between correct floating implementations: retain the declared flag, report arithmetic tolerance/conditioning and use exact reasoning where available, rather than calling solver roundoff a physical discrepancy. Initial procedure pins and final dependency unions have different roles; reviewers must verify their declared relationship, not assume identical inventories. Distinct repeated-run directories are also necessary to claim two executions. These are demonstrated local workflow needs, not inspected Sherlock defects or verified fixes. This extends the existing generic fixture only; no case payload or new transmission is authorized while routing remains unresolved.

**2026-09-12 appearance correspondence and differential inference — local only, SFB-002/SFB-004:** Extend the existing annotation contract with a generic fixture where two analysts place the same visible corner at the same coordinates but disagree about whether it continues the original feature. Preserve location and correspondence as separate fields; rectangle overlap cannot repair identity. Include a second fixture where one displacement interval excludes zero and another includes it, but their difference still includes zero: separate threshold outcomes do not establish a difference or event order. A third fixture removes one reference map at an earlier selected sample; the first available positive mapped interval moves later without changing the underlying observations. Report that as an availability effect, not delayed motion. A marked derivative must not inherit an unmarked-image caption, and display-cell origins versus centers must be explicit. These are observed local workflow needs, not inspected Sherlock defects or verified fixes. This generic supplement contains no case measurements, names, images, private paths or source payloads. Delivery and acknowledgment remain pending the unresolved archived-destination routing; no transmission occurred.

**2026-09-12 calibration/clock/feature-join supplement — local only, SFB-002/SFB-004:** Preserve assigned units separately from independently verified physical calibration. A tape can reproduce a stored transform exactly while several different landmark pairs share its length. Synthetic acceptance: retain candidate endpoint identities and distinguish floor level, window top and parapet; do not manufacture a discrepancy from unlike quantities or validate endpoints with scalar agreement. Distinguish pixels-per-length from length-per-pixel, playback rate from analysis and exposure clocks, constant origin shifts from window/initial-condition changes, and horizontal-marker amplification from vertical physical descent. Require clock-rate sensitivity with its squared effect and correct direction; do not treat arbitrary synthetic parameters as historical error bounds. Reject calibrating a measurement by assuming the very quantity it is meant to test, while permitting a separate authenticated calibration experiment. Missing provenance must not automatically become a measured distortion or a veto on explicit conditional reasoning. These are observed investigation-workflow needs and tested mathematical fixtures, not inspected Sherlock defects or verified fixes. The proposed generic note includes no case data, names, source paths or payloads. Delivery remains pending locally under the unresolved archived-destination routing boundary.

**Additive endpoint/repetition acceptance, same SFB-002/SFB-004 item — local only:** Extend the calibration fixture with a query at a foreground boundary and visible repetition nearby. Preserve direct endpoint identity separately from an extrapolated row and indirect approximate-scale support; neither occlusion alone nor a strong periodicity score resolves the calibration. Nested windows and repeated transforms reuse evidence and must not become independent confirmations. Exact saved coordinates and display-centre/corner conventions are not physical localization precision. Check declared versus actually generated display labels and exact-point exclusion versus patch overlap; retain a scoped discrepancy instead of silently rewriting a frozen declaration. These are demonstrated investigation-workflow needs, not inspected Sherlock defects or verified fixes. This generic extension includes no case values, images, names, paths or source payloads. Nothing sent; archived-destination routing remains unresolved.

**Additive conditional-fit and annotation-history acceptance, same SFB-002/SFB-004 item — local only:** A saved “keyframe” may represent manual or automatic marking, or a loader fallback; membership is not a historical provenance trail or independent measurement. Extend the generic fixture with preserved positions, optional key metadata and distinct original/derived states, including a strictly validated alternative numeric-array serialization. Retain the initial format rejection and recoverable code rather than calling it scientific missingness. For trajectory tools, preserve every declared overlapping window and model, the polynomial normalization and derivative response weights; do not promote a window-centered coefficient to an instantaneous event or turn coincident nominal/encoded clocks into independent corroboration. Unit perturbation response is not a measured uncertainty distribution, and a plotted near-reference segment must not replace all-window results. These are demonstrated workflow needs, not newly inspected Sherlock defects or verified fixes. No case values, tracks, media, names, paths or payloads are proposed for transfer. Delivery remains pending locally under the existing archived-destination boundary.

**Further acceptance cases for SFB-002/SFB-004 above — local only, 2026-09-12:** A fixed-image-column silhouette sample and a material landmark require different observable types; common vertical translation can cancel while horizontal motion changes the sampled contour. Preserve a known sampling coordinate when the other coordinate becomes unlocalizable. For subjective interval propagation, distinguish each window's feasible coefficient from one jointly feasible sequence across overlapping windows; retain any constructed feasibility witness as a calculation, never an observation or probability. Numerical texture-screen success must not overwrite a separate visual rejection. Negative-control records should preserve attempted inputs (nonfinite values symbolically), not just rejection names; derivative failure receipts should cover exception paths as well as explicit mismatches. These extend the existing synthetic annotation/fit/failure fixtures, not a new issue or an inspected Sherlock defect. No case data, images, measurements, source names or private paths are proposed for transfer. Still pending locally while the designated destination is archived and routing unresolved; no delivery or fix claimed.

**Two-axis/architectural-region extension to the same SFB-002/SFB-004 acceptance cases — local only:** Preserve a source-supported architectural region separately from an exact physical material point, attachment, depth and metric calibration. A generic facade graphic can identify a component family without supplying an engineering node or distance. Extend the joint-box fixture to x/y simultaneously, retaining original observer-box intersections, empty local intersections, global separation conflicts and constructed witness membership. Uniform box widening is mathematical sensitivity, never an estimated actual error. Test labels must name operations actually performed: a constant difference array is not evidence that two source arrays underwent a shared transformation; retain the transformation inputs to test that claim. These are observed workflow needs, not newly inspected Sherlock defects. No case details, media, measurements, source names or private paths are proposed for transfer. Deduplicated local queue only; archived-destination routing and delivery remain unresolved.

## SFB-003 — Feedback intake and capability-specific readiness

**Observed need:** 2026-09-08. **Priority:** P2, investigation/development coordination. **State:** acknowledged; minimal project log verified, broader acceptance criteria not yet met.

**Requested improvement:** A lightweight project-owned intake for investigation feedback with stable IDs, duplicate linkage, impact, safe reproduction, acceptance tests, acknowledgment, and fix-verification status. Readiness should distinguish schema availability, implemented command, tested synthetic behavior, validated domain method, and human/expert review prerequisite.

**Synthetic reproduction:** Submit the same capability request twice, acknowledge one canonical item, and mark an implementation reported but not independently retested.

**Acceptance:** No duplicate active work item; versioned status history; a reported fix remains unverified until its acceptance test is recorded; a generic stage label cannot imply that a specialist measurement or inverse-analysis capability exists.

## Delivery ledger

**2026-09-08 second measurement supplement acknowledged:** Added SFB-002 lessons from synthetic template tracking: high correlation is not physical-point identity; retain full search surfaces and competing coordinates; record boundary/occlusion stopping rather than silent interpolation; distinguish deterministic scientific products from variable runtime logs. The payload contained no historical frames, real coordinates or case content. Acceptance is reconstruction of each selected/competing result plus known-translation and identity/occlusion limitation tests. The destination turn completed and direct inspection of its FEEDBACK.md confirmed the supplement; no implementation or fix verification is claimed.

**2026-10-03 runtime-log recurrence, local only, same SFB-002:** Two extraction runs can have identical sampled pixels and encoded timestamps while their final processing-throughput fields differ. This is already covered by the acknowledged deterministic-products versus runtime-logs requirement, not a new issue. Retain complete logs and explicit differing fields; keep material equality separate from whole-log inequality. A synthetic fixture should preserve that distinction while refusing changed frame timestamps, unexpected diagnostic lines or unexplained differences. Do not expand a generic warning allowlist to obtain a pass. The local audit retained this distinction; no inspected Sherlock defect, implementation fix, new delivery or acknowledgment is claimed. No actual media, case identifiers, private paths or raw logs are proposed for transfer; the existing archived-destination routing boundary remains.

## SFB-004 — Operation-scoped labels and dependent validation data

**Original-source search disposition extension, local only, SFB-004/SFB-005:** Extend the existing acquisition-state fixture with four distinct outcomes: a located packet not fetched pending approval; a standalone route rejected by the tool; an attachment name without a usable link in the inspected representation; and a paper located only through a bibliography. Acceptance: do not collapse these into unavailable, reviewed, withheld or historically absent; preserve exact search coverage, independent source-family limits and unused search allowance. A guessed sheet name used as a query must never become a verified member locator. This deduplicates observed source-review needs, not a new inspected Sherlock defect or fixed feature. Generic synthetic examples only; no case records, actual URLs, private paths or personal data proposed for transmission. Delivery remains pending the existing archived-destination routing decision.

**2026-09-13 source-erratum/applicability extension — local only, SFB-004/SFB-005:** Extend the existing version/dependence fixture with an erratum that swaps directional values and changes a plan attribution. Acceptance: preserve the original reading, update current attribution, and keep the author's assertion about historical inputs separate from actual input/run verification. A floor-specific modification must not propagate as either universal presence or universal absence. Distinguish source-label associations from a second export that verifies only property references; a nearby caption cannot replace the direct named-endpoint locator. This is an observed workflow need, not an inspected Sherlock defect or verified fix. Generic synthetic fixture only; no case values, sources, files or private paths proposed for transfer. Delivery remains pending the archived destination's unresolved routing; no transmission or acknowledgment.

**2026-09-12 missing-definition and conditional-field extension — local only, SFB-004/SFB-005:** Extend the existing typed-namespace fixture with a missing reference in region A and a same-original-ID definition in region B whose include transform changes the effective namespace. Add same-number component pairs that differ in their material reference. Acceptance: report both the unresolved reference and the supplied counterpart without silently substituting it or claiming blanket absence. Keep raw numeric cards and versioned field interpretations separate: an explicit point table can supersede a zero scalar field, and a dimension field's meaning can depend on a formulation flag. Model-specific mass allocation must not become measured physical density. Preserve the source mapping, manual-version/run gap and independently tested scope, including known parser omissions. This records an observed local workflow need, not an inspected Sherlock defect or verified fix. Only generic synthetic examples are proposed; no case values, files, source names or private paths. Delivery remains pending the archived destination's unresolved routing; no transmission or acknowledgment.

**2026-09-12 repeated-field trace extension — local only, SFB-004/SFB-005:** Extend the existing typed-model fixture with repeated coefficients at identifiers that belong to only one structural part, alongside shared-part identifiers with no repeats. Acceptance: do not infer a load/export-region identity from part membership; preserve row order without treating it as chronology or precedence; label analyst-defined sorting runs separately from source-defined blocks. Keep reported software version, acquired executable identity and authenticated run/input linkage as distinct states. A periodic coordinate pattern should remain descriptive until its generating rule is located. This is an observed investigation-workflow need, not a demonstrated Sherlock defect. Only a generic synthetic fixture is proposed; no real values, case names, source files or private paths are outbound. Pending locally under the existing archived-destination routing limit; no delivery or fix is claimed.

**Failure-replay extension to the typed-model fixture, local only:** A failed run receipt can pin a code hash while the corresponding source revision is no longer saved. Acceptance: retain the runnable revision or explicitly report replay unavailable; current synthetic reproduction of a failure class is not an exact rerun of that earlier revision. This observed local limitation is not a demonstrated Sherlock defect. Same pending routing and minimized-payload boundaries apply.

**2026-09-12 typed-model join supplement — local only, SFB-004/SFB-005:** A numeric input can use two rows for one element and repeat an identical assignment to a shared node. Synthetic acceptance: distinguish physical lines, typed records, unique identifiers and part-incidence counts; keep contradictory duplicates separate from exact repetitions; preserve required blank cards and type-specific identifier offsets. A named diagnostic must resolve through its referenced set and member graph, not through a coincidentally matching ID. Validate the active include/deletion state before labeling a supplied companion as applied, and do not turn input coefficients or model-authored labels into historical physical observations. Numeric-only inspection must allowlist keyword text as well as values; unknown text and failed-parser diagnostics must not leak source metadata. These are demonstrated local workflow needs, not inspected Sherlock defects or verified fixes. The proposed generic fixture includes no real model values, source names, case material, paths or attachments. Delivery remains pending while the designated task is archived and routing unresolved; no new transmission or acknowledgment is claimed.

**Observed need:** 2026-09-08. **Priority:** P2, comparison/validation integrity. **State:** acknowledged; no fix reported. This is a workflow-contract request, not a source-inspected claim that a particular Sherlock field is missing.

A project can use several methods while a clip shows only one unidentified operation. Project-level documentation must not silently label that clip's mechanism. Likewise, an image time inferred with a model assumption cannot serve as independent validation of that same assumption. Derivative copies must not inflate independent sample counts.

**Synthetic reproduction:** One project has operations A/B using different methods, three clips including one unresolved operation, and two timestamps: an independent clock and an interval inferred from model assumption X.

**Acceptance:** Clip/operation/project scopes remain explicit; unresolved method stays unknown; attribution and dependence links are retained; common-origin derivatives count once; assumption-X-derived labels cannot qualify as independent validation of X. Record a late correction without silently rewriting historical classifier inputs.

**Delivery:** Sent to the existing destination task on 2026-09-08 together with the SFB-002 supplement above. The message requested logging/triage only, not broad implementation or investigation-file access. Only generic synthetic examples were included. The destination turn completed; direct read of its FEEDBACK.md confirmed SFB-004 under the same ID with acknowledged status and the intended acceptance criteria. This is receipt/triage, not a software fix.

**2026-09-15 annotation-severity calibration extension — local only, SFB-004:**
Extend the already acknowledged caution/exclusion fixture, not a new duplicate
issue. A synthetic region has minor frame overlap, unknown glazing and adequate
displayed-appearance opportunity; another has dominant obstruction. Require
separate candidate identity, opportunity, incidental caution and reasoned
decisive exclusion. Switching among ordinary appearance classes must not change
membership with identical opportunity inputs. A passing opportunity paired with
`non_evaluable` must retain both inputs and an explicit consistency-review state,
not silently become a negative observation. Test threshold-touching intervals,
zero in-frame extent, and exclusion precedence while preserving unresolved
reasons. Text-scenario agreement is rule comprehension, not visual calibration
or accuracy. This is an observed local workflow need, not an inspected Sherlock
defect or verified product fix. No case examples, images, results, private paths
or source metadata are proposed for transmission. Pending locally under the
existing archived-destination routing boundary; nothing newly sent.

**2026-09-16 non-exclusive observation and lineage-key extension — local only,
SFB-004/SFB-005:** Extend the existing annotation/dependence fixture rather than
opening a duplicate issue. Synthetic smoke presence, local flame nondetection
and ambiguous brightness may coexist. Preserve separate axes, every locator
and the original reason: agreement on a coarse presence field must not erase
disagreement on location, target identity or shape. An uncertain smooth bright
edge must not silently become positive fire evidence. Separately, a raw credit
string, normalized source-family key and verified common-origin relationship
are different fields; mixed raw/normalized keys cannot be counted as distinct
independent sources. Test an explicitly linked video pair with inconsistent
credits and an approximate time inherited from a precisely timed neighbor:
keep the contradiction and original precision, not a fabricated combined
answer. These are observed local workflow needs, not inspected Sherlock defects
or verified fixes. Generic synthetic payload only; no case images, identifiers,
results, source names or private paths proposed for transfer. Delivery remains
pending the archived destination's routing decision; no new send or receipt.

## Earlier delivery history

**2026-09-10 media and candidate-record supplements — observed, local only:** Deduplicate under existing IDs; no new delivery, acknowledgement or fix claim. These are reproducible workflow lessons from local methods/source reading, not source-inspected Sherlock defects. Before any later send, review the minimized exact payload and chosen destination; do not include case names, actual footage, personal metadata, local paths, headers or linked investigation reports.

- **SFB-002, seek/timebase and stored/display geometry:** Synthetic reproduction: a tiny nonzero-start video has valid frames in requested absolute-second bins, but an exit-0 seeking command yields no images; an exact-duration boundary also wrongly rejects complete coverage. Test a full unseeked reference decode against the bounded selector and retain both failed candidates and corrected outcomes. Acceptance: every requested bin maps to an actual exact-rational PTS; empty-successful output fails; nonsquare sample aspect is separate from stored raster; RGB conversion never implies calibrated radiometry. This extends the existing media contract; the local correction is not a Sherlock fix.
- **SFB-002/SFB-004, compilation clocks and inherited exposure times:** Synthetic reproduction: a joined video lists rounded chapter offsets and historical start times, while a report's cited close-up appears at a different relative position; a film photo is timed using a separate digital exposure. Acceptance: retain shot coverage, source-declared clocks, actual decoder PTS, exact-versus-similar frame correspondence and missing edit/clock records separately. Do not invent a constant offset, continuous burn history or independent corroboration from a reused source family. Truncated displays count as unreviewed, not successful visual inspections.
- **SFB-005, partial acquisition versus current HTTP status:** Synthetic reproduction: HTTP 200 terminates with a timeout and partial bytes; a fresh no-clobber copy resumes with HTTP 206. Acceptance: preserve the failed original, verify numeric range, final size/hash and prefix identity before admitting the new file. Keep transport metadata local pending exact-payload review. A successful HTTP or process exit alone is not source acquisition, and an access denial is not historical absence. The Didik transport-state lesson is deduplicated here.
  **September28 recurrence, local only:** A declared timeout again left an HTTP200 partial; a separately preserved full retry met the expected byte count and passed later checks. Retain both attempt states and never treat the partial as an extra source. Extend the generic adapter fixture to accept a documented top-level authenticated file-reference object as well as any supported string form; do not misclassify an object as a missing download or print/store its temporary bearer URL. Test shape validation, empty inline bytes, exact source/size joins and secret-free receipts. These are observed workflow needs, not inspected Sherlock defects or verified fixes. No case data or local paths proposed for transfer; archived-destination routing remains unresolved, with no new delivery or acknowledgment.
  **October3 recurrence, local only:** A terminal timeout receipt reported elapsed time beyond the explicitly requested cap. Desired behavior: retain configured limit, reported elapsed time, terminal status and admitted/excluded state separately; a requested setting is not proof the cap was met. Synthetic extension: a mock HTTP200 partial ends with a timeout after its configured limit, followed by one permitted, separately preserved complete retry. Acceptance: flag the overrun without silently relaxing the rule, retain and exclude the partial, distinguish integrity checks from protocol compliance, and never restart a live process merely because an observation wait ended. Priority: evidence-integrity reporting. The cause remains unknown; this is an observed workflow requirement, not an inspected Sherlock defect or verified fix. Proposed feedback contains no real source IDs, media, case values or local paths. Existing archived-destination routing remains unresolved; no new delivery or acknowledgment.
- **SFB-004/SFB-005, received candidate versus authenticated origin:** Synthetic reproduction: a field inventory attributes items A/B to a facility; a receiving agency preserves those exact compound codes but leaves origin blank and lists them as unidentified. Acceptance: advance receipt without claiming accepted origin; distinguish report acknowledgement from a signed transfer and a physical-photo join, Trip Date from intake date, repeated tables from independent custody evidence, and a request-log locator from a response/outcome. Preserve the earlier unknown-receipt state as dated history and require attribution worksheets for the remaining question.

**2026-09-09 model-scope/version supplements — delivery failed, retained locally:** A new minimized note was submitted to the designated task, but the app returned that the task is archived. No receipt or acknowledgment is claimed. The user was asked whether to reopen that task or designate another. Do not silently unarchive or create a replacement task. This is a feedback-routing limit, not a blocker on the independent scientific work.

Pending SFB-004 supplement: preserve model domain, imposed versus predicted events, calibration dependencies and negative-outcome type. Synthetic reproduction is a failure-titled paper that computes heat transfer, prescribes an opening time from an image and has a non-spread alternative run. Acceptance: no inference of global mechanical collapse, independently predicted opening failure or a whole-system no-collapse control. Unknown actual loading, prior damage/preparation and recording provenance must stay explicit, not default to absent or matched.

Pending SFB-005 supplement: preserve conflicting version labels when one acquired PDF identifies itself as an author original and another repository labels an unacquired, same-named but different-sized file accepted. Acceptance: keep source-attached assertions, acquisition status and hashes; no assumed byte identity, final-edition peer-review status or extra independent corroboration. These are integration requirements, not source-inspected Sherlock bugs. The proposed payload includes only these generic synthetic examples and asks for logging/triage, not broad implementation or real-case access.

**2026-09-09 additional supplements — observed, not sent:** These extend existing issues rather than opening duplicate feature requests. The entries below are generic workflow requirements, not demonstrated defects in Sherlock's current implementation.

- **SFB-005, initiated versus acquired:** A public download action returned without a file path; the page subsequently displayed a download-in-progress heading, and the available content-export command was unsupported. Impact: mistaking UI progress for acquisition would allow unread evidence into a report. Synthetic reproduction: a generic repository page advertises a PDF and displays a download message, but the tool returns no usable bytes. Acceptance: retain separate located, initiated, acquired, parsed and reviewed states; require an actual artifact and integrity/format checks for acquired status; preserve the failure without claiming the source is absent, unsafe or deliberately withheld.
- **SFB-004, item provenance versus collection labels:** A report describes sorting material in a named area while expressly retaining mixed origins; a separate specimen report gives tentative origin and unresolved event timing. Impact: joining these by their location label could invent custody or historical causation. Synthetic reproduction: mixed items from facilities A/B enter sorting zone A, while an unrelated specimen X is tentatively attributed to A and laboratory testing identifies damage without dating it. Acceptance: storage/sorting location, asserted origin, exact member location, custody transfers, laboratory observation and historical timing remain distinct; an explicit source-backed link is required before joining the specimen to that sorting operation. Compatible laboratory chemistry must not become a demonstrated historical cause.
- **SFB-005, representation coverage and locator identity:** An HTML transcription omits a chart that is present in the source scan and differs in two date fields; another acquired PDF ends at an advertised spreadsheet's cover, without its item rows. Impact: an agent could call accessible material missing, merge distinct claims or mark an inventory complete merely because the container parses. Synthetic reproduction: a scanned report with a table and a replacement redaction sheet, an incomplete text mirror, and a companion attachment cover without the attachment. Acceptance: store source-specific physical-page, printed-page and section locators; record reviewed coverage and absent components; preserve conflicting transcriptions and explicit corrections; do not count alternate representations as independent corroboration or infer a missing attachment's contents from its title.

No source documents, case examples, names, actual measurements, confidential metadata or case-specific paths are part of these proposed outbound supplements. Before a later send, review the exact combined payload and user-selected destination under the privacy rule; request logging/triage only and record the actual delivery outcome.

**2026-09-09 model, inventory and bridge follow-up — observed, not sent:** Deduplicate these additions under the existing IDs. The proposed software examples remain generic; the linked local investigation reports are not outbound attachments.

- **SFB-004, model-transition and illustration provenance:** Synthetic reproduction: a static model retains load successfully, a revised model changes both geometry and thermal loading, and a proposed seconds-scale cascade is illustrated with annotated video stills. A construction photograph also carries a drawn rotation tangent. Acceptance: preserve the stable response; distinguish prescribed damage from calculated failure, static instability from dynamic contact/impact, and an illustrative annotation from an observed measurement. Do not label the changed cases a one-variable ablation or count the same interpretation as independent validation. Retain conflicting source labels pending native outputs. This is an observed research-workflow need, not a demonstrated Sherlock implementation defect.
- **SFB-005, acquired-edition closure and item-level joins:** Synthetic reproduction: an early mirror ends at an inventory cover, while a later official copy includes all advertised rows; one numbered item contains two attached components, and the cover lists only an aggregate shipment total. Acceptance: close the specific acquisition gap without erasing its history; preserve component/item namespaces and row boundaries; do not assign aggregate totals to rows or infer an item-to-specimen/receipt join. Alternate representations remain one source family. OCR and locator titles are not substitutes for row inspection or acquisition.
- **SFB-003/SFB-005, schema readiness versus verified translation:** The [isolated bridge-schema checks](sherlock-integration/faraday-schema-verification.md) now demonstrate acceptance of unverified locators/hashes/endpoint IDs, default date-format non-enforcement, and rejection of a question reference kind. Synthetic acceptance tests should distinguish schema availability, expected schema behavior, a verified translation adapter, a two-engine workflow and a validated scientific method. A future adapter needs byte/hash and exact endpoint/version verification plus explicit direction/role and reference-kind policy. An offline runner should declare dependencies and report unavailable validators, schema rejections and harness failures separately, without engine imports or workspace/provider access. These observed schema limits do not establish defects in an adapter that was not located; the local harness's generic OS-read restriction was its own issue, not a Faraday defect.

State: **local only; no new delivery, acknowledgment or fix claimed**. All 13 final schema expectations passed, including expected acceptance of deliberately unverified inputs; this is not 13 successful authentication checks or scientific tests. The existing archived destination still needs the user's routing decision. Before sending, minimize the exact payload again; omit these local report links, source bytes, case details and environment metadata.

**2026-09-08 byte-layer and annotation-calibration supplements acknowledged:** Sent generic synthetic additions under SFB-002 (container/stored ciphertext/decrypted encoded image/decoded-pixel layers; page placement and reviewed figure association instead of object enumeration order) and SFB-004 (localized positives outside incomplete-opening denominators; undefined empty denominators; calibrating caution versus decisive exclusion; shared geometry is not independent geometry validation). No case names, images, measurements, source URLs, private paths or confidential material were included. Destination turn `01a0836f-d2f1-7073-b0b2-03c860906b2d` completed; direct read of its FEEDBACK.md confirmed the additions under the existing IDs. These are acknowledged integration requirements observed in a separate prototype, not source-inspected Sherlock defects or verified fixes. The live investigation preserves the original reviewer field-usage difference rather than relabeling it into consensus.

**2026-09-08 timing-API, decode-warning and candidate-coverage supplement acknowledged:** Sent synthetic examples under SFB-002 distinguishing stretched engine-time and uniform mean-duration APIs with identical endpoints, serializer units versus runtime API units, corrupt-frame warnings despite exit0, per-source acceptance, diagnostic byte integrity versus semantic repeatability, and false/many-to-one nearest matches in countdown/static/repeated imagery. No historical media, case-specific results, original paths, source URLs, confidential records or personal metadata were included. Destination turn `01a0824d-d643-7040-96bc-bdd511c61547` completed; direct inspection of its FEEDBACK.md confirmed all three additions under SFB-002. This is logging/triage acknowledgment only; no implementation, fix verification or new real-case access was authorized.

**2026-09-08 package-resolution and project-timing additions acknowledged:** SFB-005 below and an SFB-002 supplement were sent using synthetic examples only. The outgoing note excluded case names, source URLs, actual numerical results, original archive member names, author-machine paths, contact details, protected records and litigation strategy. Destination remained the user-designated Sherlock task. Turn `01a0822c-714f-79f2-bb05-fb89f89d4c09` completed; direct read of its FEEDBACK.md confirmed SFB-005 with acknowledged status and the SFB-002 supplement. This verifies receipt/triage, not a software fix or a demonstrated software defect.

**2026-09-08 cadence and event-time supplements acknowledged:** Sent minimized additions under SFB-002 (distinguish pixel identity, approximate image similarity, original exposure identity and acquisition cadence; no automatic retiming/deletion) and SFB-004 (retain conflicting source event-time assertions, their time bases and alignment/calibration dependencies). The synthetic examples used generic noisy/static test images and unrelated placeholder event times. No historical names, images, real measurements, private metadata or case documents were sent. The destination turn `01a08200-4031-7ce3-9ff6-369b52114daf` completed; direct inspection of its FEEDBACK.md confirmed both supplements under their existing acknowledged IDs. This is receipt of a contract request, not a claim of an existing verified Sherlock bug, a software fix, or authorization for implementation.

On 2026-09-08, SFB-001 through SFB-003 were sent together to the destination task above. The app confirmed delivery to that task. The payload contained the minimized technical observations, synthetic acceptance tests, and a request to document/triage rather than implement. It did not include the investigation charter, case documents, private correspondence, or broader task history.

The destination turn completed, and direct inspection of `/Users/admin/dev/sherlock/FEEDBACK.md` confirmed all three entries under the same IDs with **acknowledged** status. Sherlock confirmed SFB-001's unsupported full-charter path and SFB-002's missing validated media-method contract. SFB-003 now has a minimal project-owned log; command-managed lifecycle, duplicate handling, readiness distinctions, and fix-verification gates remain unimplemented/unverified. No software fix is claimed. This is a delivery/triage result, not a causal or case finding.

## SFB-005 — Resolved-package completeness and run identity

**2026-10-04 shared-lane and dependency-map extension — local only:** A passing
synthetic suite did not test omission of a required source entry from one
chunk's input map. Acceptance must check every chunk against a fresh mandatory
source/reference map; checking only a conflict-free union is insufficient.
Separate negative controls now exercise missing source/reference, cross-pass
conflicts and changed bytes at final recheck. A second local failure arose when
parallel synthetic suites shared a byte-counted directory and one removed its
temporary fixture during the other's filesystem walk. Preserve the incomplete
run, serialize runs sharing that accounting boundary, and rerun unchanged
checks; do not convert missing files into zero-byte successes. These are local
workflow lessons, not verified Sherlock defects or product fixes. Generic
fixture only; no case payload or private paths. Archived routing unchanged:
queued locally, not sent, acknowledged or fixed in Sherlock.

**2026-10-03 process-supervision extension — local only, same fixture:** Test a
successful parent with a still-running child, a termination-ignoring descendant,
an immediate stop, interruption and a failed final filesystem inspection.
Acceptance requires bounded cleanup of the owned process group, the original
failure reason, honest unknown measurements, persistent failure receipts and
actual child-termination checks. A successful leader exit alone is insufficient;
requested limits, observed duration and possible polling overshoot stay separate.
Local preflight failures and their subsequent passing checks were retained;
their operating-system cause is unproven. This is a workflow requirement based
on local code review, not a demonstrated Sherlock defect or product fix. Generic
synthetic fixture only; archived routing unchanged, not sent or acknowledged.

**Observed integration need:** 2026-09-08. **Priority:** P2. **State:** acknowledged; no fix reported. This is an investigation workflow requirement, not a source-inspected defect in Sherlock.

A successful HTTP response and valid ZIP may deliver only a README pointing elsewhere. Different landing pages may converge on the same package. A repaired earlier-version archive, a final report and a public solver engine do not establish a complete final-version executable case. A published postprocessor warning about previous-run outputs also motivates an explicit input/run/output identity contract; no contaminated scientific run was demonstrated here.

**Synthetic reproduction:** A final-version landing page yields a small valid ZIP with only a README; the README redirects to an earlier-version package also linked by another site. Supply a generic engine repository without the case input manifest, and a results directory from a prior synthetic run.

**Acceptance:** Distinguish link located, response obtained, wrapper acquired, target package acquired, version crosswalk verified, dependencies complete, execution reproduced and physical validation. Deduplicate convergent origins; retain exact artifact hashes and unresolved version relationships. Engine availability must not imply case completeness. Postprocessing must bind outputs to a specific input/run manifest, flag stale or unmatched outputs without deleting preserved records, and retain failures as separate results.

**Related SFB-002 supplement:** Saved project frame duration/step settings are distinct from encoded presentation timestamps and original acquisition timing. Retain nested archive/project/media lineage, literal settings and verified software semantics separately. Use a synthetic archive with safe relative media and a duplicate Windows-absolute entry; never use the latter as an extraction destination or repeat personal path components in diagnostics. This adds scope to the existing measurement contract, not a request to launch untrusted projects.

October 8 nullable-clock recurrence, same SFB-002/SFB-005 fixture: a local
native-media parser accepted absent stored PTS and relabeled decoder
best-effort timestamps as PTS; it also failed on a final record without either
field. Preserve nullable stored and decoder-estimated clocks separately,
including genuine zero values. An ordinal-only source screen may continue
under its own declared method, but must not clear a failed timing test or
fill absent values from nominal frame rate. A nine-frame synthetic fixture
with missing first/final fields now passes the local separation controls;
present disagreement, nonmonotonic known values and fewer-than-eight inputs
are rejected for the fixed eight-frame screen. This is a reproduced local
adapter issue/repair, not an inspected Sherlock defect or product fix.
Failure-output preservation remains covered by the existing diagnostic
fixture; partial stdout on timeout and oversized-output receipt handling
remain limitations of this local adapter. Generic fixture only; no source
names, actual frame counts, images or paths sent. Queued locally under the
unchanged archived-destination boundary, not delivered or acknowledged.

October 8 timestamp-provenance clarification, same nullable-clock fixture:
the earlier shorthand “stored PTS” must not imply literal container or camera
storage merely because a decoder reports a value. A normal processing path
may derive a present timestamp; an explicit generation path can fill absent
values without authenticating exposure timing. Extend the synthetic fixture
with distinct packet DTS, frame PTS, best-effort and generated-output fields,
picture reordering and ordinal gaps. Acceptance: preserve raw nulls and field
provenance; generated regularity cannot clear an original-clock gate; compare
timestamp differences against ordinal gaps, not just successive known values.
Source-slice hash equality and unique positional joins must not become proof
of one packet per exposure. This records a demonstrated local workflow need,
not an inspected Sherlock defect or a verified product fix. Generic example
only; no case values, media, paths or source names transmitted. Still queued
locally under the same archived-destination routing decision.

Related checker controls, under the existing completeness/exact-arithmetic
fixture: a producer-selected empty comparison-field list must not make a
changed baseline pass; independently enforce the full declared field set.
Two individually safe integers can yield an unsafe subtraction or product;
reject unsafe intermediates or use exact integer arithmetic. Both failures
were reproduced synthetically and repaired in the local checker before its
historical use. A passing check must list unchecked summary flags/status
labels rather than silently certify the whole report. No product-wide fix
or delivery is claimed.


## 2026-09-08 — SFB-001 local adoption verification

The original SFB-001 source inspection and earlier no-fix statements are preserved as historical observations of the prior CLI. The project-owned [local integration](sherlock-integration/README.md) now pins Sherlock **0.1.2** and uses its supported full-charter path. Local initialization preserves the complete original `CHARTER.md` text exactly in structured scope, retains explicit constraint/review fields, and creates Q01–Q10 as ten open questions with their material-change conditions. This clears the local full-charter creation blocker; it does not amend the scientific charter or imply an accepted case finding.

Only charter and question state is initialized. Evidence files and research reports are not imported; no accepted findings, publication or canonical promotion are created. The local workbench acts as an agent and disables review acceptance, report generation and automatic report downloads. The integration guide identifies the pinned runtime and verification commands; original charter bytes, WP0 results and existing scientific outputs remain preserved.

SFB-002 through SFB-005 and their domain-method requirements are **not resolved by this adoption**. Validated media measurement, calibration and uncertain event-time treatment, comparison/annotation contracts, resolved-package completeness and run identity still require their specific acceptance evidence. The command-based feedback lifecycle requested under SFB-003 is also not established by a local runtime launcher. Software initialization is distinct from method validation, human/expert review and scientific completion. No new feedback transmission or external disclosure accompanies this local entry.

## 2026-09-09 — Sherlock–Faraday bridge capability lead

**2026-09-10 source-chain supplement — local only, SFB-004/SFB-005:** A document dated after an event attributes a counterfactual opinion to an interviewee; a transcript has a segment-start clock but no per-utterance timestamps; a response encloses an index containing other request identifiers. Preserve assertion time, described event time, utterance position, document role and parent/enclosure identifiers separately. Synthetic acceptance: reject automatic conversion of later opinion into prior forecast, header time into every utterance's time, or an index-production response into disposition of a listed request. Keep challenged joins and reviewer narrowing auditable. This is an observed workflow need, not a demonstrated Sherlock defect or a verified fix. No case details, documents or raw headers sent; the designated destination remains archived pending routing.

The user reports that Sherlock should now have a bridge to Faraday and asks that it be considered for pursuing or auditing scientific rigor in this investigation. Record this as a **capability lead pending verification**, not a finding that the pinned project runtime supports it or that a scientific review has occurred. No callable Sherlock/Faraday tool was present in the current tool inventory at this check.

The [local capability review](sherlock-integration/faraday-bridge-review.md) now verifies a documented external-engine/Faraday interoperability contract. The actual project-owned operational bridge and its tests remain unverified; no bridge was invoked. The note defines the first synthetic acceptance test and preserves the pinned-runtime and data-flow boundaries.

**Subsequent verification:** the [Faraday-side interface audit](sherlock-integration/faraday-interface-audit.md) located a format-1 receipt schema, example/test source and launcher skeleton. An isolated schema-only continuation completed **13 expected outcomes, zero failed/skipped, exit 0**, with source pins unchanged and no engine or case transfer. Earlier dependency and harness failures are retained in the [verification receipt](sherlock-integration/faraday-schema-verification.md). The proposed two-engine scientific fixture was not run; an operational translation adapter and domain-review capability remain unverified. These later checks supersede only the earlier lack of interface/schema-test inspection, not the operational or scientific limits.

Before relying on the bridge, inspect its supported interface, version, actual implementation/tests, destination and data flow; compare the development checkout with the separately pinned local runtime. Do not silently upgrade the runtime, invoke a bridge, import/export case data or supply human-review attestations. Potential uses include auditing claim-to-source links, assumptions, disconfirming tests, uncertainty, calibration versus validation, and reproducibility. Each use needs a declared input, audit question, procedure/version and acceptance criteria.

First validate an appropriate minimal synthetic workflow only after its execution and disclosure boundaries are understood. Any real material transfer must satisfy the repository's exact-payload/destination privacy rule. Preserve Faraday's suggestions as review outputs with provenance and unresolved objections; they are not new historical evidence, independent experiments, professional certification, accepted findings or authority to promote records. Any demonstrated integration friction should extend the existing SFB issues where applicable. This note itself initiates no bridge call or transmission.
