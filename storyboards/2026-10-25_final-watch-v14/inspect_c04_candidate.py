from pathlib import Path
import sys,json,math,hashlib,subprocess,re
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
Q=Path(__file__).resolve().parent;O=Q/'C04';P=O/'C04_Q-AI_Fair_final_v14.mp4'
F=O/'frames';F.mkdir(exist_ok=True);C=O/'contacts';C.mkdir(exist_ok=True)
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
ed=json.loads((O/'edit_manifest.json').read_text(encoding='utf-8'))
targets=set(range(0,1044,12))|set(range(72,169,6))|{1043}
joins={}
for n,t in enumerate([3,7]+[x['start'] for x in ed['timeline'][2:]],1):
 idx=round(t*24);ids=[x for x in range(idx-2,idx+3) if 0<=x<1044]
 joins[f'J{n:02}_{t:06.3f}']=ids;targets.update(ids)
written={};pts=[]
with av.open(str(P)) as ct:
 for i,fr in enumerate(ct.decode(video=0)):
  ts=float(fr.pts*fr.time_base);pts.append(ts)
  if i in targets:
   p=F/f'{i:04}_{ts:07.3f}.png';fr.to_image().save(p);written[i]=p
assert len(pts)==1044
assert all(abs(b-a-1/24)<1e-5 for a,b in zip(pts,pts[1:]))
def sheet(ids,path,cols=3,w=480):
 h=round(w*9/16);ch=h+28;can=Image.new('RGB',(cols*w,math.ceil(len(ids)/cols)*ch),(15,18,23));d=ImageDraw.Draw(can)
 for n,i in enumerate(ids):
  im=Image.open(written[i]).resize((w,h));x=n%cols*w;y=n//cols*ch;can.paste(im,(x,y+28));d.text((x+5,y+2),f'C04 V14 {i/24:.3f}s | f{i}',font=FONT,fill='white')
 can.save(path,quality=93)
seq=[x for x in sorted(written) if x%12==0 or x==1043]
for n in range(0,len(seq),12):sheet(seq[n:n+12],C/f'sequence_{n//12+1:02}.jpg')
for name,ids in joins.items():sheet(ids,C/f'{name}.jpg',5,384)
ids=list(range(72,169,6))
for n in range(0,len(ids),12):sheet(ids[n:n+12],C/f'note_detail_{n//12+1:02}.jpg')
ff=Q.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
p=subprocess.run([str(ff),'-hide_banner','-i',str(P),'-af','loudnorm=I=-23:TP=-3:LRA=11:print_format=json','-f','null','-'],capture_output=True)
assert p.returncode==0
ln=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr.decode(errors='replace'))[-1])
qa={'file':str(P),'sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'frames':len(pts),'duration_seconds':43.5,'resolution':[1280,720],'fps':24,'pts_gaps':0,'full_decode':'PASS','loudness':{k:v for k,v in ln.items() if k.startswith('input_')},'audio_listening_verified':False,'actual_continuous_playback_verified':False,'method':'Fresh final decoded frames every0.5s,NOTE every0.25s,joins -2 through+2frames','caption_note_duration':ed['captions'][2]['end']-ed['captions'][2]['start']}
(O/'technical_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False),flush=True)
