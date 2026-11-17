import sys
import struct
from zipfile import ZipFile
class Bits:
 def __init__(self,b,bit=0): self.b=b;self.p=bit
 def get(self,n):
  v=0
  for _ in range(n):v=(v<<1)|((self.b[self.p//8]>>(7-self.p%8))&1);self.p+=1
  return v
 def align(self):self.p=(self.p+7)//8*8
 def skiprect(self):
  n=self.get(5);self.get(4*n);self.align()
 def skipmatrix(self):
  if self.get(1):n=self.get(5);self.get(2*n)
  if self.get(1):n=self.get(5);self.get(2*n)
  n=self.get(5);self.get(2*n);self.align()
 def byte(self):self.align();return self.get(8)
 def uint16(self):return self.byte()|(self.byte()<<8)
def tags(b):
 i=8+((5+4*(b[8]>>3)+7)//8)+4
 while i+2<=len(b):
  h=struct.unpack_from('<H',b,i)[0];i+=2;t=h>>6;l=h&63
  if l==63:l=struct.unpack_from('<I',b,i)[0];i+=4
  yield t,b[i:i+l];i+=l
  if t==0:break
with ZipFile(sys.argv[1]) as z:b=z.read('UA93.swf')
ts=list(tags(b));fonts={}
for typ,x in ts:
 if typ!=48:continue
 try:
  fid=struct.unpack_from('<H',x,0)[0];fl=x[2];namelen=x[4];pos=5+namelen;count=struct.unpack_from('<H',x,pos)[0];pos+=2
  wideoff=bool(fl&8);widecode=bool(fl&4);width=4 if wideoff else 2
  fmt='<I' if wideoff else '<H';off=struct.unpack_from(fmt,x,pos+count*width)[0];code=pos+off
  fonts[fid]=[struct.unpack_from('<H',x,code+j*2)[0] if widecode else x[code+j] for j in range(count)]
 except Exception as e: print('font error',type(e).__name__)
out=[];errors=0
for typ,x in ts:
 if typ not in (11,33):continue
 try:
  rd=Bits(x,16);rd.skiprect();rd.skipmatrix();gb=rd.byte();ab=rd.byte();fid=None;txt=''
  while True:
   rd.align();fl=rd.byte()
   if not fl:break
   if fl&8:fid=rd.uint16()
   if fl&4: rd.get(32 if typ==33 else 24)
   if fl&1:rd.get(16)
   if fl&2:rd.get(16)
   if fl&8:rd.get(16)
   count=rd.byte()
   for j in range(count):
    glyph=rd.get(gb);rd.get(ab);code=fonts.get(fid,[]);txt+=chr(code[glyph]) if glyph<len(code) else '?'
   rd.align()
  if txt:out.append((struct.unpack_from('<H',x,0)[0],txt))
 except Exception:errors+=1
print('fonts',len(fonts),'text tags',len(out),'errors',errors)
for cid,t in out:
 if cid in {1034,1357,1358,1359,1360}:print('character',cid,repr(t))
