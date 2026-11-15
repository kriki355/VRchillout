import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':600}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(500)
        print(await pg.evaluate("""(()=>{ for(const it of [...items]) if(!isCeil(it)) items.splice(items.indexOf(it),1); const it=addItem({type:'sinktable',variant:0,x:4,z:3,rot:0,y:0}); gatherScene();
          let hit=null; (function w(n){ if(n.tapHit) hit=n; n.children.forEach(w); })(it.root); const W=itemWorld(it),c=M4.pt(W,hit.pos[0],hit.pos[1],hit.pos[2]); const out=[];
          for(const [dx,dy] of [[0,0],[0.07,0.0],[-0.07,0.03],[0.05,0.08],[0,-0.05]]){ const o=[c[0]+dx,c[1]+dy+0.4,c[2]+1.0],d=norm3([c[0]+dx-o[0],c[1]+dy-o[1],c[2]-o[2]]); const h=pick(o,d); out.push(h&&h.node===hit?'TAP':(h?h.kind:'none')); } return out.join(','); })()"""))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
