import sys, json, base64, numpy as np
sys.path.insert(0,'/home/claude/tools3'); from prev import render
from PIL import Image, ImageDraw
D=json.load(open(sys.argv[1])); ims=[]
for k,m in D.items():
    T=[]
    for p in m['parts']:
        q=np.frombuffer(base64.b64decode(p['p']),'<i2').reshape(-1,3).astype(float); lo=np.array(p['lo']); hi=np.array(p['hi'])
        V=lo+(q+32767)/65534*(hi-lo); I=np.frombuffer(base64.b64decode(p['i']),'<u2').reshape(-1,3); T.append(V[I])
    P=np.concatenate(T)
    if len(P)>6000: P=P[np.random.RandomState(0).choice(len(P),6000,replace=False)]
    im=render(P,200,((0,1,2),(2,1,0),(0,2,1))); ImageDraw.Draw(im).text((4,4),k+' '+str(list(m['groups'].keys())),fill=(200,0,0)); ims.append(im)
cols=2; W=Image.new('RGB',(ims[0].width*cols,ims[0].height*((len(ims)+1)//2)),(255,255,255))
for i,im in enumerate(ims): W.paste(im,((i%cols)*im.width,(i//cols)*im.height))
W.save(sys.argv[2])
