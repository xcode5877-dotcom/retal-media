from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
PLUM=(78,30,92); PLUM_D=(46,14,58); GOLD=(196,160,96); GOLD_D=(160,120,60); IVORY=(247,241,219); MUTED=(112,86,110); BLUSH=(236,205,210)
FD='/home/claude/retal/fonts/'; L=ImageFont.Layout.RAQM
def F(n,s): return ImageFont.truetype(FD+n,s,layout_engine=L)
XB,SB,MD='Alexandria-ExtraBold.ttf','Alexandria-SemiBold.ttf','Alexandria-Medium.ttf'
LOGO=Image.open('/home/claude/retal/logo.png').convert('RGB')
SRC=Image.open('/home/claude/retal/w46/card.jpg').convert('RGB')  # 1136x1408
RX=W-80
def crop(box, size):
    im=SRC.crop(box); k=max(size[0]/im.width,size[1]/im.height)
    im=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
    x=(im.width-size[0])//2; y=(im.height-size[1])//2; return im.crop((x,y,x+size[0],y+size[1]))
def tb(d,s,f): bb=d.textbbox((0,0),s,font=f,direction='rtl',language='ar'); return bb,bb[2]-bb[0],bb[3]-bb[1]
def rt(img,s,f,top,c,right=RX):
    d=ImageDraw.Draw(img); bb,tw,th=tb(d,s,f); d.text((right-tw-bb[0],top-bb[1]),s,font=f,fill=c,direction='rtl',language='ar'); return top+th
def ct(img,s,f,cy,c):
    d=ImageDraw.Draw(img); bb,tw,th=tb(d,s,f); d.text(((W-tw)/2-bb[0],cy-th/2-bb[1]),s,font=f,fill=c,direction='rtl',language='ar')
def rounded(img, ph, xy, r=36):
    m=Image.new('L',ph.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,ph.width-1,ph.height-1],radius=r,fill=255); img.paste(ph,xy,m)
def dots(img,k):
    d=ImageDraw.Draw(img); x=W//2+3*22
    for i in range(4):
        cx=W//2+(1.5-i)*44; c=PLUM if i==k-1 else (210,195,205)
        d.ellipse([cx-9,H-70-9,cx+9,H-70+9],fill=c)
def concept(img):
    d=ImageDraw.Draw(img); f=F(MD,22); s='تصور إبداعي للتغليف'; bb,tw,th=tb(d,s,f); d.text((80-bb[0],H-80-th-bb[1]),s,font=f,fill=MUTED,direction='rtl',language='ar')

