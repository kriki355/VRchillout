import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':900,'height':1200}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file:///home/claude/tests/out/s25/kp.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("(()=>{ const c=document.querySelectorAll('[data-p]'); c[0].textContent='48500'; c[1].textContent='21900'; c[0].dispatchEvent(new Event('input')); })()")
        await pg.screenshot(path='out/s25/kp_full.png',full_page=True)
        h=await pg.evaluate("document.body.scrollHeight"); print('h',h,errs)
        await b.close()
asyncio.run(main())
