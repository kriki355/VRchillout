import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':760}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s18/ed1.png')
        await pg.click('[data-f="light"]'); await pg.wait_for_timeout(500); await pg.screenshot(path='out/s18/ed2.png')
        await pg.evaluate("openPop(__app.items.find(i=>i.type==='lamp_square'))"); await pg.wait_for_timeout(600); await pg.screenshot(path='out/s18/ed3.png')
        await pg.click('[data-f="office"]'); await pg.wait_for_timeout(500); await pg.screenshot(path='out/s18/ed4.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
