"""Local, reversible pacing candidate. V13 and all generated originals remain unchanged."""
from pathlib import Path
import subprocess, json, hashlib, sys
Q=Path(__file__).resolve().parent
SB=Q.parent
SRC=SB/'2026-10-25_final-six-v13/C04/C04_Q-AI_Fair_final_v13.mp4'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
OUT=Q/'C04';OUT.mkdir(exist_ok=True)
DST=OUT/'C04_Q-AI_Fair_final_v14.mp4'
def run(a):
 p=subprocess.run([str(FF),*map(str,a)],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-4000:])
 return p
srcsha=hashlib.sha256(SRC.read_bytes()).hexdigest()
# Retain the whole insertion/empty-hand withdrawal. Only the five-second NOTE shot runs at 1.25x.
# Captions are already composited, so their placement stays locked to the shot.
f=';'.join([
 '[0:v]split=3[v0][v1][v2]',
 '[v0]trim=start_frame=0:end_frame=72,setpts=PTS-STARTPTS[a]',
 '[v1]trim=start_frame=72:end_frame=192,setpts=(PTS-STARTPTS)/1.25,fps=24[b]',
 '[v2]trim=start_frame=192:end_frame=1068,setpts=PTS-STARTPTS[c]',
 '[a][b][c]concat=n=3:v=1:a=0[v]',
 '[0:a]asplit=3[s0][s1][s2]',
 '[s0]atrim=start=0:end=3,asetpts=PTS-STARTPTS,afade=t=out:st=2.995:d=0.005[x]',
 '[s1]atrim=start=3:end=8,asetpts=PTS-STARTPTS,atempo=1.25,atrim=duration=4,apad=whole_dur=4,afade=t=in:d=0.005,afade=t=out:st=3.995:d=0.005[y]',
 '[s2]atrim=start=8:end=44.5,asetpts=PTS-STARTPTS,afade=t=in:d=0.005[z]',
 '[x][y][z]concat=n=3:v=0:a=1[au]'])
run(['-hide_banner','-y','-i',SRC,'-filter_complex',f,'-map','[v]','-map','[au]',
 '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r','24',
 '-c:a','aac','-b:a','192k','-ar','48000','-t','43.5','-movflags','+faststart',DST])
run(['-v','error','-i',DST,'-f','null','-'])
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==srcsha
def t(x):return x if x<=3 else 3+(x-3)/1.25 if x<=8 else x-1
ed=json.loads((SRC.parent/'edit_manifest.json').read_text(encoding='utf-8'))
for k in ('timeline','captions'):
 for item in ed[k]:
  item['v13_start']=item['start'];item['v13_end']=item['end']
  item['start']=t(item['start']);item['end']=t(item['end'])
  if item.get('cut')=='NOTE':item['speed']=1.25
ed.update(file=DST.name,duration_seconds=43.5,parent_version=str(SRC),parent_sha256=srcsha,
 final_sha256=hashlib.sha256(DST.read_bytes()).hexdigest(),status='CANDIDATE_PENDING_THREE_RECHECK',
 change='V13 3-8s NOTE shot at1.25x, preserving entire insertion and withdrawal. 1s shorter. All other pictures and captions retain content/order.',
 audio_change='Same V13 BGM/SFX; NOTE audio atempo1.25,5ms boundary ramps. Not listened to.',
 actual_continuous_playback_verified=False,actual_listening_verified=False)
ed.pop('final_review_record',None)
(OUT/'edit_manifest.json').write_text(json.dumps(ed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(DST,flush=True)
