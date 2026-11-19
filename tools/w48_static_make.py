# Week 47 static designs: Monday post, Thursday carousel, daily stories. Renders HTML via Playwright.
import os, asyncio
from playwright.async_api import async_playwright
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSS = f"""
@font-face{{font-family:AX;src:url(file://{R}/fonts/Alexandria-ExtraBold.ttf);font-weight:800}}
@font-face{{font-family:AX;src:url(file://{R}/fonts/Alexandria-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:AX;src:url(file://{R}/fonts/Alexandria-Medium.ttf);font-weight:500}}
*{{box-sizing:border-box}} html,body{{margin:0}}
.pg{{position:relative;overflow:hidden;font-family:AX;color:#FAF4E4;direction:rtl;
 background:radial-gradient(120% 80% at 50% 30%,#5c2670 0%,#4E1E5C 42%,#280C34 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(210,175,110,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(210,175,110,.06) 2px,transparent 2px);background-size:90px 90px}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.gold{{color:#D2AF6E}} .blush{{color:#ECCDD2}} .xb{{font-weight:800}} .sb{{font-weight:600}} .md{{font-weight:500}}
.plate{{position:absolute;left:50%;transform:translateX(-50%);background:#F7F1DB;border-radius:22px;padding:18px 24px}}
.plate img{{display:block}}
.pill{{position:absolute;left:50%;transform:translateX(-50%);background:#D2AF6E;color:#280C34;font-weight:600;border-radius:80px;white-space:nowrap}}
.box{{position:absolute;left:90px;right:90px;background:rgba(250,244,228,.08);border:3px solid rgba(210,175,110,.45);border-radius:40px;text-align:center}}
.num{{position:absolute;left:50%;transform:translateX(-50%);border-radius:50%;background:#D2AF6E;color:#280C34;display:flex;align-items:center;justify-content:center;font-weight:800}}
.ai{{position:absolute;font-weight:500;font-size:24px;color:#280C34;background:rgba(250,244,228,.85);padding:8px 18px;border-radius:30px}}
.ico{{position:absolute;left:50%;transform:translateX(-50%);color:#D2AF6E}}
.dots{{position:absolute;left:0;right:0;text-align:center;direction:ltr}}
.dots i{{display:inline-block;width:16px;height:16px;border-radius:50%;margin:0 8px;background:rgba(250,244,228,.25)}} .dots i.on{{background:#D2AF6E}}
"""
LOGO = f'file://{R}/logo.png'
ENV = '<svg viewBox="0 0 200 200" width="{s}" height="{s}"><rect x="25" y="55" width="150" height="100" rx="8" fill="currentColor" opacity=".18"/><rect x="25" y="55" width="150" height="100" rx="8" fill="none" stroke="currentColor" stroke-width="6"/><path d="M25 60 L100 112 L175 60" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round"/></svg>'

def page(w, h, body): return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="pg" style="width:{w}px;height:{h}px"><div class="grid"></div>{body}</div></body></html>'
def plate(top, w=300): return f'<div class="plate" style="top:{top}px"><img src="{LOGO}" style="width:{w}px"></div>'

# ===================== Week 48 (22–28 Nov 2026) =====================
G = lambda n: f'file://{R}/gen/w48/{n}.jpg'
AI = '<div class="ai" style="top:{t}px;left:{l}px">تصور إبداعي للتغليف</div>'
def ai(t=30, l=30): return AI.format(t=t, l=l)
def dots(i, n, top=1290): return f'<div class="dots" style="top:{top}px">' + ''.join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n)) + '</div>'
def lab(txt, top, left, gold=False):
    bg = '#D2AF6E;color:#280C34' if gold else 'rgba(40,12,52,.82);color:#FAF4E4'
    return f'<div style="position:absolute;top:{top}px;left:{left}px;transform:translateX(-50%);background:{bg};font-weight:600;font-size:36px;padding:12px 30px;border-radius:50px;white-space:nowrap">{txt}</div>'
