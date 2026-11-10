// Independent chain-rule implementation of the published rounded curve.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
const [input, output] = process.argv.slice(2);
assert(input && output, 'Usage: node check_printed_fit.mjs INPUT OUTPUT');
const raw = fs.readFileSync(input);
const original = JSON.parse(raw);
const rows = [];
for (const r of original.rows) {
  const t = r.t_s;
  const u = (0.18562 * t) ** 3.5126;
  const du = t === 0 ? 0 : 3.5126 * u / t;
  const ddu = t === 0 ? 0 : 3.5126 * (3.5126-1) * u / (t*t);
  const z = 379.62 * (1-Math.exp(-u));
  const v = 379.62 * Math.exp(-u) * du;
  const a = 379.62 * Math.exp(-u) * (ddu-du*du);
  const errors = [Math.abs(z-r.z_fit_ft), Math.abs(v-r.v_derivative_ft_s),
                  Math.abs(a-r.a_derivative_ft_s2)];
  assert(errors.every(x => Number.isFinite(x) && x < 1e-10));
  rows.push({t_s:t,z_ft:z,v_ft_s:v,a_ft_s2:a,absolute_errors:errors});
}
assert.equal(rows.length, 11);
const result = {
  status:'independent_chain_rule_arithmetic_pass',
  input_sha256:crypto.createHash('sha256').update(raw).digest('hex'),
  script_sha256:crypto.createHash('sha256').update(fs.readFileSync(new URL(import.meta.url))).digest('hex'),
  runtime:process.version,
  absolute_tolerance:1e-10,
  rows,
  limit:'Agreement of two finite arithmetic implementations, not raw-data or historical validation.'
};
fs.writeFileSync(output, JSON.stringify(result,null,2)+'\n', {flag:'wx'});
