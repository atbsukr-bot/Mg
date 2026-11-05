"""ep002 shorts: 1080x1920 cut-downs of the finished episode.

Source = the caption-free pieces of the final timeline (work/concat_A5.txt, exact frame counts) + the A6 mix (work/mix_A6.wav),
so captions are re-set for the vertical frame instead of being cropped away.
- face shots: 9:16 crop that follows his face (haar detector, smoothed per shot), zoom alternates every 3 s, face kept high
- shots without a face (paper scenes, B-roll): the whole 16:9 frame over a blurred, darkened copy of itself (no background change)
- hook title big under the face for the first 2.5 s, then a fixed title bar on top; "the full story is on the channel" at the end
- channel logo top-right, red/yellow progress bar on top

Usage: python3 scripts/shorts.py [n ...]      (default: all)
"""
import json, os, re, subprocess, sys
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, 'work')
OUT = os.path.join(ROOT, 'out', 'shorts')
FPS, SW, SH = 30, 2560, 1440
OW, OH = 1080, 1920

# (start s, end s, title) on the final timeline (A5/A6)
SHORTS = [
    (95.35, 144.30, 'اتصال من رقم مفصول'),
    (156.30, 204.75, 'رقم مفصول من 10 سنين'),
    (432.75, 502.25, 'مسرح جريمة في بيت مهجور'),
    (559.10, 622.10, 'تلفون بدون سلك… يرن'),
    (833.75, 896.60, 'سؤال واحد كشفه'),
    (1103.30, 1173.80, 'الساعة 2:17 بالضبط'),
]
END_TXT = 'القصة كاملة على القناة'


def pieces():
    txt = open(os.path.join(WORK, 'concat_A5.txt')).read()
    files = re.findall(r"file '([^']+)'\nduration ([\d.]+)", txt)
    out, f0 = [], 0
    for p, d in files:
        n = int(round(float(d) * FPS))
        out.append((p, f0, n)); f0 += n
    return out


