import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
IVORY = (247, 241, 219)      # logo background, so the logo sits seamlessly
PLUM = (78, 30, 92)
PLUM_D = (46, 14, 58)
GOLD = (196, 160, 96)
TERRA = (78, 30, 92)         # mistake accent -> brand plum
SAGE = (196, 160, 96)        # fix accent -> brand gold
BLUSH = (236, 205, 210)
GOLD_D = (160, 120, 60)
MUTED = (112, 86, 110)
L = ImageFont.Layout.RAQM
FD = '/home/claude/retal/fonts/'
XB, SB, MD = FD + 'Alexandria-ExtraBold.ttf', FD + 'Alexandria-SemiBold.ttf', FD + 'Alexandria-Medium.ttf'
def F(p, s): return ImageFont.truetype(p, s, layout_engine=L)
GEN = '/home/claude/retal/gen/'
LOGO = Image.open('/home/claude/retal/logo.png').convert('RGB')
OUT = '/home/claude/retal/carousel3/out_' + os.environ.get('BGMODE', 'ivory'); os.makedirs(OUT, exist_ok=True)
RX = W - 90
MODE = os.environ.get('BGMODE', 'ivory')
DARK = MODE in ('plum', 'photo')
T_TITLE = IVORY if DARK else PLUM
T_BODY = (236, 205, 210) if DARK else MUTED
def bg_img(photo=None, fy=0.5):
    if MODE == 'plum':
        img = Image.new('RGB', (W, H), PLUM)
        g = Image.new('L', (1, H))
        for y in range(H): g.putpixel((0, y), int(255 * (y / H) ** 1.2))
        img.paste(Image.new('RGB', (W, H), PLUM_D), (0, 0), g.resize((W, H)))
        d = ImageDraw.Draw(img, 'RGBA')
        for r in (260, 320, 380): d.arc([W - r, -r, W + r, r], 90, 180, fill=GOLD + (55,), width=2)
        return img
    if MODE == 'blush':
        img = Image.new('RGB', (W, H), (250, 240, 236))
        g = Image.new('L', (1, H))
        for y in range(H): g.putpixel((0, y), int(255 * (y / H)))
        img.paste(Image.new('RGB', (W, H), (238, 210, 214)), (0, 0), g.resize((W, H)))
        d = ImageDraw.Draw(img, 'RGBA')
        for r in (300, 370, 440): d.arc([-r, H - r, r, H + r], 270, 360, fill=GOLD + (90,), width=2)
        d.rectangle([40, 40, W - 40, H - 40], outline=GOLD + (120,), width=2)
        return img
    if MODE == 'photo' and photo:
        im = Image.open(photo).convert('RGB')
        ph = round(im.height * W / im.width)
        if ph >= H:
            img = cover(photo, W, H, fy); top = 0
        else:
            img = Image.new('RGB', (W, H), PLUM_D)
            img.paste(im.resize((W, ph), Image.LANCZOS), (0, H - ph)); top = H - ph
        y0 = max(600, top + 150); y1 = y0 + 400
        ov = Image.new('L', (1, H))
        for y in range(H):
            if y < y0: a = 1.0
            elif y < y1: a = (1 - (y - y0) / (y1 - y0)) ** 1.6
            else: a = 0
            if y > H - 220: a = max(a, 0.55 * (y - (H - 220)) / 220)
            ov.putpixel((0, y), int(255 * a))
        img.paste(Image.new('RGB', (W, H), PLUM_D), (0, 0), ov.resize((W, H)))
        return img
    return Image.new('RGB', (W, H), IVORY)

def tsize(d, s, f):
    bb = d.textbbox((0, 0), s, font=f, direction='rtl', language='ar'); return bb, bb[2] - bb[0], bb[3] - bb[1]

def rtext(img, s, f, top, color, right=RX):
    d = ImageDraw.Draw(img); bb, tw, th = tsize(d, s, f)
    d.text((right - tw - bb[0], top - bb[1]), s, font=f, fill=color, direction='rtl', language='ar')
    return top + th, right - tw

def ctext(img, s, f, cy, color):
    d = ImageDraw.Draw(img); bb, tw, th = tsize(d, s, f)
    d.text(((W - tw) / 2 - bb[0], cy - th / 2 - bb[1]), s, font=f, fill=color, direction='rtl', language='ar')

