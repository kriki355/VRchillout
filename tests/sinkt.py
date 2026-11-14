import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':700})
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(500)
        print(await pg.evaluate("""(()=>{ for(const it of [...items]) if(!isCeil(it)) items.splice(items.indexOf(it),1); const it=addItem({type:'sinktable',variant:0,x:4,z:3,rot:0,y:0}); const c=state.cam; c.x=3.62; c.z=3.9; c.yaw=0; c.pitch=-0.5; (function w(n){ if(n.anim&&n.anim.type==='scaleY') n.anim.target=1; n.children.forEach(w); })(it.root); window._it=it; return 1; })()"""))
        await pg.wait_for_timeout(1200)
        print(await pg.evaluate("(()=>{ const r=screenRay(450,350); const h=pick(r.o,r.d); return JSON.stringify([h&&h.kind,h&&!!h.inter,h&&h.point]); })()")); print(await pg.evaluate("""(()=>{ const r=screenRay(450,350); const out=[]; for(const e of drawList){ if(!e.item||!e.mesh) continue; const inv=M4.inv(e.w),lo=M4.pt(inv,...r.o),ld=M4.dir(inv,...r.d),t=rayAabb(lo,ld,e.mesh.mn,e.mesh.mx); if(t!==null){ let a=e.node,an=false; while(a&&!a.item){ if(a.anim){an=true;break;} a=a.parent; } out.push([+t.toFixed(3),an,e.mat===undefined]); } } out.sort((a,b)=>a[0]-b[0]); return JSON.stringify(out.slice(0,12)); })()"""))
        await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s26/sink2.png'); print(await pg.evaluate("(()=>{ let r=null; (function w(n){ if(n.anim&&n.anim.type==='scaleY') r=[n.pos,n.anim.t,n.children.length]; n.children.forEach(w); })(window._it.root); return JSON.stringify(r); })()")); await b.close()
asyncio.run(main())
