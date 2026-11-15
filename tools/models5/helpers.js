// ===== геометрия для новых моделей: тела вращения, трубки по кривой, листья =====
function latheGeom(pts,seg=32){ const pos=[],nrm=[],uv=[],idx=[],L=[0]; for(let i=1;i<pts.length;i++) L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1])); const LT=L[L.length-1]||1;
  for(let j=0;j<pts.length;j++){ const a=pts[Math.max(0,j-1)],b=pts[Math.min(pts.length-1,j+1)],dr=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dr,dy)||1,nr=dy/l,ny=-dr/l;
    for(let i=0;i<=seg;i++){ const t=i/seg*Math.PI*2,c=Math.cos(t),s=Math.sin(t); pos.push(pts[j][0]*c,pts[j][1],pts[j][0]*s); nrm.push(nr*c,ny,nr*s); uv.push(i/seg,L[j]/LT); } }
  for(let j=0;j<pts.length-1;j++) for(let i=0;i<seg;i++){ const a=j*(seg+1)+i,b=a+seg+1; idx.push(a,b,a+1,a+1,b,b+1); } return {pos,nrm,uv,idx}; }
const LATHE=(key,pts,seg=32)=>{ const k='lt_'+key; if(!meshCache.has(k)) meshCache.set(k,makeMesh(latheGeom(pts,seg))); return meshCache.get(k); };
function LT(parent,key,pts,m,x,y,z,o={}){ return parent.add(new Node(Object.assign({mesh:LATHE(key,pts,o.seg||32),mat:m,pos:[x,y,z]},o))); }
// трубка по ломаной (провода, венчик, спираль тестомеса, паровая трубка)
function tubeGeom(path,r,seg=8){ const pos=[],nrm=[],uv=[],idx=[],n=path.length;
  for(let j=0;j<n;j++){ const p=path[j],q=path[Math.min(n-1,j+1)],o=path[Math.max(0,j-1)]; let t=norm3([q[0]-o[0],q[1]-o[1],q[2]-o[2]]); let a=Math.abs(t[1])<0.9?[0,1,0]:[1,0,0];
    let u=norm3([a[1]*t[2]-a[2]*t[1],a[2]*t[0]-a[0]*t[2],a[0]*t[1]-a[1]*t[0]]),v=[t[1]*u[2]-t[2]*u[1],t[2]*u[0]-t[0]*u[2],t[0]*u[1]-t[1]*u[0]];
    for(let i=0;i<=seg;i++){ const th=i/seg*Math.PI*2,c=Math.cos(th),s=Math.sin(th),nx=u[0]*c+v[0]*s,ny=u[1]*c+v[1]*s,nz=u[2]*c+v[2]*s; pos.push(p[0]+nx*r,p[1]+ny*r,p[2]+nz*r); nrm.push(nx,ny,nz); uv.push(i/seg,j/(n-1)); } }
  for(let j=0;j<n-1;j++) for(let i=0;i<seg;i++){ const a=j*(seg+1)+i,b=a+seg+1; idx.push(a,a+1,b,a+1,b+1,b); } return {pos,nrm,uv,idx}; }
function TB(parent,path,r,m,o={}){ return parent.add(new Node(Object.assign({mesh:makeMesh(tubeGeom(path,r,o.seg||8)),mat:m,pos:[0,0,0]},o))); }
function earClip(P){ const n=P.length,V=[...Array(n).keys()],out=[]; let ar=0; for(let i=0;i<n;i++){ const p=P[i],q=P[(i+1)%n]; ar+=p[0]*q[1]-q[0]*p[1]; } if(ar<0) V.reverse();
  const cr=(u,v,w)=>(v[0]-u[0])*(w[1]-u[1])-(v[1]-u[1])*(w[0]-u[0]),ins=(a,b,c,p)=>cr(a,b,p)>=0&&cr(b,c,p)>=0&&cr(c,a,p)>=0; let g=0;
  while(V.length>3&&g++<8000){ let cut=false; for(let i=0;i<V.length;i++){ const ia=V[(i+V.length-1)%V.length],ib=V[i],ic=V[(i+1)%V.length],a=P[ia],b=P[ib],c=P[ic]; if(cr(a,b,c)<=1e-12) continue; let ok=true; for(const j of V){ if(j===ia||j===ib||j===ic) continue; if(ins(a,b,c,P[j])){ ok=false; break; } } if(!ok) continue; out.push(ia,ib,ic); V.splice(i,1); cut=true; break; } if(!cut) break; }
  if(V.length===3) out.push(V[0],V[1],V[2]); return out; }
