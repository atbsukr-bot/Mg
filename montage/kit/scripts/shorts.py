import json, numpy as np, soundfile as sf
FPS=30; P='/home/claude/proj/app/public/'
edl=json.load(open(P+'edl.json'))
FACE=json.load(open('/home/claude/proj/raw/face.json'))
pieces=json.load(open('/home/claude/proj/raw/pieces.json'))['pieces']
def o2s(o):
    for p in pieces:
        if p['os']<=o<=p['oe']: return p['s']+o-p['os']
def face_c(o0,o1):
    xs=[];ys=[]
    for o in np.arange(o0,o1,0.5):
        s=o2s(o)
        if s is None: continue
        n=[x for x in FACE if x['face'] and abs(x['t']-s)<0.6]
        xs+= [x['cx'] for x in n]; ys+=[x['cy'] for x in n]
    return (float(np.median(xs)),float(np.median(ys))) if xs else (0.5,0.45)
# segs: (output_start, output_end, kind[, cx, cy])  kind: close | wide | insert (inserts: give cx/cy of the subject)
SHORTS=[
 dict(name='short1', title='مونتاج كامل بجملة وحدة', title2='ولا ثانية لمستها', segs=[(0.0,8.45,'close'),(21.0,41.6,'close')]),
 dict(name='short2', title='قلت: كلاود حط هنا…', title2='وحطّه!', segs=[(41.68,57.3,'close'),(196.44,204.0,'close')]),
 dict(name='short3', title='كيف تبني سكيل مونتاج؟', title2='بخطوات بسيطة', segs=[(60.35,97.7,'close')]),
 dict(name='short4', title='قبل وبعد مونتاج كلاود', title2='شوف الفرق', segs=[(112.4,123.08,'close'),(123.11,131.08,'insert',0.36,0.45),(131.11,140.08,'insert',0.5,0.4),(140.11,146.6,'close'),(149.31,155.3,'insert',0.5,0.5)]),
]
# portrait positions: every card sits in the band under his face and above the captions
POS={'keyword':dict(x=540,y=1060), 'beat':dict(x=540,y=1060), 'sparks':dict(x=540,y=1060), 'image':dict(x=760,y=1060), 'strings':dict(x=540,y=1090,scale=1.0), 'chords':dict(x=540,y=1150,scale=0.84,cols=4),
     'raw':dict(x=540,y=1130), 'checklist':dict(x=540,y=1110), 'phone':dict(x=830,y=1160,height=460), 'wide':dict(x=540,y=1100,w=700), 'ref':dict(x=540,y=1150),
     'prompt':dict(x=540,y=1120), 'editor':dict(x=540,y=1150,scale=1.0), 'notes':dict(x=540,y=1150), 'skill':dict(x=540,y=1150), 'branch':dict(x=560,y=1140,scale=0.95),
     'notice':dict(x=540,y=1130,scale=0.72), 'badge':dict(x=540,y=1480), 'counter':dict(x=540,y=1640)}
KEEP=('keyword','sparks','beat','image','chords','strings','punch','bw','glitch','shake','flash','raw','checklist','phone','wide','ref','prompt','editor','notes','skill','branch','notice','badge','counter')
mix,sr=sf.read('/home/claude/proj/app/out/mix_final.wav',dtype='float32',always_2d=True)
sfx=lambda n: sf.read(P+f'sfx/{n}.wav',dtype='float32',always_2d=True)[0]
for S in SHORTS:
    segs=[];caps=[];items=[];acc=0;audio=[]
    for sg in S['segs']:
        o0,o1,kind=sg[:3]
        a=int(round(o0*FPS)); b=int(round(o1*FPS)); L=b-a
        cx,cy=face_c(o0,o1) if kind=='close' else ((sg[3],sg[4]) if len(sg)>4 else (0.31,0.47))
        segs.append(dict(a=a,len=L,cx=cx,cy=cy,kind=kind))
        for c in edl['captions']:
            if a<=c['from']<b: caps.append(dict(from_=c['from']-a+acc,to=min(c['to'],b)-a+acc,words=c['words'],hl=c['hl']))
        for it in edl['items']:
            t=it['type']
            if t not in KEEP: continue
            f0,f1=it['from'],it['from']+it['dur']
            if f1<=a or f0>=b: continue
            n=dict(it); n['from']=max(f0,a)-a+acc; n['dur']=min(f1,b)-max(f0,a)
            if t in POS: n.update(POS[t])
            if t=='keyword': n['size']=min(72,int(it.get('size',64)*1.1)) if len(it['text'])<14 else 54
            if t=='beat': n['size']=min(170,it.get('size',200))
            if n['dur']>=4: items.append(n)
        seg=mix[int(o0*sr):int(o1*sr)].copy(); fl=int(0.015*sr); seg[:fl]*=np.linspace(0,1,fl)[:,None]; seg[-fl:]*=np.linspace(1,0,fl)[:,None]
        audio.append(seg); acc+=L
    dur=acc
    # a big card owns its moment: drop small words that would sit on top of it
    BIG=('raw','checklist','phone','wide','ref','prompt','editor','notes','skill','branch','notice')
    cards=[(i['from'],i['from']+i['dur']) for i in items if i['type'] in BIG]
    items=[i for i in items if not (i['type'] in ('keyword','beat','sparks') and any(a<i['from']+i['dur'] and i['from']<b for a,b in cards))]
    for c in caps: c['from']=c.pop('from_')
    caps=[c for c in caps if c['to']-c['from']>=5]
    au=np.concatenate(audio)
    N=int(dur/FPS*sr); au=au[:N] if len(au)>=N else np.pad(au,((0,N-len(au)),(0,0)))
    def add(fr,n,v):
        x=sfx(n)*v; st=int(fr/FPS*sr); en=min(len(au),st+len(x)); au[st:en]+=x[:en-st]
    add(0,'impact',0.55); add(0,'whoosh',0.4); add(72,'swoosh',0.3)
    j=0
    for s_ in segs[:-1]:
        j+=s_['len']; add(j-4,'whoosh',0.45)
    add(dur-75,'pop',0.5); add(dur-75,'ding',0.3)
    fo=int(0.6*sr); au[-fo:]*=np.linspace(1,0,fo)[:,None]
    au=np.tanh(au)
    sf.write(f'/home/claude/proj/app/out/{S["name"]}.wav',au,sr,subtype='PCM_16')
    spec=dict(duration=dur,title=S['title'],title2=S['title2'],segs=segs,captions=caps,items=items)
    json.dump(spec,open(P+S['name']+'.json','w'),ensure_ascii=False)
    print(S['name'],dur/FPS,'caps',len(caps),'items',len(items),[ (round(s['cx'],2),round(s['cy'],2)) for s in segs])
