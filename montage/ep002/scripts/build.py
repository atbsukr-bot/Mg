"""ep002 build: EDL (scripts/edl_<ver>.json) -> finished 2560x1440 long-form video.

Master clock = cam2 time (cam2 covers the whole shoot). cam1 time = master - SYNC['cam1'].
EDL entry (one spoken unit, kept in order):
  {"a": 49.9, "b": 57.3,            master seconds to keep (snapped to silence by --snap)
   "text": "...",                    corrected caption text (empty = no caption)
   "cam": "c1"|"c2"|"auto",          angle; auto alternates, falls back to c2 when cam1 is off
   "zoom": 1.0,                      punch-in (1.0 = full frame)
   "ins": {"id": "Clock", "props": {...}, "lead": 0.0},   full-screen insert over this unit (voice continues)
   "look": "flash",                  optional: 'flash' = 2014/2016 flashback grade, 'bw'
   "sfx": [["ring", 0.0, 0.5]],      [name, offset s, volume]
   "gap": 0.0,                       extra silence after the unit (dramatic pause)
   "music": "calm"|"tension"|"finale"|"none"   switch music cue from here
  }
Usage: python3 scripts/build.py edl_A.json out/ep002_A.mp4 [--preview]
"""
import hashlib, json, os, subprocess, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get('EP002_SRC', '/tmp/claude-0/-home-user-Mg/1696909f-e6cb-52b7-9a07-e6b6a363bb06/scratchpad/src')
WORK = os.path.join(ROOT, 'work')
FPS = 30
W, H = 2560, 1440
cfg = json.load(open(os.path.join(ROOT, 'scripts', os.environ.get('EP002_CFG', 'sources.json'))))
SYNC = cfg['sync']            # {"cam1": offset}  master = cam1 + offset
CAM1_DUR = cfg['cam1_dur']
VOICE = cfg['voice']          # which camera's audio is the voice: "c1" | "c2" (or per-range list)
os.makedirs(WORK, exist_ok=True)


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def h(*a):
    return hashlib.md5(json.dumps(a, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


# ---------- grading (manual, per camera; no auto colour correction) ----------
GRADE = cfg['grade']  # {"c1": "eq=...,colorbalance=...", "c2": "..."}
LOOK = {
    'flash': 'eq=saturation=0.45:contrast=1.05,colorchannelmixer=rr=1.0:rg=0.08:gg=0.95:bb=0.78,noise=alls=12:allf=t',
    'bw': 'hue=s=0,eq=contrast=1.15',
    None: 'null',
}


def cam_input(cam, t_master):
    if cam == 'c1':
        return os.path.join(SRC, cfg['cam1_file']), t_master - SYNC['cam1']
    return os.path.join(SRC, cfg['cam2_file']), t_master


piece_cam = {}


def piece(cam, a, b, zoom, look, crop_c):
    """render one camera piece (video only) to an intermediate clip"""
    src, t0 = cam_input(cam, a)
    # cache key in camera-local time, so re-syncing the master clock reuses rendered pieces
    key = h('p5', cam, round(t0, 3), round(b - a, 3), zoom, look, crop_c, GRADE.get(cam))
    out = os.path.join(WORK, f'p_{key}.mp4')
    if os.path.exists(out):
        piece_cam[out] = cam
        return out
    cx, cy = crop_c
    vf = []
    if cam == 'c2':
        vf.append('null')  # cam2 is read with -noautorotate (sensor is landscape; the rotate flag is wrong)
    vf.append(f'fps={FPS}')
    vf.append(f'scale={W}:{H}:flags=lanczos')
    if zoom > 1.001:
        cw, ch = int(W / zoom) // 2 * 2, int(H / zoom) // 2 * 2
        x = int(min(max(cx * W - cw / 2, 0), W - cw)); y = int(min(max(cy * H - ch / 2, 0), H - ch))
        vf.append(f'crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos')
    vf += [GRADE.get(cam, 'null'), LOOK.get(look, 'null'), 'format=yuv420p']
    pre = ['-noautorotate'] if cam == 'c2' else []
    piece_cam[out] = cam
    run(['ffmpeg', '-v', 'error', '-y', *pre, '-ss', f'{t0:.3f}', '-i', src, '-map', '0:v:0', '-frames:v', str(round((b - a) * FPS)), '-an',
         '-vf', ','.join(vf), '-c:v', 'libx264', '-preset', 'faster', '-crf', '15', '-video_track_timescale', '15360', out])
    return out


BROLL_LOOK = {
    # Abu-Al-Sadiq-style archive: teal/amber split, lifted blacks, grain, flicker, old-TV bezel
    'archive': "eq=contrast=1.08:brightness=0.02:saturation=0.75,colorbalance=rs=-0.06:gs=0.0:bs=0.08:rh=0.10:gh=0.04:bh=-0.08,"
               "curves=master='0/0.05 0.5/0.5 1/0.95',noise=alls=14:allf=t,eq=brightness='0.015*sin(9*t)':eval=frame",
    'night': "eq=contrast=1.08:brightness=0.02:saturation=0.65:gamma=1.1,colorbalance=rs=-0.08:bs=0.12:rm=-0.05:bm=0.08,noise=alls=10:allf=t",
    'clean': "eq=contrast=1.04:saturation=0.9,noise=alls=6:allf=t",
}


def broll(br, dur):
    """stock clip -> slow push-in, graded, inside the old-TV bezel (or full frame)"""
    src = os.path.join(ROOT, 'public', 'broll', br['src'])
    look = br.get('look', 'archive'); framed = br.get('frame', look == 'archive')
    z0, z1 = br.get('zoom', (1.0, 1.12))
    n = round(dur * FPS)
    key = h('b2', br, n)
    out = os.path.join(WORK, f'b_{key}.mp4')
    if os.path.exists(out):
        return out
    zexpr = f"{z0}+({z1 - z0})*n/{max(n - 1, 1)}"
    vf = (f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"{'reverse,' if br.get('rev') else ''}"
          f"scale=w='trunc({W}*({zexpr})/2)*2':h='trunc({H}*({zexpr})/2)*2':eval=frame:flags=bicubic,crop={W}:{H},"
          f"{BROLL_LOOK[look]},vignette=angle=PI/5")
    srcdur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    ss = br.get('ss', 0.0)
    loop = ['-stream_loop', '-1'] if ss + dur > srcdur - 0.1 else []
    if framed:
        fx = os.path.join(ROOT, 'public', 'fx', 'tvframe.png')
        cmd = ['ffmpeg', '-v', 'error', '-y', *loop, '-ss', f'{ss:.3f}', '-i', src, '-i', fx, '-filter_complex',
               f"[0:v]{vf},scale={W - 300}:{H - 190}[v];color=c=0x060a09:s={W}x{H}:r={FPS}[bg];[bg][v]overlay=150:95:shortest=1[c];[c][1:v]overlay=0:0,format=yuv420p",
               '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'faster', '-crf', '15', '-video_track_timescale', '15360', out]
    else:
        cmd = ['ffmpeg', '-v', 'error', '-y', *loop, '-ss', f'{ss:.3f}', '-i', src, '-vf', vf + ',format=yuv420p',
               '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'faster', '-crf', '15', '-video_track_timescale', '15360', out]
    run(cmd)
    return out


def insert(ins, dur):
    props = dict(ins.get('props', {}), dur=round(dur * FPS))
    key = h('i3', ins['id'], props)
    out = os.path.join(WORK, f'i_{key}.mp4')
    if not os.path.exists(out):
        run(['npx', 'remotion', 'render', 'src/index.ts', ins['id'], out, '--props', json.dumps(props, ensure_ascii=False),
             '--codec=h264', '--crf=14', '--log=error'], cwd=ROOT)
        # normalise to the exact stream params of the camera pieces so the concat demuxer joins cleanly
        tmp = out + '.n.mp4'
        run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-an', '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264', '-preset', 'faster',
             '-crf', '15', '-video_track_timescale', '15360', tmp])
        os.replace(tmp, out)
    return out


def wav_read(p):
    w = wave.open(p); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    return x.reshape(-1, ch).mean(1) if ch > 1 else x, w.getframerate()


def build(edl_path, out_path, preview=False):
    edl = json.load(open(edl_path))
    units = edl['units']
    # ---------- voice analysis (needed to cut every silence) ----------
    vx, sr = wav_read(os.path.join(SRC, cfg['voice_wav']))  # master-clock voice track (mono)
    voff = cfg['voice_offset']
    hop = int(0.01 * sr)
    env = np.sqrt(np.convolve(vx ** 2, np.ones(hop) / hop, 'same')[::hop] + 1e-12)   # 10 ms envelope
    floor = np.percentile(env, 8)
    thr = floor * 3.5          # ~ +11 dB over the room noise = speech

    def tighten(a, b):
        """split [a,b] (master s) into speech runs: every pause >= MAXP is removed (owner: no silent looks at camera)"""
        MAXP, PAD0, PAD1 = 0.2, 0.04, 0.07
        i0 = max(0, int((a - voff) / 0.01)); i1 = min(len(env), int((b - voff) / 0.01))
        sp = env[i0:i1] > thr
        if not sp.any():
            return [(a, b)]
        runs = []; k = 0; n = len(sp)
        while k < n:
            if sp[k]:
                j = k
                while j < n and sp[j]:
                    j += 1
                runs.append([k, j]); k = j
            else:
                k += 1
        merged = [runs[0]]
        for r in runs[1:]:
            if (r[0] - merged[-1][1]) * 0.01 < MAXP:
                merged[-1][1] = r[1]
            else:
                merged.append(r)
        out = []
        for r0, r1 in merged:
            if (r1 - r0) * 0.01 < 0.06:   # clicks / breaths alone are dropped
                continue
            sa = a + r0 * 0.01 - PAD0; sb = a + r1 * 0.01 + PAD1
            out.append((max(a - 0.05, sa), min(b + 0.1, sb)))
        return out or [(a, b)]

    # ---------- timeline ----------
    t = 0.0; tl = []
    alt = 0
    for u in units:
        segs = [(u['a'], u['b'])] if (u.get('keep_pauses') or u.get('ins') and not u.get('text')) else tighten(u['a'], u['b'])
        segs = [(sa, sa + max(1, round((sb - sa) * FPS)) / FPS) for sa, sb in segs]
        d = sum(sb - sa for sa, sb in segs)
        u = dict(u, segs=segs, gap=round(min(u.get('gap', 0), u.get('max_gap', 0.25)) * FPS) / FPS)
        cam = u.get('cam', 'auto')
        c1_ok = 0 <= u['a'] - SYNC['cam1'] and u['b'] - SYNC['cam1'] <= CAM1_DUR
        if cam == 'auto':
            cam = ('c1' if alt % 3 != 2 else 'c2') if c1_ok else 'c2'
            alt += 1
        if cam == 'c1' and not c1_ok:
            cam = 'c2'
        if not cfg.get('c2_available', True):
            cam = 'c1'
        tl.append(dict(u, cam=cam, t=t, d=d))
        t += d + u['gap']
    total = t + (edl.get('tail', 4.0) if edl.get('end') else 0.0)
    json.dump([{k: u[k] for k in ('id', 't', 'd', 'segs', 'gap') if k in u} for u in tl], open(os.path.join(WORK, 'timeline.json'), 'w'))

    # ---------- video pieces ----------
    pieces = []  # (file, dur)
    zstate = [0]

    def face(u, o0, o1):
        """face pieces for output range [o0,o1) of unit u (relative), one per speech run: every jump cut alternates framing"""
        oc = 0.0
        for k, (sa, sb) in enumerate(u['segs']):
            d = sb - sa; s0, s1 = max(o0, oc), min(o1, oc + d)
            last = k == len(u['segs']) - 1
            if last and o1 > oc + d:          # the unit's trailing gap holds on the last run
                s1 = o1
            if s1 > s0 + 1e-6:
                base = u.get('zoom')
                z = base if base is not None else (1.0, 1.16, 1.0, 1.3)[zstate[0] % 4]
                zstate[0] += 1
                src_a = sa + (s0 - oc)
                pieces.append((piece(u['cam'], src_a, src_a + (s1 - s0), z, u.get('look'), tuple(u.get('c', cfg['face'][u['cam']]))), s1 - s0))
            oc += d

    for u in tl:
        full = u['d'] + u['gap']
        over = u.get('broll') or u.get('ins')
        if over:
            lead = round(over.get('lead', 0.0) * FPS) / FPS
            if lead > 0:
                face(u, 0, lead)
            rest = full - lead
            pieces.append(((broll(u['broll'], rest) if u.get('broll') else insert(u['ins'], rest)), rest))
        else:
            face(u, 0, full)
    end = edl.get('end')
    if end:
        pieces.append((insert(end, edl.get('tail', 4.0)), edl.get('tail', 4.0)))
    # whip transitions (El-Dahih / Abu-Al-Sadiq style): wherever the picture source changes
    # (face <-> B-roll <-> graphic, or cam1 <-> cam2) the cut gets a short horizontal smear + whoosh
    def kind(path):
        b = os.path.basename(path)
        return b[:2]
    whips = []; tt = 0.0
    for (p0, d0), (p1, _d1) in zip(pieces, pieces[1:]):
        tt += d0
        k0, k1 = kind(p0), kind(p1)
        cam_change = k0 == k1 == 'p_' and piece_cam.get(p0) != piece_cam.get(p1)
        if k0 != k1 or cam_change:
            whips.append(round(tt, 3))
    lst = os.path.join(WORK, 'concat.txt')
    with open(lst, 'w') as f:
        for p, d in pieces:
            f.write(f"file '{p}'\nduration {d:.4f}\n")
    vcat = os.path.join(WORK, 'vcat.mp4')
    # re-time every piece to exact frame counts so audio and video never drift
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', f'fps={FPS},setpts=N/{FPS}/TB',
         '-c:v', 'libx264', '-preset', 'faster', '-crf', '15', '-an', vcat])

    # ---------- voice ----------
    voice = np.zeros(int(total * sr) + sr)
    cover = np.zeros_like(voice)
    fade = int(0.02 * sr)
    rin = np.sin(np.linspace(0, np.pi / 2, fade)) ** 2
    for u in tl:
        oc = u['t']
        for sa, sb in u['segs']:
            seg = vx[max(0, int((sa - voff) * sr)):int((sb - voff) * sr)].copy()
            if len(seg) > 2 * fade:
                seg[:fade] *= rin; seg[-fade:] *= rin[::-1]
            i = int(oc * sr); j = min(len(voice), i + len(seg))
            voice[i:j] += seg[:j - i]; cover[i:j] = 1.0
            oc += sb - sa
    # room tone under the gaps so silence never drops to digital zero
    qi = int(np.argmin(np.convolve(env, np.ones(100) / 100, 'same')[50:-50])) + 50
    tone = vx[max(0, (qi - 50) * hop):(qi + 50) * hop]
    if len(tone) > sr // 4:
        loop = np.tile(tone, len(voice) // len(tone) + 1)[:len(voice)]
        g = np.convolve(1 - cover, np.ones(int(0.08 * sr)) / int(0.08 * sr), 'same')
        voice += loop * g * 0.9
    vpath = os.path.join(WORK, 'voice.wav')
    with wave.open(vpath, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())

    # ---------- music + sfx ----------
    mus = {k: wav_read(os.path.join(ROOT, 'public', 'music', f'{k}.wav'))[0] for k in ('calm', 'tension', 'finale')}
    msr = 48000
    bed = np.zeros(int(total * msr) + msr)
    cue, start = edl.get('music0', 'calm'), 0.0
    changes = [(u['t'], u['music']) for u in tl if u.get('music')] + [(total, None)]
    for tc, nxt in changes:
        if cue != 'none' and tc > start:
            src = mus[cue]; n = int((tc - start) * msr)
            loop = np.tile(src, n // len(src) + 1)[:n].copy()
            f = int(1.5 * msr); m = min(f, n // 2)
            loop[:m] *= np.linspace(0, 1, m); loop[-m:] *= np.linspace(1, 0, m)
            i = int(start * msr); bed[i:i + n] += loop
        cue, start = (nxt or cue), tc
    sfx = np.zeros_like(bed)
    wsx, _ = wav_read(os.path.join(ROOT, 'public', 'sfx', 'whoosh.wav'))
    for tw in whips:
        i = int((tw - 0.35) * msr); j = min(len(sfx), i + len(wsx))
        if i >= 0:
            sfx[i:j] += wsx[:j - i] * 0.22
    for u in tl:
        for name, off, vol in u.get('sfx', []):
            s, _ = wav_read(os.path.join(ROOT, 'public', 'sfx', f'{name}.wav'))
            i = int(out_time(u, u['a'] + off) * msr); j = min(len(sfx), i + len(s)); sfx[i:j] += s[:j - i] * vol
    for name, path in (('bed', bed), ('sfx', sfx)):
        with wave.open(os.path.join(WORK, f'{name}.wav'), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(msr)
            w.writeframes((np.clip(path, -1, 1) * 32767).astype(np.int16).tobytes())

    # ---------- captions (ASS) ----------
    ass = os.path.join(WORK, 'captions.ass')
    write_ass(tl, ass, cfg.get('words'))

    # ---------- final mix + encode ----------
    logo = os.path.join(ROOT, 'public', 'logo.png')
    fc = (
        # voice: clean-up chain (manual EQ/compression, no AI enhancement)
        f"[1:a]aresample=48000,highpass=f=80,lowpass=f=12000,afftdn=nf=-28,acompressor=threshold=-22dB:ratio=3:attack=8:release=120,"
        f"loudnorm=I=-16:TP=-1.5:LRA=8,asplit=2[vo][vk];"
        # music ducks under the voice: base level ~0.11, ~0.06 under speech
        f"[2:a]volume=0.11[m];[m][vk]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[md];"
        f"[3:a]volume=0.8[sx];"
        f"[vo][md][sx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a];"
        f"[4:v]scale=110:110[lg];"
        f"[0:v]{whip_filter(whips)}ass='{ass}':fontsdir='{os.path.join(ROOT, 'public', 'fonts')}':shaping=complex[sv];"
        f"[sv][lg]overlay=x=60*{W}/1920:y=50*{H}/1080:enable='between(t,3,{total - (edl.get('tail', 4.0) if edl.get('end') else 0):.2f})':format=auto,format=yuv420p[v]"
    )
    fc = fc.replace('scale=110:110', f'scale={int(110 * W / 1920)}:{int(110 * W / 1920)},format=rgba,colorchannelmixer=aa=0.85')
    enc = ['-c:v', 'libx264', '-preset', 'medium' if not preview else 'veryfast', '-crf', '18' if not preview else '24',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart']
    run(['ffmpeg', '-v', 'error', '-y', '-i', vcat, '-i', vpath, '-i', os.path.join(WORK, 'bed.wav'), '-i', os.path.join(WORK, 'sfx.wav'),
         '-loop', '1', '-i', logo, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', *enc, out_path])
    print('built', out_path, f'{total / 60:.1f} min', len(tl), 'units')


def out_time(u, src_t):
    """map a source (master) time inside unit u to the output timeline after silence removal"""
    oc = u['t']
    for sa, sb in u['segs']:
        if src_t < sa:
            return oc
        if src_t <= sb:
            return oc + (src_t - sa)
        oc += sb - sa
    return oc


def whip_filter(whips):
    if not whips:
        return ''
    # 0.1 s each side of the cut: strong horizontal blur (motion smear), slightly brighter
    en = '+'.join(f'between(t,{w - 0.1:.3f},{w + 0.1:.3f})' for w in whips)
    return f"avgblur=sizeX=70:sizeY=1:enable='{en}',eq=brightness=0.06:enable='{en}',"


def ts(x):
    hh = int(x // 3600); mm = int(x % 3600 // 60); ss = x % 60
    return f'{hh}:{mm:02d}:{ss:05.2f}'


def write_ass(tl, path, _words):
    """caption = corrected text, split into chunks of <=5 words, spread across the unit's duration
    weighted by word length. Bottom-centre, below the chin, Cairo ExtraBold, bone on translucent night box."""
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Cairo Cap,100,&H00D6E2E8,&H0041A4D9,&H00101210,&H96101210,0,0,0,0,100,100,0,0,3,22,0,2,240,240,80,1
Style: Key,Cairo Cap,100,&H0041A4D9,&H0041A4D9,&H00101210,&H96101210,0,0,0,0,100,100,0,0,3,22,0,2,240,240,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for u in tl:
        txt = (u.get('text') or '').strip()
        if not txt or u.get('ins') and not u.get('cap_on_insert'):
            continue
        for ch in ('…', '...', '.', ':', '؟', '?', '!'):
            txt = txt.replace(ch, ' ')
        txt = txt.replace('،', ' ').replace(',', ' ')
        words = txt.split()
        chunks = [words[i:i + 5] for i in range(0, len(words), 5)]
        wts = [sum(len(w) for w in c) + 2 for c in chunks]
        tot = sum(wts); t0 = u['t'] + 0.05
        for c, wt in zip(chunks, wts):
            d = (u['d'] - 0.1) * wt / tot
            s = ' '.join(c)
            # libass reorders RTL runs split by inline colour tags, so a key line is coloured as a whole
            if any(k in s for k in u.get('key', [])):
                s = '{\\c&H0041A4D9&}' + s
            lines.append(f'Dialogue: 0,{ts(t0)},{ts(t0 + d)},Cap,,0,0,0,,{s}')
            t0 += d
    open(path, 'w').write(hdr + '\n'.join(lines) + '\n')


if __name__ == '__main__':
    build(os.path.join(ROOT, 'scripts', sys.argv[1]), sys.argv[2], '--preview' in sys.argv)
