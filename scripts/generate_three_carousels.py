from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import textwrap,random
W,H=1080,1350; BG=(10,25,47); CY=(0,255,255); WH=(255,255,255); MU=(185,199,217)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
posts={
'agentes_autonomos_001':[
{'badge':'IA + PRIVACIDADE','white':'SE A IA ACEITA OS TERMOS POR VOCÊ,','cyan':'QUEM É O RESPONSÁVEL?','sub':'O avanço dos agentes autônomos e a crise do consentimento digital.'},
{'cyan':'O QUE JÁ É REAL?','body':'Agentes de IA já navegam na internet e executam tarefas em seu nome. Isso inclui aceitar cookies, concordar com termos e compartilhar dados pessoais de forma 100% automatizada.'},
{'cyan':'UM CLIQUE AUTOMÁTICO VALE COMO CONSENTIMENTO?','body':'Sob a ótica da LGPD, o consentimento deve ser livre e inequívoco. Como garantir que a IA refletiu a real vontade do usuário? A responsabilidade civil precisa ser verificável.'},
{'white':'A IA AGE.','cyan':'A RESPONSABILIDADE NÃO PODE DESAPARECER.','cta':'Confiaria seus dados a um agente de IA? Comente abaixo!','footer':'Fonte: Reuters | @direitobinario'}],
'deepfakes_responsabilidade_002':[
{'badge':'DIREITO + TECNOLOGIA','white':'IA NO DIREITO: QUEM RESPONDE QUANDO A DECISÃO AUTOMATIZADA','cyan':'ERRA?','sub':'Tecnologia não elimina responsabilidade.'},
{'cyan':'A ERA DAS DEEPFAKES','body':'Vídeos e áudios manipulados por IA estão cada vez mais realistas. Eles podem arruinar reputações e causar prejuízos financeiros. Mas, na prática, quem paga a conta?'},
{'cyan':'PLATAFORMAS X CRIADORES','body':'Pelo Art. 19 do Marco Civil da Internet, as plataformas só são responsabilizadas se descumprirem ordem judicial. Mas quem cria e impulsiona a deepfake pode ser civilmente responsabilizado pelo dano.'},
{'cyan':'PRECEDENTES EM EVOLUÇÃO','body':'O Direito Digital está em constante mutação. Fique por dentro das novas teses para se proteger.','cta':'Salve este post para consultar depois.','footer':'Fonte: TJDFT | @direitobinario'}],
'aprendizado_federado_003':[
{'badge':'IA + PRIVACIDADE','white':'TREINAR IA','cyan':'SEM COMPARTILHAR OS DADOS?','sub':'Sim. Entenda como o Aprendizado Federado protege sua privacidade.'},
{'cyan':'O QUE É APRENDIZADO FEDERADO?','body':"É uma técnica que permite treinar modelos de IA sem enviar os dados para um único local. O modelo 'viaja' até o dado, e não o contrário."},
{'cyan':'O USO PELO GOVERNO','body':'A Receita Federal apresentou à OCDE o uso dessa técnica em projetos de IA. Ela permite colaborar entre instituições sem compartilhar dados sensíveis dos contribuintes.'},
{'cyan':'INOVAÇÃO E PRIVACIDADE CAMINHAM JUNTAS','body':'É possível reduzir riscos de vazamento e ainda assim treinar IA. A tecnologia também pode ser desenhada para proteger.','cta':'Compartilhe este post com aquele amigo que tem medo de usar IA!','footer':'Fonte: Receita Federal / OCDE | @direitobinario'}]}
def font(sz,b=True): return ImageFont.truetype(FB if b else FR,sz)
def lines(d,t,f,m=870):
 out=[]; cur=''
 for w in t.split():
  q=(cur+' '+w).strip()
  if d.textbbox((0,0),q,font=f)[2]<=m: cur=q
  else:
   if cur: out.append(cur)
   cur=w
 if cur: out.append(cur)
 return out
def render(pid,n,s):
 im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); r=random.Random(pid+str(n))
 for _ in range(24):
  x=r.randint(40,1000); y=r.randint(60,1250); l=r.randint(70,220); c=(0,95,110)
  d.line((x,y,min(1030,x+l),y),fill=c,width=2); d.ellipse((min(1030,x+l)-3,y-3,min(1030,x+l)+3,y+3),fill=CY)
 d.rectangle((48,48,1032,1302),outline=(0,130,150),width=2); y=100
 if s.get('badge'):
  d.rounded_rectangle((75,y,430,y+58),12,outline=CY,width=2); d.text((95,y+11),s['badge'],font=font(28),fill=CY); y+=110
 for k,col,sz in [('white',WH,60),('cyan',CY,62)]:
  if s.get(k):
   f=font(sz)
   for ln in lines(d,s[k],f): d.text((78,y),ln,font=f,fill=col); y+=sz+14
   y+=18
 if s.get('sub'):
  y=max(y,730); f=font(34,False)
  for ln in lines(d,s['sub'],f): d.text((80,y),ln,font=f,fill=MU); y+=48
 if s.get('body'):
  y=max(y,500); f=font(39,False)
  for ln in lines(d,s['body'],f): d.text((80,y),ln,font=f,fill=WH); y+=58
 if s.get('cta'):
  y=max(y,1040); d.line((80,y-28,1000,y-28),fill=CY,width=2); f=font(31)
  for ln in lines(d,s['cta'],f): d.text((80,y),ln,font=f,fill=CY); y+=44
 if s.get('footer'): d.text((80,1245),s['footer'],font=font(24,False),fill=MU)
 d.text((80,1290),'DIREITO BINÁRIO',font=font(22),fill=CY)
 out=Path('public/posts')/pid; out.mkdir(parents=True,exist_ok=True); base=out/f'{pid}_tela_{n:02d}'
 im.save(str(base)+'.png','PNG',optimize=True); im.save(str(base)+'.jpg','JPEG',quality=94,optimize=True)
for pid,slides in posts.items():
 for i,s in enumerate(slides,1): render(pid,i,s)
