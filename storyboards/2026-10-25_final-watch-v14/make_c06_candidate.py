"""Move one postproduction caption to the visible bag handoff. No Flow generation."""
from pathlib import Path
import sys,json,subprocess,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
Q=Path(__file__).resolve().parent;SB=Q.parent;O=Q/'C06';O.mkdir(exist_ok=True)
SRC=SB/'2026-10-25_final-six-v13/C06/C06_Q-AI_Fair_final_v13.mp4'
RAW=SB/'2026-10-23_C06-C05-flow-run01/C06_K02_take01.mp4'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
DST=O/'C06_Q-AI_Fair_final_v14.mp4';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_hashes={str(p):sha(p) for p in [SRC,RAW]}
raw={}
with av.open(str(RAW)) as c:
 for i,f in enumerate(c.decode(video=0)):
  if 102<=i<180:raw[i]=f.to_ndarray(format='rgb24')
# V13 sorting cut uses RAW4.25..7.5. Check uncaptained start matches before replacing it.
with av.open(str(SRC)) as c:
 for i,f in enumerate(c.decode(video=0)):
  if i==156:
   delta=float(np.abs(f.to_ndarray(format='rgb24').astype(np.int16)-raw[102].astype(np.int16)).mean());break
assert delta<6, f'Sorting source/frame alignment is not confirmed: {delta}'
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',42)
cmd=[str(FF),'-hide_banner','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','pipe:0','-i',str(SRC),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','slow','-pix_fmt','yuv420p','-c:a','copy','-t','48.75','-movflags','+faststart',str(DST)]
log=(O/'render.log').open('wb');p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
with av.open(str(SRC)) as c:
 for i,f in enumerate(c.decode(video=0)):
  im=Image.fromarray(raw[102+i-156]) if 156<=i<234 else f.to_image()
  if 78<=i<114:
   layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer);text='고마워요.';bb=d.textbbox((0,0),text,font=font);tw=bb[2]-bb[0];x=(1280-tw)//2;y=633
   d.rounded_rectangle((x-22,y-10,x+tw+22,y+59),radius=9,fill=(8,18,25,220));d.text((x,y-bb[1]+2),text,font=font,fill='white')
   im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
  p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0;log.close()
r=subprocess.run([str(FF),'-v','error','-i',str(DST),'-f','null','-'],capture_output=True);assert r.returncode==0,r.stderr
for fn,h in source_hashes.items():assert sha(Path(fn))==h
ed=json.loads((SRC.parent/'edit_manifest.json').read_text(encoding='utf-8'))
for cap in ed.get('captions',[]):
 if cap.get('text')=='고마워요.':cap.update(start=3.25,end=4.75,old_start=7.75,old_end=9.55)
ed.update(file=DST.name,final_sha256=sha(DST),status='CANDIDATE_PENDING_THREE_RECHECK',parent_version=str(SRC),parent_sha256=source_hashes[str(SRC)],
 change='Only the postproduction thank-you caption moves7.75-9.55s to3.25-4.75s, beside bag handoff. Sorting source remains RAW4.25-7.5s, same framing and timing; no crop.',
 audio_change='V13 AAC stream copied without encoding; BGM and effects timing unchanged; no source speech.',source_alignment_mean_abs_rgb_delta=delta,
 actual_continuous_playback_verified=False,actual_listening_verified=False)
ed.pop('final_review_record',None)
(O/'edit_manifest.json').write_text(json.dumps(ed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'file':str(DST),'source_alignment_delta':delta,'sha256':sha(DST)},ensure_ascii=False),flush=True)
