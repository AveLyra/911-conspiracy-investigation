#!/usr/bin/env python3
"""Transcribe verified publication uncertainty tables; never apply to native samples."""
import csv,json
from pathlib import Path

out=Path('r08_work')
man=json.loads((out/'gate_reports/retrieval_manifest.json').read_text())
sha={Path(r['final_url']).name:r['sha256'] for r in man}
rows=[]

def add(quantity,family,std,expanded,units,locator,pdfpage,conditions,limits,report='2055',kind='published_measurement_uncertainty',stdkind='combined_standard_uncertainty',result='',sd='',sdunit='',sdmeaning=''):
    rows.append(dict(quantity=quantity,sensor_or_quantity_family=family,record_kind=kind,
        standard_uncertainty_value=std,standard_uncertainty_unit=units if std!='' else '',standard_uncertainty_kind=stdkind if std!='' else '',
        expanded_uncertainty_value=expanded,expanded_uncertainty_unit=units if expanded!='' else '',expanded_coverage_factor=2 if expanded!='' else '',
        published_result=result,reported_SD_value=sd,reported_SD_unit=sdunit,reported_SD_meaning=sdmeaning,
        temperature_or_operating_conditions=conditions,exact_publication_locator=locator,pdf_page_1_based=pdfpage,
        source_url=f'https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.{report}.pdf',source_sha256=sha[f'NIST.TN.{report}.pdf'],
        limits_and_join_rules=limits,applicability='publication only; not per-cell native uncertainty/calibration',
        native_uncertainty_or_calibration_assigned=False,numeric_transformation='none; printed values retained, including published rounding',
        sign_convention='uncertainty and SD magnitudes shown positive; source uses plus/minus',
        percentage_basis='percent as published; no new reading/full-scale interpretation' if units=='%' else ''))

