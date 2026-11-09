# halftone cut-out card: B&W dots + white sticker border + soft shadow (transparent PNG)
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps
src, dst, W = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert('L'); im = im.resize((W, int(im.height*W/im.width)), Image.LANCZOS)
im = ImageOps.autocontrast(im, cutoff=2)
cell = 7; w, h = im.size
out = Image.new('L', (w, h), 245); d = ImageDraw.Draw(out)
small = im.resize((w//cell+1, h//cell+1), Image.BOX)
for y in range(small.height):
    for x in range(small.width):
        v = 1 - small.getpixel((x, y))/255
        r = cell*0.62*v**0.8
        if r > 0.4:
            cx, cy = x*cell+cell/2, y*cell+cell/2
            d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=18)
out = Image.blend(out, im.point(lambda p: p*0.9+10), 0.25)
B = 22; S = 26
card = Image.new('RGBA', (w+2*B+2*S, h+2*B+2*S), (0,0,0,0))
sh = Image.new('L', card.size, 0); ImageDraw.Draw(sh).rectangle((S+8, S+12, S+2*B+w+8, S+2*B+h+12), fill=110)
sh = sh.filter(ImageFilter.GaussianBlur(14))
card.paste((0,0,0,255), (0,0), sh)
ImageDraw.Draw(card).rectangle((S, S, S+2*B+w, S+2*B+h), fill=(250,248,242,255))
card.paste(out.convert('RGBA'), (S+B, S+B))
card.save(dst)
