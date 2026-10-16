"""36s C01 recut. Keep all originals. K06 replacement voice is optional/pending."""
from pathlib import Path
import subprocess, json, hashlib, sys, re, shutil
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
SB=ROOT.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
CACHE=ROOT/'.render'
CACHE.mkdir(exist_ok=True)
SR=48000
LENGTH=36
def run(args, **kw):
    p=subprocess.run([str(FF),'-y','-hide_banner',*map(str,args)],capture_output=True,**kw)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace'))
    return p
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def loudness(p,target=-18,tp=-1.5):
    r=run(['-i',p,'-af',f'loudnorm=I={target}:TP={tp}:LRA=11:print_format=json','-f','null','-'])
    return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr.decode(errors='replace'))[-1])
def lf(m,target=-18,tp=-1.5):
    return (f'loudnorm=I={target}:TP={tp}:LRA=11:measured_I={m["input_i"]}:measured_TP={m["input_tp"]}:'
            f'measured_LRA={m["input_lra"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true')

sources=[
 ('K01','2026-10-16_flow-run-06/C01_K01_take02.mp4',0,4.5,0),
 ('K02','2026-10-16_flow-run-06/C01_K02_take02.mp4',0,4,4.5),
 ('K03','2026-10-16_flow-run-06/C01_K03_take02.mp4',0,4.5,8.5),
 ('K04','2026-10-16_flow-run-05/C01_K04_take02.mp4',.5,6,13),
 ('K05','2026-10-16_flow-run-04/C01_K05_take01.mp4',0,5,18.5),
 ('K06','2026-10-16_flow-run-05/C01_K06_take01.mp4',0,6.5,23.5),
]
segments=[]
for cid,rel,ins,outs,start in sources:
    p=SB/rel; dest=CACHE/f'{cid}.mp4'
    duration=outs-ins
    vf=f'trim=start={ins}:end={outs},setpts=PTS-STARTPTS,fps=24,setsar=1'
    args=['-v','error','-i',p]
    if cid=='K03': vf+=',crop=800:450:0:160,scale=1280:720:flags=lanczos'
    if cid=='K06':
        # D becomes offscreen during replacement question; real moving audience reaction.
        args+=['-loop','1','-i',SB/'2026-10-16_C01-edit-v01/context_caption_720.png']
        vf=('[0:v]split[w][c];[w]trim=0:3,setpts=PTS-STARTPTS,setsar=1[vw];'
            '[c]trim=3:6.5,setpts=PTS-STARTPTS,crop=960:540:0:100,scale=1280:720:flags=lanczos,setsar=1[vc];'
            '[vw][vc]concat=n=2:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.05,fps=24,trim=duration=6.5[v0];[v0][1:v]overlay=0:0:shortest=1[v]')
        args+=['-filter_complex',vf,'-map','[v]']
    else: args+=['-vf',vf]
    run(args+['-an','-t',duration,'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',dest])
    segments.append(dest)
    print('Picture:',cid,flush=True)

# Freeze the final included audience-reaction frame, never return to deleted K07.
freeze=ROOT/'ending_source_frame.png'
run(['-v','error','-i',SB/sources[-1][1],'-vf',"select='eq(n,155)',crop=960:540:0:100,scale=1280:720:flags=lanczos",'-frames:v','1',freeze])
ending=CACHE/'ending.mp4'
run(['-v','error','-loop','1','-framerate','24','-i',freeze,'-loop','1','-i',SB/'2026-10-16_C01-edit-v01/title_overlay_720.png',
     '-filter_complex','[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]','-map','[v]','-an','-t','6','-c:v','libx264','-preset','medium','-crf','18',ending])
segments.append(ending)
lst=CACHE/'segments.txt'; lst.write_text(''.join("file '"+p.name+"'\n" for p in segments),encoding='utf8')
picture=CACHE/'picture.mp4'
run(['-v','error','-f','concat','-safe','0','-i',lst,'-an','-c:v','copy',picture])

