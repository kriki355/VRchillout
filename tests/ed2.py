import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#etabs button[data-tab=plan]'); await pg.wait_for_timeout(500)
        await pg.evaluate("document.getElementById('wings').scrollIntoView()"); await pg.wait_for_timeout(500)
        await pg.screenshot(path='out/s26/f1_wings.png',clip={'x':0,'y':60,'width':370,'height':720})
        await pg.click('#etabs button[data-tab=finish]'); await pg.wait_for_timeout(500)
        await pg.click('#roomPick button[data-id="3"]'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='out/s26/f2_finish.png',clip={'x':0,'y':60,'width':370,'height':720})
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(500)
        await pg.evaluate("document.getElementById('structBox').scrollIntoView()"); await pg.wait_for_timeout(400)
        await pg.screenshot(path='out/s26/f3_build.png',clip={'x':0,'y':60,'width':370,'height':720})
        # высота в клетке и в отсеке разная
        await pg.click('#etabs button[data-tab=finish]'); await pg.wait_for_timeout(300)
        await pg.click('#roomPick button[data-id="2"]'); await pg.wait_for_timeout(300)
        for i in range(4): await pg.click('#rhPlus'); await pg.wait_for_timeout(150)
        print('heights',await pg.evaluate("JSON.stringify([roomH(1),roomH(2),roomH(3),topH(L),elev(1),PRJ.storeys[0].stairs])"))
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ const c=state.cam; c.x=14.0; c.z=2.5; c.yaw=0.25; c.pitch=0.45; })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s26/f4_wingceil.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
