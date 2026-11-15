  mfu:{name:'МФУ лазерное',cat:'office',small:true,purpose:'Лазерное МФУ: принтер снизу, сканер с автоподатчиком сверху. Нажмите на крышку сканера — она поднимется, под ней стекло. Крышка автоподатчика открывается отдельно. Лоток бумаги снизу выдвигается, передняя крышка откидывается — внутри картридж. На сенсорном экране нажмите «Печать» — из принтера выедет лист.',
    specs:[['Габариты','420×390×400 мм'],['Печать','38 стр./мин, A4, 1200 dpi, двусторонняя'],['Сканер','600 dpi, автоподатчик на 50 листов'],['Лоток','250 листов'],['Экран','сенсорный 4,3"'],['Связь','Wi-Fi, Ethernet, USB']],materials:'Корпус — матовый ABS-пластик, стекло сканера — закалённое',
    variants:[{name:'Белый и графит',b:'#e7e7e4',a:'#3a3c40',t:'#d3d4d2'},{name:'Графит',b:'#45474c',a:'#222327',t:'#38393d'}],
    build(root,v){ const W=0.42,D=0.39,pl=TX.plastic(),body=mat(hex(v.b),0.35,{tex:pl,texMode:4,texScale:7}),acc=mat(hex(v.a),0.4,{tex:pl,texMode:4,texScale:7}),top=mat(hex(v.t),0.35,{tex:pl,texMode:4,texScale:7}),dark=mat(hex('#141518'),0.45,{noTex:true}),paper=mat(hex('#f7f7f4'),0.08,{noTex:true}),pg=mat(hex('#f4f4f0'),0.05,{tex:TX.pages(),texMode:4,texScale:40});
      for(const sx of [-1,1]) for(const sz of [-1,1]) C(root,0.012,0.008,dark,sx*(W/2-0.04),0.004,sz*(D/2-0.04),{seg:12});
      // корпус принтера
      RB(root,W,0.235,D,0.012,body,0,0.008+0.1175,0,{N:6}); for(let i=0;i<12;i++) P(root,0.002,0.004,0.14,dark,W/2+0.0005,0.06+i*0.011,0.04);
      // лоток бумаги
      const tr=G(root,0,0,0,{anim:anim('slideZ',0.2,'Лоток бумаги')}); tr.anim.rate=1.8; RB(tr,W-0.016,0.075,0.016,0.006,acc,0,0.05,D/2+0.002,{N:5}); P(tr,0.14,0.012,0.008,dark,0,0.07,D/2+0.009); P(tr,W-0.04,0.004,D-0.04,acc,0,0.016,0); P(tr,0.216,0.03,0.3,pg,0,0.034,0); for(const sx of [-1,1]) P(tr,0.006,0.035,0.2,acc,sx*0.115,0.036,0.02);
      // передняя крышка с картриджем внутри
      P(root,W-0.05,0.115,0.002,dark,0,0.158,D/2+0.001); P(root,0.3,0.07,0.003,mat(hex('#232428'),0.5,{noTex:true}),0,0.16,D/2+0.0022); P(root,0.07,0.016,0.002,mat(hex('#e46a1f'),0.5,{noTex:true}),0,0.185,D/2+0.0038);
      const fd=G(root,0,0.098,D/2+0.009,{anim:anim('rotX',1.25,'Передняя крышка')}); fd.anim.rate=1.8; RB(fd,W-0.03,0.13,0.014,0.006,body,0,0.065,0.0,{N:5}); P(fd,0.16,0.01,0.006,dark,0,0.115,0.008); P(fd,0.3,0.002,0.004,mat(hex(v.a),0.3,{noTex:true}),0,0.02,0.008);
      // выходной лоток между принтером и сканером
      P(root,W-0.06,0.04,0.004,dark,-0.02,0.262,-D/2+0.03); P(root,0.26,0.004,0.24,acc,-0.05,0.247,0.02,{rotX:-0.06}); P(root,0.04,0.04,D-0.02,body,W/2-0.02,0.263,0);
      const sc=mkCanvas(256,360),x=sc.getContext('2d'); x.fillStyle='#fbfbf8'; x.fillRect(0,0,256,360); x.fillStyle='#1d3f78'; x.font='700 17px "Golos Text",Arial'; x.fillText('Коммерческое предложение',16,34); x.fillStyle='#8a8d92'; for(let i=0;i<7;i++) x.fillRect(16,54+i*12,200-(i%3)*40,4);
      [60,90,72,120,104].forEach((h,i)=>{ x.fillStyle=['#e9a300','#3f6fb5','#2f8a5c','#c4572e','#7b5cc4'][i]; x.fillRect(30+i*42,300-h,28,h); }); x.fillStyle='#8a8d92'; x.fillRect(16,300,224,2); for(let i=0;i<3;i++) x.fillRect(16,318+i*11,170,3); const sk='mfuSheet'; if(!TEX[sk]) TEX[sk]=texFromCanvas(sc);
      const sh=G(root,-0.05,0.252,-0.17,{anim:anim('slideZ',0.25,'Печать')}); sh.anim.rate=0.8; sh.add(new Node({mesh:QUAD(0.21,0.297),mat:mat([1,1,1],0.1,{tex:sk}),pos:[0,0.0012,0],rotX:-Math.PI/2})); P(sh,0.21,0.0015,0.297,paper,0,0,0);
      // сканер: корпус, стекло, крышка с автоподатчиком
      RB(root,W,0.055,D-0.01,0.01,top,0,0.3075,-0.005,{N:6}); P(root,W-0.06,0.002,D-0.08,mat([0.14,0.2,0.26],1,{noTex:true}),-0.01,0.3355,0.0); P(root,0.025,0.002,D-0.08,dark,W/2-0.035,0.3355,0);
      const lid=G(root,0,0.336,-D/2+0.015,{anim:anim('rotX',-1.1,'Крышка сканера')}); lid.anim.rate=1.6; RB(lid,W,0.024,D-0.03,0.008,top,0,0.012,(D-0.03)/2,{N:5}); P(lid,W-0.04,0.0015,D-0.07,mat(hex('#f1f1ef'),0.15,{noTex:true}),0,-0.0005,(D-0.03)/2);
      RB(lid,0.1,0.055,D-0.05,0.012,top,-W/2+0.06,0.05,(D-0.03)/2,{N:5}); P(lid,0.25,0.004,0.26,acc,0.06,0.04,0.2,{rotX:-0.09}); P(lid,0.21,0.008,0.24,pg,0.06,0.047,0.21,{rotX:-0.09}); for(const sx of [-1,1]) P(lid,0.006,0.02,0.12,acc,0.06+sx*0.11,0.052,0.2);
      const adf=G(lid,-W/2+0.01,0.078,(D-0.03)/2,{anim:anim('rotZ',1.3,'Крышка автоподатчика')}); adf.anim.rate=1.8; RB(adf,0.1,0.012,D-0.05,0.005,acc,0.05,0.0,0); for(let i=0;i<3;i++) C(lid,0.012,0.08,mat(hex('#2a2b2e'),0.4,{noTex:true}),-W/2+0.06,0.052,0.06+i*0.12,{rotZ:Math.PI/2,seg:12});
      // сенсорная панель
      const pc=mkCanvas(512,288),y=pc.getContext('2d'),g=y.createLinearGradient(0,0,0,288); g.addColorStop(0,'#1e4a78'); g.addColorStop(1,'#0e2744'); y.fillStyle=g; y.fillRect(0,0,512,288); y.fillStyle='rgba(255,255,255,.85)'; y.font='600 20px "Golos Text",Arial'; y.fillText('12:40   Wi-Fi ●   Тонер 78%',18,32);
      [['Копия','#e9a300'],['Скан','#3fa0e0'],['Печать','#38b46a'],['Факс','#9a7be0'],['USB','#d0d3d8'],['Настройки','#8a8f98']].forEach(([t,c],i)=>{ const X=16+(i%3)*166,Y=56+Math.floor(i/3)*112; y.fillStyle=i===2?'rgba(56,180,106,.28)':'rgba(255,255,255,.09)'; rrect(y,X,Y,152,100,12); y.fill(); y.fillStyle=c; rrect(y,X+52,Y+14,48,42,8); y.fill(); y.fillStyle='#fff'; y.font='600 21px "Golos Text",Arial'; y.textAlign='center'; y.fillText(t,X+76,Y+86); y.textAlign='left'; });
      const pk='mfuScreen'; if(!TEX[pk]) TEX[pk]=texFromCanvas(pc);
      const pn=G(root,0.075,0.29,D/2-0.008,{rotX:-0.62}); RB(pn,0.24,0.012,0.15,0.008,dark,0,0,0,{N:5}); pn.add(new Node({mesh:QUAD(0.13,0.073),mat:mat([1,1,1],0.6,{emis:0.75,tex:pk}),pos:[-0.03,0.0064,0.0],rotX:-Math.PI/2}));
      const hb=P(pn,0.04,0.004,0.026,mat([1,1,1],0.1,{noTex:true}),0.0127,0.0062,-0.0096); hb.noDraw=true; hb.trig=sh;
      const st=G(pn,0,0,0,{anim:anim('glow',1,'Индикатор')}); C(st,0.004,0.003,mat([0.2,0.4,0.25],0.5,{glow:[0.3,1,0.5],glowFull:true,noTex:true}),0.085,0.007,0.05,{seg:10}); sh.anim.link=[st];
      const pw=C(pn,0.009,0.004,mat(hex('#2a2c31'),0.5,{noTex:true}),0.095,0.007,0.0,{seg:16}); C(pn,0.0095,0.0012,mat([0.2,0.5,0.9],0.5,{emis:0.8,noTex:true}),0.095,0.0095,0.0,{seg:16}); pw.trig=sh;
      P(root,0.014,0.006,0.002,dark,-W/2+0.05,0.31,D/2-0.009);
      const lc=mkCanvas(256,48),z=lc.getContext('2d'); z.fillStyle=v.b; z.fillRect(0,0,256,48); z.fillStyle=v.a; z.font='700 26px "Golos Text",Arial'; z.textAlign='center'; z.fillText('LaserPro M40',128,34); const lk='mfuLogo'+v.b; if(!TEX[lk]) TEX[lk]=texFromCanvas(lc);
      root.add(new Node({mesh:QUAD(0.1,0.019),mat:mat([1,1,1],0.3,{tex:lk}),pos:[-0.12,0.235,D/2+0.0005]})); } },
