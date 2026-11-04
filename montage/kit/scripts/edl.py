"""python3 edl.py [out.json] [limit_seconds]  -> app/public/<out>.json for the Main composition.
Times in CAPS / items are SOURCE seconds of raw.mov (s2o maps them to the cut). Insert clips are addressed with ins('<file>')."""
import json, sys
FPS = 30
P = json.load(open('/home/claude/proj/raw/pieces.json'))
pieces, total = P['pieces'], P['total']
RAWP = [p for p in pieces if p.get('src', 'raw') == 'raw']
T = json.load(open('/home/claude/proj/raw/transcript.json'))
WORDS = [w for s in T for w in s['words']]
FACE = json.load(open('/home/claude/proj/raw/face.json'))
LIMIT = float(sys.argv[2]) if len(sys.argv) > 2 else None
OUTNAME = sys.argv[1] if len(sys.argv) > 1 else 'edl.json'
F = lambda sec: int(round(sec * FPS))

def s2o(ts, snap=True):
    for p in RAWP:
        if p['s'] - 0.01 <= ts <= p['e'] + 0.01: return p['os'] + min(max(ts, p['s']), p['e']) - p['s']
    if not snap: return None
    best = min(RAWP, key=lambda p: min(abs(ts - p['s']), abs(ts - p['e'])))
    return best['os'] if abs(ts - best['s']) < abs(ts - best['e']) else best['oe']
def ins(src):  # output (start, end) seconds of an insert clip
    p = next(p for p in pieces if p.get('src') == src); return p['os'], p['oe']

