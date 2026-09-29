# Read-only integrity/repeat and local-link checks. Does not verify physics.
require 'json'
require 'digest'

base = File.expand_path(__dir__)
cache = {}
checks = 0
runs = %w[run01 run02 run03 run04 identifiers01 identifiers02 identifiers03]
old_code = %w[eff900720a56dbf026df8f9dcc60571803b7ece70f04ff1d8a4918279f64aa8d
              e77b6eff0b58ecb66e1b8914735abd8e4217978ddc92853766356ceffeccd116]
runs.each do |run|
  receipt = JSON.parse(File.read(File.join(base, run, 'receipt.json')))
  raise 'Before/after dependency mismatch' unless receipt.fetch('before') == receipt.fetch('after')
  receipt.fetch('before').each do |path, expected|
    actual_path = old_code.include?(expected.fetch('sha256')) ? File.join(base, 'source-v1', File.basename(path)) : path
    actual = cache[actual_path] ||= {'sha256' => Digest::SHA256.file(actual_path).hexdigest,
                                   'bytes' => File.size(actual_path)}
    raise 'Dependency mismatch' unless actual == expected
    checks += 1
  end
  path = File.join(base, run, 'results.json')
  actual = {'sha256' => Digest::SHA256.file(path).hexdigest, 'bytes' => File.size(path)}
  raise 'Result mismatch' unless actual == receipt.fetch('results')
end
%w[run02 run03 run04].each do |run|
  raise 'Stem repeat differs' unless File.binread(File.join(base, 'run01/results.json')) == File.binread(File.join(base, run, 'results.json'))
end
%w[identifiers02 identifiers03].each do |run|
  raise 'Identifier repeat differs' unless File.binread(File.join(base, 'identifiers01/results.json')) == File.binread(File.join(base, run, 'results.json'))
end

documents = Dir.glob(File.join(base, '*.md')).sort
local_links = 0
external_links = 0
documents.each do |path|
  contents = File.read(path)
  raise 'Missing terminal newline' unless contents.end_with?("\n")
  raise 'Trailing whitespace' if contents.lines.any? { |line| line.match?(/[ \t]+\r?\n\z/) }
  raise 'Conflict marker' if contents.match?(/^(<<<<<<<|=======|>>>>>>>)(?: |$)/)
  # Sufficient for this unit's simple Markdown links, not a general parser.
  contents.scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each do |target|
    if target.start_with?('http://', 'https://')
      external_links += 1
      next
    end
    next if target.start_with?('#')
    target = target.split('#', 2).first
    resolved = File.expand_path(target, File.dirname(path))
    raise "Missing local link in #{File.basename(path)}" unless File.exist?(resolved)
    local_links += 1
  end
end
puts JSON.generate({runs: runs.length, dependency_checks: checks,
                    distinct_pinned_dependencies: cache.length,
                    stem_outputs_equal: true, identifier_outputs_equal: true,
                    documents: documents.length, local_links: local_links,
                    external_links_not_reopened: external_links})
