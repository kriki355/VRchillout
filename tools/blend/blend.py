import struct, sys
class Blend:
    def __init__(s,path):
        d=s.d=open(path,'rb').read()
        assert d[:7]==b'BLENDER'
        if d[7:9]==b'17':  # новый заголовок Blender 5: BLENDER17-01v0503
            s.hsize=17; s.ptr=8; s.end='<'; s.bh=32; s.newbh=True
        else:
            s.hsize=12; s.ptr=8 if d[7:8]==b'-' else 4; s.end='<' if d[8:9]==b'v' else '>'; s.newbh=False; s.bh=24 if s.ptr==8 else 20
        s.blocks=[]; p=s.hsize
        while p<len(d):
            code=d[p:p+4]
            if s.newbh:
                sdna,old,ln,nr=struct.unpack('<iQqq',d[p+4:p+32]); hb=32
            else:
                ln,old,sdna,nr=struct.unpack('<iQii',d[p+4:p+24]); hb=24
            s.blocks.append({'code':code,'old':old,'len':ln,'sdna':sdna,'nr':nr,'off':p+hb})
            p+=hb+ln
            if code==b'ENDB': break
        s.byold={b['old']:b for b in s.blocks}
        dna=[b for b in s.blocks if b['code']==b'DNA1'][0]; s.parse_sdna(d[dna['off']:dna['off']+dna['len']])
    def parse_sdna(s,x):
        p=8; n=struct.unpack('<i',x[p:p+4])[0]; p+=4; names=[]
        for _ in range(n): e=x.index(b'\0',p); names.append(x[p:e].decode()); p=e+1
        p=(p+3)&~3; assert x[p:p+4]==b'TYPE'; p+=4; n=struct.unpack('<i',x[p:p+4])[0]; p+=4; types=[]
        for _ in range(n): e=x.index(b'\0',p); types.append(x[p:e].decode()); p=e+1
        p=(p+3)&~3; assert x[p:p+4]==b'TLEN'; p+=4; tlen=list(struct.unpack('<%dh'%n,x[p:p+2*n])); p+=2*n; p=(p+3)&~3
        assert x[p:p+4]==b'STRC'; p+=4; n=struct.unpack('<i',x[p:p+4])[0]; p+=4; structs=[]
        for _ in range(n):
            t,nf=struct.unpack('<hh',x[p:p+4]); p+=4; fs=[]
            for _ in range(nf): ft,fn=struct.unpack('<hh',x[p:p+4]); p+=4; fs.append((types[ft],names[fn]))
            structs.append((types[t],fs))
        s.names,s.types,s.tlen,s.structs=names,types,tlen,structs; s.sbyname={t:i for i,(t,_) in enumerate(structs)}
    def fsize(s,t,name):
        if name.startswith('*') or name.startswith('(*'): base=s.ptr
        else: base=s.tlen[s.types.index(t)]
        import re; arr=1
        for m in re.findall(r'\[(\d+)\]',name): arr*=int(m)
        return base*arr
    def layout(s,sname):
        fs=s.structs[s.sbyname[sname]][1]; off=0; L={}
        for t,n in fs:
            sz=s.fsize(t,n); key=n.split('[')[0].lstrip('*').replace('(*','').split(')')[0]; L[key]=(off,t,n,sz); off+=sz
        return L
    def read(s,blk_off,sname,field,idx=0):
        L=s.layout(sname); off,t,n,sz=L[field]; o=blk_off+off; d=s.d
        if n.startswith('*'): return struct.unpack('<Q',d[o:o+8])[0]
        fmt={'int':'i','short':'h','char':'b','float':'f','double':'d','int64_t':'q','uint64_t':'Q','int8_t':'b','uchar':'B','uint':'I','ushort':'H','int32_t':'i','uint32_t':'I'}.get(t)
        if '[' in n and t=='char': return d[o:o+sz].split(b'\0')[0].decode('utf-8','replace')
        if fmt: return struct.unpack('<'+fmt,d[o:o+struct.calcsize(fmt)])[0]
        return o
