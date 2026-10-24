from pathlib import Path
import sys, json, hashlib, subprocess, math
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=Path(__file__).resolve().parent
SB=OUT.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
BASE=SB/'2026-10-23_C05-C06-edit-v04/C06/C06_Q-AI_Fair_edit_v04.mp4'
RAW=SB/'2026-10-23_C06-C05-flow-run01/C06_K03_take01.mp4'
ART=SB/'2026-10-23_C05-C06-edit-v03/graphics/C06_projector.png'
FPS,W,H=24,1280,720
START,END=9.88,14.0
NEW='퇴근시키려면,\n일을 끝내줘야겠네.'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace'))
 return p
# The v03 original projector composite and caption geometry are reused verbatim.
def font(s): return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',s)
def warp(art,quad):
 mat=[];vec=[]
 for (x,y),(u,v) in zip(quad,[(0,0),(art.width,0),(art.width,art.height),(0,art.height)]):
  mat.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);vec.extend([u,v])
 return art.transform((W,H),Image.Transform.PERSPECTIVE,np.linalg.solve(np.array(mat),np.array(vec)),Image.Resampling.BICUBIC)
def caption(tx):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);lines=tx.split('\n');size=42
 tw=max(d.textlength(x,font=font(size)) for x in lines);hh=len(lines)*55+20
 x=(W-tw)/2;y=H-48-hh
 d.rounded_rectangle((x-23,y,x+tw+23,y+hh),12,fill=(7,14,22,218))
 for j,line in enumerate(lines): d.text((x+tw/2,y+10+j*55+25),line,font=font(size),fill='white',anchor='mm')
 return im
hashes={str(x.relative_to(SB)):sha(x) for x in (BASE,RAW,ART)}
projector=warp(Image.open(ART).convert('RGBA'),[(676,101),(1234,44),(1234,277),(676,302)])
cap=caption(NEW);cap.save(OUT/'replacement_caption.png')
raw_frames={}
with av.open(str(RAW)) as c:
 for i,f in enumerate(c.decode(video=0)):
  st=i/FPS;t=9.75+st-1.25
  if START<=t<END:
   im=f.to_image().convert('RGBA');im.alpha_composite(projector);im.alpha_composite(cap)
   raw_frames[round(t*FPS)]=im.convert('RGB')
assert len(raw_frames)==98
picture=OUT/'C06_picture_v05.mp4'
with (OUT/'render_stderr.txt').open('wb') as log:
 enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
 try:
  with av.open(str(BASE)) as c:
   for i,f in enumerate(c.decode(video=0)):
    im=raw_frames.get(i) if i in raw_frames else f.to_image()
    enc.stdin.write(im.tobytes())
  count=i+1
 finally: enc.stdin.close();enc.wait()
assert count==1170 and enc.returncode==0
FINAL=OUT/'C06_Q-AI_Fair_edit_v05.mp4'
run(['-y','-v','error','-i',picture,'-i',BASE,'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',FINAL])
run(['-v','error','-i',FINAL,'-f','null','-'])
def audio_packet_info(path):
 with av.open(str(path)) as c:
  s=c.streams.audio[0]
  packets=[p for p in c.demux(s) if p.size]
  return {'sha256':hashlib.sha256(b''.join(bytes(p) for p in packets)).hexdigest(),'count':len(packets),'pts':[p.pts for p in packets],'time_base':str(s.time_base)}
a0,a1=audio_packet_info(BASE),audio_packet_info(FINAL)
assert a0==a1
frames=OUT/'review_frames';frames.mkdir(exist_ok=True)
samples={0,round(9.75*FPS),237,238,240,264,288,312,335,336,341,342,1055,1056,1169}
samples|={round(t*FPS) for t in [2,5,8,15,18,22,26,30,35,39,42,46,48]}
thumbs=[];pts=[]
with av.open(str(FINAL)) as c:
 for i,f in enumerate(c.decode(video=0)):
  pts.append(float(f.time))
  if i in samples:
   im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png')
   card=Image.new('RGB',(320,208),(15,23,31));card.paste(im.resize((320,180)),(0,28));ImageDraw.Draw(card).text((8,3),f'{i/FPS:.3f}s',font=font(17),fill='white');thumbs.append(card)
assert len(pts)==1170 and np.allclose(np.diff(pts),1/FPS)
for batch in range(math.ceil(len(thumbs)/16)):
 sub=thumbs[batch*16:(batch+1)*16];sheet=Image.new('RGB',(1280,208*math.ceil(len(sub)/4)),(15,23,31))
 for j,im in enumerate(sub):sheet.paste(im,((j%4)*320,(j//4)*208))
 sheet.save(OUT/f'review_contact_{batch+1:02d}.jpg',quality=95)
assert hashes=={str(x.relative_to(SB)):sha(x) for x in (BASE,RAW,ART)}
manifest=json.loads((BASE.parent/'edit_manifest.json').read_text(encoding='utf-8-sig'))
for q in manifest['captions']:
 if q['start']==START:q['text']=NEW
manifest.update(file=FINAL.name,fps=FPS,resolution=[W,H],source_edit=str(BASE.relative_to(SB)),source_sha256=hashes,changed_interval_seconds=[START,END],changed_frame_indices_inclusive=[238,335],replacement_method='Decode original C06_K03_take01 frames; apply exact v03 projector composite and fresh caption. No covering patch over old caption.',audio='All v04 AAC payloads and packet PTS preserved byte-for-byte',flow_credits_used=0,generated_action_replaced_with_stills=False,status='Rendered; actual extracted-frame inspection completed separately in README')
dump(OUT/'edit_manifest.json',manifest)
def srt(t):
 ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
(OUT/'C06_captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt(q["start"])} --> {srt(q["end"])}\n{q["text"]}' for i,q in enumerate(manifest['captions']))+'\n',encoding='utf-8-sig')
dump(OUT/'technical_validation.json',dict(file=FINAL.name,sha256=sha(FINAL),duration_seconds=48.75,frames=len(pts),fps=FPS,dimensions=[W,H],full_av_decode='PASS',video_pts_step_seconds=1/FPS,audio_payload_and_pts_unchanged=True,audio_packet_sha256=a1['sha256'],audio_packet_count=a1['count'],original_sha256_unchanged=True,actual_listening_verified=False,actual_continuous_playback_verified=False))
print(json.dumps({'file':str(FINAL),'frames':len(pts),'audio_unchanged':True},ensure_ascii=False))
