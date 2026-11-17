"""Vehicles, side view facing right, with a friendly face option on the front."""
import math
from .common import balloon


def _w(p, *xs, y=-22, r=9):
    for x in xs:
        p.wheel(x, y, r)


def _win(p, x, y, w, h, r=3):
    p.rect(x, y, w, h, "sky", r=r)


def _eyes(p, x, y, s=1):
    p.eye(x, y, 2.4 * s)


def car(p, acc=None, role="red", label=None):
    p.path([("M", -40, -22), ("L", -40, -4), ("Q", -40, 2, -34, 3), ("L", -22, 4), ("L", -12, 20),
            ("Q", -10, 22, -6, 22), ("L", 14, 22), ("Q", 18, 22, 20, 19), ("L", 28, 4), ("L", 38, 2),
            ("Q", 44, 0, 44, -6), ("L", 44, -22)], role)
    p.path([("M", -18, 5), ("L", -10, 18), ("L", 2, 18), ("L", 2, 5)], "sky")
    p.path([("M", 6, 5), ("L", 6, 18), ("L", 14, 18), ("L", 22, 5)], "sky")
    p.line(4, 4, 4, -18)
    p.rect(-4, -4, 6, 2.5, "gray", r=1.2)
    p.circle(40, -4, 3, "yellow")
    p.rect(-42, -14, 5, 4, "orange", r=1.5)
    if label:
        p.rect(-14, 22, 18, 7, "yellow", r=2)
    _w(p, -24, 26)


def taxi(p, acc=None):
    car(p, role="yellow", label=True)
    with p.width(.6):
        for x in (-36, -28, -20, 10, 18):
            p.rect(x, -12, 4, 4, "ink")


def police(p, acc=None):
    car(p, role="blue")
    p.rect(-8, 22, 12, 5, "white", r=2)
    p.rect(-8, 22, 6, 5, "red", r=2)
    p.star(-20, -8, 5, "gold")


def truck(p, acc=None, role="blue"):
    p.rect(-44, -20, 54, 34, "orange", r=3)
    for x in (-34, -20, -6):
        p.line(x, -16, x, 10)
    p.path([("M", 12, -20), ("L", 12, 26), ("Q", 12, 30, 16, 30), ("L", 30, 30), ("L", 44, 8),
            ("L", 44, -20)], role)
    p.path([("M", 18, 8), ("L", 18, 24), ("L", 28, 24), ("L", 38, 8)], "sky")
    p.circle(42, -6, 3, "yellow")
    _w(p, -30, -10, 30)


def bus(p, acc=None, role="yellow"):
    p.rect(-46, -20, 92, 46, role, r=8)
    for x in (-40, -24, -8, 8):
        _win(p, x, 6, 13, 13)
    p.path([("M", 26, 6), ("L", 26, 19), ("L", 40, 19), ("L", 44, 6)], "sky")
    p.rect(24, -14, 10, 18, "sky", r=2)
    p.line(29, -14, 29, 4)
    p.rect(-46, -4, 70, 4, "orange")
    p.circle(42, -10, 3, "white")
    _w(p, -28, 28, y=-22)


def firetruck(p, acc=None):
    p.rect(-46, -20, 62, 30, "red", r=3)
    p.lines([(-40, 18), (8, 26)])
    p.lines([(-40, 12), (8, 20)])
    for k in range(6):
        x0 = -36 + k * 8
        p.line(x0, 12 + k * 1.33, x0, 18 + k * 1.33)
    p.rect(-6, 10, 10, 6, "gray", r=2)
    p.path([("M", 16, -20), ("L", 16, 26), ("Q", 16, 30, 20, 30), ("L", 32, 30), ("L", 46, 6),
            ("L", 46, -20)], "red")
    p.path([("M", 22, 6), ("L", 22, 24), ("L", 30, 24), ("L", 40, 6)], "sky")
    p.rect(22, 30, 8, 5, "blue", r=2)
    for x in (-40, -26, -12):
        p.rect(x, -14, 10, 14, "orange", r=2)
    _w(p, -32, -10, 32)


def ambulance(p, acc=None):
    truck(p, role="white")
    p.rect(-26, -10, 16, 6, "red", r=1)
    p.rect(-21, -15, 6, 16, "red", r=1)
    p.rect(18, 30, 8, 5, "red", r=2)


