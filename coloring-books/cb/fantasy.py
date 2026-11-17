"""Princesses, mermaids, unicorns and friends."""
import math
from .common import hat, flower
from .animals import horse, frog


def _back_hair(p, x=0, y=14, hair="gold", style=0):
    r = 15
    if style == 0:  # long
        p.path([("M", x - r - 2, y + 2), ("Q", x - r - 6, y - 26, x - r + 2, y - 30), ("L", x + r - 2, y - 30),
                ("Q", x + r + 6, y - 26, x + r + 2, y + 2)], hair)
    elif style == 1:  # pigtails
        for sx in (-1, 1):
            p.ellipse(x + sx * (r + 6), y - 2, 6, 11, hair, rot=sx * 20)
            p.circle(x + sx * (r + 1), y + 6, 3, "pink")
    elif style == 2:  # bun
        p.circle(x, y + r + 3, 7, hair)


def _girl_head(p, x=0, y=14, hair="gold", style=0, crown=True):
    r = 15
    if style != 0:
        _back_hair(p, x, y, hair, style)
    p.circle(x, y, r, "peach")
    # fringe
    p.path([("M", x - r, y + 2), ("Q", x - r, y + r + 3, x, y + r + 1), ("Q", x + r, y + r + 3, x + r, y + 2),
            ("Q", x + 8, y + 10, x + 2, y + 7), ("Q", x - 2, y + 12, x - 6, y + 7), ("Q", x - 10, y + 10, x - r, y + 2)],
           hair)
    p.face(x, y - 2, .85, eye_gap=6)
    if crown:
        hat(p, x, y + r + 1, .8, "crown")


def princess(p, acc=None, style=0, dress="pink"):
    hair = "gold" if style != 1 else "brown"
    if style == 0:
        _back_hair(p, 0, 14, hair, 0)
    p.path([("M", -10, -2), ("L", -30, -44), ("Q", 0, -50, 30, -44), ("L", 10, -2)], dress)
    with p.width(.7):
        p.curve((-24, -36), (-12, -40), (0, -36), (12, -40), (24, -36))
    for x, y in ((-12, -24), (10, -30), (0, -16), (-4, -34)):
        p.star(x, y, 3, "yellow")
    p.rect(-10, -6, 20, 8, dress, r=3)
    for sx in (-1, 1):
        p.ellipse(sx * 16, -10, 3.5, 9, "peach", rot=sx * 25)
        p.ellipse(sx * 12, 0, 5, 5, dress)
    _girl_head(p, 0, 14, hair, style)


def princess2(p, acc=None):
    princess(p, style=1, dress="lilac")


def princess3(p, acc=None):
    princess(p, style=2, dress="sky")


def mermaid(p, acc=None):
    _back_hair(p, 0, 22, "red", 0)
    p.path([("M", -12, -8), ("Q", -16, -30, 4, -38), ("Q", 16, -44, 24, -38), ("Q", 6, -30, 12, -8)], "teal")
    p.path([("M", 22, -38), ("Q", 34, -30, 40, -40), ("Q", 34, -50, 22, -44), ("Q", 20, -54, 8, -50),
            ("Q", 18, -44, 22, -38)], "teal")
    with p.width(.6):
        for x, y in ((-4, -14), (4, -14), (0, -22), (8, -22), (4, -30)):
            p.arc(x, y, 3.5, 200, 340)
    p.rect(-11, -8, 22, 16, "peach", r=5)
    for sx in (-1, 1):
        p.circle(sx * 5, 4, 4.2, "purple")
        p.ellipse(sx * 15, -2, 3.5, 9, "peach", rot=sx * 25)
    _girl_head(p, 0, 22, "red", 0, crown=False)
    flower(p, 11, 34, 3.5, "pink")
    for x, y, r in ((-30, 10, 3), (-34, 20, 2.2), (-28, 28, 1.6), (30, 6, 2.6)):
        p.circle(x, y, r, "white")


def unicorn(p, acc=None):
    horse(p, unicorn=True)


