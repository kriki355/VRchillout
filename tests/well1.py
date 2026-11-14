import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if m.type=='error' else None)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(1200)
        print(await pg.evaluate("JSON.stringify([PRJ.storeys.map(S=>[S.wings.map(g=>[g.side,g.offset,g.w,g.d,!!g.stair]),S.stairs]),PRJ.lift])"))
        print(await pg.evaluate("JSON.stringify(PRJ.storeys.map(S=>(S.openings||[]).filter(o=>o.kind==='arch')))"))
        await pg.screenshot(path='out/s26/w1_demo.png')
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(500); await pg.screenshot(path='out/s26/w2_build.png')
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        async def cam(x,z,yaw,pitch,n,w=1500):
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; }})()"); await pg.wait_for_timeout(w); await pg.screenshot(path=f'out/s26/{n}.png')
        print('can',await pg.evaluate("[canStand(19.2,1.0),canStand(18.5,2.4),canStand(17.5,2.4)]"))
        # подойти к проёму и посмотреть в клетку
        await cam(15.5,2.5,-1.57,-0.05,'w3_arch')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
