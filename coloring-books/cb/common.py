"""Shared body parts, accessories and props."""
import math


def sit_body(p, role, belly=None, y=-26, rx=19, ry=17, feet=True, frole=None):
    p.ellipse(0, y, rx, ry, role)
    if belly:
        p.ellipse(0, y - 2, rx * .58, ry * .66, belly)
    if feet:
        fr = frole or role
        p.ellipse(-10, y - ry + 2, 7.5, 4.8, fr)
        p.ellipse(10, y - ry + 2, 7.5, 4.8, fr)
    # little arms
    p.ellipse(-rx + 3, y + 3, 4.5, 7, role, rot=-25)
    p.ellipse(rx - 3, y + 3, 4.5, 7, role, rot=25)


def hat(p, x, y, s, kind):
    """Accessory sitting on top of a head whose top is at (x, y)."""
    if kind == "party":
        p.poly([(x - 9 * s, y - 3 * s), (x + 9 * s, y - 3 * s), (x + 2 * s, y + 18 * s)], "purple")
        with p.width(.7):
            p.line(x - 5 * s, y + 3 * s, x + 6 * s, y + 5 * s)
            p.line(x - 2 * s, y + 9 * s, x + 4 * s, y + 11 * s)
        p.circle(x + 2 * s, y + 19 * s, 3 * s, "yellow")
    elif kind == "santa":
        p.path([("M", x - 12 * s, y - 2 * s), ("Q", x - 2 * s, y + 22 * s, x + 16 * s, y + 10 * s),
                ("L", x + 12 * s, y - 2 * s)], "red")
        p.circle(x + 17 * s, y + 9 * s, 4 * s, "white")
        p.rect(x - 14 * s, y - 6 * s, 28 * s, 7 * s, "white", r=3.5 * s)
    elif kind == "bow":
        p.poly([(x, y), (x - 10 * s, y + 6 * s), (x - 10 * s, y - 6 * s)], "pink")
        p.poly([(x, y), (x + 10 * s, y + 6 * s), (x + 10 * s, y - 6 * s)], "pink")
        p.circle(x, y, 3 * s, "rose")
    elif kind == "crown":
        p.poly([(x - 10 * s, y - 2 * s), (x - 10 * s, y + 8 * s), (x - 5 * s, y + 3 * s), (x, y + 10 * s),
                (x + 5 * s, y + 3 * s), (x + 10 * s, y + 8 * s), (x + 10 * s, y - 2 * s)], "gold")
        p.circle(x, y + 2.5 * s, 1.6 * s, "red")
    elif kind == "flower":
        flower(p, x + 8 * s, y - 2 * s, 5 * s)
    elif kind == "beanie":
        p.halfdisc(x, y - 4 * s, 13 * s, 11 * s, "blue")
        p.rect(x - 14 * s, y - 7 * s, 28 * s, 6 * s, "sky", r=3 * s)
        p.circle(x, y + 8 * s, 3.5 * s, "white")


def flower(p, x, y, r, role="pink", center="yellow"):
    for i in range(5):
        a = math.radians(90 + i * 72)
        p.circle(x + r * .9 * math.cos(a), y + r * .9 * math.sin(a), r * .62, role)
    p.circle(x, y, r * .5, center)


def tulip(p, x, y, h):
    p.line(x, y, x, y + h)
    p.ellipse(x + 4, y + h * .4, 4, 1.8, "green", rot=35)
    p.path([("M", x - 5, y + h + 1), ("L", x - 5, y + h + 8), ("L", x - 2, y + h + 5), ("L", x, y + h + 9),
            ("L", x + 2, y + h + 5), ("L", x + 5, y + h + 8), ("L", x + 5, y + h + 1),
            ("Q", x, y + h - 4, x - 5, y + h + 1)], "red")


def balloon(p, x, y, r=7, role="red", string_to=None):
    if string_to:
        p.curve((x, y - r * 1.25), (x + 2, y - r * 2.2), (string_to[0], string_to[1]))
    p.ellipse(x, y, r * .85, r, role)
    p.poly([(x - 1.5, y - r - 2), (x + 1.5, y - r - 2), (x, y - r + .5)], role)


def sun(p, x, y, r, face=True):
    for i in range(10):
        a = math.radians(i * 36)
        p.poly([(x + (r + 2) * math.cos(a - .18), y + (r + 2) * math.sin(a - .18)),
                (x + (r * 1.6) * math.cos(a), y + (r * 1.6) * math.sin(a)),
                (x + (r + 2) * math.cos(a + .18), y + (r + 2) * math.sin(a + .18))], "orange")
    p.circle(x, y, r, "yellow")
    if face:
        p.face(x, y, r / 14, blush=False)


