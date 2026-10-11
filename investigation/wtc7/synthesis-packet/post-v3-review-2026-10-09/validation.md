# Verification of the October 9 changed evidence review

This record covers a derivative WP6 synthesis, selected input integrity and
bounded arithmetic/metadata checks. It does not certify historical authenticity,
repeat every source reading or experiment, or admit any physical finding.

## Controls and actual sequence

Worktree: /Users/admin/docs/911-worktrees/sherlock-wtc7-investigation.
Branch: research/sherlock-wtc7-investigation.
Starting HEAD: ca1c223335c20905d6608eb15c676f88cbfac734.
Pre-existing dirty work remains; no commit, push or main/legal edit is part of
this unit. Main AGENTS/WORKFLOW/START-HERE and the main charter control.

Root read the selected addition reports and baseline interpretations in this
turn and its pre-compaction portion. Current byte hashes bind those reads;
B05's JSON and selected fields were inspected, not every inherited dependency.
No original image, audio, gated DEP content or new network source was inspected.

The [scope](SCOPE.md) and [twenty-input manifest](inputs.json) were saved and
hashed before both assigned interpretation reviews started (3e9177):
SCOPE SHA256 cb86bb6eb97bbf316c5816dea46a9b863722f03c4f5ff38fdaacb4f095348661;
inputs SHA256 53a619f5f277f6977e8c225f33a976517db5d29c9085094165be14260464dba4.
This selection was prior-informed; it is not prospective registration of the
underlying studies. The eleven-unit selection against nine prior STATUS
headings is independently documented in [integrity-review.md](integrity-review.md).

Both analytical reviewers reported complete freezes and no counterpart access.
Root recorded final hashes in [review-freezes.json](review-freezes.json) and
re-read the final fire text after its last small pre-freeze edit (856cc5).
The intervention final text was read at 89e6ef. Root had seen the fire draft
before its freeze; no claim of root blindness is made. The two reviewers'
own separate-freeze boundary is retained. Prior method/annotation involvement
is disclosed by all three reviewing agents.

## Executed checks

- Root Ruby JSON/Digest assertions (eb5db7, exit 0): all 20 selected byte-size/
  SHA256 pins match, IDs A01–A11 complete, scope/manifest hashes as above and
  B05 parses as JSON. The unchanged B05 hash is
  e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8.
- Root initial report checks (540c37, exit 0): eleven individual A rows,
  15 then-present local links resolving and no trailing whitespace. This was
  before review/closeout links, not the final link count.
- Tracked worktree whitespace check (19c8f7, exit 0): git diff --check.
  This alone does not inspect untracked new Markdown; explicit checks do.
- Separate integrity reviewer: 20 input pins, nine-heading/eleven-report
  coverage, saved F7 exact-rational arithmetic, packet acceptance/null fields,
  NBC reference-only disposition and Cather DNS disposition. Exact commands
  and limitations are preserved in integrity-review.md; no hidden source
  reading or network witnessing is claimed.
- Root independently re-executed the bounded F7 arithmetic and packet-state
  assertions below (1ee11f, exit 0). Rows matched 27/10/35.984513,
  25/10/33.318994, 26/9/34.651754 and 24/9/31.986234 for segment count,
  separate runs and graphical page-pixel x length. Packet counts were
  42 slots/84 uninspected entries, 32 candidate/10 boundary-unresolved.
  Both physical-discrepancy fields remained null and human acceptance false.
  This uses saved segment endpoints, not fresh ink extraction or physical
  force/energy measurement.

The root arithmetic command ran from this review directory:

