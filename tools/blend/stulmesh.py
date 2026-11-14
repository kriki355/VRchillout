import sys,struct,json; sys.path.insert(0,'/home/claude/blend'); from blend import Blend
import numpy as np
b=Blend('/home/claude/newobj/dec/stul.blend'); d=b.d
me=[x for x in b.blocks if x['code']==b'ME\x00\x00'][0]; o=me['off']; ao=o+b.layout('Mesh')['attribute_storage'][0]
ptr=struct.unpack('<Q',d[ao:ao+8])[0]; num=struct.unpack('<i',d[ao+8:ao+12])[0]; blk=b.byold[ptr]
def cstr(p): bb=b.byold.get(p); return d[bb['off']:bb['off']+bb['len']].split(b'\0')[0].decode()
A={}
for i in range(num):
    base=blk['off']+i*24; name=cstr(struct.unpack('<Q',d[base:base+8])[0]); dp=struct.unpack('<Q',d[base+16:base+24])[0]; arr=b.byold[dp]
    ap=struct.unpack('<Q',d[arr['off']:arr['off']+8])[0]; db=b.byold[ap]; A[name]=d[db['off']:db['off']+db['len']]
pos=np.frombuffer(A['position'],'<f4').reshape(-1,3); cv=np.frombuffer(A['.corner_vert'],'<i4'); uv=np.frombuffer(A['UVMap'],'<f4').reshape(-1,2); mi=np.frombuffer(A['material_index'],'<i4')
po=b.byold[b.read(o,'Mesh','poly_offset_indices')]; offs=np.frombuffer(d[po['off']:po['off']+po['len']],'<i4')
print(pos.min(0),pos.max(0),len(offs),np.bincount(mi))
np.savez('/home/claude/blend/stul.npz',pos=pos,cv=cv,uv=uv,mi=mi,offs=offs)
