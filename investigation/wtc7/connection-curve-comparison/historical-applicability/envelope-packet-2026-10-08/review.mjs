// UI only. Floating-point display never replaces the packet's exact fractions.
// pointerToPixel / nudgePixel follow the already tested parent coordinate.mjs contract.
export function number(value){
  if(typeof value==='number'&&Number.isFinite(value))return value;
  if(typeof value!=='string'||!/^[-+]?\d+(?:\/\d+)?$/.test(value))throw Error('Invalid exact coordinate');
  const [a,b='1']=value.split('/').map(Number);const result=a/b;
  if(!Number.isFinite(result))throw Error('Invalid coordinate denominator');return result;
}
export function pointerToPixel(x,y,r,w,h){
  if(![x,y,r.left,r.top,r.width,r.height].every(Number.isFinite)||r.width<=0||r.height<=0||!Number.isSafeInteger(w)||!Number.isSafeInteger(h)||w<=0||h<=0||x<r.left||y<r.top||x>=r.left+r.width||y>=r.top+r.height)return null;
  return{x:Math.min(w-1,Math.floor((x-r.left)/r.width*w)),y:Math.min(h-1,Math.floor((y-r.top)/r.height*h))};
}
export function nudgePixel(p,key,w,h){
  const moves={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]};
  if(!p||!Number.isInteger(p.x)||!Number.isInteger(p.y)||p.x<0||p.y<0||p.x>=w||p.y>=h||!Object.hasOwn(moves,key))return null;
  return{x:Math.max(0,Math.min(w-1,p.x+moves[key][0])),y:Math.max(0,Math.min(h-1,p.y+moves[key][1]))};
}
const clean=value=>String(value??'').replace(/[\t\r\n]+/g,' ').trim();
export function describePair(pair){
  if(!/^[FE][3-9]$/.test(pair))return 'Synthetic control only.';
  const colors={3:'black',4:'gold',5:'blue',6:'red',7:'green',8:'cyan',9:'purple'};
  return `${pair[0]==='F'?'Force':'Dissipated-energy'} panel; ${pair[1]}-bolt pair; ${colors[pair[1]]} trace. Solid = spring; dashed = shell.`;
}
export function describeScenarios(states){
  return Object.entries(states).map(([key,value])=>{const [spring,shell]=key.split('-');return `Spring ${spring} / shell ${shell}: ${value.status}`;}).join('; ');
}
export function formatResponses(slots,responses,hash){
  const rows=[`Conditional packet SHA256\t${hash}`,'Entry\tProposal status\tHuman status\tInspected proposals\tNotes/corrected native range'];
  for(const slot of slots)for(const entry of slot.entries){
    const r=responses[entry.id];
    rows.push([entry.id,slot.selection_status,r?.status??'uninspected',r?.readers??'',r?.notes??''].map(clean).join('\t'));
  }
  return rows.join('\n');
}

