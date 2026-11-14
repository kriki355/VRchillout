import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        for t in ['plan','finish','build','furn']:
            await pg.click(f'#etabs button[data-tab="{t}"]'); await pg.wait_for_timeout(500); await pg.screenshot(path=f'out/s26/t_{t}.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
