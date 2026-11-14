import sys; sys.path.insert(0,'/home/claude/fbx'); sys.path.insert(0,'/home/claude/tools3')
from fbxparse import parse, sub
from load3 import props
import numpy as np
def anims(path):
    top=parse(path); O=[t for t in top if t['n']=='Objects'][0]; C=[t for t in top if t['n']=='Connections'][0]
    objs={n['p'][0]:n for n in O['c']}; cn2model={}; curve2cn={}
    for c in C['c']:
        a,b=c['p'][1],c['p'][2]; prop=c['p'][3] if len(c['p'])>3 else None
        if a in objs and b in objs:
            if objs[a]['n']=='AnimationCurveNode' and objs[b]['n']=='Model': cn2model[a]=(b,prop)
            if objs[a]['n']=='AnimationCurve' and objs[b]['n']=='AnimationCurveNode': curve2cn.setdefault(b,[]).append((a,prop))
    out={}
    for cn,(mid,prop) in cn2model.items():
        ks={}
        for cv,ax in curve2cn.get(cn,[]):
            v=sub(objs[cv],'KeyValueFloat'); t=sub(objs[cv],'KeyTime')
            if v: ks[ax]=(list(t['p'][0]) if t else [], list(v['p'][0]))
        nm=objs[mid]['p'][1].split('\x00')[0]
        out.setdefault(mid,{'name':nm,'lcl':props(objs[mid])})[prop]=ks
    return out
if __name__=='__main__':
    A=anims(sys.argv[1])
    for mid,d in A.items():
        for prop in ('Lcl Translation','Lcl Rotation'):
            if prop not in d: continue
            ks=d[prop]; vals={ax:(round(v[0],2),round(v[-1],2),len(v)) for ax,(t,v) in ks.items()}
            changing={ax:x for ax,x in vals.items() if abs(x[0]-x[1])>1e-3}
            if changing: print(d['name'],prop,'lcl',[round(x,2) for x in d['lcl'].get(prop,[0,0,0])],changing)
