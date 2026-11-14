import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.evaluate("document.getElementById('demoBtn').click()"); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ for(const it of items){ const n=it.root.lampSw; if(n){ n.anim.t=n.anim.target=0; } } const c=state.cam; c.x=5.2; c.z=9.0; c.yaw=0.5; c.pitch=-0.45; })()"); await pg.wait_for_timeout(2500)
        print(await pg.evaluate("JSON.stringify(gatherLights().map(l=>[l.p.map(v=>+v.toFixed(1)),l.sh,l.tile,+l.on.toFixed(2),l.pow]))"))
        await pg.screenshot(path="out/s26/dark.png"); await pg.evaluate("(()=>{ for(const it of items){ it.size={w:0.0001,d:0.0001,h:it.size.h}; } })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path="out/s26/dark2.png")
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
