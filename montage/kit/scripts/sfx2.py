import numpy as np, wave
SR=48000; out="/home/claude/proj/app/public/sfx"; rng=np.random.default_rng(3)
def save(name,x):
    x=x/(np.max(np.abs(x))+1e-9)*0.89; st=np.stack([x,x],1)
    with wave.open(f"{out}/{name}.wav","wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
# slide whistle: down-sweep with vibrato, breathy
d=0.9; t=np.arange(int(SR*d))/SR; u=t/d
f=1800*(1-u)**1.4+380 + 18*np.sin(2*np.pi*7*t)
ph=2*np.pi*np.cumsum(f)/SR
x=np.sin(ph)+0.25*np.sin(2*ph)+0.04*rng.standard_normal(len(t))
env=np.minimum(1,u*20)*np.minimum(1,(1-u)*6); save("slidewhistle",x*env)
# record scratch: back-and-forth pitch warped noise+tone
d=0.55; t=np.arange(int(SR*d))/SR
spd=np.sin(2*np.pi*3.6*t)*np.exp(-t*1.5)
f=600+1400*np.abs(spd); ph=2*np.pi*np.cumsum(f)/SR
n=rng.standard_normal(len(t)); n=np.convolve(n,np.ones(6)/6,'same')
x=(0.6*np.sign(np.sin(ph))*0.4+n*np.abs(spd)*1.2)*np.minimum(1,t*60)*np.exp(-t*2)
save("scratch",x)
# zoom whoosh: rising pitched air
d=0.45; t=np.arange(int(SR*d))/SR; u=t/d
n=rng.standard_normal(len(t)); y=np.zeros_like(n); lp=bp=0.0
for i in range(len(n)):
    fc=500+6000*u[i]**2; fq=2*np.sin(np.pi*fc/SR); hp=n[i]-lp-bp/1.3; bp+=fq*hp; lp+=fq*bp; y[i]=bp
tone=np.sin(2*np.pi*np.cumsum(200+900*u**2)/SR)*0.3
save("zoomwhoosh",(y+tone)*np.sin(np.pi*u)**1.2)
print("ok")
