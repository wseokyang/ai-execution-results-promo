"""Original local instrumental score and two restrained mat-contact cues.
No source speech. No purchased or copied music. Not a claim of actual listening.
"""
from pathlib import Path
import sys,json,subprocess,re,hashlib,math
sys.path[:0]=['C:/Users/wseok/.cache/codex-media-tools/faster-whisper','C:/Users/wseok/.cache/codex-media-tools/tinysoundfont']
import numpy as np,av
from tinysoundfont import Synth
from render_c01 import OUT,SB,FF,SR,FPS,dump,sha
SF=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
def run(args,**kwargs):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kwargs)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-3000:])
 return p

def soundtrack(duration,front=False):
 n=round(duration*SR);synth=Synth(gain=-14,samplerate=SR);sid=synth.sfload(str(SF))
 programs={0:60,1:48,2:45,3:33,4:11}
 for ch,pr in programs.items():synth.program_select(ch,sid,0,pr)
 notes=[]
 def note(t,d,p,vel,ch):
  if t<duration:notes.append(dict(start=t,duration=min(d,duration-t),pitch=p,velocity=vel,channel=ch))
 def chord(t,d,ps,vel,ch):
  for p in ps:note(t,d,p,vel,ch)
 # Deliberately over-serious, original four-chord training cue in E minor.
 for i,(root,third,fifth) in enumerate([(40,55,59),(38,54,57),(36,52,55),(35,51,54)]):
  t=i*2.5;chord(t,2.15,[root,third,fifth],36,1)
  for j in [0,2]:note(t+j*.625,.3,root,42,3)
  for j,p in enumerate([third,fifth,third,fifth]):note(t+.313+j*.625,.18,p,39,2)
 for t,p in [(0.1,64),(1.35,67),(2.6,66),(3.85,69),(5.1,64),(6.35,67),(7.6,63),(8.85,66)]:note(t,.45,p,46,0)
 # Leave the first absurd landing room to register, without a comic slide whistle.
 for i,p in enumerate([52,55,59,57,54,59]):note(12.6+i*.625,.22,p,32,2)
 chord(16.875,1.45,[40,55,59],35,0)
 # New lesson: the same pomp returns after the second fall, a second payoff.
 restart=19.5
 for k in range(max(0,math.ceil((duration-restart)/2.5))):
  t=restart+k*2.5;root=40 if k%2==0 else 38
  chord(t,1.95,[root,root+19,root+24],32,1)
  for j in range(4):note(t+j*.625,.19,root+12+[0,7,3,7][j],37,2)
  note(t,.24,root,38,3);note(t+1.25,.24,root,36,3)
 if not front:
  chord(duration-4.75,2.3,[40,52,56,59],33,4);chord(duration-2.5,2.35,[40,52,56,59,64],31,1)
 events=[]
 for no in notes:events.extend([(round(no['start']*SR),1,no),(min(n,round((no['start']+no['duration'])*SR)),0,no)])
 events.sort(key=lambda x:(x[0],x[1]));score=np.zeros((n,2),np.float32);pos=0
 for idx,on,no in events:
  if idx>pos:score[pos:idx]=np.frombuffer(synth.generate(idx-pos),np.float32).reshape(-1,2);pos=idx
  if on:synth.noteon(no['channel'],no['pitch'],no['velocity'])
  else:synth.noteoff(no['channel'],no['pitch'])
 if pos<n:score[pos:]=np.frombuffer(synth.generate(n-pos),np.float32).reshape(-1,2)
 score*=.1/max(1e-9,float(np.abs(score).max()))
 # Fixed quiet musical gap, smooth 30ms fades at both edges.
 for a,b in [(10.8,12.2),(18.6,19.4)]:
  if b>=duration:continue
  ia,ib=round(a*SR),round(b*SR);ramp=round(.03*SR);score[ia-ramp:ia]*=np.linspace(1,0,ramp)[:,None];score[ia:ib]=0;score[ib:ib+ramp]*=np.linspace(0,1,ramp)[:,None]
 mix=score.copy();rng=np.random.default_rng(101325);effects=[]
 for t in [11.375,18.75]:
  d=.28;nn=round(d*SR);x=np.arange(nn)/SR;noise=rng.normal(size=nn+95);low=np.convolve(noise,np.ones(96)/96,'valid')
  w=(.65*low+.35*np.sin(2*np.pi*78*x))*np.exp(-x*22)
  w*=np.minimum(1,x/.006);w[-round(.045*SR):]*=np.linspace(1,0,round(.045*SR));w[0]=w[-1]=0
  w*=10**(-28/20)/max(1e-9,float(np.abs(w).max()));i=round(t*SR);end=min(n,i+nn)
  mix[i:end]+=w[:end-i,None]
  effects.append(dict(at=t,duration=d,type='soft broad mat contact',visible_cause='first actual seated mat landing in selected source',pre_mix_peak_dbfs=-28,source_t=3.75 if t<15 else 3.375,actual_listening_verified=False))
 for a in [mix,score]:
  a[:round(.08*SR)]*=np.linspace(0,1,round(.08*SR))[:,None]
  a[-round(.7*SR):]*=np.linspace(1,0,round(.7*SR))[:,None]
 assert np.isfinite(mix).all() and np.abs(mix).max()<.3
 for label,w in [('score',score),('mix',mix)]:run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',OUT/f'C01_{label}.wav'],input=w.astype('float32').tobytes())
 dump(OUT/'audio_recipe.json',dict(music='Original local E-minor training cue,96BPM, restrained horn/pizzicato/strings; no borrowed melody',source_audio='All generated audio muted',duration=duration,soundfont=str(SF),soundfont_sha256=sha(SF),programs=programs,notes=notes,effects=effects,actual_listening_verified=False))
 return OUT/'C01_mix.wav'

def mux(picture,dest):
 man=json.loads((OUT/'edit_manifest.json').read_text(encoding='utf-8'));duration=man['duration_seconds'];mix=soundtrack(duration,'front' in picture.name)
 result=run(['-hide_banner','-i',mix,'-af','loudnorm=I=-21:TP=-2:LRA=11:print_format=json','-f','null','-'])
 measurement=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',result.stderr.decode(errors='replace'))[-1]);gain=min(-21-float(measurement['input_i']),-2.3-float(measurement['input_tp']))
 run(['-y','-v','error','-i',picture,'-i',mix,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'volume={gain}dB,apad=pad_dur=0.2,atrim=duration={duration},asetpts=N/SR/TB','-c:a','aac','-b:a','192k','-ar',SR,'-t',duration,'-movflags','+faststart',dest])
 recipe=json.loads((OUT/'audio_recipe.json').read_text(encoding='utf-8'));recipe.update(static_gain_db=gain,input_loudness=measurement);dump(OUT/'audio_recipe.json',recipe)
 print('mux',dest,flush=True)
if __name__=='__main__':
 if '--front' in sys.argv:mux(OUT/'C01_front_working.mp4',OUT/'C01_front_review.mp4')
 else:mux(OUT/'C01_picture.mp4',OUT/'C01_Q-AI_Fair_final_v13.mp4')
