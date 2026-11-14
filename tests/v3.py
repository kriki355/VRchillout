import sys, asyncio
from playwright.async_api import async_playwright
URL='file://'+sys.argv[1]; OUT=sys.argv[2]
PROJ="""(p)=>{ const vp=__app.state.lastVP; const c=[vp[0]*p[0]+vp[4]*p[1]+vp[8]*p[2]+vp[12],vp[1]*p[0]+vp[5]*p[1]+vp[9]*p[2]+vp[13],vp[3]*p[0]+vp[7]*p[1]+vp[11]*p[2]+vp[15]]; const r=document.getElementById('gl').getBoundingClientRect(); return [(c[0]/c[2]*0.5+0.5)*r.width,(0.5-c[1]/c[2]*0.5)*r.height]; }"""
FIND="(t)=>__app.items.find(i=>i.type===t)"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1440,'height':860}); logs=[]
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if 'GPU stall' not in m.text else None); pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto(URL); await pg.wait_for_timeout(2000)
        await pg.screenshot(path=f'{OUT}/c1_cut.png')
        await pg.click('[data-wm="full"]'); await pg.wait_for_timeout(600); await pg.screenshot(path=f'{OUT}/c2_full.png')
        await pg.click('[data-wm="cut"]'); await pg.wait_for_timeout(500)
        # тянем метку высоты
        hh=await pg.evaluate("(()=>{const n=__app.state; return null})()")
        pos=await pg.evaluate("(()=>{ const L=__app.L; return [0,0,0]; })()")
        h=await pg.evaluate("""(()=>{ const hs=[]; return 1; })()""")
        hp=await pg.evaluate("""(()=>{ let r=null; const walk=n=>{ if(n.handle&&n.handle.k==='height') r=[n.handle.x,n.handle.y,n.handle.z]; n.children.forEach(walk); }; return r; })()""")
        # высота: через drag метки (позицию берём из state через pick-список)
        hp=await pg.evaluate("""(()=>{ const e=__app.state.lastVP; const L=__app.L; let best=null,bd=-1; const cw=null; return null; })()""")
        print('wallH before', await pg.evaluate("__app.L.wallH"))
        await pg.click('#toStep2'); await pg.wait_for_timeout(300)
        await pg.click('#chips [data-f="catering"]'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/c3_catalog.png')
        # пересечение: ставим стол поверх другого
        await pg.click('#demoBtn'); await pg.wait_for_timeout(800)
        await pg.screenshot(path=f'{OUT}/c4_demo_cut.png')
        await pg.evaluate("__app.startPlace('desk')")
        d=await pg.evaluate(f"(({FIND})('desk'))&&[({FIND})('desk').x,0,({FIND})('desk').z]")
        sx,sy=await pg.evaluate(f"({PROJ})({d})"); await pg.mouse.move(sx-2,sy); await pg.wait_for_timeout(100); await pg.mouse.move(sx,sy); await pg.wait_for_timeout(200)
        print('invalid while overlapping:', await pg.evaluate("__app.state.invalid"))
        await pg.screenshot(path=f'{OUT}/c5_invalid.png')
        await pg.keyboard.press('Escape')
        # отмена
        n0=await pg.evaluate("__app.items.length"); await pg.evaluate("(()=>{ __app.state.selected=__app.items.find(i=>i.type==='desk'); __app.delSel(); })()"); n1=await pg.evaluate("__app.items.length")
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(200); n2=await pg.evaluate("__app.items.length")
        print('undo:',n0,n1,n2)
        await pg.click('#specBtn'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'{OUT}/c6_spec.png'); await pg.click('#spClose')
        # прогулка: общепит
        await pg.evaluate("__app.goZone('catering')"); await pg.wait_for_timeout(600)
        await pg.screenshot(path=f'{OUT}/d1_catering.png')
        await pg.evaluate("""(()=>{ const s=__app.state; const it=__app.items.find(i=>i.type==='fruitcase'); s.cam.x=it.x-2.6; s.cam.z=it.z; s.cam.yaw=-Math.PI/2; s.cam.pitch=-0.05; })()"""); await pg.wait_for_timeout(400)
        await pg.screenshot(path=f'{OUT}/d2_fruit.png')
        await pg.evaluate("""(()=>{ const it=__app.items.find(i=>i.type==='fruitcase'); (function w(n){ if(n.anim) __app.toggleAnim(n); n.children.forEach(w); })(it.root); })()"""); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/d3_fruit_blind.png')
        # кухня: кран, конфорки
        await pg.evaluate("""(()=>{ const s=__app.state; s.cam.x=15.0; s.cam.z=-1.6; s.cam.yaw=0.25; s.cam.pitch=-0.3; for(const t of ['sink','stove','coffee']){ const it=__app.items.find(i=>i.type===t); (function w(n){ if(n.anim&&['Кран','Конфорки','Кофе'].includes(n.anim.label)) __app.toggleAnim(n); n.children.forEach(w); })(it.root); } })()"""); await pg.wait_for_timeout(1000)
        await pg.screenshot(path=f'{OUT}/d4_kitchen.png')
        # взять кружку и бросить
        await pg.evaluate("__app.goZone('office')"); await pg.wait_for_timeout(500)
        mug0=await pg.evaluate("(()=>{const m=__app.items.find(i=>i.type==='mug'); return [m.x,m.y,m.z];})()")
        await pg.evaluate("__app.takeItem(__app.items.find(i=>i.type==='mug'))"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/d5_held.png')
        await pg.evaluate("__app.releaseHeld(true)"); await pg.wait_for_timeout(250)
        await pg.screenshot(path=f'{OUT}/d6_thrown.png')
        await pg.wait_for_timeout(2500)
        print('mug from',mug0,'to',await pg.evaluate("(()=>{const m=__app.items.find(i=>i.type==='mug'); return [+m.x.toFixed(2),+m.y.toFixed(3),+m.z.toFixed(2)];})()"),'in physics:',await pg.evaluate("__app.physSet.size"))
        # переставить стол вместе с ноутбуком
        lap0=await pg.evaluate("(()=>{const m=__app.items.find(i=>i.type==='laptop'); return [m.x,m.y,m.z];})()")
        await pg.evaluate("__app.startMove(__app.items.find(i=>i.type==='desk'))")
        dk=await pg.evaluate(f"[({FIND})('desk').x+0.8,0,({FIND})('desk').z+0.6]")
        mx,my=await pg.evaluate(f"({PROJ})({dk})"); await pg.mouse.move(mx-3,my); await pg.mouse.move(mx,my); await pg.wait_for_timeout(200)
        print('move invalid:',await pg.evaluate("__app.state.invalid"))
        await pg.screenshot(path=f'{OUT}/d7_moving.png')
        await pg.mouse.click(mx,my); await pg.wait_for_timeout(200)
        print('laptop from',lap0,'to',await pg.evaluate("(()=>{const m=__app.items.find(i=>i.type==='laptop'); return [+m.x.toFixed(2),+m.y.toFixed(3),+m.z.toFixed(2)];})()"),'move state', await pg.evaluate("!!__app.state.move"))
        await pg.evaluate("__app.sitOn(__app.items.find(i=>i.type==='sofa'))"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/d8_sit.png')
        await pg.keyboard.down('KeyW'); await pg.wait_for_timeout(200); await pg.keyboard.up('KeyW')
        print('after stand: y',await pg.evaluate("__app.state.cam.y"),'sit',await pg.evaluate("!!__app.state.sit"))
        await pg.evaluate("__app.startInspect(__app.items.find(i=>i.type==='fruitcase'))"); await pg.wait_for_timeout(900)
        await pg.screenshot(path=f'{OUT}/d9_inspect_fruit.png')
        print('\n'.join(logs) or 'no console output')
        await b.close()
asyncio.run(main())