```sh
ruby -rjson -rdigest <<'RUBY'
base = File.expand_path('../..')
fpath = File.join(base, 'connection-curve-comparison/native-footprint-pass/force7-paired-coverage/run-v2-01.json')
pfile = File.join(base, 'connection-curve-comparison/historical-applicability/f7-review-packet-2026-10-08/packet-v2-01.json')
f = JSON.parse(File.read(fpath)); p = JSON.parse(File.read(pfile))
raise 'F7 source changed' unless Digest::SHA256.file(fpath).hexdigest == 'ade1b08251bd68ed71ec535e263389725e193b81e6aa4959e8a891fcb1505aeb'
raise 'packet changed' unless Digest::SHA256.file(pfile).hexdigest == 'd2c75d2a399d495d88f270181259c71893c8025c68e542c150a57c60a91b6c83'
expected = [[27,10,'35.984513'],[25,10,'33.318994'],[26,9,'34.651754'],[24,9,'31.986234']]
actual = f.fetch('after_scenarios').map do |s|
  segs = s.fetch('segments').select { |v| v.fetch('status') == 'paired_local_candidate' }
  intervals = segs.map { |v| v.fetch('render_x').map { |x| Rational(x) } }.sort
  raise 'interval error' unless intervals.all? { |lo,hi| hi > lo } && intervals.each_cons(2).all? { |a,b| a[1] <= b[0] }
  length = intervals.inject(Rational(0)) { |sum,(lo,hi)| sum + hi - lo }
  raise 'saved length error' unless length == Rational(s.fetch('any_paired_render_length'))
  [segs.length, s.fetch('paired_runs').length, format('%.6f',length.to_f)]
end
raise 'four scenarios differ' unless actual == expected
slots = p.fetch('slots'); entries = slots.flat_map { |s| s.fetch('entries') }
raise 'sample counts' unless slots.length == 42 && entries.length == 84
raise 'review state changed' unless entries.all? { |e| e.fetch('human_status') == 'uninspected' && e.fetch('human_response').nil? } && slots.all? { |s| s.fetch('human_accepted') == false }
[f,p].each { |o| raise 'physical/acceptance state' unless o.fetch('actual_D').nil? && o.fetch('model_discrepancies').nil? && o.fetch('human_accepted') == false }
raise 'partition' unless slots.group_by { |s| s.fetch('selection_status') }.transform_values(&:length) == {'paired_local_candidate'=>32,'boundary_unresolved'=>10}
puts JSON.pretty_generate({f7_segment_run_length_rows:actual,packet_slots:slots.length,uninspected_entries:entries.length,physical_discrepancies:null=nil,accepted:false})
RUBY
```

## Retained nonpassing diagnostics and coverage limits

Three navigation/inventory commands ended exit 1: an rg search found no nested
AGENTS.md under worktree research after successful preceding reads (521476);
an ls ran before integrity-review.md existed (196b4b), while both opposed
drafts existed; a later ls preceded critique.md creation (5929e9). These are
not failed empirical tests or proof a missing file was never produced.
A combined instruction read was output-truncated, so the
affected main START-HERE/charter and required writing reference were read
completely in subsequent bounded calls before writing.

The fire reviewer reports an initial broad structured projection truncated,
then replaced by explicit successful field assertions. The intervention reviewer
reports an array-length probe omitted object counts, then a corrected key-count
inspection. The integrity reviewer likewise records a truncated initial
projection and the exact successful standalone replacement. None is represented
as complete original inspection or a failed historical experiment.

No new source acquisition, full simulation, historical media measurement,
audio listening, actual-human annotation, new library or software framework
was executed here. All old tests/results, rejected analyses, sources and v3
index remain preserved. Existing Sherlock notes are not newly routed to the
archived destination. This synthesis itself supplies no new reproducible
product defect, so it does not create a duplicate feedback item.

## Final closeout

The separate critique required one A03 precision repair: old segment counts
were 0/1/0/1, not all zero. Root applied it; the reviewer verified repaired
report SHA4010fa0f0ec71655e4da9b9746c03bd116a370bd78ce0e92faca5115912f7ba7.
Root read the final critique completely (6dffb0). No other material correction
was identified in its stated scope. The final report differs from that reviewed
version only by replacing the pending verification paragraph with the actual
integrity, reproduction and critique disposition; SHA256 is
406254d9a8eba86d8bfd82e78039f35bfbbfcbbc2d3875da5b08bd27bc42330d.

Root's final selected-input/review/coverage/link check (3c6091, exit 0) passed:
20 selected input pins, four frozen review pins, unchanged scope/manifest,
eleven matrix rows, nine explicitly bounded original status headings, seven
Markdown files/83 local links and both navigation pointers. The v3 index is
unchanged. The earlier integrity review's nine-heading command records the
pre-navigation state; the final command below explicitly excludes this new
supplement's header rather than changing the original selection.

Final git diff --check passed (c969c2). The accompanying git diff --numstat
includes extensive pre-existing README/STATUS changes, not this turn's change
count. Branch/HEAD inspection (a65963) confirms the branch and starting commit
above; the new review directory is untracked and navigation files remain dirty.
Only the new directory and two navigation pointers were edited in this unit.

