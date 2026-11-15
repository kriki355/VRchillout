import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':800,'height':500})
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.evaluate("document.getElementById('demoBtn').click()"); await pg.wait_for_timeout(2000)
        print(await pg.evaluate("""(()=>{ const out=[]; for(const w of INWALLS){ const m=(w.a+w.b)/2, it={type:'desk',variant:0,x:w.h?w.a+0.9:w.c,z:w.h?w.c:w.a+0.9,rot:0,y:0}; const a=addItem(it); out.push(placeIssue(a)); items.splice(items.indexOf(a),1); } return JSON.stringify(out); })()"""))
        await b.close()
asyncio.run(main())
