require 'json'
require 'digest'

out=ARGV.fetch(0)
findings=JSON.parse(File.read(ARGV.fetch(1)))
rows=JSON.parse(File.read(File.join(out,'source-crosswalk.json')))
manifest=JSON.parse(File.read(File.join(out,'manifest.json')))
items=JSON.parse(File.read(File.join(out,'sent-item-crosswalk.json')))
source=manifest.fetch('source_path')
payload=manifest.fetch('outbound_path')
dest=manifest.fetch('destination_log')
by_start=rows.to_h { |r| [r.fetch('source_start'),r] }
sent_lines=File.readlines(payload)
def put_new(path,body)
  File.open(path,File::WRONLY|File::CREAT|File::EXCL,0600) { |f| f.write(body) }
end
raise 'Finding roster mismatch' unless findings.map { |f| f.fetch('id') }==(1..24).map { |i| format('G%02d',i) }
findings.each do |f|
  f['source_starts'].each { |s| raise 'Finding without retained original' unless by_start.fetch(s).fetch('supplement_id') }
  f['items'].each { |id| raise 'Invalid digest item' unless items.any? { |i| i['id']==id } }
end

report=<<~MD
  # Detailed feedback comparison — selected confirmed gaps

  Local, unsent technical review, October 9, 2026. This is not a product-defect or scientific-finding report.

  These 24 comparisons distinguish a specific detail absent from the sent digest, partially preserved detail, and a detail explicitly preserved in the digest whose recipient-log pointer remains broad. They are **not an exhaustive count of omitted atomic requirements**. The accompanying annex preserves every retained technical source bundle, including details not individually discussed here, so this selected review is not used as a replacement specification.

  “Missing” below means missing or insufficiently explicit in the identified text at the pinned snapshot—not missing from the entire conversation history or current implementation. No product implementation audit was performed. Broad headings do not establish a detailed test was recorded; equally, a concise log does not prove the full received message was lost.

  Every test below is a **generic synthetic acceptance example**, not a new test result. Source notes describing earlier local tests remain attributed reports. No such fixture was run against Sherlock in this audit.

MD
findings.each do |f|
  refs=f.fetch('source_starts').map do |s|
    r=by_start.fetch(s)
    "[original lines #{r['source_start']}–#{r['source_end']}](#{source}:#{s}) → #{r['supplement_id']}"
  end
  sent=f.fetch('items').map do |id|
    line=sent_lines.index { |l| l.start_with?(format('%02d. ',id)) }+1
    "[item #{format('%02d',id)}](#{payload}:#{line})"
  end
  report << "## #{f['id']} — #{f['title']}\n\n"
  report << "Classification: `#{f['classification']}`.\n\n#{refs.join('; ')}. Sent comparison: #{sent.join(', ')}.\n\n"
  report << "Preserved: #{f['retained']}\n\nDetail requiring explicit treatment: #{f['missing']}\n\nAcceptance: #{f['test']}\n\n"
end

cover=<<~TEXT
  DRAFT SFB-SUPPLEMENT-2026-10-09 — intake cover, NOT SENT

  Intended recipient: the existing Sherlock task “Define Phase 0 invariants”.
  Purpose: preserve the material technical detail behind the received 27-item
  SFB-BATCH-2026-10-09. Logging and triage only; no product implementation,
  publication, investigation-file access, source acquisition or real-data bridge.

  The earlier batch's delivery and acknowledgment remain valid. They did not
  establish every original qualification, reproduction step or acceptance test
  was retained. The saved recipient log uses “already covered” for the same core
  requirement, which is weaker than exact detail preservation. This supplement
  does not assert that the original received message was lost.

  The proposed accompanying technical-annex.txt has 225 stable FBR entries.
  It retains whole original technical bundles rather than silently condensing
  their tests again. A bundle can contain multiple requirements; 225 is NOT a
  count of independent bugs or distinct atomic requirements. All example tests
  are synthetic; reports of earlier local tests are attributed historical notes,
  not newly verified engine behavior. Historical local-only/routing phrases do
  not describe the supplement's eventual delivery state.

  Account for every FBR entry under existing SFB-002 through SFB-005. Keep the
  detailed text available and link any deduplicated work item to all applicable
  entries and preserved tests. Do not replace this annex with only topic labels.
  For “already covered”, identify the exact requirement, qualifier and test
  locations; otherwise acknowledge as a detail extension or record a concrete
  question. Preserve resolved SFB-001 without reopening its historical defect.

  Acknowledgment must identify the received payload hash, covered FBR IDs,
  omissions or qualifications, and saved local record location. Acknowledgment
  is separate from implementation, verified fixes, activation, method validation
  and human acceptance. No cross-thread reply is authorized or needed.

  Only this cover and the reviewed technical annex are proposed for transmission.
  The source crosswalk, receipt links, investigation paths, local audit reports
  and original source log remain in the originating repository.

  Proposed annex SHA-256: #{manifest.fetch('annex_sha256')}
  Proposed annex bytes: #{manifest.fetch('annex_bytes')}
