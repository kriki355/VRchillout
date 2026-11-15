import sys, json, math, numpy as np
sys.path.insert(0,'/home/claude/tools3'); from pack3 import *
R90=roty(math.pi/2); R180=roty(math.pi); RM90=roty(-math.pi/2)
def bb(ps,names): A=np.concatenate([p['P'].reshape(-1,3) for p in ps if p['name'] in names]); return A.min(0),A.max(0)
def hinge(ps,gof,info,g,names,side,label='Дверца',amt=1.65):
    lo,hi=bb(ps,names); x=lo[0] if side=='L' else hi[0]
    for n in names: gof[n]=g
    info[g]={'type':'rotY','amount':-amt if side=='L' else amt,'pivotRaw':[float(x),0.0,float(lo[2])],'label':label}
def drawer(ps,gof,info,g,names,front,label='Ящик'):
    lo,hi=bb(ps,names); sh=front-hi[2]
    for p in ps:
        if p['name'] in names: p['P']=p['P']+np.array([0,0,sh]); gof[p['name']]=g
    info[g]={'type':'slideZ','amountRaw':float(-sh)*0.85,'label':label}
def near_handles(ps,gof,prefix,groups):
    for p in ps:
        if p['name'].startswith(prefix) and p['name'] not in gof:
            c=p['P'].reshape(-1,3).mean(0); best=None
            for g,names in groups.items():
                lo,hi=bb(ps,names); d=np.linalg.norm(np.clip(c,lo,hi)-c)
                if best is None or d<best[0]: best=(d,g)
            gof[p['name']]=best[1]
def minifridge(ps,gof,h):
    info={}; hinge(ps,gof,info,'door',['door','Plane.004','Text'],'R',label='Дверца холодильника',amt=1.7); gof['_info']=info
def garderob(ps,gof,h):
    info={}; hinge(ps,gof,info,'dR',['Cube_Plate.007'],'R'); hinge(ps,gof,info,'dL',['Cube_Plate.008'],'L')
    lo,hi=bb(ps,['Cube']); gof['_boxes']={'carcass':[lo.tolist(),hi.tolist()]}; gof['_info']=info
def wardrobe1(ps,gof,h):
    info={}
    for g,names,fz in [('a',['VIFS020','VIFS021','VIFS022','VIFS023','VIFS024','VIFS025','Furniture handle 006'],39.2),('b',['VIFS026','VIFS027','VIFS028','VIFS029','VIFS030','VIFS031','Furniture handle 05'],39.2),('c',['VIFS032','VIFS033','VIFS034','VIFS035','VIFS036','VIFS037','Furniture handle 007'],39.2)]:
        drawer(ps,gof,info,g,names,fz)
    # ручки выдаются вперёд — фасад ящика на 1 см от корпуса
    gof['_info']=info
def wardrobe2(ps,gof,h):
    # распахнутая 010 — закрыть
    p=[q for q in ps if q['name']=='Rectangle010'][0]; Q=p['P'].reshape(-1,3); hp=np.array([-106.0,-45.0]); a=math.atan2(-13+45,-65+106); c2,s2=math.cos(-a),math.sin(-a); dx=Q[:,0]-hp[0]; dz=Q[:,2]-hp[1]
    Q2=Q.copy(); Q2[:,0]=hp[0]+dx*c2-dz*s2; Q2[:,2]=hp[1]+dx*s2+dz*c2; p['P']=Q2.reshape(-1,3,3)
    info={}; D={'d0':['Rectangle010'],'d1':['Rectangle011'],'d2':['Rectangle012'],'d3':['Rectangle013'],'d4':['Rectangle014'],'d5':['Rectangle015']}
    for g,n in D.items(): gof[n[0]]=g
    near_handles(ps,gof,'Hafele',D)
    for g,n in D.items():
        names=n+[q['name'] for q in ps if gof.get(q['name'])==g and q['name']!=n[0]]
        lo,hi=bb(ps,n); hl,hh=bb(ps,names[1:]) if len(names)>1 else (lo,hi)
        side='L' if (hl[0]+hh[0])/2>(lo[0]+hi[0])/2 else 'R'
        hinge(ps,gof,info,g,names,side)
        info[g]['pivotRaw'][2]=float(lo[2])
    gof['_info']=info
