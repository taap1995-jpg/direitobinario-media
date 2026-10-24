#!/usr/bin/env python3
"""Render branded Instagram artwork from posts/<slug>.json."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAVY=(10,22,40); GOLD=(201,168,76); WHITE=(250,248,242); SOFT=(196,205,222)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FS='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

def font(path, size): return ImageFont.truetype(path, size)

def render(spec_path):
    spec=json.loads(Path(spec_path).read_text(encoding='utf-8'))
    story=spec.get('format')=='story'
    W,H=(1080,1920) if story else (1080,1350)
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    if spec.get('template') == 'carousel_editorial':
        d.rectangle((48,48,W-48,H-48),outline=GOLD,width=4)
        d.text((100,115),spec['kicker'],font=font(FB,32),fill=GOLD)
        y=210
        for line in spec['title']:
            assert font(FS,60).getlength(line) <= 880
            d.text((100,y),line,font=font(FS,60),fill=WHITE)
            y+=82
        d.line((100,490,980,490),fill=GOLD,width=3)
        y=545
        for sec in spec['sections']:
            d.text((100,y),sec['label'].upper(),font=font(FB,32),fill=GOLD)
            y+=62
            words=sec['text'].replace('\n',' ').split()
            lines=[]; current=''
            for word in words:
                candidate=(current+' '+word).strip()
                if font(FR,43).getlength(candidate)>880:
                    lines.append(current); current=word
                else: current=candidate
            if current: lines.append(current)
            for line in lines:
                d.text((100,y),line,font=font(FR,43),fill=WHITE); y+=59
            y+=56
        assert y <= 1155, 'Texto excede o espaço da arte'
        d.text((100,1180),spec['footer_bold'],font=font(FB,30),fill=WHITE)
        d.text((100,1235),spec['source'],font=font(FR,22),fill=SOFT)
        d.text((100,1273),spec['handle'],font=font(FR,24),fill=GOLD)
        out=Path(spec_path).with_suffix('.jpg')
        im.save(out,'JPEG',quality=94,optimize=True)
        print(f'Renderizado: {out} ({W}x{H})')
        return
    if story and spec.get('template') == 'editorial':
        d.line((88,240,992,240),fill=GOLD,width=4)
        d.text((88,280),'DIREITO BINÁRIO',font=font(FB,30),fill=GOLD)
        d.text((88,395),spec['kicker'],font=font(FB,34),fill=SOFT)
        y=470
        for line in spec['title']:
            d.text((82,y),line,font=font(FB,82),fill=WHITE)
            y+=106
        d.rounded_rectangle((88,735,240,744),radius=4,fill=GOLD)
        y=820
        for sec in spec['sections']:
            d.text((88,y),sec['label'],font=font(FB,31),fill=GOLD)
            y+=65
            for line in sec['text'].splitlines():
                d.text((88,y),line,font=font(FR,43),fill=WHITE)
                y+=63
            y+=80
        d.text((88,1510),spec['footer_bold'],font=font(FB,48),fill=WHITE)
        d.text((88,1600),spec['source'],font=font(FR,27),fill=SOFT)
        d.text((88,1660),spec['handle'],font=font(FB,31),fill=GOLD)
        out=Path(spec_path).with_suffix('.jpg')
        im.save(out,'JPEG',quality=94,optimize=True)
        print(f'Renderizado: {out} ({W}x{H})')
        return
    if story:
        for y in range(H):
            t=y/H
            c=tuple(int(NAVY[i]*(1-t)+((16,35,61)[i])*t) for i in range(3))
            d.line((0,y,W,y),fill=c)
        d.rectangle((76,142,W-76,146),fill=GOLD)
        d.text((78,190),'DIREITO BINÁRIO',font=font(FB,27),fill=GOLD)
        d.text((78,244),'IA  •  PRIVACIDADE',font=font(FB,19),fill=SOFT)
        d.ellipse((760,600,1300,1140),outline=(42,61,82),width=3)
        d.ellipse((835,675,1225,1065),outline=(58,69,82),width=2)
        d.text((78,500),'ANTES DE COLAR UM PROMPT',font=font(FB,23),fill=GOLD)
        d.text((70,590),'IA NO',font=font(FB,112),fill=WHITE,stroke_width=1)
        d.text((70,725),'TRABALHO?',font=font(FB,100),fill=GOLD,stroke_width=1)
        d.rounded_rectangle((78,900,220,910),radius=4,fill=GOLD)
        d.text((78,1000),'DADO CONFIDENCIAL,',font=font(FB,49),fill=WHITE)
        d.text((78,1070),'NÃO.',font=font(FB,106),fill=GOLD)
        d.text((78,1240),'Proteja informações pessoais',font=font(FR,34),fill=SOFT)
        d.text((78,1290),'e de clientes.',font=font(FR,34),fill=SOFT)
        d.line((78,1740,W-78,1740),fill=GOLD,width=2)
        d.text((78,1780),'TECNOLOGIA COM RESPONSABILIDADE',font=font(FB,18),fill=SOFT)
        d.text((78,1822),'@DIREITOBINARIO',font=font(FB,20),fill=GOLD)
    else:
        d.rectangle([48,48,W-48,H-48],outline=GOLD,width=4)
        x=110; max_w=W-220
        d.text((x,120),spec['kicker'],font=font(FB,34),fill=GOLD)
        title=spec['title']
        title_size=68 if len(title)<=2 else 60
        line_height=82 if len(title)>2 else 100
        y=200
        for line in title:
            d.text((x,y),line,font=font(FS,title_size),fill=WHITE)
            y+=line_height
        divider_y=max(420,y+18)
        d.line([x,divider_y,W-x,divider_y],fill=GOLD,width=3); y=divider_y+48
        for sec in spec['sections']:
            d.text((x,y),sec['label'].upper(),font=font(FB,30),fill=GOLD); y+=48
            for line in sec['text'].splitlines():
                d.text((x,y),line,font=font(FR,32),fill=WHITE); y+=44
            y+=25
        d.text((x,H-170),spec['footer_bold'],font=font(FB,30),fill=WHITE)
        d.text((x,H-120),spec.get('source',''),font=font(FR,22),fill=SOFT)
        d.text((x,H-80),spec['handle'],font=font(FR,24),fill=GOLD)
    out=Path(spec_path).with_suffix('.jpg')
    im.save(out,'JPEG',quality=94,optimize=True)
    print(f'Renderizado: {out} ({W}x{H})')

if __name__=='__main__':
    if len(sys.argv)!=2: sys.exit('Uso: python scripts/make_post_image.py posts/<slug>.json')
    render(sys.argv[1])
