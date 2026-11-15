import asyncio, sys, json, time, math
from playwright.async_api import async_playwright
W,H=int(sys.argv[1]),int(sys.argv[2]); N=int(sys.argv[3])
MOCK=r"""
(() => {
  const mk=(m)=>({position:{x:m.m41,y:m.m42,z:m.m43},orientation:{x:0,y:0,z:0,w:1},matrix:m.toFloat32Array(),inverse:{matrix:m.inverse().toFloat32Array()}});
  const W=%W%,H=%H%; const persp=(()=>{ const f=1/Math.tan(36*Math.PI/180),a=W/H,n=0.05,fa=200; const m=new Float32Array(16); m[0]=f/a; m[5]=f; m[10]=(fa+n)/(n-fa); m[11]=-1; m[14]=2*fa*n/(n-fa); return m; })();
  const L={}; const left={handedness:'left',targetRaySpace:{id:'lray'},gripSpace:{id:'lgrip'},gamepad:{axes:[0,0,0,0],buttons:[0,1,2,3,4,5].map(()=>({pressed:false,value:0}))}}; const right={handedness:'right',targetRaySpace:{id:'rray'},gripSpace:{id:'rgrip'},gamepad:{axes:[0,0,0,0],buttons:[0,1,2,3,4,5].map(()=>({pressed:false,value:0}))}};
  const M=window.__xrmock={mk,head:mk(new DOMMatrix().translate(0,1.62,0)),left:mk(new DOMMatrix().translate(-0.2,1.2,-0.3)),right:mk(new DOMMatrix().translate(0.2,1.3,-0.3)),leftSrc:left,rightSrc:right,t:0,cb:null,
    fire(t,src){ (L[t]||[]).forEach(f=>f({inputSource:src==='left'?left:right,frame})); },
    step(ms){ M.t+=ms; const cb=M.cb; M.cb=null; if(cb) cb(M.t,frame); } };
  const frame={ getViewerPose(){ return {transform:M.head,views:[{eye:'left',projectionMatrix:persp,transform:M.head}]}; }, getPose(space){ return {transform: space.id==='lgrip'||space.id==='lray'?M.left:M.right}; } };
  const session={inputSources:[left,right],addEventListener(t,f){ (L[t]=L[t]||[]).push(f); },updateRenderState(o){ this.renderState=o; },requestReferenceSpace:async t=>({type:t}),requestAnimationFrame(cb){ M.cb=cb; return 1; },end(){ (L.end||[]).forEach(f=>f()); }};
  window.XRWebGLLayer=class{ constructor(){ this.framebuffer=null; this.framebufferWidth=W; this.framebufferHeight=H; } getViewport(v){ return {x:0,y:0,width:W,height:H}; } };
  Object.defineProperty(navigator,'xr',{configurable:true,value:{isSessionSupported:async()=>true,requestSession:async()=>session}});
  WebGL2RenderingContext.prototype.makeXRCompatible=async function(){};
})();
""".replace('%W%',str(W)).replace('%H%',str(H))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':W,'height':H}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.add_init_script(MOCK)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4000)
        await pg.evaluate("PERF.dyn=false; PERF.scale=1; QUAL.k=1"); await pg.click('#demoBtn'); await pg.wait_for_timeout(2500)
        await pg.add_style_tag(content="body>*:not(#gl){display:none!important}")
        await pg.evaluate("$('vrBtn').click()"); await pg.wait_for_timeout(2500)
        await pg.evaluate("__xrmock.fire('select','right')"); await pg.wait_for_timeout(500)
        t0=time.time()
        for i in range(N):
            await pg.evaluate("__xrmock.step(41.67)")
            await pg.screenshot(path=f'frames/t_{i:04d}.jpg',type='jpeg',quality=92)
        print('per frame',(time.time()-t0)/N)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
