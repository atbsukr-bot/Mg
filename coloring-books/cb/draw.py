"""Drawing toolkit: bold, toddler-friendly line art on a reportlab canvas.

Every subject is drawn in a unit box of roughly -50..50 on both axes (y up).
Shapes are filled (white for the interior, colour for the cover) and stroked,
so painting back-to-front hides hidden lines automatically.
"""
import math
from contextlib import contextmanager

PALETTE = {
    "w": (1, 1, 1), "white": (1, 1, 1), "cream": (1, .97, .86),
    "red": (.93, .26, .26), "orange": (1, .6, .2), "yellow": (1, .85, .25),
    "gold": (.98, .74, .13), "lime": (.6, .85, .3), "green": (.3, .72, .4),
    "dkgreen": (.15, .5, .3), "teal": (.2, .75, .72), "sky": (.45, .78, .98),
    "blue": (.25, .5, .92), "navy": (.18, .25, .55), "purple": (.62, .42, .9),
    "lilac": (.8, .68, .98), "pink": (1, .6, .75), "rose": (.98, .4, .6),
    "peach": (1, .84, .7), "tan": (.9, .74, .52), "brown": (.62, .42, .26),
    "dkbrown": (.42, .27, .16), "gray": (.7, .72, .76), "dkgray": (.42, .44, .5),
    "ink": (0, 0, 0), "blush": (1, .7, .75),
}