// лист: контур (u — поперёк, v — вдоль 0..1), изгиб вниз к кончику, складка по центральной жилке; двусторонний
function leafGeom(outline,W,L,bend=0.25,fold=0.12,twist=0){ const tri=earClip(outline),pos=[],nrm=[],uv=[],idx=[],n=outline.length;
  const f=(u,v)=>{ const x=u*W,z=v*L,tw=twist*v; return [x*Math.cos(tw),-bend*L*v*v+fold*W*Math.abs(u)+x*Math.sin(tw)*0.3,z]; };
  for(const side of [1,-1]){ for(const [u,v] of outline){ const p=f(u,v),e=1e-3,px=f(u+e,v),pz=f(u,v+e),a=[px[0]-p[0],px[1]-p[1],px[2]-p[2]],b=[pz[0]-p[0],pz[1]-p[1],pz[2]-p[2]]; let nn=norm3([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]); if(nn[1]<0) nn=nn.map(q=>-q);
      pos.push(...p); nrm.push(...nn.map(q=>q*side)); uv.push(u*0.5+0.5,v); } }
  for(let i=0;i<tri.length;i+=3){ idx.push(tri[i],tri[i+2],tri[i+1]); idx.push(tri[i]+n,tri[i+1]+n,tri[i+2]+n); } return {pos,nrm,uv,idx}; }
function monsteraOutline(seed){ const r=rnd(seed),H=[[0,1],[0.13,0.93],[0.27,0.83],[0.39,0.69],[0.47,0.53],[0.49,0.39],[0.45,0.25],[0.37,0.13],[0.25,0.04],[0.12,0.03],[0.04,0.1],[0,0.15]],R=[];
  for(let i=0;i<H.length-1;i++){ R.push(H[i]); if(i>=1&&i<=7&&r()<0.8){ const a=H[i],b=H[i+1],m=[(a[0]+b[0])/2,(a[1]+b[1])/2],dx=b[0]-a[0],dy=b[1]-a[1],k=0.018/Math.hypot(dx,dy),dp=0.38+r()*0.18;
      R.push([m[0]-dx*k,m[1]-dy*k],[m[0]*dp,m[1]-m[0]*0.28*(1-dp)],[m[0]+dx*k,m[1]+dy*k]); } } R.push(H[H.length-1]);
  const out=R.slice(0,R.length-1); for(let i=R.length-2;i>=1;i--) out.push([-R[i][0],R[i][1]]); return out; }
