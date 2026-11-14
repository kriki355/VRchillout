import sys, json, math, base64, numpy as np, re
sys.path.insert(0,'/home/claude/tools3'); from load3 import load, decimate, smooth
R='/home/claude/new3/'
def enc(P,N,I,name,mat,g):
    lo=P.min(0); hi=P.max(0)+1e-6
    q=np.clip(np.round((P-lo)/(hi-lo)*65534-32767),-32767,32767).astype('<i2')
    return {'name':name,'mat':mat,'g':g,'lo':lo.round(5).tolist(),'hi':hi.round(5).tolist(),'p':base64.b64encode(q.tobytes()).decode(),
      'n':base64.b64encode(np.clip(np.round(N*127),-127,127).astype('i1').tobytes()).decode(),'u':'',
      'i':base64.b64encode(np.array(I,dtype='<u2').tobytes()).decode()}
def roty(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
ZUP=np.array([[1,0,0],[0,0,1],[0,-1,0]])   # (x,y,z)->(x,z,-y): ось Z вверх, перед +Y станет -Z
ZUPF=np.array([[-1,0,0],[0,0,1],[0,1,0]])  # Z вверх, перед +Y → +Z
def minang(xz):
    best=(1e18,0)
    for d in np.arange(0,90,0.25):
        a=math.radians(d); c,s=math.cos(a),math.sin(a); u=xz[:,0]*c+xz[:,1]*s; v=-xz[:,0]*s+xz[:,1]*c
        ar=(u.max()-u.min())*(v.max()-v.min()); best=min(best,(ar,a))
    return best[1]
def model(key,f,height=None,rot=None,dims=None,groups=None,target=22000,override=None,special=None,keep=None):
    ps=load(R+f,override); hinges={}
    if override: hinges={h:load.hinge(h)[:3,3].copy() for h in override}
    if keep: ps=[p for p in ps if keep(p)]
    Rm=np.eye(3) if rot is None else rot
    for p in ps: p['P']=p['P']@Rm.T
    hinges={h:v@Rm.T for h,v in hinges.items()}
    gof={}
    if special: special(ps,gof,hinges)
    A=np.concatenate([p['P'].reshape(-1,3) for p in ps]); lo=A.min(0); hi=A.max(0); c=np.array([(lo[0]+hi[0])/2,lo[1],(lo[2]+hi[2])/2])
    if dims: S=np.array(dims)/(hi-lo)
    else: S=np.full(3,height/(hi[1]-lo[1]))
    for p in ps: p['P']=(p['P']-c)*S
    hinges={h:(v-c)*S for h,v in hinges.items()}
    ext=((hi-lo)*S).max(); tot=sum(len(p['P']) for p in ps)
    # группы
    gp={}
    for p in ps:
        g=gof.get(p['name'],'') if isinstance(gof.get(p['name'],''),str) else ''
        if groups:
            for gn,spec in groups.items():
                if any(re.fullmatch(rx,p['name']) or rx in p['anc'] for rx in spec['parts']): g=gn
        p['g']=g
    cell=0 if tot<=target else ext/600
    while True:
        out=[];n=0
        for p in ps:
            for m in np.unique(p['tm']):
                Pm=p['P'][p['tm']==m]; P2,fn,ar=decimate(Pm,cell)
                if len(P2)==0: continue
                mn=p['mats'][m] if m<len(p['mats']) else p['mats'][0]
                out.append((p['g'],mn,P2,fn,ar)); n+=len(P2)
        if n<=target*1.05 or cell>ext/40: break
        cell=cell*1.35 if cell else ext/600
    # склеиваем по (группа, материал)
    merged={}
    for g,mn,P2,fn,ar in out: merged.setdefault((g,mn),[]).append((P2,fn,ar))
    res=[]
    for (g,mn),L in merged.items():
        P=np.concatenate([a for a,_,_ in L]); fn=np.concatenate([b for _,b,_ in L]); ar=np.concatenate([c for _,_,c in L])
        for s in range(0,len(P),20000):
            V,N,I=smooth(P[s:s+20000],fn[s:s+20000],ar[s:s+20000]); res.append(enc(V,N,I.reshape(-1),f'{g}|{mn}|{s}',mn,g))
    size=((hi-lo)*S).round(3).tolist(); print(key,'size',size,'tris',n,'of',tot,'cell',round(cell,4))
    gi={}
    for gn,spec in (groups or {}).items():
        gi[gn]=dict(spec); gi[gn].pop('parts',None)
        if 'hinge' in spec: gi[gn]['pivot']=hinges[spec['hinge']].round(4).tolist()
    for gn,v in gof.get('_info',{}).items():
        v=dict(v)
        if 'amountRaw' in v: v['amount']=round(v.pop('amountRaw')*S[2],4)
        if 'pivotRaw' in v: v['pivot']=((np.array(v.pop('pivotRaw'))-c)*S).round(4).tolist()
        gi[gn]=v
    for gn,spec in gi.items():
        if spec.get('edge'):
            G=np.concatenate([p['P'].reshape(-1,3) for p in ps if p['g']==gn]); H=[p['P'].reshape(-1,3) for p in ps if p['g']==gn and re.fullmatch(spec['edge'],p['name'])]
            hx=np.concatenate(H)[:,0].mean() if H else G[:,0].max(); left=hx>(G[:,0].min()+G[:,0].max())/2
            spec['pivot']=[round(float(G[:,0].min() if left else G[:,0].max()),4),0,round(float(G[:,2].min()),4)]; spec['amount']=-1.75 if left else 1.75; spec.pop('edge')
    return {'parts':res,'size':size,'groups':gi}
model.extra={}
