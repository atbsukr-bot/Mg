"""Everyday objects, shapes with faces, and holiday (winter) subjects."""
import math
from . import common as C
from . import animals as A
from . import vehicles as V
from . import fantasy as F


# ---------------- everyday objects ----------------
def apple(p, acc=None):
    with p.at(0, 0, 3):
        C.apple(p, 0, 0, 1, "red")
    p.face(0, -4, 1.3)


def ball(p, acc=None):
    C.ball(p, 0, 0, 36, "red")


def icecream(p, acc=None):
    p.poly([(-18, 0), (18, 0), (0, -46)], "tan")
    with p.width(.6):
        for k in (-10, 0, 10):
            p.line(-14 + (k + 10) * .6, -2, 4 + k * .9, -36)
            p.line(14 - (k + 10) * .6, -2, -4 - k * .9, -36)
    p.circle(0, 12, 18, "pink")
    p.circle(0, 34, 13, "cream")
    p.circle(2, 50, 5, "red")
    p.face(0, 10, 1.0)


def jellyfish(p, acc=None):
    for x in (-16, -6, 4, 14):
        p.curve((x, -4), (x - 4, -18), (x + 3, -30), (x - 2, -44))
    p.path([("M", -28, -4), ("Q", -30, 34, 0, 34), ("Q", 30, 34, 28, -4), ("Q", 14, -10, 0, -4),
            ("Q", -14, -10, -28, -4)], "pink")
    p.face(0, 12, 1.1)


def kite(p, acc=None):
    p.curve((0, -10), (-10, -24), (4, -34), (-6, -46))
    for y, x in ((-24, -8), (-36, 2)):
        p.poly([(x, y), (x - 6, y + 4), (x - 6, y - 4)], "red")
        p.poly([(x, y), (x + 6, y + 4), (x + 6, y - 4)], "red")
    p.poly([(0, 46), (-28, 14), (0, -10), (28, 14)], "yellow")
    p.poly([(0, 46), (-28, 14), (0, 14)], "red")
    p.poly([(0, -10), (28, 14), (0, 14)], "red")
    p.line(0, 46, 0, -10)
    p.line(-28, 14, 28, 14)
    p.face(0, 20, .9)


def nest(p, acc=None):
    for x, y in ((-14, 4), (0, 8), (14, 4)):
        C.egg(p, x, y, 1.2, "sky")
    p.path([("M", -40, 2), ("Q", -38, -30, 0, -30), ("Q", 38, -30, 40, 2), ("Q", 0, -6, -40, 2)], "brown")
    with p.width(.6):
        for y in (-6, -14, -22):
            p.curve((-32, y), (-12, y - 3), (10, y + 2), (32, y - 2))
    A.bird(p) if False else None


def umbrella(p, acc=None):
    p.path([("M", 0, 20), ("L", 0, -30), ("Q", 0, -40, -8, -40), ("Q", -14, -40, -14, -32)], closed=False)
    p.path([("M", -42, 6), ("Q", -40, 40, 0, 42), ("Q", 40, 40, 42, 6), ("Q", 35, 12, 28, 6), ("Q", 21, 12, 14, 6),
            ("Q", 7, 12, 0, 6), ("Q", -7, 12, -14, 6), ("Q", -21, 12, -28, 6), ("Q", -35, 12, -42, 6)], "purple")
    for x in (-28, 0, 28):
        p.curve((0, 42), (x * .6, 26), (x, 8))
    for x, y in ((-30, -20), (-20, -36), (24, -24), (34, -40), (14, -44)):
        p.path([("M", x, y + 4), ("Q", x - 3, y - 1, x, y - 2), ("Q", x + 3, y - 1, x, y + 4)], "sky")


