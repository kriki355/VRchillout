import sys, json, math, numpy as np
sys.path.insert(0,'/home/claude/tools3'); from pack3 import *
OUT={}
R90=roty(math.pi/2); R180=roty(math.pi); RM90=roty(-math.pi/2)
def tumba(ps,gof,h):
    body=[p for p in ps if p['name'] in ('VIFS023','VIFS024','VIFS025','VIFS026','VIFS027','VIFS028','VIFS029','VIFS030')]
    B=np.concatenate([p['P'].reshape(-1,3) for p in body]); a=minang(B[:,[0,2]]); Rr=roty(a)
    # ищем поворот на кратное 90°, при котором ящики торчат вперёд (+z)
    drw=[p for p in ps if p not in body]
    for k in range(4):
        Rk=roty(a+k*math.pi/2)
        Bz=(B@Rk.T)[:,2].max(); Dz=np.concatenate([p['P'].reshape(-1,3) for p in drw])@Rk.T
        if Dz[:,2].max()>Bz+0.5: break
    for p in ps: p['P']=p['P']@Rk.T
    bz=np.concatenate([p['P'].reshape(-1,3) for p in body])[:,2].max()
    info={}
    for gname,names in (('d1',['Rectangle001','VIFS016','VIFS017','VIFS018','VIFS019','VIFS020','VIFS021','VIFS022']),('d2',['Rectangle002','VIFS047','VIFS048','VIFS049','VIFS050','VIFS051','VIFS052','VIFS053'])):
        G=[p for p in ps if p['name'] in names]; fr=[p for p in G if p['name'].startswith('Rect')][0]
        frz=fr['P'].reshape(-1,3)[:,2]; shift=bz-frz.min()
        Gy=np.concatenate([p['P'].reshape(-1,3) for p in G])[:,1].mean()
        hd=[p for p in ps if p['name'].startswith('Hafele') and abs(p['P'].reshape(-1,3)[:,1].mean()@np.ones(1) if False else abs(p['P'].reshape(-1,3)@ (Rk@np.array([0,1,0]))).mean()-0)>=0]
        for p in G: p['P']=p['P']+np.array([0,0,shift]); gof[p['name']]=gname
        info[gname]={'type':'slideZ','amountRaw':float(-shift)*0.8,'label':'Ящик'}
    # ручки — к ближайшему по высоте ящику
    for p in ps:
        if p['name'].startswith('Hafele'):
            y=p['P'].reshape(-1,3)[:,1].mean(); best=None
            for gname in ('d1','d2'):
                G=np.concatenate([q['P'].reshape(-1,3) for q in ps if gof.get(q['name'])==gname]); d=abs(G[:,1].mean()-y)
                if best is None or d<best[0]: best=(d,gname)
            gn=best[1]; sh=-info[gn]['amountRaw']/0.8; p['P']=p['P']+np.array([0,0,sh]); gof[p['name']+'#h']=gn; p['name']=p['name']+'#h'
    gof['_info']=info
