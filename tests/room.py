import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800); await pg.screenshot(path='out/s18/r0_edit.png')
        await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        async def cam(x,z,yaw,pitch,n,w=1500):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s18/{n}.png')
        await cam(15.4,2.6,0,-0.05,'r1_closed')
        await pg.mouse.click(550,380); await pg.wait_for_timeout(2200); await pg.screenshot(path='out/s18/r2_open.png')
        print('stand after open', await pg.evaluate("__app.canStand(15,0)"))
        await cam(15.0,-2.8,3.14,-0.05,'r3_fromkitchen')
        # выход наружу
        await cam(9,11.0,0,-0.05,'r4',600)
        await pg.evaluate("(()=>{ const c=__app.state.cam; c.yaw=Math.PI; })()"); await pg.wait_for_timeout(1200); await pg.mouse.click(550,380); await pg.wait_for_timeout(600); await pg.screenshot(path='out/s18/r4_exit.png')
        # ящики
        await pg.evaluate("(()=>{ for(const t of ['workbench','pedestal']){ const it=__app.items.find(i=>i.type===t); (function w(n){ if(n.anim&&n.anim.type==='slideZ') __app.toggleAnim(n); n.children.forEach(w); })(it.root); } })()"); await pg.wait_for_timeout(1500)
        await cam(7.9,1.9,0.35,-0.55,'r5_bench'); await cam(5.6,3.6,0.5,-0.6,'r6_ped')
        # пол
        await pg.click('#mEdit'); await pg.wait_for_timeout(300); await pg.click('#st1'); await pg.wait_for_timeout(300)
        for k in ['laminate','parquet','ceramic','carpet']:
            await pg.click(f'#floors [data-k="{k}"]'); await pg.wait_for_timeout(900)
        await pg.screenshot(path='out/s18/r7_floors.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