def tractor(p, acc=None):
    p.rect(-6, -14, 46, 24, "green", r=4)
    for y in (-6, 2):
        p.line(18, y, 38, y)
    p.rect(30, 10, 5, 16, "gray", r=2)
    p.ellipse(32.5, 28, 5, 3, "gray")
    p.rect(-36, -10, 32, 44, "green", r=4)
    _win(p, -30, 10, 20, 18)
    p.rect(-40, 32, 40, 6, "yellow", r=3)
    p.wheel(-22, -18, 20, "dkgray")
    p.wheel(30, -26, 12, "dkgray")


def dumptruck(p, acc=None):
    p.path([("M", -46, -6), ("L", -42, 24), ("L", 6, 24), ("L", 10, -6)], "yellow")
    for x in (-34, -20, -6):
        p.line(x, -2, x + 1, 20)
    p.rect(-46, -20, 92, 14, "dkgray", r=3)
    p.path([("M", 14, -6), ("L", 14, 26), ("Q", 14, 30, 18, 30), ("L", 30, 30), ("L", 44, 10),
            ("L", 44, -6)], "orange")
    p.path([("M", 20, 10), ("L", 20, 24), ("L", 28, 24), ("L", 38, 10)], "sky")
    _w(p, -30, -10, 30, y=-22)


def digger(p, acc=None):
    p.rect(-44, -36, 60, 14, "dkgray", r=7)
    for x in (-36, -24, -12, 0, 10):
        p.circle(x, -29, 4, "gray")
    p.rect(-40, -22, 50, 18, "yellow", r=3)
    p.rect(-30, -4, 26, 30, "yellow", r=3)
    _win(p, -26, 6, 18, 16)
    p.poly([(4, 4), (10, 10), (32, 30), (36, 26), (14, 2)], "orange")
    p.poly([(32, 30), (36, 26), (44, 0), (40, -2)], "orange")
    p.path([("M", 36, 2), ("L", 48, 2), ("L", 46, -14), ("Q", 36, -14, 32, -6)], "gray")


def train(p, acc=None):
    p.rect(-14, -20, 54, 30, "red", r=4)
    p.rect(-44, -20, 34, 48, "blue", r=4)
    _win(p, -38, 6, 22, 16)
    p.rect(-48, 26, 42, 6, "red", r=3)
    p.rect(14, 10, 12, 16, "dkgray", r=2)
    p.poly([(10, 26), (30, 26), (26, 32), (14, 32)], "dkgray")
    p.cloud(26, 42, 16, "white")
    p.poly([(40, -20), (48, -20), (40, -8)], "gray")
    p.circle(42, 4, 3.5, "yellow")
    for x, r in ((-34, 9), (-12, 9), (12, 9), (30, 7)):
        p.wheel(x, -22, r)
    p.line(-34, -22, 12, -22)


def airplane(p, acc=None):
    p.path([("M", -4, 4), ("L", -22, 34), ("L", -12, 34), ("L", 14, 4)], "blue")
    p.path([("M", -40, 2), ("L", -46, 24), ("L", -38, 24), ("L", -28, 4)], "red")
    p.smooth([(-44, 6), (-30, 12), (20, 12), (40, 8), (46, 0), (40, -6), (20, -8), (-30, -6), (-44, -2)], "white")
    for x in (-24, -14, -4, 6, 16):
        p.circle(x, 4, 3, "sky")
    p.path([("M", 36, 6), ("Q", 42, 6, 44, 2), ("L", 36, 2)], "sky")
    p.path([("M", -4, -2), ("L", -24, -30), ("L", -14, -30), ("L", 14, -2)], "blue")
    p.cloud(-24, -40, 14, "white")
    p.cloud(30, 30, 12, "white")


def helicopter(p, acc=None):
    p.rect(-2, 24, 4, 8, "gray")
    p.rect(-38, 31, 76, 4, "gray", r=2)
    p.path([("M", -16, 0), ("L", -46, 6), ("L", -46, 0), ("L", -18, -8)], "orange")
    p.circle(-46, 3, 6, "white")
    p.line(-46, -3, -46, 9)
    p.ellipse(4, -2, 24, 20, "orange")
    p.path([("M", 4, 16), ("Q", 26, 14, 28, -2), ("L", 8, -2), ("Q", 6, 8, 4, 16)], "sky")
    for x in (-10, 18):
        p.line(x, -20, x, -30)
    p.rect(-20, -32, 46, 4, "gray", r=2)


