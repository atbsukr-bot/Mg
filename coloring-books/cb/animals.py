"""Cute toddler animals. Each fn(p, acc) draws in the -50..50 box.
acc: optional accessory kind for the head ("party", "bow", "santa", ...)."""
import math
from .common import sit_body, hat


def _acc(p, acc, x, y, s=1):
    if acc:
        hat(p, x, y, s, acc)


def cat(p, acc=None, tiger=False):
    role = "orange"
    # tail
    p.path([("M", 14, -36), ("C", 40, -40, 42, -10, 30, 0), ("C", 27, 4, 22, 2, 25, -3),
            ("C", 33, -14, 30, -30, 14, -28)], role)
    sit_body(p, role, belly="cream")
    for sx in (-1, 1):
        p.poly([(sx * 20, 18), (sx * 17, 40), (sx * 4, 28)], role)
        p.poly([(sx * 16, 22), (sx * 15, 34), (sx * 8, 27)], "pink")
    p.ellipse(0, 10, 23, 20, role)
    if tiger:
        for sx in (-1, 1):
            p.poly([(sx * 23, 14), (sx * 15, 12), (sx * 23, 9)], "ink")
            p.poly([(sx * 22, 4), (sx * 15, 3), (sx * 21, 0)], "ink")
        p.poly([(-4, 30), (0, 22), (4, 30)], "ink")
        for sx in (-1, 1):
            p.poly([(sx * 18, -20), (sx * 11, -22), (sx * 17, -25)], "ink")
    p.face(0, 10, 1.05, mouth=None)
    p.poly([(-2.5, 6), (2.5, 6), (0, 3.5)], "pink")
    p.arc(-2.2, 3.4, 2.2, 200, 360)
    p.arc(2.2, 3.4, 2.2, 180, 340)
    with p.width(.6):
        for dy in (1, -2):
            p.line(-13, 4 + dy, -24, 6 + dy * 2)
            p.line(13, 4 + dy, 24, 6 + dy * 2)
    _acc(p, acc, 0, 29)


def tiger(p, acc=None):
    cat(p, acc, tiger=True)


def dog(p, acc=None):
    role = "tan"
    p.path([("M", 15, -30), ("Q", 30, -25, 33, -8), ("Q", 36, -6, 34, -2), ("Q", 26, -10, 15, -22)], role)
    sit_body(p, role, belly="cream")
    p.circle(0, 10, 21, role)
    p.ellipse(7, 15, 7, 6, "brown")  # eye patch
    p.ellipse(0, 1, 10, 7.5, "cream")
    for sx in (-1, 1):
        p.ellipse(sx * 21, 8, 7, 14, "brown", rot=sx * -18)
    p.face(0, 12, 1.0, mouth=None, blush=False)
    p.ellipse(0, 4, 3.6, 2.6, "ink")
    p.arc(-2.5, 0.4, 2.5, 200, 360)
    p.arc(2.5, 0.4, 2.5, 180, 340)
    p.path([("M", -1.8, -1.2), ("Q", 0, -6, 1.8, -1.2)], "rose")
    p.rect(-12, -12, 24, 4.5, "red", r=2.2)
    p.circle(0, -13, 3, "gold")
    _acc(p, acc, 0, 31)


def bear(p, acc=None, panda=False, koala=False):
    role = "white" if panda else ("gray" if koala else "brown")
    sit_body(p, role, belly=None if panda else "tan")
    if panda:
        for sx in (-1, 1):
            p.ellipse(sx * 16, -22, 5, 8, "gray", rot=sx * 25)
    for sx in (-1, 1):
        if koala:
            p.circle(sx * 20, 24, 11, role)
            p.circle(sx * 20, 24, 6.5, "pink")
        else:
            p.circle(sx * 16, 26, 8, "gray" if panda else role)
            p.circle(sx * 16, 26, 4.5, "pink" if not panda else "gray")
    p.circle(0, 10, 21, role)
    if panda:
        for sx in (-1, 1):
            p.ellipse(sx * 8, 12, 5.5, 7, "gray", rot=sx * -30)
    if koala:
        p.face(0, 12, 1.0, mouth=None)
        p.ellipse(0, 6, 4.8, 6, "dkgray")
        p.smile(0, -2, 2.5, 1.6)
    else:
        p.ellipse(0, 3, 8.5, 6.5, "tan" if not panda else "white")
        p.face(0, 12, 1.0, mouth=None, blush=not panda)
        p.ellipse(0, 6, 3.2, 2.3, "ink")
        p.arc(-2, 3, 2, 200, 360)
        p.arc(2, 3, 2, 180, 340)
    _acc(p, acc, 0, 31)


