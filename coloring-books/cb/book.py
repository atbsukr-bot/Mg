"""Build a print-ready Amazon paperback: interior PDF, full-wrap cover PDF, listing text."""
import datetime as dt
import json
import math
import os
import random

from reportlab.lib.colors import Color
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from . import animals as A, common as C, dinos as D, fantasy as F, objects as O, vehicles as V
from .draw import Pen, PALETTE
from .fonts import register

IN = 72
TRIM_W, TRIM_H = 8.5 * IN, 11 * IN
BLEED = .125 * IN
PAPER_IN_PER_PAGE = 0.002252  # white paper
LW = 4.6  # outline width in points
PUBLISHER = "Tiny Crayon Press"
EPOCH = dt.date(2026, 11, 17)
ROTATION = ["animals", "vehicles", "fantasy", "dinos", "abc", "numbers", "seasonal"]

SEA = {"FISH", "WHALE", "OCTOPUS", "CRAB", "JELLYFISH", "SUBMARINE", "TURTLE"}
SKY = {"BUTTERFLY", "BEE", "AIRPLANE", "HELICOPTER", "HOT AIR BALLOON", "ROCKET", "PTERODACTYL", "KITE",
       "BALLOONS", "FAIRY", "PEGASUS", "MOON", "STAR", "SUN", "RAINBOW", "MAGIC WAND"}
WATER = {"SAILBOAT", "SHIP", "SWAN", "DUCK"}


# ----------------------------------------------------------------- pages
class Page:
    def __init__(self, kind, label, fn=None, bg="ground", acc=None, flip=False, extra=None):
        self.kind, self.label, self.fn, self.bg, self.acc, self.flip, self.extra = kind, label, fn, bg, acc, flip, extra


def _bg_for(label, r, theme):
    if label in SEA:
        return "sea"
    if label in SKY:
        return r.choice(["sky", "stars"])
    if label in WATER:
        return "none"
    if theme == "vehicles":
        return r.choice(["road", "road", "sky_road"])
    if theme == "seasonal_winter":
        return r.choice(["snow", "snow", "snowflakes"])
    if theme == "fantasy":
        return r.choice(["hearts", "stars", "flowers", "sparkle"])
    if theme == "dinos":
        return r.choice(["jungle", "volcano", "ground", "eggs"])
    return r.choice(["ground", "flowers", "sky", "hearts", "ground", "none"])


def build_pages(theme, r, month):
    pages = []
    if theme == "animals":
        items = r.sample(A.ANIMALS, 30)
        for name, fn in items:
            acc = r.choice(["party", "bow", "flower", "beanie", "crown"]) if name in A.HATTABLE and r.random() < .3 else None
            if name == "FROG" and acc in ("party", "beanie"):
                acc = "crown"
            pages.append(Page("subject", name, fn, _bg_for(name, r, theme), acc, r.random() < .3))
    elif theme == "vehicles":
        items = r.sample(V.VEHICLES, 30)
        for name, fn in items:
            pages.append(Page("subject", name, fn, _bg_for(name, r, theme), flip=r.random() < .25))
    elif theme == "fantasy":
        items = list(F.FANTASY)
        royal = [(n, f) for n, f in A.ANIMALS if n in A.HATTABLE]
        pets = r.sample(royal, 30 - len(items))
        for name, fn in items:
            pages.append(Page("subject", name, fn, _bg_for(name, r, theme), flip=r.random() < .3))
        for name, fn in pets:
            pages.append(Page("subject", name, fn, _bg_for(name, r, theme), r.choice(["crown", "bow", "flower"])))
        r.shuffle(pages)
    elif theme == "dinos":
        species = [d for d in D.DINOS if d[0] != "BABY DINO"]
        seq = []
        for k in range(4):
            sp = species[:]
            r.shuffle(sp)
            seq += sp
        seq = seq[:27] + [d for d in D.DINOS if d[0] == "BABY DINO"]
        r.shuffle(seq)
        for i, (name, fn) in enumerate(seq):
            pages.append(Page("subject", name, fn, _bg_for(name, r, theme), flip=(i % 2 == 1)))
        pages.insert(r.randint(5, 25), Page("subject", "DINO EGGS", _dino_eggs, "jungle"))
        pages.insert(r.randint(5, 25), Page("subject", "VOLCANO", _volcano_big, "none"))
    elif theme == "abc":
        for L, word, fn in O.ABC:
            pages.append(Page("letter", word, fn, extra=L, flip=False))
        bonus = r.sample([a for a in A.ANIMALS if a[0] in A.HATTABLE], 4)
        for name, fn in bonus:
            pages.append(Page("subject", name, fn, _bg_for(name, r, "animals"), r.choice(["party", "bow"])))
    elif theme == "numbers":
        kinds = r.sample(O.COUNT_ITEMS, len(O.COUNT_ITEMS))
        for n in range(1, 21):
            pages.append(Page("number", NUMWORDS[n], extra=(n, kinds[(n - 1) % len(kinds)])))
        for name, fn in O.SHAPES:
            pages.append(Page("subject", name, fn, r.choice(["none", "stars", "hearts", "sky"])))
    elif theme == "seasonal":
        if month in (11, 12, 1):
            items = list(O.WINTER)
            extra = r.sample([a for a in A.ANIMALS if a[0] in A.HATTABLE and a[0] not in ("PENGUIN", "BEAR")],
                             30 - len(items))
            for name, fn in items:
                pages.append(Page("subject", name, fn, _bg_for(name, r, "seasonal_winter")))
            for name, fn in extra:
                hat_ = "santa" if r.random() < .6 else "beanie"
                if name == "FROG":
                    hat_ = None
                pages.append(Page("subject", name, fn, _bg_for(name, r, "seasonal_winter"), hat_))
            r.shuffle(pages)
        else:
            pool = O.OBJECTS + r.sample(A.ANIMALS, 8) + r.sample(V.VEHICLES, 6)
            for name, fn in r.sample(pool, 30):
                pages.append(Page("subject", name, fn, _bg_for(name, r, "mixed")))
    return pages