def xylophone(p, acc=None):
    cols = ["red", "orange", "yellow", "green", "blue", "purple"]
    p.poly([(-40, 14), (40, 6), (40, -6), (-40, -22)], "none")
    for i, c in enumerate(cols):
        x = -36 + i * 13
        h = 46 - i * 5
        p.rect(x, -h / 2 - 4 + i * .6, 10, h, c, r=2)
        p.circle(x + 5, h / 2 - 8 + i * .6, 1.2, "gray")
        p.circle(x + 5, -h / 2 + 0 + i * .6, 1.2, "gray")
    for sx in (-1, 1):
        p.line(sx * 8, 30, sx * 22, 46)
        p.circle(sx * 7, 29, 4, "red")


def yoyo(p, acc=None):
    p.curve((0, 0), (6, 20), (-4, 34), (2, 48))
    p.ellipse(4, 49, 6, 3, "red")
    p.circle(0, -6, 30, "blue")
    p.circle(0, -6, 18, "sky")
    p.star(0, -6, 10, "yellow")


def house(p, acc=None):
    p.rect(18, 16, 9, 18, "red")
    p.rect(-32, -40, 64, 46, "yellow")
    p.poly([(-40, 4), (0, 38), (40, 4)], "red")
    p.rect(-8, -40, 16, 26, "brown", r=3)
    p.circle(4, -27, 1.4, "ink")
    for x in (-24, 12):
        p.rect(x, -18, 12, 12, "sky")
        p.line(x + 6, -18, x + 6, -6)
        p.line(x, -12, x + 12, -12)
    p.circle(0, 16, 6, "sky")


def tree(p, acc=None):
    p.rect(-7, -46, 14, 34, "brown", r=2)
    p.scallop(0, 14, 26, 9, 8, "green")
    for x, y in ((-10, 18), (12, 22), (0, 4), (14, 0), (-14, 0)):
        C.apple(p, x, y, .4, "red")


def flower_big(p, acc=None):
    p.line(0, -46, 0, 0)
    p.ellipse(10, -26, 10, 4.5, "green", rot=30)
    p.ellipse(-10, -34, 10, 4.5, "green", rot=-30)
    C.flower(p, 0, 16, 18, "pink", "yellow")
    p.face(0, 16, .8)


def balloons(p, acc=None):
    C.balloon(p, -16, 20, 16, "red", string_to=(0, -44))
    C.balloon(p, 18, 26, 15, "blue", string_to=(0, -44))
    C.balloon(p, 0, 4, 14, "yellow", string_to=(0, -44))
    p.rect(-4, -48, 8, 6, "pink", r=2)


def star_big(p, acc=None):
    p.star(0, 0, 44, "yellow", inner=.5)
    p.face(0, -2, 1.3)


def heart_big(p, acc=None):
    p.heart(0, 4, 40, "red")
    p.face(0, 2, 1.3)


def sun_big(p, acc=None):
    C.sun(p, 0, 0, 26)


def moon(p, acc=None):
    p.path([("M", 8, 40), ("C", -30, 40, -40, -20, 4, -38), ("C", -14, -20, -14, 24, 8, 40)], "yellow")
    p.eye(-14, 6, 2.4)
    p.smile(-16, -4, 3, 2)
    for x, y, r in ((20, 20, 6), (26, -12, 4), (12, -26, 3)):
        p.star(x, y, r, "yellow")


def gift(p, acc=None, role="red", band="yellow"):
    p.rect(-32, -40, 64, 50, role)
    p.rect(-36, 10, 72, 14, role)
    p.rect(-5, -40, 10, 64, band)
    p.ellipse(-12, 32, 13, 8, band, rot=20)
    p.ellipse(12, 32, 13, 8, band, rot=-20)
    p.circle(0, 28, 5, band)


OBJECTS = [("APPLE", apple), ("BALL", ball), ("ICE CREAM", icecream), ("JELLYFISH", jellyfish), ("KITE", kite),
           ("NEST", nest), ("UMBRELLA", umbrella), ("XYLOPHONE", xylophone), ("YO-YO", yoyo), ("HOUSE", house),
           ("TREE", tree), ("FLOWER", flower_big), ("BALLOONS", balloons), ("STAR", star_big),
           ("HEART", heart_big), ("SUN", sun_big), ("MOON", moon), ("GIFT", gift)]