def panda(p, acc=None):
    bear(p, acc, panda=True)


def koala(p, acc=None):
    bear(p, acc, koala=True)


def bunny(p, acc=None):
    role = "white"
    p.circle(20, -36, 6, "white")
    sit_body(p, role, belly="pink")
    for sx in (-1, 1):
        p.ellipse(sx * 9, 36, 7, 18, role, rot=sx * 10)
        p.ellipse(sx * 9, 36, 3.5, 12, "pink", rot=sx * 10)
    p.ellipse(0, 8, 20, 18, role)
    p.face(0, 9, 1.0, mouth=None)
    p.poly([(-2.2, 5), (2.2, 5), (0, 3)], "pink")
    p.line(0, 3, 0, 1)
    p.arc(-2, 1, 2, 200, 360)
    p.arc(2, 1, 2, 180, 340)
    p.rect(-2.4, -3.5, 4.8, 4, "white", r=.8)
    p.line(0, -3.5, 0, .5)
    _acc(p, acc, 0, 26, .9)


def pig(p, acc=None):
    role = "pink"
    p.curve((18, -30), (25, -26), (22, -21), (27, -19), (25, -14))
    sit_body(p, role, belly="blush")
    for sx in (-1, 1):
        p.poly([(sx * 8, 26), (sx * 20, 32), (sx * 18, 18)], role)
    p.circle(0, 8, 21, role)
    p.face(0, 12, 1.05, mouth=None)
    p.ellipse(0, 2, 7.5, 5.5, "rose")
    p.ellipse(-2.5, 2, 1.3, 2, "ink")
    p.ellipse(2.5, 2, 1.3, 2, "ink")
    p.smile(0, -6, 3, 1.8)
    _acc(p, acc, 0, 29)


def mouse(p, acc=None):
    role = "gray"
    p.curve((15, -38), (32, -40), (38, -28), (30, -18))
    sit_body(p, role, belly="pink")
    for sx in (-1, 1):
        p.circle(sx * 17, 24, 11, role)
        p.circle(sx * 17, 24, 6.5, "pink")
    p.ellipse(0, 6, 18, 17, role)
    p.face(0, 9, .95, mouth=None)
    p.circle(0, 2, 2.6, "pink")
    p.arc(-2, -0.5, 2, 200, 360)
    p.arc(2, -0.5, 2, 180, 340)
    with p.width(.6):
        for dy in (0, -3):
            p.line(-9, 1 + dy, -20, 3 + dy * 1.5)
            p.line(9, 1 + dy, 20, 3 + dy * 1.5)
    _acc(p, acc, 0, 24)


def lion(p, acc=None):
    p.path([("M", 15, -34), ("C", 34, -38, 40, -20, 36, -6)], closed=False)
    p.ellipse(37, -4, 3.5, 5, "orange", rot=-20)
    sit_body(p, "gold", belly="cream")
    p.scallop(0, 10, 25, 12, 6, "orange")
    for sx in (-1, 1):
        p.circle(sx * 15, 25, 6, "gold")
        p.circle(sx * 15, 25, 3, "pink")
    p.circle(0, 9, 19, "gold")
    p.ellipse(0, 2, 8, 6, "cream")
    p.face(0, 12, 1.0, mouth=None)
    p.poly([(-3, 5), (3, 5), (0, 2)], "dkbrown")
    p.arc(-2, 0.5, 2, 200, 360)
    p.arc(2, 0.5, 2, 180, 340)
    _acc(p, acc, 0, 34)


