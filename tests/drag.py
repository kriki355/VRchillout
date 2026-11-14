import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#etabs button[data-tab=furn]'); await pg.wait_for_timeout(400)
        card=await pg.query_selector('.cardI[data-t="loftpouf"]'); await card.scroll_into_view_if_needed(); bb=await card.bounding_box(); print(bb)
        n0=await pg.evaluate("__app.items.length")
        await pg.mouse.move(bb['x']+20,bb['y']+20); await pg.mouse.down()
        print('after down',await pg.evaluate("JSON.stringify(state.cardDrag)"))
        await pg.mouse.move(600,400,steps=8); print('mid',await pg.evaluate("JSON.stringify([state.cardDrag,!!state.place,document.elementFromPoint(600,400).id])"))
        await pg.mouse.move(int(sys.argv[2]),int(sys.argv[3]),steps=4); await pg.mouse.up(); await pg.wait_for_timeout(300)
        print('after',await pg.evaluate("JSON.stringify([state.cardDrag,!!state.place,state.invalid])"), (await pg.evaluate("__app.items.length"))-n0)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
