import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1100,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}')); pg.on('console',lambda m: logs.append('C:'+m.text) if m.type=='error' else None)
        await pg.goto(sys.argv[1]); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800)
        # отделка: отсек — плитка кабанчик + кафель, зал — кирпич
        await pg.click('#st1'); await pg.wait_for_timeout(300)
        await pg.click('#roomPick [data-id="2"]'); await pg.click('#walls [data-k="subway"]'); await pg.click('#floors [data-k="ceramic"]'); await pg.wait_for_timeout(300)
        await pg.click('#roomPick [data-id="1"]'); await pg.click('#walls [data-k="brick"]'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='out/s18/x0_panel.png')
        # перетаскивание карточки в зал
        await pg.click('#st2'); await pg.wait_for_timeout(400)
        card=await pg.query_selector('.cardI[data-t="loftpouf"]'); await card.scroll_into_view_if_needed(); bb=await card.bounding_box()
        n0=await pg.evaluate("__app.items.length")
        await pg.mouse.move(bb['x']+20,bb['y']+20); await pg.mouse.down(); await pg.mouse.move(600,400,steps=8); await pg.mouse.move(640,420,steps=4); await pg.mouse.up(); await pg.wait_for_timeout(400)
        print('drag placed', (await pg.evaluate("__app.items.length"))-n0, await pg.evaluate("!!__app.state.place"))
        await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        async def cam(x,z,yaw,pitch,n,w=1800):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s18/{n}.png')
        await cam(15.0,1.6,-1.57,-0.1,'x1_oven')
        await pg.evaluate("(()=>{ const it=__app.items.find(i=>i.type==='pechka'); (function w(n){ if(n.anim) __app.toggleAnim(n); n.children.forEach(w); })(it.root); const r=__app.items.find(i=>i.type==='shelving'); (function w(n){ if(n.anim) __app.toggleAnim(n); n.children.forEach(w); })(r.root); })()")
        await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s18/x2_oven_on.png')
        await cam(10.9,2.0,0,-0.2,'x3_rack')
        await cam(15.0,-2.2,0.6,-0.1,'x4_kitchen')
        await cam(9,9,0,-0.05,'x5_hall')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
