"""Eight new scene-scored instrumentals for Q-AI Fair V16, mathematical synthesis.

New notes, harmony, meter, phrasing and cue windows for each story. QREW DSP
primitives are reused as instruments, never as a finished melody or recording.
"""
from pathlib import Path
import sys,json,math,subprocess,re,hashlib
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
import numpy as np
import dsp_primitives as D
OUT=Path(__file__).resolve().parent; ROOT=OUT.parent.parent
FF=ROOT/'storyboards/2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SR=48000
DUR={'C02':36.25,'C03':43,'C04':43.5,'C05':46.75,'C06':48.75,'C07':32.6,'C08':53,'C09':44}
SILENCE={'C02':[(14.3,14.9),(20.75,21.65)],'C03':[(18.75,19.5)],
 'C04':[(28,31),(36.05,36.8)],'C05':[(13.25,14.25),(37.25,39)],
 'C06':[(28.75,29.5),(41.75,42.5)],'C07':[(4.8,6.3),(22.3,27.6)],
 'C08':[(23.1,26.75),(37.75,38.55)],'C09':[(17.25,18.95),(26.25,29.5),(31.25,34.25)]}
DESCR={
 'C02':'100 BPM noir detective groove: muted bass, clav, brushed percussion, electric piano; two exact evidence-reversal stops.',
 'C03':'108 BPM industrial delivery drama: analog pulses, dry percussion, metallic keys, increasingly layered shipments; open harmony on discovery.',
 'C04':'72 BPM solemn infiltration with low drum/open fifth/reed-like lead, then 90 BPM formal dining waltz at bowl reveal.',
 'C05':'80 BPM serious giant-monster pressure becomes a dry100 BPM maintenance groove, reusing its own three-note idea at smaller scale.',
 'C06':'96 BPM gothic electronic work motif transforms into late-night lounge, interrupted by new visitors and returning work.',
 'C07':'90 BPM formal three-beat tasting ceremony, precious-record reveal, then all music stops for the chair competition. Audio demo only.',
 'C08':'104 BPM practical office music; first heroic120 BPM brass arrives at15.5s, dies at23.1s, then104 BPM manual repair groove.',
 'C09':'76 BPM sincere farewell melodrama with new piano melody and restrained strings; all music/reverb stops at charger caption26.25s.'}

def run(args,**kw):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-5000:])
 return p
