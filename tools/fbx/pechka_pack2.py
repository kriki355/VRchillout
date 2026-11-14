import sys,json
import numpy as np
sys.path.insert(0,'/home/claude/fbx'); from packall import enc
D=json.load(open('/home/claude/fbx/pechka_dec.json')); cen=np.array(D['cen']); tri=np.array(D['tri']); mat=np.array(D['mat'])
cx=cen[tri].mean(1)[:,0]
sides={'L':cx<-60,'R':cx>=-60}; H={}
for k,m in sides.items():
    v=cen[np.unique(tri[m])]; H[k]=(v.max(0)-v.min(0)); print(k,'size units',H[k].round(1))
tall=max(H,key=lambda k:H[k][1]); s=1.75/H[tall][1]; print('tall',tall,'scale',s)
res={}; DBG={}
for k,msk in sides.items():
    T=tri[msk]; M=mat[msk]; used=np.unique(T); P=cen.copy(); mn=P[used].min(0); mx=P[used].max(0); P=(P-np.array([(mn[0]+mx[0])/2,mn[1],(mn[2]+mx[2])/2]))*s
    print(k,'size m',((mx-mn)*s).round(3))
    if k=='R': P=np.stack([-P[:,2],P[:,1],P[:,0]],1)
    P=np.stack([-P[:,0],-P[:,1],P[:,2]],1); yy=P[np.unique(T)][:,1]; P[:,1]-=yy.min()
    if k=='R': P=np.stack([-P[:,2],P[:,1],P[:,0]],1)
    DBG[k]=(P.copy(),T.copy(),M.copy())
    A=P[T[:,0]];B=P[T[:,1]];C=P[T[:,2]]; fn=np.cross(B-A,C-A); fa=np.linalg.norm(fn,axis=1); fn=fn/np.maximum(fa[:,None],1e-12)
    ax=np.argmax(np.abs(fn),1); bucket=ax*2+(fn[np.arange(len(fn)),ax]>0); out=[]
    for m in np.unique(M):
        sel=np.where(M==m)[0]; TT=T[sel]; b=bucket[sel]
        keys=np.stack([TT.reshape(-1),np.repeat(b,3)],1); uk,inv=np.unique(keys,axis=0,return_inverse=True); inv=inv.reshape(-1)
        nrm=np.zeros((len(uk),3)); np.add.at(nrm,inv,np.repeat(fn[sel]*fa[sel][:,None],3,0)); nrm/=np.maximum(np.linalg.norm(nrm,axis=1,keepdims=True),1e-12)
        pos=P[uk[:,0]]; It=inv.reshape(-1,3)
        for c in range(0,len(It),20000):
            t=It[c:c+20000]; u,ii=np.unique(t.reshape(-1),return_inverse=True); out.append(enc(pos[u],nrm[u],np.zeros((len(u),2)),ii,m+'#'+str(c),m))
    res[k]=out
json.dump(res,open('/home/claude/fbx/pechka2.json','w'),separators=(',',':')) if False else None
import pickle; pickle.dump(DBG,open('/home/claude/fbx/pech_dbg.pkl','wb'))
json.dump(res,open('/home/claude/fbx/pechka2.json','w'),separators=(',',':')); print(len(open('/home/claude/fbx/pechka2.json').read()))
