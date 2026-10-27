from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,json,math,wave,struct,asyncio,os
O=Path('media/reels/tempo-urna-parte2-20261027');O.mkdir(parents=True,exist_ok=True)
scenes=[
(4,['PASSOU DE','1 MINUTO E MEIO?'], 'PERDE O VOTO?', 'Passou de um minuto e meio na urna: perde o voto?'),
(6,['VIU A PARTE 1?','AGORA É COM VOCÊ.'],'A REGRA PARA O ELEITOR','Depois do vídeo sobre Lula e Flávio, vamos à dúvida que importa para você.'),
(7,['1 MINUTO E MEIO:','É UMA ESTIMATIVA.'],'NÃO É PRAZO FINAL','Um minuto e meio aparece como estimativa. Não significa que seu voto acaba automaticamente nesse tempo.'),
(8,['MAIS DE 40 SEGUNDOS','SEM INTERAÇÃO'],'AVISO AO MESÁRIO','O treinamento da Justiça Eleitoral prevê um aviso após mais de quarenta segundos de inatividade. Atenção: inatividade.'),
(8,['O MESÁRIO VERIFICA','SE HÁ DIFICULDADE.'],'AVISO NÃO CANCELA O VOTO','O mesário verifica se você está com dificuldade. O aviso, sozinho, não cancela o voto.'),
(7,['PRECISOU DE AJUDA?','CHAME O MESÁRIO.'],'LEVE SUA COLINHA DE PAPEL','Se precisar de orientação, chame o mesário. Levar os números anotados em papel também ajuda.'),
(5,['VOCÊ SABIA DISSO?','SALVE E COMPARTILHE.'],'SIGA @DIREITOBINARIO','Você achava que existia esse limite? Comente e compartilhe.')]
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
C='#30DFFF';G='#E4BC62'
def txt(d,y,s,size=65,col='white'):
 f=ImageFont.truetype(F,size)
 while f.getlength(s)>900:
  size-=1;f=ImageFont.truetype(F,size)
 d.text(((1080-f.getlength(s))/2,y),s,font=f,fill=col)
def art(i):
 im=Image.new('RGB',(1080,1920),'#040B17');d=ImageDraw.Draw(im)
 for x in range(0,1080,70):d.line((x,0,x,1920),fill='#0C2334',width=1)
 for y in range(0,1920,70):d.line((0,y,1080,y),fill='#0C2334',width=1)
 for r in range(440,40,-20):d.ellipse((540-r,920-r,540+r,920+r),outline='#103044',width=2)
 txt(d,170,'DB / DIREITO BINÁRIO',32,C);txt(d,235,'ELEIÇÕES 2026 • PARTE 2',26,G)
 for k,line in enumerate(scenes[i][1]):txt(d,370+k*95,line,70,C if k else 'white')
 # Illustrated voting machine, distinct screen and keypad
 d.rounded_rectangle((130,770,850,1190),40,fill='#15283B',outline=C,width=5)
 d.rounded_rectangle((155,795,825,1165),25,fill='#D4E2E8')
 d.rounded_rectangle((185,840,535,1080),15,fill='#061727',outline='#29ABD8',width=4)
 d.text((222,900),'SEU VOTO',font=ImageFont.truetype(F,37),fill=C)
 d.text((227,957),'É SECRETO',font=ImageFont.truetype(F,31),fill='white')
 for row in range(3):
  for col in range(3):
   x=575+col*70;y=830+row*65
   d.rounded_rectangle((x,y,x+56,y+51),7,fill='#152436')
   d.text((x+18,y+10),str(row*3+col+1),font=ImageFont.truetype(F,24),fill='white')
 d.rounded_rectangle((645,1027,701,1078),7,fill='#152436')
 d.text((663,1037),'0',font=ImageFont.truetype(F,24),fill='white')
 for x,c in [(570,'#FFFFFF'),(650,'#DB8E3D'),(730,'#36A864')]:d.rounded_rectangle((x,1100,x+65,1140),5,fill=c)
 # Timer is an editorial overlay
 d.rounded_rectangle((280,610,800,730),24,fill='#081826',outline=G,width=3)
 txt(d,628,'01:30?' if i<3 else ('40s INATIVO' if i==3 else 'SEU DIREITO'),58,G)
 # Original robotic scales mascot
 d.line((880,1050,880,1280),fill=C,width=14)
 d.line((785,1115,975,1115),fill=C,width=10)
 for x in (800,960):
  d.line((x,1115,x-35,1190),fill=G,width=4);d.line((x,1115,x+35,1190),fill=G,width=4)
  d.pieslice((x-43,1150,x+43,1230),0,180,fill='#204A60',outline=C,width=3)
 d.rounded_rectangle((817,1005,943,1090),22,fill='#163449',outline=C,width=4)
 for x in (849,900):d.ellipse((x,1030,x+16,1049),fill=C)
 d.arc((862,1040,899,1070),0,180,fill='white',width=3)
 d.rounded_rectangle((825,1270,940,1290),10,fill=C)
 txt(d,1370,scenes[i][2],44,G)
 txt(d,1500,'@DIREITOBINARIO',31,C)
 txt(d,1580,'FONTES: TSE / JUSTIÇA ELEITORAL',23,'#91ADBF')
 d.rounded_rectangle((90,1680,990,1688),4,fill='#1A3547')
 d.rounded_rectangle((90,1680,90+int(900*(i+1)/7),1688),4,fill=C)
 return im
async def voice():
 import edge_tts
 for i,s in enumerate(scenes):
  await edge_tts.Communicate(s[3],'pt-BR-AntonioNeural',rate='+0%').save(str(O/f'voice-{i}.mp3'))
if os.getenv('PREVIEW_ONLY')!='1':asyncio.run(voice())
durations=[];contact=Image.new('RGB',(810,1920),'#040B17')
for i,s in enumerate(scenes):
 im=art(i);im.save(O/f'scene-{i}.jpg',quality=95)
 contact.paste(im.resize((270,480)),((i%3)*270,(i//3)*480))
 if i==0:im.save(O/'cover.jpg',quality=95)
 if os.getenv('PREVIEW_ONLY')=='1':continue
 audio=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(O/f'voice-{i}.mp3')]))
 duration=max(s[0],audio+.5);durations.append(duration)
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(O/f'scene-{i}.jpg'),'-i',str(O/f'voice-{i}.mp3'),'-t',str(duration),'-vf',"zoompan=z='min(zoom+0.00006,1.012)':d=1:s=1080x1920:fps=30",'-af','apad','-c:v','libx264','-threads','2','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2',str(O/f'clip-{i}.mp4')],check=True)
contact.save(O/'preview.jpg',quality=90)
if os.getenv('PREVIEW_ONLY')!='1':
 (O/'concat.txt').write_text('\n'.join("file 'clip-%d.mp4'"%i for i in range(7)))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(O/'concat.txt'),'-c','copy','-movflags','+faststart',str(O/'reel.mp4')],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(O/'reel.mp4')]))
 (O/'qa.json').write_text(json.dumps(probe))
 for pat in ['clip-*.mp4','voice-*.mp3','concat.txt']:
  for p in O.glob(pat):p.unlink()
