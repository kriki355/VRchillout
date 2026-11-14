import sys, asyncio
from playwright.async_api import async_playwright
URL='file://'+sys.argv[1]; OUT=sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1440,'height':860}); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if ('GPU stall' not in m.text and 'ERR_TUNNEL' not in m.text) else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(500)
        await pg.click('#mWalk'); await pg.wait_for_timeout(400)
        # офис: вид на доску и растения
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=6.6; c.z=9.6; c.yaw=Math.atan2(-(2.6-6.6),-(5.6-9.6)); c.pitch=-0.12; __app.state.glide=null; })()")
        await pg.wait_for_timeout(1200); await pg.screenshot(path=f'{OUT}/e1_office.png')
        # дверь
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=9; c.z=7.5; c.yaw=Math.PI; c.pitch=0.05; })()")
        await pg.wait_for_timeout(1200); await pg.screenshot(path=f'{OUT}/e2_door.png')
        # карточка доски
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=6.0; c.z=6.4; c.yaw=Math.PI/2; c.pitch=-0.1; })()"); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='whiteboard'); __app.toggleAnim && 0; })()")
        await pg.evaluate("openPop(__app.items.find(i=>i.type==='whiteboard'))"); await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{OUT}/e3_pop.png')
        await pg.click('#popInsp'); await pg.wait_for_timeout(1800); await pg.screenshot(path=f'{OUT}/e4_insp.png')
        await pg.click('#iSpecBtn'); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'{OUT}/e5_specs.png')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(800)
        for t in ['extinguisher','plant']:
            await pg.evaluate(f"__app.startInspect(__app.items.find(i=>i.type==='{t}'))"); await pg.wait_for_timeout(1800); await pg.screenshot(path=f'{OUT}/e6_{t}.png'); await pg.evaluate("__app.closeInspect()"); await pg.wait_for_timeout(600)
        await pg.click('#mEdit'); await pg.wait_for_timeout(500); await pg.click('[data-wm="full"]'); await pg.wait_for_timeout(900); await pg.screenshot(path=f'{OUT}/e7_full.png')
        await pg.click('#specBtn'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'{OUT}/e8_spec.png')
        print('draws', await pg.evaluate("__app.drawCount()"))
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
