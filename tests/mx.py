import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':600}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.evaluate("PERF.dyn=false"); await pg.evaluate("document.getElementById('mWalk').click()"); await pg.wait_for_timeout(500)
        await pg.evaluate("""(()=>{ for(const it of [...items]) if(!isCeil(it)) items.splice(items.indexOf(it),1); const it=addItem({type:'mixer2',variant:0,x:4,z:3,rot:0,y:0}); const c=state.cam; c.x=4; c.z=4.3; c.y=1.9; c.yaw=0; c.pitch=-0.75; state.sit={}; state.sit=null; })()""")
        await pg.wait_for_timeout(2000); await pg.screenshot(path='out/nm/mx_top.png')
        # click lever via ray test
        print(await pg.evaluate("""(()=>{ const it=items[items.length-1]; gatherScene(); const W=itemWorld(it),c=M4.pt(W,0.37,1.1,-0.2),o=[c[0]+1.2,c[1]+0.3,c[2]+0.2],d=norm3([c[0]-o[0],c[1]-o[1],c[2]-o[2]]),h=pick(o,d); return h?(h.node&&h.node.tapHit?'LEVER':h.kind):'none'; })()"""))
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
