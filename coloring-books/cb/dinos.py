"""Cute dinosaurs (side view, facing right)."""
from .common import egg


def _legs(p, xs, y0, role, h=14, w=9):
    for x in xs:
        p.rect(x - w / 2, y0 - h, w, h + 4, role, r=3)
        for d in (-2.5, 0, 2.5):
            p.circle(x + d, y0 - h + 1, 1.3, "white")


def _spots(p, pts, role="lime"):
    for x, y, r in pts:
        p.circle(x, y, r, role)


def trex(p, acc=None):
    role = "green"
    _legs(p, [-8], -18, "dkgreen", 18, 10)
    for x, y in ((-6, 16), (-12, 6), (-16, -4), (-22, -14)):
        p.poly([(x + 3, y + 3), (x - 7, y + 2), (x + 1, y - 5)], "orange")
    p.smooth([(-44, -30), (-26, -20), (-14, -6), (-8, 14), (6, 22), (16, 10), (14, -10), (6, -26),
              (-10, -32), (-30, -34)], role)
    _legs(p, [6], -18, role, 20, 11)
    p.smooth([(-10, 20), (2, 38), (24, 40), (36, 30), (34, 18), (14, 14), (0, 10)], role)
    p.path([("M", 18, 20), ("Q", 28, 18, 35, 22)], closed=False)
    for x in (22, 27, 32):
        p.poly([(x - 1.5, 20.5), (x + 1.5, 20.8), (x, 17.5)], "white")
    p.eye(18, 31, 3)
    p.dot(33, 31, .9)
    with p.width(.6):
        p.ellipse(14, 24, 2.8, 1.7, "blush")
    p.ellipse(12, 6, 5, 3, role, rot=-30)
    p.ellipse(4, -10, 9, 13, "lime")
    _spots(p, [(-18, -18, 3), (-8, -14, 2.5), (-28, -24, 2.2)])


def stego(p, acc=None):
    role = "teal"
    plates = [(-30, 2), (-18, 14), (-4, 18), (10, 14), (22, 4)]
    for x, y in plates:
        p.poly([(x - 7, y - 10), (x, y + 6), (x + 7, y - 10)], "orange")
    _legs(p, [-20, 12], -18, "teal", 14, 9)
    p.smooth([(-46, -24), (-30, -6), (-6, 6), (18, 2), (30, -8), (32, -22), (14, -28), (-20, -28)], role)
    p.poly([(-46, -24), (-52, -18), (-44, -20)], "white")
    p.poly([(-44, -26), (-50, -30), (-42, -27)], "white")
    _legs(p, [-12, 20], -18, role, 16, 9)
    p.smooth([(26, -10), (34, -2), (44, -4), (46, -12), (38, -18), (28, -18)], role)
    p.eye(36, -8, 2.5)
    p.smile(42, -14, 2.5, 1.4)
    with p.width(.6):
        p.ellipse(34, -14, 2.4, 1.5, "blush")
    _spots(p, [(-14, -10, 3), (0, -6, 2.5), (-26, -16, 2.5), (10, -14, 2)], "lime")


def trike(p, acc=None):
    role = "orange"
    _legs(p, [-22, 8], -16, "orange", 14, 10)
    p.smooth([(-44, -18), (-30, -2), (-4, 6), (16, 0), (20, -18), (0, -26), (-30, -26)], role)
    _legs(p, [-14, 14], -16, role, 16, 10)
    p.smooth([(12, 22), (6, 10), (8, -6), (20, -10), (26, 4), (22, 22)], "yellow")
    for x, y in ((10, 20), (16, 25), (22, 22), (7, 12)):
        p.circle(x, y, 2.4, "yellow")
    p.smooth([(18, 6), (24, 14), (40, 12), (46, 2), (42, -8), (26, -10)], role)
    p.poly([(26, 13), (30, 28), (32, 12)], "cream")
    p.poly([(36, 12), (42, 26), (40, 10)], "cream")
    p.poly([(44, 2), (50, 4), (45, -3)], "cream")
    p.eye(34, 4, 2.6)
    p.smile(40, -3, 2.5, 1.4)
    _spots(p, [(-18, -10, 3), (-4, -6, 2.5), (-30, -14, 2.2)], "yellow")


