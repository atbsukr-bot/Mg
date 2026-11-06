# Build the 30 s a-roll (cam1, frontal) for final-timeline window [T0,T1] of ep002, frame-exact at 30 fps.
import json, subprocess, os
W='work'; T0, T1 = 90.55, 119.30; FPS=30
TL=json.load(open('/home/user/Mg/montage/ep002/work/timeline.json'))
SYNC=19.86  # cam1 time = master + 19.86
CAM1='/tmp/claude-0/-home-user-Mg/1696909f-e6cb-52b7-9a07-e6b6a363bb06/scratchpad/src/cam1_1440.mp4'
def src_at(T):
    for x in TL:
        if x['t'] <= T < x['t'] + x['d'] + x.get('gap',0):
            o = min(T - x['t'], x['d'] - 1e-3)
            for a,b in x['segs']:
                if o < b-a: return a+o
                o -= b-a
            return x['segs'][-1][1]-1e-3
    raise ValueError(T)
n=int(round((T1-T0)*FPS)); times=[src_at(T0+i/FPS) for i in range(n)]
# group into contiguous runs (consecutive frames ~1/30 apart)
runs=[]; 
for i,s in enumerate(times):
    if runs and abs(s-(runs[-1][0]+runs[-1][1]/FPS))<0.02: runs[-1][1]+=1
    else: runs.append([s,1])
os.makedirs(f'{W}/f',exist_ok=True); k=0
for s,c in runs:
    subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-ss',f'{s+SYNC:.3f}','-i',CAM1,'-frames:v',str(c),'-vf','scale=1920:1080:flags=lanczos',
                    '-q:v','2','-start_number',str(k),f'{W}/f/%05d.jpg'],check=True); k+=c
print('frames',k,'runs',len(runs))
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(T0),'-t',str(T1-T0),'-i','/home/user/Mg/montage/ep002/work/voice.wav','-ac','2','-ar','48000',f'{W}/voice.wav'],check=True)