def _dino_eggs(p, acc=None):
    p.path([("M", -40, -20), ("Q", 0, -50, 40, -20), ("Q", 0, -30, -40, -20)], "brown")
    C.egg(p, -18, 4, 2.0, "lime")
    C.egg(p, 18, 4, 2.0, "sky")
    C.egg(p, 0, 12, 2.3, "cream", crack=True)
    for x, y in ((-20, 8), (14, 0), (4, 22), (-4, 4)):
        p.circle(x, y, 2.5, "orange")


def _volcano_big(p, acc=None):
    C.volcano(p, 0, -40, 34)
    C.palm(p, -40, -44, 40)
    with p.at(28, -36, .45):
        D.baby_dino(p)


NUMWORDS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN",
            "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN", "TWENTY"]


# ----------------------------------------------------------------- page drawing
def draw_background(p, kind, r):
    """Unit box for page: x 0..612, y 0..792 (points). Subject sits around (306, 450)."""
    gy = 205 if kind in ("road", "sky_road") else 232
    if kind in ("ground", "flowers", "jungle", "volcano", "eggs", "snow", "road", "sky_road"):
        if kind == "road":
            p.line(60, gy, 552, gy)
            for x in range(80, 540, 60):
                p.rect(x, gy - 22, 34, 7, "white", r=3.5)
            p.line(60, gy - 44, 552, gy - 44)
        elif kind == "sky_road":
            p.line(60, gy, 552, gy)
            p.cloud(130, 690, 80, "white")
            p.cloud(480, 700, 70, "white")
        elif kind == "snow":
            p.path([("M", 50, gy - 10), ("Q", 180, gy + 22, 306, gy), ("Q", 430, gy - 22, 562, gy + 8)], closed=False)
            for x, y in ((100, 690), (510, 700), (80, 520), (535, 540)):
                C.snowflake(p, x, y, 18)
        else:
            p.path([("M", 50, gy), ("Q", 180, gy + 18, 306, gy + 4), ("Q", 430, gy - 12, 562, gy + 6)], closed=False)
            for x in (80, 150, 470, 530):
                C.grass_tuft(p, x, gy + (5 if x < 300 else 0), 5)
            if kind == "ground":
                C.sun(p, 95, 690, 30, face=False)
                p.cloud(500, 700, 70, "white")
            elif kind == "flowers":
                for x in (85, 530):
                    with p.at(x, gy + 2, 2.6):
                        C.tulip(p, 0, 0, 22)
                p.cloud(470, 710, 60, "white")
            elif kind == "jungle":
                with p.at(0, 0):
                    with p.at(70, gy + 2, 3):
                        C.palm(p, 0, 0, 40)
                    with p.at(535, gy + 2, 2.6):
                        C.palm(p, 0, 0, 40)
            elif kind == "volcano":
                with p.at(515, gy + 2, 2.4):
                    C.volcano(p, 0, 0, 22)
                C.sun(p, 95, 690, 30, face=False)
            elif kind == "eggs":
                C.egg(p, 85, gy + 34, 3, "cream")
                C.egg(p, 527, gy + 34, 3, "cream", crack=True)
    elif kind == "sky":
        p.cloud(120, 690, 80, "white")
        p.cloud(500, 660, 70, "white")
        p.cloud(90, 250, 60, "white")
        p.cloud(525, 240, 55, "white")
    elif kind == "stars":
        for x, y, s in ((90, 700, 22), (520, 690, 18), (80, 260, 16), (535, 280, 20), (300, 740, 12)):
            p.star(x, y, s, "yellow")
    elif kind == "sparkle":
        for x, y, s in ((90, 700, 20), (520, 690, 16), (80, 250, 14), (535, 260, 18)):
            p.star(x, y, s, "yellow", n=4, inner=.35)
    elif kind == "hearts":
        for x, y, s in ((95, 690, 22), (515, 700, 18), (80, 250, 16), (530, 260, 20)):
            p.heart(x, y, s, "pink")
    elif kind == "snowflakes":
        for x, y in ((95, 690), (515, 700), (80, 250), (530, 260), (306, 740)):
            C.snowflake(p, x, y, 20)
    elif kind == "sea":
        p.path([("M", 50, 230), ("Q", 110, 250, 170, 230), ("Q", 230, 210, 290, 230), ("Q", 350, 250, 410, 230),
                ("Q", 470, 210, 562, 230)], closed=False)
        for x, y, s in ((90, 700, 18), (130, 640, 11), (520, 680, 14), (490, 620, 9)):
            C.bubble(p, x, y, s)
        for x in (80, 530):
            p.path([("M", x, 200), ("Q", x - 20, 250, x, 290), ("Q", x + 20, 330, x, 360)], closed=False)
            p.path([("M", x + 14, 200), ("Q", x - 6, 240, x + 14, 280)], closed=False)


