from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
PLUM=(78,30,92);PLUM_D=(40,12,52);GOLD=(210,175,110);IVORY=(250,244,228);BLUSH=(236,205,210)
FD='/home/claude/retal/fonts/';L=ImageFont.Layout.RAQM
def F(n,s): return ImageFont.truetype(FD+n,s,layout_engine=L)
XB,SB,MD='Alexandria-ExtraBold.ttf','Alexandria-SemiBold.ttf','Alexandria-Medium.ttf'
LOGO=Image.open('/home/claude/retal/logo.png').convert('RGB')
img=Image.new('RGB',(W,H),PLUM); g=Image.new('L',(1,H))
for y in range(H): g.putpixel((0,y),int(255*(y/H)**1.2))
img.paste(Image.new('RGB',(W,H),PLUM_D),(0,0),g.resize((W,H)))
d=ImageDraw.Draw(img,'RGBA')
for r in (260,330,400): d.arc([W-r,-r,W+r,r],90,180,fill=GOLD+(50,),width=2)
def tb(s,f): bb=d.textbbox((0,0),s,font=f,direction='rtl',language='ar'); return bb,bb[2]-bb[0],bb[3]-bb[1]
def rt(s,f,top,c,right=W-80):
    bb,tw,th=tb(s,f); d.text((right-tw-bb[0],top-bb[1]),s,font=f,fill=c,direction='rtl',language='ar'); return top+th
lw=170; lh=round(lw*LOGO.height/LOGO.width); d.rounded_rectangle([66,66,80+lw+14,80+lh+14],radius=16,fill=IVORY); img.paste(LOGO.resize((lw,lh),Image.LANCZOS),(80,80))
y=rt('كيف بتطلب',F(XB,100),90,IVORY)
y=rt('من ريتال؟',F(XB,100),y+20,GOLD)
STEPS=[('ابعتلنا على واتساب','نوع التغليف والمقاس والكمية'),
       ('ابعت شعارك','أو فكرة التصميم اللي ببالك'),
       ('منحكي معك على التفاصيل','الخامة والألوان والسعر'),
       ('منطبع طلبك','بشعارك وألوانك، من 500 قطعة')]
top=y+80; step=200; cx=W-80-50
d.line([(cx,top+50),(cx,top+50+step*3)],fill=GOLD+(120,),width=4)
for i,(a,b) in enumerate(STEPS):
    cy=top+50+i*step
    d.ellipse([cx-50,cy-50,cx+50,cy+50],fill=GOLD)
    f=F(XB,56); s=str(i+1); bb=d.textbbox((0,0),s,font=f); d.text((cx-(bb[2]-bb[0])/2-bb[0],cy-(bb[3]-bb[1])/2-bb[1]),s,font=f,fill=PLUM_D)
    yy=rt(a,F(XB,56),cy-52,IVORY,right=cx-80)
    rt(b,F(MD,38),yy+16,BLUSH,right=cx-80)
f=F(SB,46); s='راسلنا على واتساب'; bb,tw,th=tb(s,f); pw,ph=tw+120,th+46; x0=(W-pw)//2; y0=H-150
d.rounded_rectangle([x0,y0,x0+pw,y0+ph],radius=ph//2,fill=GOLD); d.text((x0+60-bb[0],y0+23-bb[1]),s,font=f,fill=PLUM_D,direction='rtl',language='ar')
img.save('post_steps.jpg',quality=94); img.resize((540,675)).save('p.jpg')
