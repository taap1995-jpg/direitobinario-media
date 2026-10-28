from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
OUT=Path('media/posts/2026-10-28-19h-ia-soberana'); OUT.mkdir(parents=True,exist_ok=True)
W,H=1080,1350
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def F(p,s): return ImageFont.truetype(p,s)
base=Image.new('RGB',(W,H),'#020711'); a=np.array(base).astype(float); y,x=np.mgrid[0:H,0:W]
g=np.exp(-((x-860)**2/(430**2)+(y-300)**2/(430**2))); a[:,:,1]+=g*38; a[:,:,2]+=g*88
im=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(im)
for xx in range(55,1040,90): d.line((xx,170,xx,1160),fill='#092238',width=1)
for yy in range(190,1180,90): d.line((45,yy,1035,yy),fill='#092238',width=1)
d.rounded_rectangle((55,155,1025,1170),radius=28,fill='#04111E',outline='#13BCE8',width=2)
d.text((85,95),'DB / DIREITO BINÁRIO',font=F(B,28),fill='#22D7FF')
d.text((85,225),'IA + ESTADO',font=F(B,29),fill='#7EDAF1')
d.line((85,282,955,282),fill='#22D7FF',width=3)
d.text((85,355),'QUEM CONTROLA',font=F(B,70),fill='#F5FBFF')
d.text((85,445),'A IA DO GOVERNO?',font=F(B,70),fill='#F5FBFF')
d.text((85,590),'SOBERANIA DIGITAL NÃO É SÓ',font=F(B,35),fill='#D9EEF7')
d.text((85,645),'TER TECNOLOGIA.',font=F(B,35),fill='#D9EEF7')
d.text((85,735),'É GOVERNAR DADOS, AVALIAR MODELOS',font=F(R,31),fill='#B9D7E5')
d.text((85,785),'E DEFINIR CRITÉRIOS PARA O USO DE IA.',font=F(R,31),fill='#B9D7E5')
d.rounded_rectangle((85,900,955,1035),radius=20,outline='#137BA4',width=2)
d.text((120,935),'DADOS • TECNOLOGIA • PODER DE DECISÃO',font=F(B,24),fill='#22D7FF')
d.text((85,1100),'@direitobinario',font=F(R,28),fill='#F5FBFF')
im.save(OUT/'post.jpg',quality=95)
print(OUT/'post.jpg')