def sailboat(p, acc=None):
    p.line(0, -14, 0, 40)
    p.poly([(3, 38), (3, -8), (32, -8)], "white")
    p.poly([(-3, 34), (-3, -6), (-26, -6)], "yellow")
    p.poly([(0, 40), (12, 36), (0, 32)], "red")
    p.path([("M", -40, -12), ("L", 40, -12), ("L", 30, -30), ("L", -30, -30)], "red")
    for x in (-16, 0, 16):
        p.circle(x, -21, 3.5, "white")
    p.path([("M", -48, -34), ("Q", -36, -26, -24, -34), ("Q", -12, -26, 0, -34), ("Q", 12, -26, 24, -34),
            ("Q", 36, -26, 48, -34), ("L", 48, -44), ("L", -48, -44)], "sky")


def ship(p, acc=None):
    p.rect(-10, 4, 14, 22, "red", r=2)
    p.rect(10, 4, 14, 18, "red", r=2)
    p.rect(-10, 22, 14, 4, "white")
    p.rect(10, 18, 14, 4, "white")
    p.rect(-30, -8, 58, 14, "white", r=2)
    for x in (-24, -14, -4, 6, 16):
        p.circle(x, -1, 2.6, "sky")
    p.path([("M", -44, -8), ("L", 44, -8), ("L", 34, -28), ("L", -36, -28)], "navy")
    p.path([("M", -48, -30), ("Q", -36, -22, -24, -30), ("Q", -12, -22, 0, -30), ("Q", 12, -22, 24, -30),
            ("Q", 36, -22, 48, -30), ("L", 48, -44), ("L", -48, -44)], "sky")


def rocket(p, acc=None):
    for sx in (-1, 1):
        p.poly([(sx * 12, -14), (sx * 24, -30), (sx * 24, -8), (sx * 12, 8)], "red")
    p.path([("M", -8, -26), ("Q", 0, -46, 8, -26)], "orange")
    p.path([("M", -4, -26), ("Q", 0, -38, 4, -26)], "yellow")
    p.path([("M", -14, -26), ("L", -14, 20), ("Q", -12, 40, 0, 50), ("Q", 12, 40, 14, 20), ("L", 14, -26)], "white")
    p.path([("M", -12, 28), ("Q", -8, 42, 0, 50), ("Q", 8, 42, 12, 28)], "red")
    p.circle(0, 10, 7, "sky")
    p.circle(0, 10, 4.5, "sky")
    p.rect(-14, -20, 28, 6, "blue")
    p.poly([(-2, -26), (2, -26), (2, -12), (-2, -12)], "red")
    for x, y in ((-34, 30), (32, 14), (-30, -10)):
        p.star(x, y, 5, "yellow")


def submarine(p, acc=None):
    p.rect(-6, 14, 18, 14, "yellow", r=3)
    p.line(6, 28, 6, 36)
    p.line(6, 36, 12, 36)
    p.smooth([(-40, 0), (-30, 14), (20, 16), (38, 6), (40, -4), (24, -16), (-30, -16)], "yellow")
    p.poly([(-38, 0), (-48, 10), (-48, -10)], "orange")
    for x in (-18, -2, 14):
        p.circle(x, 0, 6, "sky")
    for x, y, r in ((40, 20, 3), (44, 28, 2.2), (38, 34, 1.6)):
        p.circle(x, y, r, "white")


def bicycle(p, acc=None):
    for x in (-26, 26):
        p.circle(x, -16, 17, "none")
        p.circle(x, -16, 13, "none")
        p.circle(x, -16, 2.5, "gray")
    p.poly([(-26, -16), (-4, -16), (18, 10), (-12, 10)], "none")
    p.line(-4, -16, -12, 10)
    p.line(18, 10, 26, -16)
    p.line(18, 10, 16, 20)
    p.lines([(10, 22), (16, 20), (24, 22)])
    p.line(-12, 10, -14, 16)
    p.ellipse(-14, 18, 8, 3, "red")
    p.circle(-4, -16, 5, "gray")
    p.rect(-26, -4, 22, 4, "red", r=2)


