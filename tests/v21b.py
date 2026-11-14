import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':600})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        async def cam(x,z,yaw,pitch,n,w=1600):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s18/{n}.png')
        await cam(11.2,1.2,-1.2,0.0,'w1_corner')
        await cam(18-0.6,1.0,1.3,0.0,'w2_corner')
        await cam(3.9,6.0,0.2,-0.75,'w3_button')
        await b.close()
asyncio.run(main())
