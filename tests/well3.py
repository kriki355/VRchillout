import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        # с нуля: новая комната, добавить этаж
        await pg.click('#clearBtn'); await pg.wait_for_timeout(900)
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(300)
        await pg.click('#addStorey'); await pg.wait_for_timeout(1500)
        print('fresh',await pg.evaluate("JSON.stringify([PRJ.storeys.map(S=>[S.hall,S.wings,S.stairs]),PRJ.lift,document.getElementById('toast').textContent])"))
        await pg.click('#lvBar button[data-k="0"]'); await pg.wait_for_timeout(800)
        await pg.screenshot(path='out/s26/w8_fresh.png')
        await pg.click('#etabs button[data-tab=plan]'); await pg.wait_for_timeout(500); await pg.screenshot(path='out/s26/w9_plan.png')
        # ширина зала меняется на обоих этажах, клетка переезжает
        await pg.fill('#hallW',''); await pg.type('#hallW','10'); await pg.press('#hallW','Enter'); await pg.wait_for_timeout(800)
        print('resized',await pg.evaluate("JSON.stringify([PRJ.storeys.map(S=>[S.hall.W,wellOf(S)&&[wellOf(S).side,wellOf(S).offset],S.stairs]),PRJ.lift])"))
        # отсек сверху не налезает
        await pg.click('.addw button[data-w=E]'); await pg.wait_for_timeout(600)
        print('wings',await pg.evaluate("JSON.stringify(L.wings.map(g=>[g.side,g.offset,g.w,!!g.stair]))"), await pg.evaluate("document.getElementById('toast').textContent"))
        await pg.screenshot(path='out/s26/w10_after.png')
        # поставить лестницу руками в зале — должно быть нельзя
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(300)
        await pg.click('#putStairs'); await pg.wait_for_timeout(500)
        print('ghost',await pg.evaluate("JSON.stringify([state.placeStruct&&state.placeStruct.ref,state.invalid])"))
        await pg.evaluate("(()=>{ state.placeStruct.ref.x=3; state.placeStruct.ref.z=3; structMoved(state.placeStruct); })()")
        print('in hall',await pg.evaluate("state.invalid"))
        await pg.keyboard.press('Escape')
        # удалить 2 этаж — клетка пропадает
        await pg.click('#lvBar button[data-k="1"]'); await pg.wait_for_timeout(500)
        await pg.click('.storeyRow .del'); await pg.wait_for_timeout(200); await pg.click('.storeyRow .del'); await pg.wait_for_timeout(700)
        print('removed',await pg.evaluate("JSON.stringify([PRJ.storeys.length,L.wings,L.openings.filter(o=>o.kind==='arch').length,PRJ.lift])"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
