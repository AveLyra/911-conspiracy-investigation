class UniqueObject < Hash
  def []=(key, value)
    raise "duplicate JSON key: #{key}" if key?(key)
    super
  end
end
def parse(text)
  JSON.parse(text.dup, object_class: UniqueObject, create_additions: false, allow_nan: false)
end
def check(value, message)
  raise message unless value
end
def exact(a, b)
  return false unless a.class == b.class
  case a
  when Hash then a.keys.sort == b.keys.sort && a.all? { |k,v| exact(v,b[k]) }
  when Array then a.length == b.length && a.each_index.all? { |i| exact(a[i],b[i]) }
  else a == b
  end
end
['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'].each do |bad|
  rejected = false
  begin; parse(bad); rescue JSON::ParserError, RuntimeError; rejected = true; end
  check(rejected, 'strict parser control failed')
end
check(!exact(parse('{"x":false}'),parse('{"x":0}')), 'bool/int control')
check(!exact(parse('{"x":1}'),parse('{"x":1.0}')), 'integer/float control')
u = Pathname.pwd; base = u.parent.parent; old = u.parent/'integration-2026-10-08'
specs = {
 baseline: [old/'candidate-index.json','6ad3012fd455dafe4face2cf031a3624135f83c99b24dfe641e6a35e0084f7e1'],
 extension: [u/'extension.json','41046974bccc6694b8fe9114a738511a7b8858f784892b8705d7a34f7651cc61'],
 candidate01: [u/'candidate01.json','e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8'],
 candidate02: [u/'candidate02.json','e9aac5145a7d0b631474ece1d4b8082ba0f9a53ee0a5daaaf1a531dd9b009ff8'],
 protocol: [u/'PROTOCOL.md','ea61050d5d95fa2978bb33a093331a9e1e44ad11fe3af7241c4366f5685f58aa'],
 code: [u/'extend_index.py','64129bd9df191e23e4258395d7332c91d0a2c86cc3064d50c78e8edb9c7cd10f'],
 tests: [u/'test_extend_index.py','19baab315245d71488abe5fedd19f1b075f50a2f96d3b43767500c6845e65b1b'],
 current: [u.parent/'material-claim-index.json','6ad3012fd455dafe4face2cf031a3624135f83c99b24dfe641e6a35e0084f7e1'],
 old_validator: [old/'validate_index.py','97c4cba63dd29ddc0667262a9038bfb86670ee1ddee8e27175e53626c9aaee96'],
 old_tests: [old/'test_validate_index.py','7f37639dad2a9704997037610604f74bf7bdd989bce4147d2de8b1bf1b99decb'],
 original_baseline: [old/'baseline-index.json','fcc7eef21ad67f61bfe46c8cd9a326974c19979ac0a838cc386680c144ed9d61'],
 original_inputs: [old/'inputs.json','f2458dd600accc1234c58738de11525b433cd55017e56f55295a2fee01b17fe8'],
 original_protocol: [old/'PROTOCOL.md','fbfc63b9c4559d2b7e99cf0daeb67db4f078322a74f2080da5cad2b2af78b888']
}
raw = specs.transform_values { |p,digest| bytes = File.binread(p); check(Digest::SHA256.hexdigest(bytes)==digest,"pin #{p}"); bytes }
check(raw[:candidate01] == raw[:candidate02], 'candidate bytes differ')
check(raw[:baseline] == raw[:current], 'current v2 changed')
b = parse(raw[:baseline]); c = parse(raw[:candidate01]); x = parse(raw[:extension])
check(exact(c,parse(raw[:candidate02])), 'candidate parsed difference')
check(c.keys.sort == b.keys.sort,'top key roster')
mutable = %w[version date scope remaining_index_work]
check(x['root_updates'].keys.sort == mutable.sort,'root update roster')
mutable.each { |k| check(exact(c[k],x['root_updates'][k]),"root update #{k}") }
protected_top = b.keys-mutable-['integration']
protected_top.each { |k| check(exact(b[k],c[k]),"old top #{k}") }
bi=b['integration']; ci=c['integration']; adds=x['additions']; registries=%w[artifacts families transforms claim_links]
check(ci.keys.sort == (bi.keys+['distant_view_revision']).sort,'integration key roster')
protected_integration = bi.keys-registries-['additional_claims']
protected_integration.each { |k| check(exact(bi[k],ci[k]),"old integration #{k}") }
counts={}
registries.each do |field|
  check((bi[field].keys & adds[field].keys).empty?,"collision #{field}")
  check(ci[field].keys.sort == (bi[field].keys+adds[field].keys).sort,"registry #{field}")
  bi[field].each { |id,row| check(exact(row,ci[field].fetch(id)),"old #{field} #{id}") }
  adds[field].each { |id,row| check(exact(row,ci[field].fetch(id)),"new #{field} #{id}") }
  counts[field]=[bi[field].length,adds[field].length,ci[field].length]
