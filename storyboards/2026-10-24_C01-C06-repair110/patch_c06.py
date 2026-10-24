"""Use the first desk contact only and move its existing Foley cue to the contact frame."""
from pathlib import Path
import sys,json,hashlib,subprocess,importlib.util,math
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;SB=R.parent;OUT=SB/'2026-10-25_C06-impact-edit-v06';OUT.mkdir(exist_ok=True)
BASE=SB/'2026-10-24_C06-caption-v05/C06_Q-AI_Fair_edit_v05.mp4'
RAW=R/'C06_K02_impact_take01.mp4'
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
DEST=OUT/'C06_Q-AI_Fair_edit_v06.mp4';SR=48000;DURATION=48.75
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
spec=importlib.util.spec_from_file_location('established_dsp',SB/'2026-10-23_C05-C06-edit-v04/polish_edits.py');dsp=importlib.util.module_from_spec(spec);spec.loader.exec_module(dsp)
# Rebuild the same six existing effects deterministically. Only desk timing changes.
score=dsp.decode_audio(SB/'2026-10-23_C05-C06-edit-v04/C06/C06_score.wav')
n=round(DURATION*SR);assert len(score)==n
rng=np.random.default_rng(202606);fx=np.zeros((n,2),np.float32);events=[]
for at,d,kind,db,pan,reason in dsp.CUES['C06']:
    new=6.125 if kind=='desk' else dsp.mapped('C06',at)
    mono=dsp.foley(kind,d,rng)*10**(db/20)
    wave=mono[:,None]*np.array([[math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)]])
    pos=round(new*SR);fx[pos:pos+len(wave)]+=wave
    events.append(dict(kind=kind,at=new,duration=d,old_at=at,peak_dbfs_before_mix=db,boundary_samples=[float(mono[0]),float(mono[-1])]))
amb=dsp.ramp_edges(dsp.smooth_noise(rng,n,350),.6,.8)*10**(-57/20)
mix=score+fx+np.column_stack((amb,amb));mix[:round(.05*SR)]*=np.linspace(0,1,round(.05*SR))[:,None];mix[-round(.65*SR):]*=np.linspace(1,0,round(.65*SR))[:,None]
mixfile=OUT/'C06_mix.wav';dsp.write_wav(mixfile,mix)
gain=14.5
filters='[0:v]split=2[a][b];[a]trim=start=0:end=5,setpts=PTS-STARTPTS[v0];[1:v]trim=start=0.75:end=2.25,setpts=PTS-STARTPTS[v1];[b]trim=start=6.5:end=48.75,setpts=PTS-STARTPTS[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v]'
cmd=[str(FF),'-y','-v','error','-i',str(BASE),'-i',str(RAW),'-i',str(mixfile),'-filter_complex',filters,'-map','[v]','-map','2:a','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-af',f'volume={gain}dB,apad=pad_dur=0.2,atrim=duration={DURATION},asetpts=N/SR/TB','-c:a','aac','-b:a','256k','-ar',str(SR),'-t',str(DURATION),'-movflags','+faststart',str(DEST)]
p=subprocess.run(cmd,capture_output=True);assert p.returncode==0,p.stderr
p=subprocess.run([str(FF),'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True);assert p.returncode==0,p.stderr
pts=[];tiles=[];frames=OUT/'review_frames';frames.mkdir(exist_ok=True);font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',16)
with av.open(str(DEST)) as c:
    for i,f in enumerate(c.decode(video=0)):
        pts.append(float(f.time))
        if not (96<=i<=240 and i%6==0):continue
        im=f.to_image();im.save(frames/f'{i/24:06.3f}s.png');t=Image.new('RGB',(320,205),(12,22,31));t.paste(im.resize((320,180)),(0,25));ImageDraw.Draw(t).text((8,3),f'{i/24:.3f}s',font=font,fill='white');tiles.append(t)
im=Image.new('RGB',(1280,205*math.ceil(len(tiles)/4)),(12,22,31))
for i,t in enumerate(tiles):im.paste(t,((i%4)*320,(i//4)*205))
im.save(OUT/'impact_join_contact.jpg',quality=94)
assert len(pts)==1170 and max(abs(pts[i]-i/24) for i in range(len(pts)))<1e-5
audio=dsp.decode_audio(DEST);assert np.isfinite(audio).all() and np.abs(audio).max()<1
end=0;gaps=[]
with av.open(str(DEST)) as c:
    for f in c.decode(audio=0):gaps.append(float(f.time)-end);end=float(f.time)+f.samples/f.sample_rate
assert max(abs(x) for x in gaps)<1/SR and abs(end-DURATION)<1/SR
manifest=json.loads((BASE.parent/'edit_manifest.json').read_text(encoding='utf-8'))
manifest.update(version=6,file=DEST.name,source_edit=str(BASE.relative_to(SB)),replacement=dict(source=str(RAW.relative_to(SB)),source_in=.75,source_out=2.25,timeline_in=5,timeline_out=6.5),audio='Established score/ambience/effects reconstructed; desk cue moved 5.55 to 6.125 seconds. No source dialogue/audio.',source_sha256={str(p.relative_to(SB)):sha(p) for p in [BASE,RAW]},limitations=['Only first desk contact used; second hit excluded','Paper bounce and desk vibration are not verified','Held sheet changes at join to sorting: short time ellipsis, not a seamless physical match'],status='rendered; sample review pending',continuous_playback_verified=False,actual_listening_verified=False)
legacy_keys=['changed_interval_seconds','changed_frame_indices_inclusive','replacement_method']
manifest['previous_version_v05_change']={k:manifest.pop(k) for k in legacy_keys if k in manifest}
manifest['changed_interval_seconds']=[5,6.5]
manifest['changed_frame_indices_inclusive']=[120,155]
manifest['replacement_method']='Replace 36 picture frames with original C06_K02_impact_take01 at source0.75–2.25s; rebuild established audio with desk cue shifted to6.125s.'
dump(OUT/'edit_manifest.json',manifest)
(OUT/'C06_captions.srt').write_bytes((BASE.parent/'C06_captions.srt').read_bytes())
dump(OUT/'audio_recipe.json',dict(music='Existing v04 score unchanged',source_score='2026-10-23_C05-C06-edit-v04/C06/C06_score.wav',effects=events,static_gain_db=gain,contact_source_frame=45,contact_source_time=1.875,contact_timeline_time=6.125,actual_listening_verified=False))
dump(OUT/'technical_validation.json',dict(file=DEST.name,sha256=sha(DEST),duration_seconds=DURATION,video_frames=len(pts),full_decode='PASS',constant_video_pts=True,max_audio_pts_gap_seconds=max(abs(x) for x in gaps),audio_end_seconds=end,audio_peak=float(np.abs(audio).max()),loudness=dsp.loudness(DEST),source_audio_muted=True))
print('DONE',DEST,sha(DEST))
