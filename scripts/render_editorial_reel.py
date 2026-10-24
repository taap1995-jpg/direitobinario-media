"""Render editorial Reels from verified, versioned scene specifications."""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
NAVY='#0A1628'; GOLD='#C9A84C'; WHITE='#FAF8F2'; SOFT='#BCC9DA'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def run(args): subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def render(spec_path):
    sp=json.loads(Path(spec_path).read_text(encoding='utf-8'))
    slug=sp['slug']
    assert all(c.isalnum() or c=='-' for c in slug)
    out=Path('media/reels')/slug;out.mkdir(parents=True,exist_ok=True)
    chunks=[]
    for idx,sc in enumerate(sp['scenes']):
        im=Image.new('RGB',(1080,1920),NAVY);d=ImageDraw.Draw(im)
        def text(x,y,s,size=72,color=WHITE,bold=True):
            f=ImageFont.truetype(FB if bold else FR,size)
            while f.getlength(s)>860 and size>48:
                size-=2; f=ImageFont.truetype(FB if bold else FR,size)
            assert f.getlength(s)<=860,(s,size)
            d.text((x,y),s,font=f,fill=color)
        d.line((100,265,980,265),fill=GOLD,width=4)
        text(100,302,'DIREITO BINÁRIO',29,GOLD)
        text(100,442,sc['kicker'],32,SOFT)
        y=590
        for line in sc['lines']:
            text(95,y,line,68 if len(sc['lines'])>3 else 78);y+=108
        for i in range(41):
            height=22+int(85*abs(math.sin(i*.42))*math.exp(-((i-20)/15)**2))
            x=105+i*20
            d.rounded_rectangle((x,1140-height,x+7,1140+height),radius=3,fill=GOLD)
        note=sc['note'];f=ImageFont.truetype(FR,33)
        words=note.split();lines=[];cur=''
        for word in words:
            cand=(cur+' '+word).strip()
            if f.getlength(cand)>850:lines.append(cur);cur=word
            else:cur=cand
        if cur:lines.append(cur)
        for n,line in enumerate(lines):text(100,1330+n*48,line,33,SOFT,False)
        text(100,1530,'@direitobinario',30,GOLD)
        for k in range(len(sp['scenes'])):
            x=100+k*(880/len(sp['scenes']))
            d.rounded_rectangle((x,1630,x+100,1637),radius=3,fill=GOLD if k<=idx else '#263950')
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
    assert (v['width'],v['height'],v['codec_name'],v['pix_fmt'])==(1080,1920,'h264','yuv420p')
    assert abs(float(probe['format']['duration'])-total)<.2
    assert video.stat().st_size<90000000
    (out/'qa-technical.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
    for c in chunks:c.unlink()
    lst.unlink()
    print(video)
if __name__=='__main__':render(sys.argv[1])