def cakecase(ps,gof,h):
    info={}
    for p in ps:
        if p['name'] in ('LH_front','RH_front','LH_side','RH_side'): p['mats']=['glass']; p['tm']=np.zeros(len(p['P']),int)
        if p['name']=='light': p['mats']=['emission']; p['tm']=np.zeros(len(p['P']),int)
        if p['name']=='fridge_back': gof[p['name']]='back'
    lo,hi=bb(ps,['fridge_back']); info['back']={'type':'slideX','amountRaw':0.0,'amountX':float(-(hi[0]-lo[0])*0.45),'label':'Задняя дверца'}
    gof['_boxes']={n:list(map(lambda v:v.tolist(),bb(ps,[n]))) for n in ('biottom_shelf','mid_shelf','top_shelf','counter')}
    gof['_info']=info
def telega(ps,gof,h):
    info={}; pairs=[('a','Object_6','Object_7'),('b','Object_9','Object_11'),('c','Object_13','Object_15'),('d','Object_17','Object_19'),('e','Object_21','Object_23')]
    for g,box,front in pairs:
        lo,hi=bb(ps,[box]); run=[p['name'] for p in ps if p['name'].startswith('Object_') and 'SteelRunner' in p['mats'] and abs(p['P'].reshape(-1,3)[:,1].mean()-(lo[1]+hi[1])/2)<(hi[1]-lo[1])/2+60]
        drawer(ps,gof,info,g,[box,front]+run,612)
    gof['_info']=info
def flower(ps,gof,h):
    A=np.concatenate([p['P'].reshape(-1,3) for p in ps]); lo,hi=A[:,1].min(),A[:,1].max()
    for p in ps:
        cy=p['P'][:,:,1].mean(1); p['mats']=['vase','leaf']; p['tm']=(cy>lo+0.5*(hi-lo)).astype(int)
H6=['Small_Lower_Hinge','Small_Upper_Hinge','Tall_Lower_Hinge','Tall_Middle_Lower_Hinge','Tall_Middle_Upper_Hinge','Tall_Upper_Hinge']
def ovenpart(tall):
    def k(p):
        cx=p['P'][:,:,0].mean(1); m=(cx<-6000) if tall else (cx>=-6000)
        if not m.any(): return None
        p['P']=p['P'][m]; p['tm']=p['tm'][m]; return p
    return k
def ovgroups(names):
    return {('d'+str(i)):{'type':'rotX','amount':1.48,'hinge':h,'parts':[h],'label':'Дверца камеры'} for i,h in enumerate(names)}
def ovbox(ps,gof,h):
    gof['_boxes']={g:list(map(lambda v:v.tolist(),bb(ps,[p['name'] for p in ps if hn in p['anc']]))) for g,hn in [(gg,hh) for gg,hh in h.items()]}

def promfridge(ps,gof,h):
    for side,names,(hx,hz),(fx,fz) in [('L',['door-left','door-left.001'],(-67.2,35.9),(-57.1,101.7)),('R',['door-right/dark','door-right/metal'],(67.1,35.7),(49.2,99.9))]:
        dx,dz=fx-hx,fz-hz; th=math.atan2(-dz,dx) if side=='L' else math.atan2(dz,-dx); c,s=math.cos(th),math.sin(th)
        for p in ps:
            if p['name'] in names:
                Q=p['P'].reshape(-1,3).copy(); X=Q[:,0]-hx; Z=Q[:,2]-hz; Q[:,0]=hx+X*c-Z*s; Q[:,2]=hz+X*s+Z*c; p['P']=Q.reshape(-1,3,3)
                if 'dark' in p['mats'][0]: p['mats']=['doorpanel']
    for p in ps:
        if p['name']=='Unbranded cabinet details.002': p['mats']=['fridgedisplay']
        elif 'metal' in p['mats'][0]: p['mats']=['stainless']
        elif 'dark' in p['mats'][0]: p['mats']=['fridgedark']
    info={}; hinge(ps,gof,info,'dl',['door-left','door-left.001'],'L',label='Левая дверца',amt=1.75); hinge(ps,gof,info,'dr',['door-right/dark','door-right/metal'],'R',label='Правая дверца',amt=1.75)
    A=np.concatenate([p['P'].reshape(-1,3) for p in ps if 'door' in p['name']]); print('doors z',A[:,2].min(),A[:,2].max(),'x',A[:,0].min(),A[:,0].max())
    gof['_boxes']={'disp':list(map(lambda v:v.tolist(),bb(ps,['Unbranded cabinet details.002'])))}
    gof['_info']=info