# ---------- captions: Saudi wording as he said it; unclear sentences skipped ----------
CAPS = [
    (13.3, 16.9, 'الفيديو هذا اللي تشوفونه أنا ما لمست منه ولا ثانية', 'ثانية'),
    (17.1, 19.3, 'ما منتجته ما سويت أي شي', 'منتجته'),
    (19.4, 21.9, 'فقط رفعته على الدرايف', 'الدرايف'),
    (4.5, 6.7, 'السلام عليكم ورحمة الله وبركاته', 'السلام'),
    (7.3, 11.9, 'معكم ماجد في مقطع جديد', 'ماجد'),
    (57.7, 60.2, 'عزيزي المشاهد زي ما أنت تشوف', 'المشاهد'),
    (60.3, 62.9, 'الفيديو هذا أنا ما قصيته ما منتجته', 'قصيته'),
    (63.0, 65.4, 'ما قصيت السكتات ما سويت أي شي', 'السكتات'),
    (65.5, 70.8, 'ما لمست أي شي بالفيديو هذا ما لمست ولا ثانية منه', 'ثانية'),
    (70.9, 75.1, 'فقط أخذت الفيديو صورته ورفعته لكلاود', 'كلاود'),
    (75.2, 78.7, 'قلت يا كلاود منتج الفيديو هذا على طريقة ماجد', 'ماجد'),
    (78.8, 79.9, 'زي ما أنتم تشوفون', 'تشوفون'),
    (82.6, 85.0, 'يعني لما أقول كلاود حط شعار قناتي هنا', 'شعار'),
    (86.4, 88.1, 'بيطلع لكم شعار القناة هنا', 'القناة'),
    (88.2, 90.1, 'حط آخر فيديو نزلته هنا', 'فيديو'),
    (90.2, 92.6, 'بيحط لكم آخر فيديو نزلته هنا', 'نزلته'),
    (96.3, 98.7, 'يعني صناعة المحتوى حالياً أسهل', 'أسهل'),
    (108.5, 111.5, 'بكل بساطة كيف تبني السكيل؟', 'السكيل'),
    (111.6, 115.3, 'السكيل يا طويل العمر مو سالفة إنه يا كلاود منتج لي', 'سالفة'),
    (118.2, 122.9, 'فقط خذ فيديو أعجبك المونتاج فيه', 'أعجبك'),
    (123.0, 127.2, 'خذه وعطه كلاود قل يا كلاود سوّ نفس الفيديو', 'نفس'),
    (129.8, 133.9, 'ياخذ الفيديو الخام حقك ويمنتجه نفس الطريقة', 'الخام'),
    (134.1, 135.7, 'طبعاً أول مونتاج ما راح يكون كويس', 'كويس'),
    (136.2, 141.2, 'فتقول له عدّل كذا سوّ كذا الخط كذا اللون كذا', 'عدّل'),
    (142.3, 147.2, 'فتبني مهارة جديدة تعلمها مرة وحدة ويمنتج لك طول العمر', 'مرة'),
    (147.4, 149.9, 'بس أنا ما أتكلم عن المشتركين', 'المشتركين'),
    (155.2, 157.0, 'ترى كلها تسعين ريال تدفعها', 'ريال'),
    (157.1, 159.6, 'اشتراك شهري يمنتج لك عشرين فيديو لو تبغى', 'شهري'),
    (167.9, 169.9, 'وهنا كلاود راح يطلع لكم', 'كلاود'),
    (171.3, 172.6, 'النتيجة قبل وبعد', 'النتيجة'),
    (172.8, 174.8, 'يعني تشوفونا قبل وتشوفونا بعد', 'قبل'),
    (175.5, 177.0, 'أنا ما أدري ليش ماسك هذي من اليوم', 'ماسك'),
    (177.1, 179.4, 'فبطلع لكم النتيجة قبل وبعد', 'وبعد'),
    (179.9, 184.1, 'ويطلع لكم الصورة المصغرة اللي سواها لي برضو', 'المصغرة'),
    (184.2, 186.3, 'حتى الصورة المصغرة هو اللي سواها أنا ما سويت شي', 'سواها'),
    (186.3, 188.9, 'والثلاث شورتات هذي', 'شورتات'),
    (190.3, 191.8, 'كلها كلاود سواها', 'كلاود'),
    (191.9, 195.2, 'أنا بس أصوّر وأرفع الفيديو الخام', 'الخام'),
    (195.9, 197.3, 'على طريقة ماجد', 'ماجد'),
    (197.4, 199.9, 'انتهى الموضوع كذا', 'انتهى'),
    (204.3, 205.7, 'فالفكرة يا طويل العمر', 'الفكرة'),
    (205.8, 209.2, 'إنك أنت فقط تاخذ الشي اللي أعجبك', 'أعجبك'),
    (209.3, 212.0, 'يعني هو شي لازم تتعلم المهارة هذي', 'المهارة'),
    (212.1, 215.9, 'فإذا تعلمت المهارة هذي خلاص يخدمك فيها زي ما تبغى', 'يخدمك'),
    (216.1, 220.8, 'فإلى هنا هذا ختام الفيديو وإذا تبغون إن شاء الله', 'ختام'),
    (221.7, 224.3, 'نتعلم كيف نسوي مهارات لكلاود', 'مهارات'),
    (225.7, 228.3, 'والأخيرة طبعاً ترى كل اللي سويته', 'الأخيرة'),
    (228.4, 230.8, 'كل المقاطع اللي قاعد تشوفونها اللي نزلتها', 'المقاطع'),
    (232.8, 237.2, 'بالفترة الأخيرة كلها تصوير جوال ومونتاج عن طريق الجوال', 'الجوال'),
    (237.6, 240.8, 'أنا ما أسوي شي فقط أسلمها لكلاود', 'أسلمها'),
    (240.9, 245.2, 'كلاود يبدأ يسوي لي مونتاج وكل شي وأنا آخذه وأنزله', 'مونتاج'),
    (245.3, 253.0, 'حتى يوم آخذه وأنزله أروح لكلاود أقول يا كلاود تراني نزلت مقطع طويل ونزلت ثلاث شورتات', 'شورتات'),
    (253.1, 259.6, 'فهو اللي يحط لكم العناوين هو اللي يحط الدسكربشن هو اللي يحط كل شي', 'العناوين'),
    (259.7, 263.4, 'أنا فقط أقعد أتابع وأرد على كومنتاتكم', 'كومنتاتكم'),
    (263.5, 264.5, 'فقط لا غير', 'غير'),
    (269.3, 274.7, 'اكتبوا لي في التعليقات وإن شاء الله المقطع الجاي بيكون أفضل', 'التعليقات'),
    (275.0, 276.9, 'وشكراً لكم على متابعتكم', 'متابعتكم'),
    (277.1, 279.3, 'والسلام عليكم', 'السلام'),
    (279.4, 281.9, 'ولا تنسون القناة قائمة على مجهود شخصي', 'مجهود'),
    (283.5, 286.7, 'لايك واشتراك ويعطيك العافية', 'لايك'),
    (286.8, 287.6, 'شكراً لكم', 'شكراً'),
]