slides=[]
# cover: photo full, plum veil bottom, title
img=crop((0,0,1136,1408),(W,H))
veil=Image.new('RGB',(W,H),PLUM_D); m=Image.new('L',(1,H))
for y in range(H): m.putpixel((0,y),int(255*0.95*max(0,min(1,(y-600)/380))**1.2))
img.paste(veil,(0,0),m.resize((W,H)))
d=ImageDraw.Draw(img)
f=F(SB,34); s='قبل ما تطبع'; bb,tw,th=tb(d,s,f); pw,ph=tw+56,th+28
d.rounded_rectangle([RX-pw,880,RX,880+ph],radius=ph//2,fill=GOLD); d.text((RX-pw+28-bb[0],894-bb[1]),s,font=f,fill=PLUM_D,direction='rtl',language='ar')
y=rt(img,'كروت البيزنس',F(XB,108),880+ph+28,IVORY)
y=rt(img,'4 أشياء انتبهلها',F(XB,80),y+22,GOLD)
f=F(SB,32); s='اسحب ←'; bb,tw,th=tb(d,s,f)
d.rounded_rectangle([80,1230,80+tw+60,1230+th+28],radius=(th+28)//2,outline=IVORY,width=2)
d.text((110-bb[0],1244-bb[1]),s,font=f,fill=IVORY,direction='rtl',language='ar')
lw=170; lh=round(lw*LOGO.height/LOGO.width); d.rounded_rectangle([66,66,80+lw+14,80+lh+14],radius=16,fill=IVORY); img.paste(LOGO.resize((lw,lh),Image.LANCZOS),(80,80))
slides.append(img)

TIPS=[
 ('خلّيه بسيط', ['اسمك، شعارك، رقمك،','وطريقة يوصلك فيها الزبون.','كل ما قلّ الكلام، بيبيّن أرتب.'], (300,380,860,900)),
 ('ورق سميك', ['الكرت الرقيق بيبيّن رخيص','وبينطوى بالجزدان.','السماكة بتحكي عن جودة محلك.'], (230,560,900,1060)),
 ('نفس ألوان براندك', ['نفس ألوان علبتك وكيسك،','عشان الزبون يربط بينهم','من أول نظرة.'], (0,600,560,1300)),
 ('تفصيلة بتفرق', ['وجه خلفي بلون براندك','أو تصميم مختلف عن العادي.','تفصيلة صغيرة بتخلّي الكرت ينحفظ.'], (620,700,1136,1408)),
]
for k,(title,lines,box) in enumerate(TIPS,1):
    img=Image.new('RGB',(W,H),IVORY); d=ImageDraw.Draw(img)
    rounded(img,crop(box,(W-160,560)),(80,80))
    # number
    f=F(XB,150); s=f'0{k}'; bb=d.textbbox((0,0),s,font=f)
    d.text((80-bb[0],690-bb[1]),s,font=f,fill=IVORY,stroke_width=3,stroke_fill=GOLD_D)
    fs=84
    while tb(d,title,F(XB,fs))[1] > W-160-300: fs-=4
    y=rt(img,title,F(XB,fs),700+(84-fs)//2,PLUM)
    d.rectangle([RX-110,y+28,RX,y+34],fill=GOLD)
    y+=70
    for ln in lines: y=rt(img,ln,F(MD,42),y,MUTED)+22
    dots(img,k); concept(img); slides.append(img)
# CTA
img=Image.new('RGB',(W,H),PLUM); d=ImageDraw.Draw(img)
g=Image.new('L',(1,H))
for yy in range(H): g.putpixel((0,yy),int(255*(yy/H)**1.2))
img.paste(Image.new('RGB',(W,H),PLUM_D),(0,0),g.resize((W,H)))
lw=340; lh=round(lw*LOGO.height/LOGO.width); x=(W-lw)//2
d.rounded_rectangle([x-24,170-24,x+lw+24,170+lh+24],radius=24,fill=IVORY); img.paste(LOGO.resize((lw,lh),Image.LANCZOS),(x,170))
ct(img,'كروت بيزنس',F(XB,100),480,IVORY)
ct(img,'بنفس هوية تغليفك',F(XB,80),600,GOLD)
ct(img,'ابعتلنا شعارك والكمية،',F(MD,42),730,BLUSH)
ct(img,'ومنحكي معك على كل التفاصيل.',F(MD,42),795,BLUSH)
f=F(SB,48); s='راسلنا على واتساب'; bb,tw,th=tb(d,s,f); pw,ph=tw+130,th+52; x0=(W-pw)//2; y0=910
d.rounded_rectangle([x0,y0,x0+pw,y0+ph],radius=ph//2,fill=GOLD); d.text((x0+65-bb[0],y0+26-bb[1]),s,font=f,fill=PLUM_D,direction='rtl',language='ar')
ct(img,'أقل طلب 500 قطعة',F(SB,40),1100,IVORY)
slides.append(img)
import os; os.makedirs('out',exist_ok=True)
for i,s in enumerate(slides,1): s.save(f'out/slide{i}.jpg',quality=94)
sh=Image.new('RGB',(6*250+50,312),'white')
for i,s in enumerate(slides): sh.paste(s.resize((250,312)),(i*260,0))
sh.save('out/sheet.png')
