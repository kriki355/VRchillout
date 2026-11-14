import sys, json, math
sys.path.insert(0,'/home/claude/fbx')
from fbxparse import parse,sub
top=parse(sys.argv[1]); O=[t for t in top if t['n']=='Objects'][0]; C=[t for t in top if t['n']=='Connections'][0]
objs={n['p'][0]:n for n in O['c']}
def props(n):
    P=sub(n,'Properties70'); return {p['p'][0]:p['p'][4:] for p in (P['c'] if P else [])}
def matmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def rx(a): c,s=math.cos(a),math.sin(a); return [[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]]
def ry(a): c,s=math.cos(a),math.sin(a); return [[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]]
def rz(a): c,s=math.cos(a),math.sin(a); return [[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]]
geo2model={}; mat2model={}
for c in C['c']:
    a,b=c['p'][1],c['p'][2]
    if a in objs and b in objs:
        if objs[a]['n']=='Geometry': geo2model[a]=b
        if objs[a]['n']=='Material': mat2model.setdefault(b,[]).append(objs[a]['p'][1].split('\x00')[0])
out=[]
for gid,mid in geo2model.items():
    g=objs[gid]; m=objs[mid]; pr=props(m)
    T=pr.get('Lcl Translation',[0,0,0]); R=pr.get('Lcl Rotation',[0,0,0]); S=pr.get('Lcl Scaling',[1,1,1])
    M=matmul([[1,0,0,T[0]],[0,1,0,T[1]],[0,0,1,T[2]],[0,0,0,1]],matmul(rz(math.radians(R[2])),matmul(ry(math.radians(R[1])),matmul(rx(math.radians(R[0])),[[S[0],0,0,0],[0,S[1],0,0],[0,0,S[2],0],[0,0,0,1]]))))
    V=sub(g,'Vertices')['p'][0]; PI=sub(g,'PolygonVertexIndex')['p'][0]
    LN=sub(g,'LayerElementNormal'); N=sub(LN,'Normals')['p'][0]; NI=sub(LN,'NormalsIndex'); NI=NI['p'][0] if NI else list(range(len(PI)))
    assert sub(LN,'MappingInformationType')['p'][0]=='ByPolygonVertex'
    LU=sub(g,'LayerElementUV'); UV=sub(LU,'UV')['p'][0]; UI=sub(LU,'UVIndex')['p'][0]
    # нормали: обратная транспонированная (масштаб неравномерный)
    def xf(v): return [sum(M[i][k]*v[k] for k in range(3))+M[i][3] for i in range(3)]
    inv=[1/S[0],1/S[1],1/S[2]]
    def xn(n):
        n=[n[0]*inv[0],n[1]*inv[1],n[2]*inv[2]]; r=[sum(M[i][k]/[S[0],S[1],S[2]][k]*n[k] for k in range(3)) for i in range(3)]; l=math.sqrt(sum(x*x for x in r)) or 1; return [x/l for x in r]
    pos=[];nrm=[];uv=[];idx=[]; poly=[]
    for pvi,vi in enumerate(PI):
        poly.append(pvi)
        if vi<0:
            base=len(pos)//3
            for q in poly:
                v=PI[q] if PI[q]>=0 else ~PI[q]; p=xf(V[v*3:v*3+3]); pos+= [p[0]/100,p[1]/100,p[2]/100]
                n=xn(N[NI[q]*3:NI[q]*3+3]); nrm+=n; u=UI[q]; uv+=UV[u*2:u*2+2]
            for k in range(1,len(poly)-1): idx+=[base,base+k,base+k+1]
            poly=[]
    out.append({'name':m['p'][1].split('\x00')[0],'mat':mat2model.get(mid,['?'])[0],'pos':pos,'nrm':nrm,'uv':uv,'idx':idx})
mn=[min(o['pos'][i::3][j] for o in out for j in range(len(o['pos'][i::3]))) for i in range(3)]
mx=[max(max(o['pos'][i::3]) for o in out) for i in range(3)]
print('bbox m',[round(x,3) for x in mn],[round(x,3) for x in mx])
for o in out:
    xs=o['pos'];print(o['name'],o['mat'],len(xs)//3,'verts',len(o['idx'])//3,'tris',[round(min(xs[i::3]),3) for i in range(3)],[round(max(xs[i::3]),3) for i in range(3)])
json.dump({'parts':out,'mn':mn,'mx':mx},open('/home/claude/fbx/desk_raw.json','w'))
