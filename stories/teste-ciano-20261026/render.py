from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import random, math, html
out=Path('output/story_teste_ciano_20261026');out.mkdir(parents=True,exist_ok=True)
W,H=1080,1920
im=Image.new('RGB',(W,H),'#030915')
d=ImageDraw.Draw(im); svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><rect width="1080" height="1920" fill="#030915"/>']
def line(xy,color,width=2):
 d.line(xy,fill=color,width=width)
 svg.append(f'<polyline points="{" ".join(str(xy[i])+","+str(xy[i+1]) for i in range(0,len(xy),2))}" fill="none" stroke="{color}" stroke-width="{width}"/>')
def dot(x,y,r,color):
 d.ellipse((x-r,y-r,x+r,y+r),fill=color)
 svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
def txt(x,y,text,size,color='#FFFFFF',scale=1,bold=True):
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
 box=font.getbbox(text);tw=box[2]+4
 layer=Image.new('RGBA',(tw,size*2));ImageDraw.Draw(layer).text((0,0),text,font=font,fill=color)
 layer=layer.resize((int(tw*scale),size*2),Image.Resampling.LANCZOS)
 assert x+layer.width<=990,(text,x+layer.width)
 im.paste(layer,(x,y),layer)
 svg.append(f'<text x="{x}" y="{y+size}" font-family="DejaVu Sans" font-weight="{700 if bold else 400}" font-size="{size}" textLength="{int(tw*scale)}" lengthAdjust="spacingAndGlyphs" fill="{color}">{html.escape(text)}</text>')
# Fine circuit rails frame the canvas and leave the type area clear.
for x in range(70,1080,90):line([x,230,x,1660],'#07192B',1)
for yy in range(260,1680,90):line([64,yy,1016,yy],'#07192B',1)
line([54,1490,54,280,100,234,285,234],'#123D62',3)
line([1024,360,1024,1470,966,1528,966,1630,820,1776],'#176498',3)
line([1000,1310,1000,1450,940,1510,940,1600,806,1734],'#0B344F',2)
for x,y in [(100,234),(54,560),(1024,890),(966,1528),(806,1734)]:dot(x,y,4,'#00C8EF')
txt(96,190,'DB',45,'#00C8EF')
txt(196,207,'DIREITO + TECNOLOGIA',24,'#B4CCD8',bold=False)
line([96,295,285,295],'#00C8EF',4)
# Programmatic holographic sphere.
glow=Image.new('RGB',(W,H));gd=ImageDraw.Draw(glow)
cx,cy,rad=540,650,247
for radius in range(330,0,-4):
 intensity=max(0,int(12*(1-radius/334)))
 gd.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(0,intensity,intensity*2))
im=Image.blend(im,glow,.46);d=ImageDraw.Draw(im)
for rr in [285,260,235]:
 d.ellipse((cx-rr,cy+rad-23,cx+rr,cy+rad+28),outline='#0D5C82',width=2)
 svg.append(f'<ellipse cx="{cx}" cy="{cy+rad}" rx="{rr}" ry="25" fill="none" stroke="#0D5C82" stroke-width="2"/>')
rng=random.Random(26);nodes=[]
for k in range(130):
 z=rng.uniform(-1,1);ang=rng.uniform(0,2*math.pi);s=math.sqrt(1-z*z)
 nodes.append((cx+rad*s*math.cos(ang),cy+rad*z))
for i,(x,y) in enumerate(nodes):
 near=sorted(((math.hypot(x-xx,y-yy),j,xx,yy) for j,(xx,yy) in enumerate(nodes) if j!=i))[:3]
 for distance,j,xx,yy in near:
  if j>i and distance<108:line([x,y,xx,yy],'#146A92',1)
for x,y in nodes:
 dot(x,y,2,'#24B8E5')
for idx in [5,18,29,43,66,79,92,108]:
 x,y=nodes[idx]
 for rr,col in [(14,'#06334D'),(8,'#0B799C'),(4,'#A9F4FF')]:dot(x,y,rr,col)
 line([x-16,y,x+16,y],'#3EDDF8',1);line([x,y-16,x,y+16],'#3EDDF8',1)
txt(96,1000,'A IA EVOLUI.',100,scale=.86)
txt(96,1124,'SEUS DIREITOS',100,scale=.84)
txt(96,1248,'IMPORTAM.',110,'#00C8EF',scale=.86)
line([100,1425,236,1425],'#00C8EF',5)
txt(100,1470,'ENTENDA A TECNOLOGIA.',31,'#BDDAE6')
txt(100,1520,'CONHEÇA SEUS DIREITOS.',31,'#BDDAE6')
txt(100,1640,'@direitobinario',32,'#FFFFFF',bold=False)
txt(100,1710,'#DIREITODIGITAL  #IA',21,'#45A5C5',bold=False)
im.save(out/'story_teste.jpg',quality=95,subsampling=0)
(out/'story_teste.svg').write_text(''.join(svg)+'</svg>')
print(out/'story_teste.jpg')
