import soundfile as sf, numpy as np
a,sr=sf.read('/home/claude/proj/raw/audio16k.wav'); h=int(sr*0.25)
db=20*np.log10(np.array([np.sqrt(np.mean(a[i:i+h]**2)) for i in range(0,len(a)-h,h)])+1e-9)
np.save('/home/claude/proj/raw/rms.npy',db)
