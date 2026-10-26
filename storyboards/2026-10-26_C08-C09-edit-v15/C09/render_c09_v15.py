"""C09 postproduction, real clips only. Final rendering refuses unreviewed/missing clips.
--prepare writes captions, score, endcard and available-frame compositor previews only.
"""
from pathlib import Path
import sys,json,subprocess,math
OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(OUT.parent))
from media_common import *
SOURCE=SB/'2026-10-26_C08-C09-flow-v15'
plan=json.loads((OUT/'edit_plan.json').read_text(encoding='utf8'))
EDL=plan['timeline'];by={s['cut']:s for s in EDL};duration=EDL[-1]['end']+5
assert duration<=60
assert all(abs((s['source_out']-s['source_in'])-(s['end']-s['start']))<1e-6 for s in EDL)
assert all(abs(a['end']-b['start'])<1e-6 for a,b in zip(EDL,EDL[1:]))

CAPS=[]
def cap(cut,a,b,text,pos='bottom',x=None,y=None,kind='subtitle'):
 s=by[cut];assert 0<=a<b<=s['end']-s['start']
 CAPS.append(dict(start=s['start']+a,end=s['start']+b,text=text,pos=pos,x=x,y=y,font_px=42,kind=kind))
cap('K02',.15,4.1,'저 없이 괜찮겠어요?','top',760,43)
cap('K03',.1,4.9,'공유해주신 AI 방법,\n제가 해보고 확인했어요.')
cap('K04',.2,3.1,'편히 쉬고 오세요.','top',64,43)
cap('K05',.1,1.6,'전화 · 동료','top',825,43,'external_call_badge')
cap('K05',1.7,4.6,'역시.','top',940,43)
CAPS.append(dict(start=by['K07']['start']-1.25,end=by['K07']['end']-.05,text='혹시 제 충전기…',pos='bottom',x=None,y=None,font_px=42,kind='subtitle_question_before_reveal'))
CAPS.append(dict(start=by['K08']['start']+.1,end=by['K09']['start']+1.5,text='고마워요. 푹 쉬세요.',pos='bottom',x=None,y=None,font_px=42,kind='subtitle_across_handoff_cut'))
CAPART=[(c['start'],c['end'],caption(c['text'],c['pos'],c['x'],c['y'])) for c in CAPS]
end=ending(plan['ending']['tagline'],accent=(206,117,49));end.save(OUT/'ending_v15.png')

def build_score():
 notes=[]
 def add(t,d,p,v,ch):
  if t<duration:notes.append(dict(start=round(t,4),duration=round(min(d,duration-t),4),pitch=p,velocity=v,channel=ch))
 # Original melodic cue: slow piano/cello/strings, deliberately excessive farewell.
 # No reused source melody or audio; no human speech or sung words.
 programs={0:0,1:48,2:42,3:46,4:70}
 for t,p in [(0.12,62),(.7,69),(1.4,65),(2.0,69)]:add(t,.75,p,28,0)
 chords=[[50,57,62,65],[46,53,58,62],[48,55,60,64],[45,52,57,61]]
 beat=.8
 farewell_start=by['K02']['start'];departure_end=by['K04']['end']
 for bar,t in enumerate(np.arange(farewell_start,departure_end,3.2)):
  chord=chords[bar%4]
  for p in chord:add(float(t),min(2.9,departure_end-t),p,24,1)
  add(float(t),2.8,chord[0]-12,31,2)
  for k,p in enumerate([chord[0]+12,chord[2]+12,chord[3]+12,chord[2]+12]):
   if t+k*beat<departure_end:add(float(t+k*beat),.8,p,33,0)
 # The phone call revives the protagonist's grand romantic hope.
 hope=by['K05']['start']+1.65;reveal=by['K07']['start']
 for k,t in enumerate(np.arange(hope,reveal,.7)):
  add(float(t),.62,[69,72,74,77,76,74,72,69][k%8],35,0)
  if k%4==0:
   for p in [50,57,65]:add(float(t),min(2.65,reveal-t),p,30,1)
 # Charger reveal breaks the score. The following small warmth is not mockery.
 rests=[(by['K05']['start'],hope-.05),(reveal,by['K08']['start']+.65),
        (by['K09']['start'],by['K10']['start'])]
 for t in [by['K08']['start']+.7,by['K08']['start']+2.6]:
  for p in [50,57,62]:add(t,1.4,p,27,0)
 # After the departing bus, a tiny unresolved bassoon phrase echoes the melodrama.
 for k,p in enumerate([62,60,57]):add(by['K10']['start']+.2+k*.75,.45,p,25,4)
 for t in [EDL[-1]['end']+.1,EDL[-1]['end']+2.4]:
  for p in [50,57,62,65]:add(t,1.8,p,25,0)
 # An understated two-note electronic ring follows only the visible incoming call.
 effects=[dict(at=by['K05']['start']+.2,duration=.12,frequency=880,peak=.004,visual_cause='External incoming-call badge while black phone is visible'),
          dict(at=by['K05']['start']+.47,duration=.12,frequency=1175,peak=.0035,visual_cause='Second note of the same incoming-call cue')]
 wav=OUT/'C09_original_score_v15.wav';gain,measurement=synthesize(notes,programs,duration,wav,rests,effects)
 dump(OUT/'audio_recipe.json',dict(programs=programs,notes=notes,rests_seconds=rests,effects=effects,soundfont=str(SF),soundfont_sha256=sha(SF),source_audio='ALL GENERATED AUDIO EXCLUDED',music='Original locally composed sentimental piano/cello/strings, charger reveal silence, understated warm ending',static_gain_db=gain,loudness_before_gain=measurement,actual_listening_verified=False))
 return wav,gain

