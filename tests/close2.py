import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        shots=[["g1",3.4,7.0,0,-0.35],["g2",4.6,6.5,0.8,-0.3]]
        for n,x,z,yaw,pitch in shots:
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'out/s18/{n}_off.png')
        await pg.evaluate("(()=>{ for(const t of ['gamedesk','standdesk']){ const it=__app.items.find(i=>i.type===t); (function w(n){ if(n.anim) __app.toggleAnim(n); n.children.forEach(w); })(it.root); } })()")
        await pg.wait_for_timeout(3500)
        for n,x,z,yaw,pitch in shots+[["s1",7.9,6.2,1.5708,-0.1],["l1",9,9.5,0,0.5]]:
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'out/s18/{n}_on.png')
        await b.close()
asyncio.run(main())
