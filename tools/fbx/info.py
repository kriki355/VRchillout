import sys, numpy as np
sys.path.insert(0,'/home/claude/fbx')
from fbxparse import parse,sub
from extract2 import load
for path in sys.argv[1:]:
    top=parse(path); O=[t for t in top if t['n']=='Objects'][0]
    G=[t for t in top if t['n']=='GlobalSettings'][0]; gs={p['p'][0]:p['p'][4:] for p in sub(G,'Properties70')['c']}
    mats=[n['p'][1].split('\x00')[0] for n in O['c'] if n['n']=='Material']
    texs=[ (n['p'][1].split('\x00')[0], (sub(n,'RelativeFilename') or {'p':['']})['p'][0]) for n in O['c'] if n['n'] in ('Texture','Video')]
    print('=====',path.split('/')[-1],'unit',gs.get('UnitScaleFactor'),'up',gs.get('UpAxis'),'mats',mats,'tex',texs[:8])
    try:
        ps=load(path); allp=np.concatenate([p['pos'] for p in ps]); print('  bbox',allp.min(0).round(1),allp.max(0).round(1),'parts',len(ps),'verts',sum(len(p['pos']) for p in ps))
        for p in ps[:30]: print('   ',p['name'],p['mat'],len(p['pos']),p['pos'].min(0).round(1),p['pos'].max(0).round(1))
    except Exception as e: print('  ERR',e)
