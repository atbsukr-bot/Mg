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
   "mute": true,                     no voice under this unit (cards), room tone only
  }
Usage: python3 scripts/build.py edl_A.json out/ep002_A.mp4 [--preview] [--assets]
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
GAZE = json.load(open(os.path.join(WORK, 'gaze.json'))) if os.path.exists(os.path.join(WORK, 'gaze.json')) else []


MIN_LOOK = 0.6   # a look shorter than this is a glance: it does not get its own cut


def gaze_split(a, b, cam0):
    """split master range [a,b) into (a, b, cam) parts by where the owner is looking (work/gaze.json, 0.2 s samples).
    cam1 is only used inside its recording; parts shorter than MIN_LOOK merge into the previous part.
    Split points sit on frame boundaries so the concat timing stays exact."""
    c1_ok = lambda t0, t1: 0 <= t0 - SYNC['cam1'] and t1 - SYNC['cam1'] <= CAM1_DUR
    if not GAZE or not cfg.get('c2_available', True):
        return [(a, b, cam0 if c1_ok(a, b) else 'c2')]
    lab = [(t, l) for t, l, *_ in GAZE if a <= t < b]
    if not lab:
        return [(a, b, cam0 if c1_ok(a, b) else 'c2')]
    runs = []   # [start, cam]
    for t, l in lab:
        if not runs or runs[-1][1] != l:
            runs.append([max(a, t - 0.1) if runs else a, l])
    parts = []
    for i, (s, l) in enumerate(runs):
        e = runs[i + 1][0] if i + 1 < len(runs) else b
        s = a + round((s - a) * FPS) / FPS; e = b if i + 1 == len(runs) else a + round((e - a) * FPS) / FPS
        if parts and (e - s < MIN_LOOK or parts[-1][2] == l):
            parts[-1][1] = e
        else:
            parts.append([s, e, l])
    if len(parts) > 1 and parts[0][1] - parts[0][0] < MIN_LOOK:   # a short first part joins the next one
        parts[1][0] = parts[0][0]; parts.pop(0)
    out = []
    for s, e, l in parts:
        if e - s < 1 / FPS:
            continue
        if l == 'c1' and not c1_ok(s, e):
            l = 'c2'
        if out and out[-1][2] == l:
            out[-1] = (out[-1][0], e, l)
        else:
            out.append((s, e, l))
    return out or [(a, b, cam0)]


AWAY = 18.0   # off-axis score (deg-ish) above which he is not looking into the camera that is filming


def away_split(a, b):
    """cam2-only stretch [a,b): (a, b, away?) parts. A look away from the lens shorter than MIN_LOOK stays on the face;
    a face moment shorter than MIN_LOOK between two look-aways is covered too (no flicker)."""
    smp = [(t, o2) for t, _l, _o1, o2, *_ in GAZE if a <= t < b]
    if not smp:
        return [(a, b, False)]
    runs = []
    for t, o2 in smp:
        aw = o2 is not None and o2 > AWAY
        if not runs or runs[-1][1] != aw:
            runs.append([max(a, t - 0.1) if runs else a, aw])
    parts = []
    for i, (st, aw) in enumerate(runs):
        e = runs[i + 1][0] if i + 1 < len(runs) else b
        st = a + round((st - a) * FPS) / FPS; e = b if i + 1 == len(runs) else a + round((e - a) * FPS) / FPS
        if parts and (e - st < MIN_LOOK or parts[-1][2] == aw):
            parts[-1][1] = e
        else:
            parts.append([st, e, aw])
    if len(parts) > 1 and parts[0][1] - parts[0][0] < MIN_LOOK:
        parts[1][0] = parts[0][0]; parts.pop(0)
    return [tuple(x) for x in parts if x[1] - x[0] >= 1 / FPS]


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


VSHIFT = cfg.get('vshift', {})   # per-camera picture offset vs the voice (lip sync), seconds


