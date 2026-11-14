import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        mode=sys.argv[1]
        await pg.evaluate("(()=>{ const m=wallMat('wood'); m.col=[3,0,0]; m.color=[3,0,0]; m.tex=null; m.noTex=true; })()")
        if mode=='noshadow': await pg.evaluate('GFX.pc=0')
        if mode=='hidewood': await pg.evaluate("(()=>{ const wm=wallMat('wood'); for(const n of roomRoot.children) if(n.mat===wm) n.noDraw=true; })()")
        await pg.evaluate("(()=>{ const c=state.cam; c.x=14.0; c.z=2.5; c.yaw=0.25; c.pitch=0.45; })()"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'out/s26/dbg_{mode}.png',clip={'x':700,'y':360,'width':300,'height':260})
        print(await pg.evaluate("Object.keys(wallMat('wood'))"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
