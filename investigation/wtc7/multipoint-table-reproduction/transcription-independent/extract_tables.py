# Read-only extraction aid; prints JSON and never writes files.
# Extracted tokens were separately checked against rendered source pages.
import hashlib,json,re
from pathlib import Path
import pdfplumber
source=Path("/Users/admin/docs/911-worktrees/sherlock-wtc7-investigation/research/sherlock-wtc7-investigation/luna-reevaluation-2026-09-19/chandler-walter-szamboti-2023.pdf")
sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha=="cb9d5c59010d28444f946f29b7ee4fb1fdaab24264d6cac940c092d893310394"
specs={
47:{"title":"All Camera 2 Points Vertical Positions and Velocities vs. Time","rows":70,"top":115,"bottom":695,"tb":(35,60),"headers":[
("ref_building_x","Ref Building","x",60,90),("ref_building_y","Ref Building","y",90,118),
("ne_corner_y","NE Corner","y",312,345),("ne_corner_v","NE Corner","v",345,378),
("ec_roofline_y","EC Roofline","y",378,412),("ec_roofline_v","EC Roofline","v",412,444),
("wc_roofline_y","WC Roofline","y",444,478),("wc_roofline_v","WC Roofline","v",478,511),
("nw_corner_y","NW Corner","y",511,545),("nw_corner_v","NW Corner","v",545,580)],
"excluded":["E Penthouse","N Screen Wall","W Penthouse"],
"footnote":"Start times of descent are bolded and outlined."},
50:{"title":"All Western Camera Points Vertical Positions vs. Time","rows":25,"top":126,"bottom":455,"tb":(72,104),"headers":[
("reference_point_y","Reference Point","y",104,180),
("nw_corner_y","NW Corner","y",180,216),("nw_corner_relative_y","NW Corner","relative y",216,261),
("center_y","Center","y",261,299),("center_relative_y","Center","relative y",299,345),("center_adjusted_y","Center","adjusted y",345,396),
("sw_corner_y","SW Corner","y",396,430),("sw_corner_relative_y","SW Corner","relative y",430,479),("sw_corner_adjusted_y","SW Corner","adjusted y",479,530)],
"excluded":[],"footnote":"Relative y: Position in relation to reference point. Adjusted y: Position in relation to reference point adjusted to a uniform roofline height. Start times of descent are bolded and outlined."}
}
out={}
with pdfplumber.open(source) as pdf:
 for page,spec in specs.items():
  words=[w for w in pdf.pages[page-1].extract_words() if spec["top"]<=w["top"]<spec["bottom"]]
  times=sorted([w for w in words if spec["tb"][0]<=w["x0"]<spec["tb"][1]],key=lambda w:w["top"])
  assert len(times)==spec["rows"],(page,len(times))
  rows=[]
  for i,tw in enumerate(times,1):
   assert re.fullmatch(r"-?\d+\.\d+",tw["text"])
   same=[w for w in words if abs(w["top"]-tw["top"])<0.5]
   row={"source_row":i,"time_s":tw["text"],"row_top_pdf_points":round(tw["top"],3)}
   for key,group,label,x0,x1 in spec["headers"]:
    cells=[w["text"] for w in same if x0<=w["x0"]<x1]
    assert len(cells)<=1,(page,i,key,cells)
    row[key]=cells[0] if cells else None
    assert row[key] is None or re.fullmatch(r"-?\d+\.\d+",row[key])
   rows.append(row)
  out[str(page)]={"schema":"independent-printed-table-transcription-v1","source_path":str(source),"source_sha256":sha,"pdf_page_1based":page,"printed_page":page,"title":spec["title"],"time_header":"t","numeric_token_policy":"All printed numeric tokens are strings; blank source cells are null. No recomputation or interpolation.","locator_policy":"source_row is one-based from the first numeric row; row_top_pdf_points measures down from the PDF page top. Combine source_row, time_s and header key to locate each cell.","headers":[{"key":key,"group":group,"label":label} for key,group,label,x0,x1 in spec["headers"]],"excluded_column_groups":spec["excluded"],"footnote":spec["footnote"],"rows":rows}
print(json.dumps(out))