def chip(img, s, top, fg, bg, right=RX, size=34):
    d = ImageDraw.Draw(img); f = F(SB, size); bb, tw, th = tsize(d, s, f)
    pw, ph = tw + 56, th + 30
    d.rounded_rectangle([right - pw, top, right, top + ph], radius=ph // 2, fill=bg)
    d.text((right - pw + 28 - bb[0], top + 15 - bb[1]), s, font=f, fill=fg, direction='rtl', language='ar')
    return top + ph

def cover(path, w, h, fy=0.5):
    im = Image.open(path).convert('RGB')
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x0 = (im.width - w) // 2; y0 = int(max(0, min(im.height - h, im.height * fy - h / 2)))
    return im.crop((x0, y0, x0 + w, y0 + h))

def card(img, path, box, fy=0.5, r=34):
    x0, y0, x1, y1 = box
    ph = cover(path, x1 - x0, y1 - y0, fy)
    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, ph.width - 1, ph.height - 1], radius=r, fill=255)
    img.paste(ph, (x0, y0), m)

def big_index(img, n, color):
    """huge outlined number on the left, editorial feel"""
    d = ImageDraw.Draw(img); f = F(XB, 150); s = f'0{n}'
    bb = d.textbbox((0, 0), s, font=f)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.text((86 - bb[0], 96 - bb[1]), s, font=f, fill=(0, 0, 0, 0), stroke_width=3, stroke_fill=color)
    img.paste(lay, (0, 0), lay)

def footer(img, k, total=7, label=True):
    d = ImageDraw.Draw(img)
    # dots progress, right-to-left reading
    x = RX
    for i in range(total):
        r = 9 if i == k - 1 else 6
        c = (GOLD if DARK else PLUM) if i == k - 1 else ((150, 110, 160) if DARK else (205, 190, 200))
        d.ellipse([x - 2 * r, H - 78 - r, x, H - 78 + r], fill=c); x -= 34
    if label:
        f = F(MD, 24); s = 'تصور إبداعي للتغليف'; bb, tw, th = tsize(d, s, f)
        d.text((90 - bb[0], H - 78 - th / 2 - bb[1]), s, font=f, fill=T_BODY, direction='rtl', language='ar')

def fix_box(img, s, top):
    """sage 'the fix' block with a check mark"""
    d = ImageDraw.Draw(img); size = 40
    while tsize(d, s, F(SB, size))[1] + 150 > W - 180: size -= 1
    f = F(SB, size); bb, tw, th = tsize(d, s, f)
    bw = min(W - 180, tw + 150); bh = th + 64; x1 = RX; x0 = x1 - bw
    d.rounded_rectangle([x0, top, x1, top + bh], radius=26, fill=(BLUSH if not DARK else (96, 44, 108)), outline=GOLD, width=3)
    d.text((x1 - 40 - tw - bb[0], top + 32 - bb[1]), s, font=f, fill=(IVORY if DARK else PLUM_D), direction='rtl', language='ar')
    cx, cy = x0 + 50, top + bh / 2
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(GOLD if DARK else PLUM))
    d.line([(cx - 11, cy + 1), (cx - 3, cy + 10), (cx + 13, cy - 9)], fill=IVORY, width=6, joint='curve')
    return top + bh

def mistake_head(img, n, title, body):
    big_index(img, n, GOLD)
    y = chip(img, f'غلط رقم {n}', 110, PLUM_D if DARK else IVORY, GOLD if DARK else PLUM)
    y = max(y, 250)
    size = 76
    d = ImageDraw.Draw(img)
    while tsize(d, title, F(XB, size))[1] > W - 180: size -= 2
    y, _ = rtext(img, title, F(XB, size), y + 34, T_TITLE)
    y, _ = rtext(img, body, F(MD, 38), y + 34, T_BODY)
    return y

# ---------- simple line illustrations for the photo-less slides ----------
def draw_bag(img, cx, cy, s=1.0, heavy=True):
    d = ImageDraw.Draw(img)
    w, h = 300 * s, 360 * s
    x0, y0 = cx - w / 2, cy - h / 2 + 60 * s
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=18, outline=PLUM, width=8, fill=(244, 230, 232))
    d.arc([cx - 80 * s, y0 - 110 * s, cx + 80 * s, y0 + 50 * s], 180, 360, fill=PLUM, width=10)
    # jars inside
    for k, dx in enumerate((-70, 40)):
        jx = cx + dx * s; jy = y0 - 40 * s
        d.rounded_rectangle([jx - 45 * s, jy, jx + 45 * s, jy + 120 * s], radius=14, fill=GOLD, outline=PLUM_D, width=5)
        d.rectangle([jx - 38 * s, jy - 22 * s, jx + 38 * s, jy + 6 * s], fill=PLUM_D)
    d.line([(cx - 60 * s, y0 + h * 0.55), (cx + 60 * s, y0 + h * 0.55)], fill=GOLD, width=6)

