from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random
random.seed(13)
W,H=1080,1350
OUT=Path('media/posts/outlook-20261113');OUT.mkdir(parents=True,exist_ok=True)
FN='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
F=lambda n: ImageFont.truetype(FN,n)
CY=(0,224,255); GOLD=(255,207,67); WHITE=(246,250,255); RED=(255,62,79)
SLIDES=[
('A QUEDA DO','OUTLOOK','O QUE A PANE REVELA SOBRE\nTECNOLOGIA E RESPONSABILIDADE?','cover'),
('O QUE','ACONTECEU?','OUTLOOK E SERVIÇOS MICROSOFT\nAPRESENTARAM INSTABILIDADE.','servers'),
('FOI UM ATAQUE','HACKER?','NÃO CONFUNDA UMA FALHA\nDE SERVIÇO COM UM CIBERATAQUE.','shield'),
('QUEM FICOU','NO PREJUÍZO?','A RESPONSABILIDADE DEPENDE\nDO CONTRATO E DAS PROVAS.','justice'),
('SE A NUVEM PARA,','SEU NEGÓCIO PARA?','BACKUP, CONTINGÊNCIA E SLA:\nSUA EMPRESA TEM UM PLANO B?','cloud')
]
def line(d,coords,color,w=4):
 d.line(coords,fill=color,width=w,joint='curve')
def glow_line(im,coords,color,width=4):
 overlay=Image.new('RGBA',(W,H)); q=ImageDraw.Draw(overlay)
 q.line(coords,fill=color+(230,),width=width,joint='curve')
 blur=overlay.filter(ImageFilter.GaussianBlur(11))
 im.paste(blur,(0,0),blur); im.paste(overlay,(0,0),overlay)
