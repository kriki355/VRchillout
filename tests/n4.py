import sys, asyncio, json
from playwright.async_api import async_playwright
K=[('microwave',1.0,1),('gamechair',2.4,0),('garderob',3.6,1),('minifridge',2.2,1),('cakecase',3.0,1),('oven4',3.6,1),('telega',2.4,1),('mobboard',3.4,0),('flower',1.6,0),('wardrobe2',4.0,1)]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':700}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(5000)
        await pg.click('#mWalk'); await pg.wait_for_timeout(600)
        for k,dist,op in K:
            await pg.evaluate("(()=>{ for(const it of [...items]) removeItem?removeItem(it):0; })()") if False else None
            await pg.evaluate(f"""(()=>{{ for(const it of [...items]) if(!isCeil(it)){{ const i=items.indexOf(it); items.splice(i,1); }} const it=addItem({{type:'{k}',variant:0,x:4,z:3,rot:0,y:{'0.75' if k=='microwave' else '0'}}}); window._it=it;
              if({op}) (function w(n){{ if(n.anim&&n.anim.type!=='glow'&&n.anim.type!=='spin') n.anim.target=1; if(n.anim&&(n.anim.type==='glow')) n.anim.target=1; n.children.forEach(w); }})(it.root);
              const c=state.cam,h=it.size.h; c.x=4+{dist}*0.55; c.z=3+{dist}*0.85; c.y=Math.max(1.0,h*0.8+0.3); c.yaw=Math.atan2({dist}*0.55,{dist}*0.85); c.pitch=-Math.atan2(c.y-h*0.5,{dist}); }})()""")
            if k=='mobboard':
                await pg.wait_for_timeout(800)
                await pg.evaluate("""(()=>{ const it=window._it; wbTool(it,'red'); const q=it.root.wb.q,W=it.root.wb.W,H=it.root.wb.H; it.root.wb.last=null; for(let i=0;i<=40;i++){ const u=-0.35+i*0.0175,v=0.15*Math.sin(i/5); const w=M4.mul(itemWorld(it),q.local()); wbDraw(it,M4.pt(w,u*W,v*H,0),'t'); } wbTool(it,'blue'); it.root.wb.last=null; for(let i=0;i<=30;i++){ const w=M4.mul(itemWorld(it),q.local()); wbDraw(it,M4.pt(w,(-0.2+i*0.013)*W,(-0.25+0.0*i)*H,0),'t2'); } })()""")
            await pg.wait_for_timeout(2600)
            await pg.screenshot(path=f'out/s26/v_{k}.png')
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
