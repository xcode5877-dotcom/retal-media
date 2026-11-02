from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
PLUM = (78, 30, 92); PLUM_D = (46, 14, 58); GOLD = (196, 160, 96); GOLD_D = (160, 120, 60)
IVORY = (247, 241, 219); MUTED = (112, 86, 110); BLUSH = (236, 205, 210)
FD = '/home/claude/retal/fonts/'; L = ImageFont.Layout.RAQM
def F(n, s): return ImageFont.truetype(FD + n, s, layout_engine=L)
XB, SB, MD = 'Alexandria-ExtraBold.ttf', 'Alexandria-SemiBold.ttf', 'Alexandria-Medium.ttf'
LOGO = Image.open('/home/claude/retal/logo.png').convert('RGB')
HERE = '/home/claude/retal/types/'
RX = W - 80

def photo(n):
    im = Image.open(f'{HERE}t{n}.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
    # soften the top so text sits on clean ivory
    veil = Image.new('RGB', (W, H), (246, 240, 228)); m = Image.new('L', (1, H))
    for y in range(H): m.putpixel((0, y), int(255 * 0.75 * max(0, min(1, (560 - y) / 300)) ** 1.1))
    im.paste(veil, (0, 0), m.resize((W, H))); return im

def tb(d, s, f):
    bb = d.textbbox((0, 0), s, font=f, direction='rtl', language='ar'); return bb, bb[2] - bb[0], bb[3] - bb[1]
def rt(img, s, f, top, c, right=RX):
    d = ImageDraw.Draw(img); bb, tw, th = tb(d, s, f)
    d.text((right - tw - bb[0], top - bb[1]), s, font=f, fill=c, direction='rtl', language='ar'); return top + th
def ct(img, s, f, cy, c):
    d = ImageDraw.Draw(img); bb, tw, th = tb(d, s, f)
    d.text(((W - tw) / 2 - bb[0], cy - th / 2 - bb[1]), s, font=f, fill=c, direction='rtl', language='ar')
def chips(img, items, top, right=RX):
    d = ImageDraw.Draw(img); f = F(SB, 30); x = right
    for s in items:
        bb, tw, th = tb(d, s, f); pw, ph = tw + 44, th + 26
        d.rounded_rectangle([x - pw, top, x, top + ph], radius=ph // 2, fill=PLUM)
        d.text((x - pw + 22 - bb[0], top + 13 - bb[1]), s, font=f, fill=IVORY, direction='rtl', language='ar')
        x -= pw + 14
def counter(img, k):
    d = ImageDraw.Draw(img); f = F(XB, 34); s = f'0{k} / 05'; bb = d.textbbox((0, 0), s, font=f)
    d.text((80 - bb[0], 80 - bb[1]), s, font=f, fill=GOLD_D)
def concept(img, c=MUTED):
    d = ImageDraw.Draw(img); f = F(MD, 22); s = 'تصور إبداعي للتغليف'; bb, tw, th = tb(d, s, f)
    d.text((80 - bb[0], H - 50 - th - bb[1]), s, font=f, fill=c, direction='rtl', language='ar')

TYPES = [
    ('علبة مغناطيس', 'فخمة، وبتنفتح بلحظة حلوة', ['هدايا', 'عطور', 'مجوهرات']),
    ('علبة شحن', 'قوية للطريق، وحلوة من جوّا', ['بيع أونلاين', 'توصيل', 'اشتراكات']),
    ('علبة أنبوب', 'شكلها مميز وبتلفت على الرف', ['شاي وقهوة', 'شموع', 'عطور']),
    ('علبة طي', 'خفيفة وعملية وسعرها مريح', ['كوزمتكس', 'عناية بالبشرة', 'منتجات صغيرة']),
    ('كيس ورق', 'إعلان ماشي بالشارع', ['ملابس', 'بوتيكات', 'حلويات']),
]
slides = []
# cover: ivory + five vertical strips of the five types
img = Image.new('RGB', (W, H), (246, 240, 228))
d = ImageDraw.Draw(img)
sw, gap, top = 176, 12, 620
x = W - 80
for k in range(1, 6):
    im = Image.open(f'{HERE}t{k}.jpg').convert('RGB')
    im = im.resize((int(im.width * (H - top - 90) / im.height), H - top - 90), Image.LANCZOS)
    cx = im.width // 2; strip = im.crop((cx - sw // 2, 0, cx + sw // 2, im.height))
    m = Image.new('L', strip.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, sw - 1, strip.height - 1], radius=26, fill=255)
    img.paste(strip, (x - sw, top), m); x -= sw + gap
lw = 190; lh = round(lw * LOGO.height / LOGO.width)
img.paste(LOGO.resize((lw, lh), Image.LANCZOS), (80, 76))
y = rt(img, '5 أنواع علب', F(XB, 108), 120, PLUM)
y = rt(img, 'أي وحدة لمنتجك؟', F(XB, 76), y + 30, GOLD_D)
f = F(SB, 32); s = 'اسحب ←'; bb, tw, th = tb(d, s, f)
d.rounded_rectangle([RX - tw - 60, y + 40, RX, y + 40 + th + 28], radius=(th + 28) // 2, fill=PLUM)
d.text((RX - tw - 30 - bb[0], y + 54 - bb[1]), s, font=f, fill=IVORY, direction='rtl', language='ar')
concept(img, MUTED); slides.append(img)
# types
for k, (name, line, use) in enumerate(TYPES, 1):
    img = photo(k)
    counter(img, k)
    y = rt(img, name, F(XB, 96), 70, PLUM)
    y = rt(img, line, F(MD, 42), y + 26, MUTED)
    y = rt(img, 'مناسبة لـ:', F(SB, 30), y + 34, GOLD_D)
    chips(img, use, y + 14)
    concept(img, MUTED); slides.append(img)
# CTA
img = Image.new('RGB', (W, H), PLUM); d = ImageDraw.Draw(img)
g = Image.new('L', (1, H))
for yy in range(H): g.putpixel((0, yy), int(255 * (yy / H) ** 1.2))
img.paste(Image.new('RGB', (W, H), PLUM_D), (0, 0), g.resize((W, H)))
lw = 360; lh = round(lw * LOGO.height / LOGO.width); x = (W - lw) // 2
d.rounded_rectangle([x - 26, 150 - 26, x + lw + 26, 150 + lh + 26], radius=26, fill=IVORY)
img.paste(LOGO.resize((lw, lh), Image.LANCZOS), (x, 150))
ct(img, 'مش متأكد', F(XB, 96), 470, IVORY)
ct(img, 'أي نوع بيناسبك؟', F(XB, 84), 590, GOLD)
ct(img, 'احكيلنا شو بتبيع، ومنساعدك تختار', F(MD, 40), 720, BLUSH)
ct(img, 'النوع والمقاس والتصميم', F(MD, 40), 780, BLUSH)
f = F(SB, 48); s = 'راسلنا على واتساب'; bb, tw, th = tb(d, s, f)
pw, ph = tw + 130, th + 52; x0 = (W - pw) // 2; y0 = 900
d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=ph // 2, fill=GOLD)
d.text((x0 + 65 - bb[0], y0 + 26 - bb[1]), s, font=f, fill=PLUM_D, direction='rtl', language='ar')
ct(img, 'أقل طلب 500 قطعة', F(SB, 40), 1090, IVORY)
slides.append(img)

import os; os.makedirs(HERE + 'out', exist_ok=True)
for i, s in enumerate(slides, 1): s.save(f'{HERE}out/slide{i}.jpg', quality=94)
sheet = Image.new('RGB', (7 * 236 + 60, 295), 'white')
for i, s in enumerate(slides): sheet.paste(s.resize((236, 295)), (i * 246, 0))
sheet.save(HERE + 'out/sheet.png')
