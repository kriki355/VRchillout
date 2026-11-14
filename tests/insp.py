import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':640})
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        for t in ['combi','sofa','desk']:
            await pg.evaluate(f"__app.startInspect(__app.items.find(i=>i.type==='{t}'))"); await pg.wait_for_timeout(2000); await pg.screenshot(path=f'out/s18/i_{t}.png'); await pg.evaluate("__app.closeInspect()"); await pg.wait_for_timeout(700)
        await b.close()
asyncio.run(main())
