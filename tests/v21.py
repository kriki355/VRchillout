import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        print('iss',await pg.evaluate("JSON.stringify(__app.items.map(it=>[it.type,placeIssue(it)]).filter(r=>r[1]))"))
        async def cam(x,z,yaw,pitch,n,w=1600,y=None):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s18/{n}.png')
        await cam(11.6,7.4,3.14,-0.35,'v1_meeting')
        await cam(10.9,2.4,0,-0.15,'v2_rack')
        await cam(13.3,1.4,0.5,-0.05,'v3_corner')
        await cam(9,9,0,0.55,'v4_ceiling')
        await cam(6,9.5,0,0.08,'v5_windows')
        await cam(3.4,6.6,0,-0.6,'v6_gdesk')
        # дверь: ручка
        await cam(14.6,1.4,0,-0.1,'v7_door',1200)
        await pg.mouse.click(560,400); await pg.wait_for_timeout(120); await pg.screenshot(path='out/s18/v7b_handle.png'); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s18/v7c_open.png')
        # хлыст: взять и щёлкнуть
        await cam(8.0,4.6,0,-0.4,'v8_whip_table')
        await pg.evaluate("__app.takeItem(__app.items.find(i=>i.type==='whip'))"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s18/v8b_held.png')
        await pg.mouse.click(560,400); await pg.wait_for_timeout(250); await pg.screenshot(path='out/s18/v8c_flick.png')
        print('draws',await pg.evaluate("__app.drawCount()"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