def word_times(a, b, words):
    orig = [w for w in WORDS if a - 0.15 <= w['s'] < b]
    if len(orig) == len(words): return [(o['s'], o['e']) for o in orig]
    s0 = orig[0]['s'] if orig else a
    e0 = orig[-1]['e'] if orig else b
    L = [len(w) + 2 for w in words]; tot = sum(L); out = []; t = s0
    for l in L:
        d = (e0 - s0) * l / tot; out.append((t, t + d)); t += d
    return out

captions = []
stop = {'في', 'من', 'و', 'لكم', 'اللي', 'على', 'يا', 'هذا', 'هذي', 'أنا', 'إن', 'شاء', 'الله', 'أو', 'لا', 'ما', 'بس', 'يعني', 'أنت', 'كذا'}
for a, b, text, kw in CAPS:
    ws = text.split(); tm = word_times(a, b, ws)
    chunks, cur = [], []
    for w, (s, e) in zip(ws, tm):
        if cur and (len(cur) >= 4 or (len(cur) >= 2 and e - cur[0][1] > 1.8)): chunks.append(cur); cur = []
        cur.append((w, s, e))
    if cur: chunks.append(cur)
    merged = []
    for ch in chunks:
        if merged and len(ch) == 1 and len(merged[-1]) <= 4: merged[-1] += ch
        elif merged and len(merged[-1]) == 1: merged[-1] += ch
        else: merged.append(ch)
    for ch in merged:
        so = s2o(ch[0][1], False) or s2o(ch[0][1]); eo = s2o(ch[-1][2])
        pc = next((p for p in RAWP if p['os'] - 0.01 <= so <= p['oe'] + 0.01), None)
        if pc and eo is not None and eo > pc['oe']:  # never let a caption run across a cut into an insert
            nxt = next((p for p in pieces if p['os'] >= pc['oe'] - 0.01), None)
            if not nxt or nxt.get('src', 'raw') != 'raw': eo = pc['oe'] - 0.25
        if so is None or eo is None or eo <= so: continue
        words = [c[0] for c in ch]
        if kw in words: hl = words.index(kw)
        else:
            cand = [(len(w), i) for i, w in enumerate(words) if w not in stop]
            hl = max(cand)[1] if cand else 0
        captions.append({'from': F(so), 'to': F(eo) + 6, 'words': words, 'hl': hl})
captions.sort(key=lambda c: c['from'])
for i in range(len(captions) - 1):
    if captions[i]['to'] > captions[i + 1]['from']: captions[i]['to'] = captions[i + 1]['from']
    if captions[i + 1]['from'] - captions[i]['to'] < 8: captions[i]['to'] = captions[i + 1]['from']
captions = [c for c in captions if c['to'] - c['from'] >= 6]

# ---------- camera ----------
def face_at(ts):
    near = [x for x in FACE if x['face'] and abs(x['t'] - ts) < 1.2]
    if not near: return None
    return sum(x['cx'] for x in near) / len(near), sum(x['cy'] for x in near) / len(near)
cam = []
def add(f, s, x, y, mode='cut', dur=None):
    k = {'f': f, 's': s, 'x': x, 'y': y, 'mode': mode}
    if dur: k['dur'] = dur
    cam.append(k)