def measure(path):
 p=run(['-hide_banner','-i',path,'-af','loudnorm=I=-18.5:TP=-2:LRA=14:print_format=json','-f','null','-'])
 return {k:float(v) for k,v in json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',p.stderr.decode(errors='replace'))[-1]).items() if k.startswith('input_')}
def felt_piano(midi,duration):
 t=D.axis(duration);f=D.hz(midi)
 signal=np.zeros_like(t)
 for h in range(1,9):
  decay=max(.08,1.1/h**.85)
  stretch=1+.00012*h*h
  signal+=np.sin(2*np.pi*f*h*stretch*t+.035*h)*np.exp(-t/decay)/(h**1.85)
 signal+=.075*np.sin(2*np.pi*f*1.0017*t)*np.exp(-t/.65)
 return D.fade(signal,.008,min(.28,duration*.3))
def reed(midi,duration):
 t=D.axis(duration);f=D.hz(midi);phase=2*np.pi*f*t+.014*np.sin(2*np.pi*4.9*t)
 signal=sum(np.sin(h*phase)/(h**1.75) for h in [1,3,5,7])
 return D.fade(signal*(.91+.07*np.sin(2*np.pi*.7*t)),.055,min(.15,duration*.3))
INSTR={'piano':felt_piano,'reed':reed,'bass':D.funk_bass,'clav':D.clav,'ep':D.electric_key,
 'strings':D.strings,'pressure':D.low_blast,'drone':D.submarine,'pad':D.suspended_tone,
 'kettle':D.kettle,'pluck':D.pluck,'chime':D.chime}

class Score:
 def __init__(self,cid):
  self.cid=cid;self.duration=DUR[cid];self.n=round(self.duration*SR)
  self.dry=np.zeros((self.n,2),np.float32);self.send=np.zeros_like(self.dry)
  self.events=[];self.cues=[];self.rng=np.random.default_rng(16000+int(cid[1:]))
  D.RNG=np.random.default_rng(76126+int(cid[1:])*13)
 def add(self,inst,t,dur=.4,midi=60,gain=.15,pan=0,rev=.12,role='music'):
  if t>=self.duration or dur<=0:return
  dur=min(dur,self.duration-t)
  if inst in ['kick','snare','hat','rim','depth_pulse']:
   signal=getattr(D,inst)(duration=dur)
  elif inst=='brass':signal=D.brass_stab(midi,dur)
  else:signal=INSTR[inst](midi,dur)
  i=max(0,round(t*SR));n=min(len(signal),self.n-i)
  angle=(pan+1)*np.pi/4
  stereo=(signal[:n,None]*[np.cos(angle),np.sin(angle)]*gain).astype(np.float32)
  self.dry[i:i+n]+=stereo;self.send[i:i+n]+=stereo*rev
  self.events.append({'instrument':inst,'start':round(t,5),'duration':round(dur,5),'pitch':midi,'gain':gain,'pan':pan,'reverb_send':rev,'role':role})
 def cue(self,a,b,desc):self.cues.append({'start':a,'end':b,'description':desc})
 def chord(self,inst,t,dur,notes,gain=.2,rev=.3):
  for i,n in enumerate(notes):self.add(inst,t,dur,n,gain/math.sqrt(len(notes)),-.48+.96*i/max(1,len(notes)-1),rev)
 def melody(self,a,b,bpm,notes,gain=.15,inst='piano',beats=1.0):
  beat=60/bpm;t=a;i=0
  # Phrases breathe after the fourth note; answer phrases are not a one-bar loop.
  while t<b-.05:
   p=notes[i%len(notes)];phrase=i//len(notes)
   dur=min(beat*(1.3 if i%4==3 else .85),b-t)
   if i%8!=7:self.add(inst,t,dur,p+(12 if phrase%4==3 and inst=='chime' else 0),gain*(.87+.13*(i%3)/2),-.18 if i%2 else .14,.22)
   t+=beat*(1.5 if i%4==3 else beats);i+=1
 def groove(self,a,b,bpm,roots,chords,motif,style='office',density=1,gain=1):
  beat=60/bpm;bar=beat*4;idx=0
  for start in np.arange(a,b,bar):
   start=float(start);root=roots[idx%len(roots)];ch=chords[idx%len(chords)]
   if style=='noir':pattern=[(0,0,.55),(1.5,7,.28),(2.25,10,.20),(3.25,3,.42)]
   elif style=='industrial':pattern=[(0,0,.35),(1,0,.26),(2,7,.35),(3,2,.23)]
   elif style=='repair':pattern=[(0,0,.25),(.75,7,.16),(2,3,.22),(3.5,7,.18)]
   elif style=='gothic':pattern=[(0,0,.44),(1.75,7,.25),(2.5,3,.25),(3.25,2,.22)]
   else:pattern=[(0,0,.32),(1.25,7,.22),(2.5,4,.30),(3.5,2,.18)]
   for off,step,length in pattern:
    t=start+off*beat
    if t<b:self.add('bass',t,min(length,b-t),root+step,.24*gain,0,.035)
   for off in [0,2.0 if style!='repair' else 2.5]:
    t=start+off*beat
    if t<b:self.add('kick',t,min(.22,b-t),gain=.24*gain,rev=.01)
   for off in [1,3]:
    t=start+off*beat
    if t<b:self.add('rim' if style in ['noir','repair','office'] else 'snare',t,min(.13,b-t),gain=.12*gain,pan=-.12,rev=.025)
   if density>=1:
    for off in np.arange(0,4,.5):
     t=start+float(off)*beat
     if t<b:self.add('hat',t,min(.065,b-t),gain=(.028 if off%1 else .042)*gain,pan=.35,rev=0)
   # Chord responses differ between bars; neither constant pad nor one repeated hit.
   for off in ([.75,2.75] if idx%2==0 else [1.5,3.25]):
    t=start+off*beat
    if t<b:self.chord('clav' if style in ['noir','repair'] else 'ep',t,min(.32,b-t),[p+12 for p in ch[-3:]],.13*gain,.12)
   if density>=2 and idx%2==0:
    for k,p in enumerate(motif[:3]):
     t=start+(1+k*.65)*beat
     if t<b:self.add('ep' if style!='industrial' else 'chime',t,min(.4,b-t),p,.13*gain,-.25+.25*k,.18)
   idx+=1
 def waltz(self,a,b,bpm,roots,chords,melody,gain=.7):
  beat=60/bpm
  for j,t in enumerate(np.arange(a,b,3*beat)):
   t=float(t);root=roots[j%len(roots)];ch=chords[j%len(chords)]
   self.add('bass',t,min(.55,b-t),root,.20*gain,0,.08)
   for off in [1,2]:
    when=t+off*beat
    if when<b:self.chord('piano',when,min(.8,b-when),ch,.20*gain,.2)
   p=melody[j%len(melody)]
   self.add('reed' if j%3==2 else 'piano',t+.03,min(1.4*beat,b-t-.03),p,.12*gain,.15,.27)
 def sustained(self,a,b,chords,inst='strings',gain=.24,span=4):
  for j,t in enumerate(np.arange(a,b,span)):
   t=float(t);self.chord(inst,t,min(span+.12,b-t),chords[j%len(chords)],gain,.45)
 def finish(self):
  mix=self.dry.copy()
  for sec,gain,swap in [(.037,.29,False),(.083,.23,True),(.157,.18,False),(.271,.12,True),(.419,.08,False),(.613,.05,True)]:
   n=round(sec*SR);mix[n:]+=self.send[:-n,::-1] * gain if swap else self.send[:-n]*gain
  # The whole music and reverb are gated together at story reveals.
  for a,b in SILENCE[self.cid]:
   ia,ib=round(a*SR),round(b*SR);fade=round(.006*SR)
   mix[max(0,ia-fade):ia]*=np.linspace(1,0,min(fade,ia))[:,None]
   mix[ia:ib]=0
   n=min(round(.012*SR),len(mix)-ib);mix[ib:ib+n]*=np.linspace(0,1,n)[:,None]
  mix[:480]*=np.linspace(0,1,480)[:,None]
  mix[-round(.45*SR):]*=np.linspace(1,0,round(.45*SR))[:,None]
  folder=OUT/'audio'/self.cid;folder.mkdir(parents=True,exist_ok=True)
  raw=folder/f'{self.cid}_score_raw_v16.wav';wav=folder/f'{self.cid}_score_v16.wav'
  run(['-y','-v','error','-f','f32le','-ar',SR,'-ac',2,'-i','-','-c:a','pcm_f32le',raw],input=mix.astype(np.float32).tobytes())
  before=measure(raw);gain=-18.5-before['input_i']
  run(['-y','-v','error','-i',raw,'-af',f'volume={gain}dB,alimiter=limit=0.70:attack=5:release=85:level=0:latency=1',
       '-t',self.duration,'-ar',SR,'-c:a','pcm_s24le',wav])
  after=measure(wav)
  run(['-y','-v','error','-i',wav,'-c:a','libmp3lame','-b:a','192k',folder/f'{self.cid}_music_preview_v16.mp3'])
  rec={'concept_id':self.cid,'duration_seconds':self.duration,'description':DESCR[self.cid],
   'scope':'audio demo only; no C07 video exists' if self.cid=='C07' else 'new music for existing video',
   'original_new_composition':True,'source_music_reused':False,'voice_or_lyrics':False,
   'dsp_basis':'See ../../dsp_provenance.json; instrument functions only.',
   'cues':self.cues,'events':self.events,'silence_windows':SILENCE[self.cid],
   'mastering':{'fixed_gain_db':gain,'limiter_ceiling':.70,'raw_loudness':before,'final_wav_loudness':after},
   'file':wav.name,'sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),
   'actual_listening_verified':False,'subjective_naturalness_verified':False}
  (folder/'score_manifest.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(self.cid,'score',self.duration,'seconds',len(self.events),'events',after,flush=True)

def create(cid):
 s=Score(cid)
 if cid=='C02':
  roots=[41,37,39,36];ch=[[41,48,56,60],[37,44,53,60],[39,46,55,62],[36,43,52,58]];mot=[65,68,67,60]
  for a,b,den,g in [(0,6.25,0,.75),(6.25,12.25,2,.95),(12.25,14.3,0,.45),(14.9,20.75,2,1),(21.65,31.5,1,.65)]:s.groove(a,b,100,roots,ch,mot,'noir',den,g)
  s.melody(31.5,35.5,100,[65,67,60,65],.17,'ep');s.chord('ep',34.3,1.6,[41,48,56,60,67],.20,.23)
  s.cue(0,14.3,'Serious noir investigation; evidence comparison adds dry syncopation.')
  s.cue(14.3,14.9,'Wiped spot reveal: complete music/reverb stop.')
  s.cue(14.9,20.75,'The detective regains confidence; investigation groove resumes before the cuff reversal.')
  s.cue(20.75,21.65,'Cuff creates new trace: self-confidence interrupted.')
  s.cue(21.65,36.25,'Smaller record-keeping groove, same musical identity resolves without fanfare.')
 elif cid=='C03':
  roots=[40,36,33,38];ch=[[40,47,54,59],[36,43,52,59],[33,40,50,52],[38,45,54,57]];mot=[64,71,66,69]
  s.sustained(0,6,[[40,47,54]],'drone',.10,3)
  for a,b,den,g in [(0,6,0,.40),(6,12.5,1,.7),(12.5,13.5,0,.35),(13.5,18.75,2,.95),(19.5,23.25,0,.25),(23.25,29,2,.7),(29,35,2,.9),(35,37,2,1.1)]:s.groove(a,b,108,roots,ch,mot,'industrial',den,g)
  s.chord('ep',26.25,1.6,[40,47,55,59,66],.23,.16)
  s.sustained(37,43,[[40,47,56,59],[45,52,59,61]],'ep',.26,2.2)
  s.melody(37.15,42.3,108,[64,66,71,68,64],.15,'chime')
  s.cue(0,18.75,'Industrial shipping pulse grows with each delivered environment; glove inserts stay thin.')
  s.cue(18.75,19.5,'Phone-answer gap, reverb included.')
  s.cue(19.5,23.25,'A thin industrial pulse continues under the reply, leading into the delivered records.')
  s.cue(23.25,37,'Records and discovery open the harmony; purposeful action returns the pulse.')
  s.cue(37,43,'Open, concise event cadence.')
 elif cid=='C04':
  s.sustained(0,28,[[36,43],[32,39],[34,41],[31,38]],'drone',.13,5.5)
  for i,t in enumerate(np.arange(.25,23,60/72*2)):
   s.add('kettle',float(t),.6,36 if i%2==0 else 31,.18,pan=-.1,rev=.35)
   if t>11:s.add('reed',float(t+.7),.55,[60,63,67,62,65][i%5],.10,.2,.22)
  s.chord('reed',19,3.8,[55,62],.13,.25)
  s.waltz(31,43.5,90,[36,41,43,36],[[60,64,67],[57,60,65],[59,62,67],[60,64,67,74]],[67,64,72,67],.78)
  s.cue(0,19,'Solemn low-drum infiltration, open fifths and cautious reed replies.')
  s.cue(19,28,'Utensil question holds its breath; denial thins the score to bass pressure.')
  s.cue(28,31,'Window reveal kills the military score and its reflections.')
  s.cue(31,43.5,'Bowl and spoon become excessively formal dining waltz; commander caption gets a stop.')
 elif cid=='C05':
  s.sustained(0,13.25,[[31,38,46],[27,34,43],[29,36,45]],'strings',.23,4.4)
  for i,t in enumerate([.2,2.45,4.7,7.25,9.5,10.25,11.75,12.5]):
   s.add('pressure',t,min(1.4,13.25-t),[31,27,29][i%3],.24,0,.48)
   s.add('kettle',t,.65,31,.22,-.13,.35)
  s.melody(7.25,13.25,80,[55,58,57,62],.12,'strings')
  s.sustained(14.25,21.75,[[31,38,45],[31,38,46]],'drone',.11,3.75)
  roots=[43,39,41,38];ch=[[43,50,58,62],[39,46,55,62],[41,48,57,60],[38,45,54,60]]
  for a,b,d,g in [(21.75,24.25,1,.75),(24.25,31.5,1,.7),(31.5,36.85,0,.45)]:s.groove(a,b,100,roots,ch,[67,70,69],'repair',d,g)
  s.add('bass',36.85,.4,43,.18)
  s.melody(39,41.7,100,[55,58,57],.11,'clav')
  s.chord('ep',41.75,2.2,[43,50,59,62],.22,.3);s.melody(42.1,46,100,[67,69,71,67],.14,'ep')
  s.cue(0,13.25,'Earnest large-scale monster pressure; one rising entry phrase.')
  s.cue(13.25,14.25,'Head trapped: full music stop at the caption.')
  s.cue(14.25,21.75,'Uneasy low held tones, no arbitrary impacts on every edit.')
  s.cue(21.75,36.85,'Visible worker starts the maintenance rhythm; orchestration gradually drops out as humans leave.')
  s.cue(36.85,46.75,'One bass note then silence, small motif on hand release, bright event cadence.')
 elif cid=='C06':
  s.sustained(0,5,[[30,42,49,57]],'drone',.19,5)
  s.add('chime',.4,1,66,.05,.4,.4);s.add('pressure',5,1.1,30,.14,0,.2)
  s.add('kettle',6.125,.45,30,.27,0,.08,role='single verified desk-contact accent')
  roots=[42,38,45,37];ch=[[42,49,57,61],[38,45,54,61],[45,52,56,61],[37,44,53,59]];mot=[66,73,69,68]
  for a,b,d,g in [(6.5,14.25,1,.7),(14.25,20.75,2,.65),(20.75,25.75,0,.4),(29.5,33.25,0,.25),(37.75,41.75,1,.45)]:s.groove(a,b,96,roots,ch,mot,'gothic',d,g)
  s.waltz(25.75,28.75,72,[38],[[54,57,61,64]],[69,66],.65)
  s.melody(33.25,37.75,96,[66,69,73,68],.17,'ep')
  s.chord('ep',42.5,2,[42,49,58,61],.22,.26);s.melody(44,48,96,[66,68,73,66],.13,'ep')
  s.cue(0,6.5,'Gothic electronic pressure; one accent follows the observed desk contact at6.125s.')
  s.cue(6.5,25.75,'The ghost begins working: a regular rhythm steadies and then winds down.')
  s.cue(25.75,29.5,'Late-night lounge appears, then new visitors interrupt it exactly.')
  s.cue(29.5,48.75,'Quiet inquiry, orderly event motif, return of work rhythm and reaction silence.')
 elif cid=='C07':
  roots=[46,43,39,41];ch=[[58,62,65],[55,58,62],[55,58,63],[57,60,65]];mel=[70,72,77,74]
  s.waltz(0,11,90,roots,ch,mel,.65)
  s.sustained(11,15,[[58,62,65],[60,65,69]],'strings',.22,2)
  s.melody(11.2,15,90,[70,74,77,79],.13,'strings')
  s.waltz(15,22.3,90,roots,ch,[77,74,72,70],.88)
  s.chord('piano',27.6,2,[46,53,62,65],.22,.3);s.melody(28,32,90,[70,72,77,70],.14,'piano')
  s.cue(0,11,'Formal tasting waltz; one-line recipe receives a dry stop.')
  s.cue(11,15,'Trial records treated as an absurdly precious treasure.')
  s.cue(15,22.3,'Ceremonial serving theme grows without copying a known tune.')
  s.cue(22.3,27.6,'Chair competition is deliberately unscored; exact motion sounds await actual footage.')
  s.cue(27.6,32.6,'Brief return to the original formal theme. Demo only, no video.')
 elif cid=='C08':
  roots=[45,41,48,43];ch=[[45,52,60,64],[41,48,57,60],[48,55,60,64],[43,50,59,62]];mot=[69,72,76,74]
  s.sustained(0,2.75,[[45,52,59]],'drone',.09,2.75)
  s.groove(2.75,6.75,104,roots,ch,mot,'office',0,.45)
  s.groove(6.75,15.5,104,roots,ch,mot,'office',2,.7)
  s.sustained(15.5,23.1,[[38,45,54,57],[43,50,59,62]],'strings',.3,3.8)
  for i,t in enumerate([15.5,16.5,17.75,19.0,20.75,22.0]):
   s.add('brass',t,min(.7,23.1-t),[[62,66,69],[64,67,71],[66,69,74]][i%3],.38,0,.4)
   s.add('kick',t,.25,gain=.4,rev=.1)
  s.groove(26.75,36.25,104,roots,ch,mot,'repair',1,.75)
  s.groove(36.25,37.75,104,roots,ch,mot,'repair',0,.28)
  s.groove(38.55,48,104,roots,ch,mot,'repair',1,.55)
  s.chord('ep',48,2.1,[45,52,61,64],.25,.2);s.melody(48.2,52.4,104,[69,73,76,69],.14,'clav')
  s.cue(0,15.5,'Practical office score, no hero brass while AI template and human check are shown.')
  s.cue(15.5,23.1,'First heroic brass at actual entrance, serious cinematic gesture held through landing.')
  s.cue(23.1,26.75,'Already finished caption: complete heroic music and reverb stop.')
  s.cue(26.75,48,'Manual repair groove; level-check caption37.75 receives a second dry stop.')
  s.cue(48,53,'Office theme resolves, not a second heroic fanfare.')
 elif cid=='C09':
  chords=[[39,46,55,58],[35,42,51,58],[36,43,51,55],[34,41,50,56]]
  s.melody(.15,2.5,76,[67,65,63],.12,'piano')
  s.sustained(2.5,17.25,chords,'strings',.17,3.16)
  s.melody(2.6,17.25,76,[67,65,63,58,60,62],.22,'piano')
  for i,t in enumerate(np.arange(2.5,17.25,3.16)):s.add('bass',float(t),.9,[39,35,36,34][i%4],.13,0,.2)
  s.sustained(18.95,26.25,[[39,46,55,58],[44,51,60,63]],'strings',.21,3.65)
  s.melody(19,26.25,76,[67,70,72,74,72,70,67],.25,'piano')
  s.add('ep',29.6,.65,63,.12,-.1,.12);s.add('ep',30.4,.7,67,.10,.12,.12)
  s.melody(34.5,38.8,76,[67,65,63,58],.13,'piano',1.2)
  s.chord('piano',39,2,[39,46,55,58,65],.24,.27);s.melody(39.25,43.4,76,[67,65,70,63],.17,'piano')
  s.cue(0,17.25,'Sincere new farewell theme; charger setup stays understated and boarding grows without drums.')
  s.cue(17.25,18.95,'Call caption gets a quiet gap before hope returns.')
  s.cue(18.95,26.25,'Protagonist expects to be needed: melody expands with his return.')
  s.cue(26.25,29.5,'Exact charger-question caption onset: all music/reverb to zero.')
  s.cue(29.5,34.25,'Two small handoff notes; departing bus unscored.')
  s.cue(34.25,44,'An unfinished farewell fragment for being left behind; restrained warm ending.')
 s.finish()

if __name__=='__main__':
 for cid in sys.argv[1:] or list(DUR):create(cid)
