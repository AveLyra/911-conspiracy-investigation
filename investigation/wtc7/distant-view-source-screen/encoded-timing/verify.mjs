// Independent raw-record arithmetic checker. Does not import audit.py.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const json=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const eq=(a,b)=>assert.deepEqual(a,b);
const OLD={frames:['stream_index','best_effort_timestamp','pts','duration','pkt_duration','width','height','pix_fmt','key_frame','pict_type'],
  streams:['index','codec_name','codec_type','width','height','pix_fmt','sample_aspect_ratio','display_aspect_ratio','r_frame_rate','avg_frame_rate','time_base','start_pts','start_time','duration_ts','duration','nb_frames','side_data_list']};
const IDENTITY={streams:OLD.streams,frames:['stream_index','key_frame','pict_type','width','height','pix_fmt','duration','pkt_duration','pkt_pos'],packets:['stream_index','duration','pos','size','flags','data_hash']};
const safe=n=>{assert(Number.isSafeInteger(n),'unsafe exact arithmetic');return n;};
function number(v){
  if(v===undefined || v===null || v==='N/A')return null;
  assert(typeof v==='number' || (typeof v==='string' && /^-?\d+$/.test(v)));
  const n=Number(v); assert(Number.isSafeInteger(n)); return n;
}
function split(d){
  if(d.packets_and_frames){
    assert(!d.packets && !d.frames);
    assert(d.packets_and_frames.every(r=>['packet','frame'].includes(r.type)));
    return {frames:d.packets_and_frames.filter(r=>r.type==='frame'),packets:d.packets_and_frames.filter(r=>r.type==='packet'),streams:d.streams};
  }
  return {frames:d.frames??[],packets:d.packets??[],streams:d.streams??[]};
}
function fraction(a,b){
  safe(a);safe(b);assert(b!==0); if(b<0){a=-a;b=-b;}
  let x=Math.abs(a),y=b;while(y){[x,y]=[y,x%y];}
  a/=x;b/=x;return b===1?String(a):`${a}/${b}`;
}
function pairs(rows,key,offset=0,tick=[1,1]){
  tick.forEach(n=>{safe(n);assert(n>0);});
  const known=rows.flatMap((r,i)=>number(r[key])===null?[]:[[offset+i,number(r[key])]]);
  return known.slice(1).map(([j,y],n)=>{
    const [i,x]=known[n],delta=safe(y-x);return {from_ordinal:i,to_ordinal:j,ordinal_gap:j-i,
      from_value:x,to_value:y,delta,delta_seconds_exact:fraction(safe(delta*tick[0]),tick[1]),delta_per_ordinal_exact:fraction(delta,j-i)};
  });
}
function tabs(rows){
  const out={};for(const r of rows){const type=r.pict_type??'<missing>';
    const a=out[type]??={count:0,pts_present:0,pts_missing:0,best_effort_present:0,best_effort_missing:0};
    a.count++;a[number(r.pts)===null?'pts_missing':'pts_present']++;
    a[number(r.best_effort_timestamp)===null?'best_effort_missing':'best_effort_present']++;
  }return out;
}
function differences(left,right,section,fields){
  const changes=[];
  for(let i=0;i<Math.max(left.length,right.length);i++){
    const a=left[i]??{},b=right[i]??{};
    if(i>=left.length||i>=right.length)changes.push({section,ordinal:i,field:'__record__',left_present:i<left.length,left_value:null,right_present:i<right.length,right_value:null});
    const keys=fields??[...new Set([...Object.keys(a),...Object.keys(b)])].sort();
    for(const field of keys){const lp=Object.hasOwn(a,field),rp=Object.hasOwn(b,field);
      if(lp!==rp || JSON.stringify(a[field])!==JSON.stringify(b[field]))changes.push({section,ordinal:i,field,left_present:lp,left_value:lp?a[field]:null,right_present:rp,right_value:rp?b[field]:null});
    }
  }return changes;
}
function selftest(){
  eq(number(0),0);eq(number(undefined),null);assert.throws(()=>number(true));assert.throws(()=>number('1.2'));
  eq(pairs([{pts:0},{},{pts:2},{pts:1}],'pts').map(p=>[p.ordinal_gap,p.delta,p.delta_per_ordinal_exact]),[[2,2,'1'],[1,-1,'-1']]);
  eq(pairs([{pts:0},{pts:0}],'pts')[0].delta_seconds_exact,'0');
  eq(fraction(-2,6),'-1/3');eq(fraction(4,2),'2');
  eq(tabs([{pict_type:'I'},{pict_type:'B',pts:0,best_effort_timestamp:0}]).B.pts_present,1);
  eq(differences([{}],[{pts:null}],'frames')[0].left_present,false);
  eq(differences([{pts:0,width:4}],[{pts:1,width:8}],'frames',OLD.frames).map(d=>d.field).sort(),['pts','width']);
  assert.throws(()=>pairs([{pts:-9007199254740991},{pts:9007199254740990}],'pts'));
  assert.throws(()=>pairs([{pts:0},{pts:9007199254740991}],'pts',0,[2,1]));
  assert.throws(()=>pairs([{pts:0},{pts:1}],'pts',0,[0,1]));
  assert.throws(()=>split({packets_and_frames:[{type:'alien'}]}));
  eq(split({packets_and_frames:[{type:'packet'},{type:'frame'}]}).frames.length,1);
  console.log('Independent primitive controls passed (16 assertions/groups).');
}
if(process.argv.includes('--self-test')){selftest();process.exit(0);}
const name=process.argv[2];assert(/^run\d+$/.test(name??''));
const run=path.join(here,name), result=json(path.join(run,'analysis.json'));
eq(Object.keys(result.arms).sort(),['default','genpts']);
eq(result.baseline_comparisons.length,2);
const source=fs.readFileSync(path.join(here,'../source/DistantViewWTC7.avi'));
eq(hash(source),'a082b44ebad53fbb32b5ca7f2672944b27c91e28d5c309960b996b5886c9224e');
const raw={};const independent={};
for(const arm of ['default','genpts']){
  const d=split(json(path.join(run,arm,'stdout.json')));raw[arm]=d;
  const out=result.arms[arm];
  eq(out.streams,d.streams);
  eq(out.frames,d.frames.map((record,ordinal)=>({ordinal,record})));
  eq(out.packets,d.packets.map((record,ordinal)=>({ordinal,record})));
  const tick=d.streams[0].time_base.split('/').map(Number);
  for(const [scope,start,end] of [['all',0,d.frames.length],['selected_274_411',274,412]]){
    const rows=d.frames.slice(start,end),s=out.frame_summaries[scope];
    eq(s.count,rows.length);
    eq(s.picture_type_tabs,tabs(rows));
    for(const key of ['pts','pkt_dts','best_effort_timestamp']){
      const t=s.timestamps[key],p=pairs(rows,key,start,tick);
      eq(t.missing_ordinals,rows.flatMap((r,i)=>number(r[key])===null?[start+i]:[]));
      eq(t.pairs,p);eq(t.adjacent_pairs,p.filter(v=>v.ordinal_gap===1));eq(t.gap_pairs,p.filter(v=>v.ordinal_gap>1));
    }
  }
  const groups=new Map();d.packets.forEach((r,i)=>{const pos=number(r.pos);if(pos!==null&&pos>=0){if(!groups.has(pos))groups.set(pos,[]);groups.get(pos).push(i);}});
  eq(out.joins.length,d.frames.length);
  for(let i=0;i<d.frames.length;i++){
    const pos=number(d.frames[i].pkt_pos),matches=pos===null?[]:(groups.get(pos)??[]),j=out.joins[i];
    eq(j.frame_ordinal,i);eq(j.position,pos);eq(j.packet_ordinals,matches);eq(j.disposition,matches.length===1?'unique':matches.length===0?'zero':'multiple');
  }
  eq(out.payload_checks.length,d.packets.length);
  for(let i=0;i<d.packets.length;i++){
    const r=d.packets[i],p=number(r.pos),n=number(r.size),valid=p!==null&&n!==null&&p>=0&&n>=0&&p+n<=source.length;
    const sha=valid?hash(source.subarray(p,p+n)):null,c=out.payload_checks[i];
    eq(c.packet_ordinal,i);eq(c.position,p);eq(c.size,n);eq(c.computed_sha256,sha);
    eq(c.hash_matches,valid&&typeof r.data_hash==='string'&&/^SHA256:[a-fA-F0-9]{64}$/.test(r.data_hash)?r.data_hash.toLowerCase()===`sha256:${sha}`:null);
  }
  eq(out.packet_summary.count,d.packets.length);
  eq(out.packet_summary.dts.pairs,pairs(d.packets,'dts',0,tick));
  eq(out.packet_summary.null_counts,Object.fromEntries(['stream_index','pts','dts','duration','pos','size','flags','data_hash'].map(k=>[k,d.packets.filter(r=>r[k]===null||r[k]===undefined).length])));
  eq(out.packet_summary.position_groups,[...groups].sort((a,b)=>a[0]-b[0]).map(([position,packet_ordinals])=>({position,packet_ordinals})));
  eq(out.packet_summary.known_nonnegative_positions_unique,[...groups.values()].every(ids=>ids.length===1));
  independent[arm]={frame_count:d.frames.length,packet_count:d.packets.length,tabs:tabs(d.frames),selected_tabs:tabs(d.frames.slice(274,412)),
    null_packet_pts:d.packets.filter(r=>number(r.pts)===null).length,null_packet_dts:d.packets.filter(r=>number(r.dts)===null).length,
    unique_positions:groups.size,join_counts:Object.fromEntries(['zero','unique','multiple'].map(k=>[k,out.joins.filter(r=>r.disposition===k).length])),
    payload_matching:out.payload_checks.filter(r=>r.hash_matches===true).length,
    frame_pts_offsets:[...new Set(d.frames.flatMap((r,i)=>number(r.pts)===null?[]:[number(r.pts)-i]))],
    frame_best_effort_offsets:[...new Set(d.frames.flatMap((r,i)=>number(r.best_effort_timestamp)===null?[]:[number(r.best_effort_timestamp)-i]))]};
}
const changes=['streams','frames','packets'].flatMap(k=>differences(raw.default[k],raw.genpts[k],k));
const sortDiff=a=>a.toSorted((x,y)=>x.section.localeCompare(y.section)||x.ordinal-y.ordinal||x.field.localeCompare(y.field));
eq(sortDiff(result.arm_differences.all),sortDiff(changes));
for(const k of Object.keys(IDENTITY))eq([...result.arm_differences.identity_fields[k]].sort(),[...IDENTITY[k]].sort());
eq(sortDiff(result.arm_differences.identity),sortDiff(changes.filter(r=>r.field==='__record__'||IDENTITY[r.section].includes(r.field))));
for(const [i,b] of result.baseline_comparisons.entries()){
  eq(path.resolve(here,b.baseline_path),path.resolve(here,`../probe0${i+2}-diagnostics/probe-stdout.json`));
  eq(hash(fs.readFileSync(path.resolve(here,b.baseline_path))),'c0c7ce905e0f3e96a4ce9fedbc8b4309d9c9a13c43d5f86afbe0d176e2e5ac84');
  const old=split(json(path.resolve(here,b.baseline_path)));
  for(const k of ['streams','frames'])eq([...b.compared_fields[k]].sort(),[...OLD[k]].sort());
  const ds=['streams','frames'].flatMap(k=>differences(old[k],raw.default[k],k,OLD[k]));
  eq(sortDiff(b.differences),sortDiff(ds));
}
const receipt={checker_sha256:hash(fs.readFileSync(fileURLToPath(import.meta.url))),run:name,status:'pass',
  raw_hashes:Object.fromEntries(['default','genpts'].map(k=>[k,hash(fs.readFileSync(path.join(run,k,'stdout.json')))])),
  independent,changes_by_field:changes.reduce((a,c)=>(a[`${c.section}.${c.field}`]=(a[`${c.section}.${c.field}`]??0)+1,a),{}),
  limitations:'Checks raw FFprobe records and arithmetic, not an independent decoder, camera clock, pixel identity or physical trajectory.'};
const output=path.join(here,`${name}-independent.json`);
fs.writeFileSync(output,JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify(receipt,null,2));
