import sys
src=open('more_products.html').read()
head=src[:src.index('<div id="stage">')]
head=head.replace("@font-face{font-family:AX;src:url(/home/claude/retal/fonts/Alexandria-ExtraBold.ttf);font-weight:800}",
 "@font-face{font-family:AX;src:url(/home/claude/retal/fonts/Alexandria-ExtraBold.ttf);font-weight:800}\n@font-face{font-family:HB;src:url(/home/claude/retal/fonts/Heebo-VF.ttf);font-weight:100 900}")
head=head.replace('</style>','#A .shade,#B .shade,#C .shade{background:linear-gradient(to bottom,rgba(40,12,52,.9) 0%,rgba(40,12,52,.55) 24%,rgba(40,12,52,0) 42%,rgba(40,12,52,0) 55%,rgba(40,12,52,.92) 80%,rgba(40,12,52,.97) 100%)}\n#B .photo img{object-position:62% 50%}\n.he #stage{font-family:HB}\n.he .xb{font-weight:900}.he .sb{font-weight:700}.he .md{font-weight:500}\n</style>')
T={
'ar':dict(lang='ar',cls='',q1=['ليش','زبونك'],q1b=['بيرمي','الكيس','فوراً؟'],q2=['لأنه','ما','فيه','إشي','بيستاهل','يحتفظ','فيه'],
  b1=['خلّي','كيسك'],b2=['يستاهل'],k1='بشعارك',k2='بألوانك',k3=['بتصميم','بينحفظ'],c1=['ونفس','الإشي'],c2=['لكرتونتك'],
  e1=['كراتين','وأكياس'],e2=['بهوية','محلك'],pill='راسلنا على واتساب',e3='أقل طلب 500 قطعة',tag='تصور إبداعي للتغليف'),
'he':dict(lang='he',cls='he',q1=['למה','הלקוח'],q1b=['זורק','את','השקית?'],q2=['כי','אין','בה','שום','סיבה','לשמור','אותה'],
  b1=['תן','לשקית'],b2=['סיבה','להישאר'],k1='עם הלוגו שלך',k2='בצבעים שלך',k3=['בעיצוב','שזוכרים'],c1=['וגם'],c2=['הקרטון','שלך'],
  e1=['שקיות','וקרטונים'],e2=['בזהות','של','העסק'],pill='שלחו הודעה בוואטסאפ',e3='מינימום הזמנה 500 יחידות',tag='הדמיה להמחשה בלבד'),
}
def W(ws): return ' '.join(f'<span class="w">{w}</span>' for w in ws)
for k,t in T.items():
    body=f'''<div id="stage"><div id="cam">
  <div class="layer" id="A"><div class="photo"><img src="/home/claude/retal/w46/bag.jpg"></div><div class="shade"></div></div>
  <div class="layer" id="B" style="visibility:hidden"><div class="photo"><img src="/home/claude/retal/types/t5.jpg"></div><div class="shade"></div><div class="streak"></div><div class="tag">{t['tag']}</div></div>
  <div class="layer" id="C" style="visibility:hidden"><div class="photo"><img src="/home/claude/retal/w46/unbox.jpg"></div><div class="shade"></div><div class="streak"></div><div class="tag">{t['tag']}</div></div>
  <div class="line xb" id="q1" style="top:200px;font-size:120px">{W(t['q1'])}</div>
  <div class="line xb gold" id="q1b" style="top:370px;font-size:104px">{W(t['q1b'])}</div>
  <div class="line md blush" id="q2" style="top:1500px;font-size:54px">{W(t['q2'])}</div>
  <div class="line xb" id="b1" style="top:230px;font-size:120px;visibility:hidden">{W(t['b1'])}</div>
  <div class="line xb gold" id="b2" style="top:370px;font-size:120px;visibility:hidden">{W(t['b2'])}</div>
  <div class="line xb" id="k1" style="top:1450px;font-size:120px;visibility:hidden"><span class="w">{t['k1']}</span></div>
  <div class="line xb gold" id="k2" style="top:1450px;font-size:120px;visibility:hidden"><span class="w">{t['k2']}</span></div>
  <div class="line xb" id="k3" style="top:1460px;font-size:110px;visibility:hidden">{W(t['k3'])}</div>
  <div class="line xb" id="c1" style="top:230px;font-size:110px;visibility:hidden">{W(t['c1'])}</div>
  <div class="line xb gold" id="c2" style="top:370px;font-size:110px;visibility:hidden">{W(t['c2'])}</div>
  <div class="layer" id="end" style="visibility:hidden">
    <div class="glow" style="top:200px"></div>
    <div class="plate" id="plate"><img src="/home/claude/retal/logo.png"></div>
    <div class="line xb" id="e1" style="top:760px;font-size:100px">{W(t['e1'])}</div>
    <div class="line xb gold" id="e2" style="top:890px;font-size:100px">{W(t['e2'])}</div>
    <div class="pill" id="pill">{t['pill']}</div>
    <div class="line md blush" id="e3" style="top:1330px;font-size:50px">{t['e3']}</div>
  </div>
  <div id="flash"></div>
</div>
<div id="progbg"></div><div id="prog"></div>
</div>'''
    js=open('hook_tl.js').read()
    html=head.replace('<html lang="ar" dir="rtl">',f'<html lang="{t["lang"]}" dir="rtl" class="{t["cls"]}">')+body+'\n<script src="/home/claude/retal/motion/node_modules/gsap/dist/gsap.min.js"></script>\n<script>'+js+'</script></body></html>'
    open(f'hook_{k}.html','w').write(html)
