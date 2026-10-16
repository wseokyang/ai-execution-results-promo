"""Original sparse score, user-selected Flow voice, unchanged55-second picture edit."""
from pathlib import Path
import sys, subprocess, json, hashlib, shutil, re
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import numpy as np
from tinysoundfont import Synth

root=Path(__file__).resolve().parent
sb=root.parent
ff=sb/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
source=sb/'2026-10-17_C01-voice-v04/C01_review_edit_v04_take03_55s.mp4'
sf=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
sr=48000
length=55
synth=Synth(gain=-10,samplerate=sr)
sid=synth.sfload(str(sf))
synth.program_select(0,sid,0,0)
synth.program_select(1,sid,0,48)
synth.control_change(0,10,58)
synth.control_change(1,10,70)
notes=[]
def note(t,d,pitch,velocity=48,channel=0):
    notes.append({'start':t,'duration':d,'pitch':pitch,'velocity':velocity,'channel':channel})
def chord(t,d,pitches,v=31):
    for pitch in pitches: note(t,d,pitch,v,1)

# A restrained D-minor motif. No borrowed song, sample melody or demo MIDI.
note(.25,3.5,62,48)
chord(6.1,7.2,[50,57,65],30)
for t,p,v in [(6.4,57,39),(8.8,62,42),(10.4,65,44)]: note(t,2.2,p,v)
chord(14.1,6.4,[46,53,62],34)
note(15.1,2.3,62,43); note(18.0,2.3,65,42)
chord(21.1,5.4,[43,50,58],26)
note(26.1,1.5,62,35)
chord(27.1,4.0,[50,53,57],31)
chord(31.25,2.4,[45,52,62],32)
note(32.3,1.0,64,40)
# Callback between the two K07 utterances (ASR43.36–44.28 and46.94–48.12).
note(45.15,.65,62,40)
# Quiet title cadence, related to the same motif.
chord(49.05,4.4,[53,57,60,64],34)
for t,p,v in [(49.12,62,43),(50.2,65,46),(51.4,69,45),(52.45,67,40),(53.15,65,38)]:
    note(t,1.4,p,v)

events=[]
for n in notes:
    events.append((round(n['start']*sr),1,n))
    events.append((round((n['start']+n['duration'])*sr),0,n))
events.sort(key=lambda x:(x[0],x[1]))
audio=np.zeros((length*sr,2),dtype=np.float32)
cursor=0
for frame,on,n in events:
    frame=min(frame,len(audio))
    if frame>cursor:
        audio[cursor:frame]=np.frombuffer(synth.generate(frame-cursor),dtype=np.float32).reshape(-1,2)
        cursor=frame
    if on: synth.noteon(n['channel'],n['pitch'],n['velocity'])
    else: synth.noteoff(n['channel'],n['pitch'])
if cursor<len(audio): audio[cursor:]=np.frombuffer(synth.generate(len(audio)-cursor),dtype=np.float32).reshape(-1,2)
t=np.arange(len(audio))/sr
# Silence at reveal; normalization/resampling can leave negligible rounding residue.
points=[(0,0),(.1,1),(20.7,1),(21.1,.52),(26,.52),(26.7,.8),(27.1,.55),(30.5,.55),(31.2,1),
        (33.8,1),(34,0),(45.05,0),(45.15,.75),(45.9,.75),(46.45,0),(48.95,0),(49.05,1.5),(53.8,1.5),(54.8,0),(55,0)]
env=np.interp(t,[p[0] for p in points],[p[1] for p in points]).astype(np.float32)
audio*=env[:,None]
assert np.isfinite(audio).all()
peak=float(np.abs(audio).max())
audio*=.50/max(peak,1e-9)
def run(args,**kwargs):
    try:
        return subprocess.run([str(ff),*args],check=True,**kwargs)
    except subprocess.CalledProcessError as e:
        raise RuntimeError((e.stderr or b'').decode(errors='replace')) from e
dry=root/'C01_original_score_dry_float.wav'
run(['-y','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','-','-c:a','pcm_f32le',str(dry)],input=audio.tobytes(),capture_output=True)
def loudness(path,target,tp):
    p=run(['-hide_banner','-i',str(path),'-af',f'loudnorm=I={target}:TP={tp}:LRA=11:print_format=json','-f','null','-'],capture_output=True)
    return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr.decode(errors='replace'))[-1])
def linear_filter(m,target,tp):
    return (f'loudnorm=I={target}:TP={tp}:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:'
            f'measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')
