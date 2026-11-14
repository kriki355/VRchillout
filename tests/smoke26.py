import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        # выбрать предмет кликом
        await pg.evaluate("(()=>{ state.selected=items.find(i=>i.type==='sofa'); updateSel(); })()"); await pg.wait_for_timeout(600)
        await pg.screenshot(path='out/s26/s1_sel.png')
        await pg.keyboard.press('KeyR'); await pg.wait_for_timeout(300)
        await pg.click('#sbDup'); await pg.wait_for_timeout(300)
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(500)
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(500)
        await pg.keyboard.press('Control+y'); await pg.wait_for_timeout(500)
        print('undo ok',await pg.evaluate("[items.length,PRJ.storeys.length,!!wellOf(PRJ.storeys[0]),PRJ.storeys[0].stairs.length]"))
        # этаж 2, отделка клетки
        await pg.click('#lvBar button[data-k="1"]'); await pg.wait_for_timeout(700)
        await pg.click('#etabs button[data-tab=finish]'); await pg.wait_for_timeout(300)
        btns=await pg.evaluate("[...document.querySelectorAll('#roomPick button')].map(b=>b.textContent)"); print(btns)
        await pg.click('#roomPick button:last-child'); await pg.wait_for_timeout(300)
        await pg.click('#floors button[data-k=laminate]'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='out/s26/s2_toast.png')
        await pg.click('#lvBar button[data-k="0"]'); await pg.wait_for_timeout(700)
        await pg.click('#mWalk'); await pg.wait_for_timeout(1500)
        await pg.click('#mEdit'); await pg.wait_for_timeout(800)
        # сохранить-загрузить
        d=await pg.evaluate("JSON.stringify(serialize())"); await pg.evaluate(f"loadLayout(JSON.parse({d!r}),true)"); await pg.wait_for_timeout(600)
        print('reload',await pg.evaluate("[PRJ.storeys.map(S=>S.wings.length),PRJ.storeys.map(S=>S.stairs.length),!!PRJ.lift]"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
