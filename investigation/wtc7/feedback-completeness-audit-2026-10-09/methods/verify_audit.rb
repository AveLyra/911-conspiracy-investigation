require 'json'
require 'digest'
require 'csv'

dir=ARGV.fetch(0)
m=JSON.parse(File.read(File.join(dir,'manifest.json')))
source=File.read(m.fetch('source_path'))
sent=File.read(m.fetch('outbound_path'))
dest=File.read(m.fetch('destination_log'))
rows=JSON.parse(File.read(File.join(dir,'source-crosswalk.json')))
annex=File.read(File.join(dir,'technical-annex.txt'))
trace=JSON.parse(File.read(File.join(dir,'traceability.json')))
findings=JSON.parse(File.read(File.join(dir,'findings.json')))
checks=[]
def check(name,checks)
  raise "FAIL: #{name}" unless yield
  checks << {name:name,result:'pass'}
end
def complete_roster?(rows,source)
  blocks=source.split(/\n[ \t]*\n/).reject { |s| s.strip.empty? }
  rows.length==blocks.length && rows.map { |r| r['source_start'] }.uniq.length==rows.length && rows.each_with_index.all? { |r,i| source.lines[(r['source_start']-1)..(r['source_end']-1)].join.strip==blocks[i].strip }
end
def reconstructed_body(raw)
  raw.gsub(/\[([^\]\n]+)\]\([^)\n]+\)/,'\1').gsub(/\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b/i,'[prior receipt identifier retained locally]').sub('The Didik transport-state lesson is deduplicated here.','This transport-state lesson is deduplicated here.')
end
def exact_retention?(rows,source)
  rows.select { |r| r['supplement_id'] }.all? do |r|
    raw=source.lines[(r['source_start']-1)..(r['source_end']-1)].join
    raw_hash=Digest::SHA256.hexdigest(raw)
    transformed=reconstructed_body(raw)
    raw_hash==r['source_block_sha256'] && transformed==r['text'] && Digest::SHA256.hexdigest(transformed)==r['supplement_sha256']
  end
end
def unique_ids?(rows)
  ids=rows.map { |r| r['supplement_id'] }.compact
  ids==(1..225).map { |i| format('FBR-%03d',i) }