score_measure=loudness(dry,-30,-9)
score=root/'C01_original_score_55s.wav'
run(['-y','-v','error','-i',str(dry),'-af',linear_filter(score_measure,-30,-9),'-ar',str(sr),'-c:a','pcm_f32le',str(score)],capture_output=True)
mix=root/'C01_mix_before_master_float.wav'
run(['-y','-v','error','-i',str(source),'-i',str(score),'-filter_complex',
     '[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,atrim=duration=55[a]',
     '-map','[a]','-ar',str(sr),'-c:a','pcm_f32le',str(mix)],capture_output=True)
master_measure=loudness(mix,-18,-1.5)
out=root/'C01_why_now_edit_v05_55s.mp4'
run(['-y','-v','error','-i',str(source),'-i',str(mix),'-map','0:v:0','-map','1:a:0',
     '-af',linear_filter(master_measure,-18,-1.5)+',alimiter=limit=0.89:level=false:latency=true',
     '-c:v','copy','-c:a','aac','-b:a','256k','-ar',str(sr),'-ac','2','-t','55','-movflags','+faststart',str(out)],capture_output=True)
run(['-v','error','-i',str(out),'-f','null','-'],capture_output=True)
def video_hash(path):
    return run(['-v','error','-i',str(path),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-'],capture_output=True).stdout.decode().strip()
def packets(path):
    s=run(['-v','error','-i',str(path),'-map','0:v:0','-c','copy','-f','framehash','-'],capture_output=True).stdout.decode()
    return [[x.strip() for x in l.split(',')] for l in s.splitlines() if l and not l.startswith('#')]
a,b=packets(source),packets(out)
assert len(a)==len(b)==1320
shift=int(b[0][2])-int(a[0][2])
for x,y in zip(a,b):
    assert x[0]==y[0] and x[3:]==y[3:]
    assert int(y[1])-int(x[1])==shift and int(y[2])-int(x[2])==shift
assert video_hash(source)==video_hash(out)
decoded=run(['-v','error','-i',str(out),'-vn','-f','f32le','-ar',str(sr),'-ac','2','-'],capture_output=True).stdout
da=np.frombuffer(decoded,dtype=np.float32)
assert np.isfinite(da).all() and np.abs(da).max()<1
score_audio=run(['-v','error','-i',str(score),'-f','f32le','-ar',str(sr),'-ac','2','-'],capture_output=True).stdout
sa=np.frombuffer(score_audio,dtype=np.float32).reshape(-1,2)
assert np.abs(sa[34*sr:42*sr]).max()<1e-8
final_measure=loudness(out,-18,-1.5)
record={'status':'finished_edit_final_mix_listening_pending','file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
        'duration_seconds':55,'selected_voice':'Flow run07 take03, user said 세 번째로 진행',
        'dialogue':'제가 실수한 부분도 같이 보여드릴게요.','picture':'All7 existing generated motion clips and6s ending retained',
        'BGM':'New sparse piano/strings note sequence; no existing music or demo MIDI used',
        'cue_regions':[[0,34],[45.15,46.45],[49.05,54.8]],'music_silent_34_to_42':True,
        'silence_scope':'Numerical silence below1e-8, not a claim of bit-exact zero after resampling',
        'score_34_to_42_peak':float(np.abs(sa[34*sr:42*sr]).max()),
        'score_loudness':score_measure,'master_measurement':master_measure,'final_loudness':final_measure,
        'decoded_peak':float(np.abs(da).max()),'samples_above_full_scale':int((np.abs(da)>=1).sum()),
        'video_packets':1320,'video_payload_and_relative_timing_identical':True,'video_sha256':video_hash(out),'mux_shift_seconds':shift/12288,
        'full_decode_pass':True,'originals_overwritten_or_reencoded':False,'additional_Flow_credits_for_music_or_edit':0,'paid_API_calls':0,
        'actual_listening_by_assistant':False,'remaining_review':'Full mix auditory check; do not claim human listening or all lip-sync verified.'}
(root/'final_manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
(root/'original_score_notes.json').write_text(json.dumps({'duration_seconds':55,'samplerate':sr,'instruments':{'0':synth.sfpreset_name(sid,0,0),'1':synth.sfpreset_name(sid,0,48)},'notes':notes,'envelope':points},ensure_ascii=False,indent=2),encoding='utf8')
for n in ['score_sources.json','GeneralUser-GS-LICENSE.txt']:
    shutil.copyfile(sb/'2026-10-17_C01-sound-v04'/n,root/n)
preview=Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
shutil.copyfile(out,preview/out.name)
print(json.dumps(record,ensure_ascii=False),flush=True)
