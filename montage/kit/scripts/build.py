"""Build the cut list -> raw/pieces.json (then run cut.sh).
Each range: (src, start, end, kind, cutSilence)
  src  : 'raw' = the new raw footage (raw/raw.mov), or any other file inside raw/ (insert clips: intro, before/after, shorts...)
  kind : 'close' talking head | 'wide' guitar/wide shot | 'insert' full-screen clip from another file (camera stays still)
  cutSilence=False keeps the range whole (playing sections, inserts)
Ranges play in LIST ORDER, so you can move a sentence (e.g. a hook) to the start.
Only 'raw' pieces get captions / face camera / source-time mapping."""
import json, sys, numpy as np
db = np.load('/home/claude/proj/raw/rms.npy')  # 0.25 s hops of raw.mov audio

# ===== video 2 (skill promo, Oct 2026) - rebuild this list for every new video =====
RANGES = [
    ('raw', 13.1, 21.9, 'close', True),        # hook: ما لمست منه ولا ثانية
    ('raw', 4.5, 12.0, 'close', True),         # السلام عليكم
    ('intro.mp4', 0, 5.0, 'insert', False),    # channel intro with its sound
    ('raw', 57.7, 80.0, 'close', True),
    ('raw', 80.0, 92.8, 'close', True),        # كلاود حط ... هنا (pointing)
    ('raw', 94.2, 102.4, 'close', True),
    ('raw', 108.4, 147.3, 'close', True),      # how to build the skill
    ('raw', 147.3, 159.6, 'close', True),      # price
    ('raw', 159.6, 161.8, 'close', False),     # hold for the big 'usage limit' note
    ('raw', 167.7, 179.5, 'close', True),      # النتيجة قبل وبعد
    ('guitar_raw.mov', 194.0, 202.0, 'insert', False),    # BEFORE
    ('guitar_final.mp4', 64.0, 73.0, 'insert', False),    # AFTER
    ('raw', 179.8, 189.0, 'close', True),      # thumbnail + shorts
    ('shorts3.mp4', 0, 9.0, 'insert', False),  # 3 shorts playing
    ('raw', 190.2, 200.0, 'close', True),
    ('raw', 204.2, 220.9, 'close', True),
    ('raw', 221.6, 264.5, 'close', True),
    ('raw', 264.5, 287.7, 'close', True),
]

def speech_pieces(a, b, thr=-41.0, min_sil=0.4, pad=0.12):
    hop = 0.25
    i0, i1 = int(a / hop), int(b / hop)
    loud = db[i0:i1] > thr
    pieces, cur = [], None
    for k, l in enumerate(loud):
        t = (i0 + k) * hop
        if l and cur is None: cur = [t, t + hop]
        elif l: cur[1] = t + hop
        elif cur is not None and t - cur[1] >= min_sil:
            pieces.append(cur); cur = None
    if cur: pieces.append(cur)
    out = []
    for p in pieces:
        s, e = max(a, p[0] - pad), min(b, p[1] + pad)
        if e - s > 0.3: out.append([s, e])
    m = []
    for p in out:
        if m and p[0] <= m[-1][1] + 0.05: m[-1][1] = max(m[-1][1], p[1])
        else: m.append(p)
    return m

pieces = []
for src, a, b, kind, cut in RANGES:
    ps = speech_pieces(a, b) if (cut and src == 'raw') else [[a, b]]
    for s, e in ps:
        pieces.append({'src': src, 's': round(s, 3), 'e': round(e, 3), 'kind': kind, 'play': (kind == 'wide' and not cut)})
t = 0.0
for p in pieces:
    p['os'] = t; t += p['e'] - p['s']; p['oe'] = t
print('pieces', len(pieces), 'output sec', round(t, 1), file=sys.stderr)
json.dump({'pieces': pieces, 'total': t}, open('/home/claude/proj/raw/pieces.json', 'w'))