// ===== текстуры для новых моделей — рисуются один раз при первом использовании =====
const GT=(key,draw,w=512,h=512,rep=true)=>{ if(!TEX[key]){ const c=mkCanvas(w,h),x=c.getContext('2d'); draw(x,w,h); TEX[key]=texFromCanvas(c,rep); } return key; };
function speckle(x,w,h,n,cols,rmax,seed){ const r=rnd(seed); for(let i=0;i<n;i++){ x.fillStyle=cols[Math.floor(r()*cols.length)]; const s=r()*rmax+0.4; x.fillRect(r()*w,r()*h,s,s); } }
const TX={
  concrete:()=>GT('concrete',(x,w,h)=>{ x.fillStyle='#a9a7a2'; x.fillRect(0,0,w,h); const r=rnd(77); for(let i=0;i<900;i++){ const g=x.createRadialGradient(0,0,0,0,0,1); const a=r()*0.08; g.addColorStop(0,`rgba(${r()<0.5?60:230},${r()<0.5?60:228},${r()<0.5?58:222},${a})`); g.addColorStop(1,'rgba(0,0,0,0)'); x.setTransform(r()*60+10,0,0,r()*60+10,r()*w,r()*h); x.fillStyle=g; x.beginPath(); x.arc(0,0,1,0,7); x.fill(); } x.setTransform(1,0,0,1,0,0);
    speckle(x,w,h,5000,['rgba(70,68,64,.5)','rgba(240,238,232,.35)','rgba(110,106,100,.4)'],1.6,78); for(let i=0;i<260;i++){ x.fillStyle='rgba(55,52,48,.55)'; x.beginPath(); x.arc(r()*w,r()*h,r()*2.2+0.6,0,7); x.fill(); } }),
  linen:()=>GT('linen',(x,w,h)=>{ x.fillStyle='#e9e1d2'; x.fillRect(0,0,w,h); const r=rnd(5); for(let y=0;y<h;y+=2){ x.fillStyle=`rgba(${120+r()*40},${105+r()*30},${80+r()*20},${0.05+r()*0.12})`; x.fillRect(0,y,w,1); } for(let X=0;X<w;X+=2){ x.fillStyle=`rgba(255,255,255,${0.04+r()*0.1})`; x.fillRect(X,0,1,h); } speckle(x,w,h,1400,['rgba(140,120,90,.35)','rgba(255,255,250,.4)'],2,6); }),
  soil:()=>GT('soil',(x,w,h)=>{ x.fillStyle='#3b2c20'; x.fillRect(0,0,w,h); speckle(x,w,h,9000,['#2a1f16','#4d3a2a','#5c4632','#1d1610','#6f6a60'],3.2,9); }),
  leafMon:()=>GT('leafMon',(x,w,h)=>{ const g=x.createLinearGradient(0,0,0,h); g.addColorStop(0,'#1f5426'); g.addColorStop(0.5,'#2a6b30'); g.addColorStop(1,'#245f2b'); x.fillStyle=g; x.fillRect(0,0,w,h); const r=rnd(12);
    for(let i=0;i<5000;i++){ x.fillStyle=`rgba(${r()<0.5?20:90},${r()<0.5?60:140},${r()<0.5?25:70},${r()*0.12})`; x.fillRect(r()*w,r()*h,2,2); }
    x.strokeStyle='rgba(170,205,120,.75)'; x.lineWidth=7; x.beginPath(); x.moveTo(w/2,0); x.lineTo(w/2,h); x.stroke(); x.lineWidth=3; x.strokeStyle='rgba(150,195,110,.5)';
    for(let k=1;k<13;k++){ const y0=h*k/13; for(const s of [-1,1]){ x.beginPath(); x.moveTo(w/2,y0); x.quadraticCurveTo(w/2+s*w*0.22,y0+h*0.05,w/2+s*w*0.5,y0+h*0.09); x.stroke(); } }
    const sh=x.createLinearGradient(0,0,w,0); sh.addColorStop(0,'rgba(0,0,0,.18)'); sh.addColorStop(0.5,'rgba(255,255,255,.06)'); sh.addColorStop(1,'rgba(0,0,0,.18)'); x.fillStyle=sh; x.fillRect(0,0,w,h); },512,1024,false),
  sansev:()=>GT('sansev',(x,w,h)=>{ x.fillStyle='#2f5a2c'; x.fillRect(0,0,w,h); const r=rnd(31); for(let y=0;y<h;y+=6+r()*14){ x.fillStyle=r()<0.5?`rgba(150,185,120,${0.25+r()*0.25})`:`rgba(18,40,20,${0.3+r()*0.3})`; x.beginPath(); x.moveTo(0,y); for(let X=0;X<=w;X+=16) x.lineTo(X,y+Math.sin(X*0.05+y)*5); x.lineTo(w,y+4+r()*5); x.lineTo(0,y+4+r()*5); x.fill(); }
    const e=x.createLinearGradient(0,0,w,0); e.addColorStop(0,'rgba(220,205,90,.95)'); e.addColorStop(0.09,'rgba(220,205,90,.0)'); e.addColorStop(0.91,'rgba(220,205,90,0)'); e.addColorStop(1,'rgba(220,205,90,.95)'); x.fillStyle=e; x.fillRect(0,0,w,h); },128,1024,false),
  pages:()=>GT('pages',(x,w,h)=>{ x.fillStyle='#f1ece0'; x.fillRect(0,0,w,h); const r=rnd(3); for(let y=0;y<h;y+=2){ x.fillStyle=`rgba(120,105,80,${0.05+r()*0.14})`; x.fillRect(0,y,w,1); } for(let X=0;X<w;X+=2){ x.fillStyle=`rgba(120,105,80,${0.05+r()*0.14})`; x.fillRect(X,0,1,h); } },256,256),
  cloth:()=>GT('cloth',(x,w,h)=>{ x.fillStyle='#ffffff'; x.fillRect(0,0,w,h); const r=rnd(44); for(let y=0;y<h;y+=2){ x.fillStyle=`rgba(0,0,0,${0.03+r()*0.06})`; x.fillRect(0,y,w,1); } for(let X=0;X<w;X+=2){ x.fillStyle=`rgba(255,255,255,${0.05+r()*0.1})`; x.fillRect(X,0,1,h); } speckle(x,w,h,1500,['rgba(0,0,0,.12)','rgba(255,255,255,.25)'],1.5,45); }),
  glaze:()=>GT('glaze',(x,w,h)=>{ x.fillStyle='#ffffff'; x.fillRect(0,0,w,h); const r=rnd(8); for(let y=0;y<h;y++){ x.fillStyle=`rgba(0,0,0,${Math.max(0,Math.sin(y*0.09+Math.sin(y*0.013)*4))*0.06})`; x.fillRect(0,y,w,1); } speckle(x,w,h,2200,['rgba(60,45,30,.55)','rgba(110,90,70,.4)','rgba(255,255,255,.6)'],2.2,9); }),
  wax:()=>GT('wax',(x,w,h)=>{ x.fillStyle='#ffffff'; x.fillRect(0,0,w,h); const r=rnd(19); for(let i=0;i<60;i++){ x.strokeStyle=`rgba(200,180,150,${r()*0.18})`; x.lineWidth=r()*6+1; x.beginPath(); const X=r()*w; x.moveTo(X,0); x.bezierCurveTo(X+r()*30-15,h*0.3,X+r()*30-15,h*0.7,X+r()*20-10,h); x.stroke(); } },256,256),
  grate:()=>GT('grate',(x,w,h)=>{ x.fillStyle='#d6d9dc'; x.fillRect(0,0,w,h); x.fillStyle='#1a1b1d'; for(let i=0;i<16;i++) for(let j=0;j<16;j++){ rrect(x,i*w/16+3,j*h/16+3,w/16-6,h/16-6,3); x.fill(); } },256,256),
  marble:()=>GT('marble',(x,w,h)=>{ x.fillStyle='#ecebe7'; x.fillRect(0,0,w,h); const r=rnd(61); for(let i=0;i<26;i++){ x.strokeStyle=`rgba(${110+r()*40},${110+r()*40},${115+r()*40},${0.15+r()*0.35})`; x.lineWidth=r()*2.4+0.4; x.beginPath(); let X=r()*w,Y=r()*h; x.moveTo(X,Y); for(let k=0;k<12;k++){ X+=r()*80-30; Y+=r()*60-30; x.lineTo(X,Y); } x.stroke(); } speckle(x,w,h,1500,['rgba(140,140,145,.25)','rgba(255,255,255,.5)'],2,62); })
};
