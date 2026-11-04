"""EDL for a vertical client clip (no face, POV) -> app/public/edl.json  (composition: Vert)"""
import json
FPS = 30
DUR = 1460
F = lambda t: int(round(t * FPS))

CAPS = [  # (from, to, words, hl) in seconds, dialect
    (2.7, 3.5, ['أول', 'ما', 'تدخلون'], 2),
    (3.5, 4.3, ['قسم', 'الحلويات'], 1),
    (4.3, 5.4, ['شوفوا', 'الرفوف'], 1),
    (5.4, 6.9, ['يا', 'بوي!'], 1),
    (7.0, 8.4, ['تويكس', '١٢', 'ريال'], 1),
    (8.4, 9.4, ['و٨٠', 'هللة'], 0),
    (9.5, 10.4, ['ترى', 'مرة', 'مرة'], 2),
    (10.4, 11.1, ['أحب', 'تويكس'], 1),
    (11.2, 12.0, ['شوفوا', 'هذي'], 1),
    (12.0, 12.8, ['إيش', 'اسمها؟'], 1),
    (12.8, 13.5, ['نسيت', 'والله'], 0),
    (14.4, 15.2, ['هذا', 'كامل'], 1),
    (15.2, 16.1, ['قسم', 'الكيو', 'كير'], 1),
    (16.1, 19.1, ['جميع', 'الكريمات', 'والأشياء'], 1),
    (19.2, 20.3, ['وترى', 'فيه', 'فحص'], 2),
    (20.3, 21.3, ['عندهم', 'هناك'], 0),
    (21.4, 22.5, ['طبعاً', 'بخلص', 'وبرجع'], 2),
    (23.3, 25.0, ['وباخذ', 'لي', 'أوريو'], 2),
    (25.0, 26.1, ['سعره', 'صفر', 'ريال'], 1),
    (26.2, 27.6, ['شوفوا!'], 0),
    (27.7, 29.1, ['مدري', 'كيف', 'أستوعب'], 2),
    (29.2, 30.0, ['إن', 'هذا', 'كله'], 2),
    (30.0, 31.0, ['قسم', 'مجمدات'], 1),
    (31.1, 32.0, ['وأنا', 'أشوفه'], 1),
    (32.0, 33.0, ['ما شاء الله', 'تبارك الله'], 0),
    (33.0, 33.5, ['الثلاجات'], 0),
    (33.5, 34.4, ['الكيو', 'كير'], 0),
    (35.2, 36.2, ['إيش', 'أقول'], 1),
    (36.2, 37.5, ['والله', 'العظيم', 'مغرمة'], 2),
    (37.5, 38.3, ['شي', 'طبيعي'], 1),
    (38.3, 39.8, ['المكان', 'يفتح', 'النفس'], 2),
    (39.9, 41.1, ['طبعاً', 'هنا', 'إذا', 'تبين'], 1),
    (41.2, 42.7, ['تسوين', 'ميك أب'], 1),
    (42.8, 44.0, ['أحط', 'الميك أب', 'هنا'], 1),
    (44.0, 45.5, ['وأقعد', 'قدام', 'المراية'], 2),
    (45.6, 46.6, ['طبعاً', 'من', 'الماركات'], 2),
    (46.6, 47.7, ['بولفر', 'أحلى', 'شي'], 0),
    (47.7, 48.6, ['وجوده'], 0),
]

items, sfx = [], []
def add(t, d, **k): items.append(dict(from_=F(t), dur=F(d), **k))
def kw(t, d, text, x, y, color='red', icon=None, size=72, tilt=-3, s='pop'):
    add(t, d, type='keyword', text=text, x=x, y=y, color=color, icon=icon, size=size, tilt=tilt); sfx.append((t, s, 0.5))
    add(t, 0.4, type='punch', amt=0.05)
def beat(t, d, text, x=540, y=1000, color='#FFD23F', size=170, s='impact', tilt=-6):
    add(t, d, type='beat', text=text, x=x, y=y, color=color, size=size, tilt=tilt); sfx.append((t, s, 0.45))
    add(t, 0.5, type='punch', amt=0.08)

