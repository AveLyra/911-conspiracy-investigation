"""Primary manual F6-Im3 reading; literal run expansion only, no RGB selection."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHORITY_EXPECTED = {
    '../../../CHARTER.md': ('54a4a23558a6b1ed756d3398e9e58d0972c6e531aadef5cd4027f29c4b9756bd', 24068),
    '../../../../../../../911/AGENTS.md': ('934437bfc0ddbe522cc73461819593706d12c0644cb306d263d9f1fe3914a857', 15240),
    '../../../../../../../911/WORKFLOW.md': ('17c41f8e81bb419a5a740a4ec8bb1984cb29c381d26ff8d54cec679f6ac6637a', 5868),
    '../../../../../../../911/START-HERE.md': ('b291da2b9ab3f1a8e9e69ff5a5d930c689ff2d45a6b2ce06a521e76295fbd560', 6383),
    '../../../../../../../../.codex/skills/evidence-falsification-auditor/SKILL.md': ('7894e7c6150319ec9591ec39ee1d11c3687f37deaf494d8a7c97b515f29c48a2', 4215),
    '../../../../../../../../.codex/skills/source-of-truth-guardian/SKILL.md': ('d283182d3b1f493001ad8952102ff70ebf4d7d0575cbfa1891a38df80e313ab5', 4218),
}

# Inclusive x ranges, then literal inclusive y ranges. Each entry was chosen
# from the finite raw displays, with whole-strip/page orientation.
SOLID = [
    (146,146,'87','85-86','s-rise-a'),
    (147,147,'85-87','84','s-rise-a'),
    (148,148,'83-84','81-82,85-86','s-rise-a'),
    (149,149,'80-82','83','s-rise-a'),
    (150,150,'80','79,81','s-rise-a'),
    (169,169,'27-29','26,30','s-rise-b'),
    (170,170,'24-27','23,28','s-rise-b'),
    (171,171,'22-25','21,26','s-rise-b'),
    (172,172,'20-22','19,23-24','s-rise-b'),
    (173,173,'18-20','17,21-22','s-rise-b'),
    (174,174,'15-18','14,19','s-rise-b'),
    (175,175,'12-16','11,17','s-rise-b'),
    (176,176,'9-13','8,14','s-rise-b'),
    (177,177,'7-10','6,11-12','s-rise-b'),
    (178,178,'3-5','1-2,6-8','s-rise-b'),
    (179,179,'1-4','0,5-6','s-rise-b'),
    (366,366,'7-9','10','s-fall-a'),
    (367,367,'8-10','11-12','s-fall-a'),
    (368,368,'9-12','8,13','s-fall-a'),
    (369,369,'9-14','8,15','s-fall-a'),
    (370,370,'13-15','12,16','s-fall-a'),
    (371,371,'15-17','14,18','s-fall-a'),
    (372,372,'17-19','16,20','s-fall-a'),
    (373,373,'18-20','17,21','s-fall-a'),
    (374,374,'20-22','19,23','s-fall-a'),
    (375,375,'22-24','21,25','s-fall-a'),
    (376,376,'24-26','23,27','s-fall-a'),
    (377,377,'25-27','24,28','s-fall-a'),
    (378,378,'27-29','26,30','s-fall-a'),
    (379,379,'28-31','27,32','s-fall-a'),
    (380,380,'30-33','29,34','s-fall-a'),
    (381,381,'32-34','31,35','s-fall-a'),
    (382,382,'34-36','33,37','s-fall-a'),
    (383,383,'35-38','34,39','s-fall-a'),
    (384,384,'37-39','36','s-fall-a'),
    (386,386,'41-43','40,44','s-fall-b'),
    (387,387,'43-45','42,46','s-fall-b'),
    (388,388,'45-47','44,48','s-fall-b'),
    (389,389,'46-48','45,49','s-fall-b'),
    (390,390,'48-51','47,52','s-fall-b'),
    (391,391,'50-52','49,53','s-fall-b'),
    (392,392,'51-54','50,55','s-fall-b'),
    (393,393,'53-56','52,57','s-fall-b'),
    (394,394,'56-58','55,59','s-fall-b'),
    (395,395,'57-60','56,61','s-fall-b'),
    (396,396,'59-61','58,62','s-fall-b'),
    (397,397,'61-63','60,64','s-fall-b'),
    (398,398,'63-65','62,66','s-fall-b'),
    (399,399,'64-67','63,68','s-fall-b'),
    (400,400,'66-69','65,70','s-fall-b'),
    (401,401,'68-70','67,71','s-fall-b'),
    (402,402,'70-72','69,73','s-fall-b'),
    (403,403,'72-74','71,75','s-fall-b'),
]
DASH = [
    (152,152,'87','86','d-rise-01'),
    (153,153,'87','86','d-rise-01'),
    (154,154,'83-87','82','d-rise-01'),
    (155,155,'85-87','84','d-rise-01'),
    (165,165,'86-87','85','d-rise-02'),
    (166,166,'84-86','83,87','d-rise-02'),
    (170,170,'80-85','79,86','d-rise-03'),
    (171,171,'83-86','82,87','d-rise-03'),
    (180,180,'84-87','82-83','d-rise-04'),
    (181,181,'82-86','81,87','d-rise-04'),
    (182,182,'81-82','80,83','d-rise-04'),
    (183,183,'76-77','75,78','d-rise-04'),
    (184,184,'72-77','71,78','d-rise-04'),
    (185,185,'72-74','71,75-76','d-rise-04'),
    (186,186,'64-67','68','d-rise-05'),
    (187,187,'64','65-66','d-rise-05'),
    (189,189,'61-62','63-64','d-rise-06'),
    (190,190,'62-64','61,65','d-rise-06'),
    (191,191,'','63-65','d-rise-06'),
    (191,191,'68','67,69','d-rise-07'),
    (192,192,'68-70','67','d-rise-07'),
    (193,193,'69-70','68,71','d-rise-07'),
    (199,199,'62-64','61,65','d-rise-08'),
    (200,200,'54-55','53,56','d-rise-09'),
    (201,201,'51-55','50,56','d-rise-09'),
    (202,202,'50-52','49,53','d-rise-09'),
    (203,203,'','50-51','d-rise-09'),
    (205,205,'43-45','42','d-rise-10'),
    (206,206,'41-44','40','d-rise-10'),
    (207,207,'41-42','40,43','d-rise-10'),
    (207,207,'','35-37','d-rise-11'),
    (208,208,'33-37','32','d-rise-11'),
    (209,209,'32-35','31,36','d-rise-11'),
    (210,210,'','31-34','d-rise-11'),
    (212,212,'27-28','26,29','d-rise-12'),
    (213,213,'25-28','24','d-rise-12'),
    (214,214,'23-26','22,27','d-rise-12'),
    (215,215,'23-24','22,25','d-rise-12'),
    (216,216,'17-19','16','d-rise-13'),
    (217,217,'14-17','13,18','d-rise-13'),
    (218,218,'13-15','12,16','d-rise-13'),
    (219,219,'','13-15','d-rise-13'),
    (220,220,'8-9','7,10','d-rise-14'),
    (221,221,'5-9','4,10','d-rise-14'),
    (222,222,'4-7','3,8','d-rise-14'),
    (222,222,'0','1','d-rise-15'),
    (223,223,'0','1','d-rise-15'),
    (224,224,'','0','d-rise-15'),
    (366,366,'4-5','3','d-fall-01'),
    (370,370,'18-21','17,22-23','d-fall-02'),
    (371,371,'20-23','19,24','d-fall-02'),
    (372,372,'27-29','26,30','d-fall-03'),
    (373,373,'28-31','27,32','d-fall-03'),
    (374,374,'30-32','29,33','d-fall-03'),
    (375,375,'32','31,33','d-fall-03'),
    (377,377,'','35-37','d-fall-04'),
    (378,378,'36-38','35,39','d-fall-04'),
    (379,379,'37-41','36,42','d-fall-04'),
    (380,380,'40','38-39,41','d-fall-04'),
    (381,381,'45','44,46','d-fall-05'),
    (382,382,'44-45','43,46','d-fall-05'),
    (383,383,'42-45','46','d-fall-05'),
    (384,384,'42-43','44','d-fall-05'),
    (386,386,'35-37','34,38','d-shoulder-01'),
    (387,387,'35-37','34','d-shoulder-01'),
    (388,388,'35-37','34,38','d-shoulder-01'),
    (389,389,'37-38','36','d-shoulder-01'),
    (390,390,'','42','d-shoulder-02'),
    (391,391,'41-42','43','d-shoulder-02'),
    (394,394,'32-34','31,35','d-shoulder-03'),
    (395,395,'30-34','29,35','d-shoulder-03'),
    (396,396,'29-31','28,32','d-shoulder-03'),
    (397,397,'29-31','28','d-shoulder-03'),
    (398,398,'34-35','33,36','d-shoulder-04'),
    (399,399,'34-38','33,39','d-shoulder-04'),
    (400,400,'37-39','36,40','d-shoulder-04'),
    (401,401,'38-39','37,40','d-shoulder-04'),
    (402,402,'34','33,35','d-shoulder-05'),
    (403,403,'31-34','30,35','d-shoulder-05'),
    (404,404,'30-32','33','d-shoulder-05'),
    (406,406,'24-25','23,26','d-shoulder-06'),
    (407,407,'24-26','23,27','d-shoulder-06'),
    (408,408,'25-27','24,28','d-shoulder-06'),
    (409,409,'','26-27','d-shoulder-06'),
    (409,409,'31','30,32','d-shoulder-07'),
    (410,410,'31-33','30','d-shoulder-07'),
    (411,411,'32-34','31','d-shoulder-07'),
    (412,412,'31-33','30,34','d-shoulder-07'),
    (413,413,'31-32','30,33','d-shoulder-07'),
    (415,415,'22-24','21,25','d-shoulder-08'),
    (416,416,'21-22','23','d-shoulder-08'),
    (417,417,'','24-25','d-shoulder-09'),
    (418,418,'24-27','23,28','d-shoulder-09'),
    (419,419,'25-29','24','d-shoulder-09'),
    (420,420,'28-29','27,30','d-shoulder-09'),
    (422,422,'31-32','30,33','d-shoulder-10'),
    (423,423,'29-32','28','d-shoulder-10'),
    (424,424,'29-30','28,31','d-shoulder-10'),
    (425,425,'29','30','d-shoulder-10'),
    (427,427,'35','34,36','d-terminal-01'),
    (428,428,'36-39','35,40','d-terminal-01'),
    (429,429,'37-40','36,41','d-terminal-01'),
    (430,430,'','43-44','d-terminal-02'),
    (431,431,'43','44','d-terminal-02'),
    (432,432,'43','44','d-terminal-02'),
    (437,437,'48-51','47,52','d-terminal-03'),
    (439,439,'56-59','55','d-terminal-04'),
]
# Candidate bands intentionally carry no unique F6 pixel ownership. They
# remain separate from all attributed cells, including pale and mixed colors.
BANDS = [
    (151,151,'76-78','solid','rise-mixed-green-orange'),
    (152,152,'72-76','solid','rise-mixed-green-orange'),
    (153,153,'69-73','solid','rise-mixed-green-orange'),
    (154,154,'61-67','solid','rise-mixed-green-purple'),
    (155,155,'58-64','solid','rise-mixed-green-purple'),
    (156,156,'53-61','solid','rise-mixed-green-purple'),
    (157,157,'50-59','solid','rise-mixed-green-purple'),
    (158,158,'46-54','solid','rise-mixed-green-purple'),
    (159,159,'44-52','solid','rise-mixed-green-purple'),
    (160,160,'40-48','solid','rise-mixed-green-purple'),
    (161,161,'38-47','solid','rise-mixed-green-purple'),
    (162,162,'36-42','solid','rise-mixed-green-purple'),
    (163,163,'36-41','solid','rise-mixed-green-purple'),
    (164,164,'32-39','solid','rise-green-blue-ownership-unknown'),
    (165,165,'29-35','solid','rise-green-blue-ownership-unknown'),
    (166,166,'25-34','solid','rise-green-blue-ownership-unknown'),
    (167,167,'25-30','solid','rise-green-blue-ownership-unknown'),
    (168,168,'26-30','solid','rise-mixed-green-orange'),
    (180,180,'0-3','solid','source-top-cyan-mix'),
    (156,156,'86-87','dash','dash-purple-contact'),
    (167,167,'76-80','dash','dash-orange-contact'),
    (168,168,'75-78','dash','dash-orange-contact'),
    (169,169,'74-77','dash','dash-orange-contact'),
    (169,169,'80-82','dash','separate-pale-red-body'),
    (185,185,'65-69','dash','dash-orange-contact'),
    (186,186,'60-63','dash','dash-orange-contact'),
    (187,187,'60-63','dash','dash-orange-contact'),
    (188,188,'58-61','dash','dash-orange-contact'),
    (189,189,'58-60','dash','dash-orange-contact'),
    (194,194,'68-70','dash','dash-green-contact'),
    (198,198,'62-64','dash','dash-green-contact'),
    (200,200,'61-63','dash','dash-green-contact'),
    (204,204,'44-46','dash','dash-orange-contact'),
    (208,208,'40-42','dash','dash-orange-contact'),
    (211,211,'27-29','dash','isolated-pale-red-ownership'),
    (361,361,'0-1','both','top-red-blue-style-contact'),
    (362,362,'0-5','both','top-red-blue-style-contact'),
    (363,363,'2-5','both','top-red-blue-style-contact'),
    (364,364,'3-6','both','top-red-blue-style-contact'),
    (365,365,'4-8','both','red-style-contact'),
    (366,366,'6','both','red-style-contact'),
    (367,367,'4-6','dash','red-blue-contact'),
    (368,368,'4-7','dash','red-blue-contact'),
    (384,384,'40-41','both','red-style-contact'),
    (385,385,'37-43','both','red-style-contact'),
    (392,392,'38-42','dash','red-blue-shoulder-contact'),
    (393,393,'38-41','dash','red-blue-shoulder-contact'),
    (394,394,'37-41','dash','red-blue-shoulder-contact'),
    (404,404,'73-77','solid','red-purple-descent-contact'),
    (405,405,'72-79','solid','red-purple-descent-contact'),
    (406,406,'76-81','solid','red-purple-descent-contact'),
    (407,407,'78-83','solid','red-purple-descent-contact'),
    (408,408,'79-84','solid','red-purple-descent-contact'),
    (409,409,'81-86','solid','red-purple-descent-contact'),
    (410,410,'82-87','solid','red-purple-descent-contact'),
    (411,411,'84-87','solid','red-purple-descent-contact'),
    (412,412,'85-87','solid','red-purple-descent-contact'),
    (413,413,'86-87','solid','red-purple-descent-contact'),
    (405,405,'24-30','dash','red-green-shoulder-contact'),
    (414,414,'23-28','dash','red-purple-shoulder-contact'),
    (426,426,'28-31','dash','red-cyan-shoulder-contact'),
    (433,433,'42-44','dash','red-cyan-terminal-contact'),
    (434,434,'41-45','dash','red-cyan-terminal-contact'),
    (435,435,'42-46','dash','red-cyan-terminal-contact'),
    (436,436,'46-50','dash','red-cyan-terminal-contact'),
    (438,438,'49-52','dash','red-cyan-terminal-contact'),
    (438,438,'55-62','dash','pale-red-purple-contact'),
    (439,439,'60-62','dash','red-purple-terminal-contact'),
]

BLOCKS = [([143,152], 'f047d2'), ([153,168], '3e7334'), ([169,188], '42b35e'),
    ([189,208],'0c670f'), ([209,228],'d43738'), ([229,258],'205b21'),
    ([259,298],'8ce306'), ([299,328],'85fce8'), ([329,348],'4a0e37'),
    ([349,368],'6dcd34'), ([369,388],'de6a83'), ([389,408],'84463a'),
    ([409,428],'c483da'), ([429,441],'dad394')]

def rows(text):
    result = []
    for item in text.split(',') if text else []:
        bounds = [int(n) for n in item.split('-')]
        result.extend(range(bounds[0], bounds[-1]+1))
    assert result == sorted(set(result))
    return result

def pin(path):
    raw = path.read_bytes()
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def flags(x, selected):
    return [name for name, yes in [('target_left',x==145 and bool(selected)),
        ('target_right',x==439 and bool(selected)), ('target_top',0 in selected),
        ('target_bottom',87 in selected)] if yes]

def inputs():
    result = {}
    for name in ['context01.json','context02.json']:
        result[name] = pin(HERE/name)
        assert result[name]['sha256'] == '8cdcf742827f98c2c1cb4d2a7920d248bc4b5ff99e8194e8f6c006cb8990d024'
        for rel, expected in json.loads((HERE/name).read_text())['inputs'].items():
            assert pin(HERE/rel) == expected, rel
            result[rel] = expected
    for rel, (sha256, byte_count) in AUTHORITY_EXPECTED.items():
        expected = dict(sha256=sha256, bytes=byte_count)
        assert pin(HERE/rel) == expected, rel
        result[rel] = expected
    return result

def build():
    before = inputs()
    # Completion is amended only after actual observations; never manufacture
    # empty records for columns outside these explicitly recorded blocks.
    inspected = {x for (a,b), receipt in BLOCKS for x in range(a,b+1)}
    target_x = sorted(inspected.intersection(range(145,440)))
    routes = {}
    for route, specs in [('solid',SOLID),('dash',DASH)]:
        selected = {}
        for xa,xb,c,f,frag in specs:
            for x in range(xa,xb+1):
                assert x in target_x
                selected.setdefault(x,[]).append({'fragment_id':frag,'core':rows(c),'fringe':rows(f)})
        output=[]
        for x in target_x:
            pieces=selected.get(x,[])
            c=sorted(y for p in pieces for y in p['core'])
            f=sorted(y for p in pieces for y in p['fringe'])
            bounds=flags(x,c+f)
            output.append(dict(x=x,core=c,fringe=f,fragment_id=pieces[0]['fragment_id'] if len(pieces)==1 else None,
                fragment_membership=pieces,status='boundary_truncated' if bounds else 'identified_local_fragment' if c else 'fringe_only' if f else 'no_attributable_cells',
                reason='Manually attributed visible red stroke; pale/mixed margins remain tentative.' if c or f else 'Context inspected; no confidently attributable F6 cells selected for this route at this column. This is not evidence of physical absence.',
                boundary_flags=bounds,unassigned_band_refs=[]))
        routes[route]=output
    bands=[]
    for number,(xa,xb,ys,candidate,why) in enumerate(BANDS):
        for x in range(xa,xb+1):
            band_id=f'primary-band-{number:03}-{x}'
            frag=f'u-{why}'
            f=rows(ys)
            candidates=['solid','dash'] if candidate=='both' else [candidate]
            bands.append(dict(x=x,band_id=band_id,core=[],fringe=f,fragment_id=frag,
                fragment_membership=[dict(fragment_id=frag,core=[],fringe=f)],status='identity_conflict',
                reason=why+'; candidate F6 ownership is unresolved among mixed, pale, or competing colored cells; no hidden red stroke is asserted.',
                boundary_flags=flags(x,f),candidate_routes=candidates))
            for route in candidates:
                row=next(r for r in routes[route] if r['x']==x)
                row['unassigned_band_refs'].append(band_id)
                if not row['core'] and not row['fringe']:
                    row['status']='identity_conflict'
                    row['reason']='Context inspected; candidate F6 cells retained in referenced unresolved band, without unique route ownership.'
    result=dict(region_id='F6-Im3',pair='F6',source='Im3.jpg',reader='primary',target_box=[145,0,440,88],context_box=[143,0,442,88],
        inputs=before,script_pin=pin(Path(__file__)),coverage=dict(full_context_inspected=inspected==set(range(143,442)),
            raw_context_cells=len(inspected)*88,raw_blocks=[dict(columns=xs,receipt=receipt) for xs,receipt in BLOCKS],
            actual_views=[dict(path='../../native-strips01/Im3.jpg',receipt='functions.exec image view before f047d2; native 741x88'),dict(path='../../render01/page-076.png',receipt='functions.exec image view before f047d2; full page displayed, tool resized 1700x2200 to1376x1780')],
            prior_knowledge='Current protocols and declared previous F5 context overlap only; no prior F5 or counterpart annotation read. Whole page/strip informed route-style orientation. Same-source AI reading, not blind selection or historical corroboration.',
            rows=[0,87],display_convention='Only exact RGB(255,255,255) omitted; all other cells shown, inclusive equal-RGB runs and gN grayscale shorthand.',
            uncompleted_context=[x for x in range(143,442) if x not in inspected]),
        routes=routes,unassigned_bands=bands,human_accepted=False,physical_support=None)
    assert before==inputs()
    return result

if __name__ == '__main__':
    result=build()
    target=HERE/'reader-primary.json'
    with target.open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    assert result['inputs']==inputs()
    print(json.dumps({'file':target.name,**pin(target)},sort_keys=True))
