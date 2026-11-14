import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.click('#mWalk'); await pg.wait_for_timeout(600)
        st=lambda: pg.evaluate("[ACT,+state.cam.x.toFixed(2),+state.cam.z.toFixed(2),+state.cam.y.toFixed(2),+(state.fh||0).toFixed(2),LIFT.st,+LIFT.y.toFixed(2),+LIFT.door.toFixed(2)]")
        # подъём: шаги по лестнице через canStand
        for z in [2.6,3.2,4.0,4.8,5.4,5.8,6.4,7.2,7.9,8.4]:
            ok=await pg.evaluate(f"(()=>{{ const c=state.cam; const can=canStand(17.25,{z}); c.x=17.25; c.z={z}; c.yaw=Math.PI; c.pitch=-0.1; return can; }})()"); await pg.wait_for_timeout(350); print('z',z,ok,await st())
        await pg.wait_for_timeout(800); await pg.screenshot(path='out/s25/c1_top.png')
        await pg.evaluate("(()=>{ const c=state.cam; c.x=16.0; c.z=8.5; c.yaw=0.6; c.pitch=-0.45; })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s25/c2_down_well.png')
        await pg.evaluate("(()=>{ const c=state.cam; c.x=9; c.z=6; c.yaw=-1.6; c.pitch=-0.12; })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s25/c3_floor2.png')
        # спуститься обратно по лестнице
        for z in [8.4,7.5,6.6,5.6,4.6,3.6,2.6]:
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.x=17.25; c.z={z}; }})()"); await pg.wait_for_timeout(350); print('down',z,await st())
        # лифт: вызвать на 1 этаже
        await pg.evaluate("(()=>{ const c=state.cam; c.x=14.6; c.z=10.5; c.yaw=-Math.PI/2; c.pitch=-0.1; })()"); await pg.wait_for_timeout(600)
        await pg.evaluate("liftPress({kind:'call',k:0})"); await pg.wait_for_timeout(2500); print('after call',await st()); await pg.screenshot(path='out/s25/d1_lift_open.png')
        # войти в кабину
        for x in [15.3,15.8,16.3,16.8,17.0]:
            ok=await pg.evaluate(f"(()=>{{ const c=state.cam; const can=canStand({x},10.5); if(can) c.x={x}; return can; }})()"); await pg.wait_for_timeout(250); print('enter',x,ok)
        await pg.evaluate("(()=>{ const c=state.cam; c.yaw=-Math.PI/2+Math.PI; c.pitch=-0.05; })()")
        await pg.evaluate("(()=>{ const c=state.cam; c.yaw=Math.PI/2; })()"); await pg.wait_for_timeout(800); await pg.screenshot(path='out/s25/d2_in_cabin.png')
        await pg.evaluate("liftPress({kind:'go',k:1})")
        for i in range(10):
            await pg.wait_for_timeout(900); print('ride',i,await st())
            if i==3: await pg.screenshot(path='out/s25/d3_riding.png')
        await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s25/d4_arrived.png')
        # выйти
        for x in [16.5,16.0,15.5,15.0]:
            ok=await pg.evaluate(f"(()=>{{ const c=state.cam; const can=canStand({x},10.5); if(can) c.x={x}; return can; }})()"); await pg.wait_for_timeout(250); print('exit',x,ok,await st())
        await pg.evaluate("(()=>{ const c=state.cam; c.x=13.0; c.z=10.5; c.yaw=-Math.PI/2; c.pitch=0.05; })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s25/d5_lift_floor2.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
