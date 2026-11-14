import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        async def cam(x,z,yaw,pitch,n,w=1800):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s18/{n}.png')
        await cam(6.3,7.2,3.14,-0.35,'n1_loft')
        await cam(2.0,7.6,3.4,-0.3,'n2_pouf')
        await cam(15.4,1.4,-1.57,-0.1,'n3_oven')
        # крупная карта
        big=await pg.evaluate("(()=>{ const c=mkCanvas(800,800); drawMap(c.getContext('2d'),800,800,{x:__app.state.cam.x,z:__app.state.cam.z,yaw:__app.state.cam.yaw},true); return c.toDataURL('image/png'); })()")
        import base64; open('out/s18/n4_map.png','wb').write(base64.b64decode(big.split(',')[1]))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