def wardrobe2(ps,gof,h):
    # распахнутая дверца: тонкая деталь под углом — закрываем, делаем интерактивной
    A=np.concatenate([p['P'].reshape(-1,3) for p in ps]); info={}
    for p in ps:
        Q=p['P'].reshape(-1,3); xz=Q[:,[0,2]]
        if len(Q)<12: continue
        a=minang(xz); deg=math.degrees(a)
        if 8<deg<82:
            c,s=math.cos(a),math.sin(a); u=xz[:,0]*c+xz[:,1]*s; v=-xz[:,0]*s+xz[:,1]*c
            if (v.max()-v.min())>0.15*(u.max()-u.min()) and (u.max()-u.min())>0.15*(v.max()-v.min()): continue
            print('door',p['name'],round(deg,1))
            # петля — конец двери, ближе к корпусу (к центру масс модели)
            ends=[xz[np.argmin(u if (u.max()-u.min())>(v.max()-v.min()) else v)],xz[np.argmax(u if (u.max()-u.min())>(v.max()-v.min()) else v)]]
            cen=A[:,[0,2]].mean(0); hp=max(ends,key=lambda e:np.linalg.norm(e-cen)); other=min(ends,key=lambda e:np.linalg.norm(e-cen))
            ang=math.atan2(other[1]-hp[1],other[0]-hp[0])  # угол двери в xz
            target=0.0 if abs(math.cos(ang))>abs(math.sin(ang)) or True else 0
            tgt=math.pi if other[0]<hp[0] else 0.0; dth=tgt-ang  # повернуть в плоскость фасада (вдоль x)
            # поворот вокруг Y на угол: в нашей системе x'=x c + z s ... rot в xz на dth по математике
            c2,s2=math.cos(dth),math.sin(dth); Q2=Q.copy(); dx=Q[:,0]-hp[0]; dz=Q[:,2]-hp[1]
            Q2[:,0]=hp[0]+dx*c2-dz*s2; Q2[:,2]=hp[1]+dx*s2+dz*c2; p['P']=Q2.reshape(-1,3,3); gof[p['name']]='door'
            info['door']={'type':'rotY','amount':-1.6 if dth<0 else 1.6,'pivotRaw':[float(hp[0]),0.0,float(hp[1])],'label':'Дверца'}
    gof['_info']=info
def flower(ps,gof,h):
    A=np.concatenate([p['P'].reshape(-1,3) for p in ps]); lo,hi=A[:,1].min(),A[:,1].max()
    for p in ps:
        cy=p['P'][:,:,1].mean(1); p['mats']=['vase','leaf']; p['tm']=(cy>lo+0.5*(hi-lo)).astype(int)
H6=['Small_Lower_Hinge','Small_Upper_Hinge','Tall_Lower_Hinge','Tall_Middle_Lower_Hinge','Tall_Middle_Upper_Hinge','Tall_Upper_Hinge']
pg={('d'+str(i)):{'type':'rotX','amount':1.48,'hinge':h,'parts':[h],'label':'Дверца камеры'} for i,h in enumerate(H6)}
CFG=[
 ('microwave','microwavenew.fbx',dict(height=0.31)),
 ('minifridge','minifridge.fbx',dict(height=0.86,rot=RM90,groups={'door':{'type':'rotY','parts':['door','arm','Plane.004','Text'],'edge':'arm','label':'Дверца'}})),
 ('chestfreezer','newholodilnik1.fbx',dict(height=0.88)),
 ('sinktable','newmoika1.fbx',dict(height=1.2,rot=R180)),
 ('drawers','newtumba1.fbx',dict(height=0.6,special=tumba)),
 ('cakecase','newvitrina.fbx',dict(height=1.3)),
 ('wardrobe1','newwardrobe1.fbx',dict(height=2.4)),
 ('wardrobe2','newwardrobe2.fbx',dict(height=2.4,special=wardrobe2)),
 ('deckoven','pechkaanimated.fbx',dict(height=2.0,rot=ZUPF,override={h:[-90,0,0] for h in H6},groups=pg,target=30000)),
 ('workbench','verstak.fbx',dict(height=2.0)),
 ('mobboard','whiteboard.fbx',dict(height=1.85)),
 ('chester','divanelitny.fbx',dict(height=0.78,target=24000)),
 ('flower','flower.fbx',dict(height=0.85,target=14000,special=flower)),
 ('gamechair','gamekreslo.fbx',dict(height=1.33,target=24000)),
 ('garderob','garderob.fbx',dict(height=1.95,rot=R180)),
 ('prodtable','stolproizvod.fbx',dict(rot=R90,dims=[1.6,0.88,0.8])),
]
only=sys.argv[1:]
for key,f,kw in CFG:
    if only and key not in only: continue
    OUT[key]=model(key,f,**kw)
json.dump(OUT,open('/home/claude/tools3/new3.json' if not only else '/home/claude/tools3/new3_part.json','w'))
