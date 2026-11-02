"""Build the vertical, face-tracked, pause-cut A-roll for ep001.
Source: /home/user/media/IMG_0259.MOV (4K, stored sideways). Output: public/aroll.mp4 + public/words.json
"""
import json, subprocess
SRC = '/home/user/media/IMG_0259.MOV'
OFF = 40  # input is read from 40 s, so filter time t = source time - OFF
# face centre (fraction of upright frame width) sampled by hand from frames
KF = [(42,.50),(45,.48),(47,.64),(49,.39),(51,.50),(53,.64),(55,.58),(57,.73),(60,.73),(68,.70),(70,.70),(72,.38),(74,.50),(76,.58),(78,.56),(80,.58),(82,.52),(84,.55),(86,.56),(88,.56),(90,.62),(92,.59),(94,.58),(96,.38),(98,.38),(100,.56),(102,.50),(104,.59),(106,.55),(108,.47),(110,.44),(112,.61),(114,.61)]
W, H, CW = 3840, 2160, 1215
def xexpr():
    # piecewise-linear crop x in pixels, clamped
    e = str(int(min(max(KF[-1][1]*W-CW/2,0),W-CW)))
    for (t0,c0),(t1,c1) in reversed(list(zip(KF,KF[1:]))):
        x0=min(max(c0*W-CW/2,0),W-CW); x1=min(max(c1*W-CW/2,0),W-CW)
        e=f"if(lt(t\\,{t1-OFF})\\,{x0:.0f}+({x1-x0:.0f})*(t-{t0-OFF})/{t1-t0}\\,{e})"
    return e
# --- keep intervals from word timings
words = json.load(open('/home/user/media/words_all.json'))
def keep(lo, hi, pad=0.07, gap=0.28):
    ws=[w for w in words if lo<=w['s']<hi]
    iv=[]
    for w in ws:
        a,b=max(w['s']-pad,lo),min(w['e']+pad,hi)
        if iv and a-iv[-1][1] < gap: iv[-1][1]=max(iv[-1][1],b)
        else: iv.append([a,b])
    return iv
segs = keep(82.85,87.55) + keep(42.7,58.4) + keep(69.5,111.98)
# --- ffmpeg: rotate upright, track-crop, scale, then trim+concat each interval
parts=[]; fc=[]
base = f"[0:v]transpose=1,crop={CW}:{H}:'{xexpr()}':0,scale=1080:1920,setsar=1,fps=30,split={len(segs)}" + ''.join(f'[v{i}]' for i in range(len(segs)))
fc.append(base)
fc.append(f"[0:a]aresample=48000,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,asplit={len(segs)}"+''.join(f'[a{i}]' for i in range(len(segs))))
out_t=0; mapping=[]
for i,(a,b) in enumerate(segs):
    fc.append(f"[v{i}]trim={a-OFF:.3f}:{b-OFF:.3f},setpts=PTS-STARTPTS[vv{i}]")
    fc.append(f"[a{i}]atrim={a-OFF:.3f}:{b-OFF:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03[aa{i}]")
    mapping.append(dict(src_a=a,src_b=b,out_a=out_t)); out_t+=b-a
fc.append(''.join(f'[vv{i}][aa{i}]' for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=1[v][a0]")
fc.append("[a0]loudnorm=I=-14:TP=-1.5:LRA=9[a]")
open('scripts/filter.txt','w').write(';\n'.join(fc))
subprocess.run(['ffmpeg','-v','error','-y','-ss','40','-to','114','-i',SRC,'-filter_complex_script','scripts/filter.txt','-map','[v]','-map','[a]',
  '-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','public/aroll.mp4'],check=True)
json.dump(mapping,open('scripts/mapping.json','w'),indent=1)
print(len(segs),'segments',round(out_t,2),'s')
