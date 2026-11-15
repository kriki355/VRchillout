import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':760}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.evaluate("document.getElementById('demoBtn').click()"); await pg.wait_for_timeout(2500)
        for k in range(2):
            await pg.evaluate(f"setActive({k})"); await pg.wait_for_timeout(1200)
            r=await pg.evaluate("""(()=>{ const out=[]; for(const it of items){ if(isCeil(it)) continue; const q=placeIssue(it); if(q) out.push([it.type,it.x,it.z,q]); } return JSON.stringify({bad:out,well:L.wings.filter(g=>g.stair).map(g=>wingRect(g))}); })()""")
            print(k,r)
            await pg.evaluate("(()=>{ state.ed.dist=34; state.ed.pitch=1.05; state.ed.pitchT=1.05; state.ed.tx=L.hall.x+L.hall.W/2+1; state.ed.tz=L.hall.z+L.hall.D/2; })()"); await pg.wait_for_timeout(2500)
            await pg.screenshot(path=f'out/s32/demo{k}.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
