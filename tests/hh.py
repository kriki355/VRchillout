import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':1440,'height':860}); logs=[]; pg.on('pageerror',lambda e: logs.append(str(e)))
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1800)
        hp=await pg.evaluate("""(()=>{ let r=null; return r; })()""")
        # находим метку высоты в сцене
        P=await pg.evaluate("""(()=>{ const vp=__app.state.lastVP; const hs=__app.edgeHandles(); return null; })()""")
        pos=await pg.evaluate("""(()=>{ const st=__app.state; const vp=st.lastVP; let n=null; for(const d of (window.__dl||[])) ; return null; })()""")
        await pg.screenshot(path=sys.argv[2]+'/h1.png')
        print(logs or 'ok')
        await b.close()
asyncio.run(main())
