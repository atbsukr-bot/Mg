"""QC: list every pause in the finished video's voice longer than LIMIT seconds (owner rule: no silent looks)."""
import subprocess, sys
import numpy as np
f = sys.argv[1]; LIMIT = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vn', '-ac', '1', '-ar', '16000', '-af', 'highpass=f=120,lowpass=f=4000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(float)
h = 160; e = np.sqrt(np.convolve(x ** 2, np.ones(h) / h, 'same')[::h] + 1)
thr = np.percentile(e, 10) * 3.0
sil = e < thr; out = []; k = 0
while k < len(sil):
    if sil[k]:
        j = k
        while j < len(sil) and sil[j]:
            j += 1
        if (j - k) * 0.01 >= LIMIT:
            out.append((round(k * 0.01, 2), round((j - k) * 0.01, 2)))
        k = j
    else:
        k += 1
print(len(out), 'pauses >', LIMIT, 's:', out[:40])
