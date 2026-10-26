from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, shutil, wave, math, struct, html
import numpy as np
out=Path('output/reel_prorrogacao_20261026'); out.mkdir(parents=True,exist_ok=True)
W,H=1080,1920
navy='#0A1628'; gold='#C9A84C'; white='#F4F1E9'; muted='#AFBDCF'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
scenes=[
(6,'O QUE MUDOU?',['Lula e Flávio','pediram mais','tempo para votar.'],['Os motivos foram diferentes.'],'25 OUT 2026  /  2º TURNO'),
(8,'PEDIDO DA CAMPANHA DE LULA',['Problemas no','transporte','público.'],['Relatos de dificuldades com ônibus.','O pedido começou na Bahia','e foi ampliado ao país.'],'PEDIDOS  /  01'),
(8,'PEDIDO DA CAMPANHA DE FLÁVIO',['Chuvas fortes,','alagamentos','e falta de energia.'],['A campanha pediu extensão','em municípios de cinco estados.','MG · RS · SP · PR · SC'],'PEDIDOS  /  02'),
(8,'DECISÃO DE CRISTIANO ZANIN',['Votação','até as 19h.'],['O esclarecimento restringiu','o cumprimento aos locais','com urnas ainda abertas.'],'STF  /  ESCLARECIMENTO'),
(7,'O DETALHE JURÍDICO',['Pedido não','é decisão.'],['Motivo, alcance e condições','precisam ser lidos juntos.','Fontes e contexto na legenda.'],'INFORMAÇÃO COM CONTEXTO'),
(5,'DIREITO & TECNOLOGIA',['Entenda antes','de compartilhar.'],['Siga @direitobinario','Direito explicado com clareza.'],'SALVE  /  COMPARTILHE')
]
for i,(duration,kicker,title,body,tag) in enumerate(scenes):
    im=Image.new('RGB',(W,H),navy); d=ImageDraw.Draw(im)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1080" height="1920" fill="{navy}"/>']
    def line(coords,fill,width):
        d.line(coords,fill=fill,width=width)
        svg.append(f'<line x1="{coords[0]}" y1="{coords[1]}" x2="{coords[2]}" y2="{coords[3]}" stroke="{fill}" stroke-width="{width}"/>')
    def txt(x,y,t,size=40,fill=white,isbold=False):
        f=ImageFont.truetype(bold if isbold else regular,size)
        assert d.textbbox((x,y),t,font=f)[2] < 980,(t,size)
        d.text((x,y),t,font=f,fill=fill)
        svg.append(f'<text x="{x}" y="{y+size}" font-family="DejaVu Sans" font-size="{size}" font-weight="{700 if isbold else 400}" fill="{fill}">{html.escape(t)}</text>')
    for x in range(80,1100,120): line((x,230,x,1470),'#12263F',1)
    line((80,290,930,290),gold,3)
    txt(80,170,'DB  /  DIREITO BINÁRIO',32,gold,True)
    txt(80,340,kicker,26,muted,True)
    txt(80,433,f'{i+1:02d}',108,gold,True)
    y=650
    size=66 if i==2 else 74
    for t in title:txt(80,y,t,size,white,True); y+=size+18
    y=max(1040,y+65)
    for t in body:txt(80,y,t,36,muted); y+=59
    line((80,1440,930,1440),gold,2)
    txt(80,1490,tag,26,gold,True)
    txt(80,1560,'@direitobinario',33,white,True)
    txt(80,1620,'CONTEXTO DO EPISÓDIO DE 25/10/2026',22,muted)
    for j in range(6):line((80+j*145,1710,195+j*145,1710),gold if j<=i else '#29405C',7)
    im.save(out/f'scene{i}.png')
    (out/f'scene{i}.svg').write_text(''.join(svg)+'</svg>')
# Original instrumental: calm electronic pulse, composed programmatically.
sr=44100; total=sum(s[0] for s in scenes)
t=np.arange(sr*total)/sr; a=np.zeros_like(t)
chords=[(146.83,185,220),(130.81,164.81,196),(164.81,196,246.94),(130.81,174.61,220)]
for k in range(math.ceil(total/4)):
    start=k*4; ix=(t>=start)&(t<min(start+4,total)); tt=t[ix]-start
    env=np.minimum(tt/.5,1)*np.minimum((4-tt)/.8,1)
    for f in chords[k%4]:a[ix]+=.025*np.sin(2*np.pi*f*tt)*env
for b in np.arange(0,total,.75):
    ix=(t>=b)&(t<b+.21); tt=t[ix]-b
    a[ix]+=.035*np.sin(2*np.pi*660*tt)*np.exp(-tt*25)
a*=np.minimum(t/2,1)*np.minimum((total-t)/2,1)
with wave.open(str(out/'music.wav'),'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a*32767).astype('<i2').tobytes())
ff=shutil.which('ffmpeg')
if not ff:
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe()
args=[ff,'-y','-hide_banner','-loglevel','error']
for i,s in enumerate(scenes):args+=['-loop','1','-t',str(s[0]),'-i',str(out/f'scene{i}.png')]
args+=['-i',str(out/'music.wav')]
filters=''.join(f'[{i}:v]fps=30,format=yuv420p,setsar=1[v{i}];' for i in range(6))
filters+=''.join(f'[v{i}]' for i in range(6))+'concat=n=6:v=1:a=0[v]'
args+=['-filter_complex',filters,'-map','[v]','-map','6:a','-c:v','libx264','-preset','ultrafast','-crf','22','-c:a','aac','-b:a','128k','-ar','44100','-movflags','+faststart','-t',str(total),str(out/'reel_prorrogacao.mp4')]
subprocess.run(args,check=True)
thumb=Image.new('RGB',(540*3,960*2))
for i in range(6):thumb.paste(Image.open(out/f'scene{i}.png').resize((540,960)),((i%3)*540,(i//3)*960))
thumb.save(out/'preview.jpg')
print(out/'reel_prorrogacao.mp4')
