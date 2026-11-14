import sys,json,math
import numpy as np
sys.path.insert(0,'/home/claude/fbx'); from packall import enc
D=json.load(open('/home/claude/fbx/pechka_dec.json')); cen=np.array(D['cen']); tri=np.array(D['tri']); mat=np.array(D['mat'])
up=sys.argv[1] if len(sys.argv)>1 else 'y'; H=float(sys.argv[2]) if len(sys.argv)>2 else 1.0
P=cen.copy()
if up=='z': P=np.stack([P[:,0],P[:,2],-P[:,1]],1)
if len(sys.argv)>3 and sys.argv[3]=='flipz': P[:,2]*=-1; P[:,0]*=-1
mn=P.min(0); mx=P.max(0); s=H/(mx[1]-mn[1]); P=(P-np.array([(mn[0]+mx[0])/2,mn[1],(mn[2]+mx[2])/2]))*s
print('size',((mx-mn)*s).round(3))
A=P[tri[:,0]];B=P[tri[:,1]];C=P[tri[:,2]]; fn=np.cross(B-A,C-A); fa=np.linalg.norm(fn,axis=1); fn=fn/np.maximum(fa[:,None],1e-12)
ax=np.argmax(np.abs(fn),1); bucket=ax*2+(fn[np.arange(len(fn)),ax]>0)
out=[]
for m in np.unique(mat):
    sel=np.where(mat==m)[0]; T=tri[sel]; b=bucket[sel]
    keys=np.stack([T.reshape(-1),np.repeat(b,3)],1); uk,inv=np.unique(keys,axis=0,return_inverse=True); inv=inv.reshape(-1)
    nrm=np.zeros((len(uk),3)); np.add.at(nrm,inv,np.repeat(fn[sel]*fa[sel][:,None],3,0)); nrm/=np.maximum(np.linalg.norm(nrm,axis=1,keepdims=True),1e-12)
    pos=P[uk[:,0]]
    It=inv.reshape(-1,3)
    for c in range(0,len(It),20000):
        t=It[c:c+20000]; u,ii=np.unique(t.reshape(-1),return_inverse=True); out.append(enc(pos[u],nrm[u],np.zeros((len(u),2)),ii,m,m))
json.dump(out,open('/home/claude/fbx/pechka.json','w'),separators=(',',':')); print('json',len(open('/home/claude/fbx/pechka.json').read()),'parts',len(out))
