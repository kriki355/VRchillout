import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True); pg=await ctx.new_page(); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(6000)
        await pg.screenshot(path='out/m/0.png')
        await pg.evaluate("document.getElementById('demoBtn')&&document.getElementById('demoBtn').click()"); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='out/m/1.png')
        await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='out/m/2.png')
        await pg.set_viewport_size({'width':844,'height':390}); await pg.wait_for_timeout(2000); await pg.screenshot(path='out/m/3.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
