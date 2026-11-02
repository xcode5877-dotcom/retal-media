import os, sys
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool

W, H, FPS, DUR = 1080, 1920, 30, 12.5
NF = int(FPS * DUR)
PLUM = (78, 30, 92); PLUM_D = (40, 12, 52); GOLD = (210, 175, 110); IVORY = (250, 244, 228); BLUSH = (236, 205, 210)
LOGO_BG = (247, 241, 219)
L = ImageFont.Layout.RAQM; FD = '/home/claude/retal/fonts/'
def F(n, s): return ImageFont.truetype(FD + n, s, layout_engine=L)
XB, SB, MD = 'Alexandria-ExtraBold.ttf', 'Alexandria-SemiBold.ttf', 'Alexandria-Medium.ttf'
HERE = '/home/claude/retal/reel_carton/'; SRC = '/home/claude/retal/nov/'
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
A, B = load('wed_start'), load('wed_end')

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
        if top: a = max(a, 240 * cl((640 - y) / 640) ** 0.8)
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
from PIL import ImageFilter
CONCEPT = tlayer('تصور إبداعي للتغليف', MD, 26, IVORY)
T0, T1 = 3.3, 4.5   # transformation window
END = 9.4
def wipe(a, b, p):
    """diagonal golden sweep from bottom-left to top-right"""
    if p <= 0: return a.copy()
    if p >= 1: return b.copy()
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    pos = -150 + p * (W + H + 300)
    d.polygon([(0, H), (0, H - pos), (pos, H), ], fill=255) if False else None
    # band across diagonal x + (H - y) < pos
    poly = [(-10, H + 10), (pos, H + 10), (-10, H + 10 - pos)]
    d.polygon(poly, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(40))
    out = Image.composite(b, a, m).convert('RGBA')
    glow = Image.new('L', (W, H), 0); dg = ImageDraw.Draw(glow)
    dg.line([(pos, H), (-10, H - pos)], fill=255, width=90)
    glow = glow.filter(ImageFilter.GaussianBlur(45))
    gl = Image.new('RGBA', (W, H), (255, 220, 150, 0)); gl.putalpha(glow.point(lambda v: int(v * 0.85)))
    out.alpha_composite(gl); return out.convert('RGB')

def render(fi):
    t = fi / FPS
    fr = BG.copy().convert('RGBA')
    if t < END + 0.4:
        z = cl(t / END)
        a, b = zoom(A, z), zoom(B, z)
        img = wipe(a, b, eio(pr(t, T0, T1))).convert('RGBA')
        fr.alpha_composite(img); fr.alpha_composite(SHADE)
        # texts
        h = pr(t, 0.1, 0.5); o1 = 1 - pr(t, 1.6, 1.8)
        put(fr, tlayer('هاي كرتونة عادية..', XB, 92, IVORY), cy=300, alpha=min(1, h * 2) * o1, scale=1.3 - 0.3 * eob(h) if h < 1 else 1)
        g = pr(t, 1.8, 2.2); o2 = 1 - pr(t, T0 - 0.2, T0)
        put(fr, tlayer('شوف شو بيصير', XB, 92, IVORY), cy=260, alpha=eo(g) * o2, dy=(1 - eo(g)) * 30)
        put(fr, tlayer('لما تلبس هوية محلك', XB, 80, GOLD), cy=400, alpha=eo(pr(t, 2.1, 2.5)) * o2, dy=(1 - eo(pr(t, 2.1, 2.5))) * 30)
        q = pr(t, T1 + 0.1, T1 + 0.5); o3 = 1 - pr(t, 6.9, 7.1)
        put(fr, tlayer('نفس الكرتونة..', XB, 96, IVORY), cy=280, alpha=eo(q) * o3, scale=0.85 + 0.15 * eob(q) if q < 1 else 1)
        put(fr, pill('الفرق بالتغليف', 64), cy=1640, alpha=eo(pr(t, T1 + 0.5, T1 + 0.9)) * o3, scale=0.7 + 0.3 * eob(pr(t, T1 + 0.5, T1 + 0.9)) if t < T1 + 0.9 else 1)
        r = pr(t, 7.1, 7.5)
        put(fr, tlayer('الزبون بيحكم', XB, 100, IVORY), cy=280, alpha=eo(r), dy=(1 - eo(r)) * 30)
        put(fr, tlayer('من أول نظرة', XB, 100, GOLD), cy=420, alpha=eo(pr(t, 7.4, 7.8)), dy=(1 - eo(pr(t, 7.4, 7.8))) * 30)
        put(fr, CONCEPT, cx=W - 60 - CONCEPT.width // 2, cy=1870, alpha=0.8)
    if t >= END:
        a = eo(pr(t, END, END + 0.4))
        bb = BG.copy().convert('RGBA'); bb.putalpha(int(255 * a)); fr.alpha_composite(bb)
        e = eo(pr(t, END + 0.1, END + 0.6))
        lw = 460; lh = round(lw * LOGO.height / LOGO.width); pad = 28
        plate = Image.new('RGBA', (lw + pad * 2, lh + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(plate).rounded_rectangle([0, 0, lw + pad * 2 - 1, lh + pad * 2 - 1], radius=28, fill=LOGO_BG + (255,))
        plate.paste(LOGO.resize((lw, lh), Image.LANCZOS), (pad, pad))
        put(fr, plate, cy=600, alpha=e, scale=0.9 + 0.1 * e)
        s1 = pr(t, END + 0.4, END + 0.8); s2 = pr(t, END + 0.6, END + 1.0)
        put(fr, tlayer('منعملك علبة', XB, 96, IVORY), cy=880, alpha=eo(s1), dy=(1 - eo(s1)) * 40)
        put(fr, tlayer('بيتذكرها زبونك', XB, 96, GOLD), cy=1005, alpha=eo(s2), dy=(1 - eo(s2)) * 40)
        p = eo(pr(t, END + 1.0, END + 1.4))
        if p > 0: put(fr, pill('راسلنا على واتساب', 52), cy=1200, alpha=p, scale=0.85 + 0.15 * eob(p))
        put(fr, tlayer('أقل طلب 500 قطعة', MD, 46, BLUSH), cy=1330, alpha=eo(pr(t, END + 1.3, END + 1.7)))
    return fr.convert('RGB')

def job(fi):
    p = f'{OUT}/f{fi:04d}.png'
    if not os.path.exists(p): render(fi).save(p, compress_level=1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for s in sys.argv[1:]: render(int(float(s) * FPS)).save(f'{HERE}t_{s}.jpg', quality=88)
    else:
        with Pool(2) as pool: pool.map(job, range(NF), chunksize=6)
