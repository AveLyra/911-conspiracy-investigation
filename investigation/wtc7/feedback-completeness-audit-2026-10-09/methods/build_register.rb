require 'json'
require 'digest'
require 'csv'

# A bounded, non-executing source-to-draft transformation. No network or product imports.
SOURCE_ROOT = '/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation'.freeze
DEST_LOG = '/Users/admin/dev/sherlock/FEEDBACK.md'.freeze
SOURCE_PIN = 'e1c718bb928ba846deb0d527f69cda7ea00a8d888c2247a864b1d666b4204133'.freeze
BEFORE_PIN = 'b15c8252d1de66034bd6778ef6185c9a345d1f597f358e5e412085ed3cd39c78'.freeze
PAYLOAD_PIN = 'bd3f148bdfb1c5c4c55a33afbba0bedad7e3d3258c224754a12566925d61a740'.freeze
DEST_PIN = '7348db6041d047f204b6eec4d6e30fc0d800e6794e267fc9ad55672695ddc108'.freeze
RECEIPT_PIN = '7461fce2fad58b5e88ce097d0bdf9ea444869a6800962090fb7d26a7d1d56463'.freeze
ACK_PIN = 'fb7236a2ff74dde3e093bd6da7b7bbd18205a944d1c228fee86ab2f61dcb2a3f'.freeze

# These are exact paragraph-start decisions, not a keyword filter deleting unknown content.
# Every other nonblank paragraph is retained in the proposed technical annex.
EXCLUSIONS = {
  'administrative_or_delivery_history' => [1,3,5,7,9,12,14,19,430,452,479,2287,2324,2333,2339,2345,2347,2353,2359,2363,2365],
  'section_heading' => [1875,2249,2259,2265,2322,2367,2448,2456],
  'resolved_SFB001_preserve_do_not_reopen' => [1861,1863,1865,1867,1869,1871,1873,2450,2452],
  'capability_or_status_not_a_new_requirement' => [2141,2143,2251,2279,2395,2454,2460,2462,2464]
}.freeze

