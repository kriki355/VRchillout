import asyncio, sys, json, time, math, os
from playwright.async_api import async_playwright
W,H,FPS=1280,720,24
START=int(sys.argv[1]) if len(sys.argv)>1 else 0
MOCK=open('rec.py').read().split('MOCK=r"""')[1].split('"""')[0].replace('%W%',str(W)).replace('%H%',str(H))
RJS=open('recjs.js').read()
PI=math.pi
def ss(a,b,t): 
    if t<=a: return 0.0
    if t>=b: return 1.0
    u=(t-a)/(b-a); return u*u*(3-2*u)
def lerp(a,b,k): return a+(b-a)*k
def path(pts,k):  # квадратичная кривая по 3 точкам
    (x0,z0),(x1,z1),(x2,z2)=pts; return ((1-k)**2*x0+2*(1-k)*k*x1+k*k*x2,(1-k)**2*z0+2*(1-k)*k*z1+k*k*z2)
def yawto(dx,dz): return math.atan2(-dx,-dz)
LAP=None
def P_at(t,f):
    P={'fps':FPS}; ev=[]
    def at(tt): return abs(t-tt)<0.5/FPS
    # ---- риг (позиция и поворот тела)
    if t<4: rig=(7.0,9.35,0.0)
    elif t<8: k=ss(4,8,t); x,z=path([(7.0,9.35),(5.6,8.4),(4.3,8.5)],k); rig=(x,z,lerp(0,1.99,ss(4.3,7.8,t)))
    elif t<17.6: rig=(4.3,8.5,1.99)
    elif t<21: rig=(3.6,lerp(4.3,3.6,ss(19.5,21,t)),lerp(1.99,0.0,ss(17.9,19.6,t)))
    elif t<35: rig=(3.6,3.6,0.0)
    elif t<43: k=ss(35,43,t); x,z=path([(3.6,3.6),(8.6,4.8),(10.9,8.3)],k); rig=(x,z,lerp(0,-2.457,ss(36,42.5,t)))
    elif t<51: rig=(10.9,8.3,-2.457)
    elif t<62: k=ss(51,53,t); rig=(lerp(10.9,12.25,k),lerp(8.3,7.0,k),lerp(-2.457,-PI/2,k))
    elif t<76: k=ss(62.4,64,t); k2=ss(64,65.2,t); rig=(lerp(15.6,15.2,k2),lerp(3.3,2.6,k2),lerp(-PI/2,0.257,k))
    elif t<86: k=ss(76,78.5,t); rig=(lerp(15.2,16.95,k),lerp(2.6,4.75,k),lerp(0.257,-PI/2,k))
    elif t<92: rig=(16.95,4.75,lerp(-PI/2,-3.52,ss(86,87.6,t)))
    elif t<97: rig=(16.95,4.75,-3.52)
    else: k=ss(97,102,t); rig=(lerp(16.95,12.3,k),lerp(4.75,4.2,k),lerp(-3.52,-4.712,ss(97,100.5,t)))
    P['rig']=rig
    # ---- взгляд, луч, события
    look=None; aim=None
    if t<1.6: look={'t':'w','p':[7.0,1.25,7.6]}
    elif t<3: look={'t':'w','p':[4.9,1.0,9.2]}
    elif t<8: look={'t':'item','type':'chester','y':0.5}
    elif t<15:
        if t<9.8: look={'t':'item','type':'chester','y':0.5}; aim={'t':'item','type':'chester','y':0.5}
        else:
            look={'t':'card','u':0.5,'v':0.5}
            aim={'t':'card','u':0.125,'v':0.9} if t<13.2 else {'t':'card','u':0.875,'v':0.9}
        if at(9.3) or at(11.6) or at(12.6) or at(14.3): ev.append('select')
        if t>14.6: aim=None
    elif t<19.5:
        if t<17.7: look={'t':'w','p':[3.6,0.0,4.3]}; aim={'t':'w','p':[3.6,0.0,4.3]}
        if 15.9<=t<17.6: P['rax']=[0,0,0,-0.9]
    elif t<30:
        if t<27.6: look={'t':'w','p':[LAP[0],LAP[1]+0.15,LAP[2]]}
        # хват ноутбука и поворот в руке
        if 21<=t<27.6:
            base=LAP; d0=[3.6+0.16,1.3,3.6-0.3]
            if t<22.2: k=ss(21,22.1,t); P['rhw']=[lerp(d0[0],base[0],k),lerp(d0[1],base[1]+0.02,k),lerp(d0[2],base[2],k)]
            elif t<26.2:
                k=ss(22.4,23.8,t)-ss(25.0,26.1,t); P['rhw']=[base[0]+0.15*k,base[1]+0.02+0.32*k,base[2]+0.45*k]
                P['ryaw']=lerp(0,0.9,ss(23.6,24.6,t))-lerp(0,0.9,ss(24.6,25.6,t)); P['rpitch']=lerp(-25,10,ss(22.4,23.8,t))-lerp(0,35,ss(25,26.1,t)); P['roll']=lerp(0,35,ss(23.8,24.6,t))-lerp(0,35,ss(24.6,25.4,t))
            else: P['rhw']=[base[0],base[1]+0.02,base[2]]; P['rpitch']=-25; P['ryaw']=0
            if at(22.2): ev.append('squeezestart')
            if at(26.6): ev.append('squeezeend')
        if t>=27.6: look={'t':'lab','type':'cabinet','i':1,'label':'Дверца'}; aim=look if t>27.9 else None
        if at(29.0): ev.append('select')
    elif t<35:
        P['lh']='up' if t<33.6 else 'down'; look={'t':'hand','u':0.5,'v':0.42} if t<33.4 else None
    elif t<43: look=None; P['hy']=0
    elif t<51:
        look={'t':'lab','type':'coffee','label':'Холдер — пролив'}; aim=look if 43.8<t<47.5 else None
        if at(45.4): ev.append('select')
        if t>46.5: look={'t':'lab','type':'coffee','label':'Пролив'}
    elif t<59:
        if t<55: look={'t':'lab','type':'promfridge','label':'Левая дверца'}
        elif t<57: look={'t':'lab','type':'promfridge','label':'Правая дверца'}
        else: look={'t':'btn','type':'promfridge','label':'Подсветка камеры'}
        if t>53.2: aim=look
        if at(54.2) or at(56.2) or at(57.9): ev.append('select')
        if t>58.3: aim=None; look={'t':'w','p':[13.4,1.1,6.9]}
    elif t<64:
        if t<62: look={'t':'w','p':[15.6,0.0,3.3]}; aim=look if t>59.5 else None
        if 60.2<=t<62: P['rax']=[0,0,0,-0.9]
    elif t<76:
        if t<67: look={'t':'btn','type':'pka6','label':'Работа'}; aim=look if t>65.3 else None
        elif t<69.6: look={'t':'w','p':[15.3,1.85,1.2]}
        elif t<72: look={'t':'lab','type':'pka6','label':'Дверца'}; aim=look if t>69.9 else None
        elif t<74: look={'t':'lab','type':'pka6','label':'Гастроёмкость'}; aim=look if t>72.3 else None
        else: look={'t':'lab','type':'pk6','label':'Противень 3'}; aim=look if t>74.2 else None
        if at(66.3) or at(71.0) or at(73.2) or at(75.2): ev.append('select')
    elif t<86:
        if t<78.5: look=None
        elif t<80: look={'t':'tap','type':'mixer2','k':2}; aim=look if t>78.8 else None
        elif t<82.5: look={'t':'lab','type':'mixer2','label':'Спираль'}
        else: look={'t':'lab','type':'mixer2','label':'Защитная крышка'}; aim=look if t>82.7 else None
        if at(79.6) or at(83.6): ev.append('select')
    elif t<92:
        if t<89.4: look={'t':'lab','type':'saladette','label':'Правая дверца'}; aim=look if t>87.6 else None
        else: look={'t':'lab','type':'saladette','label':'Крышка ванн'}; aim=look if t>89.6 else None
        if at(88.6) or at(90.8): ev.append('select')
    elif t<97:
        P['hp']=-0.05
        if at(92.6) or at(95.8): P['btn']=[['left',4,True]]
        elif at(92.6+1/FPS) or at(95.8+1/FPS): P['btn']=[['left',4,False]]
    if look: P['look']=look
    if aim: P['aim']=aim
    if ev: P['ev']=ev
    if t<0.05: P['snap']=True
    return P