def draw_swatches(img, cx, cy):
    d = ImageDraw.Draw(img)
    cols = [PLUM, (236, 205, 210), GOLD, IVORY]
    for i, c in enumerate(cols):
        x = cx - 270 + i * 180
        d.ellipse([x - 70, cy - 70, x + 70, cy + 70], fill=c, outline=PLUM, width=5)
    # a box wearing the same colors
    bx, by = cx, cy + 250
    d.polygon([(bx - 200, by - 40), (bx, by - 120), (bx + 200, by - 40), (bx, by + 40)], fill=(236, 205, 210), outline=PLUM)
    d.polygon([(bx - 200, by - 40), (bx, by + 40), (bx, by + 220), (bx - 200, by + 140)], fill=PLUM, outline=PLUM_D)
    d.polygon([(bx + 200, by - 40), (bx, by + 40), (bx, by + 220), (bx + 200, by + 140)], fill=(110, 50, 120), outline=PLUM_D)
    d.line([(bx - 200, by + 80), (bx, by + 160)], fill=GOLD, width=6)
    d.line([(bx + 200, by + 80), (bx, by + 160)], fill=GOLD, width=6)

def draw_two_boxes(img, cx, cy):
    d = ImageDraw.Draw(img)
    # gift box with ribbon (right, bigger)
    x0, y0 = cx + 30, cy - 120
    d.rounded_rectangle([x0, y0, x0 + 320, y0 + 260], radius=14, fill=PLUM, outline=PLUM_D, width=5)
    d.rectangle([x0 - 10, y0 - 40, x0 + 330, y0 + 10], fill=(96, 40, 112), outline=PLUM_D, width=5)
    d.rectangle([x0 + 145, y0 - 40, x0 + 175, y0 + 260], fill=GOLD)
    d.ellipse([x0 + 90, y0 - 110, x0 + 162, y0 - 40], outline=GOLD, width=14)
    d.ellipse([x0 + 158, y0 - 110, x0 + 230, y0 - 40], outline=GOLD, width=14)
    # everyday mailer (left, simple)
    x1, y1 = cx - 370, cy - 20
    d.rounded_rectangle([x1, y1, x1 + 300, y1 + 160], radius=10, fill=(236, 205, 210), outline=PLUM, width=5)
    d.line([(x1, y1 + 40), (x1 + 300, y1 + 40)], fill=PLUM, width=4)
    d.ellipse([x1 + 125, y1 + 75, x1 + 175, y1 + 125], outline=PLUM, width=5)
    f = F(SB, 36)
    for s, xx in (('هدية', x0 + 160), ('يومي', x1 + 150)):
        bb, tw, th = tsize(d, s, f)
        d.text((xx - tw / 2 - bb[0], cy + 190 - bb[1]), s, font=f, fill=PLUM, direction='rtl', language='ar')

slides = []

# 1 — cover
if MODE == 'photo':
    img = cover(GEN + 'img2.png', W, H, 0.4)
    ov = Image.new('L', (1, H))
    for y in range(H): ov.putpixel((0, y), int(255 * 0.96 * min(1, max(0, (y - 520) / 360)) ** 1.3))
    img.paste(Image.new('RGB', (W, H), PLUM_D), (0, 0), ov.resize((W, H)))
    d = ImageDraw.Draw(img)
    y = chip(img, 'قبل ما تطبع علبتك', 860, PLUM_D, GOLD)
    y, _ = rtext(img, '5 أخطاء بالتغليف', F(XB, 104), y + 30, IVORY)
    y, _ = rtext(img, 'بتخسّرك زباين', F(XB, 84), y + 26, GOLD)
    d.rounded_rectangle([90, 1230, 250, 1290], radius=30, fill=GOLD)
    f = F(SB, 32); bb, tw, th = tsize(d, 'اسحب ←', f)
    d.text((170 - tw / 2 - bb[0], 1260 - th / 2 - bb[1]), 'اسحب ←', font=f, fill=PLUM_D, direction='rtl', language='ar')
    slides.append(img)
else:
    img = Image.new('RGB', (W, H), IVORY)
    img.paste(cover(GEN + 'img2.png', W, 760, 0.42), (0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 760, W, 768], fill=GOLD)
    y = chip(img, 'قبل ما تطبع علبتك', 820, IVORY, PLUM)
    y, _ = rtext(img, '5 أخطاء بالتغليف', F(XB, 104), y + 30, PLUM)
    y, _ = rtext(img, 'بتخسّرك زباين', F(XB, 84), y + 26, GOLD_D)
    d.rounded_rectangle([90, 1210, 250, 1270], radius=30, fill=GOLD)
    f = F(SB, 32); bb, tw, th = tsize(d, 'اسحب ←', f)
    d.text((170 - tw / 2 - bb[0], 1240 - th / 2 - bb[1]), 'اسحب ←', font=f, fill=PLUM_D, direction='rtl', language='ar')
    slides.append(img)

