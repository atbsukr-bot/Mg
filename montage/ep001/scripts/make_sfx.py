"""Synthesise every sound effect for ep001 from scratch (no third-party audio, no rights issues)."""
import numpy as np, wave, os
SR=48000; os.makedirs('public/sfx',exist_ok=True); rng=np.random.default_rng(7)
def save(name,x):
    x=np.clip(x/ (np.max(np.abs(x))+1e-9)*0.9,-1,1)
    with wave.open(f'public/sfx/{name}.wav','wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes())
t=lambda d: np.arange(int(SR*d))/SR
def env(n,a=0.005,r=0.1):
    e=np.ones(n); A=int(SR*a); R=int(SR*r); e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R); return e
def lp(x,k=30): return np.convolve(x,np.ones(k)/k,'same')
# pop
x=t(.12); save('pop', np.sin(2*np.pi*(900-5000*x)*x)*np.exp(-x*40))
# hit (low boom)
x=t(1.2); save('hit', (np.sin(2*np.pi*(55+40*np.exp(-x*8))*x)+0.3*lp(rng.standard_normal(len(x)),8)*np.exp(-x*20))*np.exp(-x*3.2))
# radio static burst
x=t(.9); n=rng.standard_normal(len(x)); save('static', (n-lp(n,6))*(0.6+0.4*np.sign(np.sin(2*np.pi*13*x)))*env(len(x),.01,.2))
# phone ring: two-tone 440+480 Hz, 2 rings
x=t(2.4); g=((x%1.2)<0.8).astype(float); save('ring', (np.sin(2*np.pi*440*x)+np.sin(2*np.pi*480*x))*g*(0.6+0.4*np.sign(np.sin(2*np.pi*20*x)))*env(len(x),.01,.05))
# siren (wail, distant)
x=t(4.0); f=750+350*np.sin(2*np.pi*0.55*x); ph=2*np.pi*np.cumsum(f)/SR; s=np.sin(ph)+0.3*np.sin(2*ph); save('siren', lp(s,12)*env(len(x),.6,1.2))
# camera shutter
x=t(.25); n=rng.standard_normal(len(x)); save('shutter', n*(np.exp(-x*90)+0.7*np.exp(-np.maximum(x-.09,0)*80)*(x>.09)))
# heartbeat (2 beats/sec pair)
x=t(4.0); hb=np.zeros(len(x))
for b0 in np.arange(0,4,1.0):
    for d in (0,.28):
        i=int((b0+d)*SR); k=t(.25); hb[i:i+len(k)]+= np.sin(2*np.pi*48*k)*np.exp(-k*18)*(1 if d==0 else .7)
save('heartbeat', hb)
# whoosh
x=t(.6); n=rng.standard_normal(len(x)); w=np.concatenate([lp(n[i:i+2400],max(2,int(40-36*i/len(n)))) for i in range(0,len(n),2400)])[:len(x)]; save('whoosh', w*np.sin(np.pi*x/.6)**2)
# glitch
x=t(.3); save('glitch', np.sign(np.sin(2*np.pi*(180+rng.integers(0,900,len(x))//4800*300)*x))*rng.choice([0,1],len(x),p=[.3,.7])*env(len(x),.002,.05)*0.6)
# tick
x=t(.05); save('tick', np.sin(2*np.pi*2400*x)*np.exp(-x*120))
# stamp thud
x=t(.35); save('stamp', (np.sin(2*np.pi*90*x)*np.exp(-x*25)+0.5*lp(rng.standard_normal(len(x)),4)*np.exp(-x*60)))
# music bed: dark drone pad, D minor-ish, 70 s, slow pulse
x=t(70.0); pad=sum(np.sin(2*np.pi*fr*x+np.sin(2*np.pi*.07*x*(i+1)))*a for i,(fr,a) in enumerate([(73.4,1),(110,.6),(146.8,.35),(174.6,.25)]))
pad*= 0.75+0.25*np.sin(2*np.pi*x/2.0)**2
tick_=np.zeros(len(x))
for b in np.arange(0,70,1.0): i=int(b*SR); k=t(.04); tick_[i:i+len(k)]+=np.sin(2*np.pi*1800*k)*np.exp(-k*150)*0.15
save('../bed', lp(pad,20)+tick_)
print('sfx ok', sorted(os.listdir('public/sfx')))
