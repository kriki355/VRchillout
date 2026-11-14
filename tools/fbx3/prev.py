import sys; sys.path.insert(0,'/home/claude/tools3')
import numpy as np
from PIL import Image, ImageDraw
from load3 import load, decimate
def render(P, size=260, views=((0,1,2),(2,1,0),(0,2,1))):
    # P (t,3,3); views: (ось вправо, ось вверх, ось глубины)
    out=Image.new('RGB',(size*len(views),size),(235,235,230)); d=ImageDraw.Draw(out)
    A=P.reshape(-1,3); lo=A.min(0); hi=A.max(0); sc=(size-20)/max((hi-lo).max(),1e-9)
    fn=np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]); fn/=np.maximum(np.linalg.norm(fn,axis=1,keepdims=True),1e-12)
    for vi,(a,b,c) in enumerate(views):
        sgn=-1 if vi==1 else 1
        depth=P[:,:,c].mean(1)*(1 if vi!=2 else -1)
        order=np.argsort(depth)  # дальние сначала: камера смотрит со стороны +c
        L=np.array([0.3,0.8,0.5]); L/=np.linalg.norm(L)
        for t in order:
            xs=(P[t,:,a]-lo[a])*sc*(sgn if a==2 else 1); 
            if a==2 and sgn<0: xs=(hi[a]-P[t,:,a])*sc
            ys=(P[t,:,b]-lo[b])*sc
            pts=[(vi*size+10+x, size-10-y) if vi!=2 else (vi*size+10+x, 10+y) for x,y in zip(xs,ys)]
            sh=0.35+0.65*abs(fn[t]@L); col=tuple(int(v*sh) for v in (200,190,175))
            d.polygon(pts,fill=col)
    return out
if __name__=='__main__':
    ims=[]
    for f in sys.argv[1:]:
        ps=load(f); P=np.concatenate([p['P'] for p in ps]); ext=(P.reshape(-1,3).max(0)-P.reshape(-1,3).min(0)).max()
        P,_,_=decimate(P,ext/90)
        im=render(P); ImageDraw.Draw(im).text((4,4),f,fill=(200,0,0)); ims.append(im)
    W=Image.new('RGB',(ims[0].width,sum(i.height for i in ims))); y=0
    for i in ims: W.paste(i,(0,y)); y+=i.height
    W.save('/home/claude/new3/prev.png')