def pegasus(p, acc=None):
    p.path([("M", -4, -4), ("Q", -24, 30, -6, 34), ("Q", -12, 20, 2, 26), ("Q", -2, 10, 10, 14),
            ("Q", 4, 0, 6, -6)], "white")
    horse(p, unicorn=True)


def castle(p, acc=None):
    for x in (-36, 24):
        p.rect(x, -40, 12, 50, "lilac")
        p.poly([(x - 3, 10), (x + 6, 30), (x + 15, 10)], "purple")
        p.line(x + 6, 30, x + 6, 38)
        p.poly([(x + 6, 38), (x + 14, 35), (x + 6, 32)], "pink")
        _win = (x + 3, -6, 6, 9)
        p.rect(*_win, "sky", r=3)
    p.rect(-24, -40, 48, 40, "lilac")
    for x in range(-24, 24, 8):
        p.rect(x, 0, 6, 6, "lilac")
    p.rect(-10, 6, 20, 24, "lilac")
    p.poly([(-13, 30), (0, 46), (13, 30)], "purple")
    p.circle(0, 18, 5, "sky")
    p.path([("M", -9, -40), ("L", -9, -24), ("Q", 0, -12, 9, -24), ("L", 9, -40)], "brown")
    for x in (-16, 16):
        p.rect(x - 3, -18, 6, 9, "sky", r=3)


def crown(p, acc=None):
    p.poly([(-34, -16), (-40, 22), (-20, 4), (0, 30), (20, 4), (40, 22), (34, -16)], "gold")
    p.rect(-36, -28, 72, 14, "gold", r=4)
    for x, role in ((-22, "red"), (0, "blue"), (22, "green")):
        p.ellipse(x, -21, 5, 4, role)
    for x, y in ((-40, 22), (0, 30), (40, 22)):
        p.circle(x, y + 3, 4, "pink")
    p.heart(0, 4, 6, "red")


def fairy(p, acc=None):
    for sx in (-1, 1):
        p.ellipse(sx * 18, 6, 14, 18, "sky", rot=sx * -30)
        p.ellipse(sx * 14, -16, 9, 11, "lilac", rot=sx * 30)
    p.path([("M", -8, -2), ("L", -18, -34), ("L", -10, -30), ("L", -4, -36), ("L", 4, -30), ("L", 10, -36),
            ("L", 18, -34), ("L", 8, -2)], "green")
    for sx in (-1, 1):
        p.lines([(sx * 4, -34), (sx * 5, -44)])
    p.ellipse(-12, -8, 3.5, 8, "peach", rot=-25)
    p.lines([(14, -6), (24, 10)])
    p.star(25, 13, 5, "yellow")
    p.ellipse(12, -8, 3.5, 8, "peach", rot=25)
    _girl_head(p, 0, 14, "brown", 2, crown=False)
    for x, y in ((-34, 30), (32, 30), (-30, -30)):
        p.star(x, y, 3.5, "yellow")


def dragon(p, acc=None):
    role = "green"
    p.path([("M", -6, 4), ("Q", -30, 34, -42, 20), ("Q", -34, 18, -36, 10), ("Q", -28, 12, -26, 4),
            ("Q", -20, 6, -16, -4)], "lime")
    p.path([("M", 14, -30), ("Q", 34, -36, 40, -24), ("L", 46, -22), ("L", 40, -18), ("Q", 32, -28, 14, -22)], role)
    p.ellipse(0, -22, 20, 20, role)
    p.ellipse(0, -26, 12, 13, "yellow")
    with p.width(.6):
        for y in (-20, -26, -32):
            p.line(-10, y, 10, y)
    for sx in (-1, 1):
        p.ellipse(sx * 10, -42, 7, 4.5, role)
    for sx in (-1, 1):
        p.poly([(sx * 8, 26), (sx * 14, 38), (sx * 16, 24)], "cream")
    p.circle(0, 12, 18, role)
    p.ellipse(0, 4, 10, 7, "lime")
    p.dot(-3, 6, 1)
    p.dot(3, 6, 1)
    p.face(0, 14, .9, mouth=None, eye_gap=7)
    p.smile(0, 0, 3, 2)
    for x in (-6, 0, 6):
        p.poly([(x - 3, 29), (x, 35), (x + 3, 29)], "orange")


