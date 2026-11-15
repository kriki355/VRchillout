import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':800,'height':500}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        print(await pg.evaluate("""(()=>{ for(const it of [...items]) if(!isCeil(it)) items.splice(items.indexOf(it),1); const it=addItem({type:'gamedesk',variant:0,x:3,z:3,rot:0,y:0}); gatherScene();
          const m=GDESK.top; const out={mn:m.mn,mx:m.mx,hits:[]}; for(const [dx,dz] of [[0,0],[0,0.3],[0,0.38],[0.4,0.3],[-0.5,-0.3],[0.5,0.32]]){ const h=pick([3+dx,2.5,3+dz],[0,-1,0]); out.hits.push([dx,dz,h?h.kind:null,h?+h.point[1].toFixed(3):null,h?!!h.top:null,h&&h.node?(h.node.mesh===GDESK.top?"TOP":h.node.mesh===GDESK.frame?"FRAME":(h.node.anim?"anim":"other")+JSON.stringify(h.node.mesh.mx)):null]); } return JSON.stringify(out); })()"""))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
