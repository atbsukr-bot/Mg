"""QA: build a book and save cover + contact sheet of all interior pages."""
import sys, os, datetime as dt
import pymupdf
from PIL import Image
from cb.book import build
out = sys.argv[1]; theme = sys.argv[2] if len(sys.argv) > 2 else None
day = dt.date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else dt.date.today()
res = build(out, day, theme)
d = pymupdf.open(res["cover"]); d[0].get_pixmap(dpi=55).save(os.path.join(out, "qa_cover.png"))
d = pymupdf.open(res["interior"])
idx = [0, 2, 3] + list(range(4, len(d), 2))
ims = [Image.open(__import__("io").BytesIO(d[i].get_pixmap(dpi=22).tobytes("png"))) for i in idx]
w, h = ims[0].size; cols = 9; rows = (len(ims) + cols - 1) // cols
S = Image.new("RGB", (cols * (w + 4), rows * (h + 4)), "gray")
for k, im in enumerate(ims): S.paste(im, ((k % cols) * (w + 4), (k // cols) * (h + 4)))
S.save(os.path.join(out, "qa_sheet.png")); print(res["meta"]["title"], res["meta"]["interior_pages"])
