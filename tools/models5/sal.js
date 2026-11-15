    build(root,v){ const W=1.37,D=0.7,H=0.86,st=mat(hex('#c9ccd0'),0.85,{tex:'brushed',texMode:4,texScale:3}),st2=mat(hex('#d8dbde'),0.95,{tex:'brushed',texMode:4,texScale:5}),dk=mat(hex('#1d1e21'),0.4,{noTex:true}),ins=mat(hex('#e9eaeb'),0.6,{tex:'brushed',texMode:4,texScale:6}),chrome=mat(hex('#e8ebee'),1,{noTex:true}),t=0.02,F=D/2,yb=0.205,dH=H-0.015-yb-0.006;
      for(const sx of [-1,1]) for(const sz of [-1,1]){ C(root,0.025,0.1,st2,sx*(W/2-0.06),0.05,sz*(D/2-0.06),{seg:16}); C(root,0.032,0.012,dk,sx*(W/2-0.06),0.006,sz*(D/2-0.06),{seg:16}); }
      // корпус: дно, бока, зад, средняя стойка, цоколь с решёткой и пультом
      P(root,W,t,D,st,0,0.11,0); P(root,t,H-0.1,D,st,-W/2+t/2,0.11+(H-0.1)/2,0); P(root,t,H-0.1,D,st,W/2-t/2,0.11+(H-0.1)/2,0); P(root,W,H-0.1,t,st,0,0.11+(H-0.1)/2,-D/2+t/2);
      P(root,0.03,H-yb,D-0.03,st,0,yb+(H-yb)/2,0.0); P(root,W,yb-0.11,0.02,st,0,(yb+0.11)/2,F-0.01); P(root,W,0.015,0.02,st,0,H-0.0075,F-0.01);
      for(let i=0;i<5;i++) P(root,0.62,0.006,0.002,dk,-0.3,0.13+i*0.014,F+0.0005);
      // камеры: обшивка и решётчатые полки
      for(const sx of [-1,1]){ const xc=sx*(W/4+0.004),cw=W/2-0.045; P(root,cw,0.004,D-0.06,ins,xc,yb+0.002,0); P(root,cw,dH,0.004,ins,xc,yb+dH/2,-D/2+0.024); P(root,cw,0.004,D-0.06,ins,xc,H-0.017,0);
        for(const y of [yb+0.22,yb+0.43]){ const sh=G(root,xc,y,0); P(sh,cw-0.02,0.004,D-0.12,mat(hex('#d0d3d6'),0.9,{tex:TX.grate(),texMode:4,texScale:14}),0,0,0); for(const ss of [-1,1]) TB(root,[[xc+ss*(cw/2-0.008),y,-D/2+0.06],[xc+ss*(cw/2-0.008),y,D/2-0.06]],0.004,chrome,{seg:6}); }
        P(root,0.004,0.06,0.03,dk,sx*(W/2-0.022),yb+0.06,F-0.04); }
      // столешница, борт, ванны с продуктами
      P(root,W,0.04,D,st,0,H+0.02,0); P(root,W,0.12,0.03,st,0,H+0.1,-D/2+0.015);
      const food=['#c93a2a','#6aa33f','#f0d36a','#f3efe4','#2d2a24','#e8a04a'];
      for(let i=0;i<6;i++){ const x=-0.5+i*0.2; P(root,0.18,0.004,0.17,dk,x,H+0.041,-0.13); P(root,0.165,0.004,0.155,mat(hex(food[i]),0.15,{noTex:true}),x,H+0.032,-0.13); for(let k=0;k<9;k++) C(root,0.012,0.008,mat(hex(food[i]).map(c=>c*(0.85+0.3*((k*37)%10)/10)),0.2,{noTex:true}),x-0.05+(k%3)*0.05,H+0.038,-0.18+Math.floor(k/3)*0.05,{seg:8}); }
      const lid=G(root,0,H+0.04,-0.215,{anim:anim('rotX',-1.35,'Крышка ванн')}); lid.anim.rate=1.6; P(lid,1.24,0.012,0.2,st,0,0.006,0.1); P(lid,1.24,0.02,0.012,st2,0,0.012,0.2); P(lid,0.3,0.008,0.03,st2,0,0.004,0.215);
      P(root,1.2,0.022,0.26,mat(hex('#f4f4ef'),0.25,{noTex:true}),-0.03,H+0.051,0.2); P(root,1.2,0.002,0.26,mat(hex('#e6e6df'),0.2,{noTex:true}),-0.03,H+0.0625,0.2);
      // дверцы во всю высоту проёма: нержавейка снаружи, обшивка и уплотнитель внутри, ручка-скоба
      const dw=W/2-0.022; [[-1,'Левая дверца'],[1,'Правая дверца']].forEach(([s,l])=>{ const d=G(root,s*(W/2-0.004),yb+0.003,F,{anim:anim('rotY',s*1.75,l)}); d.anim.rate=1.6; const cx=-s*dw/2;
        RB(d,dw,dH,0.045,0.006,st,cx,dH/2,0.0225,{N:4}); P(d,dw-0.05,dH-0.05,0.004,ins,cx,dH/2,-0.002); const g=mat(hex('#2b2d31'),0.3,{noTex:true}); P(d,dw-0.02,0.012,0.008,g,cx,0.012,-0.002); P(d,dw-0.02,0.012,0.008,g,cx,dH-0.012,-0.002); P(d,0.012,dH-0.02,0.008,g,cx-dw/2+0.012,dH/2,-0.002); P(d,0.012,dH-0.02,0.008,g,cx+dw/2-0.012,dH/2,-0.002);
        const hx=-s*(dw-0.055); for(const yy of [dH/2-0.17,dH/2+0.17]) C(d,0.008,0.03,chrome,hx,yy,0.06,{rotX:Math.PI/2,seg:12}); TB(d,[[hx,dH/2-0.18,0.074],[hx,dH/2+0.18,0.074]],0.0095,chrome,{seg:14}); });
      // пульт на цоколе справа: табло, кнопка, индикатор — не на дверце
      const pc=mkCanvas(256,128),x=pc.getContext('2d'); x.fillStyle='#1b1c1f'; x.fillRect(0,0,256,128); x.fillStyle='#071108'; rrect(x,14,22,150,84,8); x.fill(); x.fillStyle='#38ff76'; x.font='700 58px "Courier New",monospace'; x.textAlign='center'; x.fillText('+4°',89,84);
      x.fillStyle='#9aa0a6'; x.font='600 18px Arial'; x.fillText('SET',214,48); x.fillText('°C',214,96); if(!TEX.salPanel) TEX.salPanel=texFromCanvas(pc);
      P(root,0.19,0.082,0.006,dk,W/2-0.17,0.158,F+0.002); root.add(new Node({mesh:QUAD(0.17,0.075),mat:mat([1,1,1],0.3,{tex:'salPanel',emis:0.3}),pos:[W/2-0.17,0.158,F+0.0052]}));
      const on=G(root,0,0,0,{anim:anim('glow',1,'Охлаждение',true)}); C(on,0.006,0.004,mat([0.1,0.4,0.15],0.2,{glow:[0.2,1,0.4],glowFull:true,noTex:true}),W/2-0.045,0.18,F+0.004,{rotX:Math.PI/2,seg:12});
      const bt=C(root,0.013,0.012,dk,W/2-0.045,0.145,F+0.006,{rotX:Math.PI/2,seg:18}); bt.trig=on; } },
