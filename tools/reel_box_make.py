import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from multiprocessing import Pool

W, H, FPS, DUR = 1080, 1920, 30, 14.0
NF = int(FPS * DUR)
PLUM = (78, 30, 92); PLUM_D = (40, 12, 52); GOLD = (210, 175, 110); IVORY = (250, 244, 228); BLUSH = (236, 205, 210)
LOGO_BG = (247, 241, 219)
L = ImageFont.Layout.RAQM; FD = '/home/claude/retal/fonts/'
def F(n, s): return ImageFont.truetype(FD + n, s, layout_engine=L)
XB, SB, MD = 'Alexandria-ExtraBold.ttf', 'Alexandria-SemiBold.ttf', 'Alexandria-Medium.ttf'
HERE = '/home/claude/retal/reel_box/'
LOGO = Image.open('/home/claude/retal/logo.png').convert('RGB')
OUT = HERE + 'frames'; os.makedirs(OUT, exist_ok=True)

def cl(x, a=0., b=1.): return max(a, min(b, x))
def pr(t, a, b): return cl((t - a) / (b - a))
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eob(x, k=1.7): x -= 1; return 1 + (k + 1) * x ** 3 + k * x ** 2

# photos, pre-sized a bit larger than the frame for a slow push-in
PH = []
for i in (1, 2, 3):
    im = Image.open(f'{HERE}b{i}.png').convert('RGB')
    PH.append(im.resize((int(W * 1.12), int(H * 1.12)), Image.LANCZOS))

def photo_frame(k, z):
    """z in 0..1 -> zoom from 1.0 to 1.12 (crop shrinks)"""
    im = PH[k]; s = 1.12 / (1 + 0.10 * z)
    cw, ch = int(W * s), int(H * s)
    x0 = (im.width - cw) // 2; y0 = (im.height - ch) // 2
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)

BG = Image.new('RGB', (W, H), PLUM)
_g = Image.new('L', (1, H))
for y in range(H): _g.putpixel((0, y), int(255 * (y / H) ** 1.2))
BG.paste(Image.new('RGB', (W, H), PLUM_D), (0, 0), _g.resize((W, H)))

# bottom shade for labels
SHADE = Image.new('RGBA', (W, H), PLUM_D + (0,))
_m = Image.new('L', (1, H))
for y in range(H): _m.putpixel((0, y), int(235 * cl((y - 1150) / 600) ** 1.3))
SHADE.putalpha(_m.resize((W, H)))

_cache = {}
def tlayer(s, font, size, color):
    k = (s, font, size, color)
    if k not in _cache:
        f = F(font, size); d = ImageDraw.Draw(Image.new('L', (1, 1)))
        bb = d.textbbox((0, 0), s, font=f, direction='rtl', language='ar')
        lay = Image.new('RGBA', (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((20 - bb[0], 20 - bb[1]), s, font=f, fill=color + (255,), direction='rtl', language='ar')
        _cache[k] = lay
    return _cache[k]

def put(fr, lay, cx=None, cy=0, right=None, alpha=1., scale=1., dx=0, dy=0):
    if alpha <= 0: return
    l = lay
    if scale != 1:
        l = l.resize((max(1, int(l.width * scale)), max(1, int(l.height * scale))), Image.LANCZOS)
    if alpha < 1:
        l = l.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * alpha)))
    x = (W - l.width) // 2 if right is None else right - l.width
    if cx is not None: x = cx - l.width // 2
    fr.alpha_composite(l, (int(x + dx), int(cy - l.height / 2 + dy)))

