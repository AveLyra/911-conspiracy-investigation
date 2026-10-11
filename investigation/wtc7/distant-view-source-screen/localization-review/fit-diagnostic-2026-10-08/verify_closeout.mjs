// Read-only, independent byte and live-HTTP checks. No producer imports.
import assert from 'node:assert/strict';
import {readFileSync, readdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import http from 'node:http';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.argv[2]);
assert(Number.isInteger(port) && port > 0 && port <= 65535, 'explicit live port required');
const read = p => readFileSync(p);
const sha = b => createHash('sha256').update(b).digest('hex');
const m = JSON.parse(read(path.join(here, 'packet03/manifest.json')));
const expected = ['/', '/assets.mjs', '/control.png', '/coordinate-core.mjs', '/diagnostics.mjs', '/response.mjs', '/review.mjs'];
assert.deepEqual(Object.keys(m.routes).sort(), expected);
assert.equal(m.historical_measurement, false);
assert.equal(m.human_acceptance, false);
let inputCount = 0;
for (const [p, pin] of Object.entries(m.inputs)) {
  const b = read(p); assert.equal(b.length, pin.bytes); assert.equal(sha(b), pin.sha256); inputCount++;
}
const names = [...Object.keys(m.products), 'manifest.json'].sort();
for (const packet of ['packet03', 'packet04']) {
  assert.deepEqual(readdirSync(path.join(here, packet)).sort(), names);
  for (const name of names) {
    const b = read(path.join(here, packet, name));
    assert.deepEqual(b, read(path.join(here, 'packet03', name)));
    if (name !== 'manifest.json') {
      assert.equal(b.length, m.products[name].bytes); assert.equal(sha(b), m.products[name].sha256);
    }
  }
}
const original = path.join(here, '../packet02');
for (const name of ['review.mjs', 'response.mjs', 'coordinate-core.mjs', 'assets.mjs']) {
  assert.deepEqual(read(path.join(here, 'packet03', name)), read(path.join(original, name)));
}
const tag = '  <script type="module" src="./diagnostics.mjs"></script>\n';
const html = read(path.join(here, 'packet03/review.html')).toString();
assert.equal(html.split(tag).length, 2);
assert.equal(html.replace(tag, ''), read(path.join(original, 'review.html')).toString());
const csp = "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'none'; frame-ancestors 'none'; form-action 'none'; base-uri 'none'";
const rows = [];
function request(url, method = 'GET', headers = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request({hostname:'127.0.0.1', port, path:url, method, headers}, res => {
      const chunks = []; res.on('data', b => chunks.push(b));
      res.on('end', () => resolve({status:res.statusCode, headers:res.headers, body:Buffer.concat(chunks)}));
      res.on('error', reject);
    });
    req.setTimeout(5000, () => req.destroy(new Error('HTTP check timeout')));
    req.on('error', reject); req.end();
  });
}
function policy(r) {
  for (const [k,v] of Object.entries({'cache-control':'no-store','x-content-type-options':'nosniff','referrer-policy':'no-referrer','cross-origin-resource-policy':'same-origin','content-security-policy':csp})) assert.equal(r.headers[k],v);
}
for (const url of expected) {
  const r = await request(url); const pin = m.routes[url];
  assert.equal(r.status,200); policy(r); assert.equal(r.headers['content-type'],pin.mime);
  assert.equal(r.body.length,pin.bytes); assert.equal(sha(r.body),pin.sha256);
  assert.equal(Number(r.headers['content-length']),pin.bytes);
  rows.push({url,method:'GET',status:r.status,bytes:r.body.length,sha256:sha(r.body)});
}
for (const [url, method, headers, status] of [
  ['/frames/274.png','GET',{},404], ['/manifest.json','GET',{},404], ['/PROTOCOL.md','GET',{},404],
  ['/','POST',{},501], ['/','GET',{Host:'example.invalid'},403],
  ['/','GET',{Origin:'https://example.invalid'},403], ['/','HEAD',{},200]
]) {
  const r = await request(url,method,headers); assert.equal(r.status,status); policy(r);
  if (method === 'HEAD') { assert.equal(r.body.length,0); assert.equal(Number(r.headers['content-length']),m.routes['/'].bytes); }
  rows.push({url,method,headers,status:r.status,bytes:r.body.length});
}
console.log(JSON.stringify({status:'passed',scope:'Synthetic diagnostic byte/HTTP checks only',port,
  manifest_sha256:sha(read(path.join(here,'packet03/manifest.json'))),inputs_checked:inputCount,
  deterministic_files_per_packet:names.length,unchanged_original_modules:4,html_derivation:'One appended module tag only',http:rows},null,2));
