import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(); await pg.goto(sys.argv[1]); await pg.wait_for_timeout(2500)
        print(await pg.evaluate(sys.argv[2])); await b.close()
asyncio.run(main())