# Existing selected-voice mix, without v05 score. K02 full phrase overlaps K03 insert.
base=SB/'2026-10-17_C01-voice-v04/C01_review_edit_v04_take03_55s.mp4'
decoded=run(['-v','error','-i',base,'-vn','-f','f32le','-ar',SR,'-ac','2','-']).stdout
old=np.frombuffer(decoded,dtype=np.float32).reshape(-1,2)
mix=np.zeros((LENGTH*SR,2),dtype=np.float32)
audio_edits=[]
def add(start,end,dest,gain=1,fade=.015):
    a=old[round(start*SR):round(end*SR)].copy()*gain
    n=min(round(fade*SR),len(a)//2)
    if n: a[:n]*=np.linspace(0,1,n)[:,None]; a[-n:]*=np.linspace(1,0,n)[:,None]
    off=round(dest*SR); mix[off:off+len(a)]+=a
    audio_edits.append({'v04_source':[start,end],'new_start':dest,'gain':gain,'fade_seconds':fade})
add(0,4.5,0)
add(6,14,4.5,fade=.005) # Preserve late '좀' through complete source end.
add(14,18.5,8.5,.55)
add(21.5,27,13) # Selected K04 take03 remains 13.5–17.2, no speed/pitch change.
add(27,32,18.5)
voice=ROOT/'K06_clear_voice_selected.wav'
has_voice=voice.exists()
if has_voice:
    add(34,36.4,23.5)
    # Reuse quiet room sound after both original spoken lines; no old D phrase.
    bed=old[round(40.7*SR):round(41.7*SR)]*.32
    off=round(25.9*SR); n=round(4.1*SR)
    mix[off:off+n]+=np.tile(bed,(5,1))[:n]
    v=run(['-v','error','-i',voice,'-f','f32le','-ar',SR,'-ac','2','-']).stdout
    v=np.frombuffer(v,dtype=np.float32).reshape(-1,2)
    assert len(v)<=round(3.3*SR), 'Do not truncate or accelerate replacement speech.'
    off=round(26.5*SR); mix[off:off+len(v)]+=v
    voice_state='replacement_present_listening_pending'
else:
    add(34,40.5,23.5)
    voice_state='original_K06_voice_TEMPORARY_replacement_pending'

# Retimed original note sequence. No callback cue belonging to removed K07.
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
from tinysoundfont import Synth
sf=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
synth=Synth(gain=-10,samplerate=SR); sid=synth.sfload(str(sf))
synth.program_select(0,sid,0,0); synth.program_select(1,sid,0,48)
notes=[]
def note(t,d,p,v=42,c=0): notes.append(dict(start=t,duration=d,pitch=p,velocity=v,channel=c))
def chord(t,d,ps,v=30):
    for p in ps: note(t,d,p,v,1)
note(.2,3.5,62,48)
chord(4.6,3.6,[50,57,65]); note(4.8,1.7,57,39); note(6.8,1.5,65)
chord(8.6,4.1,[46,53,62],34); note(9.1,1.5,62); note(11.1,1.5,65)
chord(13.1,5.0,[43,50,58],25)
chord(18.6,4.5,[50,53,57],30); note(22.1,1.1,64,38)
chord(30.05,4.4,[53,57,60,64],34)
for t,p,v in [(30.12,62,43),(31.2,65,46),(32.4,69,45),(33.45,67,40),(34.15,65,38)]: note(t,1.4,p,v)
events=sorted([(round(n['start']*SR),1,n) for n in notes]+[(round((n['start']+n['duration'])*SR),0,n) for n in notes],key=lambda x:(x[0],x[1]))
score=np.zeros_like(mix); cursor=0
for frame,on,n in events:
    frame=min(frame,len(score))
    if frame>cursor: score[cursor:frame]=np.frombuffer(synth.generate(frame-cursor),dtype=np.float32).reshape(-1,2); cursor=frame
    if on: synth.noteon(n['channel'],n['pitch'],n['velocity'])
    else: synth.noteoff(n['channel'],n['pitch'])
if cursor<len(score): score[cursor:]=np.frombuffer(synth.generate(len(score)-cursor),dtype=np.float32).reshape(-1,2)
points=[(0,0),(.1,1),(12.8,1),(13.1,.5),(18.3,.5),(18.6,.55),(22.8,.8),(23.5,0),(29.95,0),(30.05,1.5),(34.8,1.5),(35.8,0),(36,0)]
t=np.arange(len(score))/SR
score*=np.interp(t,[p[0] for p in points],[p[1] for p in points]).astype(np.float32)[:,None]
score*=.5/max(float(np.abs(score).max()),1e-8)
dry=CACHE/'score_dry.wav'
run(['-v','error','-f','f32le','-ar',SR,'-ac','2','-i','-','-c:a','pcm_f32le',dry],input=score.tobytes())
m=loudness(dry,-30,-9); scorefile=ROOT/'C01_original_score_v06_36s.wav'
run(['-v','error','-i',dry,'-af',lf(m,-30,-9),'-ar',SR,'-c:a','pcm_f32le',scorefile])
scoredata=np.frombuffer(run(['-v','error','-i',scorefile,'-f','f32le','-ar',SR,'-ac','2','-']).stdout,dtype=np.float32).reshape(-1,2)
mix+=scoredata[:len(mix)]
premaster=CACHE/'mix_float.wav'
run(['-v','error','-f','f32le','-ar',SR,'-ac','2','-i','-','-c:a','pcm_f32le',premaster],input=mix.tobytes())
measurement=loudness(premaster)
name='C01_recut_v06_36s.mp4' if has_voice else 'C01_recut_v06_36s_voice_pending.mp4'
out=ROOT/name
run(['-v','error','-i',picture,'-i',premaster,'-map','0:v:0','-map','1:a:0','-af',lf(measurement)+',alimiter=limit=0.89:level=false:latency=true',
     '-c:v','copy','-c:a','aac','-b:a','256k','-ar',SR,'-ac','2','-t',LENGTH,'-movflags','+faststart',out])
run(['-v','error','-i',out,'-f','null','-'])
da=np.frombuffer(run(['-v','error','-i',out,'-vn','-f','f32le','-ar',SR,'-ac','2','-']).stdout,dtype=np.float32)
assert np.isfinite(da).all() and np.abs(da).max()<1
packets=run(['-v','error','-i',out,'-map','0:v:0','-c','copy','-f','framehash','-']).stdout.decode()
assert len([l for l in packets.splitlines() if l and not l.startswith('#')])==864
manifest={'status':'recut_review_voice_replacement_pending' if not has_voice else 'recut_review', 'voice_status':voice_state,
 'output':{'name':name,'bytes':out.stat().st_size,'sha256':sha(out)},'duration_seconds':36,'resolution':[1280,720],'fps':24,'frames':864,
 'changes':['K07 entire cut and both lines removed','First water gag advances from14 to8.5s','K02 complete8s voice L-cut over moving K03 insert','Reveal advances from34 to23.5s','K06 audience reaction insert after3s for offscreen replacement D','Title freezes K06 frame155,30–36s','Original score recomposed for shorter edit; no K07 callback'],
 'clips':[{'id':c,'source':p,'sha256':sha(SB/p),'source_in':i,'source_out':o,'new_in':s,'new_out':s+o-i} for c,p,i,o,s in sources],
 'audio_edits_from_v04':audio_edits,'K04_voice':'user-selected Flow run07 take03, same3.70s at13.5–17.2','K06_voice_replacement_file':voice.name if has_voice else None,
 'audio_speed_or_pitch_changed':False,'full_decode_pass':True,'final_loudness':loudness(out),'decoded_peak':float(np.abs(da).max()),'full_scale_samples':int((np.abs(da)>=1).sum()),
 'assistant_actual_listening':False,'originals_modified':False,'new_Flow_requests_by_render':0,'title_source':'2026-10-16_C01-edit-v01/title_overlay_720.png'}
(ROOT/'edit_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'score_notes.json').write_text(json.dumps({'notes':notes,'envelope':points},indent=2),encoding='utf8')
for n in ['score_sources.json','GeneralUser-GS-LICENSE.txt']: shutil.copyfile(SB/'2026-10-17_C01-final-v05'/n,ROOT/n)
frames=ROOT/'review_frames'; frames.mkdir(exist_ok=True)
times=sorted(set([0,1,2,3,4,4.45,4.5,5,6,7,8,8.45,8.5,9,10,11,12,12.95,13,14,15,16,17,18,18.45,18.5,19,20,21,22,23,23.45,23.5,24,25,26,26.45,26.5,27,28,29,29.95,30,32,34,35.9]))
for sec in times:
    run(['-v','error','-ss',sec,'-i',out,'-frames:v','1',frames/f'{sec:05.2f}s.jpg'])
for page in range((len(times)+15)//16):
    sheet=Image.new('RGB',(1280,800),'#101010'); d=ImageDraw.Draw(sheet)
    for j,sec in enumerate(times[page*16:(page+1)*16]):
        im=Image.open(frames/f'{sec:05.2f}s.jpg').resize((320,180)); x=(j%4)*320; y=(j//4)*200
        sheet.paste(im,(x,y)); d.text((x+6,y+182),f'{sec:.2f}s',fill='white')
    sheet.save(frames/f'sheet_{page+1:02d}.jpg')
preview=Path('C:/Users/wseok/.codex/visualizations/2026/10/16/01a13daf-3732-7b90-99a8-92c605090d35')
shutil.copyfile(out,preview/name)
print(json.dumps(manifest,ensure_ascii=False),flush=True)
