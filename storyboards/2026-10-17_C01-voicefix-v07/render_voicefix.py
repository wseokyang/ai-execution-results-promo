"""Replace K06 offscreen question; preserve the reviewed v06 picture packets."""
from pathlib import Path
import subprocess,json,hashlib,re,shutil
from fractions import Fraction
import numpy as np
R=Path(__file__).resolve().parent; SB=R.parent; SR=48000
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
C=R/'.render'; C.mkdir(exist_ok=True)
def run(args,**kw):
 p=subprocess.run([str(FF),'-y','-hide_banner',*map(str,args)],capture_output=True,**kw)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace'))
 return p
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pcm(p): return np.frombuffer(run(['-v','error','-i',p,'-vn','-f','f32le','-ar',SR,'-ac','2','-']).stdout,dtype=np.float32).reshape(-1,2)
def measure(p,target=-18,tp=-1.5):
 r=run(['-i',p,'-af',f'loudnorm=I={target}:TP={tp}:LRA=11:print_format=json','-f','null','-'])
 return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr.decode(errors='replace'))[-1])
def lf(m,target=-18,tp=-1.5):
 return f'loudnorm=I={target}:TP={tp}:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true'
bounds=json.loads((R/'voice_trim_bounds.json').read_text(encoding='utf8'))
source=SB/'2026-10-17_flow-run-09'/bounds['source_filename']
assert source.exists(), 'Wait for completed original download.'
start,end=bounds['source_seconds']; placement=bounds['timeline_start']
assert 0<=start<end<=len(pcm(source))/SR, 'Trim must stay within the completed source audio.'
assert 26.5<=placement and placement+end-start<=30, 'Keep complete new speech within offscreen reaction insert.'
raw=C/'voice_trim_float.wav'; voice=R/'C01_K06_D_clear_voice.wav'
run(['-v','error','-i',source,'-vn','-af',f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS','-ar',SR,'-ac','2','-c:a','pcm_f32le',raw])
m=measure(raw,-18,-2)
run(['-v','error','-i',raw,'-af',lf(m,-18,-2)+',alimiter=limit=0.89:level=false:latency=true','-ar',SR,'-ac','2','-c:a','pcm_f32le',voice])
old=pcm(SB/'2026-10-17_C01-voice-v04/C01_review_edit_v04_take03_55s.mp4')
mix=np.zeros((36*SR,2),dtype=np.float32)
def add(a,b,d,g=1,fade=.015):
 s=old[round(a*SR):round(b*SR)].copy()*g; n=round(fade*SR)
 if n: s[:n]*=np.linspace(0,1,n)[:,None]; s[-n:]*=np.linspace(1,0,n)[:,None]
 off=round(d*SR); mix[off:off+len(s)]+=s
add(0,4.5,0); add(6,14,4.5,fade=.005); add(14,18.5,8.5,.55)
add(21.5,27,13); add(27,32,18.5); add(34,36.4,23.5)
# Quiet tail of the existing K06 after its D line; no rejected old question remains.
bed=old[round(40.7*SR):round(41.7*SR)].copy()*.20
n=round(4.1*SR); amb=np.tile(bed,(5,1))[:n]; f=round(.04*SR)
amb[:f]*=np.linspace(0,1,f)[:,None]; amb[-f:]*=np.linspace(1,0,f)[:,None]
mix[round(25.9*SR):30*SR]+=amb
v=pcm(voice).copy(); n=round(.015*SR); v[:n]*=np.linspace(0,1,n)[:,None]; v[-n:]*=np.linspace(1,0,n)[:,None]
assert abs(len(v)/SR-(end-start))<.01 and placement+len(v)/SR<=30, 'Check actual normalized speech duration before mixing.'
off=round(placement*SR); mix[off:off+len(v)]+=v
score=SB/'2026-10-17_C01-recut-v06/C01_original_score_v06_36s.wav'; mix+=pcm(score)[:len(mix)]
pre=C/'mix_float.wav'
run(['-v','error','-f','f32le','-ar',SR,'-ac','2','-i','-','-c:a','pcm_f32le',pre],input=mix.tobytes())
master=measure(pre)
picture=SB/'2026-10-17_C01-recut-v06/C01_recut_v06_36s_voice_pending.mp4'
out=R/'C01_recut_v07_36s.mp4'
run(['-v','error','-i',picture,'-i',pre,'-map','0:v:0','-map','1:a:0','-af',lf(master)+',alimiter=limit=0.89:level=false:latency=true','-c:v','copy','-c:a','aac','-b:a','256k','-ar',SR,'-ac','2','-t','36','-movflags','+faststart',out])
run(['-v','error','-i',out,'-f','null','-'])
def packets(p):
 lines=run(['-v','error','-i',p,'-map','0:v','-c','copy','-f','framehash','-']).stdout.decode().splitlines()
 tb=next(l.split(':',1)[1].strip() for l in lines if l.startswith('#tb 0:'))
 return [[v.strip() for v in l.split(',')] for l in lines if l and not l.startswith('#')],tb
(a,tba),(b,tbb)=packets(picture),packets(out); assert len(a)==len(b)==864 and tba==tbb
offset=int(b[0][2])-int(a[0][2])
assert all(x[0]==y[0] and x[3:]==y[3:] and int(y[1])-int(x[1])==offset and int(y[2])-int(x[2])==offset for x,y in zip(a,b))
da=pcm(out); assert np.isfinite(da).all() and np.abs(da).max()<1
context=R/'C01_K06_voicefix_context_12_5s.mp4'
run(['-v','error','-ss','23.5','-i',out,'-t','12.5','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',context])
record={'status':'voice_replaced_auditory_review_pending','file':out.name,'bytes':out.stat().st_size,'sha256':sha(out),'duration_seconds':36,'frames':864,'resolution':[1280,720],
 'voice_original':str(source.relative_to(SB)),'voice_original_sha256':sha(source),'voice_trim_seconds':[start,end],'voice_timeline_seconds':[placement,placement+end-start],'trim_basis':bounds['basis'],
 'dialogue':'다음 사례도 볼까요?','old_D_voice_removed':True,'old_K06_A_preserved_source':[34,36.4],'new_D_offscreen':True,'selected_K04_voice_unchanged':True,
 'video_packets_identical_to_v06':True,'packet_timestamp_offset':offset,'packet_timebase':tba,'packet_offset_seconds':offset*float(Fraction(tba)),'actual_voice_duration_seconds':len(v)/SR,'full_decode_pass':True,'loudness':measure(out),'PCM_peak':float(np.abs(da).max()),'full_scale_samples':int((np.abs(da)>=1).sum()),
 'voice_speed_or_pitch_change':False,'actual_listening_by_assistant':False,'new_voice_user_acceptance':False,'originals_modified':False,'score':'v06 original36s score reused unchanged'}
(R/'edit_manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
preview=Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
for p in [out,context,voice,source]: shutil.copyfile(p,preview/p.name)
print(json.dumps(record,ensure_ascii=False),flush=True)