WIDE_C = (0.31, 0.47)   # where he sits in a wide shot (x,y 0..1) - measure from a wide frame
TAB_ZONES = []          # source ranges where a tab/graphic sits on top of a wide shot
FIXED = [(80.0, 93.0)]  # pointing ("كلاود حط ... هنا"): camera locked at s=1.06 so graphics land on the finger
toggle = 0
for p in pieces:
    f0, f1 = F(p['os']), F(p['oe'])
    if p['kind'] == 'insert':
        add(f0, 1.0, 0, 0); continue
    if any(a <= p['s'] < b for a, b in FIXED):
        add(f0, 1.06, 0, 0); continue
    if p['kind'] == 'wide':  # guitar/wide shot: face too small for mediapipe -> manual WIDE_C, slow dolly
        cx, cy = WIDE_C; fx, fy = (0.5 - cx) * 1920, (0.5 - cy) * 1080
        n = max(1, round((f1 - f0) / (6 * FPS))); seg = (f1 - f0) / n
        tabzone = any(a < p['s'] < b for a, b in TAB_ZONES)
        if tabzone: fx, fy = fx * 0.5, 55
        for k in range(n):
            a = round(f0 + k * seg)
            s_a = [1.1, 1.16][k % 2] if tabzone else [1.42, 1.62][k % 2]
            s_b = [1.16, 1.1][k % 2] if tabzone else [1.62, 1.42][k % 2]
            if k == 0: add(a, s_a, round(fx), round(fy))
            add(round(a + seg) - 1, s_b, round(fx + (k % 2 * 2 - 1) * 30), round(fy), 'ease', round(seg) - 4)
        continue
    t = f0
    while t < f1:
        ts = p['s'] + (t - f0) / FPS
        fc = face_at(ts + 0.5) or (0.5, 0.42)
        s = [1.06, 1.2, 1.1, 1.28][toggle % 4]
        fx, fy = (0.5 - fc[0]) * 1920, (0.5 - fc[1]) * 1080 + (40 if s > 1.15 else 0)
        k = 0.85 if s > 1.15 else 0.3
        fx *= k; fy *= k
        add(t, s, round(fx), round(fy)); toggle += 1
        step = 4 * FPS if s > 1.15 else 5 * FPS
        if f1 - t > step + 2 * FPS:
            add(t + step - 1, s + 0.035, round(fx * 1.05), round(fy * 1.05), 'ease', step - 6); t += step
        else:
            if f1 - t > 2 * FPS: add(f1 - 1, s + 0.03, round(fx), round(fy), 'ease', max(10, f1 - t - 8))
            break
cam.sort(key=lambda c: c['f'])

# ---------- items / sfx / music ----------
items, sfx, music = [], [], []
def item(t, src=True, **kw):
    f = F(s2o(t)) if src else F(t)
    kw['from'] = f; items.append(kw); return f
def snd(f, name, v=0.5): sfx.append({'f': max(0, f), 'name': name, 'v': v})
def dur_to(a, b): return max(12, F(s2o(b)) - F(s2o(a)))

# hook
f = item(16.3, type='keyword', dur=50, text='ولا ثانية!', x=1440, y=270, icon='clock', color='red', size=78); snd(f, 'impact', 0.55); item(16.3, type='punch', dur=14, amt=0.08); item(16.3, type='shake', dur=10, amt=10)
f = item(19.5, type='raw', dur=dur_to(19.5, 21.9) + 6, x=1460, y=470, img='frames/00800.jpg', time='٤:٥٢', label='رفعته على الدرايف'); snd(f, 'whoosh', 0.4)
f = item(4.6, type='glitch', dur=6); snd(f, 'glitch', 0.4)
f = item(7.4, type='lower', dur=110); snd(f, 'swoosh', 0.45)
# channel intro (its own sound) — corner logo starts after it
a, b = ins('intro.mp4'); items.append({'type': 'nologo', 'from': F(a), 'dur': F(b - a)}); LOGO_START = F(b)
# what Claude did
f0 = item(60.3, type='checklist', dur=dur_to(60.3, 70.8) + 10, title='سواها كلاود', items=['القص', 'المونتاج', 'قص السكتات', 'كل شي'], at=[F(s2o(61.5)) - F(s2o(60.3)), F(s2o(62.4)) - F(s2o(60.3)), F(s2o(63.6)) - F(s2o(60.3)), F(s2o(65.0)) - F(s2o(60.3))])
snd(f0, 'whoosh', 0.4)
for t in (61.5, 62.4, 63.6, 65.0): snd(F(s2o(t)), 'click', 0.7)
f = item(70.3, type='keyword', dur=40, text='ولا ثانية!', x=1440, y=270, icon='hand', color='yellow', size=70); snd(f, 'pop', 0.5)
f = item(71.8, type='raw', dur=dur_to(71.8, 73.6), x=1460, y=470, img='frames/00800.jpg', time='٤:٥٢', label='الخام'); snd(f, 'whoosh', 0.4)
f = item(73.7, type='phone', dur=dur_to(73.7, 79.9) + 8, x=1470, y=520, dir='type', n=220, rate=0.9, start=20, height=780, label='جملة وحدة'); snd(f, 'whoosh', 0.5); snd(f + 4, 'pop', 0.5)
f = item(77.6, type='punch', dur=30, amt=0.12, tau=14); snd(f - 2, 'zoomwhoosh', 0.45)
# pointing: logo + latest video exactly where the finger is (cam locked 1.06)
f = item(84.9, type='image', dur=dur_to(84.9, 88.1) + 4, img='logo.png', x=1600, y=560, size=270, label='شعار القناة'); snd(f, 'whoosh', 0.45); snd(f + 3, 'impact', 0.5); item(84.9, type='sparks', dur=16, x=1600, y=560, r=170)
f = item(89.3, type='wide', dur=dur_to(89.3, 92.7) + 6, img='latest.jpg', x=390, y=440, w=620, label='آخر فيديو نزلته'); snd(f, 'whoosh', 0.45); snd(f + 3, 'impact', 0.45)
# easy
for k, (w, tt) in enumerate([('إيزي!', 94.4), ('إيزي!', 95.1)]):
    f = item(tt, type='beat', dur=20, text=w, x=[1350, 1480][k], y=[320, 380][k], tilt=[-7, 6][k], color=['#FFD23F', '#ffffff'][k], size=[190, 210][k]); snd(f, 'pop', 0.6); item(tt, type='punch', dur=12, amt=0.06)