ABC = [("A", "Apple", apple), ("B", "Bear", A.bear), ("C", "Cat", A.cat), ("D", "Dog", A.dog),
       ("E", "Elephant", A.elephant), ("F", "Fish", A.fish), ("G", "Giraffe", A.giraffe), ("H", "House", house),
       ("I", "Ice Cream", icecream), ("J", "Jellyfish", jellyfish), ("K", "Kite", kite), ("L", "Lion", A.lion),
       ("M", "Monkey", A.monkey), ("N", "Nest", nest), ("O", "Owl", A.owl), ("P", "Pig", A.pig),
       ("Q", "Queen", F.princess), ("R", "Rocket", V.rocket), ("S", "Sun", sun_big), ("T", "Turtle", A.turtle),
       ("U", "Umbrella", umbrella), ("V", "Van", V.van), ("W", "Whale", A.whale), ("X", "Xylophone", xylophone),
       ("Y", "Yo-yo", yoyo), ("Z", "Zebra", A.zebra)]


# ---------------- small counting items ----------------
def _sm(fn, s):
    def f(p):
        with p.at(0, 0, s):
            fn(p)
    return f


COUNT_ITEMS = [
    ("APPLES", lambda p: C.apple(p, 0, 0, 1.0, "red")),
    ("STARS", lambda p: p.star(0, 0, 13, "yellow")),
    ("HEARTS", lambda p: p.heart(0, 0, 12, "pink")),
    ("BALLS", lambda p: C.ball(p, 0, 0, 11, "blue")),
    ("FLOWERS", lambda p: C.flower(p, 0, 0, 8, "pink")),
    ("BALLOONS", lambda p: C.balloon(p, 0, 3, 10, "red", string_to=(0, -16))),
    ("FISH", _sm(A.fish, .32)), ("DUCKS", _sm(A.duck, .3)), ("LADYBUGS", _sm(A.ladybug, .3)),
    ("CARS", _sm(V.car, .3)), ("CUPCAKES", _sm(F.cupcake, .32)), ("BUTTERFLIES", _sm(A.butterfly, .3)),
    ("CHICKS", _sm(A.chick, .3)), ("SUNS", lambda p: C.sun(p, 0, 0, 7, face=True)),
    ("EGGS", lambda p: C.egg(p, 0, 0, 1.0, "cream")),
]


# ---------------- shapes with faces ----------------
def _shape(draw):
    def f(p, acc=None):
        draw(p)
        p.face(0, 0, 1.6, eye_gap=8)
    return f


def _poly_n(n, r=38, rot=90):
    return [(r * math.cos(math.radians(rot + i * 360 / n)), r * math.sin(math.radians(rot + i * 360 / n))) for i in range(n)]


SHAPES = [
    ("CIRCLE", _shape(lambda p: p.circle(0, 0, 38, "red"))),
    ("SQUARE", _shape(lambda p: p.rect(-34, -34, 68, 68, "blue", r=4))),
    ("TRIANGLE", _shape(lambda p: p.poly([(-42, -30), (42, -30), (0, 42)], "green"))),
    ("RECTANGLE", _shape(lambda p: p.rect(-44, -26, 88, 52, "orange", r=4))),
    ("STAR", _shape(lambda p: p.star(0, -2, 46, "yellow", inner=.5))),
    ("HEART", _shape(lambda p: p.heart(0, 4, 40, "pink"))),
    ("OVAL", _shape(lambda p: p.ellipse(0, 0, 44, 30, "purple"))),
    ("DIAMOND", _shape(lambda p: p.poly([(0, 46), (32, 0), (0, -46), (-32, 0)], "teal"))),
    ("PENTAGON", _shape(lambda p: p.poly(_poly_n(5, 42), "lime"))),
    ("HEXAGON", _shape(lambda p: p.poly(_poly_n(6, 40, 0), "gold"))),
]


