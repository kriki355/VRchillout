import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True); pg=await ctx.new_page(); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(6000)
        await pg.evaluate("document.getElementById('demoBtn').click()"); await pg.wait_for_timeout(1500)
        await pg.evaluate("$('sheetBtn').click()"); await pg.wait_for_timeout(1200); await pg.screenshot(path='out/m/sheet.png')
        await pg.evaluate("$('sheetBtn').click()")
        d0=await pg.evaluate("state.ed.dist")
        await pg.evaluate("""(()=>{ const c=canvas,ev=(t,id,x,y)=>c.dispatchEvent(new PointerEvent(t,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true,isPrimary:id===1}));
          ev('pointerdown',1,150,400); ev('pointerdown',2,240,400); for(let i=1;i<=10;i++){ ev('pointermove',1,150-i*8,400); ev('pointermove',2,240+i*8,400); } ev('pointerup',1,70,400); ev('pointerup',2,320,400); })()""")
        print('pinch dist',d0,'->',await pg.evaluate("state.ed.dist"))
        await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(1000)
        await pg.evaluate('state.cam.x=8;state.cam.z=7;state.cam.yaw=0'); x0=await pg.evaluate('[state.cam.x,state.cam.z,state.cam.yaw]')
        bb=await pg.evaluate("(()=>{ const r=$('joy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]; })()")
        await pg.evaluate(f"""(()=>{{ const j=$('joy'),ev=(t,x,y)=>j.dispatchEvent(new PointerEvent(t,{{pointerId:7,pointerType:'touch',clientX:x,clientY:y,bubbles:true}})); ev('pointerdown',{bb[0]},{bb[1]}); ev('pointermove',{bb[0]},{bb[1]-60}); window._ev=ev; }})()""")
        f0=await pg.evaluate('FRAME'); await pg.wait_for_timeout(1200); print('frames',await pg.evaluate('FRAME')-f0); await pg.evaluate(f"window._ev('pointerup',{bb[0]},{bb[1]})")
        print('joy move',x0,'->',await pg.evaluate("[state.cam.x,state.cam.z]"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