f = item(98.1, type='keyword', dur=50, text='أسهل', x=1440, y=270, icon='up', color='red'); snd(f, 'pop', 0.5)
f = item(101.5, type='leak', dur=36); snd(f, 'shimmer', 0.3)
# how to build the skill
f = item(108.5, type='glitch', dur=6); snd(f, 'glitch', 0.45); snd(f, 'whoosh', 0.35)
f = item(110.0, type='keyword', dur=70, text='كيف تبني السكيل؟', x=1400, y=265, icon='bulb', color='dark', size=70); snd(f, 'pop', 0.5)
for k, tt in enumerate([116.2, 117.0, 117.7]):
    f = item(tt, type='beat', dur=22, text='غلط!', x=[1250, 1450, 1650][k], y=[330, 300, 350][k], tilt=[-8, 5, -4][k], color='#E3262A', size=170); snd(f, 'pop', 0.6); item(tt, type='punch', dur=12, amt=0.05)
f = item(119.4, type='ref', dur=dur_to(119.4, 123.6), x=1460, y=480); snd(f, 'whoosh', 0.45); snd(f + 14, 'pop', 0.5)
f = item(123.8, type='prompt', dur=dur_to(123.8, 129.4), x=960, y=270, text='يا كلاود سوّ نفس الفيديو', label='قل لكلاود', typeStart=6, cps=14); snd(f, 'whoosh', 0.4)
for k in range(8): snd(f + 8 + k * 6, 'click', 0.35)
f = item(129.8, type='editor', dur=dur_to(129.8, 134.0) + 10, x=1480, y=470); snd(f, 'whoosh', 0.5); snd(f + 10, 'riser', 0.3)
f = item(134.1, type='bw', dur=dur_to(134.1, 135.6)); item(134.1, type='glitch', dur=5); snd(F(s2o(134.1)), 'glitch', 0.4)
f = item(135.0, type='keyword', dur=40, text='ما راح يكون كويس', x=1430, y=270, icon='fire', color='white'); snd(f, 'slidewhistle', 0.5)
n0 = F(s2o(136.4))
f = item(136.4, type='notes', dur=dur_to(136.4, 141.4) + 10, x=1460, y=470, title='التعديلات', items=['عدّل القص', 'كبّر الزوم', 'غيّر الخط', 'غيّر اللون'], at=[0, F(s2o(137.6)) - n0, F(s2o(138.3)) - n0, F(s2o(139.7)) - n0]); snd(f, 'whoosh', 0.4)
for t in (136.4, 137.6, 138.3, 139.7): snd(F(s2o(t)) + 9, 'scratch', 0.3)
f = item(142.4, type='skill', dur=dur_to(142.4, 147.3) + 10, x=1440, y=470); snd(f, 'whoosh', 0.45)
for k in range(4): snd(f + 14 + k * 6, 'pop', 0.4)
snd(f + 42, 'impact', 0.45); snd(f + 42, 'shimmer', 0.35)
f = item(144.8, type='keyword', dur=55, text='مرة وحدة', x=520, y=270, icon='check', color='yellow'); snd(f, 'pop', 0.5)
# price + big usage-limit note (user asked for it)
f = item(156.0, type='keyword', dur=50, text='٩٠ ريال', x=1440, y=265, icon='star', color='yellow', size=80); snd(f, 'impact', 0.5); item(156.0, type='punch', dur=14, amt=0.07)
f = item(159.3, type='notice', dur=F(3.6), title='ملاحظة مهمة', text='الاشتراك الشهري عليه حد استخدام', sub='عدد الفيديوهات يختلف حسب طولها وحسب خطتك'); snd(f, 'impact', 0.6); snd(f, 'whoosh', 0.4)
# result before/after
f = item(167.9, type='glitch', dur=6); snd(f, 'glitch', 0.4)
f = item(171.3, type='keyword', dur=45, text='قبل وبعد', x=1440, y=265, icon='star', color='red', size=72); snd(f, 'pop', 0.5)
f = item(175.6, type='arrow', dur=dur_to(175.6, 177.1) + 6, x1=1700, y1=430, x2=1420, y2=760, label='هذي!', bend=-120); snd(f, 'slidewhistle', 0.55); item(175.6, type='shake', dur=14, amp=7)
a, b = ins('guitar_raw.mov'); fa = F(a)
items += [{'type': 'whip', 'from': fa - 7, 'dur': 14, 'dir': -1}, {'type': 'badge', 'from': fa + 4, 'dur': F(b - a) - 6, 'text': 'قبل', 'sub': 'الخام زي ما صورته', 'color': '#141414'},
          {'type': 'counter', 'from': fa + 10, 'dur': F(b - a) - 12, 'x': 1640, 'y': 920, 'fromSec': 658, 'toSec': 658, 'label': 'الخام', 'runFor': 1},
          {'type': 'nologo', 'from': fa, 'dur': F(b - a)}]
