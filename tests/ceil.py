import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':700,'height':440})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600); await pg.click('#mWalk'); await pg.wait_for_timeout(400)
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=6; c.z=10; c.yaw=0; c.pitch=0.45; })()")
        for k in ['armstrong','gkl','rack','grill','woodslat','stretch']:
            await pg.evaluate(f"(()=>{{ L.ceil='{k}'; applyCeil(); }})()"); await pg.wait_for_timeout(1300); await pg.screenshot(path=f'out/s18/c_{k}.png')
        await b.close()
asyncio.run(main())
