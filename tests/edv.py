import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#etools button[data-wm=full]'); await pg.wait_for_timeout(300)
        await pg.evaluate("(()=>{ const e=state.ed; e.tx=18; e.tz=4; e.dist=14; })()"); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='out/s26/e1_full.png')
        await pg.evaluate("(()=>{ const e=state.ed; e.yaw+=2.4; })()"); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='out/s26/e2_full_back.png')
        await pg.click('#etools button[data-wm=cut]'); await pg.wait_for_timeout(300)
        await pg.evaluate("(()=>{ const e=state.ed; e.yaw-=2.4; e.tx=12; e.tz=5; e.dist=30; })()"); await pg.wait_for_timeout(1200)
        await pg.click('#etabs button[data-tab=plan]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='out/s26/e3_plan.png')
        await pg.click('#etabs button[data-tab=furn]'); await pg.wait_for_timeout(800)
        await pg.screenshot(path='out/s26/e4_furn.png')
        await pg.click('.cgrp[data-g=tables] .ghead'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='out/s26/e5_furn_shut.png')
        await pg.click('#chips button[data-f=seats]'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='out/s26/e6_seats.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