end
check('pinned_source_and_earlier_payload_unchanged',checks) { Digest::SHA256.hexdigest(source)==m['source_sha256'] && Digest::SHA256.hexdigest(sent)==m['outbound_sha256'] }
check('pinned_recipient_log_unchanged',checks) { Digest::SHA256.hexdigest(dest)==m['destination_log_sha256'] }
check('all_272_source_blocks_accounted_for_in_order',checks) { rows.length==272 && complete_roster?(rows,source) }
check('all_225_technical_bundles_exactly_retained_after_declared_substitutions',checks) { exact_retention?(rows,source) && rows.count { |r| r['supplement_id'] }==225 }
check('all_47_exclusions_explicitly_classified',checks) { rows.count { |r| r['disposition']=='not_retransmitted' && r['reason'] && r['supplement_id'].nil? }==47 }
check('stable_supplement_ids_unique_contiguous',checks) { unique_ids?(rows) }
check('five_logged_substitutions_only',checks) { rows.sum { |r| r.fetch('redactions',[]).length }==5 }
check('complete_annex_hash_and_size',checks) { Digest::SHA256.hexdigest(annex)==m['annex_sha256'] && annex.bytesize==m['annex_bytes'] }
check('annex_contains_each_retained_bundle_exactly_once',checks) { rows.select { |r| r['supplement_id'] }.all? { |r| annex.scan(Regexp.new(Regexp.escape("#{r['supplement_id']} | Existing batch items "))).length==1 && annex.include?(r['text']) } }
csv=CSV.read(File.join(dir,'source-crosswalk.csv'),headers:true)
check('csv_register_same_roster_and_hashes_as_json',checks) { csv.length==272 && csv.zip(rows).all? { |a,b| a['source_start'].to_i==b['source_start'] && a['source_block_sha256']==b['source_block_sha256'] && a['supplement_id']==b['supplement_id'] } }
check('prior_27_item_and_ack_rosters_match',checks) { sent.scan(/^(\d{2})\. /).flatten.map(&:to_i)==(1..27).to_a && dest.scan(/\*\*Item (\d{2}) —/).flatten.map(&:to_i)==(1..27).to_a }
check('traceability_preserves_draft_null_receipts',checks) { trace.length==225 && trace.all? { |r| r.dig('proposed_supplement','state')=='draft_not_sent' && r.dig('proposed_supplement','delivery_receipt').nil? && r.dig('proposed_supplement','detail_acknowledgment').nil? } }
check('all_24_findings_link_to_retained_original_bundles_and_sent_items',checks) { findings.length==24 && findings.all? { |f| f['source_starts'].all? { |s| rows.any? { |r| r['source_start']==s && r['supplement_id'] } } && f['items'].all? { |i| (1..27).include?(i) } } }
proposed=annex+File.read(File.join(dir,'supplement-cover.txt'))
disclosure_pattern=%r{https?://|/Users/|/private/|protonmail|@|DOC-NIST|\bWTC\d*\b|\bNIST\b|\bRory\b|\bDahl\b|\bDidik\b|\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b}i
check('proposed_payload_has_no_screened_locators_names_contacts_or_uuid_receipts',checks) { !proposed.match?(disclosure_pattern) }
check('disclosure_screen_benign_word_and_sensitive_marker_controls',checks) { !'deterministic'.match?(disclosure_pattern) && 'https://synthetic.invalid/path'.match?(disclosure_pattern) && '/Users/synthetic/file'.match?(disclosure_pattern) }
mutated=Marshal.load(Marshal.dump(rows)); mutated.pop
check('negative_control_missing_source_block_rejected',checks) { !complete_roster?(mutated,source) }
mutated=Marshal.load(Marshal.dump(rows)); mutated.find { |r| r['supplement_id'] }['text'] << ' changed'
check('negative_control_changed_technical_text_rejected',checks) { !exact_retention?(mutated,source) }
mutated=Marshal.load(Marshal.dump(rows)); kept=mutated.select { |r| r['supplement_id'] }; kept[1]['supplement_id']=kept[0]['supplement_id']
check('negative_control_duplicate_supplement_id_rejected',checks) { !unique_ids?(mutated) }
check('negative_control_altered_annex_hash_rejected',checks) { Digest::SHA256.hexdigest(annex+' changed')!=m['annex_sha256'] }
receipt={status:'pass',checks:checks,checked_at_utc:Time.now.utc.strftime('%Y-%m-%dT%H:%M:%SZ'),runtime:RUBY_DESCRIPTION,prior_attempt:{status:'harness_failed_before_completion',error:'NoMethodError: Array#filter_map unavailable in installed Ruby',repair:'Use map followed by compact with unchanged roster predicate; no acceptance criterion changed.'},commands:["ruby -c build_register.rb","ruby build_register.rb <empty-output-directory>","ruby build_report.rb <output-directory> findings.json","ruby verify_audit.rb <output-directory>"],limits:['Mechanical retention and lineage checks do not prove exhaustive semantic equivalence or privacy clearance.','No proposed acceptance test was run against Sherlock.','No transmission, implementation, commit or push was performed.'],payloads:%w[supplement-cover.txt technical-annex.txt].map { |n| path=File.join(dir,n); {file:n,bytes:File.size(path),sha256:Digest::SHA256.file(path).hexdigest} }}
if ARGV[1]=='--save'
  File.open(File.join(dir,'verification.json'),File::WRONLY|File::CREAT|File::EXCL,0600) { |f| f.write(JSON.pretty_generate(receipt)+"\n") }
end
puts JSON.pretty_generate(receipt)