def cam_input(cam, t_master):
    if cam == 'c1':
        return os.path.join(SRC, cfg['cam1_file']), t_master - SYNC['cam1'] + VSHIFT.get('c1', 0.0)
    return os.path.join(SRC, cfg['cam2_file']), t_master + VSHIFT.get('c2', 0.0)


piece_cam = {}
_cascade = None


def face_center(src, t, cam):
    """punch-ins follow the face: detect it in one frame and centre the crop there (None if not found)"""
    global _cascade
    try:
        import cv2
    except ImportError:
        return None
    if _cascade is None:
        _cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    w, hh = 960, 540
    pre = ['-noautorotate'] if cam == 'c2' else []
    raw = subprocess.run(['ffmpeg', '-v', 'quiet', *pre, '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', f'scale={w}:{hh},format=gray',
                          '-f', 'rawvideo', '-'], capture_output=True).stdout
    if len(raw) < w * hh:
        return None
    g = np.frombuffer(raw[:w * hh], np.uint8).reshape(hh, w)
    f = _cascade.detectMultiScale(g, 1.1, 5, minSize=(50, 50))
    if len(f) == 0:
        return None
    x, y, fw, fh = max(f, key=lambda r: r[2] * r[3])
    # centre a little below the eyes so the chin and shoulders stay in a tight shot
    return ((x + fw / 2) / w, min(0.62, (y + fh * 0.75) / hh))


def frames_ok(path, n):
    """a cached piece is only reused if it is complete (a killed render once left a 22-frame piece that should have had 97)"""
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets',
                        '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip().split(',')[0]
    return r.isdigit() and int(r) == n


def piece(cam, a, b, zoom, look, crop_c, hold=False):
    """render one camera piece (video only) to an intermediate clip"""
    src, t0 = cam_input(cam, a)
    # cache key in camera-local time, so re-syncing the master clock reuses rendered pieces
    key = h('p6', cam, round(t0, 3), round(b - a, 3), zoom, look, crop_c, GRADE.get(cam), *(['hold'] if hold else []))
    out = os.path.join(WORK, f'p_{key}.mp4')
    if os.path.exists(out) and frames_ok(out, round((b - a) * FPS)):
        piece_cam[out] = cam
        return out
    cx, cy = crop_c
    if zoom > 1.001:
        fc = face_center(src, t0 + min(0.5, (b - a) / 2), cam)
        if fc:
            cx, cy = fc
    vf = []
    if cam == 'c2':
        vf.append('null')  # cam2 is read with -noautorotate (sensor is landscape; the rotate flag is wrong)
    vf.append(f'fps={FPS}')
    if hold:   # one frame, held (a pause where the source has him already talking)
        vf.append(f'trim=end_frame=1,tpad=stop_mode=clone:stop={max(0, round((b - a) * FPS) - 1)}')
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
    out = os.path.join(WORK, f"{'c' if br.get('cover') else 'b'}_{key}.mp4")
    if os.path.exists(out) and normalised(out, n):
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


def normalised(path, n):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=time_base', '-of', 'csv=p=0', path],
                       capture_output=True, text=True).stdout.strip().split(',')[0]
    return r == '1/15360' and frames_ok(path, n)


def clip_piece(path, dur):
    """a finished clip (the channel intro: logo + music) shown full-frame; its sound is mixed in by the sfx pass"""
    n = round(dur * FPS)
    out = os.path.join(WORK, f"i_clip_{h('c1', path, n)}.mp4")
    if os.path.exists(out) and normalised(out, n):
        return out
    run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(ROOT, path), '-vf', f'fps={FPS},scale={W}:{H}:flags=lanczos,format=yuv420p,tpad=stop_mode=clone:stop=60',
         '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'faster', '-crf', '15', '-video_track_timescale', '15360', out])
    return out


def insert(ins, dur):
    props = dict(ins.get('props', {}), dur=round(dur * FPS))
    key = h('i3', ins['id'], props)
    out = os.path.join(WORK, f'i_{key}.mp4')
    if os.path.exists(out) and not normalised(out, props['dur']):
        os.remove(out)          # a render stopped between Remotion and normalisation leaves a raw file: it broke the concat once
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