def monkey(p, acc=None):
    role = "brown"
    p.curve((14, -36), (34, -36), (36, -18), (26, -14), (24, -22), (30, -24))
    sit_body(p, role, belly="tan")
    for sx in (-1, 1):
        p.circle(sx * 22, 10, 7.5, role)
        p.circle(sx * 22, 10, 4.2, "peach")
    p.circle(0, 10, 20, role)
    p.path([("M", 0, 16), ("C", -6, 24, -17, 18, -14, 8), ("C", -16, -2, -8, -6, 0, -6),
            ("C", 8, -6, 16, -2, 14, 8), ("C", 17, 18, 6, 24, 0, 16)], "peach")
    p.face(0, 11, 1.0, mouth=None, eye_gap=6)
    p.dot(-1.5, 5, .8)
    p.dot(1.5, 5, .8)
    p.smile(0, -1, 4.5, 3)
    p.curve((-2, 29), (0, 33), (3, 31))
    _acc(p, acc, 0, 30)


def fox(p, acc=None):
    role = "orange"
    p.smooth([(12, -36), (30, -40), (42, -24), (40, -8), (32, -12), (24, -26)], role)
    p.smooth([(36, -12), (40, -8), (42, -14), (40, -18)], "white")
    sit_body(p, role, belly="white")
    for sx in (-1, 1):
        p.poly([(sx * 21, 14), (sx * 22, 38), (sx * 6, 26)], role)
        p.poly([(sx * 18, 19), (sx * 19, 32), (sx * 10, 25)], "dkbrown")
    p.ellipse(0, 10, 22, 18, role)
    p.path([("M", -22, 8), ("Q", -12, -16, 0, -6), ("Q", 12, -16, 22, 8), ("Q", 10, -2, 0, 2),
            ("Q", -10, -2, -22, 8)], "white")
    p.face(0, 12, 1.0, mouth=None, blush=False)
    p.ellipse(0, 1, 2.8, 2, "ink")
    p.smile(0, -3, 2.5, 1.5)
    _acc(p, acc, 0, 28)


def cow(p, acc=None):
    role = "white"
    sit_body(p, role, belly=None)
    p.ellipse(-8, -22, 6, 5, "dkgray")
    p.ellipse(10, -30, 5, 4, "dkgray")
    for sx in (-1, 1):
        p.path([("M", sx * 10, 24), ("Q", sx * 18, 34, sx * 14, 40), ("Q", sx * 22, 32, sx * 16, 22)], "cream")
        p.ellipse(sx * 25, 18, 9, 4.5, role, rot=sx * -20)
    p.ellipse(0, 12, 20, 18, role)
    p.ellipse(-9, 20, 7, 5, "dkgray")
    p.ellipse(0, 0, 14, 9, "pink")
    p.ellipse(-5, 1, 1.6, 2.3, "ink")
    p.ellipse(5, 1, 1.6, 2.3, "ink")
    p.face(0, 15, 1.0, mouth=None, blush=False)
    p.smile(0, -5, 3, 1.8)
    p.rect(-6, -14, 12, 9, "gold", r=3)
    p.dot(0, -12, 1.2)
    _acc(p, acc, 0, 30)


def sheep(p, acc=None):
    p.scallop(0, -18, 22, 11, 5, "white")
    for sx in (-1, 1):
        p.rect(sx * 10 - 3, -48, 6, 10, "dkgray", r=2)
    p.scallop(0, 22, 12, 8, 4, "white")
    for sx in (-1, 1):
        p.ellipse(sx * 18, 10, 9, 4.5, "dkgray", rot=sx * -25)
    p.ellipse(0, 6, 14, 16, "gray")
    p.face(0, 8, .9, mouth=None)
    p.smile(0, -2, 3, 2)
    _acc(p, acc, 0, 36)


def elephant(p, acc=None):
    role = "gray"
    p.curve((18, -32), (26, -30), (30, -24))
    sit_body(p, role, belly=None)
    for sx in (-1, 1):
        p.smooth([(sx * 12, 22), (sx * 30, 30), (sx * 36, 14), (sx * 30, -2), (sx * 14, 0)], role)
        p.smooth([(sx * 15, 18), (sx * 27, 24), (sx * 31, 13), (sx * 27, 3), (sx * 16, 4)], "pink")
    p.circle(0, 12, 19, role)
    p.path([("M", -5, 6), ("C", -6, -6, -4, -16, 4, -20), ("C", 8, -22, 11, -18, 8, -15),
            ("C", 4, -12, 4, -4, 5, 6)], role)
    p.face(0, 15, 1.0, mouth=None, eye_gap=8)
    _acc(p, acc, 0, 31)