def wand(p, acc=None):
    p.rect(-3, -46, 6, 50, "purple", r=3)
    with p.width(.7):
        p.lines([(-3, -6), (3, -10)])
        p.lines([(-3, -16), (3, -20)])
    p.star(0, 18, 22, "yellow", inner=.5)
    p.face(0, 16, .8)
    for x, y, r in ((-30, 30, 5), (30, 36, 4), (-26, 0, 3.5), (28, 4, 4.5), (0, 46, 3)):
        p.star(x, y, r, "yellow")
    p.heart(-30, -24, 5, "pink")
    p.heart(28, -30, 4, "pink")


def rainbow(p, acc=None):
    cols = ["red", "orange", "yellow", "green", "blue", "purple"]
    for i, c in enumerate(cols):
        r = 44 - i * 6
        p.halfdisc(0, -10, r, r, c)
    p.halfdisc(0, -10, 8, 8, "white")
    p.cloud(-34, -16, 22, "white")
    p.cloud(34, -16, 22, "white")


def carriage(p, acc=None):
    p.path([("M", -30, -10), ("L", -34, -14), ("L", 34, -14), ("L", 30, -10)], "gold")
    p.smooth([(0, 34), (24, 30), (34, 10), (28, -12), (0, -16), (-28, -12), (-34, 10), (-24, 30)], "orange")
    for x in (-14, 0, 14):
        p.curve((x * .2, 32), (x, 10), (x * .2, -14))
    p.rect(-8, 2, 16, 16, "sky", r=8)
    p.curve((0, 34), (2, 40), (8, 42))
    p.ellipse(10, 38, 5, 2.5, "green", rot=20)
    for x in (-24, 24):
        p.circle(x, -24, 11, "none")
        p.circle(x, -24, 3, "gold")
        for a in range(0, 180, 45):
            t = math.radians(a)
            p.line(x - 11 * math.cos(t), -24 - 11 * math.sin(t), x + 11 * math.cos(t), -24 + 11 * math.sin(t))


def frog_prince(p, acc=None):
    frog(p, acc="crown")


def chest(p, acc=None):
    p.rect(-36, -36, 72, 40, "brown", r=3)
    p.path([("M", -36, 4), ("Q", -36, 30, 0, 30), ("Q", 36, 30, 36, 4)], "brown")
    for x in (-24, 24):
        p.rect(x - 3, -36, 6, 66 if False else 40, "gold")
    p.rect(-8, -8, 16, 16, "gold", r=3)
    p.circle(0, 1, 2.5, "ink")
    p.poly([(-1.5, 0), (1.5, 0), (0, -5)], "ink")
    for x, y in ((-30, 36), (-14, 40), (14, 40), (30, 34)):
        p.circle(x, y, 5, "gold")
    p.star(0, 42, 6, "yellow")


def cupcake(p, acc=None, s=1):
    p.path([("M", -22 * s, -4 * s), ("L", -16 * s, -40 * s), ("L", 16 * s, -40 * s), ("L", 22 * s, -4 * s)], "pink")
    with p.width(.7):
        for x in (-10, -2, 6, 13):
            p.line(x * s, -6 * s, (x * .8) * s, -38 * s)
    p.path([("M", -26 * s, -4 * s), ("Q", -34 * s, 10 * s, -20 * s, 14 * s), ("Q", -24 * s, 30 * s, -6 * s, 28 * s),
            ("Q", 0, 40 * s, 8 * s, 28 * s), ("Q", 26 * s, 30 * s, 20 * s, 14 * s), ("Q", 34 * s, 10 * s, 26 * s, -4 * s),
            ("Q", 0, -10 * s, -26 * s, -4 * s)], "cream")
    p.circle(2 * s, 36 * s, 6 * s, "red")
    for x, y in ((-14, 8), (10, 6), (-2, 18), (14, 18), (-12, 20)):
        p.ellipse(x * s, y * s, 2.5 * s, 1.2 * s, "blue", rot=30)


