import sys, asyncio, json
from playwright.async_api import async_playwright
URL='file://'+sys.argv[1]
FAKE = r"""
(() => {
  window.__socks=[];
  class FakeWS { constructor(url,proto){ this.url=url; this.readyState=0; this.binaryType='blob'; window.__socks.push(this); this.id=window.__socks.length; setTimeout(()=>{ this.readyState=1; this.onopen&&this.onopen(); },50); }
    send(b){ window.__ws_send(Array.from(new Uint8Array(b))); }
    close(){ this.readyState=3; } }
  window.WebSocket=FakeWS;
  window.__ws_recv=(arr)=>{ const s=window.__socks[window.__socks.length-1]; if(s&&s.onmessage) s.onmessage({data:new Uint8Array(arr).buffer}); };
})();
"""
class Broker:
    def __init__(s): s.subs={}; s.retained={}; s.pubs=[]; s.pages={}
    def rl(s,n):
        o=[]
        while True:
            d=n%128; n//=128
            if n>0: d|=128
            o.append(d)
            if n==0: return o
    async def handle(s,name,data):
        b=bytes(data); i=0
        while i<len(b):
            h=b[i]; t=h>>4; mul=1; ln=0; j=i+1
            while True:
                d=b[j]; j+=1; ln+=(d&127)*mul; mul*=128
                if not d&128: break
            body=b[j:j+ln]; i=j+ln
            if t==1:
                pl=(body[0]<<8)|body[1]; assert body[2:2+pl]==b'MQTT' and body[2+pl]==4, 'bad connect'
                await s.send(name,[0x20,2,0,0])
            elif t==8:
                assert h&0xF==2
                tl=(body[2]<<8)|body[3]; topic=body[4:4+tl].decode(); s.subs.setdefault(topic,set()).add(name)
                await s.send(name,[0x90,3,body[0],body[1],0])
                if topic in s.retained:
                    await s.deliver(name,topic,s.retained[topic])
            elif t==3:
                tl=(body[0]<<8)|body[1]; topic=body[2:2+tl].decode(); payload=body[2+tl:]
                if h&1: s.retained[topic]=payload
                s.pubs.append((name,topic,len(payload)))
                for n in s.subs.get(topic,()):
                    await s.deliver(n,topic,payload)
            elif t==12:
                await s.send(name,[0xD0,0])
    async def deliver(s,name,topic,payload):
        tb=topic.encode(); body=[len(tb)>>8,len(tb)&255]+list(tb)+list(payload)
        await s.send(name,[0x30]+s.rl(len(body))+body)
    async def send(s,name,arr):
        await s.pages[name].evaluate("a=>__ws_recv(a)",arr)
async def main():
    br=Broker()
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        ctxA=await b.new_context(viewport={'width':1300,'height':800}); ctxB=await b.new_context(viewport={'width':1000,'height':700},user_agent='Mozilla/5.0 (X11; Linux x86_64; Quest 2) OculusBrowser/40.0 Chrome/136.0 VR Safari/537.36')
        A=await ctxA.new_page(); B=await ctxB.new_page(); br.pages={'A':A,'B':B}; logs=[]
        for n,pg in (('A',A),('B',B)):
            pg.on('pageerror',lambda e,n=n: logs.append(f'{n} PAGEERROR: {e}'))
            await pg.add_init_script(FAKE)
            await pg.expose_function('__ws_send',lambda arr,n=n: asyncio.ensure_future(br.handle(n,arr)))
        await A.goto(URL); await A.wait_for_timeout(1200)
        await A.click('#syncBtn'); await A.wait_for_timeout(500)
        code=await A.evaluate("SYNC.code"); print('code', code, 'panel', (await A.inner_text('#syncP'))[:80].replace('\n',' | '))
        await A.wait_for_timeout(4000)
        await A.evaluate("__app.addItem? 0:0")
        await A.evaluate("(()=>{ addItem({type:'desk',x:3,z:3}); addItem({type:'globe',x:3,y:0.75,z:3}); rebuildDecor(); })()"); await A.wait_for_timeout(1600)
        print('A btn', await A.inner_text('#syncBtn'), 'pubs', br.pubs)
        await B.goto(URL); await B.wait_for_timeout(1200); await B.evaluate('showVRStart(false)')
        await B.fill('#roomIn',code); await B.click('#roomGo'); await B.wait_for_timeout(2500)
        print('B status', await B.inner_text('#roomSt'))
        print('B items', await B.evaluate("JSON.stringify(__app.items.map(i=>i.type))"))
        await B.evaluate("(()=>{ const d=__app.items.find(i=>i.type==='desk'); d.x=5.5; syncRoot(d); })()"); await B.wait_for_timeout(2000)
        print('A desk x', await A.evaluate("__app.items.find(i=>i.type==='desk').x"))
        await A.wait_for_timeout(3000)
        print('total publishes', len(br.pubs), [x[0] for x in br.pubs])
        print('\n'.join(logs) or 'no page errors')
        await b.close()
asyncio.run(main())
