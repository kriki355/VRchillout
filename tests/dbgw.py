import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':1400,'height':860}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.click('#demoBtn'); await pg.wait_for_timeout(900)
        await pg.click('#mWalk'); await pg.wait_for_timeout(800)
        r=await pg.evaluate("""(()=>{ const wm=wallMat('wood'),out=[]; const walk=(n,M)=>{ const m=M4.mul(M,n.local?n.local():M4.ident()); }; 
          for(const n of roomRoot.children){ if(n.mat!==wm) continue; out.push({pos:n.pos,mesh:n.mesh&&n.mesh.n}); } return out; })()""")
        for x in r: print(x)
        print('\n'.join(logs) or 'ok'); await b.close()
asyncio.run(main())
