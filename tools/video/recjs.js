window.__rec=(()=>{ const R={aim:null,look:null,hy:0,hp:-0.08,lhUp:0};
  const findItem=(type,i=0)=>items.filter(it=>it.type===type)[i];
  const nodeBy=(it,f)=>{ let r=null; (function w(n){ if(!r&&f(n)) r=n; n.children.forEach(w); })(it.root); return r; };
  const center=n=>{ let m=null; (function w(q){ if(!m&&q.mesh&&q.world&&!q.noDraw) m=q; q.children.forEach(w); })(n); if(!m) (function w(q){ if(!m&&q.mesh&&q.world) m=q; q.children.forEach(w); })(n); if(!m) return n.world?[n.world[12],n.world[13],n.world[14]]:null; const a=m.mesh.mn,b=m.mesh.mx; return M4.pt(m.world,(a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2); };
  R.target=T=>{ if(!T) return null; if(T.t==='w') return T.p;
    if(T.t==='lab'){ const it=findItem(T.type,T.i||0); if(!it) return null; const n=nodeBy(it,q=>q.anim&&q.anim.label===T.label); return n?center(n):null; }
    if(T.t==='btn'){ const it=findItem(T.type,T.i||0); const n=nodeBy(it,q=>q.trig&&q.trig.anim&&q.trig.anim.label===T.label&&q.mesh); return n?center(n):null; }
    if(T.t==='tap'){ const it=findItem(T.type,T.i||0); const L=[]; (function w(q){ if(q.tapHit) L.push(q); q.children.forEach(w); })(it.root); const n=L[T.k||0]; return n&&n.world?M4.pt(n.world,0,0,0):null; }
    if(T.t==='item'){ const it=findItem(T.type,T.i||0); return M4.pt(itemWorld(it),0,T.y!=null?T.y:it.size.h*0.6,0); }
    if(T.t==='card'){ const n=xr.cardNode; if(!n) return null; const Wm=n.fixed||n.world; if(!Wm) return null; return M4.pt(Wm,(T.u-0.5)*VCARD_W,(0.5-T.v)*VCARD_H,0); }
    if(T.t==='hand'){ const n=xr.handNode; if(!n||!n.world) return null; const w=n.world,lx=(T.u-0.5)*0.22,ly=(0.5-T.v)*0.275; return [w[0]*lx+w[4]*ly+w[12],w[1]*lx+w[5]*ly+w[13],w[2]*lx+w[6]*ly+w[14]]; }
    return null; };
  const lerp3=(a,b,k)=>a?[a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,a[2]+(b[2]-a[2])*k]:b.slice();
  R.frame=P=>{ const X=__xrmock; if(P.rig){ xr.rig.x=P.rig[0]; xr.rig.z=P.rig[1]; xr.rig.yaw=P.rig[2]; }
    const inv=M4.inv(rigMatrix()),toL=w=>M4.pt(inv,w[0],w[1],w[2]);
    // голова: смотрит на цель плавно, плюс лёгкое живое покачивание
    let ty=P.hy||0,tp=P.hp!=null?P.hp:-0.08; const lw=R.target(P.look); if(lw){ const l=toL(lw),hy0=1.62; ty=Math.atan2(-l[0],-l[2]); tp=Math.atan2(l[1]-hy0,Math.hypot(l[0],l[2])); tp=Math.max(-0.9,Math.min(0.6,tp)); }
    const k=P.snap?1:0.09; R.hy+=(ty-R.hy)*k; R.hp+=(tp-R.hp)*k; const t=X.t/1000,wob=P.still?0:1;
    const hy=R.hy+Math.sin(t*0.9)*0.012*wob,hp=R.hp+Math.sin(t*1.3+1)*0.008*wob,hx=Math.sin(t*0.7)*0.01*wob,hyy=1.62+Math.sin(t*1.7)*0.004*wob;
    X.head=X.mk(new DOMMatrix().translate(hx,hyy,0).rotateAxisAngle(0,1,0,hy*180/Math.PI).rotateAxisAngle(1,0,0,hp*180/Math.PI));
    const c=Math.cos(hy),s=Math.sin(hy),loc=(ox,oy,oz)=>[hx+c*ox+s*oz,hyy+oy,-s*ox+c*oz];
    // правая рука: целится лучом или держит предмет
    let rp=loc(0.16,-0.3,-0.3); if(P.rhw) rp=toL(P.rhw);
    const aw=R.target(P.aim); if(aw) R.aim=lerp3(R.aim,aw,P.snap?1:0.22); else R.aim=null;
    let yaw=hy*180/Math.PI,pitch=-25,roll=P.roll||0; if(R.aim){ const a=toL(R.aim),d=[a[0]-rp[0],a[1]-rp[1],a[2]-rp[2]]; yaw=Math.atan2(-d[0],-d[2])*180/Math.PI; pitch=Math.atan2(d[1],Math.hypot(d[0],d[2]))*180/Math.PI; }
    if(P.ryaw!=null) yaw=P.ryaw*180/Math.PI; if(P.rpitch!=null) pitch=P.rpitch;
    X.right=X.mk(new DOMMatrix().translate(...rp).rotateAxisAngle(0,1,0,yaw).rotateAxisAngle(1,0,0,pitch).rotateAxisAngle(0,0,1,roll));
    // левая рука: внизу или поднята к лицу (мини-карта)
    R.lhUp+=((P.lh==='up'?1:0)-R.lhUp)*0.12; const u=R.lhUp,lp=loc(-0.19+0.1*u,-0.36+0.17*u,-0.3-0.02*u);
    X.left=X.mk(new DOMMatrix().translate(...lp).rotateAxisAngle(0,1,0,hy*180/Math.PI+20*u).rotateAxisAngle(1,0,0,-35+40*u).rotateAxisAngle(0,0,1,25*u));
    X.rightSrc.gamepad.axes=P.rax||[0,0,0,0]; X.leftSrc.gamepad.axes=P.lax||[0,0,0,0];
    for(const [sd,i,v] of (P.btn||[])){ const g=(sd==='left'?X.leftSrc:X.rightSrc).gamepad; g.buttons[i].pressed=v; g.buttons[i].value=v?1:0; }
    for(const e of (P.ev||[])) X.fire(e,'right');
    X.step(1000/P.fps); return true; };
  return R; })();
