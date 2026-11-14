import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':800}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if m.type=='error' else None)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.screenshot(path='out/s25/a0_start.png')
        await pg.click('#demoBtn'); await pg.wait_for_timeout(1200); await pg.screenshot(path='out/s25/a1_demo.png')
        print(await pg.evaluate("[PRJ.storeys.length,ACT,items.length,PRJ.storeys[1].its&&PRJ.storeys[1].its.length,JSON.stringify(PRJ.lift),elev(1)]"))
        for t in ['finish','build','furn']:
            await pg.click(f'#etabs button[data-tab={t}]'); await pg.wait_for_timeout(600); await pg.screenshot(path=f'out/s25/a2_{t}.png')
        await pg.click('#lvBar button[data-k="1"]'); await pg.wait_for_timeout(900); await pg.screenshot(path='out/s25/a3_lv2.png')
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(400); await pg.screenshot(path='out/s25/a3b_lv2build.png')
        await pg.click('#lvBar button[data-k="0"]'); await pg.wait_for_timeout(900)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        async def cam(x,z,yaw,pitch,n,w=1500):
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s25/{n}.png')
        await cam(14.5,1.5,-2.4,-0.05,'b1_stairs_view')
        await cam(15.2,9.0,-1.9,-0.02,'b2_lift_view')
        # подняться по лестнице: идём от z=2.5 к z=8.5 по x=17.25
        await pg.evaluate("(()=>{ const c=state.cam; c.x=17.25; c.z=2.4; c.yaw=Math.PI; c.pitch=0.0; })()"); await pg.wait_for_timeout(500)
        await pg.keyboard.down('KeyW'); 
        for i in range(8):
            await pg.wait_for_timeout(700)
            print('walk',i,await pg.evaluate("[ACT,+state.cam.z.toFixed(2),+state.cam.y.toFixed(2),+(state.fh||0).toFixed(2)]"))
            if i==2: await pg.screenshot(path='out/s25/b3_onstairs.png')
        await pg.keyboard.up('KeyW'); await pg.wait_for_timeout(600); await pg.screenshot(path='out/s25/b4_top.png')
        await cam(17.25,9.0,0,-0.35,'b5_look_down')
        await cam(6,6,-1.2,-0.1,'b6_floor2')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
