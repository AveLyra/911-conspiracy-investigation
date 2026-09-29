// Synthetic display geometry and minimal DOM lifecycle; no historical pixels read.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { pointerToPixel as map, pixelCenter, nudgePixel, ASSETS, CANDIDATES,
  initializeReview } from './coordinate.mjs';
const rect = (left, top, width, height) => ({left, top, width, height});

test('both dimensions: 100%, fractional cells, fit and 200%', () => {
  for (const [w,h] of [[1280,720],[1700,2200]]) {
    assert.deepEqual(map(10.75,20.99,rect(0,0,w,h),w,h),{x:10,y:20});
    assert.deepEqual(map(15.4,30.4,rect(10,20,w/2,h/2),w,h),{x:10,y:20});
    assert.deepEqual(map(31.9,63.9,rect(10,20,w*2,h*2),w,h),{x:10,y:21});
  }
});
test('fractional CSS offsets and negative scroll origins', () => {
  assert.deepEqual(map(21.375,31.125,rect(10.125,20.375,1275,1650),1700,2200),{x:15,y:14});
  assert.deepEqual(map(20.5,30.5,rect(-500,-200,1700,2200),1700,2200),{x:520,y:230});
});
test('upper-left included; right/bottom excluded; last cell retained', () => {
  for (const [w,h] of [[1280,720],[1700,2200]]) {
    const r=rect(10,20,w/2,h/2);
    assert.deepEqual(map(10,20,r,w,h),{x:0,y:0});
    assert.deepEqual(map(10+w/2-.001,20+h/2-.001,r,w,h),{x:w-1,y:h-1});
    for(const [x,y] of [[9.99,20],[10,19.99],[10+w/2,20],[10,20+h/2]]) assert.equal(map(x,y,r,w,h),null);
  }
});
test('invalid numeric dimensions, pointer values and rectangles rejected', () => {
  for(const bad of [0,-1,1.5,NaN,Infinity,true,'1700',undefined]) {
    assert.equal(map(1,1,rect(0,0,1700,2200),bad,2200),null);
    assert.equal(map(1,1,rect(0,0,1700,2200),1700,bad),null);
    assert.equal(pixelCenter({x:0,y:0},rect(0,0,1700,2200),bad,2200),null);
    assert.equal(nudgePixel({x:0,y:0},'ArrowRight',1700,bad),null);
  }
  for(const r of [null,{},rect(NaN,0,1,1),rect(0,0,0,1),rect(0,0,1,-1),rect(0,0,true,1),rect(Number.MAX_VALUE,0,Number.MAX_VALUE,1)]) assert.equal(map(0,0,r,1700,2200),null);
  for(const bad of [NaN,Infinity,true,'1',undefined]) assert.equal(map(bad,0,rect(0,0,1700,2200),1700,2200),null);
});
test('pixel-center convention and roundtrip across scales and scroll', () => {
  assert.deepEqual(pixelCenter({x:0,y:0},rect(0,0,1700,2200),1700,2200),{clientX:.5,clientY:.5});
  for(const [w,h] of [[1280,720],[1700,2200]]) for(const scale of [.25,.67,1,2]) {
    const r=rect(-1200.25,19.375,w*scale,h*scale);
    for(const p of [{x:0,y:0},{x:w-1,y:h-1},{x:449,y:224}]) {
      const c=pixelCenter(p,r,w,h); assert.deepEqual(map(c.clientX,c.clientY,r,w,h),p);
    }
  }
});
test('one-cell nudges, clamp, invalid keys and points', () => {
  const p={x:50,y:60};
  for(const [key,expected] of [['ArrowLeft',{x:49,y:60}],['ArrowRight',{x:51,y:60}],['ArrowUp',{x:50,y:59}],['ArrowDown',{x:50,y:61}]]) assert.deepEqual(nudgePixel(p,key,1700,2200),expected);
  assert.deepEqual(p,{x:50,y:60});
  assert.deepEqual(nudgePixel({x:0,y:0},'ArrowLeft',1700,2200),{x:0,y:0});
  assert.deepEqual(nudgePixel({x:1699,y:2199},'ArrowDown',1700,2200),{x:1699,y:2199});
  for(const p of [null,{}, {x:true,y:1},{x:1.5,y:0},{x:-1,y:0},{x:1700,y:0},{x:0,y:2200}]) assert.equal(nudgePixel(p,'ArrowRight',1700,2200),null);
  for(const key of ['Escape','toString','',null]) assert.equal(nudgePixel(p,key,1700,2200),null);
});
test('literal seven-asset scope and six valid candidate points', () => {
  assert.deepEqual(Object.keys(ASSETS).sort(),['117','73','74','75','76','77','control']);
  assert.equal(new Set(Object.values(ASSETS).map(x=>x.url)).size,7);
  assert.equal(Object.keys(CANDIDATES).length,6);
  for(const p of Object.values(CANDIDATES)) assert.deepEqual(map(p.x+.5,p.y+.5,rect(0,0,1700,2200),1700,2200),p);
});

