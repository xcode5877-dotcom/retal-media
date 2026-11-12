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

jobs = []
# ---------- Monday post 1080x1350 ----------
img = f'file://{R}/gen/w47/minibox.jpg'
jobs.append(('posts/2026-11-16_minibox/post_minibox.jpg', 1080, 1350, page(1080, 1350, f'''
<img src="{img}" style="position:absolute;top:0;left:0;width:1080px;height:900px;object-fit:cover;object-position:50% 40%">
<div style="position:absolute;top:640px;left:0;right:0;height:270px;background:linear-gradient(to bottom,rgba(40,12,52,0),#3a1547)"></div>
<div class="ai" style="top:30px;left:30px">تصور إبداعي للتغليف</div>
<div style="position:absolute;top:900px;left:0;right:0;bottom:0;background:linear-gradient(#3a1547,#280C34)"></div>
<div class="c xb" style="top:800px;font-size:92px">علب صغيرة <span class="gold">بشعارك</span></div>
<div class="c sb blush" style="top:940px;font-size:44px;line-height:1.5">للمجوهرات والإكسسوارات والعطور والحلويات<br>تفاصيل صغيرة بتعمل فرق كبير</div>
<div class="pill" style="top:1110px;font-size:42px;padding:20px 56px">راسلنا على واتساب</div>
<div class="c md" style="top:1230px;font-size:34px;opacity:.85">أقل طلب 500 قطعة</div>
''')))
# ---------- Thursday carousel 1080x1350 ----------
ideas = [('الفواتير والإيصالات', 'سلّم الفاتورة بمغلف بشعارك<br>بدل ورقة مطوية'),
         ('كروت الشكر', 'حطها بمغلف صغير جوّا الطلب<br>وشوف كيف بتفرق مع الزبون'),
         ('قسائم الهدايا', 'القسيمة بمغلف أنيق<br>بتصير هدية بحد ذاتها'),
         ('دعوات الافتتاح والمناسبات', 'أول انطباع عن مناسبتك<br>بيبدأ من المغلف'),
         ('الضمان وتعليمات الاستعمال', 'أوراق زبونك المهمة<br>بتضل مرتبة وما بتضيع')]
