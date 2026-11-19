import gzip, struct, json, base64, numpy as np, sys
SRC='/tmp/ext/mesh/'
def load(f):
    b=open(SRC+f,'rb').read(); b=gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
    attr,nf,nv,ns=struct.unpack('<HIII',b[2:16]); o=16+ns
    F=np.frombuffer(b,np.int32,nf*3,o).reshape(-1,3).copy(); o+=nf*12
    V=np.frombuffer(b,np.float32,nv*3,o).reshape(-1,3).astype(np.float64); o+=nv*12
    S=None
    if attr&4: o+=nv*4
    if attr&8: S=np.frombuffer(b,np.float32,nv,o).copy()
    return F,V,S
def neighbors(F,n):
    nb=[set() for _ in range(n)]
    for a,b,c in F:
        nb[a].update((b,c)); nb[b].update((a,c)); nb[c].update((a,b))
    return [np.array(sorted(s)) for s in nb]
def vnormals(F,V):
    N=np.zeros_like(V); fn=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]])
    for k in range(3): np.add.at(N,F[:,k],fn)
    return N/np.linalg.norm(N,axis=1,keepdims=True)
b64=lambda a: base64.b64encode(a.tobytes()).decode()

F,V,_=load('BrainMesh_ICBM152.lh.mz3'); n=len(V)
nb=neighbors(F,n)
# sulcal depth: distance to a heavily smoothed surface
Vs=V.copy()
for it in range(60):
    Vs=0.5*Vs+0.5*np.array([Vs[x].mean(0) for x in nb])
Ns=vnormals(F,Vs)
d=((V-Vs)*Ns).sum(1)
ao=np.clip((-d-(-1.0))/6.0,0,1)   # deeper (negative d) -> more occlusion
x,y,z=V[:,0],V[:,1],V[:,2]
sylv = 2 - 0.45*y
yc = -8 - 0.67*(z-25)
lobe=np.zeros(n,np.uint8)
occ = y < -72 + 0.12*(z-20)
tem = (~occ) & (z < sylv) & (y < 28)
fro = (~occ) & (~tem) & (y > yc)
lobe[fro]=1; lobe[(~occ)&(~tem)&(~fro)]=2; lobe[tem]=3; lobe[occ]=4
# smooth labels (majority of neighbours)
for it in range(4):
    nl=lobe.copy()
    for i in range(n):
        vals=np.bincount(lobe[nb[i]],minlength=5); vals[lobe[i]]+=1; nl[i]=vals.argmax()
    lobe=nl
area=np.zeros(n,np.uint8)
lat = x < -30
area[(lobe==1)&(y-yc<11)&(z>22)]=11
area[(lobe==2)&(yc-y<11)&(z>22)]=12
area[(lobe==1)&(x<-36)&(y>6)&(y<34)&(z>-2)&(z<24)]=13
area[(lobe==3)&(x<-42)&(y>-56)&(y<-24)&(z>-2)&(z<22)]=14
area[(lobe==4)&((x>-16)|(y<-96))]=15
area[(lobe==1)&(area==0)&(y>26)]=16
for it in range(2):
    na=area.copy()
    for i in range(n):
        vals=np.bincount(area[nb[i]],minlength=17); vals[area[i]]+=1; na[i]=vals.argmax()
    area=na
area[(area!=0)&(((area<=12)|(area==16))&(lobe!=1)&(lobe!=2))]=0
print('lobes',np.bincount(lobe),'areas',{k:int((area==k).sum()) for k in range(11,17)},file=sys.stderr)
Vq=np.round(V*100).astype(np.int16)
out={"cortex":{"n":n,"v":b64(Vq),"f":b64(F.astype(np.uint16)),"lobe":b64(lobe),"area":b64(area),
               "ao":b64(np.round(ao*255).astype(np.uint8)),"lat":b64(lat.astype(np.uint8))}}
# subcortical
F2,V2,S2=load('CIT168.mz3')
groups={"ganglios":[1,2,3,4,5,6,9,10,11,12,23,24,31,32],"hipotalamo":[27,28,29,30]}
out["sub"]={}
for g,labs in groups.items():
    keep=np.isin(S2,labs)
    idx=np.cumsum(keep)-1
    fk=keep[F2].all(1); Fg=idx[F2[fk]]; Vg=V2[keep]
    out["sub"][g]={"v":b64(np.round(Vg*100).astype(np.int16)),"f":b64(Fg.astype(np.uint16))}
    print(g,len(Vg),len(Fg),file=sys.stderr)
json.dump(out,open(sys.argv[1],'w'),separators=(',',':'))
