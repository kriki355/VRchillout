import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ const c=state.cam; c.x=14.0; c.z=2.5; c.yaw=0.25; c.pitch=0.45; })()"); await pg.wait_for_timeout(1500)
        for y in [455,462,470]:
            print(y,await pg.evaluate(f"(()=>{{ const r=screenRay(850,{y}); const h=pick(r.o,r.d,{{}}); return h?[h.kind,h.point.map(v=>+v.toFixed(3))]:null; }})()"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