# Human topic crosswalk after complete source reading. It is NOT a claim that the
# digest preserves every conjunct, fixture or qualifier in the mapped bundle.
TOPICS = {
  22=>[1,4],37=>[5],52=>[5,6],68=>[10,23],80=>[10],89=>[12,13],102=>[12],112=>[6,12],123=>[12],135=>[10,19],149=>[5],157=>[6],166=>[6,10],174=>[10,11],181=>[6],191=>[12,13],200=>[10,12],211=>[13],223=>[12],234=>[12,21],249=>[24],260=>[24],272=>[13],281=>[13],292=>[13],308=>[24],317=>[13,24],330=>[6,12],343=>[12],353=>[12],367=>[23],379=>[23],391=>[21],401=>[21],411=>[21],436=>[10,11,24],460=>[26],462=>[1,17],485=>[3,22],500=>[1,3,21],512=>[2],523=>[2],531=>[3],542=>[2,3],554=>[2,3,8],564=>[2,3,22],572=>[3,19],582=>[3,22],590=>[20],605=>[19,20],619=>[19,20],628=>[19,22],637=>[19],647=>[19],660=>[19],669=>[4,5],680=>[5],687=>[5],697=>[4,10,24,26],714=>[26],725=>[4,25],735=>[8,23,25],751=>[25],761=>[25],774=>[10,18,20,24],793=>[20],805=>[2,4,5],822=>[2,8],835=>[2],847=>[2],860=>[2],873=>[2],879=>[2],891=>[19],899=>[19,20,21],913=>[20],924=>[19,20],937=>[24,26],955=>[18,19,20],973=>[5,18,23],985=>[22],995=>[4,8],1006=>[8],1015=>[19,22],1031=>[22],1044=>[18,20],1062=>[13,20],1076=>[7],1096=>[7],1108=>[8,10],1138=>[8],1152=>[27],1169=>[27],1175=>[27],1184=>[27],1198=>[10],1217=>[10,18],1231=>[8],1244=>[8],1252=>[8,27],1265=>[11],1283=>[11],1290=>[11],1304=>[11],1322=>[14,27],1344=>[7,8,27],1359=>[7],1365=>[5,6],1374=>[10,14],1391=>[1,14],1405=>[6,27],1430=>[1,4,7],1442=>[4],1449=>[1,3,4],1464=>[1,3],1476=>[4,8],1492=>[1,2,3],1507=>[2,3],1519=>[2,3],1531=>[2,3],1544=>[10,14,15],1560=>[1,3,4,8],1580=>[8,10,14],1598=>[12,14,21],1614=>[15,16,21],1635=>[16],1649=>[3,5],1665=>[18],1679=>[14,18,21],1693=>[19,24,26],1706=>[6,19,21,24],1719=>[5,6,23],1738=>[18],1754=>[5,6,8],1774=>[19,20,23],1793=>[4,19,22],1795=>[19,22],1797=>[3,21,22],1799=>[5,6,19],1801=>[18,19],1803=>[11,19,27],1815=>[12,22,23],1829=>[11,12],1843=>[3,12,14],1852=>[12,14],1877=>[17,23],1889=>[1,17,23],1905=>[8,15],1921=>[15,22],1933=>[15],1945=>[14,20,21],1959=>[2,23],1967=>[5,9],1979=>[9],1987=>[8,23],2000=>[8,9,23],2011=>[16],2024=>[16,19,21],2036=>[10,21],2042=>[10,14,21],2055=>[12,14,21],2068=>[14,18],2082=>[9,15,16,21],2102=>[16,23],2117=>[15,16,21],2126=>[16],2145=>[14,15,17,26],2147=>[14,15,17],2149=>[14,15,17],2151=>[8,15,23],2153=>[14,17],2155=>[17,23],2168=>[14,15,27],2170=>[12,14],2184=>[14],2194=>[10,12,14],2206=>[12,14],2217=>[15,27],2227=>[8,14,23],2229=>[14,16,18],2231=>[8,14,15],2233=>[14,16,21],2235=>[6,18,23],2237=>[12,14,18],2239=>[14,15,19,21],2241=>[14,16,21],2243=>[5,14,15],2245=>[8,12,14,18],2247=>[12,14,18,23],2253=>[26],2255=>[26],2257=>[26],2261=>[16,23],2263=>[8,23],2267=>[1,2],2269=>[10,19,22],2271=>[6,19],2273=>[6,15,19],2275=>[23],2277=>[4,5,6,19],2281=>[19,21,22],2283=>[19,21,22],2285=>[19,21,22],2289=>[12,18,21],2305=>[12,14,21],2326=>[7,14,15,22],2335=>[19,20],2337=>[1,3,19,21],2341=>[1,3,19,22],2349=>[3,19,20,25],2355=>[12,21,27],2357=>[8,15,16],2361=>[14,15],2369=>[6,9],2383=>[9],2397=>[1,6,19,23],2399=>[1,6,23],2401=>[1,6,23],2403=>[5,15],2405=>[8,15],2422=>[15],2437=>[18],2458=>[22],2466=>[25,26],2468=>[25,26]
}.freeze

def checked(path,pin)
  data=File.binread(path)
  raise "Input pin mismatch: #{File.basename(path)}" unless Digest::SHA256.hexdigest(data)==pin
  data.force_encoding('UTF-8')
end

def persist(path,data)
  File.open(path, File::WRONLY|File::CREAT|File::EXCL, 0600) { |f| f.write(data) }
end

out=ARGV.fetch(0)
raise 'Output must be an existing empty directory' unless Dir.exist?(out) && Dir.children(out).empty?
source_path=File.join(SOURCE_ROOT,'SHERLOCK-FEEDBACK.md')
payload_path=File.join(SOURCE_ROOT,'feedback-delivery-2026-10-09/outbound.txt')
receipt_path=File.join(SOURCE_ROOT,'feedback-delivery-2026-10-09/receipt.json')
source=checked(source_path,SOURCE_PIN)
payload=checked(payload_path,PAYLOAD_PIN)
destination=checked(DEST_LOG,DEST_PIN)
receipt=JSON.parse(checked(receipt_path,RECEIPT_PIN))
ack_path=File.join(SOURCE_ROOT,'feedback-delivery-2026-10-09/acknowledgment.txt')
checked(ack_path,ACK_PIN)
old_routing='**Current routing:** That task is archived. New notes are **pending locally**, not delivered, while the existing user question about reopening it or choosing another task remains unanswered. The standing feedback request does not by itself select a replacement destination or authorize silently unarchiving a task. Continue the investigation and batch useful notes; do not repeatedly retry the archived destination.'
before=source.sub(/^\*\*Current routing:\*\*.*$/,old_routing).sub(/<!-- feedback-delivery-2026-10-09:start -->\n.*?<!-- feedback-delivery-2026-10-09:end -->\n\n/m,'')
raise 'Pre-delivery reconstruction mismatch' unless Digest::SHA256.hexdigest(before)==BEFORE_PIN && before.lines.length==2455
raise 'Payload receipt mismatch' unless receipt.fetch('payload_sha256')==PAYLOAD_PIN && receipt.fetch('payload_bytes')==payload.bytesize

