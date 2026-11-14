import sys, asyncio, json
from playwright.async_api import async_playwright
URL=sys.argv[1]; OUT=sys.argv[2]; VIEWS=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
DEF=[["a_hall",9,11.4,0,-0.12],["b_corner",16.5,10.8,0.75,-0.1],["c_kitchen",14.5,1.2,-2.6,-0.25],["d_office",6.5,8.5,-2.3,-0.18],["e_combi",13.0,0.2,-1.2,-0.32]]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':760}); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if ('GPU stall' not in m.text and 'ERR_TUNNEL' not in m.text) else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(4000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(600)
        await pg.click('#mWalk'); await pg.wait_for_timeout(500)
        for n,x,z,yaw,pitch in (VIEWS or DEF):
            await pg.evaluate(f"(()=>{{ const c=__app.state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pitch}; __app.state.glide=null; }})()")
            await pg.wait_for_timeout(1300); await pg.screenshot(path=f'{OUT}/{n}.png')
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
