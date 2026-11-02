import os, sys
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool

W, H, FPS, DUR = 1080, 1920, 30, 16.5
NF = int(FPS * DUR)
PLUM = (78, 30, 92); PLUM_D = (40, 12, 52); GOLD = (210, 175, 110); IVORY = (250, 244, 228); BLUSH = (236, 205, 210)
LOGO_BG = (247, 241, 219)
L = ImageFont.Layout.RAQM; FD = '/home/claude/retal/fonts/'
def F(n, s): return ImageFont.truetype(FD + n, s, layout_engine=L)
XB, SB, MD = 'Alexandria-ExtraBold.ttf', 'Alexandria-SemiBold.ttf', 'Alexandria-Medium.ttf'
HERE = '/home/claude/retal/reel_guess/'; SRC = '/home/claude/retal/nov/'
LOGO = Image.open('/home/claude/retal/logo.png').convert('RGB')
OUT = HERE + 'frames'; os.makedirs(OUT, exist_ok=True)

def cl(x, a=0., b=1.): return max(a, min(b, x))
def pr(t, a, b): return cl((t - a) / (b - a))
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eob(x, k=1.7): x -= 1; return 1 + (k + 1) * x ** 3 + k * x ** 2

Z = 1.12
def load(n):
    return Image.open(SRC + n + '.jpg').convert('RGB').resize((int(W * Z), int(H * Z)), Image.LANCZOS)
PAIRS = [(load(f'sat_{k}_start'), load(f'sat_{k}_end')) for k in 'abc']

def zoom(im, z):
    s = Z / (1 + 0.10 * z); cw, ch = int(W * s), int(H * s)
    x0 = (im.width - cw) // 2; y0 = (im.height - ch) // 2
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)

BG = Image.new('RGB', (W, H), PLUM)
_g = Image.new('L', (1, H))
for y in range(H): _g.putpixel((0, y), int(255 * (y / H) ** 1.2))
BG.paste(Image.new('RGB', (W, H), PLUM_D), (0, 0), _g.resize((W, H)))

def shade(top=True, bottom=True):
    lay = Image.new('RGBA', (W, H), PLUM_D + (0,)); m = Image.new('L', (1, H))
    for y in range(H):
        a = 0
        if top: a = max(a, 215 * cl((520 - y) / 520) ** 1.2)
        if bottom: a = max(a, 235 * cl((y - 1250) / 670) ** 1.3)
        m.putpixel((0, y), int(a))
    lay.putalpha(m.resize((W, H))); return lay
SHADE = shade()

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

def put(fr, lay, cx=None, cy=0, alpha=1., scale=1., dx=0, dy=0):
    if alpha <= 0: return
    l = lay
    if scale != 1: l = l.resize((max(1, int(l.width * scale)), max(1, int(l.height * scale))), Image.LANCZOS)
    if alpha < 1: l = l.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * alpha)))
    x = (W - l.width) // 2 if cx is None else cx - l.width // 2
    fr.alpha_composite(l, (int(x + dx), int(cy - l.height / 2 + dy)))

def pill(s, size=64, fg=PLUM_D, bg=GOLD):
    t = tlayer(s, XB, size, fg); pw, ph = t.width + 80, t.height + 20
    lay = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=ph // 2, fill=bg + (255,))
    lay.alpha_composite(t, (40, 10)); return lay

ANS = [pill('عطر'), pill('حلويات'), pill('شمعة')]
NUMS = ['علبة 1', 'علبة 2', 'علبة 3']
SC = [2.0, 5.6, 9.2]; SL = 3.6; REV = 2.0   # reveal at +2.0s
END = 12.8
CONCEPT = tlayer('تصور إبداعي للتغليف', MD, 26, IVORY)
DOTS = [None] * 3