items={}
payload.to_enum(:scan,/^(\d{2})\. /).each { items[Regexp.last_match[1].to_i] = Regexp.last_match.begin(0) }
raise 'Digest roster mismatch' unless items.keys==(1..27).to_a
ack_ids=destination.scan(/\*\*Item (\d{2}) —/).flatten.map(&:to_i)
raise 'Acknowledgment roster mismatch' unless ack_ids==(1..27).to_a
item_records=items.map do |id,offset|
  endpoint=items[id+1] || payload.index("\nPlease record receipt",offset) || payload.length
  text=payload[offset...endpoint].strip
  line=destination.lines.index { |l| l.include?("**Item #{format('%02d',id)} —") }+1
  {id:id,text:text,sha256:Digest::SHA256.hexdigest(text),ack_line:line,disposition:([15,16,27].include?(id) ? 'recipient_reports_already_covered_core_requirement' : 'acknowledged_extension'),detail_preservation_verified:false}
end

lines=source.lines
blocks=[]; start=nil
lines.each_with_index do |line,i|
  if line.strip.empty?
    blocks << [start+1,i] if start
    start=nil
  else
    start=i unless start
  end
end
blocks << [start+1,lines.length] if start
raise 'Source block census mismatch' unless blocks.length==272
excluded=EXCLUSIONS.flat_map { |reason,starts| starts.map { |s| [s,reason] } }.to_h
raise 'Duplicate exclusion decision' unless excluded.length==EXCLUSIONS.values.flatten.length
raise 'Unclassified source block' unless blocks.map(&:first).sort==(excluded.keys+TOPICS.keys).sort
raise 'Invalid item link' unless TOPICS.values.flatten.all? { |x| (1..27).include?(x) }