snd(fa - 7, 'whoosh', 0.7); snd(fa + 4, 'impact', 0.5)
a, b = ins('guitar_final.mp4'); fb = F(a)
items += [{'type': 'flash', 'from': fb, 'dur': 7}, {'type': 'badge', 'from': fb + 4, 'dur': F(b - a) - 6, 'text': 'بعد', 'sub': 'بعد مونتاج كلاود', 'color': '#E3262A'},
          {'type': 'counter', 'from': fb + 14, 'dur': F(b - a) - 16, 'x': 1640, 'y': 920, 'fromSec': 658, 'toSec': 324, 'label': 'المدة', 'runFrom': 8, 'runFor': 45},
          {'type': 'nologo', 'from': fb, 'dur': F(b - a)}]
snd(fb, 'impact', 0.6); snd(fb, 'shimmer', 0.35); snd(fb + 53, 'ding', 0.35)
# thumbnail + shorts
f = item(181.0, type='wide', dur=dur_to(181.0, 186.2) + 4, img='thumb.jpg', x=1400, y=450, w=720, label='الصورة المصغرة', tilt=3); snd(f, 'whoosh', 0.45); snd(f + 3, 'impact', 0.45)
a, b = ins('shorts3.mp4'); fs = F(a)
items += [{'type': 'whip', 'from': fs - 7, 'dur': 14, 'dir': 1}, {'type': 'badge', 'from': fs + 4, 'dur': F(b - a) - 6, 'text': '٣ شورتات', 'sub': 'جاهزة للنشر', 'color': '#FFD23F', 'y': 70}, {'type': 'nologo', 'from': fs, 'dur': F(b - a)}]
snd(fs - 7, 'whoosh', 0.6)
f = item(190.6, type='keyword', dur=40, text='كلها كلاود!', x=1440, y=265, icon='star', color='red', size=74); snd(f, 'impact', 0.5); item(190.6, type='sparks', dur=16, x=1440, y=265, r=140)
f = item(195.0, type='branch', dur=dur_to(195.0, 199.9) + 6, x=1370, y=500); snd(f, 'whoosh', 0.45)
for k in range(3): snd(f + 20 + k * 7, 'pop', 0.45)
# idea + closing
f = item(204.3, type='leak', dur=36); snd(f, 'shimmer', 0.3)
f = item(207.4, type='keyword', dur=55, text='خذ اللي يعجبك', x=1430, y=265, icon='bulb', color='yellow'); snd(f, 'pop', 0.5)
f = item(213.6, type='keyword', dur=55, text='يخدمك طول العمر', x=1430, y=265, icon='check', color='red'); snd(f, 'pop', 0.5)
f = item(222.6, type='keyword', dur=50, text='مهارات لكلاود؟', x=1430, y=265, icon='bulb', color='dark'); snd(f, 'pop', 0.5)
f = item(225.7, type='glitch', dur=6); snd(f, 'glitch', 0.4)
f = item(235.0, type='keyword', dur=60, text='تصوير جوال + مونتاج جوال', x=1330, y=265, icon='mic', color='yellow', size=58); snd(f, 'pop', 0.5); item(235.0, type='punch', dur=14, amt=0.06)
f = item(237.8, type='phone', dur=dur_to(237.8, 245.2) + 6, x=1470, y=500, dir='chat', n=451, rate=1.1, start=1, height=760, label='كلاود يشتغل'); snd(f, 'whoosh', 0.5)
f0 = F(s2o(253.1))
f = item(253.1, type='checklist', dur=dur_to(253.1, 259.6) + 12, title='وبعد النشر', items=['العناوين', 'الدسكربشن', 'كل شي'], at=[F(s2o(254.4)) - f0, F(s2o(256.7)) - f0, F(s2o(259.0)) - f0])
snd(f, 'whoosh', 0.4)
for t in (254.4, 256.7, 259.0): snd(F(s2o(t)), 'click', 0.7)
f = item(261.0, type='keyword', dur=55, text='أرد على تعليقاتكم', x=1430, y=265, icon='hand', color='white'); snd(f, 'pop', 0.5)
f = item(269.3, type='keyword', dur=70, text='اكتبوا لي بالتعليقات', x=1400, y=265, icon='mic', color='red'); snd(f, 'pop', 0.5)
def subscribe_at(t):
    f = item(t, type='subscribe', dur=115, x=960, y=850); snd(f, 'whoosh', 0.35); [snd(f + 4 + k * 4, 'click', 0.45) for k in range(4)]
    snd(f + 30, 'click', 0.7); snd(f + 30, 'ding', 0.3); snd(f + 52, 'bell', 0.45); snd(f + 72, 'click', 0.6); snd(f + 72, 'pop', 0.4); snd(f + 92, 'click', 0.6)
