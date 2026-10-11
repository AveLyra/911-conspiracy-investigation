// Separate packet checks; no builder imports, image decoding, or annotations.
// Optional numeric port checks the already-running IPv4 loopback server only.
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const base = path.dirname(fileURLToPath(import.meta.url));
const sha = b => createHash('sha256').update(b).digest('hex');
const raw = await fs.readFile(path.join(base, 'packet01/manifest.json'));
const manifestHash = '1c6b76f665ae63f43a722139317ba5890a9f1c7e25511f094a6f6fa4184e4bb6';
assert.equal(sha(raw), manifestHash);
const manifest = JSON.parse(raw);
const one = (await fs.readdir(path.join(base, 'packet01'))).sort();
assert.deepEqual(one, (await fs.readdir(path.join(base, 'packet02'))).sort());
assert.equal(one.length, 6);
for (const name of one) {
  const a = await fs.readFile(path.join(base, 'packet01', name));
  assert.ok(a.equals(await fs.readFile(path.join(base, 'packet02', name))), name);
  if (name !== 'manifest.json') {
    assert.equal(sha(a), manifest.products[name].sha256);
    assert.equal(a.length, manifest.products[name].bytes);
  }
}
assert.equal(Object.keys(manifest.prior_input_pins_unchanged).length, 660);
for (const [p, pin] of Object.entries(manifest.prior_input_pins_unchanged)) {
  const bytes = await fs.readFile(p);
  assert.equal(bytes.length, pin.bytes, p); assert.equal(sha(bytes), pin.sha256, p);
  if ((await fs.lstat(p)).isSymbolicLink()) {
    assert.equal(p, '/opt/homebrew/bin/ffmpeg');
    assert.equal(await fs.realpath(p), '/opt/homebrew/Cellar/ffmpeg/7.1.1_3/bin/ffmpeg');
  }
}
for (const [p, pin] of Object.entries(manifest.packet_input_pins_unchanged)) {
  const bytes = await fs.readFile(p);
  assert.equal(bytes.length, pin.bytes); assert.equal(sha(bytes), pin.sha256);
  assert.equal((await fs.lstat(p)).isSymbolicLink(), false);
}
const order = [274, 300, 342, 365, 388, 411];
const generated = await import(pathToFileURL(path.join(base, 'packet01/assets.mjs')));
assert.deepEqual(generated.FRAME_ORDER, order);
assert.deepEqual(generated.ASSETS, manifest.assets);
assert.equal(generated.SOURCE_HASH, manifest.source_sha256);
assert.equal(generated.PROTOCOL_HASH, manifest.protocol_sha256);
const frames = JSON.parse(await fs.readFile(path.join(base, '../continuity-274-411/run01/frames.json')));
const core = await fs.readFile(path.join(base, '../../comparator-r1-replication/coordinate.js'));
assert.ok((await fs.readFile(path.join(base, 'packet01/coordinate-core.mjs'))).equals(core.subarray(0, 2524)));
const routes = ['/', '/review.mjs', '/response.mjs', '/coordinate-core.mjs', '/assets.mjs',
  '/control.png', ...order.map(n => `/frames/${n}.png`)];
assert.deepEqual(Object.keys(manifest.routes).sort(), routes.sort());
for (const name of ['review.html', 'review.mjs', 'response.mjs']) {
  assert.ok((await fs.readFile(path.join(base, name))).equals(await fs.readFile(path.join(base, 'packet01', name))));
}
const clocks = [];
for (const ordinal of order) {
  const asset = generated.ASSETS[String(ordinal)], row = frames.find(r => r.index === ordinal);
  for (const key of ['stored_pts', 'best_effort_timestamp', 'stored_pts_seconds_exact', 'best_effort_seconds_exact'])
    assert.equal(asset[key], row[key]);
  const bytes = await fs.readFile(manifest.routes[asset.url].path);
  assert.equal(sha(bytes), row.native.sha256);
  assert.equal(bytes.readUInt32BE(16), 704); assert.equal(bytes.readUInt32BE(20), 480);
  assert.equal(bytes[25], 0); assert.equal(asset.mode, 'L'); assert.equal(asset.synthetic, false);
  clocks.push({ ordinal, stored_pts: asset.stored_pts, best_effort: asset.best_effort_timestamp });
}
const control = await fs.readFile(manifest.routes['/control.png'].path);
assert.equal(control[25], 2); assert.equal(control.readUInt32BE(16), 1280);
assert.equal(control.readUInt32BE(20), 720); assert.equal(sha(control), manifest.assets.control.sha256);
const result = { status: 'pass', method: 'Separate Node checks; no builder imports, image decode or historical coordinates',
  repeated_files: one, prior_pins: 660, packet_pins: Object.keys(manifest.packet_input_pins_unchanged).length,
  routes: 12, clocks, manifest_sha256: manifestHash, http: null };

if (process.argv.length > 2) {
  assert.equal(process.argv.length, 3);
  assert.match(process.argv[2], /^[0-9]+$/);
  const port = Number(process.argv[2]); assert.ok(port >= 1 && port <= 65535);
  const request = (requestPath, method = 'GET', headers = {}) => new Promise((resolve, reject) => {
    const r = http.request({ hostname: '127.0.0.1', port, path: requestPath, method, headers }, s => {
      const parts = []; s.on('data', b => parts.push(b));
      s.on('end', () => resolve({ status: s.statusCode, headers: s.headers, bytes: Buffer.concat(parts) }));
    });
    r.on('error', reject); r.setTimeout(5000, () => r.destroy(new Error('Loopback request timeout'))); r.end();
  });
  for (const [route, pin] of Object.entries(manifest.routes)) {
    const r = await request(route); assert.equal(r.status, 200, route);
    assert.equal(r.bytes.length, pin.bytes); assert.equal(sha(r.bytes), pin.sha256);
    assert.ok(r.headers['content-security-policy']);
  }
  const checks = [];
  // Expected codes come from the unchanged handler and its existing tests.
  for (const [requestPath, method, headers, expected] of [
    ['/manifest.json', 'GET', {}, 404], ['/PROTOCOL.md', 'GET', {}, 404],
    ['/', 'POST', {}, 501], ['/', 'GET', { Host: 'invalid.test' }, 403],
    ['/', 'GET', { Origin: 'http://invalid.test' }, 403], ['/', 'HEAD', {}, 200],
  ]) {
    const r = await request(requestPath, method, headers);
    assert.equal(r.status, expected); assert.ok(r.headers['content-security-policy']);
    if (method === 'HEAD') assert.equal(r.bytes.length, 0);
    checks.push({ path: requestPath, method, headers, status: r.status, body_bytes: r.bytes.length });
  }
  result.http = { port, allowed_routes_hashed: 12, checks };
}
console.log(JSON.stringify(result, null, 2));
