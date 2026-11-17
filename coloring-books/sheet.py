"""Contact sheet of subjects for visual QA: python3 sheet.py module [color] out.png"""
import sys, importlib
from reportlab.pdfgen import canvas
from cb.draw import Pen
from cb import fonts
import fitz
fonts.register()
mod, color, out = sys.argv[1], sys.argv[2] == "color", sys.argv[3]
attr = sys.argv[4] if len(sys.argv) > 4 else None
m = importlib.import_module("cb." + mod)
items = getattr(m, attr) if attr else [v for k, v in vars(m).items() if k.isupper() and isinstance(v, list)][0]
cols = 6; cell = 160; rows = (len(items) + cols - 1) // cols
pdf = out.replace(".png", ".pdf")
c = canvas.Canvas(pdf, pagesize=(cols * cell, rows * cell))
for i, (name, fn) in enumerate(items):
    x = (i % cols) * cell + cell / 2; y = (rows - 1 - i // cols) * cell + cell / 2 + 8
    p = Pen(c, color=color, lw=1)
    with p.at(x, y, s=1.25):
        fn(p, None)
    c.setFont("FredokaBold", 11); c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(x, y - 75, name)
c.save()
d = fitz.open(pdf); d[0].get_pixmap(dpi=110).save(out)
