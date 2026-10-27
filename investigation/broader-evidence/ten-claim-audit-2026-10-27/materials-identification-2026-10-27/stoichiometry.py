"""Conditional oxygen-budget algebra. No spectra fitted or chemical assay run."""
from pathlib import Path
from fractions import Fraction as F
import json
D=Path(__file__).resolve().parent
def atom_basis(al_over_o):
    if al_over_o<=0:raise ValueError('Positive ratio required')
    maximum=min(F(1),F(2,3)/al_over_o)
    return maximum,1-maximum,max(F(1),F(3,2)*al_over_o)
def mass_basis(al_over_o):
    if al_over_o<=0:raise ValueError('Positive ratio required')
    # Explicit rounded masses: Al27, O16; not additional measured inputs.
    maximum=min(F(1),F(2*27,3*16)/al_over_o)
    return maximum,1-maximum,max(F(1),F(3*16,2*27)*al_over_o)
checks=[]
def check(name,result):checks.append({'name':name,'passed':bool(result)})
check('atom3:1 conservative upper bound',atom_basis(F(3))[0]==F(2,9))
check('atom3:1 unassigned fraction',atom_basis(F(3))[1]==F(7,9))
check('atom3:1 oxygen correction threshold',atom_basis(F(3))[2]==F(9,2))
check('mass3:1 conservative upper bound',mass_basis(F(3))[0]==F(3,8))
check('mass3:1 unassigned fraction',mass_basis(F(3))[1]==F(5,8))
check('mass3:1 oxygen correction threshold',mass_basis(F(3))[2]==F(8,3))
check('stoichiometric atom oxide has no unassignedAl',atom_basis(F(2,3))==(F(1),F(0),F(1)))
check('stoichiometric mass oxide has no unassignedAl',mass_basis(F(9,8))==(F(1),F(0),F(1)))
grid=[F(1,2),F(2,3),F(1),F(9,8),F(2),F(3),F(10)]
for fn in [atom_basis,mass_basis]:
    vals=[fn(r)[1] for r in grid]
    check(fn.__name__+' monotonic conditional remainder',all(a<=b for a,b in zip(vals,vals[1:])))
    try:fn(F(0));valid=False
    except ValueError:valid=True
    check(fn.__name__+' rejects undefinedzero ratio',valid)
def record(name,fn):
    a,b,c=fn(F(3))
    return {'basis':name,'reported_approximate_Al_over_O_assumed_exact_for_algebra':'3/1',
      'max_fraction_reported_Al_explainable_as_Al2O3':str(a),
      'fraction_reported_Al_not_explained_as_Al2O3_given_measured_O':str(b),
      'required_multiplier_on_reported_O_over_Al_to_allow_all_Al_as_Al2O3':str(c),
      'max_percent':100*float(a),'unassigned_percent':100*float(b),'oxygen_ratio_multiplier':float(c)}
out={'rows':[record('atomic',atom_basis),record('mass_with_rounded_masses27_and16',mass_basis)],
 'assumptions':['Reported3:1 is a corrected atom or mass ratio, not raw xray peak-height/count ratio.',
 'ReportedAl andO quantify the same analyzed material without unmodeled substrate, geometry, contamination or response bias.',
 'All reportedO is allocated toAl2O3 to maximize oxideAl; oxygen bound toFe,Si orother constituents would lower that maximum.',
 'The remainder is not automaticallyAlmetal; unmeasured nonoxygen compounds, response errors or wrong sample attribution remain possible.',
 'Approximate published ratio has no supplied uncertainty here; no confidence interval or actual dust/metal mass fraction is inferred.'],
 'raw_counts_basis':'Not identifiable from this algebra; detector/matrix response must first convert counts to composition.',
 'falsifying_scenarios':['Foratomic3:1, a4.5fold upward correction inO/Al allows allAl asAl2O3; for mass3:1, the threshold is8/3. No evidence such an error actually occurred is supplied.',
 'A verified oxide standard returns zero unassignedAl. An accurately validated3:1 composition would conflict with an all-Al-as-oxide description of that analyzed region.',
 'NonoxygenAl compounds or substrate contributions break inference from oxygen deficit to metallicAl.'],
 'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),
 'scope':'Exact conditional stoichiometry only, not verification of the reported ratio, a spectrum measurement, elemental-state assay, thermite identification or mechanism probability.'}
with (D/'STOICHIOMETRY-RESULT.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
assert not out['failed']
print(json.dumps({'rows':out['rows'],'passed':out['passed'],'failed':out['failed'],'scope':out['scope']},indent=2))
