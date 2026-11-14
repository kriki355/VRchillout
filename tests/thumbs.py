import sys, asyncio, base64
from playwright.async_api import async_playwright
KEYS=sys.argv[2].split(',')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':640}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(5000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800)
        for k in KEYS:
            await pg.evaluate(f"(()=>{{ const it=__app.addItem?null:null; }})()")
            await pg.evaluate(f"(()=>{{ const it=makeItem({{type:'{k}',x:9,z:9}}); items.push(it); __app.startInspect(it); }})()"); await pg.wait_for_timeout(2200)
            await pg.screenshot(path=f'out/s18/t_{k}.png'); await pg.evaluate("__app.closeInspect()"); await pg.wait_for_timeout(700)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
