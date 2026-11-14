import sys, math, numpy as np
sys.path.insert(0,'/home/claude/fbx')
from fbxparse import parse, sub
def props(n):
    P=sub(n,'Properties70'); return {p['p'][0]:p['p'][4:] for p in (P['c'] if P else [])}
def _r(v):
    a=[math.radians(x) for x in v]
    def rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
    def ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
    def rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
    M=np.eye(4); M[:3,:3]=rz(a[2])@ry(a[1])@rx(a[0]); return M
def _t(v): M=np.eye(4); M[:3,3]=v; return M
def _s(v): return np.diag([v[0],v[1],v[2],1.0])
def lmat(pr,rot=None):
    g=lambda k,d=(0,0,0): list(pr.get(k,d))
    R=rot if rot is not None else g('Lcl Rotation')
    Rp=g('RotationPivot'); Sp=g('ScalingPivot')
    M=_t(g('Lcl Translation'))@_t(g('RotationOffset'))@_t(Rp)@_r(g('PreRotation'))@_r(R)@np.linalg.inv(_r(g('PostRotation')))@_t([-x for x in Rp])@_t(g('ScalingOffset'))@_t(Sp)@_s(g('Lcl Scaling',(1,1,1)))@_t([-x for x in Sp])
    return M
def geo(pr):
    g=lambda k,d=(0,0,0): list(pr.get(k,d))
    return _t(g('GeometricTranslation'))@_r(g('GeometricRotation'))@_s(g('GeometricScaling',(1,1,1)))
def load(path,override=None):
    override=override or {}
    top=parse(path); O=[t for t in top if t['n']=='Objects'][0]; C=[t for t in top if t['n']=='Connections'][0]
    objs={n['p'][0]:n for n in O['c']}; g2m={}; m2mat={}; par={}
    for c in C['c']:
        a,b=c['p'][1],c['p'][2]
        if a in objs and b in objs:
            ta,tb=objs[a]['n'],objs[b]['n']
            if ta=='Geometry' and tb=='Model': g2m[a]=b
            if ta=='Material': m2mat.setdefault(b,[]).append(objs[a]['p'][1].split('\x00')[0])
            if ta=='Model' and tb=='Model': par[a]=b
    nm=lambda i: objs[i]['p'][1].split('\x00')[0]
    def world(mid):
        M=lmat(props(objs[mid]),override.get(nm(mid))); p=par.get(mid)
        while p is not None: M=lmat(props(objs[p]),override.get(nm(p)))@M; p=par.get(p)
        return M
    def anc(mid):
        out=[]; p=par.get(mid)
        while p is not None: out.append(nm(p)); p=par.get(p)
        return out
    def hinge(name):
        for i in objs:
            if objs[i]['n']=='Model' and nm(i)==name: return world(i)
    load.hinge=hinge
    parts=[]
    for gid,mid in g2m.items():
        g=objs[gid]; M=world(mid)@geo(props(objs[mid]))
        if abs(np.linalg.det(M[:3,:3]))<1e-12: continue
        vs=sub(g,'Vertices'); pis=sub(g,'PolygonVertexIndex')
        if not vs or not pis: continue
        V=np.array(vs['p'][0],float).reshape(-1,3); PI=np.array(pis['p'][0],np.int64)
        if len(PI)<3: continue
        end=PI<0; vi=np.where(end,~PI,PI)
        start=np.zeros(len(PI),bool); start[0]=True; start[1:]=end[:-1]
        pid=np.cumsum(start)-1; sidx=np.flatnonzero(start); first=sidx[pid]
        k=np.arange(len(PI)); ok=(~start)&(~end)
        tri=np.stack([first[ok],k[ok],k[ok]+1],1)   # углы
        LM=sub(g,'LayerElementMaterial'); MI=np.array(sub(LM,'Materials')['p'][0]) if LM else np.zeros(1,int)
        mm=sub(LM,'MappingInformationType')['p'][0] if LM else 'AllSame'
        tm=MI[pid[tri[:,0]]] if (mm=='ByPolygon' and len(MI)>=pid.max()+1) else np.full(len(tri),MI[0] if len(MI) else 0)
        Pw=(M[:3,:3]@V.T).T+M[:3,3]
        P=Pw[vi[tri]]  # (t,3,3)
        if np.linalg.det(M[:3,:3])<0: P=P[:,[0,2,1]]
        mats=m2mat.get(mid) or ['?']
        parts.append({'anc':anc(mid),'name':objs[mid]['p'][1].split('\x00')[0],'mats':mats,'P':P,'tm':tm})
    return parts
def decimate(P,cell):
    # P (t,3,3) треугольники → кластеризация вершин
    if cell<=0: Q=P.reshape(-1,3)
    else:
        flat=P.reshape(-1,3); key=np.floor(flat/cell).astype(np.int64); _,inv=np.unique(key,axis=0,return_inverse=True); inv=inv.reshape(-1)
        cnt=np.bincount(inv); mean=np.stack([np.bincount(inv,flat[:,a])/cnt for a in range(3)],1); Q=mean[inv]
        P=Q.reshape(-1,3,3)
    P=P.reshape(-1,3,3); fn=np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]); ar=np.linalg.norm(fn,axis=1); keep=ar>1e-12; P=P[keep]; fn=fn[keep]/ar[keep,None]; ar=ar[keep]
    return P,fn,ar
def smooth(P,fn,ar,ang=40):
    # вершина = (позиция, корзина нормали); нормаль — среднее граней в корзине
    flat=P.reshape(-1,3); fnc=np.repeat(fn,3,0); arc=np.repeat(ar,3)
    b=np.round(fnc*1.4).astype(np.int64)
    key=np.concatenate([np.round(flat*20000).astype(np.int64),b],1)
    _,first,inv=np.unique(key,axis=0,return_index=True,return_inverse=True); inv=inv.reshape(-1)
    acc=np.zeros((len(first),3));
    for a in range(3): acc[:,a]=np.bincount(inv,fnc[:,a]*arc,minlength=len(first))
    N=acc/np.maximum(np.linalg.norm(acc,axis=1,keepdims=True),1e-12)
    return flat[first],N,inv.reshape(-1,3)
