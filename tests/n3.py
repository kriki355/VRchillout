import sys, asyncio, json
from playwright.async_api import async_playwright
K=['microwave','minifridge','chestfreezer','sinktable','drawers','cakecase','wardrobe1','wardrobe2','deckoven','workbench','mobboard','chester','flower','gamechair','garderob','prodtable']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.click('#clearBtn'); await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ L.hall.W=16; L.hall.D=12; roomChanged(); })()"); await pg.wait_for_timeout(500)
        r=await pg.evaluate("""(()=>{ const K=%s; const out=[]; let i=0; for(const k of K){ const x=2+(i%%5)*3.1, z=2.2+Math.floor(i/5)*3.2; const o={type:k,variant:0,x,z,rot:0,y:0}; if(CATALOG[k].small){ o.x=2+(i%%5)*3.1; } const it=addItem(o); out.push([k,it.size.w.toFixed(2),it.size.d.toFixed(2),it.size.h.toFixed(2)]); i++; } return out; })()""" % json.dumps(K))
        for x in r: print(x)
        await pg.wait_for_timeout(800)
        await pg.evaluate("(()=>{ const e=state.ed; e.tx=8; e.tz=6; e.dist=19; })()"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='out/s26/n3_all.png')
        # открыть все подвижные части
        await pg.evaluate("(()=>{ for(const it of items){ (function w(n){ if(n.anim){ n.anim.target=1; } n.children.forEach(w); })(it.root); } })()"); await pg.wait_for_timeout(2500)
        await pg.screenshot(path='out/s26/n3_open.png')
        await pg.click('#etabs button[data-tab=furn]'); await pg.wait_for_timeout(600)
        await pg.click('#chips button[data-f=kitchen]'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='out/s26/n3_cat.png',clip={'x':0,'y':60,'width':370,'height':720})
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