end
check(counts=={'artifacts'=>[207,65,272],'families'=>[19,2,21],'transforms'=>[23,4,27],'claim_links'=>[58,5,63]},'counts')
check(bi['additional_claims'].length==18 && exact(ci['additional_claims'][0,18],bi['additional_claims']),'old18 prefix')
check(ci['additional_claims'].length==23 && exact(ci['additional_claims'][18..-1],adds['additional_claims']),'new5 suffix')
expected_revision=parse(JSON.generate(x['revision']))
expected_revision['extension']=parse(JSON.generate({'path'=>'synthesis-packet/distant-view-integration-2026-10-08/extension.json','bytes'=>raw[:extension].bytesize,'sha256'=>specs[:extension][1]}))
expected_revision['protocol']=x['controls']['protocol']; expected_revision['baseline']=x['controls']['baseline']
check(exact(ci['distant_view_revision'],expected_revision),'revision mismatch')
check(ci['distant_view_revision']['limits'].values.all? { |v| v.equal?(false) },'acceptance flags')
claims=%w[Q03-DistantView-selected-corner-coverage Q03-DistantView-contour-correspondence Q10-DistantView-localization-pilot-pending Q03-DistantView-PTS-type-association Q10-DistantView-generated-clock-limit]
check(adds['additional_claims'].map { |r| r['id'] }.sort==claims.sort && adds['claim_links'].keys.sort==claims.sort,'newclaim roster')
check(adds['families'].keys.sort==%w[F-DistantView-access-copy F-FFmpeg-tagged-source].sort,'family roster')
check((ci['claim_links'].keys-ci['additional_claims'].map { |r| r['id'] }).length==40,'old40 roster')
expected_units={
 'source-screen'=>[[claims[0]],'T-DistantView-source-screen'],
 'contour-correspondence'=>[[claims[1]],'T-DistantView-contour-correspondence'],
 'localization-packet'=>[[claims[2]],'T-DistantView-localization-packet'],
 'encoded-timing'=>[claims[3..4],'T-DistantView-encoded-timing']
}
units=ci['distant_view_revision']['units']; af=%w[input_artifacts code_artifacts output_artifacts verification_artifacts]
check(units.map { |r| r['id'] }.sort==expected_units.keys.sort,'unit roster')
check(adds['transforms'].keys.sort==expected_units.values.map { |v| v[1] }.sort,'transform roster')
artifacts=ci['artifacts']; transforms=ci['transforms']
ci['claim_links'].each do |id,row|
  {'work_packages'=>'wp_components','dependencies'=>'dependencies','causal_links'=>'causal_links'}.each do |edge,registry|
    row[edge].each { |r| check(ci[registry].key?(r['id']),"dangling #{id} #{edge}") }
  end
  row['evidence'].each do |r|
    check(artifacts.key?(r['artifact_id']),"dangling #{id} artifact")
    check(r['locator'].is_a?(String) && !r['locator'].strip.empty?,"locator #{id}")
    check(r['family_id'].nil? || ci['families'].key?(r['family_id']),"dangling #{id} family")
  end
  row['transforms'].each { |tid| check(transforms.key?(tid),"dangling #{id} transform") }
