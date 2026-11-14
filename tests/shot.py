import sys, asyncio, json
from playwright.async_api import async_playwright

URL = 'file://' + sys.argv[1]
OUT = sys.argv[2]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width': 1400, 'height': 820})
        logs = []
        pg.on('console', lambda m: logs.append(f'{m.type}: {m.text}'))
        pg.on('pageerror', lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(URL)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'{OUT}/1_walk.png')
        # клик по шкафу: откроем карточку через зону «Офис»
        await pg.evaluate("__app.goZone('office')")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{OUT}/2_office.png')
        # найти и кликнуть по дверце шкафа в центре экрана — ищем точку с интерактивом
        found = await pg.evaluate("""() => {
          const c=document.getElementById('gl'); const r=c.getBoundingClientRect(); let res=[];
          for(let y=200;y<700;y+=20) for(let x=100;x<1300;x+=20){ const ray=__app.screenRay(x,y); const h=__app.pick(ray.o,ray.d); if(h&&h.kind==='item'){ res.push({x,y,inter:h.inter?h.inter.anim.label:null,type:h.item.type,t:h.t}); } }
          return res; }""")
        doors = [f for f in found if f['inter'] == 'Дверца' and f['type'] == 'cabinet']
        items = [f for f in found if not f['inter']]
        print('hits', len(found), 'doors', len(doors), 'plain', len(items))
        if doors:
            d = doors[len(doors)//2]
            await pg.mouse.click(d['x'], d['y'])
            await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/3_door.png')
        if items:
            it = [i for i in items if i['type'] == 'desk'] or items
            it = it[len(it)//2]
            await pg.mouse.click(it['x'], it['y'])
            await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/4_card.png')
        # общепит
        await pg.evaluate("document.getElementById('card').style.display='none'; __app.goZone('catering')")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{OUT}/5_catering.png')
        await pg.evaluate("__app.goZone('production')")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{OUT}/6_production.png')
        # редактор
        await pg.click('#mEdit')
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=f'{OUT}/7_editor.png')
        # добавить отсек на юг и предмет
        await pg.click('#addWing')
        await pg.wait_for_timeout(300)
        await pg.evaluate("document.querySelectorAll('#catalog button')[0].click()")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=f'{OUT}/8_editor_wing.png')
        lay = await pg.evaluate("JSON.stringify(__app.serialize())")
        print('layout items', len(json.loads(lay)['items']), 'wings', len(json.loads(lay)['wings']))
        await pg.click('#goWalk')
        await pg.wait_for_timeout(600)
        # пройтись вперёд W
        await pg.keyboard.down('KeyW'); await pg.wait_for_timeout(700); await pg.keyboard.up('KeyW')
        await pg.screenshot(path=f'{OUT}/9_walk_after.png')
        print('\n'.join(logs) or 'no console output')
        await b.close()

asyncio.run(main())