def scooter(p, acc=None):
    p.rect(-36, -18, 60, 7, "purple", r=3.5)
    p.line(24, -14, 30, 30)
    p.lines([(22, 30), (30, 30), (38, 30)])
    p.ellipse(22, 30, 4, 2, "pink")
    p.ellipse(38, 30, 4, 2, "pink")
    p.wheel(-30, -24, 8)
    p.wheel(28, -24, 8)


def motorcycle(p, acc=None):
    p.path([("M", -30, -10), ("Q", -20, 8, 0, 8), ("L", 20, 8), ("Q", 30, 0, 32, -10)], "red")
    p.ellipse(-12, 12, 14, 4, "dkgray")
    p.line(22, 6, 30, 22)
    p.lines([(26, 24), (30, 22), (34, 24)])
    p.ellipse(34, 6, 3.5, 4.5, "yellow")
    p.rect(-14, -14, 22, 12, "gray", r=3)
    p.line(-24, -8, -40, -10)
    _w(p, -28, 28, y=-20, r=12)


def balloon_air(p, acc=None):
    p.lines([(-12, -8), (-8, -26)])
    p.lines([(12, -8), (8, -26)])
    p.path([("M", 0, -6), ("Q", -40, 10, -30, 32), ("Q", -20, 50, 0, 50), ("Q", 20, 50, 30, 32),
            ("Q", 40, 10, 0, -6)], "red")
    p.path([("M", 0, -6), ("Q", -18, 14, -12, 32), ("Q", -8, 48, 0, 50), ("Q", 8, 48, 12, 32),
            ("Q", 18, 14, 0, -6)], "yellow")
    p.path([("M", 0, -6), ("Q", -4, 20, 0, 50), ("Q", 4, 20, 0, -6)], "red")
    p.rect(-11, -40, 22, 14, "brown", r=2)
    with p.width(.6):
        for x in (-5, 1, 7):
            p.line(x, -40, x, -26)
    p.cloud(-34, -24, 14, "white")
    p.cloud(36, -4, 12, "white")


def icecream_truck(p, acc=None):
    truck(p, role="pink")
    p.rect(-38, -4, 40, 14, "sky", r=2)
    p.poly([(-20, 14), (-14, 14), (-17, 28)], "tan")
    p.circle(-17, 30, 5, "pink")
    p.circle(-17, 36, 4, "white")


def racecar(p, acc=None):
    p.rect(-44, -6, 10, 18, "red", r=2)
    p.path([("M", -40, -18), ("L", -40, 4), ("L", -16, 6), ("Q", -6, 18, 8, 6), ("L", 44, 0), ("L", 44, -18)], "red")
    p.path([("M", -12, 6), ("Q", -4, 14, 4, 6)], "sky")
    p.circle(12, -6, 7, "white")
    p.text_outline("1", 12, -9.5, 10, role="white")
    with p.width(.6):
        for x in (-36, -30):
            p.line(x, -14, x + 6, 0)
    _w(p, -26, 30, y=-20, r=10)


def van(p, acc=None):
    p.path([("M", -44, -20), ("L", -44, 22), ("Q", -44, 28, -38, 28), ("L", 22, 28), ("L", 40, 4),
            ("L", 44, 0), ("L", 44, -20)], "teal")
    for x in (-38, -22, -6):
        _win(p, x, 8, 13, 14)
    p.path([("M", 12, 8), ("L", 12, 22), ("L", 22, 22), ("L", 34, 8)], "sky")
    p.line(8, 26, 8, -16)
    p.circle(41, -6, 3, "yellow")
    _w(p, -26, 26)


def garbage(p, acc=None):
    p.rect(-46, -18, 58, 38, "green", r=6)
    for x in (-36, -24, -12, 0):
        p.line(x, -12, x, 14)
    p.path([("M", 14, -18), ("L", 14, 26), ("Q", 14, 30, 18, 30), ("L", 30, 30), ("L", 44, 8),
            ("L", 44, -18)], "green")
    p.path([("M", 20, 8), ("L", 20, 24), ("L", 28, 24), ("L", 38, 8)], "sky")
    _w(p, -30, -10, 30)


