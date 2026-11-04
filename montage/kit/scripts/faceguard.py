"""Face guard: no graphic may cover his face.
Reads app/public/edl.json + raw/face.json + raw/pieces.json, estimates the on-screen face box for every frame
(after the camera zoom/pan of Main.tsx) and each item's box, and moves any item that overlaps the face
to the first free candidate spot (mirror side, lower, smaller). Rewrites edl.json in place and prints a report.
usage: python3 faceguard.py [--check]   (--check = report only)"""
import json, sys, math
PUB = '/home/claude/proj/app/public/'
E = json.load(open(PUB + 'edl.json'))
FACE = json.load(open('/home/claude/proj/raw/face.json'))
P = json.load(open('/home/claude/proj/raw/pieces.json'))['pieces']
FPS = 30; W, H = 1920, 1080
CHECK = '--check' in sys.argv
face_t = {round(x['t'] * 5): x for x in FACE}

def cam_at(f):
    cam = E['cam']; i = 0
    while i + 1 < len(cam) and cam[i + 1]['f'] <= f: i += 1
    a = cam[i]; b = cam[i + 1] if i + 1 < len(cam) else None
    if b and b.get('mode') == 'ease':
        d = b.get('dur', 20)
        if f > b['f'] - d:
            t = min(1, (f - (b['f'] - d)) / d); t = t * t * (3 - 2 * t)
            return a['s'] + (b['s'] - a['s']) * t, a['x'] + (b['x'] - a['x']) * t, a['y'] + (b['y'] - a['y']) * t
    return a['s'], a['x'], a['y']

def face_box(f):
    """screen-space face+head box at output frame f, or None (inserts / no face)."""
    t = f / FPS
    p = next((p for p in P if p['os'] <= t < p['oe']), None)
    if not p or p.get('src', 'raw') != 'raw': return None
    src = p['s'] + (t - p['os'])
    x = face_t.get(round(src * 5))
    if not x or not x.get('face'):
        for d in (1, -1, 2, -2, 3, -3):
            x = face_t.get(round(src * 5) + d)
            if x and x.get('face'): break
        else: return None
    s, cx, cy = cam_at(f)
    mx, my = (s - 1) * W / 2, (s - 1) * H / 2
    tx = max(-mx, min(mx, cx * s)); ty = max(-my, min(my, cy * s))
    fx, fy, fw = x['cx'] * W, x['cy'] * H, x['w'] * W
    bw, bh = fw * 1.25, fw * 1.75            # whole head incl. forehead/chin
    sx = W / 2 + (fx - W / 2) * s + tx; sy = H / 2 + (fy - fw * 0.15 - H / 2) * s + ty
    return (sx - bw * s / 2 - 25, sy - bh * s / 2 - 25, sx + bw * s / 2 + 25, sy + bh * s / 2 + 25)

DEF = {'raw': (1430, 470), 'checklist': (1460, 470), 'phone': (1450, 540), 'ref': (1430, 470), 'prompt': (960, 300), 'editor': (1380, 460),
       'notes': (1450, 470), 'skill': (1430, 480), 'branch': (1380, 500), 'counter': (1600, 900), 'badge': (960, 120), 'notice': (960, 500), 'subscribe': (960, 800)}
