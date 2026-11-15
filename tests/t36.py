import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1000,'height':560}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.evaluate("document.getElementById('demoBtn').click()"); await pg.wait_for_timeout(2000)
        await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ const c=state.cam; c.x=7.5; c.z=8.5; c.yaw=0.9; c.pitch=-0.3; })()"); await pg.wait_for_timeout(2000)
        n0=await pg.evaluate("SHD.n")
        for i in range(8):
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.yaw=0.9+{i}*0.12; c.x=7.5-{i}*0.15; }})()"); await pg.wait_for_timeout(500)
            if i in (0,7): await pg.screenshot(path=f'out/s32/rot{i}.png')
        print('rerenders while walking/rotating:',await pg.evaluate("SHD.n")-n0)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
