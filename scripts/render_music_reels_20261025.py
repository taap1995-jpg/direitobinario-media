"""Render approved editorial Reels with original instrumental music and no voice."""
import json, math, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'editorial/days/2026-10-25/music-reels.json'
NAVY='#0A1628';GOLD='#C9A84C';WHITE='#FAF8F2';SOFT='#BCC9DA'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def run(args):
 result=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if result.returncode:raise RuntimeError(result.stderr.decode(errors='replace')[-4000:])

def music(path,duration,seed):
 sr=44100;n=int(duration*sr);audio=np.zeros((n,2),np.float64)
 beat=60/88;rng=np.random.default_rng(seed)
 def note(start,length,midi,volume,pan=0,soft=False):
  begin=int(start*sr);count=min(int(length*sr),n-begin)
  if count<=0:return
  t=np.arange(count)/sr;freq=440*2**((midi-69)/12)
  env=(1-np.exp(-t/(.09 if soft else .012)))*np.exp(-t/(length*.6))
  env*=np.minimum(1,(length-t)/.15)
  sound=(np.sin(2*np.pi*freq*t)+.2*np.sin(2*np.pi*freq*2*t)+.06*np.sin(2*np.pi*freq*3*t))*env*volume
  audio[begin:begin+count,0]+=sound*math.sqrt((1-pan)/2)
  audio[begin:begin+count,1]+=sound*math.sqrt((1+pan)/2)
 chords=[(45,57,60,64),(41,53,57,60),(48,55,60,64),(43,55,59,62)]
 for bar,start in enumerate(np.arange(0,duration,beat*4)):
  chord=chords[bar%4]
  for j,pitch in enumerate(chord):note(start,beat*4+.1,pitch,.065,-.35+j*.22,True)
  for step in range(8):note(start+step*beat/2,beat*.95,chord[1+step%3]+12,.04,(-1)**step*.28)
  for pulse in [0,2]:
   begin=int((start+pulse*beat)*sr);count=min(int(.15*sr),n-begin)
   if count>0:
    t=np.arange(count)/sr;sound=np.sin(2*np.pi*(50*t+3*(1-np.exp(-t*30))))*np.exp(-t*28)*.055
    audio[begin:begin+count]+=sound[:,None]
 peak=float(np.max(np.abs(audio)));audio*=.28/max(peak,1e-8)
 fade=np.minimum(1,np.arange(n)/sr/.8)*np.minimum(1,(n-1-np.arange(n))/sr/1.5)
 audio*=fade[:,None];rms=float(np.sqrt(np.mean(audio**2)));assert rms>.01
 pcm=(np.clip(audio,-1,1)*32767).astype('<i2')
 with wave.open(str(path),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
 return {'type':'original_instrumental_synthesis','narration':False,'samples_from_third_parties':False,'bpm':88,'rms':rms,'peak':float(np.max(np.abs(audio)))}

def render(item):
 slug=item['id'];assert all(c.isalnum() or c=='-' for c in slug)
 out=ROOT/'media/reels'/slug;out.mkdir(parents=True,exist_ok=True)
 clips=[];total=sum(s['seconds'] for s in item['music_scenes'])
 for index,scene in enumerate(item['music_scenes']):
  im=Image.new('RGB',(1080,1920),NAVY);draw=ImageDraw.Draw(im)
  def text(x,y,value,size=64,color=WHITE,bold=True):
   f=ImageFont.truetype(FB if bold else FR,size)
   while f.getlength(value)>875 and size>40:size-=1;f=ImageFont.truetype(FB if bold else FR,size)
   assert f.getlength(value)<=875,(value,size)
   draw.text((x,y),value,font=f,fill=color)
  draw.line((100,270,980,270),fill=GOLD,width=4)
  text(100,310,'DIREITO BINÁRIO',30,GOLD)
  text(100,440,item['kicker'],32,SOFT)
  y=580
  for line in scene['lines']:text(100,y,line,72);y+=100
  draw.line((100,960,250,960),fill=GOLD,width=6)
  f=ImageFont.truetype(FR,42);lines=[];current=''
  for word in scene['detail'].split():
   candidate=(current+' '+word).strip()
   if f.getlength(candidate)>870:lines.append(current);current=word
   else:current=candidate
  if current:lines.append(current)
  assert len(lines)<=5
  for j,line in enumerate(lines):text(100,1040+j*62,line,42,SOFT,False)
  text(100,1460,item['source_label'],28,SOFT,False)
  text(100,1535,'@direitobinario',31,GOLD)
  for k in range(len(item['music_scenes'])):
   x=100+k*220;draw.rounded_rectangle((x,1630,x+190,1638),radius=3,fill=GOLD if k<=index else '#263950')
  png=out/f'scene-{index+1:02d}.png';im.save(png)
  if index==0:im.save(out/'cover.jpg',quality=94)
  clip=out/f'part-{index+1:02d}.mp4'
  run(['ffmpeg','-y','-loop','1','-i',str(png),'-t',str(scene['seconds']),'-vf',"zoompan=z='min(zoom+0.000035,1.012)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30",'-c:v','libx264','-threads','2','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p','-an',str(clip)])
  clips.append(clip)
 lst=out/'concat.txt';lst.write_text('\n'.join("file '"+p.name+"'" for p in clips))
 wav=out/'music-original.wav';audio_qa=music(wav,total,item['topic_id'])
 video=out/'music-reel.mp4'
 run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(wav),'-t',str(total),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(video)])
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
 vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (vs['width'],vs['height'],vs['codec_name'],vs['pix_fmt'])==(1080,1920,'h264','yuv420p')
 assert au['codec_name']=='aac' and abs(float(probe['format']['duration'])-total)<.2
 assert video.stat().st_size<90000000
 qa={'duration':total,'width':1080,'height':1920,'fps':30,'video_codec':'h264','audio_codec':'aac','music':audio_qa,'bytes':video.stat().st_size,'spoken_audio':False}
 (out/'qa-music.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
 for p in clips+[wav,lst]:p.unlink()
 print(json.dumps({'video':str(video.relative_to(ROOT)),'qa':qa}),flush=True)

if __name__=='__main__':
 for approved in json.loads(SPEC.read_text()):render(approved)