# 2 — mistake 1 + photo
img = bg_img(GEN + 'img3.png', 0.62)
y = mistake_head(img, 1, 'علبة أكبر من المنتج', 'المنتج بيتحرك جوا وبيوصل مخدوش.')
y = fix_box(img, 'الحل: علبة على المقاس مع حشوة بتثبّته', y + 40)
if MODE != 'photo': card(img, GEN + 'img3.png', (90, y + 40, W - 90, 1220), 0.62)
footer(img, 2); slides.append(img)

# 3 — mistake 2 + photo
img = bg_img(GEN + 'img4.png', 0.5)
y = mistake_head(img, 2, 'تغليف بلا شعار', 'الزبون ما بيتذكر من وين اشترى.')
y = fix_box(img, 'الحل: شعارك على الغطا، ولو صغير', y + 40)
if MODE != 'photo': card(img, GEN + 'img4.png', (90, y + 40, W - 90, 1220), 0.5)
footer(img, 3); slides.append(img)

# 4 — mistake 3, illustration
img = bg_img(GEN + 'img5_bag.png', 0.5)
y = mistake_head(img, 3, 'كيس رقيق لمنتج تقيل', 'أول تجربة سيئة بتضل بذاكرة الزبون.')
y = fix_box(img, 'الحل: اختار الكيس حسب وزن المنتج', y + 40)
if MODE != 'photo': card(img, GEN + 'img5_bag.png', (90, y + 40, W - 90, 1220), 0.5)
footer(img, 4); slides.append(img)

# 5 — mistake 4, swatches
img = bg_img(GEN + 'img6_set.png', 0.45)
y = mistake_head(img, 4, 'ألوان مش ألوانك', 'التغليف لازم يكمّل هوية محلك.')
y = fix_box(img, 'الحل: نفس ألوان براندك على كل قطعة', y + 40)
if MODE != 'photo': card(img, GEN + 'img6_set.png', (90, y + 40, W - 90, 1220), 0.45)
footer(img, 5); slides.append(img)

# 6 — mistake 5, two boxes
img = bg_img(GEN + 'img7_gift.png', 0.62)
y = mistake_head(img, 5, 'نفس العلبة للهدية واليومي', 'كل استعمال إله تغليف مختلف.')
y = fix_box(img, 'الحل: هدية بلحظة فتح، ويومي عملي', y + 40)
if MODE != 'photo': card(img, GEN + 'img7_gift.png', (90, y + 40, W - 90, 1220), 0.62)
footer(img, 6); slides.append(img)

# 7 — CTA, plum closing slide
img = Image.new('RGB', (W, H), PLUM)
d = ImageDraw.Draw(img)
lw = 380; lh = round(lw * LOGO.height / LOGO.width); pad = 26
x = (W - lw) // 2
d.rounded_rectangle([x - pad, 150 - pad, x + lw + pad, 150 + lh + pad], radius=26, fill=IVORY)
img.paste(LOGO.resize((lw, lh), Image.LANCZOS), (x, 150))
ctext(img, 'بدك تغليف', F(XB, 100), 470, IVORY)
ctext(img, 'بلا ولا غلط؟', F(XB, 100), 600, GOLD)
ctext(img, 'ابعتلنا نوع التغليف والمقاس والكمية', F(MD, 40), 740, (236, 205, 210))
ctext(img, 'وشعارك أو فكرة التصميم', F(MD, 40), 800, (236, 205, 210))
f = F(SB, 48); bb, tw, th = tsize(d, 'راسلنا على واتساب', f)
pw, ph = tw + 130, th + 52; x0 = (W - pw) // 2; y0 = 920
d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=ph // 2, fill=GOLD)
d.text((x0 + 65 - bb[0], y0 + 26 - bb[1]), 'راسلنا على واتساب', font=f, fill=PLUM_D, direction='rtl', language='ar')
ctext(img, 'أقل طلب 500 قطعة', F(SB, 40), 1110, IVORY)
slides.append(img)

for i, s in enumerate(slides, 1): s.save(f'{OUT}/slide{i}.jpg', quality=94)
sheet = Image.new('RGB', (7 * 236 + 60, 295), 'white')
for i, s in enumerate(slides): sheet.paste(s.resize((236, 295)), (i * 246, 0))
sheet.save(f'{OUT}/sheet.png')