def frog(p, acc=None):
    role = "lime"
    for sx in (-1, 1):
        p.smooth([(sx * 8, -40), (sx * 30, -42), (sx * 30, -30), (sx * 14, -28)], role)
    p.ellipse(0, -22, 22, 20, role)
    p.ellipse(0, -24, 14, 13, "yellow")
    for sx in (-1, 1):
        p.circle(sx * 12, 20, 10, role)
        p.circle(sx * 12, 21, 6, "white")
        p.eye(sx * 12, 21, 3.2)
    p.ellipse(0, 6, 25, 15, role)
    p.arc(0, 8, 13, 210, 330, ry=8)
    with p.width(.6):
        p.ellipse(-16, 2, 3, 1.8, "blush")
        p.ellipse(16, 2, 3, 1.8, "blush")
    _acc(p, acc, 0, 28)


def owl(p, acc=None):
    role = "brown"
    p.rect(-30, -44, 60, 6, "dkbrown", r=3)
    p.smooth([(0, 34), (24, 28), (28, 0), (22, -32), (0, -40), (-22, -32), (-28, 0), (-24, 28)], role)
    for sx in (-1, 1):
        p.poly([(sx * 12, 30), (sx * 24, 42), (sx * 24, 24)], role)
        p.ellipse(sx * 25, -10, 7, 16, "dkbrown", rot=sx * 12)
    p.ellipse(0, -16, 15, 17, "tan")
    with p.width(.6):
        for yy in (-10, -18):
            for xx in (-6, 0, 6):
                p.arc(xx, yy, 3, 200, 340)
    for sx in (-1, 1):
        p.circle(sx * 10, 14, 10, "cream")
        p.circle(sx * 10, 14, 6, "white")
        p.eye(sx * 10, 14, 3.6)
    p.poly([(-3.5, 6), (3.5, 6), (0, 0)], "orange")
    for sx in (-1, 1):
        for d in (-3, 0, 3):
            p.ellipse(sx * 9 + d, -40, 1.8, 3.5, "orange")
    _acc(p, acc, 0, 32)


def chick(p, acc=None):
    role = "yellow"
    for sx in (-1, 1):
        p.lines([(sx * 8, -34), (sx * 8, -42), (sx * 4, -46)])
        p.lines([(sx * 8, -42), (sx * 12, -46)])
    p.circle(0, -2, 30, role)
    for sx in (-1, 1):
        p.ellipse(sx * 28, -6, 7, 12, role, rot=sx * -30)
    p.path([("M", -3, 28), ("Q", -2, 38, 2, 36), ("Q", 0, 32, 4, 34), ("Q", 4, 30, 2, 28)], role)
    p.face(0, 6, 1.1, mouth=None, eye_gap=8)
    p.poly([(-4, 2), (4, 2), (0, -4)], "orange")
    p.path([("M", -26, -16), ("L", -18, -10), ("L", -10, -18), ("L", -2, -10), ("L", 6, -18), ("L", 14, -10),
            ("L", 22, -18), ("L", 27, -14), ("Q", 20, -40, 0, -40), ("Q", -22, -40, -26, -16)], "cream")
    _acc(p, acc, 0, 30)


def duck(p, acc=None):
    role = "yellow"
    p.smooth([(-34, -6), (-26, -2), (-10, -12), (14, -10), (30, -14), (30, -30), (10, -42), (-18, -40),
              (-32, -28)], role)
    p.smooth([(-12, -20), (2, -16), (14, -22), (4, -30), (-10, -30)], role)
    p.circle(16, 6, 15, role)
    p.path([("M", 28, 6), ("Q", 44, 8, 44, 2), ("Q", 40, -3, 28, 0)], "orange")
    p.eye(19, 10, 2.8)
    with p.width(.6):
        p.ellipse(23, 1, 2.6, 1.6, "blush")
    p.curve((12, 20), (14, 27), (18, 24))
    with p.width(.8):
        p.curve((-44, -44), (-30, -38), (-16, -44), (-2, -38), (12, -44), (26, -38), (40, -44))
    _acc(p, acc, 16, 21, .8)


