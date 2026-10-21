#!/usr/bin/env python3
'Renderiza uma arte 1080x1350 (JPEG) a partir de um arquivo posts/<slug>.json.
Uso: python scripts/make_post_image.py posts/<slug>.json
Saida: posts/<slug>.jpg
'
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
NAVY = (14, 27, 56)
GOLD = (201, 162, 74)
WHITE = (250, 248, 242)
SOFT = (196, 205, 222)
F_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F_R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F_S = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'


def wrap(d, text, font, max_w):
    lines, line = [], ''
    for word in text.split():
        test = (line + ' ' + word).strip()
        if d.textlength(test, font=font) > max_w and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def render(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding='utf-8'))
    img = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.rectangle([48, 48, W - 48, H - 48], outline=GOLD, width=4)
    f_kicker = ImageFont.truetype(F_B, 34)
    f_title = ImageFont.truetype(F_S, 68)
    f_label = ImageFont.truetype(F_B, 30)
    f_body = ImageFont.truetype(F_R, 34)
    f_foot = ImageFont.truetype(F_B, 30)
    f_small = ImageFont.truetype(F_R, 26)
    x, max_w = 110, W - 220
    d.text((x, 120), spec['kicker'], font=f_kicker, fill=GOLD)
    y = 200
    for line in spec['title']:
        d.text((x, y), line, font=f_title, fill=WHITE)
        y += 100
    d.line([x, 420, W - 110, 420], fill=GOLD, width=3)
    y = 470
    for sec in spec['sections']:
        d.text((x, y), sec['label'].upper(), font=f_label, fill=GOLD)
        y += 48
        for line in wrap(d, sec['text'], f_body, max_w):
            d.text((x, y), line, font=f_body, fill=WHITE)
            y += 46
        y += 26
    d.text((x, H - 230), spec['footer_bold'], font=f_foot, fill=WHITE)
    d.text((x, H - 168), spec['source'], font=f_small, fill=SOFT)
    d.text((x, H - 120), spec['handle'], font=f_small, fill=GOLD)
    out = Path(spec_path).with_suffix('.jpg')
    img.save(out, 'JPEG', quality=92, optimize=True)
    print('Renderizado:', out)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Uso: python scripts/make_post_image.py posts/<slug>.json')
    render(sys.argv[1])