end
transforms.each { |id,row| af.each { |field| row[field].each { |aid| check(artifacts.key?(aid),"dangling #{id} #{field}") } } }
ci['families'].each { |id,row| row['basis'].each { |r| check(artifacts.key?(r['artifact_id']) && r['locator'].is_a?(String) && !r['locator'].strip.empty?,"dangling #{id} basis") } }
reachable=[]; unit_counts={}
units.each do |row|
  uc,tid=expected_units.fetch(row['id'])
  check(row['claim_ids'].sort==uc.sort && row['transform_ids']==[tid],'unit map')
  reached=[]
  uc.each do |cid|
    link=ci['claim_links'][cid]
    check(link['transforms'].include?(tid),"unit transform #{cid}")
    check(link['causal_links'].empty? && link['absences']['causal_links']['kind']=='not_applicable','causal support')
    reached.concat(link['evidence'].map { |r| r['artifact_id'] })
    link['transforms'].each { |t| af.each { |field| reached.concat(transforms[t][field]) } }
  end
  reached.uniq!; reachable.concat(reached)
  unit_counts[row['id']]={claims:uc.length,transforms:row['transform_ids'].length,reachable_artifacts:reached.length,new_reachable_artifacts:(reached & adds['artifacts'].keys).length}
end
check((adds['artifacts'].keys-reachable).empty?,'orphan new artifact')
roots=['/Users/admin/docs/911','/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation']; seen={}; total=0
artifacts.each do |id,row|
  p=Pathname.new(row['path']); p=base/p unless p.absolute?
  check(!p.each_filename.to_a.include?('..') && p.ascend.none? { |a| a.symlink? },"escape/symlink #{id}")
  p=p.realpath
  check(roots.any? { |root| p.to_s.start_with?(root+'/') },"outside root #{id}")
  check(!seen.key?(p.to_s),"duplicate artifact path #{id}"); seen[p.to_s]=id
  before=p.stat; bytes=File.binread(p); after=p.stat
  check([before.dev,before.ino,before.size,before.mtime,before.ctime]==[after.dev,after.ino,after.size,after.mtime,after.ctime],"changed read #{id}")
  check(row['bytes'].class==Integer && bytes.bytesize==row['bytes'],"size #{id}")
  check(Digest::SHA256.hexdigest(bytes)==row['sha256'],"hash #{id}"); total+=bytes.bytesize
end
specs.each { |name,(path,digest)| bytes=File.binread(path); check(bytes.b==raw[name].b && Digest::SHA256.hexdigest(bytes)==digest,"changed control #{name}") }
puts JSON.pretty_generate({status:'pass',strict_parser_controls:5,independent_language:RUBY_DESCRIPTION,candidates_byte_identical:true,candidate_bytes:raw[:candidate01].bytesize,candidate_sha256:specs[:candidate01][1],current_index_remains_v2:true,preserved_old_claim_links:58,preserved_old_addition_prefix:18,original_claim_links:40,registry_counts_old_added_final:counts,final_additional_claims:23,old_protected_top_objects:protected_top,old_protected_integration_objects:protected_integration,exact_extension_revision:true,units:unit_counts,new_reachable_artifacts:(adds['artifacts'].keys & reachable).length,all_selected_artifact_pins_verified:artifacts.length,artifact_bytes_total:total,unique_resolved_artifact_paths:seen.length,controls_unchanged:specs.length,limit:'Mechanical preservation, bytes and explicit graph references only; no semantic support, inherited source tests, source authenticity, human/expert acceptance or historical/cause inference.'})