def grass_tuft(p, x, y, s=1):
    p.lines([(x - 3 * s, y), (x - 2 * s, y + 4 * s), (x - 1 * s, y), (x + 1 * s, y + 5 * s), (x + 2 * s, y),
             (x + 3.5 * s, y + 3.5 * s), (x + 4 * s, y)])


def egg(p, x, y, s=1, role="cream", crack=False):
    p.smooth([(x, y + 13 * s), (x + 8 * s, y + 6 * s), (x + 9.5 * s, y - 4 * s), (x + 5 * s, y - 11 * s),
              (x, y - 12 * s), (x - 5 * s, y - 11 * s), (x - 9.5 * s, y - 4 * s), (x - 8 * s, y + 6 * s)], role)
    if crack:
        p.lines([(x - 9 * s, y), (x - 5 * s, y + 3 * s), (x - 2 * s, y - 1 * s), (x + 2 * s, y + 3 * s),
                 (x + 5 * s, y - 1 * s), (x + 9 * s, y + 2 * s)])


def palm(p, x, y, h):
    p.path([("M", x - 3, y), ("Q", x - 1, y + h * .5, x + 2, y + h), ("L", x + 6, y + h),
            ("Q", x + 3, y + h * .5, x + 3, y)], "brown")
    tx, ty = x + 4, y + h
    for ang, ln in ((160, 16), (120, 14), (60, 14), (20, 16), (200, 12), (-20, 12)):
        a = math.radians(ang)
        ex, ey = tx + ln * math.cos(a), ty + ln * math.sin(a) * .8
        mx, my = (tx + ex) / 2, (ty + ey) / 2 + 5
        p.path([("M", tx, ty), ("Q", mx, my + 3, ex, ey), ("Q", mx, my - 3, tx, ty)], "green")
    p.circle(tx - 2, ty - 3, 2.2, "brown")
    p.circle(tx + 2, ty - 3.5, 2.2, "brown")


def volcano(p, x, y, w):
    p.poly([(x - w, y), (x - w * .25, y + w * 1.1), (x + w * .25, y + w * 1.1), (x + w, y)], "brown")
    p.path([("M", x - w * .25, y + w * 1.1), ("Q", x - w * .1, y + w * .8, x, y + w * 1.0),
            ("Q", x + w * .1, y + w * .8, x + w * .25, y + w * 1.1)], "orange")
    p.cloud(x, y + w * 1.5, w * .8, "gray")


def apple(p, x, y, s=1, role="red"):
    p.smooth([(x, y + 9 * s), (x + 8 * s, y + 11 * s), (x + 12 * s, y + 3 * s), (x + 9 * s, y - 9 * s),
              (x + 3 * s, y - 12 * s), (x, y - 10 * s), (x - 3 * s, y - 12 * s), (x - 9 * s, y - 9 * s),
              (x - 12 * s, y + 3 * s), (x - 8 * s, y + 11 * s)], role)
    p.path([("M", x, y + 8 * s), ("Q", x + 1 * s, y + 13 * s, x + 2 * s, y + 16 * s)], closed=False)
    p.ellipse(x + 6 * s, y + 13.5 * s, 4.5 * s, 2.2 * s, "green", rot=25)


def ball(p, x, y, r, role="red"):
    p.circle(x, y, r, role)
    p.arc(x, y, r, 30, 150, ry=r * .45)
    p.arc(x, y - r * .1, r, 210, 330, ry=r * .45)
    p.path([("M", x, y + r), ("Q", x - r * .55, y, x, y - r)], closed=False)
    p.path([("M", x, y + r), ("Q", x + r * .55, y, x, y - r)], closed=False)


def bubble(p, x, y, r):
    p.circle(x, y, r, "white")
    with p.width(.6):
        p.arc(x, y, r * .6, 100, 160)


def snowflake(p, x, y, r):
    for i in range(6):
        a = math.radians(i * 60 + 90)
        ex, ey = x + r * math.cos(a), y + r * math.sin(a)
        p.line(x, y, ex, ey)
        for k in (.55,):
            bx, by = x + r * k * math.cos(a), y + r * k * math.sin(a)
            for d in (-40, 40):
                b = a + math.radians(d)
                p.line(bx, by, bx + r * .3 * math.cos(b), by + r * .3 * math.sin(b))
