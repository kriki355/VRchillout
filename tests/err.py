import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}')); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000); print('\n'.join(l for l in logs if 'ERR_TUNNEL' not in l)[:3000]); await b.close()
asyncio.run(main())
