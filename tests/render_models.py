import sys, asyncio, base64, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(viewport={'width':800,'height':600}); await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        res=await pg.evaluate("""(()=>{ const S=1200,T=ensureTarget('big',S,S,true),px=new Uint8Array(S*S*4),cv=mkCanvas(S,S),cx=cv.getContext('2d'),img=cx.createImageData(S,S),out=[];
          for(const [k,def] of Object.entries(CATALOG)){ const root=new Node(); def.build(root,def.variants[0]); (function w(n){ if(n.anim&&['Ночная шторка','Кран','Кофе','Конфорки'].includes(n.anim.label)) {} n.children.forEach(w); })(root);
            const bb=bboxOf(root),c=[(bb.mn[0]+bb.mx[0])/2,(bb.mn[1]+bb.mx[1])/2,(bb.mn[2]+bb.mx[2])/2],r=0.5*Math.hypot(bb.mx[0]-bb.mn[0],bb.mx[1]-bb.mn[1],bb.mx[2]-bb.mn[2]);
            const flat=(bb.mx[1]-bb.mn[1])<0.3*Math.max(bb.mx[0]-bb.mn[0],bb.mx[2]-bb.mn[2]);
            const rootM=M4.mul(M4.mul(M4.rotX(flat?0.7:0.32),M4.rotY(-0.62)),M4.trans(-c[0],-c[1],-c[2])),dist=r/Math.sin(15*DEG)*1.08; const list=[]; for(const ch of root.children) collect(ch,rootM,null,0,list);
            gl.bindFramebuffer(gl.FRAMEBUFFER,T.fb); gl.viewport(0,0,S,S); gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
            renderScene(M4.trans(0,0,-dist),M4.persp(30*DEG,1,dist*0.03,dist*4),[0,0,dist],list,{shadows:false,ao:0,light:LIGHT_I,exp:0.86});
            gl.readPixels(0,0,S,S,gl.RGBA,gl.UNSIGNED_BYTE,px); for(let y=0;y<S;y++) img.data.set(px.subarray((S-1-y)*S*4,(S-y)*S*4),y*S*4); cx.putImageData(img,0,0);
            const sz=[bb.mx[0]-bb.mn[0],bb.mx[2]-bb.mn[2],bb.mx[1]-bb.mn[1]].map(v=>Math.round(v*1000));
            out.push({k,name:def.name,cat:def.cat,small:!!def.small,size:sz,variants:def.variants.map(v=>v.name),png:cv.toDataURL('image/png')}); }
          gl.bindFramebuffer(gl.FRAMEBUFFER,null); return out; })()""")
        meta=[]
        for i,r in enumerate(res):
            fn=f"{i+1:02d}_{r['k']}.png"; open(f"{sys.argv[2]}/{fn}",'wb').write(base64.b64decode(r['png'].split(',')[1])); r.pop('png'); r['file']=fn; meta.append(r)
        json.dump(meta,open(sys.argv[2]+'/../models.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print(len(meta),'models'); await b.close()
asyncio.run(main())