def seahorse(p, acc=None):
    p.smooth([(6, 34), (18, 30), (20, 18), (10, 10), (14, -4), (10, -20), (0, -30), (-6, -40), (4, -46),
              (-12, -46), (-14, -32), (-4, -16), (-4, 0), (-8, 14), (-6, 28)], "orange")
    p.path([("M", 18, 28), ("L", 32, 28), ("L", 32, 22), ("L", 18, 22)], "orange")
    p.eye(8, 26, 2.6)
    p.path([("M", -6, 18), ("Q", -20, 14, -14, 4), ("Q", -10, 10, -4, 8)], "yellow")
    for x, y in ((-4, 36), (2, 38), (8, 37)):
        p.poly([(x - 2, y - 2), (x, y + 4), (x + 2, y - 2)], "yellow")
    for x, y, r in ((-30, 20, 3), (-34, 30, 2), (30, 0, 2.6)):
        p.circle(x, y, r, "white")


def swan(p, acc=None):
    p.path([("M", -34, -14), ("Q", -40, 10, -24, 6), ("Q", -10, -2, 4, 0), ("Q", 30, 4, 30, -18),
            ("Q", 20, -32, -10, -30), ("Q", -30, -28, -34, -14)], "white")
    p.path([("M", -16, -6), ("Q", -4, 10, 14, -2), ("Q", 6, -16, -16, -6)], "white")
    p.path([("M", 16, -6), ("Q", 30, 6, 22, 20), ("Q", 14, 34, 22, 40), ("Q", 32, 42, 32, 34), ("Q", 24, 30, 30, 20),
            ("Q", 38, 6, 26, -12)], "white")
    p.poly([(32, 38), (40, 34), (31, 32)], "orange")
    p.eye(27, 36, 2.2)
    hat(p, 25, 41, .55, "crown")
    p.path([("M", -48, -34), ("Q", -36, -26, -24, -34), ("Q", -12, -26, 0, -34), ("Q", 12, -26, 24, -34),
            ("Q", 36, -26, 48, -34), ("L", 48, -44), ("L", -48, -44)], "sky")


def teaset(p, acc=None):
    p.ellipse(-16, -30, 22, 6, "white")
    p.path([("M", -32, -4), ("Q", -32, -30, -16, -30), ("Q", 0, -30, 0, -4)], "pink")
    p.ellipse(-16, -4, 16, 4, "pink")
    p.path([("M", 0, -10), ("Q", 10, -10, 10, -18), ("Q", 6, -24, -1, -22)], closed=False)
    p.heart(-16, -16, 5, "white")
    p.path([("M", 14, -32), ("L", 14, 6), ("Q", 14, 18, 28, 18), ("Q", 42, 18, 42, 6), ("L", 42, -32)], "sky")
    p.path([("M", 14, 4), ("Q", 2, 14, 4, 26), ("L", 8, 26), ("Q", 8, 16, 16, 12)], "sky")
    p.ellipse(28, 20, 10, 3, "sky")
    p.circle(28, 25, 3, "pink")
    flower(p, 28, -10, 6, "pink")
    p.ellipse(28, -32, 16, 3, "white")


FANTASY = [
    ("PRINCESS", princess), ("PRINCESS", princess2), ("PRINCESS", princess3), ("MERMAID", mermaid),
    ("UNICORN", unicorn), ("PEGASUS", pegasus), ("CASTLE", castle), ("CROWN", crown), ("FAIRY", fairy),
    ("DRAGON", dragon), ("MAGIC WAND", wand), ("RAINBOW", rainbow), ("CARRIAGE", carriage),
    ("FROG PRINCE", frog_prince), ("TREASURE", chest), ("CUPCAKE", cupcake),
    ("SWAN", swan), ("TEA PARTY", teaset),
]
