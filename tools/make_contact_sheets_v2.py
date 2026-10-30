#!/usr/bin/env python3
"""Contact sheets v2 for expansion picks — code-labeled thumbs."""
import os, glob
from PIL import Image, ImageDraw, ImageFont

ORG = os.path.expanduser('~/workspace/user/media_library/portfolio-business-best/facebook-picks-organized')
OUT = os.path.expanduser('~/workspace/your_files/contact-sheets-v2')
os.makedirs(OUT, exist_ok=True)
FONT = ImageFont.load_default(size=28)
COLS, TW, TH, LAB = 5, 340, 300, 36

def files(folder, codes):
    res = []
    for c in codes:
        hits = sorted(glob.glob(os.path.join(ORG, folder, c + '_*.jpg')))
        assert hits, f'{folder}/{c} missing'
        res.append((c, hits[0]))
    return res

def sheet(name, items):
    rows = (len(items) + COLS - 1) // COLS
    W, H = COLS * TW, rows * (TH + LAB)
    canvas = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(canvas)
    for i, (code, path) in enumerate(items):
        im = Image.open(path).convert('RGB')
        im.thumbnail((TW, TH))
        x = (i % COLS) * TW + (TW - im.width) // 2
        y = (i // COLS) * (TH + LAB) + (TH - im.height) // 2
        canvas.paste(im, (x, y))
        d.text(((i % COLS) * TW + 10, (i // COLS) * (TH + LAB) + TH + 4), code, fill='black', font=FONT)
    p = os.path.join(OUT, name)
    canvas.save(p, quality=88)
    print(p, len(items))

nb = [f'N{i}' for i in range(12, 59)]
sheet('contact-v2-newborn-a.jpg', files('Newborn', nb[:24]))
sheet('contact-v2-newborn-b.jpg', files('Newborn', nb[24:]))
sheet('contact-v2-fashion.jpg', files('Fashion', [f'P{i}' for i in range(11, 35)]))
sheet('contact-v2-empowerment.jpg', files('Empowerment', [f'B{i}' for i in range(15, 25)]))
sheet('contact-v2-maternity.jpg', files('Maternity', [f'M{i}' for i in range(26, 35)]))
sheet('contact-v2-weddings.jpg', files('Weddings', [f'W{i}' for i in range(32, 48)]))