This completes the bounded WP6 changed-evidence reconciliation, not the full
charter. No new empirical cause evidence or accepted state is claimed. The
report's three discriminator groups preserve exact source/human/expert gates.
For the next authorized unit, use full-reasoning review of the main charter,
current report and the relevant existing protocol; select a genuinely available
missing input or actual review response and define acceptance before execution.
Do not repeat completed scans or synthetic checks as new science. Decisions
about sensitive DEP review, archived feedback routing and outside expertise
remain user-owned. Existing status/report carry the context-distiller handoff;
no competing handoff document was created.

The exact final check ran from this review directory:

```sh
ruby -rjson -rdigest -rpathname <<'RUBY'
u = Pathname.pwd; b = u.parent.parent
m = JSON.parse(File.read('inputs.json'))
raise 'input count' unless m.fetch('inputs').length == 20
m.fetch('inputs').each { |r| raise "input changed #{r['id']}" unless File.size(r['path']) == r['bytes'] && Digest::SHA256.file(r['path']).hexdigest == r['sha256'] }
f = JSON.parse(File.read('review-freezes.json'))
raise 'scope changed' unless Digest::SHA256.file('SCOPE.md').hexdigest == f.fetch('scope_sha256')
raise 'manifest changed' unless Digest::SHA256.file('inputs.json').hexdigest == f.fetch('manifest_sha256')
f.fetch('reviews').each { |r| raise "review changed #{r['file']}" unless File.size(r['file']) == r['bytes'] && Digest::SHA256.file(r['file']).hexdigest == r['sha256'] }
{'integrity-review.md'=>'1cb413c0c630c9356ba986b9422aff3d058ffe14746370ee3c0193eab118293e', 'critique.md'=>'37feb496678fcef8dfc7711a5be7babc487bbbb357d007a8b0be296a96bbc640'}.each { |p,h| raise "critique changed #{p}" unless Digest::SHA256.file(p).hexdigest == h }
report = File.read('report.md')
raise 'matrix coverage' unless report.scan(/^\| (A\d{2}) /).flatten == (1..11).map { |i| 'A%02d'%i }
raise 'old draft marker' if report.include?('Final integrity and root-report critique are pending')
mds = Dir['*.md']; links = 0
mds.each do |p|
  t = File.read(p)
  raise "whitespace #{p}" if t.lines.any? { |l| l.chomp.match?(/[ \t]+$/) }
  raise "conflict #{p}" if t.lines.any? { |l| l.match?(/\A(?:<<<<<<<|=======|>>>>>>>)(?:\s|$)/) }
  t.scan(/\]\(([^)]+)\)/).flatten.each do |x|
    next if x.match?(/\A(?:https?:|#)/)
    raise "link #{p}: #{x}" unless File.exist?(File.expand_path(x.split('#',2).first, File.dirname(p)))
    links += 1
  end
end
text = File.read(b+'STATUS.md')
start = text.index("## Cather Pound execution source unavailable through the checked locator\n")
finish = text.index("## DistantView material claim integration\n")
raise 'selection bounds' unless start && finish && finish > start
section = text[start...finish]
raise 'nine original headings' unless section.scan(/^## /).length == 9
local = section.scan(/\]\(([^)]+)\)/).flatten.reject { |x| x.match?(/\A[a-z]+:/i) }.map { |x| (b+x.split('#',2).first).cleanpath.to_s }
additions = m.fetch('inputs').select { |r| r['id'].start_with?('A') }
raise 'selection missing report' unless additions.length == 11 && additions.all? { |r| local.include?(r['path']) }
raise 'STATUS navigation' unless text.include?('(synthesis-packet/post-v3-review-2026-10-09/report.md)')
raise 'README navigation' unless File.read(b.parent+'README.md').include?('(sherlock-wtc7-investigation/synthesis-packet/post-v3-review-2026-10-09/report.md)')
puts JSON.pretty_generate({input_pins:20,review_pins:4,scope_manifest_unchanged:true,addition_rows:11,bounded_status_headers:9,markdown_files:mds.length,local_links:links,navigation:true,index_unchanged:true,report_sha256:Digest::SHA256.file('report.md').hexdigest})
RUBY
```
