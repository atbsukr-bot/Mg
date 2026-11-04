import numpy as np, wave, os
SR=48000; out="/home/claude/proj/app/public/sfx"
rng=np.random.default_rng(7)
def save(name,x):
    x=np.asarray(x,float); x=x/ (np.max(np.abs(x))+1e-9)*0.89
    st=np.stack([x,x],1) if x.ndim==1 else x
    with wave.open(f"{out}/{name}.wav","wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
def t(d): return np.arange(int(SR*d))/SR
def env(n,a,r): 
    e=np.ones(n); A=int(a*SR); R=int(r*SR); e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R)**2; return e
def bandnoise(n,fc_curve,q=1.5):
    # time-varying bandpass via STFT-ish: simple one-pole state variable filter
    x=rng.standard_normal(n); y=np.zeros(n); lp=bp=0.0
    for i in range(n):
        f=2*np.sin(np.pi*fc_curve[i]/SR); hp=x[i]-lp-bp/q; bp+=f*hp; lp+=f*bp; y[i]=bp
    return y
# whoosh
d=0.55; n=int(SR*d); tt=np.linspace(0,1,n)
fc=300+3500*np.sin(np.pi*tt)**1.5; w=bandnoise(n,fc,1.2)*np.sin(np.pi*tt)**2
pan=np.linspace(-1,1,n); save("whoosh",np.stack([w*(1-pan)/2+w*0.3,w*(1+pan)/2+w*0.3],1))
# fast swoosh
d=0.28; n=int(SR*d); tt=np.linspace(0,1,n); fc=800+5000*tt; w=bandnoise(n,fc,1.0)*np.sin(np.pi*tt)**1.5; save("swoosh",w)
# pop
x=t(0.12); f=900*np.exp(-x*40)+250; ph=2*np.pi*np.cumsum(f)/SR; p=np.sin(ph)*np.exp(-x*45); save("pop",p)
# click
x=t(0.04); c=rng.standard_normal(len(x))*np.exp(-x*300)+np.sin(2*np.pi*3000*x)*np.exp(-x*200); save("click",c)
# impact (boom)
x=t(1.6); f=110*np.exp(-x*3)+38; ph=2*np.pi*np.cumsum(f)/SR
b=np.sin(ph)*np.exp(-x*2.2)+0.5*rng.standard_normal(len(x))*np.exp(-x*18)
b=np.tanh(b*2.2); save("impact",b)
# riser
x=t(1.4); tt=x/1.4; f=200+1800*tt**2; ph=2*np.pi*np.cumsum(f)/SR
r=0.5*np.sin(ph)+0.5*bandnoise(len(x),400+6000*tt**2,2); r*=tt**2; save("riser",r)
# glitch
n=int(SR*0.35); g=np.zeros(n); i=0
while i<n:
    L=int(SR*rng.uniform(0.01,0.04)); k=rng.integers(3)
    seg=np.arange(min(L,n-i))/SR
    g[i:i+len(seg)]= [np.sign(np.sin(2*np.pi*rng.uniform(80,1500)*seg)), rng.standard_normal(len(seg)), np.sin(2*np.pi*rng.uniform(2000,6000)*seg)][k]*rng.uniform(.3,1)
    i+=L
save("glitch",g*0.7)
# ding
x=t(1.2); dn=sum(a*np.sin(2*np.pi*f*x)*np.exp(-x*dcy) for f,a,dcy in [(1568,1,3),(3136,.4,5),(2349,.3,4),(4704,.15,7)]); save("ding",dn)
# shutter/camera-ish tick + bell for subscribe "bell"
x=t(0.9); bl=sum(a*np.sin(2*np.pi*f*x)*np.exp(-x*dcy) for f,a,dcy in [(2093,1,4),(2637,.6,5),(3520,.3,6)])*(1+0.3*np.sin(2*np.pi*9*x)); save("bell",bl)
# flash / shimmer
x=t(0.8); sh=bandnoise(len(x),np.full(len(x),7000.0),3)*np.exp(-x*5); save("shimmer",sh)
print(os.listdir(out))
