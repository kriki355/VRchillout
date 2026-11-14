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
        r=await pg.evaluate("""JSON.stringify([roomSegs.filter(s=>!s.inner&&(Math.abs((s.h?s.z:s.x)-12.5)<0.01||Math.abs((s.h?s.z:s.x))<0.01)).map(s=>[s.h,s.x,s.z,s.a,s.b,s.n,s.room]),INWALLS.map(w=>[w.h,w.c,w.a,w.b,w.f])])""")
        print(r)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
