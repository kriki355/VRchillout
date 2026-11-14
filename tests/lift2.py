import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        print('stand on stairs',await pg.evaluate("[canStand(21.0,1.0),canStand(22.5,1.0)]"))
        await pg.click('#lvBar button[data-k="1"]'); await pg.wait_for_timeout(700)
        await pg.click('#mWalk'); await pg.wait_for_timeout(1000)
        await pg.evaluate("(()=>{ const c=state.cam; c.x=19.6; c.z=3.6; c.yaw=-2.2; c.pitch=-0.75; })()"); await pg.wait_for_timeout(1500)
        print(await pg.evaluate("[ACT,state.cam.y,state.fh]"))
        await pg.screenshot(path='out/s26/lift_f2.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