def frames(a, b, w, h):
    """yield frames a..b-1 (timeline frame numbers) as BGR arrays of w x h"""
    last = None
    for p, f0, n in pieces():
        if f0 + n <= a or f0 >= b:
            continue
        skip = max(0, a - f0); take = min(f0 + n, b) - (f0 + skip)
        # count frames instead of seeking: some pieces' timestamps do not start at 0, so -ss can land past the end
        cmd = ['ffmpeg', '-v', 'error', '-noautorotate', '-i', p,
               '-vf', f'scale={w}:{h}:flags=bicubic', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-']
        pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        for _ in range(skip):
            if len(pr.stdout.read(w * h * 3)) < w * h * 3:
                break
        got = 0
        while got < take:
            buf = pr.stdout.read(w * h * 3)
            if len(buf) < w * h * 3:
                break
            last = np.frombuffer(buf, np.uint8).reshape(h, w, 3); got += 1
            yield last
        pr.stdout.close(); pr.wait()
        for _ in range(take - got):   # frame-complete like the build: pad a short piece with its last frame
            yield last


def analyse(a, b):
    """per-frame plan: ('face', cx, cy, fh) or ('fit',) - all normalised to the source frame"""
    front = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    prof = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
    w, h = 640, 360
    small, det = [], {}
    prev = None; cuts = [0]
    for i, fr in enumerate(frames(a, b, w, h)):
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        t = cv2.resize(g, (64, 36)).astype(np.float32)
        if prev is not None and np.abs(t - prev).mean() > 28:
            cuts.append(i)
        prev = t
        if i % 5 == 0:
            fs = list(front.detectMultiScale(g, 1.15, 6, minSize=(50, 50)))
            if not fs:
                fs = list(prof.detectMultiScale(g, 1.15, 6, minSize=(50, 50))) + \
                     [(w - x - fw, y, fw, fh) for x, y, fw, fh in prof.detectMultiScale(cv2.flip(g, 1), 1.15, 6, minSize=(50, 50))]
            if fs:
                x, y, fw, fh = max(fs, key=lambda r: r[2] * r[3])
                det[i] = ((x + fw / 2) / w, (y + fh / 2) / h, fh / h)
        small.append(None)
    n = len(small); cuts.append(n)
    plan = [None] * n
    for s, e in zip(cuts[:-1], cuts[1:]):
        smp = [k for k in range(s, e) if k % 5 == 0]
        hits = [k for k in smp if k in det and det[k][2] > 0.12]
        if smp and len(hits) >= 0.4 * len(smp):
            ks = np.array(hits)
            xs = np.array([det[k][0] for k in hits]); ys = np.array([det[k][1] for k in hits]); hs = np.array([det[k][2] for k in hits])
            # drop outliers (a hand / the guitar picked up as a face), then interpolate and smooth over ~1.5 s
            mx = np.median(xs); ok = np.abs(xs - mx) < 0.12
            ks, xs, ys, hs = ks[ok], xs[ok], ys[ok], hs[ok]
            fr_ = np.arange(s, e)
            X = np.interp(fr_, ks, xs); Y = np.interp(fr_, ks, ys)
            k = np.ones(45) / 45
            pad = lambda v: np.convolve(np.pad(v, 22, mode='edge'), k, mode='valid')[:len(v)]
            X, Y = pad(X), pad(Y)
            fh = float(np.median(hs))
            for j, f in enumerate(fr_):
                plan[f] = ('face', float(X[j]), float(Y[j]), fh)
        else:
            for f in range(s, e):
                plan[f] = ('fit',)
    return plan, cuts


def render_video(a, b, plan, cuts, path):
    logo = cv2.imread(os.path.join(ROOT, 'public', 'logo.png'), cv2.IMREAD_UNCHANGED)
    ls = 120; logo = cv2.resize(logo, (ls, ls), interpolation=cv2.INTER_AREA)
    la = logo[:, :, 3:4].astype(np.float32) / 255 * 0.9; lc = logo[:, :, :3].astype(np.float32)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    n = b - a
    shot_start = {c: True for c in cuts}
    s0 = 0
    for i, fr in enumerate(frames(a, b, SW, SH)):
        if i in shot_start:
            s0 = i
        p = plan[min(i, len(plan) - 1)]
        tsec = i / FPS
        if p[0] == 'face':
            _, cx, cy, fh = p
            # zoom steps every 3 s (1.0 / 1.12 / 1.05 / 1.18) with a slow push inside each step
            step = int((i - s0) / (3 * FPS)); within = ((i - s0) % (3 * FPS)) / (3 * FPS)
            z = [1.0, 1.12, 1.05, 1.18][step % 4] + 0.025 * within
            ch = SH / z; cw = ch * 9 / 16
            x0 = np.clip(cx * SW - cw / 2, 0, SW - cw)
            y0 = np.clip(cy * SH - 0.36 * ch, 0, SH - ch)
            M = np.float32([[OW / cw, 0, -x0 * OW / cw], [0, OH / ch, -y0 * OH / ch]])
            out = cv2.warpAffine(fr, M, (OW, OH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        else:
            bg = cv2.resize(fr, (192, 108), interpolation=cv2.INTER_AREA)
            bg = cv2.GaussianBlur(bg, (0, 0), 6)
            bh = OH; bw = int(bh * 16 / 9)
            bg = cv2.resize(bg, (bw, bh), interpolation=cv2.INTER_LINEAR)[:, (bw - OW) // 2:(bw - OW) // 2 + OW]
            out = (bg.astype(np.float32) * 0.45).astype(np.uint8)
            push = 1.0 + 0.03 * min(1, (i - s0) / (6 * FPS))
            cw_, ch_ = int(SW / push), int(SH / push)
            src = fr[(SH - ch_) // 2:(SH - ch_) // 2 + ch_, (SW - cw_) // 2:(SW - cw_) // 2 + cw_]
            fg = cv2.resize(src, (OW, 608), interpolation=cv2.INTER_AREA)
            out[600:1208] = fg
        # logo top-right, below the title bar
        y, x = 300, OW - ls - 40
        roi = out[y:y + ls, x:x + ls].astype(np.float32)
        out[y:y + ls, x:x + ls] = (roi * (1 - la) + lc * la).astype(np.uint8)
        # progress bar
        px = int(OW * (i + 1) / n)
        out[0:14, :] = (out[0:14, :] * 0.4).astype(np.uint8)
        out[0:14, :px] = (42, 38, 227)
        out[10:14, :px] = (63, 210, 255)
        enc.stdin.write(out.tobytes())
    enc.stdin.close(); enc.wait()


def ass_time(x):
    hh = int(x // 3600); mm = int(x % 3600 // 60); ss = x % 60
    return f'{hh}:{mm:02d}:{ss:05.2f}'


def write_ass(a_s, b_s, title, path):
    rows = []
    for l in open(os.path.join(WORK, 'captions.ass')):
        if not l.startswith('Dialogue'):
            continue
        p = l.rstrip('\n').split(',', 9)
        if p[3] not in ('Cap', 'Key'):
            continue
        def s(x):
            h, m, sec = x.split(':'); return int(h) * 3600 + int(m) * 60 + float(sec)
        a, b = s(p[1]), s(p[2])
        if b <= a_s or a >= b_s:
            continue
        rows.append((max(0, a - a_s), min(b_s, b) - a_s, p[3], re.sub(r'\{[^}]*\}', '', p[9])))
    d = b_s - a_s
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {OW}
PlayResY: {OH}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Cairo Cap,74,&H00FFFFFF,&H00FFFFFF,&H00141414,&H80000000,0,0,0,0,100,100,0,0,1,6,3,2,70,70,430,1
Style: Key,Cairo Cap,78,&H00FFFFFF,&H00FFFFFF,&H002A26E3,&H962A26E3,0,0,0,0,100,100,0,0,3,20,0,2,70,70,430,1
Style: Title,Cairo Cap,64,&H00141414,&H00141414,&H003FD2FF,&H003FD2FF,0,0,0,0,100,100,0,0,3,22,0,8,60,60,110,1
Style: Hook,Cairo Cap,104,&H00FFFFFF,&H00FFFFFF,&H002A26E3,&H002A26E3,0,0,0,0,100,100,0,0,3,30,0,2,60,60,640,1
Style: End,Cairo Cap,70,&H00141414,&H00141414,&H003FD2FF,&H003FD2FF,0,0,0,0,100,100,0,0,3,24,0,2,60,60,640,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 2,{ass_time(0)},{ass_time(2.5)},Hook,,0,0,0,,{{\\fad(0,200)\\t(0,180,\\fscx112\\fscy112)\\t(180,320,\\fscx100\\fscy100)}}{title}",
          f"Dialogue: 2,{ass_time(2.5)},{ass_time(d)},Title,,0,0,0,,{{\\fad(150,0)}}{title}",
          f"Dialogue: 2,{ass_time(d - 2.6)},{ass_time(d)},End,,0,0,0,,{{\\fad(200,0)}}{END_TXT}"]
    for a, b, st, t in rows:
        ev.append(f"Dialogue: 1,{ass_time(a)},{ass_time(b)},{st},,0,0,0,,{t}")
    open(path, 'w').write(head + '\n'.join(ev) + '\n')


def make(k):
    a_s, b_s, title = SHORTS[k]
    a, b = int(round(a_s * FPS)), int(round(b_s * FPS))
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(WORK, f'short{k + 1}')
    plan, cuts = analyse(a, b)
    nf = sum(1 for p in plan if p[0] == 'fit')
    print(f'short {k + 1}: {(b - a) / FPS:.1f}s, {len(cuts) - 2} cuts, {nf / len(plan):.0%} without face', flush=True)
    render_video(a, b, plan, cuts, tmp + '_v.mp4')
    write_ass(a / FPS, b / FPS, title, tmp + '.ass')
    d = (b - a) / FPS
    fonts = os.path.join(ROOT, 'public', 'fonts')
    out = os.path.join(OUT, f'ep002_short{k + 1}.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp + '_v.mp4', '-ss', f'{a / FPS:.3f}', '-t', f'{d:.3f}', '-i', os.path.join(WORK, 'mix_A6.wav'),
                    '-filter_complex', f"[0:v]ass='{tmp}.ass':fontsdir='{fonts}':shaping=complex[v];"
                                       f"[1:a]afade=t=in:d=0.12,afade=t=out:st={d - 0.6:.3f}:d=0.6[a]",
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-t', f'{d:.3f}', out], check=True)
    os.remove(tmp + '_v.mp4')
    print('built', out, flush=True)


if __name__ == '__main__':
    ks = [int(x) - 1 for x in sys.argv[1:]] or range(len(SHORTS))
    for k in ks:
        make(k)