sfx.append((0.0, 'swoosh', 0.5))
add(0.0, 0.5, type='punch', amt=0.1)
kw(3.5, 1.6, 'قسم الحلويات', 540, 470, 'red', 'star')
add(7.6, 1.3, type='ping', x=420, y=380); sfx.append((7.6, 'ding', 0.4))
beat(7.9, 1.3, '١٢.٨٠ ريال', 540, 1030, size=140)
kw(10.2, 1.1, 'مرة أحب تويكس', 540, 520, 'white', 'fire')
beat(12.1, 1.0, 'إيش اسمها؟', 600, 1060, color='#fff', size=130, s='slidewhistle', tilt=4)
add(14.2, 0.33, type='whip', dir=-1); sfx.append((14.2, 'whoosh', 0.5))
add(15.3, 1.1, type='ping', x=760, y=880); sfx.append((15.3, 'pop', 0.4))
kw(15.5, 1.6, 'كيو كير', 700, 1090, 'dark', 'star', size=80)
kw(19.6, 1.6, 'فيه فحص!', 540, 520, 'yellow', 'check')
# zero riyal: the funny/shock moment
add(25.3, 0.4, type='glitch'); sfx.append((25.3, 'glitch', 0.45))
add(25.3, 0.25, type='flash')
add(25.4, 0.7, type='shake', amp=18)
beat(25.4, 1.5, 'صفر ريال؟!', 540, 1050, size=160)
add(28.9, 0.33, type='whip', dir=1); sfx.append((28.9, 'whoosh', 0.5))
kw(30.0, 1.6, 'قسم المجمدات', 540, 470, 'red', 'star')
kw(32.0, 1.2, 'ما شاء الله', 360, 1100, 'white', None, size=70, tilt=3)
beat(36.9, 1.4, 'مغرمة!', 540, 900, color='#FFD23F', size=190, s='shimmer')
add(36.9, 1.0, type='sparks', x=540, y=900, r=200)
kw(38.6, 1.3, 'يفتح النفس', 540, 520, 'yellow', 'bulb')
add(39.7, 0.33, type='whip', dir=-1); sfx.append((39.7, 'whoosh', 0.5))
kw(41.2, 1.6, 'ركن الميك أب', 540, 470, 'red', 'star')
add(43.4, 1.2, type='ping', x=600, y=1040); sfx.append((43.4, 'pop', 0.4))
beat(47.0, 1.2, 'أحلى شي!', 540, 1050, size=150)
add(47.9, 0.8, type='fadeout')

# zoom steps (Khater style hard cuts), 1.0 while a ping marks a spot
ZS = [1.0, 1.1, 1.04, 1.14]
pings = [(it['from_'], it['from_'] + it['dur']) for it in items if it['type'] == 'ping']
zooms, k = [], 0
for f in range(0, DUR, 75):
    zooms.append(dict(f=f, s=ZS[k % 4])); k += 1
for a, b in pings:
    zooms = [z for z in zooms if not (a <= z['f'] < b)]
    prev = [z for z in zooms if z['f'] < a][-1]['s']
    zooms += [dict(f=a, s=1.0), dict(f=b, s=prev)]
zooms.sort(key=lambda z: z['f'])

for it in items: it['from'] = it.pop('from_')
spec = dict(duration=DUR, title='كيو وصل الرياض!', title2='جولة كاملة', bar='جولة في كيو', cta='تابعوني عشان تشوفون أكثر',
            zooms=zooms, captions=[dict(**{'from': F(a), 'to': F(b)}, words=w, hl=h) for a, b, w, h in CAPS], items=items,
            sfx=[dict(f=F(t), name=n, v=v) for t, n, v in sfx],
            music=[dict(f=0, v=0.09), dict(f=F(2.5), v=0.07), dict(f=F(46.5), v=0.07), dict(f=DUR, v=0.14)], musicFile='music/bed.mp3')
json.dump(spec, open('/home/claude/proj/app/public/edl.json', 'w'), ensure_ascii=False)
print('items', len(items), 'caps', len(CAPS), 'zooms', len(zooms))
