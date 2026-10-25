"""C05 causal-repair derivative. Flow originals and previous edits stay read-only.

All action frames come from original videos; only titles/captions are graphics.
No paid service is called. Rejected new creature variants are excluded; a real worker cutaway covers a temporal ellipsis.
"""
from pathlib import Path
import sys,json,hashlib,subprocess,math,importlib.util
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/faster-whisper')
sys.path.insert(0,'C:/Users/wseok/.cache/codex-media-tools/tinysoundfont')
import av,numpy as np
from PIL import Image,ImageDraw,ImageFont
from tinysoundfont import Synth
OUT=Path(__file__).resolve().parent;SB=OUT.parent.parent
FF=SB/'2026-10-15_flow-pilot-01/.tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SF=Path('C:/Users/wseok/.cache/codex-media-tools/soundfonts/GeneralUser-GS-2.0.3/GeneralUser-GS.sf2')
FPS,W,H,SR=24,1280,720,48000
# Read-only import of the established v04 DSP functions, no render call.
spec=importlib.util.spec_from_file_location('prior_dsp',SB/'2026-10-23_C05-C06-edit-v04/polish_edits.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
R1='2026-10-23_C06-C05-flow-run01';R3='2026-10-23_C06-C05-flow-run03';N='2026-10-24_C05-first-flow-run01';V='2026-10-25_final-six-v13';R='2026-10-24_C01-C06-repair110'
TIMELINE=[
 ('K01',R3,'C05_K01_take02',0,3.25,None),
 ('K02A',R1,'C05_K02A_take01',1.75,5.75,None),
 ('K02B',R1,'C05_K02B_take02',.5,3.5,None),
 ('N01_entry',N,'C05_N01_take01',.5,4.5,None),
 ('N02_hands_grip_front_edge',N,'C05_N02_take02',1.5,4.5,None),
 ('N03_neck_withdraws',N,'C05_N03_take01',3,7.5,None),
 ('K04_worker_jack_insert',R,'C05_K04_jack_detail_take01',1.5,3,None),
 ('K04_wide',R1,'C05_K04_take02',2.5,3.25,None),
 ('K04_plead',R1,'C05_K04_take02',4.5,7.25,None),
 ('K05',R1,'C05_K05_take02',.5,5.25,None),
 ('K06',R3,'C05_K06_take02',.5,3.5,None),
 ('K07',R3,'C05_K07_take02',1,5.5,None),
 ('K08_thumb',R1,'C05_K08_take01',.5,1.5,None),
 ('K08_return',R3,'C05_K08_take02',0,6.75,None)]
CAPTIONS=[(.6,3.15,'이 입구는 내가 접수한다.'),(13.25,14.25,'어…?'),(24.25,26.55,'조금만 더 잡아주세요.'),(26.95,30.35,'잠시 후, AI 실행 사례 공개'),(36.85,38.85,'들리세요?')]
CUES=[(3.85,.85,'stone_scrape',-31,0,'pillar pulled away with visible dust'),(7,.38,'stone_land',-26,-.15,'pillar settles before empty-hand shot'),(13.25,.52,'structural_stress',-33,0,'neck caught under roof'),(21.95,1.15,'wheels',-37,.3,'sharp original of worker rolling jack'),(31.75,2,'wheels',-36,-.3,'ladder rolls'),(39.5,.42,'structural_stress',-32,0,'supporting hand leaves roof')]
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,**kw):
 p=subprocess.run([str(FF),*map(str,args)],capture_output=True,**kw)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-5000:])
 return p
def font(s):return ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',s)
def cap(tx):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im);tw=d.textlength(tx,font=font(42));x=(W-tw)/2;y=597
 d.rounded_rectangle((x-23,y,x+tw+23,y+75),12,fill=(7,14,22,218));d.text((640,y+37),tx,font=font(42),fill='white',anchor='mm');return im
def ending():
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 d.rounded_rectangle((228,547,1052,695),18,fill=(9,18,24,229))
 d.text((640,591),'Q-AI Fair',font=font(65),fill='white',anchor='mm')
 d.text((640,657),'AI 실행 사례, 지금 시작합니다.',font=font(36),fill=(223,242,241),anchor='mm');return im
def tile(im,label):
 z=Image.new('RGB',(320,205),(12,22,31));z.paste(im.resize((320,180)),(0,25));ImageDraw.Draw(z).text((8,3),label,font=font(15),fill='white');return z