def penguin(p, acc=None):
    role = "navy"
    for sx in (-1, 1):
        p.ellipse(sx * 9, -42, 7, 3.5, "orange")
    p.smooth([(0, 34), (20, 26), (26, 0), (22, -30), (0, -40), (-22, -30), (-26, 0), (-20, 26)], role)
    for sx in (-1, 1):
        p.ellipse(sx * 26, -8, 6, 16, role, rot=sx * 20)
    p.smooth([(0, 18), (14, 12), (17, -10), (12, -32), (0, -36), (-12, -32), (-17, -10), (-14, 12)], "white")
    p.path([("M", 0, 24), ("C", -8, 30, -18, 22, -15, 12), ("Q", -8, 10, 0, 14),
            ("Q", 8, 10, 15, 12), ("C", 18, 22, 8, 30, 0, 24)], "white")
    p.face(0, 18, .9, mouth=None, eye_gap=6)
    p.poly([(-3.5, 13), (3.5, 13), (0, 8)], "orange")
    _acc(p, acc, 0, 33)


def fish(p, acc=None):
    p.poly([(18, 0), (40, 16), (36, 0), (40, -16)], "orange")
    p.smooth([(-34, 2), (-20, 20), (6, 22), (22, 6), (22, -6), (6, -22), (-20, -20)], "yellow")
    p.path([("M", -10, 18), ("Q", 0, 34, 12, 20)], "orange")
    p.path([("M", -4, -18), ("Q", 2, -30, 10, -18)], "orange")
    with p.width(.6):
        for xx, yy in ((0, 4), (8, -4), (0, -10), (8, 10), (-8, -4)):
            p.arc(xx, yy, 4, 100, 260)
    p.path([("M", -18, 18), ("Q", -12, 0, -18, -16)], closed=False)
    p.eye(-24, 6, 3)
    p.smile(-29, -3, 2.5, 1.5)


def turtle(p, acc=None):
    for x in (-18, 16):
        p.ellipse(x, -18, 7, 6, "lime")
    p.poly([(-30, -10), (-38, -6), (-30, -4)], "lime")
    p.circle(30, -4, 12, "lime")
    p.eye(33, -1, 2.6)
    p.smile(36, -8, 2.5, 1.5)
    with p.width(.6):
        p.ellipse(28, -8, 2.4, 1.5, "blush")
    p.halfdisc(-4, -12, 30, 30, "green")
    p.rect(-36, -16, 64, 6, "yellow", r=3)
    p.poly([(-12, 2), (4, 2), (10, 10), (4, 18), (-12, 18), (-18, 10)], "lime")
    for x0, y0 in ((-22, -2), (12, -2)):
        p.poly([(x0 - 5, y0), (x0 + 5, y0), (x0 + 7, y0 + 6), (x0, y0 + 10), (x0 - 7, y0 + 6)], "lime")
    _acc(p, acc, 30, 8, .7)


def snail(p, acc=None):
    p.path([("M", -40, -30), ("L", 30, -30), ("Q", 40, -30, 38, -16), ("L", 34, 4),
            ("Q", 26, 10, 22, 0), ("L", 20, -20), ("L", -40, -24)], "lime")
    p.line(26, 6, 22, 18)
    p.line(33, 6, 36, 18)
    p.circle(22, 19, 2.5, "lime")
    p.circle(36, 19, 2.5, "lime")
    p.eye(25, -4, 2.2)
    p.eye(32, -4, 2.2)
    p.smile(29, -12, 2.5, 1.5)
    p.circle(-10, -2, 24, "purple")
    pts = []
    for i in range(80):
        a = i * .18
        rr = 1.5 + i * .24
        pts.append((-10 + rr * math.cos(a), -2 + rr * math.sin(a)))
    p.lines(pts)
    _acc(p, acc, -10, 22, .8)