def text_center(d,y,msg,size,color):
 ft=F(size); bb=d.textbbox((0,0),msg,font=ft)
 d.text(((W-(bb[2]-bb[0]))//2,y),msg,font=ft,fill=color,stroke_width=1,stroke_fill=(0,0,0))
def icon_envelope(d,cy):
 d.rounded_rectangle((235,cy-105,845,cy+230),radius=27,outline=CY,width=14,fill=(4,31,62))
 line(d,[(243,cy-95),(540,cy+95),(836,cy-95)],CY,11)
 line(d,[(245,cy+215),(445,cy+32)],(19,105,173),8)
 line(d,[(835,cy+215),(633,cy+32)],(19,105,173),8)
 line(d,[(555,cy-100),(490,cy+70),(562,cy+53),(507,cy+230)],RED,12)
 d.polygon([(802,cy+86),(874,cy+209),(730,cy+209)],fill=RED)
 text_center(d,cy+113,'!',91,WHITE)
def icon_servers(d):
 for k in range(3):
  x=212+k*227
  d.rounded_rectangle((x,635,x+175,918),radius=14,fill=(9,40,69),outline=CY,width=6)
  for j in range(6):
   yy=665+j*40;d.rounded_rectangle((x+18,yy,x+155,yy+24),radius=6,fill=(20,66,104),outline=(24,119,172),width=2)
   d.ellipse((x+29,yy+7,x+41,yy+19),fill=RED if (k+j)%3==0 else CY)
 d.polygon([(540,724),(615,851),(465,851)],fill=RED)
 text_center(d,762,'!',80,WHITE)
def icon_shield(d):
 pts=[(540,601),(790,685),(768,874),(540,979),(312,874),(290,685)]
 d.polygon(pts,fill=(7,46,80),outline=CY,width=13)
 d.polygon([(540,651),(737,715),(710,843),(540,923),(370,843),(344,715)],outline=GOLD,width=6)
 d.rounded_rectangle((483,733,598,839),radius=13,fill=(4,36,66),outline=CY,width=6)
 d.arc((502,666,582,780),180,360,fill=CY,width=12)
 d.ellipse((531,775,550,795),fill=GOLD)
 d.rectangle((539,789,545,811),fill=GOLD)
def icon_justice(d):
 line(d,[(540,623),(540,954)],GOLD,19)
 line(d,[(314,705),(765,705)],GOLD,12)
 d.ellipse((516,605,566,655),fill=GOLD)
 for x in [330,747]:
  line(d,[(x,701),(x-80,849)],GOLD,5);line(d,[(x,701),(x+80,849)],GOLD,5)
  d.arc((x-95,822,x+95,895),0,180,fill=GOLD,width=13)
 d.rounded_rectangle((421,945,658,968),radius=8,fill=GOLD)
 d.rounded_rectangle((355,975,720,1002),radius=11,fill=(125,88,26),outline=GOLD,width=4)
def icon_cloud(d):
 d.ellipse((250,685,560,925),fill=(11,69,112),outline=CY,width=11)
 d.ellipse((420,591,740,907),fill=(11,69,112),outline=CY,width=11)
 d.ellipse((628,690,834,907),fill=(11,69,112),outline=CY,width=10)
 d.rounded_rectangle((280,786,812,930),radius=46,fill=(11,69,112),outline=CY,width=9)
 line(d,[(425,808),(505,882),(668,718)],GOLD,22)
def render(idx,slide):
 top,bottom,body,typ=slide
 im=Image.new('RGB',(W,H))
 pix=im.load()
 for y in range(H):
  for x in range(W):
   v=max(0,1-abs(x-W//2)/(W//2))
   pix[x,y]=(int(3+8*v+3*y/H),int(14+22*v+5*y/H),int(31+34*v+8*y/H))
 d=ImageDraw.Draw(im)
 for k in range(15):
  xx=25+k*76
  line(d,[(xx,1050),(540+(xx-540)*1.55,1320)],(7,51,80),1)
 for yy in range(1020,1350,47): line(d,[(0,yy),(1080,yy)],(6,44,74),1)
 for k in range(36):
  x=random.randrange(0,W);y=random.randrange(425,1030)
  d.ellipse((x,y,x+2,y+2),fill=(20,91,126))
 glow_line(im,[(35,130),(35,40),(155,40)],CY,5)
 glow_line(im,[(925,40),(1045,40),(1045,130)],GOLD,5)
 glow_line(im,[(35,1235),(35,1310),(145,1310)],GOLD,4)
 glow_line(im,[(940,1310),(1045,1310),(1045,1225)],CY,4)
 d=ImageDraw.Draw(im)
 text_center(d,66,'@DIREITOBINARIO',43,WHITE)
 d.line((280,135,800,135),fill=GOLD,width=3)
 d.rounded_rectangle((72,176,1008,234),radius=12,outline=CY,width=3)
 text_center(d,182,'TECNOLOGIA  •  DIREITO  •  INFORMAÇÃO',32,CY)
 for size in [78,74,70,66,60]:
  if d.textbbox((0,0),top,font=F(size))[2]<966: break
 text_center(d,266,top,size,WHITE)
 for size in [110,100,90,80,73]:
  if d.textbbox((0,0),bottom,font=F(size))[2]<968: break
 text_center(d,365,bottom,size,GOLD)
 d.line((142,500,938,500),fill=CY,width=5)
 if typ=='cover': icon_envelope(d,690)
 elif typ=='servers': icon_servers(d)
 elif typ=='shield': icon_shield(d)
 elif typ=='justice': icon_justice(d)
 else: icon_cloud(d)
 d.rounded_rectangle((55,1058,1025,1245),radius=19,fill=(2,26,49),outline=CY,width=5)
 for j,txt in enumerate(body.split('\n')):
  for sz in [49,46,43,40,37]:
   if d.textbbox((0,0),txt,font=F(sz))[2]<925:break
  text_center(d,1085+j*76,txt,sz,WHITE if j==0 else GOLD)
 text_center(d,1275,f'DIREITO BINÁRIO   •   {idx}/5',30,WHITE)
 im.save(OUT/f'slide-{idx}.jpg','JPEG',quality=91,optimize=True)
for i,s in enumerate(SLIDES,1):render(i,s)
print('Rendered 5 cards 1080x1350')