VEHICLES = [
    ("CAR", car), ("TAXI", taxi), ("POLICE CAR", police), ("TRUCK", truck), ("BUS", bus),
    ("FIRE TRUCK", firetruck), ("AMBULANCE", ambulance), ("TRACTOR", tractor), ("DUMP TRUCK", dumptruck),
    ("DIGGER", digger), ("TRAIN", train), ("AIRPLANE", airplane), ("HELICOPTER", helicopter),
    ("SAILBOAT", sailboat), ("SHIP", ship), ("ROCKET", rocket), ("SUBMARINE", submarine),
    ("BICYCLE", bicycle), ("SCOOTER", scooter), ("MOTORCYCLE", motorcycle), ("HOT AIR BALLOON", balloon_air),
    ("ICE CREAM TRUCK", icecream_truck), ("RACE CAR", racecar), ("VAN", van), ("GARBAGE TRUCK", garbage),
]


def mixer(p, acc=None):
    p.rect(-46, -20, 60, 8, "dkgray", r=2)
    p.lines([(-4, -12), (-8, 0)])
    with p.at(-18, 8, 1, rot=12):
        p.ellipse(0, 0, 26, 17, "orange")
        with p.width(.7):
            for x in (-14, -4, 6, 16):
                p.curve((x - 3, 15), (x + 3, 0), (x - 3, -15))
    p.path([("M", 14, -20), ("L", 14, 26), ("Q", 14, 30, 18, 30), ("L", 30, 30), ("L", 44, 8),
            ("L", 44, -20)], "yellow")
    p.path([("M", 20, 8), ("L", 20, 24), ("L", 28, 24), ("L", 38, 8)], "sky")
    _w(p, -32, -10, 30)


def towtruck(p, acc=None):
    p.rect(-40, -20, 52, 16, "gray", r=2)
    p.lines([(-20, -4), (-36, 26), (-46, 8)])
    p.path([("M", -46, 8), ("Q", -50, 0, -44, -2)], closed=False)
    p.path([("M", 12, -20), ("L", 12, 26), ("Q", 12, 30, 16, 30), ("L", 30, 30), ("L", 44, 8),
            ("L", 44, -20)], "red")
    p.path([("M", 18, 8), ("L", 18, 24), ("L", 28, 24), ("L", 38, 8)], "sky")
    p.rect(16, 30, 10, 5, "orange", r=2)
    _w(p, -26, 30)


def wagon(p, acc=None):
    p.rect(-36, -14, 64, 24, "red", r=3)
    with p.width(.7):
        p.line(-36, 2, 28, 2)
    p.lines([(28, -6), (44, 22)])
    p.rect(40, 20, 10, 5, "dkgray", r=2.5)
    with p.at(-14, 22, .35):
        C_ball(p)
    _w(p, -24, 16, y=-22, r=8)


def C_ball(p):
    from .common import ball
    ball(p, 0, 0, 30, "blue")


def skateboard(p, acc=None):
    p.path([("M", -44, 0), ("Q", -46, 8, -38, 8), ("L", 38, 8), ("Q", 46, 8, 44, 0), ("Q", 40, -6, 30, -4),
            ("L", -30, -4), ("Q", -40, -6, -44, 0)], "lime")
    for x in (-22, 22):
        p.poly([(x - 6, -4), (x + 6, -4), (x, -12)], "gray")
        p.wheel(x - 6, -16, 6, "orange")
        p.wheel(x + 6, -16, 6, "orange")
    p.star(0, 2, 4, "yellow")


def jeep(p, acc=None):
    p.rect(-46, -2, 8, 22, "dkgray", r=3)
    p.path([("M", -40, -20), ("L", -40, 6), ("L", -24, 6), ("L", -24, 26), ("L", 12, 26), ("L", 18, 6),
            ("L", 42, 4), ("L", 44, -20)], "green")
    _win(p, -20, 8, 14, 14)
    p.path([("M", -2, 8), ("L", -2, 22), ("L", 10, 22), ("L", 14, 8)], "sky")
    p.circle(40, -6, 3, "yellow")
    _w(p, -24, 26, r=11)


VEHICLES += [("CEMENT MIXER", mixer), ("TOW TRUCK", towtruck), ("WAGON", wagon), ("SKATEBOARD", skateboard),
             ("JEEP", jeep)]
