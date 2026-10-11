"""F9-Im1 independent manual peer literals, frozen before expanded exports."""
from peer_export import run
SOLID_RUNS = [
    [307,307,[],[0],'s01'], [308,308,[0],[1],'s01'], [309,310,[0,1],[2],'s01'],
    [311,311,[2],[1,3],'s01'], [312,312,[2,3],[4],'s01'],
    [313,313,[3,4],[2,5],'s01'], [314,314,[4],[3,5],'s01'],
    [315,315,[4,5],[3,6],'s01'], [316,316,[5,6],[4,7],'s01'],
    [317,317,[6],[5,7],'s01'], [318,318,[6,7],[5,8],'s01'],
    [319,319,[7,8],[6,9],'s01'], [320,320,[8],[7,9],'s01'],
    [321,321,[9],[8,10],'s01'], [322,322,[10],[9,11],'s01'],
    [323,323,[11],[10,12],'s01'], [324,324,[12,13],[11,14],'s01'],
    [325,325,[13,14],[12,15],'s01'], [326,326,[14,15],[13,16],'s01'],
    [327,327,[15,16],[14,17],'s01'], [328,328,[17],[16,18],'s01'],
    [329,329,[17,18],[16,19],'s01'], [330,330,[18,19],[17,20],'s01'],
    [331,331,[19,20],[18,21],'s01'], [332,332,[20,21],[19,22],'s01'],
    [333,333,[21,22],[20,23],'s01'], [334,334,[22,23],[21,24],'s01'],
    [335,335,[23],[22],'s01'], [336,336,[24,25],[23,26],'s01'],
    [337,337,[25,26],[24,27],'s01'], [338,338,[26,27],[25,28],'s01'],
    [339,339,[28],[27,29],'s01'], [340,340,[28,29],[27,30],'s01'],
    [341,341,[30],[29,31],'s01'], [342,342,[31],[30,32],'s01'],
    [343,343,[32],[31,33,34],'s01'], [344,344,[33,34],[32,35],'s01'],
    [345,345,[34,35],[33,36],'s01'], [346,346,[35,36],[34,37],'s01'],
    [347,347,[36,37],[35,38],'s01'], [348,348,[37,38],[36,39],'s01'],
    [349,349,[38,39],[37,40],'s01'], [350,350,[39,40],[38,41],'s01'],
    [351,351,[41],[40,42,43],'s01'], [352,352,[42,43],[41,44],'s01'],
    [353,353,[44],[43,45],'s01'], [354,354,[45,46],[44,47],'s01'],
    [355,355,[46,47,48],[45,49],'s01'], [356,356,[48,49],[47,50],'s01'],
    [357,357,[49,50,51],[48,52],'s01'], [358,358,[51,52,53],[50,54],'s01'],
    [359,359,[53,54],[52,55],'s01'], [360,360,[54,55,56],[53,57],'s01'],
    [361,361,[56,57],[55,58],'s01'], [362,362,[57,58],[56,59],'s01'],
    [363,363,[58,59,60],[57,61],'s01'], [364,364,[60,61],[59,62],'s01'],
    [365,365,[61,62,63],[60,64],'s01'], [366,366,[63,64],[62,65],'s01'],
    [367,367,[64,65],[63,66],'s01'], [368,368,[65,66,67],[64,68],'s01'],
    [369,369,[67,68],[66,69],'s01'], [370,370,[69],[68,70],'s01'],
    [371,371,[69,70,71],[68],'s01'],
]
DASH_RUNS = [
    [245,245,[],[33,34],'d01'], [246,246,[33,34],[32,35],'d01'],
    [247,247,[32],[31,33],'d01'], [248,248,[30,31],[29,32],'d01'],
    [249,249,[30],[29,31],'d01'],
    [251,251,[],[26,27,28],'d02'], [252,252,[26,27],[25,28],'d02'],
    [253,253,[25,26],[24,27],'d02'], [254,254,[24,25],[23,26],'d02'],
    [255,255,[23],[22,24],'d02'], [256,256,[22],[21,23],'d02'],
    [257,257,[21,22],[23],'d02'],
    [261,261,[17],[16],'d03'], [262,262,[16,17],[15],'d03'],
    [263,263,[15,16],[14],'d03'], [264,264,[15],[14,16],'d03'],
    [266,266,[11,12],[10,13],'d04'], [267,267,[10,11,12],[9,13],'d04'],
    [268,268,[10,11],[9,12],'d04'],
    [270,270,[8,9],[7,10],'d05'], [271,271,[7,8],[6,9],'d05'],
    [272,272,[7],[6,8],'d05'],
    [274,274,[],[3,4,5],'d06'], [275,275,[3,4],[2,5],'d06'],
    [276,276,[2,3],[1,4],'d06'], [277,277,[0,1,2],[3],'d06'],
    [278,278,[0,1],[2],'d06'],
    [295,296,[],[0],'d07'], [298,298,[1,2],[0,3],'d08'],
    [299,299,[0,1,2],[3],'d08'], [300,300,[1,2],[0,3],'d08'],
    [301,301,[],[5,6],'d09'], [302,303,[3,4,5],[2,6],'d09'],
    [305,305,[6,7],[5,8],'d10'], [306,307,[7],[6,8],'d10'],
    [308,308,[8,9],[7,10],'d10'], [309,309,[9],[8,10],'d10'],
    [311,311,[],[11,12],'d11'], [312,312,[11,12,13,14],[10,15],'d11'],
    [313,313,[14,15,16],[13,17],'d11'], [314,314,[14,15,16],[13,17],'d11'],
    [315,315,[14,15,16,17],[13,18],'d11'], [316,316,[17],[16,18,20,21],'d11'],
    [317,317,[17,18,19,20,21],[16,22],'d11'], [318,318,[17],[16,18,20,21],'d11'],
    [319,319,[21,22,23],[20,24,25],'d12'], [320,320,[22,23,24,25],[21,26],'d12'],
    [321,321,[24],[23,25],'d12'],
    [323,323,[26,27,28],[25,29],'d13'], [324,324,[27,28],[26,29],'d13'],
    [325,325,[27,28],[29],'d13'],
    [330,331,[35,36,37,38],[34,39],'d14'],
    [333,333,[38,39,40,41,42],[37,43],'d15'],
    [334,334,[40,41,42,43],[39,44],'d15'], [335,335,[42],[41,43],'d15'],
    [336,336,[41,42,43],[40,44,45],'d15'], [337,337,[43,44,45],[42,46],'d15'],
    [339,339,[],[47,48],'d16'], [340,340,[47,48,49],[50],'d16'],
    [343,343,[52,53,54,55],[51,56],'d17'], [344,344,[54,55,56,57],[53,58],'d17'],
    [345,345,[],[61,62],'d18'], [346,346,[61,62],[60,63],'d18'],
    [347,347,[62,63,64,65],[61,66],'d18'], [348,348,[65,66],[64,67],'d18'],
    [350,350,[73,74,75],[76],'d19'], [351,351,[74,75],[73,76],'d19'],
    [352,352,[80,81,82,83],[79,84],'d20'], [353,353,[81,82,83,84],[80,85],'d20'],
]
UNASSIGNED_RUNS = [
    [250,250,[],[29,30],'u-dash-gap'], [257,257,[],[20],'u-dash-cyan'],
    [258,258,[],[20,21],'u-dash-gap'], [259,259,[],[18,19],'u-dash-cyan'],
    [260,260,[],[17,18,19],'u-dash-cyan'], [261,262,[],[18,19],'u-dash-cyan'],
    [263,263,[],[17,18],'u-dash-cyan'], [265,265,[],[11,12],'u-dash-gap'],
    [269,269,[],[9,10,11],'u-dash-gap'], [273,273,[],[6,7],'u-dash-gap'],
    [279,279,[],[0,1],'u-dash-top'],
    [294,294,[],[0],'u-dash-onset'], [297,297,[],[0,1],'u-dash-gap'],
    [301,301,[],[1],'u-dash-gap'], [304,304,[],[4,5],'u-dash-gap'],
    [310,310,[],[9,10],'u-dash-gap'], [322,322,[],[26,27],'u-dash-gap'],
    [326,326,[],[27,28],'u-dash-gap'], [327,327,[],[31,32,33,34],'u-dash-cyan'],
    [328,328,[],[30,31,32,33,34],'u-dash-cyan'], [329,329,[],[30,31,32,33],'u-dash-cyan'],
    [332,332,[],[35,36],'u-dash-gap'], [335,335,[],[24,25],'u-solid-cyan'],
    [338,338,[],[45,46],'u-dash-gap'], [339,339,[],[44,45,46],'u-dash-cyan'],
    [340,340,[],[44,45,46],'u-dash-cyan'], [341,341,[],[48,49,50],'u-dash-gap'],
    [342,342,[],[51,52,53],'u-dash-gap'],
    [345,345,[],[57],'u-dash-tail'], [348,348,[],[69,70,71],'u-dash-cyan'],
    [349,349,[],[70,71,72],'u-dash-cyan'], [350,350,[],[71,72],'u-dash-cyan'],
    [351,351,[],[79,80],'u-dash-onset'], [354,354,[],[83,84],'u-dash-tail'],
    [354,355,[],[87],'u-dash-bottom'],
    [370,370,[],[71,72],'u-solid-green'], [371,371,[],[72,73],'u-solid-green'],
    [372,372,[],[71,72,73,74],'u-solid-green'], [373,373,[],[72,73,74,75,76],'u-solid-green'],
    [374,374,[],[73,74,75,76,77],'u-solid-green'],
]
CONFIG = {
    'pair':'F9','region_id':'F9-Im1','source_image':'Im1.jpg',
    'target':[245,0,375,88],'context':[243,0,377,88],
    'solid':SOLID_RUNS,'dash':DASH_RUNS,'unassigned':UNASSIGNED_RUNS,
    'unassigned_candidates':{250:['dash'],257:['dash'],258:['dash'],259:['dash'],260:['dash'],261:['dash'],262:['dash']},
    'unassigned_reasons':{
        250:'Pale purple material between broken bodies; dash association unresolved.',
        257:'Purple/cyan mixed upper boundary of broken purple body; possible dash contribution only.',
        258:'Pale purple material between broken bodies; dash association unresolved.',
        259:'Visible blue crossing material dominated by cyan; possible purple dash contribution unresolved.',
        260:'Visible blue/purple crossing material; possible purple dash contribution unresolved.',
        261:'Visible blue/purple crossing material below purple body; possible dash contribution unresolved.',
        262:'Visible blue/purple crossing material below purple body; possible dash contribution unresolved.',
    },
    'raw_blocks':[{'display_region':'F9-Im1','box':[243,0,263,88],'untruncated':True,'receipt':'818552; own complete exact RGB display, all88contextrows x243..262, only exact white omitted.'}],
    'identity_basis':'Confirmed nine-bolt purple, solid Spring and broken Shell; native strip and full composed page inspected. Same-color overlap retained once; clipping not a physical endpoint.',
}
CONFIG['unassigned_candidates'].update({263:['dash'],265:['dash'],269:['dash'],273:['dash'],279:['dash']})
CONFIG['unassigned_reasons'].update({263:'Purple/cyan mixed lower edge of broken purple body; possible dash contribution only.',265:'Pale purple material between broken bodies; dash membership unresolved.',269:'Pale purple material between broken bodies; dash membership unresolved.',273:'Pale purple material between broken bodies; dash membership unresolved.',279:'Pale top-edge tail; possible purple dash membership, not a physical endpoint.'})
CONFIG['raw_blocks'] += [{'display_region':'F9-Im1','box':[263,0,283,88],'untruncated':True,'receipt':'3c82b3; own complete all88row exact RGB display x263..282, only exact white omitted.'}]
CONFIG['unassigned_candidates'].update({294:['dash'],297:['dash'],301:['dash'],304:['dash'],310:['dash'],322:['dash']})
CONFIG['unassigned_reasons'].update({294:'Gray-pale top-edge onset before purple broken body; possible dash membership.',297:'Pale top-edge purple material between broken bodies; dash membership unresolved.',301:'Pale upper fragment after d08, separate from lower d09 onset; only dash could own it.',304:'Pale purple material between broken bodies; dash membership unresolved.',310:'Pale purple material between broken bodies; dash membership unresolved.',322:'Pale purple material between broken bodies; dash membership unresolved.'})
CONFIG['raw_blocks'] += [
    {'display_region':'F9-Im1','box':[283,0,303,88],'untruncated':True,'receipt':'1bdc67; own all88row exact RGB display x283..302, only exact white omitted.'},
    {'display_region':'F9-Im1','box':[303,0,323,88],'untruncated':True,'receipt':'d6ee41; own all88row exact RGB display x303..322, only exact white omitted.'},
]
CONFIG['unassigned_candidates'].update({326:['dash'],327:['dash'],328:['dash'],329:['dash'],332:['dash'],335:['solid'],338:['dash'],339:['dash'],340:['dash'],341:['dash'],342:['dash']})
CONFIG['unassigned_reasons'].update({326:'Pale purple material between broken bodies; possible dash only.',327:'Blue/purple mixed crossing with cyan broken body; possible purple dash only.',328:'Blue/purple mixed crossing with cyan broken body; possible purple dash only.',329:'Blue/purple mixed crossing with cyan broken body; possible purple dash only.',332:'Pale purple material between broken bodies; possible dash only.',335:'Purple/blue lower boundary of purple solid beside cyan broken line; only solid could own this band.',338:'Pale purple material between broken bodies; possible dash only.',339:'Blue/purple mixed crossing with cyan broken body; possible purple dash only.',340:'Blue/purple mixed crossing with cyan broken body; possible purple dash only.',341:'Pale purple material after crossing; dash membership unresolved.',342:'Pale purple material between broken bodies; possible dash only.'})
CONFIG['raw_blocks'] += [{'display_region':'F9-Im1','box':[323,0,343,88],'untruncated':True,'receipt':'ddcfc3; own all88row exact RGB display x323..342, only exact white omitted.'}]
CONFIG['unassigned_candidates'].update({345:['dash'],348:['dash'],349:['dash'],350:['dash'],351:['dash'],354:['dash'],355:['dash'],370:['solid'],371:['solid'],372:['solid'],373:['solid'],374:['solid']})
CONFIG['unassigned_reasons'].update({345:'Pale purple upper tail separate from lower d18 onset; only dash possible.',348:'Blue/purple mixed crossing with solid cyan; possible purple dash only.',349:'Blue/purple mixed crossing with solid cyan; possible purple dash only.',350:'Blue/purple upper boundary of purple broken body; possible dash only.',351:'Pale separate onset below broken purple body; possible dash only.',354:'Two pale purple fragments: body tail and bottom-edge material; only dash possible, no physical endpoint identified.',355:'Pale purple bottom-edge material; possible dash membership, not physical endpoint.',370:'Purple/gray-green boundary at green crossing; possible purple solid only.',371:'Purple/gray-green boundary at green crossing; possible purple solid only.',372:'Gray-purple mixed crossing band; possible purple solid contribution unresolved.',373:'Gray-green mixed crossing band; possible purple solid contribution unresolved, no hidden route reconstruction.',374:'Gray-green mixed crossing band; possible purple solid contribution unresolved, no hidden route reconstruction.'})
CONFIG['raw_blocks'] += [
    {'display_region':'F9-Im1','box':[343,0,363,88],'untruncated':True,'receipt':'d8136d; own all88row exact RGB display x343..362, only exact white omitted.'},
    {'display_region':'F9-Im1','box':[363,0,377,88],'untruncated':True,'receipt':'aab7cb; own all88row exact RGB display x363..376, only exact white omitted.'},
]
CONFIG['notes']='Full 11792-cell context x243..376 rows0..87 read in seven finite untruncated original exact-white-only-omission blocks. One solid local descent piece and 20 local broken bodies are manual selections. Top/bottom clipping does not identify physical endpoints; target ending in mixed green/purple material does not reconstruct a hidden purple route. Candidate-route uncertainty is explicit per band; no same-column default to both styles. Empty route records follow full contextual inspection and do not establish physical absence. Native ink only, not physical metrics, human sample acceptance, or mechanistic conclusions. Context reuse by other regions is not independent corroboration.'
if __name__ == '__main__': run(CONFIG,__file__)