# ---------------- winter holidays ----------------
def xtree(p, acc=None):
    p.rect(-7, -46, 14, 12, "brown")
    for (w, y0, h) in ((40, -36, 30), (32, -16, 28), (24, 4, 26)):
        p.path([("M", -w, y0), ("L", 0, y0 + h + 10), ("L", w, y0), ("Q", 0, y0 - 6, -w, y0)], "green")
    p.star(0, 44, 9, "yellow")
    for x, y, c in ((-18, -26, "red"), (14, -22, "blue"), (-8, -8, "yellow"), (10, 4, "red"), (-6, 16, "blue"),
                    (6, 26, "yellow"), (24, -32, "purple")):
        p.circle(x, y, 3.6, c)


def snowman(p, acc=None):
    p.circle(0, -26, 22, "white")
    p.circle(0, 6, 16, "white")
    for y in (-16, -26, -36):
        p.circle(0, y, 2.2, "ink")
    for sx in (-1, 1):
        p.lines([(sx * 14, 4), (sx * 32, 16)])
        p.lines([(sx * 26, 12), (sx * 30, 20)])
    p.circle(0, 30, 13, "white")
    p.face(0, 31, .8, mouth=None)
    p.poly([(0, 30), (12, 27), (0, 26)], "orange")
    p.smile(0, 23, 3, 2)
    p.path([("M", -14, 20), ("Q", 0, 14, 14, 20), ("L", 14, 14), ("Q", 0, 8, -14, 14)], "red")
    p.rect(6, 0, 7, 16, "red", r=2)
    p.rect(-14, 40, 28, 4, "dkgray", r=1)
    p.rect(-9, 44, 18, 10, "dkgray", r=1)


def stocking(p, acc=None):
    p.path([("M", -10, 30), ("L", -10, -10), ("Q", -10, -26, -24, -30), ("Q", -40, -36, -30, -46), ("Q", -16, -50, 6, -40),
            ("Q", 18, -32, 16, -10), ("L", 16, 30)], "red")
    p.rect(-14, 26, 34, 16, "white", r=4)
    p.heart(2, -6, 6, "white")
    p.star(-8, 50, 6, "yellow")
    p.rect(12, 34, 6, 18, "pink", r=1)


def candycane(p, acc=None):
    p.path([("M", -6, -46), ("L", -6, 18), ("Q", -6, 40, 14, 40), ("Q", 34, 40, 34, 18), ("L", 34, 12), ("L", 22, 12),
            ("L", 22, 18), ("Q", 22, 28, 14, 28), ("Q", 6, 28, 6, 18), ("L", 6, -46), ("Q", 0, -50, -6, -46)], "white")
    for y in (-38, -24, -10, 4):
        p.poly([(-6, y), (6, y + 6), (6, y + 12), (-6, y + 6)], "red")
    p.poly([(16, 40), (20, 28), (26, 30), (22, 40)], "red")
    p.ellipse(-14, 18, 8, 4, "green", rot=30)
    p.ellipse(-12, 26, 8, 4, "green", rot=-20)
    p.circle(-6, 20, 3, "red")


def bell(p, acc=None):
    for sx in (-1, 1):
        with p.at(sx * 16, 0, 1, rot=sx * -12):
            p.path([("M", -16, -18), ("Q", -16, 26, 0, 26), ("Q", 16, 26, 16, -18), ("L", 20, -24), ("L", -20, -24)], "gold")
            p.circle(0, -28, 4, "gold")
    p.poly([(-10, 30), (0, 38), (10, 30), (0, 34)], "red")
    p.ellipse(-8, 38, 9, 5, "red", rot=20)
    p.ellipse(8, 38, 9, 5, "red", rot=-20)
    p.circle(0, 36, 3.5, "red")


