import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#etabs button[data-tab=furn]'); await pg.wait_for_timeout(400)
        card=await pg.query_selector('.cardI[data-t="loftpouf"]'); await card.scroll_into_view_if_needed(); bb=await card.bounding_box()
        n0=await pg.evaluate("items.length")
        X,Y=int(sys.argv[1]),int(sys.argv[2])
        await pg.mouse.move(bb['x']+20,bb['y']+20); await pg.mouse.down()
        await pg.mouse.move(X-30,Y-20,steps=8); await pg.mouse.move(X,Y,steps=4); await pg.wait_for_timeout(500)
        print('mid',await pg.evaluate("JSON.stringify([state.place&&[state.place.ghost.x,state.place.ghost.z],state.invalid])"))
        await pg.screenshot(path='out/s26/drag_mid.png')
        await pg.mouse.up(); await pg.wait_for_timeout(300)
        print('after',await pg.evaluate("JSON.stringify([!!state.place,state.invalid])"), (await pg.evaluate("items.length"))-n0)
        await pg.screenshot(path='out/s26/drag_after.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