def num_badge(n, r=78):
    lay = Image.new('RGBA', (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([4, 4, 2 * r + 4, 2 * r + 4], fill=GOLD + (255,))
    t = tlayer(str(n), XB, int(r * 1.15), PLUM_D)
    lay.alpha_composite(t, (r + 4 - t.width // 2, r + 4 - t.height // 2 + 4))
    return lay
BADGE = [num_badge(n) for n in (1, 2, 3)]
SMALLB = [num_badge(n, 46) for n in (1, 2, 3)]

LABELS = [('هادية وفخمة', 'للمحلات الراقية والهدايا'),
          ('جريئة وملفتة', 'للبراندات اللي بدها تنشاف'),
          ('طبيعية ودافية', 'للمنتجات البيتية والحِرفية')]
SC = [2.2, 4.8, 7.4]; SLEN = 2.6   # scene starts; each lasts 2.6s
TRI = 10.0; END = 12.0
CONCEPT = tlayer('تصور إبداعي للتغليف', MD, 26, IVORY)

def scene(fr, k, t):
    t0 = SC[k]; lt = t - t0
    ph = photo_frame(k, cl(lt / (SLEN + 0.4))).convert('RGBA')
    # push-in transition: comes in from the left with a slight scale
    a = eio(pr(lt, 0, 0.38))
    if a < 1:
        dx = int(-(1 - a) * W)
        fr.alpha_composite(ph, (dx, 0)) if dx > -W else None
    else:
        fr.alpha_composite(ph)
    fr.alpha_composite(SHADE)
    b = pr(lt, 0.35, 0.75)
    put(fr, BADGE[k], cx=W - 150, cy=200, alpha=min(1, b * 2), scale=0.6 + 0.4 * eob(b) if b < 1 else 1)
    l1 = pr(lt, 0.5, 0.9); l2 = pr(lt, 0.7, 1.1)
    put(fr, tlayer(LABELS[k][0], XB, 104, IVORY), cy=1560, alpha=eo(l1), dy=(1 - eo(l1)) * 60)
    put(fr, tlayer(LABELS[k][1], MD, 46, BLUSH), cy=1690, alpha=eo(l2), dy=(1 - eo(l2)) * 40)
    put(fr, CONCEPT, right=W - 60, cy=1860, alpha=0.8)

def render(fi):
    t = fi / FPS
    fr = BG.copy().convert('RGBA')
    if t < SC[0] + 0.38:
        # hook
        h = pr(t, 0.0, 0.45)
        put(fr, tlayer('أي علبة', XB, 150, IVORY), cy=820, scale=1.7 - 0.7 * eob(h) if h < 1 else 1, alpha=min(1, h * 2))
        g = pr(t, 0.7, 1.1)
        put(fr, tlayer('بتشبه محلك؟', XB, 120, GOLD), cy=1000, alpha=eo(g), dy=(1 - eo(g)) * 50)
        p = pr(t, 1.3, 1.6)
        for k in range(3):
            q = pr(t, 1.3 + k * 0.14, 1.6 + k * 0.14)
            if q > 0: put(fr, SMALLB[k], cx=W // 2 + (1 - k) * 150, cy=1200, alpha=min(1, q * 2), scale=0.5 + 0.5 * eob(q) if q < 1 else 1)
        if t >= SC[0]:
            scene(fr, 0, t)
    elif t < TRI + 0.4:
        k = 2 if t >= SC[2] else 1 if t >= SC[1] else 0
        # keep previous scene under the incoming one during its push-in
        if k > 0 and t < SC[k] + 0.38:
            scene(fr, k - 1, t)
        scene(fr, k, t)
        if t >= TRI:
            tri(fr, t)
    elif t < END + 0.4:
        tri(fr, t)
        if t >= END: end(fr, t)
    else:
        end(fr, t)
    return fr.convert('RGB')

TW = 300; TH = 533
THUMBS = []
for k in range(3):
    im = PH[k].resize((TW, TH), Image.LANCZOS)
    m = Image.new('L', (TW, TH), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, TW - 1, TH - 1], radius=28, fill=255)
    lay = Image.new('RGBA', (TW, TH), (0, 0, 0, 0)); lay.paste(im, (0, 0), m)
    ImageDraw.Draw(lay).rounded_rectangle([0, 0, TW - 1, TH - 1], radius=28, outline=GOLD + (255,), width=4)
    THUMBS.append(lay)

def tri(fr, t):
    a = eo(pr(t, TRI, TRI + 0.4))
    base = BG.copy().convert('RGBA')
    if a < 1:
        base.putalpha(int(255 * a))
    fr.alpha_composite(base)
    put(fr, tlayer('إنت أي رقم؟', XB, 110, IVORY), cy=420, alpha=eo(pr(t, TRI + 0.1, TRI + 0.5)))
    xs = [W - 50 - TW, (W - TW) // 2, 50]   # RTL: 1 on the right
    for k in range(3):
        q = pr(t, TRI + 0.15 + k * 0.15, TRI + 0.55 + k * 0.15)
        if q <= 0: continue
        th = THUMBS[k]
        if q < 1:
            th = th.copy(); th.putalpha(th.getchannel('A').point(lambda v: int(v * q)))
        fr.alpha_composite(th, (xs[k], int(620 + (1 - eo(q)) * 120)))
        put(fr, SMALLB[k], cx=xs[k] + TW // 2, cy=620 + TH, alpha=q, scale=0.5 + 0.5 * eob(q) if q < 1 else 1)
    c = pr(t, TRI + 0.8, TRI + 1.2)
    put(fr, tlayer('اكتبلنا الرقم بالتعليقات', XB, 72, GOLD), cy=1440, alpha=eo(c), dy=(1 - eo(c)) * 40)

def end(fr, t):
    a = eo(pr(t, END, END + 0.4))
    base = BG.copy().convert('RGBA'); base.putalpha(int(255 * a)); fr.alpha_composite(base)
    e = eo(pr(t, END + 0.1, END + 0.6))
    lw = 500; lh = round(lw * LOGO.height / LOGO.width); pad = 30
    plate = Image.new('RGBA', (lw + pad * 2, lh + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, lw + pad * 2 - 1, lh + pad * 2 - 1], radius=30, fill=LOGO_BG + (255,))
    plate.paste(LOGO.resize((lw, lh), Image.LANCZOS), (pad, pad))
    put(fr, plate, cy=640, alpha=e, scale=0.9 + 0.1 * e)
    s1 = pr(t, END + 0.4, END + 0.8); s2 = pr(t, END + 0.6, END + 1.0)
    put(fr, tlayer('منعملك تغليف', XB, 92, IVORY), cy=920, alpha=eo(s1), dy=(1 - eo(s1)) * 40)
    put(fr, tlayer('بيشبه محلك', XB, 92, GOLD), cy=1045, alpha=eo(s2), dy=(1 - eo(s2)) * 40)
    p = eo(pr(t, END + 0.9, END + 1.3))
    if p > 0:
        lay = tlayer('راسلنا على واتساب', SB, 52, PLUM_D)
        pw, ph = lay.width + 110, lay.height + 34
        pill = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=ph // 2, fill=GOLD + (255,))
        pill.alpha_composite(lay, (55, 17))
        put(fr, pill, cy=1230, alpha=p, scale=0.85 + 0.15 * eob(p))
    put(fr, tlayer('أقل طلب 500 قطعة', MD, 44, BLUSH), cy=1360, alpha=eo(pr(t, END + 1.1, END + 1.5)))

def job(fi):
    p = f'{OUT}/f{fi:04d}.png'
    if not os.path.exists(p): render(fi).save(p, compress_level=1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for s in sys.argv[1:]: render(int(float(s) * FPS)).save(f'{HERE}t_{s}.jpg', quality=88)
    else:
        with Pool(2) as pool: pool.map(job, range(NF), chunksize=6)