def scene(fr, k, t):
    lt = t - SC[k]; c, o = PAIRS[k]
    z = cl(lt / (SL + 0.4))
    base = zoom(c, z)
    r = pr(lt, REV, REV + 0.45)
    if r > 0:
        base = Image.blend(base, zoom(o, z), eio(r))
    ph = base.convert('RGBA')
    a = eio(pr(lt, 0, 0.38))
    if a < 1: fr.alpha_composite(ph, (int(-(1 - a) * W), 0))
    else: fr.alpha_composite(ph)
    fr.alpha_composite(SHADE)
    # golden flash at reveal
    fl = pr(lt, REV - 0.05, REV + 0.15) * (1 - pr(lt, REV + 0.15, REV + 0.55))
    if fl > 0:
        f = Image.new('RGBA', (W, H), (255, 236, 200, int(150 * fl))); fr.alpha_composite(f)
    q = pr(lt, 0.35, 0.75)
    put(fr, tlayer(NUMS[k], SB, 54, GOLD), cy=200, alpha=eo(q), dy=(1 - eo(q)) * -30)
    if lt < REV + 0.1:
        g = pr(lt, 0.5, 0.9)
        put(fr, tlayer('شو جوّاها؟', XB, 110, IVORY), cy=330, alpha=eo(g) * (1 - pr(lt, REV - 0.1, REV + 0.1)), scale=0.85 + 0.15 * eob(g) if g < 1 else 1)
        # 3-2-1 countdown dots
        for i in range(3):
            on = lt >= 0.9 + i * 0.35
            d = ImageDraw.Draw(fr); cx = W // 2 + (1 - i) * 70; cy = 1650
            d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(GOLD if on else (120, 90, 130)) + (255,))
    else:
        p = pr(lt, REV + 0.3, REV + 0.7)
        put(fr, ANS[k], cy=1640, alpha=min(1, p * 2), scale=0.6 + 0.4 * eob(p) if p < 1 else 1)
    put(fr, CONCEPT, cx=W - 60 - CONCEPT.width // 2, cy=1870, alpha=0.8)

def end(fr, t):
    a = eo(pr(t, END, END + 0.4))
    b = BG.copy().convert('RGBA'); b.putalpha(int(255 * a)); fr.alpha_composite(b)
    e = eo(pr(t, END + 0.1, END + 0.6))
    lw = 460; lh = round(lw * LOGO.height / LOGO.width); pad = 28
    plate = Image.new('RGBA', (lw + pad * 2, lh + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, lw + pad * 2 - 1, lh + pad * 2 - 1], radius=28, fill=LOGO_BG + (255,))
    plate.paste(LOGO.resize((lw, lh), Image.LANCZOS), (pad, pad))
    put(fr, plate, cy=560, alpha=e, scale=0.9 + 0.1 * e)
    s1 = pr(t, END + 0.4, END + 0.8); s2 = pr(t, END + 0.6, END + 1.0)
    put(fr, tlayer('كل منتج', XB, 96, IVORY), cy=820, alpha=eo(s1), dy=(1 - eo(s1)) * 40)
    put(fr, tlayer('إله علبة بتليق فيه', XB, 84, GOLD), cy=945, alpha=eo(s2), dy=(1 - eo(s2)) * 40)
    s3 = pr(t, END + 1.0, END + 1.4)
    put(fr, tlayer('اكتبلنا: إنت شو بتبيع؟', SB, 58, IVORY), cy=1120, alpha=eo(s3))
    put(fr, tlayer('ومنقلّك شو العلبة اللي إلك', MD, 46, BLUSH), cy=1200, alpha=eo(pr(t, END + 1.2, END + 1.6)))
    p = eo(pr(t, END + 1.6, END + 2.0))
    if p > 0: put(fr, pill('أقل طلب 500 قطعة', 46), cy=1370, alpha=p, scale=0.85 + 0.15 * eob(p))

def render(fi):
    t = fi / FPS
    fr = BG.copy().convert('RGBA')
    if t < SC[0] + 0.4:
        h = pr(t, 0.0, 0.45)
        put(fr, tlayer('خمّن', XB, 170, GOLD), cy=780, scale=1.7 - 0.7 * eob(h) if h < 1 else 1, alpha=min(1, h * 2))
        g = pr(t, 0.6, 1.0)
        put(fr, tlayer('شو جوّا العلبة', XB, 112, IVORY), cy=960, alpha=eo(g), dy=(1 - eo(g)) * 50)
        g2 = pr(t, 1.1, 1.5)
        put(fr, tlayer('3 علب.. 3 مفاجآت', MD, 50, BLUSH), cy=1090, alpha=eo(g2))
        if t >= SC[0]: scene(fr, 0, t)
    elif t < END + 0.4:
        k = 2 if t >= SC[2] else 1 if t >= SC[1] else 0
        if k > 0 and t < SC[k] + 0.38: scene(fr, k - 1, t)
        scene(fr, k, t)
        if t >= END: end(fr, t)
    else:
        end(fr, t)
    return fr.convert('RGB')

def job(fi):
    p = f'{OUT}/f{fi:04d}.png'
    if not os.path.exists(p): render(fi).save(p, compress_level=1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for s in sys.argv[1:]: render(int(float(s) * FPS)).save(f'{HERE}t_{s}.jpg', quality=88)
    else:
        with Pool(2) as pool: pool.map(job, range(NF), chunksize=6)
