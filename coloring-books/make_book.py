"""Daily book generator.  python3 make_book.py [--date YYYY-MM-DD] [--theme NAME] [--out DIR] [--preview]"""
import argparse, datetime as dt, json, os
from cb.book import build

ap = argparse.ArgumentParser()
ap.add_argument("--date"); ap.add_argument("--theme"); ap.add_argument("--out", default="output")
ap.add_argument("--preview", action="store_true")
a = ap.parse_args()
day = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
res = build(a.out, day, a.theme)
if a.preview:
    import pymupdf
    d = pymupdf.open(res["cover"]); d[0].get_pixmap(dpi=60).save(os.path.join(a.out, res["slug"] + "_cover.png"))
    d = pymupdf.open(res["interior"])
    for i in (0, 2, 3, 4, 6, 8):
        d[i].get_pixmap(dpi=50).save(os.path.join(a.out, f"{res['slug']}_p{i+1}.png"))
print(json.dumps({"slug": res["slug"], "interior": res["interior"], "cover": res["cover"],
                  "title": res["meta"]["title"], "pages": res["meta"]["interior_pages"]}, indent=1))
