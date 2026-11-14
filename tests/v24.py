import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900); await pg.screenshot(path='out/s18/y0_edit.png')
        await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        async def cam(x,z,yaw,pitch,n,w=1800):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s18/{n}.png')
        await cam(9,11.2,0,-0.15,'y1_hall')
        await cam(3.9,5.0,0,-0.45,'y2_desk')
        await cam(14.6,9.6,0,-0.35,'y3_long')
        await cam(15,0.9,0,-0.25,'y4_wing')
        # клик по креслу — должна открыться карточка
        await cam(3.4,7.8,0,-0.5,'y5_chair',1200)
        h=await pg.evaluate("(()=>{ const r=screenRay(550,420); const h=pick(r.o,r.d); return h?[h.kind,h.item&&h.item.type,!!h.inter]:null; })()"); print('pick chair',h)
        # сесть и повернуть голову
        await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='loftchair'); sitOn(it); state.cam.yaw+=0.9; })()"); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ standUp(); })()"); await pg.wait_for_timeout(300)
        await cam(3.9,4.6,0,-0.5,'y6_swivel',1200)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
