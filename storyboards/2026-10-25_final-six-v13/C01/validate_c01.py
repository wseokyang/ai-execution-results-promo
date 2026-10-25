from pathlib import Path
import sys,json,math,subprocess,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
from render_c01 import OUT,SB,FF,FPS,SR,dump,sha
p=OUT/('C01_front_review.mp4' if '--front' in sys.argv else 'C01_Q-AI_Fair_final_v13.mp4')
man=json.loads((OUT/'edit_manifest.json').read_text(encoding='utf-8'));dur=man['duration_seconds'];expected=round(dur*FPS);samples=set(range(0,expected,6))|{expected-1}
for seg in man['timeline']:
 i=round(seg['start']*FPS);samples|={i-1,i,i+1}
frames=OUT/('front_review_frames' if '--front' in sys.argv else 'review_frames');frames.mkdir(exist_ok=True);tiles=[];pts=[]
with av.open(str(p)) as c:
 audio_count=len(c.streams.audio)
 for i,f in enumerate(c.decode(video=0)):
  pts.append(float(f.time))
  if i in samples:
   im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png');card=Image.new('RGB',(320,205),(16,23,29));card.paste(im.resize((320,180)),(0,25));ImageDraw.Draw(card).text((6,4),f'{i/FPS:.3f} s',font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',15),fill='white');tiles.append(card)
assert len(pts)==expected and np.allclose(np.diff(pts),1/FPS)
for j in range(math.ceil(len(tiles)/20)):
 batch=tiles[j*20:j*20+20];sheet=Image.new('RGB',(1280,205*math.ceil(len(batch)/4)),(16,23,29))
 for k,im in enumerate(batch):sheet.paste(im,(k%4*320,k//4*205))
 sheet.save(OUT/f'{"front_" if "--front" in sys.argv else ""}review_contact_{j+1:02d}.jpg',quality=94)
proc=subprocess.run([str(FF),'-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert proc.returncode==0,proc.stderr
source_unchanged=all(sha(SB/name)==h for name,h in man['source_sha256'].items());assert source_unchanged
astats={}
if audio_count:
 a=np.frombuffer(subprocess.run([str(FF),'-v','error','-i',str(p),'-vn','-f','f32le','-ar',str(SR),'-ac','2','-'],capture_output=True).stdout,np.float32).reshape(-1,2)
 assert np.isfinite(a).all() and np.abs(a).max()<1
 end=0;gaps=[];total=0
 with av.open(str(p)) as c:
  for f in c.decode(audio=0):gaps.append(float(f.time)-end);end=float(f.time)+f.samples/f.sample_rate;total+=f.samples
 assert max(abs(g) for g in gaps)<1/SR
 astats=dict(audio_peak=float(np.abs(a).max()),audio_end=end,audio_timeline_samples=total,max_audio_pts_gap_seconds=max(abs(g) for g in gaps),actual_listening_verified=False)
dump(OUT/('front_technical_validation.json' if '--front' in sys.argv else 'technical_validation.json'),dict(file=p.name,sha256=sha(p),bytes=p.stat().st_size,duration_seconds=dur,frames=expected,dimensions=[1280,720],fps=24,full_decode='PASS',source_sha256_unchanged=source_unchanged,video_pts='constant1/24s',audio_streams=audio_count,continuous_full_playback_verified=False,**astats))
print('QA',p.name,dur,expected,astats,flush=True)
