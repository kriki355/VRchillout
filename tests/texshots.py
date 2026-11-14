import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(str(e)))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(2500); await pg.click('#demoBtn'); await pg.wait_for_timeout(800)
        for t in sys.argv[3].split(','):
            await pg.evaluate(f"__app.startInspect(__app.items.find(i=>i.type==='{t}'))"); await pg.wait_for_timeout(1800)
            await pg.screenshot(path=f'{sys.argv[2]}/t_{t}.png'); await pg.evaluate("__app.closeInspect()"); await pg.wait_for_timeout(700)
        print(logs or 'ok'); await b.close()
asyncio.run(main())