def butterfly(p, acc=None):
    for sx in (-1, 1):
        p.ellipse(sx * 20, 12, 18, 16, "purple", rot=sx * 20)
        p.ellipse(sx * 16, -14, 12, 12, "pink", rot=sx * -20)
        p.circle(sx * 22, 14, 6, "yellow")
        p.circle(sx * 16, -15, 4, "sky")
    p.ellipse(0, -4, 5, 24, "dkbrown")
    p.circle(0, 24, 7, "dkbrown")
    p.curve((-2, 30), (-6, 38), (-10, 40))
    p.curve((2, 30), (6, 38), (10, 40))
    p.circle(-10, 40, 2, "ink")
    p.circle(10, 40, 2, "ink")
    p.eye(-2.5, 25, 1.4)
    p.eye(2.5, 25, 1.4)


def bee(p, acc=None):
    for sx in (-1, 1):
        p.ellipse(sx * 10, 20, 9, 14, "white", rot=sx * -30)
    p.poly([(28, -4), (38, -6), (28, -10)], "ink")
    p.ellipse(0, -6, 30, 20, "yellow")
    for x in (-4, 8, 20):
        p.path([("M", x - 3, 13), ("Q", x + 3, -6, x - 3, -25), ("L", x + 3, -25),
                ("Q", x + 9, -6, x + 3, 13.5)], "ink" if False else "dkbrown")
    p.circle(-26, 2, 14, "yellow")
    p.curve((-28, 14), (-30, 24), (-34, 26))
    p.curve((-22, 15), (-20, 25), (-16, 27))
    p.circle(-34, 26, 2, "ink")
    p.circle(-16, 27, 2, "ink")
    p.face(-26, 2, .75, eye_gap=5)


def ladybug(p, acc=None):
    for i, y in enumerate((-18, -8, 2)):
        for sx in (-1, 1):
            p.line(sx * 20, y, sx * 32, y - 5)
    p.circle(0, 22, 13, "dkgray")
    p.face(0, 22, .8, eye_gap=5)
    p.curve((-5, 33), (-9, 40), (-14, 41))
    p.curve((5, 33), (9, 40), (14, 41))
    p.ellipse(0, -8, 26, 28, "red")
    p.line(0, 20, 0, -36)
    for x, y, r in ((-12, 6, 5), (12, 6, 5), (-14, -14, 4.5), (14, -14, 4.5), (-6, -26, 3.5), (6, -26, 3.5)):
        p.circle(x, y, r, "dkgray")


def whale(p, acc=None):
    p.path([("M", 28, -6), ("Q", 36, 2, 46, 10), ("Q", 44, 0, 48, -4), ("Q", 40, -6, 34, -14)], "blue")
    p.smooth([(-38, -2), (-30, 18), (-6, 24), (20, 16), (32, -6), (24, -22), (-10, -28), (-34, -20)], "blue")
    p.path([("M", -38, -6), ("Q", -6, -10, 30, -12), ("Q", 20, -26, -10, -28), ("Q", -34, -22, -38, -6)], "sky")
    p.eye(-20, 4, 3)
    p.smile(-26, -2, 4, 2.5)
    with p.width(.6):
        p.ellipse(-14, -4, 3, 1.8, "blush")
    p.curve((-6, 24), (-6, 34))
    p.curve((-6, 34), (-14, 42))
    p.curve((-6, 34), (2, 42))
    p.curve((-6, 34), (-6, 44))


def octopus(p, acc=None):
    for i in range(6):
        x = -25 + i * 10
        p.path([("M", x - 4, -6), ("Q", x - 8, -26, x + (6 if i % 2 else -6), -40),
                ("Q", x + 6, -38, x + 2, -30), ("Q", x + 2, -18, x + 6, -6)], "purple")
    p.path([("M", -30, -6), ("Q", -34, 40, 0, 40), ("Q", 34, 40, 30, -6), ("Q", 0, -14, -30, -6)], "purple")
    p.face(0, 12, 1.3, eye_gap=8)
    for x, y in ((-18, 26), (16, 28), (-6, 32)):
        p.circle(x, y, 2.5, "lilac")
    _acc(p, acc, 0, 40)


