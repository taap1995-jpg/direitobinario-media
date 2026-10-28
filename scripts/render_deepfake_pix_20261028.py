"""Approved Pix/deepfake Reel, instrumental only."""
import sys,json,math,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_music_reels_20261025 import music
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'media/reels/2026-10-28-deepfake-pix';out.mkdir(parents=True,exist_ok=True)
scenes=[
(6,'VOZ CLONADA.','PIX REAL.','Seu pai pede dinheiro. A voz parece dele. Mas pode ser IA.'),
(6,'O BANCO TEM','QUE DEVOLVER?','Não é automático. A responsabilidade depende das falhas e das provas.'),
(7,'SÚMULA 479','DO STJ','Fraudes ligadas ao risco da atividade bancária podem gerar responsabilidade objetiva.'),
(7,'FORA DO SEU','PERFIL?','Operações suspeitas que o banco deixou passar podem indicar falha de segurança.'),
(7,'CAIU NO GOLPE?','AJA RÁPIDO.','Avise o banco, solicite o MED e guarde os comprovantes.'),
(7,'MED NÃO GARANTE','DEVOLUÇÃO.','Salve este vídeo. Você já recebeu uma ligação suspeita?')]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
for i,(sec,a,b,detail) in enumerate(scenes):
 im=Image.new('RGB',(1080,1920),'#071222');d=ImageDraw.Draw(im)
 for x in range(0,1080,90):d.line((x,0,x,1920),fill='#10283C',width=1)
 for y in range(0,1920,90):d.line((0,y,1080,y),fill='#10283C',width=1)
 # Neon robot and smartphone illustration
 d.rounded_rectangle((320,260,760,600),70,fill='#102B40',outline='#00E5FF',width=7)
 d.line((540,260,540,210),fill='#00E5FF',width=7);d.ellipse((525,182,555,212),fill='#C9A84C')
 for x in (405,610):d.rounded_rectangle((x,365,x+65,410),14,fill='#00E5FF')
 d.line((440,495,640,495),fill='#C9A84C',width=8)
 d.rounded_rectangle((715,455,850,700),20,fill='#071222',outline='#C9A84C',width=5)
 for j in range(7):
  x=735+j*14;h=18+int(35*abs(math.sin(j*1.7+i)))
  d.line((x,575-h,x,575+h),fill='#00E5FF',width=5)
 def txt(y,t,size,color='#FAF8F2',bold=True):
  f=ImageFont.truetype(font if bold else regular,size)
  assert d.textlength(t,font=f)<900,t
  d.text((90,y),t,font=f,fill=color)
 txt(115,'DIREITO + IA + TECNOLOGIA',30,'#C9A84C')
 txt(775,a,65);txt(865,b,65,'#00E5FF')
 f=ImageFont.truetype(regular,43);words=detail.split();lines=[];line=''
 for w in words:
  test=(line+' '+w).strip()
  if d.textlength(test,font=f)>890:lines.append(line);line=w
  else:line=test
 lines.append(line)
 for j,line in enumerate(lines):txt(1040+j*66,line,43,bold=False)
 txt(1460,'Fontes: STJ e Banco Central',28,'#B9CBDD',False)
 txt(1530,'@direitobinario',35,'#C9A84C')
 for j in range(6):
  d.rounded_rectangle((90+j*150,1630,220+j*150,1638),4,fill='#00E5FF' if j<=i else '#244154')
 im.save(out/f'scene-{i}.png')
 if i==0:im.save(out/'cover.jpg',quality=95)
 subprocess.run(['ffmpeg','-y','-loop','1','-i',str(out/f'scene-{i}.png'),'-t',str(sec),'-vf',"zoompan=z='min(zoom+0.00003,1.012)':d=1:s=1080x1920:fps=30",'-c:v','libx264','-threads','2','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p','-an',str(out/f'part-{i}.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(out/'concat.txt').write_text('\n'.join("file 'part-%s.mp4'"%i for i in range(6)))
qa=music(out/'music.wav',40,28102026)
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-i',str(out/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','160k','-t','40','-movflags','+faststart',str(out/'reel.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out/'reel.mp4')]))
assert abs(float(p['format']['duration'])-40)<.2
assert any(s['codec_name']=='aac' for s in p['streams'])
(out/'qa.json').write_text(json.dumps({'duration':40,'narration':False,'music':qa,'probe':p},indent=2))
for file in list(out.glob('part-*.mp4'))+[out/'concat.txt',out/'music.wav']:file.unlink()