def gingerbread(p, acc=None):
    p.smooth([(0, 44), (14, 40), (16, 24), (10, 16), (34, 14), (36, 4), (14, 2), (16, -18), (28, -40), (18, -46),
              (0, -26), (-18, -46), (-28, -40), (-16, -18), (-14, 2), (-36, 4), (-34, 14), (-10, 16), (-16, 24),
              (-14, 40)], "tan", tension=.9)
    p.face(0, 28, .9)
    for y in (8, -2, -12):
        p.circle(0, y, 2.6, "red")
    with p.width(.7):
        for sx in (-1, 1):
            p.curve((sx * 24, 13), (sx * 26, 9), (sx * 24, 5))
            p.curve((sx * 18, -36), (sx * 22, -34), (sx * 24, -38))
    p.ellipse(0, 18, 7, 3, "green")


def santa(p, acc=None):
    p.path([("M", -14, -4), ("L", -26, -40), ("Q", 0, -46, 26, -40), ("L", 14, -4)], "red")
    p.rect(-28, -46, 56, 8, "white", r=4)
    p.rect(-24, -26, 48, 6, "dkgray")
    p.rect(-5, -27, 10, 8, "gold", r=1)
    p.line(0, -20, 0, -40)
    for sx in (-1, 1):
        p.ellipse(sx * 22, -16, 6, 10, "red", rot=sx * 30)
        p.circle(sx * 26, -26, 5, "white")
    p.scallop(0, 2, 18, 9, 4, "white")
    p.circle(0, 14, 14, "peach")
    p.face(0, 14, .8, mouth=None)
    p.circle(0, 10, 3, "pink")
    p.path([("M", -10, 6), ("Q", -4, 0, 0, 6), ("Q", 4, 0, 10, 6), ("Q", 6, 10, 0, 8), ("Q", -6, 10, -10, 6)], "white")
    C.hat(p, 0, 26, 1.0, "santa")


def reindeer(p, acc=None):
    for sx in (-1, 1):
        p.lines([(sx * 10, 26), (sx * 18, 44), (sx * 26, 48)])
        p.lines([(sx * 15, 38), (sx * 8, 46)])
        p.lines([(sx * 20, 45), (sx * 22, 50)])
    A.bear(p)
    p.circle(0, 6, 4.5, "red")


def ornament(p, acc=None):
    p.curve((0, 28), (-4, 40), (0, 48))
    p.rect(-8, 24, 16, 8, "gold", r=1)
    p.circle(0, -6, 32, "red")
    p.path([("M", -31, 0), ("Q", -16, 8, 0, 0), ("Q", 16, -8, 31, 0)], closed=False)
    p.path([("M", -30, -14), ("Q", -16, -6, 0, -14), ("Q", 16, -22, 30, -14)], closed=False)
    for x in (-16, 0, 16):
        p.star(x, -7, 4, "yellow")


def mittens(p, acc=None):
    for sx, c in ((-1, "red"), (1, "blue")):
        with p.at(sx * 18, 0, 1, rot=sx * -10):
            p.smooth([(-12, -18), (-14, 10), (-6, 24), (6, 24), (13, 10), (14, -18)], c)
            p.ellipse(-14, 2, 6, 9, c, rot=20)
            p.rect(-15, -30, 30, 12, "white", r=4)
            p.heart(0, 4, 5, "white")
    p.curve((-18, -30), (0, -44), (18, -30))


def snowflake_big(p, acc=None):
    with p.width(1.5):
        C.snowflake(p, 0, 0, 44)
    p.circle(0, 0, 9, "sky")


def wreath(p, acc=None):
    p.circle(0, 0, 40, "green")
    p.circle(0, 0, 22, "white")
    for i in range(12):
        a = math.radians(i * 30)
        p.ellipse(31 * math.cos(a), 31 * math.sin(a), 8, 5, "dkgreen", rot=i * 30 + 60)
    for a in (40, 160, 260):
        r = math.radians(a)
        p.circle(31 * math.cos(r), 31 * math.sin(r), 3.5, "red")
    p.poly([(0, -32), (-14, -24), (-14, -40)], "red")
    p.poly([(0, -32), (14, -24), (14, -40)], "red")
    p.circle(0, -32, 4, "red")


