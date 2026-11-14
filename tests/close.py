import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':760})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        await pg.evaluate("""(()=>{ const it=__app.items.find(i=>i.type==='combi'); const ns=[]; (function w(n){ if(n.anim) ns.push(n); n.children.forEach(w); })(it.root); ns.forEach(n=>__app.toggleAnim(n,it)); })()""")
        for n,x,z,yaw,pitch in [["combi1",14.0,-1.5,1.5708,-0.42],["combi2",13.75,-1.25,1.25,-0.3],["sofa1",2.4,8.4,1.5708,-0.4],["sofa2",2.0,9.6,0.9,-0.45]]:
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; __app.state.glide=null; }})()")
            await pg.wait_for_timeout(1800); await pg.screenshot(path=f'out/s18/{n}.png')
        await b.close()
asyncio.run(main())
