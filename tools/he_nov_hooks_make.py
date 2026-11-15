"""RETAL — Hebrew sector ads, Nov 2026: Hook 1 (unboxing/camera) + Hook 2 (Hanukkah).
Run from repo root: python3 tools/he_nov_hooks_make.py  -> ads/he_nov_hooks/*.jpg
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, random
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'ads', 'he_nov_hooks'); os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
PLUM=(78,30,92); PLUM_D=(46,14,58); GOLD=(196,160,96); GOLD_D=(160,120,60); IVORY=(247,241,219); MUTED=(110,82,110)
L = ImageFont.Layout.RAQM
def F(weight, size):
    f = ImageFont.truetype(os.path.join(R, 'fonts', 'Heebo-VF.ttf'), size, layout_engine=L)
    f.set_variation_by_name({'xb': 'Black', 'sb': 'Bold', 'md': 'Medium'}[weight]); return f
LOGO = Image.open(os.path.join(R, 'logo.png')).convert('RGB')
def cover(im, w, h, fx=0.5, fy=0.5):
    k = max(w/im.width, h/im.height); im = im.resize((round(im.width*k), round(im.height*k)), Image.LANCZOS)
    x = int((im.width-w)*fx); y = int((im.height-h)*fy); return im.crop((x, y, x+w, y+h))
def tb(d, s, f): bb = d.textbbox((0, 0), s, font=f, direction='rtl', language='he'); return bb, bb[2]-bb[0], bb[3]-bb[1]
def ct(img, s, f, cy, c, cx=W//2):
    d = ImageDraw.Draw(img); bb, tw, th = tb(d, s, f); d.text((cx-tw/2-bb[0], cy-th/2-bb[1]), s, font=f, fill=c, direction='rtl', language='he')
def pill(img, s, f, cy, fg, bg, cx=W//2, padx=44, pady=22):
    d = ImageDraw.Draw(img); bb, tw, th = tb(d, s, f); pw, ph = tw+2*padx, th+2*pady; x0 = int(cx-pw/2); y0 = int(cy-ph/2)
    d.rounded_rectangle([x0, y0, x0+pw, y0+ph], radius=ph//2, fill=bg); d.text((x0+padx-bb[0], y0+pady-bb[1]), s, font=f, fill=fg, direction='rtl', language='he')
def logo(img, x, y, w=130):
    h = round(w*LOGO.height/LOGO.width); p = 12
    ImageDraw.Draw(img).rounded_rectangle([x-p, y-p, x+w+p, y+h+p], radius=14, fill=IVORY); img.paste(LOGO.resize((w, h), Image.LANCZOS), (x, y))
def grad(top, bot):
    img = Image.new('RGB', (W, H), top); g = Image.new('L', (1, H))
    for y in range(H): g.putpixel((0, y), int(255*(y/H)))
    img.paste(Image.new('RGB', (W, H), bot), (0, 0), g.resize((W, H))); return img
def card(img, ph, x, y, r=34, outline=None, shadow=(120, 80, 100), sh_a=110):
    w, h = ph.size
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle([x, y+16, x+w, y+h+16], radius=r, fill=sh_a)
    img.paste(Image.new('RGB', (W, H), shadow), (0, 0), sh.filter(ImageFilter.GaussianBlur(22)))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w-1, h-1], radius=r, fill=255)
    img.paste(ph, (x, y), m)
    if outline: ImageDraw.Draw(img).rounded_rectangle([x, y, x+w-1, y+h-1], radius=r, outline=outline, width=5)
def tag(img, c):
    d = ImageDraw.Draw(img); f = F('md', 20); s = 'הדמיה להמחשה בלבד'; bb, tw, th = tb(d, s, f)
    d.text((W-50-tw-bb[0], H-26-th-bb[1]), s, font=f, fill=c, direction='rtl', language='he')

CW, CH, CX, CY = 920, 690, (W-920)//2, 430

# ---------- HOOK 1: customers film the package ----------
img = grad((244, 232, 226), (233, 211, 214))
ct(img, 'הלקוחות שלך מצלמים', F('xb', 82), 150, PLUM)
ct(img, 'את החבילה?', F('xb', 92), 262, GOLD_D)
ct(img, 'אריזה ממותגת = פרסום בחינם בכל סטורי', F('md', 38), 360, MUTED)
ph = cover(Image.open(os.path.join(R, 'gen', 'w46', 'unbox.jpg')).convert('RGB'), CW, CH, 0.5, 0.62)
# camera viewfinder overlay
ov = ph.copy(); d = ImageDraw.Draw(ov, 'RGBA')
d.rectangle([0, 0, CW, 70], fill=(0, 0, 0, 70))
m, ln, wd = 46, 70, 6
for (cx, cy, sx, sy) in ((m, m+40, 1, 1), (CW-m, m+40, -1, 1), (m, CH-m, 1, -1), (CW-m, CH-m, -1, -1)):
    d.line([(cx, cy), (cx+sx*ln, cy)], fill=(255, 255, 255, 235), width=wd)
    d.line([(cx, cy), (cx, cy+sy*ln)], fill=(255, 255, 255, 235), width=wd)
d.ellipse([34, 22, 60, 48], fill=(230, 40, 40, 255))
fr = ImageFont.truetype(os.path.join(R, 'fonts', 'Heebo-VF.ttf'), 30); fr.set_variation_by_name('Bold')
d.text((72, 18), 'REC  00:07', font=fr, fill=(255, 255, 255, 255))
# focus square in the centre
fx, fy, fs = CW//2, CH//2+40, 120
d.rectangle([fx-fs//2, fy-fs//2, fx+fs//2, fy+fs//2], outline=(255, 214, 90, 230), width=4)
card(img, ov, CX, CY)
pill(img, 'קופסאות משלוח ממותגות מ-500 יחידות', F('sb', 36), 1200, IVORY, PLUM)
ct(img, 'שלחו הודעה בוואטסאפ', F('sb', 40), 1285, PLUM)
logo(img, 50, 44); tag(img, MUTED)
img.save(os.path.join(OUT, 'he_hook1_unboxing.jpg'), quality=94)

# ---------- HOOK 2: Hanukkah ----------
img = grad(PLUM_D, (28, 8, 36))
random.seed(7); bk = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bk)
for _ in range(46):
    r = random.randint(6, 30); x = random.randint(0, W); y = random.choice([random.randint(0, 420), random.randint(1100, H)]) if random.random() < .75 else random.randint(0, H)
    bd.ellipse([x-r, y-r, x+r, y+r], fill=(230, 190, 110, random.randint(40, 120)))
img.paste(bk.filter(ImageFilter.GaussianBlur(5)), (0, 0), bk.filter(ImageFilter.GaussianBlur(5)))
ct(img, 'חנוכה בעוד 3 שבועות', F('xb', 84), 150, IVORY)
ct(img, 'האריזות שלכם מוכנות?', F('xb', 84), 262, GOLD)
ct(img, 'מארזי מתנה, שקיות וקופסאות עם הלוגו שלכם', F('md', 36), 360, (220, 200, 210))
ph = cover(Image.open(os.path.join(R, 'gen', 'img7_gift.png')).convert('RGB'), CW, CH, 0.5, 0.55)
card(img, ph, CX, CY, outline=GOLD, shadow=(0, 0, 0), sh_a=160)
pill(img, 'כדאי להזמין עכשיו · מ-500 יחידות', F('sb', 36), 1200, PLUM_D, GOLD)
ct(img, 'שלחו הודעה בוואטסאפ', F('sb', 40), 1285, IVORY)
logo(img, 50, 44); tag(img, (200, 180, 195))
img.save(os.path.join(OUT, 'he_hook2_hanukkah.jpg'), quality=94)

s = Image.new('RGB', (2*540+20, 675), 'white')
for i, n in enumerate(['he_hook1_unboxing', 'he_hook2_hanukkah']): s.paste(Image.open(os.path.join(OUT, n+'.jpg')).resize((540, 675)), (i*560, 0))
s.save('/tmp/he_hooks_sheet.jpg', quality=88)