def mixer2(ps,gof,h):
    info={}
    for p in ps:
        n=p['name']
        if n=='whisk detail': gof[n]='wh'; p['mats']=['mixsteel']
        elif n=='guard detail': gof[n]='gd'; p['mats']=['mixguard']
        elif n=='static detail.003': p['mats']=['mixstart']
        elif n=='static detail.004': p['mats']=['mixstop']
        elif 'cream' in p['mats'][0]: p['mats']=['mixbody']
        elif 'mid grey' in p['mats'][0]: p['mats']=['mixsteel']
        elif 'elastomer' in p['mats'][0]: p['mats']=['mixdark']
    lo,hi=bb(ps,['whisk detail']); info['wh']={'type':'spin','amount':7.0,'pivotRaw':[float((lo[0]+hi[0])/2),0.0,float((lo[2]+hi[2])/2)],'label':'Спираль'}
    lo,hi=bb(ps,['guard detail']); info['gd']={'type':'rotX','amount':-1.15,'pivotRaw':[0.0,float(hi[1]),float(lo[2])],'label':'Защитная крышка'}
    gof['_boxes']={k:list(map(lambda v:v.tolist(),bb(ps,[n]))) for k,n in [('whisk','whisk detail'),('start','static detail.003'),('stop','static detail.004'),('guard','guard detail'),('all','static detail.001')]}
    gof['_info']=info
CFG=[
 ('minifridge','minifridge.fbx',dict(height=0.86,rot=RM90,special=minifridge,drop=('arm',))),
 ('sinktable','newmoika1.fbx',dict(height=1.2,rot=R180)),
 ('cakecase','newvitrina.fbx',dict(height=1.3,special=cakecase)),
 ('wardrobe1','newwardrobe1.fbx',dict(height=2.4,special=wardrobe1)),
 ('wardrobe2','newwardrobe2.fbx',dict(height=2.4,special=wardrobe2)),
 ('oven4','pechkaanimated.fbx',dict(height=2.0,rot=ZUPF,override={h:[-90,0,0] for h in H6},groups=ovgroups(H6[2:]),target=26000,keep=ovenpart(True))),
 ('oven2','pechkaanimated.fbx',dict(height=None,rot=ZUPF,override={h:[-90,0,0] for h in H6},groups=ovgroups(H6[:2]),target=16000,keep=ovenpart(False))),
 ('workbench','verstak.fbx',dict(height=2.0)),
 ('mobboard','whiteboard.fbx',dict(height=1.85)),
 ('chester','divanelitny.fbx',dict(height=0.78,target=24000)),
 ('flower','flower.fbx',dict(height=0.85,target=42000,special=flower,twoside=True)),
 ('garderob','garderob.fbx',dict(height=1.95,rot=R180,special=garderob,drop=('Cube',))),
 ('prodtable','stolproizvod.fbx',dict(rot=R90,dims=[1.6,0.88,0.8])),
 ('drawers',None,None),
 ('telega','../new4/telega.fbx',dict(height=1.0,special=telega)),
 ('mixer2','mixer2.fbx',dict(height=1.47,special=mixer2,target=16000)),
 ('promfridge','promfridge.fbx',dict(height=2.05,special=promfridge,target=12000)),
]

OUT=json.load(open('/home/claude/tools3/new4.json'))
for k in ['microwave','chestfreezer','gamechair','deckoven']: OUT.pop(k,None)
only=sys.argv[1:]
for key,f,kw in CFG:
    if f is None or (only and key not in only): continue
    if key=='oven2': kw['scale']=OUT['oven4']['S']
    OUT[key]=model(key,f,**kw)
json.dump(OUT,open('/home/claude/tools3/new4.json','w'),separators=(',',':'))
print({k:list(v['groups'].keys()) for k,v in OUT.items()})