_BBOX = {}


def measure(fn, acc=None):
    """Bounding box of a subject in unit coords, by rasterising it once."""
    key = (fn, acc)
    if key in _BBOX:
        return _BBOX[key]
    import io
    import pymupdf
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(600, 600))
    p = Pen(c, color=False, lw=LW)
    with p.at(300, 300, 2.5):
        fn(p, acc) if acc else fn(p)
    c.save()
    d = pymupdf.open(stream=buf.getvalue(), filetype="pdf")
    pix = d[0].get_pixmap(dpi=72, colorspace=pymupdf.csGRAY)
    w, h, sam = pix.width, pix.height, pix.samples
    xs, ys = [], []
    for yy in range(0, h, 2):
        row = sam[yy * w:(yy + 1) * w]
        for xx in range(0, w, 2):
            if row[xx] < 128:
                xs.append(xx); ys.append(yy)
    bb = ((min(xs) - 300) / 2.5, (300 - max(ys)) / 2.5, (max(xs) - 300) / 2.5, (300 - min(ys)) / 2.5)
    _BBOX[key] = bb
    return bb


GROUNDED = ("ground", "flowers", "jungle", "volcano", "eggs", "snow", "road", "sky_road")


def place(page):
    """Return (cx, cy, scale) so the subject fills its area and stands on the ground."""
    x0, y0, x1, y1 = measure(page.fn, page.acc)
    if page.flip:
        x0, x1 = -x1, -x0
    w, h = x1 - x0, y1 - y0
    if page.bg in GROUNDED:
        gy = 205 if page.bg in ("road", "sky_road") else 232
        base, top = gy - 6, 690
    else:
        base, top = 190, 700
    s = min(420 / w, (top - base) / h, 5.4)
    cx = 306 - (x0 + x1) / 2 * s
    if page.bg in GROUNDED:
        cy = base - y0 * s
    else:
        cy = (base + top) / 2 - (y0 + y1) / 2 * s
    return cx, cy, s


def fit_text(txt, font, size, maxw):
    while stringWidth(txt, font, size) > maxw and size > 10:
        size -= 2
    return size


def draw_label(p, txt, y=78, size=64, maxw=480):
    size = fit_text(txt, "FredokaBold", size, maxw)
    with p.width(.55):
        p.text_outline(txt, TRIM_W / 2, y, size)


def frame(c):
    c.setLineWidth(2.2)
    c.setStrokeColorRGB(0, 0, 0)
    c.roundRect(30, 30, TRIM_W - 60, TRIM_H - 60, 22, stroke=1, fill=0)


