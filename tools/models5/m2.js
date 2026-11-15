  pka6:{name:'Пароконвектомат ПКА 6-1/3П',cat:'catering',small:true,purpose:'Бойлерный мини-пароконвектомат на 6 уровней GN 1/3: пар и горячий воздух по отдельности или вместе. Нажмите на ручку — откроется дверца со стеклом. Круглая кнопка справа на панели включает аппарат: загораются табло, свет в камере, крутится вентилятор и из трубы идёт пар. Гастроёмкости внутри выдвигаются.',
    specs:[['Габариты','520×540 (593 с ручкой) × 690 мм'],['Уровней','6 × GN 1/3, шаг 60 мм'],['Температура','до 270 °C'],['Парообразование','бойлерное'],['Мощность','3,2 кВт, 230 В'],['Масса','45 кг']],materials:'Корпус и камера — нержавеющая сталь AISI 304, дверца — закалённое двойное стекло в чёрной стеклянной рамке, панель — стекло',
    variants:[{name:'Нержавейка'}],
    build(root,v){ const W=0.52,D=0.54,H=0.69,st=mat(hex('#cdd0d4'),0.9,{tex:'brushed',texMode:4,texScale:3.2}),stI=mat(hex('#dfe2e5'),1,{tex:'brushed',texMode:4,texScale:5}),blk=mat(hex('#0d0e10'),1,{noTex:true}),chrome=mat(hex('#e8ebee'),1,{noTex:true}),dk=mat(hex('#1d1e21'),0.5,{noTex:true}),F=D/2;
      for(const sx of [-1,1]) for(const sz of [-1,1]){ C(root,0.016,0.018,dk,sx*(W/2-0.04),0.009,sz*(D/2-0.05),{seg:14}); }
      // корпус из листов: бока, верх, низ, зад, рамка проёма камеры
      const y0=0.018,y1=H; P(root,0.012,y1-y0,D,st,-W/2+0.006,(y0+y1)/2,0); P(root,0.012,y1-y0,D,st,W/2-0.006,(y0+y1)/2,0); P(root,W,0.012,D,st,0,y1-0.006,0); P(root,W,0.03,D,st,0,y0+0.015,0); P(root,W,y1-y0,0.012,st,0,(y0+y1)/2,-D/2+0.006);
      for(let i=0;i<9;i++) P(root,0.002,0.006,0.16,dk,-W/2-0.0005,0.42+i*0.016,-0.12);
      const cx=-0.03,cw=0.37,ch=0.38,cy=0.1+ch/2,cd=0.4,cz=F-0.03-cd/2; // камера
      P(root,cw,0.004,cd,stI,cx,cy-ch/2,cz); P(root,cw,0.004,cd,stI,cx,cy+ch/2,cz); P(root,0.004,ch,cd,stI,cx-cw/2,cy,cz); P(root,0.004,ch,cd,stI,cx+cw/2,cy,cz); P(root,cw,ch,0.004,stI,cx,cy,cz-cd/2);
      P(root,W-0.024,0.052,0.03,st,0,0.074,F-0.015); P(root,W-0.024,0.58-(cy+ch/2),0.03,st,0,(0.58+cy+ch/2)/2,F-0.015);
      P(root,(cx-cw/2)-(-W/2+0.012),ch,0.03,st,(-W/2+0.012+cx-cw/2)/2,cy,F-0.015); P(root,(W/2-0.012)-(cx+cw/2),ch,0.03,st,(W/2-0.012+cx+cw/2)/2,cy,F-0.015);
      // направляющие на 6 уровней
      for(const sx of [-1,1]){ const xx=cx+sx*(cw/2-0.02); for(const zz of [cz-cd/2+0.05,cz+cd/2-0.05]) TB(root,[[xx,cy-ch/2+0.02,zz],[xx,cy+ch/2-0.03,zz]],0.003,chrome,{seg:6});
        for(let k=0;k<6;k++){ const yy=cy-ch/2+0.045+k*0.058; TB(root,[[xx,yy,cz-cd/2+0.05],[xx+sx*0.004,yy-0.004,cz-cd/2+0.03],[xx+sx*0.004,yy-0.004,cz+cd/2-0.03],[xx,yy,cz+cd/2-0.05]],0.0022,chrome,{seg:5}); } }
      // вентилятор с кольцевым ТЭНом и решёткой
      const fz=cz-cd/2+0.014; const ring=r=>{ const p=[]; for(let i=0;i<=36;i++){ const a=i/36*Math.PI*2; p.push([cx+Math.cos(a)*r,cy+Math.sin(a)*r,fz]); } return p; };
      TB(root,ring(0.125),0.006,mat(hex('#5b5f66'),0.6,{noTex:true}),{seg:8}); TB(root,ring(0.112),0.006,mat(hex('#5b5f66'),0.6,{noTex:true}),{seg:8});
      const on=G(root,0,0,0,{anim:anim('glow',1,'Работа')}); on.anim.rate=1.2; root.ovenOn=on;
      const fan=G(root,cx,cy,fz+0.008,{anim:anim('spin',9,'Вентилятор')}); fan.anim.axis='z'; fan.anim.rate=0.8; C(fan,0.022,0.012,chrome,0,0,0,{rotX:Math.PI/2,seg:18});
      for(let k=0;k<8;k++){ const a=k/8*Math.PI*2,g=G(fan,0,0,0,{rotZ:a}); P(g,0.012,0.08,0.016,stI,0.02,0.055,0,{rotY:0.5}); } on.anim.link=[fan];
      for(const r of [0.06,0.1,0.14]) TB(root,ring(r).map(p=>[p[0],p[1],fz+0.03]),0.0016,chrome,{seg:5}); for(let k=0;k<12;k++){ const a=k/12*Math.PI*2; TB(root,[[cx+Math.cos(a)*0.03,cy+Math.sin(a)*0.03,fz+0.03],[cx+Math.cos(a)*0.145,cy+Math.sin(a)*0.145,fz+0.03]],0.0016,chrome,{seg:5}); }
      // подсветка камеры
      C(on,0.02,0.006,mat([0.7,0.68,0.6],0.5,{glow:[1,0.92,0.7],glowFull:true,noTex:true}),cx+cw/2-0.002,cy+ch/2-0.06,cz+0.08,{rotZ:Math.PI/2,seg:18});
      // гастроёмкости GN 1/3 с выпечкой
      const gm=mat(hex('#d9dce0'),1,{tex:'brushed',texMode:4,texScale:8}),bun=mat(hex('#c98a3e'),0.35,{noTex:true}),bunT=mat(hex('#a7652a'),0.45,{noTex:true});
      [1,3].forEach((lv,i)=>{ const yy=cy-ch/2+0.045+lv*0.058+0.003,tr=G(root,cx,yy,cz+0.01,{anim:anim('slideZ',0.26,'Гастроёмкость')}); tr.anim.rate=1.8;
        P(tr,0.325,0.003,0.176,gm,0,0,0); for(const sz of [-1,1]) P(tr,0.325,0.022,0.003,gm,0,0.011,sz*0.088); for(const sx of [-1,1]) P(tr,0.003,0.022,0.176,gm,sx*0.1625,0.011,0); for(const sx of [-1,1]) P(tr,0.008,0.004,0.19,gm,sx*0.17,0.022,0);
        for(let k=0;k<6;k++){ const bx=-0.11+(k%3)*0.11,bz=-0.042+Math.floor(k/3)*0.084; if(i===0){ SPHn(tr,1,bun,bx,0.016,bz,{scl:[0.042,0.018,0.034]}); SPHn(tr,1,bunT,bx,0.022,bz,{scl:[0.034,0.014,0.027]}); } else { const g=G(tr,bx,0.012,bz,{rotY:k*0.7}); SPHn(g,1,bun,0,0,0,{scl:[0.048,0.014,0.022]}); for(const q of [-0.03,0,0.03]) SPHn(g,1,bunT,q,0.006,0,{scl:[0.014,0.01,0.02]}); } } });
      // панель управления: чёрное стекло, табло, кнопки
      const pc=mkCanvas(1024,224),x=pc.getContext('2d'),gg=x.createLinearGradient(0,0,0,224); gg.addColorStop(0,'#1a1b1e'); gg.addColorStop(0.5,'#0a0b0c'); gg.addColorStop(1,'#141517'); x.fillStyle=gg; x.fillRect(0,0,1024,224);
      x.fillStyle='#cfd2d6'; x.font='600 17px Arial'; x.textAlign='center'; x.fillText('ТЕМПЕРАТУРА',370,46); x.fillText('ЩУП',530,46); x.fillText('ВРЕМЯ',690,46); x.fillText('1  2  3  4',850,46);
      for(const X of [370,530,690]){ x.fillStyle='#050505'; rrect(x,X-62,58,124,56,6); x.fill(); x.fillStyle='rgba(120,20,20,.55)'; x.font='700 44px "Courier New",monospace'; x.fillText('888',X,102); }
      const ic=[[70,'☁'],[130,'♨'],[190,'≋'],[250,'✱'],[310,'↻']]; ic.forEach(([X,t])=>{ x.strokeStyle='#8e9196'; x.lineWidth=2; rrect(x,X-22,128,44,40,6); x.stroke(); x.fillStyle='#d9dbde'; x.font='22px Arial'; x.fillText(t,X,156); });
      for(const X of [330,410,490,570,650,730]){ x.strokeStyle='#8e9196'; x.beginPath(); x.moveTo(X-10,156); x.lineTo(X,144); x.lineTo(X+10,156); x.stroke(); }
      for(let i=0;i<4;i++){ x.fillStyle='#1f8b3c'; x.beginPath(); x.arc(818+i*22,72,5,0,7); x.fill(); } x.strokeStyle='#8e9196'; rrect(x,810,128,80,40,6); x.stroke(); x.fillStyle='#d9dbde'; x.font='600 18px Arial'; x.fillText('ПУСК/СТОП',850,154);
      x.fillStyle='#e8eaec'; x.font='italic 700 26px Georgia,serif'; x.fillText('Abat',90,70); const pk='pkaPanel'; if(!TEX[pk]) TEX[pk]=texFromCanvas(pc);
      const PH=0.1,PY=0.63; P(root,W-0.004,PH+0.008,0.014,blk,0,PY,F-0.004); root.add(new Node({mesh:QUAD(W-0.012,PH),mat:mat([1,1,1],1,{tex:pk}),pos:[0,PY,F+0.0032]}));
      const dc=mkCanvas(512,96),y=dc.getContext('2d'); y.fillStyle='#000'; y.fillRect(0,0,512,96); y.fillStyle='#ff2a1a'; y.font='700 70px "Courier New",monospace'; y.textAlign='center'; y.fillText('180',86,74); y.fillText('---',256,74); y.fillText('0:25',428,74); const dk2='pkaDisp'; if(!TEX[dk2]) TEX[dk2]=texFromCanvas(dc);
      const px=X=>-(W-0.012)/2+X/1024*(W-0.012),py=Y=>PY+PH/2-Y/224*PH; [[370,0],[530,1],[690,2]].forEach(([X,i])=>{ const q=on.add(new Node({mesh:QUAD(0.059,0.024),mat:mat([0.25,0.05,0.04],0.3,{tex:dk2,glow:[1.3,1.3,1.3],glowFull:true}),pos:[px(X),py(86),F+0.0036]})); q.mesh=makeMesh({pos:[-0.0295,-0.012,0,0.0295,-0.012,0,0.0295,0.012,0,-0.0295,0.012,0],nrm:[0,0,1,0,0,1,0,0,1,0,0,1],uv:[i/3,1,(i+1)/3,1,(i+1)/3,0,i/3,0],idx:[0,1,2,0,2,3]}); });
      const pw=C(root,0.014,0.008,mat(hex('#202226'),0.6,{noTex:true}),W/2-0.035,PY+0.012,F+0.006,{rotX:Math.PI/2,seg:22}); pw.trig=on; C(on,0.016,0.002,mat([0.1,0.3,0.6],0.4,{glow:[0.3,0.7,1],glowFull:true,noTex:true}),W/2-0.035,PY+0.012,F+0.0105,{rotX:Math.PI/2,seg:22});
      const sb=P(root,0.04,0.02,0.004,mat(hex('#1a1b1e'),0.5,{noTex:true}),px(850),py(148),F+0.0045); sb.trig=on;
      // полоса с прорезями под панелью
      P(root,W-0.02,0.02,0.006,st,0,0.568,F-0.002); for(let i=0;i<14;i++) P(root,0.016,0.004,0.002,dk,-0.2+i*0.031,0.568,F+0.0015);
      // труба пароотвода и пар
      C(root,0.02,0.045,st,W/2-0.08,H+0.022,-D/2+0.08,{seg:18}); const stm=G(root,W/2-0.08,H+0.045,-D/2+0.08,{anim:anim('sway',0.25,'Пар')}); stm.anim.speed=2.5; const sm=mat([0.95,0.96,0.97],0.2,{alpha:0.22,noTex:true});
      const puff=G(stm,0,0,0,{anim:anim('scaleY',1,'Клубы пара')}); for(let k=0;k<5;k++) SPHn(puff,1,sm,Math.sin(k*1.7)*0.012,0.03+k*0.035,Math.cos(k*1.3)*0.01,{scl:[0.022+k*0.007,0.02+k*0.006,0.022+k*0.007]}); on.anim.link=[fan,stm,puff];
      // дверца: чёрное стекло, окно, винты, логотип, ручка слева
      const dW=W-0.012,dH=0.51,dz=F+0.002,door=G(root,W/2-0.006,0.045,dz,{anim:anim('rotY',1.95,'Дверца')}); door.anim.rate=1.4; const ox=-dW/2,gl=mat(hex('#0b0c0e'),1,{noTex:true});
      const wx0=-0.335,wx1=-0.085,wy0=0.075,wy1=0.42,dcx=cx-(W/2-0.006),dcy=cy-0.045; P(door,dW,wy0,0.03,gl,ox,wy0/2,0.015); P(door,dW,dH-wy1,0.03,gl,ox,(dH+wy1)/2,0.015);
      P(door,(wx0)-(-dW),wy1-wy0,0.03,gl,(wx0-dW)/2,(wy0+wy1)/2,0.015); P(door,0-wx1,wy1-wy0,0.03,gl,wx1/2,(wy0+wy1)/2,0.015);
      P(door,wx1-wx0,wy1-wy0,0.004,mat([0.18,0.2,0.22],1,{alpha:0.35,noTex:true}),(wx0+wx1)/2,(wy0+wy1)/2,0.028); P(door,wx1-wx0+0.03,wy1-wy0+0.03,0.004,mat([0.6,0.62,0.64],1,{alpha:0.18,noTex:true}),(wx0+wx1)/2,(wy0+wy1)/2,-0.004);
      for(const xx of [wx0-0.03,wx1+0.03]) for(const yy of [wy0-0.02,wy1+0.02]) C(door,0.007,0.004,chrome,xx,yy,0.031,{rotX:Math.PI/2,seg:14});
      const lc=mkCanvas(256,64),z=lc.getContext('2d'); z.fillStyle='#0b0c0e'; z.fillRect(0,0,256,64); z.fillStyle='#e8eaec'; z.font='italic 700 34px Georgia,serif'; z.textAlign='center'; z.fillText('Abat',128,44); const lk='abatLogo'; if(!TEX[lk]) TEX[lk]=texFromCanvas(lc);
      door.add(new Node({mesh:QUAD(0.09,0.0225),mat:mat([1,1,1],0.8,{tex:lk}),pos:[ox,0.035,0.0305]}));
      // внутренняя сторона: нержавейка и белый уплотнитель
      const sl=mat(hex('#eceae6'),0.2,{noTex:true}); P(door,cw+0.02,0.012,0.012,sl,dcx,dcy+ch/2+0.006,-0.008); P(door,cw+0.02,0.012,0.012,sl,dcx,dcy-ch/2-0.006,-0.008); P(door,0.012,ch+0.02,0.012,sl,dcx-cw/2-0.006,dcy,-0.008); P(door,0.012,ch+0.02,0.012,sl,dcx+cw/2+0.006,dcy,-0.008);
      const hm=mat(hex('#e9eaec'),0.8,{noTex:true}); P(door,0.022,0.05,0.02,hm,ox-dW/2+0.03,0.31,0.04); P(door,0.022,0.04,0.02,hm,ox-dW/2+0.03,0.18,0.04); TB(door,[[ox-dW/2+0.03,0.33,0.05],[ox-dW/2+0.03,0.315,0.068],[ox-dW/2+0.034,0.25,0.072],[ox-dW/2+0.03,0.17,0.066],[ox-dW/2+0.03,0.16,0.05]],0.012,hm,{seg:12}); },
    lights:it=>{ const n=it.root.ovenOn; return n?[{p:M4.pt(itemWorld(it),-0.03,0.25,0.4),c:[1,0.86,0.6],pow:0.45,k:5,down:false,sh:false,on:ease(n.anim.t)}]:[]; } },
  pk6:{name:'Подставка ПК-6-6/4',cat:'catering',purpose:'Подставка под пароконвектомат или конвекционную печь с направляющими на 6 противней 600×400. Нажмите на противень — он выдвинется. На столешницу можно поставить пароконвектомат.',
    specs:[['Габариты','840×700×770 (800) мм'],['Противни','6 × 600×400 мм'],['Масса','26 кг'],['Опоры','регулируемые, +30 мм']],materials:'Нержавеющая сталь AISI 430, профильная труба 40×40 мм',
    variants:[{name:'Нержавейка'}],
    build(root,v){ const W=0.84,D=0.7,H=0.77,st=mat(hex('#cdd0d4'),0.9,{tex:'brushed',texMode:4,texScale:3}),tb=mat(hex('#c3c7cb'),0.85,{tex:'brushed',texMode:4,texScale:6}),dk=mat(hex('#2a2b2e'),0.5,{noTex:true}),T=0.04,fh=0.035;
      // столешница с загибом
      P(root,W,0.0025,D,st,0,H-0.00125,0); for(const sz of [-1,1]) P(root,W,0.035,0.0025,st,0,H-0.0175,sz*(D/2-0.00125)); for(const sx of [-1,1]) P(root,0.0025,0.035,D,st,sx*(W/2-0.00125),H-0.0175,0);
      for(const sx of [-1,1]) for(const sz of [-1,1]) C(root,0.004,0.002,dk,sx*(W/2-0.025),H+0.001,sz*(D/2-0.025),{seg:10});
      // ножки и регулируемые опоры
      const lx=W/2-T/2-0.004,lz=D/2-T/2-0.004; for(const sx of [-1,1]) for(const sz of [-1,1]){ P(root,T,H-0.035-fh,T,tb,sx*lx,fh+(H-0.035-fh)/2,sz*lz); P(root,T-0.004,0.003,T-0.004,dk,sx*lx,fh+0.0015,sz*lz); C(root,0.008,0.02,mat(hex('#b9bcc0'),0.9,{noTex:true}),sx*lx,fh-0.01,sz*lz,{seg:6}); C(root,0.02,0.012,dk,sx*lx,0.006,sz*lz,{seg:18}); }
      // нижняя рама и обвязка под столешницей
      const r=0.03,yl=0.12; for(const sx of [-1,1]) P(root,r,r,D-2*T,tb,sx*lx,yl,0); P(root,W-2*T,r,r,tb,0,yl,-lz); P(root,W-2*T,r,r,tb,0,H-0.05,-lz); for(const sx of [-1,1]) P(root,r,r,D-2*T,tb,sx*lx,H-0.05,0);
      // секция с направляющими справа
      const rx0=W/2-T-0.4-0.012,ix=rx0-0.015; for(const sz of [-1,1]) P(root,r,H-0.05-yl,r,tb,ix,(H-0.05+yl)/2,sz*lz); P(root,r,r,D-2*T,tb,ix,yl,0); P(root,r,r,D-2*T,tb,ix,H-0.05,0);
      const levels=[0.19,0.27,0.35,0.43,0.51,0.59]; for(const y of levels){ for(const [xx,s] of [[ix+r/2,1],[lx-T/2,-1]]){ P(root,0.022,0.0025,D-2*T+0.03,tb,xx+s*0.011,y,0); P(root,0.0025,0.02,D-2*T+0.03,tb,xx+s*0.0012,y+0.009,0); } }
      const tm=mat(hex('#b3b7bc'),0.95,{tex:'brushed',texMode:4,texScale:7}),bun=mat(hex('#c98a3e'),0.35,{noTex:true}),bunT=mat(hex('#a7652a'),0.45,{noTex:true}),cx=(ix+r/2+lx-T/2)/2;
      levels.forEach((y,i)=>{ const tr=G(root,cx,y+0.003,0,{anim:anim('slideZ',0.42,'Противень '+(i+1))}); tr.anim.rate=1.8; P(tr,0.4,0.0015,0.6,tm,0,0,0); for(const sz of [-1,1]) P(tr,0.4,0.012,0.0015,tm,0,0.006,sz*0.3); for(const sx of [-1,1]) P(tr,0.0015,0.012,0.6,tm,sx*0.2,0.006,0);
        if(i===1||i===4){ for(let k=0;k<12;k++){ const bx=-0.135+(k%3)*0.135,bz=-0.23+Math.floor(k/3)*0.153; SPHn(tr,1,bun,bx,0.016,bz,{scl:[0.045,0.02,0.045]}); SPHn(tr,1,bunT,bx,0.023,bz,{scl:[0.036,0.014,0.036]}); } } }); } },
