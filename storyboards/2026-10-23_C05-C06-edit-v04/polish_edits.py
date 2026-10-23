"""Local derivative edits. Previous renders and all Flow originals stay read-only.

Review basis: exact visual events and PCM analysis, not subjective listening.
"""
from pathlib import Path
import sys, json, subprocess, hashlib, re, shutil, math
sys.path.insert(0, 'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
OLD=OUT.parent/'2026-10-23_C05-C06-edit-v03'
FF=OUT.parent/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SR=48000
FPS=24
AUDIO_ONLY='--audio-only' in sys.argv
FILES={'C05':'C05_Q-AI_Fair_edit_v02.mp4','C06':'C06_Q-AI_Fair_edit_v03.mp4'}
# The retained frame intervals are in the old delivered video's time coordinate.
KEEP={'C05':[(0,22.5),(23.25,38.5)],
      'C06':[(0,37.75),(38.5,42.5),(43,50)]}
# Old-video event positions; every event is remapped after the trims.
# start, duration, material, peak dBFS before common mix gain, pan, visible cause
CUES={
 'C05':[
  (4.60,.85,'stone_scrape',-31,0,'pillar pulled away; dust begins'),
  (8.00,.38,'stone_land',-26,-.15,'pillar settles onto ground'),
  (9.78,.52,'structural_stress',-33,0,'roof catch at cut; no invented collapse'),
  (12.95,1.15,'wheels',-37,.3,'jack rolls; no invisible pump clicks'),
  (23.50,2.0,'wheels',-36,-.3,'ladder rolls; no brake latch shown'),
  (31.25,.42,'structural_stress',-32,0,'slow attack peaks as supporting hand leaves roof')],
 'C06':[
  (3.458,.25,'paper',-36,0,'worker releases folder into ghost hand'),
  (5.55,.24,'desk',-31,0,'hands contact desk'),
  (7.90,.36,'paper',-35,-.1,'paper stack placed'),
  (18.00,.40,'pencil',-39,.15,'pen checking original document'),
  (25.333,.22,'door',-31,-.35,'door reaches near-closed position'),
  (39.792,.15,'hinge',-37,-.25,'folding chair reaches open position')]
}

def dump(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,**kw):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kw)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-5000:])
 return p
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def mapped(c,t):
 cursor=0
 for a,b in KEEP[c]:
  if a<=t<b: return cursor+t-a
  cursor+=b-a
 if abs(t-KEEP[c][-1][1])<1e-6: return cursor
 return None
def mapping_boundary(c,t):
 # A caption end within a removed tail clamps to that join.
 return sum(max(0,min(t,b)-a) for a,b in KEEP[c])
def smooth_noise(rng,n,width):
 x=rng.normal(size=n+width-1)
 x=np.convolve(x,np.ones(width)/width,'valid')
 return x/max(1e-8,float(np.std(x)))