def giraffe(p, acc=None):
    role = "yellow"
    p.ellipse(-2, -24, 24, 14, role)
    for x in (-18, -8, 6, 16):
        p.rect(x - 3, -46, 6, 18, role, r=2)
        p.rect(x - 3, -47, 6, 4, "dkbrown", r=1.5)
    p.curve((-25, -20), (-32, -30), (-30, -36))
    p.path([("M", 6, -16), ("Q", 12, 4, 11, 26), ("L", 25, 26), ("Q", 22, 0, 22, -20)], role)
    for x, y in ((14, 0), (17, 12), (14, -8)):
        p.ellipse(x, y, 2.5, 3, "orange")
    for x, y in ((-12, -20), (2, -26), (-4, -18)):
        p.ellipse(x, y, 4, 3, "orange")
    for sx in (-1, 1):
        p.line(18 + sx * 4, 34, 18 + sx * 5, 42)
        p.circle(18 + sx * 5, 43, 2.5, "brown")
        p.ellipse(18 + sx * 12, 34, 5, 2.5, role, rot=sx * 20)
    p.ellipse(18, 30, 11, 10, role)
    p.ellipse(22, 25, 8, 5.5, "tan")
    p.eye(15, 33, 2.2)
    p.eye(22, 33, 2.2)
    p.dot(21, 26, .9)
    p.dot(25, 26, .9)
    with p.width(.6):
        p.ellipse(11, 28, 2.2, 1.4, "blush")
    _acc(p, acc, 18, 40, .6)


def hippo(p, acc=None):
    role = "lilac"
    sit_body(p, role, belly="pink", rx=22)
    for sx in (-1, 1):
        p.ellipse(sx * 14, 28, 5, 6, role)
    p.ellipse(0, 18, 18, 13, role)
    p.ellipse(0, 2, 22, 13, role)
    p.face(0, 20, .95, mouth=None, blush=False)
    p.ellipse(-6, 6, 2, 3, "ink")
    p.ellipse(6, 6, 2, 3, "ink")
    p.smile(0, -6, 8, 3)
    with p.width(.6):
        p.ellipse(-15, 0, 3, 2, "blush")
        p.ellipse(15, 0, 3, 2, "blush")
    _acc(p, acc, 0, 30)


def hedgehog(p, acc=None):
    pts = []
    for i in range(29):
        a = math.pi * i / 28
        rr = 34 if i % 2 else 26
        pts.append((-2 + rr * math.cos(a) * 1.05, -24 + rr * math.sin(a)))
    p.poly(pts, "brown")
    p.path([("M", 22, -24), ("Q", 24, 4, 8, 4), ("Q", 26, 6, 40, -14), ("Q", 40, -24, 22, -24)], "tan")
    p.ellipse(30, -26, 6, 3.5, "tan")
    p.ellipse(10, -26, 6, 3.5, "tan")
    p.circle(41, -14, 2.4, "ink")
    p.eye(26, -6, 2.4)
    p.smile(33, -18, 2.5, 1.5)
    with p.width(.6):
        p.ellipse(25, -14, 2.4, 1.5, "blush")


def crab(p, acc=None):
    for i, y in enumerate((-14, -20, -26)):
        for sx in (-1, 1):
            p.lines([(sx * 20, y + 6), (sx * 34, y), (sx * 38, y - 8)])
    for sx in (-1, 1):
        p.lines([(sx * 18, 2), (sx * 28, 16)])
        p.path([("M", sx * 22, 14), ("Q", sx * 22, 34, sx * 34, 32), ("L", sx * 30, 24), ("L", sx * 40, 22),
                ("Q", sx * 38, 10, sx * 22, 14)], "red")
    for sx in (-1, 1):
        p.line(sx * 6, 4, sx * 8, 16)
        p.circle(sx * 8, 18, 4.5, "white")
        p.eye(sx * 8, 18, 2.4)
    p.ellipse(0, -10, 24, 16, "red")
    p.smile(0, -10, 4, 2.5)
    with p.width(.6):
        p.ellipse(-10, -8, 3, 1.8, "blush")
        p.ellipse(10, -8, 3, 1.8, "blush")


