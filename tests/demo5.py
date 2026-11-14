import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(1500)
        print(await pg.evaluate("JSON.stringify([items.length,PRJ.storeys.map(S=>S.wings.map(g=>[g.side,g.offset,!!g.stair])),PRJ.lift])"))
        print('bad',await pg.evaluate("JSON.stringify(items.filter(it=>!isCeil(it)).map(it=>[it.type,placeIssue(it)]).filter(x=>x[1]))"))
        print('small y',await pg.evaluate("JSON.stringify(items.filter(it=>CATALOG[it.type].small).map(it=>[it.type,+(it.y||0).toFixed(2)]))"))
        await pg.evaluate("(()=>{ const e=state.ed; e.tx=11; e.tz=6; e.dist=26; })()"); await pg.wait_for_timeout(1500); await pg.screenshot(path='out/s26/d5_f1.png')
        # удаление этажа через окно
        await pg.evaluate('removeStorey(0)'); await pg.wait_for_timeout(500); await pg.screenshot(path='out/s26/d5_confirm.png')
        print('dlg',await pg.evaluate("(()=>{const d=document.getElementById('cfmDlg'); return d?[d.className,getComputedStyle(d).display,d.innerHTML.length]:null})()")); await pg.screenshot(path='out/s26/d5_confirm.png'); await pg.evaluate("document.querySelector('#cfmDlg .yes').click()"); await pg.wait_for_timeout(800)
        print('after del',await pg.evaluate("JSON.stringify([PRJ.storeys.length,ACT,items.length,L.hall.floor])"))
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(800)
        print('undo',await pg.evaluate("JSON.stringify([PRJ.storeys.length,items.length])"))
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        for n,(x,z,yaw,pit) in {'w_bakery':(17.2,5.2,0.0,-0.12),'w_cafe':(11.0,10.8,3.14,-0.2),'w_office':(5.0,4.6,0.7,-0.25)}.items():
            await pg.evaluate(f"(()=>{{ const c=state.cam; c.x={x}; c.z={z}; c.yaw={yaw}; c.pitch={pit}; }})()"); await pg.wait_for_timeout(1500); await pg.screenshot(path=f'out/s26/{n}.png')
        # мойка: рычаг
        print('sink',await pg.evaluate("(()=>{ const it=items.find(i=>i.type==='sinktable'); let lv=null; (function w(n){ if(n.anim&&/Рычаг/.test(n.anim.label)) lv=n; n.children.forEach(w); })(it.root); if(!lv) return 'no lever'; toggleAnim(lv); return lv.anim.link.length; })()"))
        await pg.evaluate("(()=>{ const c=state.cam; c.x=13.95; c.z=12.3; c.yaw=0; c.pitch=-0.5; })()"); await pg.wait_for_timeout(1800); await pg.screenshot(path='out/s26/w_sink.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
