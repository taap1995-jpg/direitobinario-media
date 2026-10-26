from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, math, wave, json
import numpy as np
OUT=Path('media/reels/constituicao-voto-20261026'); OUT.mkdir(parents=True,exist_ok=True)
W,H=1080,1920
scenes=[
(5,'O QUE ACONTECEU?','17H → 19H',['POR QUE O HORÁRIO MUDOU?','E O RESULTADO É VÁLIDO?'],'ELEIÇÕES • 25/10/2026'),
(7,'PEDIDOS À JUSTIÇA','AS DUAS CAMPANHAS',['LULA (PT) E FLÁVIO (PL)','PEDIRAM MAIS TEMPO PARA VOTAR.'],'MOTIVOS E ABRANGÊNCIAS DIFERENTES'),
(7,'OS MOTIVOS','ACESSO ÀS URNAS',['LULA: FALHAS NO TRANSPORTE.','FLÁVIO: CHUVAS E ALAGAMENTOS.'],'PEDIDOS DISTINTOS • FONTES NA LEGENDA'),
(8,'POR QUE O SUPREMO?','UMA RECLAMAÇÃO',['A CAMPANHA DE LULA ALEGOU','DESCUMPRIMENTO DE DECISÃO DO STF','SOBRE TRANSPORTE ELEITORAL.'],'PRECEDENTE: ADPF 1.013'),
(8,'BASE CONSTITUCIONAL','ART. 102, I, “L”',['O STF JULGA RECLAMAÇÕES PARA','GARANTIR A AUTORIDADE','DAS PRÓPRIAS DECISÕES.'],'NÃO É REVISÃO AUTOMÁTICA DOS ATOS DO TSE'),
(7,'DECISÃO E CUMPRIMENTO','STF + TSE',['ZANIN CONCEDEU A LIMINAR.','AO TSE COUBE OPERACIONALIZAR','O CUMPRIMENTO DA MEDIDA.'],'DECISÃO INDIVIDUAL • NÃO DO PLENÁRIO'),
(6,'DIREITO PROTEGIDO','ACESSO AO VOTO',['O ART. 14 DA CONSTITUIÇÃO','PROTEGE A SOBERANIA POPULAR','E O VOTO COM IGUAL VALOR.'],'O OBJETIVO DECLARADO ERA PROTEGER O VOTO'),
(7,'O LIMITE DA MEDIDA','ATÉ AS 19H',['A EXTENSÃO VALEU PARA','AS SEÇÕES AINDA ABERTAS.','URNAS ENCERRADAS NÃO REABRIRAM.'],'ENCERRAMENTO ADIADO DAS 17H PARA AS 19H'),
(6,'RESULTADO OFICIAL','LULA REELEITO',['O RESULTADO FOI ANUNCIADO','PELO TRIBUNAL SUPERIOR ELEITORAL.'],'CONFIRMAÇÃO OFICIAL DO TSE'),
(7,'VALIDADE DA ELEIÇÃO','MUDAR O HORÁRIO',['POR SI SÓ, NÃO DEMONSTRA FRAUDE','NEM ANULA A VITÓRIA.'],'A ANÁLISE JURÍDICA DEPENDE DO CASO'),
(8,'GARANTIAS LEGAIS','CONTESTAR ≠ ANULAR',['CONTESTAÇÕES SÃO POSSÍVEIS','PELOS MEIOS LEGAIS. ALEGAR NÃO BASTA:','É PRECISO FUNDAMENTO E PROVAS.'],'A DECISÃO CABE À JUSTIÇA COMPETENTE'),
(5,'DIREITO COM CLAREZA','RESPEITE O RESULTADO',['CONSULTE AS FONTES NA LEGENDA.','SALVE PARA REVER A EXPLICAÇÃO.'],'@direitobinario')]
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def text(d,xy,s,size,color='#F4FAFF',bold=True,maxwidth=880):
 f=ImageFont.truetype(B if bold else R,size)
 assert d.textbbox(xy,s,font=f)[2]-xy[0]<=maxwidth,(s,size)
 d.text(xy,s,font=f,fill=color)
def wrap(s,font,width):
 lines=[]; line=''
 for word in s.split():
  trial=(line+' '+word).strip()
  if font.getlength(trial)>width:
   lines.append(line); line=word
  else: line=trial
 if line: lines.append(line)
 return lines
