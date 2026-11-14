import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':700,'height':440})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600); await pg.click('#mWalk'); await pg.wait_for_timeout(400)
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=11.5; c.z=10.5; c.yaw=0.6; c.pitch=-0.45; })()")
        for k in ['tile','laminate','parquet','ceramic','lino','carpet','epoxy']:
            await pg.evaluate(f"(()=>{{ L.floor='{k}'; applyFloor(); }})()"); await pg.wait_for_timeout(1300); await pg.screenshot(path=f'out/s18/f_{k}.png')
        await b.close()
asyncio.run(main())
