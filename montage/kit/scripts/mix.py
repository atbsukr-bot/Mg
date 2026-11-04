import json, numpy as np, soundfile as sf
P='/home/claude/proj/app/public/'; SR=48000; FPS=30
e=json.load(open(P+'edl.json'))
N=int(e['duration']/FPS*SR)
def load(p):
    a,sr=sf.read(p,dtype='float32',always_2d=True)
    if a.shape[1]==1: a=np.repeat(a,2,1)
    if sr!=SR:
        idx=np.arange(0,len(a),sr/SR); a=np.stack([np.interp(idx,np.arange(len(a)),a[:,c]) for c in range(2)],1).astype('float32')
    return a
mix=np.zeros((N,2),'float32')
v=load(P+'voice.wav')[:N]; mix[:len(v)]+=v
m=load(P+e['musicFile']); reps=int(np.ceil(N/len(m)))+1
# loop with 2s crossfade
L=len(m); xf=2*SR; seg=m.copy(); out=m.copy()
while len(out)<N:
    fade=np.linspace(0,1,xf)[:,None]
    out=np.concatenate([out[:-xf], out[-xf:]*(1-fade)+seg[:xf]*fade, seg[xf:]])
out=out[:N]
kf=e['music']; fr=np.array([k['f'] for k in kf])/FPS*SR; vv=np.array([k['v'] for k in kf])
env=np.interp(np.arange(N),fr,vv).astype('float32')
# smooth envelope (0.3 s)
k=int(0.3*SR); env=np.convolve(env,np.ones(k)/k,mode='same').astype('float32')
mix+=out*env[:,None]
cache={}
for s in e['sfx']:
    if s['name'] not in cache: cache[s['name']]=load(P+f"sfx/{s['name']}.wav")
    a=cache[s['name']]*s.get('v',0.5)*0.9; st=int(s['f']/FPS*SR); en=min(N,st+len(a))
    if st<N: mix[st:en]+=a[:en-st]
fl=int(1.6*SR); mix[-fl:]*=np.linspace(1,0,fl)[:,None]**1.5
peak=np.max(np.abs(mix)); print('peak',peak)
mix=np.tanh(mix*1.0)  # soft safety limiter
sf.write('/home/claude/proj/app/out/mix.wav',mix,SR,subtype='PCM_16')
print('ok',N/SR)