// Deliberately small fake DOM: checks lifecycle, not browser layout or event quantization.
function fakeDOM() {
  class Element {
    constructor() { this.listeners={}; this.dataset={}; this.style={}; this.hidden=false; this.textContent=''; this.clientWidth=800; this.clientHeight=600; this.scrollLeft=0; this.scrollTop=0; }
    addEventListener(k,f) { this.listeners[k]=f; }
    fire(k,extra={}) { this.listeners[k]?.({preventDefault(){},...extra}); }
    setAttribute(k,v) { this[k]=v; }
    focus() {}
    scrollIntoView(options) { this.scrolledIntoView=options; }
    getBoundingClientRect() { return rect(0,0,1700,2200); }
    replaceWith(next) { nodes['page-image']=next; }
  }
  const nodes=Object.fromEntries(['viewport','stage','marker','page','readout','load-status','page-image','kind','dimensions','hash','source-hash','clear'].map(k=>[k,new Element()]));
  nodes.page.value='control';
  const zooms=['fit','1','2'].map(z=>Object.assign(new Element(),{dataset:{zoom:z}}));
  const candidates=Object.keys(CANDIDATES).map(k=>Object.assign(new Element(),{dataset:{candidate:k}}));
  const document=new Element(); document.getElementById=k=>nodes[k];
  document.querySelectorAll=s=>s==='[data-zoom]'?zooms:candidates;
  const images=[]; class Image extends Element { constructor(){super();images.push(this);} }
  globalThis.document=document; globalThis.Image=Image;
  globalThis.ResizeObserver=class { constructor(f){this.f=f;} observe(){} };
  initializeReview();
  return {nodes,images,candidates,zooms,document,load(w,h,img=images.at(-1)){img.naturalWidth=w;img.naturalHeight=h;img.onload();}};
}
test('load gating, stale callback, dimension error and network error stay unavailable', () => {
  const d=fakeDOM();
  try {
    assert.match(d.nodes.readout.textContent,/unavailable/);
    d.nodes.stage.fire('click',{clientX:10,clientY:20}); assert.equal(d.nodes.marker.hidden,true);
    const stale=d.images[0]; d.nodes.page.value='76'; d.nodes.page.fire('change');
    d.load(1280,720,stale); assert.match(d.nodes.readout.textContent,/unavailable/);
    d.load(1280,720); assert.match(d.nodes['load-status'].textContent,/Rejected/);
    assert.equal(d.nodes.marker.hidden,true);
    d.nodes.page.fire('change'); d.images.at(-1).onerror();
    assert.match(d.nodes['load-status'].textContent,/failed/); assert.match(d.nodes.readout.textContent,/unavailable/);
  } finally { delete globalThis.document; delete globalThis.Image; delete globalThis.ResizeObserver; }
});
test('candidate provenance, genuine click, nudge, clear, frame reset and variable load', () => {
  const d=fakeDOM();
  try {
    d.load(1280,720); assert.match(d.nodes['load-status'].textContent,/Loaded 1280 × 720/);
    d.candidates[0].fire('click'); assert.equal(d.nodes.page.value,'76');
    assert.match(d.nodes.readout.textContent,/unavailable/);
    d.load(1700,2200); assert.match(d.nodes.readout.textContent,/AI PROPOSED F0 ±3 px each axis — x: 449, y: 829/);
    assert.equal(d.nodes.stage.style.width,'1700px');
    assert.equal(d.nodes.viewport.scrollTop,829.5-300);
    assert.deepEqual(d.nodes.viewport.scrolledIntoView,{block:'center'});
    d.nodes.stage.fire('click',{clientX:10.5,clientY:20.5}); assert.match(d.nodes.readout.textContent,/CLICK LOCKED — x: 10, y: 20/);
    d.nodes.viewport.fire('keydown',{key:'ArrowRight'}); assert.match(d.nodes.readout.textContent,/KEYBOARD ADJUSTED — x: 11, y: 20/);
    d.zooms[2].fire('click'); assert.equal(d.nodes.stage.style.width,'3400px'); assert.match(d.nodes.readout.textContent,/x: 11, y: 20/);
    d.document.fire('keydown',{key:'Escape'}); assert.equal(d.nodes.marker.hidden,true);
    d.nodes.page.value='73'; d.nodes.page.fire('change'); assert.match(d.nodes.readout.textContent,/unavailable/);
    d.load(1700,2200); assert.match(d.nodes.readout.textContent,/No point/);
  } finally { delete globalThis.document; delete globalThis.Image; delete globalThis.ResizeObserver; }
});
