#!/usr/bin/env python3
"""Record source-located visual observations; no dimensions are measured from pixels."""
import csv,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
items=[
 (1,'TestSetupDrawings','A1','B26','Test setup 3D view','not independently used for sensor reconciliation'),
 (2,'TestSetupDrawings','A2','B58','Front view: support columns, loading trusses, beam and actuators','visually inspected; dimension42ft/1280cm shown between support-column lines'),
 (3,'TestSetupDrawings','A3','B101','Test setup plan view','inventoried; see original graphic'),
 (4,'TestSetupDrawings','A4','B147','Test setup side view','inventoried; see original graphic'),
 (5,'TestSetupDrawings','A5','B177','Compartment and burners front view','inventoried; see original graphic'),
 (6,'TestSetupDrawings','A6','B198','Compartment and burners plan view','inventoried; see original graphic'),
 (7,'TestSetupDrawings','A7','B231','Compartment and burners side view','inventoried; see original graphic'),
 (8,'TestSetupDrawings','A8','B259','Double-angle and shear-tab connection details','inventoried; see original graphic'),
 (9,'TestSetupDrawings','A9','B296','Slab continuity for SC specimens','inventoried; see original graphic'),
 (10,'InstrumentationLayout-AmbTest','B1(a-e)','B73','Ambient displacement, rotation, strain, slip and gap','visually inspected except panel(d), which renders incompletely in Inkscape; do not treat preview omission as missing native source'),
 (11,'InstrumentationLayout-AmbTest','B1(f)','B73','Ambient loading-truss strain and rotation','visually inspected; west Tri1/RotLT1, middle Tri2/RotLT2, east Tri3/RotLT3'),
 (12,'InstrumentationLayout-FireTests','C1','B32','Fire vertical displacement and slab rotations','visually inspected; west-to-east VD2,VD3,VD4,VD5; do not use conflicting prose descriptions as exact sensor locations'),
 (13,'InstrumentationLayout-FireTests','C2(a-b)','B102','Sections1-8; thermocouples in sections1,2,7,8','visually inspected; section and sensor-depth labels are source dimensions, not measured pixels'),
 (14,'InstrumentationLayout-FireTests','C2(c-d)','B102','Thermocouples in sections3-6 and Inconel STC1-12','visually inspected; STC1-4 at Y23.5in; preserve discrepancies with dictionaries'),
 (15,'InstrumentationLayout-FireTests','C3(a-b)','B145','West double-angle and shear-tab connection thermocouples','visually inspected; distinct angle-leg vs shear-tab geometry; do not reuse generic shear-tab descriptions for double angles'),
 (16,'InstrumentationLayout-FireTests','C4(a-b)','B194','Compartment gas and ventilation-opening thermocouples','visually inspected; plan repeats TCC1 at southeast interior whereas elevation labels corresponding point TCC13 south'),
 (17,'InstrumentationLayout-FireTests','C5(a-b)','B218','Plate thermometers near beam and east wall','visually inspected; PT2 beside web, PT3 below bottom flange, PT1 near east wall; installation must be checked by specimen'),
 (18,'InstrumentationLayout-FireTests','C6(a)','B290','West column-brace strain gauges','visually inspected; ColW1-4 on upper brace, ColW5-8 on lower brace; depicted north/south positions retained in image'),
 (19,'InstrumentationLayout-FireTests','C6(b-c)','B290','Loading-truss rotations and SC rebar load cells','visually inspected; RotLT1 west,RotLT2 middle,RotLT3 east; LCW1-4 north-to-south at west slab anchorage'),
]
rows=[]
for n,sheet,fig,caption,subject,review in items:
 ext='png' if 2<=n<=7 else 'emf'
 p=ROOT/'drawings_inspection'/f'image{n}.{ext}'
 rows.append({'workbook':'drawings.xlsx','sheet':sheet,'figure':fig,'caption_cell':caption,
  'native_media_member':f'xl/media/image{n}.{ext}','native_media_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
  'subject':subject,'review':review,'preview':f'previews/image{n}.png',
  'preview_status':'native embedded PNG' if ext=='png' else 'derived Inkscape rasterization; original EMF preserved unchanged inside workbook'})
with (ROOT/'drawing_media_inventory.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
positions=[]
for lab,expr,x in [('VD2','132',132),('VD3','132+84',216),('VD4','504-132-84',288),('VD5','504-132',372)]:
 positions.append({'label':lab,'source_workbook':'drawings.xlsx','source_sheet':'InstrumentationLayout-FireTests','source_figure':'C1','source_media':'xl/media/image12.emf','caption_cell':'B32',
  'drawing_dimension_expression_inches':expr,'derived_x_inches':x,'derived_x_cm':x*2.54,
  'drawing_datum':'west dimension endpoint in C1; not silently equated with published centerline datum',
  'published_TN2055_Table13_x_cm':{'VD2':336,'VD3':548,'VD4':732,'VD5':944}[lab],
  'published_datum':'west column centerline','method':'arithmetic on written dimensions and displayed symmetry; no pixel measurement or curve digitization'})
(ROOT/'drawing_VD_positions_observed_and_derived.json').write_text(json.dumps(positions,indent=2)+'\n')
print(json.dumps({'figures_and_parts':len(rows),'vertical_position_records':len(positions)}))
