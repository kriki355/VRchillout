import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        print(await pg.evaluate("JSON.stringify([PRJ.lift,LIFT.btns.map(b=>[b.liftBtn.kind,b.liftBtn.k,b.world?[b.world[12],b.world[13],b.world[14]].map(v=>+v.toFixed(2)):null])])"))
        # встать в кабину и навести взгляд на кнопку кабины
        r=await pg.evaluate("""(()=>{ const L0=PRJ.lift,c=state.cam; c.x=L0.x; c.z=L0.z; return 1; })()""")
        await pg.wait_for_timeout(1200)
        res=await pg.evaluate("""(()=>{ const b=LIFT.btns.find(b=>b.liftBtn.kind!=='call'&&b.world); if(!b) return 'nobtn'; const w=b.world,c=state.cam,dx=w[12]-c.x,dy=w[13]-(c.y||1.6),dz=w[14]-c.z; c.yaw=Math.atan2(-dx,-dz); c.pitch=Math.atan2(dy,Math.hypot(dx,dz)); return [c.x,c.z,c.y,w[12],w[13],w[14]]; })()""")
        print('aim',res); await pg.wait_for_timeout(800)
        print('pick',await pg.evaluate("(()=>{ const r=screenRay(550,350); const h=pick(r.o,r.d,{}); return h?[h.kind,h.btn&&JSON.stringify(h.btn),h.point.map(v=>+v.toFixed(2)),h.node&&h.node.mesh&&h.node.mat===MAT.frame]:null; })()"))
        await pg.screenshot(path='out/s26/lift_in.png')
        await pg.mouse.click(550,350); await pg.wait_for_timeout(500)
        print('after click',await pg.evaluate("JSON.stringify([LIFT.st,LIFT.queue,LIFT.lit])"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