def brachio(p, acc=None):
    role = "blue"
    _legs(p, [-18, 10], -22, "blue", 16, 10)
    p.smooth([(-46, -26), (-30, -10), (-10, -2), (8, 0), (20, -10), (18, -26), (-4, -32), (-30, -32)], role)
    p.path([("M", 4, -4), ("Q", 6, 20, 22, 36), ("L", 30, 30), ("Q", 18, 14, 20, -12)], role)
    _legs(p, [-10, 18], -22, role, 18, 10)
    p.ellipse(28, 36, 11, 7, role)
    p.eye(30, 38, 2.4)
    p.smile(35, 33, 2.4, 1.3)
    with p.width(.6):
        p.ellipse(25, 33, 2.4, 1.5, "blush")
    _spots(p, [(-14, -12, 3), (0, -16, 2.5), (-28, -20, 2.2), (12, 10, 2), (16, 22, 1.8)], "sky")


def ptero(p, acc=None):
    role = "purple"
    p.path([("M", -4, 4), ("Q", -24, 30, -46, 24), ("Q", -34, 14, -36, 4), ("Q", -24, 8, -14, -4)], role)
    p.path([("M", 4, 4), ("Q", 24, 30, 46, 24), ("Q", 34, 14, 36, 4), ("Q", 24, 8, 14, -4)], role)
    p.ellipse(0, -8, 11, 18, "lilac")
    p.ellipse(0, -10, 6, 11, "pink")
    p.smooth([(0, 22), (10, 18), (24, 14), (10, 8), (-6, 8), (-10, 16), (-14, 26)], role)
    p.eye(2, 15, 2.5)
    for sx in (-1, 1):
        p.lines([(sx * 5, -26), (sx * 6, -32)])
        p.lines([(sx * 3, -34), (sx * 6, -31), (sx * 9, -34)])


def ankylo(p, acc=None):
    role = "brown"
    _legs(p, [-16, 12], -18, role, 12, 10)
    p.path([("M", -26, -16), ("Q", -40, -16, -42, -10)], closed=False)
    p.circle(-44, -8, 6, "tan")
    p.halfdisc(-2, -18, 30, 22, role)
    for x, y in ((-18, -8), (-6, -2), (6, -2), (18, -8), (-12, 8), (2, 10), (14, 6)):
        p.circle(x, y, 3.5, "tan")
    p.rect(-32, -20, 60, 5, "tan", r=2.5)
    p.smooth([(24, -4), (34, 2), (42, -4), (40, -16), (28, -18)], role)
    p.eye(33, -6, 2.4)
    p.smile(38, -12, 2.2, 1.3)


def baby_dino(p, acc=None):
    egg(p, 0, -24, 1.9, "cream")
    p.halfdisc(0, -18, 17, 14, "lime")
    p.ellipse(0, 4, 17, 15, "lime")
    for x in (-8, 0, 8):
        p.poly([(x - 3, 17), (x, 23), (x + 3, 17)], "orange")
    p.face(0, 4, .9)
    p.path([("M", -18, -20), ("L", -12, -14), ("L", -6, -20), ("L", 0, -14), ("L", 6, -20), ("L", 12, -14),
            ("L", 18, -20), ("Q", 18, -48, 0, -48), ("Q", -18, -48, -18, -20)], "cream")
    for sx in (-1, 1):
        p.ellipse(sx * 15, -10, 4, 6, "lime", rot=sx * 30)


def spino(p, acc=None):
    role = "red"
    p.path([("M", -26, -2), ("Q", -24, 30, -6, 30), ("Q", 6, 32, 14, 18), ("Q", 4, 4, -26, -2)], "orange")
    for x in (-18, -10, -2, 6):
        p.line(x, 4, x + 1, 24)
    _legs(p, [-6], -20, role, 18, 10)
    p.smooth([(-46, -26), (-26, -14), (-14, 0), (6, 6), (18, 0), (18, -14), (6, -28), (-16, -32), (-34, -32)], role)
    _legs(p, [8], -20, role, 20, 10)
    p.smooth([(12, 2), (22, 14), (40, 14), (48, 10), (44, 4), (24, 0)], role)
    p.eye(24, 10, 2.5)
    p.ellipse(4, -14, 8, 10, "pink")


DINOS = [
    ("T-REX", trex), ("STEGOSAURUS", stego), ("TRICERATOPS", trike), ("BRACHIOSAURUS", brachio),
    ("PTERODACTYL", ptero), ("ANKYLOSAURUS", ankylo), ("BABY DINO", baby_dino), ("SPINOSAURUS", spino),
]