def ramp_edges(x,attack=.008,release=.035):
 na=min(len(x)//2,round(attack*SR)); nr=min(len(x)//2,round(release*SR))
 x=x.copy()
 x[:na]*=np.sin(np.linspace(0,np.pi/2,na))**2
 x[-nr:]*=np.cos(np.linspace(0,np.pi/2,nr))**2
 x[0]=0; x[-1]=0
 return x
def foley(kind,d,rng):
 n=round(d*SR); t=np.arange(n)/SR
 low=smooth_noise(rng,n,180); mid=smooth_noise(rng,n,18)
 if kind=='stone_scrape':
  x=(.75*low+.25*mid)*(np.sin(np.pi*t/d)**1.5)
 elif kind=='stone_land':
  x=(np.sin(2*np.pi*76*t)+.35*np.sin(2*np.pi*119*t)+.60*low)*np.exp(-t*18)
 elif kind=='structural_stress':
  # No swept sine/chirp. Broad low friction with restrained fixed resonances.
  env=np.sin(np.pi*t/d)**1.5
  x=(.75*low+.2*np.sin(2*np.pi*105*t)+.1*np.sin(2*np.pi*153*t))*env
 elif kind=='wheels':
  x=(.8*low+.2*mid)*(.72+.18*np.sin(2*np.pi*13*t))
 elif kind=='paper':
  fine=smooth_noise(rng,n,4)-smooth_noise(rng,n,28)*.18
  x=fine*(np.sin(np.pi*t/d)**2)*(.65+.35*np.sin(2*np.pi*31*t)**2)
 elif kind=='pencil':
  x=(mid-.2*low)*(np.sin(np.pi*t/d)**2)*(.5+.5*np.sin(2*np.pi*22*t)**2)
 elif kind in ('door','desk','wood'):
  hz={'door':115,'desk':175,'wood':260}[kind]
  decay={'door':24,'desk':28,'wood':36}[kind]
  x=(.65*np.sin(2*np.pi*hz*t)+.2*np.sin(2*np.pi*hz*1.87*t)+.45*mid)*np.exp(-t*decay)
 elif kind=='hinge':
  x=(.35*np.sin(2*np.pi*650*t)+.15*np.sin(2*np.pi*1110*t)+.60*mid)*np.exp(-t*44)
 else: raise ValueError(kind)
 x-=x.mean()
 x=ramp_edges(x,.003 if kind in ('door','desk','wood','hinge','stone_land') else .025,.045)
 return x/max(1e-8,float(np.abs(x).max()))
def decode_audio(p):
 return np.frombuffer(run(['-v','error','-i',p,'-vn','-ar',SR,'-ac',2,'-f','f32le','-']).stdout,np.float32).reshape(-1,2).copy()
def write_wav(p,x):
 run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',p],input=x.astype('float32').tobytes())
def loudness(p):
 q=run(['-hide_banner','-i',p,'-af','loudnorm=I=-19:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
 return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',q.stderr.decode(errors='replace'))[-1])
def srt_time(t):
 ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'

def render(c):
 out=OUT/c;out.mkdir(exist_ok=True)
 src=OLD/c/FILES[c];source_hash=sha(src)
 old_manifest=json.loads((OLD/c/'edit_manifest.json').read_text(encoding='utf-8'))
 old_recipe=json.loads((OLD/c/'audio_recipe.json').read_text(encoding='utf-8'))
 duration=sum(b-a for a,b in KEEP[c]);n=round(duration*SR)
 # Preserve original composition, bypass old mixed FX completely.
 old_score=decode_audio(OLD/c/f'{c}_score.wav')
 pieces=[]
 for a,b in KEEP[c]:
  part=old_score[round(a*SR):round(b*SR)].copy()
  # Short fades at splice boundaries, never overlap spoken syllables (no speech).
  fade=round(.045*SR)
  part[:fade]*=np.linspace(0,1,fade)[:,None]
  part[-fade:]*=np.linspace(1,0,fade)[:,None]
  pieces.append(part)
 score=np.concatenate(pieces);assert len(score)==n
 rng=np.random.default_rng(202605 if c=='C05' else 202606)
 fx=np.zeros((n,2),np.float32);events=[]
 for at,d,kind,db,pan,reason in CUES[c]:
  new=mapped(c,at);assert new is not None
  mono=foley(kind,d,rng)*10**(db/20)
  left=math.sqrt((1-pan)/2);right=math.sqrt((1+pan)/2)
  wave=mono[:,None]*np.array([[left,right]])
  pos=round(new*SR);end=min(n,pos+len(wave));fx[pos:end]+=wave[:end-pos]
  events.append(dict(old_at=at,at=new,duration=d,kind=kind,pre_mix_peak_dbfs=db,pan=pan,visible_cause=reason,
                     boundary_samples=[float(mono[0]),float(mono[-1])],actual_listening_verified=False))
 # Quiet broad ambience joins silent passages, not a fake recording of the venue.
 amb=smooth_noise(rng,n,350)
 amb=ramp_edges(amb,.6,.8)*10**(-57/20)
 ambience=np.column_stack((amb,amb))
 mix=score+fx+ambience
 mix[:round(.05*SR)]*=np.linspace(0,1,round(.05*SR))[:,None]
 mix[-round(.65*SR):]*=np.linspace(1,0,round(.65*SR))[:,None]
 write_wav(out/f'{c}_score.wav',score);write_wav(out/f'{c}_fx.wav',fx);write_wav(out/f'{c}_mix.wav',mix)
 m=loudness(out/f'{c}_mix.wav')
 # Fixed gain avoids time-varying loudness pumping and the old limiter's 55ms PTS gap.
 gain_db=min(-21.0-float(m['input_i']),-2.3-float(m['input_tp']))
 select='+'.join(f'between(n,{round(a*FPS)},{round(b*FPS)-1})' for a,b in KEEP[c])
 final=out/f'{c}_Q-AI_Fair_edit_v04.mp4'
 print(c,'rendering',duration,flush=True)
 if AUDIO_ONLY:
  picture=out/f'{c}_picture.mp4';shutil.copy2(final,picture)
  inp=picture;video_args=['-c:v','copy']
 else:
  inp=src;video_args=['-vf',f"select='{select}',setpts=N/({FPS}*TB)",'-fps_mode','cfr','-r',FPS,
                    '-c:v','libx264','-crf',16,'-preset','medium','-pix_fmt','yuv420p']
 run(['-y','-v','error','-i',inp,'-i',out/f'{c}_mix.wav','-map','0:v:0','-map','1:a:0',*video_args,
      '-af',f'volume={gain_db}dB,apad=pad_dur=0.2,atrim=duration={duration},asetpts=N/SR/TB','-c:a','aac','-b:a','256k','-ar',SR,
      '-t',duration,'-movflags','+faststart',final])
 caps=[]
 for cp in old_manifest['captions']:
  cp=cp.copy();cp['start']=mapping_boundary(c,cp['start']);cp['end']=mapping_boundary(c,cp['end'])
  if cp['end']>cp['start']:caps.append(cp)
 (out/f'{c}_captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(q["start"])} --> {srt_time(q["end"])}\n{q["text"]}' for i,q in enumerate(caps))+'\n',encoding='utf-8-sig')
 dump(out/'edit_manifest.json',dict(film=c,duration_seconds=duration,source_edited_file=str(src.relative_to(OUT.parent.parent)),source_edited_sha256=source_hash,
    keep_old_time_intervals=KEEP[c],captions=caps,flow_credits_used=0,source_audio='Muted',action_stills_inserted=False,
    continuous_playback_verified=False,actual_listening_verified=False,status='awaiting updated sample review'))
 dump(out/'audio_recipe.json',dict(music='Unchanged composition, cut at same video edits, 45ms seam fades',
    source_score_sha256=sha(OLD/c/f'{c}_score.wav'),original_recipe=str((OLD/c/'audio_recipe.json').relative_to(OUT.parent.parent)),
    effects=events,old_effects_removed=True,ambience='Local synthesized low broad noise, -57dBFS RMS before mix gain; not field recording',
    target_lufs=-21,static_gain_db=gain_db,peak_headroom_db=2.3,normalization='One fixed measured gain; no dynamic loudnorm or lookahead limiter',actual_listening_verified=False))
 run(['-v','error','-i',final,'-f','null','-'])
 audio=decode_audio(final);assert np.isfinite(audio).all() and np.abs(audio).max()<1
 audio_end=0.;audio_gaps=[];audio_sample_total=0
 with av.open(str(final)) as con:
  for f in con.decode(audio=0):
   audio_gaps.append(float(f.time)-audio_end)
   audio_end=float(f.time)+f.samples/f.sample_rate;audio_sample_total+=f.samples
 assert max(abs(x) for x in audio_gaps)<1/SR
 assert abs(audio_end-duration)<1/SR
 frames=out/'review_frames';frames.mkdir(exist_ok=True)
 times=[];thumbs=[];expected=round(duration*FPS)
 sample=set(range(0,expected,12))|{expected-1}
 joins=[sum(b-a for a,b in KEEP[c][:i]) for i in range(1,len(KEEP[c]))]
 for t in joins+[q['at'] for q in events]:
  sample.update(range(max(0,round((t-.25)*FPS)),min(expected,round((t+.50)*FPS)),3))
 with av.open(str(final)) as con:
  for i,f in enumerate(con.decode(video=0)):
   times.append(float(f.time))
   if i not in sample or AUDIO_ONLY:continue
   im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png')
   tile=Image.new('RGB',(320,205),(12,22,31));tile.paste(im.resize((320,180)),(0,25))
   ImageDraw.Draw(tile).text((8,3),f'{i/FPS:.3f}s',font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',16),fill='white');thumbs.append(tile)
 assert len(times)==expected
 assert np.max(np.abs(np.diff(times)-1/FPS))<1e-5
 for j in range(math.ceil(len(thumbs)/20)):
  batch=thumbs[j*20:j*20+20];sheet=Image.new('RGB',(1280,205*math.ceil(len(batch)/4)),(12,22,31))
  for i,im in enumerate(batch):sheet.paste(im,((i%4)*320,(i//4)*205))
  sheet.save(out/f'review_contact_{j+1:02d}.jpg',quality=93)
 assert sha(src)==source_hash
 validation=dict(file=final.name,sha256=sha(final),bytes=final.stat().st_size,duration_seconds=duration,video_frames=expected,
    fps=24,resolution=[1280,720],full_decode='PASS',video_pts_steps='constant 1/24 second',audio_samples=len(audio),
    audio_peak=float(np.abs(audio).max()),loudness=loudness(final),all_sfx_boundary_samples_zero=all(q['boundary_samples']==[0.0,0.0] for q in events),
    audio_decoded_timeline_samples=audio_sample_total,audio_end_seconds=audio_end,max_audio_pts_gap_seconds=max(abs(x) for x in audio_gaps),
    previous_delivered_video_unchanged=True,actual_realtime_playback_verified=False,actual_listening_verified=False)
 dump(out/'technical_validation.json',validation)
 print(c,'DONE',validation['sha256'],flush=True)

if __name__=='__main__':
 for c in [a for a in sys.argv[1:] if not a.startswith('--')] or ['C05','C06']:render(c)
