import struct, zlib, sys, json
def parse(path):
    d=open(path,'rb').read(); ver=struct.unpack('<I',d[23:27])[0]; big=ver>=7500
    def rprop(p):
        t=chr(d[p]); p+=1
        if t=='Y': return struct.unpack('<h',d[p:p+2])[0],p+2
        if t=='C': return d[p]!=0,p+1
        if t=='I': return struct.unpack('<i',d[p:p+4])[0],p+4
        if t=='F': return struct.unpack('<f',d[p:p+4])[0],p+4
        if t=='D': return struct.unpack('<d',d[p:p+8])[0],p+8
        if t=='L': return struct.unpack('<q',d[p:p+8])[0],p+8
        if t in 'SR':
            n=struct.unpack('<I',d[p:p+4])[0]; s=d[p+4:p+4+n]; return (s.decode('utf-8','replace') if t=='S' else s),p+4+n
        if t in 'fdlib':
            n,enc,cl=struct.unpack('<III',d[p:p+12]); p+=12; raw=d[p:p+cl]; p+=cl
            if enc==1: raw=zlib.decompress(raw)
            fmt={'f':'f','d':'d','l':'q','i':'i','b':'?'}[t]; return list(struct.unpack('<%d%s'%(n,fmt),raw)),p
        raise ValueError(t)
    def rnode(p):
        if big: end,np_,pl=struct.unpack('<QQQ',d[p:p+24]); p+=24
        else: end,np_,pl=struct.unpack('<III',d[p:p+12]); p+=12
        nl=d[p]; p+=1
        if end==0: return None,p
        name=d[p:p+nl].decode(); p+=nl; props=[]
        for _ in range(np_): v,p=rprop(p); props.append(v)
        ch=[]
        while p<end:
            c,p2=rnode(p)
            if c is None: p=p2; break
            ch.append(c); p=p2
        return {'n':name,'p':props,'c':ch},end
    p=27; top=[]
    while p<len(d)-200:
        c,p=rnode(p)
        if c is None: break
        top.append(c)
    return top
def find(nodes,name): return [n for n in nodes if n['n']==name]
def sub(n,name):
    for c in n['c']:
        if c['n']==name: return c
if __name__=='__main__':
    top=parse(sys.argv[1])
    def show(n,ind=0,depth=3):
        ps=[ (f'[{len(x)}]' if isinstance(x,list) else (repr(x)[:60])) for x in n['p']]
        print(' '*ind+n['n'],ps[:6])
        if ind//2<depth:
            for c in n['c'][:40]: show(c,ind+2,depth)
    for t in top:
        if t['n'] in ('Objects','Connections','GlobalSettings'): show(t,0,int(sys.argv[2]) if len(sys.argv)>2 else 2)
        else: print(t['n'])
