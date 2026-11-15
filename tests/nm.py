import asyncio,sys
from playwright.async_api import async_playwright
T=sys.argv[1].split(',')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg=await b.new_page(viewport={'width':900,'height':640}); logs=[]
        pg.on('pageerror',lambda e: logs.append(f'PAGEERROR: {e}'))
        pg.on('console',lambda m: logs.append(f'{m.type}: {m.text}') if m.type=='error' else None)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(4500)
        await pg.evaluate("PERF.dyn=false; PERF.scale=1")
        for t in T:
            name,_,mode=t.partition(':')
            await pg.evaluate("""([t,mode])=>{ const it=items.find(i=>i.type===t)||null; if(it) startInspect(it); }""",[name,mode])
            await pg.evaluate("""([t,mode])=>{ if(state.inspect) finishInspect(); for(const it of [...items]) if(!isCeil(it)) items.splice(items.indexOf(it),1); const it=addItem({type:t,variant:0,x:4,z:3,rot:0,y:0}); startInspect(it);
              if(mode==='open'){ (function w(n){ if(n.anim) n.anim.target=1; n.children.forEach(w); })(it.root); } }""",[name,mode])
            await pg.wait_for_timeout(3000); await pg.screenshot(path=f'out/nm/{name}{"_"+mode if mode else ""}.png')
        print('\n'.join(logs[:12]) or 'ok'); await b.close()
asyncio.run(main())
