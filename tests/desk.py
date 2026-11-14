import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.click('#clearBtn'); await pg.wait_for_timeout(600)
        print(await pg.evaluate("""(()=>{ const d=addItem({type:'standdesk',variant:0,x:4,z:3,rot:0,y:0}); const e=addItem({type:'extinguisher',variant:0,x:4.2,z:3,rot:0,y:0.72}); const m=addItem({type:'microwave',variant:0,x:3.7,z:3,rot:0,y:0.72});
          (function w(n){ if(n.anim&&n.anim.type==='slideY') n.anim.target=1; n.children.forEach(w); })(d.root); window._t=[e,m]; return [e.y,m.y]; })()"""))
        await pg.wait_for_timeout(3500)
        print("after up",await pg.evaluate("[...window._t.map(i=>+i.y.toFixed(3)),+(items.find(i=>i.type==='standdesk').root.liftNode.anim.amount*ease(items.find(i=>i.type==='standdesk').root.liftNode.anim.t)).toFixed(3)]"))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
