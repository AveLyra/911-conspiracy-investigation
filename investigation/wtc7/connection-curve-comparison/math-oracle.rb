# Independent fixed synthetic arithmetic oracle. No historical input, producer
# imports, image processing, or physical validation. Stdlib exact Rational.
require 'json'

def q(x)
  Rational(x)
end

# A segment is [left, right, slope, intercept], not a sampled ordinate array.
def exact_comparison(reference, candidate)
  length = signed = absolute = squared = ref_area = cand_area = q(0)
  maximum = q(0)
  reference.each do |r|
    candidate.each do |c|
      u = [r[0], c[0]].max
      v = [r[1], c[1]].min
      next unless v > u
      a, b = c[2]-r[2], c[3]-r[3]
      anti = ->(x) { a*x*x/2 + b*x }
      cuts = [u, v]
      zero = a == 0 ? nil : -b/a
      cuts << zero if zero && u < zero && zero < v
      cuts.sort.each_cons(2) { |lo, hi| absolute += (anti.call(hi)-anti.call(lo)).abs }
      signed += anti.call(v)-anti.call(u)
      squared += a*a*(v**3-u**3)/3+a*b*(v*v-u*u)+b*b*(v-u)
      length += v-u
      ref_area += r[2]*(v*v-u*u)/2+r[3]*(v-u)
      cand_area += c[2]*(v*v-u*u)/2+c[3]*(v-u)
      maximum = [maximum, (a*u+b).abs, (a*v+b).abs].max
    end
  end
  raise 'no positive common interval' if length == 0
  {length: length, signed: signed, absolute: absolute, squared: squared,
   maximum: maximum, reference_area: ref_area, candidate_area: cand_area}
end

def segments(rows)
  rows.map { |row| row.map { |x| q(x) } }
end

def ordered_area(points)
  points.each_cons(2).map { |u,v| (u[1]+v[1])*(v[0]-u[0])/2 }.inject(q(0), :+)
end

cases = {
  identical_different_partition: [
    segments([[0,1,1,0]]),
    segments([[0,'1/3',1,0],['1/3',1,1,0]]),
    {length: '1', signed: '0', absolute: '0', squared: '0', maximum: '0', reference_area: '1/2', candidate_area: '1/2'}],
  sign_cancellation: [
    segments([[0,1,0,1]]), segments([[0,1,2,0]]),
    {length: '1', signed: '0', absolute: '1/2', squared: '1/3', maximum: '1', reference_area: '1', candidate_area: '1'}],
  zero_reference: [
    segments([[0,1,0,0]]), segments([[0,1,0,2]]),
    {length: '1', signed: '2', absolute: '2', squared: '4', maximum: '2', reference_area: '0', candidate_area: '2'}],
  narrow_triangle: [
    segments([[0,1,0,0]]),
    segments([[0,'49/100',0,0],['49/100','1/2',100,-49],['1/2','51/100',-100,51],['51/100',1,0,0]]),
    {length: '1', signed: '1/100', absolute: '1/100', squared: '1/150', maximum: '1', reference_area: '0', candidate_area: '1/100'}],
  disconnected_support: [
    segments([[0,'1/4',0,1],['3/4',1,0,1]]), segments([[0,1,0,2]]),
    {length: '1/2', signed: '1/2', absolute: '1/2', squared: '1/2', maximum: '1', reference_area: '1/2', candidate_area: '1'}]
}
results = {}
assertions = 0
cases.each do |name,(r,c,expected)|
  actual = exact_comparison(r,c)
  expected.each do |key,value|
    raise "#{name}/#{key} mismatch" unless actual.fetch(key) == q(value)
    assertions += 1
  end
  results[name] = actual.transform_values(&:to_s)
end
reversal = ordered_area([[0,0],[1,1],[0,0]].map { |p| p.map { |x| q(x) } })
vertical = ordered_area([[0,0],[1,1],[1,0],[2,0]].map { |p| p.map { |x| q(x) } })
elastic = ordered_area([[0,0],[1,1]].map { |p| p.map { |x| q(x) } })
raise 'ordered/recoverable examples' unless reversal == 0 && vertical == q('1/2') && elastic == q('1/2')
assertions += 3
unit = q('1000000') * q('1') * q('1')
raise 'unit conversion' unless unit == 1_000_000
assertions += 1
puts JSON.pretty_generate({status: 'synthetic_only', assertions: assertions,
  comparisons: results,
  ordered: {reversal: reversal.to_s, vertical_drop: vertical.to_s,
            elastic_work: elastic.to_s, elastic_dissipation_by_definition: '0/1'},
  one_MN_m_in_N_m: unit.to_s,
  limit: 'Fixed analytic examples; not a general parser, source registration or historical result.'})
