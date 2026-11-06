# Composite: neon room behind the person + Majed-style montage (handheld camera, zoom steps, punches,
# flash/glitch, captions in the owner's dialect, channel logo). Writes out/neon30b_v.mp4 (no audio).
import numpy as np, cv2, re, subprocess, math
from PIL import Image, ImageDraw, ImageFont
FPS=30; T0=90.55; N=862; END=38            # 862 a-roll frames + 38-frame end card = 30.0 s
P='/home/user/Mg/montage/ep002/'
BG=cv2.imread('work/room_bg.png').astype(np.float32)/255
H0,W0=BG.shape[:2]
LOGO=Image.open(P+'public/logo.png').convert('RGBA').resize((118,118))
FONT=ImageFont.truetype(P+'public/fonts/CairoCap-ExtraBold.ttf',66)
FONT_END=ImageFont.truetype(P+'public/fonts/Tajawal-Black.ttf',92)
FACE=(890,400)
# captions from the delivered ep002 subtitles (already corrected to his dialect)
caps=[]
for l in open(P+'work/captions.ass',encoding='utf8'):
    m=re.match(r'Dialogue: \d,(\d+):(\d+):([\d.]+),(\d+):(\d+):([\d.]+),(Cap|Key),[^,]*,\d+,\d+,\d+,,(.*)',l)
    if not m: continue
    a=int(m[1])*3600+int(m[2])*60+float(m[3])-T0; b=int(m[4])*3600+int(m[5])*60+float(m[6])-T0
    if b>0 and a<N/FPS: caps.append((max(a,0),b,m[7],m[8].strip()))
# moments (seconds in this clip)
PUNCH=[3.04,5.43,25.13]          # «قبل العاصفة», «رنّ», «جريمة قتل»
FLASH=[5.43]; GLITCH=[(25.13,0.45)]
# zoom steps every ~2.5 s, alternating like the kit (1.06 / 1.2 / 1.1 / 1.28), slow push inside each step
STEPS=[0,2.4,5.43,8.2,10.9,13.6,16.4,19.0,21.8,25.13,27.4]; SC=[1.06,1.2,1.1,1.28,1.06,1.18,1.1,1.25,1.08,1.3,1.12]
def cam(t):
    k=max(i for i,s in enumerate(STEPS) if s<=t); s=SC[k]*(1+0.012*(t-STEPS[k]))
    for p in PUNCH:
        if 0<=t-p<0.5: s*=1+0.10*math.exp(-(t-p)*7)
    hx=6*math.sin(t*1.7)+3*math.sin(t*4.3); hy=4*math.sin(t*1.3+1)+2*math.sin(t*3.7)
    return s,hx,hy
def warp(img,s,hx,hy,cx,cy):
    M=np.float32([[s,0,(1-s)*cx+hx],[0,s,(1-s)*cy+hy]])
    return cv2.warpAffine(img,M,(1920,1080),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
GRADE=np.array([1.10,0.96,0.90],np.float32)   # BGR: cool the subject toward the room light
def composite(i,t):
    f=cv2.imread(f'work/f/{i:05d}.jpg').astype(np.float32)/255
    a=cv2.imread(f'work/m2/{i:05d}.png',0).astype(np.float32)/255
    a=cv2.GaussianBlur(np.clip((a-0.18)/0.64,0,1),(0,0),1.6)[...,None]
    s,hx,hy=cam(t)
    bx=int((W0-1920)/2-hx*0.4); by=int((H0-1080)/2-hy*0.4)
    bg=BG[by:by+1080,bx:bx+1920].copy()
    # camera grain on the plate so both layers share the same texture
    bg=np.clip(bg+np.random.normal(0,0.012,bg.shape).astype(np.float32),0,1)
    # relight: the room's own light, very blurred, becomes the light that falls on him
    room=cv2.GaussianBlur(BG[by:by+1080,bx:bx+1920],(0,0),120)
    lum=f.mean(2,keepdims=True)
    tint=room/ (room.mean(2,keepdims=True)+1e-3)            # room colour, normalised
    fg=f*0.72*(0.58+0.42*tint)+lum*0.10*tint                 # darker, colour of the room, skin still readable
    # TV-side rim light (right) + cool fill from the left
    xs=np.linspace(0,1,1920,dtype=np.float32)[None,:,None]
    sa=cv2.GaussianBlur(a,(0,0),3)[...,None]; edge=np.clip(sa-cv2.GaussianBlur(sa,(0,0),10)[...,None],0,1)*a
    rim=edge*(np.array([1.0,0.35,0.75],np.float32)*xs**1.5+np.array([1.0,0.45,0.15],np.float32)*(1-xs)**2*0.6)
    fg=np.clip(fg+rim*0.7,0,1)
    # light wrap: the background bleeds a little over his outline
    wrap=cv2.GaussianBlur(bg,(0,0),14)*np.clip(1-cv2.GaussianBlur(a,(0,0),6)[...,None],0,1)*a
    fg=np.clip(fg+wrap*0.2,0,1)
    out=bg*(1-a)+fg*a
    return warp(out,s,hx,hy,*FACE)
def fx(img,t):
    for p in FLASH:
        if 0<=t-p<0.25: img=img+(1-img)*0.7*(1-(t-p)/0.25)
    for p,d in GLITCH:
        if 0<=t-p<d:
            g=cv2.cvtColor(cv2.cvtColor((img*255).astype(np.uint8),cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR).astype(np.float32)/255
            o=int(18*(1-(t-p)/d)); g[...,2]=np.roll(g[...,2],o,1); g[...,0]=np.roll(g[...,0],-o,1)
            if int(t*30)%3==0: g=np.roll(g,int(40*math.sin(t*90)),0)
            img=g
    return np.clip(img,0,1)
def overlay(img,t,end=False):
    im=Image.fromarray(cv2.cvtColor((img*255).astype(np.uint8),cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(im)
    im.paste(LOGO,(1920-118-40,36),LOGO)
    for a,b,st,tx in caps:
        if a<=t<b and not end:
            w=d.textlength(tx,font=FONT,direction='rtl'); x=(1920-w)/2; y=950
            pop=min(1,(t-a)*8)
            if st=='Key':
                pad=22; d.rounded_rectangle((x-pad,y-8,x+w+pad,y+96),14,fill=(227,38,42))
                d.text((x,y),tx,font=FONT,fill=(255,255,255),direction='rtl')
            else:
                d.text((x,y),tx,font=FONT,fill=(255,255,255),direction='rtl',stroke_width=7,stroke_fill=(20,20,20))
    if end:
        tx='القصة كاملة على القناة'; w=d.textlength(tx,font=FONT_END,direction='rtl')
        d.text(((1920-w)/2,880),tx,font=FONT_END,fill=(255,210,63),direction='rtl',stroke_width=8,stroke_fill=(122,16,34))
    return np.asarray(im)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-',
    '-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','out/neon30b_v.mp4'],stdin=subprocess.PIPE)
last=None
for i in range(N):
    t=i/FPS; img=fx(composite(i,t),t); last=img
    enc.stdin.write(overlay(img,t).tobytes())
for j in range(END):                     # end card: darkened, blurred freeze + call to action
    t=(N+j)/FPS; a=min(1,j/8)
    img=last*(1-0.55*a); img=cv2.GaussianBlur(img,(0,0),1+8*a)
    enc.stdin.write(overlay(img,t,end=True).tobytes())
enc.stdin.close(); enc.wait(); print('done',N+END)
