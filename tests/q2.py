import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':900,'height':500}); await pg.goto(sys.argv[1]); await pg.wait_for_timeout(2500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(500); await pg.click('#mWalk'); await pg.wait_for_timeout(400)
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=9; c.z=9.5; c.yaw=Math.PI; c.pitch=0.05; })()"); await pg.wait_for_timeout(1000)
        await pg.screenshot(path='out/v6/w_a.png')
        await pg.evaluate("SHD.on=false"); await pg.wait_for_timeout(1000); await pg.screenshot(path='out/v6/w_b.png')
        await pg.evaluate("SHD.on=true; window.__noLamps=true"); await pg.wait_for_timeout(1000); await pg.screenshot(path='out/v6/w_c.png')
        await b.close()
asyncio.run(main())
