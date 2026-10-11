"""F9-Im0 manual peer literals, frozen before matching-primary exchange."""
from peer_export import run

SOLID_RUNS = [
    [230,230,[],[87],'s01'], [231,231,[],[86,87],'s01'],
    [232,232,[85,86,87],[83,84],'s01'], [233,233,[81,82,83,84],[79,80,85,86],'s01'],
    [234,234,[78,79,80],[76,77,81,82],'s01'], [235,235,[75,76,77],[73,74,78,79],'s01'],
    [236,236,[71,72,73,74],[69,70,75,76],'s01'], [237,237,[69,70,71],[68,72,73],'s01'],
    [238,238,[67,68,69],[66,70],'s01'], [239,239,[66,67],[65,68],'s01'],
    [240,246,[66],[65,67],'s01'], [247,247,[66,67],[65,68],'s01'],
    [248,248,[66],[65,67],'s01'], [249,253,[66,67],[65,68],'s01'],
    [254,254,[66],[65,67],'s01'], [255,255,[66,67],[65,68],'s01'],
    [256,260,[66],[65,67],'s01'], [261,262,[66,67],[65,68],'s01'],
    [263,263,[67],[66,68],'s01'], [264,264,[67,68],[66,69],'s01'],
    [265,266,[68],[67,69],'s01'], [267,267,[68,69],[67,70],'s01'],
    [268,269,[69],[68,70],'s01'], [270,270,[69,70],[68,71],'s01'],
    [271,271,[70],[69,71],'s01'], [272,272,[69,70],[68,71],'s01'],
    [273,273,[70],[69,71],'s01'], [274,275,[70,71],[69,72],'s01'],
    [276,277,[71],[70,72],'s01'], [278,278,[71,72],[70,73],'s01'],
    [279,280,[72],[71,73],'s01'], [281,281,[72,73],[71,74],'s01'],
    [282,283,[73],[72,74],'s01'], [284,284,[73,74],[72,75],'s01'],
    [285,285,[74],[73,75],'s01'], [286,286,[74,75],[73,76],'s01'],
    [287,288,[75],[74,76],'s01'], [289,289,[75,76],[74,77],'s01'],
    [290,290,[76],[75,77],'s01'], [291,291,[76,77],[75,78],'s01'],
    [292,292,[77,78],[76,79],'s01'], [293,293,[78],[77,79],'s01'],
    [294,294,[78,79],[77,80],'s01'], [295,295,[79,80],[78,81],'s01'],
    [296,296,[80],[79,81],'s01'], [297,297,[80,81],[79,82],'s01'],
    [298,298,[81,82],[80,83],'s01'], [299,299,[82],[81,83],'s01'],
    [300,300,[82,83],[81,84],'s01'], [301,302,[83,84],[82,85],'s01'],
    [303,303,[84,85],[83,86],'s01'], [304,304,[85],[84,86],'s01'],
    [305,305,[86],[85,87],'s01'], [306,306,[86,87],[85],'s01'],
    [307,307,[87],[86],'s01'], [308,308,[],[87],'s01'],
]
DASH_RUNS = [
    [278,278,[],[87],'d01'], [279,279,[],[86,87],'d01'],
    [280,280,[86,87],[85],'d01'], [281,281,[85,86],[84,87],'d01'],
    [282,282,[83,84,85],[82,86],'d01'], [283,283,[83,84],[82,85],'d01'],
    [284,285,[82,83,84],[81,85],'d01'],
    [287,288,[83,84],[82,85],'d02'], [289,289,[84,85],[83,86],'d02'],
    [290,290,[],[84,85],'d02'],
    [293,293,[],[86,87],'d03'], [294,294,[86],[85,87],'d03'],
    [295,295,[86,87],[85],'d03'], [296,296,[87],[86],'d03'],
    [297,297,[86,87],[85],'d03'], [298,298,[],[86,87],'d03'],
]
UNASSIGNED_RUNS = [
    [286,286,[],[82,83,84,85],'u-dash-bodies'],
    [291,291,[],[85],'u-dash-tail'],
    [309,309,[],[87],'u-solid-exit'],
]
CONFIG = {
    'pair':'F9','region_id':'F9-Im0','source_image':'Im0.jpg',
    'target':[220,55,325,88],'context':[218,53,327,88],
    'solid':SOLID_RUNS,'dash':DASH_RUNS,'unassigned':UNASSIGNED_RUNS,
    'unassigned_candidates':{286:['dash'],291:['dash'],309:['solid']},
    'unassigned_reasons':{
        286:'Pale purple material between two locally distinguishable broken bodies; possible Shell ink/compression, body membership unresolved. Not a Solid conflict.',
        291:'Pale purple possible broken-body tail/compression; no unique body attribution. Solid remains separate above.',
        309:'Pale bottom-cell possible continuation fringe/compression after the solid exits; cannot establish a physical endpoint.',
    },
    'raw_blocks':[
        {'display_region':'F9-Im0','box':[218,53,238,88],'untruncated':True,'receipt':'Own read_context.py show F9-Im0 --first218 --last237; full output displayed in this force69_peer turn.'},
        {'display_region':'F9-Im0','box':[238,53,268,88],'untruncated':True,'receipt':'Own read_context.py show F9-Im0 --first238 --last267; full output displayed in this force69_peer turn.'},
        {'display_region':'F9-Im0','box':[268,53,298,88],'untruncated':True,'receipt':'Own read_context.py show F9-Im0 --first268 --last297; full output displayed in this force69_peer turn.'},
        {'display_region':'F9-Im0','box':[298,53,327,88],'untruncated':True,'receipt':'Own read_context.py show F9-Im0 --first298 --last326; full output displayed in this force69_peer turn.'},
    ],
    'identity_basis':'Purple solid crest/decline and separate lower broken bodies in the complete unchanged strip; confirmed composed-page legend: nine bolts, solid Spring and broken Shell. No cross-strip join or vertical-order-only assignment.',
    'notes':'Read all context cells. Source background in early/late columns receives no target attribution. Distinguishable broken bodies retain local IDs; unresolved interbody/tail material is stored once with route-specific candidates. Bottom truncation is not a physical zero or endpoint.',
}
if __name__ == '__main__':
    run(CONFIG,__file__)
