import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        ctx=await b.new_context(viewport={'width':1100,'height':700},accept_downloads=True); pg=await ctx.new_page(); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#mWalk'); await pg.wait_for_timeout(600)
        async def cam(x,z,yaw,pitch,n,w=1400):
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s25/{n}.png')
        await cam(12.0,1.2,-0.15,0.15,'e1_seam')
        await cam(5.6,1.5,0,0.2,'e2_window')
        # лифт: ускоренная поездка
        await pg.evaluate("(()=>{ const c=state.cam; c.x=17; c.z=10.5; c.yaw=Math.PI/2; c.pitch=0.02; LIFT.at=0; LIFT.y=0; LIFT.st='idle'; })()"); await pg.wait_for_timeout(400)
        await pg.evaluate("liftPress({kind:'go',k:1})")
        for i in range(12):
            await pg.evaluate("(()=>{ for(let i=0;i<6;i++) update(0.05); })()"); await pg.wait_for_timeout(200)
            r=await pg.evaluate("[ACT,LIFT.st,+LIFT.y.toFixed(2),+state.cam.y.toFixed(2),+(state.fh||0).toFixed(2)]"); print('ride',i,r)
            if i==5: await pg.screenshot(path='out/s25/f1_mid.png')
        await pg.evaluate("(()=>{ for(let i=0;i<20;i++) update(0.05); })()"); await pg.wait_for_timeout(1200); await pg.screenshot(path='out/s25/f2_arrived.png')
        print('final',await pg.evaluate("[ACT,LIFT.st,LIFT.at,+LIFT.door.toFixed(2),canStand(15.6,10.5)]"))
        # избранное и КП
        await pg.evaluate("(()=>{ const its=allItems().filter(i=>!isCeil(i)); [0,3,5,9,12,20,31,45].forEach(i=>{ if(its[i]) toggleFav(its[i]); }); })()")
        await pg.click('#favBtn'); await pg.wait_for_timeout(800); await pg.screenshot(path='out/s25/g1_fav.png')
        async with pg.expect_download() as dl:
            await pg.click('#fKp')
        d=await dl.value; await d.save_as('out/s25/kp.html'); print('kp saved',d.suggested_filename)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
