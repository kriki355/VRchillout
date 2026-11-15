import json,struct,numpy as np
b=open('printer.glb','rb').read()
L=struct.unpack('<I',b[12:16])[0]; J=json.loads(b[20:20+L]); off=20+L; BL=struct.unpack('<I',b[off:off+4])[0]; BIN=b[off+8:off+8+BL]
CT={5126:'f4',5123:'u2',5125:'u4',5121:'u1'}; NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
def acc(i):
    a=J['accessors'][i]; bv=J['bufferViews'][a['bufferView']]; o=bv.get('byteOffset',0)+a.get('byteOffset',0); nc=NC[a['type']]; dt=np.dtype(CT[a['componentType']]); st=bv.get('byteStride') or dt.itemsize*nc
    raw=np.frombuffer(BIN,dtype=np.uint8,count=st*(a['count']-1)+dt.itemsize*nc,offset=o)
    out=np.zeros((a['count'],nc),dtype=dt)
    for k in range(a['count']): out[k]=np.frombuffer(raw[k*st:k*st+dt.itemsize*nc].tobytes(),dtype=dt)
    return out