records=[]; annex=[]; serial=0
blocks.each do |first,last|
  raw=lines[(first-1)...last].join
  record={source_start:first,source_end:last,source_block_sha256:Digest::SHA256.hexdigest(raw),source_locator:"#{source_path}:#{first}",pre_delivery_start:(first>=22 ? first-13 : nil),pre_delivery_end:(first>=22 ? last-13 : nil)}
  if excluded.key?(first)
    record.merge!(disposition:'not_retransmitted',reason:excluded[first],digest_items:[],supplement_id:nil)
  else
    serial+=1
    id=format('FBR-%03d',serial)
    transformed=raw.dup
    redactions=[]
    # Remove links, not their visible technical descriptions; no linked source body is loaded.
    transformed.gsub!(/\[([^\]\n]+)\]\(([^)\n]+)\)/) do
      redactions << {kind:'link_destination_removed',original_sha256:Digest::SHA256.hexdigest(Regexp.last_match[0])}
      Regexp.last_match[1]
    end
    transformed.gsub!(/\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i) do |value|
      redactions << {kind:'delivery_identifier_removed',original_sha256:Digest::SHA256.hexdigest(value)}
      '[prior receipt identifier retained locally]'
    end
    phrase='The Didik transport-state lesson is deduplicated here.'
    if transformed.include?(phrase)
      transformed=transformed.sub(phrase,'This transport-state lesson is deduplicated here.')
      redactions << {kind:'case_specific_source_label_removed',original_sha256:Digest::SHA256.hexdigest(phrase)}
    end
    raise "Unexpected disclosure candidate in source block #{first}" if transformed.match?(%r{https?://|/Users/|/private/|protonmail|@|DOC-NIST|\bWTC\d*\b|\bNIST\b|\bRory\b|\bDahl\b|\bDidik\b|01a074ee}i)
    record.merge!(disposition:'technical_detail_retained_in_draft_annex',digest_items:TOPICS.fetch(first),digest_coverage:'topic_correspondence_only_not_complete_clause_certification',supplement_id:id,supplement_sha256:Digest::SHA256.hexdigest(transformed),redactions:redactions,acknowledgment:'not_sent_or_acknowledged',text:transformed)
    annex << "#{id} | Existing batch items #{TOPICS.fetch(first).map { |n| format('%02d',n) }.join(', ')}\n\n#{transformed.rstrip}\n"
  end
  records << record
end

header=<<~TEXT
  DRAFT SFB-SUPPLEMENT-2026-10-09 — technical detail annex

  Intended destination: the existing Sherlock task “Define Phase 0 invariants”.
  NOT SENT. This draft requires review of this exact payload before transmission.

  Purpose: preserve the detailed technical requirements, qualifications, synthetic
  reproductions and acceptance tests behind SFB-BATCH-2026-10-09. The 27-item digest
  and its acknowledgment remain valid delivery records; they are not proof of
  complete requirement preservation. Item links below are topic cross-references,
  not a certification that each detail was already recorded.

  Entries below preserve the original technical note bundles, including detailed
  tests rather than only their subject headings. Every conjunct and test within
  a retained bundle remains part of that bundle. Some requirements overlap or were
  previously acknowledged; deduplicate work items under existing SFB-002 through
  SFB-005, but retain every distinct condition/test and exact supplementary ID.
  Do not reopen resolved SFB-001. This is not a request to implement product code,
  read investigation sources, invoke a real-data bridge, publish, or create tasks.

  The entries are preserved historical technical notes, NOT current operational
  instructions or new test results. “Local only”, “queued”, archived routing and
  earlier delivery phrases describe the note's original writing time. They do
  not override this supplement's actual delivery state. Statements about local
  tests are attributed reports, not tests newly run here or verified Sherlock
  fixes. Synthetic scenarios are not historical case evidence. No case-source
  packet, source link, personal data, private path or original receipt identifier
  is included. Some failure observations are local-workflow observations, not
  source-inspected Sherlock defects. Preserve those qualifications.

  On an authorized delivery, record each FBR identifier with its content hash,
  existing SFB owner, and disposition. An “already covered” disposition should
  name the exact preserved requirement AND reproduction/acceptance details, not
  only a parent heading. Any intentionally excluded or unclear clause must be
  recorded explicitly. Acknowledge receipt independently from implementation,
  testing, activation, scientific validation and human review.
TEXT
body=header+"\n"+annex.join("\n")
csv=CSV.generate do |c|
  c << %w[source_start source_end pre_delivery_start pre_delivery_end source_block_sha256 disposition reason digest_items supplement_id supplement_sha256 acknowledgment]
  records.each do |r|
    c << [r[:source_start],r[:source_end],r[:pre_delivery_start],r[:pre_delivery_end],r[:source_block_sha256],r[:disposition],r[:reason],r[:digest_items].join(';'),r[:supplement_id],r[:supplement_sha256],r[:acknowledgment]]
  end
end
manifest={schema:'feedback-completeness-audit-v1',date:'2026-10-09',state:'local_draft_not_transmitted',scope:'Pinned feedback log and sent 27-item batch; not all investigation records or linked source reports',source_path:source_path,source_sha256:SOURCE_PIN,pre_delivery_sha256:BEFORE_PIN,pre_delivery_lines:2455,outbound_path:payload_path,outbound_sha256:PAYLOAD_PIN,receipt_path:receipt_path,destination_log:DEST_LOG,destination_log_sha256:DEST_PIN,destination_thread:receipt.fetch('destination'),source_blocks:blocks.length,retained_technical_bundles:serial,not_retransmitted:excluded.length,annex_sha256:Digest::SHA256.hexdigest(body),annex_bytes:body.bytesize,coverage_limit:'A bundle can contain several requirements/tests. Counts are not a count of distinct atomic requirements. Digest topic links do not certify semantic completeness. The annex retains complete selected source bundles with only logged locator/receipt-identifier substitutions.',excluded_reasons:EXCLUSIONS,send_authorization:'exact new payload review pending; no send invoked',source_after_unchanged:Digest::SHA256.file(source_path).hexdigest==SOURCE_PIN,destination_after_unchanged:Digest::SHA256.file(DEST_LOG).hexdigest==DEST_PIN}
raise 'Input changed during audit' unless manifest[:source_after_unchanged] && manifest[:destination_after_unchanged]
persist(File.join(out,'technical-annex.txt'),body)
persist(File.join(out,'source-crosswalk.csv'),csv)
persist(File.join(out,'source-crosswalk.json'),JSON.pretty_generate(records)+"\n")
persist(File.join(out,'sent-item-crosswalk.json'),JSON.pretty_generate(item_records)+"\n")
persist(File.join(out,'manifest.json'),JSON.pretty_generate(manifest)+"\n")
puts JSON.pretty_generate(manifest.reject { |k,v| [:source_path,:outbound_path,:receipt_path,:destination_log,:destination_thread,:excluded_reasons].include?(k) })