def sheets(tiles,prefix,size=20):
 for batch in range(math.ceil(len(tiles)/size)):
  items=tiles[batch*size:(batch+1)*size];im=Image.new('RGB',(1280,205*math.ceil(len(items)/4)),(12,22,31))
  for i,v in enumerate(items):im.paste(v,((i%4)*320,(i//4)*205))
  im.save(OUT/f'{prefix}_{batch+1:02d}.jpg',quality=94)
def audio(duration):
 n=round(duration*SR);oldscorepath=SB/'2026-10-23_C05-C06-edit-v04/C05/C05_score.wav'
 prior=old.decode_audio(oldscorepath);score=np.zeros((n,2),np.float32)
 score[:round(8.5*SR)]=prior[:round(8.5*SR)]
 score[round(21.75*SR):]=prior[round(12.75*SR):round(37.75*SR)]
 # Existing string timbre, new quiet sustain bridges the longer visible cause chain.
 synth=Synth(gain=-12,samplerate=SR);sid=synth.sfload(str(SF));synth.program_select(0,sid,0,48)
 for p in [33,40,48]:synth.noteon(0,p,20)
 ln=round((21.75-8.5)*SR);bridge=np.frombuffer(synth.generate(ln),np.float32).reshape(-1,2).copy()
 bridge*=.009/max(1e-8,float(np.abs(bridge).max()))
 for p in [33,40,48]:synth.noteoff(0,p)
 fade=round(.25*SR);bridge[:fade]*=np.linspace(0,1,fade)[:,None];bridge[-fade:]*=np.linspace(1,0,fade)[:,None]
 score[round(8.5*SR):round(21.75*SR)]=bridge
 fade=round(.045*SR)
 for at in [8.5,21.75]:
  i=round(at*SR);score[i-fade:i]*=np.linspace(1,0,fade)[:,None];score[i:i+fade]*=np.linspace(0,1,fade)[:,None]
 rng=np.random.default_rng(202605);fx=np.zeros_like(score);events=[]
 for at,d,kind,db,pan,reason in CUES:
  mono=old.foley(kind,d,rng)*10**(db/20);wave=mono[:,None]*np.array([[math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)]])
  i=round(at*SR);fx[i:i+len(wave)]+=wave
  events.append(dict(at=at,duration=d,kind=kind,pre_mix_peak_dbfs=db,pan=pan,visible_cause=reason,boundary_samples=[float(mono[0]),float(mono[-1])]))
 amb=old.ramp_edges(old.smooth_noise(rng,n,350),.6,.8)*10**(-57/20);mix=score+fx+np.column_stack((amb,amb))
 mix[:round(.05*SR)]*=np.linspace(0,1,round(.05*SR))[:,None];mix[-round(.65*SR):]*=np.linspace(1,0,round(.65*SR))[:,None]
 for name,x in [('score',score),('fx',fx),('mix',mix)]:old.write_wav(OUT/f'C05_{name}.wav',x)
 m=old.loudness(OUT/'C05_mix.wav');gain=min(-21-float(m['input_i']),-2.3-float(m['input_tp']))
 dump(OUT/'audio_recipe.json',dict(source_audio='All source speech/audio removed',music='Existing v04 composition reused at 0–8.5 and 12.75–37.75 mapped to 21.75–46.75. Quiet sustained strings 33/40/48 velocity20 bridge 8.5–21.75.',source_score=str(oldscorepath.relative_to(SB)),source_score_sha256=sha(oldscorepath),soundfont_sha256=sha(SF),bridge_peak_before_mix=.009,effects=events,old_9_78_stress_removed=True,no_added_hand_impact_collapse_or_jack_click=True,normalization='One measured fixed gain; continuous audio PTS; no lookahead limiter',static_gain_db=gain,target_lufs=-21,actual_listening_verified=False))
 return gain,events
def main():
 segs=[];cursor=0
 for cut,runid,name,a,b,crop in TIMELINE:
  segs.append(dict(cut=cut,source=f'{runid}/{name}.mp4',source_in=a,source_out=b,start=cursor,end=cursor+b-a,crop=crop));cursor+=b-a
 assert cursor==46.75;duration=cursor;expected=1122
 hashes={s['source']:sha(SB/s['source']) for s in segs}
 capdata=[dict(start=a,end=b,text=tx,position='bottom',font_px=42) for a,b,tx in CAPTIONS]
 capdata.append(dict(start=41.75,end=46.75,text='Q-AI Fair\nAI 실행 사례, 지금 시작합니다.',position='ending'))
 manifest=dict(film='C05',version=13,duration_seconds=duration,fps=FPS,resolution=[W,H],segments=segs,captions=capdata,source_sha256=hashes,flow_credits_for_edit=0,source_audio='muted',action_stills_inserted=False,source_of_picture='Original Flow MP4s only; no baked-caption video reused',causal_design='pillar removal → attempted entrance → neck caught → front grip → neck withdrawal → worker jack cutaway covering a clear temporal ellipsis → original long-neck front support → front view',limitations=['Full outward turn and continuous hand transfer NOT captured. N03 neck withdrawal is followed by an actual worker jack cutaway, then the original long-neck front support. This is a temporal ellipsis, not a continuous action.','N05–N08 variants excluded entirely for character/anatomy/support/dissolve defects.','Jack shot establishes transport only, not a verified stop/lift action.','All source speech removed; actual listening not verified.'],status='render and sample review pending',actual_realtime_playback_verified=False,actual_listening_verified=False)
 dump(OUT/'edit_manifest.json',manifest)
 (OUT/'C05_captions.srt').write_text('\n\n'.join(f'{i+1}\n{old.srt_time(q["start"])} --> {old.srt_time(q["end"])}\n{q["text"]}' for i,q in enumerate(capdata))+'\n',encoding='utf-8-sig')
 caps=[(a,b,cap(tx)) for a,b,tx in CAPTIONS];end=ending();end.save(OUT/'ending_overlay.png')
 picture=OUT/'C05_picture.mp4';crop_tiles=[]
 with (OUT/'render_stderr.txt').open('wb') as err:
  enc=subprocess.Popen([str(FF),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(picture)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=err)
  fc=0
  try:
   for s in segs:
    count=0;needed=round((s['source_out']-s['source_in'])*FPS)
    with av.open(str(SB/s['source'])) as con:
     for f in con.decode(video=0):
      st=float(f.time)
      if st<s['source_in']-1e-5:continue
      if st>=s['source_out']-1e-5:break
      t=fc/FPS;im=f.to_image()
      if s['crop']:
       x,y,w,h=s['crop'];assert x>=0 and y>=0 and x+w<=im.width and y+h<=im.height
       im=im.crop((x,y,x+w,y+h)).resize((W,H),Image.Resampling.LANCZOS);crop_tiles.append(tile(im,f'src {st:.3f}s / out {t:.3f}s'))
      im=im.convert('RGBA')
      for a,b,c in caps:
       if a<=t<b:im.alpha_composite(c)
      if t>=41.75:im.alpha_composite(end)
      enc.stdin.write(im.convert('RGB').tobytes());fc+=1;count+=1
    assert count==needed,(s,count,needed)
    print(s['cut'],count,flush=True)
  finally:enc.stdin.close();enc.wait()
 assert enc.returncode==0 and fc==expected;sheets(crop_tiles,'worker_crop_all_frames',36)
 gain,events=audio(duration);final=OUT/'C05_Q-AI_Fair_final_v13.mp4'
 run(['-y','-v','error','-i',picture,'-i',OUT/'C05_mix.wav','-map','0:v','-map','1:a','-c:v','copy','-af',f'volume={gain}dB,apad=pad_dur=0.2,atrim=duration={duration},asetpts=N/SR/TB','-c:a','aac','-b:a','256k','-ar',SR,'-t',duration,'-movflags','+faststart',final])
 run(['-v','error','-i',final,'-f','null','-']);pcm=old.decode_audio(final);assert np.isfinite(pcm).all() and np.abs(pcm).max()<1
 audio_end=0.;gaps=[];audio_samples=0
 with av.open(str(final)) as con:
  for f in con.decode(audio=0):gaps.append(float(f.time)-audio_end);audio_end=float(f.time)+f.samples/f.sample_rate;audio_samples+=f.samples
 assert max(abs(x) for x in gaps)<1/SR and abs(audio_end-duration)<1/SR
 frames=OUT/'review_frames';frames.mkdir(exist_ok=True)
 samples=set(range(0,expected,12))|{expected-1};joinframes=set()
 for s in segs[1:]:
  j=round(s['start']*FPS);joinframes|={j-1,j,j+1}
 samples|=joinframes;thumbs=[];joins=[];times=[]
 with av.open(str(final)) as con:
  for i,f in enumerate(con.decode(video=0)):
   times.append(float(f.time))
   if i not in samples:continue
   im=f.to_image();im.save(frames/f'{i/FPS:06.3f}s.png');th=tile(im,f'{i/FPS:.3f}s');thumbs.append(th)
   if i in joinframes:joins.append(th)
 assert len(times)==expected and np.max(np.abs(np.diff(times)-1/FPS))<1e-5
 sheets(thumbs,'review_contact');sheets(joins,'join_contact',16)
 assert hashes=={s:sha(SB/s) for s in hashes}
 info=dict(file=final.name,sha256=sha(final),bytes=final.stat().st_size,duration_seconds=duration,video_frames=expected,fps=24,resolution=[W,H],full_decode='PASS',video_pts_steps='constant 1/24 second',audio_samples=len(pcm),audio_decoded_timeline_samples=audio_samples,audio_end_seconds=audio_end,max_audio_pts_gap_seconds=max(abs(x) for x in gaps),audio_peak=float(np.abs(pcm).max()),loudness=old.loudness(final),originals_unchanged=True,all_sfx_boundary_samples_zero=all(e['boundary_samples']==[0,0] for e in events),actual_realtime_playback_verified=False,actual_listening_verified=False)
 dump(OUT/'technical_validation.json',info);print('DONE',info['sha256'],flush=True)
if __name__=='__main__':main()
