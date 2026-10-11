"""F7-Im1 independent manual peer literals, frozen before expanded exports."""
from peer_export import run
SOLID_RUNS = [
    [224,224,[67,68,69],[66,70],'s01'], [225,225,[67,68],[66,69],'s01'],
    [226,226,[67],[66,68],'s01'], [227,227,[66,67],[65,68],'s01'],
    [228,228,[65,66],[64,67],'s01'], [229,229,[65,66],[64,67],'s01'],
    [230,230,[64,65],[63,66],'s01'], [231,231,[64],[63,65],'s01'],
    [232,232,[63,64],[62,65],'s01'], [233,233,[63,64],[62,65],'s01'],
    [234,234,[62,63],[61,64],'s01'], [235,235,[62,63],[61,64],'s01'],
    [236,236,[62],[61,63],'s01'], [237,238,[61,62],[60,63],'s01'],
    [239,239,[61,62],[60,63],'s01'], [240,240,[61],[60,62],'s01'],
    [241,241,[61],[60,62],'s01'], [242,242,[60,61],[59,62],'s01'],
    [243,244,[60,61],[59,62],'s01'], [245,245,[60],[59,61],'s01'],
    [246,247,[59,60],[58,61],'s01'], [248,250,[59],[58,60],'s01'],
    [251,253,[58,59],[57,60],'s01'], [254,256,[58],[57,59],'s01'],
    [257,258,[57,58],[56,59],'s01'], [259,261,[58],[57,59],'s01'],
    [262,262,[58,59],[57,60],'s01'],
    [263,264,[58,59],[57,60],'s01'], [265,267,[59],[58,60],'s01'],
    [268,271,[59,60],[58,61],'s01'], [272,273,[60],[59,61],'s01'],
    [274,277,[60,61],[59,62],'s01'], [278,279,[60,61],[59],'s01'],
    [280,282,[61],[60],'s01'],
    [283,284,[61,62],[60],'s01'],
    [289,289,[64],[65],'s02'], [290,290,[64],[65],'s02'],
    [291,291,[64,65],[63,66],'s02'], [292,292,[64,65,66],[63,67],'s02'],
    [293,293,[65,66],[64,67],'s02'], [294,294,[66],[65,67],'s02'],
    [295,295,[66,67],[65,68],'s02'], [296,296,[67],[66,68],'s02'],
    [297,297,[67,68],[66,69],'s02'], [298,298,[68],[67,69],'s02'],
    [299,299,[68,69],[67,70],'s02'], [300,300,[69],[68,70],'s02'],
    [301,302,[69,70],[68],'s02'], [303,303,[70],[],'s02'],
    [305,305,[71,72],[73],'s03'], [306,306,[72],[71,73],'s03'],
    [307,307,[72,73],[71,74],'s03'], [308,308,[73],[72,74],'s03'],
    [309,309,[73,74],[72,75],'s03'], [310,311,[74,75],[73,76],'s03'],
    [312,312,[75,76],[74,77],'s03'], [313,313,[76],[75,77],'s03'],
    [314,314,[76],[75,77],'s03'], [315,315,[76,77],[75,78],'s03'],
    [316,316,[77,78],[76,79],'s03'], [317,317,[78],[77,79],'s03'],
    [318,318,[78,79],[77,80],'s03'], [319,319,[79,80],[78,81],'s03'],
    [320,320,[80,81],[79,82],'s03'], [321,321,[80,81,82],[79,83],'s03'],
    [322,322,[81,82,83],[80,84],'s03'],
    [323,323,[83],[82,84],'s03'], [324,324,[84],[85],'s03'],
    [325,325,[84,85],[86],'s03'],
]
DASH_RUNS = []
UNASSIGNED_RUNS = [
    [220,221,[],[68,69,70],'u-solid-purple'],
    [222,222,[],[68,69,70],'u-solid-purple'],
    [223,223,[],[68,69],'u-solid-purple'],
    [278,278,[],[62,63],'u-solid-cyan'], [279,279,[],[62,63,64],'u-solid-cyan'],
    [280,280,[],[62,63],'u-solid-cyan'], [281,281,[],[59,62,63],'u-solid-cyan'],
    [282,282,[],[58,59,62],'u-solid-cyan'],
    [283,284,[],[63],'u-solid-cyan'], [285,285,[],[61,62,63],'u-solid-cyan'],
    [286,286,[],[61,62,63],'u-solid-cyan'], [287,287,[],[62,63,64],'u-solid-cyan'],
    [288,288,[],[63,64],'u-solid-cyan'], [289,289,[],[62,63],'u-solid-cyan'],
    [290,290,[],[63],'u-solid-cyan'], [301,302,[],[71],'u-solid-red'],
    [303,303,[],[71,72],'u-solid-red'], [304,304,[],[70,71,72,73],'u-solid-red'],
    [305,305,[],[70],'u-solid-red'],
    [324,325,[],[83],'u-solid-red'], [326,326,[],[85,86],'u-solid-red'],
    [327,327,[],[85,86,87],'u-solid-red'], [328,328,[],[86,87],'u-solid-red'],
    [329,329,[],[86,87],'u-solid-bottom'],
]
CONFIG = {
    'pair':'F7','region_id':'F7-Im1','source_image':'Im1.jpg',
    'target':[220,50,335,88],'context':[218,48,337,88],
    'solid':SOLID_RUNS,'dash':DASH_RUNS,'unassigned':UNASSIGNED_RUNS,
    'unassigned_candidates':{220:['solid'],221:['solid'],222:['solid'],223:['solid']},
    'unassigned_reasons':{
        220:'Mixed purple/gray band at green solid crossing; possible green contribution unresolved.',
        221:'Mixed purple/gray band at green solid crossing; possible green contribution unresolved.',
        222:'Mixed purple/gray-green band at green solid crossing; possible green contribution unresolved.',
        223:'Gray-green material at end of crossing; possible green solid contribution unresolved.',
    },
    'raw_blocks':[{'display_region':'F8-Im1','box':[218,8,243,88],'untruncated':True,'receipt':'96949a; own all80row exact RGB display; this region reuses x218..242 rows48..87 by exact source/cell equality, not a separate observation.'}],
    'identity_basis':'Confirmed seven-bolt green; solid Spring and broken Shell. Full unchanged Im1 and composed page inspected. Crossings and clipping do not identify physical endpoints.',
}
CONFIG['raw_blocks'] += [{'display_region':'F9-Im1','box':[243,0,263,88],'untruncated':True,'receipt':'818552; own complete all88row exact raw display; this region reuses rows48..87 by exact source/cell equality, not separate corroboration.'}]
CONFIG['unassigned_candidates'].update({278:['solid'],279:['solid'],280:['solid'],281:['solid'],282:['solid']})
CONFIG['unassigned_reasons'].update({278:'Green/cyan mixed boundary; possible green solid only.',279:'Green/cyan mixed boundary; possible green solid only.',280:'Green/cyan mixed boundary; possible green solid only.',281:'Green/cyan mixed boundary on both sides of green body; possible green solid only.',282:'Green/cyan mixed boundary on both sides of green body; possible green solid only.'})
CONFIG['raw_blocks'] += [{'display_region':'F9-Im1','box':[263,0,283,88],'untruncated':True,'receipt':'3c82b3; own all88row raw display, reused rows48..87 by exact source/cell equality, not new corroboration.'}]
CONFIG['unassigned_candidates'].update({283:['solid'],284:['solid'],285:['solid'],286:['solid'],287:['solid'],288:['solid'],289:['solid'],290:['solid'],301:['solid'],302:['solid'],303:['solid'],304:['solid'],305:['solid']})
CONFIG['unassigned_reasons'].update({283:'Green/cyan mixed boundary; possible green solid only.',284:'Green/cyan mixed boundary; possible green solid only.',285:'Green/cyan mixed band; possible green solid contribution unresolved.',286:'Cyan-dominant mixed band; possible green solid contribution unresolved, no hidden path reconstructed.',287:'Cyan-dominant mixed band; possible green solid contribution unresolved, no hidden path reconstructed.',288:'Cyan/green mixed band; possible green solid contribution unresolved.',289:'Cyan/green mixed band beside green solid; contribution unresolved.',290:'Pale mixed cyan/green edge; possible green solid contribution.',301:'Yellow-green mixed edge near red crossing; possible green solid only.',302:'Yellow-green mixed edge near red crossing; possible green solid only.',303:'Brown/green mixed crossing with red; possible green solid only.',304:'Brown/green mixed crossing with red; possible green solid only.',305:'Pale yellow-green fringe near crossing; possible green solid only.'})
CONFIG['raw_blocks'] += [
    {'display_region':'F9-Im1','box':[283,0,303,88],'untruncated':True,'receipt':'1bdc67; own all88row raw display; exact reuse of rows48..87, not new corroboration.'},
    {'display_region':'F9-Im1','box':[303,0,323,88],'untruncated':True,'receipt':'d6ee41; own all88row raw display; exact reuse of rows48..87, not new corroboration.'},
]
CONFIG['unassigned_candidates'].update({324:['solid'],325:['solid'],326:['solid'],327:['solid'],328:['solid'],329:['solid']})
CONFIG['unassigned_reasons'].update({324:'Yellow/brown-green mixed boundary at red crossing; possible green solid only.',325:'Yellow/brown-green mixed boundary at red crossing; possible green solid only.',326:'Brown/green mixed bottom-edge crossing material; possible green solid unresolved.',327:'Brown/green mixed bottom-edge crossing material; possible green solid unresolved.',328:'Olive mixed bottom-edge material; possible green solid unresolved.',329:'Pale bottom-edge green tail; possible solid contribution, not a physical endpoint.'})
CONFIG['raw_blocks'] += [{'display_region':'F9-Im1','box':[323,0,343,88],'untruncated':True,'receipt':'ddcfc3; own all88row exact RGB display. This region reuses only x323..336 rows48..87 by exact source/cell equality; x337..342 are not part of its context, no extra corroboration claimed.'}]
CONFIG['notes']='Every required context cell x218..336, rows48..87 was read, using own F8 x218..242 rows8..87 display and own F9 x243..342 all88row displays with exact source/cell equality. Reuse is coverage only, not independent corroboration. All target columns have both local style outcomes. No confidently attributable green broken-line footprint in this target after full contextual inspection; that is not a claim of physical absence outside the fixed locator. Three solid local pieces and mixed cyan/purple/red bands are retained; unassigned material names only the possible solid route. No interpolation, physical metric, endpoint identification, accepted human sample, or causal conclusion.'
if __name__ == '__main__': run(CONFIG,__file__)
