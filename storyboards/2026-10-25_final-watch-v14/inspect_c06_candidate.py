from pathlib import Path
import sys,json,math,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
Q=Path(__file__).resolve().parent;O=Q/'C06';P=O/'C06_Q-AI_Fair_final_v14.mp4'
SRC=Q.parent/'2026-10-25_final-six-v13/C06/C06_Q-AI_Fair_final_v13.mp4'
F=O/'frames';F.mkdir(exist_ok=True);C=O/'contacts';C.mkdir(exist_ok=True)
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
ed=json.loads((O/'edit_manifest.json').read_text(encoding='utf-8'))
targets=set(range(0,1170,12))|set(range(60,240,6))|{1169};joins={}
for n,t in enumerate(sorted({3.25,4.75,6.5,7.75,9.55,9.75}|{x['start'] for x in ed['timeline'][1:]}),1):
 idx=round(t*24);ids=[x for x in range(idx-2,idx+3) if 0<=x<1170];joins[f'J{n:02}_{t:06.3f}']=ids;targets.update(ids)
written={};pts=[]
with av.open(str(P)) as ct:
 for i,fr in enumerate(ct.decode(video=0)):
  ts=float(fr.pts*fr.time_base);pts.append(ts)
  if i in targets:
   p=F/f'{i:04}_{ts:07.3f}.png';fr.to_image().save(p);written[i]=p
assert len(pts)==1170
assert all(abs(b-a-1/24)<1e-5 for a,b in zip(pts,pts[1:]))
def sheet(ids,path,cols=3,w=480):
 h=round(w*9/16);ch=h+28;can=Image.new('RGB',(cols*w,math.ceil(len(ids)/cols)*ch),(15,18,23));d=ImageDraw.Draw(can)
 for n,i in enumerate(ids):
  im=Image.open(written[i]).resize((w,h));x=n%cols*w;y=n//cols*ch;can.paste(im,(x,y+28));d.text((x+5,y+2),f'C06 V14 {i/24:.3f}s | f{i}',font=FONT,fill='white')
 can.save(path,quality=93)
seq=[x for x in sorted(written) if x%12==0 or x==1169]
for n in range(0,len(seq),12):sheet(seq[n:n+12],C/f'sequence_{n//12+1:02}.jpg')
for name,ids in joins.items():sheet(ids,C/f'{name}.jpg',5,384)
ids=list(range(60,240,6))
for n in range(0,len(ids),12):sheet(ids[n:n+12],C/f'caption_detail_{n//12+1:02}.jpg')
def packet_sha(p):
 h=hashlib.sha256();n=0
 with av.open(str(p)) as c:
  for pa in c.demux(audio=0):
   if pa.size:h.update(bytes(pa));n+=1
 return {'sha256':h.hexdigest(),'packets':n}
old=packet_sha(SRC);new=packet_sha(P);assert old==new
peak=0.;audioend=0.;gaps=[]
with av.open(str(P)) as c:
 for f in c.decode(audio=0):
  a=f.to_ndarray();assert np.isfinite(a).all();peak=max(peak,float(np.abs(a).max()));t=float(f.pts*f.time_base);gaps.append(t-audioend);audioend=t+f.samples/f.sample_rate
qa={'file':str(P),'sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'frames':len(pts),'duration_seconds':48.75,'resolution':[1280,720],'fps':24,'pts_gaps':0,'full_decode':'PASS','audio_packets_identical_to_v13':old,'audio_peak':peak,'max_audio_pts_gap_seconds':max(abs(x) for x in gaps),'audio_listening_verified':False,'actual_continuous_playback_verified':False,'method':'Fresh final decoded frames every0.5s,changed caption sequence every0.25s,joins -2 through+2frames','caption_moved':[3.25,4.75],'old_caption_removed':[7.75,9.55]}
(O/'technical_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
srt=(SRC.parent/'source_C06_captions.srt').read_text(encoding='utf-8').replace('00:00:07,750 --> 00:00:09,550','00:00:03,250 --> 00:00:04,750')
(O/'C06_captions.srt').write_text(srt,encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False),flush=True)
