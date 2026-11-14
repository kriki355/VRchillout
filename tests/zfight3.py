import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg=await b.new_page(); await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(1500)
        res=await pg.evaluate("""(()=>{ const out={};
          for(const [k,def] of Object.entries(CATALOG)){ for(let vi=0;vi<1;vi++){ const root=new Node(); zfixBuild(def,def.variants[vi],root); const list=[]; for(const ch of root.children) collect(ch,M4.ident(),null,0,list);
            const groups=new Map(); list.forEach((e,ei)=>{ if(!e.mesh||!e.mesh.g||e.node.noDraw) return; const g=e.mesh.g,P=g.pos,I=g.idx,W=e.w;
              for(let t=0;t<I.length;t+=3){ const v=[0,1,2].map(q=>M4.pt(W,P[I[t+q]*3],P[I[t+q]*3+1],P[I[t+q]*3+2])); const a=[v[1][0]-v[0][0],v[1][1]-v[0][1],v[1][2]-v[0][2]],c=[v[2][0]-v[0][0],v[2][1]-v[0][1],v[2][2]-v[0][2]];
                let n=[a[1]*c[2]-a[2]*c[1],a[2]*c[0]-a[0]*c[2],a[0]*c[1]-a[1]*c[0]]; const l=Math.hypot(...n); if(l<1e-7) continue; n=n.map(x=>x/l); const area=l/2; if(area<2e-5) continue;
                const d=n[0]*v[0][0]+n[1]*v[0][1]+n[2]*v[0][2]; const key=n.map(x=>Math.round(x*50)).join(',')+'|'+Math.round(d*2000);
                const ax=Math.abs(n[0])>Math.abs(n[1])?(Math.abs(n[0])>Math.abs(n[2])?0:2):(Math.abs(n[1])>Math.abs(n[2])?1:2),u=(ax+1)%3,w=(ax+2)%3;
                const bb=[Math.min(v[0][u],v[1][u],v[2][u]),Math.max(v[0][u],v[1][u],v[2][u]),Math.min(v[0][w],v[1][w],v[2][w]),Math.max(v[0][w],v[1][w],v[2][w])];
                if(!groups.has(key)) groups.set(key,[]); groups.get(key).push([ei,bb]); } });
            const hits=new Set(); for(const arr of groups.values()){ if(arr.length<2) continue; for(let i=0;i<arr.length;i++) for(let j=i+1;j<arr.length;j++){ const [ea,A]=arr[i],[eb,B]=arr[j]; if(ea===eb) continue; const ma=list[ea].mat,mb=list[eb].mat; if(ma===mb||(ma.tex===mb.tex&&String(ma.color)===String(mb.color)&&ma.spec===mb.spec)) continue;
                const ox=Math.min(A[1],B[1])-Math.max(A[0],B[0]),oy=Math.min(A[3],B[3])-Math.max(A[2],B[2]); if(ox>0.002&&oy>0.002) hits.add(Math.min(ea,eb)+'-'+Math.max(ea,eb)); } }
            if(hits.size){ const desc=[...hits].slice(0,6).map(h=>{ const [a,b2]=h.split('-').map(Number); const nm=e=>{ const m=list[e].mat; return (m.tex||'')+'#'+(m.color||[]).map(x=>x.toFixed(2)).join(','); }; const pp=e=>[list[e].w[12],list[e].w[13],list[e].w[14]].map(x=>x.toFixed(3)).join(','); return nm(a)+'@'+pp(a)+' | '+nm(b2)+'@'+pp(b2); }); out[k]={n:hits.size,desc}; } } }
          return out; })()""")
        for k,v in res.items(): print(k, v['n'], v['desc'][:6])
        print('items with z-fight:',len(res)); await b.close()
asyncio.run(main())