def build(edl_path, out_path, preview=False, assets_only=False):
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
        segs = [(u['a'], u['b'])] if (u.get('keep_pauses') or (u.get('ins') or u.get('clip')) and not u.get('text')) else tighten(u['a'], u['b'])
        segs = [(sa, sa + max(1, round((sb - sa) * FPS)) / FPS) for sa, sb in segs]
        d = sum(sb - sa for sa, sb in segs)
        u = dict(u, segs=segs, gap=round(min(u.get('gap', 0), u.get('max_gap', 0.25)) * FPS) / FPS)
        cam = u.get('cam', 'auto')
        c1_ok = 0 <= u['a'] - SYNC['cam1'] and u['b'] - SYNC['cam1'] <= CAM1_DUR
        if cam == 'auto':
            # owner's rule: the angle follows his eyes. gaze.json says which camera he faces at each moment
            g = [lab for tg, lab, *_ in GAZE if u['a'] <= tg <= u['b']]
            look2 = g and g.count('c2') > len(g) / 2
            cam = 'c2' if (look2 or not c1_ok) else 'c1'
            alt += 1
        if cam == 'c1' and not c1_ok:
            cam = 'c2'
        if not cfg.get('c2_available', True):
            cam = 'c1'
        tl.append(dict(u, cam=cam, t=t, d=d))
        t += d + u['gap']
    total = t + (edl.get('tail', 4.0) if edl.get('end') else 0.0)
    json.dump([{k: u[k] for k in ('id', 't', 'd', 'segs', 'gap') if k in u} for u in tl], open(os.path.join(WORK, 'timeline.json'), 'w'))

    if assets_only:   # pre-render graphics + B-roll (small) while the camera sources are still being prepared
        for u in tl:
            over = u.get('broll') or u.get('ins')
            if over:
                lead = round(over.get('lead', 0.0) * FPS) / FPS
                rest = u['d'] + u['gap'] - lead
                broll(u['broll'], rest) if u.get('broll') else insert(u['ins'], rest)
        print('assets ready', round(total / 60, 1), 'min', len(tl), 'units')
        return

    # ---------- video pieces ----------
    pieces = []  # (file, dur)
    zstate = [0]
    covers = edl.get('cover', [])      # [[from_master_s, [clip, ...]], ...]
    cstate = [0]

    def cover_shot(t, dur):
        pool = [c for t0, c in covers if t >= t0][-1] if any(t >= t0 for t0, _ in covers) else covers[0][1]
        k = cstate[0]; cstate[0] += 1
        src = pool[k % len(pool)]
        sd = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                   os.path.join(ROOT, 'public', 'broll', src)], capture_output=True, text=True).stdout)
        span = max(0.1, sd - dur - 0.3)
        ss = round((k // len(pool)) * 3.3 % span, 2)       # each reuse of a clip starts further in
        return dict(src=src, ss=ss, look='night', frame=False, cover=True, zoom=(1.04, 1.14) if k % 2 else (1.14, 1.04))

    def face(u, o0, o1):
        """face pieces for output range [o0,o1) of unit u (relative), one per speech run: every jump cut alternates framing"""
        oc = 0.0
        for k, (sa, sb) in enumerate(u['segs']):
            d = sb - sa; s0, s1 = max(o0, oc), min(o1, oc + d)
            last = k == len(u['segs']) - 1
            gap_out = (o1 - (oc + d)) if (last and o1 > oc + d) else 0.0   # the unit's trailing dramatic gap
            if s1 > s0 + 1e-6:
                src_a = sa + (s0 - oc)
                # owner's rule: the shot is always the camera he is looking into, switching mid-sentence if his eyes do
                for ca, cb, cam in gaze_split(src_a, src_a + (s1 - s0), u['cam']):
                    c1_ok = 0 <= ca - SYNC['cam1'] and cb - SYNC['cam1'] <= CAM1_DUR
                    sub = away_split(ca, cb) if (cam == 'c2' and not c1_ok and covers) else [(ca, cb, False)]
                    for pa, pb, aw in sub:
                        if aw:
                            # owner's rule: never on screen looking away from the lens. cam1 (the camera he is
                            # looking into) had stopped, so this moment is covered with a B-roll shot; the voice runs on
                            pieces.append((broll(cover_shot(pa, pb - pa), pb - pa), pb - pa))
                            continue
                        base = u.get('zoom')
                        z = base if base is not None else (1.0, 1.16, 1.0, 1.3)[zstate[0] % 4]
                        zstate[0] += 1
                        pieces.append((piece(cam, pa, pb, z, u.get('look'), tuple(u.get('c', cfg['face'][cam]))), pb - pa))
                        held = (cam, pb, z)
            if gap_out > 1e-6 and s1 >= oc + d - 1e-6:
                cam_h, pb, z = held
                i0 = max(0, int((pb - voff) * 100)); i1 = int((pb + gap_out - voff) * 100)
                talking = (env[i0:i1] > thr).mean() > 0.1 if i1 > i0 else False
                # owner, 5 Nov: "the words don't follow my mouth" - in a pause the source often has him already saying the
                # next (cut) line, so his lips moved with no sound. Live footage only if he is silent there; else hold a frame
                pieces.append((piece(cam_h, pb, pb + gap_out, z, u.get('look'), tuple(u.get('c', cfg['face'][cam_h])), hold=talking), gap_out))
            oc += d

    for u in tl:
        full = u['d'] + u['gap']
        over = u.get('broll') or u.get('ins')
        if u.get('clip'):
            pieces.append((clip_piece(u['clip'], full), full))
            continue
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
        # angle changes between the two cameras follow his eyes and are clean cuts (identity card #002); whips only on source changes
        if k0 != k1 and {k0, k1} != {'p_', 'c_'}:
            whips.append(round(tt, 3))
    face_rng, tt = [], 0.0
    for p, d in pieces:
        if kind(p) == 'p_':
            if face_rng and abs(face_rng[-1][1] - tt) < 1e-3:
                face_rng[-1][1] = tt + d
            else:
                face_rng.append([tt, tt + d])
        tt += d
    lst = os.path.join(WORK, 'concat.txt')
    with open(lst, 'w') as f:
        for p, d in pieces:
            f.write(f"file '{p}'\nduration {d:.4f}\n")
    # no intermediate concat file (it was ~7 GB and a whole extra encode): the final pass reads the pieces directly

    # ---------- voice ----------
    voice = np.zeros(int(total * sr) + sr)
    cover = np.zeros_like(voice)
    fade = int(0.02 * sr)
    rin = np.sin(np.linspace(0, np.pi / 2, fade)) ** 2
    for u in tl:
        if u.get('mute'):   # chapter cards / black screen: room tone only, never stray set noise
            continue
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
    if edl.get('end'):
        # owner, 5 Nov: "at the end the sound disappears" - after the last line only the ducked bed (0.075) was left under the
        # end card. Bring the score up there (x3.5 = ~0.26) and let it fade out over the last 1.5 s
        t0 = int((total - edl.get('tail', 4.0)) * msr); r = int(0.8 * msr)
        g = np.ones(len(bed)); g[t0:t0 + r] = np.linspace(1, 5.0, r); g[t0 + r:] = 5.0
        bed *= g
    sfx = np.zeros_like(bed)
    wsx, _ = wav_read(os.path.join(ROOT, 'public', 'sfx', 'whoosh.wav'))
    for tw in whips:
        i = int((tw - 0.35) * msr); j = min(len(sfx), i + len(wsx))
        if i >= 0:
            sfx[i:j] += wsx[:j - i] * 0.12
    for u in tl:
        if u.get('clip'):   # the intro's own music / logo sting
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(ROOT, u['clip']), '-vn', '-ac', '1', '-ar', str(msr), '-f', 's16le', '-'],
                                 capture_output=True).stdout
            s_ = np.frombuffer(raw, np.int16).astype(np.float32) / 32768 / 0.42   # undo the sfx bus trim: the intro plays at its own level
            i = int(u['t'] * msr); j = min(len(sfx), i + len(s_)); sfx[i:j] += s_[:j - i]
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
        f"[1:a]aresample=48000,highpass=f=85,equalizer=f=280:t=q:w=1:g=-2,equalizer=f=2600:t=q:w=1.3:g=3.5,"
        # owner, 5 Nov: the +7/+5/+4 dB presence boost sounded sharp -> gentle +3.5 dB clarity, de-esser, nothing above 4 kHz
        f"deesser=i=0.4:m=0.5:f=0.5,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=150,"
        f"loudnorm=I=-15:TP=-1.5:LRA=8,aresample=48000,asplit=2[vo][vk];"
        # music ducks under the voice: base level ~0.11, ~0.06 under speech
        f"[2:a]volume=0.075[m];[m][vk]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[md];"
        f"[3:a]volume=0.42[sx];"
        f"[vo][md][sx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a];"
        f"[4:v]scale=110:110[lg];"
        f"[0:v]setpts=N/{FPS}/TB,{handheld(face_rng)}{whip_filter(whips)}ass='{ass}':fontsdir='{os.path.join(ROOT, 'public', 'fonts')}':shaping=complex[sv];"
        f"[sv][lg]overlay=x={W}-60*{W}/1920-{int(110 * W / 1920)}:y=50*{H}/1080:enable='between(t,3,{total - (edl.get('tail', 4.0) if edl.get('end') else 0):.2f})':format=auto,format=yuv420p[v]"
    )
    fc = fc.replace('scale=110:110', f'scale={int(110 * W / 1920)}:{int(110 * W / 1920)},format=rgba,colorchannelmixer=aa=0.85')
    enc = ['-c:v', 'libx264', '-preset', 'medium' if not preview else 'veryfast', '-crf', '18' if not preview else '24',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart']
    # -noautorotate: cam2 pieces carry the phone's (wrong) rotate flag; never let it turn the whole video portrait
    # owner's subscribe / bell / like / share animation over the face shot (below the face), wherever a unit asks for it
    subs = [u['t'] + 0.3 for u in tl if u.get('subscribe')]
    sub_in = []
    if subs:
        sub_mov = os.path.join(WORK, 'sub_overlay.mov')
        if not os.path.exists(sub_mov):
            run(['npx', 'remotion', 'render', 'src/index.ts', 'SubscribeOverlay', sub_mov, '--props', '{"dur":120}', '--codec=prores',
                 '--prores-profile=4444', '--image-format=png', '--pixel-format=yuva444p10le', '--log=error'], cwd=ROOT)
        for k, ts_ in enumerate(subs):
            sub_in += ['-itsoffset', f'{ts_:.3f}', '-i', sub_mov]
            fc = fc.replace('format=yuv420p[v]', f'format=yuva420p[v{k}];[v{k}][{5 + k}:v]overlay=eof_action=pass:format=auto,format=yuv420p[v]')
    run(['ffmpeg', '-v', 'error', '-y', '-noautorotate', '-f', 'concat', '-safe', '0', '-i', lst, '-i', vpath, '-i', os.path.join(WORK, 'bed.wav'), '-i', os.path.join(WORK, 'sfx.wav'),
         '-loop', '1', '-i', logo, *sub_in, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', *enc, out_path])
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


def handheld(rng):
    """owner's style: a handheld feel on every face shot (slow drift + base push 1.06), none on graphics / B-roll"""
    if not rng:
        return ''
    F = '+'.join(f'between(t,{a:.3f},{b - 0.001:.3f})' for a, b in rng)
    z = f"(1+({F})*(0.06+0.012*sin(t*0.37)))"
    dx = f"(({F})*(9*sin(t*1.13)+5*sin(t*2.71)))"
    dy = f"(({F})*(6*sin(t*0.91+1.3)+4*sin(t*2.17)))"
    return (f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame:flags=bicubic,"
            f"crop={W}:{H}:x='(iw-{W})/2+{dx}':y='(ih-{H})/2+{dy}',")


def whip_filter(whips):
    if not whips:
        return ''
    # 0.1 s each side of the cut: strong horizontal blur (motion smear), slightly brighter
    en = '+'.join(f'between(t,{w - 0.1:.3f},{w + 0.1:.3f})' for w in whips)
    return f"avgblur=sizeX=70:sizeY=1:enable='{en}',eq=brightness=0.06:enable='{en}',"


def ts(x):
    hh = int(x // 3600); mm = int(x % 3600 // 60); ss = x % 60
    return f'{hh}:{mm:02d}:{ss:05.2f}'


def cap_chunks(txt, keys):
    """owner's caption style: 2-4 words per line; the key phrase is its own line (red box).
    -> [(words, is_key), ...]"""
    words = txt.split()
    marks = [False] * len(words)
    for k in keys:
        kw = k.replace('،', ' ').replace('…', ' ').split()
        for i in range(len(words) - len(kw) + 1):
            if [w.strip('،.؟?!:…') for w in words[i:i + len(kw)]] == kw:
                for j in range(i, i + len(kw)):
                    marks[j] = True
                break
    out, i = [], 0
    while i < len(words):
        j = i
        while j < len(words) and marks[j] == marks[i]:
            j += 1
        run = words[i:j]
        if marks[i]:
            out.append((run, True))
        else:
            n = len(run)
            k = 0
            while k < n:
                left = n - k
                step = left if left <= 4 else (3 if left != 5 else 3)
                if left - step == 1:
                    step -= 1
                out.append((run[k:k + step], False)); k += step
        i = j
    return out


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
Style: Cap,Cairo Cap,100,&H00FFFFFF,&H00FFFFFF,&H00141414,&H80000000,0,0,0,0,100,100,0,0,1,7,3,2,240,240,80,1
Style: Banner,Cairo Cap,74,&H00141414,&H00141414,&H003FD2FF,&H803FD2FF,0,0,0,0,100,100,0,0,3,26,0,8,240,240,70,1
Style: Key,Cairo Cap,104,&H00FFFFFF,&H00FFFFFF,&H002A26E3,&H962A26E3,0,0,0,0,100,100,0,0,3,24,0,2,240,240,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for u in tl:
        if u.get('banner'):
            lines.append(f"Dialogue: 1,{ts(u['t'] + 0.2)},{ts(u['t'] + 7.0)},Banner,,0,0,0,,{{\\fad(300,300)}}{u['banner']}")
        txt = (u.get('text') or '').strip()
        if not txt:
            continue
        # a full-screen graphic carries its own text: captions only run over the face lead-in before it (clean graphic)
        cap_end = u['t'] + u['d']
        if u.get('ins') and not u.get('cap_on_insert'):
            cap_end = u['t'] + round(u['ins'].get('lead', 0.0) * FPS) / FPS
            if cap_end <= u['t'] + 0.3:
                continue
        for ch in ('…', '...', '.', ':', '؟', '?', '!'):
            txt = txt.replace(ch, ' ')
        txt = txt.replace('،', ' ').replace(',', ' ')
        chunks = cap_chunks(txt, u.get('key', []))
        wts = [sum(len(w) for w in c) + 2 for c, _k in chunks]
        tot = sum(wts); t0 = u['t'] + 0.05
        for (c, is_key), wt in zip(chunks, wts):
            d = (u['d'] - 0.1) * wt / tot
            if t0 < cap_end - 0.2:
                lines.append(f"Dialogue: 0,{ts(t0)},{ts(min(t0 + d, cap_end))},{'Key' if is_key else 'Cap'},,0,0,0,,{' '.join(c)}")
            t0 += d
    open(path, 'w').write(hdr + '\n'.join(lines) + '\n')


if __name__ == '__main__':
    build(os.path.join(ROOT, 'scripts', sys.argv[1]), sys.argv[2], '--preview' in sys.argv, '--assets' in sys.argv)