DUR=102.0
async def main():
    global LAP
    os.makedirs('frames2',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':W,'height':H}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.add_init_script(MOCK)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4000)
        await pg.evaluate("PERF.dyn=false; PERF.scale=1; QUAL.k=1; GFX.pc=3"); await pg.click('#demoBtn'); await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content="body>*:not(#gl){display:none!important}")
        await pg.evaluate("$('vrBtn').click()"); await pg.wait_for_timeout(2500)
        await pg.evaluate("__xrmock.fire('select','right')"); await pg.wait_for_timeout(300)
        await pg.evaluate(RJS)
        await pg.evaluate("(()=>{ const b=performance.now(),t0=__xrmock.t; performance.now=()=>b+(__xrmock.t-t0); })()")
        LAP=await pg.evaluate("__rec.target({t:'item',type:'laptop',i:2,y:0.04})")
        print('laptop',LAP,flush=True)
        N=int(DUR*FPS); t0=time.time()
        for i in range(N):
            P=P_at(i/FPS,i)
            await pg.evaluate("P=>__rec.frame(P)",P)
            if i>=START: await pg.screenshot(path=f'frames2/f_{i:05d}.jpg',type='jpeg',quality=93)
            if i%120==0: print(i,N,round(time.time()-t0),'s',flush=True)
        print('\n'.join(logs) or 'ok',flush=True); await b.close()
asyncio.run(main())
