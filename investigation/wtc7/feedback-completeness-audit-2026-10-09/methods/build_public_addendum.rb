require 'json'
require 'digest'

audit,record_path,digest_path,out=ARGV
raise 'Pass audit directory, public record, exact digest, empty output directory' unless out && Dir.exist?(out) && Dir.children(out).empty?
source=JSON.parse(File.read(File.join(audit,'manifest.json')))
crosswalk=JSON.parse(File.read(File.join(audit,'source-crosswalk.json')))
findings=JSON.parse(File.read(File.join(audit,'findings.json')))
record=JSON.parse(File.read(record_path))
digest=File.read(digest_path)
raise 'Source identity mismatch' unless record.fetch('source').fetch('sha256')==source.fetch('source_sha256')
raise 'Digest mismatch' unless Digest::SHA256.hexdigest(digest)==source.fetch('outbound_sha256')
start=digest.index(/^01\. /)
finish=digest.index("\nPlease record receipt",start)
raise 'Missing digest boundaries' unless start && finish
excerpt=digest[start...finish].rstrip+"\n"
raise 'Digest roster mismatch' unless excerpt.scan(/^(\d{2})\. /).flatten.map(&:to_i)==(1..27).to_a
units=record.fetch('units')
findings.each do |f|
  spans=f.fetch('source_starts').map { |s| crosswalk.find { |r| r['source_start']==s } }
  raise 'Missing original span' if spans.any?(&:nil?)
  f['public_technical_units']=units.select { |u| spans.any? { |s| u['start']<=s['source_end'] && u['end']>=s['source_start'] } }.map { |u| u['id'] }
  raise 'Missing public technical-unit link' if f['public_technical_units'].empty?
  f['public_unit_line_numbers']=f['public_technical_units'].to_h { |id| [id,File.readlines(record_path).index { |line| line.include?("\"id\": \"#{id}\"") }+1] }
end
counts=findings.group_by { |f| f['classification'] }.transform_values(&:length)
raise 'Unexpected classification counts' unless counts=={'partial'=>13,'specific_detail_absent'=>10,'preserved_in_digest_not_detailed_in_recipient_pointer'=>1}
review=<<~MD
  # Detailed digest coverage comparisons

  These 24 selected comparisons concern the earlier 27-item digest, **not omissions from the later public technical record**. The technical-unit references link to the separately published detailed requirements; source line numbers are coordinates in the frozen feedback snapshot, not private paths. “Absent” means the specified detail is absent from the digest, not from all conversations or product code. No new product acceptance tests were run.

  Each acceptance example below is synthetic. The earlier digest is reproduced in [DIGEST-ITEMS.txt](DIGEST-ITEMS.txt); detailed requirements remain in the [existing technical record](../feedback-technical-record-2026-10-09/README.md). These comparisons do not enumerate every omitted atomic requirement.

MD
findings.each do |f|
  review << "## #{f['id']} #{f['title']}\n\nClassification: `#{f['classification']}`. Digest items: #{f['items'].map { |i| format('%02d',i) }.join(', ')}. Public technical units: #{f['public_technical_units'].map { |id| "[#{id}](../feedback-technical-record-2026-10-09/record.json#L#{f['public_unit_line_numbers'][id]})" }.join(', ')}.\n\nPreserved in digest: #{f['retained']}\n\nDetail requiring explicit treatment: #{f['missing']}\n\nSynthetic acceptance example: #{f['test']}\n\n"
end
readme=<<~MD
  # Sherlock feedback digest coverage addendum

  Receipt of the earlier 27-item feedback digest established that all 27 items arrived, not that every original qualification and test survived condensation. This bounded audit identifies 10 specific missing details and 13 partially preserved requirements among 24 selected comparisons. One investigated detail—testing exclusion through actual resampling kernels—was already explicit in the sent digest. This is not an exhaustive omission count or a product defect assessment.

  Read [the comparisons](FINDINGS.md), [the 27 digest items](DIGEST-ITEMS.txt), and the [existing detailed technical record](../feedback-technical-record-2026-10-09/README.md). The detailed record remains the published requirements reference; this addendum does not replace it or claim it has the digest's omissions.

  ## Evidence and limits

  The reviewed feedback snapshot has SHA-256 `#{source['source_sha256']}`. The complete earlier sent message has SHA-256 `#{source['outbound_sha256']}`. The digest file here is only the exact numbered-item excerpt: administrative intake directions and the receipt request are omitted, and its separate hash is recorded in the manifest. It is not represented as the full transmitted message.

  The private preservation audit accounted for 272 nonblank source blocks, retaining 225 complete technical bundles and classifying 47 administrative, heading, status or resolved-item blocks for non-retransmission. These are paragraph-bundle counts, not distinct requirement counts. The existing public technical record uses a different, finer unit scheme; its unit counts are not in conflict with this paragraph census. This addendum does not certify a new exhaustive semantic review.

  Nineteen local preservation and negative-control checks passed after a Ruby-version compatibility repair. A separate regeneration produced ten byte-identical audit/report files. Those checks establish bounded retention and reproducibility, not semantic completeness, privacy clearance, product implementation or scientific validity. The private original and detailed receipts are not included here. Readers can examine the digest and public technical transcriptions; direct source comparison requires separately authorized access to the pinned original.

  A concise recipient log does not prove that the complete received message was lost. Its “already covered” disposition addressed core requirements rather than verifying every detailed test. The audit distinguishes that narrower scope from an actual original-to-digest omission.

  ## Publication boundary

  This addendum includes generic requirements, explicitly synthetic acceptance examples, original source line numbers, public technical-unit references and integrity hashes. It excludes the original feedback log, private source paths, task and message identifiers, receipt records, correspondence, case documents and media. Hashes do not contain plaintext source text but can permit candidate-text comparison; they are not a privacy guarantee.

  Repository publication is not a new acknowledgment by the designated Sherlock task, an implementation instruction, an independently verified fix, activation, or a scientific finding. The earlier acknowledgment retains its original scope. The previously published technical record at commit `e62491ba8cbfe7da9ad79a5194776fd4781036fd` is left unchanged.

  ## Reproduce the integrity checks

  Run `ruby verify_addendum.rb` from this directory. It checks exact manifest file hashes, the digest and finding rosters, classification counts, source identity and public-unit JSON line links. In-memory negative controls reject an altered payload and an omitted finding. These are documentation checks, not the proposed product acceptance tests. The manifest pins the existing public record used for the links.
MD
def save(out,name,text)
  File.open(File.join(out,name),File::WRONLY|File::CREAT|File::EXCL,0644) { |f| f.write(text) }
end
save(out,'README.md',readme)
save(out,'FINDINGS.md',review.rstrip+"\n")
save(out,'DIGEST-ITEMS.txt',excerpt)
save(out,'findings.json',JSON.pretty_generate(findings)+"\n")
metadata={schema:'sherlock-feedback-digest-coverage-addendum/v1',date:'2026-10-09',source_sha256:source['source_sha256'],complete_sent_message_sha256:source['outbound_sha256'],comparison_scope:'selected comparisons against earlier digest, not a new exhaustive review of the later technical record',counts:counts,public_record:{path:'../feedback-technical-record-2026-10-09/record.json',sha256:Digest::SHA256.file(record_path).hexdigest,existing_published_commit:'e62491ba8cbfe7da9ad79a5194776fd4781036fd'},private_receipts:'not included',product_tests_run:false,new_recipient_acknowledgment:false}
save(out,'metadata.json',JSON.pretty_generate(metadata)+"\n")
puts JSON.generate({files_created:5,findings:findings.length,digest_items:27,counts:counts})
