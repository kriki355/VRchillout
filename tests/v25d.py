import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1280,'height':800}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4000)
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(300)
        await pg.click('#addStorey'); await pg.wait_for_timeout(1500)
        print('after add',await pg.evaluate("[PRJ.storeys.length,ACT,JSON.stringify(PRJ.storeys[0].stairs),JSON.stringify(PRJ.lift),PRJ.storeys[1].openings.length]"))
        await pg.screenshot(path='out/s25/h1_added.png')
        await pg.click('#lvBar button[data-k="0"]'); await pg.wait_for_timeout(900); await pg.screenshot(path='out/s25/h2_lv1.png')
        # выбрать лестницу кликом
        pt=await pg.evaluate("(()=>{ const st=PRJ.storeys[0].stairs[0]; const vp=state.lastVP,p=[st.x,0.8,st.z],c=[vp[0]*p[0]+vp[4]*p[1]+vp[8]*p[2]+vp[12],vp[1]*p[0]+vp[5]*p[1]+vp[9]*p[2]+vp[13],vp[3]*p[0]+vp[7]*p[1]+vp[11]*p[2]+vp[15]]; const r=canvas.getBoundingClientRect(); return [(c[0]/c[2]*0.5+0.5)*r.width,(0.5-c[1]/c[2]*0.5)*r.height]; })()")
        await pg.mouse.move(pt[0],pt[1]); await pg.mouse.down(); await pg.mouse.move(pt[0]+40,pt[1]+70,steps=6); await pg.mouse.up(); await pg.wait_for_timeout(700)
        print('drag',await pg.evaluate("[JSON.stringify(PRJ.storeys[0].stairs[0]),state.selStruct&&state.selStruct.kind,state.invalid,hist.undo.length]"))
        await pg.screenshot(path='out/s25/h3_dragged.png')
        await pg.keyboard.press('KeyR'); await pg.wait_for_timeout(600); print('rot',await pg.evaluate("JSON.stringify(PRJ.storeys[0].stairs[0])"))
        await pg.screenshot(path='out/s25/h4_rot.png')
        print('toast',await pg.evaluate("document.getElementById('toast').textContent"))
        # высота отсека и потолок
        await pg.click('#etabs button[data-tab=plan]'); await pg.wait_for_timeout(300)
        await pg.click('.addw button[data-w=E]'); await pg.wait_for_timeout(600)
        await pg.click('.wing .hm'); await pg.click('.wing .hm'); await pg.click('.wing .hm'); await pg.wait_for_timeout(500)
        print('wing h',await pg.evaluate("[L.wings[0].h,roomH(2),topH(L)]"))
        await pg.screenshot(path='out/s25/h5_wing.png')
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ const c=state.cam; c.x=6.5; c.z=3; c.yaw=-Math.PI/2; c.pitch=0.25; })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s25/h6_wing_walk.png')
        await pg.click('#mEdit'); await pg.wait_for_timeout(500)
        await pg.click('#etabs button[data-tab=build]'); await pg.wait_for_timeout(300)
        await pg.click('#lvBar button[data-k="1"]'); await pg.wait_for_timeout(500)
        await pg.click('.storeyRow .del'); await pg.wait_for_timeout(300); await pg.click('.storeyRow .del'); await pg.wait_for_timeout(700)
        print('removed',await pg.evaluate("[PRJ.storeys.length,ACT,PRJ.lift,JSON.stringify(PRJ.storeys[0].stairs)]"))
        await pg.screenshot(path='out/s25/h7_removed.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
