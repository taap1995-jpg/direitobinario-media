"""Render editorial Reels with visual QA preview."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAVY='#0A192F'; PANEL='#0D223B'; GOLD='#FFD700'; CYAN='#00E5FF'; WHITE='#FFFFFF'; SOFT='#C8D5E6'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
ROOT=Path(__file__).resolve().parents[1]
BEAT_PATH=ROOT/'file_000000001eb4820eaa383f6f71b23a8a.png'
W,H=1080,1920; LEFT=150; RIGHT=930; TOP=150; BOTTOM=1670

def run(args): subprocess.run(args,check=True)
def font(size,bold=True): return ImageFont.truetype(FB if bold else FR,size)
def text_w(f,s): return f.getlength(s)

def wrap_fit(text, start_size, max_width=780, min_size=32, max_lines=3, bold=True):
    words=text.split()
    for size in range(start_size,min_size-1,-2):
        f=font(size,bold); lines=[]; cur=''
        for word in words:
            cand=(cur+' '+word).strip()
            if text_w(f,cand)<=max_width or not cur: cur=cand
            else: lines.append(cur); cur=word
        if cur: lines.append(cur)
        if len(lines)<=max_lines and all(text_w(f,x)<=max_width for x in lines): return lines,f
    f=font(min_size,bold); lines=[]; cur=''
    for word in words:
        cand=(cur+' '+word).strip()
        if text_w(f,cand)<=max_width or not cur: cur=cand
        else: lines.append(cur); cur=word
    if cur: lines.append(cur)
    return lines,f

def draw_block(d,x,y,text,size,color,bold=True,max_width=780,max_lines=3,gap=12):
    lines,f=wrap_fit(text,size,max_width,32,max_lines,bold)
    bbox=f.getbbox('Ag'); lh=bbox[3]-bbox[1]+gap
    for line in lines:
        d.text((x,y),line,font=f,fill=color); y+=lh
    return y

def load_beat():
    if not BEAT_PATH.exists(): raise FileNotFoundError(f'BEAT not found: {BEAT_PATH}')
    src=Image.open(BEAT_PATH).convert('RGBA')
    # Official sheet: retain left-side mascot pose, then constrain to support-visual size.
    crop=src.crop((0,0,min(960,src.width),src.height))
    crop.thumbnail((300,300),Image.Resampling.LANCZOS)
    return crop

def scene_image(sc,idx,total,beat):
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    # Header / hook area.
    d.text((LEFT,TOP),'DB / DIREITO BINÁRIO',font=font(29),fill=GOLD)
    d.line((LEFT,TOP+60,RIGHT,TOP+60),fill=CYAN,width=3)
    y=TOP+115
    y=draw_block(d,LEFT,y,sc['kicker'],50,CYAN,True,780,2,10)+24
    headline=' '.join(sc.get('lines',[]))
    y=draw_block(d,LEFT,y,headline,78,WHITE,True,780,3,14)
    # Clean explanatory panel in center; no mascot or decorative bars behind it.
    panel_top=max(850,y+70); panel_bottom=1390
    d.rounded_rectangle((LEFT,panel_top,RIGHT,panel_bottom),radius=28,fill=PANEL,outline='#173A5E',width=2)
    note_y=panel_top+55
    draw_block(d,LEFT+45,note_y,sc.get('note',''),36,SOFT,False,690,6,10)
    # BEAT is a small support visual fixed bottom-right, outside text panel.
    bx=RIGHT-beat.width; by=1580-beat.height
    im.paste(beat,(bx,by),beat)
    d=ImageDraw.Draw(im)
    d.text((LEFT,1575),'@direitobinario',font=font(29),fill=GOLD)
    # Quiet progress indicator only; no waveform/audio bars.
    seg=780/total
    for k in range(total):
        x=LEFT+k*seg
        d.rounded_rectangle((x,1645,x+max(30,seg-12),1652),radius=3,fill=CYAN if k<=idx else '#263950')
    return im

def render(spec_path,preview_scene=None):
    sp=json.loads(Path(spec_path).read_text(encoding='utf-8')); slug=sp['slug']
    out=Path('media/reels')/slug; out.mkdir(parents=True,exist_ok=True); beat=load_beat()
    if preview_scene is not None:
        idx=preview_scene-1
        if idx<0 or idx>=len(sp['scenes']): raise ValueError('preview scene out of range')
        im=scene_image(sp['scenes'][idx],idx,len(sp['scenes']),beat)
        preview=Path('renders')/f'{slug}-qa-scene-{preview_scene:02d}.png'; preview.parent.mkdir(parents=True,exist_ok=True); im.save(preview)
        print(preview); return
    chunks=[]
    for idx,sc in enumerate(sp['scenes']):
        im=scene_image(sc,idx,len(sp['scenes']),beat); png=out/f'scene-{idx+1:02d}.png'; im.save(png)
        clip=out/f'clip-{idx+1:02d}.mp4'
        run(['ffmpeg','-y','-loop','1','-i',str(png),'-t',str(sc['seconds']),'-vf',"zoompan=z='min(zoom+0.0001,1.012)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30",'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-an',str(clip)])
        chunks.append(clip)
    lst=out/'concat.txt'; lst.write_text('\n'.join("file '"+c.name+"'" for c in chunks),encoding='utf-8')
    total=sum(x['seconds'] for x in sp['scenes']); video=out/'reel.mp4'
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(lst),'-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',str(total),'-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(video)])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    v=next(x for x in probe['streams'] if x['codec_type']=='video'); a=next(x for x in probe['streams'] if x['codec_type']=='audio')
    assert (v['width'],v['height'],v['codec_name'],v['pix_fmt'])==(1080,1920,'h264','yuv420p'); assert a['codec_name']=='aac'; assert 40<=float(probe['format']['duration'])<=50
    (out/'qa-technical.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
    for c in chunks: c.unlink()
    lst.unlink(); print(video)

if __name__=='__main__':
    preview=None
    if '--preview-scene' in sys.argv:
        i=sys.argv.index('--preview-scene'); preview=int(sys.argv[i+1]); del sys.argv[i:i+2]
    render(sys.argv[1],preview)
