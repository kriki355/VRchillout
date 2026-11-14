import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':760})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=9; c.z=11.4; c.yaw=0; c.pitch=-0.12; })()")
        print(await pg.evaluate(sys.argv[2]))
        await pg.wait_for_timeout(1300); await pg.screenshot(path='out/dbg.png'); await b.close()
asyncio.run(main())
