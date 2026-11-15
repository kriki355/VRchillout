import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        logs=[]
        for w,h in [(1366,700),(1024,640)]:
            pg=await b.new_page(viewport={'width':w,'height':h})
            pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
            await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
            await pg.click('#setBtn'); await pg.wait_for_timeout(500); await pg.click('#fpsBtn'); await pg.wait_for_timeout(2500)
            print(w, await pg.evaluate("(()=>{ const t=$('top'); return [t.scrollWidth,t.clientWidth,PERF.scale,PERF.fps]; })()"))
            await pg.screenshot(path=f'out/s32/top{w}.png',clip={'x':0,'y':0,'width':w,'height':330})
            await pg.close()
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
