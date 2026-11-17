import sys
from zipfile import ZipFile
import struct
class Bit:
 def __init__(self,b):self.b=b;self.i=0
 def u(self,n):
  v=0
  for _ in range(n):v=v*2+((self.b[self.i//8]>>(7-self.i%8))&1);self.i+=1
  return v
 def s(self,n):
  v=self.u(n);return v-(1<<n) if n and v&(1<<(n-1)) else v
def mat(x):
 a=Bit(x)
 if a.u(1):n=a.u(5);a.s(n);a.s(n)
 if a.u(1):n=a.u(5);a.s(n);a.s(n)
 n=a.u(5);return a.s(n),a.s(n)
def tags(b,i):
 while i+2<=len(b):
  h=struct.unpack_from('<H',b,i)[0];i+=2;t=h>>6;l=h&63
  if l==63:l=struct.unpack_from('<I',b,i)[0];i+=4
  if i+l>len(b):break
  yield t,b[i:i+l];i+=l
  if t==0:break
with ZipFile(sys.argv[1]) as z:b=z.read('UA93.swf')
for typ,x in tags(b,8+((5+4*(b[8]>>3)+7)//8)+4):
 if typ!=39 or struct.unpack_from('<H',x,0)[0]!=1369:continue
 frame=1
 for t,y in tags(x,4):
  if t==1:frame+=1
  if t==26 and len(y)>=5 and y[0]&2:
   char=struct.unpack_from('<H',y,3)[0];depth=struct.unpack_from('<H',y,1)[0]
   if char in {1034,1357,1358,1359,1360}:
    xy=mat(y[5:]) if y[0]&4 else None
    print('frame',frame,'depth',depth,'character',char,'translation_twips',xy,'flags',hex(y[0]))
