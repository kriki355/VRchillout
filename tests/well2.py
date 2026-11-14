import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':800}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(1000)
        # третий этаж
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(300)
        await pg.click('#addStorey'); await pg.wait_for_timeout(1500)
        print('3 storeys',await pg.evaluate("JSON.stringify([PRJ.storeys.map(S=>[wellOf(S)&&[wellOf(S).d],S.stairs]),ACT,document.getElementById('toast').textContent])"))
        await pg.screenshot(path='out/s26/w4_3rd.png')
        await pg.click('#lvBar button[data-k="0"]'); await pg.wait_for_timeout(800)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        # подъём по полосе A: из зала (x=17) к лестнице z=1, ось x
        await pg.evaluate("(()=>{ const c=state.cam; c.x=18.6; c.z=1.0; c.yaw=-Math.PI/2; c.pitch=0; })()"); await pg.wait_for_timeout(400)
        for i in range(24):
            await pg.evaluate("(()=>{ state.cam.x+=0.3; })()"); await pg.wait_for_timeout(250)
            if i%3==0: print('walk',i,await pg.evaluate("[ACT,+state.cam.x.toFixed(2),+state.cam.z.toFixed(2),+(state.fh||0).toFixed(2)]"))
            if i==9: await pg.screenshot(path='out/s26/w5a_mid.png')
        await pg.wait_for_timeout(500); await pg.screenshot(path='out/s26/w5_top1.png')
        # повернуться к залу по коридору
        await pg.evaluate("(()=>{ const c=state.cam; c.x=24.8; c.z=4.2; c.yaw=Math.PI/2+0.25; c.pitch=-0.15; })()"); await pg.wait_for_timeout(1200); await pg.screenshot(path='out/s26/w6_floor2_back.png')
        print('pos',await pg.evaluate("[ACT,state.cam.x,state.cam.z,state.cam.y,state.fh]"))
        await pg.evaluate("(()=>{ const c=state.cam; c.x=19.0; c.z=4.0; c.yaw=-Math.PI/2-0.5; c.pitch=-0.1; })()"); await pg.wait_for_timeout(1200); await pg.screenshot(path='out/s26/w7_floor2_in.png')
        print('stand f2',await pg.evaluate("[canStand(22.5,4.0),canStand(21,4.0),canStand(19,4.0),canStand(17,4.0),canStand(23.5,2.5)]"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