TEXT

trace=rows.select { |r| r['supplement_id'] }.map do |r|
  {supplement_id:r['supplement_id'],source:{path:source,sha256:manifest['source_sha256'],first_line:r['source_start'],last_line:r['source_end'],pre_delivery_first_line:r['pre_delivery_start'],bundle_sha256:r['source_block_sha256']},earlier_sent:{path:payload,sha256:manifest['outbound_sha256'],topic_items:r['digest_items'],semantic_detail_equivalence:'not_certified'},earlier_acknowledgments:r['digest_items'].map { |id| item=items.find { |i| i['id']==id }; {item:id,log_path:dest,line:item['ack_line'],disposition:item['disposition'],scope:'batch_item_not_every_original_clause'} },proposed_supplement:{bundle_sha256:r['supplement_sha256'],state:'draft_not_sent',delivery_receipt:nil,detail_acknowledgment:nil}}
end

readme=<<~MD
  # Sherlock feedback preservation audit — October 9, 2026

  **Outcome:** the received 27-item batch does not itself establish complete preservation of the original requirements. Concrete qualifications and tests are absent or only broadly represented. A local technical-detail supplement is prepared; **nothing from this audit has been sent, committed or pushed**.

  ## Scope and acceptance

  Compare the pinned original feedback, exact transmitted batch and saved acknowledgment; preserve technical detail; keep source-to-message-to-acknowledgment links locally. No investigation source acquisition, new scientific analysis, legal drafting, product implementation or source-record rewriting is authorized here.

  Acceptance for preservation is complete accounting of the source blocks and exact retention of selected technical bundles, with every locator/receipt-identifier substitution logged. This is **not** a claim that topic matching proves clause-by-clause semantic equivalence to the older digest. Acceptance for delivery requires separate authorization of the exact new payload, an actual send receipt and verification of a detail-level recipient acknowledgment; those steps remain pending.

  ## Results

  - The current feedback source has 2,468 lines and reconstructs the exact 2,455-line pre-delivery source whose hash appears in the prior receipt.
  - All 272 nonblank source blocks are accounted for: 225 technical bundles retained; 47 administrative/heading/status/resolved-item blocks explicitly listed for non-retransmission.
  - All 27 sent item IDs and all 27 corresponding recipient-log item IDs are present exactly once. This verifies item-level receipt, not preservation of every source clause.
  - [Detailed comparison](requirement-gap-review.md) records 24 selected comparisons, including counterexamples to overclaiming a gap: actual resampling-kernel exclusion is already explicit in sent item 16, and common-support/no-refitting is already explicit there too.
  - The [technical annex](technical-annex.txt) retains complete technical bundles with stable FBR identifiers. It is approximately 217 kB because tests and qualifications have not been condensed again. It is not the whole investigation record; nevertheless, size and safe content require exact-payload review before sending.

  The strongest limitation on these results is that **225 is a bundle count, not a count of distinct atomic requirements**, and the 24 detailed comparisons are not an exhaustive clause-level omission census. The complete selected source text is retained precisely so this limitation does not silently delete remaining requirements. The annex is a preservation solution, not certification of a finished deduplicated implementation specification.

  ## Review and delivery boundary

  Proposed recipient: **Define Phase 0 invariants**, the existing Sherlock task. Proposed payload is exactly [supplement-cover.txt](supplement-cover.txt) plus [technical-annex.txt](technical-annex.txt). The cover binds the annex hash and requests intake/triage only. Review excludes investigation documents, case links, source identifiers, private paths, personal contact data and original receipt IDs from the proposed payload; a textual screen supplements but does not substitute for human content review.

  Local-only: source crosswalks, detailed comparison, source hashes/locators, prior delivery records and acknowledgment links. Do not transmit the whole directory. Do not append these drafts to the parent feedback log as though delivered. After authorized delivery, save exact payload/receipt, check the recipient's preserved detailed text, and append the new receipt and detail acknowledgment to the local traceability record. Reopening a chat is not delivery; a receipt is not a fix.

  ## Files and authority

  - [source-crosswalk.csv](source-crosswalk.csv) / [JSON](source-crosswalk.json): every source block, inclusion/exclusion reason, original and pre-delivery locators, source/annex hashes and topic links. JSON contains local paths and is not an outbound attachment.
  - [sent-item-crosswalk.json](sent-item-crosswalk.json): exact sent item text, hash and recipient-log disposition/pointer. Scope remains item-level.
  - [traceability.json](traceability.json): original bundle → older sent items → older acknowledgment → draft supplement, with new delivery/acknowledgment fields explicitly null.
  - [manifest.json](manifest.json): pinned inputs, source reconstruction and preservation scope.
  - [verification.json](verification.json): actually executed preservation checks and negative controls. These are audit checks, not Sherlock feature tests.
  - [findings.json](findings.json): structured form of the 24 detailed comparisons.

  The original source and destination log remain authoritative for what was written and acknowledged. This audit does not change their history or any case pleading. Resolved SFB-001 material remains in the original source and destination's existing SFB-001 section; it is not reopened or certified anew.

  ## Method and limitations

  The source and sent batch were read; the pre-delivery version was reconstructed from the documented routing/delivery additions and verified against its earlier receipt hash. Source paragraphs were explicitly classified rather than deleted by keyword. Technical text was retained verbatim except five logged changes: one case-source label generalized, one link destination removed while retaining its label, and three historical receipt UUIDs replaced. Those redactions are not implementation requirements. Historical routing boilerplate remains clearly marked as historical within retained bundles.

  The builder uses standard Ruby libraries only and does not execute source notes, import Sherlock or contact a provider. A separate verifier compares generated artifacts back to pinned inputs and exercises in-memory missing-row, altered-text, duplicate-ID and annex-tampering controls. Deterministic rerun equality is checked for generated preservation files. Exact commands and observed results are in verification.json.

  The evidence-falsification-auditor and source-of-truth-guardian skills shaped the distinction between receipt, content retention, semantic equivalence and verified implementation. repo-orchestrator kept this bounded work separate from the active investigation. The write-page guidance was used for readable local documentation in the established repository, with no cloud Page or disclosure.
MD

if ARGV[2]=='--publication'
  report=report.rstrip+"\n"
  readme=readme.sub("## Scope and acceptance", "## Subsequent repository publication\n\nThe user subsequently authorized documentation, commit and push to the private and public repositories. [PUBLICATION.md](PUBLICATION.md) controls that later publication status; the original preparation statements above and frozen receipts below remain historical. Repository publication is not a new message or acknowledgment by the Sherlock task. The selected public addendum does not include private source paths or receipt records.\n\n## Scope and acceptance")
  readme=readme.sub('**nothing from this audit has been sent, committed or pushed**','**at initial preparation, nothing from this audit had been sent, committed or pushed**')
end
put_new(File.join(out,'requirement-gap-review.md'),report)
put_new(File.join(out,'supplement-cover.txt'),cover)
put_new(File.join(out,'traceability.json'),JSON.pretty_generate(trace)+"\n")
put_new(File.join(out,'findings.json'),JSON.pretty_generate(findings)+"\n")
put_new(File.join(out,'README.md'),readme)
puts JSON.generate({created:5,findings:findings.length,traceability_rows:trace.length,state:'not_sent'})
