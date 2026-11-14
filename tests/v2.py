import sys, asyncio
from playwright.async_api import async_playwright

URL = 'file://' + sys.argv[1]
OUT = sys.argv[2]

PROJ = """(p)=>{ const vp=__app.state.lastVP; const c=[vp[0]*p[0]+vp[4]*p[1]+vp[8]*p[2]+vp[12],vp[1]*p[0]+vp[5]*p[1]+vp[9]*p[2]+vp[13],vp[3]*p[0]+vp[7]*p[1]+vp[11]*p[2]+vp[15]];
  const r=document.getElementById('gl').getBoundingClientRect(); return [(c[0]/c[2]*0.5+0.5)*r.width, (0.5-c[1]/c[2]*0.5)*r.height]; }"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width':1440,'height':860})
        logs=[]; pg.on('console', lambda m: logs.append(f'{m.type}: {m.text}') if 'GPU stall' not in m.text else None); pg.on('pageerror', lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{OUT}/a1_empty.png')
        # тянем метку восточной стены
        hs = await pg.evaluate("__app.edgeHandles()")
        e = [h for h in hs if h['e']=='E'][0]
        wy = await pg.evaluate("(()=>{const e=__app.state.ed,k=e.dist*0.075; return 0.35+0.35*k/0.6;})()")
        sx, sy = await pg.evaluate(f"({PROJ})([{e['x']},{wy},{e['z']}])")
        tx, ty = await pg.evaluate(f"({PROJ})([{e['x']+3},{0},{e['z']}])")
        await pg.mouse.move(sx, sy); await pg.wait_for_timeout(100); await pg.mouse.down();
        for i in range(1,11): await pg.mouse.move(sx+(tx-sx)*i/10, sy+(ty-sy)*i/10); await pg.wait_for_timeout(30)
        await pg.mouse.up(); await pg.wait_for_timeout(300)
        print('hall after drag', await pg.evaluate("JSON.stringify(__app.L.hall)"))
        await pg.click('.addw button[data-w="N"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f'{OUT}/a2_resized.png')
        await pg.click('#toStep2'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/a3_catalog.png')
        # ставим стол и ноутбук на него
        await pg.evaluate("__app.startPlace('desk')"); await pg.wait_for_timeout(100)
        cx, cy = await pg.evaluate(f"({PROJ})([(__app.L.hall.x+__app.L.hall.W/2),0,(__app.L.hall.z+__app.L.hall.D/2)])")
        await pg.mouse.move(cx, cy); await pg.wait_for_timeout(150); await pg.mouse.click(cx, cy); await pg.wait_for_timeout(300)
        desk = await pg.evaluate("JSON.stringify(__app.items.map(i=>[i.type,i.x,i.y,i.z]))"); print('items', desk)
        await pg.evaluate("__app.startPlace('laptop')"); await pg.wait_for_timeout(100)
        dx, dy = await pg.evaluate(f"({PROJ})([__app.items[0].x,0.75,__app.items[0].z])")
        await pg.mouse.move(dx-3, dy-3); await pg.wait_for_timeout(120); await pg.mouse.move(dx, dy); await pg.wait_for_timeout(120)
        await pg.screenshot(path=f'{OUT}/a4_placing.png')
        await pg.mouse.click(dx, dy); await pg.wait_for_timeout(300)
        print('items', await pg.evaluate("JSON.stringify(__app.items.map(i=>[i.type,+i.x.toFixed(2),+i.y.toFixed(3),+i.z.toFixed(2)]))"))
        await pg.screenshot(path=f'{OUT}/a5_selected.png')
        await pg.evaluate("__app.toggleGrid()"); await pg.wait_for_timeout(200)
        await pg.screenshot(path=f'{OUT}/a6_nogrid.png')
        # демо + прогулка
        await pg.click('#demoBtn'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/a7_demo_edit.png')
        await pg.evaluate("__app.goZone('office')"); await pg.wait_for_timeout(700)
        # навести на стол
        it = await pg.evaluate("(()=>{const i=__app.items.find(i=>i.type==='desk'); return [i.x-0.6,0.73,i.z+0.3];})()")
        hx, hy = await pg.evaluate(f"({PROJ})({it})")
        await pg.mouse.move(hx, hy); await pg.wait_for_timeout(250)
        await pg.screenshot(path=f'{OUT}/a8_hover.png')
        await pg.mouse.click(hx, hy); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/a9_pop.png')
        await pg.click('#popInsp'); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/b1_inspect.png')
        await pg.click('#iSpecBtn'); await pg.wait_for_timeout(1000)
        await pg.screenshot(path=f'{OUT}/b2_specs.png')
        await pg.click('#iSw [data-v="2"]'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f'{OUT}/b3_variant.png')
        await pg.click('#iClose'); await pg.wait_for_timeout(700)
        print('desk variant after close', await pg.evaluate("__app.items.find(i=>i.type==='desk').variant"), 'inspect', await pg.evaluate("!!__app.state.inspect"))
        # мелкий предмет — ложка
        await pg.evaluate("__app.startInspect(__app.items.find(i=>i.type==='spoon'))"); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/b4_spoon.png')
        await pg.evaluate("__app.toggleSpecs()"); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/b5_spoon_specs.png')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(600)
        await pg.evaluate("__app.startInspect(__app.items.find(i=>i.type==='laptop'))"); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/b6_laptop.png')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(600)
        await pg.evaluate("__app.goZone('catering')"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/b7_catering.png')
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