def dots(i, n=7): return '<div class="dots" style="top:1270px">' + ''.join(f'<i class="{"on" if k==i else ""}"></i>' for k in range(n)) + '</div>'
D = 'posts/2026-11-19_carousel_envelopes/'
jobs.append((D+'slide1.jpg', 1080, 1350, page(1080, 1350, f'''
<div style="position:absolute;width:900px;height:900px;left:90px;top:120px;border-radius:50%;background:radial-gradient(circle,rgba(210,175,110,.3),rgba(210,175,110,0) 65%)"></div>
<div class="ico" style="top:150px">{ENV.format(s=330)}</div>
<div class="c xb gold" style="top:500px;font-size:190px;line-height:1">5 أفكار</div>
<div class="c xb" style="top:720px;font-size:80px;line-height:1.35">تستعمل فيها<br>المغلفات بشعارك</div>
<div class="c md blush" style="top:1010px;font-size:40px">لمحلك أو مشروعك</div>
<div class="c sb gold" style="top:1150px;font-size:38px">اسحب ←</div>
{dots(0)}''')))
for i, (t, d) in enumerate(ideas, 1):
    fs = 76 if len(t) < 16 else 62
    jobs.append((D+f'slide{i+1}.jpg', 1080, 1350, page(1080, 1350, f'''
<div class="c sb blush" style="top:120px;font-size:38px">فكرة رقم</div>
<div class="num" style="top:190px;width:200px;height:200px;font-size:130px">{i}</div>
<div class="ico" style="top:430px;opacity:.9">{ENV.format(s=210)}</div>
<div class="c xb" style="top:680px;font-size:{fs}px">{t}</div>
<div class="box" style="top:850px;padding:46px 30px;font-size:46px;font-weight:600;line-height:1.55">{d}</div>
{dots(i)}''')))
jobs.append((D+'slide7.jpg', 1080, 1350, page(1080, 1350, f'''
<div style="position:absolute;width:900px;height:900px;left:90px;top:80px;border-radius:50%;background:radial-gradient(circle,rgba(210,175,110,.3),rgba(210,175,110,0) 65%)"></div>
{plate(200, 380)}
<div class="c xb" style="top:470px;font-size:84px">مغلفات <span class="gold">بشعارك</span></div>
<div class="c xb" style="top:590px;font-size:84px">وألوان محلك</div>
<div class="c sb blush" style="top:740px;font-size:44px">احفظ البوست، وابعتلنا لما تجهز</div>
<div class="pill" style="top:880px;font-size:48px;padding:24px 64px">راسلنا على واتساب</div>
<div class="c md" style="top:1030px;font-size:40px;opacity:.9">أقل طلب 500 قطعة</div>
{dots(6)}''')))
# ---------- Stories 1080x1920 ----------
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
S = 'stories/w47/'
jobs.append((S+'d16.jpg', 1080, 1920, page(1080, 1920, f'''
<img src="{img}" style="position:absolute;top:0;left:0;width:1080px;height:1350px;object-fit:cover">
<div style="position:absolute;top:1000px;left:0;right:0;height:350px;background:linear-gradient(to bottom,rgba(40,12,52,0),#3a1547)"></div>
<div style="position:absolute;top:1350px;left:0;right:0;bottom:0;background:linear-gradient(#3a1547,#280C34)"></div>
<div class="ai" style="top:40px;left:40px">تصور إبداعي للتغليف</div>
<div class="pill" style="top:1130px;font-size:40px;padding:14px 44px;background:#ECCDD2">منشور جديد</div>
<div class="c xb" style="top:1270px;font-size:92px;white-space:nowrap">علب صغيرة <span class="gold">بشعارك</span></div>
<div class="c sb blush" style="top:1440px;font-size:50px">شوف المنشور على الصفحة</div>
<div class="c md" style="top:1760px;font-size:34px;opacity:.75">أقل طلب 500 قطعة · راسلنا على واتساب</div>''')))
jobs.append((S+'d17.jpg', 1080, 1920, story('ريل جديد', 'هاد', 'ولا هاد؟', 'اختار تغليف محلك<br>واكتبلنا اختياراتك بالتعليقات', l1s=170, l2s=150)))
jobs.append((S+'d18.jpg', 1080, 1920, story('ريل جديد', 'طلبك وصل…', 'بس مين بيعرف<br>إنه منك؟', 'الجواب بالريل الجديد', l1s=120, l2s=100)))
jobs.append((S+'d19.jpg', 1080, 1920, story('منشور جديد', '5 أفكار', 'للمغلفات بشعارك', 'اسحب على المنشور<br>واحفظه لبعدين', extra=f'<div class="ico" style="top:540px">{ENV.format(s=200)}</div>', l1s=150, l2s=96)))
opts = ['كراتين', 'أكياس', 'كروت بيزنس', 'علب صغيرة', 'مغلفات']
rows = ''.join(f'<div style="position:absolute;top:{820+k*150}px;left:150px;right:150px;height:120px;border-radius:60px;background:rgba(250,244,228,.1);border:3px solid rgba(210,175,110,.5);display:flex;align-items:center;padding:0 20px;font-size:54px;font-weight:600"><span style="display:inline-flex;width:84px;height:84px;border-radius:50%;background:#D2AF6E;color:#280C34;align-items:center;justify-content:center;font-weight:800;margin-left:34px">{k+1}</span>{o}</div>' for k, o in enumerate(opts))
jobs.append((S+'q20.jpg', 1080, 1920, page(1080, 1920, f'''
{plate(150, 300)}
<div class="pill" style="top:380px;font-size:40px;padding:14px 44px;background:#ECCDD2">سؤال الجمعة</div>
<div class="c xb" style="top:520px;font-size:92px;line-height:1.3">شو أكثر إشي<br><span class="gold">ناقص محلك؟</span></div>
{rows}
<div class="c sb blush" style="top:1600px;font-size:54px">ردّ على الستوري بالرقم</div>
<div class="c md" style="top:1760px;font-size:34px;opacity:.75">أقل طلب 500 قطعة · راسلنا على واتساب</div>''')))
jobs.append((S+'d20.jpg', 1080, 1920, story('بكرا على الصفحة', 'قبل موسم العروض', 'جهّز تغليفك<br>بـ3 خطوات', 'ريل جديد بكرا الساعة 8 المسا', l1s=96, l2s=110)))
jobs.append((S+'d21.jpg', 1080, 1920, story('ريل جديد', 'موسم العروض جاي', '3 خطوات<br>لتغليفك', 'شوف الريل واحفظه', l1s=100, l2s=120)))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for out, w, h, html in jobs:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            tmp = os.path.join(R, 'tools', '_tmp_w47.html'); open(tmp, 'w').write(html)
            await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(R, out), type='jpeg', quality=92); await pg.close()
        os.remove(tmp); await b.close()
asyncio.run(main())
