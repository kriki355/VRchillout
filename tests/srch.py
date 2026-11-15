import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':600}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        for q in ['столы','холодильник','халадильник','печь','кресла офисные','свет','кофе','растения','шкаф ящики','тесто','мойка','пароконвектомат','противни']:
            r=await pg.evaluate("q=>Object.entries(CATALOG).map(([k,d])=>[k,searchScore(k,d,q)]).filter(x=>x[1]>0).sort((a,b)=>b[1]-a[1]).slice(0,6).map(x=>x[0]).join(',')",q)
            print(q,'->',r)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
