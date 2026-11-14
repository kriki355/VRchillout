import sys,json,struct,base64,math
import numpy as np
sys.path.insert(0,'/home/claude/fbx'); from extract2 import load
def enc(P,N,U,I,name,mat):
    lo=P.min(0); hi=P.max(0)+1e-6
    q=np.clip(np.round((P-lo)/(hi-lo)*65534-32767),-32767,32767).astype('<i2')
    return {'name':name,'mat':mat,'lo':lo.round(5).tolist(),'hi':hi.round(5).tolist(),'p':base64.b64encode(q.tobytes()).decode(),
      'n':base64.b64encode(np.clip(np.round(N*127),-127,127).astype('i1').tobytes()).decode(),
      'u':base64.b64encode(np.clip(np.round(np.stack([U[:,0],1-U[:,1]],1)*16000+32000),0,65535).astype('<u2').tobytes()).decode(),
      'i':base64.b64encode(np.array(I,dtype='<u2').tobytes()).decode()}
def dedupe(P,N,U,I):
    key=np.round(np.concatenate([P*2000,N*50,U*4000],1)).astype(np.int64); _,first,inv=np.unique(key,axis=0,return_index=True,return_inverse=True)
    return P[first],N[first],U[first],inv.reshape(-1)[I]
def normalize(parts,height,rot90=False):
    allp=np.concatenate([p['pos'] for p in parts]); mn=allp.min(0); mx=allp.max(0); s=height/(mx[1]-mn[1])
    out=[]
    for p in parts:
        P=(p['pos']-np.array([(mn[0]+mx[0])/2,mn[1],(mn[2]+mx[2])/2]))*s; N=p['nrm'].copy()
        if rot90: P=np.stack([P[:,2],P[:,1],-P[:,0]],1); N=np.stack([N[:,2],N[:,1],-N[:,0]],1)
        out.append((p,P,N))
    return out,s
def packparts(norm):
    res=[]
    for p,P,N in norm:
        I=np.array(p['idx']).reshape(-1,3); tm=np.array(p['tmat']) if len(p['tmat'])==len(I) else np.zeros(len(I),int)
        for m in np.unique(tm):
            Ii=I[tm==m].reshape(-1); Pd,Nd,Ud,Id=dedupe(P,N,p['uv'],Ii); mn=p['mats'][m] if m<len(p['mats']) else p['mat']
            res.append(enc(Pd,Nd,Ud,Id,p['name']+'#'+str(m),mn))
    return res
if __name__=="__main__":
    R='/home/claude/newobj/7b2d2bb7-newobjects1/newobjects1/'
    out={}
    for key,f,h,rot in [('kreslo','newkreslo1.fbx',1.2,False),('stol1','newstol1.fbx',0.75,True),('stol2','newstol2.fbx',0.75,True),('stol3','newstol3.fbx',0.75,False),('pouf','pufik.fbx',0.45,False)]:
        ps=load(R+f); norm,s=normalize(ps,h,rot); out[key]=packparts(norm)
        allp=np.concatenate([P for _,P,_ in norm]); print(key,'size',(allp.max(0)-allp.min(0)).round(3),'verts',sum(len(P) for _,P,_ in norm))
    # стул из .blend
    z=np.load('/home/claude/blend/stul.npz'); pos=z['pos'].astype(float); cv=z['cv']; uv=z['uv'].astype(float); offs=z['offs']
    # Blender: Z вверх → в Y вверх: (x,y,z)->(x,z,-y)
    import os
    if os.environ.get('STULROT')=='z': pos=np.stack([pos[:,0],pos[:,2],-pos[:,1]],1)
    elif os.environ.get('STULROT')=='flip': pos=np.stack([pos[:,0],-pos[:,1],pos[:,2]],1)
    pos-=np.array([(pos[:,0].min()+pos[:,0].max())/2,pos[:,1].min(),(pos[:,2].min()+pos[:,2].max())/2])
    pos*=0.82/(pos[:,1].max()-pos[:,1].min())
    tris=[];tc=[]
    for f in range(len(offs)-1):
        a,b=offs[f],offs[f+1]
        for j in range(a+1,b-1): tris.append((cv[a],cv[j],cv[j+1])); tc.append((a,j,j+1))
    tris=np.array(tris); tc=np.array(tc)
    fn=np.cross(pos[tris[:,1]]-pos[tris[:,0]],pos[tris[:,2]]-pos[tris[:,0]]); fa=np.linalg.norm(fn,axis=1,keepdims=True); fn=fn/np.maximum(fa,1e-12)
    # автосглаживание 40°: нормаль угла = сумма нормалей соседних граней с близким направлением
    vf={}
    for t,(i0,i1,i2) in enumerate(tris):
        for v in (i0,i1,i2): vf.setdefault(v,[]).append(t)
    cos=math.cos(math.radians(40)); P=[];N=[];U=[];I=[]
    for t,(i0,i1,i2) in enumerate(tris):
        for k,v in enumerate((i0,i1,i2)):
            acc=sum((fn[o]*fa[o] for o in vf[v] if np.dot(fn[o],fn[t])>cos),np.zeros(3)); n=acc/max(np.linalg.norm(acc),1e-9)
            P.append(pos[v]); N.append(n); U.append(uv[tc[t][k]]); I.append(len(P)-1)
    P=np.array(P);N=np.array(N);U=np.array(U);I=np.array(I)
    Pd,Nd,Ud,Id=dedupe(P,N,U,I); out['stul']=[enc(Pd,Nd,Ud,Id,'stul','stul')]; print('stul size',(pos.max(0)-pos.min(0)).round(3),'verts',len(Pd),'tris',len(Id)//3)
    json.dump(out,open('/home/claude/fbx/loft.json','w'),separators=(',',':')); print('json',len(open('/home/claude/fbx/loft.json').read()))
    