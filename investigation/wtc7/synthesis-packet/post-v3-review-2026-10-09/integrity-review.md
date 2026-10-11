# Fixed-packet integrity and coverage review

October 9, 2026. **No mismatch found in the twenty selected pins, eleven-unit
selection, or specified structured spot checks.** This is local integrity,
coverage and saved-output arithmetic review, not source authentication,
historical replication, physical validation or acceptance of a mechanism.

## Scope and independence

The main AGENTS/WORKFLOW/START-HERE/CHARTER controls, [SCOPE.md](SCOPE.md) and
[inputs.json](inputs.json) govern. The four main controls match their fully read
versions. Evidence-falsification and source-of-truth skills require the stated
claim ceilings. This reviewer previously authored an F7 primary annotation and
independent checkers, and proposed/reviewed the Cather overview access unit.
The Ruby arithmetic below is newly written without importing those checkers
or producers; this is not a blind independent historical-source review.
Neither opposed interpretation was read. No gated DEP substance was inspected;
A02 was hashed as a selected report, and only STATUS's report-level handling
description was used for coverage. No original media, solver, acquisition,
network request or acceptance operation was executed.

Freeze identities checked at receipt d7ab76:

- SCOPE.md: `cb86bb6eb97bbf316c5816dea46a9b863722f03c4f5ff38fdaacb4f095348661`.
- inputs.json: `53a619f5f277f6977e8c225f33a976517db5d29c9085094165be14260464dba4`.

## Selected pins and coverage

Receipt 9f093a: **20/20 byte lengths and SHA256 values match**, with exactly
A01–A11, B01–B05 and C01–C04 and twenty distinct paths. B05 remains 444,380 bytes,
SHA256 `e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8`.
This does not recheck the index's entire inherited dependency closure.

STATUS lines 1–265 were read (8a30ec). Its nine headings preceding
“DistantView material claim integration” map as follows; exact report-link
resolution independently passes for every selected addition (acb2bd):

| Pre-v3 heading, newest first | Selected unit |
| --- | --- |
| Cather Pound execution source unavailable through the checked locator | A11 |
| Synthetic viewer miss diagnosed within the new test | A10 |
| Generator specification retrieval stopped without content | A09 |
| Thermal citation checked beyond its abstract | A08 |
| Shop drawing retrieval stopped with source unread | A07 |
| NBC source candidates and remaining acquisition step | A06 |
| OEM control change source review | A05 |
| Updated F7 human-review packet | A04 |
| Current F7 completion and municipal preservation follow through | A01, A02, A03 |

Thus eleven substantive units are represented, not nine reports. The linked
feasibility/routing update is context, not another source/test addition. This
coverage check is bounded to the declared STATUS cutoff, not a corpus census.

## Structured spot checks

A03's [saved F7 result](../../connection-curve-comparison/native-footprint-pass/force7-paired-coverage/run-v2-01.json)
contains two 220-row readings, each covering 110 unique columns 220–329; actual
conditional-window flags count 40 and 35 (dff5a9). There are 75 new dashed
candidates and 264 preserved earlier F7 candidates. Independently selecting
paired-local segments, checking positive/disjoint intervals and summing exact
Ruby rationals reproduces all four lengths and six-decimal report values
(1f8208):

| Solid/dash reader | Before | Added | Current segments | Fragment-pair runs | Exact graphical x length | Rounded |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| primary/primary | 0 | 27 | 27 | 10 | 444408741/12350000 | 35.984513 |
| primary/peer | 1 | 24 | 25 | 10 | 16459583/494000 | 33.318994 |
| peer/primary | 0 | 26 | 26 | 9 | 16459583/475000 | 34.651754 |
| peer/peer | 1 | 23 | 24 | 9 | 49378749/1543750 | 31.986234 |

Lengths use the report's 1700×2200 composed-page x coordinate, not native
pixel counts, time, force, energy, physical precision or confidence intervals.
Four reader combinations are alternatives, not independent historical events.
This spot check uses saved segment endpoints; it does not re-extract ink,
reconstruct the full pipeline or validate Hidentity/Hsupport/Hink0.

A04's [repaired packet](../../connection-curve-comparison/historical-applicability/f7-review-packet-2026-10-08/packet-v2-01.json)
has 42 slots and 84 entries. All entries are uninspected with null responses;
all slots and the packet have human_accepted=false. Recounting slot statuses
gives 32 paired-local candidates and ten boundary-unresolved slots. Composition
counts are 4779+75=4854, preserving 264 old F7 candidates. Both A03/A04 saved
results have actual_D and model_discrepancies null. Packet
original_actual_D_sampling_fulfilled remains false. No physical discrepancy or
human acceptance is supplied by these outputs (ac34bf; 1f8208).

A06's [sanitized acquisition disposition](../../audio-listening-2026-10-05/c-source-lineage/nbc-folder-2026-10-08/acquisition/disposition.json)
states no materialized path, no inline base64 and local_media_acquired=false;
the second candidate was not requested. The 2,703,430-byte number is provider
metadata, not acquired bytes. Bounded acquisition-directory inventory found
only PROTOCOL.md and disposition.json (7e4c40), not a media file. This is not a
whole-filesystem absence claim or independent witnessing of the connector.