def photo(src, top, h, pos='50% 50%'):
    return (f'<img src="{src}" style="position:absolute;top:{top}px;left:0;width:1080px;height:{h}px;object-fit:cover;object-position:{pos}">'
            f'<div style="position:absolute;top:{top+h-260}px;left:0;right:0;height:260px;background:linear-gradient(to bottom,rgba(40,12,52,0),#3a1547)"></div>'
            f'<div style="position:absolute;top:{top+h}px;left:0;right:0;bottom:0;background:linear-gradient(#3a1547,#280C34)"></div>')
def card(src, x, y, w, h, gold=False, pos='50% 50%'):
    b = 'border:6px solid #D2AF6E;' if gold else 'border:6px solid rgba(250,244,228,.25);'
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:34px;overflow:hidden;{b}box-shadow:0 24px 60px rgba(0,0,0,.45)"><img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}"></div>'

jobs = []
# ---------- SUN 22: comparison carousel (NOVA) ----------
D = 'posts/2026-11-22_carousel_same_bag/'; N = 5
jobs.append((D+'slide1.jpg', 1080, 1350, page(1080, 1350, f'''
<div class="c xb" style="top:70px;font-size:96px">نفس الكيس…</div>
<div class="c xb gold" style="top:195px;font-size:96px">انطباع مختلف</div>
{card(G('nova_plain'), 50, 360, 475, 700, pos='22% 50%')}
{card(G('nova'), 555, 360, 475, 700, True, pos='22% 50%')}
{lab('تغليف عادي', 1090, 287)}{lab('بهوية محلك', 1090, 792, True)}
<div class="c sb blush" style="top:1195px;font-size:38px">اسحب وشوف الفرق ←</div>
<div class="ai" style="top:1300px;left:30px;font-size:20px;padding:5px 14px">تصور إبداعي للتغليف</div>
{dots(0, N, 1305)}''')))
jobs.append((D+'slide2.jpg', 1080, 1350, page(1080, 1350, f'''
{photo(G('nova_plain'), 0, 960)}{ai()}
{lab('تغليف عادي', 860, 540)}
<div class="c xb" style="top:990px;font-size:80px">مرتب… بس ساكت</div>
<div class="c sb blush" style="top:1120px;font-size:44px;line-height:1.5">الزبون بياخد الطلب وبيمشي<br>وما بيعرف إنه منك</div>
{dots(1, N)}''')))
jobs.append((D+'slide3.jpg', 1080, 1350, page(1080, 1350, f'''
{photo(G('nova'), 0, 960)}{ai()}
{lab('بهوية محلك', 860, 540, True)}
<div class="c xb" style="top:990px;font-size:80px">نفس الكيس… <span class="gold">بيحكي</span></div>
<div class="c sb blush" style="top:1120px;font-size:44px;line-height:1.5">اسمك بيمشي بالشارع<br>مع كل طلب بيطلع من عندك</div>
{dots(2, N)}''')))
pts = [('الزبون بيحفظ اسمك', 'كل ما يشوف الكيس بيتذكر محلك'), ('صورة الطلب بتحكي عنك', 'لما ينزّلها على السوشال، شعارك فيها'), ('محلك بيبيّن أرتب', 'هوية وحدة على كل قطعة')]
rows = ''.join(f'''<div class="box" style="top:{380+k*285}px;height:245px;padding:0 40px;display:flex;align-items:center;text-align:right">
<div style="flex:none;width:120px;height:120px;border-radius:50%;background:#D2AF6E;color:#280C34;display:flex;align-items:center;justify-content:center;font-size:70px;font-weight:800;margin-left:40px">{k+1}</div>
<div><div class="xb" style="font-size:52px">{a}</div><div class="md blush" style="font-size:36px;margin-top:12px">{b}</div></div></div>''' for k, (a, b) in enumerate(pts))
jobs.append((D+'slide4.jpg', 1080, 1350, page(1080, 1350, f'''
<div class="c xb" style="top:120px;font-size:96px">شو <span class="gold">بيتغيّر؟</span></div>
{rows}{dots(3, N)}''')))
jobs.append((D+'slide5.jpg', 1080, 1350, page(1080, 1350, f'''
<div style="position:absolute;width:900px;height:900px;left:90px;top:80px;border-radius:50%;background:radial-gradient(circle,rgba(210,175,110,.3),rgba(210,175,110,0) 65%)"></div>
{plate(190, 380)}
<div class="c xb" style="top:470px;font-size:88px">خلّي كيسك</div>
<div class="c xb gold" style="top:590px;font-size:88px">يحكي اسم محلك</div>
<div class="c sb blush" style="top:740px;font-size:44px">أكياس وكراتين وعلب بشعارك وألوانك</div>
<div class="pill" style="top:880px;font-size:48px;padding:24px 64px">راسلنا على واتساب</div>
<div class="pill" style="top:1040px;font-size:38px;padding:16px 46px;background:#ECCDD2">أكياس وكراتين من 500 قطعة وفوق</div>
{dots(4, N)}''')))
# ---------- MON 23: product post (DANA) ----------
jobs.append(('posts/2026-11-23_sweets_box/post_sweets_box.jpg', 1080, 1350, page(1080, 1350, f'''
{photo(G('dana'), 0, 920, '50% 45%')}{ai()}
<div class="c xb" style="top:800px;font-size:90px">الحلو الطيب</div>
<div class="c xb gold" style="top:925px;font-size:90px">بستاهل علبة باسمك</div>
<div class="c sb blush" style="top:1065px;font-size:42px">علب وأكياس بهوية محلك للحلويات والهدايا</div>
<div class="pill" style="top:1150px;font-size:40px;padding:18px 52px">راسلنا على واتساب</div>
<div class="c md" style="top:1262px;font-size:32px;opacity:.9">أكياس وكراتين من 500 قطعة وفوق</div>''')))
# ---------- THU 26: style carousel ----------
D = 'posts/2026-11-26_carousel_styles/'; N = 5
jobs.append((D+'slide1.jpg', 1080, 1350, page(1080, 1350, f'''
<div class="c xb" style="top:80px;font-size:92px">ناعم، فخم،</div>
<div class="c xb gold" style="top:200px;font-size:92px">ولا طبيعي؟</div>
<div class="c sb blush" style="top:340px;font-size:44px">اختار ستايل تغليف بيشبه محلك</div>
{card(G('nova'), 40, 450, 320, 560, pos='25% 50%')}
{card(G('dana'), 380, 430, 320, 600, True, pos='40% 50%')}
{card(G('mira'), 720, 450, 320, 560, pos='45% 50%')}
{lab('طبيعي', 1060, 200)}{lab('فخم', 1060, 540, True)}{lab('ناعم', 1060, 880)}
<div class="c sb gold" style="top:1170px;font-size:38px">اسحب ←</div>
<div class="ai" style="top:1300px;left:30px;font-size:20px;padding:5px 14px">تصور إبداعي للتغليف</div>
{dots(0, N, 1305)}''')))
styles = [('mira', 'ناعم', 'ألوان فاتحة ولمسة ذهبية', 'للعناية والتجميل والإكسسوارات', '45% 50%'),
          ('dana', 'فخم', 'لون غامق وتفاصيل ذهبية', 'للحلويات والهدايا والعطور', '50% 45%'),
          ('nova', 'طبيعي', 'ورق كرافت وشعار بلون واحد', 'للكافيهات والمخابز والمنتجات الطبيعية', '35% 50%')]
