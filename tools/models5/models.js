  coffee:{name:'Кофемашина рожковая',cat:'catering',small:true,purpose:'Профессиональная однопостовая кофемашина. Нажмите на холдер — он повернётся в группе. Кнопка с чашкой на панели запускает пролив: загорается подсветка группы и течёт кофе. Паровая трубка справа поворачивается, клавиша на боку включает подсветку чашек.',
    specs:[['Размер','360×450 мм'],['Высота','380 мм'],['Бойлер','2,5 л, 93 °C'],['Давление','9 бар'],['Мощность','1,6 кВт']],materials:'Корпус — шлифованная нержавейка, боковые панели — порошковая эмаль, ручка холдера — орех',
    variants:[{name:'Сталь и красный',s:'#b3262c'},{name:'Сталь и чёрный',s:'#1f2024'},{name:'Сталь и белый',s:'#ecebe7'},{name:'Сталь и мята',s:'#8fc4b3'}],
    build(root,v){ const W=0.36,D=0.45,H=0.38,st=mat(hex('#cfd2d6'),0.9,{tex:'brushed',texMode:4,texScale:5}),side=mat(hex(v.s),0.75,{noTex:true}),chrome=mat(hex('#eceff2'),1,{noTex:true}),blk=mat(hex('#16171a'),0.5,{noTex:true}),wood=mat([0.9,0.7,0.52],0.45,{tex:'walnut',texMode:4,texScale:7}),F=D/2-0.02;
      for(const sx of [-1,1]) for(const sz of [-1,1]) C(root,0.013,0.02,blk,sx*(W/2-0.035),0.01,sz*(D/2-0.045),{seg:16});
      RB(root,W-0.06,H-0.06,D-0.02,0.018,st,0,0.02+(H-0.06)/2,-0.01); for(const sx of [-1,1]) RB(root,0.032,H-0.04,D-0.01,0.012,side,sx*(W/2-0.016),0.02+(H-0.04)/2,-0.005);
      P(root,W-0.07,0.005,D-0.07,mat(hex('#c3c6ca'),0.9,{tex:TX.grate(),texMode:4,texScale:9}),0,H-0.017,-0.02);
      for(const sx of [-1,1]) TB(root,[[sx*(W/2-0.045),H-0.02,-D/2+0.04],[sx*(W/2-0.045),H+0.025,-D/2+0.06],[sx*(W/2-0.045),H+0.025,D/2-0.1],[sx*(W/2-0.045),H-0.02,D/2-0.08]],0.0042,chrome);
      const pc=mkCanvas(512,160),x=pc.getContext('2d'),gr=x.createLinearGradient(0,0,0,160); gr.addColorStop(0,'#232428'); gr.addColorStop(1,'#141517'); x.fillStyle=gr; x.fillRect(0,0,512,160); x.fillStyle='#090b0a'; rrect(x,166,26,180,78,10); x.fill(); x.fillStyle='#ffb43a'; x.font='700 46px "Courier New",monospace'; x.textAlign='center'; x.fillText('93°C',256,82);
      x.fillStyle='rgba(255,180,58,.6)'; x.font='600 15px Arial'; x.fillText('ДАВЛЕНИЕ 9.0 БАР',256,124); x.fillStyle='#c9a24a'; x.font='700 17px "Golos Text",Arial'; x.fillText('ЭСПРЕССО · ЛИНЕЯ',256,150);
      const lab=[['1 ЧАШКА',62],['2 ЧАШКИ',122],['ПАР',392],['ВОДА',452]]; lab.forEach(([t,X])=>{ x.fillStyle='#8f9297'; x.font='600 12px Arial'; x.fillText(t,X,112); }); const pk='coffeeP'; if(!TEX[pk]) TEX[pk]=texFromCanvas(pc);
      const PW=W-0.07,PH=0.095,PY=H-0.07; root.add(new Node({mesh:QUAD(PW,PH),mat:mat([1,1,1],0.5,{tex:pk}),pos:[0,PY,F+0.0012]}));
      const brew=G(root,0,0,0,{anim:anim('glow',1,'Эспрессо')}); brew.anim.rate=1.4;
      const bx=X=>-PW/2+X/512*PW,by=PY+PH/2-PH*66/160; const btn=[]; for(const [t,X] of lab){ const b=C(root,0.0115,0.008,mat(hex('#2b2d31'),0.6,{noTex:true}),bx(X),by,F+0.004,{rotX:Math.PI/2,seg:20}); C(root,0.0085,0.0015,mat(hex('#d9dadc'),0.9,{glow:[1,0.75,0.35],noTex:true}),bx(X),by,F+0.0085,{rotX:Math.PI/2,seg:16}); btn.push(b); }
      btn[0].trig=brew; btn[1].trig=brew; btn[3].trig=brew;
      // группа и холдер
      C(root,0.046,0.05,chrome,0,0.235,F+0.012,{seg:32}); C(root,0.05,0.008,chrome,0,0.264,F+0.012,{seg:32}); C(root,0.03,0.006,blk,0,0.208,F+0.012,{seg:24});
      const led=G(brew,0,0,0); C(led,0.049,0.004,mat([0.9,0.8,0.6],0.4,{glow:[1,0.78,0.42],glowFull:true,noTex:true}),0,0.212,F+0.012,{seg:32});
      const pf=G(root,0,0.19,F+0.012,{anim:anim('rotY',0.75,'Холдер')}); pf.anim.rate=2.6; C(pf,0.037,0.024,chrome,0,0,0,{seg:28}); C(pf,0.041,0.005,chrome,0,0.011,0,{seg:28}); for(const sx of [-1,1]) C(pf,0.005,0.014,chrome,sx*0.01,-0.018,0.005,{seg:10});
      TB(pf,[[0,0,0.034],[0,-0.004,0.06],[0,-0.012,0.085]],0.009,chrome,{seg:12}); TB(pf,[[0,-0.012,0.085],[0,-0.022,0.12],[0,-0.03,0.165],[0,-0.032,0.175]],0.0135,wood,{seg:14}); C(pf,0.0138,0.004,blk,0,-0.032,0.177,{rotX:Math.PI/2+0.25,seg:14});
      // пролив кофе
      const sf=G(root,0,0.172,F+0.017,{anim:anim('scaleY',1,'Пролив')}); sf.anim.rate=2.4; const cof=mat(hex('#5a3418'),0.6,{alpha:0.85,noTex:true}); for(const sx of [-1,1]) C(sf,0.0022,0.06,cof,sx*0.01,-0.03,0,{seg:8}); brew.anim.link=[sf];
      // поддон с решёткой и чашка
      RB(root,W-0.09,0.024,0.12,0.006,st,0,0.042,F+0.04); P(root,W-0.1,0.003,0.11,mat(hex('#2a2b2e'),0.9,{tex:TX.grate(),texMode:4,texScale:9}),0,0.0555,F+0.04);
      const cupM=mat(hex('#f4f2ec'),0.8,{noTex:true}); LT(root,'saucer',[[0,0],[0.04,0],[0.052,0.008],[0.054,0.011],[0.05,0.009],[0.02,0.004],[0,0.004]],cupM,0,0.057,F+0.035);
      LT(root,'ecup',[[0,0],[0.02,0],[0.022,0.004],[0.027,0.03],[0.0285,0.052],[0.0265,0.052],[0.0252,0.03],[0.02,0.008],[0,0.008]],cupM,0,0.061,F+0.035,{seg:28}); C(root,0.025,0.002,mat(hex('#a8743f'),0.7,{noTex:true}),0,0.104,F+0.035,{seg:24});
      TB(root,[[0.027,0.105,F+0.035],[0.042,0.105,F+0.035],[0.045,0.085,F+0.035],[0.027,0.075,F+0.035]],0.0035,cupM);
      // паровая трубка и ручка крана
      const sw=G(root,W/2-0.07,0.27,F+0.005,{anim:anim('rotY',0.9,'Паровая трубка')}); C(sw,0.009,0.02,chrome,0,0,0,{seg:14}); TB(sw,[[0,-0.008,0],[0,-0.01,0.02],[0,-0.03,0.04],[0,-0.16,0.05]],0.0048,chrome); C(sw,0.0035,0.012,chrome,0,-0.165,0.05,{seg:10});
      C(root,0.016,0.024,blk,W/2-0.07,0.31,F+0.012,{rotX:Math.PI/2,seg:20}); C(root,0.016,0.024,blk,-W/2+0.07,0.31,F+0.012,{rotX:Math.PI/2,seg:20});
      // подсветка чашек
      const lg=G(root,0,0,0,{anim:anim('glow',1,'Подсветка чашек')}); P(lg,W-0.11,0.004,0.006,mat([0.8,0.8,0.8],0.3,{glow:[1,0.93,0.82],glowFull:true,noTex:true}),0,0.165,F-0.002); root.cupLight=lg;
      const ks=P(root,0.006,0.026,0.014,blk,W/2+0.0005,0.09,F-0.06); ks.trig=lg; },
    lights:it=>{ const n=it.root.cupLight; return n?[{p:M4.pt(itemWorld(it),0,0.15,0.3),c:[1,0.92,0.8],pow:0.35,k:7,down:true,sh:false,on:ease(n.anim.t)}]:[]; } },
  cooler:{name:'Кулер для воды с бутылью',cat:'catering',purpose:'Напольный кулер с нагревом и охлаждением. Нажмите синий или красный кран — потечёт холодная или горячая вода, у горячей загорается индикатор. Сбоку держатель с бумажными стаканчиками.',
    specs:[['Размер','310×330 мм'],['Высота','1000 мм + бутыль 19 л'],['Нагрев','до 95 °C, 5 л/ч'],['Охлаждение','до 8 °C, 2 л/ч']],materials:'Корпус — ABS-пластик, бутыль — поликарбонат, краны — пищевой пластик',
    variants:[{name:'Белый',b:'#eeeeeb',f:'#d9dadb'},{name:'Серебристый',b:'#c9ccd0',f:'#2a2c30'},{name:'Чёрный',b:'#222326',f:'#141517'}],
    build(root,v){ const W=0.31,D=0.33,H=1.0,body=mat(hex(v.b),0.55,{noTex:true}),fr=mat(hex(v.f),0.5,{noTex:true}),dark=mat(hex('#18191b'),0.4,{noTex:true}),wat=mat([0.62,0.78,0.92],0.95,{alpha:0.5,noTex:true});
      RB(root,W,H-0.02,D,0.03,body,0,0.01+(H-0.02)/2,0); RB(root,W-0.06,0.3,0.02,0.01,dark,0,0.73,D/2-0.005); RB(root,W-0.07,0.012,0.08,0.004,fr,0,0.59,D/2+0.02); P(root,W-0.09,0.003,0.07,mat(hex('#9b9ea3'),0.8,{tex:TX.grate(),texMode:4,texScale:14}),0,0.597,D/2+0.02);
      RB(root,W-0.04,0.05,D-0.02,0.015,fr,0,H-0.02,0); C(root,0.06,0.03,dark,0,H+0.01,0,{seg:28});
      // бутыль
      const bm=mat([0.55,0.75,0.95],1,{alpha:0.32,noTex:true}),bw=mat([0.45,0.68,0.92],0.9,{alpha:0.28,noTex:true});
      LT(root,'bottle19',[[0.028,0],[0.03,0.025],[0.036,0.05],[0.08,0.09],[0.128,0.13],[0.136,0.16],[0.136,0.2],[0.131,0.21],[0.136,0.22],[0.136,0.33],[0.131,0.34],[0.136,0.35],[0.136,0.43],[0.125,0.47],[0.08,0.49],[0,0.495]],bm,0,H+0.02,0,{seg:40});
      LT(root,'water19',[[0.024,0],[0.032,0.05],[0.078,0.09],[0.126,0.13],[0.132,0.16],[0.132,0.38],[0,0.38]],bw,0,H+0.023,0,{seg:36});
      // краны и струи
      const mk=(sx,c,lab)=>{ const g=G(root,sx*0.06,0.8,D/2+0.008,{anim:anim('scaleY',1,lab)}); g.anim.rate=3; const L=0.17; C(g,0.0055,L,wat,0,-L/2,0,{seg:12}); C(g,0.03,0.003,wat,0,-L+0.002,0,{seg:18});
        const t=RB(root,0.034,0.04,0.045,0.008,mat(hex(c),0.6,{noTex:true}),sx*0.06,0.82,D/2+0.012); const n=C(root,0.007,0.016,mat(hex(c),0.6,{noTex:true}),sx*0.06,0.797,D/2+0.012,{seg:12}); t.trig=g; n.trig=g; return g; };
      mk(-1,'#2a63c9','Холодная вода'); const hot=mk(1,'#d23a2e','Горячая вода');
      const ld=G(root,0,0,0,{anim:anim('glow',1,'Нагрев')}); C(ld,0.005,0.004,mat([0.4,0.1,0.1],0.5,{glow:[1,0.25,0.18],glowFull:true,noTex:true}),0.025,0.9,D/2+0.002,{rotX:Math.PI/2,seg:12}); hot.anim.link=[ld];
      C(root,0.005,0.004,mat([0.2,0.6,0.3],0.5,{emis:0.9,noTex:true}),-0.025,0.9,D/2+0.002,{rotX:Math.PI/2,seg:12});
      const lc=mkCanvas(256,128),x=lc.getContext('2d'); x.fillStyle=v.f; x.fillRect(0,0,256,128); x.fillStyle='#5fa8ff'; x.beginPath(); x.moveTo(128,18); x.bezierCurveTo(150,50,160,66,150,84); x.arc(128,80,22,0.2,Math.PI-0.2); x.bezierCurveTo(96,66,106,50,128,18); x.fill(); x.fillStyle='#c9d6e6'; x.font='600 20px "Golos Text",Arial'; x.textAlign='center'; x.fillText('ЧИСТАЯ ВОДА',128,122); const lk='coolerL'+v.f; if(!TEX[lk]) TEX[lk]=texFromCanvas(lc);
      root.add(new Node({mesh:QUAD(0.13,0.065),mat:mat([1,1,1],0.4,{tex:lk}),pos:[0,0.45,D/2+0.001]}));
      // стаканчики
      C(root,0.04,0.3,mat([0.85,0.9,0.95],1,{alpha:0.22,noTex:true}),W/2+0.045,0.62,0,{seg:24}); P(root,0.03,0.02,0.02,fr,W/2+0.012,0.62,0); P(root,0.03,0.02,0.02,fr,W/2+0.012,0.4,0);
      const cm=mat(hex('#f6f5f1'),0.2,{noTex:true}); for(let i=0;i<9;i++) LT(root,'pcup',[[0,0],[0.026,0],[0.036,0.075],[0.034,0.075],[0.024,0.004],[0,0.004]],cm,W/2+0.045,0.48+i*0.014,0,{seg:24});
      LT(root,'pcup',[[0,0],[0.026,0],[0.036,0.075],[0.034,0.075],[0.024,0.004],[0,0.004]],cm,0.06,0.598,D/2+0.02,{seg:24}); } },
  mfu:{name:'МФУ лазерное',cat:'office',small:true,purpose:'Принтер, сканер и копир. Нажмите на крышку сканера — она поднимется, под ней стекло. Лоток бумаги снизу выдвигается. Зелёная кнопка «Печать» на панели — из принтера выезжает лист.',
    specs:[['Размер','490×450 мм'],['Высота','420 мм'],['Печать','40 стр./мин, A4'],['Сканер','600 dpi, автоподатчик 50 листов'],['Связь','Wi-Fi, Ethernet, USB']],materials:'Корпус — ABS-пластик, стекло сканера — закалённое',
    variants:[{name:'Белый',b:'#ebebe8',a:'#3a3c40'},{name:'Графит',b:'#3a3c40',a:'#1d1e21'}],
    build(root,v){ const W=0.49,D=0.45,H=0.42,body=mat(hex(v.b),0.45,{noTex:true}),acc=mat(hex(v.a),0.5,{noTex:true}),dark=mat(hex('#18191b'),0.4,{noTex:true}),paper=mat(hex('#f7f7f4'),0.1,{noTex:true});
      RB(root,W,0.14,D,0.012,body,0,0.07,0); RB(root,W,0.2,D-0.04,0.012,body,0,0.24,-0.02); P(root,W-0.02,0.075,0.015,dark,0,0.24,D/2-0.04); P(root,W-0.06,0.003,0.12,acc,0,0.205,D/2-0.08);
      const tr=G(root,0,0,0,{anim:anim('slideZ',0.24,'Лоток бумаги')}); RB(tr,W-0.03,0.1,0.02,0.006,acc,0,0.062,D/2+0.004); P(tr,W-0.06,0.006,D-0.06,acc,0,0.016,0); P(tr,0.215,0.045,0.3,mat(hex('#f2f2ee'),0.1,{tex:TX.pages(),texMode:4,texScale:30}),0,0.044,0);
      P(tr,0.12,0.012,0.006,dark,0,0.09,D/2+0.015);
      // выезжающий лист с распечаткой
      const sc=mkCanvas(256,360),x=sc.getContext('2d'); x.fillStyle='#fbfbf8'; x.fillRect(0,0,256,360); x.fillStyle='#1d3f78'; x.font='700 18px "Golos Text",Arial'; x.fillText('Коммерческое предложение',18,34); x.fillStyle='#8a8d92'; for(let i=0;i<7;i++) x.fillRect(18,54+i*12,200-(i%3)*40,4);
      const bars=[60,90,72,120,104]; bars.forEach((h,i)=>{ x.fillStyle=['#e9a300','#3f6fb5','#2f8a5c','#c4572e','#7b5cc4'][i]; x.fillRect(30+i*42,300-h,28,h); }); x.fillStyle='#8a8d92'; x.fillRect(18,300,220,2); for(let i=0;i<3;i++) x.fillRect(18,318+i*11,170,3); const sk='mfuSheet'; if(!TEX[sk]) TEX[sk]=texFromCanvas(sc);
      const sh=G(root,0,0.222,D/2-0.27,{anim:anim('slideZ',0.25,'Печать')}); sh.anim.rate=0.9; sh.add(new Node({mesh:QUAD(0.21,0.29),mat:mat([1,1,1],0.1,{tex:sk}),pos:[0,0.001,0],rotX:-Math.PI/2})); P(sh,0.21,0.0015,0.29,paper,0,0,0);
      // сканер и крышка
      P(root,W-0.06,0.002,D-0.12,mat([0.16,0.22,0.28],1,{noTex:true}),0,0.3415,-0.02);
      const lid=G(root,0,0.343,-D/2+0.02,{anim:anim('rotX',-1.15,'Крышка сканера')}); lid.anim.rate=1.8; RB(lid,W,0.03,D-0.06,0.01,body,0,0.015,(D-0.06)/2); P(lid,W-0.04,0.002,D-0.1,mat(hex('#f0f0ee'),0.2,{noTex:true}),0,-0.0005,(D-0.06)/2);
      RB(lid,W-0.12,0.05,0.2,0.01,body,-0.03,0.05,0.12); P(lid,W-0.16,0.004,0.19,acc,-0.03,0.077,0.12,{rotX:-0.12}); P(lid,0.2,0.004,0.17,paper,-0.03,0.082,0.13,{rotX:-0.12});
      // панель управления
      const pc=mkCanvas(512,256),y=pc.getContext('2d'); y.fillStyle='#16171a'; y.fillRect(0,0,512,256); const g=y.createLinearGradient(0,30,0,226); g.addColorStop(0,'#24476f'); g.addColorStop(1,'#122a45'); y.fillStyle=g; rrect(y,20,24,330,206,12); y.fill();
      [['Копия','#e9a300'],['Скан','#3fa0e0'],['Печать','#38b46a'],['Факс','#9a7be0']].forEach(([t,c],i)=>{ const X=40+(i%2)*155,Y=46+Math.floor(i/2)*92; y.fillStyle='rgba(255,255,255,.08)'; rrect(y,X,Y,140,80,10); y.fill(); y.fillStyle=c; y.beginPath(); y.arc(X+34,Y+40,16,0,7); y.fill(); y.fillStyle='#fff'; y.font='600 22px "Golos Text",Arial'; y.fillText(t,X+58,Y+48); });
      y.fillStyle='#2a2c31'; for(let i=0;i<9;i++){ y.beginPath(); y.arc(392+(i%3)*40,60+Math.floor(i/3)*44,15,0,7); y.fill(); } y.fillStyle='#38b46a'; y.beginPath(); y.arc(432,214,24,0,7); y.fill(); const pk='mfuPanel'; if(!TEX[pk]) TEX[pk]=texFromCanvas(pc);
      const pnl=G(root,0.1,0.322,D/2-0.045,{rotX:-0.55}); RB(pnl,0.25,0.016,0.13,0.006,dark,0,0,0); pnl.add(new Node({mesh:QUAD(0.24,0.12),mat:mat([1,1,1],0.4,{emis:0.55,tex:pk}),pos:[0,0.0085,0],rotX:-Math.PI/2}));
      const pb=C(pnl,0.011,0.006,mat(hex('#38b46a'),0.6,{glow:[0.4,1,0.6],noTex:true}),0.24*(432/512-0.5),0.011,0.12*(214/256-0.5),{seg:20}); pb.trig=sh;
      const st=G(root,0,0,0,{anim:anim('glow',1,'Индикатор')}); C(st,0.004,0.004,mat([0.2,0.4,0.25],0.5,{glow:[0.3,1,0.5],glowFull:true,noTex:true}),-W/2+0.04,0.3,D/2-0.028,{rotX:Math.PI/2,seg:10}); sh.anim.link=[st];
      for(let i=0;i<10;i++) P(root,0.004,0.06,0.03,dark,W/2+0.0005,0.2,-0.12+i*0.012); } },
  organizer:{name:'Органайзер настольный',cat:'office',small:true,purpose:'Стакан с ручками и карандашами, степлер и блок стикеров на подставке. Нажмите на степлер — он раскроется, на стикеры — верхний листок отогнётся.',
    specs:[['Размер','260×120 мм'],['Высота','150 мм']],materials:'Подставка — орех, стакан — металлическая сетка, степлер — сталь',
    variants:[{name:'Орех и чёрный',w:'walnut',m:'#1f2023'},{name:'Светлый дуб и белый',w:'oak_light',m:'#ecebe7'}],
    build(root,v){ const base=mat([1,1,1],0.35,{tex:v.w,texMode:4,texScale:8}),met=mat(hex(v.m),0.6,{noTex:true}),chrome=mat(hex('#e4e7ea'),1,{noTex:true});
      RB(root,0.26,0.018,0.12,0.005,base,0,0.009,0);
      LT(root,'pencup',[[0,0],[0.038,0],[0.04,0.003],[0.04,0.1],[0.037,0.1],[0.037,0.006],[0,0.006]],mat(hex(v.m),0.5,{tex:TX.grate(),texMode:1,texScale:1}),-0.08,0.018,0,{seg:30});
      const pens=[['#1f4fa8',0.13,0.12,-0.01,0.008],['#c8312c',0.12,-0.1,0.012,0.0],['#f0c419',0.11,0.04,0.12,0.01,6],['#1f2023',0.135,-0.05,-0.13,-0.008],['#2f8a5c',0.125,0.15,0.08,-0.012]];
      for(const [c,L,rx,rz,o,seg] of pens){ const g=G(root,-0.08+o,0.024,o*0.6,{rotX:rx,rotZ:rz}); C(g,0.0045,L,mat(hex(c),0.55,{noTex:true}),0,L/2,0,{seg:seg||12}); C(g,0.005,0.03,seg?mat(hex('#e7b9a1'),0.2,{noTex:true}):met,0,L-0.012,0,{seg:seg||12}); if(seg) C(g,0.002,0.012,mat(hex('#2a2a2a'),0.3,{noTex:true}),0,L+0.003,0,{seg:8}); else TB(g,[[0.005,L-0.004,0],[0.0065,L-0.03,0],[0.0065,L-0.045,0.0]],0.0012,chrome,{seg:6}); }
      // степлер
      RB(root,0.036,0.012,0.13,0.005,met,0.035,0.024,0); const sp=G(root,0.035,0.032,-0.055,{anim:anim('rotX',-0.6,'Степлер')}); sp.anim.rate=3; RB(sp,0.03,0.016,0.13,0.006,chrome,0,0.009,0.058); RB(sp,0.034,0.008,0.07,0.004,met,0,0.019,0.075); C(root,0.008,0.024,chrome,0.035,0.03,-0.058,{rotZ:Math.PI/2,seg:12});
      // стикеры
      P(root,0.075,0.035,0.075,mat(hex('#f7e15a'),0.2,{tex:TX.pages(),texMode:4,texScale:60}),0.105,0.0355,0);
      const nc=mkCanvas(256,256),x=nc.getContext('2d'); x.fillStyle='#fbe874'; x.fillRect(0,0,256,256); x.fillStyle='#1d3f78'; x.font='italic 34px "Segoe Print","Comic Sans MS",cursive'; x.fillText('Позвонить',24,96); x.fillText('заказчику!',30,150); x.strokeStyle='#c8312c'; x.lineWidth=4; x.beginPath(); x.moveTo(30,176); x.quadraticCurveTo(130,196,220,170); x.stroke(); const nk='stickyNote'; if(!TEX[nk]) TEX[nk]=texFromCanvas(nc);
      const nt=G(root,0.105,0.054,-0.0375,{anim:anim('rotX',-0.75,'Стикер')}); nt.anim.rate=2.6; nt.add(new Node({mesh:QUAD(0.075,0.075),mat:mat([1,1,1],0.15,{tex:nk}),pos:[0,0.0011,0.0375],rotX:-Math.PI/2})); P(nt,0.075,0.001,0.075,mat(hex('#f5df5a'),0.15,{noTex:true}),0,0,0.0375); } },
  mixer:{name:'Миксер планетарный',cat:'production',small:true,purpose:'Настольный планетарный миксер 7 л. Нажмите на головку — она откинется назад. Рычаг скорости сбоку включает вращение венчика.',
    specs:[['Размер','240×360 мм'],['Высота','420 мм'],['Дежа','7 л, нержавейка'],['Скорости','10, мощность 800 Вт']],materials:'Корпус — литой алюминий с эмалью, дежа и венчик — нержавейка',
    variants:[{name:'Красный',c:'#b82a2e'},{name:'Кремовый',c:'#efe4cf'},{name:'Графит',c:'#2f3135'},{name:'Мятный',c:'#9fd1c0'}],
    build(root,v){ const body=mat(hex(v.c),0.85,{noTex:true}),chrome=mat(hex('#e9ecef'),1,{noTex:true}),st=mat(hex('#cfd2d6'),0.95,{tex:'brushed',texMode:4,texScale:6}),blk=mat(hex('#1a1b1d'),0.5,{noTex:true});
      RB(root,0.23,0.04,0.34,0.016,body,0,0.02,0,{bulge:[0,0.2,0]}); for(const sx of [-1,1]) for(const sz of [-1,1]) C(root,0.012,0.006,blk,sx*0.085,0.003,sz*0.13,{seg:12});
      RB(root,0.13,0.3,0.12,0.04,body,0,0.19,-0.11); C(root,0.02,0.02,chrome,0,0.3,-0.047,{rotX:Math.PI/2,seg:16});
      const bowl=G(root,0,0.042,0.05); LT(bowl,'mixbowl',[[0,0],[0.055,0],[0.072,0.012],[0.1,0.05],[0.112,0.135],[0.118,0.142],[0.114,0.146],[0.108,0.136],[0.096,0.052],[0.069,0.016],[0,0.014]],st,0,0,0,{seg:40}); C(bowl,0.07,0.008,chrome,0,0.004,0,{seg:28});
      for(const sx of [-1,1]) TB(bowl,[[sx*0.106,0.11,0],[sx*0.135,0.105,0],[sx*0.138,0.07,0],[sx*0.1,0.055,0]],0.0055,st);
      const head=G(root,0,0.345,-0.13,{anim:anim('rotX',-0.62,'Головка')}); head.anim.rate=1.6; RB(head,0.135,0.105,0.33,0.05,body,0,0.0,0.14,{bulge:[0.1,0.25,0]}); C(head,0.042,0.02,chrome,0,0,0.31,{rotX:Math.PI/2,seg:28}); P(head,0.137,0.016,0.2,chrome,0,0.0,0.1);
      const wh=G(head,0,-0.055,0.19,{anim:anim('spin',16,'Венчик')}); wh.anim.rate=1.4; C(wh,0.011,0.03,chrome,0,0,0,{seg:14}); C(wh,0.016,0.008,chrome,0,-0.018,0,{seg:14});
      for(let k=0;k<4;k++){ const a=k*Math.PI/4,pts=[]; for(let i=0;i<=32;i++){ const ph=i/32*Math.PI*2,r=0.05*Math.sin(ph)*(0.3+0.7*(1-Math.cos(ph))/2),yy=-0.096+0.074*Math.cos(ph); pts.push([r*Math.cos(a),yy,r*Math.sin(a)]); } TB(wh,pts,0.0016,chrome,{seg:6}); }
      const lv=G(root,0.067,0.27,-0.1,{anim:anim('rotX',-0.5,'Скорость')}); lv.anim.rate=3; P(lv,0.008,0.012,0.06,chrome,0,0,0.03); C(lv,0.008,0.014,blk,0,0,0.062,{rotZ:Math.PI/2,seg:12}); lv.anim.link=[wh];
      const bc=mkCanvas(256,64),x=bc.getContext('2d'); x.fillStyle=v.c; x.fillRect(0,0,256,64); x.fillStyle='rgba(255,255,255,.85)'; x.font='italic 700 34px Georgia,serif'; x.textAlign='center'; x.fillText('Baker·Pro',128,44); const bk='mixLogo'+v.c; if(!TEX[bk]) TEX[bk]=texFromCanvas(bc);
      for(const sx of [-1,1]){ head.add(new Node({mesh:QUAD(0.11,0.028),mat:mat([1,1,1],0.6,{tex:bk}),pos:[sx*0.0685,0.015,0.14],rotY:sx*Math.PI/2})); } } },
  doughmix:{name:'Тестомес спиральный',cat:'production',purpose:'Спиральный тестомес на 40 л теста. Нажмите на защитную решётку — она поднимется. Зелёная кнопка на панели запускает вращение дежи и спирали, на табло идёт таймер.',
    specs:[['Размер','520×850 мм'],['Высота','1150 мм'],['Дежа','42 л, до 17 кг теста'],['Скорости','2, мощность 2,2 кВт'],['Напряжение','380 В']],materials:'Корпус — сталь с порошковой эмалью, дежа, спираль и решётка — нержавеющая сталь AISI 304',
    variants:[{name:'Белый',c:'#ecebe7'},{name:'Серый металлик',c:'#9ba0a6'},{name:'Красный',c:'#b3262c'}],
    build(root,v){ const body=mat(hex(v.c),0.6,{noTex:true}),st=mat(hex('#d2d5d9'),0.95,{tex:'brushed',texMode:4,texScale:4}),chrome=mat(hex('#e6e9ec'),1,{noTex:true}),blk=mat(hex('#1a1b1d'),0.5,{noTex:true}),W=0.52,D=0.85;
      RB(root,W,0.72,D,0.03,body,0,0.38,0); for(const sx of [-1,1]) for(const sz of [-1,1]) C(root,0.03,0.025,blk,sx*(W/2-0.06),0.0125,sz*(D/2-0.07),{seg:16});
      for(let i=0;i<8;i++) P(root,0.006,0.012,0.3,mat(hex('#2a2b2e'),0.3,{noTex:true}),W/2+0.0005,0.18+i*0.03,-0.15);
      RB(root,0.32,0.46,0.26,0.03,body,0,0.97,-0.27); RB(root,0.3,0.16,0.48,0.04,body,0,1.12,-0.07);
      const bg=G(root,0,0.74,0.13,{anim:anim('spin',2.2,'Дежа')}); bg.anim.rate=0.9;
      LT(bg,'dbowl',[[0,0],[0.18,0],[0.22,0.02],[0.245,0.06],[0.25,0.29],[0.262,0.3],[0.262,0.31],[0.244,0.3],[0.24,0.065],[0.215,0.03],[0.18,0.016],[0,0.016]],st,0,0,0,{seg:48}); C(bg,0.2,0.04,mat(hex('#e9dcc2'),0.15,{tex:TX.linen(),texMode:4,texScale:8}),0,0.04,0,{seg:40});
      const hk=G(root,0.05,1.04,0.1,{anim:anim('spin',7,'Спираль')}); hk.anim.rate=0.9; C(hk,0.018,0.05,chrome,0,0.0,0,{seg:16}); const sp=[]; for(let i=0;i<=48;i++){ const t=i/48,a=t*Math.PI*2.4,r=0.025+0.05*t; sp.push([Math.cos(a)*r,-0.02-t*0.24,Math.sin(a)*r]); } TB(hk,sp,0.011,chrome,{seg:10});
      C(root,0.012,0.22,chrome,-0.08,0.92,0.14,{seg:14}); bg.anim.link=[hk];
      // защитная решётка
      const gr=G(root,0,1.06,0.13-0.27,{anim:anim('rotX',-1.15,'Защитная решётка')}); gr.anim.rate=1.4; const rg=r=>{ const p=[]; for(let i=0;i<=40;i++){ const a=i/40*Math.PI*2; p.push([Math.cos(a)*r,0,0.27+Math.sin(a)*r]); } return p; };
      for(const r of [0.262,0.19,0.11]) TB(gr,rg(r),0.005,st,{seg:6}); for(let k=0;k<10;k++){ const a=k/10*Math.PI*2; TB(gr,[[Math.cos(a)*0.06,0,0.27+Math.sin(a)*0.06],[Math.cos(a)*0.262,0,0.27+Math.sin(a)*0.262]],0.004,st,{seg:6}); } P(gr,0.06,0.012,0.04,st,0,0,0.01);
      // панель управления
      const pc=mkCanvas(512,256),x=pc.getContext('2d'); x.fillStyle='#dfe1e3'; x.fillRect(0,0,512,256); x.fillStyle='#0a0d0b'; rrect(x,150,40,212,90,10); x.fill(); x.fillStyle='#ff5a3a'; x.font='700 60px "Courier New",monospace'; x.textAlign='center'; x.fillText('06:00',256,106);
      x.fillStyle='#2f9a58'; x.beginPath(); x.arc(78,86,40,0,7); x.fill(); x.fillStyle='#c62b2b'; x.beginPath(); x.arc(434,86,40,0,7); x.fill(); x.fillStyle='#fff'; x.font='700 22px Arial'; x.fillText('ПУСК',78,94); x.fillText('СТОП',434,94);
      x.fillStyle='#4a4d52'; x.font='600 22px "Golos Text",Arial'; x.fillText('I СКОРОСТЬ    II СКОРОСТЬ',256,188); x.fillText('ТАЙМЕР',256,232); const pk='doughP'; if(!TEX[pk]) TEX[pk]=texFromCanvas(pc);
      root.add(new Node({mesh:QUAD(0.28,0.14),mat:mat([1,1,1],0.4,{tex:pk}),pos:[0,1.12,0.172]}));
      const b1=C(root,0.021,0.014,mat(hex('#2f9a58'),0.6,{glow:[0.4,1,0.6],noTex:true}),-0.28*(0.5-78/512),1.12+0.14*(0.5-86/256),0.175,{rotX:Math.PI/2,seg:20}); b1.trig=bg; const b2=C(root,0.021,0.014,mat(hex('#c62b2b'),0.6,{noTex:true}),0.28*(434/512-0.5),1.12+0.14*(0.5-86/256),0.175,{rotX:Math.PI/2,seg:20}); b2.trig=bg; } },
  torsher:{name:'Торшер с тканевым абажуром',cat:'light',purpose:'Напольный светильник с льняным абажуром и мраморным основанием. Нажмите ножную кнопку на проводе или сам абажур — свет включится тёплым тоном.',
    specs:[['Высота','1600 мм'],['Абажур','Ø 460 мм, лён'],['Лампа','E27, LED 12 Вт, 2700 K'],['Основание','мрамор Ø 300 мм']],materials:'Основание — мрамор, стойка — латунь, абажур — натуральный лён',
    variants:[{name:'Латунь, бежевый лён',p:'#c9a25a',s:'#ece2cf'},{name:'Чёрный, серый лён',p:'#1f2023',s:'#c9c7c2'},{name:'Латунь, терракота',p:'#c9a25a',s:'#c97b5a'}],
    build(root,v){ const brass=mat(hex(v.p),0.9,{noTex:true}),mar=mat([1,1,1],0.6,{tex:TX.marble(),texMode:1}),blk=mat(hex('#1a1b1d'),0.4,{noTex:true});
      LT(root,'tbase',[[0,0],[0.148,0],[0.15,0.004],[0.15,0.022],[0.142,0.03],[0,0.03]],mar,0,0,0,{seg:48}); C(root,0.025,0.03,brass,0,0.045,0,{seg:20});
      C(root,0.011,1.32,brass,0,0.06+0.66,0,{seg:16}); C(root,0.016,0.03,brass,0,0.7,0,{seg:16}); C(root,0.02,0.05,brass,0,1.36,0,{seg:18});
      TB(root,[[0.02,0.012,0.0],[0.12,0.004,0.06],[0.28,0.004,0.18],[0.4,0.004,0.22]],0.003,blk); const fs=C(root,0.024,0.016,blk,0.42,0.008,0.22,{seg:18});
      const lg=G(root,0,0,0,{anim:anim('glow',1,'Свет')}); lg.anim.rate=2.6; root.lampSw=lg; fs.trig=lg;
      const sm=mat(hex(v.s),0.08,{tex:TX.linen(),texMode:1,glow:hex(v.s).map(c=>Math.min(1,c*1.15+0.1))});
      const sh=LT(lg,'shade46',[[0.23,0],[0.175,0.28],[0.172,0.28],[0.226,0.002]],sm,0,1.3,0,{seg:48}); sh.trig=lg;
      LT(lg,'srim',[[0.231,-0.002],[0.231,0.004]],brass,0,1.3,0,{seg:48}); for(let k=0;k<3;k++){ const a=k/3*Math.PI*2; TB(lg,[[0,1.4,0],[Math.cos(a)*0.17,1.565,Math.sin(a)*0.17]],0.0025,brass,{seg:6}); }
      SPHn(lg,0.045,mat([0.9,0.88,0.8],0.3,{glow:[1,0.86,0.62],glowFull:true,noTex:true}),0,1.43,0); },
    lights:it=>{ const n=it.root.lampSw; return n?[{p:M4.pt(itemWorld(it),0,1.4,0),c:[1,0.8,0.56],pow:1.9,k:0.3,down:false,sh:false,on:ease(n.anim.t)}]:[]; } },
  monstera:{name:'Монстера в бетонном кашпо',cat:'office',purpose:'Живое растение с резными листьями. Нажмите на листья — растение покачнётся, как от сквозняка.',
    specs:[['Высота','1200 мм'],['Кашпо','Ø 400 мм, высота 380 мм'],['Уход','полив раз в неделю, рассеянный свет']],materials:'Кашпо — архитектурный бетон, грунт с дренажом',
    variants:[{name:'Серый бетон',c:[1,1,1]},{name:'Графитовый бетон',c:[0.55,0.55,0.57]},{name:'Белый бетон',c:[1.18,1.17,1.14]}],
    build(root,v){ const pot=mat(v.c,0.15,{tex:TX.concrete(),texMode:1}),leaf=mat([1,1,1],0.55,{tex:TX.leafMon(),texMode:1}),stem=mat(hex('#4a7a3a'),0.4,{noTex:true});
      LT(root,'mpot',[[0,0],[0.15,0],[0.165,0.01],[0.2,0.36],[0.205,0.38],[0.19,0.38],[0.186,0.36],[0,0.36]],pot,0,0,0,{seg:44}); C(root,0.186,0.012,mat([1,1,1],0.05,{tex:TX.soil(),texMode:2,texScale:6}),0,0.36,0,{seg:40});
      const sw=G(root,0,0,0,{anim:anim('sway',0.05,'Листья')}); sw.anim.rate=0.6; sw.anim.speed=2.2; const r=rnd(7);
      const L=[[0.2,0.95,0.55,0.48,-0.55],[1.3,0.75,0.5,0.44,-0.4],[2.4,1.05,0.6,0.52,-0.7],[3.4,0.7,0.45,0.4,-0.35],[4.3,0.88,0.56,0.47,-0.5],[5.3,0.62,0.4,0.36,-0.25],[0.85,0.55,0.32,0.3,-0.15],[2.9,0.5,0.3,0.28,-0.1]];
      L.forEach(([a,h,len,w,tilt],i)=>{ const d=[Math.sin(a),Math.cos(a)],R=0.1+len*0.25,b=[d[0]*0.03,0.36,d[1]*0.03],e=[d[0]*R,0.36+h*0.75,d[1]*R];
        TB(sw,[b,[d[0]*R*0.25,0.36+h*0.4,d[1]*R*0.25],[d[0]*R*0.7,0.36+h*0.68,d[1]*R*0.7],e],0.0075,stem,{seg:7});
        sw.add(new Node({mesh:makeMesh(leafGeom(monsteraOutline(30+i),w,len,0.3,0.1)),mat:leaf,pos:[e[0]-d[0]*len*0.12,e[1]+0.01,e[2]-d[1]*len*0.12],rotY:a,rotX:tilt+(r()-0.5)*0.2})); });
      root.leafPick=sw; } },
  sansev:{name:'Сансевиерия в кашпо',cat:'office',purpose:'Неприхотливое растение с плотными полосатыми листьями — хорошо смотрится у входа и в переговорной. Нажмите на листья — они чуть качнутся.',
    specs:[['Высота','850 мм'],['Кашпо','Ø 250 мм, высота 340 мм'],['Уход','полив раз в 2–3 недели']],materials:'Кашпо — бетон, грунт для суккулентов',
    variants:[{name:'Графитовый бетон',c:[0.5,0.5,0.52]},{name:'Серый бетон',c:[1,1,1]},{name:'Терракота',c:[1.25,0.78,0.6]}],
    build(root,v){ const pot=mat(v.c,0.15,{tex:TX.concrete(),texMode:1}),lm=mat([1,1,1],0.6,{tex:TX.sansev(),texMode:1});
      LT(root,'spot',[[0,0],[0.11,0],[0.12,0.01],[0.12,0.33],[0.126,0.34],[0.112,0.34],[0.108,0.33],[0,0.33]],pot,0,0,0,{seg:40}); C(root,0.108,0.01,mat([1,1,1],0.05,{tex:TX.soil(),texMode:2,texScale:6}),0,0.33,0,{seg:32});
      const sw=G(root,0,0,0,{anim:anim('sway',0.035,'Листья')}); sw.anim.rate=0.6; sw.anim.speed=1.8; const r=rnd(21),O=[[0,1],[0.22,0.88],[0.42,0.62],[0.5,0.35],[0.46,0.12],[0.34,0],[-0.34,0],[-0.46,0.12],[-0.5,0.35],[-0.42,0.62],[-0.22,0.88]];
      for(let i=0;i<11;i++){ const a=i*2.4+r()*0.5,rr=0.02+r()*0.05,len=0.4+r()*0.36,w=0.055+r()*0.025; sw.add(new Node({mesh:makeMesh(leafGeom(O,w,len,-0.04+r()*0.06,0.3,(r()-0.5)*0.8)),mat:lm,pos:[Math.sin(a)*rr,0.33,Math.cos(a)*rr],rotY:a+Math.PI/2*(r()<0.5?1:-1)*0.3,rotX:-Math.PI/2+(0.06+r()*0.2)})); }
      root.leafPick=sw; } },
  book:{name:'Книга',cat:'office',small:true,purpose:'Книга в тканевом переплёте с тиснением. Нажмите — обложка откроется, видна первая страница.',
    specs:[['Формат','170×240 мм'],['Толщина','35 мм']],materials:'Переплёт — ткань с золотым тиснением, бумага офсетная',
    variants:[{name:'Синяя «Интерьер»',c:'#24427a',t:['ДИЗАЙН','ИНТЕРЬЕРА']},{name:'Зелёная «Ботаника»',c:'#2f5a3c',t:['БОТАНИКА','ОФИСА']},{name:'Бордовая «Архитектура»',c:'#7a2430',t:['АРХИТЕКТУРА','ПРОСТРАНСТВА']},{name:'Охра «Свет»',c:'#b07a2a',t:['СВЕТ','И ЦВЕТ']}],
    build(root,v){ const W=0.17,D=0.24,T=0.035,cl=mat(hex(v.c),0.25,{tex:TX.cloth(),texMode:4,texScale:20}),pg=mat(hex('#f2ede1'),0.08,{tex:TX.pages(),texMode:4,texScale:40});
      P(root,W,0.003,D,cl,0,0.0015,0); P(root,W-0.008,T-0.006,D-0.008,pg,0.002,T/2,0); RB(root,0.012,T,D,0.004,cl,-W/2+0.004,T/2,0);
      const cc=mkCanvas(340,480),x=cc.getContext('2d'); x.fillStyle=v.c; x.fillRect(0,0,340,480); const sp=rnd(3); for(let i=0;i<3000;i++){ x.fillStyle=`rgba(${sp()<0.5?0:255},${sp()<0.5?0:255},${sp()<0.5?0:255},0.05)`; x.fillRect(sp()*340,sp()*480,2,2); }
      x.strokeStyle='#d8b45a'; x.lineWidth=3; x.strokeRect(22,22,296,436); x.lineWidth=1; x.strokeRect(30,30,280,420); x.fillStyle='#e2c06a'; x.textAlign='center'; x.font='700 34px Georgia,serif'; x.fillText(v.t[0],170,190); x.font='600 26px Georgia,serif'; x.fillText(v.t[1],170,232); x.font='22px Georgia,serif'; x.fillText('❦',170,290); x.font='italic 18px Georgia,serif'; x.fillText('Шоурум · 2026',170,420);
      const ck='bookC'+v.c; if(!TEX[ck]) TEX[ck]=texFromCanvas(cc);
      const pc=mkCanvas(340,480),y=pc.getContext('2d'); y.fillStyle='#f6f1e4'; y.fillRect(0,0,340,480); y.fillStyle='#2a2a2a'; y.textAlign='center'; y.font='700 24px Georgia,serif'; y.fillText(v.t[0]+' '+v.t[1],170,120); y.fillStyle='#8a857a'; for(let i=0;i<14;i++) y.fillRect(50,170+i*18,240-(i%4)*30,4); const pk='bookP'; if(!TEX[pk]) TEX[pk]=texFromCanvas(pc);
      root.add(new Node({mesh:QUAD(W-0.012,D-0.012),mat:mat([1,1,1],0.05,{tex:pk}),pos:[0.004,T-0.0055,0],rotX:-Math.PI/2}));
      const cv=G(root,-W/2+0.002,T-0.0015,0,{anim:anim('rotZ',2.9,'Открыть книгу')}); cv.anim.rate=1.6; P(cv,W,0.003,D,cl,W/2,0,0); cv.add(new Node({mesh:QUAD(W-0.004,D-0.004),mat:mat([1,1,1],0.3,{tex:ck}),pos:[W/2,0.0016,0],rotX:-Math.PI/2}));
      cv.add(new Node({mesh:QUAD(W-0.004,D-0.004),mat:mat(hex('#e9dcc0'),0.1,{noTex:true}),pos:[W/2,-0.0016,0],rotX:Math.PI/2})); } },
  candle:{name:'Свеча',cat:'office',small:true,purpose:'Свеча из соевого воска. Нажмите — фитиль загорится, пламя мягко колышется и подсвечивает стол.',
    specs:[['Размер','Ø 72 мм'],['Высота','120 мм'],['Время горения','до 40 часов']],materials:'Соевый воск, хлопковый фитиль; стакан — янтарное стекло',
    variants:[{name:'Столбик, молочная',c:'#f1ead8',g:0},{name:'В янтарном стакане',c:'#efe3c7',g:1},{name:'Столбик, графит',c:'#3b3c40',g:0}],
    build(root,v){ const wx=mat(hex(v.c),0.25,{tex:TX.wax(),texMode:1,glow:hex(v.c).map(c=>Math.min(1,c+0.1))}),H=v.g?0.085:0.12,R=v.g?0.03:0.036;
      const fl=G(root,0,0,0,{anim:anim('glow',1,'Свеча')}); fl.anim.rate=2; root.lampSw=fl;
      const body=LT(fl,'candle'+v.g,[[0,0],[R,0],[R+0.001,0.003],[R+0.001,H-0.004],[R-0.002,H],[R-0.008,H-0.006],[0.006,H-0.009],[0,H-0.009]],wx,0,v.g?0.006:0,0,{seg:36}); body.trig=fl;
      const y0=(v.g?0.006:0)+H-0.009; C(root,0.0012,0.012,mat(hex('#1b1b1b'),0.2,{noTex:true}),0,y0+0.005,0,{seg:6});
      const fz=G(fl,0,y0+0.012,0,{anim:anim('sway',0.12,'Пламя')}); fz.anim.speed=11; fl.anim.link=[fz];
      fz.add(new Node({mesh:SPH(1),mat:mat([0.95,0.6,0.2],0.2,{glow:[1,0.78,0.38],glowFull:true,noTex:true}),pos:[0,0.012,0],scl:[0.0062,0.017,0.0062]})); fz.add(new Node({mesh:SPH(1),mat:mat([0.5,0.6,0.9],0.2,{glow:[0.75,0.85,1],glowFull:true,noTex:true}),pos:[0,0.004,0],scl:[0.003,0.005,0.003]}));
      if(v.g){ LT(root,'cjar',[[0,0],[0.036,0],[0.038,0.004],[0.038,0.105],[0.035,0.105],[0.035,0.006],[0,0.006]],mat([0.85,0.55,0.2],1,{alpha:0.45,noTex:true}),0,0,0,{seg:36}); } },
    lights:it=>{ const n=it.root.lampSw; return n?[{p:M4.pt(itemWorld(it),0,0.16,0),c:[1,0.68,0.36],pow:0.42,k:6,down:false,sh:false,on:ease(n.anim.t)}]:[]; } },
  vase:{name:'Ваза керамическая',cat:'office',small:true,purpose:'Керамическая ваза ручной работы с глазурью. В высоких — сухие колосья пампасной травы: нажмите, они качнутся. Круглую можно повернуть.',
    specs:[['Высота','220–320 мм'],['Диаметр','140–180 мм']],materials:'Керамика с реактивной глазурью, сухоцветы',
    variants:[{name:'Терракота, амфора',c:'#b5643c',s:0},{name:'Молочная, шар',c:'#efede6',s:1},{name:'Графит, цилиндр',c:'#3a3b3f',s:2},{name:'Шалфей, бутыль',c:'#8fa58c',s:3}],
    build(root,v){ const gm=mat(hex(v.c),0.75,{tex:TX.glaze(),texMode:1});
      const S=[[[0,0],[0.045,0],[0.06,0.02],[0.085,0.09],[0.082,0.16],[0.05,0.24],[0.04,0.28],[0.05,0.31],[0.046,0.312],[0.036,0.28],[0.04,0.25],[0,0.25]],
        [[0,0],[0.04,0],[0.07,0.02],[0.09,0.08],[0.088,0.13],[0.06,0.18],[0.035,0.195],[0.038,0.205],[0.033,0.205],[0.03,0.19],[0,0.19]],
        [[0,0],[0.07,0],[0.072,0.004],[0.072,0.22],[0.066,0.224],[0.064,0.22],[0.064,0.01],[0,0.01]],
        [[0,0],[0.06,0],[0.066,0.012],[0.068,0.15],[0.05,0.2],[0.022,0.25],[0.02,0.3],[0.024,0.306],[0.018,0.306],[0.016,0.25],[0,0.24]]][v.s];
      const top=S.reduce((a,p)=>Math.max(a,p[1]),0); const rot=G(root,0,0,0,{anim:anim('rotY',Math.PI,'Повернуть')}); LT(rot,'vase'+v.s,S,gm,0,0,0,{seg:44});
      if(v.s!==1){ const sw=G(root,0,0,0,{anim:anim('sway',0.08,'Колосья')}); sw.anim.speed=2; const r=rnd(5+v.s),stem=mat(hex('#bfa77e'),0.2,{noTex:true}),fl=mat(hex('#ece2cc'),0.1,{tex:TX.linen(),texMode:1});
        for(let i=0;i<7;i++){ const a=i*0.9+r(),tilt=0.12+r()*0.22,L=0.35+r()*0.25,b=[Math.cos(a)*0.008,top-0.06,Math.sin(a)*0.008],e=[Math.cos(a)*L*tilt*1.6,top-0.06+L,Math.sin(a)*L*tilt*1.6]; TB(sw,[b,[(b[0]+e[0])*0.45,(b[1]+e[1])/2,(b[2]+e[2])*0.45],e],0.0018,stem,{seg:5});
          sw.add(new Node({mesh:makeMesh(leafGeom([[0,1],[0.35,0.75],[0.5,0.4],[0.4,0.1],[0,0],[-0.4,0.1],[-0.5,0.4],[-0.35,0.75]],0.035,0.13,0.08,0.4)),mat:fl,pos:e,rotY:a,rotX:-1.2+tilt})); } }
      else rot.trig=rot; } },
  reception:{name:'Стойка ресепшн с логотипом',cat:'office',purpose:'Стойка администратора: высокая столешница из кварца, фасад из дубовых реек и световой логотип. Нажмите на логотип или кнопку за стойкой — включится подсветка. Ящик тумбы выдвигается со стороны сотрудника.',
    specs:[['Размер','2200×750 мм'],['Высота','1080 / 740 мм'],['Подсветка','LED 3000 K, логотип — световой короб']],materials:'Фасад — рейки дуба на чёрном основании, столешница — кварцевый агломерат, каркас — ЛДСП',
    variants:[{name:'Дуб и белый кварц',w:'oak_teco',t:'#efeeea'},{name:'Орех и графит',w:'walnut',t:'#3b3c40'},{name:'Светлый дуб и бежевый',w:'oak_light',t:'#e7dfd0'}],
    build(root,v){ const W=2.2,D=0.75,H=1.08,wood=mat([1,1,1],0.35,{tex:v.w,texMode:4,texScale:2.4}),back=mat(hex('#1d1e21'),0.3,{noTex:true}),top=mat(hex(v.t),0.75,{tex:TX.marble(),texMode:4,texScale:0.9}),wh=mat(hex(v.t),0.4,{noTex:true}),F=D/2-0.04;
      P(root,W,H-0.06,0.02,back,0,(H-0.06)/2,F); for(const sx of [-1,1]) RB(root,0.05,H-0.04,D-0.04,0.008,wh,sx*(W/2-0.025),(H-0.04)/2,-0.02);
      const n=Math.floor((W-0.1)/0.046); for(let i=0;i<n;i++) RB(root,0.03,H-0.08,0.022,0.004,wood,-W/2+0.05+0.023+i*(W-0.1)/n,(H-0.08)/2+0.02,F+0.021,{N:4});
      RB(root,W+0.04,0.035,0.34,0.008,top,0,H-0.0175,F-0.11); P(root,W-0.1,0.03,D-0.2,wh,0,0.74,-0.08); RB(root,0.45,0.66,0.55,0.006,wh,W/2-0.33,0.36,-0.1);
      const dr=G(root,0,0,0,{anim:anim('slideZ',-0.32,'Ящик')}); RB(dr,0.43,0.18,0.02,0.005,wh,W/2-0.33,0.6,-0.385); P(dr,0.12,0.012,0.012,mat(hex('#c9a25a'),0.9,{noTex:true}),W/2-0.33,0.64,-0.4); P(dr,0.4,0.1,0.48,back,W/2-0.33,0.56,-0.13);
      const lg=G(root,0,0,0,{anim:anim('glow',1,'Подсветка',true)}); lg.anim.rate=1.6; root.lampSw=lg; const led=mat([0.85,0.82,0.75],0.3,{glow:[1,0.9,0.72],glowFull:true,noTex:true});
      P(lg,W-0.02,0.006,0.012,led,0,H-0.04,F+0.05); P(lg,W-0.02,0.006,0.012,led,0,0.012,F+0.035);
      const lc=mkCanvas(1024,256),x=lc.getContext('2d'); x.fillStyle='#0f1012'; x.fillRect(0,0,1024,256); x.fillStyle='#e9a300'; x.beginPath(); x.moveTo(70,60); x.lineTo(190,60); x.lineTo(70,196); x.closePath(); x.fill(); x.fillStyle='#ffffff'; x.beginPath(); x.moveTo(190,60); x.lineTo(190,196); x.lineTo(70,196); x.closePath(); x.fill();
      x.fillStyle='#ffffff'; x.font='800 92px "Golos Text",Arial'; x.textBaseline='alphabetic'; x.fillText('ДЖИМАЛ ГРУП',236,140); x.fillStyle='#e9a300'; x.font='700 46px "Golos Text",Arial'; x.fillText('КИБЕР 102',240,200); const lk='recLogo'; if(!TEX[lk]) TEX[lk]=texFromCanvas(lc);
      RB(root,0.98,0.26,0.03,0.01,back,0,0.66,F+0.05); const logo=lg.add(new Node({mesh:QUAD(0.94,0.235),mat:mat([0.75,0.75,0.75],0.4,{tex:lk,glow:[1.1,1.1,1.1]}),pos:[0,0.66,F+0.0655]})); logo.trig=lg;
      const bt=C(root,0.012,0.01,mat(hex('#2a2b2e'),0.5,{glow:[1,0.75,0.35],noTex:true}),-W/2+0.2,0.76,-D/2+0.13,{seg:16}); bt.trig=lg; },
    lights:it=>{ const n=it.root.lampSw; return n?[{p:M4.pt(itemWorld(it),0,0.5,0.75),c:[1,0.9,0.75],pow:0.7,k:1.6,down:false,sh:false,on:ease(n.anim.t)}]:[]; } },