def draw_page(c, page, r, color=False):
    p = Pen(c, color=color, lw=LW)
    frame(c)
    if page.kind == "subject":
        draw_background(p, page.bg, r)
        cx, cy, sc = place(page)
        with p.at(cx, cy, sc, flip=page.flip):
            page.fn(p, page.acc) if page.acc else page.fn(p)
        draw_label(p, page.label)
    elif page.kind == "letter":
        L = page.extra
        with p.width(.7):
            p.text_outline(L + L.lower(), TRIM_W / 2, 590, 150)
        x0, y0, x1, y1 = measure(page.fn)
        sc = min(400 / (x1 - x0), 285 / (y1 - y0), 5)
        with p.at(306 - (x0 + x1) / 2 * sc, 305 - (y0 + y1) / 2 * sc, sc):
            page.fn(p)
        draw_label(p, page.label, size=60)
    elif page.kind == "number":
        n, (iname, ifn) = page.extra
        with p.width(.7):
            p.text_outline(str(n), TRIM_W / 2, 585, 160)
        cols = min(5, n if n <= 3 else math.ceil(math.sqrt(n * 1.6)))
        cols = max(cols, 1)
        rows = math.ceil(n / cols)
        cw, ch = 470 / cols, 380 / max(rows, 1)
        cell = min(cw, ch)
        bx0, by0, bx1, by1 = measure(ifn)
        s = min(cell * .8 / max(bx1 - bx0, by1 - by0), 14)
        ox, oy = -(bx0 + bx1) / 2 * s, -(by0 + by1) / 2 * s
        x0 = TRIM_W / 2 - cell * cols / 2 + cell / 2
        y0 = 160 + 380 / 2 + cell * rows / 2 - cell / 2
        for i in range(n):
            rr, cc = divmod(i, cols)
            in_row = min(cols, n - rr * cols)
            xo = (cols - in_row) * cell / 2
            with p.at(x0 + xo + cc * cell + ox, y0 - rr * cell + 20 + oy, s):
                ifn(p)
        draw_label(p, page.label, size=60)


def blank_back(c):
    c.setFont("FredokaMed", 9)
    c.setFillColorRGB(.6, .6, .6)
    c.drawCentredString(TRIM_W / 2, 36, "This page is left blank so colors won't bleed through.")


