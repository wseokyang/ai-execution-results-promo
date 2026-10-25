from pathlib import Path
import json,hashlib,shutil,sys,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;SB=P.parent;out=P/'C06';out.mkdir(exist_ok=True)
old=SB/'2026-10-25_C06-impact-edit-v06';src=old/'C06_Q-AI_Fair_edit_v06.mp4';dst=out/'C06_Q-AI_Fair_final_v13.mp4'
shutil.copyfile(src,dst);assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(dst.read_bytes()).digest()
font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',18)
thumbs=[];pts=[]
with av.open(str(dst)) as c:
 for i,f in enumerate(c.decode(video=0)):
  pts.append(float(f.time))
  if i%12==0 or i==1169:
   im=Image.new('RGB',(320,204),(14,21,30));im.paste(f.to_image().resize((320,180)),(0,24));ImageDraw.Draw(im).text((6,1),f'{i/24:.3f}s',font=font,fill='white');thumbs.append(im)
audio_count=0;ends=[];starts=[]
with av.open(str(dst)) as c:
 for f in c.decode(audio=0):
  starts.append(float(f.time));ends.append(float(f.time)+f.samples/f.sample_rate);audio_count+=1
assert len(pts)==1170 and np.allclose(np.diff(pts),1/24,atol=1e-6)
assert max(abs(starts[i]-ends[i-1]) for i in range(1,len(starts)))<.0001
for n in range(math.ceil(len(thumbs)/20)):
 part=thumbs[n*20:(n+1)*20];im=Image.new('RGB',(1280,204*math.ceil(len(part)/4)),(14,21,30))
 for j,t in enumerate(part):im.paste(t,((j%4)*320,(j//4)*204))
 im.save(out/f'review_contact_{n+1:02d}.jpg',quality=94)
rec={'file':dst.name,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size,'duration':48.75,'frames':len(pts),'fps':24,'resolution':[1280,720],'full_video_audio_decode':'PASS','audio_frames':audio_count,'audio_pts_gaps':'NONE','source':str(src.relative_to(SB)),'byte_identical_to_previous_v06':True,'change':'No new C06 motion needed. Previously repaired impact and synchronized effect preserved. Repackaged without re-encoding.','review_scope':'Technical decode and new0.5scontact sheets; fresh independent final review pending','actual_listening':False}
(out/'technical_validation.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for n in ['edit_manifest.json','C06_captions.srt']:
 if (old/n).exists():shutil.copyfile(old/n,out/('source_'+n))
print(rec)