export function initialize(packet){
  const el=id=>document.getElementById(id),make=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
  const responses=Object.create(null),testResponses=Object.create(null);let generation=0;
  const synthetic={id:'TEST-ONLY',pair:'synthetic',page_x:'320',selection_status:'synthetic_control_not_evidence',duplicate_paired_slots:[],scenario_states:{},entries:[{id:'TEST-ONLY-spring',model:'synthetic spring',reason:'Synthetic coordinate/control check only.',mappings:{primary:[{source:'control',role:'primary',native_rectangle:[315,175,326,186],native_x:'320',render_rectangle:[315,175,326,186],asset_url:'/control.png'}],peer:[]},duplicate_entries:{primary:[],peer:[]}}]};
  const slots=[synthetic,...packet.slots],selector=el('slot');selector.replaceChildren();
  for(const slot of slots){const option=make('option',slot.id+' — '+slot.selection_status);option.value=slot.id;selector.append(option);}
  const selected=()=>slots.find(s=>s.id===selector.value),store=()=>selector.value==='TEST-ONLY'?testResponses:responses;
  const asset=name=>name==='control'?{width:1280,height:720,url:'/control.png'}:packet.assets[name];
  function updateOutput(){
    const actual=formatResponses(packet.slots,responses,packet.packet_sha256);
    const test=Object.keys(testResponses).length?'\n\nSYNTHETIC UI TEST — NOT HUMAN EVIDENCE\n'+formatResponses([synthetic],testResponses,'synthetic'):'';
    el('review-output').value=actual+test;
    el('copy-status').textContent='';
  }
  function makeBox(parent,rect,w,h,className='box'){
    const box=make('span');box.className=className;
    const r=rect.map(number);Object.assign(box.style,{left:100*r[0]/w+'%',top:100*r[1]/h+'%',width:100*(r[2]-r[0])/w+'%',height:100*(r[3]-r[1])/h+'%'});parent.append(box);
  }
  function imageView(mapping,role,token){
    const a=asset(mapping.source),holder=make('div');holder.className='native-view';
    holder.append(make('h3',`${role}: ${mapping.source} — native strip coordinates`));
    const meta=make('p',`Proposed edges [${mapping.native_rectangle.join(', ')}]; target native x = ${mapping.native_x}. ${mapping.boundary_touch?'Boundary touch.':''} ${mapping.fragment_id?'Fragment: '+mapping.fragment_id+'.':''}`);meta.className='small metadata';holder.append(meta);
    const viewport=make('div');viewport.className='viewport';viewport.tabIndex=0;viewport.setAttribute('aria-label',`${role} ${mapping.source} native image`);
    const stage=make('div');stage.className='stage';const image=make('img');image.alt=`Unchanged native ${mapping.source}, ${role} proposal`;image.draggable=false;
    const zoom=Number(el('zoom').value);stage.style.width=a.width*zoom+'px';image.style.width=a.width*zoom+'px';image.style.height=a.height*zoom+'px';
    const overlay=make('div');overlay.className='overlay';overlay.hidden=!el('overlays').checked;makeBox(overlay,mapping.native_rectangle,a.width,a.height);
    const line=make('span');line.className='target';line.style.left=100*number(mapping.native_x)/a.width+'%';overlay.append(line);
    const marker=make('span');marker.className='point';marker.hidden=true;stage.append(image,overlay,marker);viewport.append(stage);holder.append(viewport);
    const readout=make('p','Loading source; coordinates disabled.');readout.className='small coordinate-readout';holder.append(readout);let ready=false,locked=null;
    const show=(point,kind)=>{if(!ready||!point)return;marker.hidden=false;marker.style.left=100*(point.x+.5)/a.width+'%';marker.style.top=100*(point.y+.5)/a.height+'%';readout.textContent=`${kind} — ${mapping.source} native pixel x: ${point.x}, y: ${point.y}; not an accepted response.`;};
    const eventPoint=e=>ready?pointerToPixel(e.clientX,e.clientY,image.getBoundingClientRect(),a.width,a.height):null;
    stage.addEventListener('pointermove',e=>{if(!locked)show(eventPoint(e),'HOVER');});
    stage.addEventListener('click',e=>{const point=eventPoint(e);if(point){locked=point;show(point,'LOCKED');viewport.focus({preventScroll:true});}});
    viewport.addEventListener('keydown',e=>{if(e.key==='Escape'){locked=null;marker.hidden=true;readout.textContent='Point cleared; no human response changed.';return;}const next=nudgePixel(locked,e.key,a.width,a.height);if(next){e.preventDefault();locked=next;show(next,'KEYBOARD');}});
    image.onload=()=>{if(token!==generation)return;if(image.naturalWidth!==a.width||image.naturalHeight!==a.height){readout.textContent='Rejected: source dimensions differ.';readout.classList.add('error');return;}ready=true;readout.textContent=`Loaded ${a.width} × ${a.height}. Hover/click, then arrows; Escape clears. Coordinates do not fill your response.`;viewport.scrollLeft=(number(mapping.native_x)+.5)*zoom-viewport.clientWidth/2;viewport.scrollTop=((mapping.native_rectangle[1]+mapping.native_rectangle[3])/2)*zoom-viewport.clientHeight/2;};
    image.onerror=()=>{ready=false;readout.textContent='Source unavailable; coordinates disabled.';readout.classList.add('error');};image.src=a.url;
    return holder;
  }
  function render(){
    const token=++generation,slot=selected();el('entries').replaceChildren();el('full-overlay').replaceChildren();
    el('full-overlay').hidden=!el('overlays').checked||slot.id==='TEST-ONLY';
    const index=slots.indexOf(slot);el('previous').disabled=index===0;el('next').disabled=index===slots.length-1;
    el('slot-status').textContent=`${slot.id}: ${slot.selection_status}. ${describePair(slot.pair)} ${slot.page_x===null?'No primary paired coverage; do not invent coordinates.':`Exact page x: ${slot.page_x}.`}${slot.duplicate_paired_slots.length?' Duplicate paired footprints: '+slot.duplicate_paired_slots.join(', ')+'.':''}${slot.selection_status==='boundary_unresolved'?' Locator review cannot resolve the excluded boundary.':''}`;
    el('scenario-status').textContent=describeScenarios(slot.scenario_states);
    for(const entry of slot.entries){
      const section=make('section');section.className='entry';section.append(make('h2',entry.id+' — '+entry.model));section.append(make('p',entry.reason));
      const views=make('div');views.className='views';
      for(const role of ['primary','peer']){
        const maps=entry.mappings[role];
        if(!maps.length)views.append(make('p',role+': no eligible mapping at this source position.'));
        for(const m of maps){views.append(imageView(m,role,token));if(slot.id!=='TEST-ONLY')makeBox(el('full-overlay'),m.render_rectangle,1700,2200);}
        if(entry.duplicate_entries[role]?.length)section.append(make('p',`${role} footprint also appears in: ${entry.duplicate_entries[role].join(', ')}`));
      }
      section.append(views);
      const answer=store()[entry.id]??{status:'uninspected',readers:'',notes:''};
      const stateLabel=make('label','Human status '),state=make('select');state.setAttribute('aria-label',entry.id+' human status');
      for(const status of ['uninspected','agree with mapping','correction','unreadable','unresolved']){const o=make('option',status);o.value=status;state.append(o);}state.value=answer.status;stateLabel.append(state);
      const scopeLabel=make('label',' Inspected proposals '),scope=make('select');scope.setAttribute('aria-label',entry.id+' inspected proposals');
      for(const value of ['','primary','peer','both']){const o=make('option',value||'not specified');o.value=value;scope.append(o);}scope.value=answer.readers;scopeLabel.append(scope);
      const notes=make('textarea');notes.setAttribute('aria-label',entry.id+' notes');notes.placeholder='Cue inspected; corrections as source name + native x/y range. Agreement is optional.';notes.value=answer.notes;
      const save=()=>{store()[entry.id]={status:state.value,readers:scope.value,notes:notes.value};updateOutput();};state.addEventListener('change',save);scope.addEventListener('change',save);notes.addEventListener('input',save);
      section.append(stateLabel,scopeLabel,notes);el('entries').append(section);
    }
    updateOutput();
  }
  selector.addEventListener('change',render);el('zoom').addEventListener('change',render);el('overlays').addEventListener('change',render);
  el('previous').addEventListener('click',()=>{selector.selectedIndex--;render();});el('next').addEventListener('click',()=>{selector.selectedIndex++;render();});
  el('copy').addEventListener('click',async()=>{updateOutput();try{await navigator.clipboard.writeText(el('review-output').value);el('copy-status').textContent='Copied. Paste your inspection record into chat.';}catch{el('review-output').focus();el('review-output').select();el('copy-status').textContent='Copy the selected table manually, then paste into chat.';}});
  el('clear-test').addEventListener('click',()=>{for(const key of Object.keys(testResponses))delete testResponses[key];render();});
  el('provenance').textContent=`Packet SHA256: ${packet.packet_sha256}. ${JSON.stringify(packet.summary)}. Assumptions unvalidated: ${packet.assumptions.join(', ')}.`;
  el('load-status').textContent='Fixed packet loaded: 42 paired slots, 84 intended entries. Synthetic control is not evidence.';render();
}
if(typeof document!=='undefined'){
  import('/viewer-data.mjs').then(({PACKET})=>initialize(PACKET)).catch(()=>{document.getElementById('load-status').textContent='Packet unavailable; review disabled.';});
}