def cocoa(p, acc=None):
    p.path([("M", 22, 8), ("Q", 40, 8, 38, -8), ("Q", 36, -22, 20, -20)], closed=False)
    p.path([("M", 22, 2), ("Q", 32, 2, 31, -8), ("Q", 30, -15, 20, -14)], closed=False)
    p.path([("M", -26, 14), ("L", -22, -32), ("Q", 0, -38, 22, -32), ("L", 26, 14)], "red")
    p.ellipse(0, 14, 26, 6, "brown")
    for x in (-10, 4):
        p.rect(x - 5, 16, 10, 10, "white", r=2)
    for x in (-8, 6):
        p.curve((x, 30), (x - 3, 38), (x + 2, 46))
    p.face(0, -10, 1.0)


def elf(p, acc=None):
    p.path([("M", -10, -2), ("L", -22, -36), ("L", 22, -36), ("L", 10, -2)], "green")
    p.rect(-24, -40, 48, 6, "red", r=3)
    for sx in (-1, 1):
        p.rect(sx * 8 - 4, -48, 8, 10, "green")
        p.ellipse(sx * 10, -48, 6, 3, "red")
        p.ellipse(sx * 16, -12, 3.5, 9, "peach", rot=sx * 25)
    F._girl_head(p, 0, 14, "brown", 1, crown=False)
    p.path([("M", -15, 22), ("Q", 0, 50, 26, 42), ("Q", 6, 36, 15, 22)], "green")
    p.circle(27, 43, 3.5, "red")
    for sx in (-1, 1):
        p.poly([(sx * 14, 14), (sx * 22, 20), (sx * 14, 8)], "peach")


def snowhouse(p, acc=None):
    house(p)
    p.path([("M", -42, 4), ("Q", -30, 10, -20, 12), ("L", 0, 40), ("L", 20, 12), ("Q", 30, 10, 42, 4), ("L", 0, 42)],
           "white")
    for x, y in ((-40, 30), (36, 34), (30, -2), (-44, -12)):
        C.snowflake(p, x, y, 5)


def cookies(p, acc=None):
    p.rect(8, -40, 26, 50, "white", r=3)
    p.rect(8, -10, 26, 4, "sky")
    p.ellipse(-14, -36, 26, 7, "sky")
    for x, y in ((-24, -30), (-6, -30), (-15, -22)):
        p.circle(x, y, 9, "tan")
        for dx, dy in ((-3, 2), (3, -1), (0, -4)):
            p.circle(x + dx, y + dy, 1.3, "dkbrown")
    p.star(-30, 30, 6, "yellow")
    p.star(30, 30, 5, "yellow")


def sled(p, acc=None):
    p.path([("M", -44, -24), ("L", 34, -24), ("Q", 46, -24, 44, -12)], closed=False)
    for x in (-28, 18):
        p.line(x, -24, x, -10)
    p.rect(-36, -12, 70, 10, "red", r=3)
    with p.at(0, 20, .55):
        gift(p, role="blue", band="yellow")
    with p.at(-22, 10, .4):
        gift(p, role="green", band="red")


def polar_bear(p, acc=None):
    A.bear(p, acc="santa")


def penguin_hat(p, acc=None):
    A.penguin(p, acc="santa")


WINTER = [
    ("CHRISTMAS TREE", xtree), ("SNOWMAN", snowman), ("STOCKING", stocking), ("CANDY CANE", candycane),
    ("BELLS", bell), ("GINGERBREAD", gingerbread), ("SANTA", santa), ("REINDEER", reindeer),
    ("ORNAMENT", ornament), ("MITTENS", mittens), ("SNOWFLAKE", snowflake_big), ("WREATH", wreath),
    ("HOT COCOA", cocoa), ("ELF", elf), ("GIFT", gift), ("SNOWY HOUSE", snowhouse), ("COOKIES", cookies),
    ("SLED", sled), ("TEDDY BEAR", polar_bear), ("PENGUIN", penguin_hat), ("STAR", star_big),
]