# ----------------------------------------------------------------- front matter
def title_page(c, meta, cover_fn):
    c.setFillColorRGB(0, 0, 0)
    sz = fit_text(meta["display_title"], "FredokaBold", 46, 500)
    c.setFont("FredokaBold", sz)
    y = 650
    for line in meta["title_lines"]:
        s2 = fit_text(line, "FredokaBold", 50, 500)
        c.setFont("FredokaBold", s2)
        c.drawCentredString(TRIM_W / 2, y, line)
        y -= s2 * 1.1
    p = Pen(c, color=False, lw=LW)
    with p.at(306, 340, 3.2):
        cover_fn(p)
    c.setFont("FredokaMed", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(TRIM_W / 2, 110, PUBLISHER)


def copyright_page(c, meta):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("FredokaMed", 11)
    lines = [meta["display_title"], "", f"Copyright © {meta['year']} {PUBLISHER}", "All rights reserved.", "",
             "No part of this book may be reproduced or shared in any form",
             "without written permission from the publisher, except for personal use.", "",
             "Coloring tip: place a sheet of cardboard behind the page",
             "when using markers. Crayons and colored pencils work best!"]
    y = 230
    for ln in lines:
        c.drawCentredString(TRIM_W / 2, y, ln)
        y -= 16


def belongs_page(c, r):
    frame(c)
    p = Pen(c, color=False, lw=LW)
    with p.width(.55):
        p.text_outline("THIS BOOK", TRIM_W / 2, 640, 60)
        p.text_outline("BELONGS TO", TRIM_W / 2, 570, 60)
    c.setLineWidth(3)
    c.line(110, 470, 502, 470)
    with p.at(306, 280, 2.6):
        A.bear(p, "party")
    for x, y in ((110, 380), (500, 380), (120, 150), (490, 150)):
        p.star(x, y, 18, "yellow")


def test_page(c):
    frame(c)
    p = Pen(c, color=False, lw=LW)
    with p.width(.55):
        p.text_outline("COLOR TEST PAGE", TRIM_W / 2, 680, 46)
    c.setFont("FredokaMed", 14)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(TRIM_W / 2, 640, "Try your crayons and markers here!")
    for row in range(5):
        for col in range(5):
            x = 120 + col * 93
            y = 540 - row * 95
            if (row + col) % 3 == 0:
                p.circle(x, y, 34)
            elif (row + col) % 3 == 1:
                p.heart(x, y, 34)
            else:
                p.star(x, y, 40)


# ----------------------------------------------------------------- cover
THEME_COLORS = {
    "animals": ((.36, .75, .96), "orange"), "vehicles": ((1, .78, .2), "red"), "fantasy": ((.98, .62, .8), "purple"),
    "dinos": ((.45, .8, .45), "orange"), "abc": ((.55, .5, .95), "yellow"), "numbers": ((1, .55, .35), "blue"),
    "seasonal": ((.85, .2, .25), "green"),
}


def outlined(c, txt, x, y, size, fill=(1, 1, 1), stroke=(0.1, .1, .2), sw=None, font="FredokaBold"):
    sw = sw or size * .14
    w = stringWidth(txt, font, size)
    for mode, lw, col in ((1, sw, stroke), (0, 0, fill)):
        t = c.beginText()
        t.setFont(font, size)
        t.setTextRenderMode(mode)
        t.setTextOrigin(x - w / 2, y)
        c.saveState()
        c.setLineJoin(1)
        c.setLineWidth(lw)
        c.setStrokeColorRGB(*col)
        c.setFillColorRGB(*col)
        t.textOut(txt)
        c.drawText(t)
        c.restoreState()


def make_cover(path, meta, pages, theme, r, n_pages):
    spine = n_pages * PAPER_IN_PER_PAGE * IN
    W = 2 * BLEED + 2 * TRIM_W + spine
    H = 2 * BLEED + TRIM_H
    c = canvas.Canvas(path, pagesize=(W, H), initialFontName="FredokaMed")
    c.setTitle(meta["display_title"] + " - Cover")
    bg, accent = THEME_COLORS[theme]
    if theme == "seasonal" and meta.get("season") != "winter":
        bg = (.3, .75, .7)
    c.setFillColorRGB(*bg)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # soft pattern
    lighter = tuple(min(1, v + .12) for v in bg)
    c.setFillColorRGB(*lighter)
    rr = random.Random(r.random())
    for i in range(70):
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        c.circle(x, y, rr.uniform(6, 22), stroke=0, fill=1)

    fx = BLEED + TRIM_W + spine  # front panel origin
    cx = fx + TRIM_W / 2
    # title block
    lines = meta["title_lines"]
    y = H - BLEED - 115
    sizes = [60, 76, 52]
    for i, ln in enumerate(lines):
        sz = fit_text(ln, "FredokaBold", sizes[min(i, 2)], TRIM_W - 90)
        outlined(c, ln, cx, y, sz, fill=(1, 1, 1) if i != 1 else PALETTE["yellow"])
        y -= sz * 1.08
    # hero card
    card_y0, card_h = BLEED + 150, y - BLEED - 160
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(.1, .1, .2)
    c.setLineWidth(5)
    c.roundRect(fx + 55, card_y0, TRIM_W - 110, card_h, 36, stroke=1, fill=1)
    heroes = meta["cover_subjects"]
    p = Pen(c, color=True, lw=4.2)
    mid_y = card_y0 + card_h / 2
    s_big = min(card_h / 102, 3.9)
    name, fn, acc = heroes[0]
    with p.at(cx + 60, mid_y + 5, s_big):
        fn(p, acc) if acc else fn(p)
    for (name, fn, acc), (dx, dy) in zip(heroes[1:3], ((-165, card_h * .22), (-170, -card_h * .24))):
        with p.at(cx + dx, mid_y + dy, s_big * .42):
            fn(p, acc) if acc else fn(p)
    # bottom ribbon
    ry = BLEED + 70
    c.setFillColorRGB(*PALETTE[accent])
    c.setStrokeColorRGB(.1, .1, .2)
    c.setLineWidth(4)
    c.roundRect(fx + 70, ry, TRIM_W - 140, 60, 30, stroke=1, fill=1)
    outlined(c, meta["ribbon"], cx, ry + 19, fit_text(meta["ribbon"], "FredokaBold", 30, TRIM_W - 190), sw=4)
    # badge
    bx, by = fx + TRIM_W - 95, H - BLEED - 300
    c.setFillColorRGB(*PALETTE["red"])
    c.setLineWidth(4)
    c.circle(bx, by, 52, stroke=1, fill=1)
    outlined(c, str(meta["n_drawings"]), bx, by + 2, 40, sw=4)
    outlined(c, "PAGES", bx, by - 24, 17, sw=3)
    c.setFont("FredokaMed", 15)
    c.setFillColorRGB(.1, .1, .2)
    c.drawCentredString(cx, BLEED + 32, PUBLISHER)

    # back cover
    bxo = BLEED
    bcx = bxo + TRIM_W / 2
    top = H - BLEED - 50
    bot = BLEED + 130
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(.1, .1, .2)
    c.setLineWidth(4)
    c.roundRect(bxo + 50, bot, TRIM_W - 100, top - bot, 30, stroke=1, fill=1)
    outlined(c, meta["back_head"], bcx, top - 60, fit_text(meta["back_head"], "FredokaBold", 34, TRIM_W - 150),
             fill=PALETTE[accent], sw=4)
    c.setFillColorRGB(.1, .1, .2)
    c.setFont("FredokaMed", 17)
    yy = top - 110
    for ln in meta["back_lines"]:
        c.drawString(bxo + 90, yy, ln)
        yy -= 27
    thumbs = [pg for pg in pages if pg.kind == "subject"][:3]
    tw = (TRIM_W - 160) / 3
    th = min(tw * 1.25, yy - bot - 40)
    for i, pg in enumerate(thumbs):
        tx = bxo + 80 + i * tw
        ty = bot + 30
        c.setLineWidth(2.5)
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(.1, .1, .2)
        c.roundRect(tx + 6, ty, tw - 12, th, 14, stroke=1, fill=1)
        pp = Pen(c, color=False, lw=2.2)
        with pp.at(tx + tw / 2, ty + th * .56, min(tw, th) / 118, flip=pg.flip):
            pg.fn(pp, pg.acc) if pg.acc else pg.fn(pp)
        c.setFont("FredokaBold", 12)
        c.setFillColorRGB(.1, .1, .2)
        c.drawCentredString(tx + tw / 2, ty + 10, pg.label)
    c.setFont("FredokaBold", 15)
    c.setFillColorRGB(.1, .1, .2)
    c.drawString(bxo + 60, BLEED + 60, PUBLISHER)
    # barcode zone is the bottom-right of back cover: keep clear (Amazon prints barcode there)
    c.showPage()
    c.save()
    return W / IN, H / IN, spine / IN


# ----------------------------------------------------------------- metadata
TITLE_WORDS = {
    "animals": ["Cute Animals", "Happy Animals", "Animal Friends", "Baby Animals", "Silly Animals", "Sweet Animals",
                "Cuddly Animals", "Zoo & Farm Animals"],
    "vehicles": ["Things That Go", "Cars, Trucks & More", "Busy Vehicles", "Big Trucks & Cars", "Vroom Vroom",
                 "Wheels & Wings", "Diggers & Trucks"],
    "fantasy": ["Princesses & Unicorns", "Magical Friends", "Fairy Tale", "Princess & Mermaid", "Enchanted",
                "Royal Friends"],
    "dinos": ["Cute Dinosaurs", "Baby Dinosaurs", "Dino Friends", "Happy Dinosaurs", "Roar! Dinosaurs"],
    "abc": ["ABC", "Alphabet", "My First ABC", "Letters A to Z"],
    "numbers": ["Numbers & Shapes", "123 Counting", "Count to 20", "My First Numbers"],
    "seasonal_winter": ["Christmas", "Merry Christmas", "Winter Holiday", "Holiday Fun"],
    "seasonal_mixed": ["My First Big", "Everyday Things", "Simple Things", "First Words"],
}


def make_meta(theme, vol, r, pages, month, today):
    key = theme if theme != "seasonal" else ("seasonal_winter" if month in (11, 12, 1) else "seasonal_mixed")
    words = TITLE_WORDS[key]
    word = words[(vol - 1) % len(words)]
    cycle = (vol - 1) // len(words)
    n = sum(1 for pg in pages)
    title_lines = ["My First", word, "Coloring Book"] if theme not in ("abc", "numbers") else [word, "Coloring Book", "for Toddlers"]
    if theme in ("abc", "numbers") and word.startswith("My First"):
        title_lines = ["My First", word.replace("My First ", ""), "Coloring Book"]
    display = " ".join(title_lines).replace("My First My First", "My First")
    title = f"{display} for Toddlers" if "Toddlers" not in display else display
    if cycle:
        title += f" {cycle + 1}"
    age = "Ages 2-4"
    subj = {"animals": "Cute Animals", "vehicles": "Cars, Trucks, Trains & More", "fantasy": "Princesses, Unicorns & Mermaids",
            "dinos": "Cute Dinosaurs", "abc": "Letters A to Z with Fun Pictures", "numbers": "Numbers 1-20 & Shapes",
            "seasonal_winter": "Christmas & Winter Pictures", "seasonal_mixed": "Simple Everyday Things"}[key]
    subtitle = f"{n} Big & Simple {subj} to Color for Kids {age} | Bold Lines, One Picture per Page"
    picks = [pg for pg in pages if pg.kind == "subject"]
    hero_pool = r.sample(picks, min(3, len(picks)))
    pref = {"seasonal_winter": ["SANTA", "SNOWMAN", "CHRISTMAS TREE", "REINDEER", "GINGERBREAD"],
            "fantasy": ["UNICORN", "PRINCESS", "MERMAID", "CASTLE"], "dinos": ["T-REX", "TRICERATOPS", "STEGOSAURUS"],
            "vehicles": ["FIRE TRUCK", "DUMP TRUCK", "TRACTOR", "CAR", "TRAIN", "DIGGER"]}.get(key)
    if pref:
        top = [pg for pg in picks if pg.label in pref]
        if top:
            first = r.choice(top)
            rest = [pg for pg in hero_pool if pg is not first][:2]
            hero_pool = [first] + rest
    if theme == "abc":
        hero_pool = [Page("subject", w, f) for L, w, f in r.sample(O.ABC, 3)]
    if theme == "numbers":
        hero_pool = [Page("subject", nm, f) for nm, f in r.sample(O.SHAPES, 3)]
    cover_subjects = [(pg.label, pg.fn, pg.acc) for pg in hero_pool]
    ribbon = {"animals": "BIG & EASY PAGES FOR AGES 2-4", "vehicles": "BIG & EASY PAGES FOR AGES 2-4",
              "fantasy": "BIG & EASY PAGES FOR AGES 2-4", "dinos": "BIG & EASY PAGES FOR AGES 2-4",
              "abc": "LEARN & COLOR  -  AGES 2-4", "numbers": "COUNT & COLOR  -  AGES 2-4",
              "seasonal": "BIG & EASY PAGES FOR AGES 2-4"}[theme]
    back_lines = [
        f"{n} big, simple pictures made for little hands.",
        "",
        "  •  Thick, bold outlines that are easy to stay inside",
        "  •  One picture per page, printed on one side only",
        "  •  A word under every picture to learn new words",
        "  •  Great for crayons, pencils and markers",
        "  •  Builds focus, fine motor skills and creativity",
        "",
        "Perfect for home, travel, daycare and preschool!",
    ]
    keywords = {
        "animals": ["toddler coloring book ages 1-3", "animal coloring book for kids ages 2-4", "my first coloring book",
                    "big simple coloring pages toddlers", "preschool coloring book animals", "easy coloring book for kids",
                    "coloring books for 2 year olds"],
        "vehicles": ["truck coloring book for toddlers", "car coloring book kids ages 2-4", "vehicles coloring book boys",
                     "things that go coloring book", "construction coloring book toddler", "my first coloring book trucks",
                     "coloring books for 3 year olds"],
        "fantasy": ["princess coloring book toddlers", "unicorn coloring book kids ages 2-4", "mermaid coloring book girls",
                    "toddler coloring book for girls", "fairy tale coloring book preschool", "my first coloring book princess",
                    "easy coloring book for 3 year olds"],
        "dinos": ["dinosaur coloring book toddlers", "dino coloring book kids ages 2-4", "toddler coloring book boys",
                  "big simple coloring pages dinosaurs", "preschool coloring book", "my first dinosaur book",
                  "coloring books for 2 year olds"],
        "abc": ["abc coloring book toddlers", "alphabet coloring book preschool", "letter coloring book ages 2-4",
                "learn letters toddler activity book", "kindergarten coloring book", "my first abc book",
                "toddler learning coloring book"],
        "numbers": ["numbers coloring book toddlers", "123 coloring book preschool", "counting coloring book kids",
                    "shapes coloring book ages 2-4", "toddler learning activity book", "math coloring book kindergarten",
                    "my first numbers book"],
        "seasonal_winter": ["christmas coloring book toddlers", "christmas gifts for toddlers", "stocking stuffers for kids",
                            "winter coloring book ages 2-4", "santa coloring book kids", "holiday coloring book preschool",
                            "christmas activity book for kids"],
        "seasonal_mixed": ["toddler coloring book ages 1-3", "my first coloring book", "big simple coloring pages",
                           "easy coloring book for kids", "preschool coloring book", "coloring books for 2 year olds",
                           "first words coloring book"],
    }[key]
    third = {"animals": "Children's Books > Animals > General",
             "vehicles": "Children's Books > Cars, Trains & Things That Go > General",
             "fantasy": "Children's Books > Fairy Tales, Folk Tales & Myths > General",
             "dinos": "Children's Books > Animals > Dinosaurs",
             "seasonal_winter": "Children's Books > Holidays & Celebrations > Christmas",
             "seasonal_mixed": "Children's Books > Early Learning > Basic Concepts > General"}
    if theme == "abc":
        categories = ["Children's Books > Activities, Crafts & Games > Coloring Books",
                      "Children's Books > Early Learning > Basic Concepts > Alphabet",
                      "Children's Books > Activities, Crafts & Games > Activity Books"]
    elif theme == "numbers":
        categories = ["Children's Books > Activities, Crafts & Games > Coloring Books",
                      "Children's Books > Early Learning > Basic Concepts > Counting",
                      "Children's Books > Early Learning > Basic Concepts > Shapes"]
    else:
        categories = ["Children's Books > Activities, Crafts & Games > Coloring Books",
                      "Children's Books > Activities, Crafts & Games > Activity Books", third[key]]
    desc = (f"<p><b>A first coloring book your toddler will love!</b></p>"
            f"<p>{title} is packed with {n} big, simple pictures with thick, bold lines that are easy for little hands "
            f"to color. Every picture is printed on its own page with a word underneath, so kids can learn new words while they color.</p>"
            f"<p><b>Inside you'll find:</b></p><ul>"
            f"<li>{n} single-sided coloring pages (no bleed-through)</li>"
            f"<li>Large 8.5 x 11 inch pages</li><li>Thick outlines, simple shapes and lots of space to color</li>"
            f"<li>A 'This Book Belongs To' page and a color test page</li>"
            f"<li>Great for crayons, colored pencils and markers</li></ul>"
            f"<p>Coloring helps build fine motor skills, focus, hand-eye coordination and color recognition. "
            f"A perfect gift for birthdays, holidays, travel, daycare and preschool.</p>"
            f"<p><b>Grab your copy today and let the coloring fun begin!</b></p>")
    season = "winter" if key == "seasonal_winter" else None
    return {
        "date": today.isoformat(), "theme": theme, "volume": vol, "year": today.year,
        "title": title, "subtitle": subtitle, "display_title": title, "title_lines": title_lines,
        "series": "Tiny Crayon Toddler Coloring Books", "author": PUBLISHER, "publisher": PUBLISHER,
        "description_html": desc, "keywords": keywords, "categories": categories,
        "reading_age": "2 - 4", "price_usd": 6.99, "n_drawings": n, "cover_subjects": cover_subjects,
        "ribbon": ribbon, "back_head": "BIG PICTURES FOR LITTLE HANDS!", "back_lines": back_lines, "season": season,
    }


def build(out_dir, day=None, theme=None):
    register()
    today = day or dt.date.today()
    idx = (today - EPOCH).days
    theme = theme or ROTATION[idx % len(ROTATION)]
    vol = idx // len(ROTATION) + 1
    r = random.Random(idx * 7919 + 17)
    pages = build_pages(theme, r, today.month)
    meta = make_meta(theme, vol, r, pages, today.month, today)
    os.makedirs(out_dir, exist_ok=True)
    slug = f"{today.isoformat()}_{theme}_v{vol}"
    interior = os.path.join(out_dir, slug + "_interior.pdf")
    cover = os.path.join(out_dir, slug + "_cover.pdf")

    c = canvas.Canvas(interior, pagesize=(TRIM_W, TRIM_H), initialFontName="FredokaMed")
    c.setTitle(meta["title"])
    c.setAuthor(PUBLISHER)
    hero = meta["cover_subjects"][0]
    title_page(c, meta, lambda p: hero[1](p, hero[2]) if hero[2] else hero[1](p)); c.showPage()
    copyright_page(c, meta); c.showPage()
    belongs_page(c, r); c.showPage()
    test_page(c); c.showPage()
    for pg in pages:
        draw_page(c, pg, r)
        c.showPage()
        blank_back(c)
        c.showPage()
    c.save()
    n_pages = 4 + 2 * len(pages)
    cw, ch, sp = make_cover(cover, meta, pages, theme, r, n_pages)

    m = {k: v for k, v in meta.items() if k not in ("cover_subjects", "title_lines", "back_lines", "display_title")}
    m.update({"interior_pages": n_pages, "trim": "8.5 x 11 in", "bleed": "No bleed (interior)",
              "paper": "White paper, black & white interior", "cover_finish": "Matte",
              "cover_size_in": f"{cw:.3f} x {ch:.3f}", "spine_in": round(sp, 4),
              "files": {"interior": os.path.basename(interior), "cover": os.path.basename(cover)}})
    with open(os.path.join(out_dir, slug + "_listing.json"), "w") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)
    with open(os.path.join(out_dir, slug + "_listing.txt"), "w") as f:
        f.write(listing_text(m))
    return {"slug": slug, "interior": interior, "cover": cover, "meta": m}