def item_box(it):
    t = it['type']; dx, dy = DEF.get(t, (960, 540)); x, y = it.get('x', dx), it.get('y', dy)
    if t == 'keyword':
        sz = it.get('size', 64); w = len(it['text']) * sz * 0.52 + sz * 1.0 + (sz * 1.4 if it.get('icon') else 0); h = sz * 1.45
    elif t == 'beat': sz = it.get('size', 230); w = len(it['text']) * sz * 0.6 + 30; h = sz * 1.15
    elif t == 'raw': w, h = 560, 480
    elif t == 'checklist': w, h = 520, 90 + 66 * len(it['items'])
    elif t == 'phone': hh = it.get('height', 860); w, h = hh * 0.4625 + 28, hh + 60
    elif t == 'wide': ww = it.get('w', 620); w, h = ww + 24, ww * 0.5625 + 70
    elif t == 'ref': w, h = 540, 340
    elif t == 'prompt': w, h = 980, 210
    elif t == 'editor': sc = it.get('scale', 1); w, h = 860 * sc, 340 * sc
    elif t == 'notes': w, h = 520, 80 + 56 * len(it['items'])
    elif t == 'skill': w, h = 560, 360
    elif t == 'branch': sc = it.get('scale', 1); w, h = 760 * sc, 520 * sc
    elif t == 'notice': sc = it.get('scale', 1); w, h = 1300 * sc, 400 * sc
    elif t == 'image': sz = it.get('size', 300); w, h = sz + 40, sz + 80
    elif t == 'badge': w, h = 700, 140
    elif t == 'counter': w, h = 460, 120
    elif t == 'subscribe': w, h = 1100, 130
    elif t == 'lower': return (1300, 740, 1830, 890)
    elif t == 'arrow':
        xs, ys = [it['x1'], it['x2']], [it['y1'], it['y2']]
        return (min(xs) - 40, min(ys) - 110, max(xs) + 40, max(ys) + 40)
    elif t in ('chords', 'tab', 'strings'): return None
    else: return None
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)

def overlap(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))

def hits(it, box=None):
    box = box or item_box(it)
    if not box: return 0
    n = 0
    for f in range(it['from'] + 4, it['from'] + it['dur'] - 4, 3):
        fb = face_box(f)
        if fb and overlap(box, fb) > 0: n += 1
    return n

def candidates(it):
    dx0, dy0 = DEF.get(it['type'], (960, 540)); x, y = it.get('x', dx0), it.get('y', dy0)
    if it['type'] == 'notice': return [(960, 790, 0.78), (960, 820, 0.7)]
    if it['type'] == 'subscribe': return [(960, 960, 1.0), (1380, 900, 1.0), (540, 900, 1.0), (960, 130, 1.0)]
    out = [(1460, 640, 1.0), (460, 640, 1.0)] if it['type'] in ('prompt', 'editor', 'branch', 'skill') else []
    if it['type'] in ('keyword', 'beat'): out += [(x, 860, 1.0), (W - x, 860, 1.0), (x, 700, 1.0), (W - x, 700, 1.0)]
    for dx in (0, None):
        nx = x if dx == 0 else W - x
        for ny in (y, y + 140, y - 120, y + 260, 760, 300):
            out.append((nx, ny, 1.0))
    for nx in (330, 1590): out.append((nx, 560, 0.85))
    for nx in (420, 1500): out += [(nx, 600, 0.72), (nx, 700, 0.62)]
    return out

MOVABLE = {'subscribe', 'keyword', 'beat', 'raw', 'checklist', 'phone', 'wide', 'ref', 'prompt', 'editor', 'notes', 'skill', 'branch', 'notice', 'counter'}
report = []
for it in E['items']:
    if it['type'] not in MOVABLE and it['type'] not in ('image', 'arrow', 'lower', 'subscribe', 'badge'): continue
    h = hits(it)
    if not h: continue
    if CHECK or it['type'] not in MOVABLE:
        report.append((it['from'], it['type'], it.get('text', ''), 'OVERLAP', h)); continue
    best = None
    for nx, ny, sc in candidates(it):
        trial = dict(it, x=nx, y=ny)
        if sc != 1.0:
            if trial['type'] in ('notice', 'editor', 'branch'): trial['scale'] = sc
            for k in ('size', 'height', 'w'):
                if k in trial: trial[k] = trial[k] * sc
        hb = hits(trial)
        b = item_box(trial)
        inside = b and b[0] > 10 and b[2] < W - 10 and b[1] > 10 and b[3] < H - (20 if trial['type'] in ('notice', 'subscribe') else 150)
        if hb == 0 and inside: best = trial; break
    if best:
        report.append((it['from'], it['type'], it.get('text', ''), f"moved {it.get('x')},{it.get('y')} -> {best['x']},{best['y']}", h))
        it.update(best)
    else:
        report.append((it['from'], it['type'], it.get('text', ''), 'NO FREE SPOT', h))
for r in report: print(r)
if not CHECK: json.dump(E, open(PUB + 'edl.json', 'w'), ensure_ascii=False)
print('items checked', len(E['items']), 'issues', len(report))
