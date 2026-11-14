import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':700,'height':500}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#mWalk'); await pg.wait_for_timeout(400)
        await pg.evaluate("__app.startInspect(__app.items.find(i=>i.type==='meeting'))"); await pg.wait_for_timeout(2000)
        for k,yaw in enumerate([0.0,0.8]):
            await pg.evaluate(f"(()=>{{ const s=__app.state.inspect; s.auto=false; s.yaw={yaw}; }})()"); await pg.wait_for_timeout(1200); await pg.screenshot(path=f'out/s18/i{k}.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