class Pen:
    def __init__(self, c, color=False, lw=1.0):
        self.c = c
        self.color = color
        self.lw = lw
        c.setLineJoin(1)
        c.setLineCap(1)
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(lw)

    # ---------- state ----------
    def _fill(self, role):
        if role is None or role == "none":
            return 0
        if role == "ink":
            self.c.setFillColorRGB(0, 0, 0)
        elif role in ("white",):
            self.c.setFillColorRGB(1, 1, 1)
        elif self.color:
            self.c.setFillColorRGB(*PALETTE.get(role, PALETTE["w"]))
        else:
            self.c.setFillColorRGB(1, 1, 1)
        return 1

    @contextmanager
    def at(self, x=0, y=0, s=1.0, rot=0, flip=False):
        c = self.c
        c.saveState()
        c.translate(x, y)
        if rot:
            c.rotate(rot)
        sx = -s if flip else s
        c.scale(sx, s)
        old = self.lw
        c.setLineWidth(self.lw / s)
        self.lw = self.lw / s
        try:
            yield
        finally:
            self.lw = old
            c.restoreState()

    @contextmanager
    def width(self, k):
        old = self.lw
        self.lw = old * k
        self.c.setLineWidth(self.lw)
        try:
            yield
        finally:
            self.lw = old
            self.c.setLineWidth(old)

    # ---------- primitives ----------
    def circle(self, x, y, r, role="w"):
        f = self._fill(role)
        self.c.circle(x, y, r, stroke=1, fill=f)

    def ellipse(self, cx, cy, rx, ry, role="w", rot=0):
        f = self._fill(role)
        if rot:
            with self.at(cx, cy, rot=rot):
                self.c.ellipse(-rx, -ry, rx, ry, stroke=1, fill=f)
        else:
            self.c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, stroke=1, fill=f)

    def rect(self, x, y, w, h, role="w", r=0):
        f = self._fill(role)
        if r:
            self.c.roundRect(x, y, w, h, r, stroke=1, fill=f)
        else:
            self.c.rect(x, y, w, h, stroke=1, fill=f)

    def poly(self, pts, role="w", closed=True):
        p = self.c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        if closed:
            p.close()
            f = self._fill(role)
            self.c.drawPath(p, stroke=1, fill=f)
        else:
            self.c.drawPath(p, stroke=1, fill=0)

    def lines(self, pts):
        self.poly(pts, closed=False)

    def line(self, x1, y1, x2, y2):
        self.c.line(x1, y1, x2, y2)

    def path(self, cmds, role="w", closed=True):
        """cmds: ('M',x,y) ('L',x,y) ('Q',cx,cy,x,y) ('C',x1,y1,x2,y2,x,y)"""
        p = self.c.beginPath()
        cur = (0, 0)
        for cmd in cmds:
            k = cmd[0]
            if k == "M":
                p.moveTo(cmd[1], cmd[2]); cur = cmd[1:3]
            elif k == "L":
                p.lineTo(cmd[1], cmd[2]); cur = cmd[1:3]
            elif k == "Q":
                cx, cy, x, y = cmd[1:]
                x0, y0 = cur
                p.curveTo(x0 + 2 / 3 * (cx - x0), y0 + 2 / 3 * (cy - y0),
                          x + 2 / 3 * (cx - x), y + 2 / 3 * (cy - y), x, y)
                cur = (x, y)
            elif k == "C":
                p.curveTo(*cmd[1:]); cur = cmd[5:7]
        if closed:
            p.close()
            self.c.drawPath(p, stroke=1, fill=self._fill(role))
        else:
            self.c.drawPath(p, stroke=1, fill=0)

    def curve(self, *pts):
        """Open smooth stroke through points (no fill)."""
        self.smooth(list(pts), role=None, closed=False)

    def smooth(self, pts, role="w", closed=True, tension=1.0):
        """Catmull-Rom spline through points, as cubic beziers."""
        n = len(pts)
        p = self.c.beginPath()
        p.moveTo(*pts[0])
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
            t = tension / 6
            c1 = (p1[0] + (p2[0] - p0[0]) * t, p1[1] + (p2[1] - p0[1]) * t)
            c2 = (p2[0] - (p3[0] - p1[0]) * t, p2[1] - (p3[1] - p1[1]) * t)
            p.curveTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
        if closed:
            p.close()
            self.c.drawPath(p, stroke=1, fill=self._fill(role))
        else:
            self.c.drawPath(p, stroke=1, fill=0)

    def arc(self, cx, cy, r, a0, a1, ry=None):
        ry = r if ry is None else ry
        self.c.arc(cx - r, cy - ry, cx + r, cy + ry, a0, a1 - a0)

    def wedge(self, cx, cy, r, a0, a1, role="w"):
        p = self.c.beginPath()
        p.moveTo(cx, cy)
        p.arcTo(cx - r, cy - r, cx + r, cy + r, a0, a1 - a0)
        p.close()
        self.c.drawPath(p, stroke=1, fill=self._fill(role))

    def halfdisc(self, cx, cy, rx, ry, role="w", up=True):
        """Dome: flat side down (up=True)."""
        p = self.c.beginPath()
        p.moveTo(cx - rx, cy)
        p.arcTo(cx - rx, cy - ry, cx + rx, cy + ry, 180 if up else 0, -180 if up else -180)
        p.close()
        self.c.drawPath(p, stroke=1, fill=self._fill(role))

    # ---------- details ----------
    def dot(self, x, y, r):
        self.c.setFillColorRGB(0, 0, 0)
        self.c.circle(x, y, r, stroke=0, fill=1)

    def eye(self, x, y, r=2.6):
        self.dot(x, y, r)
        self.c.setFillColorRGB(1, 1, 1)
        self.c.circle(x + r * .35, y + r * .38, r * .36, stroke=0, fill=1)

    def smile(self, x, y, w=5, h=None):
        h = w * .7 if h is None else h
        self.arc(x, y + h, w, 200, 340, ry=h)

    def face(self, x=0, y=0, s=1.0, blush=True, mouth="smile", eye_gap=7):
        g = eye_gap * s
        self.eye(x - g, y + 2 * s, 2.6 * s)
        self.eye(x + g, y + 2 * s, 2.6 * s)
        if blush:
            with self.width(.6):
                self.ellipse(x - g - 3.5 * s, y - 3 * s, 2.6 * s, 1.6 * s, "blush")
                self.ellipse(x + g + 3.5 * s, y - 3 * s, 2.6 * s, 1.6 * s, "blush")
        if mouth == "smile":
            self.smile(x, y - 3 * s, 3.2 * s, 2.2 * s)
        elif mouth == "open":
            self.path([("M", x - 3.5 * s, y - 2 * s), ("Q", x, y - 2.5 * s, x + 3.5 * s, y - 2 * s),
                       ("Q", x, y - 9 * s, x - 3.5 * s, y - 2 * s)], "rose")

    def star(self, cx, cy, r, role="w", n=5, inner=.48, rot=90, round_=True):
        pts = []
        for i in range(n * 2):
            rr = r if i % 2 == 0 else r * inner
            a = math.radians(rot + i * 180 / n)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, role)

    def heart(self, cx, cy, s, role="w"):
        # s = half width
        self.path([("M", cx, cy - s * .95),
                   ("C", cx - s * 1.25, cy - s * .05, cx - s * .95, cy + s * .95, cx, cy + s * .45),
                   ("C", cx + s * .95, cy + s * .95, cx + s * 1.25, cy - s * .05, cx, cy - s * .95)], role)

    def cloud(self, cx, cy, w, role="w"):
        """Single clean outline: union of bumps over a flat base."""
        circles = [(-.42, .02, .26), (-.16, .2, .3), (.17, .22, .27), (.42, .04, .24)]
        circles = [(cx + a * w, cy + b * w, r * w) for a, b, r in circles]
        base = cy - .12 * w
        xmin = min(x - r for x, y, r in circles)
        xmax = max(x + r for x, y, r in circles)
        pts = []
        n = 90
        for i in range(n + 1):
            x = xmin + (xmax - xmin) * i / n
            ys = [y + math.sqrt(max(r * r - (x - X) ** 2, 0)) for X, y, r in circles if abs(x - X) <= r]
            yy = max(ys) if ys else base
            pts.append((x, max(yy, base)))
        pts.append((xmax - .05 * w, base))
        pts.append((xmin + .05 * w, base))
        self.poly(pts, role)

    def scallop(self, cx, cy, r, n, bump, role="w", phase=0):
        """Flower/mane outline: circle with n round bumps."""
        pts = []
        for i in range(n * 10):
            a = 2 * math.pi * i / (n * 10) + phase
            k = (i % 10) / 10
            rr = r + bump * math.sin(math.pi * k)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        self.poly(pts, role)

    def wheel(self, x, y, r, role="dkgray"):
        self.circle(x, y, r, role)
        self.circle(x, y, r * .5, "gray")
        self.dot(x, y, r * .12)

    def text_outline(self, txt, x, y, size, font="FredokaBold", role="w"):
        """Hollow bubble lettering, centred at x."""
        c = self.c
        from reportlab.pdfbase.pdfmetrics import stringWidth
        w = stringWidth(txt, font, size)
        t = c.beginText()
        t.setFont(font, size)
        t.setTextRenderMode(2)  # fill + stroke
        t.setTextOrigin(x - w / 2, y)
        c.saveState()
        self._fill(role)
        t.textOut(txt)
        c.drawText(t)
        c.restoreState()
        return w
