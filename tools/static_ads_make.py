from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob
W,H=1080,1350
PLUM=(78,30,92);PLUM_D=(46,14,58);GOLD=(196,160,96);GOLD_D=(160,120,60);IVORY=(247,241,219);MUTED=(110,82,110)
L=ImageFont.Layout.RAQM
def F(lang,weight,size):
    if lang=='ar':
        n={'xb':'Alexandria-ExtraBold.ttf','sb':'Alexandria-SemiBold.ttf','md':'Alexandria-Medium.ttf'}[weight]
        return ImageFont.truetype('/home/claude/retal/fonts/'+n,size,layout_engine=L)
    f=ImageFont.truetype('/home/claude/retal/fonts/Heebo-VF.ttf',size,layout_engine=L)
    f.set_variation_by_name({'xb':'Black','sb':'Bold','md':'Medium'}[weight]); return f
LOGO=Image.open('/home/claude/retal/logo.png').convert('RGB')
UP=glob.glob('/root/.claude/uploads/*/')[0]
def cover(im,w,h,fx=0.5,fy=0.5):
    k=max(w/im.width,h/im.height); im=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def tb(d,s,f,lang): bb=d.textbbox((0,0),s,font=f,direction='rtl',language=lang); return bb,bb[2]-bb[0],bb[3]-bb[1]
