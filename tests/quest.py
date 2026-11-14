import sys, asyncio
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
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        ctx=await b.new_context(viewport={'width':1400,'height':820},user_agent='Mozilla/5.0 (X11; Linux x86_64; Quest 2) AppleWebKit/537.36 (KHTML, like Gecko) OculusBrowser/40.0 Chrome/136.0 VR Safari/537.36')
        pg=await ctx.new_page(); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if ('GPU stall' not in m.text and 'ERR_' not in m.text and 'manifest' not in m.text.lower()) else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.add_init_script(MOCK)
        await pg.goto(URL); await pg.wait_for_timeout(2000)
        print('overlay', await pg.evaluate("getComputedStyle(document.getElementById('vrStart')).display"))
        await pg.screenshot(path=f'{OUT}/q1_start.png')
        await pg.click('#vrGo'); await pg.wait_for_timeout(2500)
        print('session', await pg.evaluate("!!__app.xr.session"), 'mode', await pg.evaluate("__app.state.mode"), 'items', await pg.evaluate("__app.items.length"))
        await pg.evaluate("__app.xr.session.end()"); await pg.wait_for_timeout(1500)
        print('overlay after end', await pg.evaluate("getComputedStyle(document.getElementById('vrStart')).display"), await pg.inner_text('#vrGo'))
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
