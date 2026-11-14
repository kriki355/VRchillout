import sys, asyncio, json
from playwright.async_api import async_playwright
URL='file://'+sys.argv[1]; OUT=sys.argv[2]
MOCK = r"""
(() => {
  const mk = (m) => ({ position:{x:m.m41,y:m.m42,z:m.m43}, orientation:{x:0,y:0,z:0,w:1}, matrix:m.toFloat32Array(), inverse:{matrix:m.inverse().toFloat32Array()} });
  const persp = (() => { const f=1/Math.tan(45*Math.PI/180), a=700/820, n=0.05, fa=200; const m=new Float32Array(16); m[0]=f/a; m[5]=f; m[10]=(fa+n)/(n-fa); m[11]=-1; m[14]=2*fa*n/(n-fa); return m; })();
  const L = {}; const left={handedness:'left', targetRaySpace:{id:'lray'}, gripSpace:{id:'lgrip'}, gamepad:{axes:[0,0,0,0]}}; const right={handedness:'right', targetRaySpace:{id:'rray'}, gripSpace:{id:'rgrip'}, gamepad:{axes:[0,0,0,0]}};
  const M = window.__xrmock = { head: mk(new DOMMatrix().translate(0,1.6,0)), left: mk(new DOMMatrix().translate(-0.2,1.2,-0.3).rotateAxisAngle(1,0,0,-70)), right: mk(new DOMMatrix().translate(0.2,1.3,-0.1)), leftSrc:left, rightSrc:right, frames:0,
    aim(wx,wy,wz){ const xr=__app.xr; const c=Math.cos(xr.rig.yaw), s=Math.sin(xr.rig.yaw); const dx0=wx-xr.rig.x, dz0=wz-xr.rig.z; const lx=c*dx0 - s*dz0, lz=s*dx0 + c*dz0, ly=wy-xr.rig.y;
      const o=[0.2,1.3,-0.1], d=[lx-o[0], ly-o[1], lz-o[2]]; const yaw=Math.atan2(-d[0],-d[2])*180/Math.PI, pitch=Math.atan2(d[1],Math.hypot(d[0],d[2]))*180/Math.PI;
      M.right = mk(new DOMMatrix().translate(...o).rotateAxisAngle(0,1,0,yaw).rotateAxisAngle(1,0,0,pitch)); },
    select(){ (L.select||[]).forEach(f=>f({inputSource:right})); }, squeeze(t){ (L[t]||[]).forEach(f=>f({inputSource:right})); }, squeezeF(t,src){ (L[t]||[]).forEach(f=>f({inputSource:src==='left'?left:right,frame})); }, at(x,y,z,rx){ M.right=mk(new DOMMatrix().translate(x,y,z).rotateAxisAngle(1,0,0,rx||0)); }, atL(x,y,z){ M.left=mk(new DOMMatrix().translate(x,y,z)); }, btn(side,i,v){ const g=(side==='left'?left:right).gamepad; if(!g.buttons) g.buttons=[0,1,2,3,4,5].map(()=>({pressed:false,value:0})); g.buttons[i].pressed=v; g.buttons[i].value=v?1:0; } };
  const frame = { getViewerPose(){ return {transform:M.head, views:[{eye:'left',projectionMatrix:persp,transform:M.head},{eye:'right',projectionMatrix:persp,transform:M.head}]}; },
                  getPose(space){ return {transform: space.id==='lgrip'||space.id==='lray' ? M.left : M.right}; } };
  const session = { inputSources:[left,right], addEventListener(t,f){ (L[t]=L[t]||[]).push(f); }, updateRenderState(o){ this.renderState=o; },
    requestReferenceSpace: async (t) => ({type:t}), requestAnimationFrame(cb){ setTimeout(()=>{ M.frames++; cb(performance.now(), frame); }, 16); return 1; }, end(){ (L.end||[]).forEach(f=>f()); } };
  window.XRWebGLLayer = class { constructor(){ this.framebuffer=null; this.framebufferWidth=1400; this.framebufferHeight=820; } getViewport(v){ return v.eye==='left'?{x:0,y:0,width:700,height:820}:{x:700,y:0,width:700,height:820}; } };
  Object.defineProperty(navigator,'xr',{configurable:true, value:{ isSessionSupported: async()=>true, requestSession: async()=>session }});
  WebGL2RenderingContext.prototype.makeXRCompatible = async function(){};
})();
"""
LOC="(x,y,z)=>{ const p=M4.pt(M4.inv(rigMatrix()),x,y,z); return p; }"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':820}); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if ('GPU stall' not in m.text and 'ERR_' not in m.text) else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.add_init_script(MOCK)
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(500)
        print('new items', await pg.evaluate("JSON.stringify(__app.items.filter(i=>['fan','globe','microwave','mixer','drillpress'].includes(i.type)).map(i=>[i.type,+i.y.toFixed(3)]))"))
        await pg.click('#vrBtn'); await pg.wait_for_timeout(2500)
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(500)
        # руки в кадре
        await pg.evaluate("__xrmock.at(0.12,1.42,-0.32); __xrmock.atL(-0.14,1.40,-0.34); __xrmock.btn('right',0,false)"); await pg.wait_for_timeout(1200)
        await pg.screenshot(path=f'{OUT}/w1_hands.png')
        await pg.evaluate("__xrmock.btn('right',1,true)"); await pg.wait_for_timeout(1200); await pg.screenshot(path=f'{OUT}/w1b_fist.png'); await pg.evaluate("__xrmock.btn('right',1,false)")
        # настройки на X
        await pg.evaluate("__xrmock.btn('left',4,true)"); await pg.wait_for_timeout(500); await pg.evaluate("__xrmock.btn('left',4,false)"); await pg.wait_for_timeout(800)
        print('cfg on', await pg.evaluate("__app.xr.cfgOn"))
        await pg.screenshot(path=f'{OUT}/w2_cfg.png')
        pt=await pg.evaluate("""(()=>{ const r=__app.xr.cfgRects[2],u=(r.x+r.w/2)/1200,v=(r.y+r.h/2)/825,w=__app.xr.cfgNode.world,lx=(u-0.5)*0.96,ly=(0.5-v)*0.66; return [w[0]*lx+w[4]*ly+w[12],w[1]*lx+w[5]*ly+w[13],w[2]*lx+w[6]*ly+w[14]]; })()""")
        await pg.evaluate(f"__xrmock.aim({pt[0]},{pt[1]},{pt[2]})"); await pg.wait_for_timeout(800); await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(500)
        print('turn now', await pg.evaluate("__app.xr.cfg.turn"))
        await pg.evaluate("__app.xr.cfg.turn='snap30'; __app.xr.cfgOn=false")
        # карточка с размерами
        await pg.evaluate("(()=>{ const d=__app.items.find(i=>i.type==='desk'); teleportRig(d.x,d.z+1.6,0); })()"); await pg.wait_for_timeout(600)
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='desk'); __xrmock.aim(it.x+0.5, 0.745, it.z+0.2);})()"); await pg.wait_for_timeout(800)
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(1500)
        print('card', await pg.evaluate("__app.xr.card&&__app.xr.card.type"), 'dims', await pg.evaluate("!!__app.xr.dims"))
        await pg.screenshot(path=f'{OUT}/w3_card.png')
        # кружка: хват правой, поворот кисти, передача в левую
        mug=await pg.evaluate("(()=>{ const m=__app.items.find(i=>i.type==='mug'); return [m.x,m.y,m.z,m.size.h]; })()")
        lp=await pg.evaluate(f"({LOC})({mug[0]},{mug[1]+mug[3]/2},{mug[2]})")
        await pg.evaluate(f"__xrmock.at({lp[0]},{lp[1]},{lp[2]+0.04})"); await pg.wait_for_timeout(1000)
        await pg.evaluate("__xrmock.squeezeF('squeezestart','right')"); await pg.wait_for_timeout(500)
        await pg.evaluate(f"__xrmock.at({lp[0]},{lp[1]+0.2},{lp[2]+0.04},90)"); await pg.wait_for_timeout(1000)
        print('rotated in hand', await pg.evaluate("(()=>{ const m=__app.items.find(i=>i.type==='mug'); const W=m.root.fixed; return W?[+W[5].toFixed(2),+W[6].toFixed(2)]:null; })()"))
        await pg.evaluate(f"__xrmock.atL({lp[0]},{lp[1]+0.2},{lp[2]})"); await pg.wait_for_timeout(1000)
        await pg.evaluate("__xrmock.squeezeF('squeezestart','left')"); await pg.wait_for_timeout(600)
        print('holders', await pg.evaluate("JSON.stringify([...__app.xr.grab.entries()].map(([s,g])=>[s.handedness,g.it.type]))"))
        await pg.evaluate("__xrmock.squeezeF('squeezeend','right')"); await pg.wait_for_timeout(300)
        print('after right release still held', await pg.evaluate("JSON.stringify([...__app.xr.grab.entries()].map(([s,g])=>[s.handedness,g.it.type]))"))
        await pg.evaluate("__xrmock.squeezeF('squeezeend','left')"); await pg.wait_for_timeout(2500)
        print('mug dropped', await pg.evaluate("(()=>{ const m=__app.items.find(i=>i.type==='mug'); return [m.x,m.y,m.z,!!m.root.fixed].map(v=>typeof v==='number'?+v.toFixed(2):v); })()"))
        # вращение: шпиндель станка
        r=await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='drillpress'); let sp=null,st=null; (function w(n){ if(n.anim&&n.anim.type==='spin') sp=n; if(n.trig) st=n; n.children.forEach(w); })(it.root); toggleAnim(st.trig); return !!sp; })()")
        await pg.wait_for_timeout(1500)
        print('spindle phase', await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='drillpress'); let sp=null; (function w(n){ if(n.anim&&n.anim.type==='spin') sp=n; n.children.forEach(w); })(it.root); return +sp.anim.phase.toFixed(2); })()"))
        print('fan link', await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='fan'); let h=null; (function w(n){ if(n.anim&&n.anim.type==='osc') h=n; n.children.forEach(w); })(it.root); toggleAnim(h); return h.anim.link[0].anim.target; })()"))
        # перетаскивание мебели в стену — красный
        await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='roundtable'); teleportRig(it.x+1.2,it.z+1.6,0); })()"); await pg.wait_for_timeout(600)
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); __xrmock.aim(it.x, 0.74, it.z);})()"); await pg.wait_for_timeout(800)
        await pg.evaluate("__xrmock.squeeze('squeezestart')"); await pg.wait_for_timeout(500)
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='sofa'); __xrmock.aim(it.x, 0, it.z);})()"); await pg.wait_for_timeout(1500)
        print('drag bad', await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); return [it.bad, +it.x.toFixed(2), +it.z.toFixed(2)];})()"))
        await pg.screenshot(path=f'{OUT}/w4_bad.png')
        await pg.evaluate("__xrmock.squeeze('squeezeend')"); await pg.wait_for_timeout(500)
        print('after release', await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); return [it.bad, it.x, it.z];})()"))
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