base=Image.new('RGB',(W,H),'#030915')
pix=np.array(base).astype(float)
y,x=np.mgrid[0:H,0:W]
glow=np.exp(-((x-920)**2/(520**2)+(y-510)**2/(700**2)))
pix[:,:,1]+=glow*27;pix[:,:,2]+=glow*63
base=Image.fromarray(pix.clip(0,255).astype('uint8'))
for i,(seconds,kicker,title,body,foot) in enumerate(scenes):
 im=base.copy(); d=ImageDraw.Draw(im)
 for xx in range(70,1040,105):
  d.line((xx,220,xx,1580),fill='#0C2035',width=1)
 for yy in range(250,1600,105):d.line((55,yy,1005,yy),fill='#0C2035',width=1)
 for j in range(5):
  yy=330+j*130
  d.line((950,yy,1020,yy,1020,yy+65,990,yy+65),fill='#146086',width=2)
  d.ellipse((985,yy+60,995,yy+70),fill='#00C8EF')
 d.rounded_rectangle((65,260,1010,1550),radius=22,fill='#061222',outline='#174D70',width=2)
 text(d,(95,195),'DB / DIREITO BINÁRIO',32,'#00C8EF')
 text(d,(95,310),kicker,28,'#8AB8D0')
 d.line((95,375,950,375),fill='#00C8EF',width=3)
 text(d,(95,430),f'{i+1:02d}',96,'#167BD1')
 fs=90 if i==0 else 76
 lines=wrap(title,ImageFont.truetype(B,fs),850)
 yy=650
 for line in lines:text(d,(95,yy),line,fs,'#F4FAFF',maxwidth=850);yy+=fs+18
 yy=max(970,yy+70)
 for phrase in body:
  for line in wrap(phrase,ImageFont.truetype(R,42),850):
   text(d,(95,yy),line,42,'#D5E6F4',False);yy+=62
 assert yy<1370,(i,yy)
 text(d,(95,1400),foot,23,'#00C8EF',maxwidth=870)
 text(d,(95,1490),'@direitobinario',30,'#F4FAFF',False)
 d.rectangle((95,1615,950,1622),fill='#10283E')
 d.rectangle((95,1615,95+int(855*(i+1)/len(scenes)),1622),fill='#00C8EF')
 text(d,(95,1650),'DIREITO & TECNOLOGIA',24,'#79A6C1')
 im.save(OUT/f'scene-{i:02}.png')
 if i==0: im.save(OUT/'cover.jpg',quality=94)
 thumb=im.resize((270,480))
 if i==0:contact=Image.new('RGB',(1080,1440))
 contact.paste(thumb,((i%4)*270,(i//4)*480))
contact.save(OUT/'preview.jpg',quality=90)
# Original electronic instrumental, no third-party recordings.
sr=44100; total=sum(s[0] for s in scenes); t=np.arange(sr*total)/sr; a=np.zeros(len(t))
for k in range(math.ceil(total/4)):
 ix=(t>=4*k)&(t<4*k+4); tt=t[ix]-4*k
 env=np.minimum(tt/.4,1)*np.minimum((4-tt)/.8,1)
 for f in [(146.83,185,220),(130.81,164.81,196),(164.81,196,246.94),(130.81,174.61,220)][k%4]:
  a[ix]+=.035*np.sin(2*np.pi*f*tt)*env
for beat in np.arange(0,total,.75):
 ix=(t>=beat)&(t<beat+.18);tt=t[ix]-beat
 a[ix]+=.025*np.sin(2*np.pi*660*tt)*np.exp(-tt*25)
a*=np.minimum(t/2,1)*np.minimum((total-t)/2,1)
with wave.open(str(OUT/'music.wav'),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype('<i2').tobytes())
if __import__('os').environ.get('PREVIEW_ONLY')!='1':
 for i,s in enumerate(scenes):
  subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(OUT/f'scene-{i:02}.png'),'-t',str(s[0]),'-vf',"zoompan=z='min(zoom+0.00008,1.014)':d=1:s=1080x1920:fps=30",'-c:v','libx264','-threads','2','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-an',str(OUT/f'clip-{i:02}.mp4')],check=True)
 (OUT/'concat.txt').write_text('\n'.join("file 'clip-%02d.mp4'"%i for i in range(len(scenes))))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(OUT/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','128k','-ac','2','-movflags','+faststart','-t',str(total),str(OUT/'reel.mp4')],check=True)
 for p in OUT.glob('clip-*.mp4'):p.unlink()
 (OUT/'concat.txt').unlink();(OUT/'music.wav').unlink()
 print(OUT/'reel.mp4')
(OUT/'scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2))
