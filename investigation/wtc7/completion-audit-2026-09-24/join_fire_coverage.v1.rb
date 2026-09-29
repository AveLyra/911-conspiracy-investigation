#!/usr/bin/env ruby
# Read only named historical research records. Output only to a fresh file.
require 'json'
require 'digest'
require 'pathname'

MAIN = Pathname('/Users/admin/docs/911/research/sherlock-wtc7-investigation')
BASE = Pathname(__dir__).parent
FILES = {
  source_map: MAIN.join('fire-observation-source-map.md'),
  key: MAIN.join('fire-annotation/assets/run-01/reviewed-provenance-key.json'),
  batch: BASE.join('fire-coverage-batch2/inventory01.json'),
  extension: MAIN.join('fire-coverage-extension/lineage.json'),
  extension_scope: MAIN.join('fire-coverage-extension/selection-v1.md'),
  peskin: MAIN.join('fire-originals/peskin/report.md'),
  didik: MAIN.join('fire-originals/didik/report.md'),
  correspondence: BASE.join('peskin-figure-correspondence/report.md'),
  photometric: BASE.join('peskin-photometric-sensitivity/report.md'),
  late: BASE.join('late-fire-sequence/report.md'),
  protocol: Pathname(__dir__).join('FIRE-FIRST-ACTION.md'),
  script: Pathname(__FILE__)
}.freeze
bytes = FILES.transform_values(&:binread)
pins = FILES.map { |id, path| {id: id, path: path.to_s, sha256: Digest::SHA256.hexdigest(bytes[id])} }
key = JSON.parse(bytes.fetch(:key))
batch = JSON.parse(bytes.fetch(:batch))
extension = JSON.parse(bytes.fetch(:extension))
# Exact transcription of the source-map's 'Located but not visually inspected'
# table, not an automated interpretation of arbitrary prose or page numbers.
pages = {79=>[214],111=>[240],114=>[244],116=>[246],118=>[248],145=>[275],146=>[276]}
[[[59,60,61],[198,199]], [[121,122,123,124],[252,253,254]],
 [[128,129,130],[258,259]], [[132,133,134],[261,264]],
 [[136,138,139,140,141,142,143,144],[266,268,269,270,271,272,273]],
 [[152,153,154,155,156,159],[281,282,283,284,286]]].each do |figures, group_pages|
  figures.each { |figure| pages[figure] = group_pages }
end
# Grouped map locators stay ranges/sets; never guess an exact figure/page join.
pages = pages.sort.to_h
associations = key.fetch('assets').flat_map { |a| a.fetch('figure_associations').map { |f| f.merge('asset_id'=>a.fetch('asset_id')) } }
paired = batch.fetch('assets').select { |a| ['prior_paired_photographic','new_batch2_photographic'].include?(a.fetch('review_status')) }
raise 'unexpected paired membership' unless paired.size == 25 && paired.map { |a| a['asset_id'] }.uniq.size == 25
selection = extension.fetch('selection').fetch('target_pages_1_based')
rows = pages.map do |n, candidate_pages|
  figure = "5-#{n}"
  located = associations.select { |a| a.fetch('figure') == figure }
  scored = paired.select { |a| a.fetch('figure_association').fetch('figure') == figure }
  extension_coverage = (candidate_pages - selection).empty?
  {figure: figure, candidate_physical_pages: candidate_pages,
   page_assignment: candidate_pages.size > 1 ? 'grouped-map locator; no unique page assigned' : 'map locator; not fresh source association',
   extracted_ids: located.map { |a| a.fetch('asset_id') },
   paired_ids: scored.map { |a| a.fetch('asset_id') },
   extension_covers_candidate_pages: extension_coverage,
   disposition: !scored.empty? ? 'paired-in-declared-25' : (!located.empty? ? 'extracted-no-paired-match' : (extension_coverage ? 'prior-extension-screening-only' : 'no-coverage-in-declared-union'))}
end
raise 'selected gap unexpectedly paired' unless rows.select { |r| %w[5-145 5-146].include?(r[:figure]) }.all? { |r| r[:disposition] == 'no-coverage-in-declared-union' }
raise 'input changed' unless FILES.all? { |id, path| path.binread == bytes[id] }
result = {schema_version: 1, scope: 'finite source-map candidate join, not full report/public-source coverage',
          inputs: pins, candidate_count: rows.size, rows: rows,
          counts: rows.group_by { |r| r[:disposition] }.transform_values(&:size),
          manual_followup_account: {'peskin/correspondence/photometric'=>%w[5-147 5-148 5-149 5-151], 'late'=>%w[5-157 5-158], 'didik'=>'5-125/126/150 context and already selected images, not new 5-145/146 images'},
          limitation: 'Report-target account is a reviewed scope transcription, not a search of every image or authentication of captions.'}
output = ARGV.fetch(0)
File.open(output, 'wx') { |f| f.write(JSON.pretty_generate(result) + "\n") }
puts JSON.generate({candidate_count: rows.size, counts: result[:counts], selected_gaps: %w[5-145 5-146]})
