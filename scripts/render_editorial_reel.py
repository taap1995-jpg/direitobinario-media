"""Render editorial Reels from verified, versioned scene specifications."""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAVY='#0A1628'; GOLD='#C9A84C'; WHITE='#FAF8F2'; SOFT='#BCC9DA'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
ROOT=Path(__file__).resolve().parents[1]
BEAT_PATH=ROOT/'file_000000001eb4820eaa383f6f71b23a8a.png'

def run(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def fit_lines(s, size=72, max_width=860, min_size=32, bold=True):
    font_path=FB if bold else FR
    words=s.split()
    if not words:
        return [''], ImageFont.truetype(font_path,size)
    for candidate_size in range(size,min_size-1,-2):
        f=ImageFont.truetype(font_path,candidate_size)
        lines=[]; cur=''
        for word in words:
            cand=(cur+' '+word).strip()
            if f.getlength(cand)<=max_width:
                cur=cand
            else:
                if cur: lines.append(cur)
                cur=word
        if cur: lines.append(cur)
        if all(f.getlength(line)<=max_width for line in lines) and len(lines)<=2:
            return lines,f
    f=ImageFont.truetype(font_path,min_size)
    lines=[]; cur=''
    for word in words:
        cand=(cur+' '+word).strip()
        if f.getlength(cand)<=max_width or not cur:
            cur=cand
        else:
            lines.append(cur); cur=word
    if cur: lines.append(cur)
    return lines,f

def draw_wrapped(d,x,y,s,size=72,color=WHITE,bold=True,max_width=860,line_gap=10):
    lines,f=fit_lines(s,size,max_width,32,bold)
    bbox=f.getbbox('Ag')
    line_h=(bbox[3]-bbox[1])+line_gap
    for n,line in enumerate(lines):
        d.text((x,y+n*line_h),line,font=f,fill=color)
    return y+len(lines)*line_h

def load_beat():
    if not BEAT_PATH.exists():
        raise FileNotFoundError(f'Official BEAT asset not found: {BEAT_PATH}')
    src=Image.open(BEAT_PATH).convert('RGB')
    # Official source is a character sheet. Use the large left-side BEAT pose.
    crop=src.crop((0,0,min(960,src.width),src.height))
    crop.thumbnail((680,725),Image.Resampling.LANCZOS)
    return crop

def render(spec_path):
    sp=json.loads(Path(spec_path).read_text(encoding='utf-8'))
    slug=sp['slug']
    assert all(c.isalnum() or c=='-' for c in slug)
    out=Path('media/reels')/slug;out.mkdir(parents=True,exist_ok=True)
    beat=load_beat()
    chunks=[]
    for idx,sc in enumerate(sp['scenes']):
        im=Image.new('RGB',(1080,1920),NAVY);d=ImageDraw.Draw(im)
        d.line((150,265,930,265),fill=GOLD,width=4)
        draw_wrapped(d,150,302,'DIREITO BINÁRIO',29,GOLD,True,780)
        draw_wrapped(d,150,442,sc['kicker'],32,SOFT,True,780)
        y=590
        for line in sc['lines']:
            y=draw_wrapped(d,150,y,line,68 if len(sc['lines'])>3 else 78,WHITE,True,780,12)+18
        # BEAT is composed from the repository-local official asset on every scene.
        bx=540-beat.width//2
        by=880
        im.paste(beat,(bx,by))
        d=ImageDraw.Draw(im)
        for i in range(39):
            height=18+int(65*abs(math.sin(i*.42))*math.exp(-((i-19)/15)**2))
            x=150+i*20
            d.rounded_rectangle((x,1190-height,x+7,1190+height),radius=3,fill=GOLD)
        note=sc['note']; f=ImageFont.truetype(FR,33)
        words=note.split();lines=[];cur=''
        for word in words:
            cand=(cur+' '+word).strip()
            if f.getlength(cand)>780 and cur:
                lines.append(cur);cur=word
            else: cur=cand
        if cur:lines.append(cur)
        for n,line in enumerate(lines[:3]):
            draw_wrapped(d,150,1330+n*48,line,33,SOFT,False,780,5)
        draw_wrapped(d,150,1530,'@direitobinario',30,GOLD,True,780)
        for k in range(len(sp['scenes'])):
            x=150+k*(780/len(sp['scenes']))
            d.rounded_rectangle((x,1630,x+80,1637),radius=3,fill=GOLD if k<=idx else '#263950')
        png=out/f'scene-{idx+1:02d}.png';im.save(png)
        if idx==0:im.save(out/'cover.jpg',quality=94)
        clip=out/f'clip-{idx+1:02d}.mp4'
        run(['ffmpeg','-y','-loop','1','-i',str(png),'-t',str(sc['seconds']),'-vf',"zoompan=z='min(zoom+0.0001,1.018)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30",'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-an',str(clip)])
        chunks.append(clip)
    lst=out/'concat.txt';lst.write_text('\n'.join("file '"+c.name+"'" for c in chunks),encoding='utf-8')
    total=sum(x['seconds'] for x in sp['scenes'])
    video=out/'reel.mp4'
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(lst),'-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',str(total),'-c:v','copy','-c:a','aac','-b:a','128k','-movflags','+faststart',str(video)])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    v=next(x for x in probe['streams'] if x['codec_type']=='video')
    a=next(x for x in probe['streams'] if x['codec_type']=='audio')
    assert (v['width'],v['height'],v['codec_name'],v['pix_fmt'])==(1080,1920,'h264','yuv420p')
    assert a['codec_name']=='aac'
    assert abs(float(probe['format']['duration'])-total)<.2
    assert video.stat().st_size<90000000
    (out/'qa-technical.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
    for c in chunks:c.unlink()
    lst.unlink()
    print(video)

if __name__=='__main__':render(sys.argv[1])
