import sys, json, math
import numpy as np
sys.path.insert(0,'/home/claude/fbx')
from fbxparse import parse,sub
def load(path):
    top=parse(path); O=[t for t in top if t['n']=='Objects'][0]; C=[t for t in top if t['n']=='Connections'][0]
    objs={n['p'][0]:n for n in O['c']}; g2m={}; m2mat={}
    for c in C['c']:
        a,b=c['p'][1],c['p'][2]
        if a in objs and b in objs:
            if objs[a]['n']=='Geometry': g2m[a]=b
            if objs[a]['n']=='Material': m2mat.setdefault(b,[]).append(objs[a]['p'][1].split('\x00')[0])
    parts=[]
    for gid,mid in g2m.items():
        g=objs[gid]; m=objs[mid]; P=sub(m,'Properties70'); pr={p['p'][0]:p['p'][4:] for p in (P['c'] if P else [])}
        T=pr.get('Lcl Translation',[0,0,0]); R=[math.radians(x) for x in pr.get('Lcl Rotation',[0,0,0])]; S=pr.get('Lcl Scaling',[1,1,1])
        def rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
        def ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
        def rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
        Rm=rz(R[2])@ry(R[1])@rx(R[0]); M=Rm@np.diag(S); Nm=Rm@np.diag([1/x for x in S])
        V=np.array(sub(g,'Vertices')['p'][0]).reshape(-1,3); PI=sub(g,'PolygonVertexIndex')['p'][0]
        LN=sub(g,'LayerElementNormal')
        if LN: N=np.array(sub(LN,'Normals')['p'][0]).reshape(-1,3); mt=sub(LN,'MappingInformationType')['p'][0]; NI=sub(LN,'NormalsIndex'); NI=NI['p'][0] if NI else None
        else: N=np.zeros((len(PI),3)); N[:,1]=1; mt='ByPolygonVertex'; NI=None
        LU=sub(g,'LayerElementUV')
        if LU: UV=np.array(sub(LU,'UV')['p'][0]).reshape(-1,2); UI=sub(LU,'UVIndex')['p'][0]
        else: UV=np.zeros((1,2)); UI=[0]*len(PI)
        LM=sub(g,'LayerElementMaterial'); MI=sub(LM,'Materials')['p'][0] if LM else [0]; mmode=sub(LM,'MappingInformationType')['p'][0] if LM else 'AllSame'
        flip=np.linalg.det(M)<0; pos=[];nrm=[];uv=[];idx=[];poly=[];pmat=[];fi=0
        for k,vi in enumerate(PI):
            poly.append(k)
            if vi<0:
                b=len(pos)
                for q in poly:
                    v=PI[q] if PI[q]>=0 else ~PI[q]; pos.append(M@V[v]+np.array(T))
                    n=N[v] if mt=='ByVertice' else (N[NI[q]] if NI is not None else N[q]); n=Nm@n; nrm.append(n/np.linalg.norm(n)); uv.append(UV[UI[q]])
                for j in range(1,len(poly)-1): idx+= [b,b+j+1,b+j] if flip else [b,b+j,b+j+1]; pmat.append(MI[fi] if mmode=='ByPolygon' and fi<len(MI) else MI[0])
                poly=[]; fi+=1
        if not pos: continue
        parts.append({'name':m['p'][1].split('\x00')[0],'mat':(m2mat.get(mid) or ['?'])[0],'mats':m2mat.get(mid) or ['?'],'tmat':pmat,'pos':np.array(pos),'nrm':np.array(nrm),'uv':np.array(uv),'idx':idx,'hasN':bool(LN)})
    return parts
if __name__=='__main__':
    ps=load(sys.argv[1]); allp=np.concatenate([p['pos'] for p in ps]); print('bbox',allp.min(0).round(1),allp.max(0).round(1))
    for p in ps: print(p['name'],p['mat'],len(p['pos']),p['pos'].min(0).round(1),p['pos'].max(0).round(1))
