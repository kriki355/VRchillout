import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1440,'height':860}); logs=[]; pg.on('pageerror',lambda e: logs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1800)
        await pg.mouse.move(1248,375); await pg.wait_for_timeout(300); await pg.mouse.down()
        for i in range(1,9): await pg.mouse.move(1248,375-i*12); await pg.wait_for_timeout(120)
        await pg.mouse.up(); await pg.wait_for_timeout(400)
        print('wallH after drag:', await pg.evaluate("__app.L.wallH"), 'undo stack', await pg.evaluate("__app.hist.undo.length"))
        await pg.screenshot(path=sys.argv[2]+'/h2.png'); print(logs or 'ok'); await b.close()
asyncio.run(main())