for i, (img, name, d1, d2, pos) in enumerate(styles, 1):
    jobs.append((D+f'slide{i+1}.jpg', 1080, 1350, page(1080, 1350, f'''
{photo(G(img), 0, 900, pos)}{ai()}
<div class="pill" style="top:770px;font-size:46px;padding:14px 56px">ستايل {name}</div>
<div class="c xb" style="top:930px;font-size:70px">{d1}</div>
<div class="c sb blush" style="top:1060px;font-size:44px">{d2}</div>
<div class="c md gold" style="top:1160px;font-size:36px">بنطبعه بشعار محلك وألوانه</div>
{dots(i, N)}''')))
jobs.append((D+'slide5.jpg', 1080, 1350, page(1080, 1350, f'''
<div style="position:absolute;width:900px;height:900px;left:90px;top:80px;border-radius:50%;background:radial-gradient(circle,rgba(210,175,110,.3),rgba(210,175,110,0) 65%)"></div>
{plate(190, 380)}
<div class="c xb" style="top:470px;font-size:84px">شو الستايل اللي</div>
<div class="c xb gold" style="top:590px;font-size:84px">بيشبه محلك؟</div>
<div class="c sb blush" style="top:740px;font-size:44px">اكتبلنا بالتعليقات: ناعم، فخم، ولا طبيعي</div>
<div class="pill" style="top:880px;font-size:48px;padding:24px 64px">راسلنا على واتساب</div>
<div class="c md" style="top:1030px;font-size:40px;opacity:.9">أقل طلب 500 قطعة</div>
{dots(4, N)}''')))
# ---------- SAT 28: comparison post (MIRA) ----------
jobs.append(('posts/2026-11-28_compare_mira/post_compare_mira.jpg', 1080, 1350, page(1080, 1350, f'''
<div class="c xb" style="top:70px;font-size:94px">علبة بدون اسم…</div>
<div class="c xb gold" style="top:190px;font-size:94px">ولا علبة باسمك؟</div>
<div class="c md blush" style="top:320px;font-size:40px">نفس العلبة، بس الانطباع غير</div>
{card(G('mira_plain'), 50, 410, 475, 680, pos='40% 50%')}
{card(G('mira'), 555, 410, 475, 680, True, pos='40% 50%')}
{lab('بدون هوية', 1115, 287)}{lab('بهوية محلك', 1115, 792, True)}
<div class="pill" style="top:1200px;font-size:40px;padding:16px 50px">أقل طلب 500 قطعة · راسلنا على واتساب</div>
<div class="ai" style="top:30px;left:30px;font-size:20px;padding:5px 14px">تصور إبداعي للتغليف</div>''')))
# ---------- Stories ----------
def story(label, l1, l2, sub, extra='', l1s=110, l2s=110):
    return page(1080, 1920, f'''
<div style="position:absolute;width:1000px;height:1000px;left:40px;top:420px;border-radius:50%;background:radial-gradient(circle,rgba(210,175,110,.3),rgba(210,175,110,0) 65%)"></div>
{plate(170, 330)}
<div class="pill" style="top:420px;font-size:40px;padding:14px 44px;background:#ECCDD2">{label}</div>
{extra}
<div class="c xb" style="top:760px;font-size:{l1s}px;line-height:1.25">{l1}</div>
<div class="c xb gold" style="top:{760+int(l1s*1.25*(l1.count('<br>')+1))+20}px;font-size:{l2s}px;line-height:1.25">{l2}</div>
<div class="c sb blush" style="top:1420px;font-size:52px;line-height:1.5">{sub}</div>
<div class="c md" style="top:1760px;font-size:34px;opacity:.75">أقل طلب 500 قطعة · راسلنا على واتساب</div>''')
S = 'stories/w48/'
def istory(img, label, l1, l2, sub, pos='50% 50%'):
    return page(1080, 1920, f'''
<img src="{img}" style="position:absolute;top:0;left:0;width:1080px;height:1350px;object-fit:cover;object-position:{pos}">
<div style="position:absolute;top:1000px;left:0;right:0;height:350px;background:linear-gradient(to bottom,rgba(40,12,52,0),#3a1547)"></div>
<div style="position:absolute;top:1350px;left:0;right:0;bottom:0;background:linear-gradient(#3a1547,#280C34)"></div>
<div class="ai" style="top:40px;left:40px">تصور إبداعي للتغليف</div>
<div class="pill" style="top:1110px;font-size:40px;padding:14px 44px;background:#ECCDD2">{label}</div>
<div class="c xb" style="top:1240px;font-size:88px;white-space:nowrap">{l1}</div>
<div class="c xb gold" style="top:1360px;font-size:88px;white-space:nowrap">{l2}</div>
<div class="c sb blush" style="top:1520px;font-size:50px">{sub}</div>
<div class="c md" style="top:1760px;font-size:34px;opacity:.75">أقل طلب 500 قطعة · راسلنا على واتساب</div>''')
jobs.append((S+'d22.jpg', 1080, 1920, istory(G('nova'), 'منشور جديد', 'نفس الكيس…', 'انطباع مختلف', 'اسحب على المنشور وشوف الفرق', '30% 50%')))
jobs.append((S+'d23.jpg', 1080, 1920, istory(G('dana'), 'منشور جديد', 'الحلو الطيب', 'بستاهل علبة باسمك', 'شوف المنشور على الصفحة')))
jobs.append((S+'d24.jpg', 1080, 1920, story('ريل جديد', 'بلاك فرايدي', 'هالجمعة', 'طلباتك رح تكثر…<br>تغليفك جاهز؟', l1s=150, l2s=130)))
jobs.append((S+'d25.jpg', 1080, 1920, istory(G('mira'), 'ريل جديد', 'حط اسمك…', 'وشوف الفرق', 'الجواب بالريل الجديد', '45% 50%')))
jobs.append((S+'d26.jpg', 1080, 1920, story('منشور جديد', 'ناعم، فخم،', 'ولا طبيعي؟', 'اسحب على المنشور<br>واختار ستايل محلك', l1s=120, l2s=120)))
opts = [('ناعم', 'ألوان فاتحة ولمسة ذهبية'), ('فخم', 'لون غامق وتفاصيل ذهبية'), ('طبيعي', 'كرافت وشعار بلون واحد')]
rows = ''.join(f'<div style="position:absolute;top:{830+k*200}px;left:120px;right:120px;height:160px;border-radius:80px;background:rgba(250,244,228,.1);border:3px solid rgba(210,175,110,.5);display:flex;align-items:center;padding:0 24px"><span style="flex:none;display:inline-flex;width:110px;height:110px;border-radius:50%;background:#D2AF6E;color:#280C34;align-items:center;justify-content:center;font-weight:800;font-size:64px;margin-left:34px">{k+1}</span><span style="line-height:1.25"><span style="display:block;font-size:60px;font-weight:800">{a}</span><span style="display:block;font-size:34px;font-weight:500;color:#ECCDD2;margin-top:12px">{b}</span></span></div>' for k, (a, b) in enumerate(opts))
jobs.append((S+'q27.jpg', 1080, 1920, page(1080, 1920, f'''
{plate(150, 300)}
<div class="pill" style="top:380px;font-size:40px;padding:14px 44px;background:#ECCDD2">سؤال الجمعة</div>
<div class="c xb" style="top:520px;font-size:92px;line-height:1.3">أي ستايل تغليف<br><span class="gold">بيشبه محلك؟</span></div>
{rows}
<div class="c sb blush" style="top:1500px;font-size:54px">ردّ على الستوري بالرقم</div>
<div class="c md" style="top:1760px;font-size:34px;opacity:.75">أقل طلب 500 قطعة · راسلنا على واتساب</div>''')))
jobs.append((S+'d28.jpg', 1080, 1920, istory(G('mira'), 'منشور جديد', 'علبة بدون اسم…', 'ولا علبة باسمك؟', 'شوف المقارنة على الصفحة', '45% 50%')))
for d in ['posts/2026-11-22_carousel_same_bag', 'posts/2026-11-23_sweets_box', 'posts/2026-11-26_carousel_styles', 'posts/2026-11-28_compare_mira', 'stories/w48']:
    os.makedirs(os.path.join(R, d), exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for out, w, h, html in jobs:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            tmp = os.path.join(R, 'tools', '_tmp_w48.html'); open(tmp, 'w').write(html)
            await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(R, out), type='jpeg', quality=92); await pg.close()
        os.remove(tmp); await b.close()
asyncio.run(main())