def listing_text(m):
    L = [
        "AMAZON KDP LISTING  (copy each field as-is)", "=" * 48, "",
        f"Language: English", f"Book Title: {m['title']}", f"Subtitle: {m['subtitle']}",
        f"Series: {m['series']}  |  Volume: {m['volume']}", f"Author (pen name): {m['author']}",
        f"Publisher / Imprint: {m['publisher']}", "", "Description (paste into the HTML box):", m["description_html"], "",
        "Keywords (7 boxes):"] + [f"  {i + 1}. {k}" for i, k in enumerate(m["keywords"])] + [
        "", "Categories (choose up to 3):"] + [f"  - {k}" for k in m["categories"]] + [
        "", f"Reading age: {m['reading_age']}", "Primary audience: No sexually explicit content", "Low-content book: NO",
        "Large print: NO", "AI-generated content: YES - Images (drawings were generated by an AI tool)",
        "", "PRINT SETTINGS", f"  Ink & paper: Black & white interior, white paper", f"  Trim size: {m['trim']}",
        f"  Bleed: {m['bleed']}", f"  Cover finish: {m['cover_finish']}", f"  Interior pages: {m['interior_pages']}",
        f"  Cover file size: {m['cover_size_in']} in (spine {m['spine_in']} in)",
        f"  Suggested list price: ${m['price_usd']} (Amazon.com)", "",
        f"Files: {m['files']['interior']}  +  {m['files']['cover']}",
    ]
    return "\n".join(L) + "\n"
