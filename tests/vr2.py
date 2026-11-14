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
    select(){ (L.select||[]).forEach(f=>f({inputSource:right})); }, squeeze(t){ (L[t]||[]).forEach(f=>f({inputSource:right})); }, squeezeF(t){ (L[t]||[]).forEach(f=>f({inputSource:right,frame})); }, at(x,y,z){ M.right=mk(new DOMMatrix().translate(x,y,z)); } };
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
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if ('GPU stall' not in m.text and 'ERR_' not in m.text and 'manifest' not in m.text.lower()) else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.add_init_script(MOCK)
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(500)
        await pg.click('#vrBtn'); await pg.wait_for_timeout(3000)
        print('help on', await pg.evaluate("__app.xr.helpOn"))
        await pg.screenshot(path=f'{OUT}/v1_help.png')
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(800)
        print('help after select', await pg.evaluate("__app.xr.helpOn"))
        # застрять внутри стола и уйти стиком
        await pg.evaluate("(()=>{ const d=__app.items.find(i=>i.type==='desk'); teleportRig(d.x,d.z); })()"); await pg.wait_for_timeout(600)
        r0=await pg.evaluate("[__app.xr.head[0],__app.xr.head[2], canStand(__app.xr.head[0],__app.xr.head[2])]")
        await pg.evaluate("__xrmock.leftSrc.gamepad.axes=[0,0,0,1]"); await pg.wait_for_timeout(4000); await pg.evaluate("__xrmock.leftSrc.gamepad.axes=[0,0,0,0]")
        r1=await pg.evaluate("[__app.xr.head[0],__app.xr.head[2], canStand(__app.xr.head[0],__app.xr.head[2])]")
        print('stuck escape', r0, '->', r1)
        # телепорт стиком вперёд
        await pg.evaluate("teleportRig(9,8,0)"); await pg.wait_for_timeout(500)
        await pg.evaluate("__xrmock.aim(9.5,0,5.5)"); await pg.evaluate("__xrmock.rightSrc.gamepad.axes=[0,0,0,-1]"); await pg.wait_for_timeout(2500)
        print('aiming', await pg.evaluate("!!__app.xr.tpAim"), await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h&&h[1].kind})()"))
        await pg.screenshot(path=f'{OUT}/v2_tpaim.png')
        await pg.evaluate("__xrmock.rightSrc.gamepad.axes=[0,0,0,0]"); await pg.wait_for_timeout(2000)
        print('after stick teleport head', await pg.evaluate("__app.xr.head.map(v=>+v.toFixed(2))"))
        # прямой хват кружки
        mug=await pg.evaluate("(()=>{ const m=__app.items.find(i=>i.type==='mug'); return [m.x,m.y,m.z,m.size.h]; })()")
        await pg.evaluate(f"teleportRig({mug[0]},{mug[2]+0.6},0)"); await pg.wait_for_timeout(800)
        lp=await pg.evaluate(f"({LOC})({mug[0]},{mug[1]+mug[3]/2},{mug[2]})")
        await pg.evaluate(f"__xrmock.at({lp[0]},{lp[1]},{lp[2]+0.04})"); await pg.wait_for_timeout(1200)
        await pg.evaluate("__xrmock.squeezeF('squeezestart')"); await pg.wait_for_timeout(600)
        print('grab', await pg.evaluate("JSON.stringify([...__app.xr.grab.values()].map(g=>[g.it.type,g.mode,!!g.direct]))"))
        await pg.evaluate(f"__xrmock.at({lp[0]+0.3},{lp[1]+0.2},{lp[2]})"); await pg.wait_for_timeout(1500)
        print('mug moved', mug[:3], '->', await pg.evaluate("(()=>{ const m=__app.items.find(i=>i.type==='mug'); return [m.x,m.y,m.z].map(v=>+v.toFixed(2)); })()"))
        await pg.evaluate("__xrmock.squeezeF('squeezeend')"); await pg.wait_for_timeout(2500)
        print('mug after drop', await pg.evaluate("(()=>{ const m=__app.items.find(i=>i.type==='mug'); return [m.x,m.y,m.z].map(v=>+v.toFixed(2)); })()"))
        # касание дверцы шкафа
        tgt=await pg.evaluate("""(()=>{ const it=__app.items.find(i=>i.type==='cabinet'); let n=null; (function w(x){ if(!n&&x.anim) n=x; x.children.forEach(w); })(it.root); let m=null; (function w(x){ if(!m&&x.mesh) m=x; x.children.forEach(w); })(n);
          const c=[(m.mesh.mn[0]+m.mesh.mx[0])/2,(m.mesh.mn[1]+m.mesh.mx[1])/2,(m.mesh.mn[2]+m.mesh.mx[2])/2]; const p=M4.pt(m.world,...c); return {p:p, t:n.anim.target, x:it.x, z:it.z}; })()""")
        await pg.evaluate(f"teleportRig({tgt['x']},{tgt['z']+1.0},0)"); await pg.wait_for_timeout(800)
        lp=await pg.evaluate(f"({LOC})({tgt['p'][0]},{tgt['p'][1]},{tgt['p'][2]})")
        await pg.evaluate(f"__xrmock.at({lp[0]},{lp[1]},{lp[2]+0.07})"); await pg.wait_for_timeout(1500)
        t2=await pg.evaluate("""(()=>{ const it=__app.items.find(i=>i.type==='cabinet'); let r=[]; (function w(x){ if(x.anim) r.push(x.anim.target); x.children.forEach(w); })(it.root); return r; })()""")
        print('poke door targets before', tgt['t'], 'after', t2)
        await pg.screenshot(path=f'{OUT}/v3_poke.png')
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