def bird(p, acc=None):
    p.rect(-44, -36, 88, 6, "brown", r=3)
    p.ellipse(30, -26, 7, 3.5, "green", rot=30)
    p.poly([(-16, -10), (-36, -2), (-34, -12)], "blue")
    p.circle(0, -4, 22, "sky")
    p.ellipse(4, -10, 12, 9, "blue", rot=-20)
    p.ellipse(-4, -14, 10, 8, "cream")
    for x in (-6, 6):
        p.lines([(x, -26), (x, -32)])
        p.lines([(x - 3, -34), (x, -31), (x + 3, -34)])
    p.face(2, 2, .9, mouth=None, eye_gap=6)
    p.poly([(-1, -1), (5, -1), (2, -5)], "orange")
    p.curve((-2, 18), (0, 24), (4, 22))
    _acc(p, acc, 2, 18, .8)


def horse(p, acc=None, zebra=False, unicorn=False):
    role = "white" if (zebra or unicorn) else "tan"
    # tail
    p.smooth([(-22, 0), (-36, -4), (-40, -24), (-32, -20), (-28, -10)], "lilac" if unicorn else "brown")
    for x in (-18, -8, 8, 18):
        p.rect(x - 3.5, -46, 7, 26, role, r=2.5)
        p.rect(x - 3.5, -47, 7, 5, "dkgray", r=2)
    p.ellipse(0, -16, 26, 14, role)
    # mane
    mane = "pink" if unicorn else ("dkgray" if zebra else "brown")
    p.smooth([(16, 34), (6, 26), (5, 10), (2, -4), (12, -6), (16, 12)], mane)
    p.path([("M", 10, -12), ("Q", 14, 4, 13, 20), ("L", 30, 20), ("Q", 26, 0, 24, -16)], role)
    if zebra:
        for x, y in ((-12, -6), (-2, -4), (8, -6)):
            p.path([("M", x - 2, y), ("Q", x, y - 8, x - 2, y - 14), ("L", x + 2, y - 13), ("Q", x + 4, y - 7, x + 2, y)], "ink")
        for y in (0, 8):
            p.path([("M", 13, y), ("L", 22, y + 2), ("L", 13, y + 4)], "ink")
    for sx in (-1, 1):
        p.poly([(20 + sx * 6, 34), (20 + sx * 9, 44), (20 + sx * 1, 36)], role)
    if unicorn:
        p.poly([(18, 36), (22, 36), (22, 52)], "gold")
        with p.width(.6):
            p.line(18.8, 40, 22, 41)
            p.line(19.6, 45, 22, 46)
    p.ellipse(22, 29, 13, 11.5, role)
    p.ellipse(30, 21, 10, 7.5, "pink" if not zebra else "gray")
    p.dot(27, 22, 1)
    p.dot(33, 22, 1)
    p.eye(22, 32, 2.6)
    with p.width(.6):
        p.ellipse(17, 25, 2.3, 1.4, "blush")
    if acc and not unicorn:
        hat(p, 20, 38, .6, acc)


def zebra(p, acc=None):
    horse(p, acc, zebra=True)


ANIMALS = [
    ("CAT", cat), ("DOG", dog), ("BEAR", bear), ("BUNNY", bunny), ("PIG", pig), ("MOUSE", mouse),
    ("LION", lion), ("MONKEY", monkey), ("PANDA", panda), ("FOX", fox), ("COW", cow), ("SHEEP", sheep),
    ("ELEPHANT", elephant), ("FROG", frog), ("OWL", owl), ("CHICK", chick), ("DUCK", duck),
    ("PENGUIN", penguin), ("FISH", fish), ("TURTLE", turtle), ("SNAIL", snail), ("BUTTERFLY", butterfly),
    ("BEE", bee), ("LADYBUG", ladybug), ("WHALE", whale), ("OCTOPUS", octopus), ("GIRAFFE", giraffe),
    ("HIPPO", hippo), ("KOALA", koala), ("TIGER", tiger), ("HEDGEHOG", hedgehog), ("CRAB", crab),
    ("BIRD", bird), ("HORSE", horse), ("ZEBRA", zebra),
]
# animals that wear a hat nicely
HATTABLE = {"CAT", "DOG", "BEAR", "BUNNY", "PIG", "MOUSE", "LION", "MONKEY", "PANDA", "FOX", "COW", "SHEEP",
            "ELEPHANT", "FROG", "OWL", "CHICK", "PENGUIN", "HIPPO", "KOALA", "TIGER", "OCTOPUS", "BIRD"}