def ct(img,s,f,cy,c,lang,cx=W//2):
    d=ImageDraw.Draw(img); bb,tw,th=tb(d,s,f,lang); d.text((cx-tw/2-bb[0],cy-th/2-bb[1]),s,font=f,fill=c,direction='rtl',language=lang)
def pill(img,s,f,cy,lang,fg=IVORY,bg=PLUM,cx=W//2,padx=44,pady=22):
    d=ImageDraw.Draw(img); bb,tw,th=tb(d,s,f,lang); pw,ph=tw+2*padx,th+2*pady; x0=int(cx-pw/2); y0=int(cy-ph/2)
    d.rounded_rectangle([x0,y0,x0+pw,y0+ph],radius=ph//2,fill=bg); d.text((x0+padx-bb[0],y0+pady-bb[1]),s,font=f,fill=fg,direction='rtl',language=lang)
def logo(img,x,y,w=150):
    h=round(w*LOGO.height/LOGO.width); p=12
    ImageDraw.Draw(img).rounded_rectangle([x-p,y-p,x+w+p,y+h+p],radius=14,fill=IVORY); img.paste(LOGO.resize((w,h),Image.LANCZOS),(x,y))
def bg():
    img=Image.new('RGB',(W,H),(244,232,226)); g=Image.new('L',(1,H))
    for y in range(H): g.putpixel((0,y),int(255*(y/H)))
    img.paste(Image.new('RGB',(W,H),(233,211,214)),(0,0),g.resize((W,H))); return img

T={'ar':dict(h1='نفس الكرتونة...',h2='انطباع مختلف',sub='التغليف جزء من هوية محلك',l1='كرتونة عادية',l2='كرتونة بهوية محلك',
             offer='أكياس وكراتين من 500 قطعة وفوق',tag='تصور إبداعي للتغليف',
             b1='كيس وعلبة',b2='بيحكوا عن براندك',bsub='بشعارك وألوانك على كل قطعة',cta='راسلنا على واتساب'),
   'he':dict(h1='אותו קרטון...',h2='רושם אחר',sub='האריזה היא חלק מהזהות של העסק',l1='קרטון רגיל',l2='קרטון בזהות של העסק',
             offer='שקיות וקרטונים מ-500 יחידות',tag='הדמיה להמחשה בלבד',
             b1='שקית וקופסה',b2='שמספרות על המותג',bsub='עם הלוגו והצבעים שלך על כל פריט',cta='שלחו הודעה בוואטסאפ')}
A=Image.open('/home/claude/retal/nov/wed_start.jpg').convert('RGB')
B=Image.open('/home/claude/retal/nov/wed_end.jpg').convert('RGB')
for lang,t in T.items():
    # ---- AD 1: comparison
    img=bg()
    ct(img,t['h1'],F(lang,'xb',92),150,PLUM,lang)
    ct(img,t['h2'],F(lang,'xb',92),270,PLUM,lang)
    ct(img,t['sub'],F(lang,'md',40),370,MUTED,lang)
    cw,ch=470,640; top=440; gap=40; xR=W//2+gap//2; xL=W//2-gap//2-cw
    for im,x,lab,dark in ((B,xR,t['l2'],True),(A,xL,t['l1'],False)):   # RTL: branded on the right
        ph=cover(im,cw,ch,0.5,0.55); m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).rounded_rectangle([0,0,cw-1,ch-1],radius=30,fill=255)
        sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).rounded_rectangle([x,top+14,x+cw,top+ch+14],radius=30,fill=110)
        img.paste(Image.new('RGB',(W,H),(120,80,100)),(0,0),sh.filter(ImageFilter.GaussianBlur(20)))
        img.paste(ph,(x,top),m)
        if dark: ImageDraw.Draw(img).rounded_rectangle([x,top,x+cw-1,top+ch-1],radius=30,outline=GOLD,width=5)
        pill(img,lab,F(lang,'sb',34),top+ch+50,lang,fg=IVORY if dark else PLUM,bg=PLUM if dark else (236,224,224),cx=x+cw//2,padx=30,pady=16)
    pill(img,t['offer'],F(lang,'sb',38),H-105,lang,fg=IVORY,bg=PLUM)
    logo(img,50,44,130)
    d=ImageDraw.Draw(img); f=F(lang,'md',20); bb,tw,th=tb(d,t['tag'],f,lang); d.text((W-50-tw-bb[0],H-28-th-bb[1]),t['tag'],font=f,fill=MUTED,direction='rtl',language=lang)
    img.save(f'ad_compare_{lang}.jpg',quality=94)
    # ---- AD 2: hero bag + box
    hero=Image.open(UP+'16ab461c-image.png').convert('RGB')
    img=cover(hero,W,H,0.5,0.2).filter(ImageFilter.GaussianBlur(30))
    sw=760; hr=hero.resize((sw,round(hero.height*sw/hero.width)),Image.LANCZOS).crop((0,200,sw,200+860))
    fm=Image.new('L',hr.size,255); fd=ImageDraw.Draw(fm)
    for i in range(60):
        a=int(255*i/60); fd.rectangle([i,i,hr.width-1-i,hr.height-1-i],outline=a)
    img.paste(hr,((W-sw)//2,H-860-150),fm.filter(ImageFilter.GaussianBlur(6)))
    veil=Image.new('RGB',(W,H),(244,232,222)); m=Image.new('L',(1,H))
    for y in range(H): m.putpixel((0,y),int(255*0.92*max(0,min(1,(560-y)/300))**1.1))
    img.paste(veil,(0,0),m.resize((W,H)))
    m2=Image.new('L',(1,H))
    for y in range(H): m2.putpixel((0,y),int(220*max(0,(y-1120)/230)**1.3))
    img.paste(Image.new('RGB',(W,H),PLUM_D),(0,0),m2.resize((W,H)))
    ct(img,t['b1'],F(lang,'xb',100),160,PLUM,lang)
    ct(img,t['b2'],F(lang,'xb',84),285,GOLD_D,lang)
    ct(img,t['bsub'],F(lang,'md',40),385,MUTED,lang)
    pill(img,t['offer'],F(lang,'sb',36),H-175,lang,fg=PLUM_D,bg=GOLD)
    ct(img,t['cta'],F(lang,'sb',40),H-90,IVORY,lang)
    logo(img,50,44,130)
    d=ImageDraw.Draw(img); f=F(lang,'md',20); bb,tw,th=tb(d,t['tag'],f,lang); d.text((W-50-tw-bb[0],H-28-th-bb[1]),t['tag'],font=f,fill=IVORY,direction='rtl',language=lang)
    img.save(f'ad_hero_{lang}.jpg',quality=94)
s=Image.new('RGB',(4*400+30,500),'white')
for i,n in enumerate(['ad_compare_ar','ad_hero_ar','ad_compare_he','ad_hero_he']): s.paste(Image.open(n+'.jpg').resize((400,500)),(i*410,0))
s.save('sheet.jpg',quality=88)
