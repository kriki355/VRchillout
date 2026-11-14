import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        async def cam(x,z,yaw,pitch,n,w=1500):
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s26/{n}.png')
        await cam(12.5,1.3,0,0.1,'z1_n_wing_corner')
        await cam(17.4,1.3,0.0,0.1,'z2_ne')
        await cam(16.8,0.8,-1.57,0.1,'z3_well_left')
        await cam(16.8,6.5,-1.57,0.1,'z4_well_right')
        await cam(13.0,-1.5,-2.3,0.1,'z5_wing_inside')
        await cam(19.5,6.0,2.6,0.05,'z6_well_inside')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
