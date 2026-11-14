import sys, asyncio, json
from playwright.async_api import async_playwright
URL='file://'+sys.argv[1]; OUT=sys.argv[2]
PROJ = """(p)=>{ const vp=__app.state.lastVP; const c=[vp[0]*p[0]+vp[4]*p[1]+vp[8]*p[2]+vp[12],vp[1]*p[0]+vp[5]*p[1]+vp[9]*p[2]+vp[13],vp[3]*p[0]+vp[7]*p[1]+vp[11]*p[2]+vp[15]];
  const r=document.getElementById('gl').getBoundingClientRect(); return [(c[0]/c[2]*0.5+0.5)*r.width, (0.5-c[1]/c[2]*0.5)*r.height]; }"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1440,'height':860}); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if ('GPU stall' not in m.text and 'ERR_TUNNEL' not in m.text) else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        O="JSON.stringify(__app.openings.map(o=>[o.kind,o.x,o.z,o.w,!!o.ghost]))"
        print('empty openings', await pg.evaluate(O))
        await pg.click('[data-wm="full"]'); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/o1_empty_full.png')
        # поставить дверь на северную стену через UI
        await pg.click('#opn button[data-k="door"]'); await pg.wait_for_timeout(300)
        x,y=await pg.evaluate(f"({PROJ})([0.9,1.0,0.02])")
        await pg.mouse.move(x-5,y); await pg.mouse.move(x,y); await pg.wait_for_timeout(400)
        print('ghost', await pg.evaluate(O), 'invalid', await pg.evaluate("__app.state.invalid"))
        await pg.screenshot(path=f'{OUT}/o2_ghost.png')
        await pg.mouse.click(x,y); await pg.wait_for_timeout(400)
        print('after place', await pg.evaluate(O), 'sel', await pg.evaluate("__app.state.selOpen&&__app.state.selOpen.kind"))
        await pg.screenshot(path=f'{OUT}/o3_placed.png')
        # недопустимо: поверх окна
        await pg.click('#opn button[data-k="window"]'); await pg.wait_for_timeout(300)
        x2,y2=await pg.evaluate(f"({PROJ})([2.5,1.5,0.02])"); await pg.mouse.move(x2,y2); await pg.wait_for_timeout(300)
        print('over window invalid:', await pg.evaluate("__app.state.invalid"))
        await pg.mouse.click(x2,y2); await pg.wait_for_timeout(300)
        print('still placing', await pg.evaluate("!!__app.state.placeOpen"))
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
        print('after esc', await pg.evaluate(O))
        # выбрать окно и перетащить
        x3,y3=await pg.evaluate(f"({PROJ})([5.6,1.6,0.03])")
        await pg.mouse.move(x3,y3); await pg.mouse.down(); await pg.wait_for_timeout(100)
        x4,y4=await pg.evaluate(f"({PROJ})([7.0,1.6,0.03])")
        for k in range(1,6): await pg.mouse.move(x3+(x4-x3)*k/5,y3+(y4-y3)*k/5); await pg.wait_for_timeout(80)
        await pg.mouse.up(); await pg.wait_for_timeout(300)
        print('after drag', await pg.evaluate(O), 'hist', await pg.evaluate("__app.hist.undo.length"))
        await pg.click('#sbWide'); await pg.wait_for_timeout(200); await pg.click('#sbWide'); await pg.wait_for_timeout(200)
        print('after wide', await pg.evaluate(O), await pg.evaluate("document.getElementById('selName').textContent"))
        await pg.screenshot(path=f'{OUT}/o4_drag.png')
        await pg.keyboard.press('Delete'); await pg.wait_for_timeout(300); print('after del', len(json.loads(await pg.evaluate(O))))
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(500); print('after undo', len(json.loads(await pg.evaluate(O))))
        # ворота на восточную стену через API
        await pg.evaluate("__app.startPlaceOpening('gate')"); await pg.wait_for_timeout(200)
        x5,y5=await pg.evaluate(f"({PROJ})([7.98,1.2,3.0])"); await pg.mouse.move(x5,y5); await pg.wait_for_timeout(300); await pg.mouse.click(x5,y5); await pg.wait_for_timeout(400)
        print('gate', await pg.evaluate(O))
        await pg.click('[data-wm="cut"]'); await pg.wait_for_timeout(1200); await pg.screenshot(path=f'{OUT}/o5_cut.png')
        # сериализация
        print('serialize openings', await pg.evaluate("JSON.stringify(__app.serialize().openings)"))
        # прогулка
        await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=4; c.z=4.6; c.yaw=0; c.pitch=0.05; })()"); await pg.wait_for_timeout(1200); await pg.screenshot(path=f'{OUT}/o6_walk_n.png')
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.x=3.0; c.z=3.0; c.yaw=-Math.PI/2; c.pitch=0.05; })()"); await pg.wait_for_timeout(1200); await pg.screenshot(path=f'{OUT}/o7_walk_e.png')
        # демо: автопроёмы
        await pg.click('#mEdit'); await pg.wait_for_timeout(300); await pg.click('#demoBtn'); await pg.wait_for_timeout(600)
        print('demo openings', await pg.evaluate("__app.openings.length"), await pg.evaluate("JSON.stringify(__app.openings.filter(o=>o.kind==='door'))"))
        await pg.click('#specBtn'); await pg.wait_for_timeout(300); print('spec has openings', await pg.evaluate("document.getElementById('specP').innerText.includes('Двери и окна')"))
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
