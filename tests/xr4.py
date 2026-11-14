import sys, asyncio
from playwright.async_api import async_playwright

URL = 'file://' + sys.argv[1]
OUT = sys.argv[2]

MOCK = r"""
(() => {
  const mk = (m) => ({ position:{x:m.m41,y:m.m42,z:m.m43}, orientation:{x:0,y:0,z:0,w:1}, matrix:m.toFloat32Array(), inverse:{matrix:m.inverse().toFloat32Array()} });
  const persp = (() => { const f=1/Math.tan(45*Math.PI/180), a=700/820, n=0.05, fa=200; const m=new Float32Array(16); m[0]=f/a; m[5]=f; m[10]=(fa+n)/(n-fa); m[11]=-1; m[14]=2*fa*n/(n-fa); return m; })();
  const L = {}; const left={handedness:'left', targetRaySpace:{id:'lray'}, gripSpace:{id:'lgrip'}, gamepad:{axes:[0,0,0,0]}}; const right={handedness:'right', targetRaySpace:{id:'rray'}, gripSpace:{id:'rgrip'}, gamepad:{axes:[0,0,0,0]}};
  const M = window.__xrmock = { head: mk(new DOMMatrix().translate(0,1.6,0)), left: mk(new DOMMatrix().translate(-0.2,1.2,-0.3).rotateAxisAngle(1,0,0,-70)), right: mk(new DOMMatrix().translate(0.2,1.3,-0.1)), leftSrc:left, rightSrc:right, frames:0,
    aim(wx,wy,wz){ const xr=__app.xr; const c=Math.cos(xr.rig.yaw), s=Math.sin(xr.rig.yaw); const dx0=wx-xr.rig.x, dz0=wz-xr.rig.z; const lx=c*dx0 - s*dz0, lz=s*dx0 + c*dz0, ly=wy-xr.rig.y;
      const o=[0.2,1.3,-0.1], d=[lx-o[0], ly-o[1], lz-o[2]]; const yaw=Math.atan2(-d[0],-d[2])*180/Math.PI, pitch=Math.atan2(d[1],Math.hypot(d[0],d[2]))*180/Math.PI;
      M.right = mk(new DOMMatrix().translate(...o).rotateAxisAngle(0,1,0,yaw).rotateAxisAngle(1,0,0,pitch)); },
    select(){ (L.select||[]).forEach(f=>f({inputSource:right})); }, squeeze(t){ (L[t]||[]).forEach(f=>f({inputSource:right})); } };
  const frame = { getViewerPose(){ return {transform:M.head, views:[{eye:'left',projectionMatrix:persp,transform:M.head},{eye:'right',projectionMatrix:persp,transform:M.head}]}; },
                  getPose(space){ return {transform: space.id==='lgrip'||space.id==='lray' ? M.left : M.right}; } };
  const session = { inputSources:[left,right], addEventListener(t,f){ (L[t]=L[t]||[]).push(f); }, updateRenderState(o){ this.renderState=o; },
    requestReferenceSpace: async (t) => ({type:t}), requestAnimationFrame(cb){ setTimeout(()=>{ M.frames++; cb(performance.now(), frame); }, 16); return 1; }, end(){ (L.end||[]).forEach(f=>f()); } };
  window.XRWebGLLayer = class { constructor(){ this.framebuffer=null; this.framebufferWidth=1400; this.framebufferHeight=820; } getViewport(v){ return v.eye==='left'?{x:0,y:0,width:700,height:820}:{x:700,y:0,width:700,height:820}; } };
  Object.defineProperty(navigator,'xr',{configurable:true, value:{ isSessionSupported: async()=>true, requestSession: async()=>session }});
  WebGL2RenderingContext.prototype.makeXRCompatible = async function(){};
})();
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width':1400,'height':820})
        logs=[]; pg.on('console', lambda m: logs.append(f'{m.type}: {m.text}')); pg.on('pageerror', lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.add_init_script(MOCK)
        await pg.goto(URL); await pg.wait_for_timeout(1200)
        print('button:', await pg.inner_text('#vrBtn'))
        await pg.evaluate('__app.loadLayout(__app.DEMO)'); await pg.wait_for_timeout(300)
        await pg.click('#vrBtn'); await pg.wait_for_timeout(800)
        print('session:', await pg.evaluate("!!__app.xr.session"), 'frames', await pg.evaluate("__xrmock.frames"))
        print('rig0', await pg.evaluate("JSON.stringify(__app.xr.rig)"))
        await pg.screenshot(path=f'{OUT}/x1_enter.png')
        # телепорт: целимся в пол впереди
        await pg.evaluate("(()=>{const r=__app.xr.rig; __xrmock.aim(r.x-1.5, 0, r.z-3);})()"); await pg.wait_for_timeout(600)
        print('hit floor:', await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h? h[1].kind : null;})()"))
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(600)
        print('rig after teleport', await pg.evaluate("JSON.stringify(__app.xr.rig)"))
        # зона «Офис» через панель на руке: вызываем напрямую через телепорт зоны
        await pg.evaluate("""(()=>{ const b={minX:1e9,minZ:1e9,maxX:-1e9,maxZ:-1e9}; for(const it of __app.items){ const d=CATALOG[it.type]; if(d.small||d.cat!=='office'||it.type==='plant'||it.type==='whiteboard') continue; const r=Math.max(it.size.w,it.size.d)/2+0.2; b.minX=Math.min(b.minX,it.x-r); b.maxX=Math.max(b.maxX,it.x+r); b.minZ=Math.min(b.minZ,it.z-r); b.maxZ=Math.max(b.maxZ,it.z+r); } const vp=zoneViewpoint(b); teleportRig(vp.x,vp.z,vp.yaw); })()"""); await pg.wait_for_timeout(800)
        print('rig office', await pg.evaluate("JSON.stringify(__app.xr.rig)"))
        # дверца шкафа: целимся в переднюю плоскость первого шкафа
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='cabinet'); __xrmock.aim(it.x-0.2, 1.1, it.z+0.25);})()"); await pg.wait_for_timeout(600)
        h = await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h? {k:h[1].kind, inter:h[1].inter?h[1].inter.anim.label:null, type:h[1].item?h[1].item.type:null} : null;})()")
        print('hit cabinet:', h)
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(2800)
        print('door target:', await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='cabinet'); let r=[]; (function w(n){ if(n.anim) r.push(n.anim.target+':'+n.anim.t.toFixed(2)); n.children.forEach(w); })(it.root); return r.join(',');})()"))
        # карточка: целимся в стол
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='desk'); __xrmock.aim(it.x-0.72, 0.745, it.z+0.2);})()"); await pg.wait_for_timeout(600)
        h = await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h? {k:h[1].kind, type:h[1].item?h[1].item.type:null, inter:!!h[1].inter} : null;})()")
        print('hit desk:', h)
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(1000)
        print('vr card:', await pg.evaluate("__app.xr.card ? __app.xr.card.type : null"))
        await pg.screenshot(path=f'{OUT}/x2_card.png')
        # кнопка «Другой вариант» на карточке: целимся в её левую нижнюю часть
        await pg.evaluate("""(()=>{ const n=__app.xr.cardNode; const w=n.world; const u=0.12, v=0.9; const lx=(u-0.5)*0.9, ly=(0.5-v)*0.6; const p=[w[0]*lx+w[4]*ly+w[12], w[1]*lx+w[5]*ly+w[13], w[2]*lx+w[6]*ly+w[14]]; __xrmock.aim(...p); })()"""); await pg.wait_for_timeout(600)
        print('hit card panel:', await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h? h[1].kind+':'+(h[1].panel?h[1].panel.type:'') : null;})()"))
        v0 = await pg.evaluate("__app.xr.card.variant")
        await pg.evaluate("__xrmock.select()"); await pg.wait_for_timeout(600)
        print('variant', v0, '->', await pg.evaluate("__app.xr.card.variant"))
        # стики
        r0 = await pg.evaluate("JSON.stringify(__app.xr.rig)")
        await pg.evaluate("__xrmock.rightSrc.gamepad.axes=[0,0,1,0]"); await pg.wait_for_timeout(600); await pg.evaluate("__xrmock.rightSrc.gamepad.axes=[0,0,0,0]"); await pg.wait_for_timeout(600)
        print('snap turn', r0, '->', await pg.evaluate("JSON.stringify(__app.xr.rig)"))
        await pg.evaluate("__xrmock.leftSrc.gamepad.axes=[0,0,0,-1]"); await pg.wait_for_timeout(2000); await pg.evaluate("__xrmock.leftSrc.gamepad.axes=[0,0,0,0]")
        print('walk', await pg.evaluate("JSON.stringify(__app.xr.rig)"))
        await pg.screenshot(path=f'{OUT}/x3_after.png')
        await pg.evaluate('(()=>{ __app.xr.card=null; __app.xr.cardNode=null; })()'); await pg.wait_for_timeout(2400)
        print('draw entries:', await pg.evaluate('__app.drawCount()'))
        # хват мелкого предмета
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='laptop'); __xrmock.aim(it.x, it.y+0.01, it.z+0.05);})()"); await pg.wait_for_timeout(600)
        print('aim laptop:', await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h? h[1].kind+':'+(h[1].item?h[1].item.type:'') : null;})()"))
        await pg.evaluate("__xrmock.squeeze('squeezestart')"); await pg.wait_for_timeout(2000)
        print('grabbed:', await pg.evaluate("[...__app.xr.grab.values()].map(g=>g.it.type+':'+g.mode).join()"), 'laptop at', await pg.evaluate("(()=>{const m=__app.items.find(i=>i.type==='laptop'); return [+m.x.toFixed(2),+m.y.toFixed(2),+m.z.toFixed(2)];})()"))
        await pg.screenshot(path=f'{OUT}/x5_hold.png')
        await pg.evaluate("__xrmock.squeeze('squeezeend')"); await pg.wait_for_timeout(6000)
        print('after release laptop at', await pg.evaluate("(()=>{const m=__app.items.find(i=>i.type==='laptop'); return [+m.x.toFixed(2),+m.y.toFixed(3),+m.z.toFixed(2)];})()"), 'grab size', await pg.evaluate("__app.xr.grab.size"))
        # перетаскивание крупной мебели
        c0 = await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); return [it.x,it.z];})()")
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); __xrmock.aim(it.x, 0.74, it.z);})()"); await pg.wait_for_timeout(600)
        print('aim table:', await pg.evaluate("(()=>{const h=[...__app.xr.hits.entries()].find(([s])=>s.handedness==='right'); return h? h[1].kind+':'+(h[1].item?h[1].item.type:'') : null;})()"))
        await pg.evaluate("__xrmock.squeeze('squeezestart')"); await pg.wait_for_timeout(600)
        print('grab:', await pg.evaluate("[...__app.xr.grab.values()].map(g=>g.it.type+':'+g.mode).join()"))
        await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); __xrmock.aim(it.x+1.0, 0, it.z-0.6);})()"); await pg.wait_for_timeout(1600)
        print('ray floor', await pg.evaluate("(()=>{ const xr=__app.xr; const r=xr.rig; const c=Math.cos(r.yaw),s=Math.sin(r.yaw); const m=__xrmock.right.matrix; const lo=[m[12],m[13],m[14]], ld=[-m[8],-m[9],-m[10]]; const o=[r.x+c*lo[0]+s*lo[2], r.y+lo[1], r.z-s*lo[0]+c*lo[2]], d=[c*ld[0]+s*ld[2], ld[1], -s*ld[0]+c*ld[2]]; const t=-o[1]/d[1]; const g=[...xr.grab.values()][0]; return [o[0]+d[0]*t, o[2]+d[2]*t, g&&g.dx, g&&g.dz]; })()"))
        print('during drag', await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); return [it.x,it.z, __app.placeIssue(it)];})()"))
        await pg.evaluate("__xrmock.squeeze('squeezeend')"); await pg.wait_for_timeout(600)
        print('roundtable', c0, '->', await pg.evaluate("(()=>{const it=__app.items.find(i=>i.type==='roundtable'); return [it.x,it.z];})()"))
        await pg.evaluate("__app.xr.session.end()"); await pg.wait_for_timeout(1600)
        print('ended, session=', await pg.evaluate("!!__app.xr.session"))
        await pg.screenshot(path=f'{OUT}/x4_back.png')
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
