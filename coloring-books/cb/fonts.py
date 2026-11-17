import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")


def register():
    for name, f in (("FredokaBold", "Fredoka-Bold.ttf"), ("FredokaMed", "Fredoka-Medium.ttf")):
        try:
            pdfmetrics.getFont(name)
        except KeyError:
            pdfmetrics.registerFont(TTFont(name, os.path.join(_D, f)))