A11's [access result](../../comparator-cather-pound/project-overview-2026-10-09/access-result.json)
records curl exit6, HTTP metric000, null received status, zero bytes/redirects
and no source-content reading. It agrees with the report's DNS-stage limit,
not server denial, 404, historical absence or concealment (47fbcc; 1f8208).
These network details remain root's labeled transcription. The preceding
separate access review independently inspected the empty scratch header and
absent body; no new acquisition or scratch inspection occurred in this unit.

Additional structured-file identities measured in 1f8208:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| F7 run-v2-01.json | 1193518 | ade1b08251bd68ed71ec535e263389725e193b81e6aa4959e8a891fcb1505aeb |
| packet-v2-01.json | 233479 | d2c75d2a399d495d88f270181259c71893c8025c68e542c150a57c60a91b6c83 |
| NBC acquisition/disposition.json | 1849 | 29416432e071674a1a89f58a0b02ad344c79e83ea1d7efdc3ae35e4bf32fd0ca |
| Cather access-result.json | 1877 | 833d0c211790c1404e0d56eec9da49447e2aa4af0419fae04bcee7e3dafc478b |

## Exact verification commands

All commands used login:false. `command -v ruby` and `ruby --version` returned
/usr/bin/ruby, Ruby 2.6.10p210, universal.arm64e-darwin25 (d7ab76).
The following commands ran from this review directory, each exit0:

```sh
ruby -rjson -rdigest -e 'j=JSON.parse(File.binread("inputs.json")); rows=j.fetch("inputs"); raise "count" unless rows.length==20; raise "IDs" unless rows.map{|r|r.fetch("id")}.sort==((1..11).map{|i|"A%02d"%i}+(1..5).map{|i|"B%02d"%i}+(1..4).map{|i|"C%02d"%i}); rows.each{|r|b=File.binread(r.fetch("path")); raise "bytes #{r.fetch("id")}" unless b.bytesize==r.fetch("bytes"); raise "hash #{r.fetch("id")}" unless Digest::SHA256.hexdigest(b)==r.fetch("sha256"); puts "#{r.fetch("id")} #{b.bytesize} #{Digest::SHA256.hexdigest(b)} PASS"}; puts "20/20 selected pins match; unique paths=#{rows.map{|r|r.fetch("path")}.uniq.length}"'
ruby -rjson -rpathname -e 'u=Pathname.pwd; b=u.parent.parent; text=File.read(b+"STATUS.md"); section=text.split(/^## DistantView material claim integration\s*$/,2).first; heads=section.scan(/^## (.+)$/).flatten; raise "headings #{heads.length}" unless heads.length==9; puts heads.each_with_index.map{|h,i|"#{i+1}. #{h}"}; additions=JSON.parse(File.read("inputs.json")).fetch("inputs").select{|r|r.fetch("id").start_with?("A")}; sections=section.split(/(?=^## )/); additions.each{|r| hit=sections.select{|s|s.scan(/\]\(([^)]+)\)/).flatten.any?{|link| !link.match?(/\A[a-z]+:/i) && (b+link.split("#",2).first).cleanpath.to_s==r.fetch("path")}}; raise "coverage #{r.fetch("id")}" unless hit.length>=1; puts "#{r.fetch("id")}: #{hit.map{|s|s.lines.first.strip}.join(" | ")}"}; puts "11/11 addition report paths linked within nine pre-v3 headings"'
shasum -a 256 SCOPE.md inputs.json
```

The following standalone check ran from the investigation root
`/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation`,
exit0 (1f8208). It reads four named saved JSON files only:

```sh
ruby -rjson -rdigest <<'RUBY'
root = Dir.pwd
paths = {
  f7: 'connection-curve-comparison/native-footprint-pass/force7-paired-coverage/run-v2-01.json',
  packet: 'connection-curve-comparison/historical-applicability/f7-review-packet-2026-10-08/packet-v2-01.json',
  nbc: 'audio-listening-2026-10-05/c-source-lineage/nbc-folder-2026-10-08/acquisition/disposition.json',
  cather: 'comparator-cather-pound/project-overview-2026-10-09/access-result.json'
}
objects = paths.transform_values { |p| JSON.parse(File.binread(p)) }
paths.each { |k,p| bytes=File.binread(p); puts "#{k} #{bytes.bytesize} #{Digest::SHA256.hexdigest(bytes)} #{p}" }
f=objects.fetch(:f7)
raise 'F7 ceiling' unless f.fetch('actual_D').nil? && f.fetch('model_discrepancies').nil? && f.fetch('human_accepted')==false
raise 'readings/candidates' unless f.fetch('new_readings').map{|r|r.fetch('rows').length}==[220,220] && f.fetch('new_candidate_cells').length==75 && f.fetch('preserved_old_F7_candidate_cells').length==264
raise 'candidate routes' unless f.fetch('new_candidate_cells').all?{|c|c.fetch('route')=='dash'}
expected=[['primary','primary',0,27,10,'35.984513'],['primary','peer',1,25,10,'33.318994'],['peer','primary',0,26,9,'34.651754'],['peer','peer',1,24,9,'31.986234']]
raise 'scenario count' unless f.fetch('after_scenarios').length==4 && f.fetch('before_scenarios').length==4
f.fetch('after_scenarios').zip(f.fetch('before_scenarios'),expected).each do |s,b,e|
  segments=s.fetch('segments').select{|x|x.fetch('status')=='paired_local_candidate'}
  intervals=segments.map{|x|x.fetch('render_x').map{|v|Rational(v)}}.sort
  raise 'nonpositive/overlap' unless intervals.all?{|lo,hi|hi>lo} && intervals.each_cons(2).all?{|x,y|x[1]<=y[0]}
  length=intervals.inject(Rational(0)){|sum,(lo,hi)|sum+hi-lo}
  actual=[s.fetch('solid_reader'),s.fetch('dash_reader'),b.fetch('paired_segment_count'),segments.length,s.fetch('paired_runs').length,format('%.6f',length.to_f)]
  raise "scenario #{actual}" unless actual==e && s.fetch('paired_segment_count')==segments.length && length>0 && length==Rational(s.fetch('any_paired_render_length')) && length==Rational(s.fetch('render_lengths').fetch('paired_local_candidate')) && s.fetch('actual_D').nil? && s.fetch('human_accepted')==false
  puts "F7 #{actual.join(' | ')}; exact page-render x length=#{length}; added segments=#{segments.length-b.fetch('paired_segment_count')}"
end
p=objects.fetch(:packet); slots=p.fetch('slots'); entries=slots.flat_map{|s|s.fetch('entries')}
raise 'packet ceiling/counts' unless slots.length==42 && entries.length==84 && entries.all?{|e|e.fetch('human_status')=='uninspected' && e.fetch('human_response').nil?} && slots.all?{|s|s.fetch('human_accepted')==false} && p.fetch('human_accepted')==false && p.fetch('actual_D').nil? && p.fetch('model_discrepancies').nil? && p.fetch('original_actual_D_sampling_fulfilled')==false
counts=slots.group_by{|s|s.fetch('selection_status')}.transform_values(&:length)
raise 'slot categories' unless counts=={'paired_local_candidate'=>32,'boundary_unresolved'=>10} && counts==p.fetch('summary')
raise 'composition counts' unless p.fetch('composition').values_at('old_candidate_cell_count','added_F7_candidate_cell_count','composed_candidate_cell_count','preserved_old_F7_candidate_cell_count')==[4779,75,4854,264]
puts 'Packet: 42 slots / 84 uninspected-null entries / 32 paired-local + 10 boundary; discrepancy and D null; human false'
n=objects.fetch(:nbc)
raise 'NBC acquisition' unless n.fetch('local_media_acquired')==false && n.fetch('materialized_local_path_fields')==[] && n.fetch('inline_base64_returned')==false && n.fetch('second_candidate').fetch('request_made')==false
puts 'NBC: no materialized local path/base64/media; second candidate not requested; metadata size is not acquired bytes'
c=objects.fetch(:cather); net=c.fetch('curl')
raise 'Cather access' unless c.fetch('status')=='stopped_without_source_content' && c.fetch('web_reader').fetch('http_status').nil? && net.fetch('exit_code')==6 && net.fetch('http_code_metric')=='000' && net.fetch('received_http_status').nil? && net.fetch('size_download')==0 && net.fetch('num_redirects')==0 && net.fetch('source_content_acquired')==false && c.fetch('content_review')=={'root'=>false,'peer'=>false}
puts 'Cather: saved exit6 / HTTP metric000 / no received status / zero bytes or redirects / no content reading'
puts 'All scoped structured spot checks PASS; no producer/checker code imported or historical extraction rerun'
RUBY
```

Also from that investigation root, each exit0:

```sh
jq -e '[.new_readings[]|{rows:(.rows|length),unique_columns:([.rows[].column]|unique|length),minimum:([.rows[].column]|min),maximum:([.rows[].column]|max),windows:([.rows[]|select(.conditional_window==true)]|length)}] == [{rows:220,unique_columns:110,minimum:220,maximum:329,windows:40},{rows:220,unique_columns:110,minimum:220,maximum:329,windows:35}]' connection-curve-comparison/native-footprint-pass/force7-paired-coverage/run-v2-01.json
find audio-listening-2026-10-05/c-source-lineage/nbc-folder-2026-10-08/acquisition -maxdepth 2 -type f -exec stat -f '%N %z bytes' {} +
```

Navigation used bounded `cat`, `sed`, `rg` and `jq`. An initial verbose F7
projection was display-truncated (d53640); it was not treated as complete
reading. The compact projection (c8a2f3) and full-object scoped assertions
(1f8208) supplied the results above. No failed assertion was waived. Only this
review file was added. Root's forthcoming synthesis, reviewer freezes, output
links and final navigation remain separate later checks.
