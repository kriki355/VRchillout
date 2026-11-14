import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1440,'height':860}); await pg.add_init_script("window.WebSocket=class{constructor(){this.readyState=0;} send(){} close(){}}")
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1200); await pg.click('#syncBtn'); await pg.wait_for_timeout(500)
        await pg.screenshot(path=sys.argv[2]); await b.close()
asyncio.run(main())
