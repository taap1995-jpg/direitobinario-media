from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess, wave, math, struct
p=Path(__file__).parent
bg=Image.open('generated_images/exec-7b0bc7b0-e1d7-4ab3-8f95-87e0142d3931.png').convert('RGB').resize((720,1280))
scenes=[('E SE A IA CAUSAR\nUMA GRANDE CRISE?','EMPRESAS JÁ ENSAIAM\nO DIA SEGUINTE.',5),('OPENAI E ANTHROPIC','SEGUNDO A AXIOS, EXECUTIVOS\nSIMULAM CENÁRIOS DE CRISE.',6),('QUAL É O RISCO?','ATAQUES QUE INTERROMPAM\nBANCOS, INTERNET\nE SERVIÇOS ESSENCIAIS.',6),('ISSO É INEVITÁVEL?','NÃO É UMA CERTEZA.\nA OPENAI DIZ QUE OS EXERCÍCIOS\nTESTAM DIFERENTES POSSIBILIDADES.',7),('E QUEM RESPONDE?','A DISCUSSÃO ENVOLVE\nPREVENÇÃO, FISCALIZAÇÃO\nE RESPONSABILIDADE.',6),('ESPERAR A CRISE\nPARA CRIAR REGRAS?','COMENTE SUA OPINIÃO.\nSALVE E SIGA @DIREITOBINARIO.',6)]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def block(d,txt,y,size,col):
 f=ImageFont.truetype(font,size)
 while max(d.textlength(t,font=f) for t in txt.split('\n'))>620:
  size-=1;f=ImageFont.truetype(font,size)
 d.multiline_text((360,y),txt,font=f,fill=col,anchor='ma',align='center',spacing=12,stroke_width=1)
for i,(title,body,duration) in enumerate(scenes):
 im=bg.copy();d=ImageDraw.Draw(im)
 d.rectangle((0,0,720,420),fill='#050911')
 block(d,'DIREITO + TECNOLOGIA',90,21,'#38d9ff')
 block(d,title,145,43,'#ffffff')
 block(d,body,280,26,'#e8c26a')
 d.rounded_rectangle((45,1050,675,1130),radius=16,fill='#050911',outline='#22cfff',width=2)
 block(d,'CENÁRIO DE RISCO ≠ PREVISÃO',1075,23,'#ffffff')
 block(d,'@DIREITOBINARIO  •  '+str(i+1)+'/6',1170,21,'#ffffff')
 block(d,'FONTES: AXIOS / TILT UOL • OUT/2026',1213,14,'#bbbbbb')
 im.save(p/f'scene{i}.jpg',quality=93)
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(p/f'scene{i}.jpg'),'-t',str(duration),'-r','24','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','25','-pix_fmt','yuv420p',str(p/f'part{i}.mp4')],check=True)
(p/'concat.txt').write_text(''.join(f"file 'part{i}.mp4'\n" for i in range(len(scenes))))
sr=22050;total=sum(s[2] for s in scenes)
with wave.open(str(p/'music.wav'),'w') as w:
 w.setparams((1,2,sr,0,'NONE','not compressed'))
 for n in range(sr*total):
  t=n/sr; beat=t%0.5
  bass=math.sin(2*math.pi*55*t)*math.exp(-beat*9)
  pad=sum(math.sin(2*math.pi*f*t) for f in (110,130.81,164.81))/5
  v=(bass*.15+pad*.13)*min(1,t/2,(total-t)/3)
  w.writeframesraw(struct.pack('<h',int(v*32767)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(p/'concat.txt'),'-i',str(p/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(p/'reel_catastrofe_ia.mp4')],check=True)
print('RENDER_OK', (p/'reel_catastrofe_ia.mp4').stat().st_size)
