import sys,struct,math,pickle,numpy as np
sys.path.insert(0,'/home/claude/blend'); from blend import Blend
b=Blend(sys.argv[1]); d=b.d
def cstr(p):
    bb=b.byold.get(p); return d[bb['off']:bb['off']+bb['len']].split(b'\0')[0].decode('utf-8','replace') if bb else ''
def fl(o,sname,field,n):
    off=b.layout(sname)[field][0]; return list(struct.unpack('<%df'%n,d[o+off:o+off+4*n]))
def idname(o): off=b.layout('ID')['name'][0] if 'name' in b.layout('ID') else 0; return d[o+off:o+off+66].split(b'\0')[0].decode('utf-8','replace')[2:]
def rmat(r):
    cx,sx=math.cos(r[0]),math.sin(r[0]); cy,sy=math.cos(r[1]),math.sin(r[1]); cz,sz=math.cos(r[2]),math.sin(r[2])
    Rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]]); Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]); Rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]]); return Rz@Ry@Rx
obs={}; 
for x in b.blocks:
    if x['code']==b'OB\x00\x00': obs[x['old']]=x
def local(x):
    o=x['off']; M=np.eye(4); M[:3,:3]=rmat(fl(o,'Object','rot',3))@np.diag(fl(o,'Object','size',3)); M[:3,3]=fl(o,'Object','loc',3); return M
def world(x):
    o=x['off']; M=local(x); p=b.read(o,'Object','parent')
    if p and p in obs: PI=np.array(fl(o,'Object','parentinv',16)).reshape(4,4).T; M=world(obs[p])@PI@M
    return M
def mesh_attrs(mo):
    ao=mo+b.layout('Mesh')['attribute_storage'][0]; ptr=struct.unpack('<Q',d[ao:ao+8])[0]; num=struct.unpack('<i',d[ao+8:ao+12])[0]; blk=b.byold[ptr]; A={}
    for i in range(num):
        base=blk['off']+i*24; name=cstr(struct.unpack('<Q',d[base:base+8])[0]); dp=struct.unpack('<Q',d[base+16:base+24])[0]; arr=b.byold.get(dp)
        if not arr: continue
        ap=struct.unpack('<Q',d[arr['off']:arr['off']+8])[0]; db=b.byold.get(ap)
        if db: A[name]=d[db['off']:db['off']+db['len']]
    return A
def matnames(o,sname,cnt_field='totcol'):
    n=b.read(o,sname,cnt_field); p=b.read(o,sname,'mat'); out=[]
    if p and n>0:
        blk=b.byold[p]
        for i in range(n):
            mp=struct.unpack('<Q',d[blk['off']+8*i:blk['off']+8*i+8])[0]; mb=b.byold.get(mp); out.append(idname(mb['off']) if mb else '?')
    return out
parts=[]
for old,x in obs.items():
    o=x['off']; dp=b.read(o,'Object','data'); mb=b.byold.get(dp)
    if not mb or mb['code']!=b'ME\x00\x00': continue
    mo=mb['off']; A=mesh_attrs(mo)
    if 'position' not in A: continue
    pos=np.frombuffer(A['position'],'<f4').reshape(-1,3).astype(float); cv=np.frombuffer(A['.corner_vert'],'<i4')
    po=b.byold[b.read(mo,'Mesh','poly_offset_indices')]; offs=np.frombuffer(d[po['off']:po['off']+po['len']],'<i4'); tp=b.read(mo,'Mesh','totpoly'); offs=offs[:tp+1] if tp and tp+1<=len(offs) else offs; offs=offs[offs<=len(cv)]
    mi=np.frombuffer(A['material_index'],'<i4') if 'material_index' in A else np.zeros(len(offs)-1,int)
    mats=matnames(mo,'Mesh') or ['?']
    W=world(x); P=(W[:3,:3]@pos.T).T+W[:3,3]
    tris=[];tm=[]
    for f in range(len(offs)-1):
        a,c=offs[f],offs[f+1]
        for j in range(a+1,c-1): tris.append((cv[a],cv[j],cv[j+1])); tm.append(mi[f] if f<len(mi) else 0)
    T=P[np.array(tris)]
    if np.linalg.det(W[:3,:3])<0: T=T[:,[0,2,1]]
    # Blender Z вверх → Y вверх, перед -Y → +Z
    T=T[:,:,[0,2,1]]*np.array([1,1,-1]); T=T[:,[0,2,1]]
    nm=idname(o); parts.append({'name':nm,'anc':[],'mats':mats,'P':T,'tm':np.array(tm)})
    print(nm,mats,len(T),T.reshape(-1,3).min(0).round(2),T.reshape(-1,3).max(0).round(2))
pickle.dump(parts,open(sys.argv[2],'wb'))