subscribe_at(99.9); subscribe_at(283.3)
items.append({'type': 'fadeout', 'from': F(total) - 50, 'dur': 46})

for p in pieces[1:]:
    if p['kind'] != 'insert': snd(F(p['os']), 'swoosh', 0.12)

# music: up in hook, under voice, out during inserts that carry their own sound
for p in pieces:
    v = 0.0 if p['kind'] == 'insert' else 0.075
    music.append({'f': F(p['os']), 'v': v}); music.append({'f': F(p['oe']) - 1, 'v': v})
music[0] = {'f': 0, 'v': 0.16}; music.insert(1, {'f': 60, 'v': 0.075})
music.append({'f': F(total) - 60, 'v': 0.075}); music.append({'f': F(total), 'v': 0.2})
music.sort(key=lambda m: m['f'])

# big cards: pull the camera back (s=1.0) while they are on screen so his face stays small and clear of them
BIG = {'raw', 'checklist', 'phone', 'wide', 'ref', 'prompt', 'editor', 'notes', 'skill', 'branch', 'notice'}
def cam_val(f):
    i = 0
    while i + 1 < len(cam) and cam[i + 1]['f'] <= f: i += 1
    return cam[i]
spans = sorted((it['from'], it['from'] + it['dur']) for it in items if it['type'] in BIG)
merged = []
for a, b in spans:
    if merged and a <= merged[-1][1] + 15: merged[-1][1] = max(merged[-1][1], b)
    else: merged.append([a, b])
for a, b in merged:
    resume = dict(cam_val(b)); resume.update({'f': b, 'mode': 'cut'}); resume.pop('dur', None)
    cam[:] = [c for c in cam if not (a <= c['f'] <= b)] + [{'f': a, 's': 1.0, 'x': 0, 'y': 0, 'mode': 'cut'}, resume]
    cam.sort(key=lambda c: c['f'])

edl = {'duration': F(total), 'video': 'aroll.mp4', 'musicFile': 'music/bed.mp3', 'logoStart': LOGO_START, 'cam': cam, 'captions': captions,
       'items': sorted(items, key=lambda i: i['from']), 'sfx': sorted(sfx, key=lambda s: s['f']), 'music': music}
if LIMIT: edl['duration'] = F(LIMIT)
json.dump(edl, open(f'/home/claude/proj/app/public/{OUTNAME}', 'w'), ensure_ascii=False)
print('frames', edl['duration'], 'captions', len(captions), 'items', len(items), 'cam', len(cam))