common='TN2055 Table4 printed p26; TN2054 Table4-3 printed p80'
cool='TN2054 §4.5 p78 says load cells and position transducers protected or in cool zone below35°C; no per-channel temperature validation performed here.'
add('Actuator load','Actuator load cells; LoadNE/SE/NM/SM/NW/SW family',3.8,8,'%',common,29,cool,'Not beam-end axial force; do not confuse the8% expanded uncertainty with temporal SD of maintained total load.')
add('Reinforcement axial load','Through-hole load cells on slab reinforcement; continuous-slab specimens',5.2,11,'%',common,29,cool,'Applies to reinforcing-bar load-cell family; not whole-connection force.')
add('Displacement','String potentiometers',2.1,5,'%',common,29,cool,'Family-level estimate. Does not resolve VD location conflicts or independently establish actuator-stroke uncertainty.')
add('Actuator stroke','MTS built-in displacement channel family','','','', 'TN2055 §2.4 printed p24; Table4 printed p26',27,'Native ambient baseline units in; fire-specimen units mm.','No separately named actuator-stroke uncertainty row identified; do not silently assign the general string-potentiometer5% to every actuator channel.',kind='uncertainty_not_explicitly_assigned')
add('Beam-column gap','BEI linear position sensor',2.1,5,'%', 'TN2054 Table4-3 printed p80',98,cool,'Publication gap family; dictionary location and sensor type still govern any individual channel join.',report='2054')
add('Beam-slab slip','TR50 displacement sensor',2.3,5,'%', 'TN2054 Table4-3 printed p80',98,cool,'Publication slip family; not slab vertical displacement.',report='2054')
add('Rotation at ambient temperature','Inclinometers',4.4,9,'%',common,29,'Ambient25°C.','Do not carry9% unchanged into heated sensors; see separate-40..85°C row.')
add('Rotation within extended operating range','Inclinometers',14.3,29,'%', 'TN2054 §4.5 printed p78; Table4-3 printed p81',99,'Table specifies-40°C to85°C; p78 identifies85°C as maximum operating temperature.','The29% estimate applies within the stated range; it is not a bound for readings above85°C or failed cables.',report='2054')
add('Rotation outside operating range or failed sensor','Inclinometers and cables','','','', 'TN2054 §4.5 printed p78; TN2055 §3.4.3 printed p74',77,'DA-SC rotation readings reported unreliable after56min when85°C exceeded; SP-SC end rotation failures discussed around54/57min.','Publication event/quality warning only. No native row flags were fabricated; no quantitative uncertainty assigned to failed readings.',kind='published_operating_limit_or_failure')
add('Steel strain','Resistive steel strain gauges; brace gauges only when steel location established',2.3,5,'%', 'TN2055 Table4 printed p26; TN2054 Table4-3 printed p81',29,'TN2054 §4.5 describes near-ambient linear calibration; this table does not certify every sensor temperature.','Do not assign this5% to FBG or unidentified concrete gauges; force derivation also needs calibration-factor uncertainty.')
add('Concrete embedded strain','Resistive concrete-embedded strain gauges',1.2,3,'%', 'TN2054 Table4-3 printed p81',99,'Published sensor-class budget; no native per-channel calibration inspected.','Do not identify a native gauge as embedded solely from a generic SG prefix.',report='2054')
add('Concrete surface strain','Resistive concrete-surface strain gauges',1.5,3,'%', 'TN2054 Table4-3 printed p81',99,'Published sensor-class budget; no native per-channel calibration inspected.','Do not identify a native gauge as surface-mounted solely from a generic SG prefix.',report='2054')
add('FBG strain','Fiber Bragg Grating gauge-average concrete strain',3.1,'','microstrain', 'TN2055 §2.4 printed pp24-25',28,'Fire specimens CB-DA/CB-DA-SC:25cm gauge length; PTFE protection described up to300°C.','The3.1microstrain is an absolute standard uncertainty, not3.1% and not expanded k=2; native strain-channel availability must be established separately.',stdkind='measurement_standard_uncertainty')
add('Steel temperature','Steel thermocouple family; TN2054 table says glass sheathed TC',2.2,5,'%', 'TN2055 Table4 printed p26 and footnote1; TN2054 Table4-3 printed p81',29,'Random term evaluated at700°C,N=300; that temperature is not a general operating limit.','Insulation failure and thermocouple dislodging excluded. Do not assign to every TC/STC header without material/contact identity.')
add('Concrete temperature','Concrete thermocouple family; TN2054 table says glass sheathed TC',3.1,7,'%', 'TN2055 Table4 printed p26; TN2054 Table4-3 printed p81',29,'Random term evaluated at600°C,N=300; not a general operating limit.','No blanket assignment to section-numbered TC channels; material and depth must be established.')
add('Steel deck temperature','Steel-deck thermocouple family; TN2054 table says Nextel braided TC',2.4,5,'%', 'TN2055 Table4 printed p26; TN2054 Table4-3 printed p81',29,'Random term evaluated at1000°C,N=300; not a general operating limit.','Preserve north/south location conflicts; no per-cell assignment.')
add('Gas temperature','Compartment-gas thermocouple family; construction not assigned to native channels',1.6,4,'%', 'TN2055 Table4 printed p26; TN2054 Table4-3 printed p81',29,'Random term evaluated at1000°C,N=3000; not a general operating limit.','Gas temperature is not a beam-surface thermal boundary condition; confirm location and exposure before channel join.')
add('Plate thermometer temperature','Plate thermometers',2.2,5,'%', 'TN2055 Table4 printed p26; TN2054 Table4-3 printed p81',29,'Random term estimated; no specific temperature listed in this row.','Use only for actual plate-thermometer channels; do not infer installation in CB-DA from a generic family list.')
add('Burner heat release rate','Fuel-flow-derived burner HRR',0.8,2,'%', 'TN2055 §2.4 p25; Table4 printed p27',30,'Natural-gas fuel-flow method.','Not oxygen-consumption calorimeter HRR and not member incident heat flux.')
add('Calorimeter heat release rate','Exhaust-hood oxygen-consumption calorimetry HRR',7.4,15,'%', 'TN2055 §2.4 p25; Table4 printed p27',30,'13.7m by15.2m exhaust hood.','Not burner setpoint or fuel-flow HRR.')
add('Incident heat flux','Heat-flux sensor family','','','', 'TN2055 §2.4; Table4 printed pp26-27',29,'No separate heat-flux uncertainty row in the inspected Table4.','No quantitative uncertainty assigned; do not substitute burner-HRR or temperature uncertainty.',kind='uncertainty_not_explicitly_assigned')
add('Dimensions larger than0.5m','Surveyed geometry',13,27,'mm','TN2055 Table4 continuation printed p27',30,'Strictly larger than0.5m, as printed.','Absolute dimensional uncertainty; not a complete as-built connection tolerance survey; no boundary convention supplied at exactly0.5m.')
add('Dimensions smaller than0.5m','Surveyed geometry',4,8,'mm','TN2055 Table4 continuation printed p27',30,'Strictly smaller than0.5m, as printed.','Absolute dimensional uncertainty; do not use as blanket uncertainty of nominal drawing dimensions.')
add('Beam-end axial force inferred from brace strain','Brace strain times3.90kN/microstrain','','','', 'TN2055 §3.4.1 printed pp66-67',69,'Load-to-strain factor measured at ambient temperature; structural restraint during fire.','No complete force uncertainty budget established here. Strain5% alone and the reported peak SD are not substitute propagated uncertainties.',kind='derived_quantity_uncertainty_not_quantified')
add('CB-DA maintained actuator-load landmark','Total mechanical load in ambient-loading stage of fire specimen','','','', 'TN2055 §3.2.1/Table5 printed p38',41,'Time average over15–40min interval in Figure14.','This is the fire specimen CB-DA ambient-loading stage, not the independent CB-DA-AMB baseline.',kind='published_result_dispersion_not_measurement_uncertainty',result='106.1kN',sd=0.1,sdunit='kN',sdmeaning='Published temporal standard deviation of maintained load; not combined standard uncertainty or expanded uncertainty.')
add('CB-DA peak beam-end compression landmark','Force estimated from brace strains','','','', 'TN2055 §3.4.1 printed p66; Table12 printed p67',70,'Peak reported at30min after ignition.','Not a direct connection-load-cell result; not an expanded confidence interval.',kind='published_result_dispersion_not_measurement_uncertainty',result='716kN at30min',sd=85,sdunit='kN',sdmeaning='Published SD among axial-load estimates from top/bottom braces at east/west ends; not total propagated measurement uncertainty.')

with (out/'published_uncertainty_map.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
assert len(rows)==26
assert all(not r['native_uncertainty_or_calibration_assigned'] for r in rows)
assert all(r['standard_uncertainty_value']=='' and r['expanded_uncertainty_value']=='' for r in rows if r['record_kind']=='published_result_dispersion_not_measurement_uncertainty')
print(f'Wrote {len(rows)} publication rows; no native per-cell uncertainty or calibration assigned.')