def write_captions():
 caps=CAPS+[dict(start=EDL[-1]['end'],end=duration,text='Q-AI Fair\n'+plan['ending']['tagline']+'\n품질팀 AI 성과 교류회',kind='endcard')]
 def ts(t):
  m=round(t*1000);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
 (OUT/'C09_captions_v15.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n',encoding='utf-8-sig')
 dump(OUT/'caption_manifest.json',caps)
 return caps

def composite(frame,t,seg=None):
 if seg and 'crop' in seg:frame=frame.crop(tuple(seg['crop'])).resize((W,H),Image.Resampling.LANCZOS)
 im=frame.convert('RGBA')
 for a,b,art in CAPART:
  if a<=t<b:im.alpha_composite(art)
 return im.convert('RGB')

def preview():
 folder=OUT/'composite_previews';folder.mkdir(exist_ok=True)
 for s in EDL:
  path=SOURCE/s['file']
  if not path.exists():continue
  targets={round((s['source_in']+j)*FPS) for j in [.5,1.8,3.] if s['source_in']+j<s['source_out']}
  with av.open(str(path)) as c:
   for i,f in enumerate(c.decode(video=0)):
    if i in targets:
     st=float(f.time);t=s['start']+st-s['source_in'];composite(f.to_image(),t,s).save(folder/f'{s["cut"]}_{st:04.2f}s.png')
 print('PREPARED: captions, available-frame composites, endcard and provisional score',flush=True)

def main(prepare=False):
 caps=write_captions()
 if prepare:build_score();preview();return
 assert all(s['approved_for_final'] for s in EDL),'Every real original must be visually reviewed; repaired K04 mandatory.'
 assert all((SOURCE/s['file']).exists() for s in EDL),'Missing real source clip'
 hashes={s['file']:sha(SOURCE/s['file']) for s in EDL};pic=OUT/'C09_picture_v15.mp4';n=0
 with (OUT/'render_stderr.txt').open('wb') as log:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p',str(pic)],stdin=subprocess.PIPE,stderr=log)
  try:
   for s in EDL:
    ct=0
    with av.open(str(SOURCE/s['file'])) as c:
     assert float(c.streams.video[0].average_rate)==FPS
     for f in c.decode(video=0):
      st=float(f.time)
      if st<s['source_in']-1e-6:continue
      if st>=s['source_out']-1e-6:break
      t=s['start']+st-s['source_in'];enc.stdin.write(composite(f.to_image(),t,s).tobytes());n+=1;ct+=1
    assert ct==round((s['end']-s['start'])*FPS)
    print('RENDERED',s['cut'],ct,flush=True)
   for i in range(5*FPS):enc.stdin.write(end.tobytes());n+=1
  finally:enc.stdin.close();enc.wait()
 assert enc.returncode==0 and n==round(duration*FPS)
 wav,gain=build_score();final=OUT/'C09_Q-AI_Fair_screening_v15.mp4';mux(pic,wav,final,duration,gain)
 q=technical_qa(final,OUT,duration,[s['start'] for s in EDL]+[EDL[-1]['end']])
 assert hashes=={s['file']:sha(SOURCE/s['file']) for s in EDL}
 dump(OUT/'edit_manifest.json',dict(concept_id='C09',file=final.name,duration_seconds=duration,timeline=EDL,captions=caps,source_sha256=hashes,source_audio='ALL EXCLUDED',original_files_unchanged=True,action_stills_inserted=False,end_card_seconds=5,ui='External incoming-call badge; no fake UI printed on phone back. Shared AI application and human check are explicit post captions.',known_editorial_compromises=plan['known_editorial_compromises'],status='TECHNICAL_PASS_VISUAL_REVIEW_PENDING',actual_listening_verified=False,actual_continuous_playback_verified=False,technical_qa=q))
 print('DONE',final.name,duration,q['sha256'],flush=True)

if __name__=='__main__':main('--prepare' in sys.argv)
