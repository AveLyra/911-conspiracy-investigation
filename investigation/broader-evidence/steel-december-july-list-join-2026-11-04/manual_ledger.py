"""Manual visual identifier-cell transcription, not OCR normalization or a physical-object inventory."""
from pathlib import Path
import json
U=Path(__file__).resolve().parent
ADMIN={
3:'''A-0004 A-0007 A-0009 A-0016 A-0017 A-0023 A-0024 A-0039 A-0041 A-0043 A-0044
B-0024 B-0025 B-0026 B-0027 B-0028 B-0030 B-0031 B-0032 B-0034 B-0038 B-0041 B-0046 B-0047 B-0048 B-0050 B-0062
C-0011.001 C-0011.002 C-0011.003 C-0011.004 C-0011.005 C-0011.006 C-0011.007 C-0013 C-0021 C-0024 C-0033 C-0034 C-0035
E-0001 E-0002 E-0003 E-0004 E-0005 E-0006 E-0007 E-0009''',
4:'''E-0010 E-0011 E-0012 E-0013 E-0014 E-0015 E-0016 E-0017 E-0018 E-0019 E-0022 E-0024 E-0025 E-0026 E-0028 E-0029 E-0030 E-0031
F-0004 F-0006.001 F-0006.003 F-0006.004 F-0008 F-0009 F-0014 F-0021.000 F-0032.014
G-0011 G-0012 G-0016 G-0020 G-0033 G-0039 G-0041 G-0048 G-0050 G-0057 G-0058 G-0059 G-0060 G-0061 G-0062 G-0063 G-0065 G-0072 G-0073 G-0074 G-0075 G-0076 G-0077 G-0079 G-0080''',
5:'''G-0081 G-0082 G-0084 G-0085 G-0088 G-0089 G-0090 G-0091 G-0092 G-0093 G-0095 G-0097 G-0098 G-0100 G-0101 G-0102 G-0113 G-0114 G-0121 G-0134 G-0141 G-0144 G-0146 G-0147 G-0158
H-0040 H-0047 H-0048 H-0049 H-0050 H-0052 H-0053 H-0054 H-0055 H-0056 H-0057 H-0058 H-0059 H-0060 H-0061 H-0062 H-0063 H-0065 H-0067 H-0068 H-0069 H-0072 H-0073 H-0074 H-0075 H-0076 H-0078''',
6:'''H-0079 H-0081 H-0082 H-0083 H-0084 H-0087 H-0089 H-0092 H-0093 H-0094 H-0095 H-0096 H-0097 H-0098 H-0103 H-0104 H-0106 H-0108 H-0109 H-0110 H-0111 H-0114 H-0115 H-0116 H-0117 H-0119 H-0121 H-0122 H-0124 H-0125 H-0126 H-0127 H-0129 H-0130 H-0131 H-0132 H-0133 H-0138 H-0139 H-0141 H-0142 H-0156 H-0162
I-0067 I-0070 I-0072 I-0073 I-0074 I-0075 I-0076 I-0077 I-0078''',
7:'''I-0080 I-0081 I-0082 I-0083 I-0085 I-0087 I-0088 I-0089 I-0090 I-0091 I-0092 I-0093 I-0094 I-0095 I-0096 I-0098 I-0099 I-0100 I-0101 I-0102 I-0103 I-0104 I-0105 I-0106 I-0107 I-0108 I-0109 I-0110 I-0111 I-0112 I-0113 I-0114 I-0116 I-0117 I-0118 I-0121 I-0126 I-0128 I-0132 I-0133 I-0138 I-0139 I-0142 I-0143 I-0145 I-0147 I-0149 I-0150 I-0151 I-0152 I-0153 I-0154''',
8:'''I-0155 I-0158 I-0160 I-0166 I-0168 I-0171 I-0175 I-0176
J-0002 J-0003 J-0004 J-0008 J-0009 J-0010 J-0011
L-0001 L-0005 L-0006 L-0014 L-0025'''
}
NIST={
8:'''ASCE-3
B-1075
B-6152-1
B-6152-2
C-10
C-11
C-15
C-28
C-32
C-35
C-43
C-44
C-45
C-47 (not visbl on pc)
C-49 or S-6
C-54
C-55
C-61
C-62
C-64
C-67
C-68
C-71
C-73
C-74
C-75
C-78''',
9:'''C-79
C-80
C-82
C-89
C-91
C-93
C-95
C-97
C-99
C-100
C-101
C-102
C-104
C-105
C-117
C-118
C-124
C-126
C-129
C-130
C-133
C-142
C-143
C-145
C-146a
C-147
C-148
C-149
C-150
C-152
C-153
C-154
C-155
M-11
M-18
M-20
M-22
M-23
M-24
M-28
M-37
N-3
N-4
N-5
N-6
S-10 or C-17
U-4
n-0017
n-0033
n-022
n-141'''
}
rows=[]
for page in range(3,10):
    current=[]
    for label in ADMIN.get(page,'').split():
        current.append({'identifier_verbatim':label,'source_field':'Inventory Archive Item Number','source_namespace':'Port Authority WTC Artifacts'})
    for i,label in enumerate(NIST.get(page,'').splitlines(),1):
        current.append({'identifier_verbatim':label,'source_field':'NIST Number','source_namespace':'NIST Number as printed','row_in_NIST_section_on_page':i})
    for i,row in enumerate(current,1):
        row.update(physical_pdf_page=page,identifier_row_on_page=i,ledger_row=len(rows)+1,reading_status='visually_read_full_source_face')
        rows.append(row)
with (U/'DECEMBER-IDENTIFIER-ROWS.json').open('x') as f:json.dump(rows,f,indent=2);f.write('\n')
print(json.dumps({'rows':len(rows),'per_page':{p:len([r for r in rows if r['physical_pdf_page']==p]) for p in range(3,10)},'source_fields':{h:len([r for r in rows if r['source_field']==h]) for h in ['Inventory Archive Item Number','NIST Number']}}))
