from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, math, wave, json, os
import numpy as np
OUT=Path('media/reels/engenharia-reversa-tv-openai-20261026'); OUT.mkdir(parents=True,exist_ok=True)
W,H=1080,1920
scenes=[
(6,'ENGENHARIA REVERSA','NA SUA PRÓPRIA TV?',['ANALISAR UM EQUIPAMENTO SEU','NÃO É, POR SI SÓ, UM ATAQUE.'],'DIREITO + CIBERSEGURANÇA'),
(7,'O CASO','PESQUISADOR BANIDO?',['UM PESQUISADOR RELATOU TER PERDIDO','ACESSO À OPENAI DURANTE UMA ANÁLISE','DE UMA SMART TV SAMSUNG.'],'RELATO PÚBLICO • SEM CONFIRMAÇÃO DA OPENAI'),
(7,'DISTINÇÃO ESSENCIAL','TV ≠ PLATAFORMA',['INVESTIGAR O SEU EQUIPAMENTO É UMA COISA.','TENTAR CONTORNAR OU EXPLORAR','SISTEMAS DA PLATAFORMA É OUTRA.'],'O ENQUADRAMENTO DEPENDE DA CONDUTA'),
(8,'TERMOS DE USO','LIMITES CONTRATUAIS',['PLATAFORMAS PODEM RESTRINGIR','ENGENHARIA REVERSA DOS PRÓPRIOS SERVIÇOS','E CONTORNO DE MECANISMOS DE SEGURANÇA.'],'CONTRATO NÃO SUBSTITUI A ANÁLISE LEGAL'),
(8,'PESQUISA LEGÍTIMA','OU ABUSO?',['SISTEMAS AUTOMÁTICOS PODEM NÃO DISTINGUIR','PESQUISA DE SEGURANÇA DE ATIVIDADE MALICIOSA','SEM CONTEXTO SUFICIENTE.'],'DAÍ A IMPORTÂNCIA DE REVISÃO E RECURSO'),
(7,'NO BRASIL','NÃO HÁ REGRA ÚNICA',['ENGENHARIA REVERSA PODE TOCAR','SOFTWARE, CONTRATOS, SEGURANÇA E','DIREITOS AUTORAIS AO MESMO TEMPO.'],'O CASO CONCRETO IMPORTA'),
(7,'CONCLUSÃO','BANIMENTO NÃO PROVA CRIME',['UMA SUSPENSÃO DE CONTA É UMA DECISÃO','DA PLATAFORMA. NÃO É, SOZINHA,','UMA CONDENAÇÃO OU PROVA DE ILICITUDE.'],'DIREITO BINÁRIO'),
(5,'PERGUNTA FINAL','SEGURANÇA OU EXCESSO?',['ATÉ ONDE A MODERAÇÃO AUTOMÁTICA','DEVE IR NA PESQUISA DE SEGURANÇA?'],'@direitobinario')]
B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; R='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(path,size): return ImageFont.truetype(path,size)
def wrap(text_,f,maxw):
    out=[]; line=''
    for w in text_.split():
        t=(line+' '+w).strip()
        if f.getlength(t)>maxw and line: out.append(line); line=w
        else: line=t
    if line: out.append(line)
    return out
def put(d,x,y,s,size,color='#F5FBFF',bold=True,maxw=870):
    f=font(B if bold else R,size)
    for line in wrap(s,f,maxw): d.text((x,y),line,font=f,fill=color); y+=size+14
    return y
base=Image.new('RGB',(W,H),'#020710')
pix=np.array(base).astype(float); y,x=np.mgrid[0:H,0:W]
glow=np.exp(-((x-870)**2/(470**2)+(y-450)**2/(650**2)))
pix[:,:,1]+=glow*35; pix[:,:,2]+=glow*82
base=Image.fromarray(np.clip(pix,0,255).astype('uint8'))
for i,(sec,kicker,title,body,foot) in enumerate(scenes):
    im=base.copy(); d=ImageDraw.Draw(im)
    for xx in range(70,1040,95): d.line((xx,220,xx,1640),fill='#0A2033',width=1)
    for yy in range(250,1660,95): d.line((55,yy,1025,yy),fill='#0A2033',width=1)
    d.rounded_rectangle((60,255,1020,1585),radius=24,fill='#04111E',outline='#0B84B8',width=2)
    d.text((90,175),'DB / DIREITO BINÁRIO',font=font(B,32),fill='#22D7FF')
    d.text((90,305),kicker,font=font(B,28),fill='#82CFE8')
    d.line((90,368,955,368),fill='#22D7FF',width=3)
    d.text((90,420),f'{i+1:02d}',font=font(B,92),fill='#127FD2')
    yy=620; yy=put(d,90,yy,title,80 if i==0 else 72,'#F5FBFF',True,850); yy=max(930,yy+60)
    for p in body: yy=put(d,90,yy,p,39,'#D8EAF5',False,850)+16
    d.text((90,1425),foot,font=font(B,23),fill='#22D7FF')
    d.text((90,1510),'@direitobinario',font=font(R,30),fill='#F5FBFF')
    d.rectangle((90,1620,955,1628),fill='#0E2B3F'); d.rectangle((90,1620,90+int(865*(i+1)/len(scenes)),1628),fill='#22D7FF')
    d.text((90,1662),'DIREITO • TECNOLOGIA • IA',font=font(R,24),fill='#82AFC4')
    im.save(OUT/f'scene-{i:02}.png')
    if i==0: im.save(OUT/'cover.jpg',quality=94)
sr=44100; total=sum(s[0] for s in scenes); t=np.arange(sr*total)/sr; a=np.zeros(len(t))
chords=[(146.83,185,220),(130.81,164.81,196),(164.81,196,246.94),(130.81,174.61,220)]
for k in range(math.ceil(total/4)):
    ix=(t>=4*k)&(t<4*k+4); tt=t[ix]-4*k; env=np.minimum(tt/.5,1)*np.minimum((4-tt)/.9,1)
    for f in chords[k%4]: a[ix]+=.032*np.sin(2*np.pi*f*tt)*env
for beat in np.arange(0,total,.75):
    ix=(t>=beat)&(t<beat+.16); tt=t[ix]-beat; a[ix]+=.02*np.sin(2*np.pi*720*tt)*np.exp(-tt*24)
a*=np.minimum(t/2,1)*np.minimum((total-t)/2,1)
with wave.open(str(OUT/'music.wav'),'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a*32767).astype('<i2').tobytes())
if os.environ.get('PREVIEW_ONLY')!='1':
    for i,s in enumerate(scenes):
        subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(OUT/f'scene-{i:02}.png'),'-t',str(s[0]),'-vf',"zoompan=z='min(zoom+0.00008,1.014)':d=1:s=1080x1920:fps=30",'-c:v','libx264','-threads','2','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-an',str(OUT/f'clip-{i:02}.mp4')],check=True)
    (OUT/'concat.txt').write_text('\n'.join("file 'clip-%02d.mp4'"%i for i in range(len(scenes))))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-i',str(OUT/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','128k','-ac','2','-movflags','+faststart','-t',str(total),str(OUT/'reel.mp4')],check=True)
    for p in OUT.glob('clip-*.mp4'): p.unlink()
    (OUT/'concat.txt').unlink(); (OUT/'music.wav').unlink()
(OUT/'scenes.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2))
print(OUT/'reel.mp4')
