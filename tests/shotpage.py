import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for src,out,w,h,full in [('scheme.html','Схема_VR-шоурум.png',1920,1080,False),('catalog.html','Каталог_моделей.png',1920,1080,True)]:
            pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=2); await pg.goto('file://'+sys.argv[1]+'/'+src); await pg.wait_for_timeout(800)
            await pg.screenshot(path=sys.argv[1]+'/'+out,full_page=full); await pg.close()
        await b.close()
asyncio.run(main())
