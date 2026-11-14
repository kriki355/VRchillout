import sys,json,base64,math
import numpy as np
sys.path.insert(0,'/home/claude/fbx'); from extract2 import load
from packall import enc
ps=load('/home/claude/newobj/8de515fe-newobjects2/newobjects2/pechka.fbx')
# собираем все треугольники с материалами
T=[];M=[];names=[]
for p in ps:
    I=np.array(p['idx']).reshape(-1,3)
    for t,mi in zip(I,p['tmat']):
        T.append(p['pos'][t]); M.append(p['mats'][mi] if mi<len(p['mats']) else p['mats'][0])
T=np.array(T); M=np.array(M); allp=T.reshape(-1,3); mn=allp.min(0); mx=allp.max(0); print('n tris',len(T),mn.round(1),mx.round(1))
cs=float(sys.argv[1]) if len(sys.argv)>1 else 0.6
V=T.reshape(-1,3); key=np.floor((V-mn)/cs).astype(np.int64); _,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.reshape(-1,3)
# центры кластеров
nc=inv.max()+1; cen=np.zeros((nc,3)); cnt=np.zeros(nc); np.add.at(cen,inv.reshape(-1),V); np.add.at(cnt,inv.reshape(-1),1); cen/=cnt[:,None]
ok=(inv[:,0]!=inv[:,1])&(inv[:,1]!=inv[:,2])&(inv[:,0]!=inv[:,2]); inv=inv[ok]; Mk=M[ok]
srt=np.sort(inv,1); _,u=np.unique(np.concatenate([srt,np.searchsorted(np.unique(Mk),Mk)[:,None]],1),axis=0,return_index=True); inv=inv[u]; Mk=Mk[u]
print('decimated',len(inv))
json.dump({'cen':cen.tolist(),'tri':inv.tolist(),'mat':Mk.tolist(),'mn':mn.tolist(),'mx':mx.tolist()},open('/home/claude/fbx/pechka_dec.json','w'))
