require 'json'
require 'digest'

dir=File.dirname(__FILE__)
manifest=JSON.parse(File.read(File.join(dir,'manifest.json')))
expected=manifest.fetch('files')
raise 'Unexpected packet files' unless Dir.children(dir).sort==(expected.keys+['manifest.json']).sort
expected.each do |name,spec|
  bytes=File.binread(File.join(dir,name))
  raise "Changed file: #{name}" unless Digest::SHA256.hexdigest(bytes)==spec.fetch('sha256') && bytes.bytesize==spec.fetch('bytes')
end
metadata=JSON.parse(File.read(File.join(dir,'metadata.json')))
record_path=File.expand_path(metadata.fetch('public_record').fetch('path'),dir)
raise 'Changed public technical record' unless Digest::SHA256.file(record_path).hexdigest==metadata['public_record']['sha256']
record=JSON.parse(File.read(record_path))
raise 'Different source snapshot' unless record.fetch('source').fetch('sha256')==metadata.fetch('source_sha256')
findings=JSON.parse(File.read(File.join(dir,'findings.json')))
def valid_roster?(rows)
  rows.map { |r| r['id'] }==(1..24).map { |n| format('G%02d',n) }
end
raise 'Finding roster mismatch' unless valid_roster?(findings)
counts=findings.group_by { |r| r.fetch('classification') }.transform_values(&:length)
raise 'Classification mismatch' unless counts==metadata.fetch('counts') && counts.values.sum==24
ids=record.fetch('units').map { |u| u.fetch('id') }
record_lines=File.readlines(record_path)
rendered_findings=File.read(File.join(dir,'FINDINGS.md'))
findings.each do |r|
  raise 'Unmapped finding' if r.fetch('public_technical_units').empty?
  r.fetch('public_technical_units').each do |id|
    raise 'Invalid public unit' unless ids.include?(id)
    line=r.fetch('public_unit_line_numbers').fetch(id)
    raise 'Incorrect JSON line link' unless record_lines.fetch(line-1).include?("\"id\": \"#{id}\"")
    raise 'Missing rendered link' unless rendered_findings.include?("[#{id}](../feedback-technical-record-2026-10-09/record.json#L#{line})")
  end
end
digest=File.read(File.join(dir,'DIGEST-ITEMS.txt'))
raise 'Digest roster mismatch' unless digest.scan(/^(\d{2})\. /).flatten.map(&:to_i)==(1..27).to_a
raise 'Negative roster control failed' if valid_roster?(findings[0...-1])
spec=expected.fetch('DIGEST-ITEMS.txt')
raise 'Negative content control failed' if Digest::SHA256.hexdigest(digest+'changed')==spec.fetch('sha256')
puts JSON.pretty_generate({status:'pass',manifest_files:expected.length,digest_items:27,findings:24,counts:counts,negative_controls:2,public_unit_links:'valid',original_source_accessed:false,product_tests_run:false})
