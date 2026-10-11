import test from 'node:test';
import assert from 'node:assert/strict';
import {number,pointerToPixel,nudgePixel,formatResponses,describePair,describeScenarios,identityHeader,validateIdentity,validatePacket,PACKET_ID} from './review.mjs';
const identity={version:2,packet_id:PACKET_ID,packet_sha256:'a'.repeat(64)};
test('display rational is not rounded source replacement',()=>{assert.equal(number('5/2'),2.5);assert.equal(number('-2'),-2);for(const v of ['NaN','1/0','1.2',true])assert.throws(()=>number(v));});
test('native coordinates at scaled screen geometry',()=>{const r={left:20,top:30,width:1482,height:176};assert.deepEqual(pointerToPixel(41,71,r,741,88),{x:10,y:20});assert.equal(pointerToPixel(1502,71,r,741,88),null);assert.equal(pointerToPixel(41,206,r,741,88),null);assert.equal(pointerToPixel(19,30,r,741,88),null);});
test('keyboard remains in native image bounds',()=>{assert.deepEqual(nudgePixel({x:10,y:20},'ArrowRight',741,88),{x:11,y:20});assert.deepEqual(nudgePixel({x:0,y:0},'ArrowLeft',741,88),{x:0,y:0});assert.equal(nudgePixel(null,'ArrowRight',741,88),null);});
test('proposal never prefills a response',()=>{const slots=[{selection_status:'boundary_unresolved',entries:[{id:'CE-F3Q1-spring'},{id:'CE-F3Q1-shell'}]}];const result=formatResponses(slots,{},identity);assert.equal(result.split('\n').filter(s=>s.includes('\tuninspected\t')).length,2);assert(!result.includes('agree'));});
test('notes sanitized without inventing reviewer scope',()=>{const slots=[{selection_status:'paired_local_candidate',entries:[{id:'one'}]}];const out=formatResponses(slots,{one:{status:'correction',readers:'primary',notes:'x\t1\ny 2'}},identity);assert(out.endsWith('one\tpaired_local_candidate\tcorrection\tprimary\tx 1 y 2'));});
test('all fourteen panels and confirmed trace colors are explicit',()=>{for(const panel of ['F','E'])for(const [bolt,color] of [[3,'black'],[4,'gold'],[5,'blue'],[6,'red'],[7,'green'],[8,'cyan'],[9,'purple']]){const description=describePair(panel+bolt);assert(description.includes(`${bolt}-bolt pair; ${color} trace`));assert(description.startsWith(panel==='F'?'Force':'Dissipated-energy'));assert(description.endsWith('Solid = spring; dashed = shell.'));}assert.equal(describePair('synthetic'),'Synthetic control only.');});
test('scenario labels retain missing and conflicting alternatives',()=>{assert.equal(describeScenarios({'primary-peer':{status:'shared_ink_ownership_conflict'},'peer-primary':{status:'outside_candidate_extent'}}),'Spring primary / shell peer: shared_ink_ownership_conflict; Spring peer / shell primary: outside_candidate_extent');assert.equal(describeScenarios({}),'');});

function fixture(){
  const slots=[];for(const panel of ['F','E'])for(let b=3;b<=9;b++)for(let q=1;q<=3;q++){
    const id=`CE-${panel}${b}Q${q}`;
    slots.push({id,human_accepted:false,selection_status:'unavailable_empty_primary_domain',entries:['spring','shell'].map(model=>({id:id+'-'+model,human_status:'uninspected',human_response:null}))});
  }
  const assets={};for(const name of ['page',...Array.from({length:12},(_,i)=>'Im'+i)])assets[name]={url:name==='page'?'/page.png':'/source/'+name+'.jpg',width:name==='page'?1700:741,height:name==='page'?2200:88};
  return {...identity,status:'conditional_mapping_packet_pending_human',human_accepted:false,slots,assets};
}
test('copied notes carry ID version and the complete hash',()=>{
  const output=formatResponses(fixture().slots,{},identity);
  assert(output.startsWith('Conditional packet ID\t'+PACKET_ID+'\nConditional packet version\t2\nConditional packet SHA256\t'+'a'.repeat(64)+'\n'));
  assert.equal(output.split('\n').filter(s=>s.includes('\tuninspected\t')).length,84);
});
test('bare hash and older version cannot bind stable CE identifiers',()=>{
  assert.throws(()=>formatResponses([],{},'a'.repeat(64)));
  for(const patch of [{version:1},{version:true},{packet_id:'old'},{packet_sha256:'a'.repeat(63)},{packet_sha256:'A'.repeat(64)}])assert.throws(()=>validateIdentity({...identity,...patch}));
});
test('changing packet hash changes copied identity while preserving CE labels',()=>{
  const a=formatResponses(fixture().slots,{},identity),b=formatResponses(fixture().slots,{},{...identity,packet_sha256:'b'.repeat(64)});
  assert.notEqual(a,b);assert.equal(a.split('\n').slice(4).join('\n'),b.split('\n').slice(4).join('\n'));
});
test('valid fixture starts with all 84 entries uninspected and validation does not mutate it',()=>{
  const packet=fixture(),before=structuredClone(packet);assert.equal(validatePacket(packet),packet);assert.deepEqual(packet,before);
});
test('initial acceptance or old human response is refused',()=>{
  for(const mutate of [p=>p.human_accepted=true,p=>p.slots[0].human_accepted=true,p=>p.slots[0].entries[0].human_status='agree with mapping',p=>p.slots[0].entries[0].human_response={}]){const p=fixture();mutate(p);assert.throws(()=>validatePacket(p));}
});
test('all ordered slots entries and twelve strips are required',()=>{
  for(const mutate of [p=>p.slots.pop(),p=>p.slots.reverse(),p=>p.slots[0].entries.reverse(),p=>delete p.assets.Im11,p=>p.assets.Im0.url='https://example.test/source',p=>p.assets.Im0.width=true]){const p=fixture();mutate(p);assert.throws(()=>validatePacket(p));}
});
test('synthetic response stays explicitly test-only and cannot prefill actual entries',()=>{
  const packet=fixture(),responses={'TEST-ONLY-spring':{status:'correction',readers:'primary',notes:'SYNTHETIC TEST ONLY'}};
  const out=formatResponses(packet.slots,responses,identity);assert(!out.includes('SYNTHETIC TEST ONLY'));assert.equal(out.split('\n').filter(s=>s.includes('\tuninspected\t')).length,84);
});
test('HTML exposes visible identity and full native strip access without persistence',async()=>{
  const {readFile}=await import('node:fs/promises');
  const html=await readFile(new URL('./review.html',import.meta.url),'utf8'),js=await readFile(new URL('./review.mjs',import.meta.url),'utf8');
  assert(html.includes('id="packet-identity"'));assert(html.includes('id="all-native-strips"'));
  assert(html.includes('earlier response does not transfer'));assert(html.includes('src="/page.png"'));
  for(const forbidden of ['localStorage','sessionStorage','indexedDB','sendBeacon','fetch('])assert(!js.includes(forbidden));
  assert(js.includes('identityHeader(packet)'));assert(js.includes('formatResponses([synthetic],testResponses,packet)'));
});
